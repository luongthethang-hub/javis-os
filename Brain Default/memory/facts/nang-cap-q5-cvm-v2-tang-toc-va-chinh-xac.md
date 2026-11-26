---
slug: nang-cap-q5-cvm-v2-tang-toc-va-chinh-xac
title: Nâng cấp bắt buộc Q5-CVM v2.0 (Tăng tốc phá lặp <=35s & Trọng số QC-5) cho Toàn Liên minh
type: system
created: 2026-11-26
updated: 2026-11-26
tags: [q5-cvm, v2, micro-cvm, early-stop, qc-5, alliance, mandatory]
source: layer0-directive-2026-11-26
---

# Nâng cấp Bắt buộc Toàn Liên minh: Q5-CVM v2.0

Áp dụng mặc định cho 100% thành viên (Javis, Antigravity, Claude, Codex, DeepSeek, Grok, Perplexity, Dola AI) và CAM từ ngày 26/11/2026.

## 6 Cơ chế Bắt buộc trong Q5-CVM v2.0 (`D:\AI AGENT\q5-voting-engine\q5_voting\v2_accelerator.py`)
1. **Micro-CVM Fast Path (`<= 35s`):** Rút gọn còn 3 mắt xích (`CORE -> RISK -> ACCEPTANCE`, `TTLConfig.micro_fast_path()`) cho ca `LOW/MEDIUM` cần thoát kẹt nhanh; `HIGH/CRITICAL` giữ cứng đủ 5 mắt xích T0.
2. **Early-Stop Lock (`check_early_stop_lock`):** Khóa phiên ngay lập tức khi khoảng cách dẫn đầu lớn hơn tổng trọng số phiếu còn lại chưa nộp.
3. **Loop Fingerprint Breaker (`LoopFingerprintBreaker`):** Băm SHA-256 `(topic | error)`; lặp từ lần 2 tự chặn phương án từng thất bại và ép nhảy sang `Micro-CVM`.
4. **Trọng số chuyên môn QC-5 (`get_voter_weight`):** Nhân hệ số tin cậy đúng sở trường (MQL5/Toán: DeepSeek & Antigravity `x1.3`; Kiến trúc/T0: Claude & Perplexity `x1.3`; Red Team: Grok `x1.25`).
5. **Tiền lọc bất biến T0 (`pre_vote_t0_filter`):** Chặn phương án vi phạm T0 ngay pha P1 trước khi bỏ phiếu P2.
6. **Cổng bằng chứng E1 cho Veto (`validate_veto_e1_evidence`):** Phủ quyết `X` thiếu dẫn chứng E1 tự hạ thành phản đối thường, chống kẹt vòng vá `P3b`.

## Kiểm chứng E1
- `D:\AI AGENT\q5-voting-engine`: `pytest` đạt **18/18 PASS** (`test_q5_v2_accelerator.py` + `test_voting_engine.py`).
