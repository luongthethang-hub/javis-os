import sqlite3, datetime, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
now = datetime.datetime.now().timestamp()
c = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\runtime.db"); c.row_factory = sqlite3.Row
print("=== step dang RUNNING ===")
for r in c.execute("select id,provider,model,started_at from runtime_steps where status='RUNNING'"):
    print(r["id"][:14], r["provider"], r["model"], datetime.datetime.fromtimestamp(r["started_at"]).strftime("%H:%M:%S"),
          "tuoi_phut", round((now - r["started_at"]) / 60, 1))
print("\n=== turn_ledger ===")
try:
    cc = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\state\turn_ledger.sqlite3")
    print(cc.execute("select name from sqlite_master where type='table'").fetchall())
except Exception as e:
    print("err", e)
