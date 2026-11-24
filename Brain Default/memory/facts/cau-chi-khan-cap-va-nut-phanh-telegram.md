---
slug: cau-chi-khan-cap-va-nut-phanh-telegram
title: Cơ chế Cầu chì Khẩn cấp và Phanh Đột ngột từ xa qua Telegram
type: decision
memory_tier: T1
created: 2026-11-24
updated: 2026-11-24
status: verified
tags: [architecture, watchdog, emergency_stop, telegram, kill_switch, hard_reset]
source: chat 2026-11-24 (merged cau-chi-khan-cap-va-hard-reset-telegram)
---

# Cơ chế Cầu chì Khẩn cấp & Nút Phanh Đột ngột từ xa qua Telegram

Đã thiết lập và kiểm chuẩn cơ chế 2 lớp phanh khẩn cấp (In-Band + Out-of-Band Kill-Switch) cho toàn bộ hệ thống Javis & Liên minh AI nhằm xử lý triệt để tình huống bão hòa RAM, tắc hàng đợi hoặc tiến trình CLI con treo.

## Lớp 1: In-Band Phanh Trực tiếp trên Gateway Javis Bot
- Nâng cấp `_tg_command` trong `server/main.py`: nhận diện `/stop`, `/panic`, `/phanh`.
- Khi gõ lệnh: lập tức `cancel_all` subprocess của phiên chat, thực hiện `taskkill /F /IM node_repl.exe` và `taskkill /F /IM antigravity.exe` để giải phóng RAM và CPU bị kẹt.
- Phục hồi lại trạng thái rảnh tay cho chat trong vòng < 1 giây.

## Lớp 2: Out-of-Band Watchdog Daemon Độc lập (Khi Javis đơ toàn phần)
- Vị trí: `Javis/watchdog/emergency_watchdog.py` và script khởi chạy `Javis/watchdog/run_watchdog.bat`.
- Tiến trình mỏng chạy Python thuần và `psutil` (< 15 MB RAM), hoàn toàn không nạp LLM/context/prompt.
- Các lệnh điều khiển độc quyền (chỉ Thắng Lee ID `1894254685` và Group `-1004479278576`):
  - `/panic`, `/stop` hoặc `/phanh`: cắt sạch các CLI process con bị treo, giữ lại Server 7777.
  - `/hard_reset`, `/reset`, `/reboot` hoặc `/reset_all`: cắt sạch các process treo, hạ server cổng 7777 và khởi động lại toàn bộ trong ~3 giây.
  - `/ram`, `/stat` hoặc `/status`: trả về ngay telemetry % CPU, % RAM và Top 5 tiến trình chiếm RAM.
