---
name: ui-ux-thuc-chung
description: "Thiết kế và rà soát UI UX theo hệ thống có sẵn, accessibility, trạng thái tương tác và kiểm chứng responsive."
group: AI
---
# UI UX thực chứng

## Khi nào dùng
Thiết kế, sửa hoặc rà soát giao diện web/app, responsive và accessibility. Không thay kỹ năng biểu đồ, xuất Webcake hoặc dựng video.

## Chuẩn bị
Nguồn: UI UX Pro Max, nextlevelbuilder, MIT, commit 8db36338810d0942567b97ce439affd1619fcf31.
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/8db36338810d0942567b97ce439affd1619fcf31
Bản chưng cất diễn đạt lại từ README, không kèm dataset, search.py hoặc design engine upstream.
Tài liệu và ranh giới chung: `skills/cam-tien-hoa/references/repo-distillation.md` từ gốc brain.

## Quy trình
1. Xác định người dùng, việc cần hoàn thành, màn hình và tiêu chí nghiệm thu; đọc framework, component và theme tokens hiện có.
2. Giữ cấu trúc tốt đang dùng. Chọn hierarchy, typography, spacing và màu theo mục tiêu; không tạo theme song song không cần thiết.
3. Thiết kế trạng thái loading, empty, error, success và disabled phù hợp; giữ dữ liệu form khi lỗi và hướng dẫn sửa cụ thể.
4. Dùng semantics, accessible name, keyboard và focus nhìn rõ; không truyền ý nghĩa chỉ bằng màu. Đối thoại cần quản lý focus.
5. Kiểm tương phản chữ thường tối thiểu 4.5:1; kiểm nội dung dài, xuống dòng, phóng to và reduced motion. Animation không được làm hỏng trạng thái.
6. Kiểm responsive tại các mốc phù hợp, tham khảo 375, 768, 1024, 1440 px; thử keyboard, theme và thao tác lặp nhanh nếu có.
7. Bàn giao tệp đã đổi, kiểm đã chạy, lỗi còn lại và cách kiểm lại. Không có browser hoặc runtime thì ghi rõ mới kiểm tĩnh.

## Bẫy
- Không coi bản thiết kế đẹp hoặc screenshot là bằng chứng chức năng/accessibility đạt.
- Không bịa khả năng tìm kiếm dataset hoặc báo đã cài công cụ upstream.
- Không gửi thông tin dự án riêng ra dịch vụ thiết kế ngoài khi chưa có yêu cầu.
- Có chart hoặc dashboard visualization: nạp dataviz trước thiết kế biểu đồ. Xuất Webcake: dùng html-to-webcake.
- Sửa tối thiểu trên baseline có đường lùi; không tự phát hành hoặc đổi production.

## Kiểm chứng
Input mẫu: yêu cầu rà form đăng ký đang có, kèm code và cách chạy.
Đầu ra kỳ vọng: patch thực tế trong phạm vi được phép; danh sách ca keyboard, lỗi form, narrow viewport đã/chưa chạy.
Ca âm tính: không có dataset thì không gọi search.py; không có browser thì không báo responsive đã đạt; biểu đồ phải chuyển sang dataviz.
