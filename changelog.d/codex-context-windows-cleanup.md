### Fixed

- Close every SQLite connection in the Codex context regression before Windows removes its temporary database, preventing `WinError 32` after otherwise successful checks.
