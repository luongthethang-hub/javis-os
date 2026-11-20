"""Track admitted work until it finishes, and briefly close admission for restart."""
from functools import wraps

from starlette.responses import JSONResponse

_work = set()
_maintenance = None


def busy():
    return bool(_work)


def begin():
    ticket = object()
    _work.add(ticket)
    return ticket


def end(ticket):
    _work.discard(ticket)


def blocked():
    global _maintenance
    if _maintenance is not None and not _maintenance():
        _maintenance = None
    return _maintenance is not None


def close_admission(still_updating):
    global _maintenance
    _maintenance = still_updating


def track(fn):
    @wraps(fn)
    async def run(*args, **kwargs):
        ticket = begin()
        try:
            return await fn(*args, **kwargs)
        finally:
            end(ticket)
    return run


class WorkRequests:
    """Count work HTTP requests through their last body frame, including streaming."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        path = scope.get("path", "")
        method = scope.get("method")
        work = scope["type"] == "http" and (
            method not in {"GET", "HEAD", "OPTIONS"} or path in {"/workflows/run", "/workflows/resume"}
        ) and path != "/update"
        if not work:
            return await self.app(scope, receive, send)
        if blocked():
            return await JSONResponse(
                {"ok": False, "error": "Javis is restarting for an update. Retry shortly."},
                status_code=503, headers={"Retry-After": "30"},
            )(scope, receive, send)
        ticket = begin()
        try:
            return await self.app(scope, receive, send)
        finally:
            end(ticket)
