# Đề xuất phân công 4 mảng

Căn cứ inventory `Javis/index.md` hiện có: 22 agents, 11 skills, 3 workflows (1 active), 0 loops. Đây là đề xuất phân công, không xác nhận rằng các chỉ số đã được đo hay mọi nguồn dữ liệu đã kết nối.

## 1. Trading / EA
- **Phụ trách:** Kỹ sư EA - Claude (bản nháp/sửa mã và mô phỏng); Kiểm chứng dữ liệu xác nhận số liệu/nguồn; Quản trị Rủi ro rà giới hạn; Phản biện chéo - ChatGPT rà độc lập khi phù hợp. Các vai này hiện có trong inventory. Không đặt/sửa lệnh, không thao tác MT5.
- **Đầu vào:** yêu cầu và đặc tả EA, mã nguồn/diff, dữ liệu lịch sử có nguồn và đơn vị, giả định mô phỏng, giới hạn rủi ro.
- **Đầu ra:** bản mã nháp/diff, kết quả mô phỏng có điều kiện chạy, danh sách lỗi/giả định, biên bản phản biện và điểm cần chủ quyết.
- **KPI đề xuất:** tỷ lệ yêu cầu có đặc tả và nguồn dữ liệu; lỗi nghiêm trọng còn mở; mức tái lập mô phỏng; thời gian đến bản nháp. Chưa có baseline trong inventory.

## 2. Content
- **Phụ trách:** Trợ lý Content cá nhân; có thể dùng workflow “Sản xuất Content & Video ngắn” (active), Phản biện nội dung, Nghiên cứu & Kiểm chứng, Biên tập Video ngắn, Kiểm duyệt & Chuẩn bị đăng.
- **Đầu vào:** mục tiêu, phân khúc, kênh, lịch, hồ sơ thương hiệu, tư liệu có quyền sử dụng và dữ kiện đã xác nhận.
- **Đầu ra:** nội dung/kịch bản/caption/edit brief, nguồn và giả định, rubric, trạng thái chờ chủ duyệt.
- **KPI đề xuất:** tỷ lệ nội dung qua duyệt lần đầu; lỗi dữ kiện/riêng tư/bản quyền; thời gian sản xuất; chỉ số kênh (lưu, xem hết, hỏi tư vấn) nếu kết nối và có baseline. Không tự đăng.

## 3. Affiliate
- **Phụ trách:** hiện chưa thấy agent chuyên affiliate trong inventory. Trợ lý Content cá nhân có thể soạn nháp theo hướng dẫn; Phản biện nội dung rà tuyên bố và công bố liên kết. Phải xác minh inventory/kết nối trước khi giao đo hiệu quả.
- **Đầu vào:** sản phẩm, điều khoản chương trình, tracking link, bằng chứng/nguồn, quy định công bố quan hệ thương mại và kênh.
- **Đầu ra:** bản nháp có công bố affiliate rõ, link đã kiểm tra, ghi chú tuân thủ; chờ chủ duyệt trước công bố.
- **KPI đề xuất:** lượt nhấp, chuyển đổi được xác nhận, doanh thu/hoa hồng đối soát, tỷ lệ hoàn/huỷ và lỗi công bố. Hiện chưa có số liệu hay nguồn affiliate xác nhận.

## 4. Hạ tầng
- **Phụ trách:** Điều phối AI Company điều phối; chưa thấy agent vận hành hạ tầng chuyên trách trong inventory. Kỹ sư EA chỉ xử lý phần mã EA, không mặc định giao quản trị hệ thống. Xác minh connector và chủ sở hữu vận hành trước khi phân công kỹ thuật.
- **Đầu vào:** danh mục agent/skill/workflow/plugin, trạng thái provider và connector, lỗi có log, giới hạn/quyền, thay đổi được chủ duyệt.
- **Đầu ra:** báo cáo trạng thái, lỗi có bằng chứng, đề xuất thay đổi có phương án hoàn tác; không tự đổi cấu hình/quyền.
- **KPI đề xuất:** tỷ lệ workflow/job thành công, thời gian khôi phục, lỗi lặp lại, mức sử dụng provider và chi phí theo nguồn có dữ liệu. Hiện inventory không cung cấp baseline vận hành/chi phí.

## Điều kiện áp dụng
Chủ xác nhận quyền sở hữu từng mảng, KPI/baseline và nguồn dữ liệu; bổ sung vai affiliate/hạ tầng nếu cần. Mọi KPI hiệu suất chỉ báo cáo sau khi có nguồn nối và kỳ đo xác định.
