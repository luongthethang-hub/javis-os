---
slug: claude-desktop-tri-thuc-du-an-cam
title: Tri thức Claude Desktop nạp vào não (dự án CAM, 25-26/11/2026)
type: reference
created: 2026-11-26
updated: 2026-11-26
tags: [claude-desktop, cam, ingest, tri-thuc, token, hoi-dong]
source: "chat 2026-11-26 (73b7d347), trích từ ~/.claude/projects entrypoint=claude-desktop"
---

# Tri thức Claude Desktop nạp vào não (dự án CAM, 25-26/11/2026)

Đã đọc hội thoại THẬT của Claude Desktop (model claude-opus-5-5) trong dự án `D:\AI AGENT\council-agent-manager` và ingest vào Second Brain.

## Nguồn và sản phẩm
- Source thô: `sources/Claude Desktop - Hoi dong CAM 2026-11-25.md` (85 lượt user/assistant, đã lọc relay/spawn/system-prompt/tool noise).
- Wiki chưng cất: `wiki/claude-desktop-du-an-cam-nhat-ky-2026-11.md`.
- Cách trích tái lập được: `tmp/claude-desktop-extract.py`, `tmp/digest2.py`, `tmp/build_source.py`.

## Nội dung cốt lõi
- Nối Claude (token dài hạn 1 năm qua Vault, không lách lớp an toàn) và DeepSeek (phiên tài khoản sẵn có, không cần API key) vào CAM.
- Tiết kiệm token: lõi luật phân tầng L1/L2/L3 + bể ngữ cảnh, đo thật bằng Claude CLI giảm 28-73% tùy loại việc; system prompt gốc Claude Code ~34k token/lần nên phần tiết kiệm chỉ ở lõi.
- Luật cứng: cấm ký tự tượng hình trong mã ngữ cảnh (chỉ ASCII), kiểm tra báo P1.
- Cổng dữ liệu fail-closed: gói chứa S2/S3 không ra khỏi máy.
- Đội nano săn lỗi đọc log CAM có sẵn, bỏ phiếu 2/3, gieo lỗi giả 10/10 bắt được.
- Kết quả: CAM v3.3.0, CAM Corporation v2 tại /company; test tự báo tới 257/257.

## Giới hạn
- Số test/phiên bản là Claude tự báo, chưa chạy lại xác nhận tại thời điểm ingest.
- Claude Desktop đã chạm giới hạn 5 giờ (reset 16:20 Asia/Bangkok) tại lần đọc.
