# Chuẩn trải nghiệm khung chat (lõi cho mọi hệ, áp trước cho CAM) - v1, 26/11/2026

Nguyên tắc L0: "Nghĩ xem người dùng sẽ dùng thế nào, thao tác thế nào; đủ chức năng cần thiết, tránh thiết kế ra mà người dùng không bao giờ dùng."

## 1. Luật thiết kế
1. Đo trước khi làm: từ log 7 ngày đo số tin/ngày, độ dài tin, tỉ lệ dán ảnh/file, việc lặp lại nhiều nhất, lỗi/khó chịu L0 từng phàn nàn.
2. Mỗi tính năng ghi rõ: L0 dùng lúc nào, ước bao nhiêu lần/tuần, bằng chứng từ log. Không có thì không làm.
3. Ít bấm nhất: việc hay làm phải có phím tắt hoặc 1 cú bấm; không bắt L0 mở dòng lệnh cho việc hằng ngày.
4. Sau 1 tuần đo lượt dùng từng tính năng; 0 lượt thì ẩn hoặc gỡ (chống khối u giao diện, V8).
5. Mỗi thay đổi có test tự động mô phỏng thao tác thật (gõ, dán, bấm) + ảnh chụp trước/sau.

## 2. Khung chat bắt buộc (P0)
- Enter = gửi; Shift+Enter = xuống dòng. Khi đang gõ tiếng Việt (Unikey/EVKey, IME đang ghép chữ) Enter KHÔNG được gửi nhầm (kiểm isComposing).
- Ô nhập tự giãn theo nội dung (tối đa ~40% chiều cao), cuộn bên trong khi dài.
- Giữ bản nháp khi chuyển trang, tải lại hoặc lỡ tắt.
- Dán ảnh bằng Ctrl+V, kéo-thả ảnh/file vào khung; hiện ảnh thu nhỏ, xóa được trước khi gửi; nhiều ảnh một lần; quá dung lượng thì báo rõ tiếng Việt.
- Copy:
  - Nút Copy trên MỌI tin (của Sếp và của CAM), chọn được "chữ thường" hoặc "giữ định dạng (markdown)".
  - Nút Copy riêng cho từng khối code, từng bảng.
  - Chọn nhiều tin (ô tích) rồi copy một lần, giữ thứ tự và ghi ai nói.
  - "Copy toàn bộ hội thoại" và "Xuất file .md".
- Gửi xong vẫn sửa được: phím mũi tên lên để sửa tin vừa gửi khi CAM chưa trả lời.
- Nút Dừng khi CAM đang trả lời; Esc cũng dừng.
- Trạng thái rõ: "đang suy nghĩ", "đang chạy công cụ X"; lỗi hiện tiếng Việt kèm nút "Thử lại".

## 3. Đọc câu trả lời (P0)
- Kết quả trước, giải thích sau; câu trả lời dài có mục lục nhỏ ở đầu.
- Bảng, danh sách, số liệu chính in đậm; đường dẫn file bấm mở được.
- Tìm trong hội thoại (Ctrl+F nội bộ hoặc Ctrl+K), nhảy tới tin.

## 4. Việc cần Sếp (P1, cần thiết kế an ninh + soát khác hãng trước)
- Thẻ "Cần Sếp duyệt" ngay trong chat với nút Xem / Duyệt / Từ chối, thay cho dòng lệnh cam_approve.py.
- Phải giữ cổng người thật: agent không được tự bấm duyệt qua API (mã xác nhận chỉ hiện trên màn hình, chỉ nhận từ giao diện cục bộ, có log).
- Thông báo: chỉ hiện việc thật sự cần Sếp, gom theo loại, có nút "Tắt loại thông báo này".

## 5. Nghiệm thu
- Test tự động cho từng mục P0 (gõ Enter/Shift+Enter, ghép chữ tiếng Việt, dán ảnh, copy từng tin/nhiều tin/toàn bộ, giữ nháp).
- L0 dùng thử 1 ngày, chấm 1-5 từng mục; dưới 4 thì sửa lại.
- Đo lượt dùng sau 1 tuần (luật 4).
