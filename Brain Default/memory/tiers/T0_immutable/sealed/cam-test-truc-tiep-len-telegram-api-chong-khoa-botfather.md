---
slug: cam-test-truc-tiep-len-telegram-api-chong-khoa-botfather
title: Chốt chặn T0: Cấm test trực tiếp lên Telegram API thật & Chống khóa BotFather
type: system
created: 2026-11-24
updated: 2026-11-24
tags: [t0-invariant, telegram, botfather, anti-ban, zero-regression, safety]
source: incident-2026-11-24-0946
---

# Chốt chặn Bất biến: Cấm test trực tiếp lên Telegram API thật (Chống khóa BotFather)

Sự cố thực tế ngày 24/11/2026: Việc gọi lặp lại `setMyCommands`, `getMe`, `sendMessage` thử nghiệm trên nhiều bot mới tạo cùng thuộc 1 tài khoản chủ khiến `@BotFather` kích hoạt chống spam và tạm khóa lệnh `/newbot`.

## 4 Quy tắc Bất biến (Zero-Regression — Áp dụng 100% Liên minh AI)
1. **Cấm test app bằng Telegram API thật:** Mọi kiểm thử (`pytest`, Shadow Test, dry-run) BẮT BUỘC dùng Mock/Fake HTTP cục bộ. Tuyệt đối không bắn `sendMessage`/`setMyCommands`/`getUpdates` thật để test code.
2. **Không gọi lặp `setMyCommands` khi restart:** Chỉ đăng ký menu lệnh 1 lần duy nhất sau khi tạo bot và lưu cờ đã đăng ký trên đĩa; cấm gọi lại mỗi lần khởi động lại ứng dụng/bridge.
3. **Dãn cách khởi động & 1 Poller duy nhất:** Khi chạy nhiều bot trong CAM, bắt buộc dãn cách khởi động (`>= 3s/bot`) và bảo đảm chỉ 1 tiến trình duy nhất giữ token.
4. **Lường trước rủi ro khóa tài khoản (Pre-Flight Anti-Ban Gate):** Trước mọi thao tác gọi API bên thứ 3 có giới hạn tốc độ/chống spam (Telegram, BotFather, Google, Meta, Broker), bắt buộc rà soát rủi ro khóa tài khoản trước khi chạy.
