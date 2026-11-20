import sqlite3, json

db = r"C:\Users\Admin\JavisOS\server\conversations.db"
con = sqlite3.connect(db)
cur = con.cursor()
rows = cur.execute(
    "select m.id, m.session_id, m.role, m.ts, m.content from messages m "
    "where m.content like '%Pitfall%' or m.content like '%chờ bạn duyệt%' "
    "order by m.id"
).fetchall()
print("count", len(rows))
for r in rows:
    mid, sid, role, ts, content = r
    print("=" * 60)
    print(mid, sid[:8], role, ts, len(content))
    print(content[:2500])
