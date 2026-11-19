"""Exercise the real workflow entry point with fake, tool-free providers."""
from _paths import ROOT, SERVER  # noqa: F401
import asyncio
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

with patch.dict(os.environ, {"JAVIS_STATE_DIR": tempfile.mkdtemp(prefix="guard-state-")}):
    import main
    import workflow_runs


class WorkflowTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="javis-guard-brain-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "workflows").mkdir()
        (self.root / "agents").mkdir()
        (self.root / "agents" / "writer.md").write_text("Writer", encoding="utf-8")
        self.store = workflow_runs.WorkflowRunStore(self.root / "runs.sqlite3")
        self.addCleanup(self.store._db.close)
        self.calls = []
        owner = self
        class Engine:
            async def query(self, prompt):
                owner.calls.append(prompt)
                yield {"type": "final", "content": "READY\nA usable draft", "tokens_in": 8, "tokens_out": 4}
        self.engine = Engine
        self.meta = {
            "name": "Guard test", "status": "active", "supplied_data_only": True,
            "execution_guard": {"enabled": True, "max_reported_tokens": 100},
            "contract_steps": [{"id": "draft", "agent": "writer", "task": "Write {{input}}",
                                "max_retries": 0, "require_first_line": "READY"}],
        }

    async def run_workflow(self):
        (self.root / "workflows" / "demo.md").write_text(
            "---\n" + yaml.safe_dump(self.meta) + "---\n", encoding="utf-8")
        helpers = (None, lambda *a: ("Writer", "system", "", ""), lambda *a: None, lambda *a: "")
        with patch.object(main, "_workflow_agent_helpers", return_value=helpers), \
                patch.object(main, "_workflow_supplied_data_engine", side_effect=lambda *a, **kw: self.engine()), \
                patch.object(main, "_agent_jobs_key", return_value=""), \
                patch.object(workflow_runs, "get_store", return_value=self.store), \
                patch.object(main, "_auto_learner"), \
                patch.object(main.system_sync, "ensure_synced"), patch.object(main.system_sync, "mirror_skills"):
            return [e async for e in main.execute_workflow(str(self.root), "demo", "brief", source="web")]

    async def test_valid_run_reaches_real_history(self):
        rows = await self.run_workflow()
        self.assertEqual(rows[-1]["type"], "done")
        self.assertEqual(len(self.calls), 1)
        usage = next(x for x in rows if x["type"] == "step_usage")
        self.assertEqual(usage["tokens_in"], 8)
        run_id = next(x["run_id"] for x in rows if x["type"] == "start")
        saved = self.store.lay(run_id)
        self.assertEqual(saved["status"], "done")

    async def test_rejection_spends_no_calls(self):
        self.meta["contract_steps"][0]["agent"] = "missing"
        rows = await self.run_workflow()
        self.assertEqual(self.calls, [])
        self.assertIn("agent_unavailable", rows[-1]["content"])

    async def test_reported_usage_stops_before_second_step(self):
        self.meta["execution_guard"]["max_reported_tokens"] = 10
        self.meta["contract_steps"].append({"agent": "writer", "task": "Review", "max_retries": 0})
        rows = await self.run_workflow()
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(rows[-1]["content"], "execution_guard:reported_token_budget")
        run_id = next(x["run_id"] for x in rows if x["type"] == "start")
        self.assertEqual(self.store.lay(run_id)["status"], "error")

    async def test_idle_provider_is_closed_and_recorded_as_failed(self):
        closed = []
        class Hanging:
            async def query(self, prompt):
                try:
                    await asyncio.sleep(10)
                    yield {"type": "final", "content": "late"}
                finally:
                    closed.append(True)
        self.engine = Hanging
        self.meta["execution_guard"]["idle_seconds"] = 0.01
        rows = await self.run_workflow()
        self.assertTrue(closed)
        self.assertEqual(rows[-1]["content"], "execution_guard:idle_timeout")
        self.assertFalse(any(x["type"] == "done" for x in rows))

    async def test_wrong_first_line_stops_before_next_step(self):
        self.meta["contract_steps"][0]["require_first_line"] = "APPROVED"
        self.meta["contract_steps"].append({"agent": "writer", "task": "Review"})
        rows = await self.run_workflow()
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(rows[-1]["content"], "execution_guard:author_output_contract_failed")

    async def test_supplied_data_rejects_declared_tools(self):
        self.meta["contract_steps"][0]["tools"] = ["Read"]
        rows = await self.run_workflow()
        self.assertEqual(self.calls, [])
        self.assertEqual(rows[-1]["content"], "execution_guard:tools_unavailable_in_supplied_data_run:0")


if __name__ == "__main__":
    unittest.main()
