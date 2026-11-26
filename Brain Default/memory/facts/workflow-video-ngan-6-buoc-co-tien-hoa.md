---
type: decision
created: 2026-11-26
updated: 2026-11-26
---
Quy trình `san-xuat-video-ngan-1-phut` được nâng từ 4 bước tĩnh lên **6 bước có vòng tiến hóa**, giữ `status: on`, nhóm Nội dung.

- Bước 1 `grok`: chốt 1 luận điểm, 3 hook 3 giây, kịch bản 60 giây theo mốc giây, 150-165 từ lời đọc.
- Bước 2 `codex`: bảng phân cảnh 9:16 1080x1920 30fps, phụ đề SRT tối đa 8 từ mỗi dòng, rà chính sách TikTok/Shorts/Reels, đánh dấu số liệu cần bằng chứng.
- Bước 3 `antigravity`: voice anchor `vi-VN-NamMinhNeural` (rate -3%, pitch -6Hz), chuỗi DSP FFmpeg, chuyển chữ Đ đầu câu thành đ để tránh lỗi Azure `NoAudioReceived`, xuất Motion.md, dừng chờ chủ duyệt trước khi render.
- Bước 4 `antigravity` (codex đối soát): render MP4, ffprobe xác nhận 58-62 giây, không lệch tiếng.
- Bước 5 `codex`: ghi vết mỗi lần chạy vào `attachments/video-production/log/<YYYY-MM-DD-HHmm>-<slug>.md`, một file mỗi lần chạy, 9 trường cố định, thiếu dữ liệu thì ghi "không có dữ liệu", không điền số đoán.
- Bước 6 `grok`: chưng cất bài học, dưới 2 file log thì trả `INSUFFICIENT_DATA` và dừng; từ 2 log mới soạn đề xuất CUP theo skill `cam-tien-hoa`.

Chốt chặn: bước 6 chỉ đề xuất, không tự sửa file workflow; mọi thay đổi phải qua chủ duyệt kèm bản cũ để hoàn tác.

**Vì sao:** bản 4 bước chỉ có `max_retries: 2`, chạy lại y nguyên nên không rút ra bài học; không có log thì không có bằng chứng để sửa quy trình.

**Áp dụng:** vòng chạy đầu chỉ ghi log rồi báo thiếu dữ liệu, phải đến lần thứ hai mới có đề xuất thật. Điều kiện chạy: `ffmpeg`, `ffprobe` trong PATH, Azure TTS đã cấu hình, agent `antigravity` bật kèm skill `openmotion`; thiếu thì báo BỊ CHẶN CÔNG CỤ, không báo khống đã render.
