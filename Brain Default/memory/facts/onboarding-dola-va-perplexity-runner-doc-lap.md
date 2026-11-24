---
slug: onboarding-dola-va-perplexity-runner-doc-lap
title: Đã Kích hoạt Bot Runner Độc lập cho Dola AI và Perplexity vào Liên minh AI
type: fact
created: 2026-11-24
updated: 2026-11-24
tags: [dola, perplexity, runner, full-mesh, a2a_bus, telegram]
source: chat 2026-11-24 (Chỉ đạo Tổng chỉ huy)
---

# Kích hoạt Runner Độc lập cho Dola AI và Perplexity

Đã chính thức tách Dola AI và Perplexity khỏi danh nghĩa "persona Antigravity", nâng cấp thành 2 thành viên Agent độc lập có worker riêng:

1. **Dola AI Runner (`Javis/runners/dola_runner.py`):**
   - Kênh: `@DolaAI_ThangLee_bot` (Token `9160223359`).
   - Định vị: COO & Chief Engagement Officer (Tác chiến & Trải nghiệm).
   - Tự động nhận tin Telegram, ghi nhận trực tiếp vào `memory/a2a_bus/inbox_dola.jsonl`.
   - Tiến trình: `run_dola.bat` đang chạy nền ổn định.

2. **Perplexity Runner (`Javis/runners/perplexity_runner.py`):**
   - Kênh: `@PerplexcityThangLee_bot` (Token `9186042684`).
   - Định vị: CIO & Research Lead (Nghiên cứu & Dữ liệu chuyên sâu).
   - Tự động nhận tin Telegram, ghi nhận trực tiếp vào `memory/a2a_bus/inbox_perplexity.jsonl`.
   - Tiến trình: `run_perplexity.bat` đang chạy nền ổn định.

3. **Kiểm chuẩn thực tế (Test PASS):**
   - Cả hai bot đã phát thông điệp chào mừng độc lập vào nhóm Thắng Lee Group (-1004479278576) thành công 100%.
