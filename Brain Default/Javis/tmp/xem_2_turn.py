import sqlite3, datetime, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
c = sqlite3.connect(r"C:\Users\Admin\JavisOS\server\runtime.db"); c.row_factory = sqlite3.Row
for sid in ("rs_dbe21d5bffd74924b464b7ec58a2ce89", "rs_ebab45e0a1de4310bd34c975085a1f99"):
    rows = [dict(r) for r in c.execute("select * from runtime_events where step_id=? order by seq", (sid,))]
    print("==", sid[:14], "events", len(rows))
    if rows:
        t0 = rows[0]["created_at"]
        for r in rows:
            print(f"  +{r['created_at']-t0:7.1f}s", r["event_type"], str(r["payload_json"])[:160])
    st = c.execute("select * from runtime_steps where id=?", (sid,)).fetchone()
    print("  started", datetime.datetime.fromtimestamp(st["started_at"]).strftime("%H:%M:%S"),
          "status", st["status"], "uuoc", st["estimated_input_tokens"])
