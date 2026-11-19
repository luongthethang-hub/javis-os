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
1. Hỏi đáp ngắn: trả lời trực tiếp. Điều phối AI Company là đầu mối cho việc thường lệ; chỉ mời Kiểm chứng dữ liệu, Phản biện chéo hoặc Quản trị Rủi ro theo yêu cầu của đầu ra.
2. Content đào tạo lái xe: chỉ dùng san-xuat-content-video-ngan khi đã có provider được smoke test thành công. Nếu runtime chưa hỗ trợ execution_guard hoặc provider chưa chạy được, giữ workflow tắt cho chạy nền. Chỉ dùng đường thay thế đã kiểm chứng và phù hợp với dữ liệu được phép chuyển. Mỗi yêu cầu tối đa một lần bàn giao; lỗi thì dừng, không thử nhiều app liên tiếp. Khi CLI sẵn sàng, dùng workflow với brief đủ mục tiêu, đối tượng, kênh và dữ kiện. Chỉ soạn chữ. Tác giả, reviewer, biên tập; tối đa một lượt sửa và rà lại.
3. Dựng tệp video thật: giao bien-tap-video-ngan riêng, kèm đường dẫn, quyền shell/FFmpeg và đầu ra. Nếu không có công cụ thì trả BỊ CHẶN CÔNG CỤ, không giả báo đã render.
4. EA: dùng phat-trien-ea-ban-va với JSON Task Card đủ GOAL, ENV, CODE, EXPECTED, CONSTRAINTS, ACCEPTANCE. Chỉ soạn và rà patch; chưa compile phải ghi rõ. Cổng compile/regression cần môi trường tách biệt và yêu cầu cụ thể của chủ.
5. Trading research: dùng phien-hop-phan-tich-thi-truong với ba vai Kiểm chứng dữ liệu, Phân tích thị trường và Quản trị Rủi ro. Hồ sơ cần nguồn, đơn vị, thời điểm và giới hạn độ mới. Chưa đủ thì dừng ở cửa kiểm dữ liệu. Chỉ mời chuyên viên vĩ mô, dòng tiền hoặc CIO khi có câu hỏi cụ thể. Không đưa công cụ MT5 hoặc tài khoản vào luồng nghiên cứu.
6. Affiliate: Giám đốc Marketing phụ trách lựa chọn sản phẩm và đo chuyển đổi thử nghiệm. Chỉ chuẩn bị brief/so sánh khi có offer, điều khoản và tracking đã cung cấp. Chưa đủ nguồn thì CẦN DỮ LIỆU; chưa tạo tự động đăng hoặc mua dịch vụ.
7. Lỗi xác thực/hạn mức: ghi nguyên mã lỗi đã quan sát được, chỉ chuyển sang nguồn thực sự sẵn sàng và giữ nguyên phạm vi quyền. Lỗi dữ liệu, quyền hay công cụ không được xử lý bằng đổi model liên tục.
8. Khi runtime dừng: bàn giao run_id, bước đã xong, bằng chứng, lý do dừng và phần cần bổ sung. Xem lịch sử workflow trước khi khôi phục. Không tự chạy lại hành động ra ngoài có trạng thái chưa xác định.
9. Đổi prompt/workflow theo yêu cầu chủ phải có phiên bản và đường hoàn tác; không lập lịch tự sửa hàng loạt.


## Bàn giao giữa các phòng
- Chủ doanh nghiệp duyệt mục tiêu, ngân sách và hành động ra ngoài. Javis Core tiếp nhận, giao việc qua cơ chế của chủ và nhận báo cáo. Ban Điều hành AI Company, do COO dẫn, xử lý việc đa phòng, ưu tiên và ngoại lệ.
- Phòng Marketing và Nội dung chịu trách nhiệm tuyển sinh, nội dung, video và affiliate trong phạm vi brief. Phòng Kỹ thuật và EA chịu trách nhiệm bản vá và kiểm thử mô phỏng. Team Phân tích Thị trường chịu trách nhiệm hồ sơ nghiên cứu và kiểm soát rủi ro.
- Trưởng phòng giữ một người chịu trách nhiệm chính cho mỗi việc, kèm deadline đã xác nhận và người kiểm định. Kiểm định độc lập có thể yêu cầu sửa hoặc chặn. Ghi lỗi, bằng chứng và tiêu chí mở lại.
- Task Card bàn giao gồm mã việc cha, mã bàn giao ổn định, phòng gửi, phòng nhận, người chịu trách nhiệm, mục tiêu, đầu vào và nguồn, phạm vi quyền, hạn, tiêu chí đạt, phiên bản và đường dẫn đầu ra. Trường thiếu ghi rõ; không dùng mã mới để thử lại cùng một việc.
- Thành viên Team gửi phiếu về điều hành. Chỉ Javis Core hoặc chủ trong ngữ cảnh được host cho phép mới dispatch sang Team nhận. Kiểm tra job và trạng thái nghiệm thu trước khi dùng kết quả cho bước kế tiếp.
- Báo cáo ngắn gồm mã việc, trạng thái, sản phẩm và bằng chứng, việc chưa đạt, người xử lý tiếp và quyết định cần chủ. Khi báo cáo đến, ghi nhận và chờ yêu cầu phù hợp để chuyển bước. Dừng tại cổng cấp quyền cho xuất bản, gửi tin, chi tiền hoặc thay đổi tài khoản.

## Bẫy
- Tác giả và reviewer khác vai nhưng cùng họ model không phải phản biện chéo mô hình.
- Hạn token báo cáo chỉ ngăn công việc tiếp theo sau khi nhận usage; không bảo đảm chặn tiền đang phát sinh trong một request.
- Giới hạn bước gọi model không tính được mọi retry nội bộ của SDK/provider.
- Lịch sử lưu đầu ra từng bước; khôi phục tự động cho workflow tuần tự chưa được triển khai. Không hứa resume tự động.
- Không tự nối GitHub, đăng nhập, tạo token, tăng quyền hoặc bỏ chặn policy để chạy được.

## Kiểm chứng
Bàn giao gồm: sản phẩm; vị trí; model thực chạy nếu có; phần đã kiểm; phần chưa kiểm; trạng thái HOÀN TẤT / CHỜ CHỦ DUYỆT / CẦN DỮ LIỆU / BỊ CHẶN.
