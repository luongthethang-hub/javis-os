---
type: decision
created: 2026-11-24
updated: 2026-11-24
source: chat 2026-11-24 (02:00)
status: superseded
superseded_by: cau-chi-khan-cap-va-nut-phanh-telegram
superseded_at: '2026-11-24'
---
# Cơ chế Cầu chì Khẩn cấp và Hard Reset Ngoại vi (Out-of-Band Kill-Switch)

## Bối cảnh & Nguyên nhân gốc rễ
Khi Javis bị quá tải (bão hòa RAM, hàng đợi tắc, hoặc tiến trình con CLI chạy vòng lặp ngầm), chính luồng nhận diện tin nhắn của Javis bị block. Tin nhắn gửi qua bot Javis lúc đó bị xếp hàng chờ, khiến Sếp Thắng không thể phanh hay can thiệp từ xa.

## Quyết định Kỹ thuật
Thiết lập tiến trình giám sát ngoại vi độc lập (Watchdog Daemon) hoàn toàn tách rời khỏi Javis Core Server:
- **Tiến trình mỏng:** Python thuần (`urllib`/`requests`), tiêu tốn dưới 15 MB RAM, không nạp LLM/context/prompt.
- **Quyền hạn độc quyền:** Chỉ lắng nghe chỉ thị từ Telegram cá nhân Sếp Thắng (`chat_id: 1894254685`).
- **Các mức can thiệp:**
  - `/panic` hoặc `/stop`: Phanh cấp độ 1, lập tức `taskkill` các tiến trình CLI con (`antigravity.exe`, `node_repl.exe`, sub-task treo), giải phóng RAM mà không tắt Javis Core Server.
  - `/reset` hoặc `/reboot`: Phanh cấp độ 2, dọn sạch tiến trình con và khởi động lại Javis Core Server (cổng 7777) trong vòng 3 giây.
  - `/status`: Trả về ngay telemetry CPU, RAM và danh sách tiến trình đang chiếm dụng tài nguyên.
