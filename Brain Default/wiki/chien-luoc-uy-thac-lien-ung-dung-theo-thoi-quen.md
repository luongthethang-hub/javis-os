---
type: wiki
created: 2026-11-24
updated: 2026-11-24
tags: [lien-minh-ai, dieu-phoi, thoi-quen, toan-luc]
---
# Chiến Lược Ủy Thác Liên Ứng Dụng và Tiến Hóa Theo Thói Quen Người Dùng

Tài liệu chuẩn hóa mô hình vận hành và điều phối tác vụ dựa trên thói quen thực tế của Chủ sở hữu (Sếp Thắng):

## 1. Nguyên Lý Tận Dụng Gói Thuê Bao Sẵn Có (Desktop Handoff)
- **Bản chất:** Thay vì tiêu tốn chi phí gọi API riêng lẻ, hệ thống ưu tiên tối đa việc khai thác các gói thuê bao cố định không giới hạn số lượng câu lệnh (ChatGPT Plus/Pro, Claude Pro qua Desktop/CLI, Antigravity CLI qua tài khoản Google).
- **Cơ chế Handoff:**
  - Script điều phối ngầm (`handoff.ps1`) kiểm soát cửa sổ ứng dụng desktop (tọa độ hiển thị, focus, dán prompt, kiểm tra văn bản đầu ra).
  - Tự động chuyển việc khi tương tác Telegram bị nghẽn hoặc khi cần năng lực chuyên biệt mà Javis Core không tối ưu.
- **Phân định thế mạnh:**
  - `Claude Desktop`: Phân tích ngữ cảnh lớn, đọc toàn bộ file mã nguồn, kiến trúc phần mềm, kiểm tra an toàn logic.
  - `ChatGPT Desktop`: Tạo và phân tích hình ảnh, tra cứu dữ liệu web mở, phản biện chéo độc lập.
  - `Antigravity CLI`: Codebase lớn, compile test trực tiếp, xử lý MQL5, render video OpenMotion.
  - `DeepSeek`: Toán định lượng, giải thuật tối ưu hóa, reasoning sâu chi phí thấp.

## 2. Kiểm Soát Cạn Hạn Mức và Chuyển Hướng Linh Hoạt
- Nhờ vả chỉ có giá trị khi gói ứng dụng còn hạn mức.
- Khi ứng dụng desktop chạm trần hạn mức (quota reset window) hoặc không có cửa sổ hiển thị, hệ thống lập tức kích hoạt đường vòng qua A2A Bus hoặc chuyển cho Antigravity/DeepSeek, cấm để công việc rơi vào trạng thái chờ treo vô tận.

## 3. Quy Chuẩn Phản Hồi Theo Thói Quen Zero Fluff
- Mở đầu bằng kết quả thực tế hoặc hành động sẵn sàng.
- Trình bày dạng danh sách thoáng mắt (spaced bullets), loại bỏ bảng biểu phức tạp trừ khi so sánh kỹ thuật.
- Khi cần duyệt, tóm tắt rõ rủi ro và điều kiện để duyệt nhanh 1 ký tự (`Y`).
