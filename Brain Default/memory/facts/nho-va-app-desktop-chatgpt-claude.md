---
type: preference
created: 2026-11-19
updated: 2026-11-19
source: chat 2026-11-19 (4f619b60)
---
Chủ muốn Javis có thói quen nhờ vả app desktop: khi nhận yêu cầu qua Telegram mà Javis không xử lý được, chuyển nguyên nội dung sang ChatGPT Desktop hoặc Claude Desktop để app đó tìm hướng xử lý. Lý do chủ nêu: dùng gói desktop tiết kiệm token hơn mà chất lượng vẫn tốt.

**Đã dựng (kiểm chứng thật 19/11/2026):**
- Script `C:\Users\Admin\.codex\javis-guard\handoff.ps1` (bản trong brain: `Javis/scripts/handoff.ps1`), dùng chung cho cả 2 app, có `-App claude|chatgpt`, `-Text` hoặc `-PromptFile`, `-WaitSeconds`. Script tự: đưa cửa sổ lệch ngoài màn hình về 60,40, focus, xoá ô soạn, dán, so khớp nội dung, bấm nút Gửi (rồi Enter, rồi bấm chuột), chờ transcript ổn định, in phần trả lời mới và ghi ra `handoff-<app>-last.txt`.
- Đã chạy thật với Claude Desktop 3 lần: prompt 405 ký tự trả lời trong 61 giây; prompt 445 ký tự (nhờ đọc file PowerShell) trả lời trong 55 giây; đọc được đủ nội dung.
- Rule "handoff sang app desktop, chạy luôn không hỏi lại" đã ghi vào `C:\Users\Admin\.codex\AGENTS.md` và bản mẫu `AGENTS.template.md` của guard, nên plugin cập nhật vẫn khôi phục được.
- Skill `skills/chuyen-viec-sang-app-desktop/SKILL.md` giữ cách dùng, mã thoát và bảng chia việc.

**Giới hạn đo được:**
- ChatGPT Desktop (`OpenAI.Codex` 26.1111.2228) đang cạn hạn mức "Codex và Công việc", mốc đặt lại 20:26 ngày 17/12/2026, nên chưa nghiệm thu được chiều này; ô soạn nhận chữ nhưng không gửi.
- Claude Desktop báo đã dùng hơn 90% hạn mức 5 giờ (đặt lại 5:40). Đây là hạn mức gói, không phải token API.
- `codex exec` trên CLI trả về đúng lỗi hết hạn mức; `claude -p` trả về "Not logged in". Nên đường CLI không thay thế được app desktop.
- Cách này cần phiên desktop đang mở, không khoá màn hình; và nó điều khiển chuột bàn phím thật nên cửa sổ sẽ nhảy lên trước mặt người dùng.

**Áp dụng:** Ưu tiên làm tại Javis nếu Javis có tool. Chỉ handoff khi bị chặn (hết hạn mức, thiếu năng lực, lỗi cài đặt) hoặc khi việc cần một tính năng riêng của app. Chọn Claude cho phân tích/code/tài liệu dài, ChatGPT cho ảnh/tra web/phản biện chéo. Luôn nói rõ đã chuyển gì, app nào, và kết quả đọc về được bao nhiêu, không nói chung là "đã nhờ xong".
