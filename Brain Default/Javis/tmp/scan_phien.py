import sqlite3, json, datetime, collections

DB = r"C:\Users\Admin\JavisOS\server\conversations.db"
c = sqlite3.connect(DB)
c.row_factory = sqlite3.Row
tables = [r[0] for r in c.execute("select name from sqlite_master where type='table'")]
print("TABLES", tables)
cols = [d[1] for d in c.execute("PRAGMA table_info(messages)")]
print("MSG_COLS", cols)
scols = [d[1] for d in c.execute("PRAGMA table_info(sessions)")] if "sessions" in tables else []
print("SES_COLS", scols)

# message sizes per session
rows = c.execute("select session_id, count(*) n, sum(length(coalesce(content,''))) chars, max(id) maxid from messages group by session_id order by chars desc limit 8").fetchall()
for r in rows:
    print(dict(r))
