import sqlite3, datetime, statistics
DB = r"C:\Users\Admin\JavisOS\server\runtime.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
rows = [dict(r) for r in c.execute("select * from runtime_steps order by started_at")]
done = [r for r in rows if r["started_at"] and r["completed_at"]]
print("=== phan bo token/luot (input) ===")
ins = sorted((r["actual_input_tokens"] or 0) for r in done)
for q in (0.5, 0.75, 0.9, 0.95, 0.99):
    print(f"p{int(q*100)}", f"{ins[int(len(ins)*q)]:,}")
print("max", f"{ins[-1]:,}")
print("\n=== so luot theo nguong input token ===")
for t in (50_000, 100_000, 250_000, 500_000, 1_000_000, 2_000_000):
    k = [r for r in done if (r["actual_input_tokens"] or 0) >= t]
    print(f">= {t:>9,}: {len(k):3d} luot")

# cost per turn from usage events
import json
ev = [json.loads(l) for l in open(r"C:\Users\Admin\JavisOS\server\usage-events.jsonl", encoding="utf-8") if l.strip()]
costs = sorted((e.get("cost") or 0) for e in ev)
print("\n=== phan bo chi phi/lan goi model (USD) ===")
for q in (0.5, 0.9, 0.95, 0.99):
    print(f"p{int(q*100)}", round(costs[int(len(costs)*q)], 4))
print("max", round(costs[-1], 4), "tong", round(sum(costs), 2))
big = [e for e in ev if (e.get("cost") or 0) >= 0.5]
print("so lan goi >= $0.5:", len(big), "tong", round(sum(e["cost"] for e in big), 2))
