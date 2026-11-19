# Đề xuất: đánh giá sau việc và lịch rà soát

Ngày: 2026-11-19  
Trạng thái: đề xuất, chờ Chủ duyệt  
Phạm vi: chỉ thiết kế; chưa tạo lịch, chưa sửa agent/skill/workflow.

## Vòng đánh giá sau khi đóng việc

1. Chỉ chấm việc đã có đầu ra và tiêu chí hoàn thành; lưu mã việc, ngày, mảng, đầu vào/đầu ra và nguồn bằng chứng.
2. Chấm 0-2 cho mỗi tiêu chí: đúng yêu cầu/phạm vi; độ chính xác và khả năng kiểm chứng; an toàn và tuân thủ quyền; hữu ích/đủ dùng; đúng hạn và hiệu quả lượt/tool. Tổng tối đa 10. Ghi riêng lỗi nghiêm trọng, không để điểm cao bù lỗi an toàn.
3. Nếu có lỗi an toàn hoặc dữ kiện bịa: kết quả không đạt, nêu nguyên nhân và biện pháp chặn. 8-10: đạt; 6-7: cần rà soát; 0-5: không đạt. Một việc đơn lẻ chỉ tạo bài học khi có bằng chứng rõ; sửa năng lực chỉ đề xuất khi lỗi lặp lại hoặc có tác động lớn.
4. Wiki chỉ nhận quy trình/khái niệm tái sử dụng có provenance `user` hoặc `source` và citation. Kinh nghiệm chỉ suy ra từ đầu ra của assistant không được ghi thành tri thức chắc chắn; lưu báo cáo đánh giá ở proposals để Chủ xem. Đề xuất sửa capability gồm lỗi, bằng chứng lặp, thay đổi nhỏ, kiểm tra hồi quy và đường lui; chờ duyệt trước khi áp dụng.

## Lịch định kỳ đề xuất

Đề nghị một reminder mỗi tuần, quyền `suggest`, đọc các việc đã đóng trong 7 ngày gần nhất và báo cáo điểm, lỗi nghiêm trọng, bài học có căn cứ, đề xuất sửa. Không tự sửa wiki/capability trong reminder; chỉ tạo bản đề xuất ở `inbox/proposals/`. Giới hạn một báo cáo mỗi kỳ, tối đa 20 việc gần nhất; nếu thiếu log hoặc bằng chứng thì ghi “không xác định”, không suy diễn. Rủi ro chính là log thiếu/không chuẩn làm điểm sai và trùng với reminder tự học hiện có. `Javis/reminders.json` hiện có reminder tự học mỗi 8 giờ ở `suggest`; cần Chủ quyết định nếu lịch tuần mới bổ sung phạm vi riêng hay thay thế/điều chỉnh lịch đó. Không tạo lịch cho tới khi xác định người nhận và tránh trùng lịch.

## Điều kiện áp dụng

- Chốt nguồn log việc đã đóng, người nhận báo cáo và cách phân biệt đánh giá theo từng mảng.
- Chủ duyệt thang điểm, ngưỡng, giới hạn 20 việc và lịch tuần; quyền vẫn ở `suggest`.
- Bất kỳ sửa đổi agent/skill/workflow nào phải là đề xuất riêng trong `inbox/proposals/`, không ghi đè trước khi duyệt.

