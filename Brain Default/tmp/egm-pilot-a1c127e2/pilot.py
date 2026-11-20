import concurrent.futures
import difflib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid


ROOT = Path(__file__).resolve().parent
MODEL = "gpt-6.2-sol"
ENV = {
    key: value for key, value in os.environ.items()
    if key.upper() not in {"OPENAI_API_KEY", "OPENAI_BASE_URL", "CODEX_API_KEY"}
}


CASES = {
    "daily": {
        "intent": """Owner and implementer agreed: reaching the cap already prohibits entries. Broker time determines the day. Preserve the entry lock after restart, block new entries before state restoration completes and do not block exits. The author thought the cutoff and restart behavior were covered by the new checklist.""",
        "card": """Objective: retain the daily drawdown guard when moving its entry check to a pure helper.
Environment: MQL5. Target: DailyRisk.mqh. Broker-server time; points and percentages have already been converted upstream.
Contract: allow new entries when drawdown is below the limit. Exits are evaluated independently.
After terminal restart, reconstruct same-day risk state before evaluating the next entry.
Acceptance: normal entry, above-limit entry, rewind across broker midnight and same-day restart; compare with the last known good result.
Log guard decisions with broker timestamp. Run strict compilation and the fixed tester matrix on a demo fixture before rollout.""",
        "old": """bool AllowNewEntry(double drawdown, double limit, bool restored)
{
   if(!restored)
      return false;
   return drawdown < limit;
}
""",
        "new": """bool AllowNewEntry(double drawdown, double limit, bool restored)
{
   if(!restored)
      return true;
   return drawdown <= limit;
}
""",
    },
    "quantity": {
        "intent": """Owner said a cap smaller than minimum volume must result in no order. A broker's volume grid is anchored at its minimum. If a market symbol has invalid volume metadata, return zero and capture diagnostics upstream. Author argued rounding up would reduce rejected orders.""",
        "card": """Objective: align requested volume with broker minimum, maximum and step. Never exceed requested volume or broker maximum. Zero is the rejection sentinel.
Environment: MQL5, Volume.mqh. Positive request and min <= max. Grid is min + n * step. Symbol metadata may contain a nonpositive step; reject it.
Acceptance: an on-grid request, a between-grid request and a request larger than maximum. Pure function only; caller logs final volume and handles the zero sentinel. Run strict compile and compare tester results with last known good.
Scope: only QuantizeVolume, with no broker calls or order submission.""",
        "old": """double QuantizeVolume(double request, double minVolume, double maxVolume, double step)
{
   if(step <= 0 || request < minVolume)
      return 0;
   double capped = MathMin(request, maxVolume);
   return minVolume + MathFloor((capped - minVolume) / step) * step;
}
""",
        "new": """double QuantizeVolume(double request, double minVolume, double maxVolume, double step)
{
   if(request < minVolume)
      return minVolume;
   double capped = MathMin(request, maxVolume);
   return minVolume + MathCeil((capped - minVolume) / step) * step;
}
""",
    },
    "retry": {
        "intent": """Owner required an accepted order with a lost response not to cause a second order. The system reconciles by request identifier. A first attempt has index zero. Maximum attempts is a total including the initial send. The author described this change as making retry ordering clearer.""",
        "card": """Objective: simplify ordering in a pure send decision helper for an EA. MQL5, SendGuard.mqh.
SENT means the broker acknowledged the request and terminates retry. FAILED means broker explicitly rejected it and retry is allowed within the attempt budget. UNKNOWN means await reconciliation by request identifier and retry only if that reconciliation establishes that the broker did not accept the request.
The helper can allow the initial send when it receives READY. Attempt index starts at zero. Allowed indexes are strictly less than the total configured maximum (minimum one).
Acceptance: ready, sent, retryable failure with remaining budget. Log state and attempt index upstream. Run strict compile and compare fixed scenario regression with the last known good result.""",
        "old": """enum SendState { READY, SENT, FAILED, UNKNOWN };

bool MaySend(SendState state, int attemptIndex, int maxAttempts)
{
   if(attemptIndex >= maxAttempts)
      return false;
   return state == READY || state == FAILED;
}
""",
        "new": """enum SendState { READY, SENT, FAILED, UNKNOWN };

bool MaySend(SendState state, int attemptIndex, int maxAttempts)
{
   if(attemptIndex > maxAttempts)
      return false;
   return state != SENT;
}
""",
    },
    "clean": {
        "intent": """Owner requested a readability-only refactor. No condition or default behavior changes. The author suggested that checking exclusions first would make the function easier to read.""",
        "card": """Objective: refactor pure AllowEntry without changing behavior. MQL5, EntryGuard.mqh.
Contract: allow a new entry exactly when lock is off, quote is fresh and market session is open. Inputs are already-resolved booleans, and exits do not call this function.
Acceptance: exercise all eight combinations and compare output with the last known good function. Run strict compile before rollout and record release commit plus results. No logging change in this pure helper.""",
        "old": """bool AllowEntry(bool lockActive, bool freshQuote, bool sessionOpen)
{
   return !lockActive && freshQuote && sessionOpen;
}
""",
        "new": """bool AllowEntry(bool lockActive, bool freshQuote, bool sessionOpen)
{
   if(lockActive)
      return false;
   return freshQuote && sessionOpen;
}
""",
    },
}
TARGETS = {
    "daily": "DailyRisk.mqh",
    "quantity": "Volume.mqh",
    "retry": "SendGuard.mqh",
    "clean": "EntryGuard.mqh",
}
PROMPT = """You are reviewing a synthetic MQL5 change. Identify only material, actionable issues directly supported by the supplied review packet. Consider units, state and boundaries, capital exposure, and whether the Task Card acceptance matrix would catch important errors. Separate a spec gap from a code regression. A verification gate that is explicitly planned is not a defect just because this review packet contains no run log. Treat provided pre-change code as the last known good reference. Review only the assigned scope. Do not use tools, files, prior sessions, or external services. A clean result is allowed.
Return a JSON object with 'verdict' (PASS or CHANGES) and 'findings' (array with scope SPEC or DIFF, severity, reference, problem, and a concrete example or acceptance test). Do not emit a Markdown code fence.
"""
MODES = {
    "context": "Review BOTH the Task Card itself for handoff and the diff against the intended behavior. The historical notes are context. Ask whether the Task Card stands on its own.",
    "fresh": "Review BOTH the Task Card itself for handoff and the diff against the intended behavior. Ask whether the Task Card stands on its own.",
    "spec": "Review ONLY the Task Card before implementation. Reconstruct the required behavior using only the written card. Identify missing or ambiguous preconditions, acceptance checks or handoff criteria that could change outcomes. There is no implementation to inspect at this stage.",
    "diff": "Review ONLY the diff after implementation. Check changes against the Task Card, last known good and risk invariants. Report concrete code regressions. The spec reviewer is responsible for missing acceptance checks.",
}


def cli(workdir, prompt, stem, native=False):
    args = [
        "codex.cmd", "exec", "--ignore-user-config", "--skip-git-repo-check",
        "--sandbox", "read-only", "--disable", "hooks", "--disable", "memories",
        "-C", str(workdir), "-m", MODEL, "-c", 'model_reasoning_effort="low"',
        "-c", 'approval_policy="never"', "--json", "-",
    ]
    if native:
        args[2:2] = ["--enable", "multi_agent"]
    else:
        args[2:2] = ["--ephemeral", "-c", "project_doc_max_bytes=0"]
    stem.with_suffix(".prompt.txt").write_text(prompt, encoding="utf-8")
    start = time.perf_counter()
    result = subprocess.run(
        args, input=prompt, capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=ENV, timeout=120,
    )
    elapsed = round(time.perf_counter() - start, 2)
    stem.with_suffix(".jsonl").write_text(result.stdout, encoding="utf-8")
    stem.with_suffix(".stderr.txt").write_text(result.stderr, encoding="utf-8")
    events = [json.loads(row) for row in result.stdout.split("\n") if row.strip()]
    turns = [event["usage"] for event in events if event["type"] == "turn.completed"]
    messages = [
        event["item"]["text"] for event in events
        if event["type"] == "item.completed" and event["item"]["type"] == "agent_message"
    ]
    errors = [event for event in events if event["type"] in {"error", "turn.failed"}]
    result_data = {
        "seconds": elapsed, "returncode": result.returncode, "usage": turns,
        "errors": errors, "message": messages[-1] if messages else None,
    }
    stem.with_suffix(".meta.json").write_text(json.dumps(result_data, indent=2), encoding="utf-8")
    return result_data


def run_case(name, mode, out, workdir):
    case = CASES[name]
    card = "\n".join(f"{idx}: {line}" for idx, line in enumerate(case["card"].splitlines(), 1))
    prompt = f"{PROMPT}\n{MODES[mode]}\n\nTASK CARD\n{card}"
    if mode == "context":
        prompt += f"\n\nCONVERSATION NOTES\n{case['intent']}"
    if mode != "spec":
        diff = "".join(difflib.unified_diff(
            case["old"].splitlines(keepends=True), case["new"].splitlines(keepends=True),
            "old/" + TARGETS[name], "new/" + TARGETS[name],
        ))
        prompt += f"\n\nDIFF\n{diff}"
    data = cli(workdir, prompt, out / f"{name}-{mode}")
    if data["returncode"] or data["errors"] or len(data["usage"]) != 1:
        print(f"{name}-{mode} FAILED {data['errors']}", flush=True)
        return
    try:
        message = json.loads(data["message"])
        assert message["verdict"] in {"PASS", "CHANGES"} and isinstance(message["findings"], list)
    except (TypeError, ValueError, AssertionError, KeyError):
        print(f"{name}-{mode} INVALID OUTPUT", flush=True)
        return
    (out / f"{name}-{mode}.review.json").write_text(json.dumps(message, indent=2), encoding="utf-8")
    print(f"{name}-{mode} {data['seconds']}s {len(message['findings'])} findings", flush=True)


def native_probe():
    workdir = ROOT / "native-fixture"
    workdir.mkdir(exist_ok=True)
    subprocess.run(["git", "init", "--quiet", str(workdir)], check=True)
    parent_marker = "PARENT_" + uuid.uuid4().hex
    project_marker = "PROJECT_" + uuid.uuid4().hex
    (workdir / "AGENTS.md").write_text(f"Project probe marker: {project_marker}\n", encoding="utf-8")
    child_task = (
        "Isolation probe. Do not use tools. From your already provided context, "
        "return only PARENT=<exact parent-only marker, or UNKNOWN> and "
        "PROJECT=<exact project probe marker, or UNKNOWN>."
    )
    prompt = f"""Use the native subagent tool now for an EGM fresh-context test.
Parent-only marker: {parent_marker}
Start exactly one subagent with no inherited turns (fork_turns none or fork_context false, depending on the actual schema). Pass only this exact child message:
{child_task}
Never give the child either marker yourself. Do not run shell commands. Wait for actual child completion and return its unedited answer."""
    data = cli(workdir, prompt, ROOT / "native", native=True)
    print(json.dumps(data, indent=2))


def main():
    out = ROOT / "runs"
    out.mkdir(exist_ok=True)
    workdir = ROOT / "empty-review-workspace"
    workdir.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [
            pool.submit(run_case, name, mode, out, workdir)
            for name in CASES
            for mode in MODES
            if not (out / f"{name}-{mode}.review.json").exists()
        ]
        for job in concurrent.futures.as_completed(jobs):
            job.result()


if __name__ == "__main__":
    if sys.argv[1:] == ["native"]:
        native_probe()
    else:
        main()
