---
type: wiki
status: active
tags: [wiki, CAM, claude-desktop, hoi-dong, van-hanh, tri-thuc, 2026-11]
created: 2026-11-26
updated: 2026-11-26
source: [[sources/Claude Desktop - Hoi dong CAM 2026-11-25.md]]
---

# Claude Desktop trong dự án CAM: nhật ký thực thi 25-26/11/2026

Bản chưng cất từ hội thoại THẬT của Claude Desktop (model `claude-opus-5-5`) trong dự án `council-agent-manager`, giai đoạn 25/11 03:39 đến 26/11 04:37. Đây là việc Claude đã làm thật, kèm số liệu tự báo, không phải kế hoạch. Nguồn: [[sources/Claude Desktop - Hoi dong CAM 2026-11-25.md]].

## 1. Đăng nhập và nối Claude/DeepSeek vào CAM
- Claude CLI bản 2.1.331 lúc đầu chưa đăng nhập (`loggedIn: false`), không có `.credentials.json`. Claude Desktop xin Sếp tự chạy `run_claude_login.bat` để tạo token dài hạn 1 năm vào Vault; nó không lách lớp kiểm soát an toàn.
- Sau khi Sếp cấp token: gọi thử đơn giản trả "ok", gọi có dùng công cụ đếm đúng 39 file `.py` trong `cam_core`.
- DeepSeek nối bằng phiên đăng nhập tài khoản sẵn có trên máy (không cần API key) qua `config/dsh_team_patch.yaml`, trả "ok" sau khoảng 4,8 giây; `ask_deepseek("17*23")` trả 391, đúng.
- Sửa lỗi `test_team_settings_file_passed`: thêm nạp `config/claude_team_settings.json` và gỡ biến `ANTHROPIC_*`/`CLAUDE_CODE_USE_*` trước khi gọi `claude`.

## 2. Tiết kiệm token: lõi luật phân tầng và bể ngữ cảnh
- Trước: mỗi việc gửi toàn bộ lõi luật ~2.488 ký tự (~830 token).
- Sau: lõi siêu nhỏ luôn gửi 450 ký tự (~150 token), cộng luật nạp theo loại việc. Đo thật bằng Claude CLI: giảm 28-70% tùy loại việc (chào hỏi -64%, toán/MQL5 -70%, sửa code -31%).
- Bể ngữ cảnh (context pools) đo thật: general 1.427 → 394 token (-72%), quant_math -73%, architecture -67%. Lưu ý: system prompt gốc của Claude Code ~34.000 token mỗi lần gọi, nên phần tiết kiệm chỉ là phần lõi.
- Ba mức chi tiết L1/L2/L3: thợ xin bản đầy đủ bằng mã `NEED <mã>.L3`, tối đa 1 vòng; giữ phiên DeepSeek bằng cách chỉ gửi hash khi lõi không đổi.

## 3. Bài học đã chốt vào CAM
- **Cấm ký tự tượng hình:** mã ngữ cảnh chỉ dùng ASCII (chữ, số, `._-`); dùng ký tự lạ làm model đếm token nhiều hơn và dễ bịa. Đã thành luật cứng, có bước kiểm báo lỗi P1.
- **Lõi luật bị cắt cụt ở 2.600 ký tự:** prompt từng mất dòng cuối, kể cả "không ghi core_immutable / không git push". Đã rút gọn để vừa đủ.
- **Cổng dữ liệu fail-closed:** adapter kiểm toàn bộ gói trước khi gửi; gói chứa dữ liệu S2/S3 thì báo lỗi, không gửi gì ra ngoài.
- **DeepSeek tự ghi file vào thư mục CAM:** DeepSeek Harness mặc định có quyền ghi thư mục khởi động, tạo ra `tests/test_api_smoke_a/b.py`; cần cảnh giác, coi output là dữ liệu không tin cậy.
- **Chuột/bàn phím ảo:** `virtual_cursor.py` gửi `PostMessageW` thẳng vào cửa sổ đích, không gọi `SetCursorPos`/`SendInput`, nên không chiếm chuột thật.

## 4. Đội săn lỗi và hội đồng
- Đội "nano" săn lỗi đọc thẳng log CAM hiện có (cam.log, logs/runs, team_traces, token_usage.db), không tạo log mới. Mỗi phát hiện kèm tên file, số dòng, logger, trace id.
- Nâng cấp: gieo lỗi giả (10 thợ đều bắt), bản đồ phủ 71 file + lộ 71 route API chưa test, bỏ phiếu 2/3 (CAM cục bộ + DeepSeek + Claude khi mana >50%).
- Bỏ phiếu chạy sau quét sâu 02:00; nhiệm vụ báo động giả tự hủy.

## 5. Kết quả cuối giai đoạn
- CAM lên v3.3.0, rồi CAM Corporation v2 (9 phòng ban, 23 nhân sự) chạy tại `http://127.0.0.1:8787/company`.
- Test tăng dần tới 257/257 đạt trong các mốc báo cáo.
- Mốc chặn: nhiều lần dính giới hạn 5 giờ của Claude (reset 19:40, 00:40, 16:20 hôm sau).

## 6. Điểm chưa xác minh (cần đối chiếu, không coi là đã chốt)
- Số test và phiên bản là Claude tự báo trong hội thoại, chưa chạy lại để xác nhận tại thời điểm ingest.
- "CAM 3.3.0 đang chạy" phụ thuộc Sếp bấm `run_cam.bat`; Claude bị lớp an toàn máy chặn tự khởi động.
- Trạng thái mana/limit của Claude Desktop tại lần đọc: đã chạm giới hạn 5 giờ, reset 16:20 (Asia/Bangkok).
