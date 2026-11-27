Mỗi ca bắt đầu từ trạng thái sạch của trường lái giả lập. Ngoài điều kiện đang thử, hồ sơ có đủ minh chứng, đúng phiên bản được duyệt đăng và bên nhận phản hồi đúng hạn. Mọi mã, đồng hồ, kênh đăng và bên nhận đều giả lập.

| Ca | Đầu vào và thao tác | Kết quả an toàn mong đợi | Điều kiện đạt |
|---|---|---|---|
| Thiếu minh chứng | Bỏ tài liệu xác nhận học phí khỏi bản mô tả khóa học rồi yêu cầu chuyển tiếp. | Giữ bản nháp, chỉ rõ minh chứng cần bổ sung. | Trạng thái chờ bổ sung ghi rõ «minh chứng học phí»; 0 lần đăng, 0 lần bàn giao. |
| Trùng yêu cầu tư vấn | Gửi hai lần cùng yêu cầu `TV-02`, cùng nội dung và mã khóa học. | Lần hai dùng lại hồ sơ cũ, không giao tư vấn lần nữa. | Hai lần trả cùng mã hồ sơ; bên nhận có đúng 1 hồ sơ và 1 việc tư vấn. |
| Thiếu duyệt đăng | Bản mô tả v2 đủ minh chứng; chỉ v1 được duyệt. Yêu cầu đăng v2. | Giữ v2 chờ duyệt, không dùng quyết định duyệt v1 cho v2. | v2 ở trạng thái chờ duyệt; nhật ký có 0 lệnh đăng và 0 lượt bàn giao từ v2. |
| Bàn giao quá hạn | Đặt hạn xác nhận 60 giây; bên nhận lưu `TV-04` nhưng không trả xác nhận. Đưa đồng hồ tới giây 61. | Đánh dấu quá hạn để đối soát, không báo đã bàn giao thành công hoặc tự tạo yêu cầu mới. | `TV-04` ở trạng thái quá hạn, có 1 việc đối soát; bên nhận vẫn có đúng 1 hồ sơ, bên gửi không ghi nhận thành công. |
