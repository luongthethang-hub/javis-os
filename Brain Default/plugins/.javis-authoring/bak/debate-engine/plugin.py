"""Debate Engine - Red/Blue Team with circuit breaker and cost tracking.

Orchestrates the red-blue-team-review workflow with:
- Circuit breaker: stops after N consecutive failures
- Budget cap: tracks estimated cost per session, refuses when exceeded
- Session log: writes results to vault for audit
"""
import json
import os
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- constants ---
DEFAULT_MAX_CONSECUTIVE_FAIL = 3
DEFAULT_BUDGET_USD = 5.0
STATE_FILE = "debate_state.json"
LOG_FILE = "debate_log.jsonl"

# Rough cost estimate per workflow run (3 agents, ~4k tokens each avg)
EST_COST_PER_RUN_USD = 0.35


def _state_path(ctx):
    """State file lives in plugin's data_dir, not the vault."""
    return os.path.join(ctx.data_dir, STATE_FILE)


def _log_path(ctx):
    return os.path.join(ctx.data_dir, LOG_FILE)


def _load_state(ctx):
    path = _state_path(ctx)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "total_runs": 0,
        "total_cost_usd": 0.0,
        "consecutive_failures": 0,
        "budget_usd": DEFAULT_BUDGET_USD,
        "max_consecutive_fail": DEFAULT_MAX_CONSECUTIVE_FAIL,
        "circuit_open": False,
        "circuit_opened_at": None,
        "last_run_at": None,
    }


def _save_state(ctx, state):
    os.makedirs(ctx.data_dir, exist_ok=True)
    path = _state_path(ctx)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _append_log(ctx, entry):
    os.makedirs(ctx.data_dir, exist_ok=True)
    path = _log_path(ctx)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _now_iso():
    tz = timezone(timedelta(hours=7))
    return datetime.now(tz).isoformat(timespec="seconds")


def register(ctx):
    def handler(args, ctx):
        op = args.get("op", "run")

        # --- status: show current state ---
        if op == "status":
            state = _load_state(ctx)
            return json.dumps({
                "status": "circuit_open" if state["circuit_open"] else "ready",
                "total_runs": state["total_runs"],
                "total_cost_usd": round(state["total_cost_usd"], 4),
                "budget_usd": state["budget_usd"],
                "budget_remaining_usd": round(
                    state["budget_usd"] - state["total_cost_usd"], 4
                ),
                "consecutive_failures": state["consecutive_failures"],
                "max_consecutive_fail": state["max_consecutive_fail"],
                "last_run_at": state["last_run_at"],
            }, ensure_ascii=False)

        # --- config: adjust budget or circuit breaker threshold ---
        if op == "config":
            state = _load_state(ctx)
            if "budget_usd" in args:
                state["budget_usd"] = float(args["budget_usd"])
            if "max_consecutive_fail" in args:
                state["max_consecutive_fail"] = int(args["max_consecutive_fail"])
            _save_state(ctx, state)
            return json.dumps({
                "ok": True,
                "budget_usd": state["budget_usd"],
                "max_consecutive_fail": state["max_consecutive_fail"],
            }, ensure_ascii=False)

        # --- reset: clear circuit breaker ---
        if op == "reset":
            state = _load_state(ctx)
            state["circuit_open"] = False
            state["circuit_opened_at"] = None
            state["consecutive_failures"] = 0
            _save_state(ctx, state)
            return json.dumps({"ok": True, "message": "Circuit breaker reset"}, ensure_ascii=False)

        # --- run: trigger a debate session ---
        if op == "run":
            content = args.get("content", "").strip()
            if not content:
                return "ERROR: 'content' is required - the text to review."

            state = _load_state(ctx)

            # Circuit breaker check
            if state["circuit_open"]:
                return json.dumps({
                    "blocked": True,
                    "reason": "circuit_open",
                    "message": (
                        f"Circuit breaker OPEN since {state['circuit_opened_at']}. "
                        f"{state['consecutive_failures']} consecutive failures reached "
                        f"the limit of {state['max_consecutive_fail']}. "
                        f"Use op=reset to close the breaker after fixing the issue."
                    ),
                }, ensure_ascii=False)

            # Budget check
            remaining = state["budget_usd"] - state["total_cost_usd"]
            if remaining < EST_COST_PER_RUN_USD:
                return json.dumps({
                    "blocked": True,
                    "reason": "budget_exceeded",
                    "message": (
                        f"Budget exhausted: ${remaining:.4f} remaining, "
                        f"estimated cost per run is ${EST_COST_PER_RUN_USD}. "
                        f"Use op=config with budget_usd to increase."
                    ),
                    "total_cost_usd": round(state["total_cost_usd"], 4),
                    "budget_usd": state["budget_usd"],
                }, ensure_ascii=False)

            # All checks passed - queue the workflow via hub
            import urllib.request
            import urllib.error

            chat_id = args.get("chat_id", "")
            task_payload = {
                "title": f"Debate Engine: Red/Blue Review #{state['total_runs'] + 1}",
                "body": content,
                "route": "wf:red-blue-team-review",
                "priority": "high",
            }
            if chat_id:
                task_payload["chat_id"] = chat_id

            try:
                req = urllib.request.Request(
                    "http://127.0.0.1:7777/kanban/task",
                    data=json.dumps(task_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                # Record failure
                state["consecutive_failures"] += 1
                if state["consecutive_failures"] >= state["max_consecutive_fail"]:
                    state["circuit_open"] = True
                    state["circuit_opened_at"] = _now_iso()
                _save_state(ctx, state)
                _append_log(ctx, {
                    "ts": _now_iso(),
                    "op": "run",
                    "status": "error",
                    "error": str(e),
                    "consecutive_failures": state["consecutive_failures"],
                })
                return f"ERROR: Failed to queue workflow - {e}"

            # Success - update state
            state["total_runs"] += 1
            state["total_cost_usd"] += EST_COST_PER_RUN_USD
            state["consecutive_failures"] = 0  # reset on success
            state["last_run_at"] = _now_iso()
            _save_state(ctx, state)

            _append_log(ctx, {
                "ts": _now_iso(),
                "op": "run",
                "status": "queued",
                "run_number": state["total_runs"],
                "cost_usd": EST_COST_PER_RUN_USD,
                "total_cost_usd": round(state["total_cost_usd"], 4),
                "budget_remaining_usd": round(
                    state["budget_usd"] - state["total_cost_usd"], 4
                ),
                "task_result": result,
            })

            return json.dumps({
                "queued": True,
                "run_number": state["total_runs"],
                "task": result,
                "cost_this_run_usd": EST_COST_PER_RUN_USD,
                "total_cost_usd": round(state["total_cost_usd"], 4),
                "budget_remaining_usd": round(
                    state["budget_usd"] - state["total_cost_usd"], 4
                ),
                "circuit_breaker": "closed",
            }, ensure_ascii=False)

        # --- record_outcome: called after workflow finishes to track pass/fail ---
        if op == "record_outcome":
            verdict = args.get("verdict", "").strip().lower()
            if verdict not in ("pass", "conditional", "fail"):
                return "ERROR: 'verdict' must be 'pass', 'conditional', or 'fail'."

            actual_cost = float(args.get("actual_cost_usd", EST_COST_PER_RUN_USD))
            state = _load_state(ctx)

            # Adjust cost if actual differs from estimate
            cost_diff = actual_cost - EST_COST_PER_RUN_USD
            if abs(cost_diff) > 0.001:
                state["total_cost_usd"] += cost_diff

            if verdict == "fail":
                state["consecutive_failures"] += 1
                if state["consecutive_failures"] >= state["max_consecutive_fail"]:
                    state["circuit_open"] = True
                    state["circuit_opened_at"] = _now_iso()
            else:
                state["consecutive_failures"] = 0

            _save_state(ctx, state)
            _append_log(ctx, {
                "ts": _now_iso(),
                "op": "record_outcome",
                "verdict": verdict,
                "actual_cost_usd": actual_cost,
                "consecutive_failures": state["consecutive_failures"],
                "circuit_open": state["circuit_open"],
            })

            return json.dumps({
                "ok": True,
                "verdict": verdict,
                "consecutive_failures": state["consecutive_failures"],
                "circuit_open": state["circuit_open"],
                "total_cost_usd": round(state["total_cost_usd"], 4),
                "budget_remaining_usd": round(
                    state["budget_usd"] - state["total_cost_usd"], 4
                ),
            }, ensure_ascii=False)

        return f"ERROR: Unknown op '{op}'. Use: run, status, config, reset, record_outcome."

    ctx.register_tool(
        name="debate_engine",
        description=(
            "Red/Blue Team debate orchestrator with circuit breaker and cost tracking. "
            "ops: run {content, chat_id?} - queue a red/blue review workflow; "
            "status - show circuit breaker state and budget; "
            "config {budget_usd?, max_consecutive_fail?} - adjust limits; "
            "reset - close an open circuit breaker; "
            "record_outcome {verdict: pass|conditional|fail, actual_cost_usd?} - "
            "log the result after a run finishes to update the circuit breaker."
        ),
        handler=handler,
        min_mode="safe",
        schema={
            "type": "object",
            "properties": {
                "op": {
                    "type": "string",
                    "enum": ["run", "status", "config", "reset", "record_outcome"],
                    "description": "Operation to perform",
                },
                "content": {
                    "type": "string",
                    "description": "(run) The text/output to submit for red/blue team review",
                },
                "chat_id": {
                    "type": "string",
                    "description": "(run) Chat ID to report results back to, e.g. web:xxx",
                },
                "verdict": {
                    "type": "string",
                    "enum": ["pass", "conditional", "fail"],
                    "description": "(record_outcome) The final verdict from the debate",
                },
                "actual_cost_usd": {
                    "type": "number",
                    "description": "(record_outcome) Actual cost if different from estimate",
                },
                "budget_usd": {
                    "type": "number",
                    "description": "(config) Set the total budget in USD",
                },
                "max_consecutive_fail": {
                    "type": "integer",
                    "description": "(config) Max consecutive failures before circuit opens",
                },
            },
            "required": ["op"],
        },
    )
