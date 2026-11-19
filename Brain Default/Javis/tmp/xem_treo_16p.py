import sqlite3, datetime, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
c = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\runtime.db"); c.row_factory = sqlite3.Row
sid = "rs_dbe21d5bffd74924b464b7ec58a2ce89"
print("now", datetime.datetime.now().strftime("%H:%M:%S"))
st = c.execute("select * from runtime_steps where id=?", (sid,)).fetchone()
print("step", st["status"], datetime.datetime.fromtimestamp(st["started_at"]).strftime("%H:%M:%S"),
      "completed", st["completed_at"], "err", st["error_code"])
rows = [dict(r) for r in c.execute("select event_type,payload_json,created_at from runtime_events where step_id=? order by seq", (sid,))]
t0 = rows[0]["created_at"] if rows else 0
for r in rows:
    print(f"  +{r['created_at']-t0:7.1f}s", r["event_type"], str(r["payload_json"])[:200])
