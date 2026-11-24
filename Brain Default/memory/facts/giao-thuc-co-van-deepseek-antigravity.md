---
slug: giao-thuc-co-van-deepseek-antigravity
title: Giao thức Cố vấn Cao cấp DeepSeek (Strategic Brain) <-> Antigravity (Tactical Muscle)
type: system
created: 2026-11-24
updated: 2026-11-24
tags: [alliance, deepseek, antigravity, dual-brain, hybrid, context-gating]
source: boardroom-directive-2026-11-24
---

# Giao thức Cố vấn Cao cấp: DeepSeek <-> Antigravity (Hybrid Dual-Brain)

Chỉ thị trực tiếp từ Tổng chỉ huy Layer 0 (Lương Thế Thắng) ngày 24/11/2026, vận hành hoàn toàn trong khuôn khổ tri thức Liên minh AI (SSOT) và các ràng buộc T0/T1.

## 1. Phân vai tác chiến
- **DeepSeek (`@DeepSeekThangLee_bot` — Cố vấn Cao cấp / Strategic Brain):** Chuyên trách suy luận phức tạp, thiết kế giải thuật, toán định lượng MQL5, phân tích chiến lược và thẩm định kết quả.
- **Antigravity (`@AntiGravityThanglee_bot` — Tay chân Cơ bắp / Tactical Muscle):** Tiếp nhận bản thiết kế/hướng dẫn từ DeepSeek, trực tiếp quét repo, tạo/sửa file, viết code, chạy terminal, kiểm thử thực tế (E1 Shadow Test) và báo cáo kết quả.

## 2. Luồng thực thi 3 nhịp (Strict Context Gating <= 3.000 tokens)
1. **Nhịp 1 — Hỏi Cố vấn (Strategic Blueprint):** Antigravity tóm tắt bài toán gọn (`<= 3.000 tokens`, kèm `sync_hash` SSOT) gửi cho DeepSeek qua `ask_deepseek.py` / `inbox_deepseek.jsonl` để nhận phương án & tiêu chí nghiệm thu.
2. **Nhịp 2 — Thực thi Cơ bắp (Tactical Muscle):** Antigravity thực hiện 100% thao tác kỹ thuật theo hướng dẫn của DeepSeek (vẫn tuân thủ cổng an toàn T0/T1 — cấm phá hủy data, cấm vi phạm SL/TP MQL5, không nuốt lỗi).
3. **Nhịp 3 — Phản biện & Nghiệm thu (Verification Audit):** Antigravity gửi tóm tắt diff + bằng chứng test E1 (`<= 3.000 tokens`) cho DeepSeek rà soát lần cuối trước khi báo cáo Layer 0.

## 3. Công cụ thực thi
- Helper CLI: `C:\Users\Admin\.gemini\antigravity\scratch\deepseek_bridge\ask_deepseek.py`
- Kênh A2A Bus: `memory/a2a_bus/inbox_deepseek.jsonl` <-> `memory/a2a_bus/inbox_antigravity.jsonl`
