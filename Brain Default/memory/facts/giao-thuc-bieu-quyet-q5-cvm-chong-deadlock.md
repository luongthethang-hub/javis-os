---
type: rule
provenance: agent
origin: antigravity-bridge
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23 (00b5f1d9)
---
Layer 0 (Lương Thế Thắng) đã duyệt chính thức ngày 23/11/2026 giao thức biểu quyết **Q5-CVM (5-Question Chained Voting Matrix)** để chấm dứt vòng lặp tranh luận vô tận và lỗi treo đơn điểm khi Javis ngừng phản hồi.

- **Cấu trúc Ma trận Kx5 (K=3..5 khía cạnh):** Mỗi thành viên phụ trách 1 khía cạnh nộp đúng 5 câu trắc nghiệm khóa 5 mắt xích nhân quả (`Q1:SCOPE -> Q2:CORE -> Q3:RISK -> Q4:INTERFACE -> Q5:ACCEPTANCE`), 3 phương án loại trừ `A/B/C` + cờ `X (VETO <= 160 ký tự)`. Trần `<= 450` tokens/bộ.
- **Chống treo & Kế vị Chủ tọa (5s Circuit Breaker):** Thứ tự kế vị tự động `Javis -> Antigravity -> Claude -> Codex`. Quá `5s` không `ACK` -> tự động chuyển Chủ tọa và giao khía cạnh sang `Backup Owner`.
- **Trần thời gian cứng O(1) vòng (`<= 155s`):** `P0(10s) -> P1(60s) -> P2(45s) -> P3(20s)` (+1 vòng vá duy nhất `P3b 30s`). Đạt Quorum `>= 60%` active và `>= 3` phiếu hoặc hết TTL thì chốt ngay; bot im lặng tự gán `ABSTAIN`.
- **Nhất quán chuỗi, Phá hòa & An toàn T0:** Ưu tiên `Q1 > Q2 > Q3 > Q4 > Q5`; phá hòa theo `Owner(+0.5) -> Audit Monitor (Claude/Perplexity) -> Layer 0`; rủi ro `HIGH/CRITICAL` dừng tại `RECOMMENDED_LOCK` chờ L0 duyệt `Y`.
- **Hạ tầng thực thi:** Động cơ Python tại `D:\AI AGENT\q5-voting-engine` (`q5_vote.py`, `run_q5_voting.bat`), tầng dữ liệu nguyên tử tại `memory/a2a_bus/voting/<task_id>/` (1 agent = 1 file JSON). Đã qua 10/10 unit & Shadow Test (`pytest`). [[wiki/giao-thuc-bieu-quyet-q5-cvm]]

## 2. Quy chuẩn Tinh chỉnh Vận hành Thực tế (Duyệt 23/11/2026)
- **Cô lập kênh Telegram (100% Background Execution):** Toàn bộ các pha biểu quyết P0-P3 chạy hoàn toàn ngầm tại tệp tin `memory/a2a_bus/voting/<task_id>/`. Tuyệt đối cấm các bot gửi câu hỏi lẻ, tranh luận hoặc phiếu bầu con lên kênh Telegram gây spam.
- **Báo cáo Chốt gọn 1 trang (Executive Summary Gate):** Sau khi động cơ chốt kết quả, chỉ duy nhất bot Chủ tọa xuất 1 bản tóm tắt <= 200 từ lên kênh giao tiếp: `Kết luận chốt -> Luận điểm cốt lõi -> Trạng thái (APPROVED / RECOMMENDED_LOCK chờ L0 duyệt Y)`.
