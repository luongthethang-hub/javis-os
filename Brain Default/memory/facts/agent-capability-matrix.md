---
type: system
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23
---

# Ma trận Năng lực Liên minh AI (Alliance Agent Capability Matrix)

Ma trận năng lực thực chứng dùng cho định tuyến tác vụ tự động và giao việc của Thủ lĩnh Javis (Layer 1) dưới sự chỉ đạo của Layer 0 (Lương Thế Thắng). Cập nhật theo giao thức TCBP (Triple-Candidate Benchmark Protocol).

## 1. Thang đo định lượng 5 trục (QC-5)
- **C (Correctness):** 1-10. Tỷ lệ đáp ứng chính xác tiêu chí nghiệm thu không cần can thiệp sửa đổi.
- **R (Robustness):** 1-10. Khả năng tự phát hiện bẫy logic, bắt ngoại lệ runtime và bao phủ edge cases.
- **E (Efficiency):** 1-10. Tối ưu chi phí token/USD trên một đơn vị tác vụ hoàn thành.
- **L (Latency):** 1-10. Tốc độ phản hồi và thời gian hoàn tất chu kỳ xử lý (10 = nhanh nhất).
- **Z (Zero-Fluff):** 1-10. Kỷ luật tuân thủ cấu trúc, không code placeholder, không văn phong xã giao thừa.

## 2. Bảng đối soát năng lực thực chứng

| Agent / Model | C | R | E | L | Z | Điểm mạnh thực chứng | Điểm yếu & Vùng cấm | Định tuyến tối ưu |
|---|---|---|---|---|---|---|---|---|
| **Claude Code / Desktop** (Sonnet 3.7 / Opus) | 9.5 | 9.5 | 6.5 | 6.5 | 9.5 | Kiến trúc đa file phức tạp, refactor an toàn, tuân thủ rule tuyệt đối, bắt lỗi biên tinh vi. | Chi phí token cao; latency cao hơn mô hình flash; cấm dùng cho quét dữ liệu thô hàng triệu token. | Thiết kế kiến trúc, audit an toàn, debug logic ngầm, viết core engine. |
| **Antigravity CLI / IDE** (Gemini 2.5 Flash / Pro) | 9.0 | 8.5 | 9.5 | 9.5 | 9.0 | Context window siêu lớn (1M-2M tokens), tốc độ xử lý nhanh, chi phí cực thấp, quét repo toàn diện. | Có xu hướng tóm tắt nếu prompt thiếu neo chặn; cấm quyết định lệnh tài chính đơn độc. | Rà soát codebase lớn, đọc phân tích log backtest MQL5, xử lý batch data, drafting nhanh. |
| **Codex / ChatGPT Desktop** (GPT-4o / o1 / o3-mini) | 9.0 | 9.0 | 7.5 | 7.5 | 8.5 | Suy luận logic toán học, giải thuật tối ưu, viết test unit và script automation. | Thỉnh thoảng phát sinh boilerplate dài dòng; nhạy cảm với ngắt kết nối bridge stdio. | Viết test suite, mô phỏng thuật toán, script phụ trợ, tự động hóa pipeline. |
| **DeepSeek** (API V3 / R1) | 9.0 | 8.5 | 9.0 | 6.5 | 8.5 | Suy luận chuỗi logic sâu (Chain-of-Thought), tối ưu hóa toán định lượng và giải thuật. | Độ trễ API dao động theo tải máy chủ; cấm dùng cho tác vụ cần phản hồi thời gian thực dưới 3s. | Phân tích định lượng, mô hình hóa xác suất, tối ưu thuật toán nặng. |
| **Grok Build** (xAI grok binary) | 8.0 | 7.5 | 8.5 | 9.0 | 8.0 | Tốc độ quét thông tin trực tuyến cực nhanh, góc nhìn đối lập phi quy ước, không rào cản gượng gạo. | Tuân thủ định dạng nghiêm ngặt kém hơn Claude/Antigravity; cấm dùng cho core logic tài chính. | Quét xu hướng thị trường, tổng hợp dữ liệu real-time, Red Team phản biện góc nhìn mở. |

## 3. Quy tắc giao việc của Thủ lĩnh
1. **Nguyên tắc kép (Primary + Shadow):** Với tác vụ HIGH/CRITICAL, Javis giao cho Primary Agent thực thi và Shadow Agent chạy đối soát độc lập.
2. **Kích hoạt TCBP:** Khi gặp tác vụ mới chưa có số liệu hiệu năng trong ma trận, bắt buộc cắt Micro-Task kiểm tra 3 ứng cử viên trước khi giao luồng việc chính.
3. **Cập nhật lũy tiến:** Sau mỗi đợt chạy task lớn hoặc benchmark, cập nhật lại điểm số QC-5 và ghi nhận sự cố/đột phá vào lịch sử vận hành.


## 4. Cơ chế San Tải Linh Hoạt Đa Tác Tử (Dynamic Load-Balancing & Token Economy)
1. **Phân cấp tải 3 cấp độ (Load-Tiering):**
   - **Tác vụ nhẹ/Giao tiếp thường ngày (Light/Chat):** Mặc định dùng mô hình Flash tốc độ cao, chi phí cực thấp (Antigravity Flash / DeepSeek Flash / Groq) để trả lời dưới 2 giây và tiết kiệm 95% token.
   - **Tác vụ trung bình (Data/Drafting/Code nhỏ):** Tự động san tải sang Antigravity CLI (context 2M) hoặc Codex/ChatGPT.
   - **Tác vụ nặng/Kiến trúc/Audit an toàn (Heavy/Critical):** Chỉ kích hoạt mô hình suy luận cao (Claude Opus/Sonnet 3.7 hoặc GPT-o1/DeepSeek R1) khi bài toán đòi hỏi tính chính xác tuyệt đối.
2. **Nguyên tắc Chuyển giao Động (Fallback & Cross-Assist):**
   - Khi một tác tử bị nghẽn (rate limit, bận tiến trình, lỗi kết nối), tác tử rảnh rỗi gần nhất trong ma trận có điểm QC-5 tương đương sẽ tự động tiếp quản xử lý ngay, không để Sếp phải chờ.
   - Không cứng nhắc gán chết vị trí; linh hoạt tương trợ theo tải thực tế tại thời điểm gọi.
