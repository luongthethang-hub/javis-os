import json
P = r"C:\Users\Admin\JavisOS\server\usage-events.jsonl"
rows = [json.loads(l) for l in open(P, encoding="utf-8") if l.strip()]
r = max(rows, key=lambda x: (x.get("in") or 0))
print(json.dumps(r, ensure_ascii=False, indent=2)[:2500])
print("---- co execution khong:", sum(1 for x in rows if x.get("execution")), "/", len(rows))
