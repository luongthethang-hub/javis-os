import sqlite3, datetime
DB = r"C:\Users\Admin\JavisOS\server\runtime.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
rows = [dict(r) for r in c.execute("select * from runtime_steps order by started_at desc limit 60")]
print("n", len(rows))
for r in rows[:25]:
    st = r["started_at"]; en = r["completed_at"]
    dur = (en - st) if (st and en) else None
    print(r["id"][:12], r["status"], r["provider"], r["model"], "dur", None if dur is None else round(dur, 1),
          "in", r["actual_input_tokens"], "out", r["actual_output_tokens"], "err", r["error_code"])
durs = [(r["completed_at"] - r["started_at"]) for r in rows if r["started_at"] and r["completed_at"]]
if durs:
    durs.sort()
    print("dur sec: min", round(durs[0], 1), "median", round(durs[len(durs)//2], 1), "max", round(durs[-1], 1))
# status distribution
from collections import Counter
print(Counter(r["status"] for r in rows))
print(Counter(r["error_code"] for r in rows))
