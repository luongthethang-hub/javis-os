import asyncio
import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

root = Path.cwd()
sys.path.insert(0, str(root / "tests" / "python"))
os.environ["JAVIS_STATE_DIR"] = str(root.parent / "maos-06070-canary-state")
from test_execution_guard_workflow import WorkflowTests, engine, main

async def canary(status_code, expected, task):
    test = WorkflowTests()
    await test.asyncSetUp()
    calls = []
    local_text = []
    base = type("Base", (), {"system_prompt": "Follow the short instruction exactly."})()
    real_stream = engine.ollama_local_stream

    async def primary(key, model, messages, reasoning):
        calls.append(("primary", model))
        error = engine.ev_loi_http("Gemini", status_code, "synthetic overload")
        error.pop("tam_thoi", None)
        yield error

    async def local(key, model, messages, reasoning):
        calls.append(("fallback", model))
        async for event in real_stream(key, model, messages, reasoning):
            if event.get("type") in ("text", "final"):
                local_text.append(event.get("content"))
            yield event

    try:
        test.meta["execution_guard"].update(
            idle_seconds=50, wall_seconds=60,
            max_reported_tokens=1500, max_model_stages=2,
        )
        step = test.meta["contract_steps"][0]
        step["task"] = task
        step["require_first_line"] = expected
        test.add_fallback(model="deepseek-r1:1.5b")
        test.factory = main._workflow_supplied_data_engine
        started = time.monotonic()
        with patch.object(main.aux_engine, "availability", return_value=(True, "")), \
                patch.object(main.aux_engine, "api_key_for", return_value="synthetic-key"), \
                patch.object(main.aux_engine._ApiAuxEngine, "_ghi_muc_dung"), \
                patch.object(main, "_reply_policy_sandbox_engine", return_value=base), \
                patch.object(engine, "gemini_stream", side_effect=primary), \
                patch.object(engine, "ollama_local_stream", side_effect=local), \
                patch.object(engine, "ollama_local_url", return_value="http://127.0.0.1:11434/v1/chat/completions"), \
                patch("mcp_hub.discover_all", side_effect=AssertionError("unexpected tool discovery")):
            rows = await test.run_workflow()
        run_id = next((e["run_id"] for e in rows if e["type"] == "start"), "")
        status = test.store.lay(run_id)["status"] if run_id else None
        switches = [e["status_code"] for e in rows if e["type"] == "step_fallback"]
        summary = {
            "expected": expected,
            "seconds": round(time.monotonic() - started, 2),
            "calls": calls,
            "switches": switches,
            "status": status,
            "usage": [(e["tokens_in"], e["tokens_out"]) for e in rows if e["type"] == "step_usage"],
            "terminal": rows[-1],
            "local_text": "".join(t or "" for t in local_text),
        }
        print(json.dumps(summary, ensure_ascii=True), flush=True)
        return (status == "done" and rows[-1].get("result", "").strip() == expected
                and switches == [status_code] and len(calls) == 2)
    finally:
        test.store._db.close()
        test.tmp.cleanup()

async def main_cases():
    cases = [
        (503, "READY", "Copy the next line verbatim. Preserve uppercase letters and give only the copied line.\nREADY"),
        (429, "17", "The shipment has exactly 17 boxes. How many boxes? Reply with the number only."),
        (503, "AB-24", "The reference number is AB-24. Return only the reference number, exactly as written."),
    ]
    results = []
    for args in cases:
        results.append(await canary(*args))
    return all(results)

raise SystemExit(0 if asyncio.run(main_cases()) else 1)


