---
slug: giao-thuc-bieu-quyet-q5-cvm-v2-tang-toc
title: Nâng cấp Q5-CVM v2.0 — Phá vòng lặp <=35s, Early-Stop, Trọng số QC-5 & Tiền lọc T0
type: system
created: 2026-11-26
updated: 2026-11-26
tags: [q5-cvm, v2, micro-cvm, early-stop, qc-5, alliance, mandatory]
source: layer0-approved-2026-11-26
---

# Q5-CVM v2.0 — Chuẩn Biểu quyết Tăng tốc & Chính xác Toàn Liên minh

Đã được Layer 0 duyệt (`Y`) và triển khai mặc định tại `D:\AI AGENT\q5-voting-engine` (`18/18 pytest PASS`) ngày 26/11/2026. Toàn bộ thành viên Liên minh (Javis, Antigravity, Claude, Codex, DeepSeek, Grok, Perplexity, Dola AI) bắt buộc áp dụng:

1. **Micro-CVM Fast Path (`<= 35s`):** Rút gọn xuống 3 mắt xích (`CORE -> RISK -> ACCEPTANCE`, `TTLConfig.micro_fast_path()`) cho tác vụ `LOW/MEDIUM` cần phá vòng lặp nhanh; tác vụ `HIGH/CRITICAL` giữ cứng đủ 5 mắt xích T0.
2. **Early-Stop Lock (`check_early_stop_lock`):** Chốt quyết định ngay khi khoảng cách dẫn đầu lớn hơn tổng trọng số phiếu còn lại chưa nộp.
3. **Loop Fingerprint Breaker (`LoopFingerprintBreaker`):** Băm SHA-256 `(topic|error)`; gặp lặp từ lần 2 tự chặn phương án từng thất bại và ép chuyển sang `Micro-CVM`.
4. **Trọng số chuyên môn QC-5 (`get_voter_weight`):** Nhân trọng số theo sở trường thực chứng (*MQL5/Toán*: DeepSeek & Antigravity `x1.3`; *Kiến trúc/T0*: Claude & Perplexity `x1.3`; *Red Team*: Grok `x1.25`).
5. **Tiền lọc bất biến T0 (`pre_vote_t0_filter`):** Tự động gắn trong `Q5VotingEngine.submit_sheet` để chặn đáp án vi phạm T0 trước pha bỏ phiếu P2.
6. **Cổng bằng chứng E1 cho Veto (`validate_veto_e1_evidence`):** Tự động gắn trong `Q5VotingEngine.submit_ballot` để hạ các phiếu `X` cảm tính thiếu bằng chứng E1.
