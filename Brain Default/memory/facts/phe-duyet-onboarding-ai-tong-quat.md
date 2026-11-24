---
slug: phe-duyet-onboarding-ai-tong-quat
title: Quy chế Bắt buộc Onboarding & Đề xuất CUP cho Mọi Thành viên AI Mới
type: rule
memory_tier: T1
provenance: l0-approved
origin: antigravity-bridge
created: 2026-11-23
updated: 2026-11-24
status: verified
source: chat 2026-11-23 (9bb9fbc4, merged quy-che-onboarding-ai-tong-quat & quy-trinh-onboarding-ai-moi-va-cup-bat-buoc)
tags: [t1, onboarding, cup, qc-5, a2a-bus, alliance]
---

# Quy chế Bắt buộc Onboarding & Đề xuất CUP cho Mọi Thành viên AI Mới

Layer 0 (Thắng Lee) đã phê duyệt `Y`: mọi quy trình kết nạp bot/AI mới (Telegram bot, API model, CLI, Desktop bridge) đều BẮT BUỘC thực hiện đủ 4 bước chuẩn hóa:

1. **Phát đề xuất CUP ngay lập tức:** Sau khi tích hợp kỹ thuật thành công, gửi ngay đề xuất CUP (duyệt 1 ký tự `Y`) lên Telegram với tóm tắt 1-2 câu dễ hiểu về vai trò mới, lệnh gọi bot và ma trận san tải. Cấm hoàn tất âm thầm.
2. **Định vị vào Ma trận năng lực QC-5:** Ghi rõ thế mạnh thực chứng, vùng cấm và quy tắc san tải động.
3. **Cấp hòm thư A2A Bus:** Khởi tạo `memory/a2a_bus/<agent>/` và nạp toàn bộ quy chuẩn chung của Liên minh (Comprehension Filter, Zero-Fluff, Context Gating <= 3.000 tokens).
4. **Kích hoạt san tải động:** Kết nối vào cơ chế điều phối và kiểm chuẩn T0 trước khi bàn giao.
