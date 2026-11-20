---
bump: patch
title: Bound opt-in sequential workflow execution
---

## vi
### Sửa lỗi
- Quy trình khai báo giới hạn chạy dừng khi chờ quá lâu, vượt số lượt/bộ công cụ hoặc sửa lặp lại cùng đầu ra. Đầu vào và trợ lý được kiểm tra trước khi gọi model.
- Khi dừng, luồng engine được đóng và lỗi được ghi vào lịch sử; mức token chỉ tính theo dữ liệu nhà cung cấp thực sự trả về.

## en
### Fixed
- Opt-in sequential workflows stop on elapsed or idle deadlines, stage/tool limits and unchanged repair outputs. Input and assistant contracts are validated before model calls.
- Stopping closes the engine stream and records a failure in run history. Token accounting uses only provider-reported usage.
