---
name: Huấn luyện Agent Chuyên sâu (v1)
description: "Quy trình huấn luyện Agent đa bước theo RUULEE v6.0: TaskPacket handoff, thang tự chủ A0-A4, trí nhớ 3 tầng và kiểm toán trace_id."
group: AI
---

# Quy trình Huấn luyện Agent Chuyên sâu (Agent Pipeline v1 - RUULEE v6.0)

Quy trình thiết kế, huấn luyện và kiểm chuẩn các Agent hành động đa bước có sử dụng công cụ (tool-use), phối hợp subagent L0-L1-L2, thang tự chủ A0-A4 và hội tụ trí nhớ dài hạn theo **RUULEE v6.0**.

## Khi nào dùng

- Xây dựng, nâng cấp hoặc kiểm chuẩn một Agent / Workflow nhiều bước có gọi tool, đọc/ghi tệp hoặc điều phối subagent.
- Khắc phục lỗi Agent bị kẹt vòng lặp công cụ, phình ngữ cảnh khi bàn giao, hoặc vượt quá phạm vi quyền cho phép.
- Thiết lập cơ chế học từ tín hiệu sửa sai của Layer 0 mà không phá vỡ ràng buộc T0/T1.

## Chuẩn bị

- Nạp `skills/ruulee-operational-charter/SKILL.md` (và `references/l012-matrix-and-modules.md` cho `TaskPacket`, A0-A4 và FMEA).
- Kiểm tra danh sách Agent và Workflow hiện có trong `Javis/index.md` để không tạo trùng vai.
- Xác định rõ quyền tối thiểu (`min_mode`: `readonly` / `safe` / `full`) và danh sách tool được cấp cho từng bước.

## 5 Trụ cột Nâng cấp so với Huấn luyện AI Đơn lượt

1. **Vòng lặp Hành động Đa bước (Multi-Turn Agentic Loop):**
   - Quản lý trạng thái qua nhiều lượt gọi công cụ, kiểm tra hậu điều kiện sau hành động có tác động và xử lý lỗi timeout/429 có kiểm soát.
   - Biết dừng đúng lúc theo cổng `A0 (Ask-First)` khi thiếu dữ kiện ảnh hưởng tính đúng/an toàn thay vì đoán bừa.
2. **Bàn giao Cô lập bằng `TaskPacket` (L1 -> L2 Handoff):**
   - Không chuyển toàn bộ lịch sử chat thô cho L2; chỉ truyền gói `TaskPacket` gồm `trace_id`, `autonomy_level`, `risk_tier`, `goal`, `constraints`, `inputs`, `checklist` (3-5 mục) và `max_retries: 2`.
   - Khi L2 thất bại quá 2 lần -> kích hoạt ngay Cascade Escalation về L1 kèm log lỗi đã lọc bí mật.
3. **Huấn luyện theo Thang Tự chủ A0-A4:**
   - `A0` (Manual/Ask-First): Dừng xin xác nhận tươi từ L0 khi rủi ro `CRITICAL` hoặc thiếu mục tiêu cốt lõi.
   - `A1` (Assisted Preview): Xuất Impact Preview và kế hoạch hoàn tác trước hành động `HIGH`.
   - `A2` (Guarded Auto-Run): Tự chạy tác vụ `MEDIUM` kèm kiểm tra đầu vào và nhật ký kiểm toán sau khi xong.
   - `A3` (Autonomous Swarm): Điều phối song song nhiều L2 cho tác vụ `LOW` qua `TaskPacket`, Cascade sau 2 lỗi.
   - `A4` (Closed-Loop Calibration): Tinh chỉnh cấu hình/trí nhớ tầng `T2` qua Shadow Test mà vẫn khóa cứng `T0/T1`.
4. **Hội tụ Trí nhớ 3 Tầng (Episodic-to-Semantic):**
   - Tách rõ Working Context (`TaskPacket`), Episodic Trace (`trace_id` + tín hiệu L0 sửa sai) và Semantic Long-Term Memory (`memory/tiers/` T0/T1/T2).
   - Tri thức tầng T2 bắt buộc có `provenance` và chính sách suy giảm (`decay_days`); bản trùng hợp nhất bằng `superseded_by`.
5. **Tách Giám sát Quan sát khỏi Kiểm soát Runtime:**
   - Truyền `trace_id` thống nhất xuyên suốt chuỗi `L0 -> L1 -> L2 -> Tool Call` (Tier 1 log gọn 1-2 dòng; Tier 2 mở khi lỗi/audit).
   - Lớp Runtime Governance (`execution_guard.py`, `secret_guard.py`, quyền tối thiểu, kiểm đường dẫn canonical, lọc dữ liệu nhạy cảm) vận hành độc lập và fail-closed, không phụ thuộc vào lớp ghi log quan sát.

## Quy trình Kiểm chuẩn Agent (5 Bước)

1. **Khóa hợp đồng vai & quyền:** Định nghĩa đầu vào, đầu ra, tool allowlist, rủi ro và mức tự chủ A0-A4 của Agent.
2. **Kiểm tra biên bàn giao `TaskPacket`:** Xác nhận L2 hoàn thành được việc chỉ với gói `TaskPacket` <= 3.000 tokens mà không cần lịch sử thô.
3. **Diễn tập sự cố FMEA:** Thử nghiệm tool timeout, đầu ra sai schema, dữ liệu ngoài chứa prompt injection (GOV-005) và kiểm chứng kích hoạt Cascade sau 2 lỗi.
4. **Kiểm định Red/Blue & Shadow Run:** Chạy đối kháng 6 vector và thử nghiệm ẩn không tác dụng phụ trên ca thực tế trước khi bật.
5. **Bàn giao & CUP:** Ghi nhận bài học vào `memory/tiers/T2_adaptive/`, chỉ trình CUP lên L0 nếu cần đổi quy tắc T1 hoặc mở rộng năng lực mới.

## Bẫy

- Không đánh đồng "Agent trả lời mạch lạc" với "Agent hoàn thành đúng hậu điều kiện công cụ"; luôn kiểm bằng chứng `E1`.
- Không tự bật workflow, loop hay plugin mới tạo; để trạng thái `off` / `enabled: false` chờ L0 duyệt.
- Không cho phép Agent tự sửa T0, tự nâng quyền hoặc tự tắt cổng kiểm thử.

## Kiểm chứng

Agent chỉ đạt `VERIFIED_IN_SCOPE` khi:
- Vượt qua bài kiểm tra kịch bản hợp lệ + kịch bản biên (thiếu dữ liệu, tool lỗi, dữ liệu ngoài không tin cậy).
- Log truy vết thể hiện đủ `trace_id`, số lần thử (<= 2), trạng thái hậu điều kiện và không rò rỉ bí mật.
