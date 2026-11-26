---
type: fact
title: "[Liên minh] Cam Cot Song Va Van Hanh On Dinh"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/alliance_j0018_cam_cot_song_va_van_hanh_.md"
evidence: E2
cam_content_hash: 204e164744ea6389be0713a3a24be7c9c9824493e39028bc389ac64e4e13cbc0
cam_bundle_hash: 34caca1411c0e585
---

# [Liên minh] Cam Cot Song Va Van Hanh On Dinh

---
slug: alliance_j0018_cam_cot_song_va_van_hanh_
title: [Liên minh] Cam Cot Song Va Van Hanh On Dinh
evidence: E2
source: cam-council
updated: 2026-11-26T23:34:18+07:00
tags: [alliance, bridge, fact, knowledge-sync, sync]
---

# [Liên minh] Cam Cot Song Va Van Hanh On Dinh

# Cột sống CAM và vận hành ổn định

Bản chưng cất lớp CAM cho tra cứu nhanh. Chi tiết có citation tại `wiki/cot-song-cam-va-van-hanh-on-dinh.md`.

## Đã nạp và áp dụng

- Trang wiki chưng cất 6 mục: khung quyền, đường nhanh, ổn định bot, TaskPacket, tiến hóa có kiểm, giới hạn bằng chứng.
- `skills/cam-cot-song/SKILL.md` thêm mục Đường nhanh: việc nhỏ trả lời thẳng, không quét vault, không nạp toàn bộ CAM (undo #51).
- `skills/cam-tien-hoa/SKILL.md` thêm mục Tính ổn định vận hành: một process sở hữu bot token, gặp HTTP 409 thì dừng worker, kiểm hậu điều kiện trước retry (undo #52).

## Bằng chứng đo

- `Javis/scripts/cam_queue.py` compile sạch; smoke test 9 bước trên DB tạm PASS: chống trùng `existing`, worker không hợp lệ trả `null`, worker thứ hai bị chặn, ticket sai bị từ chối, submit đúng chuyển `review`.
- Benchmark DB tạm, gọi subprocess tuần tự: `put` 225,6 ms/gói (200 gói), `claim` 95,3 ms/lượt (50 lượt).
- Vá lỗi thật trong `Javis/scripts/cam_queue.py`: ticket `secrets.token_urlsafe` có thể mở đầu bằng `-` nên argparse coi là option và `submit` hỏng; đổi sang `secrets.token_hex(24)`. Sao lưu: `Javi
