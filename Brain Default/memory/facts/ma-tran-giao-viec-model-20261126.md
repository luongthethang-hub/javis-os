---
slug: ma-tran-giao-viec-model-20261126
title: Ma trận giao việc G1-G9 cho đội model (26/11/2026)
type: project
memory_tier: T2
provenance: darklord-distilled
evidence: E2
created: 2026-11-26
updated: 2026-11-26
decay_days: 30
tags: [fact, ma-tran, giao-viec, model, codex, antigravity, deepseek, cam-os]
source: "project-files cam-van-hanh/ma-tran-giao-viec-20261126.md (~17:25); teacher-agent/so-van-hanh-darklord.md (21:25, 22:45)"
---

# Ma trận giao việc G1-G9 cho đội model

## Ai gọi được
- DR Doctor Agent (Claude): sẵn sàng. Lưu ý: từ 18:35 quyền ghi CAM OS thuộc thread tái cấu trúc, xem [[quyet-dinh-l0-20261126]].
- AG Antigravity `agy` 1.5.18: gọi được. Lệnh an toàn: `agy -p - --output-format json --sandbox --mode plan --model <ghi rõ> --print-timeout 180s`. Headless không được duyệt công cụ, chỉ giao việc sinh văn bản.
- CX Codex CLI 0.172.0: KHÔNG gọi được (refresh token bị thu hồi, kiểm lại 22:40 vẫn vậy). Lệnh soát luôn có `-s read-only`.
- DS DeepSeek Harness `dsh` 0.2.2-rc.5: KHÔNG gọi được (MISSING_CREDENTIAL, kiểm lại 22:40 vẫn vậy).

## Luật áp dụng
- Thợ khác chỉ quét, soạn bản vá trên bản sao, viết test, soát diff; bên giữ quyền ghi duyệt rồi mới áp.
- Chưa có cổng S (`sgate.py`) nên lọc tay: model hosted chỉ nhận mã nguồn và diff (S1).
- Việc D3 trở lên: người soát khác hãng người viết (Blue Claude thì Red CX hoặc AG; Blue AG thì Red DR hoặc CX).
- Việc tay chân giao AG với model rẻ `gemini-3.8-flash-*`; DS sau khi có key, ngoài giờ cao điểm (08-11h, 13-17h VN, T2-T6).

## Gói việc
- G1 chặn lỗi Codex #1-#6 (D5, R=3): Blue DR (Opus), AG quét shell/subprocess, Red CX. L0 duyệt Impact Preview.
- G2 từ chối prop_5e5e1f1e (D1): đường reject có sẵn, L0 gõ mã 6 ký tự.
- G3 bộ đếm chi phí V7 (D3): Blue DR (Sonnet), DS bảng giá, AG viết test.
- G4 cổng S `sgate.py` (D4, R=2): Blue DR (Opus), AG sinh mẫu S0-S3 GIẢ, Red CX.
- G5 rò rỉ cô lập test (D3): AG soạn vá trên bản sao, DR duyệt.
- G6 U1 khung chat (D3): AG soạn UI trên bản sao, DR duyệt, CX soát; nghiệm thu bằng ảnh chụp.
- G7 U0 đo thói quen chat (S2, D2): DR, script cục bộ, chỉ xuất số tổng hợp.
- G8 tìm kết quả chưng cất góp ý (S2, D1): DR.
- G9 soát khác hãng lượt 2 (D3): CX + DS song song, AG dự phòng, sau G1-G5.

## Thực tế lúc 21:25 26/11
- AG đã sinh văn bản: `ag_G1_scan.md` (gemini-3.8-flash-low), `ag_G5.patch` (133 passed trên bản sao), `ag_G6.patch` (133 passed; lỗi nút Copy bị disabled vĩnh viễn; chưa thử IME Telex). Bản chép ở `teacher-agent/ban-va-ag-20261126/`. Chưa áp vào repo CAM thật.

## Rủi ro mở (chờ L0)
- `bridge.py` đưa tin Telegram thẳng vào `agy --dangerously-skip-permissions`, không sandbox; L0 chấp nhận 18:07. bridge chạy trùng 2 tiến trình (Run key + Startup), Telegram 409.
- Codex `config.toml` mặc định danger-full-access.

Liên quan: [[ban-giao-darklord-20261126]], [[luat-phong-giam-doc-20261126]], [[cam-os-v4-antigravity-20261126]].
