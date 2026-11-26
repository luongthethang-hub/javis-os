---
slug: quyet-dinh-l0-20261126
title: Quyết định của L0 ngày 26/11/2026 (relay V7, prop_5e5e1f1e, tái cấu trúc CAM OS, tắt Sync_4h)
type: fact
memory_tier: T1
provenance: owner-decision
evidence: E1
created: 2026-11-26
updated: 2026-11-26
decay_days: 365
tags: [fact, l0, quyet-dinh, cam-os, khoa-ghi, sync-4h]
source: "teacher-agent/quyet-dinh-L0-20261126.md; Sổ Cái quyet-dinh:sync4h-tat-20261126"
---

# Quyết định của L0 ngày 26/11/2026 (giờ VN)

Nguyên văn L0 nằm trong `teacher-agent/quyet-dinh-L0-20261126.md`. Mục 1-3 là cách hiểu của phiên điều phối Darklord từ hai tin ngắn ("Duỵet" 16:59:07, "router bật" 16:59:37); L0 chưa xác nhận lại từng mục.

1. Từ chối đề xuất `prop_5e5e1f1e` (theo khuyến nghị Doctor). Thực tế: chưa thao tác trong CAM; cần L0 gõ mã ở cổng bàn phím (`cam_approve.py`).
2. V7: GIỮ relay/router trả phí cho Claude trong CAM, không chuyển sang CLI gói Pro/Max. Hệ quả: bộ đếm chi phí V7 cần làm sớm.
3. Bật Auto memory cho Doctor Agent: cài đặt trên claude.ai, L0 tự bật.
4. 18:31: thread Darklord "Tái cấu trúc lõi CAM OS" được đọc, ghi, sửa toàn bộ `D:\AI AGENT\council-agent-manager`. Thay luật cũ "chỉ Doctor sửa code CAM OS" trong phạm vi tái cấu trúc.
5. Điều kiện kèm mục 4: trình bản thiết kế trước khi sửa lớn; nhánh git riêng, commit nhỏ; test cô lập, sao lưu trước; soát khác hãng nếu gọi được; ô V1-V5 đỏ thì lùi ngay; chỉ merge khi L0 nghiệm thu; không in key.
6. Khóa ghi: từ 18:35 Sổ Cái `khoa-ghi:cam-os = dang-giu` (thread tái cấu trúc giữ). Doctor và mọi bên khác chỉ đọc/đo cho tới khi khóa chuyển `da-tra`. Kiểm: `cd "D:\AI AGENT\so-cai" ; python -m so_cai lien-ket khoa-ghi:cam-os`.
7. 21:06: tiền kiểm 3 tầng trước khi Javis nhận việc thay Claude, xem [[cam-co-che-khoa-doc-quyen-chong-sua-chong]].
8. 22:42: tắt tác vụ `CAM_AITEP_Alliance_Sync_4h` đến khi chữa CAM xong. Thực tế lúc 22:49: tác vụ VẪN BẬT (lệnh /DISABLE bị bộ lọc quyền Claude Code chặn), lần chạy kế 27/11 01:34. L0 tự chạy `schtasks /Change /TN CAM_AITEP_Alliance_Sync_4h /DISABLE`; cách lùi `/ENABLE`.

Liên quan: [[ban-giao-darklord-20261126]], [[luat-phong-giam-doc-20261126]], [[cam-os-v4-antigravity-20261126]].
