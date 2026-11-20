# Nhật ký triển khai AI Company

## 19/11/2026 - Giới hạn chạy và phân tách nghiệp vụ

### Mã nguồn và cấu hình

- Thêm `server/execution_guard.py`, tích hợp vào entry point workflow tuần tự có `execution_guard`. Kiểm tra agent, Task Card, quyền công cụ khai báo và số lượt tối thiểu trước khi gọi model.
- Giới hạn thời gian tổng, thời gian chờ sự kiện, số bước gọi model, số tool call, token nhà cung cấp báo cáo và kích thước đầu ra. Chặn bản sửa giống hệt đầu ra cũ. Lỗi adapter được chuyển thành lỗi kết thúc.
- Đóng luồng engine khi hủy hoặc guard dừng, ghi lỗi vào lịch sử thay vì đánh dấu xong.
- Thêm marker `execution_guard_version` và timeout team vào `/health` cho yêu cầu nội bộ/đã xác thực.
- `.env`: team trả lời 300 giây, bước làm việc 600 giây, background 900 giây; first response 180 giây, idle 240 giây, tool 600 giây; API owner tối đa 60 vòng tool, khách 30; team có 2 slot CLI/API, 2 team đồng thời, 1 việc mỗi team và 1 tool step mỗi thư mục. Đây là ngưỡng vận hành ban đầu.
- Các giới hạn nằm trong `.env` và marker mới chỉ có hiệu lực sau khi server nạp lại. Script một lần `tools/activate-local-execution-guard.ps1` chờ phiên hiện tại và các CLI khác của Javis kết thúc, rồi khởi động lại và kiểm `/health`. Script có thời hạn 30 phút; không ép ngắt việc khác.

### Brain và mã hoàn tác

- #1: thay workflow content bằng hai bước tác giả/biên tập, reviewer gắn ở tác giả. Lượt sạch có ba lời gọi ở cấp workflow; tối đa một lượt sửa rồi rà lại. Chỉ chữ, chưa đăng.
- #2: thêm workflow phát triển EA, tách khỏi nghiên cứu thị trường. Đầu vào JSON Task Card.
- #3 đến #6: thử pin bốn vai sang Codex; smoke thực tế không đạt. Đã hoàn tác qua #10 đến #13, không giữ các pin thử thất bại.
- #7 và #14: skill vận hành ổn định; #8 và #15: gắn định tuyến và handoff desktop vào điều phối.
- #9: thêm guard cho workflow nghiên cứu thị trường hiện có.
- Mọi workflow nghiệp vụ trên đang tắt. Không tạo loop/schedule; không mở MT5, không đăng bài, không đặt lệnh hoặc chi tiền.

### Kết quả kiểm chứng

- 19 kiểm thử guard thuần và 4 kiểm thử qua entry point workflow thật dùng engine giả đã đạt. Các tình huống gồm timeout, hủy engine, thiếu agent/Task Card, sai quyền tool, vượt hạn, bản sửa không tiến triển, lỗi adapter và ghi lịch sử.
- Năm bộ kiểm thử workflow hiện có về model/reasoning, tài khoản, hub, giới hạn Codex và chat cũng đạt. Tổng cộng bảy file kiểm thử đạt.
- `py_compile`, kiểm định changelog fragment và `git diff --check` đạt.
- Claude CLI: `loggedIn: false`, `authMethod: none`.
- Codex login status exit 0, nhưng gọi thật `gpt-6.2-sol` và một kiểm tra dự phòng `gpt-6.1-sol` đều nhận `503 Service Unavailable: No compatible account is available for this model` tại gateway cục bộ. Không coi đăng nhập hoặc model cache là bằng chứng model chạy được. Đã dừng thử thêm.
- Workflow content CLI run `ec6456d6cb3c47b3b7a1eaf0dc727606` dừng ở tác giả, không gọi reviewer. Chi phí/token của các request thất bại chưa xác định.
- Handoff ban đầu lỗi `ERROR: khong tim thay cua so claude`. Đã xác định package Claude có trên máy, mở app và gửi lại thành công. Claude Desktop trả bản nháp content; đầu ra đã đọc và lưu tại `content-lai-xe-ban-nhap.md`. Đây là tác giả và tự rà trong một app, chưa phải kiểm chứng chéo model hay nghiệm thu workflow CLI.
- GitHub chưa kết nối; công cụ `javis_improve op=source` trả lỗi tương ứng. Các thay đổi nguồn chỉ ở nhánh cục bộ `feat/ai-company-reliability-local-20261119`, chưa commit/PR/merge/phát hành.

### Giới hạn và công việc còn phụ thuộc

- Chưa có cơ chế đo tiến bộ ngữ nghĩa hoặc trần tiền USD chính xác. Token chỉ được tính khi engine báo usage, có thể báo sau khi request đã phát sinh chi phí; số stage không bao quát retry nội bộ SDK/provider.
- Lịch sử hiện có lưu một phần đầu ra mỗi bước (bị cắt theo trần của store). Resume tự động đầy đủ cho luồng tuần tự chưa được triển khai. Không được dùng lịch sử bị cắt như checkpoint mã nguồn hoàn chỉnh.
- Chưa có provider CLI chạy thật thành công nên chưa bật tự động. Tuyến desktop đã chạy một mẫu, vẫn cần phiên desktop mở và không phải backend chạy nền liên tục.
- Cần source EA, build/môi trường tách biệt và tiêu chí chấp nhận để compile/regression. Cần dữ liệu thị trường/offer thật trước khi mở rộng các luồng còn lại.

### Hoàn tác

- Brain: dùng `javis_improve op=undo` theo thứ tự ngược #15, #14, #9, #8, #7, #2, #1 khi chủ yêu cầu; #3 đến #6 đã được hoàn tác.
- Nguồn và `.env`: bản trước thay đổi nằm trong `C:\Users\Admin\AppData\Local\JavisOS\backups\ai-company-20261119`. Chỉ phục hồi khi hash bản hiện tại khớp manifest bản sau chỉnh sửa để không ghi đè công việc mới hơn. Các file mới có thể để nguyên khi gỡ import/tích hợp; xóa file cần yêu cầu riêng.
- Không dùng `git reset` hoặc `git clean`: checkout đã có thay đổi khác trước phiên này.

Trạng thái kích hoạt được ghi riêng trong `activation-status.json`. Chỉ `status: activated` kèm marker/timeouts đúng mới là bằng chứng server đang nạp cấu hình mới.

Đã khởi động worker kích hoạt PID 16584, chờ phiên CLI PID 21416 kết thúc. Quan sát ban đầu: `status: waiting_for_turn`. Công cụ `javis_job op=list` trả `ERROR: theo dõi việc chạy nền chưa hỗ trợ Windows`; vì vậy không hứa có thông báo tự động từ job tracker. Xem file trạng thái để xác nhận kết quả worker.
