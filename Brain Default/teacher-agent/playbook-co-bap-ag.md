# Playbook cơ bắp cho Antigravity (AG) - v1, 26/11/2026

Lệnh L0 (22:53): AG làm việc cơ bắp; Claude chỉ viết TaskPacket ngắn và soát diff/kết quả test.
Đính kèm playbook này vào MỌI gói giao AG.

## 1. Mẫu TaskPacket (Claude viết, tối đa ~40 dòng)

```
TP-<số> | nhánh: refactor/kernel-20261126 | repo: D:\AI AGENT\council-agent-manager
Mục tiêu: <1 câu>
Phạm vi được sửa: <danh sách file>. Cấm sửa mọi file khác.
Ngữ cảnh: <đoạn mã liên quan, có số dòng>
Tiêu chí nghiệm thu: <test nào phải đỏ trước, xanh sau; lệnh kiểm>
Đầu ra: MỘT khối ```diff unified (đường dẫn a/... b/... tương đối gốc repo) + MỘT khối ```text tự kiểm. Không gì khác.
```

## 2. Luật cơ bắp (không ngoại lệ)

1. Chỉ trả bản vá dạng văn bản. Không tự ghi vào repo thật, không commit, không chạy CAM thật. Claude áp bản vá trên bản sao, chạy test, rồi mới commit.
2. Chỉ sửa file trong "Phạm vi được sửa". Cần sửa thêm file khác thì ghi vào mục tự kiểm, không tự sửa.
3. Không tạo module, endpoint, tác vụ hẹn giờ, script nền, file tài liệu mới nếu gói không yêu cầu (luật V8: thứ mọc ngoài kế hoạch là khối u).
4. Không đụng `vault/`, `brains/`, `config/accounts_pool.json`, `policy/`, `logs/`, `approvals/`, `backups/`. Không in hay chép key/token.
5. Mỗi thay đổi hành vi phải kèm test. Test dùng `tmp_path`, không dùng đường dẫn thật, không gọi mạng thật, không gọi Telegram API thật.
6. Chặn là chặn ở gốc: không chạy lệnh qua shell (`powershell -Command`, `shell=True`, `create_subprocess_shell`). Không vá bằng cách thêm ký tự vào danh sách đen.
7. Không viết "đã kiểm chứng", "VERIFIED", "100%" khi chưa chạy. Chưa chạy thì ghi "chưa chạy".
8. Bản vá phải áp được bằng `git apply --check` trên HEAD đã nêu: đúng ngữ cảnh, đúng khoảng trắng, xuống dòng LF.

## 3. Checklist tự kiểm (AG điền vào khối ```text)

```
[ ] Chỉ sửa file trong phạm vi: <liệt kê file đã sửa>
[ ] Không thêm module/endpoint/tác vụ/script mới ngoài gói
[ ] Có test cho mỗi thay đổi hành vi: <tên test>
[ ] Test không ghi dữ liệu thật, không gọi mạng
[ ] Không có shell=True / powershell -Command / create_subprocess_shell mới
[ ] Những gì CHƯA làm hoặc CHƯA chắc: <ghi rõ>
```

## 4. Claude soát gì (tốn ít token)

- `git apply --check` trên bản sao; `pytest tests -q -p no:cacheprovider` toàn bộ; test tái hiện của gói đỏ trước, xanh sau.
- Đọc diff, không đọc lại cả file. Lệch luật thì trả về AG kèm 1-3 dòng lý do, tối đa 2 vòng; vòng 3 Claude tự sửa hoặc báo L0.
- Đạt thì commit trên nhánh, ghi Sổ Cái, cập nhật sổ vận hành.
