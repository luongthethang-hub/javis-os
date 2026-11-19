---
name: Chuyển việc sang app desktop
description: "Đẩy việc bị chặn sang ChatGPT Desktop hoặc Claude Desktop, gửi prompt và đọc trả lời tự động."
group: AI
---

# Chuyển việc sang app desktop (ChatGPT / Claude)

## Khi nào dùng

- Người dùng nhắn qua Telegram mà yêu cầu bị chặn: hết hạn mức model, thiếu tool, lỗi cài đặt hệ thống không tự sửa được, cần một app có tính năng riêng (tạo ảnh, duyệt web, đọc file lớn).
- Chủ dặn nhờ 2 app desktop để tiết kiệm token: việc nặng nhưng không cần Javis tự chạy lại nhiều lần thì đẩy sang đó rồi lấy kết quả về.
- KHÔNG dùng cho: việc cần ghi file trong brain, gọi tool Javis, chạy lệnh trên máy. Mấy việc đó làm ở Javis rẻ và chắc hơn.

## Chuẩn bị

- App đích phải đang chạy và đã đăng nhập: `ChatGPT` (Appx `OpenAI.Codex`) hoặc `claude` (`Anthropic.Claude`).
- Kiểm tra nhanh: `javis_app_list` với filter `chatgpt` / `claude`. Không thấy trong `running` thì mở bằng `javis_app_open`.
- Script `handoff.ps1` nằm ở `C:\Users\Admin\JavisOS\brains\Brain Default\Javis\scripts\handoff.ps1` (bản sao cho Codex: `C:\Users\Admin\.codex\javis-guard\handoff.ps1`).

## Cách chạy

Prompt ngắn thì truyền thẳng:

```
powershell -NoProfile -ExecutionPolicy Bypass -File "<đường dẫn>\handoff.ps1" -App claude -Text "<prompt>" -WaitSeconds 180
```

Prompt dài hoặc nhiều dòng thì ghi ra file UTF-8 rồi trỏ vào, tránh vỡ dấu nháy:

```
powershell -NoProfile -ExecutionPolicy Bypass -File "<đường dẫn>\handoff.ps1" -App chatgpt -PromptFile "Javis/tmp/handoff-prompt.txt" -WaitSeconds 300
```

Script làm đúng thứ tự: đưa cửa sổ vào vùng nhìn thấy (nếu nó đang nằm lệch ngoài màn hình), dồn lên trước, xoá sạch ô soạn, dán nội dung, kiểm tra ô soạn khớp từng ký tự, bấm nút Gửi (không được thì Enter, không được nữa thì bấm chuột vào nút), rồi chờ văn bản trong cửa sổ ngừng thay đổi và in phần trả lời mới ra.

Mã thoát: `0` xong, `3` không thấy cửa sổ, `4` không đưa được cửa sổ lên trước, `5` không có nội dung, `6` không thấy ô soạn, `7` ô soạn không nhận nội dung, `9` không xoá sạch được ô soạn cũ, `10` gửi không được. Gặp mã khác 0 thì đọc dòng `ERROR:` cuối và báo đúng nội dung đó, không đoán.

Phần trả lời cũng được ghi ra `Javis/scripts/handoff-<app>-last.txt` để đọc lại nếu đầu ra bị cắt.

## Chia việc app nào

| Việc | Chọn |
|---|---|
| Phân tích có cấu trúc, đọc tài liệu dài, viết/refactor code, soạn tài liệu dài | `claude` |
| Tạo và sửa ảnh, tra web, phản biện chéo bằng một model khác | `chatgpt` |
| Cần kết quả quay về ngay trong chat Telegram | app nào cũng được, script đọc trả lời trực tiếp |
| Việc phải dùng tool của Javis hoặc ghi file trong brain | không chuyển, làm tại Javis |

## Bẫy

- Cửa sổ app hay bị Windows đẩy ra toạ độ âm (đo được `L=-1085 T=194`). Script tự `MoveWindow` về 60,40; nếu người dùng đang nhìn màn hình thì việc này sẽ nhảy cửa sổ của họ, nên báo trước khi chuyển.
- Ô soạn thảo của Claude Desktop đôi khi còn sót ký tự xuống dòng cũ, `Trim()` mới là 0. Script đã xử lý, đừng tự thay bằng so sánh độ dài thuần.
- ChatGPT Desktop khi tài khoản hết hạn mức thì ô soạn vẫn nhận chữ nhưng nút Gửi bị `enabled=False`; script báo `exit 10`. Lúc đó nói rõ là app đích đang hết hạn mức kèm mốc reset, đừng nói chung là "không gửi được".
- Phải có phiên desktop đang đăng nhập và màn hình không khoá. Máy chạy SSH không có phiên desktop thì cách này không dùng được.
- Chỉ gửi nội dung do chủ đặt. Không tự gửi tin đại diện ra bên thứ ba.

## Kiểm chứng

- Đã chạy thật 19/11/2026: Claude Desktop nhận prompt 405 ký tự, trả lời trong 61 giây, script đọc về đủ nội dung.
- Cùng ngày: `codex exec` và `claude -p` trên CLI đều trả về hết hạn mức hoặc chưa đăng nhập, nên đường CLI không thay thế được app desktop trong trường hợp này.
