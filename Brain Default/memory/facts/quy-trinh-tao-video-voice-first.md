---
type: preference
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23
---
Mặc định khi tạo video có giọng đọc BẮT BUỘC áp dụng Quy trình B (Voice-First): Kịch bản -> Tạo giọng đọc & khóa trục thời gian Audio Anchor -> Trích xuất mốc thời gian timestamp -> Dựng visual & chuyển động khớp âm thanh -> Render MP4.

**Vì sao:**
- Trục âm thanh (Audio Anchor) cố định thời lượng chuẩn xác đến từng mili-giây, triệt tiêu hoàn toàn lỗi lệch pha (hình hết trước tiếng hoặc tiếng hết nhưng hình bị đơ).
- Cho phép kích hoạt chính xác hiệu ứng thị giác, kinetic typography và chuyển cảnh ngay tại âm tiết trọng tâm.
- Tiết kiệm thời gian và tài nguyên render, không phải kéo giãn timeline hay render lại video nhiều lần khi tốc độ đọc thay đổi.

**Ngoại lệ:**
- Những video không dùng giọng đọc (nhạc nền thuần, loop hình, B-roll phong cảnh, kinetic text theo nhịp nhạc) vẫn áp dụng quy trình Visual-First bình thường.
