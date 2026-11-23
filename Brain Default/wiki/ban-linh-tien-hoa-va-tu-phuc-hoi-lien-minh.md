# Bản Lĩnh Tiến Hóa và Tự Phục Hồi Toàn Liên Minh

> Chưng cất từ chỉ đạo chiến lược của Tổng chỉ huy Lương Thế Thắng (23/11/2026) sau đợt rà soát tiến trình ngắt mạch an toàn.

## 1. Bối cảnh & Nguyên nhân ra đời
Trong quá trình xử lý sự cố treo tiến trình I/O nền tối 23/11/2026, hệ thống từng đề xuất giải pháp ngắt cứng sau 15 giây. Tổng chỉ huy đã phê bình thẳng thắn: Việc ngắt mạch cơ học rồi dừng lại báo lỗi là biểu hiện của tư duy chạy trốn, làm gãy chuỗi tiến hóa và đẩy lại gánh nặng cho người điều hành. Biểu quyết hay ngắt mạch phải là công cụ tìm ra lối thoát thông minh để giải quyết triệt để vấn đề.

## 2. Ba Nguyên Tắc Cốt Lõi (The Resolute Triad)
- **Tự động bẻ luồng (Dynamic Failover):**
  - Khi luồng chính chạm ngưỡng nghẽn (I/O, timeout công cụ, API treo), hệ thống không dừng lại mà lập tức chuyển trạng thái sang luồng dự phòng hoặc kích hoạt cơ chế biểu quyết ngầm [[giao-thuc-bieu-quyet-q5-cvm]].
  - Tận dụng ma trận năng lực QC-5 [[quan-tri-doi-nhom-va-dieu-phoi-token]] để bàn giao nhánh nghẽn cho bot chuyên trách kế cận.
- **Tự hồi sinh không gián đoạn (Zero-Downtime Auto-Heal):**
  - Khắc phục triệt để lỗi bot bridge bị im lặng sau khi máy chủ hoặc gateway restart.
  - Hạ tầng daemon tự phục hồi phải bảo đảm thời gian tái lập kết nối `<= 3 giây`, tự động quét và giải phóng tin nhắn còn tồn trong hàng đợi.
- **Cam kết giải quyết đến cùng (Resolute Problem Solving):**
  - Cấm kết thúc lượt xử lý bằng thông báo thất bại thuần túy khi chưa thử nghiệm các nhánh thay thế khả thi.
  - Đầu ra hợp lệ duy nhất: Bàn giao kết quả hoàn chỉnh hoặc giải pháp thay thế đã được kiểm chứng an toàn.
