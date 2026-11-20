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
    import engine
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
        self.agent_routes = {}
        owner = self
        class Engine:
            async def query(self, prompt):
                owner.calls.append(prompt)
                yield {"type": "final", "content": "READY\nA usable draft", "tokens_in": 8, "tokens_out": 4}
        self.engine = Engine
        self.factory = lambda *a, **kw: self.engine()
        self.meta = {
            "name": "Guard test", "status": "active", "supplied_data_only": True,
            "execution_guard": {"enabled": True, "max_reported_tokens": 100},
            "contract_steps": [{"id": "draft", "agent": "writer", "task": "Write {{input}}",
                                "max_retries": 0, "require_first_line": "READY"}],
        }

    def add_fallback(self, index=0, **overrides):
        route = {"provider": "ollama-local", "model": "local-draft"}
        route.update(overrides)
        self.meta["contract_steps"][index]["author_fallback"] = route
        self.agent_routes["writer"] = ("main-draft", "gemini")

    def script(self, *responses):
        pending = iter(responses)
        calls = self.calls

        def factory(system, model, provider, **kwargs):
            class Scripted:
                async def query(self, prompt):
                    calls.append((provider, model, prompt))
                    for event in next(pending):
                        yield event

            return Scripted()

        self.factory = factory

    @staticmethod
    def answer(text="READY\nDraft"):
        return {"type": "final", "content": text}

    @staticmethod
    def failure(code):
        return {"type": "error", "ma": code, "content": f"Provider error {code}"}

    async def run_workflow(self):
        (self.root / "workflows" / "demo.md").write_text(
            "---\n" + yaml.safe_dump(self.meta) + "---\n", encoding="utf-8")
        def agent(slug, *args):
            return slug.title(), "system", *self.agent_routes.get(slug, ("", ""))

        helpers = (None, agent, lambda *a: None, lambda *a: "")
        with patch.object(main, "_workflow_agent_helpers", return_value=helpers), \
                patch.object(main, "_workflow_supplied_data_engine", side_effect=self.factory), \
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

    async def test_middle_step_503_uses_previous_output_and_verifier(self):
        self.meta["contract_steps"] += [
            {"agent": "writer", "task": "Expand {{prev}}", "verify_agent": "reviewer", "max_retries": 0},
            {"agent": "writer", "task": "Finish {{prev}}"},
        ]
        (self.root / "agents" / "reviewer.md").write_text("Reviewer", encoding="utf-8")
        self.agent_routes["reviewer"] = ("review-model", "openai")
        self.add_fallback(1)
        self.script([self.answer("READY\nFirst")], [self.failure(503)], [self.answer("Recovered")],
                    [self.answer('{"pass":true}')], [self.answer("Finished")])
        rows = await self.run_workflow()
        self.assertEqual(self.calls[:3], [
            ("gemini", "main-draft", "Write brief"),
            ("gemini", "main-draft", "Expand READY\nFirst"),
            ("ollama-local", "local-draft", "Expand READY\nFirst"),
        ])
        self.assertEqual(self.calls[3][:2], ("openai", "review-model"))
        self.assertIn("Recovered", self.calls[3][2])
        self.assertEqual(self.calls[4], ("gemini", "main-draft", "Finish Recovered"))
        self.assertEqual(rows[-1], {"type": "done", "result": "Finished"})
        self.assertEqual([e["i"] for e in rows if e["type"] == "step_done"], [0, 1, 2])
        self.assertEqual([e["status_code"] for e in rows if e["type"] == "step_fallback"], [503])
        self.assertFalse(any(e["type"] == "step_error" for e in rows))
        run_id = next(e["run_id"] for e in rows if e["type"] == "start")
        self.assertEqual(self.store.lay(run_id)["status"], "done")

    async def test_real_api_adapters_close_primary_and_count_usage(self):
        self.add_fallback()
        self.factory = main._workflow_supplied_data_engine
        closed = []

        async def primary(key, model, messages, reasoning):
            self.calls.append((model, messages))
            try:
                yield {"type": "usage", "input": 6, "output": 1}
                error = {**engine.ev_loi_http("Gemini", 429, "busy"), "da_thu": 3}
                error.pop("tam_thoi", None)
                yield error
            finally:
                closed.append("primary")

        async def fallback(key, model, messages, reasoning):
            self.assertEqual(closed, ["primary"])
            self.calls.append((model, messages))
            yield {"type": "text", "content": "\n\nREADY\nRecovered"}
            yield {"type": "usage", "input": 9, "output": 2}

        base = type("Base", (), {"system_prompt": "system"})()
        with patch.object(main.aux_engine, "availability", return_value=(True, "")), \
                patch.object(main.aux_engine, "api_key_for", return_value="test-only"), \
                patch.object(main.aux_engine._ApiAuxEngine, "_ghi_muc_dung"), \
                patch.object(main, "_reply_policy_sandbox_engine", return_value=base), \
                patch.object(engine, "gemini_stream", side_effect=primary), \
                patch.object(engine, "ollama_local_stream", side_effect=fallback), \
                patch("mcp_hub.discover_all", side_effect=AssertionError("unexpected tool discovery")) as discover:
            rows = await self.run_workflow()
        discover.assert_not_called()
        self.assertEqual([call[0] for call in self.calls], ["main-draft", "local-draft"])
        for _, messages in self.calls:
            self.assertEqual(messages[0], {"role": "system", "content": "system"})
        self.assertEqual(self.calls[0][1][-1], self.calls[1][1][-1])
        self.assertEqual([(e["tokens_in"], e["tokens_out"]) for e in rows if e["type"] == "step_usage"],
                         [(6, 1), (9, 2), (0, 0)])
        self.assertEqual(rows[-1], {"type": "done", "result": "\n\nREADY\nRecovered"})

    async def test_unsafe_or_unsupported_failure_never_switches(self):
        self.add_fallback()
        for events in (
            [self.failure(400)], [self.failure(401)], [self.failure(403)],
            [{"type": "error", "content": "503 in text only"}],
            [{**self.failure(503), "resume_failed": True}],
            [{"type": "text", "content": "Visible text"}, self.failure(503)],
            [self.answer(), self.failure(503)],
            [{"type": "tool_call", "name": "send"}, self.failure(503)],
        ):
            with self.subTest(events=events):
                self.calls.clear()
                self.script(events)
                rows = await self.run_workflow()
                self.assertEqual(len(self.calls), 1)
                self.assertEqual(rows[-1]["type"], "error")
                self.assertFalse(any(e["type"] == "step_fallback" for e in rows))

    async def test_disabled_fallback_keeps_original_error(self):
        self.script([self.failure(503)])
        rows = await self.run_workflow()
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(rows[-1]["content"], "Provider error 503")

    async def test_invalid_configuration_spends_no_calls(self):
        for route, reason in (
            ({"provider": "unknown"}, "fallback_route_invalid"),
            ({"model": " "}, "fallback_route_invalid"),
            ({"provider": ["openai"]}, "fallback_route_invalid"),
            ({"provider": "gemini"}, "fallback_provider_matches_primary"),
        ):
            with self.subTest(route=route):
                self.add_fallback(**route)
                rows = await self.run_workflow()
                self.assertEqual(self.calls, [])
                self.assertIn(reason, rows[-1]["content"])
        self.add_fallback()
        self.meta["supplied_data_only"] = False
        rows = await self.run_workflow()
        self.assertEqual(self.calls, [])
        self.assertIn("fallback_requires_supplied_data_only", rows[-1]["content"])

    async def test_no_second_switch_in_same_run(self):
        self.meta["contract_steps"].append({"agent": "writer", "task": "Then {{prev}}"})
        self.add_fallback(0)
        self.add_fallback(1)
        self.script([self.failure(503)], [self.answer()], [self.failure(429)])
        rows = await self.run_workflow()
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(sum(e["type"] == "step_fallback" for e in rows), 1)
        self.assertEqual(rows[-1]["type"], "error")

    async def test_fallback_failure_or_bad_output_cannot_finish_step(self):
        self.add_fallback()
        self.meta["contract_steps"].append({"agent": "writer", "task": "Then {{prev}}"})
        for fallback_reply in (self.failure(503), self.answer("Bad contract")):
            with self.subTest(fallback_reply=fallback_reply):
                self.calls.clear()
                self.script([self.failure(429)], [fallback_reply])
                rows = await self.run_workflow()
                self.assertEqual(len(self.calls), 2)
                self.assertEqual(rows[-1]["type"], "error")
                self.assertFalse(any(e["type"] == "step_done" for e in rows))

    async def test_verifier_can_reject_the_fallback_output(self):
        self.add_fallback()
        self.meta["contract_steps"][0]["verify_agent"] = "reviewer"
        self.meta["contract_steps"].append({"agent": "writer", "task": "Then {{prev}}"})
        (self.root / "agents" / "reviewer.md").write_text("Reviewer", encoding="utf-8")
        self.agent_routes["reviewer"] = ("review-model", "openai")
        self.script([self.failure(503)], [self.answer()], [self.answer('{"pass":false,"reason":"Wrong"}')])
        rows = await self.run_workflow()
        self.assertEqual([provider for provider, _, _ in self.calls], ["gemini", "ollama-local", "openai"])
        self.assertEqual(rows[-1]["type"], "error")
        self.assertFalse(any(e["type"] == "step_done" for e in rows))

    async def test_fallback_admission_counts_stage_and_provider_usage(self):
        self.add_fallback()
        for limit, reason, first_response in (
            ("max_model_stages", "model_call_budget", [self.failure(503)]),
            ("max_reported_tokens", "reported_token_budget",
             [{"type": "usage", "input": 1, "output": 0}, self.failure(503)]),
        ):
            with self.subTest(limit=limit):
                self.calls.clear()
                self.meta["execution_guard"][limit] = 1
                self.script(first_response)
                rows = await self.run_workflow()
                del self.meta["execution_guard"][limit]
                self.assertEqual(len(self.calls), 1)
                self.assertEqual(rows[-1]["content"], "execution_guard:" + reason)

    async def test_cancel_during_fallback_closes_stream_and_marks_history_failed(self):
        self.add_fallback()
        started = asyncio.Event()
        closed = asyncio.Event()

        class Primary:
            async def query(self, prompt):
                yield WorkflowTests.failure(503)

        class Fallback:
            async def query(self, prompt):
                started.set()
                try:
                    await asyncio.sleep(60)
                    yield WorkflowTests.answer()
                finally:
                    closed.set()

        self.factory = lambda system, model, provider, **kw: (
            Primary() if provider == "gemini" else Fallback())
        task = asyncio.create_task(self.run_workflow())
        await asyncio.wait_for(started.wait(), timeout=3)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(closed.is_set())
        states = self.store.gan_nhat(main._brain_key(str(self.root)), slug="demo")
        self.assertEqual([state["status"] for state in states], ["error"])


if __name__ == "__main__":
    unittest.main()
