import sqlite3, json, datetime, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
c = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\runtime.db"); c.row_factory = sqlite3.Row
sid = "rs_086e77c56e854da69b59d85884fb4c3e"
for r in c.execute("select event_type,payload_json,created_at from runtime_events where step_id=? order by seq", (sid,)):
    if r["event_type"] in ("payload.observed", "usage.observed", "route.observed", "compiler.shadow"):
        print(r["event_type"], str(r["payload_json"])[:500])
        print()
