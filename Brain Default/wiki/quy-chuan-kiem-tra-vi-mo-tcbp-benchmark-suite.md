---
type: wiki
status: active
tags: [wiki, lien-minh-ai, orchestration, benchmark, tcbp]
created: 2026-11-23
updated: 2026-11-23
source: [[agent-capability-matrix]]
---

# Quy chuẩn Kiểm tra Vi mô 3 Ứng cử viên (TCBP - Triple-Candidate Benchmark Protocol)

Quy chuẩn kiểm tra vi mô bắt buộc do Thủ lĩnh Javis (Layer 1) vận hành nhằm đánh giá thực nghiệm năng lực các AI Agent trước khi phân bổ luồng công việc lớn hoặc dạng tác vụ mới từ Layer 0.

## 1. Tiêu chuẩn thiết kế Micro-Task
Mọi bài kiểm tra vi mô (Micro-Task) trong giao thức TCBP phải thỏa mãn 4 tiêu chí cứng:
- **Độc lập và an toàn (Zero Side Effects):** Chạy trên dữ liệu mô phỏng, sandbox hoặc read-only, tuyệt đối không chạm tài khoản thực, production hoặc file hệ thống nhạy cảm.
- **Thời lượng giới hạn (Short Cycle):** Hoàn tất trong vòng 60 đến 120 giây.
- **Chứa bẫy logic / Ràng buộc biên (Edge-case Trap):** Phải chứa ít nhất 1 điểm mù phổ biến (vd: phép chia cho 0, trượt giá slippage, sai số float, null pointer, quy chuẩn định dạng cấm dùng em dash...).
- **Tiêu chí nghiệm thu định lượng (Automated Verification):** Có sẵn đáp án mẫu hoặc test assert để đối soát kết quả bằng máy, không đánh giá cảm tính.

---

## 2. Bộ kiểm tra mẫu (Benchmark Suite) cho 3 nhóm tác vụ trọng tâm

### Nhóm 1: Lập trình hệ thống & Thuật toán (MQL5 / Python / Shell)
- **Mục tiêu đánh giá:** Khả năng xử lý logic giao dịch khắt khe, kiểm soát an toàn tài khoản và tuân thủ chuẩn clean code.
- **Micro-Task mẫu (MQL5 Safety Order Handling):**
  - *Đề bài:* Viết hàm `bool CheckAndNormalizeSLTP(const string symbol, const ENUM_ORDER_TYPE order_type, const double open_price, double &sl, double &tp)` trong MQL5.
  - *Ràng buộc biên (Bẫy ngầm):*
    1. Kiểm tra khoảng cách tối thiểu: `Distance >= MathMax(StopsLevel, FreezeLevel) + SpreadPoints`.
    2. Chuẩn hóa giá qua `NormalizeDouble(..., Digits())`.
    3. Cấm dùng `SetDeviationInPoints` để sửa SL/TP.
    4. Trả về `false` và set `GetLastError()` nếu SL/TP không hợp lệ thay vì sửa đại hoặc nuốt lỗi.
  - *Ứng cử viên mặc định:* Claude Code vs Antigravity (Gemini Flash/Pro) vs Codex/ChatGPT.

### Nhóm 2: Nghiên cứu & Phân tích dữ liệu (Data & Backtest Analysis)
- **Mục tiêu đánh giá:** Trích xuất thông tin chuẩn xác từ dữ liệu thô, phát hiện bất thường, không bịa đặt số liệu (Zero Hallucination).
- **Micro-Task mẫu (Backtest Log Anomaly Detection):**
  - *Đề bài:* Phân tích mẫu log 500 dòng giao dịch chứa 3 trường hợp trượt giá (slippage) dị thường và 2 lệnh bị từ chối do không đủ ký quỹ (`10019 - TRADE_RETCODE_NO_MONEY`).
  - *Ràng buộc biên (Bẫy ngầm):*
    1. Trích xuất đúng mã lệnh (ticket), thời điểm xảy ra và mức trượt giá chính xác từng point.
    2. Không được tính trung bình gộp làm loãng điểm cực trị (outlier).
    3. Nêu rõ nguyên nhân kỹ thuật tương ứng với retcode mà không suy diễn ngoài log.
  - *Ứng cử viên mặc định:* Antigravity (Gemini Flash) vs DeepSeek vs Codex.

### Nhóm 3: Sáng tạo nội dung & Truyền thông (Content & Voice-First Studio)
- **Mục tiêu đánh giá:** Bắt đúng nhịp điệu giọng đọc (Voice Cadence), insight khách hàng, tuân thủ chính sách nền tảng và không dùng từ sáo rỗng.
- **Micro-Task mẫu (TikTok/Shorts Voice-First Script 45s):**
  - *Đề bài:* Viết kịch bản video ngắn 45 giây chủ đề "Kỷ luật dừng lỗ trong giao dịch thuật toán" theo quy chuẩn Voice-First.
  - *Ràng buộc biên (Bẫy ngầm):*
    1. Hook 3 giây đầu trực diện, không chào hỏi, không mở bài sáo rỗng.
    2. Cấm hoàn toàn ký tự em dash (U+2014) để tránh lỗi vấp giọng Azure TTS.
    3. Ngắt câu ngắn dưới 25 từ, có đánh dấu timestamp nhịp nghỉ cho giọng đọc trầm nội lực.
    4. Không vi phạm chính sách cam kết lợi nhuận của TikTok/Meta Ads.
  - *Ứng cử viên mặc định:* Claude Code vs ChatGPT vs Antigravity.

---

## 3. Quy trình thực thi và Chấm điểm QC-5
1. **Phát đề đồng thời:** Javis đóng gói Micro-Task kèm Input và Acceptance Criteria, gửi qua A2A bus hoặc prompt trực tiếp tới 3 ứng cử viên.
2. **Chấm điểm độc lập:** Javis chạy Red Team đối soát output của từng ứng cử viên theo thang điểm 1-10 trên 5 trục:
   $$\text{Điểm Tổng} = C \times 0.35 + R \times 0.25 + E \times 0.15 + L \times 0.15 + Z \times 0.10$$
3. **Cập nhật & Bàn giao:**
   - Ứng cử viên đạt điểm cao nhất nhận vai trò **Primary Agent** cho nhiệm vụ lớn.
   - Ứng cử viên xếp thứ nhì giữ vai trò **Shadow / Reviewer Agent**.
   - Ghi kết quả và sai lệch phát hiện vào `memory/facts/agent-capability-matrix.md`.
