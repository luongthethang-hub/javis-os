---
type: fact
title: "[Liên minh] Workflow Video Ngan 6 Buoc Co Tien Hoa"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/alliance_j0022_workflow_video_ngan_6_buo.md"
evidence: E2
cam_content_hash: 2180a1f393dde4157821badc814cf68e9b6b176d507e10b0b3b2be3bfb604ad5
cam_bundle_hash: 34caca1411c0e585
---

# [Liên minh] Workflow Video Ngan 6 Buoc Co Tien Hoa

---
slug: alliance_j0022_workflow_video_ngan_6_buo
title: [Liên minh] Workflow Video Ngan 6 Buoc Co Tien Hoa
evidence: E2
source: cam-council
updated: 2026-11-26T23:34:19+07:00
tags: [alliance, bridge, fact, knowledge-sync, sync]
---

# [Liên minh] Workflow Video Ngan 6 Buoc Co Tien Hoa

Quy trình `san-xuat-video-ngan-1-phut` được nâng từ 4 bước tĩnh lên **6 bước có vòng tiến hóa**, giữ `status: on`, nhóm Nội dung.

- Bước 1 `grok`: chốt 1 luận điểm, 3 hook 3 giây, kịch bản 60 giây theo mốc giây, 150-165 từ lời đọc.
- Bước 2 `codex`: bảng phân cảnh 9:16 1080x1920 30fps, phụ đề SRT tối đa 8 từ mỗi dòng, rà chính sách TikTok/Shorts/Reels, đánh dấu số liệu cần bằng chứng.
- Bước 3 `antigravity`: voice anchor `vi-VN-NamMinhNeural` (rate -3%, pitch -6Hz), chuỗi DSP FFmpeg, chuyển chữ Đ đầu câu thành đ để tránh lỗi Azure `NoAudioReceived`, xuất Motion.md, dừng chờ chủ duyệt trước khi render.
- Bước 4 `antigravity` (codex đối soát): render MP4, ffprobe xác nhận 58-62 giây, không lệch tiếng.
- Bước 5 `codex`: ghi vết mỗi lần chạy vào `attachments/video-production/log/<YYYY-MM-DD-HHmm>-<slug>.md`, một file mỗi lần chạy, 9 trường cố định, thiếu dữ liệu thì ghi "không có dữ liệu", không điền số đoán.
- Bước 6 `grok`: chưng cất bài học, dưới 2 file log thì trả `INSUFFICIENT_DATA` và dừng; từ 2 log mới soạn đề xuất CUP theo skill `cam-tien-hoa`.

Chốt chặn: bước 6 chỉ đề xuất, không tự sửa 
