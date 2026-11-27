# Cơ Chế Hoạt Động Của Team Doctor Agent (Cấp Độ Tập Đoàn)

## 1. Mục đích & Nguyên tắc
Team **Hội đồng Hội chẩn - Doctor Agent** đóng vai trò như một bộ phận R&D / QA nội bộ và Kiến trúc sư hệ thống tự động, có nhiệm vụ:
- Định kỳ hoặc khi có sự cố phát sinh từ các team nghiệp vụ, hội chẩn để bóc tách nguyên nhân gốc rễ.
- Chuẩn hóa, tối ưu hóa và tái cấu trúc system prompt của từng agent và mô tả mục tiêu của từng team theo chuẩn metaprompt công nghiệp.
- Thiết kế ca kiểm thử hồi quy độc lập (Golden Tests) để đảm bảo prompt mới không gây thoái lui chất lượng hoặc trôi hành vi trước khi cập nhật.

## 2. Nhân sự & Phân công
- **Trưởng hội chẩn Doctor Agent** (`truong-hoi-chan-doctor-agent-2`): Nhận tín hiệu lỗi/nhu cầu, chủ trì hội chẩn, chốt đề xuất CUP và báo cáo duyệt.
- **Bác sĩ Prompt & Workflow** (`bac-si-prompt-workflow-2` - model `claude-sonnet-4-6`): Chuyên trách bóc tách cấu trúc prompt, viết lại prompt theo 6 khối chuẩn, xử lý edge-cases.
- **Bác sĩ Thẩm định & Kiểm thử Độc lập** (`bac-si-tham-dinh-kiem-thu-doc-lap-2` - model `gpt-5.6-sol`): Kiểm thử chéo độc lập, chạy test đối soát baseline vs new prompt, nghiệm thu pass/fail.

## 3. Quy trình tự động chỉnh sửa Prompt & Mô tả Team
1. **Phát hiện & Chẩn đoán**: Thu thập nhật ký lỗi (ví dụ: lỗi công cụ, ảo giác, sai lệch đầu ra).
2. **Kê đơn (CUP - Capability Upgrade Proposal)**: Soạn bản vá unified diff của prompt hoặc mô tả mục tiêu.
3. **Thẩm định & Kiểm thử (Red/Blue)**: Chạy tối thiểu 3 ca test độc lập (ca chuẩn, ca nhiễu/thiếu dữ liệu, ca biên).
4. **Cập nhật & Bàn giao**: Ghi đè vào hồ sơ agent/team khi đạt chuẩn, gửi báo cáo 1 trang cho Chủ duyệt.
