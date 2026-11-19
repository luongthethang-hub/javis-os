---
name: Tiết kiệm token Terminal (RTK)
description: Dùng RTK để rút gọn đầu ra lệnh Terminal trong tác vụ kỹ thuật; giữ đủ chi tiết khi cần xác minh.
group: Năng suất
---

# Tiết kiệm token Terminal với RTK

Khi làm tác vụ kỹ thuật cần chạy lệnh Terminal, ưu tiên `rtk` cho các lệnh nó hỗ trợ như `git status`, `git diff`, `git log`, `rg`, và lệnh test/build. RTK rút gọn đầu ra trước khi đưa vào hội thoại.

- Chỉ dùng RTK cho lệnh đọc trạng thái, tìm kiếm, kiểm tra hoặc build/test thông thường.
- Nếu kết quả thiếu ngữ cảnh để sửa đúng hoặc xác minh, chạy lại lệnh đầy đủ bằng `rtk bypass <lệnh>` hoặc lệnh gốc.
- Không rút gọn nội dung người dùng cần xem, thông báo lỗi quan trọng, diff cần kiểm duyệt, hay bằng chứng kiểm tra cuối.
- Đừng gộp lệnh phá huỷ hoặc thay đổi dữ liệu vào lệnh rút gọn; kiểm tra tác động trước khi chạy.
- RTK chỉ giảm phần đầu ra Terminal được hỗ trợ, không tự giảm chi phí mọi lời gọi model hay hội thoại.
