---
type: fact
title: "[Liên minh] Giới hạn kỹ thuật: Telegram cấm bot nhắn bot"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/alliance_l0002_gioi_han_ky_thuat_telegra.md"
evidence: E2
cam_content_hash: 6a8095ba4cd480b1c51903b33a5afce113776b82a39596ebd100b254d2d94228
cam_bundle_hash: 34caca1411c0e585
---

# [Liên minh] Giới hạn kỹ thuật: Telegram cấm bot nhắn bot

---
slug: alliance_l0002_gioi_han_ky_thuat_telegra
title: [Liên minh] Giới hạn kỹ thuật: Telegram cấm bot nhắn bot
evidence: E2
source: cam-council
updated: 2026-11-26T23:34:16+07:00
tags: [alliance, bridge, connectivity, knowledge-sync, limits, telegram]
---

# [Liên minh] Giới hạn kỹ thuật: Telegram cấm bot nhắn bot

# Giới hạn kỹ thuật: Telegram cấm bot nhắn bot

## Điều đã kiểm chứng (2026-11-24)

Chủ sở hữu yêu cầu kết nối `deepseek-lead` với `javis` (@ThangLeeJavisBot).
Kết quả kiểm tra thực tế:

| Bước | Lệnh | Kết quả |
|---|---|---|
| Bot Javis có tồn tại | `getChat @ThangLeeJavisBot` | ✅ `id 8664216130`, tên "Javis - ThangLee" |
| Bot nhắn riêng bot | `sendMessage chat_id=8664216130` | ❌ HTTP 400, `USER_BOT_TO_BOT_DISABLED` |

**Kết luận:** Telegram Bot API không cho phép bot gửi tin nhắn trực tiếp cho bot khác, và
`getUpdates` cũng không chuyển tin từ bot sang bot. Đây là giới hạn của Telegram, không phải lỗi cấu hình.

## Các phương án khả thi

1. **Nhóm Telegram chung (cần chủ tạo nhóm + thêm cả 2 bot làm admin).**
   - Ưu: đơn giản, thấy được lịch sử, chủ sở hữu theo dõi được.
   - Nhược: không có xác thực mật mã; bot chỉ nhận tin nhóm khi là admin hoặc tắt privacy mode.
2. **Chạy chung trên một máy — dùng file trong `C:\Users\Admin\.dsh\ai-alliance\`.**
   - Ưu: đơn giản nhất, không lộ bí mật, không cần mạng.
   - Nhược: chỉ dùng được khi cả hai agent cùng máy (h
