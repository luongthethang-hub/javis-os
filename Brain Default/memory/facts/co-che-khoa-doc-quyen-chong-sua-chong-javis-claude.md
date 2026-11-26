---
slug: cam-co-che-khoa-doc-quyen-chong-sua-chong
title: Cơ chế khóa độc quyền A2A Lock chống sửa chồng việc giữa Javis và Claude
type: fact
memory_tier: T1
provenance: owner-request
evidence: E1
created: 2026-11-26
updated: 2026-11-26
decay_days: 365
tags: [fact, lien-minh-ai, a2a-bus, security, lock, tien-hoa]
source: chat 2026-11-26 (6b38d862)
---

# Cơ chế khóa độc quyền chống sửa chồng việc (A2A Mutual Exclusion Lock)

Chỉ thị L0 ngày 26/11/2026: Trước khi Javis can thiệp vào mã nguồn hoặc nhận việc thay Claude, bắt buộc thực hiện tiền kiểm 3 tầng (Triple-Check):

1. **Heartbeat Activity Guard:** Quét tệp hội thoại `.jsonl` trong `~/.claude/projects/`. Nếu có ghi nhận tương tác trong vòng **5 phút** (`diff_sec < 300s`) -> Xác định Claude đang làm việc tích cực -> **Javis lập tức tạm dừng, nhường quyền tuyệt đối, không can thiệp**.
2. **Sổ Cái State Lock:** Kiểm tra trạng thái khóa `khoa-ghi:cam-os`. Nếu Claude đang giữ (`dang-giu`) và chưa có lệnh nhượng quyền từ L0 -> Javis chỉ đọc/đo, không ghi.
3. **Branch Isolation & Handoff Receipt:** Khi Claude hết hạn mức và L0 duyệt Y cho Javis tiếp quản, Javis chỉ làm việc trên nhánh git riêng (`feature/*`), ghi nhận trạng thái vào Sổ Cái và để lại biên bản `res-handoff-*.md` trong `memory/a2a_bus/claude/` để Claude tiếp tục mạch công việc mà không làm lại từ đầu.
