---
type: system
provenance: agent
origin: antigravity-bridge
created: 2026-11-23
updated: 2026-11-23
---
Lỗi Antigravity CLI không thể kết nối lại sau khi cập nhật Javis bắt nguồn từ 2 nguyên nhân gốc: (1) kiem_tra_nhanh() trong antigravity_cli.py chạy agy prompt mà không gán cwd=tempfile.gettempdir(), khiến agy quét toàn bộ workspace git JavisOS nặng >2GB làm trễ >60s và chạm trần TimeoutExpired; (2) _AUTH_CACHE chỉ lưu trong RAM khiến sau khi restart/update cache bị rỗng, trả về connected=False. Đã vá triệt để bằng cách cô lập cwd chạy agy về tempdir (giảm thời gian từ 60.35s xuống 7.9s) và lưu persistent cache ra agy-auth-cache.json.
