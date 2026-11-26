---
type: fact
title: "[Liên minh] Chuan Taskpack Tieng Anh Va Hang Doi San Viec"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/alliance_j0020_chuan_taskpack_tieng_anh_.md"
evidence: E2
cam_content_hash: c2967fac59ffc3f6529787d2421f52a19de8e069f71d0392c6edde5e586404b4
cam_bundle_hash: 34caca1411c0e585
---

# [Liên minh] Chuan Taskpack Tieng Anh Va Hang Doi San Viec

---
slug: alliance_j0020_chuan_taskpack_tieng_anh_
title: [Liên minh] Chuan Taskpack Tieng Anh Va Hang Doi San Viec
evidence: E2
source: cam-council
updated: 2026-11-26T23:34:19+07:00
tags: [alliance, bridge, fact, knowledge-sync, sync]
---

# [Liên minh] Chuan Taskpack Tieng Anh Va Hang Doi San Viec

Chuẩn gói giao việc **TaskPacket v1 bằng tiếng Anh** và hàng đợi san việc cục bộ `Javis/scripts/cam_queue.py` đã được triển khai, kèm số đo thật.

**Số đo tiếng Việt so với tiếng Anh** (tiktoken, 4 cặp chỉ dẫn cùng nghĩa):
- `o200k_base`: 45 token tiếng Việt, 37 token tiếng Anh, giảm 17,8% trên mẫu.
- `cl100k_base`: 68 token tiếng Việt, 37 token tiếng Anh, giảm 45,6% trên mẫu.
- Đây là tỷ lệ trên mẫu ngắn, chưa tính chi phí dịch và sửa lỗi dịch.

**Thí nghiệm 3 cấu hình trên cùng bộ 3 tác vụ** (Audit code, Extract dữ liệu, Ops telemetry): baseline ngữ cảnh đầy đủ tiếng Việt 658 token; gói TaskPacket tiếng Anh kèm tham chiếu SHA-256 còn 134 token, giảm 79,6%; thêm san việc work-stealing vẫn 134 token và cân được tải (worker rảnh tự kéo việc, worker quá tải không bị nhồi thêm).

**Hàng đợi `cam_queue.py`** (SQLite, pull-based): `put`, `claim`, `submit`, `fail`, `status`. Đã kiểm: 8 worker tranh một việc chỉ 1 thắng, gửi trùng không tạo bản sao, worker ngoài `eligible_workers` bị từ chối, submit đúng chuyển task sang `review`. Độ trễ đo trên DB tạm: `claim` 95,3 ms/lượt (50 lượt), `p
