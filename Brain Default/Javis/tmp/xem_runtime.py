import sqlite3, json, datetime
DB = r"C:\Users\Admin\JavisOS\server\runtime.db"
c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
tabs = [r[0] for r in c.execute("select name from sqlite_master where type='table'")]
print("TABLES", tabs)
for t in ("runtime_steps", "runtime_traces", "runtime_turns"):
    if t in tabs:
        cols = [d[1] for d in c.execute(f"PRAGMA table_info({t})")]
        n = c.execute(f"select count(*) from {t}").fetchone()[0]
        print(t, "rows", n, "cols", cols)
