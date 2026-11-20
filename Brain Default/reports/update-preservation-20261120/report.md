# B?o c?o b?o to?n tinh ch?nh sau c?p nh?t

Th?i ?i?m ki?m ch?ng: 2026-11-20 21:55 UTC+7
Repo: `C:/Users/Admin/JavisOS`
Branch: `feat/ai-company-reliability-local-20261119`

## Hai stash b?t bi?n

- Stash c? `stash@{1}`: `b062994a541d2bb362a836a0811d81eebac92d94`, base `7e9c2ec683ed99f777ac8b6dedc305fd797f0675`.
- Stash m?i `stash@{0}`: `31cc1a77fc1e2bf52fa751e1c0d978717fb665e9`, base `fe6c74c50e7cb55628e3276318a2e6b5bf83b578`.
- C? hai v?n c?n nguy?n sau ki?m th?. Kh?ng pop, drop, reset hay clean c?y th?t.
- B?n v? sao l?u: `stash-1.patch`, `stash-0.patch`.
- Ki?m k? m?y ??c ???c c?a to?n b? 87 hunk: `hunk-inventory.json`; b?n ??c tay: `hunk-inventory.md`.

## ??i chi?u theo th? t? c? r?i m?i

### Stash c?

- ?? t?ch h?p t??ng th?ch: `server/codex_models.py`, `server/team_runner.py`, `server/team_store.py`, `server/workflow_graph.py`.
- `server/main.py`: kh?ng ch?p ??. C?c hunk Codex catalog, workflow contract, supplied-data workflow v? team fallback ?? c? ho?c ???c c?y hi?n t?i m? r?ng. B?n ??i chi?u gi? t?i `stash-1-main.diff`.
- `server/engine_down_notified.json`: lo?i tr? v? l? tr?ng th?i runtime.

### Stash m?i

- ?? t?ch h?p t??ng th?ch: `server/compaction.py`, `server/sessions.py`, `server/telegram_bot.py`, `server/video_vision.py`, `tests/python/test_claude_cli_moi_lai_mach.py`, `tests/python/test_compaction.py`.
- `server/aux_engine.py`: hunk ??ng async stream giao v?i lifecycle engine hi?n t?i, kh?ng ?p nguy?n hunk ?? tr?nh h? c?p.
- `server/main.py`: c?c hunk compaction handover, Telegram video, workflow execution guard v? stream closure ?? c? b?n m?i h?n ho?c ?? t?ch sang module chuy?n tr?ch. Kh?ng ?p ??. B?n ??i chi?u gi? t?i `stash-0-conflicts.diff`.
- `server/engine_down_notified.json`, `server/mcp-stdio-pids.json`: lo?i tr? v? l? tr?ng th?i runtime.

K?t qu? ki?m k? hunk: 36 hunk c?n nguy?n v?n, 5 hunk ?? t?ch h?p nh?ng ti?n h?a, 43 hunk trong hai file xung ??t ?? ???c t?nh n?ng hi?n t?i thay th? ho?c c?n quy?t ??nh ri?ng, 3 hunk runtime b? lo?i tr?. Kh?ng c?n hunk t??ng th?ch n?o ?? x?c ??nh nh?ng ch?a t?ch h?p.

## C? ch? ?? tri?n khai v?o ???ng update th?t

- `server/update_preservation.py`: snapshot ngo?i checkout trong `STATE_DIR/update-preservation`, manifest c? intent, SHA-256, base commit v? stash OID; merge ba chi?u t?ng file; transaction to?n b?; rollback khi ghi l?i; artifact v? b?o c?o xung ??t.
- Ch?n path traversal, symlink, secret-like path v? runtime JSON. Snapshot ch? l? d? li?u, kh?ng import hay th?c thi script.
- `server/updater.py`: t?o snapshot tr??c stash, bind snapshot v?i OID, ph?c h?i sau merge release v? sau rollback.
- L?i `bind_snapshot` sau khi stash ?? t?o kh?ng l?m updater ch?t: ghi log v? gi? Git stash l?m backup.
- Nh?nh merge release l?i gi? stash qua `start_server` v? `poll_health` c?a server c?. Ch? drop khi server c? healthy, n?n kh?ng m?t backup n?u server c? c?ng h?ng.
- `tests/python/test_update_preservation.py`: c?p nh?t kh?ng xung ??t v? gi? ch?c n?ng m?i, xung ??t kh?ng s?a c?y, l?i ghi th?t sau file ??u ti?n th? rollback to?n transaction, add/delete, integrity, runtime exclusion v? protected paths.
- `tests/python/test_updater_stash.py`: stash th?t, xung ??t, rollback, l?i bind manifest v? merge l?i v?i server c? unhealthy.
- `changelog.d/update-preservation.md`: changelog c?a thay ??i.

## B?ng ch?ng ki?m th? tr?c ti?p

Ch?y ri?ng t?ng script b?ng `python -X utf8`, kh?ng d?ng unittest discovery:

- `test_update_preservation.py`: PASS.
- `test_updater_stash.py`: PASS.
- `test_updater_merge.py`: PASS, g?m merge s?ch, merge xung ??t ???c abort, fetch l?i v? detached HEAD.
- `test_compaction.py`: PASS.
- `test_claude_cli_moi_lai_mach.py`: PASS.
- `py_compile server/update_preservation.py server/updater.py`: PASS.
- `git diff --check` cho c?c file c? ch? v? test: PASS, ch? c? c?nh b?o CRLF hi?n h?u.
- Hai stash ???c ki?m tra l?i sau to?n b? test v? v?n ??ng hai OID tr?n.

## An to?n v? ho?n t?c

- Kh?ng s?a ho?c ch?y `computer-use-guard.ps1`, kh?ng t?ng quy?n, kh?ng kh?i ph?c patch v? hi?u ch?nh s?ch plugin, kh?ng d?ng app kh?c, kh?ng push, restart hay update app.
- Kh?ng ??a secret, database ho?c runtime JSON v?o c? ch? hay changelog.
- Ho?n t?c c? ch?n l?c: kh?i ph?c ri?ng hunk `server/updater.py` t? Git, x?a `server/update_preservation.py`, `tests/python/test_update_preservation.py`, `changelog.d/update-preservation.md`, v? ho?n t?c hunk test m?i trong `tests/python/test_updater_stash.py`. Kh?ng d?ng `git reset --hard` tr?n c?y th?t.
- Hai stash OID v? hai patch trong th? m?c n?y l? l?p ph?c h?i ??c l?p.
