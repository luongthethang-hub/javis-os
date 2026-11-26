# BÀN GIAO cho dự án CLAUDE - Darklord (26/11/2026 ~17:00)

Nguồn: toàn bộ cuộc trò chuyện chính giữa L0 (Thắng Lee) và Claude (Opus 5.5, phiên điều phối) từ 25/11 21:32 đến 26/11 16:55. L0 yêu cầu chuyển toàn bộ nội dung sang Darklord kèm lời nhắn "đã bàn giao".
Mọi số liệu dưới đây là theo báo cáo của Doctor Agent (E2) và chấm điểm của Teacher (E3), trừ khi ghi khác.

## 1. Những gì đã được tạo
| Thứ | Nơi | Ghi chú |
|---|---|---|
| Plugin "cam" v1.1.0 (8 skill CAM tiếng Anh: cam-seed, charter, backbone, soul, task matrix, routing, recovery, evolution) | Đã gửi L0 file cam.plugin | v1.1.0 đồng bộ bản tài khoản 26/11, vá xung đột R=3, S3, V=0, cổng S2 khác hãng; CHANGELOG có CUP-20261126-01 |
| Dự án claude.ai "Claude - Teacher Agent" (chan_014CnuGJco7pyBa6CiWRBSMs) | claude.ai/code/project/... | Huấn luyện viên ĐA HỆ: luật HLV tách luật học viên, hồ sơ học viên, 3 lớp (lõi/adapter/tinh chỉnh), vòng H0-H7, cứu hộ R0-R6, cổng chất lượng + sổ bài học, ranh giới với Doctor. Kế hoạch v0.1.0 (29 file nền teacher/), L0 duyệt lô A kèm 4 sửa -> v0.1.1 |
| Dự án "Claude - Doctor Agent" (đổi tên từ CAM's hero, chan_01JVAmybgMdL37gHW1jGSN7q) | claude.ai/code/project/... | Bác sĩ cứu hộ đa hệ, nơi DUY NHẤT sửa code; bệnh nhân hiện tại CAM OS; chế độ cứu hộ BẬT; tiêu chí giám sát V1-V8 |
| Nhóm Javis "Hội đồng Huấn luyện - Teacher Agent" (tm_398ab42dc2571a64) | Javis | 8 trợ lý: codex, antigravity, shopdonk-* (deepseek, gemini, grok, luna, sol, sonnet). Lệnh dispatch từ phiên ngoài bị Javis chặn (không có danh tính) |
| Vault Javis teacher-agent/ | Vault Javis (có git) | bai-hoc.jsonl (7 bài học), benh-an/cam-os-20261126.md, bang-diem/*.md, tieu-chi-giam-sat.md (V1-V8), ux-khung-chat.md, nguon-shopdonk.md, file này |

## 2. Luật L0 đã ban hành trong phiên
1. Giao việc trước, làm sau; không ôm việc (bài học 25/11).
2. Cổng chất lượng cho MỌI model: tiêu chí nghiệm thu cố định trước khi giao; code qua test trước khi nộp; kiểm chéo khác hãng; XONG khác ĐẠT; lỗi lặp 2 lần thì hạ vai; L0 là người nghiệm thu cuối, nhận bản đánh giá (bài học DeepSeek code cẩu thả).
3. Giám sát phải có tiêu chí cụ thể, mang tính hệ thống, nếu không sẽ lan man thành khối u -> bộ V1-V8 (V8 = khối u: thứ mọc ngoài kế hoạch).
4. Báo cáo bằng điểm /100.
5. Thiết kế theo cách người dùng thật sự dùng; không làm thứ không ai dùng (chuẩn ux-khung-chat.md).
6. Dự án CAM Company / CAM Corporation đã bị L0 dừng hẳn.
7. (Lệnh cấm can thiệp Darklord ban hành 07:34; L0 tự mở riêng cho lần bàn giao này lúc 16:55.)

## 3. CAM OS - bệnh án và điều trị
Nguyên nhân gốc "càng sửa càng hỏng": popup Hội đồng v3.2.0 cho Claude + DeepSeek tự ghi code CAM 13 lần (25/11 11:04-11:44); bộ test cũ ghi đè brains/ và config/ thật; không git; không test bật CAM thật; 3 bên sửa chồng; DeepSeek ghi đè file cấu hình.
Lỗi kết nối: 77% do 6 agent bật mà không có key + failover dồn. Thiếu quyền: quyền viết cứng, rollback xóa quyền, Claude headless không allowlist.

Đã chữa (mỗi bước 1 commit, test + smoke + CAM thật + đo V1-V8):
- P0 git (e0b1c6f), P1 smoke test (5097e87), bước 0 test cô lập (86d2c8c), 1 file chính sách (148ceae), 2 lỗi tiếng Việt + retry (a89f27f)
- 3a khóa 4 đường tự chạy lệnh/tự sửa mã + hàng chờ duyệt cam_approve.py có cổng bàn phím (5 commit)
- giám sát V1-V8 cam_monitor.py (ae491ee), việc tồn docs (3b532ec), bước 3 (7acd69e), 4 (9948355), 5 (500ac7a), 7 (c8f0f53)
- Dọn CAM Company: ẩn 16 thông báo, hủy 2 đơn chờ, cất 23 tệp + 1 ký ức vào archive/cam-company-20261126/ (4013af6), 132 test
- Roster do L0 sửa 12:09 đã commit (d6ef938), V8 gốc (d3c1b9d)
Bước 6 (cổng S) dừng đúng luật: v3.1.0 không có cổng S; L0 đã duyệt thêm cam_core/sgate.py, làm sau soát khác hãng, bắt buộc trước khi bật agent thứ 2.

Điểm: CAM 24 (sáng) -> 71 (12:00) -> 80 (12:15). Hệ huấn luyện 51 -> 59. V1-V6, V8 xanh; V7 (chi phí) vàng.

## 4. Đang chờ / việc mở (tại 12:35, chưa kiểm lại sau đó)
Cần L0 quyết:
- prop_5e5e1f1e (đề xuất tiến hóa tự sinh từ log bản mã đã gỡ): Doctor KHUYÊN TỪ CHỐI (ghi ký ức "đã nghiệm thu" rỗng; nguy cơ BootGuard trỏ vào snapshot đã bị xóa).
- V7 relay: Claude trong CAM gọi qua relay (nhiều khả năng apikey.fan, tính phí theo token, model mặc định claude-sonnet-4-5-20250929) thay vì gói Pro/Max qua CLI; CLI báo chưa đăng nhập và đang trỏ model "gpt-6.2-sol". L0 cần chọn: cho Doctor đọc tên máy chủ relay (không đọc key) và giữ relay hay chuyển sang CLI.
Đang làm/xếp hàng trong Doctor:
- U0 (chỉ đọc): đo thói quen dùng chat 7 ngày + kiểm khung chat theo ux-khung-chat.md.
- Chưng cất toàn bộ góp ý L0 (owner_feedback.db...) thành bảng + backlog + cách học từ góp ý an toàn: luồng báo "All 6 steps done", L0 chưa đọc.
- U1 khung chat: Enter gửi / Shift+Enter xuống dòng / không gửi nhầm khi gõ tiếng Việt; tự giãn + giữ nháp; dán ảnh Ctrl+V, kéo thả; Copy từng tin, khối code, nhiều tin, toàn bộ, xuất .md.
- V7 bộ đếm chi phí theo ngày; cổng S sgate.py.
- Soát khác hãng (luồng "Kiểm chéo khác hãng thiết kế CAM"): Codex đang soát; DeepSeek (dsh) chờ L0 nhập key ở trang Models của dsh; ShopDonk (Luna, Grok) chờ L0 đặt biến SHOPDONK_API_KEY.
Việc L0 tự làm (A0):
- Tắt/bật tác vụ CAM_AITEP_Alliance_Sync_4h (đang BẬT; đề xuất tắt trong lúc chữa).
- Key DeepSeek cho dsh; biến SHOPDONK_API_KEY.
- Đổi key ShopDonk: key cũ nằm nguyên văn trong memory/conversations/2026-11-25.md của Javis (vault có git). L0 chọn "để sau". Cách đổi không gián đoạn: tạo key mới -> nhập Javis -> setx -> hủy key cũ.
- Bật "Auto memory" cho Doctor Agent: chưa quyết.

## 5. Nguồn model
- ShopDonk (OpenAI Compatible, nối trong Javis 25/11): 120 req/phút, 5 luồng dùng chung; 6 model: gpt-6-luna, gpt-5.6-sol, grok-4.7, deepseek-v4.1-flash, gemini-flash-3.8-high (3/5), claude-sonnet-4-6 (không tool call). Vai: Luna + Grok soát khác hãng, Sol viết/chấm test, DeepSeek tóm log, Gemini chỉ nháp.
- apikey.fan: relay trả phí (Claude/OpenAI), key trong vault CAM (DPAPI).
- Codex CLI + DeepSeek harness (dsh) trả phí; Grok gói riêng L0 không mua.
- Giá đã kiểm 26/11: Claude Opus 5.5 4/20 USD/MTok, Sonnet 5.5 2/10, Haiku 5.5 0,10/0,50 (≤100K); DeepSeek V4-Pro 0,66/1,98 thấp điểm, V4.1-Flash 0,15/0,60; cao điểm 08-11h, 13-17h VN T2-T6 trừ lễ TQ.

## 6. Bài học (teacher-agent/bai-hoc.jsonl)
GT-PHOIHOP-001 ôm việc · GT-CODE-001..003 DeepSeek cẩu thả · GT-CAMOS-001/002 hai luồng sửa, test xanh nhưng hỏng · GT-PHOIHOP-002 giao trùng Kanban không đường nhận kết quả · GT-TEST-ISO-001 test ghi dữ liệu thật · GT-SELFMOD-001 hệ tự sửa chính nó · GT-V8-001 dự án đã bỏ vẫn sinh thông báo.

## 7. Việc định kỳ
Không có scheduled task định kỳ nào được bật. Các lời nhắc một lần của phiên điều phối đã chạy xong.
