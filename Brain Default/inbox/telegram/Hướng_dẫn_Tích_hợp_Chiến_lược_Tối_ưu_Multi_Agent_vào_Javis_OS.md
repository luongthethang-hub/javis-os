# BẢN ĐẶC TẢ KIẾN TRÚC & HƯỚNG DẪN TÍCH HỢP: HỆ THỐNG TỐI ƯU MULTI-AGENT CHO JAVIS OS

## 1. THÔNG TIN CHUNG & MỤC TIÊU (META & OBJECTIVES)

*   **Tên dự án:** Javis OS - Multi-Agent Optimization Suite (MAOS)
*   **Mục tiêu cốt lõi:**
    1. Triệt tiêu rủi ro gián đoạn công việc do nghẽn/hết Rate Limit từ LLM Provider.
    2. Giảm từ $60\%$ đến $80\%$ lượng Input Token trên các dự án lớn/codebase phức tạp.
    3. Giảm từ $70\%$ đến $90\%$ lượng Output Token thừa thừa thải (over-engineering, scope creep).
*   **Nguyên lý thiết kế:** Trích xuất 3 mẫu thiết kế cốt lõi (OmniRoute, Graphify, Ponytail) và đóng gói trực tiếp vào tầng hạ tầng (Core Infrastructure) của Javis OS thay vì dùng tiện ích mở rộng bên ngoài.

---

## 2. KIẾN TRÚC TỔNG QUAN (SYSTEM ARCHITECTURE)

Hệ thống được chia làm 3 mô-đun chính tích hợp sâu vào quy trình xử lý của Javis OS:

```
[ User Request / Task Prompt ]
              │
              ▼
    [ Javis Orchestrator ]
              │
              ├──► [ Module 2: GraphRAG / MCP Indexer ]  <-- Ngữ cảnh cấu trúc (Map)
              │
              ├──► [ Module 3: Behavioral Guardrails ]   <-- Giới hạn phạm vi & Diff-Only
              │
              ▼
    [ Module 1: Unified LLM Gateway & Dynamic Router ]
              │
              ├─► Tier 1: Primary LLM (Claude Sonnet/Opus)
              ├─► Tier 2: Secondary LLM (GPT-4o/Gemini Pro)
              └─► Tier 3: Fallback/Local (Ollama/vLLM/Free Tier)
```

---

## 3. CHI TIẾT CÁC MÔ-ĐUN THỰC THI

### MÔ-ĐUN 1: UNIFIED LLM GATEWAY & FAILOVER SYSTEM (Mô phỏng OmniRoute)

#### 1.1. Mục tiêu
Đảm bảo tính sẵn sàng cao (High Availability - HA). Tự động chuyển đổi model khi gặp lỗi `HTTP 429` (Rate Limit) hoặc `HTTP 503`.

#### 1.2. Quy tắc Routing & Chuyển vùng (Failover Policy)
*   **Routing Tiering:**
    *   **Tier 1 (Planning & Core Logic):** Claude 3.5 Sonnet / Opus.
    *   **Tier 2 (Parallel Execution & Testing):** GPT-4o / Gemini 1.5 Pro.
    *   **Tier 3 (Local / Simple Tasks):** Llama-3 / Mistral via Ollama hoặc các model API chi phí thấp.
*   **Cơ chế State Handover (Bàn giao trạng thái):**
    *   Khi Tier 1 báo lỗi limit, Gateway bắt sự kiện và gọi dịch vụ Truncation Service.
    *   Rút gọn history hội thoại, chỉ giữ lại: `System Prompt` + `Architecture Summary` + `Current Task State` + `Last Working Code`.
    *   Gửi context đã nén sang Tier 2 kèm theo Cờ báo hiệu (Flag): `IS_FALLBACK_MODE = true`.

#### 1.3. Hướng dẫn nạp vào Javis Core
*   Tạo Proxy Layer trung gian cho mọi yêu cầu HTTP từ Agent ra bên ngoài (có thể sử dụng LiteLLM Proxy làm nền tảng).
*   Cấu hình `retry_strategy` với danh sách fallback ưu tiên theo mã lỗi trả về.

---

### MÔ-ĐUN 2: KNOWLEDGE GRAPH & STRUCTURAL INDEXING (Mô phỏng Graphify)

#### 2.1. Mục tiêu
Giải quyết tình trạng phình to ngữ cảnh (Context Bloat) bằng cách xây dựng bản đồ quan hệ giữa các file/hàm thay vì đọc toàn bộ mã nguồn.

#### 2.2. Quy trình Indexing & Querying
1.  **Static Code Analysis (Phân tích tĩnh):**
    *   Sử dụng `Tree-sitter` quét toàn bộ dự án khi khởi tạo workspace.
    *   Trích xuất các thực thể: `Classes`, `Functions`, `Imports`, `Dependencies`, `API Endpoints`.
2.  **Graph Construction (Dựng đồ thị):**
    *   Lưu các mối quan hệ dưới dạng Đồ thị (Directed Graph): Node = File/Entity, Edge = Import/Call/Inherit.
    *   Phân cụm đồ thị (Graph Clustering/Community Detection) để nhóm các module liên quan chặt chẽ.
3.  **MCP Context Provider (Giao tiếp qua Model Context Protocol):**
    *   Cung cấp 3 tool chuẩn cho Javis Agent:
        *   `mcp_get_project_structure()`: Trả về bản đồ tổng quan mức cao.
        *   `mcp_query_entity_deps(entity_name)`: Trả về danh sách phụ thuộc của hàm/class cụ thể.
        *   `mcp_get_community_context(topic)`: Trả về cụm mã nguồn liên quan trực tiếp đến tác vụ.

#### 2.3. Hướng dẫn nạp vào Javis Core
*   Yêu cầu các Agent ưu tiên gọi `mcp_get_project_structure()` trước khi dùng lệnh đọc file chi tiết (`read_file`).
*   Bắt buộc Agent ghi nhận "Bản đồ tọa độ" trước khi đưa ra quyết định chỉnh sửa code.

---

### MÔ-ĐUN 3: BEHAVIORAL GUARDRAILS & DIFF ENGINE (Mô phỏng Ponytail)

#### 3.1. Mục tiêu
Tránh over-engineering, ngăn chặn Agent tự ý thêm tính năng không được yêu cầu, và ép Agent xuất kết quả dưới dạng bản vá (Patch/Diff) để tiết kiệm Token.

#### 3.2. Cấu trúc System Instruction bổ sung (Prompt Guardrail)
Nạp prompt sau vào System Prompt mặc định của toàn bộ Worker Agent trong Javis OS:

```text
[STRICT OPERATIONAL RULES: MINIMALIST & REUSE FIRST]
1. REUSE EXISTING CODE: Before creating any new function/class/file, you MUST query the Knowledge Graph to verify if a similar component already exists. Reuse existing functions wherever possible.
2. NO UNSOLICITED FEATURES: Implement ONLY the exact requirements requested. Do NOT add dark mode, export features, extra abstraction layers, or unrequested refactoring.
3. OUTPUT FORMAT - DIFF ONLY: When modifying code, do NOT rewrite entire files. Output modifications strictly using Unified Diff or Search/Replace blocks:
   <<<<<<< SEARCH
   [original code snippet]
   =======
   [updated code snippet]
   >>>>>>> REPLACE
4. LOC BUDGET: Keep code changes strictly bounded. Any output exceeding +50 lines without explicit approval will be flagged for rejection.
```

#### 3.3. Structural Gatekeeper (Cổng kiểm soát kết quả)
*   Trước khi Javis OS thực thi thay đổi vào ổ đĩa, chạy một bước kiểm định nhanh (Validation Step):
    *   Đếm số dòng thay đổi ($\Delta \text{LOC}$).
    *   Nếu $\Delta \text{LOC} > \text{Threshold}$ (Ví dụ: $> 100$ dòng cho tác vụ sửa lỗi nhỏ), kích hoạt Cảnh báo và yêu cầu Agent tối ưu lại theo nguyên tắc *Minimal Patch*.

---

## 4. LỘ TRÌNH TRIỂN KHAI THEO GIAI ĐOẠN (IMPLEMENTATION ROADMAP)

```
[ Tuần 1 ] ──► Giai đoạn 1: Triển khai Dynamic Gateway & Fallback (OmniRoute)
[ Tuần 2 ] ──► Giai đoạn 2: Tích hợp GraphRAG & Tree-sitter MCP (Graphify)
[ Tuần 3 ] ──► Giai đoạn 3: Nạp Guardrail & Diff-First Output Engine (Ponytail)
[ Tuần 4 ] ──► Giai đoạn 4: Kiểm thử tích hợp (End-to-End) & Đo lường chỉ số ROI
```

### Chi tiết hành động từng tuần:

#### Giai đoạn 1 (Tuần 1): Tầng hạ tầng LLM Gateway
- [ ] Cấu hình LiteLLM Proxy làm router trung tâm cho Javis OS.
- [ ] Cài đặt fallback rules: Claude 3.5 Sonnet $\rightarrow$ GPT-4o $\rightarrow$ Ollama (Local).
- [ ] Xây dựng middleware xử lý cắt nỏ context (`Truncation Middleware`) khi xảy ra chuyển vùng (Failover).

#### Giai đoạn 2 (Tuần 2): Tầng Ngữ cảnh & Đồ thị
- [ ] Tích hợp bộ thư viện `Tree-sitter` vào Javis Core Backend.
- [ ] Dựng sơ đồ lưu trữ Graph trên bộ nhớ tạm (In-Memory Graph / NetworkX).
- [ ] Tạo Server MCP cung cấp 3 API truy vấn đồ thị cho Agent.

#### Giai đoạn 3 (Tuần 3): Tầng Hành vi & Kiểm soát Code Output
- [ ] Cập nhật System Prompt chuẩn cho tất cả Agent Roles (Coder, Reviewer, Tester).
- [ ] Xây dựng bộ parse Unified Diff/Patch trên Javis OS để áp dụng thay đổi vào workspace.
- [ ] Thiết lập ngưỡng Cảnh báo Dòng code ($\Delta \text{LOC}$ Guardrail).

#### Giai đoạn 4 (Tuần 4): Đánh giá & Tối ưu hóa
- [ ] Chạy nghiệm thu 50 tác vụ lập trình thực tế trên hệ thống mới.
- [ ] Đo lường các chỉ số:
  - Tỷ lệ giảm Input Token (So sánh trước và sau khi dùng GraphRAG).
  - Tỷ lệ giảm Output Token (So sánh Full Output vs Patch/Diff Output).
  - Thời gian Uptime của Agent khi gặp sự cố Rate Limit API.

---

## 5. ĐÁNH ĐỔI & QUẢN TRỊ RỦI RO (RISK MANAGEMENT)

| Rủi ro kỹ thuật | Mức độ | Biện pháp xử lý trong Javis OS |
| :--- | :--- | :--- |
| Model dự phòng (Tier 2/3) sinh code kém chất lượng | Cao | Chỉ giao tác vụ viết Unit Test, refactor nhỏ hoặc format cho Tier 3. Tác vụ kiến trúc phức tạp bắt buộc phải dừng và thông báo cho User thay vì ép model yếu chạy tiếp. |
| Graph bị lệch so với mã nguồn thực tế (Stale Graph) | Trung bình | Kích hoạt sự kiện `re-index` cục bộ ngay sau mỗi lần có lệnh ghi file (`file_write` / `apply_patch`) thành công. |
| Agent quá bảo thủ không chịu refactor code | Thấp | Cung cấp Cờ cấu hình `execution_mode`: Mặc định là `PATCH_MINIMAL`, khi cần đại tu codebase cho phép chuyển sang `FULL_REFACTOR`. |

---
*Tài liệu này được biên soạn dưới dạng chuẩn kịch bản kỹ thuật cho Javis OS. Vui lòng nạp trực tiếp nội dung này vào System Memory hoặc Knowledge Base của Javis.*