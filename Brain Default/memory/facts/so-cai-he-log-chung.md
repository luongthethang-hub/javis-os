---
slug: so-cai-he-log-chung
title: Sổ Cái v0.1.0 - hệ log và chỉ mục chung cho CAM OS, Doctor, Teacher, Darklord
type: reference
memory_tier: T2
provenance: artifact-read
evidence: E1
created: 2026-11-26
updated: 2026-11-26
decay_days: 180
tags: [fact, so-cai, log, chi-muc, cam-os, lien-minh-ai]
source: "D:\\AI AGENT\\so-cai\\README.md; python -m so_cai thong-ke lúc 22:47"
---

# Sổ Cái v0.1.0 (`D:\AI AGENT\so-cai`)

Hệ log chung nằm NGOÀI repo CAM OS, chỉ đọc nguồn CAM. Gom dự án, agent, model, file, commit, quyết định L0, gói việc, sự cố, bài học vào một chỗ để tra và nhảy liên kết.

## Cấu trúc
- `du-lieu/nhat-ky/YYYYMMDD.jsonl`: nguồn chân lý, chỉ ghi thêm.
- `du-lieu/so-rieng/<agent>.jsonl`: bản sao theo agent.
- `du-lieu/chi-muc.sqlite`: chỉ mục + FTS5 tìm không dấu; xóa đi dựng lại được từ nhật ký.
- `du-lieu/MA-TRAN.md`: ma trận việc x agent x file x trạng thái, tự sinh.
- Mỗi bản ghi có `loai`, `khoa` (vd `goi:G1`, `file:cam_core/app.py`, `khoa-ghi:cam-os`), `trang_thai`, `lien_ket`, `bang_chung` (E1 log/git gốc, E2 tài liệu agent viết, E3 chấm điểm). Trạng thái hiện tại của một khóa là bản ghi mới nhất có khóa đó.

## Lệnh (chạy trong thư mục so-cai)
- `python -m so_cai tim <từ khóa>`, `lien-ket <khóa>`, `khoa <tiền tố>`, `ma-tran --in-ra`, `thong-ke`.
- `python -m so_cai nap`: nạp chỉ đọc theo `nguon.json` (git log CAM, log CAM, teacher-agent).
- Ghi: `echo {"loai":"su-co","khoa":"su-co:...","tieu_de":"..."} | python -m so_cai ghi --json -`.

## Luật an toàn
- Không đọc `vault/`, `.credentials`, `.dsh/`, `.codex/auth*`, accounts_pool, owner_feedback, `.env`, `memory/conversations/`.
- Bộ che bí mật chạy trước khi ghi (key OpenAI/Google/GitHub, token Telegram, Bearer, JWT...).
- Test chạy trong thư mục tạm; `SoCai` từ chối trỏ vào `du-lieu/` thật khi chạy pytest.
- Dữ liệu có S2: chỉ dùng cục bộ, không gửi model hosted.

## Thực tế lúc 22:47 26/11
193 sự kiện (24/11 13:26 đến 26/11 22:42): 98 trace, 22 commit, 21 phiên chạy, 16 sự cố, 12 gói việc, 7 quyết định, 7 bài học.

Liên quan: [[luat-phong-giam-doc-20261126]], [[quyet-dinh-l0-20261126]].
