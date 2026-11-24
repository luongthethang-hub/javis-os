---
slug: cam-ket-t0-chong-loi-bot-moi-cam-lang
title: Cam kết Hạt nhân T0 - Chống lỗi bot mới câm lặng khi gia nhập
type: rule
memory_tier: T0
provenance: l0-approved
origin: antigravity-bridge
created: 2026-11-23
updated: 2026-11-24
status: verified
source: chat 2026-11-23 (9bb9fbc4, merged checklist-kiem-chuan-bot-moi-gia-nhap)
tags: [t0, immutable, telegram, onboarding, nuclear-gate]
---

# Cam kết Hạt nhân T0: Chống lỗi bot mới câm lặng khi gia nhập

Lý do gốc bot mới không chat được: bot mới tạo luôn có Group Privacy bật mặc định (không đọc được tin nhắn thường nếu không tag hoặc gõ lệnh), tiến trình nền thiếu watchdog tự hồi sinh, và chưa qua Shadow Test 2 chiều.

**Quy tắc bất biến T0 (4 cổng bắt buộc trước khi bàn giao bot mới):**
1. **Cấu hình lệnh BotFather:** Cài đặt lệnh `/<botname>` tự động qua `setMyCommands` (chỉ 1 lần khi onboarding, không gọi lặp khi restart).
2. **Hướng dẫn tắt Group Privacy:** Cung cấp hướng dẫn tắt Group Privacy ngay trong phản hồi đầu tiên nếu bot cần nghe cả nhóm.
3. **Watchdog/Service tự hồi sinh:** Tích hợp Windows Watchdog/Service hoặc Alliance Bus Runner tự hồi sinh khi restart máy.
4. **Shadow Verification 2 chiều:** Thực hiện kiểm thử phản hồi thực tế có log PASS (áp dụng môi trường mock khi test tự động để tránh khóa BotFather). Nếu bot chưa phản hồi được thực tế, coi tác vụ THẤT BẠI và cấm báo hoàn thành.
