import json, collections, statistics, datetime

P = r"C:\Users\Admin\JavisOS\server\usage-events.jsonl"
rows = [json.loads(l) for l in open(P, encoding="utf-8") if l.strip()]
print("events", len(rows), "fields", sorted({k for r in rows for k in r}))

def d(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

big = sorted(rows, key=lambda r: -(r.get("in") or 0))[:12]
print("\n=== top 12 luot theo token vao ===")
for r in big:
    print(d(r["ts"]), f"{r['provider']}/{r['model']}", "in", r.get("in"), "out", r.get("out"), "cost", round(r.get("cost", 0), 4))

per_day = collections.defaultdict(lambda: [0, 0, 0.0])
for r in rows:
    b = per_day[r.get("day", "?")]
    b[0] += 1
    b[1] += (r.get("in") or 0) + (r.get("out") or 0)
    b[2] += r.get("cost", 0) or 0
print("\n=== theo ngay: so lan goi model / token / USD ===")
for k in sorted(per_day):
    n, tok, cost = per_day[k]
    print(k, "calls", n, "tokens", tok, "usd", round(cost, 3))

ins = [r.get("in") or 0 for r in rows if r.get("in")]
print("\ntoken vao: min", min(ins), "median", int(statistics.median(ins)), "max", max(ins))
over = [r for r in rows if (r.get("in") or 0) > 200000]
print("so lan goi model co >200k token vao:", len(over), "tong usd", round(sum(r.get("cost", 0) or 0 for r in over), 3))
over2 = [r for r in rows if (r.get("in") or 0) > 100000]
print("so lan >100k:", len(over2), "tong usd", round(sum(r.get("cost", 0) or 0 for r in over2), 3))
