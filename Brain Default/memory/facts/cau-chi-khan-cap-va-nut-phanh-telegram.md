---
slug: cau-chi-khan-cap-va-nut-phanh-telegram
title: Cơ chế Cầu chì Khẩn cấp và Phanh Đột ngột từ xa qua Telegram
type: fact
created: 2026-11-24
updated: 2026-11-24
tags: [architecture, watchdog, emergency_stop, telegram, kill_switch, hard_reset]
source: chat 2026-11-24
---

# Cơ chế Cầu chì Khẩn cấp & Nút Phanh Đột ngột từ xa qua Telegram

Đã thiết lập và kiểm chuẩn thành công cơ chế 2 lớp phanh khẩn cấp cho toàn bộ hệ thống Javis & Liên minh AI:

## Lớp 1: In-Band Phanh Trực tiếp trên Gateway Javis Bot
- Nâng cấp `_tg_command` trong `server/main.py`: Nhận diện `/stop`, `/panic`, `/phanh`.
- Khi gõ lệnh: Lập tức `cancel_all` subprocess của phiên chat, thực hiện `taskkill /F /IM node_repl.exe` và `taskkill /F /IM antigravity.exe` để giải phóng bộ nhớ RAM và CPU bị kẹt.
- Phục hồi lại trạng thái rảnh tay cho chat trong vòng < 1 giây.

## Lớp 2: Out-of-Band Watchdog Daemon Độc lập (Khi Javis đơ toàn phần)
- Vị trí: `Javis/watchdog/emergency_watchdog.py` và script khởi chạy `Javis/watchdog/run_watchdog.bat`.
- Bộ lắng nghe độc lập chạy trực tiếp bằng Python thuần và `psutil`, hoàn toàn không qua LLM, không load context.
- Các lệnh điều khiển độc quyền (chỉ Thắng Lee ID `1894254685` và Group `-1004479278576`):
  - `/panic` hoặc `/phanh`: Chém sạch các CLI process con bị treo, giữ lại Server 7777.
  - `/hard_reset` hoặc `/reset_all`: Chém sạch các process treo, hạ server cổng 7777 và gọi restart lại toàn bộ.
  - `/ram` hoặc `/stat`: Trả về ngay lập tức % CPU, % RAM và Top 5 tiến trình chiếm RAM.
