import sqlite3, datetime, statistics
DB = r"C:\Users\Admin\JavisOS\server\runtime.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
rows = [dict(r) for r in c.execute("select * from runtime_steps order by started_at")]
print("n", len(rows), "from", datetime.datetime.fromtimestamp(rows[0]["started_at"]) if rows else None)
tot_tok = sum((r["actual_input_tokens"] or 0) + (r["actual_output_tokens"] or 0) for r in rows)
done = [r for r in rows if r["started_at"] and r["completed_at"]]
dur = sorted((r["completed_at"] - r["started_at"]) for r in done)
tok = [( (r["actual_input_tokens"] or 0)+(r["actual_output_tokens"] or 0)) for r in rows]
print("tong token", tot_tok)
print("dur: p50", round(dur[len(dur)//2],1), "p90", round(dur[int(len(dur)*0.9)],1), "max", round(dur[-1],1))
long = [r for r in done if (r["completed_at"]-r["started_at"]) > 300]
print("so luot > 5 phut:", len(long), "/", len(done))
s = sum(((r["actual_input_tokens"] or 0)+(r["actual_output_tokens"] or 0)) for r in long)
print("token cua cac luot >5 phut:", s, "=", round(100*s/max(1,tot_tok),1), "%")
for r in sorted(done, key=lambda r: -((r["completed_at"]-r["started_at"])))[:8]:
    print(" ", round(r["completed_at"]-r["started_at"],0), "s", r["provider"], r["model"],
          "in", r["actual_input_tokens"], "out", r["actual_output_tokens"],
          datetime.datetime.fromtimestamp(r["started_at"]).strftime("%d/%m %H:%M"))
