"""Queue read-only Red/Blue reviews and reconcile their outcomes from Kanban."""
import hashlib
import json
import logging
import re
import sqlite3
import time
from contextlib import closing
from decimal import Decimal, InvalidOperation
from pathlib import Path

SLUG = "red-blue-team-review"
ROUTE = f"wf:{SLUG}"
LOG = logging.getLogger(__name__)
VERDICT = re.compile(r"\A\s*DEBATE_VERDICT: (PASS|CONDITIONAL|FAIL)[ \t]*\r?(?:\n|\Z)")
DEFAULT_BUDGET_CENTS = 500
DEFAULT_ESTIMATE_CENTS = 35
DEFAULT_FAILURE_LIMIT = 3
RESERVATION_SECONDS = 60

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    scope TEXT PRIMARY KEY,
    budget INTEGER NOT NULL,
    estimate INTEGER NOT NULL,
    failure_limit INTEGER NOT NULL,
    reset_after INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS jobs (
    seq INTEGER PRIMARY KEY,
    scope TEXT NOT NULL,
    request_id TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    task_id TEXT NOT NULL,
    charge INTEGER NOT NULL,
    outcome TEXT NOT NULL DEFAULT 'reserved',
    created REAL NOT NULL,
    detail TEXT NOT NULL DEFAULT '',
    UNIQUE (scope, request_id)
);
CREATE INDEX IF NOT EXISTS jobs_scope_outcome ON jobs(scope, outcome, seq);
"""


def _database(ctx):
    db = sqlite3.connect(Path(ctx.data_dir) / "debate.sqlite3", timeout=3)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


def _chat(turn):
    turn = turn or {}
    chat = str(turn.get("chat_id") or "").strip()
    if not turn.get("la_chu") or turn.get("chat_type") == "group" or not chat:
        return ""
    if turn.get("kenh") == "dashboard" and not chat.startswith("web:"):
        return f"web:{chat}"
    return chat


def _scope(root, chat):
    identity = json.dumps([str(Path(root).resolve()), chat], ensure_ascii=False)
    return hashlib.sha256(identity.encode()).hexdigest()


def _cents(amount):
    try:
        cents = Decimal(str(amount)) * 100
        if not (1 <= cents <= 100_000_000) or cents != cents.to_integral_value():
            raise ValueError
        return int(cents)
    except (InvalidOperation, ValueError):
        raise ValueError("Số tiền phải từ 0,01 đến 1.000.000 USD, tối đa hai chữ số thập phân.") from None


def _settings(db, scope):
    return db.execute("SELECT * FROM sessions WHERE scope=?", (scope,)).fetchone()


def _state(db, scope):
    settings = _settings(db, scope)
    used, pending = db.execute(
        """SELECT COALESCE(SUM(charge), 0),
                  COUNT(CASE WHEN outcome IN ('reserved','pending') THEN 1 END)
           FROM jobs WHERE scope=?""", (scope,),
    ).fetchone()
    budget, estimate = settings["budget"], settings["estimate"]
    failures = 0
    for row in db.execute(
        """SELECT outcome FROM jobs WHERE scope=? AND seq>?
           AND outcome IN ('pass','conditional','fail','error') ORDER BY seq DESC""",
        (scope, settings["reset_after"]),
    ):
        if row["outcome"] in ("pass", "conditional"):
            break
        failures += 1
        if failures >= settings["failure_limit"]:
            break
    state = {
        "budget_usd": budget / 100,
        "estimated_cost_per_review_usd": estimate / 100,
        "estimated_committed_usd": used / 100,
        "budget_remaining_usd": max(0, budget - used) / 100,
        "pending": pending,
        "consecutive_failures": failures,
        "max_consecutive_fail": settings["failure_limit"],
        "circuit_open": failures >= settings["failure_limit"],
    }
    if used * 5 >= budget * 4:
        state["budget_warning"] = "Ngân sách ước tính của cuộc chat đã dùng hoặc giữ chỗ từ 80% trở lên."
    return state, budget - used


def _settle(db, scope, store):
    jobs = db.execute(
        "SELECT * FROM jobs WHERE scope=? AND outcome IN ('reserved','pending')", (scope,),
    ).fetchall()
    for job in jobs:
        task = store.get_task(job["task_id"])
        if not task:
            if job["outcome"] == "pending":
                outcome, charge = "error", job["charge"]
            elif time.time() - job["created"] >= RESERVATION_SECONDS:
                outcome, charge = "error", 0
            else:
                continue
        else:
            charge = job["charge"]
            status = task["status"]
            verdict = VERDICT.match(str(task.get("result") or ""))
            if status == "cancelled":
                outcome = "cancelled"
            elif status in ("done", "review", "archived", "blocked"):
                outcome = verdict.group(1).lower() if verdict else "error"
            else:
                outcome = "pending"
        db.execute("UPDATE jobs SET outcome=?, charge=? WHERE seq=?", (outcome, charge, job["seq"]))


def _workflow_active(feature, root):
    from skill_router import read_frontmatter_only
    from workflow_graph import workflow_status

    path = Path(feature.deps.workflows_dir(root)) / f"{SLUG}.md"
    return path.is_file() and workflow_status(read_frontmatter_only(path)[0]) == "active"


def _run(db, feature, root, chat, scope, args, state, remaining, turn):
    content = args.get("content")
    if not isinstance(content, str) or not content.strip():
        return {"error": "Thiếu nội dung cần rà soát."}
    fingerprint = hashlib.sha256(content.encode()).hexdigest()
    request_id = args.get("request_id")
    if request_id is None:
        import luot_dang_chay

        active = luot_dang_chay.doan_luot(root) or {}
        message_id = turn.get("message_id") or (active.get("msg_id") if active.get("chat_id") == chat else 0)
        request_id = f"{message_id or 0}:{fingerprint}"
    if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
        return {"error": "request_id phải có từ 1 đến 128 ký tự."}
    job = db.execute(
        "SELECT * FROM jobs WHERE scope=? AND request_id=?", (scope, request_id),
    ).fetchone()
    if job:
        if job["fingerprint"] != fingerprint:
            return {"error": "request_id đã gắn với nội dung khác."}
        existing = feature.store.get_task(job["task_id"])
        if existing:
            return {"task_id": job["task_id"], "created": False, "task_status": existing["status"],
                    "outcome": job["outcome"], "orchestration": feature.store.board_mode(root), **state}
        return {"blocked": True, "reason": "existing_request", "outcome": job["outcome"],
                "detail": job["detail"], **state}

    if state["circuit_open"]:
        return {"blocked": True, "reason": "circuit_open", **state}
    if state["pending"]:
        return {"blocked": True, "reason": "review_pending", **state}
    if not _workflow_active(feature, root):
        return {"blocked": True, "reason": "workflow_inactive", "workflow": SLUG, **state}

    estimate = _settings(db, scope)["estimate"]
    if remaining < estimate:
        return {"blocked": True, "reason": "budget_exceeded", **state}

    key = hashlib.sha256(f"{scope}:{request_id}".encode()).hexdigest()
    task_id = f"t_{key[:24]}"
    db.execute(
        """INSERT INTO jobs(scope, request_id, fingerprint, task_id, charge, created)
           VALUES (?,?,?,?,?,?)""",
        (scope, request_id, fingerprint, task_id, estimate, time.time()),
    )
    # Keep the reservation if the process stops after Kanban commits and before this tool replies.
    db.commit()
    db.execute("BEGIN IMMEDIATE")
    try:
        confirmed = feature.store.enqueue(
            brain_root=root, title=f"Red/Blue Team Review {key[:8]}", intent=content, route=ROUTE,
            created_by="debate-engine", chat_id=chat, capability="files", execution_mode="suggest",
            idempotency_key=f"debate:{key}", status="ready", max_attempts=1,
            task_id=task_id, dedupe_title=False,
        )
        if confirmed != task_id:
            raise RuntimeError("Kanban trả về mã việc khác mã đã giữ chỗ.")
    except Exception as exc:
        existing = feature.store.get_task(task_id)
        if not existing:
            db.execute("UPDATE jobs SET outcome='error', charge=0, detail=? WHERE task_id=?",
                       (type(exc).__name__, task_id))
            return {"error": f"Không đưa được việc vào Kanban ({type(exc).__name__}).", **_state(db, scope)[0]}
    db.execute("UPDATE jobs SET outcome='pending' WHERE task_id=?", (task_id,))
    db.commit()
    feature.wake()
    orchestration = feature.store.board_mode(root)
    return {
        "queued": True, "task_id": task_id, "task_status": "ready", "orchestration": orchestration,
        "will_auto_dispatch": orchestration == "auto", **_state(db, scope)[0],
    }


def _handle(ctx, args, turn):
    import tasks

    current = turn or {}
    chat = _chat(current)
    if not chat or not ctx.vault_root:
        return {"error": "Cần gọi từ cuộc chat riêng của chủ đã được Javis xác thực."}
    if args.get("chat_id") not in (None, "", chat):
        return {"error": "chat_id phải khớp với cuộc chat đang yêu cầu."}
    feature = tasks.current()
    if feature is None:
        return {"error": "Kanban chưa sẵn sàng."}
    root = str(Path(ctx.vault_root).resolve())
    scope = _scope(root, chat)
    op = args.get("op", "run")
    with closing(_database(ctx)) as db, db:
        db.execute("BEGIN IMMEDIATE")
        db.execute(
            "INSERT OR IGNORE INTO sessions(scope, budget, estimate, failure_limit) VALUES (?,?,?,?)",
            (scope, DEFAULT_BUDGET_CENTS, DEFAULT_ESTIMATE_CENTS, DEFAULT_FAILURE_LIMIT),
        )
        _settle(db, scope, feature.store)
        state, remaining = _state(db, scope)
        if op == "run":
            return _run(db, feature, root, chat, scope, args, state, remaining, current)
        if op == "status":
            last = db.execute(
                "SELECT task_id, outcome FROM jobs WHERE scope=? ORDER BY seq DESC LIMIT 1", (scope,),
            ).fetchone()
            return {**state, "last_review": dict(last) if last else None,
                    "workflow_active": _workflow_active(feature, root),
                    "orchestration": feature.store.board_mode(root)}
        if op == "reset":
            if state["pending"]:
                return {"blocked": True, "reason": "review_pending", **state}
            db.execute(
                """UPDATE sessions SET reset_after=
                   (SELECT COALESCE(MAX(seq), 0) FROM jobs WHERE scope=?) WHERE scope=?""",
                (scope, scope),
            )
            return _state(db, scope)[0]
        if op == "config":
            old = _settings(db, scope)
            budget = _cents(args["budget_usd"]) if "budget_usd" in args else old["budget"]
            estimate = _cents(args["estimate_usd"]) if "estimate_usd" in args else old["estimate"]
            limit = args.get("max_consecutive_fail", old["failure_limit"])
            if type(limit) is not int or not 1 <= limit <= 20:
                raise ValueError("Ngưỡng ngắt phải là số nguyên từ 1 đến 20.")
            db.execute("UPDATE sessions SET budget=?, estimate=?, failure_limit=? WHERE scope=?",
                       (budget, estimate, limit, scope))
            return _state(db, scope)[0]
        return {"error": "Thao tác hợp lệ gồm run, status, config và reset."}


def register(ctx):
    import turn_context

    async def handler(args, call_ctx):
        try:
            return _handle(call_ctx, args, turn_context.current())
        except ValueError as exc:
            return {"error": str(exc)}
        except sqlite3.Error as exc:
            LOG.warning("Debate Engine: không đọc/ghi được trạng thái (%s).", type(exc).__name__)
            return {"error": "Không truy cập được trạng thái Debate Engine. Dùng lại cùng request_id khi thử lại."}

    # Hook returns are ignored by the hub. Log each threshold crossing once per active plugin instance.
    warned = set()

    def budget_warning(vault_root=None, turn=None, **_):
        chat = _chat(turn)
        if not chat or not vault_root:
            return
        scope = _scope(vault_root, chat)
        path = Path(ctx.data_dir) / "debate.sqlite3"
        if not path.is_file():
            return
        with closing(sqlite3.connect(path, timeout=0.1)) as db:
            row = db.execute(
                """SELECT s.budget, COALESCE(SUM(j.charge), 0)
                   FROM sessions s LEFT JOIN jobs j ON j.scope=s.scope
                   WHERE s.scope=? GROUP BY s.scope""", (scope,),
            ).fetchone()
        if row and row[1] * 5 >= row[0] * 4:
            if scope not in warned:
                warned.add(scope)
                LOG.warning("Debate Engine: đã giữ chỗ từ 80%% ngân sách ước tính (%s/%s USD).",
                            row[1] / 100, row[0] / 100)
        else:
            warned.discard(scope)

    ctx.register_tool(
        name="debate_engine", handler=handler, min_mode="safe",
        op_modes={"run": "full", "status": "safe", "config": "full", "reset": "full"},
        description=(
            "Rà soát Red/Blue theo yêu cầu rõ của chủ bằng việc Kanban chỉ đọc. "
            "run nhận content và request_id tùy chọn (giữ nguyên khi thử lại, dùng mã mới để rà lại cùng nội dung). "
            "status đọc kết quả, hạn mức ước tính và bộ ngắt theo cuộc chat. "
            "config và reset chỉ dùng khi chủ yêu cầu. Kết quả được gửi về cuộc chat đang gọi."
        ),
        schema={"type": "object", "required": ["op"], "additionalProperties": False, "properties": {
            "op": {"type": "string", "enum": ["run", "status", "config", "reset"]},
            "content": {"type": "string"},
            "request_id": {"type": "string", "minLength": 1, "maxLength": 128},
            "chat_id": {"type": "string"},
            "budget_usd": {"type": "number", "minimum": 0.01},
            "estimate_usd": {"type": "number", "minimum": 0.01},
            "max_consecutive_fail": {"type": "integer", "minimum": 1, "maximum": 20},
        }},
    )
    ctx.register_hook("post_tool_call", budget_warning)
