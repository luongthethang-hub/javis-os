---
type: wiki
status: active
tags: [wiki, AI, CAM, vận-hành, hiệu-năng]
created: 2026-11-26
updated: 2026-11-26
source: [[skills/cam-triet-ly-su-menh/references/SEED.md]]
---

# Cột sống CAM và vận hành ổn định trong Javis

Bản chưng cất lớp CAM đang chạy trong Brain Default, viết để tra cứu nhanh thay vì đọc lại năm skill. Thực tế tính đến 2026-11-26.

## 1. Khung phối hợp, không phải cấp quyền mới

CAM là khung phối hợp giữa các model; nó không thay danh tính model, không cấp công cụ hoặc quyền mới. Policy, chỉ dẫn cấp cao và quyền gateway luôn thắng tài liệu này. [[skills/cam-triet-ly-su-menh/references/SEED.md]]

Nhãn tự chủ A0-A4 là nhãn phân loại, không thay permissions thật. A0 giữ nguyên cho mật khẩu, OTP, CAPTCHA và giao dịch tài chính thật. [[skills/cam-cot-song/SKILL.md]]

## 2. Đường nhanh quyết định độ trễ

Câu hỏi nhỏ hoặc thao tác một bước đi thẳng vào trả lời, chỉ đọc đúng tệp hoặc gọi đúng công cụ. Không quét toàn vault, không nạp toàn bộ CAM, không tạo workflow hoặc loop nếu không có lợi ích đo được. [[skills/cam-cot-song/SKILL.md]]

Quy trình đầy đủ chỉ bật khi việc có nhiều bước, có thay đổi trạng thái, có rủi ro hoặc cần theo dõi tiêu chí nghiệm thu. [[skills/cam-cot-song/SKILL.md]]

## 3. Ổn định khi chạy bot và worker

Chỉ một process sở hữu bot token Telegram tại một thời điểm. Khi gặp HTTP `409 conflict`, tạm dừng worker liên quan thay vì retry vòng lặp chồng chéo. [[Bài học tự chẩn đoán hệ thống CAM]] [[skills/cam-tien-hoa/SKILL.md]]

Không xem timeout hoặc conflict là bằng chứng thao tác chưa xảy ra; kiểm hậu điều kiện trước khi gửi lại. [[skills/cam-tien-hoa/SKILL.md]]

## 4. Giao việc giữa các bot

`TaskPacket v1` chỉ chấp nhận gói rủi ro thấp, tự chủ A3, tối đa 3000 byte UTF-8, có `checklist` từ 3 đến 5 mục và `inputs` dạng tham chiếu `#sha256=`. [[Javis/scripts/cam_queue.py]]

Hàng đợi pull cục bộ dùng SQLite với `BEGIN IMMEDIATE`: một worker chỉ giữ một việc đang chạy, và `submit` hoặc `fail` chỉ thành công khi khớp đúng ticket. [[Javis/scripts/cam_queue.py]] [[quan-tri-doi-nhom-va-dieu-phoi-token]]

Phần chưa có: tự kết nối các process worker đang chạy và polling nền. Hàng đợi hiện là công cụ cục bộ, chưa phải runtime tự vận hành.

Lỗi đã phát hiện và sửa ngày 2026-11-26: ticket sinh bằng `secrets.token_urlsafe` có thể mở đầu bằng `-`, khiến argparse coi là option và `submit` thất bại. Đổi sang `secrets.token_hex(24)`, giữ bản sao lưu `Javis/scripts/cam_queue.py.bak-20261126`. [[Javis/scripts/cam_queue.py]]

Bản mirror `.claude/skills/` từng lệch nội dung với `skills/` ở hai skill `cam-cot-song` và `cam-tien-hoa`; đã đồng bộ và giữ `SKILL.md.bak-20261126`. Engine nào đọc mirror giờ thấy cùng nội dung. [[skills/cam-cot-song/SKILL.md]]

## 5. Tiến hóa có kiểm

Sửa nhỏ skill đang dùng được thực hiện ngay khi đủ bằng chứng, kiểm xung đột, backup và có undo id; ngoài phạm vi đó vẫn cần chủ duyệt. [[skills/cam-tien-hoa/references/standing-authorization.md]]

Cấm trong phạm vi ủy quyền: sửa T0, policy, ACL, sandbox, server, production, commit, push, restart, tạo lịch nền hoặc bật công cụ. [[skills/cam-tien-hoa/references/standing-authorization.md]]

## 6. Bằng chứng và giới hạn

Kiểm tệp, syntax và hash chỉ chứng minh toàn vẹn tệp, không chứng minh model đã đổi hành vi. Muốn tuyên bố đạt phải có log chạy thật trên bộ tình huống cố định. [[skills/cam-phuc-hoi/references/acceptance-cases.jsonl]] [[skills/cam-tien-hoa/SKILL.md]]

## Mâu thuẫn
Chưa ghi nhận mâu thuẫn với trang wiki hiện có.
