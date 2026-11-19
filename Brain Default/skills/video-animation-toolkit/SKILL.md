---
name: Hoạt hình & Video
description: Dựng hoặc ghép MP4/MOV từ Telegram và tệp cục bộ bằng FFmpeg, xuất video ngắn, lập quy trình hoạt hình 2D/3D và motion graphics.
group: Nội dung
---

# Hoạt hình và video: chọn công cụ, làm đến bản xuất

## Khi nào dùng

Kích hoạt khi người dùng muốn cắt, ghép hoặc xuất video từ tệp có sẵn, kể cả yêu cầu tiếp nối sau khi gửi clip qua Telegram. Cũng áp dụng khi chọn công cụ, dựng cảnh, tạo video/GIF/hoạt hình web.

## Dựng nhanh trong chat riêng Telegram

- Gửi một clip MP4/MOV tối đa 20 MB kèm `/dungvideo 00:05-00:30 9:16 pad keep`, hoặc dùng lệnh khi trả lời trực tiếp vào clip gốc. Javis cắt đoạn, kiểm tra MP4 và trả tệp trong cùng chat.
- Có thể bỏ tùy chọn để lấy phong cách đã lưu. `pad` giữ hình và thêm viền, `crop` cắt giữa để lấp khung, `keep` giữ âm, `mute` tắt âm. Tỷ lệ hỗ trợ gồm 9:16, 16:9, 1:1 và original.
- Khi chủ nói muốn dùng cùng kiểu cho các clip sau, hướng dẫn dùng `/phongcachvideo 9:16 crop keep`. Chỉ lưu các lựa chọn chủ xác nhận. Tham số của một lệnh dựng chỉ áp dụng cho clip đó.
- Các yêu cầu chọn cảnh tự do, ghép nhiều clip hoặc phụ đề theo lời nói cần một lượt biên tập chuyên biệt. Chỉ báo đã bàn giao sau khi có tệp đầu ra kiểm chứng được.

## Quy trình

1. Chốt đầu ra: video dựng sẵn, hoạt hình web tương tác, GIF, giải thích toán, cảnh 3D hay hoạt hình game. Ghi rõ nền tảng, tỉ lệ khung hình, độ dài và phong cách. Nếu thiếu, đề xuất mặc định ngắn, dễ xem và dễ sửa.
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
- Với FFmpeg 9 trên máy này, truyền đồ thị ghép qua `-filter_complex`. Tùy chọn cũ `-filter_complex_script` không có trong bản cài.
- Sau khi xuất, kiểm tra file bằng `ffprobe` và xem khung hình ở đầu, giữa, cuối. Nếu quyền terminal hoặc công cụ không khả dụng, bàn giao edit brief và nêu rõ chưa render; không thử thay bằng điều khiển preview trình duyệt.
- Không tải video lên dịch vụ ngoài và không xuất bản bài đăng nếu chưa được yêu cầu.

## Bàn giao

Nêu công cụ chính và lý do, các bước thực hiện, định dạng đầu ra và điều gì cần người dùng chọn. Khi đã tạo video, đưa đường dẫn file và ghi rõ độ phân giải, tỉ lệ, thời lượng và fps.
