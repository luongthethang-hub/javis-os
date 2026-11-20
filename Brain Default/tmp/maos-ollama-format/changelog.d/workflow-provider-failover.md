---
bump: minor
title: Let guarded text workflows switch providers once
---

## vi
### Thêm mới
- Bước soạn văn bản trong workflow có giới hạn có thể khai báo model dự phòng cho lỗi 429 hoặc 503 trước khi phát đầu ra. Lần chuyển được tính vào giới hạn số lượt gọi.
- Lượt chỉ xử lý văn bản chỉ gửi hướng dẫn của tác vụ. Bỏ qua dòng trống đầu câu trả lời khi kiểm tra dòng nội dung đầu tiên.

## en
### Added
- A guarded text workflow can opt an author step into a fallback model for a 429 or 503 before any output. The fallback counts toward the model stage budget.
- Text-only turns omit tool instructions. Leading blank lines are ignored when checking the first line of content.
