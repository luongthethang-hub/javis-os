import sqlite3, datetime
DB = r"C:\Users\Admin\JavisOS\server\runtime.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
now = datetime.datetime.now().timestamp()
print("now", datetime.datetime.now())
for r in c.execute("select id,status,provider,model,started_at,completed_at,actual_input_tokens from runtime_steps where status='RUNNING' order by started_at"):
    st = r["started_at"]
    print("RUNNING", r["id"], r["provider"], r["model"], "started", datetime.datetime.fromtimestamp(st) if st else None,
          "age_min", None if not st else round((now - st) / 60, 1), "in", r["actual_input_tokens"])

cols = [d[1] for d in c.execute("PRAGMA table_info(runtime_events)")]
print("event cols", cols)
n = c.execute("select count(*) from runtime_events").fetchone()[0]
print("events rows", n)
