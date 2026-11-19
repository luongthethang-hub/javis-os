import json, time, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
rows = [json.loads(l) for l in open(r"C:\Users\Admin\JavisOS\server\usage-events.jsonl", encoding="utf-8") if l.strip()]
now = time.time()
w = [r for r in rows if now - r["ts"] <= 5 * 3600]
by = collections.defaultdict(lambda: [0, 0, 0.0])
for r in w:
    k = f"{r['provider']}/{r['model']}"
    by[k][0] += 1
    by[k][1] += (r.get("in") or 0) + (r.get("out") or 0)
    by[k][2] += r.get("cost") or 0
print("=== 5 gio qua, theo provider/model ===")
for k, (n, tok, cost) in sorted(by.items(), key=lambda x: -x[1][1]):
    print(f"{k:38s} goi {n:3d}  token {tok:>11,}  ${cost:6.3f}")
paid = sum(v[1] for k, v in by.items() if v[2] > 0)
free = sum(v[1] for k, v in by.items() if v[2] == 0)
print(f"\ntoken ton TIEN: {paid:,}   token mien phi (goi thue bao/codex/local): {free:,}")
print("tong $ 5h:", round(sum(v[2] for v in by.values()), 2))

# 24h split
w24 = [r for r in rows if now - r["ts"] <= 24 * 3600]
paid24 = sum((r.get("in") or 0) + (r.get("out") or 0) for r in w24 if (r.get("cost") or 0) > 0)
free24 = sum((r.get("in") or 0) + (r.get("out") or 0) for r in w24 if not (r.get("cost") or 0))
print(f"24h: ton tien {paid24:,} / mien phi {free24:,} / tong $ {round(sum(r.get('cost') or 0 for r in w24),2)}")
