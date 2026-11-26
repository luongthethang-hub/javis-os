# Tiếp nhận việc Claude dở dang - 27/11/2026 00:5x

## Claude dừng ở đâu

Claude Code dừng lúc 00:22 (giờ VN) vì hết hạn mức 5 giờ, phiên `e4598612` trong `D:\AI AGENT\council-agent-manager`. Việc cuối cùng không phải CAM OS mà là **Hàng chờ việc** `D:\AI AGENT\hang-cho`:

- Đã commit `a800778` (thông báo Windows, sổ Claude tự làm, lệnh bang-tin), đã tạo lịch `CAM\HangCho-ChayVong` chạy 10 phút/lần, chạy ẩn bằng `chay-vong-an.vbs`.
- Đã đóng gói 3 gói: HC-20261127-001 (đã đóng gói), **HC-20261127-002 (lỗi)**, HC-20261127-003 (chờ, thợ javis).
- Chưa commit 2 tệp đang sửa: `cau-hinh/tho.json` (thêm thợ cam, javis) và `hang_cho/__main__.py` (sửa xuống dòng trong bang-tin).

## Vì sao HC-20261127-002 trượt 2/2 lần

Lỗi nằm ở **tiêu chí nghiệm thu của gói**, không ở thợ. Đã kiểm trên bản clone tại đúng rev ghi trong gói:

| Kiểm | Kết quả |
|---|---|
| `git apply --check` bản vá AG (`ag_G6.patch`) trên rev `6b9277a` | Đạt, áp sạch 4 tệp |
| `node --check` 2 tệp js sau khi áp | Đạt (mã thoát 0) |
| `python -m pytest tests -q` trên rev `6b9277a` **khi chưa áp gì** | **Đỏ sẵn 4 ca**: `test_lock_3a2_chat_commands`, `test_policy`, `test_step4_failover`, `test_step5_claude_allowlist` |

Gói đòi "pytest toàn bộ xanh" nhưng bộ test đã đỏ sẵn từ trước bản vá. Mọi bản nộp đều trượt, kể cả bản vá đúng. Lần 2 CAM còn nộp diff chỉ 7.513 ký tự và trượt `index.html:151` vì bản vá bị cắt, nên không có bằng chứng chất lượng thật.

## Đề xuất (cần L0 duyệt trước khi mở lại gói)

1. Đổi tiêu chí HC-002 thành: `node --check` 2 tệp js + `pytest` **trừ** 4 ca đỏ sẵn (ghi rõ mã 4 ca trong gói), hoặc vá 4 ca đỏ trước bằng một gói riêng D2.
2. Mở lại HC-002 với `mo-lai` và tăng `lan_toi_da` lên 3 (hiện 2/2 đã hết).
3. Giao HC-002 cho `ag` (Antigravity) vì đã kiểm sống ĐẠT lúc 00:4x, diff phải đủ 4 tệp.
4. HC-003 (chẩn đoán Sync_4h 0x800710E0) đang chờ thợ `javis`, tôi tự kéo bằng `nhan --tho javis`.

Không sửa gì trong repo CAM OS thật, khóa ghi `khoa-ghi:cam-os` vẫn `dang-giu`.
