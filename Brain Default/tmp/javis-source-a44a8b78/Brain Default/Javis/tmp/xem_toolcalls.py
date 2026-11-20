import sqlite3, datetime, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
c = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\conversations.db"); c.row_factory = sqlite3.Row
rows = c.execute("""select id, role, ts, length(content) n, tool_calls_json, meta_json
                    from messages where session_id='2098bbece40f41f59f32dc7976df2742'
                    and ts between 1795023000 and 1795023800 order by ts""").fetchall()
for r in rows:
    tc = r["tool_calls_json"]
    print(datetime.datetime.fromtimestamp(r["ts"]).strftime("%H:%M:%S"), r["role"], "chars", r["n"],
          "toolcalls", len(json.loads(tc)) if tc else 0,
          (r["meta_json"] or "")[:100])
