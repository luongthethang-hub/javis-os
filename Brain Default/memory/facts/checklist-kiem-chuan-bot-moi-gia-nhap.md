---
type: technical
provenance: agent
origin: antigravity-bridge
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23 (9bb9fbc4)
superseded_by: cam-ket-t0-chong-loi-bot-moi-cam-lang
superseded_at: '2026-11-24'
status: superseded
---
Lý do gốc bot mới không chat được: Bot mới tạo luôn có Group Privacy bật mặc định (không đọc được tin nhắn thường nếu không tag hoặc không gõ slash command), tiến trình chạy nền chưa có watchdog tự hồi sinh, và script chưa qua Shadow Test 2 chiều. BẮT BUỘC thực hiện đủ 4 bước kiểm chuẩn hạt nhân trước khi công bố bot sẵn sàng: (1) Cấu hình BotFather: Cài commands /<botname> và hướng dẫn tắt Group Privacy nếu cần nghe cả nhóm; (2) Tích hợp Windows Watchdog/Service tự động hồi sinh khi restart máy; (3) Shadow Verification: Tự động gửi 1 tin chào vào group và 1 tin test phản hồi 2 chiều có log PASS; (4) Chỉ báo hoàn tất khi bot thực sự phản hồi được trong group.
