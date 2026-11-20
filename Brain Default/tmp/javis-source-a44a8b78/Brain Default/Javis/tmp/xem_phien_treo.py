import sqlite3, datetime, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
DB = r"C:\Users\Admin\JavisOS\server\conversations.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
rows = c.execute("""select session_id, id, role, ts, substr(content,1,60) t
                    from messages where ts > ? order by ts desc limit 12""",
                 (datetime.datetime.now().timestamp() - 3600,)).fetchall()
for r in rows:
    print(datetime.datetime.fromtimestamp(r["ts"]).strftime("%H:%M:%S"), r["session_id"][:8], r["role"], "|", (r["t"] or "").replace("\n", " ")[:60])
print("---- phien co tin user ma chua co tra loi ----")
sess = c.execute("""select session_id, max(id) mid, max(case when role='user' then id end) last_user
                    from messages group by session_id""").fetchall()
for s in sess:
    last = c.execute("select role from messages where session_id=? order by id desc limit 1", (s["session_id"],)).fetchone()
    if last and last["role"] == "user":
        print(s["session_id"][:8], "tin cuoi la user")
