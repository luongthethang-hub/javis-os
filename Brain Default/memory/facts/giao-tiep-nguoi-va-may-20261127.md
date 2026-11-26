---
slug: giao-tiep-nguoi-va-may-20261127
title: Chuẩn giao tiếp hai chiều (người-model, model-model) chốt 27/11/2026
type: fact
memory_tier: T1
provenance: owner-instruction
evidence: E1
created: 2026-11-27
updated: 2026-11-27
decay_days: 365
tags: [fact, giao-tiep, chuan-hoa, lien-minh]
source: "chat web 27/11/2026 00:2x (L0: cách giao tiếp với tôi đang có vấn đề)"
---

# Chuẩn giao tiếp hai chiều

L0 chỉ ra lượt trả lời đang sai cách giao tiếp ở cả hai chiều. Chốt cách làm từ 27/11.

## Chiều model -> người (L0)

1. Câu đầu là kết quả hoặc việc đã làm được, không phải quá trình.
2. Không kể lại log tool. Chỉ đưa bằng chứng khi nó quyết định kết luận.
3. Thiếu dữ kiện hoặc bị chặn thì nói thẳng cái gì thiếu, ở đâu, ai gỡ, mất bao lâu.
4. Một việc một khối: Kết quả, Bằng chứng, Còn dở, Bước tiếp.
5. Không hứa "sẽ báo lại". Chỉ nói việc đã đặt vào hàng chờ hay chưa.

## Chiều model -> model (gói việc)

1. Gói việc là hợp đồng: mục tiêu, đầu vào đọc được, phạm vi tệp, lệnh nghiệm thu, tiêu chí đỏ-xanh.
2. Không đưa lời dặn chung chung ("làm cho tốt"). Tiêu chí phải là lệnh chạy được và phải xanh.
3. Thợ chỉ nhận văn bản, không có công cụ: cấm đòi thợ tự chạy lệnh hay tự đọc tệp.
4. Kết quả trả về đúng hai khối: ```diff (áp được lên rev ghi trong gói) và ```text (tự kiểm + phần chưa làm được).
5. Tiêu chí nghiệm thu phải tự kiểm trên bản clone tại đúng rev trước khi giao; tiêu chí không đạt được trên rev đó thì phải sửa gói, không được để thợ trượt.

## Đã kiểm chứng 27/11

Gói HC-20261127-002 dùng lệnh `pytest tests -q` làm tiêu chí, nhưng tại rev 6b9277a bộ test đã đỏ sẵn 4 ca (`test_lock_3a2_chat_commands`, `test_policy`, `test_step4_failover`, `test_step5_claude_allowlist`). Nghĩa là mọi bản nộp đều trượt, lỗi ở gói chứ không ở thợ.
