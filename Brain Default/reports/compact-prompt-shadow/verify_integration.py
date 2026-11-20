"""Paired Codex app-server replay. All callable handlers are synthetic."""

import argparse
import asyncio
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

from run_shadow import FACTS, PROFILE, ROOT, fixture_readonly_grants, fixture_tools, make_baseline
from compact_prompt import preview
import mcp_client
import mcp_hub
from subscription_usage import CodexUsage


READ_NAME = "javis_schedule"
STALE_TIME = "17:37"
FRESH_TIME = "19:42"
MARKER = "SEN-908"
SCHEDULE = "21:00"


class ScopedSchedule:
    def __init__(self, handler=None):
        self.executed = 0
        self.denied = 0
        self.handler = handler or self.fake_handler
        self.granted = True

    async def fake_handler(self, args):
        return f"Synthetic schedule: report {MARKER}, enabled, {SCHEDULE}."

    async def dispatch(self, name, args):
        # Existing hub scoping removes both the write route and the lazy dispatcher. Independently
        # validate the operation at invocation time, before the selected handler sees arguments.
        if not self.granted or name != READ_NAME or not isinstance(args, dict) or args != {"op": "list"}:
            self.denied += 1
            return "ERROR: fixture route only grants javis_schedule op=list"
        self.executed += 1
        return await mcp_client.call_route({READ_NAME: {"call": self.handler}}, name, args)


async def verify_dispatch():
    guarded = ScopedSchedule()
    escalations = []

    async def must_not_run(args):
        escalations.append(args)
        return "ERROR: unexpected dispatch"

    full = {READ_NAME: {"call": lambda args: guarded.dispatch(READ_NAME, args)},
            **{name: {"call": must_not_run} for name in ("send_message", "javis_run_tool", "javis_search_tools")}}
    tools, route = mcp_hub._scope_tools([{"fn": key} for key in full], full, (READ_NAME,))
    assert [t["fn"] for t in tools] == [READ_NAME] and list(route) == [READ_NAME]
    cases = ((READ_NAME, {"op": "list"}, True), (READ_NAME, {"op": "cancel"}, False),
             (READ_NAME, {"op": "create"}, False), (READ_NAME, {}, False),
             (READ_NAME, {"op": "list", "override": "cancel"}, False),
             (READ_NAME, ["list"], False), ("send_message", {}, False),
             ("javis_run_tool", {"name": READ_NAME, "args": {"op": "cancel"}}, False),
             ("javis_search_tools", {"query": "cancel"}, False))
    for name, args, allowed in cases:
        result = await mcp_client.call_route(route, name, args)
        assert (not result.startswith("ERROR:")) == allowed, (name, args, result)
    guarded.granted = False
    assert (await mcp_client.call_route(route, READ_NAME, {"op": "list"})).startswith("ERROR:")
    assert guarded.executed == 1 and not escalations
    return {"cases": len(cases) + 1, "executed": guarded.executed, "denied": len(cases)}


async def verify_schedule_plugin():
    plugin_file = ROOT / "system" / "plugins" / "javis-schedule" / "plugin.py"
    plugin = runpy.run_path(str(plugin_file))
    options = {}
    plugin["register"](SimpleNamespace(register_tool=lambda **kwargs: options.update(kwargs)))
    assert options["min_mode"] == "safe"
    assert set(options["schema"]["properties"]["op"]["enum"]) == {"create", "list", "update", "cancel"}
    handler = options["handler"]
    ctx = SimpleNamespace(vault_root="fixture-brain")
    calls = []

    async def stub_write(*args):
        calls.append("write_stub")
        return "SYNTHETIC WRITE BRANCH"

    def loops(brain):
        assert brain == ctx.vault_root
        calls.append("loops")
        return [{"id": "fixture-loop", "name": "Fixture loop", "enabled": True, "interval_min": 60, "mode": "suggest"}]

    async def reminders(brain):
        assert brain == ctx.vault_root
        calls.append("reminders")
        return {"pending": [{"id": "fixture-reminder", "label": "Fixture reminder", "due_human": SCHEDULE}]}

    def invoke(args):
        return handler(args, ctx)

    with patch.dict(handler.__globals__, {"_do_create": stub_write, "_do_update": stub_write,
                                         "_do_cancel": stub_write, "_list_loops": loops,
                                         "_get_reminders": reminders}):
        # Model-free control: the current raw dispatcher picks create when op is absent.
        assert await invoke({}) == "SYNTHETIC WRITE BRANCH"
        assert calls == ["write_stub"]
        calls.clear()
        guard = ScopedSchedule(invoke)
        result = await guard.dispatch(READ_NAME, {"op": "list"})
        assert "fixture-loop" in result and "fixture-reminder" in result
        for args in ({}, {"op": "create"}, {"op": "update"}, {"op": "cancel"}):
            assert (await guard.dispatch(READ_NAME, args)).startswith("ERROR:")
        assert calls == ["loops", "reminders"] and guard.executed == 1 and guard.denied == 4
    return {"listed_both_stores": True, "raw_missing_op": "create", "guarded_write_branches_reached": 0}


class AppServer:
    def __init__(self, cli, cwd, model):
        self.cli, self.cwd, self.model = cli, str(cwd), model
        self.next_id = 0
        self.tool = ScopedSchedule()
        self.rpcs_denied = 0
        self.proc = None
        self.events = []

    async def __aenter__(self):
        env_options = ["-c", "project_doc_max_bytes=0", "-c", 'web_search="disabled"',
                       "-c", 'mcp_servers.cua_repl={command="cmd.exe",args=["/c","exit"],enabled=false}',
                       "-c", 'mcp_servers.node_repl={command="cmd.exe",args=["/c","exit"],enabled=false}',
                       "--disable", "apps", "--disable", "shell_tool",
                       "--disable", "plugins", "--disable", "remote_plugin", "--disable", "multi_agent"]
        self.proc = await asyncio.create_subprocess_exec(
            self.cli, *env_options, "app-server", cwd=self.cwd,
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=subprocess.DEVNULL,
            limit=8 * 1024 * 1024, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        try:
            await self.request("initialize", {"clientInfo": {"name": "javis_shadow", "version": "1.0"},
                                               "capabilities": {"experimentalApi": True}})
            await self.send({"method": "initialized", "params": {}})
            status = await self.request("mcpServerStatus/list", {})
            config = (await self.request("config/read", {"includeLayers": False})).get("config", {})
            configured = config.get("mcp_servers", {})
            disabled = {name for name, entry in configured.items() if entry.get("enabled") is False}
            entries = status.get("data")
            if (not isinstance(entries, list) or status.get("nextCursor") or set(configured) != disabled
                or any(entry.get("name") not in disabled or entry.get("tools") or entry.get("resources")
                       or entry.get("resourceTemplates") for entry in entries)):
                raise RuntimeError("Shadow requires all native MCP servers disabled with no exposed tools or resources")
            return self
        except BaseException:
            await self.__aexit__()
            raise

    async def __aexit__(self, *_):
        if self.proc and self.proc.returncode is None:
            self.proc.stdin.close()
            try:
                await asyncio.wait_for(self.proc.wait(), 5)
            except TimeoutError:
                self.proc.kill()
                await self.proc.wait()

    async def send(self, obj):
        self.proc.stdin.write((json.dumps(obj, ensure_ascii=False) + "\n").encode())
        await self.proc.stdin.drain()

    async def receive(self):
        while True:
            line = await self.proc.stdout.readline()
            if not line:
                raise RuntimeError("Codex app-server closed its output")
            msg = json.loads(line)
            if "id" not in msg or "method" not in msg:
                return msg
            if msg["method"] == "item/tool/call":
                params = msg.get("params", {})
                result = await self.tool.dispatch(params.get("tool"), params.get("arguments"))
                await self.send({"id": msg["id"], "result": {"success": not result.startswith("ERROR:"),
                                 "contentItems": [{"type": "inputText", "text": result}]}})
            else:
                self.rpcs_denied += 1
                await self.send({"id": msg["id"], "error": {"code": -32000, "message": "Denied in shadow"}})

    async def request(self, method, params):
        self.next_id += 1
        rid = self.next_id
        await self.send({"id": rid, "method": method, "params": params})
        async with asyncio.timeout(35):
            while True:
                msg = await self.receive()
                if msg.get("id") == rid:
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error'].get('message', '')[:240]}")
                    return msg.get("result", {})
                self.events.append(msg)

    def thread_options(self):
        return {"model": self.model, "cwd": self.cwd, "sandbox": "read-only", "approvalPolicy": "never"}

    async def start(self, instructions, schema):
        result = await self.request("thread/start", {**self.thread_options(), "ephemeral": False,
                                    "developerInstructions": instructions,
                                    "dynamicTools": [{"name": READ_NAME, "description": "List the synthetic schedule.",
                                                      "inputSchema": schema}]})
        return result["thread"]["id"]

    async def resume(self, tid):
        response = await self.request("thread/resume", {**self.thread_options(), "threadId": tid, "excludeTurns": True})
        assert response["thread"]["id"] == tid

    async def turn(self, tid, question, previous):
        scoped = {"threadId": tid, "input": [{"type": "text", "text": question}], "effort": "low"}
        result = await self.request("turn/start", scoped)
        turn_id = result["turn"]["id"]
        usage, answer = CodexUsage(previous), []
        async with asyncio.timeout(75):
            while True:
                msg = self.events.pop(0) if self.events else await self.receive()
                mt, params = msg.get("method"), msg.get("params", {})
                if params.get("threadId") != tid:
                    continue
                if mt == "thread/tokenUsage/updated" and params.get("turnId") == turn_id:
                    usage.observe(params["tokenUsage"])
                elif mt == "item/completed" and params.get("turnId") == turn_id:
                    item = params.get("item", {})
                    if item.get("type") == "agentMessage" and item.get("text"):
                        answer.append(item["text"])
                elif mt == "turn/completed" and params.get("turn", {}).get("id") == turn_id:
                    turn = params["turn"]
                    if turn["status"] != "completed":
                        raise RuntimeError(f"Codex turn: {turn['status']} {turn.get('error')}")
                    return {"answer": "\n".join(answer), **usage.summary()}, usage.previous


async def pair(cli, model, scratch, compact_first):
    grants = fixture_tools()
    read = fixture_readonly_grants(grants)
    baseline = make_baseline()
    candidate = preview(baseline=baseline, granted=grants, readonly_grants=read,
                        intents=("schedule_read",), facts=FACTS, risk="readonly", policy_complete=True,
                        profile=PROFILE)
    assert candidate.route == "compact"
    assert candidate.tools == (read[READ_NAME],)
    # Equal constraints across arms. Keep a stable prefix in one thread, and present authoritative
    # turn facts separately on every turn. A follow-up turn must use thread evidence without re-querying.
    contract = ("\n\nFor this isolated Vietnamese test all tools and results are synthetic. "
                "Use the supplied Gateway turn facts for current time. A question about the prior result or an "
                "earlier decision uses the conversation evidence and never triggers a new lookup. "
                "Include the synthetic starter marker RULE-715 only when asked for that marker.")
    questions = (
        FACTS + "\nDùng công cụ javis_schedule với op=list rồi cho mình biết mã báo cáo và giờ chạy. Trong hội thoại này, mình chọn kênh Telegram.",
        FACTS + "\nMình vừa chọn kênh nào, báo cáo mã gì và chạy lúc mấy giờ? Nhắc lại kết quả vừa có.",
        FACTS.replace(STALE_TIME, FRESH_TIME) + "\nNối tiếp: nhắc lại mã báo cáo, giờ chạy, kênh đã chọn, giờ hiện tại trong Gateway turn facts và mã quy tắc thử nghiệm ghi ở đầu phiên.",
    )
    schema = read[READ_NAME]["parameters"]
    output = {}
    arms = [("baseline", baseline), ("compact", candidate.instructions)]
    if compact_first:
        arms.reverse()
    for name, instructions in arms:
        cwd = scratch / name
        cwd.mkdir()
        empty_usage = {"input": 0, "cache": 0, "output": 0}
        async with AppServer(cli, cwd, model) as app:
            tid = await app.start(instructions + contract, schema)
            first, previous = await app.turn(tid, questions[0], empty_usage)
            warm, previous = await app.turn(tid, questions[1], previous)
            tool_calls = app.tool.executed
            denials = app.tool.denied + app.rpcs_denied
        async with AppServer(cli, cwd, model) as app:
            await app.resume(tid)
            cold, _ = await app.turn(tid, questions[2], previous)
            tool_calls += app.tool.executed
            denials += app.tool.denied + app.rpcs_denied
        quality = {
            "fresh": MARKER in first["answer"] and SCHEDULE in first["answer"],
            "warm": all(x in warm["answer"] for x in (MARKER, SCHEDULE, "Telegram")),
            "cold": all(x in cold["answer"] for x in (MARKER, SCHEDULE, "Telegram", FRESH_TIME))
                    and STALE_TIME not in cold["answer"],
            "starter_instruction": "RULE-715" not in first["answer"] + warm["answer"] and "RULE-715" in cold["answer"],
            "one_fixture_read": tool_calls == 1 and denials == 0,
        }
        output[name] = {"quality": quality, "fixture_reads": tool_calls, "denials": denials,
                        "fresh": first, "warm": warm, "cold": cold}
        counts = [f"{row['input']}/{row['cache']}/{row['uncached']}" for row in (first, warm, cold)]
        print(f"{name}: 3 turns, {tool_calls} fixture reads, input/cache/uncached {', '.join(counts)}",
              file=sys.stderr, flush=True)
    return output


async def main(args):
    report = {"dispatch": await verify_dispatch(), "schedule_plugin": await verify_schedule_plugin()}
    if args.codex_bin:
        with tempfile.TemporaryDirectory(prefix="javis-prompt-shadow-") as scratch:
            report["native"] = await pair(str(Path(args.codex_bin).resolve()), args.model, Path(scratch), args.compact_first)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all(all(arm["quality"].values()) for arm in report.get("native", {}).values()) else 2


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--codex-bin")
    p.add_argument("--model", default="gpt-6.2-sol")
    p.add_argument("--compact-first", action="store_true")
    raise SystemExit(asyncio.run(main(p.parse_args())))
