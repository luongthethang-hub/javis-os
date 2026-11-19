import sqlite3, collections, json
DB = r"C:\Users\Admin\JavisOS\server\runtime.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
cnt = collections.Counter(r[0] for r in c.execute("select event_type from runtime_events"))
print("=== loai event ===")
for k, v in cnt.most_common(30):
    print(f"{v:5d}  {k}")
print("\n=== so event 'model.round' / 'route.observed' tren moi step (top) ===")
rows = c.execute("""select step_id, count(*) n, sum(case when event_type='route.observed' then 1 else 0 end) routes
                    from runtime_events group by step_id order by n desc limit 8""").fetchall()
for r in rows:
    print(dict(r))
print("\n=== co event chua token tung vong khong? ===")
for r in c.execute("select event_type, payload_json from runtime_events where event_type like '%usage%' or event_type like '%round%' or event_type like '%model%' limit 5"):
    print(r["event_type"], str(r["payload_json"])[:200])
