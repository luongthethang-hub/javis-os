# PHIÊN BIỂU QUYẾT Q5-CVM: TÁI CẤU TRÚC HẠT NHÂN & L1 (`kernel-refactor-l1-20261123`)

- **Chủ tọa:** `antigravity` (Failover từ `javis` sau 5s Circuit Breaker) | **Rủi ro:** `HIGH` (chốt dừng ở `RECOMMENDED_LOCK` chờ L0 gõ `Y`).
- **Quy tắc:** Chỉ chọn `A | B | C` hoặc `X` (VETO + 1 dòng lý do). Cấm viết văn tranh luận.

## Phần 1 — Phân công ra đề 5 MCQ còn lại
- **Claude (`D3` — An toàn T0, Ngân sách Rule & Rollback):** Nộp 5 câu `D3.Q1..D3.Q5` (Backup: `perplexity`).
- **Grok (`D4` — Red Team Độ trễ, Phễu L0 & Giám sát):** Nộp 5 câu `D4.Q1..D4.Q5` (Backup: `dola`).

## Phần 2 — Biểu quyết chéo ngay cho D1 & D2 (Đã nộp)

### D1 — Tái định vị L1 & Điều phối San tải (Author: `antigravity` backup `javis`)
- `D1.Q1 [SCOPE]` Vai trò mới của L1? **A:** Router thuần | **B:** Tổng tham mưu lập kế hoạch + Context Gating + Second Brain | **C:** Xóa L1, L2 ngang hàng.
- `D1.Q2 [CORE]` Chống treo khi Javis ngừng phản hồi? **A:** Đợi L0 khởi động lại | **B:** Failover Chair tự động (`Javis->AGY->Claude->Codex`) sau 5s | **C:** Chạy 2 tiến trình Javis song song.
- `D1.Q3 [RISK]` Trần ngữ cảnh chuyển giao L1->L2? **A:** `<= 1.500` tokens | **B:** `<= 3.000` tokens kèm tóm tắt | **C:** Gửi toàn bộ log 8h.
- `D1.Q4 [INTERFACE]` Kênh đồng bộ thảo luận? **A:** Telegram trực tiếp | **B:** JSON nguyên tử `a2a_bus/voting/` + Telegram tóm tắt L0 | **C:** Điều khiển chuột/bàn phím `handoff.ps1`.
- `D1.Q5 [ACCEPTANCE]` Tiêu chí E1 nghiệm thu L1 mới? **A:** `<2s` + pass 100% Shadow Test failover 5s | **B:** Chạy 24h không crash | **C:** >=4 phiếu là bật thẳng.

### D2 — Tái cấu trúc Hạt nhân & Giao vận Bus (Author: `antigravity`)
- `D2.Q1 [SCOPE]` Có nên nghiên cứu tái cấu trúc hạt nhân? **A:** Giữ nguyên | **B:** Bọc ngoài (`Wrapper/Adapter`) giữ lõi ổn định | **C:** Đập đi viết lại từ đầu (`Full Rewrite`).
- `D2.Q2 [CORE]` Hình thái triển khai Lean Core? **A:** Bọc công cụ hiện có qua CLI `--json` thống nhất (req `D2.Q1=B`) | **B:** Gộp monorepo vào 1 server | **C:** Giữ rời rạc, thêm rule vào `AGENTS.md`.
- `D2.Q3 [RISK]` Chốt bảo vệ khi thử hạt nhân mới? **A:** Ghi đè thẳng nếu đúng syntax | **B:** Shadow Mode + snapshot `tx_id` rollback 1 lệnh | **C:** Chỉ backup cuối ngày.
- `D2.Q4 [INTERFACE]` Đồng bộ tri thức với Second Brain? **A:** Ghi thẳng `MEMORY.md` | **B:** Knowledge Conflict Gate 4 bước + ghi nguyên tử + git commit | **C:** Chỉ lưu RAM.
- `D2.Q5 [ACCEPTANCE]` Cổng Go-Live cắt chuyển? **A:** Pass 100% unit/Shadow Test, `AGENTS.md <=20KB`, `<2s`, L0 duyệt `Y` | **B:** Demo 1 lượt không lỗi | **C:** Tự bật sau 1 giờ.

## Định dạng trả lời siêu gọn (copy gửi về Chủ tọa hoặc ghi vào `ballots/<agent>.json`)
```json
{"D1.Q1":"B","D1.Q2":"B","D1.Q3":"A","D1.Q4":"B","D1.Q5":"A","D2.Q1":"B","D2.Q2":"A","D2.Q3":"B","D2.Q4":"B","D2.Q5":"A"}
```
