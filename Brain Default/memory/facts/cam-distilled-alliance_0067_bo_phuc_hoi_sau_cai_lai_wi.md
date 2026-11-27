---
type: fact
title: "[Liên minh] Bộ phục hồi sau cài lại Windows và giới hạn DPAPI"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/alliance_0067_bo_phuc_hoi_sau_cai_lai_wi.md"
evidence: E1
cam_content_hash: f01b3f5bdd87e9cb239d8d628ae847ffcb3b80c7cc70b9dcf9fdc94222544384
cam_bundle_hash: 29492773df9bb934
---

# [Liên minh] Bộ phục hồi sau cài lại Windows và giới hạn DPAPI

---
slug: alliance_0067_bo_phuc_hoi_sau_cai_lai_wi
title: [Liên minh] Bộ phục hồi sau cài lại Windows và giới hạn DPAPI
evidence: E2
source: cam-council
updated: 2026-11-27T10:35:54+07:00
tags: [alliance, backup, bridge, cam, disaster-recovery, dsh, knowledge-sync, system]
---

# [Liên minh] Bộ phục hồi sau cài lại Windows và giới hạn DPAPI

# Bộ phục hồi sau cài lại Windows (2026-11-27)

Mục tiêu: cài lại Windows vẫn dựng lại được DSH + CAM + tri thức Liên minh.

## Đã có (E1)
- `C:\Users\Admin\.dsh\recovery\backup_recovery.py`: lệnh `backup`, `list`, `verify`, `restore` (restore mặc định dry-run).
- Snapshot tại `D:\AI AGENT\AI_AGENT_BACKUP\recovery\snapshot-*`: 1.746 tệp / 29 MB + bản `.tar.gz` ~21 MB.
- `verify` đạt 1.745/1.745 tệp khớp sha256, 0 thiếu, 0 lệch.
- Tự động backup mỗi 24 giờ, giữ 14 bản; runbook `C:\Users\Admin\.dsh\recovery\RESTORE.md`.

## Phạm vi
DSH (profile, skill, ai-alliance, telegram-bridge, ruulee), workspace RUULEE, CAM (brain/config/tools, loại cache & webview profile), ally-cli, alliance-knowledge-sync, alliance-bus-runner, tài liệu.

## Không thể tự khôi phục
- CAM vault mã hoá DPAPI: khoá gắn máy cũ, phải đăng nhập lại tài khoản.
- Phiên DeepSeek/Claude, license app: đăng nhập lại.
- Bản backup chứa token plaintext: cần mã hoá khi mang ra ngoài.

## Giới hạn đã được Claude chỉ ra
- Snapshot + sha256 chỉ chứng minh toàn vẹn so với manifest, không 
