# Ma trận Vận hành L0-L1-L2, Mở rộng Năng lực & Ánh xạ Native JavisOS (RUULEE v6.0)

Tài liệu tham chiếu chi tiết cho skill `ruulee-operational-charter`. Chỉ nạp khi chạy FMEA sâu, thiết kế `TaskPacket`, triển khai Shadow Test/CUP hoặc đối chiếu kiến trúc module.

## 1. Lược đồ Chưng cất Ngữ cảnh `TaskPacket` (L1 -> L2)

Khi ủy thác cho L2 (Council agent, subagent hoặc script), chỉ truyền cấu trúc tinh gọn thay cho toàn bộ lịch sử chat thô (giữ tổng gói `<= 3.000` tokens):

```json
{
  "trace_id": "tr_20261124_001",
  "autonomy_level": "A2 | A3",
  "risk_tier": "LOW | MEDIUM | HIGH",
  "goal": "Mục tiêu cụ thể trong một câu",
  "constraints": ["Ràng buộc cứng 1", "Ràng buộc cứng 2"],
  "inputs": ["duong/dan/hoac/id"],
  "checklist": [
    "Kiểm tra đầu ra khớp lược đồ",
    "Kiểm tra vệ sinh dữ liệu và bí mật",
    "Trả tóm tắt Tier 1 kèm bằng chứng E1"
  ],
  "max_retries": 2,
  "escalate_to_l1_on_fail": true
}
```

## 2. Ma trận Mở rộng Năng lực Toàn Tự động (A0-A4)

| Mức | Phạm vi | Cổng kiểm soát & Xác minh | Điều kiện kích hoạt |
| --- | --- | --- | --- |
| A0 | CRITICAL / Mơ hồ cốt lõi | Quyết định L0 tường minh + xác nhận tươi + rollback | Thiếu mục tiêu cốt lõi hoặc xung đột T0 |
| A1 | HIGH Risk / Tác động ngoài | Impact Preview + L0 duyệt theo phạm vi | Gửi tin ngoài, đăng công khai, sửa repo rộng |
| A2 | MEDIUM Risk cục bộ | Pre-flight lint + post-flight Audit Log | Cập nhật file/cấu hình có phạm vi rõ |
| A3 | LOW Risk Swarm | `TaskPacket` song song + Cascade L2->L1 (tối đa 2 lỗi) | Tra cứu đa nguồn, trích xuất, tổng hợp |
| A4 | Tinh chỉnh vòng kín T2 | Shadow Test bất đồng bộ + CUP diff -> cổng L0 | Tín hiệu sửa lặp từ L0 hoặc cụm lỗi L2 |

## 3. Ma trận Stress Test (FMEA Vectors)

Chạy kiểm thử đối với các luồng trọng yếu trước khi gắn nhãn `VERIFIED_IN_SCOPE`:

- **Biên đầu vào:** Chuỗi rỗng, trường `null`, lỗi mã hóa UTF-8/dấu tiếng Việt, payload vượt trần token budget.
- **Lỗi thực thi:** Tool timeout, thất bại một phần trong batch, rate-limit HTTP 429, tranh chấp ghi file đồng thời (race condition).
- **Vệ sinh dữ liệu & Chính sách:** Cô lập dữ liệu ngoài không tin cậy (GOV-005), kiểm tra đường dẫn canonical chống path traversal, quét lộ bí mật/PII trong đầu ra.
- **Bảo vệ chi phí & Vòng lặp:** Chặn vòng lặp thử lại vô hạn, kiểm chứng kích hoạt Cascade L2 -> L1 đúng sau **2 lần thất bại**, khống chế độ sâu đệ quy.

## 4. Quy trình Hội tụ Trí nhớ Episodic -> Semantic & CUP

1. **Thu thập (Capture):** Ghi nhận sự kiện L0 sửa sai (bản nháp bị bác, làm rõ lặp lại) cùng chỉ số `trace_id` của L2 (token, độ trễ, mã lỗi).
2. **Hội tụ (Consolidate):** Chưng cất thói quen bền vững vào `memory/facts/` kèm phân tầng `T2` (`provenance`, `decay_days`), dùng `superseded_by` hợp nhất bản trùng theo MDACPT.
3. **Đề xuất CUP (Synthesize):** Soạn đề xuất chỉnh sửa quy tắc T2 hoặc mở rộng skill/tool để triệt tiêu điểm nghẽn lặp.
4. **Chạy bóng (Shadow Run):** Chạy lại mẫu prompt thực tế trên cả bản nền và bản ứng viên ở chế độ ẩn không gây tác dụng phụ.
5. **Chấm điểm & Cổng duyệt (Judge & Gate):** So sánh độ chính xác, tuân thủ ràng buộc và mức tiết kiệm token; trình diff + rollback plan lên L0 duyệt.

## 5. Checklist Kiểm toán Doanh nghiệp & Nhật ký Truy vết

- **Khả năng truy vết:** Mọi yêu cầu L0 liên kết tới kế hoạch L1, `trace_id` của L2, đầu ra công cụ và mức bằng chứng (`E1..E5`).
- **Ghi log phân tầng:** Tier 1 ghi gọn 1-2 dòng trạng thái, quyết định, chi phí token; Tier 2 (tham số đầy đủ, stack trace) chỉ bật khi lỗi hoặc kiểm toán.
- **Tách Governance khỏi Observability:** Kiểm soát quyền tối thiểu, allowlist đường dẫn và quét bí mật chạy ở tầng runtime độc lập với tầng ghi log quan sát.

## 6. Ánh xạ Native-First trên JavisOS (So với 2026 Reference Stack)

Ưu tiên nối trực tiếp vào module Python sẵn có của JavisOS để tránh phình RAM và chồng chéo hạ tầng:

| Vai trò kiến trúc | Module Native của JavisOS (`server/`) | Tham chiếu 2026 Stack (chỉ tham khảo tư duy) |
| --- | --- | --- |
| Điều phối & Workflow Graph | `workflow_graph.py`, `tasks.py`, `execution_guard.py` | LangGraph, OpenAI Agents SDK, Google ADK |
| Định tuyến model mạnh/nhẹ | `model_router.py` (lọc năng lực trước, giá sau, fail-closed) | RouteLLM |
| Nén ngữ cảnh & Biên dịch | `context_compiler.py`, `context_compressor.py` | LLMLingua-2 |
| Trí nhớ 3 tầng & Vòng đời | `memory_control.py`, `memory/tiers/` (T0/T1/T2 + SHA-256) | Mem0, Letta/MemGPT |
| Shadow Eval & Kiểm toán | `improvement_trial_runner.py`, `agent_ledger.py`, `secret_guard.py` | Langfuse, Arize Phoenix |
