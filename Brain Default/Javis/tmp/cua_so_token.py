import json, time, datetime, collections, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
rows = [json.loads(l) for l in open(r"C:\Users\Admin\JavisOS\server\usage-events.jsonl", encoding="utf-8") if l.strip()]
now = time.time()
print("now", datetime.datetime.fromtimestamp(now).strftime("%d/%m %H:%M"))

for h in (5, 24, 24 * 7):
    w = [r for r in rows if now - r["ts"] <= h * 3600]
    tok = sum((r.get("in") or 0) + (r.get("out") or 0) for r in w)
    cost = sum(r.get("cost") or 0 for r in w)
    print(f"cua so {h}h: {len(w)} lan goi, {tok:,} token, ${cost:.2f}")

print("\n=== 5h qua, tung lan goi ===")
for r in sorted([r for r in rows if now - r["ts"] <= 5 * 3600], key=lambda r: r["ts"]):
    print(datetime.datetime.fromtimestamp(r["ts"]).strftime("%H:%M:%S"),
          f"{r['provider']}/{r['model']}", f"in {r.get('in') or 0:>9,}", f"out {r.get('out') or 0:>7,}",
          f"${(r.get('cost') or 0):.4f}")
