# Rà soát dữ liệu và hiện trạng hệ thống

Ngày rà soát: 2026-11-19. Chỉ đọc qua Javis hub.

## Bằng chứng hiện trạng
- `Javis/index.md`: 22 agents, 11 skills, 3 workflows (1 bật), 0 loops, 29 plugins (28 chạy).
- `javis_team list_agents`: có 22 agent; chỉ 2 có model riêng: `ky-su-ea---claude` = sonnet, `phan-bien-cheo---chatgpt` = gpt-5.5. Cả 20 agent còn lại dùng model chính.
- `javis_team list`: 2 team active: CEO SubAgents (7 thành viên) và Phân tích Thị trường (9 thành viên).
- Workflows: Sản xuất Content & Video ngắn đang active; Kế hoạch ngày thực dụng và Phiên họp phân tích thị trường đang off. Index ghi agent không có workflow sử dụng: dieu-phoi-ai-company, giam-doc-marketing-nganh-dao-tao-lai-xe, javis-core, ky-su-ea---claude, nhat-ky-thuc-thi, phan-bien-cheo---chatgpt.
- Schedule list trả về 1 nhắc/lịch: tự học Javis mỗi 8 giờ; index ghi không có loop.
- `javis_connections` chỉ trả ghi chú về cách hiểu trạng thái, không liệt kê connector hay trạng thái cụ thể. Do đó không xác định được nguồn trading/news đã đấu; không được kết luận không có kết nối.
- Tìm tool kiểm tra provider chỉ tìm được `javis_team`, không có công cụ đọc trạng thái đăng nhập/health model. Không chạy được tác vụ thử trực tiếp cho Claude subscription hoặc OpenAI OAuth từ các công cụ trong lượt này. Khả dụng thực tế: chưa kiểm chứng.

## Nhận xét
- Chưa thấy bản sao agent/skill/workflow hiển nhiên trong danh mục; có vùng trách nhiệm giao nhau cần phân ranh: CIO / Trưởng phòng Nghiên cứu / Phân tích thị trường an toàn; Giám đốc Marketing / Trợ lý Content. Đây là chồng lấn phạm vi, chưa đủ bằng chứng gọi là trùng lặp.
- Hầu hết agent chưa có model riêng: 20/22 dùng model chính. Chỉ hai agent có model riêng, nhưng provider thực tế cần xác minh qua cấu hình/Models.
- Bước kiểm chứng provider cần chạy tác vụ ngắn riêng bằng từng provider và lưu kết quả lỗi/thành công cùng thời điểm; kiểm tra trang Models/Kết nối chỉ khi có quyền đọc trạng thái trực tiếp.
