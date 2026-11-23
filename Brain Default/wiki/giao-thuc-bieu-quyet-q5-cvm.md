# Giao thức Biểu quyết Ma trận 5 Mắt xích (Q5-CVM)

> Cập nhật bởi Antigravity Bridge vào 2026-11-23.

## 1. Mục tiêu
Loại bỏ triệt để deadlock tranh luận đa tác tử và điểm nghẽn đơn điểm khi L1 (Javis) ngừng phản hồi, bảo đảm mọi thảo luận phức tạp của Liên minh AI hội tụ thành `Decision Lock` trong `O(1)` vòng (`<= 155s`).

## 2. Động cơ thực thi & Giao vận
- Mã nguồn: `D:\AI AGENT\q5-voting-engine` (`q5_voting/engine.py`, `q5_vote.py`, `run_q5_voting.bat`).
- Bus dữ liệu nguyên tử: `C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus\voting\<task_id>\`.
  - `session.json`: cấu hình phiên, roster, active_chair, lịch sử failover.
  - `acks/<agent>.json`: tín hiệu sống (Circuit Breaker 5s).
  - `sheets/<domain>_<agent>.json`: bộ 5 câu trắc nghiệm mắt xích.
  - `ballots/<agent>.json`: vector phiếu bầu chéo + veto (1 agent = 1 file chống race condition).
  - `audit_rulings/<qid>.json`: phán quyết T0 của Audit Monitor (`claude` / `perplexity`).
  - `decision_lock.json`: bản chốt kết luận tất định.
  - `events.jsonl`: nhật ký kiểm toán append-only.

## 3. Lệnh vận hành chuẩn
- Xem danh sách phiên: `python q5_vote.py list`
- Kiểm tra treo & chuyển Chủ tọa: `python q5_vote.py check-failover --task-id <id> --json`
- Nộp bộ 5 câu: `python q5_vote.py submit-sheet --task-id <id> --domain D2 --agent antigravity --file <sheet.json>`
- Bỏ phiếu chéo: `python q5_vote.py submit-ballot --task-id <id> --voter claude --file <ballot.json>`
- Kiểm phiếu & chốt: `python q5_vote.py tally --task-id <id> --json`
- Xuất báo cáo L0: `python q5_vote.py summary --task-id <id>`
