---
type: wiki
status: active
tags: [wiki, video, openmotion, ai-studio, motion-design]
created: 2026-11-22
updated: 2026-11-22
source: "https://github.com/nexu-io/openmotion"
---

# OpenMotion: Nền Tảng Dựng & Tái Tạo Video Bằng Mã Cho AI Agent

## 1. Bản chất & Định vị
OpenMotion là studio video mã nguồn mở (thay thế Claude Motion và CapCut) được thiết kế chuyên biệt cho AI Agent tự động hóa quá trình dựng video [[https://github.com/nexu-io/openmotion]]. Nền tảng kết hợp 2 triết lý cốt lõi:
- **Video Reverse Engineering (Dịch ngược video):** Phân tích video mẫu từ liên kết hoặc tệp MP4, bóc tách nhịp cảnh, bố cục và chuyển động thành định dạng `Motion.md`.
- **Code-Based Motion Graphics:** Dựng và diễn hoạt các thành phần chữ, logo, UI, biểu đồ bằng mã native (HTML, CSS, SVG, Canvas), giữ độ sắc nét tuyệt đối và dễ dàng tùy biến theo Brand Kit của thương hiệu cá nhân.

## 2. Các thành phần chính
- **Motion.md Specification:** Khai báo cấu trúc kịch bản theo trục thời gian, nhịp cắt, easing và phân tầng hiển thị.
- **Phân tách Layer Native vs Media:**
  - *Native Code:* Xử lý typography, card thông tin, layout, motion graphics vector.
  - *Generated/Real Media:* Xử lý footage người thật, B-roll, âm thanh lồng tiếng và hiệu ứng âm thanh.
- **Hệ sinh thái Agent & MCP:** Hỗ trợ kết nối MCP Tool để Agent tự gọi render, kiểm tra preview và xuất file MP4 hoàn chỉnh.
- **Voice Engineering:** Chuẩn hóa kỹ thuật xử lý giọng đọc nam nội lực trầm khàn qua chuỗi DSP FFmpeg (hạ pitch, tăng tần số lồng ngực 125Hz, tăng âm xước thanh quản 6kHz và nén động lực học compand).

## 3. Ứng dụng trong hệ thống Javis & Antigravity
- Kích hoạt qua skill `openmotion` (`skills/openmotion/SKILL.md`).
- Tích hợp trực tiếp vào 2 trợ lý: `dao-dien-kich-ban-video` (viết kịch bản chuẩn Motion.md) và `ky-thuat-dung-video` (dựng, tách cảnh, sync audio và render MP4).
- Phục vụ sản xuất video ngắn TikTok, Reels và Shorts chuẩn tỷ lệ 9:16 và YouTube 16:9.
