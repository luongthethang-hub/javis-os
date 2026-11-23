---
slug: onboarding-deepseek-thanh-vien-moi-lien-minh
title: Onboarding Thành viên mới DeepSeek (@DeepSeekThangLee_bot) vào Liên minh AI
type: fact
created: 2026-11-24
updated: 2026-11-24
tags: [alliance, deepseek, onboarding, telegram, qc-5, q5-cvm]
source: chat 2026-11-24 (1ea67e84)
---

# Onboarding Thành viên mới DeepSeek (@DeepSeekThangLee_bot)

Triển khai ngày 24/11/2026 theo Giao thức Kết nạp Đa tác tử (Mục 2.5) và Cam kết Hạt nhân T0.

## 1. Thông tin định danh & Kết nối kỹ thuật
- **Tên hiển thị:** DeepSeek - ThangLee (`@DeepSeekThangLee_bot`)
- **Telegram Bot ID:** `9085788595`
- **Ứng dụng Desktop trên máy:** `DeepSeek Harness.exe` (`C:\Users\Admin\AppData\Local\Programs\DeepSeek Harness\DeepSeek Harness.exe`)
- **Nhóm Telegram mục tiêu:** `Thắng Lee Group` (ID `-1004479278576`)

## 2. Kết quả Kiểm chuẩn T0 hạt nhân (E1)
1. **Xác thực Bot (`getMe`):** PASS (`id=9085788595`, `can_join_groups=True`, `can_read_all_group_messages=True` — Group Privacy đã tắt sẵn).
2. **Menu Lệnh (`setMyCommands`):** PASS — Đã đăng ký `/deepseek` và `/help`.
3. **Shadow Test Kênh riêng tư (DM Layer 0):** PASS (`message_id=10` gửi thành công tới ID `1894254685`).
4. **Shadow Test Nhóm (`Thắng Lee Group`):** CHỜ ADD GROUP (`400 chat not found` do bot chưa được thêm vào nhóm; sau khi Sếp Thắng add `@DeepSeekThangLee_bot` vào nhóm sẽ gửi tin chào nghiệm thu 2 chiều).

## 3. Định vị trong Ma trận QC-5 (Đang biểu quyết Q5-CVM `deepseek-positioning-20261124`)
- **Thế mạnh thực chứng:** Suy luận chuỗi sâu (Chain-of-Thought R1/V3), toán định lượng, tối ưu thuật toán MQL5/xác suất, chi phí token cực thấp (E: 9.0, C: 9.0).
- **Vùng cấm:** Không dùng cho phản hồi thời gian thực < 2s (nhường Flash).

## 4. Kết nối Liên minh AI Cục bộ (24/11/2026)
- deepseek-lead khởi tạo bộ tri thức liên minh tại `C:\Users\Admin\.dsh\ai-alliance\`.
- Do Telegram chặn bot-to-bot (`USER_BOT_TO_BOT_DISABLED`), hai bên thống nhất giao thức phong bì JSON v1 qua thư mục `inbox/` và HTTP nội bộ `127.0.0.1:7777`.
- Javis đã bắt tay chính thức qua `C:\Users\Admin\.dsh\ai-alliance\inbox\javis\to-deepseek-lead-0001.md`.
