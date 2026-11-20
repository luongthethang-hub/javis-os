---
bump: patch
title: Fix Codex context test cleanup on Windows
---
## vi
### Sửa lỗi
- Đóng mọi kết nối SQLite trong kiểm tra hồi quy ngữ cảnh Codex trước khi Windows xoá cơ sở dữ liệu tạm, tránh lỗi `WinError 32`.
- Kiểm tra thay đổi GitHub theo nhánh gốc của remote đang theo dõi, tránh so nhầm repository và báo diff cực lớn. Kiểm tra hồi quy chạy được trên Windows mà không cần Bash.

## en
### Fixed
- Close every SQLite connection in the Codex context regression before Windows removes its temporary database, preventing `WinError 32` after otherwise successful checks.
- Grade GitHub changes against the tracked remote's base instead of an unrelated repository, avoiding enormous false diffs. Run the regression checks on Windows without requiring Bash.
