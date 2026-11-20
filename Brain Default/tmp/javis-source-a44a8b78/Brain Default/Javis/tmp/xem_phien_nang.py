import sqlite3, datetime, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

c = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\conversations.db"); c.row_factory = sqlite3.Row
print("=== phien: token nap moi luot (last_input_tokens) + so lan nen ===")
for r in c.execute("""select id, title, engine, model, msg_count, last_input_tokens, compact_count, updated_at
                      from sessions where last_input_tokens > 0 order by last_input_tokens desc limit 10"""):
    print(f"{r['id'][:8]} {r['engine'] or '?':16s} tin {r['msg_count']:3d}  nap/luot {r['last_input_tokens']:>9,}  nen {r['compact_count']}  "
          f"{datetime.datetime.fromtimestamp(r['updated_at']).strftime('%d/%m %H:%M')}  {(r['title'] or '')[:40]}")

rt = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\runtime.db"); rt.row_factory = sqlite3.Row
print("\n=== runtime_tasks cols ===")
print([d[1] for d in rt.execute("PRAGMA table_info(runtime_tasks)")])
