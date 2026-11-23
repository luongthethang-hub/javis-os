# Quy Trình Dịch Ngược Video Tham Chiếu (Video Reverse Engineering)

## 1. Thu thập dữ liệu video mẫu
- Khi nhận link hoặc tệp video MP4/MOV:
  1. Kiểm tra codec, độ phân giải và framerate bằng `ffprobe`.
  2. Trích xuất frame định kỳ:
     `ffmpeg -i input.mp4 -vf "fps=2" -q:v 2 frames/frame_%04d.jpg`
  3. Trích xuất âm thanh:
     `ffmpeg -i input.mp4 -vn -c:a aac audio.m4a`

## 2. Phân tích nhịp và cấu trúc cảnh (Scene & Shot Analysis)
- **Điểm cắt (Cut points):** Đánh dấu chính xác timestamp khi chuyển cảnh (ví dụ: 00:00 - 00:03.200).
- **Phân loại chuyển động:**
  - Dynamic Motion: Chuyển động gia tốc (Easing: ease-in, ease-out, elastic, spring).
  - Continuous Motion: Trôi chậm (Drift, subtle scale 1.0 -> 1.05).
  - Spatial Placement: Khung hình chia cột, lưới (grid layout), card nổi.

## 3. Nhận diện Typography & Màu sắc
- Xác định kiểu font (Geometric Sans, Serif, Monospace, Condensed Display).
- Tách màu chủ đạo (Background, Primary Text, Accent Text, Border).
- Ghi nhận hiệu ứng chữ: Kinetic typography, type-writer, word-by-word highlight.

## 4. Xây dựng bản dựng thay thế (Rebuild Strategy)
- Giữ nguyên nhịp điệu (Pacing) và bố cục (Layout).
- Thay toàn bộ copy và brand assets của khách hàng/người dùng.
- Bảo đảm thời lượng đọc văn bản phù hợp với tốc độ đọc của người xem (tối thiểu 0.3s/từ).
