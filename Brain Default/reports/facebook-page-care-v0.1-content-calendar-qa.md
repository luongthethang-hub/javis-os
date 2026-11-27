# Kiểm định độc lập lịch nội dung Fanpage 7 ngày — v0.1

- **Mã việc:** FB-CARE-V0.1-QA-CALENDAR
- **Artifact được kiểm:** `reports/facebook-page-care-v0.1-content-calendar.md`
- **Phiên bản:** v0.1
- **Người tạo artifact:** Chuyên gia Nội dung & Cộng đồng Facebook
- **Người kiểm định độc lập:** Kiểm định vận hành độc lập
- **Phạm vi:** Kiểm tra tĩnh nội dung file; không đăng, gửi, lên lịch hoặc thao tác Facebook.
- **Mức bằng chứng:** **E1** — đọc trực tiếp toàn bộ artifact trong lượt kiểm định.
- **Nguồn chuẩn:** yêu cầu bước kiểm định của Chủ nhóm; `reports/hien-chuong-van-hanh-cong-ty-cam-v1.md`.

## Kết quả từng tiêu chí

| Tiêu chí | Kết quả | Bằng chứng quan sát | Phát hiện |
|---|---|---|---|
| Đủ 7 ngày | **PASS** | Có đủ các mục `Ngày 1` đến `Ngày 7`, không trùng hoặc thiếu số ngày. | Không có lỗi. |
| Mỗi ngày có mục tiêu | **PASS** | Cả 7 mục đều có trường `Mục tiêu`. | Không có lỗi. |
| Mỗi ngày có chủ đề/hook | **PASS** | Cả 7 mục đều có trường `Chủ đề/hook`. | Không có lỗi. |
| Mỗi ngày có định dạng | **PASS** | Cả 7 mục đều có trường `Định dạng`. | Không có lỗi. |
| Mỗi ngày có CTA | **PASS** | Cả 7 mục đều có trường `CTA nháp`. | CTA đều là bản nháp, chưa được gửi/đăng. |
| Mỗi ngày có nguồn/căn cứ | **PASS** | Cả 7 mục đều có trường `Căn cứ`; ngày 6 nêu rõ không có tuyên bố thực tế bên ngoài và yêu cầu nguồn cho chủ đề cụ thể. | Nhiều căn cứ đang là `[CẦN DỮ LIỆU]`, phù hợp bản nháp nhưng phải được điền trước khi duyệt xuất bản. |
| Mỗi ngày có lưu ý kiểm duyệt | **PASS** | Cả 7 mục đều có trường `Lưu ý kiểm duyệt`. | Có cảnh báo riêng về nguồn, dữ liệu cá nhân, bí mật, bản quyền và nội dung rủi ro. |
| Không suy đoán thương hiệu | **PASS** | Phần nguyên tắc cấm suy đoán; tên Trang, sứ mệnh, trụ cột, sản phẩm/dịch vụ và nhận diện đều để placeholder `[CẦN DỮ LIỆU]`. | Không thấy dữ kiện thương hiệu bị tự điền. |
| Không dùng dữ liệu khách hàng | **PASS** | File cấm dữ liệu/hình ảnh nhận diện khách hàng; ngày 4–6 yêu cầu che hoặc không thu thập dữ liệu cá nhân; không có dữ liệu khách cụ thể trong artifact. | Không thấy tên, liên hệ, nội dung inbox hoặc định danh khách hàng. |
| Không chứa hành động đăng/lên lịch | **PASS** | Phạm vi ghi rõ `không đăng, không lên lịch, không gửi tin`; toàn bộ nội dung là lịch nháp và checklist trước duyệt. | Có nhắc giả định về bài “đã thực sự xuất bản” ở ngày 7 nhưng chỉ là điều kiện nội dung/placeholder, không phải thao tác đăng hay lên lịch. |

## Kết luận

- **Kết quả kiểm định artifact:** **PASS**.
- **Trạng thái cổng nghiệm thu:** **ĐẠT** đối với đúng các tiêu chí kiểm tra tĩnh được giao.
- **Phần chưa kiểm:** độ đúng của các dữ kiện sẽ được điền vào placeholder; quyền sử dụng tài sản ảnh/video; tính phù hợp với từng Page sau khi xác minh URL/ID, thương hiệu và nguồn chính thức. Các phần này là **NOT CHECKED** vì chưa có dữ liệu thực để đối chiếu.
- **Lỗi chặn trong phạm vi kiểm:** Không có.
- **Rủi ro còn mở:** Không được dùng kết quả PASS này như phê duyệt đăng. Trước xuất bản vẫn phải điền và xác minh toàn bộ `[CẦN DỮ LIỆU]`, kiểm quyền tài sản và có phê duyệt hành động ra ngoài.
- **Điều kiện thử lại:** thử lại khi nội dung đã được điền cho một Page cụ thể hoặc artifact thay phiên bản; đối chiếu từng tuyên bố với URL/tài liệu chính thức và rà lại dữ liệu cá nhân/quyền hình ảnh.
- **Đường quay về:** giữ nguyên v0.1 ở trạng thái bản nháp, không đăng/lên lịch; nếu bản điền dữ liệu trượt, quay lại placeholder trung tính này.
