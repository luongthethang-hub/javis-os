---
name: Điều phối Đội nhóm & Token
description: "Phân rã việc theo TaskPacket, định tuyến agent theo thang A0-A4, Cascade tối đa 2 lỗi và nghiệm thu E1 trong Liên minh AI."
group: AI
---

# Điều phối Đội nhóm & Token (Đồng bộ RUULEE v6.0)

## Khi nào dùng

Kích hoạt khi nhận nhiệm vụ đa bước, dự án liên phòng ban (phát triển EA, sản xuất video, truyền thông đa kênh, kiểm toán hệ thống) hoặc cần phân công công việc giữa các thành viên Hội đồng Liên minh AI.

## Nguyên tắc cốt lõi

1. **Dynamic Gating (Fast Path):** Tác vụ đơn lẻ, tra cứu nhanh hoặc thao tác trực tiếp chạy thẳng qua model Flash/nhẹ, không dựng chuỗi điều phối nặng.
2. **Thang tự chủ A0-A4 & Quyền hạn Layer 0:**
   - `A0` (CRITICAL / mơ hồ cốt lõi): dừng hỏi L0 + xác nhận tươi + rollback plan.
   - `A1` (HIGH: sửa repo rộng, đăng bài, gửi tin ngoài, tài chính): lập Impact Preview chờ L0 duyệt phạm vi.
   - `A2` (MEDIUM: sửa file cục bộ có phạm vi): tự thực thi kèm kiểm tra trước và log sau.
   - `A3` (LOW: tra cứu, tổng hợp đa nguồn): chạy song song qua `TaskPacket` với Cascade fallback.
   - `A4` (T2 thích ứng): chỉ nâng cấp qua Shadow Test + CUP chờ L0 duyệt.
3. **Định tuyến năng lực trước, chi phí sau:** Chọn agent đáp ứng đủ ngưỡng chất lượng theo ma trận QC-5 với mức tiêu hao token thấp nhất. Không dùng model đắt tiền cho việc model nhẹ đã làm tốt.

## Quy trình Điều phối 5 Bước Tinh gọn

### Bước 1: Phân rã, Đánh giá Rủi ro & Gắn `trace_id`
- Tách bài toán thành các mục tiêu con nguyên tử (subtasks) và gắn 1 `trace_id` chung cho toàn bộ luồng.
- Phân loại mức rủi ro (`LOW | MEDIUM | HIGH | CRITICAL`) và mức tự chủ tương ứng (`A3 | A2 | A1 | A0`).

### Bước 2: Định tuyến & Chọn Agent Ứng viên (QC-5)
- Đối chiếu năng lực 8 agent hiện hành trong `Javis/index.md` và wiki `wiki/quan-tri-doi-nhom-va-dieu-phoi-token.md`.
- Chỉ định agent phản biện độc lập (Red Team: `grok`/`codex`, Safety/Ground-Truth Auditor: `claude`/`perplexity`) cho tác vụ `HIGH`/`CRITICAL`.

### Bước 3: Phát hành `TaskPacket` Chuẩn hóa (<= 3.000 tokens)
Mọi nhiệm vụ giao từ L1 sang L2 KHÔNG gửi lịch sử chat thô; chỉ đóng gói `TaskPacket` gồm:
- `trace_id`, `autonomy_level` (`A0..A4`), `risk_tier`.
- `goal`: 1 câu mục tiêu cụ thể.
- `constraints`: ràng buộc cứng, công cụ được phép dùng và điều cấm.
- `inputs`: đường dẫn tệp hoặc ID dữ liệu chính xác.
- `checklist`: 3-5 tiêu chí nghiệm thu bắt buộc.
- `max_retries: 2` và `escalate_to_l1_on_fail: true`.

#### TaskPacket v1: English handoff and shared pull queue
Write goal, constraints and acceptance checks in English. Preserve source quotations, identifiers and the requested output language. Never send raw chats or secrets. Use a new task_id per independent task; reuse the trace_id across siblings.

```json
{"schema":"taskpacket/v1","task_id":"demo-check-01","trace_id":"demo-01","goal":"Check whether all checklist items start with a verb.","constraints":["Read only the inline checklist.","Report in Vietnamese."],"inputs":[],"checklist":["Count all checklist items.","Identify any missing verb.","Return the count and findings."],"eligible_workers":["javis","deepseek-lead"],"autonomy_level":"A3","risk_tier":"LOW","max_retries":2,"escalate_to_l1_on_fail":true}
```

For local pull, use `python Javis/scripts/cam_queue.py` from the brain root. `put FILE` publishes one independent read-only A3/LOW packet (up to 3000 UTF-8 bytes). L1 lists only authorized, capable workers. Each input uses `source-or-chunk-id#sha256=<64 lowercase hex digits>`; verify the referenced bytes before use. Missing source, permission or digest match: stop and escalate.

At an authorized idle handoff, call `claim WORKER`; null means no work. Keep the returned ticket private. Never claim while busy. After execution, `submit TASK_ID TICKET EVIDENCE_REF` queues L1 review; `fail TASK_ID TICKET REASON` escalates. L1 independently verifies evidence; submission is not acceptance. `status` shows counts. A crashed worker's running claim is held for manual reconciliation, never automatically replayed. This local CLI trusts the OS account; it does not authenticate remote bots or grant tools. No external actions, scheduled polling or inbox broadcast by default.

### Bước 4: Giám sát & Cascade Escalation (`max_retries = 2`)
- Theo dõi tiến độ qua tóm tắt Tier 1 (1-2 dòng trạng thái, quyết định, chi phí token).
- **Giới hạn sửa lỗi cứng `max_retries = 2`:** Nếu một L2 agent không đạt nghiệm thu hoặc lỗi schema sau **2 lần thử**, lập tức ngắt vòng lặp và **Cascade Escalation lên L1** (hoặc chuyển agent dự phòng phù hợp / trình L0 nếu thuộc cổng A0-A1). Không giữ giới hạn cũ N = 3.

### Bước 5: Nghiệm thu Bằng chứng (`E1`) & Hội tụ Trí nhớ
- Kiểm tra hậu điều kiện thực tế và phân loại bằng chứng (`E1..E5`); không nhận hoàn thành dựa trên lời tự báo.
- Chưng cất bài học lặp lại sang tầng `T2` (`memory/tiers/T2_adaptive/`) hoặc lập đề xuất CUP nếu cần chỉnh quy tắc hệ thống.

## Bẫy

- Không gửi toàn bộ lịch sử trò chuyện vào `TaskPacket` làm phình token và nhiễu suy luận của L2.
- Không lặp quá 2 lần ở cùng một agent khi gặp cùng một lỗi cấu trúc hoặc thiếu tool/quyền.

## Kiểm chứng

Một lượt điều phối đạt chuẩn khi có `trace_id`, đầu ra từng bước khớp `checklist`, không vượt quá `max_retries = 2` và kèm bằng chứng kiểm chứng `E1`.
