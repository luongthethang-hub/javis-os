---
slug: ban-giao-darklord-20261126
title: Bàn giao phiên điều phối CAM sang dự án CLAUDE - Darklord (26/11/2026)
type: reference
memory_tier: T2
provenance: owner-request
evidence: E2
created: 2026-11-26
updated: 2026-11-26
decay_days: 90
tags: [fact, cam-os, darklord, doctor-agent, teacher-agent, ban-giao]
source: "teacher-agent/ban-giao-darklord-20261126.md (26/11 ~17:00)"
---

# Bàn giao phiên điều phối CAM sang dự án CLAUDE - Darklord

Thực tế tính đến 26/11/2026 ~17:00: L0 cho chuyển toàn bộ nội dung phiên điều phối (25/11 21:32 đến 26/11 16:55) sang dự án Darklord. Bản đầy đủ: `teacher-agent/ban-giao-darklord-20261126.md`. Số liệu bên dưới là Doctor Agent tự báo (E2) và Teacher chấm (E3), chưa được Javis chạy lại.

## Hệ đã dựng
- Plugin `cam` v1.1.0: 8 skill CAM tiếng Anh, có CUP-20261126-01.
- Dự án "Claude - Teacher Agent": huấn luyện viên đa hệ, kế hoạch v0.1.1 (L0 duyệt lô A kèm 4 sửa).
- Dự án "Claude - Doctor Agent": bác sĩ cứu hộ, bệnh nhân hiện tại CAM OS, giám sát theo tiêu chí V1-V8 (`teacher-agent/tieu-chi-giam-sat.md`).
- Nhóm Javis "Hội đồng Huấn luyện - Teacher Agent" (8 trợ lý). Lệnh dispatch từ phiên ngoài bị Javis chặn vì không có danh tính.

## Luật L0 ban hành trong phiên
1. Giao việc trước, làm sau; không ôm việc.
2. Cổng chất lượng cho mọi model: tiêu chí nghiệm thu cố định trước khi giao, test trước khi nộp, soát chéo khác hãng, "xong" khác "đạt", lỗi lặp 2 lần thì hạ vai, L0 nghiệm thu cuối.
3. Giám sát phải theo tiêu chí cụ thể (V1-V8; V8 là "khối u": thứ mọc ngoài kế hoạch).
4. Báo cáo bằng điểm /100.
5. Thiết kế theo cách người dùng thật sự dùng (`teacher-agent/ux-khung-chat.md`).
6. CAM Company / CAM Corporation đã bị L0 dừng hẳn.

## CAM OS: bệnh và điều trị
- Nguyên nhân "càng sửa càng hỏng": Hội đồng v3.2.0 cho Claude + DeepSeek tự ghi code 13 lần, test cũ ghi đè `brains/` và `config/` thật, không có git, không test bật CAM thật, 3 bên sửa chồng.
- Đã chữa từng bước, mỗi bước 1 commit (P0 git e0b1c6f đến V8 gốc d3c1b9d). Điểm CAM 24 -> 71 -> 80 (12:15); lần đo 18:09 là 72/100 vì CAM tắt (V1 đỏ).
- Cổng S (`cam_core/sgate.py`) L0 đã duyệt, chưa làm; bắt buộc có trước khi bật agent thứ hai.

## Nguồn model (giá kiểm 26/11)
- ShopDonk (OpenAI-compatible, 120 req/phút, 5 luồng): gpt-6-luna, gpt-5.6-sol, grok-4.7, deepseek-v4.1-flash, gemini-flash-3.8-high, claude-sonnet-4-6 (không tool call).
- apikey.fan là relay trả phí; key nằm trong vault CAM (DPAPI).
- Claude Opus 5.5 4/20 USD/MTok, Sonnet 5.5 2/10, Haiku 5.5 0,10/0,50; DeepSeek V4-Pro 0,66/1,98 giờ thấp điểm, V4.1-Flash 0,15/0,60.

## Việc L0 tự làm còn mở (tại 12:35, chưa kiểm lại)
- Key ShopDonk cũ còn nguyên văn trong log hội thoại Javis ngày 25/11; L0 chọn "để sau". Cách đổi: tạo key mới, nhập Javis, setx, rồi hủy key cũ. Không đọc hay chép lại file log đó.
- Key DeepSeek cho dsh; biến SHOPDONK_API_KEY.

## Bài học kèm theo
`teacher-agent/bai-hoc.jsonl`: GT-PHOIHOP-001/002, GT-CODE-001..003, GT-CAMOS-001/002, GT-TEST-ISO-001, GT-SELFMOD-001, GT-V8-001.

Liên quan: [[quyet-dinh-l0-20261126]], [[luat-phong-giam-doc-20261126]], [[so-cai-he-log-chung]], [[ma-tran-giao-viec-model-20261126]].
