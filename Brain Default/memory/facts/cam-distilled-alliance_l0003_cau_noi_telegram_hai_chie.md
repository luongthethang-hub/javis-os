---
type: fact
title: "[Liên minh] Cầu nối Telegram hai chiều của deepseek-lead"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/alliance_l0003_cau_noi_telegram_hai_chie.md"
evidence: E2
cam_content_hash: e4f457690fa350a9d94cdf2284097ec84565c0794b67a4f9f5913c973e6d7d45
cam_bundle_hash: 34caca1411c0e585
---

# [Liên minh] Cầu nối Telegram hai chiều của deepseek-lead

---
slug: alliance_l0003_cau_noi_telegram_hai_chie
title: [Liên minh] Cầu nối Telegram hai chiều của deepseek-lead
evidence: E2
source: cam-council
updated: 2026-11-26T23:34:16+07:00
tags: [alliance, bridge, infrastructure, knowledge-sync, telegram]
---

# [Liên minh] Cầu nối Telegram hai chiều của deepseek-lead

# Cầu nối Telegram hai chiều của deepseek-lead

## Thành phần

| Thành phần | Đường dẫn | Vai trò |
|---|---|---|
| Cấu hình | `C:\Users\Admin\.dsh\telegram-bridge\config.json` | token bot, chat id được phép |
| Bộ lắng nghe | `C:\Users\Admin\.dsh\telegram-bridge\bridge.js` | long-poll `getUpdates`, in tin nhắn rồi thoát để đánh thức agent |
| Gửi tin | `C:\Users\Admin\.dsh\telegram-bridge\send.js` | đọc file UTF-8, gọi `sendMessage` |
| Vị trí đã đọc | `C:\Users\Admin\.dsh\telegram-bridge\offset.json` | tránh xử lý trùng tin nhắn |

## Cách vận hành

1. Agent khởi chạy `bridge.js` như một background job.
2. Khi chủ nhắn tin, job in JSON chứa tin nhắn rồi thoát → agent được đánh thức.
3. Agent trả lời bằng `send.js`, sau đó khởi chạy lại `bridge.js` cho tin tiếp theo.
4. Job tự kết thúc sau 60 phút không có tin (idle) và được khởi chạy lại.

## Ranh giới

- Chỉ chấp nhận tin từ chat id `1894254685`; tin từ chat khác bị bỏ qua và ghi log stderr.
- Cầu nối chỉ sống khi DeepSeek Harness mở và phiên làm việc còn hiệu lực.
- Không dùng cơ chế này để nhận lệnh từ người khác.
