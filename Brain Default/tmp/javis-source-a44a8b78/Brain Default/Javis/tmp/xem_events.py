import sqlite3, json, datetime, collections
DB = r"C:\Users\Admin\JavisOS\server\runtime.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
sid = c.execute("select id from runtime_steps where actual_input_tokens>2000000 limit 1").fetchone()[0]
print("step", sid)
rows = [dict(r) for r in c.execute("select * from runtime_events where step_id=? order by seq", (sid,))]
print("events", len(rows))
cnt = collections.Counter(r["event_type"] for r in rows)
print(cnt)
t0 = rows[0]["created_at"] if rows else None
for r in rows[:40]:
    print(round((r["created_at"] - t0), 1) if t0 else "", r["event_type"], str(r["payload_json"])[:220])
