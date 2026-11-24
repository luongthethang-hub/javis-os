---
name: Hoạt hình & Video
description: Phân tích video tham chiếu MP4/MOV, dựng và xuất video bằng FFmpeg, lập quy trình hoạt hình 2D/3D và motion graphics.
group: Nội dung
---

# Hoạt hình và video: chọn công cụ, làm đến bản xuất

## Khi nào dùng

Kích hoạt khi người dùng muốn cắt, ghép hoặc xuất video từ tệp có sẵn, kể cả yêu cầu tiếp nối sau khi gửi clip qua Telegram. Cũng áp dụng khi chọn công cụ, dựng cảnh, tạo video/GIF/hoạt hình web.

Khi chủ gửi tệp video không kèm yêu cầu riêng hoặc muốn biên tập video content, mở `references/quy-trinh-bien-tap-studio.md` và bắt đầu tiếp nhận. Các cổng duyệt trong đó áp dụng cả khi gọi qua quy trình **Dựng video và trả MP4**. Chỉ dựng sau khi brief và phương án được chốt; dừng đúng mốc cần duyệt. Hướng dẫn FFmpeg bên dưới dùng để thực hiện từng phần đã được phép.

## Phân tích video tham chiếu bằng CLI cục bộ (thử nghiệm)

- Chỉ dùng khi chủ yêu cầu phân tích clip mẫu, tách cảnh hoặc lập storyboard tham chiếu. Không chạy mặc định khi nhận tệp, không gọi từ `/dungvideo` và không thay các mốc duyệt dựng.
- Trên máy Windows đã cài thử `rea-video` từ commit `131d1527557d2cccacb64059d47560964235acd7` trong môi trường Python riêng, chạy `python skills/video-animation-toolkit/scripts/analyze_reference.py "attachments/clip-mau.mp4"` từ brain. Nếu terminal đang ở thư mục khác, dùng đường dẫn tuyệt đối đến script trong brain gốc. Script chỉ nhận tệp MP4/MOV trong brain, cần `ffmpeg` và `ffprobe` trong PATH, không cần tài khoản/API key, không bật VLM, OCR, nhận dạng lời nói hoặc tách âm.
- Khi CLI thành công, đọc `VIDEO.md` và `report.md` trước; mở `storyboard.jpg` hoặc `breakdown.json` để đối chiếu mốc khi cần. Các tệp được lưu riêng từng lượt trong `attachments/video-reference-pilot/`. Xem các phân loại quay thật/AI/3D và điểm tin cậy là giả thuyết, không dùng để xác minh nguồn gốc. Không coi số cảnh là số điểm cắt đã được kiểm chứng thủ công.
- Nếu CLI lỗi, đọc `cli.log` nếu có, báo rõ phần chưa thực hiện và dùng FFprobe/contact sheet cục bộ nếu phù hợp. Không tự chuyển qua API, không tải clip lên mạng và không tự chạy bản dựng.

## Dựng nhanh trong chat riêng Telegram

- Gửi một clip MP4/MOV tối đa 20 MB kèm `/dungvideo 00:05-00:30 9:16 pad keep`, hoặc dùng lệnh khi trả lời trực tiếp vào clip gốc. Javis cắt đoạn, kiểm tra MP4 và trả tệp trong cùng chat.
- Có thể bỏ tùy chọn để lấy phong cách đã lưu. `pad` giữ hình và thêm viền, `crop` cắt giữa để lấp khung, `keep` giữ âm, `mute` tắt âm. Tỷ lệ hỗ trợ gồm 9:16, 16:9, 1:1 và original.
- Khi chủ nói muốn dùng cùng kiểu cho các clip sau, hướng dẫn dùng `/phongcachvideo 9:16 crop keep`. Chỉ lưu các lựa chọn chủ xác nhận. Tham số của một lệnh dựng chỉ áp dụng cho clip đó.
- Dùng `/phongcachvideo ghi Ưu tiên giữ trọn thao tác tay trước khi chuyển cảnh` để lưu góp ý biên tập đã xác nhận. Trợ lý Biên tập Video ngắn dùng ghi chú này khi được gọi trong chat riêng của chủ.
- Các yêu cầu chọn cảnh tự do, ghép nhiều clip hoặc phụ đề theo lời nói cần một lượt biên tập chuyên biệt. Chỉ báo đã bàn giao sau khi có tệp đầu ra kiểm chứng được.

## Quy trình

1. Chốt đầu ra: video dựng sẵn, hoạt hình web tương tác, GIF, giải thích toán, cảnh 3D hay hoạt hình game. Ghi rõ nền tảng, tỉ lệ khung hình, độ dài và phong cách. Nếu thiếu, đề xuất mặc định để chủ chọn.
2. Chọn một công cụ chính theo mục đích. Không cài cả danh sách và không phối nhiều thư viện làm cùng một việc.
3. Trước khi cài thư viện vào dự án, kiểm tra README, phiên bản, giấy phép, môi trường cần có và cách xuất hiện hành. Xin người dùng duyệt cài phần mềm hoặc thay đổi dự án.
4. Làm storyboard/nhịp cảnh ngắn; dựng một đoạn thử 3–5 giây để kiểm tra phong cách và chuyển động trước khi mở rộng.
5. Tạo cảnh, căn nhịp, âm thanh và chữ; xem bản preview theo từng cảnh; sửa lỗi cắt khung, chữ khó đọc, chuyển động giật, lệch nhịp hoặc âm thanh.
6. Xuất đúng định dạng, độ phân giải, fps, tỉ lệ và dung lượng người dùng cần. Xác nhận file xuất mở được và xem nhanh đầu/cuối cùng các đoạn chuyển cảnh.

## Chọn công cụ

- Video lập trình bằng React: Remotion Skills (`https://github.com/remotion-dev/skills`) để hướng dẫn AI trong dự án Remotion.
- Video giải thích, sơ đồ và minh hoạ theo timeline: Motion Canvas (`https://github.com/motion-canvas/motion-canvas`).
- Chuyển động giao diện web/React: Motion (`https://github.com/motiondivision/motion`).
- Làm mượt giá trị số: Ola (`https://github.com/franciscop/ola`). Dùng Anime.js (`https://github.com/juliangarnier/anime`) khi cần timeline, stagger và nhiều kiểu chuyển động; dùng Shifty (`https://github.com/jeremyckahn/shifty`) cho tweening đơn giản. TweenJS (`https://github.com/CreateJS/TweenJS`) hợp với chuỗi tween trong hệ CreateJS. Tránh ghép nhiều thư viện tween nếu không có lý do rõ.
- Vector 2D trên web: Two.js (`https://github.com/jonobr1/two.js`). Canvas có tương tác, kéo-thả và chỉnh sửa: Konva (`https://github.com/konvajs/konva`). Phát animation vector Lottie có sẵn: Lottie Web (`https://github.com/airbnb/lottie-web`). Xuất GIF từ khung hình bằng JavaScript: gifenc (`https://github.com/mattdesl/gifenc`).
- Công thức, hình học và bài giảng toán: Manim Community (`https://github.com/ManimCommunity/manim`).
- 3D trên web: Three.js (`https://github.com/mrdoob/three.js`) cho thư viện dựng hình linh hoạt; Babylon.js (`https://github.com/BabylonJS/Babylon.js`) cho engine 3D đầy đủ hơn; LUME (`https://github.com/lume/lume`) khi muốn dựng cảnh 3D theo hướng HTML khai báo. Chọn một nền tảng chính.
- Nhân vật/rig và render 3D: Blender (`https://github.com/blender/blender`). Hoạt hình trong game 2D/3D: Godot (`https://github.com/godotengine/godot`). Hạt, khói, tia sáng và hiệu ứng: Proton (`https://github.com/drawcall/Proton`).

## Nguyên tắc thực dụng

- Chọn công cụ theo nơi video sẽ chạy và cách người dùng muốn sửa, không theo số sao hay số thư viện.
- Ưu tiên công cụ đã có trong dự án; chỉ thêm phụ thuộc khi nó giải quyết nhu cầu cụ thể.
- Dùng chuyển động để làm rõ nội dung. Giữ bố cục, tương phản, cỡ chữ và nhịp xem tốt trên màn hình đích.
- Không khẳng định mọi repo còn được duy trì, miễn phí cho mọi mục đích hoặc phù hợp thương mại. Kiểm tra license và tình trạng dự án trước khi khuyến nghị dùng thật.
- Nếu lỗi render, thu nhỏ thành một cảnh tối giản để tái hiện, kiểm tra log và thông số đầu ra, rồi sửa nguyên nhân trước khi render lại toàn bộ.

## Dựng video từ tệp cục bộ trên Windows

- Với video người dùng đã tải lên hoặc gửi qua Telegram, làm việc trên đường dẫn cục bộ. Không phụ thuộc vào URL của tab trình duyệt hay browser preview để đọc hoặc dựng video.
- Kiểm tra `ffmpeg` và `ffprobe` trong PATH. Nếu chúng chưa có trong PATH của tiến trình hiện tại, tìm bản WinGet dưới `$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*\bin\` rồi gọi executable bằng đường dẫn đầy đủ.
- Dùng `ffprobe` đọc metadata; trích một số khung hình bằng `ffmpeg` và xem contact sheet trước khi viết nội dung bám footage. Không suy diễn lời thoại hoặc sự kiện không nhìn/nghe được.
- Khi có quyền chạy lệnh cục bộ, FFmpeg có thể cắt, ghép, đổi kích thước, cân chỉnh âm lượng và chèn chữ/phụ đề. Không ghi đè footage nguồn; xuất bản nháp vào thư mục riêng trong `attachments/` của Brain đang hoạt động.
- Với bản cắt hoặc ghép chuẩn, gọi `python skills/video-animation-toolkit/scripts/render_mp4.py <kế-hoạch.json>` từ brain. Dùng đường dẫn tuyệt đối đến script gốc trong brain nếu thư mục hiện hành khác. Ví dụ kế hoạch tối thiểu:

  ```json
  {"clips":[{"path":"inbox/telegram/clip.mp4","start":0.5,"end":5}],"ratio":"9:16","fit":"pad","audio":"keep"}
  ```

  `clips` chứa 1 đến 20 đoạn theo thứ tự dựng. Bỏ mốc để lấy từ đầu hoặc đến hết cảnh. Hỗ trợ `9:16`, `16:9`, `1:1`, `pad`/`crop`, `keep`/`mute` và `subtitles` (đường dẫn SRT UTF-8 trong brain, mốc theo bản ghép). Nếu có đoạn không có âm thanh và đang dùng `keep`, đoạn đó được đệm yên lặng. Đường dẫn MP4 do chương trình trả về là tệp đã qua ffprobe và giải mã toàn bộ, nằm trong `attachments/video-production/`. Chọn tên kế hoạch riêng mỗi lượt. Nếu cần cấu hình xuất ngoài các tùy chọn trên, dùng FFmpeg trực tiếp và thực hiện cùng bước kiểm tra.
- Với FFmpeg 9 trên máy này, truyền đồ thị ghép qua `-filter_complex`. Tùy chọn cũ `-filter_complex_script` không có trong bản cài.
- Sau khi xuất, kiểm tra `ffprobe` và xem khung hình đầu, giữa, cuối cùng các điểm cắt quan trọng. Khi cần, báo rõ khâu xem hình hoặc nghe tiếng nào chưa thực hiện được. Dùng quyền terminal có sẵn, không cần thao tác giao diện để chạy FFmpeg. Nếu bị chặn hoặc thiếu công cụ, nêu thông báo lỗi và bàn giao phần đã làm được.
- Không tải video lên dịch vụ ngoài và không xuất bản bài đăng nếu chưa được yêu cầu.

## Bàn giao

Trả MP4 trong cuộc trò chuyện yêu cầu, với link Markdown tương đối từ brain trong dashboard. Nếu yêu cầu đến từ Telegram, dùng cơ chế đính kèm tệp của lượt đó và chỉ xác nhận đã gửi khi có bằng chứng. Chỉ dùng kênh khác nếu chủ yêu cầu. Kèm thời lượng, khung hình, fps và nếu còn điểm cần duyệt, ghi ngắn gọn sau link.

## Bài học sau mỗi lần dựng

- Yêu cầu của video hiện tại được ưu tiên. Chỉ áp dụng mặc định lâu dài khi chủ dặn dùng cho các video sau. Trong chat trực tiếp với Biên tập Video ngắn, khi chủ dặn rõ, phát `JAVIS_RULE: ...` để Javis lưu luật. Trên Telegram, `/phongcachvideo` tiếp tục quản lý preset dựng nhanh và góp ý đã xác nhận của chủ.
- Khi có một bài học tái dùng được từ bản dựng, phản hồi hoặc lỗi đã sửa, phát tối đa hai dòng `JAVIS_LESSON: ...` theo cơ chế của Javis. Ghi điều có thể áp dụng lần sau, dựa trên kết quả thực tế. Không coi quyết định cho một clip hay tự đánh giá của trợ lý là gu đã được xác nhận.
