---
name: Vận hành AI Company ổn định
description: Kiểm tra đầu vào, chọn luồng Content, EA hoặc nghiên cứu thị trường và bàn giao lỗi có giới hạn.
group: AI
---

## Khi nào dùng
Khi điều phối việc Content, EA hoặc nghiên cứu thị trường trong Brain Default, nhất là khi provider, công cụ hoặc đầu vào thiếu.

## Chuẩn bị
- Đọc chỉ mục năng lực và xác định một đầu ra có thể nghiệm thu.
- Phân biệt model được cấu hình với model đã chạy. Không đoán khả năng từ tên model.
- Các workflow đã khai execution_guard được host kiểm đầu vào và giới hạn chạy. Nội dung skill không thay thế lớp kiểm này.
- Kiểm tra workflow có trong danh sách chạy và công cụ cần dùng thực sự có ở lượt hiện tại. Lượt chỉ chữ không thể compile, render hay xác minh web.

## Quy trình
1. Hỏi đáp ngắn: trả lời trực tiếp. Một việc cần một người chính; chỉ thêm reviewer khi có sản phẩm cần kiểm.
2. Content đào tạo lái xe: chỉ dùng san-xuat-content-video-ngan khi đã có provider được smoke test thành công. Hiện CLI bị chặn bởi tài khoản nên giữ workflow tắt, dùng skill chuyen-viec-sang-app-desktop bàn giao chính brief qua Claude Desktop. Mỗi yêu cầu tối đa một lần bàn giao; lỗi thì dừng, không thử nhiều app liên tiếp. Khi CLI sẵn sàng, dùng workflow với brief đủ mục tiêu, đối tượng, kênh và dữ kiện. Chỉ soạn chữ. Tác giả, reviewer, biên tập; tối đa một lượt sửa và rà lại.
3. Dựng tệp video thật: giao bien-tap-video-ngan riêng, kèm đường dẫn, quyền shell/FFmpeg và đầu ra. Nếu không có công cụ thì trả BỊ CHẶN CÔNG CỤ, không giả báo đã render.
4. EA: dùng phat-trien-ea-ban-va với JSON Task Card đủ GOAL, ENV, CODE, EXPECTED, CONSTRAINTS, ACCEPTANCE. Chỉ soạn và rà patch; chưa compile phải ghi rõ. Cổng compile/regression cần môi trường tách biệt và yêu cầu cụ thể của chủ.
5. Trading research: dùng phien-hop-phan-tich-thi-truong với hồ sơ có nguồn, đơn vị, thời điểm và giới hạn độ mới. Chưa đủ thì dừng ở cửa kiểm dữ liệu. Không đưa công cụ MT5 hoặc tài khoản vào luồng nghiên cứu.
6. Affiliate: chỉ chuẩn bị brief/so sánh khi có offer, điều khoản và tracking đã cung cấp. Chưa đủ nguồn thì CẦN DỮ LIỆU; chưa tạo tự động đăng hoặc mua dịch vụ.
7. Lỗi xác thực/hạn mức: ghi nguyên mã lỗi đã quan sát được, chỉ chuyển sang nguồn thực sự sẵn sàng và giữ nguyên phạm vi quyền. Lỗi dữ liệu, quyền hay công cụ không được xử lý bằng đổi model liên tục.
8. Khi runtime dừng: bàn giao run_id, bước đã xong, bằng chứng, lý do dừng và phần cần bổ sung. Xem lịch sử workflow trước khi khôi phục. Không tự chạy lại hành động ra ngoài có trạng thái chưa xác định.
9. Đổi prompt/workflow theo yêu cầu chủ phải có phiên bản và đường hoàn tác; không lập lịch tự sửa hàng loạt.

## Bẫy
- Tác giả và reviewer khác vai nhưng cùng họ model không phải phản biện chéo mô hình.
- Hạn token báo cáo chỉ ngăn công việc tiếp theo sau khi nhận usage; không bảo đảm chặn tiền đang phát sinh trong một request.
- Giới hạn bước gọi model không tính được mọi retry nội bộ của SDK/provider.
- Lịch sử lưu đầu ra từng bước; khôi phục tự động cho workflow tuần tự chưa được triển khai. Không hứa resume tự động.
- Không tự nối GitHub, đăng nhập, tạo token, tăng quyền hoặc bỏ chặn policy để chạy được.

## Kiểm chứng
Bàn giao gồm: sản phẩm; vị trí; model thực chạy nếu có; phần đã kiểm; phần chưa kiểm; trạng thái HOÀN TẤT / CHỜ CHỦ DUYỆT / CẦN DỮ LIỆU / BỊ CHẶN.
