# Đặc Tả Kỹ Thuật Motion.md (OpenMotion Schema)

Định dạng `Motion.md` là ngôn ngữ khai báo cấu trúc kịch bản và diễn hoạt thị giác:

## Metadata Cốt Lõi
- `project_name`: Tên dự án.
- `resolution`: 1080x1920 (9:16) hoặc 1920x1080 (16:9).
- `fps`: 30 hoặc 60.
- `duration`: Tổng thời lượng (giây).
- `brand_kit`:
  - `colors`: Danh sách mã màu HEX (Primary, Secondary, Background, Text).
  - `fonts`: Font chính và font bổ trợ.

## Cấu trúc Phân Cảnh (Scene Spec)
Mỗi phân cảnh bao gồm:
1. `time_range`: Thời gian bắt đầu và kết thúc (start - end).
2. `layers`: Danh sách các lớp theo thứ tự từ dưới lên trên:
   - `background`: Màu nền, gradient, video loop hoặc ảnh nền.
   - `content_media`: Video clip, ảnh sản phẩm, UI mockup.
   - `motion_graphics`: Khối đồ họa, icon, hình vẽ vector SVG/Canvas.
   - `text_typography`: Tiêu đề, phụ đề, bullet points kèm hiệu ứng animate.
3. `transitions`: Chuyển cảnh đầu/cuối của scene.
4. `audio_cues`: Giọng đọc lồng tiếng (VO) và hiệu ứng âm thanh (SFX).

## Mẫu Khai Báo YAML Frontmatter (Tùy chọn)
```yaml
---
version: "1.0"
ratio: "9:16"
fps: 30
duration: 20.5
brand:
  primary: "#1E40AF"
  accent: "#10B981"
  font_heading: "Inter-Bold"
---
```
