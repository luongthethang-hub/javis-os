---
type: wiki
tags: [kien-truc, he-thong, watchdog, resilience, kill-switch]
created: 2026-11-24
updated: 2026-11-24
---

# Kiến trúc Cầu chì Khẩn cấp và Hard Reset Ngoại vi (Out-of-Band Kill-Switch)

## 1. Nguyên lý phân tách điều khiển (Out-of-Band Architecture)
- **Vấn đề In-Band Failure:** Khi hệ thống AI chính gặp lỗi tắc luồng (I/O block, bão hòa bộ nhớ, deadlock vòng lặp), kênh tương tác trực tiếp của bot chính bị đóng băng. Mọi chỉ thị cứu hộ gửi qua kênh in-band đều vô hiệu.
- **Giải pháp Out-of-Band:** Sử dụng một daemon quan sát độc lập, không phụ thuộc vào vòng đời của ứng dụng chính:
  - Tài nguyên cực tiểu: Daemon viết bằng Python thuần, không tải AI runtime, RAM < 15 MB.
  - Phân quyền nghiêm ngặt: Xác thực danh tính cứng (`chat_id` của chủ sở hữu) trước khi thực thi lệnh hệ thống.

## 2. Bảng điều khiển lệnh ngoại vi

| Lệnh | Mức độ | Hành động thực thi | Thời gian đáp ứng |
|---|---|---|---|
| `/status` | Giám sát | Đọc CPU, RAM, danh sách PID tiến trình AI đang chạy | < 500 ms (thực đo 151 ms) |
| `/panic` | Phanh cấp 1 | `taskkill` toàn bộ tiến trình CLI con bị treo, giữ nguyên core server | < 1 giây (thực đo 739 ms) |
| `/reset` | Phanh cấp 2 | Dọn tiến trình con + Khởi động lại Core Server (Port 7777) | < 3 giây |

## 3. Cấu hình và Tệp triển khai thực tế

- **Mã nguồn Daemon:** `Javis/scripts/emergency_watchdog.py`
- **Cấu hình độc quyền:** `Javis/bridge/watchdog_config.json` (chỉ nhận `chat_id: 1894254685`)
- **Bộ khởi chạy vòng lặp:** `Javis/scripts/run_emergency_watchdog.bat`
- **Bộ kiểm thử tự động:** `Javis/scripts/test_emergency_watchdog.py` (5/5 ca test đạt chuẩn VERIFIED_IN_SCOPE)

## 4. Liên kết tri thức
- [[ban-linh-tien-hoa-va-tu-phuc-hoi-lien-minh]]: Cơ chế tự phục hồi và bảo toàn tính liên tục của hệ thống.
- [[giao-thuc-bieu-quyet-q5-cvm]]: Cơ chế phân xử ngầm phá vỡ vòng lặp vô hạn trước khi phải dùng đến can thiệp ngoại vi.
