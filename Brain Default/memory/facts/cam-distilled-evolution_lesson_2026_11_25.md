---
type: fact
title: "Bài học tự chẩn đoán hệ thống (2026-11-25)"
created: 2026-11-26
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/evolution_lesson_2026_11_25.md"
evidence: E1
cam_content_hash: 96fa10f5109bb43dc8b25a49e43341d94507dafcbb4ba3bed498418d975e5902
cam_bundle_hash: 13d603e15d74c818
---

# Bài học tự chẩn đoán hệ thống (2026-11-25)

---
slug: evolution_lesson_2026_11_25
title: Bài học tự chẩn đoán hệ thống (2026-11-25)
evidence: E1
source: cam-evolution-engine
updated: 2026-11-25T21:37:18+07:00
tags: [evolution, zero-regression, logs]
---

# Bài học tự chẩn đoán hệ thống (2026-11-25)

Phát hiện các cảnh báo/lỗi trong nhật ký chạy gần nhất cần phòng ngừa tái diễn:
- run_20261125_181925.log: 2026-11-25 18:22:22,119 [WARNING] (cam.adapter.cli) S-gate blocked outbound dsh prompt (S2)
- run_20261125_181925.log: 2026-11-25 18:22:22,119 [WARNING] (cam.chat) Direct call DeepSeek failed: Cổng dữ liệu chặn gói S2 gửi tới dsh (fail-closed tại adapter)
- run_20261125_181925.log: 2026-11-25 19:13:00,547 [WARNING] (cam.adapter.cli) S-gate blocked outbound dsh prompt (S2)
- run_20261125_181925.log: 2026-11-25 19:13:00,547 [WARNING] (cam.chat) Direct call DeepSeek failed: Cổng dữ liệu chặn gói S2 gửi tới dsh (fail-closed tại adapter)
- run_20261125_181925.log: 2026-11-25 19:13:09,745 [WARNING] (cam.adapter.cli) S-gate blocked outbound codex prompt (S2)
- run_20261125_181925.log: 2026-11-25 19:13:09,745 [WARNING] (cam.chat) Direct call ChatGPT / Codex failed: Cổng dữ liệu chặn gói S2 gửi tới codex (fail-closed tại adapter)
- run_20261125_194545_pid13512.log: 2026-11-25 19:57:46,895 [WARNING] (cam.desktop) Yeu cau khoi dong lai hoan toan CAM server (reason=manual_api)
- run_20261125_205409.log: 2026-11-25 20:54:26,848 [ERRO
