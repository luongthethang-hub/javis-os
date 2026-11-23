---
slug: kien-truc-chong-phinh-to-rule-registry-va-task-envelope
title: Kiến trúc chống phình to bộ não: Rule Registry và Task Envelope
type: fact
created: 2026-11-23
source: inbox/telegram/Mã hóa giảm dung lượng.txt
tags: [architecture, rule-registry, task-envelope, prompt-bloat, second-brain, alliance]
---

# Kiến trúc chống phình to bộ não (Prompt Bloat Prevention)

Đúc kết từ tài liệu phân tích kỹ thuật của Sếp Thắng (`Mã hóa giảm dung lượng.txt`) ngày 23/11/2026.

## 1. Bản chất vấn đề
- Thói quen nhồi nhét quy tắc liên tục vào Kernel/System Prompt khiến context phình to, lãng phí token, tăng độ trễ và xung đột chỉ dẫn.
- Nguyên tắc cốt lõi: Không nhớ mọi thứ trong System Prompt. Chuyển sang mô hình: **Control Plane ổn định + Just-in-time Context Retrieval**.

## 2. Mô hình phân tầng 4 lớp
- **Tầng 0 (Core Kernel):** Rất nhỏ, ổn định; chỉ giữ danh tính, mục tiêu, ranh giới an toàn T0, quyền hạn, format bắt buộc. Giữ trần <= 18.000 bytes.
- **Tầng 1 (Router / Dispatcher Matrix):** Bảng định tuyến nhiệm vụ sang skill/agent phù hợp kèm trigger và ngân sách token.
- **Tầng 2 (Rule Registry & Skill Modules):** Mã hóa quy tắc thành ID có cấu trúc (YAML/JSON: `id`, `scope`, `trigger`, `priority`, `constraints`, `fallback`, `tests`). Chỉ nạp khi khớp trigger.
- **Tầng 3 (Knowledge / Memory / Task Envelope):** Lưu trữ ngoài context (SQLite, Facts, JSONL), nạp theo Task Envelope chuẩn hóa.

## 3. Vòng đời bảo trì 6 bước (MDACPT)
1. **Merge:** Gộp các rule trùng mục đích.
2. **Demote:** Chuyển chi tiết ít dùng từ Kernel xuống Skill/Rule riêng.
3. **Archive:** Đưa rule cũ sang deprecated, không xóa hẳn.
4. **Compress:** Rút gọn thành checklist, bảng quyết định hoặc schema ngắn.
5. **Prune:** Loại bỏ rule/skill không còn giá trị sau các chu kỳ audit.
6. **Test:** Kiểm thử hồi quy không làm vỡ các ca sử dụng cốt lõi.
