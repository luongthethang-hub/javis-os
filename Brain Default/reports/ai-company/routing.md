# Định tuyến AI Company

Cập nhật ngày 19/11/2026. Đây là cấu hình và kết quả kiểm tra tại máy, không phải bảo đảm model luôn sẵn sàng.

| Loại việc | Vai chính | Reviewer | Tuyến và trạng thái |
|---|---|---|---|
| Content đào tạo lái xe, chỉ chữ | Giám đốc Marketing ngành đào tạo lái xe | Phản biện nội dung khi workflow chạy được | `san-xuat-content-video-ngan` đã chuẩn bị, đang tắt do provider CLI chưa chạy được. Tuyến hiện dùng: skill `chuyen-viec-sang-app-desktop` sang Claude Desktop; một lượt bàn giao, chủ duyệt bản cuối. |
| Dựng video từ tệp thật | Biên tập Video ngắn | Kiểm duyệt & Chuẩn bị đăng | Việc riêng có tệp đầu vào và công cụ render; workflow content chỉ chữ không giả thực hiện bước này. |
| Phát triển EA | Kỹ sư EA | Phản biện chéo | `phat-trien-ea-ban-va`, đang tắt; JSON Task Card bắt buộc. Chỉ soạn và rà mã. Chưa compile, regression, shadow/demo. |
| Nghiên cứu thị trường | Văn phòng phân tích hiện có | Kiểm chứng dữ liệu và Quản trị Rủi ro | `phien-hop-phan-tich-thi-truong`, đang tắt. Chỉ dữ liệu cung cấp có nguồn, đơn vị, thời điểm và thời hạn chấp nhận. Không đặt lệnh. |
| Affiliate | Trợ lý Content cá nhân khi được giao | Phản biện nội dung | Chưa triển khai tự động: thiếu offer, điều khoản và tracking xác nhận. |

Tác giả và reviewer khác vai không đủ để xác nhận khác họ model. Metadata của lượt thực tế mới là bằng chứng. Không nâng quyền hay dùng thêm API để né lỗi provider.

Các giới hạn cứng khai trong workflow được host áp sau khi mã nguồn mới nạp vào Javis. Skill hướng dẫn định tuyến không thể thay thế watchdog hoặc kiểm quyền.
