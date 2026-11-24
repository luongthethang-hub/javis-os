---
type: decision
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23 (f36fd2e7)
---
Cơ chế bảo mật thích ứng cho kênh Telegram dựa trên Behavioral Biometrics và Dynamic Risk Scoring:
- **Fast Path:** Khi phong cách giao tiếp (Stylometry), ngữ cảnh và khung giờ trùng khớp với hồ sơ chủ nhân, các tác vụ rủi ro thấp/trung bình được thực thi mượt mà không yêu cầu OTP.
- **Dynamic Context Challenge:** Khi phát hiện lệch hành vi hoặc câu lệnh bất thường, hệ thống tự động hạ quyền về Safe Mode (Read-Only) và kích hoạt câu hỏi bẫy dựa trên Second Brain nội bộ (tri thức không có trong chat Telegram).
- **Out-of-Band Alerting:** Gửi thông báo tức thì sang kênh phụ (Zalo/Push) khi nhận lệnh can thiệp file/hệ thống để vô hiệu hóa rủi ro xóa tin nhắn phi tang hai chiều.
- **Hard Boundary:** Tác vụ phá hủy dữ liệu hoặc hạ tầng bắt buộc xác thực vật lý (TOTP hoặc xác nhận trên Web Dashboard).

**Vì sao:** Ngăn chặn nguy cơ tài khoản Telegram bị chiếm đoạt và khai thác bí mật mà không làm cản trở việc tinh chỉnh hệ thống từ xa.
**Áp dụng:** Áp dụng cho mọi tin nhắn điều khiển từ kênh Telegram và các cổng giao tiếp từ xa của Javis OS.
