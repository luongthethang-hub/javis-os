#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Javis MCP stdio bridge.

Claude Desktop (MSIX / 1p build) only accepts stdio MCP servers in
claude_desktop_config.json (command / args / env). Javis exposes its tools over
Streamable HTTP at http://127.0.0.1:7777/hub/mcp. This script stands in the
middle: it speaks JSON-RPC 2.0 over stdin/stdout (what Claude Desktop expects)
and forwards every message to the Javis hub over HTTP with the brain token,
then copies the answer back.

url + headers are read from the brain's .agents/mcp_config.json so the token is
not duplicated in a second place.
"""
import json
import os
import sys

import httpx

DEFAULT_BRAIN = r"C:\Users\Admin\JavisOS\brains\Brain Default"
BRAIN = os.environ.get("JAVIS_BRAIN") or DEFAULT_BRAIN
CONFIG = os.path.join(BRAIN, ".agents", "mcp_config.json")


def _force_utf8():
    # Windows consoles default to cp1252/cp437; MCP is UTF-8 JSON on the wire.
    for stream, err in ((sys.stdin, "replace"), (sys.stdout, "strict"), (sys.stderr, "replace")):
        try:
            stream.reconfigure(encoding="utf-8", errors=err)
        except Exception:  # noqa: BLE001
            pass


def log(msg):
    try:
        sys.stderr.write("[javis-bridge] %s\n" % msg)
        sys.stderr.flush()
    except Exception:  # noqa: BLE001
        pass


def load_endpoint():
    url = os.environ.get("JAVIS_HUB_URL")
    headers = {}
    try:
        with open(CONFIG, "r", encoding="utf-8-sig") as fh:
            cfg = json.load(fh)
        srv = (cfg.get("mcpServers") or {}).get("javis") or {}
        url = url or srv.get("url") or srv.get("serverUrl")
        headers = dict(srv.get("headers") or {})
    except Exception as exc:  # noqa: BLE001
        log("could not read %s: %s" % (CONFIG, exc))
    if not url:
        url = "http://127.0.0.1:7777/hub/mcp"
    headers.setdefault("Content-Type", "application/json")
    headers.setdefault("Accept", "application/json, text/event-stream")
    return url, headers


def emit(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def iter_payloads(resp):
    ctype = (resp.headers.get("content-type") or "").lower()
    text = resp.text or ""
    if "text/event-stream" in ctype:
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                chunk = line[5:].strip()
                if not chunk or chunk == "[DONE]":
                    continue
                try:
                    yield json.loads(chunk)
                except Exception:  # noqa: BLE001
                    log("bad sse chunk: %r" % chunk[:200])
        return
    if not text.strip():
        return
    try:
        data = json.loads(text)
    except Exception:  # noqa: BLE001
        log("non-json reply: %r" % text[:200])
        return
    if isinstance(data, list):
        for item in data:
            yield item
    else:
        yield data


def main():
    _force_utf8()
    url, headers = load_endpoint()
    log("hub %s, brain %s" % (url, BRAIN))
    timeout = httpx.Timeout(connect=10.0, read=300.0, write=60.0, pool=10.0)
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        for raw in sys.stdin:
            line = raw.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except Exception:  # noqa: BLE001
                log("bad input line: %r" % line[:200])
                continue
            is_request = isinstance(msg, dict) and "method" in msg
            try:
                resp = client.post(url, headers=headers, json=msg)
            except Exception as exc:  # noqa: BLE001
                if is_request and "id" in msg:
                    emit({
                        "jsonrpc": "2.0",
                        "id": msg.get("id"),
                        "error": {"code": -32000, "message": "Javis hub unreachable: %s" % exc},
                    })
                continue
            if resp.status_code >= 400:
                if is_request and "id" in msg:
                    emit({
                        "jsonrpc": "2.0",
                        "id": msg.get("id"),
                        "error": {
                            "code": -32000,
                            "message": "Javis hub HTTP %s: %s" % (resp.status_code, (resp.text or "")[:300]),
                        },
                    })
                continue
            for payload in iter_payloads(resp):
                if isinstance(payload, dict) and payload.get("jsonrpc"):
                    emit(payload)


if __name__ == "__main__":
    main()
