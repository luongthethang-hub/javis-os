---
type: workflow
name: Sản xuất Video ngắn 1 phút Chuyên nghiệp
slug: san-xuat-video-ngan-1-phut
status: 'on'
group: Nội dung
description: "Sản xuất video ngắn 60 giây chuẩn Voice-First: chốt góc nội dung, kịch bản theo giây, voice anchor + DSP, Motion.md, render MP4 9:16 kèm QC, ghi vết và chưng cất bài học."
steps:
  - agent: grok
    task: "Chốt góc nội dung cho {{input}} (đọc phụ đề nếu là link video tham khảo). Trả về: 1 luận điểm duy nhất, 3 phương án hook 3 giây đầu, cấu trúc kịch bản 60 giây theo mốc giây (Hook 0-3s, Body 3-50s chia 4-6 nhịp cảnh, CTA 50-60s), 3 tiêu đề SEO và 2 ý tưởng thumbnail. Ước lượng độ dài lời đọc khoảng 150 đến 165 từ cho 60 giây. Không dùng em dash."
    max_retries: 2
  - agent: codex
    task: "Từ kịch bản ở {{prev}} lập bảng phân cảnh chuẩn 1 phút: mỗi cảnh ghi mốc bắt đầu và kết thúc bằng giây, cỡ chữ phụ đề, tỷ lệ 9:16 (1080x1920), fps 30. Viết phụ đề SRT ngắn gọn (tối đa 8 từ mỗi dòng), rà từ khóa dễ bị bóp tương tác hoặc vi phạm bản quyền/cộng đồng TikTok, Shorts, Reels. Đánh dấu mọi số liệu cần bằng chứng, không tự bịa số."
    max_retries: 2
  - agent: antigravity
    task: "Dựng Voice-First cho bảng phân cảnh ở {{prev}}: tạo voice anchor bằng vi-VN-NamMinhNeural (rate -3%, pitch -6Hz), áp chuỗi DSP FFmpeg (asetrate 24000*0.92, bass g=5.5:f=120, treble g=4.0:f=6000, aexciter, compand) theo skill openmotion, chuyển chữ Đ đầu câu thành đ thường để tránh lỗi Azure NoAudioReceived. Trích timestamp từng từ và xuất Motion.md đủ đặc tả để render. Dừng ở trạng thái CHỜ CHỦ DUYỆT, không render trước khi được duyệt."
    max_retries: 2
  - agent: antigravity
    task: "Render MP4 từ Motion.md đã duyệt ở {{prev}}: 1080x1920, 30fps, phụ đề vàng #FFE600 viền tương phản, âm thanh khớp mốc giây. Xuất vào attachments/video-production/. Chạy ffprobe xác nhận thời lượng 58 đến 62 giây, không lệch tiếng, không giật khung, rồi báo đường dẫn tệp và thông số thật."
    verify_agent: codex
    max_retries: 2
  - agent: codex
    task: "Ghi vết lần chạy này vào attachments/video-production/log/YYYY-MM-DD-HHmm.md theo mẫu ở mục Ghi vết (một file cho mỗi lần chạy, không sửa log cũ). Chỉ ghi số liệu thật lấy từ đầu ra các bước trước và từ ffprobe: hook đã chọn, số lần phải sửa kịch bản, số từ lời đọc, thời lượng thật, lệch tiếng, lỗi TTS gặp phải (đặc biệt NoAudioReceived do chữ Đ), số vòng retry từng bước, trạng thái cổng duyệt. Không suy diễn, không bịa số thiếu; ghi rõ trường nào không có dữ liệu. Không sửa file workflow."
    max_retries: 1
  - agent: grok
    task: "Đọc toàn bộ log trong attachments/video-production/log/. Nếu có dưới 2 lần chạy, báo INSUFFICIENT_DATA kèm số lần chạy hiện có và dừng, không đề xuất gì. Nếu từ 2 lần chạy, tìm mẫu lặp có bằng chứng (trích đúng tên file log và trường dữ liệu), rồi soạn đề xuất CUP theo skill cam-tien-hoa: vấn đề, bằng chứng, diff đề nghị cho workflows/san-xuat-video-ngan-1-phut.md, tầng ảnh hưởng, rủi ro, tiêu chí nghiệm thu, đường lùi. Chỉ đề xuất, KHÔNG tự sửa workflow. Dừng chờ chủ duyệt."
    max_retries: 1
updated: '2026-11-26'
---

# Quy trình Sản xuất Video ngắn 1 phút Chuyên nghiệp (`san-xuat-video-ngan-1-phut`)

Workflow 6 bước cho video dọc 60 giây theo pipeline Voice-First của skill `openmotion`, phối hợp `grok` -> `codex` -> `antigravity` (bước render được `codex` đối soát), rồi `codex` ghi vết và `grok` chưng cất bài học.

## Mốc thời gian chuẩn
- 00:00 đến 00:03: hook, một câu duy nhất, hình chuyển động ngay khung đầu.
- 00:03 đến 00:50: body 4 đến 6 cảnh, mỗi cảnh 5 đến 9 giây.
- 00:50 đến 01:00: CTA rõ ràng, nhạc fade out.

## Ghi vết mỗi lần chạy
Bước 5 ghi một file log cho mỗi lần chạy vào `attachments/video-production/log/<YYYY-MM-DD-HHmm>-<slug>.md`, không sửa log cũ, không gộp nhiều lần chạy vào một file.

Mẫu cố định:

| Trường | Nguồn dữ liệu |
|---|---|
| Ngày giờ chạy, đầu vào `{{input}}` | lúc khởi chạy |
| Luận điểm và hook đã chọn | đầu ra bước 1 |
| Số lần phải sửa kịch bản/phân cảnh | số vòng retry của bước 1, 2 |
| Số từ lời đọc và độ dài dự kiến | đầu ra bước 1 |
| Thời lượng thật, fps, kích thước | ffprobe ở bước 4 |
| Lệch tiếng (ms), khung giật | kiểm ở bước 4 |
| Lỗi TTS gặp phải, mã lỗi | đầu ra bước 3 |
| Số vòng retry từng bước, bước nào vượt `max_retries` | log chạy workflow |
| Trạng thái cổng duyệt (chờ/duyệt/từ chối, số lần bị trả lại) | cổng duyệt bước 3 |

Thiếu dữ liệu thì ghi `không có dữ liệu`, không điền số đoán. Log là dữ liệu chưng cất, không chứa khoá API hay dữ liệu riêng của khách.

## Chưng cất bài học
Bước 6 chỉ có hiệu lực khi đã có ít nhất 2 file log. Nó đề xuất theo skill `cam-tien-hoa`: một bài học lặp ít nhất 2 lần mới thành đề xuất, một sự cố có thiệt hại thật thì đủ căn cứ ngay.

Đầu ra là bản đề xuất CUP, không phải bản sửa. Mọi thay đổi vào chính file workflow phải qua chủ duyệt, kèm bản cũ để hoàn tác. Mẫu log sai hoặc thiếu trường cũng là một phát hiện hợp lệ để sửa mẫu.

## Cổng duyệt
Mặc định `status: 'off'`. Bước 3 luôn dừng chờ chủ duyệt Motion.md và voice anchor trước khi render, để tránh tốn thời gian dựng lại toàn bộ khi kịch bản hoặc giọng còn phải sửa.

## Điều kiện chạy
Cần `ffmpeg` và `ffprobe` trong PATH, voice Azure TTS đã cấu hình, và agent `antigravity` bật với skill `openmotion`. Thiếu công cụ nào thì báo BỊ CHẶN CÔNG CỤ, không giả báo đã render.