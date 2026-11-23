---
name: OpenMotion
description: Tái tạo và dựng video bằng mã: phân rã video mẫu thành Motion.md, thay đổi nhận diện thương hiệu, tạo tài sản đa phương tiện và xuất MP4.
group: Nội dung
---

# OpenMotion: Dựng & Tái Tạo Video Bằng Mã (Agentic Video Studio)

## Khi nào dùng

Kích hoạt khi người dùng muốn:
- Phân rã, dịch ngược (reverse engineering) video tham chiếu (URL hoặc MP4/MOV) thành dự án video có thể chỉnh sửa.
- Tái tạo video mẫu với nhận diện thương hiệu cá nhân (Brand Kit, copy, typography, màu sắc, logo).
- Dựng motion graphics bằng mã (HTML, CSS, Canvas, SVG, WebGL) kết hợp footage thực tế.
- Tạo video đa phương tiện kết hợp giọng đọc AI, âm nhạc nền và phụ đề đồng bộ.
- Chuyển đổi video thành mẫu tái sử dụng (Template to Video / Video to Template).

## Quy trình kỹ thuật 5 bước

### Quy định Pipeline Mặc định: Voice-First (Quy trình B)
- **Video có giọng đọc (Voiceover):** BẮT BUỘC thực thi theo Pipeline B (Voice-First):
  1. `Kịch bản & Copywriting` -> 2. `Tạo Voice & DSP Audio Anchor (Khóa trục thời gian)` -> 3. `Trích xuất Timestamp mili-giây từng từ` -> 4. `Dựng Visual & Motion Sync khớp từng mốc âm` -> 5. `Render MP4`.
- **Video không dùng giọng đọc:** Áp dụng quy trình Visual-First bình thường (thiết kế khung hình, chuyển động theo nhịp nhạc nền hoặc thời lượng cố định).

### 1. Phân rã video tham chiếu (Video Reverse Engineering)
1. **Trích xuất khung hình và nhịp cảnh:**
   - Dùng `ffprobe` lấy siêu dữ liệu (fps, duration, resolution).
   - Trích xuất contact sheet hoặc các khung hình đại diện tại các mốc chuyển cảnh.
2. **Lập đặc tả `Motion.md`:**
   - Ghi nhận trình tự cảnh (Scenes), thời lượng từng shot (Shot timing).
   - Xác định loại chuyển cảnh (Cut, Fade, Slide, Zoom, Wipe).
   - Nhận diện các chuyển động camera (Pan, Tilt, Orbit, Push-in, Pull-out).

### 2. Phân tách lớp hiển thị (Layer Separation)
- **Lớp Native Code (Dựng bằng HTML/CSS/Canvas/SVG):**
  - Tiêu đề, văn bản, nhãn dán, typography chuyển động.
  - Khung giao diện (UI mockup), bảng biểu số liệu, đồ thị động.
  - Khối hình học, hạt (particles), đường kẻ, logo vector.
  - Giữ độ nét vector 100%, không bị nén vỡ hay méo chữ như video AI thuần túy.
- **Lớp Media ngoại vi (Tài sản đa phương tiện):**
  - Chân dung người nói, footage đời thực, cảnh quay B-roll.
  - Sử dụng tệp có sẵn trong kho `attachments/` hoặc tạo mới qua mô hình AI khi được cấp quyền.

### 3. Tái cấu trúc theo Brand Kit
- Thay thế logo, bảng màu chủ đạo (Primary/Secondary color), font chữ thương hiệu của chủ.
- Viết lại kịch bản, lời thoại (copywriting) phù hợp ngách nội dung (Fintech, Trading, AI, Khóa học).
- Bảo toàn mật độ thị giác (Visual Density) và nhịp điệu gốc, không để khung hình trống trải hoặc tối hơn bản mẫu.

### 4. Xử lý âm thanh & Chuẩn giọng đọc khàn nội lực (Cinematic Voice Engineering)
- **Nguyên tắc chọn giọng theo thể loại:**
  - Video truyền động lực, bản lĩnh, kinh doanh, kỷ luật: BẮT BUỘC dùng giọng nam trầm nội lực, không dùng giọng nữ mỏng hoặc giọng đều đều tin tức.
  - Sử dụng `vi-VN-NamMinhNeural` với hạ pitch và giảm tốc nhẹ (`rate="-3%"`, `pitch="-6Hz"`).
- **Chuỗi xử lý âm thanh giả lập khàn điện ảnh (FFmpeg DSP Chain):**
  - Hạ cao độ: `asetrate=24000*0.92,aresample=24000` đưa âm vực xuống Deep Baritone (100Hz - 110Hz).
  - Tăng độ dày lồng ngực (Chest body): `bass=g=5.5:f=120` tạo sức nặng uy lực.
  - Tạo độ khàn xước thanh quản (Vocal Fry / Raspiness): `treble=g=4.0:f=6000,aexciter=freq=5500:amount=1.5`.
  - Nén dải động truyền hình: `compand=attacks=0.01:decays=0.15:points=-70/-70|-40/-26|-18/-8|0/-1:gain=3.8` giúp giọng dứt khoát, nổi bật trước nhạc nền.
- **Xử lý bẫy kỹ thuật Azure TTS:** Chuyển `Đ` đầu câu thành `đ` thường và ngắt câu ngắn để chống rớt kết nối `NoAudioReceived`.
- **Phụ đề động (Synced Subtitles):** Tạo thẻ phụ đề viền neon, màu vàng dạ quang (#FFE600), tương phản cao ở đáy khung hình.

### 5. Render & Nghiệm thu MP4
- Ghép các lớp chuyển động và âm thanh thông qua FFmpeg hoặc renderer cục bộ.
- Kiểm tra tính toàn vẹn: không giật lag, không lệch tiếng, tỷ lệ chuẩn (9:16 cho Shorts/TikTok/Reels, 16:9 cho YouTube).
- Xuất bản phẩm vào `attachments/video-production/` và báo cáo đường dẫn kiểm chứng.

## Cấu trúc chuẩn của Motion.md

Mỗi dự án tái tạo cần có file `Motion.md` lưu tại thư mục dự án:
```markdown
# [Tên Video / Dự án]
- Tỷ lệ: 9:16 (1080x1920) | FPS: 30 | Thời lượng: 00:25
- Brand Kit: Primary #0052FF, Accent #00E5FF, Font Inter/Cabinet Grotesk

## Scene 1: Hook (00:00 - 00:03)
- Visual: Zoom in UI mockup, chữ chuyển động bật nảy (Spring easing).
- Text: "AI Agent Tự Động Hóa 100%?"
- Audio: Voiceover câu 1 + SFX Whoosh.

## Scene 2: Vấn đề & Dẫn chứng (00:03 - 00:12)
- Visual: Biểu đồ sụt giảm chuyển động, text cảnh báo màu đỏ.
- Audio: Voiceover câu 2 + Nhạc nền tăng nhịp.

## Scene 3: Giải pháp & CTA (00:12 - 00:25)
- Visual: Chuyển sang giao diện dashboard mượt mà, nút CTA phát sáng.
- Audio: Voiceover kết luận + Nhạc fade out.
```

## Nguyên tắc an toàn & Thực dụng
1. Không tải video cá nhân lên các dịch vụ public trái phép khi chưa được người dùng xác nhận.
2. Ưu tiên render native và FFmpeg cục bộ để tối ưu chi phí và bảo mật tuyệt đối.
3. Không bịa đặt số liệu hay tự tiện thay đổi thông điệp cốt lõi của chủ khi remake video.
