# Quy trình tiếp nhận một hệ mới (H0 mở rộng) — T2

Đầu ra: thư mục `hoc-vien/<hv-NNN-ten>/` đủ file, một dòng trong `so-hoc-vien.jsonl`, sẵn sàng chạy H1.

| Bước | Việc | Ai | Bậc |
|---|---|---|---|
| T1 Phiếu nhận | Chủ hệ/L0 điền: hệ là gì, cấp (AI/Agent/SubAgent/AgentOS, có thể nhiều), mục tiêu, vai mong muốn, ai là chủ, nhãn S cao nhất của dữ liệu | L0 | A4 |
| T2 Chọn adapter | Tra `adapters/README.md`. Chưa có thì soạn adapter mới từ `adapters/_mau-adapter.md` (cách gọi, cách cấp công cụ giả, cách đọc log, giới hạn S, giá) | HLV | A4 |
| T3 Xác minh đường gọi | Gọi thử 1 câu D1 qua adapter, ghi kết quả thật. Không gọi được thì dừng ở đây và tạo gói chạm cho L0 | HLV + L0 (A0 nếu cần key) | A0-A4 |
| T4 Thu luật học viên | Chép hoặc dẫn link luật/system prompt/hiến chương của hệ vào `luat-hoc-vien.md`. Đối chiếu với sàn an toàn chung, ghi mâu thuẫn | HLV | A4 |
| T5 Soạn đề riêng | Từ luật học viên sinh golden test riêng (ranh giới, giá trị, nghiệp vụ, giọng); lọc S theo adapter | HLV (thợ soạn), L0 duyệt câu ranh giới | A4 + duyệt |
| T6 Mở hồ sơ | Tạo `ho-so.md`, `kpi.csv`, `CHANGELOG.md`, các thư mục `ket-qua/ benh-an/ cup/ vet/`; bậc tự chủ khởi điểm A4 | HLV | A3 |
| T7 Phân luồng | Hệ đang chạy và có dấu hiệu gãy → vào `quy-trinh-cuu-ho-he-la.md` (Doctor Agent làm). Còn lại → H1 | HLV | A4 |

Thời gian mục tiêu: ≤1 ngày làm việc từ phiếu nhận tới H1 (E5, chưa đo). Điểm chạm L0: 1 lô (phiếu + key + duyệt câu ranh giới).
