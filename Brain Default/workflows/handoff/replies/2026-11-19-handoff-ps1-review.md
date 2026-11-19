---
task_id: 2026-11-19-handoff-ps1-review
from: claude-desktop
status: done
confidence: trung binh (chua chay parser)
---

Không thấy lỗi cú pháp khi đọc `scripts/handoff.ps1`. Chưa chạy parser nên mức chắc chắn: trung bình.

Ba điểm dễ hỏng nhất:
1. Dựa vào UI Automation (control `Edit`/`Document`, nút "Gửi"/"Send"): app đổi giao diện hoặc ngôn ngữ thì script thoát mã 6 hoặc 10.
2. Cần phiên desktop mở, không khóa: `SendKeys`, chuột, Ctrl+A/V ghi đè clipboard; mất focus thì dán nhầm cửa sổ. Ngưỡng 1920x1080 viết cứng.
3. Coi là "xong" khi độ dài ổn định 18 giây, tối đa `WaitSeconds` = 180: trả lời dài bị cắt; `Substring` có thể ném lỗi nếu transcript ngắn đi.

<<<HANDOFF-END>>>
