"""Offline admission, cancellation and spending-limit checks for workflow guards."""
from _paths import ROOT, SERVER  # noqa: F401
import asyncio
import tempfile
import unittest
from pathlib import Path

from execution_guard import GuardError, GuardPolicy, guarded_events, preflight


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.agents = Path(self.tmp.name)
        (self.agents / "writer.md").write_text("Writer", encoding="utf-8")
        self.meta = {"execution_guard": {"enabled": True},
                     "contract_steps": [{"agent": "writer", "task": "Write"}]}

    def test_absent_policy_keeps_legacy(self):
        self.assertIsNone(preflight({}, self.agents, ""))

    def test_invalid_limits_fail_closed(self):
        for value in (0, -1, "nan", "inf", True, "bad"):
            with self.subTest(value=value), self.assertRaises(GuardError):
                GuardPolicy.from_meta({"execution_guard": {"enabled": True, "wall_seconds": value}})

    def test_missing_agent_rejected_before_execution(self):
        self.meta["contract_steps"][0]["agent"] = "missing"
        with self.assertRaisesRegex(GuardError, "agent_unavailable"):
            preflight(self.meta, self.agents, "")

    def test_unsafe_slug_rejected(self):
        self.meta["contract_steps"][0]["agent"] = "../writer"
        with self.assertRaisesRegex(GuardError, "slug_invalid"):
            preflight(self.meta, self.agents, "")

    def test_missing_task_card_fields_rejected(self):
        self.meta["execution_guard"]["required_input_fields"] = ["GOAL", "ENV", "ACCEPTANCE"]
        with self.assertRaisesRegex(GuardError, "input_fields_missing:ENV,ACCEPTANCE"):
            preflight(self.meta, self.agents, '{"GOAL":"repair"}')

    def test_impossible_call_budget_rejected(self):
        self.meta["execution_guard"]["max_model_stages"] = 1
        self.meta["contract_steps"].append({"agent": "writer", "task": "Review"})
        with self.assertRaisesRegex(GuardError, "minimum_calls"):
            preflight(self.meta, self.agents, "")

    def test_retry_loop_rejected(self):
        self.meta["contract_steps"][0]["max_retries"] = 100
        with self.assertRaisesRegex(GuardError, "review_retry_limit"):
            preflight(self.meta, self.agents, "")

    def test_text_only_cannot_require_shell(self):
        self.meta["supplied_data_only"] = True
        self.meta["contract_steps"][0]["required_tools"] = ["Bash"]
        with self.assertRaisesRegex(GuardError, "tools_unavailable"):
            preflight(self.meta, self.agents, "")

    def test_explicit_tool_grant_required(self):
        self.meta["contract_steps"][0]["required_tools"] = ["Bash"]
        with self.assertRaisesRegex(GuardError, "not_granted"):
            preflight(self.meta, self.agents, "", ["Read"])


class StreamTests(unittest.IsolatedAsyncioTestCase):
    async def collect(self, events, **limits):
        return [e async for e in guarded_events(events, GuardPolicy(**limits))]

    async def test_idle_timeout_cancels_waiting_provider(self):
        closed = []
        async def source():
            try:
                yield {"type": "step_start", "i": 0}
                await asyncio.sleep(10)
            finally:
                closed.append(True)
        rows = await self.collect(source(), idle_seconds=0.01)
        self.assertEqual(rows[-1]["content"], "execution_guard:idle_timeout")
        self.assertTrue(closed)
        self.assertNotIn("done", [e["type"] for e in rows])

    async def test_heartbeats_cannot_extend_wall_deadline(self):
        async def source():
            while True:
                await asyncio.sleep(0.002)
                yield {"type": "status"}
        rows = await self.collect(source(), wall_seconds=0.025, idle_seconds=1)
        self.assertEqual(rows[-1]["content"], "execution_guard:wall_timeout")

    async def test_stage_budget_stops_before_next_model(self):
        called = []
        async def source():
            yield {"type": "step_start", "i": 0}
            called.append(0)
            yield {"type": "step_start", "i": 1}
            called.append(1)
        rows = await self.collect(source(), max_model_stages=1)
        self.assertEqual(called, [0])
        self.assertEqual(rows[-1]["content"], "execution_guard:model_call_budget")

    async def test_tool_limit_closes_stream(self):
        closed = []
        async def source():
            try:
                yield {"type": "step_tool", "tool": "Read"}
                yield {"type": "step_tool", "tool": "Read"}
                self.fail("Must close before a third tool")
            finally:
                closed.append(True)
        rows = await self.collect(source(), max_tool_calls=1)
        self.assertEqual(rows[-1]["content"], "execution_guard:tool_call_budget")
        self.assertTrue(closed)

    async def test_usage_limit_stops_next_work(self):
        async def source():
            yield {"type": "step_usage", "tokens_in": 80, "tokens_out": 30}
            self.fail("Must stop after the budget")
        rows = await self.collect(source(), max_reported_tokens=100)
        self.assertEqual(rows[-1]["guard_stats"]["reported_tokens"], 110)

    async def test_missing_usage_never_invents_tokens(self):
        async def source():
            yield {"type": "step_usage", "content": "result"}
            yield {"type": "done", "result": "result"}
        rows = await self.collect(source(), max_reported_tokens=1)
        self.assertEqual(rows[-1]["type"], "done")

    async def test_broken_stream_is_error(self):
        async def source():
            yield {"type": "step_start", "i": 0}
        rows = await self.collect(source())
        self.assertEqual(rows[-1]["content"], "execution_guard:stream_ended_without_result")

    async def test_unchanged_repair_stops_before_another_review(self):
        async def source():
            yield {"type": "step_usage", "i": 0, "phase": "author", "content": "same draft"}
            yield {"type": "step_usage", "i": 0, "phase": "verify", "content": "change it"}
            yield {"type": "step_usage", "i": 0, "phase": "author", "content": "same draft"}
            self.fail("An unchanged repair must stop")
        rows = await self.collect(source())
        self.assertEqual(rows[-1]["content"], "execution_guard:no_progress_after_repair")

    async def test_provider_exception_becomes_terminal_failure(self):
        async def source():
            yield {"type": "step_start", "i": 0}
            raise RuntimeError("adapter failed")
        rows = await self.collect(source())
        self.assertEqual(rows[-1]["content"], "execution_guard:adapter_error:RuntimeError")

    async def test_nonstreamed_final_has_output_limit(self):
        async def source():
            yield {"type": "step_usage", "content": "too much output"}
            yield {"type": "done"}
        rows = await self.collect(source(), max_output_chars=3)
        self.assertEqual(rows[-1]["content"], "execution_guard:output_size_budget")


if __name__ == "__main__":
    unittest.main()
