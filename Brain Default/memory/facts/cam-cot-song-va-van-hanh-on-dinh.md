---
slug: cam-cot-song-va-van-hanh-on-dinh
title: Cột sống CAM và vận hành ổn định (2026-11-26)
type: fact
memory_tier: T2
provenance: owner-request
evidence: E1
created: 2026-11-26
updated: 2026-11-26
decay_days: 180
source: "chat:web:c5891efc796348dbb651343acf8556e6#msg-1173"
tags: [fact, cam, second-brain, van-hanh, hieu-nang]
---

# Cột sống CAM và vận hành ổn định

Bản chưng cất lớp CAM cho tra cứu nhanh. Chi tiết có citation tại `wiki/cot-song-cam-va-van-hanh-on-dinh.md`.

## Đã nạp và áp dụng

- Trang wiki chưng cất 6 mục: khung quyền, đường nhanh, ổn định bot, TaskPacket, tiến hóa có kiểm, giới hạn bằng chứng.
- `skills/cam-cot-song/SKILL.md` thêm mục Đường nhanh: việc nhỏ trả lời thẳng, không quét vault, không nạp toàn bộ CAM (undo #51).
- `skills/cam-tien-hoa/SKILL.md` thêm mục Tính ổn định vận hành: một process sở hữu bot token, gặp HTTP 409 thì dừng worker, kiểm hậu điều kiện trước retry (undo #52).

## Bằng chứng đo

- `Javis/scripts/cam_queue.py` compile sạch; smoke test 9 bước trên DB tạm PASS: chống trùng `existing`, worker không hợp lệ trả `null`, worker thứ hai bị chặn, ticket sai bị từ chối, submit đúng chuyển `review`.
- Benchmark DB tạm, gọi subprocess tuần tự: `put` 225,6 ms/gói (200 gói), `claim` 95,3 ms/lượt (50 lượt).
- Vá lỗi thật trong `Javis/scripts/cam_queue.py`: ticket `secrets.token_urlsafe` có thể mở đầu bằng `-` nên argparse coi là option và `submit` hỏng; đổi sang `secrets.token_hex(24)`. Sao lưu: `Javis/scripts/cam_queue.py.bak-20261126`. Sau vá: 200 vòng put/claim/submit 0 lỗi, 8 worker tranh một việc chỉ 1 thắng.
- Đồng bộ mirror `.claude/skills/` cho `cam-cot-song` và `cam-tien-hoa` (trước đó lệch hash), giữ `SKILL.md.bak-20261126`.

## Giới hạn

Chưa đo độ trễ chat thật, chưa kiểm hành vi model trên `acceptance-cases.jsonl`. Hàng đợi chưa nối process worker và chưa có polling nền. Không sửa server, gateway, T0, quyền hay production.

## Điểm cần theo dõi

`javis_improve` chỉ ghi vào `skills/`, không ghi `.claude/skills/`; hai bản từng lệch và đã đồng bộ tay ngày 2026-11-26. Lần sửa skill sau phải kiểm hash hai bên.
