---
type: technical
provenance: agent
created: 2026-11-27
updated: 2026-11-27
---
# Chia sẻ Ảnh Telegram Đa Phương Thức Toàn Liên Minh (Shared Media Inbox)

- Mọi ảnh Sếp Thắng gửi qua Telegram (cả dạng nén Photo lẫn tệp ảnh gốc Document `image/*`) được tự động tải về thư mục dùng chung toàn Liên minh: `C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus\media_inbox\` (tối đa 20 MB/ảnh).
- Javis OS đã hỗ trợ sẵn nhận ảnh & album qua Telegram (`server/telegram_bot.py` + `image_vision.py`).
- Antigravity Telegram Bridge (`bridge.py`) đã nâng cấp tự tải ảnh vào `media_inbox` và truyền thẳng đường dẫn + chú thích để đọc bằng `read_file`.
- Mọi thành viên Liên minh (Antigravity, Javis, DeepSeek Desktop, CAM, Claude) đều có thể đọc cùng một tệp ảnh từ `media_inbox` khi phối hợp xử lý yêu cầu của Sếp.
