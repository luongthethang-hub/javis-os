# Chặng xét yêu cầu tư vấn và bàn giao cho tư vấn viên (Mô phỏng nội bộ)

Phạm vi: Kịch bản giả lập cho một trường dạy lái xe hư cấu. Không dùng dữ liệu thật, không truy cập hệ thống ngoài, không liên hệ người dùng thật.

## 1. Vai trò chịu trách nhiệm
- **Người bàn giao (Chịu trách nhiệm chính ở chặng này):** Điều phối tương tác Fanpage (bộ phận tiếp nhận tin nhắn và bình luận).
- **Người tiếp nhận:** Tư vấn viên tuyển sinh.
- **Vai trò đối soát:** Kiểm tra tính nhất quán (rà thiếu mục, rà suy diễn trước khi chuyển).

## 2. Đầu vào
- Nguyên văn bình luận hoặc tin nhắn mô phỏng phát sinh từ bài đăng theo bản yêu cầu nội dung.
- Mã bài đăng hoặc chủ đề nội dung nguồn.
- Bảng phân biệt 2 nhóm đối tượng và danh mục trường thông tin tối thiểu.

## 3. Quy tắc phân loại (quan sát được trên câu chữ)
- **Nhóm chỉ tương tác (Không tạo phiếu chuyển):**
  - Chỉ thả cảm xúc, khen bài viết, hoặc bình luận xã giao.
  - Chỉ hỏi mẹo chuẩn bị buổi đầu, cách phân biệt biển báo, hoặc hỏi thông tin chung mà không bày tỏ nhu cầu đăng ký và không đề nghị tư vấn.
  - Xử lý: Giữ ở luồng phản hồi thông thường (chờ duyệt), không bàn giao.
- **Nhóm nêu nhu cầu phù hợp và chủ động đề nghị tư vấn (Đưa vào xét phiếu):**
  - Nêu rõ nhu cầu học/thi bằng lái nằm trong phạm vi đào tạo giả lập.
  - Có câu chữ chủ động đề nghị được tư vấn (ví dụ: "nhắn mình thông tin khóa học", "tư vấn giúp mình lịch học").

## 4. Phiếu đầu ra (Phiếu bàn giao yêu cầu tư vấn mô phỏng)
Mẫu phiếu gồm các trường cố định sau (không suy diễn nếu thiếu):
- **Mã phiếu mô phỏng:** `TV-GIALAP-XXX`
- **Nguồn nội dung:** Mã bài đăng/chủ đề (ví dụ: Chuẩn bị buổi đầu / Ôn thi)
- **Kênh phát sinh:** Bình luận công khai hoặc Tin nhắn (mô phỏng)
- **Trích dẫn nguyên văn nhu cầu & lời đề nghị tư vấn:** Ghi đúng câu chữ gốc
- **Các trường thông tin tối thiểu:**
  1. Nhu cầu hạng bằng / khóa học quan tâm: [Ghi nhận theo nguyên văn hoặc ghi "Chưa nêu"]
  2. Khung thời gian hoặc khu vực học dự kiến: [Ghi nhận theo nguyên văn hoặc ghi "Chưa nêu"]
  3. Xác nhận chủ động đề nghị tư vấn: [Có trích dẫn / Không có]
  4. Kênh nhận phản hồi do người hỏi chủ động nêu: [Có / Chưa có]
- **Trạng thái xét lọc:** `Đạt chuẩn bàn giao` hoặc `Chưa chuyển - Thiếu thông tin`
- **Mục thiếu cần bổ sung (nếu chưa chuyển):** Liệt kê cụ thể tên từng mục còn trống

## 5. Tiêu chí tiếp nhận quan sát được (Điều kiện để Tư vấn viên nhận hoặc trả lại)
- **Chấp nhận tiếp nhận khi đạt đủ 4 điều kiện:**
  1. Có trích dẫn nguyên văn thể hiện đồng thời: nhu cầu học phù hợp và hành động chủ động đề nghị tư vấn.
  2. Đủ cả 4 trường thông tin tối thiểu, không bỏ trống mục nào (nếu mục 2 chưa bắt buộc theo kịch bản trường thì vẫn phải ghi rõ trạng thái "Chưa nêu" chứ không tự điền).
  3. Có gắn mã bài đăng nguồn để nắm ngữ cảnh.
  4. Không chứa cam kết thay cho trường (học phí, lịch chắc chắn, tỷ lệ đậu) và không có dữ liệu thật.
- **Trả lại / Chưa chuyển khi gặp một trong các dấu hiệu:**
  1. Người dùng chỉ tương tác hoặc hỏi mẹo ôn thi, chưa đề nghị tư vấn.
  2. Thiếu ít nhất 1 mục bắt buộc (nhu cầu cốt lõi, xác nhận chủ động đề nghị, hoặc kênh phản hồi): ghi rõ từng mục thiếu vào phần `Mục thiếu cần bổ sung` và giữ ở khâu hỏi lại, chưa chuyển sang tư vấn viên.
  3. Nội dung phiếu có dấu hiệu suy diễn ngoài câu chữ gốc hoặc lẫn dữ liệu thật.
