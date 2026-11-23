# Quản trị Đội nhóm và Điều phối Token trong Liên minh AI

> Nạp và tinh chỉnh từ tài liệu Quản lý Đội nhóm AI theo kiến trúc phân tầng 3 lớp (Hybrid Integration), ngày 23/11/2026.

## 1. Phân tầng Quản trị và Quyền lực
- **Layer 0 (Lương Thế Thắng - Principal):** Quyền tối cao. Duyệt các quyết định chiến lược, T1/rủi ro cao, ngân sách tài chính, API token và phê duyệt hành động lớn.
- **Layer 1 (Javis Core & Điều phối viên):** Nhạc trưởng điều phối, phân rã công việc, theo dõi tiến độ, kiểm toán logic và giám sát tiêu hao token.
- **Layer 2 (Worker Agents / Tools / Subagents):** Thực thi chuyên môn (lập trình MQL5, phân tích Ads, dựng video, viết bài, review chất lượng).

## 2. Ma trận Phân bổ Nhiệm vụ theo Phân tầng Nguồn lực
Hệ thống ưu tiên các gói thuê bao cố định (ChatGPT Plus/Pro, Claude Code, Google AI qua Antigravity CLI) thay vì trả phí lẻ từng token. Phân bổ nhiệm vụ dựa trên rủi ro kỹ thuật và cửa sổ hạn mức:

- **Tier 1 (Tác vụ nhẹ, nhanh, rủi ro thấp):**
  - Loại việc: Định tuyến, phân loại, trích xuất dữ liệu có cấu trúc, tóm tắt ngắn.
  - Model ưu tiên: Flash / Local / Fast models (gemini-3.8-flash, gpt-4o-mini).
  - Mục tiêu: Tốc độ phản hồi dưới 2 giây, không chiếm dụng hạn mức suy luận sâu.

- **Tier 2 (Tác vụ trung bình, nghiên cứu, tổng hợp):**
  - Loại việc: Thu thập dữ liệu đa nguồn, tổng hợp tin tức, dự thảo kịch bản, biên tập sơ bộ.
  - Model ưu tiên: Medium / CLI engines (gemini-3.8-flash-high, Grok Build).
  - Mục tiêu: Cân bằng ngữ cảnh dài và độ tin cậy.

- **Tier 3 (Tác vụ chuyên sâu, rủi ro cao, coding, kiến trúc):**
  - Loại việc: Viết và debug EA MQL5, audit bảo mật, kiến trúc đa luồng, phản biện logic.
  - Model ưu tiên: Claude (Sonnet / Opus qua Claude Code hoặc API), DeepSeek-R1, GPT-5 / Reasoning.
  - Mục tiêu: Độ chính xác và an toàn tuyệt đối; bắt buộc có kiểm chứng độc lập.

- **Nhiệm vụ không rõ yêu cầu:**
  - Chuyển cho agent phân tích yêu cầu trước để chuẩn hóa prompt, tránh tiêu hao token vô ích.

## 3. Hồ sơ Năng lực Agent (10 Trường Tiêu chuẩn)
Mỗi worker agent duy trì hồ sơ năng lực để tối ưu phân công:
1. Tên agent và model nền tảng (ví dụ: ky-thuat-dung-video chạy trên gemini-3.8-flash-medium).
2. Xếp hạng năng lực cốt lõi (suy luận, lập trình, ngôn ngữ, đa phương tiện).
3. Hạn ngạch và chi phí vận hành (thuê bao cố định hoặc trần token API).
4. Ngưỡng ngữ cảnh tối đa (ví dụ: Antigravity 2M tokens so với API thông thường).
5. Tốc độ phản hồi trung bình.
6. Chuyên môn mạnh và điểm hạn chế đã kiểm chứng.
7. Tỷ lệ hoàn thành nhiệm vụ đạt chuẩn lần đầu (First-pass Yield).
8. Token trung bình tiêu thụ trên mỗi loại tác vụ.
9. Chi phí hoặc tài nguyên trên một kết quả đạt chuẩn (Cost per Verified Deliverable).
10. Trạng thái khả dụng và khóa xung đột tài nguyên.

## 4. Ngưỡng Giám sát và Cơ chế Can thiệp (Escalation)
- **Giới hạn vòng lặp sửa lỗi:** Tối đa 3 vòng sửa lỗi (N = 3). Nếu sau 3 lần vẫn không đạt tiêu chuẩn nghiệm thu, lập tức dừng và chuyển tiếp lên Layer 0 hoặc đổi sang model mạnh hơn.
- **Context Gating:** Giữ ngữ cảnh trao đổi tóm tắt dưới 3.000 tokens khi gọi các API ngoài.
- **Theo dõi hạ tầng:** Dữ liệu tiêu hao token được ghi nhận tự động vào cơ sở dữ liệu token_usage.db, không yêu cầu agent phải tự tính toán số học thủ công.

## 5. Quy tắc Tối ưu hóa Định kỳ
- **Hàng tuần:** Rà soát danh sách 10 nhiệm vụ tiêu hao nhiều tài nguyên nhất và 10 nhiệm vụ có tỷ lệ làm lại cao nhất để phát hiện nút thắt cổ chai.
- **Hàng tháng:** Cập nhật lại ma trận phân bổ dựa trên số liệu thực chứng, ưu tiên tối ưu cấu trúc quy trình (Orchestration) trước khi thay đổi model.
