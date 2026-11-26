---
type: rule
created: 2026-11-27
updated: 2026-11-27
source: lệnh L0 26/11/2026 lúc 00:19 và 00:22 (giờ VN, ngày 27/11) trong dự án Darklord; hệ thống D:\AI AGENT\hang-cho v0.1.0
---

# Nâng cấp bắt buộc: mọi thành viên Liên minh nhận việc qua Hàng chờ giao việc

L0 ra lệnh áp dụng hàng chờ giao việc cho toàn Liên minh. Từ 27/11/2026, thành viên chỉ nhận việc cơ bắp qua hàng chờ.

## Vai trò
- Claude: cắt việc, viết gói (hướng dẫn và cách test nghiệm thu), soát. Không tự làm việc khó tốn token; việc Claude tự làm phải ghi `tu-lam`.
- CAM: tự vận hành giám sát V1-V8 (tiêu chí ở teacher-agent\tieu-chi-giam-sat.md, công cụ cam_monitor.py). Chỉ đọc khi giám sát,
  không chạy pytest trên dữ liệu thật, V8 (khối u) báo L0 không tự xử lý. Kết quả ghi Sổ Cái.
- Javis, CAM: kéo gói bằng lệnh `nhan`. Antigravity, Codex: hàng chờ tự gọi. DeepSeek: tắt tới khi có key.

## Cách nhận và nộp (chạy trong D:\AI AGENT\hang-cho)
1. `python -m hang_cho ds --trang-thai cho` xem gói chờ.
2. `python -m hang_cho nhan --tho <id>` nhận; in MA_NHAN một lần. Giữ mã, không chép vào nơi khác.
3. Làm đúng TaskPacket. Đầu ra đúng mục "Đầu ra" (thường 1 khối ```diff + 1 khối ```text).
4. `python -m hang_cho nop --goi <id> --tho <id> --ma <MA_NHAN> --tep <tệp kết quả>`. Hàng chờ tự chạy test nghiệm thu.
5. Không làm được: `tra-lai --ly-do ...`. Không im lặng giữ gói.

## Luật cứng
- Chỉ thợ có tên trong danh sách đủ điều kiện của gói mới nhận được (theo D1-D5, S0-S3, nghiệp vụ). S3 và A0 không model nào nhận.
- Không gửi key/token qua hàng chờ: gói hay kết quả có bí mật bị từ chối.
- Mã nhận dùng một lần; hết hạn làm thì mất quyền, gói về hàng cho thợ khác.
- Bàn giao liên tục (L0 00:22): đang giữ gói thì sau mỗi bước ghi tiến độ; hết token hay mất kết nối thì hạn làm tự hết và gói về hàng
  kèm ghi chú tiến độ cho người tiếp quản. Không được tùy tiện bỏ gói.
- Không tự tạo tác vụ hẹn giờ, daemon, module ngoài gói (V8). Bật lịch chạy cần L0 duyệt.
- Kết quả chỉ đóng gói khi qua test nghiệm thu; gói D3+ còn cần người soát khác hãng.

## Theo dõi
- `python -m hang_cho bang-tin --gio 24`: thợ nào nhận/nộp gì, gói đang mở, Claude tự làm gì.
- Mỗi lần nhận/nộp/đạt/trượt hiện thông báo Windows trên máy L0. Sự kiện vào Sổ Cái với khóa `hc:<id gói>`.
