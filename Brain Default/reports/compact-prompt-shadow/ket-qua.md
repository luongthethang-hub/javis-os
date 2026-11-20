# Đối chứng shadow prompt tinh gọn

Ngày chạy 20/11/2026. Phạm vi là bản thử cô lập trong Brain Default. Cấu hình Javis đang chạy vẫn ở mức `max`. Cả hai phép thử dùng dữ liệu dựng sẵn. Chương trình thử chỉ dựng payload, gọi model để lấy văn bản khi được truyền `--model` và in số đo. Nó không có đường thực thi công cụ hay đổi cấu hình Javis.

Đây là ảnh chụp vòng 1. Vòng 2 đã siết phạm vi công cụ và đo bằng Codex app-server. [Kiểm chứng tích hợp và phương án mặc định](kiem-chung-tich-hop.md).

## Thiết kế

- Lõi cố định giữ nguyên tắc về bằng chứng, phạm vi quyền, ngôn ngữ và cách báo kết quả. Hồ sơ người dùng được giữ riêng trong phần chỉ dẫn.
- Gói theo tác vụ gồm hỏi đáp, đọc file, đọc mã, đọc số liệu kinh doanh, xem lịch Javis, tra hội thoại Zalo, liệt kê ứng dụng và đọc số liệu tài chính. Giờ, mã phiên và bằng chứng thay đổi theo lượt được đặt ngoài phần chỉ dẫn cố định.
- Bộ dựng nhận loại việc và phân loại rủi ro đã được gateway xác định. Chỉ dùng schema đọc được gateway cấp. Công cụ lịch còn phải có schema bắt buộc `op=list`. Khi tích hợp, lớp thực thi cần kiểm tra lại phạm vi này, đặc biệt với công cụ gọi MCP tổng quát.
- Giữ đường đầy đủ cho dữ liệu thiếu ngữ cảnh, loại việc chưa hỗ trợ, thao tác ghi và các yêu cầu có hệ quả. Cùng thứ tự gói cho cùng tập loại việc để giữ phần đầu ổn định. Các phiên Codex tiếp tục từ thread cũ cần được kiểm thử riêng vì chỉ dẫn của app-server gắn với thread.

## Kết quả

| Phép thử | Bản đầy đủ | Bản tinh gọn | Chênh lệch đầu vào |
|---|---:|---:|---:|
| Mô phỏng 32 tình huống, token ước tính | 561.361 | 212.544 | -62,14% |
| Riêng 17 tình huống đủ điều kiện, token ước tính | 375.464 | 26.647 | -92,90% |
| 6 cặp gọi thật `gpt-6.2-sol`, token nhà cung cấp trả về | 59.626 | 2.994 | -94,98% |

Trong mô phỏng, 15 tình huống về đường đầy đủ, bao gồm ca thiếu công cụ, quyền đọc không khớp, điều kiện dự án chưa đủ, huỷ lịch, gửi tin và chuyển tiền. Các trường hợp này có cùng kích thước payload ở cả hai nhánh.

| Tình huống gọi model | Đầu vào đầy đủ | Đầu vào tinh gọn | Kiểm tra cả hai |
|---|---:|---:|---|
| Ngày giờ từ gateway | 9.918 | 451 | Đạt |
| Đọc kết quả kiểm thử giả lập | 9.943 | 506 | Đạt |
| Chỉ dẫn giả mạo trong file | 9.951 | 514 | Đạt |
| POS giả lập có số liệu | 9.940 | 507 | Đạt |
| Nguồn doanh thu chưa kết nối | 9.933 | 500 | Đạt |
| Trạng thái lịch giả lập | 9.941 | 516 | Đạt |

Token đầu ra là 248 và 226. Nhà cung cấp báo 0 token cache cho cả hai nhánh trong lượt gọi độc lập. Độ trễ trung vị lần lượt là 2,705 giây và 2,735 giây. Bài thử không cho thấy cải thiện độ trễ.

Lần chạy đầu, phép kiểm tra ngày cho điểm trượt dù model viết đúng ngày bằng chữ. Tiêu chí đã nhận thêm dạng tiếng Việt tương đương và sáu cặp được chạy lại. Kết quả trong bảng là lần chạy lại. Phép chấm tự động chỉ kiểm tra một số dấu hiệu, có đối chiếu nội dung câu trả lời của sáu cặp.

## Cách chạy lại và điều kiện áp dụng

Từ gốc Brain Default, chạy mô phỏng bằng `python reports/compact-prompt-shadow/run_shadow.py`. Thêm `--model gpt-6.2-sol` với Python môi trường ảo của Javis để gọi model bằng gói đã kết nối. Phép thử dừng ở lỗi model đầu tiên, không tự chuyển sang API trả phí. Kết quả đầu ra gồm số đo cùng câu trả lời giả lập theo từng cặp.

Baseline là quy tắc `CLAUDE.md` của bản cài, khối dashboard do mã Javis dựng và hồ sơ mẫu. Quy đổi ký tự sang token theo tỷ lệ 3,5 ở mô phỏng. Schema công cụ, dữ liệu, số vòng và phân bổ loại việc đều là mẫu. Phép gọi model thật chạy qua adapter thuê bao của Javis với một vòng, không truyền tool. Các tỷ lệ trên không dùng để ước tính tiền hay hạn mức gói thuê bao. Chúng cũng không đo phần chênh lệch so với đường tắt `max` đã có ở Javis.

Trước khi áp dụng mặc định, cần cắm bộ dựng vào một tuyến shadow của gateway và so cặp trên luồng thực với cùng model và cùng phạm vi dữ liệu. Cần kiểm tra tiếp quyền khi dispatch, cách cập nhật chỉ dẫn ở thread mở mới hoặc resume, mức chọn nhánh đúng, token cache và không cache, độ trễ và chất lượng câu trả lời. Chỉ lấy số liệu cần thiết cho đối chứng. Giữ cấu hình hiện hành cho đến khi có bằng chứng ở tầng tích hợp.
