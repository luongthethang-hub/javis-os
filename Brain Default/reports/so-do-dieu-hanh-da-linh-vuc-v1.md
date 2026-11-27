# Sổ điều hành đa lĩnh vực v1 | 27/11/2026
Thiết kế mục tiêu, không phải cấu hình đã bật.

Chủ duyệt báo cáo và ngoại lệ → Javis điều phối danh mục → đầu mối từng mảng chịu trách nhiệm về khách hàng, kết quả và lợi nhuận → các nhóm chuyên môn thực hiện. Nhóm kiểm tra độc lập báo về Javis. Một người có thể kiêm vai nhưng không tự nghiệm thu sản phẩm mình làm.

| Chuỗi công việc | Bàn giao cần có | Thước đo và nguồn cần xác nhận |
|---|---|---|
| Chiến lược → ngân sách | Mỗi mảng có mục tiêu quý, hạn, trần nguồn lực và điều kiện dừng | Lãi gộp theo mảng từ doanh thu và giá vốn đối soát |
| Marketing → bán hàng | Nội dung đã duyệt, nguồn lead, nhu cầu, người nhận và hạn phản hồi | Lead đủ điều kiện / tổng lead từ CRM |
| Bán hàng → cung ứng | Đơn đã xác nhận, phạm vi cam kết, lịch và năng lực giao | Đơn giao đúng hạn / đơn đến hạn từ sổ đơn |
| Cung ứng → CSKH | Biên bản bàn giao, phản hồi, khiếu nại và người xử lý | Thời gian đóng vụ việc từ nhật ký CSKH |
| Mua hàng → thanh toán | Đề nghị, phê duyệt, nhận hàng, đối chiếu hóa đơn trước khi trình chi | Sai lệch đơn mua và hóa đơn từ sổ đối chiếu |
| Tài chính → chủ | Dòng tiền, công nợ quá hạn, lãi gộp theo mảng; tách tiền đã thu khỏi doanh thu | Sổ kế toán đối chiếu chứng từ; không tự thanh toán |
| Nhân sự, công nghệ, pháp chế → các mảng | Ma trận năng lực, phân quyền tối thiểu, rà nghĩa vụ, phương án khôi phục | Lỗi lặp, thời gian xử lý và số quyền quá hạn từ log |

## Cách chạy một việc
Ghi mã và mảng → chốt người phụ trách, đầu vào, hạn, tiêu chí đạt → giao → kiểm bằng chứng độc lập → gom ngoại lệ vào báo cáo → ghi kết quả. Nếu timeout, kiểm trạng thái trước khi giao lại. Không có nguồn thì để trống số liệu. Không tự gửi khách, xuất bản, thanh toán hay tăng quyền.

## Luật vận hành đang áp dụng
Từ 27/11/2026, toàn bộ sơ đồ này chạy dưới hiến chương `cam-triet-ly-su-menh`, bản áp dụng tại [Hiến chương vận hành công ty CAM v1](hien-chuong-van-hanh-cong-ty-cam-v1.md). Ba vai điều hành (Trưởng ban, Kiến trúc sư, Kiểm định) đã được gắn skill này trong hồ sơ.

## Nhịp đề xuất, chưa đặt lịch
Hằng ngày xử lý việc kẹt, không gửi báo cáo rỗng. Hằng tuần trình một trang: kết quả so mục tiêu, sai lệch và nguyên nhân, tác động tiền/khách, lựa chọn đề nghị, hạn quyết định, liên kết bằng chứng. Hằng tháng so hiệu quả giữa các mảng để giữ, tăng hoặc dừng đầu tư.

## Thí điểm
Hai nhóm hiện hoạt: Team Social thiết kế bàn giao nội dung tới tư vấn; Hội đồng Huấn luyện thiết kế phép thử độc lập. Bốn nhóm lưu trữ không nhận việc. Khi hai đầu ra khớp, thử trên dữ liệu giả, đo thời gian và tỷ lệ đạt ngay lần đầu. Thử một cải tiến trên cùng ca; chỉ nhân rộng nếu tốt hơn mà không mất cổng duyệt. Nếu không đạt, giữ bản cũ. Chưa có nguồn kinh doanh được kiểm chứng cho các KPI trên.