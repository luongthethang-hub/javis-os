"""Opt-in, deterministic limits for sequential workflow runs.

Usage is reported usage, not a price estimate. Providers may report it only after
a call finishes, so token limits stop subsequent work and cannot cap in-flight
billing. Wall, idle, call and tool limits remain effective without usage data.
"""
from __future__ import annotations

import asyncio
import contextlib
import contextvars
import hashlib
import json
import math
import re
import time
from dataclasses import dataclass
from pathlib import Path


class GuardError(ValueError):
    pass


@dataclass(frozen=True)
class GuardPolicy:
    wall_seconds: float = 1200
    idle_seconds: float = 180
    max_model_stages: int = 8
    max_tool_calls: int = 24
    max_reported_tokens: int = 80000
    max_output_chars: int = 120000

    @classmethod
    def from_meta(cls, meta: dict):
        raw = meta.get("execution_guard")
        if raw is None:
            return None
        if not isinstance(raw, dict) or raw.get("enabled") is not True:
            raise GuardError("guard_configuration_invalid")
        values = {}
        for key in cls.__dataclass_fields__:
            value = raw.get(key, getattr(cls(), key))
            if isinstance(value, bool):
                raise GuardError("guard_limit_invalid:" + key)
            try:
                number = float(value)
            except (TypeError, ValueError, OverflowError):
                raise GuardError("guard_limit_invalid:" + key) from None
            if not math.isfinite(number) or number <= 0:
                raise GuardError("guard_limit_invalid:" + key)
            if not key.endswith("seconds"):
                if number != int(number):
                    raise GuardError("guard_limit_invalid:" + key)
                number = int(number)
            values[key] = number
        return cls(**values)


def preflight(meta: dict, agents_dir: Path, input_text: str, tools=None, *, fallback_providers=()):
    """Validate a sequential contract before spending any model calls."""
    policy = GuardPolicy.from_meta(meta)
    if policy is None:
        return None
    steps = meta.get("contract_steps", meta.get("steps"))
    if meta.get("nodes") or not isinstance(steps, list) or not steps:
        raise GuardError("guard_requires_sequential_steps")
    required = meta["execution_guard"].get("required_input_fields", [])
    if not isinstance(required, list) or any(not isinstance(x, str) or not x for x in required):
        raise GuardError("guard_input_contract_invalid")
    if required:
        try:
            data = json.loads(input_text)
        except (ValueError, TypeError):
            raise GuardError("input_must_be_json:" + ",".join(required)) from None
        if not isinstance(data, dict):
            raise GuardError("input_must_be_object")
        missing = [key for key in required if data.get(key) is None or not str(data[key]).strip()]
        if missing:
            raise GuardError("input_fields_missing:" + ",".join(missing))
    minimum_calls = 0
    for index, step in enumerate(steps):
        if not isinstance(step, dict) or not str(step.get("task") or "").strip():
            raise GuardError(f"step_contract_invalid:{index}")
        for key in ("agent", "verify_agent"):
            slug = step.get(key)
            if key == "verify_agent" and not slug:
                continue
            if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", slug):
                raise GuardError(f"agent_slug_invalid:{index}:{key}")
            path = agents_dir / (slug + ".md")
            if not path.is_file() or not path.read_text(encoding="utf-8-sig").strip():
                raise GuardError("agent_unavailable:" + slug)
            minimum_calls += 1
        first_line = step.get("require_first_line")
        if first_line is not None and (not isinstance(first_line, str) or not first_line.strip()
                                       or first_line.splitlines() != [first_line.strip()]):
            raise GuardError(f"first_line_contract_invalid:{index}")
        retries = step.get("max_retries", 1)
        if isinstance(retries, bool) or not isinstance(retries, int) or not 0 <= retries <= 1:
            raise GuardError(f"review_retry_limit:{index}")
        required_tools = step.get("required_tools") or []
        if not isinstance(required_tools, list) or any(not isinstance(x, str) for x in required_tools):
            raise GuardError(f"required_tools_invalid:{index}")
        if "author_fallback" in step:
            if meta.get("supplied_data_only") is not True:
                raise GuardError(f"fallback_requires_supplied_data_only:{index}")
            fallback = step["author_fallback"]
            if (not isinstance(fallback, dict) or set(fallback) != {"provider", "model"}
                    or not isinstance(fallback["provider"], str)
                    or fallback["provider"] not in fallback_providers
                    or not isinstance(fallback["model"], str) or not fallback["model"].strip()
                    or fallback["model"] != fallback["model"].strip()):
                raise GuardError(f"fallback_route_invalid:{index}")
        if (required_tools or step.get("tools")) and meta.get("supplied_data_only") is True:
            raise GuardError(f"tools_unavailable_in_supplied_data_run:{index}")
        if tools is not None and required_tools:
            # An explicit tool list is the execution boundary. Do not infer a
            # shell/web grant from a provider name or an agent's prose.
            granted = set(tools) | set(step.get("tools") or [])
            missing = set(required_tools) - granted
            if missing:
                raise GuardError("required_tools_not_granted:" + ",".join(sorted(missing)))
    if minimum_calls > policy.max_model_stages:
        raise GuardError("minimum_calls_exceed_budget")
    return policy


def _reported_usage(event):
    if event.get("type") == "usage":
        event = {"tokens_in": event.get("input"), "tokens_out": event.get("output")}
    usage = event.get("usage") or {}
    if not isinstance(usage, dict):
        usage = {}

    def count(value):
        try:
            return max(0, int(value or 0))
        except (ValueError, TypeError, OverflowError):
            return 0

    return (count(event.get("tokens_in", usage.get("input_tokens", usage.get("prompt_tokens", 0)))),
            count(event.get("tokens_out", usage.get("output_tokens", usage.get("completion_tokens", 0)))))


def usage_tokens(event: dict) -> int:
    return sum(_reported_usage(event))


def usage_event(event: dict, index: int, phase: str, *, include_tokens=True) -> dict:
    tokens_in, tokens_out = _reported_usage(event) if include_tokens else (0, 0)
    return {"type": "step_usage", "i": index, "phase": phase, "tokens_in": tokens_in,
            "tokens_out": tokens_out, "content": event.get("content") or ""}


async def author_events(build, prompt, fallback=None):
    """Switch a tool-free author once, before output, on an adapter HTTP error."""
    replayable = fallback is not None
    async with contextlib.aclosing(build().query(prompt)) as stream:
        async for event in stream:
            kind = event.get("type")
            status = event.get("ma")
            if (replayable and kind == "error" and type(status) is int and status in (429, 503)
                    and not event.get("resume_failed")):
                break
            if kind in ("tool_call", "final", "error") or (kind == "text" and event.get("content")):
                replayable = False
            yield event
        else:
            return

    # The guard admits this extra stage before any fallback request starts.
    yield {"type": "author_fallback", "status_code": event["ma"]}
    async with contextlib.aclosing(fallback().query(prompt)) as stream:
        async for event in stream:
            yield event


async def guarded_events(events, policy: GuardPolicy | None):
    """Bound an event stream; cancellations close the underlying engine stream.

    This wrapper creates no scheduler and never retries or changes permissions.
    Heartbeats cannot extend the absolute deadline. A token counter is only
    updated from explicit step_usage events to avoid double-counting finals.
    """
    if policy is None:
        async for event in events:
            yield event
        return
    iterator = events.__aiter__()
    # A streaming adapter can hold a ContextVar token across event boundaries.
    stream_context = contextvars.copy_context()
    deadline = time.monotonic() + policy.wall_seconds
    calls = tools = tokens = output_chars = final_chars = 0
    current_step = None
    author_outputs = {}
    pending = None
    terminal = False
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise GuardError("wall_timeout")
            pending = asyncio.create_task(iterator.__anext__(), context=stream_context)
            wall_due_first = remaining <= policy.idle_seconds
            done, _ = await asyncio.wait({pending}, timeout=min(remaining, policy.idle_seconds))
            if not done:
                raise GuardError("wall_timeout" if wall_due_first else "idle_timeout")
            try:
                event = pending.result()
            except StopAsyncIteration:
                if not terminal:
                    raise GuardError("stream_ended_without_result")
                return
            pending = None
            kind = event.get("type")
            if kind == "step_start":
                current_step = event.get("i")
            if kind in ("step_start", "step_retry", "step_verify", "step_fallback"):
                if tokens >= policy.max_reported_tokens:
                    raise GuardError("reported_token_budget")
                calls += 1
                if calls > policy.max_model_stages:
                    raise GuardError("model_call_budget")
            if kind == "step_tool":
                tools += 1
                if tools > policy.max_tool_calls:
                    raise GuardError("tool_call_budget")
            if kind == "step_usage":
                tokens += usage_tokens(event)
                final_chars += len(str(event.get("content") or ""))
                if tokens > policy.max_reported_tokens:
                    raise GuardError("reported_token_budget")
                if final_chars > policy.max_output_chars:
                    raise GuardError("output_size_budget")
                if event.get("phase") == "author" and str(event.get("content") or "").strip():
                    digest = hashlib.sha256(str(event["content"]).strip().encode("utf-8")).hexdigest()
                    key = event.get("i")
                    if author_outputs.get(key) == digest:
                        raise GuardError("no_progress_after_repair")
                    author_outputs[key] = digest
            if kind == "step_text":
                output_chars += len(str(event.get("content") or ""))
                if output_chars > policy.max_output_chars:
                    raise GuardError("output_size_budget")
            if kind == "step_usage":
                event = {key: val for key, val in event.items() if key != "content"}
            yield event
            if kind in ("done", "error", "wait_user"):
                terminal = True
                return
    except Exception as exc:
        reason = str(exc) if isinstance(exc, GuardError) else "adapter_error:" + type(exc).__name__
        stats = {"model_stages": calls, "tool_calls": tools, "reported_tokens": tokens,
                 "token_accounting": "provider_reported_only"}
        if current_step is not None:
            yield {"type": "step_error", "i": current_step, "content": "execution_guard:" + reason}
        yield {"type": "error", "i": current_step, "content": "execution_guard:" + reason,
               "needs_input": True, "guard_stats": stats}
    finally:
        if pending is not None:
            pending.cancel()
            done, _ = await asyncio.wait({pending}, timeout=2)
            if not done:
                # Stop admitting work even if a third-party adapter fails to
                # acknowledge cancellation. Consume its eventual exception.
                pending.add_done_callback(lambda task: task.exception() if not task.cancelled() else None)
        if pending is None or pending.done():
            with contextlib.suppress(Exception):
                close = asyncio.create_task(iterator.aclose(), context=stream_context)
                done, _ = await asyncio.wait({close}, timeout=2)
                if not done:
                    close.cancel()
                    close.add_done_callback(lambda task: task.exception() if not task.cancelled() else None)
