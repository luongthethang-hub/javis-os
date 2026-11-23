---
type: preference
created: 2026-11-24
updated: 2026-11-24
source: conversation-memory-distillation-2026-11-24
status: verified
---
# Thói quen Chỉ đạo và Chuyển giao Tác vụ của Chủ sở hữu

Đúc kết từ hành vi tương tác và thói quen giao việc thực tế của Sếp Thắng:

1. **Ủy thác liên ứng dụng để tối ưu chi phí (Thói quen "nhờ vả" Desktop Apps):**
   - Khi Javis gặp bế tắc trên Telegram hoặc tác vụ vượt quá khả năng xử lý tại chỗ, tự động đẩy việc sang ChatGPT Desktop hoặc Claude Desktop qua script `handoff.ps1` để tận dụng gói thuê bao có sẵn, tiết kiệm token API.
   - Claude Desktop ưu tiên cho: đọc file dài, phân tích kiến trúc sâu, refactor mã nguồn phức tạp.
   - ChatGPT Desktop ưu tiên cho: xử lý đa phương tiện, tra cứu web diện rộng, phản biện góc nhìn độc lập.
   - Luôn kiểm tra quota gói trước khi đẩy việc; nếu ứng dụng desktop kẹt hoặc cạn hạn mức, chuyển hướng sang Antigravity/DeepSeek thay vì treo chờ.

2. **Dọn sạch gốc rễ, triệt tiêu thông báo rác:**
   - Khi phát sinh lỗi không có quyền truy cập (như repository bên ngoài không thuộc sở hữu), lập tức ngắt mạch hoàn toàn, xóa bản ghi kẹt và worktree ma; tuyệt đối không để lặp lại cảnh báo vô ích.

3. **Chỉ đạo mức kiến trúc và phê duyệt 1 ký tự:**
   - Sếp Thắng giữ vai trò Tổng chỉ huy (Layer 0), chỉ quyết định mục tiêu và kiến trúc lớn; không bắt sửa code thủ công.
   - Tối ưu hóa phản hồi để phê duyệt nhanh bằng "Y" hoặc "Duyệt", hệ thống tự động hoàn thiện và kiểm thử đến khi xong.

4. **Tiến hóa bền vững (CUP Protocol):**
   - Mọi thói quen, lỗi sửa thành công hoặc cấu hình tối ưu đều phải được đóng gói ngay thành Fact/Wiki/Rule để toàn Liên minh AI (Javis, Antigravity, Claude, DeepSeek) cùng nâng cấp nhận thức.
