---
name: Điều phối Đội nhóm & Token
description: Quy trình phân rã việc, định tuyến agent theo rủi ro, kiểm soát vòng lặp và nghiệm thu kết quả trong Liên minh AI.
group: AI
---

# Điều phối Đội nhóm & Token

## Khi nào dùng
Kích hoạt khi nhận nhiệm vụ đa bước, dự án liên phòng ban (phát triển EA, sản xuất video, marketing đa kênh) hoặc cần phân công công việc giữa nhiều agent AI trong liên minh.

## Nguyên tắc cốt lõi
1. **Dynamic Gating:** Tác vụ đơn lẻ, tra cứu thông tin hoặc thao tác trực tiếp chạy Fast Path qua model Flash/nhẹ, bỏ qua quy trình 9 bước. Chỉ kích hoạt toàn bộ quy trình với dự án phức tạp.
2. **Quyền hạn Layer 0:** Mọi tác vụ cấp độ HIGH/CRITICAL (sửa repo gốc, xuất bản nội dung, can thiệp tài chính) bắt buộc có phê duyệt từ Layer 0.
3. **Phân bổ theo rủi ro:** Giao việc theo Tier (Tier 1: Flash, Tier 2: Medium/CLI, Tier 3: Reasoning/Sonnet/Opus). Không dùng model đắt tiền cho việc model nhẹ đã làm tốt.

## Quy trình Điều phối 5 bước Tinh gọn

### Bước 1: Phân rã và Đánh giá Rủi ro
- Tách bài toán thành các mục tiêu con cụ thể (subtasks).
- Xác định mức rủi ro kỹ thuật: Thấp (đọc/tra cứu), Trung bình (soạn thảo/tổng hợp), Cao (code core/quyết định kiến trúc).

### Bước 2: Định tuyến và Chọn Agent Ứng viên
- Đối chiếu ma trận phân bổ nhiệm vụ trong wiki `wiki/quan-tri-doi-nhom-va-dieu-phoi-token.md`.
- Chọn agent đáp ứng đủ ngưỡng chất lượng với mức tiêu hao tài nguyên thấp nhất.
- Chỉ định agent phản biện độc lập (Red Team / QA) nếu nhiệm vụ thuộc nhóm rủi ro cao.

### Bước 3: Phát hành Brief Công việc Chuẩn hóa
Mọi nhiệm vụ giao đi phải kèm Tiêu chí Nghiệm thu (Acceptance Criteria):
- **Mục tiêu cụ thể:** Định rõ kết quả cần đạt.
- **Phạm vi & Ràng buộc:** Tài liệu tham chiếu, công cụ được phép dùng, những việc cấm thực hiện.
- **Định dạng đầu ra:** File path, định dạng cấu trúc, ngôn ngữ bắt buộc.
- **Trần tài nguyên:** Giới hạn token tối đa hoặc số lượt tool calls cho phép.

### Bước 4: Giám sát và Khống chế Vòng lặp (Circuit Breaker)
- Theo dõi tiến độ từng bước.
- **Giới hạn sửa lỗi N = 3:** Nếu một agent không đạt nghiệm thu sau 3 lần chỉnh sửa, lập tức dừng vòng lặp, ghi nhận nguyên nhân và chuyển cấp (escalate) lên model cấp cao hơn hoặc xin ý kiến Layer 0.

### Bước 5: Đánh giá và Nghiệm thu
- Kiểm tra tính đúng đắn dựa trên bằng chứng kiểm thử thực tế (E1/E2).
- Cập nhật hiệu năng vào Second Brain nếu phát hiện điểm mù hoặc cơ hội tối ưu mới.
