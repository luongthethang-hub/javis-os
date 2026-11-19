---
type: dpf
status: approved-design
created: 2026-11-19
updated: 2026-11-19
version: 1.0.0
owner: platform-agent
scope: reusable-agent-platform
---

# DPF: Intelligent Session Splitting (ISS)

## 1. Mục đích

Đặc tả này định nghĩa cơ chế **Tách phiên thông minh** cho hệ thống agent dùng LLM. Mục tiêu là giới hạn chi phí và rủi ro tràn ngữ cảnh, nhưng vẫn bảo toàn chính xác trạng thái công việc khi một hội thoại dài phải chuyển sang context hoặc native thread mới.

ISS không thay transcript, database nguồn, repository hay hệ thống tác vụ. Handover chỉ là chỉ mục ngữ cảnh có cấu trúc và có bằng chứng để agent tiếp tục an toàn.

## 2. Phạm vi và không thuộc phạm vi

### Trong phạm vi

- Phát hiện thời điểm cần nén, xoay context hoặc tách sang session/thread con.
- Tạo handover JSON có schema, provenance và giới hạn kích thước.
- Bảo đảm không tách giữa một lượt agent còn dang dở, nhất là tool call có side effect.
- Lưu audit, quan hệ cha-con, khả năng khôi phục sau lỗi `context_length_exceeded`.
- Bootstrap context mới từ handover, compact summary và các nguồn cần đọc tối thiểu.
- Adapter cho provider có hoặc không có telemetry token chuẩn.

### Không thuộc phạm vi

- Tự ý xoá transcript, tool log gốc, tệp nguồn hoặc lịch sử audit.
- Suy diễn token khi provider không trả telemetry đáng tin cậy.
- Tự tạo dashboard chat/session nếu UI hoặc backend không cung cấp API đã xác minh.
- Thay thế phân quyền, transaction của tool, task queue hoặc cơ chế approval hiện hữu.

## 3. Thuật ngữ

| Thuật ngữ | Ý nghĩa |
|---|---|
| Session | Hội thoại logic nhìn thấy bởi người dùng, có ID ổn định trên UI. |
| Native thread | Thread/context riêng của provider hoặc CLI bên dưới session. Có thể được xoay mà không làm đổi session UI. |
| Turn | Một đơn vị thực thi từ input người dùng tới phản hồi cuối cùng, gồm các tool call phát sinh. |
| Atomic Turn Lock | Khoá ngăn quyết định split trong khi turn còn chạy hoặc còn tool call chưa được chốt. |
| Compaction | Nén một phần lịch sử trong cùng session thành summary, không đổi session/thread. |
| Handover | Gói JSON có cấu trúc để khởi tạo context/thread/session kế tiếp. |
| Split | Hành vi tạo session con nếu nền tảng hỗ trợ, hoặc xoay native thread nếu không hỗ trợ. |
| Telemetry | Dữ liệu runtime do provider/gateway trả về, như input token, output token, context window, cache state. |

## 4. Mục tiêu chất lượng và tiêu chí chấp nhận

| Mục tiêu | Tiêu chí bắt buộc |
|---|---|
| Tính liên tục | Context mới nhận handover hợp lệ, compact summary và tập nguồn tối thiểu trước khi trả lời tiếp. |
| Tính nguyên tử | Không split khi `turn_state != completed` hoặc còn tool call `pending/running`. |
| Không bịa dữ kiện | Mọi mục “verified facts”, “decisions”, “completed work” phải có reference; thông tin chưa chắc phải đánh dấu. |
| Khả năng truy vết | Mọi split ghi lý do, thời điểm, telemetry, session/thread cũ-mới, checksum handover và kết quả. |
| Idempotency | Retry cùng `turn_id` không sinh hai split/thread con hoặc hai audit record hiệu lực. |
| Tối ưu chi phí | Ưu tiên compaction tại chỗ nếu vẫn còn ngân sách context an toàn; chỉ rotate/split khi cần. |
| Tương thích | Không đòi provider phải có token counter; degrade theo policy rõ ràng khi thiếu telemetry. |

## 5. Nguyên tắc thiết kế

1. **Telemetry thắng ước lượng.** Chỉ áp ngưỡng token khi số liệu đến từ provider/gateway hoặc bộ đếm tokenizer đã được xác nhận phù hợp model.
2. **Split sau turn, không split trong turn.** Điều phối ISS chỉ chạy tại safe point sau commit của phản hồi/tool log.
3. **Session UI ổn định trước.** Nếu không có API tạo child session được xác minh, xoay native thread thay vì phá liên kết UI/WebSocket.
4. **Nén trước, tách sau.** Với áp lực context vừa phải, compact tool log và lịch sử cũ trước khi tạo context mới.
5. **Handover có cấu trúc, không phải prompt tự do.** Prompt bootstrap được render từ JSON đã validate.
6. **Nguồn gốc quan trọng hơn tóm tắt.** Handover chứa reference và digest, không sao chép source of truth.
7. **Một lý do chính cho mỗi split.** Lý do được chọn theo thứ tự ưu tiên để audit và tối ưu policy đáng tin cậy.

## 6. Kiến trúc tham chiếu

```text
Gateway/Provider telemetry ─┐
Turn lifecycle + tool state ├─> ISS Decision Engine ─> Compactor
Session/DB state ───────────┘             │                 │
                                           │                 v
                                           │          Handover Builder + Validator
                                           │                 │
                                           v                 v
                                      Split Executor <── Audit Store
                                       ├─ rotate native thread
                                       └─ create child session (nếu có API)
                                                  │
                                                  v
                                      Bootstrapper / Context Loader
```

### Thành phần

- **Turn Coordinator**: phát event `turn_started`, `tool_started`, `tool_finished`, `turn_completed`, `turn_failed` và giữ Atomic Turn Lock.
- **Telemetry Adapter**: chuẩn hoá usage/provider metadata thành `ContextTelemetry`.
- **ISS Decision Engine**: đánh giá trigger, cooldown, safe point và action phù hợp.
- **Compactor**: nén tool log/lịch sử có thể bỏ vào `compact_summary`; transcript gốc vẫn giữ nguyên.
- **Handover Builder**: tạo gói JSON versioned từ dữ liệu đã xác minh.
- **Split Executor**: ghi transaction audit rồi xoay thread hoặc tạo child session.
- **Bootstrapper**: dựng context mới theo thứ tự handover, compact summary, message gần đây và source references.
- **Audit Store**: SQLite/PostgreSQL hay kho tương đương, hỗ trợ idempotency và quan hệ lineage.

## 7. Máy trạng thái

```text
ACTIVE
  ├─(pressure detected)────> PENDING_EVALUATION
  ├─(turn starts)──────────> TURN_LOCKED
PENDING_EVALUATION
  ├─(unsafe)───────────────> DEFERRED
  ├─(compact chosen)────────> COMPACTING ─> ACTIVE
  └─(split chosen)──────────> HANDOVER_BUILDING
TURN_LOCKED
  └─(turn completed)────────> PENDING_EVALUATION
HANDOVER_BUILDING
  ├─(validation failed)─────> FAILED_SAFE
  └─(valid)─────────────────> EXECUTING
EXECUTING
  ├─(success)───────────────> BOOTSTRAPPING ─> ACTIVE
  └─(recoverable failure)───> DEFERRED
```

`FAILED_SAFE` phải giữ native thread hiện hữu, ghi lỗi audit và chỉ cho phép trả lời/tiếp tục bằng context hiện tại nếu provider còn chấp nhận. Không được đánh dấu split thành công khi bootstrap chưa thành công.

## 8. Trigger và chính sách quyết định

### 8.1 Các lý do chuẩn

```text
threshold | cache-expiry-risk | tool-log-pressure | new-workstream |
model-handoff | manual | context-overflow-recovery
```

Nếu nhiều trigger cùng đúng, dùng ưu tiên: `context-overflow-recovery` > `threshold` > `cache-expiry-risk` > `tool-log-pressure` > `model-handoff` > `new-workstream` > `manual`.

### 8.2 Cấu hình policy mẫu

```yaml
iss:
  enabled: true
  context:
    soft_ratio: 0.55
    hard_ratio: 0.78
    emergency_ratio: 0.92
    min_safe_remaining_tokens: 12000
  cache:
    enabled: true
    min_context_tokens: 20000
    idle_seconds_before_risk: 300
  tool_logs:
    compact_after_calls: 12
    compact_after_tokens: 8000
  handover:
    max_bytes: 48000
    recent_messages: 6
    source_references_max: 20
  cooldown:
    min_turns_between_rotations: 3
  actions:
    prefer_compaction: true
    create_child_session_if_supported: true
    otherwise_rotate_native_thread: true
```

Tỷ lệ context phải tính từ `current_context_tokens / provider_context_window`. Các con số trên là policy khởi tạo, cần được hiệu chỉnh theo model, giá cache và mức độ phức tạp công việc, không phải hằng số phổ quát.

### 8.3 Thuật toán quyết định

```pseudo
on_safe_point(session, completed_turn):
  telemetry = get_verified_telemetry(session)
  triggers = evaluate_triggers(session, telemetry)

  if no triggers or session.turn_lock.is_locked:
    return DEFER
  if split_exists_for_turn(session.id, completed_turn.id):
    return NOOP

  if trigger == tool-log-pressure and can_compact(session):
    compact(session)
    return COMPACTED

  if can_compact(session) and context_after_compaction_is_safe():
    compact(session)
    return COMPACTED

  handover = build_and_validate_handover(session, trigger, telemetry)
  persist_handover_and_reservation_atomically(handover)
  execute_split_or_rotate(handover)
  bootstrap_new_context(handover)
```

## 9. Atomic Turn Lock và tool safety

Mỗi turn phải có `turn_id`, `state`, danh sách tool invocation và `side_effect_state`. Split chỉ được xét khi toàn bộ điều kiện dưới đây đúng:

- `turn.state` là `completed` hoặc `failed_terminal`.
- Không có invocation ở `queued`, `running`, `awaiting_confirmation` hay `unknown`.
- Những tool side effect đã có kết quả commit/rollback xác định.
- Assistant response của turn đã được persist hoặc kết thúc bằng lỗi terminal có audit.
- Không có split/rotation reservation hiệu lực cho cùng `turn_id`.

Nếu provider báo overflow trong lúc tool call, hệ thống **không được retry mù quáng**. Nó phải hoàn tất hoặc khôi phục transaction tool theo contract của tool, ghi `context-overflow-recovery`, sau đó mới dựng context cứu hộ.

## 10. Schema dữ liệu

### 10.1 Bảng `sessions`

```sql
ALTER TABLE sessions ADD COLUMN parent_session_id TEXT NULL;
ALTER TABLE sessions ADD COLUMN root_session_id TEXT NULL;
ALTER TABLE sessions ADD COLUMN native_thread_id TEXT NULL;
ALTER TABLE sessions ADD COLUMN compact_summary TEXT NULL;
ALTER TABLE sessions ADD COLUMN compact_count INTEGER NOT NULL DEFAULT 0;
ALTER TABLE sessions ADD COLUMN last_input_tokens INTEGER NULL;
ALTER TABLE sessions ADD COLUMN last_context_window INTEGER NULL;
ALTER TABLE sessions ADD COLUMN thread_rotated_msg INTEGER NULL;
ALTER TABLE sessions ADD COLUMN split_reason TEXT NULL;
ALTER TABLE sessions ADD COLUMN handover_summary_json TEXT NULL;
ALTER TABLE sessions ADD COLUMN token_count_at_split INTEGER NULL;
ALTER TABLE sessions ADD COLUMN split_at TEXT NULL;
```

### 10.2 Bảng append-only `session_handover_audit`

```sql
CREATE TABLE session_handover_audit (
  id TEXT PRIMARY KEY,
  idempotency_key TEXT NOT NULL UNIQUE,
  source_session_id TEXT NOT NULL,
  target_session_id TEXT NULL,
  source_native_thread_id TEXT NULL,
  target_native_thread_id TEXT NULL,
  turn_id TEXT NOT NULL,
  action TEXT NOT NULL,                 -- compact|rotate_thread|create_child|recovery
  reason TEXT NOT NULL,
  telemetry_json TEXT NULL,
  handover_json TEXT NOT NULL,
  handover_sha256 TEXT NOT NULL,
  status TEXT NOT NULL,                 -- reserved|executed|bootstrapped|failed|rolled_back
  error_code TEXT NULL,
  created_at TEXT NOT NULL,
  executed_at TEXT NULL,
  completed_at TEXT NULL
);
CREATE INDEX idx_handover_lineage ON session_handover_audit(source_session_id, created_at);
```

Không được sửa payload handover đã audit. Nếu cần chỉnh, tạo record kế tiếp tham chiếu record trước.

## 11. Handover JSON contract

### 11.1 JSON Schema rút gọn

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ISS Handover v1",
  "type": "object",
  "required": ["schema_version", "handover_id", "source", "reason", "state", "continuation"],
  "properties": {
    "schema_version": {"const": "iss-handover/v1"},
    "handover_id": {"type": "string"},
    "created_at": {"type": "string", "format": "date-time"},
    "source": {"type": "object", "required": ["session_id", "turn_id"]},
    "reason": {"enum": ["threshold", "cache-expiry-risk", "tool-log-pressure", "new-workstream", "model-handoff", "manual", "context-overflow-recovery"]},
    "telemetry": {"type": "object"},
    "state": {"type": "object", "required": ["objective", "verified_facts", "owner_decisions", "completed", "in_progress", "risks", "open_questions"]},
    "continuation": {"type": "object", "required": ["next_step", "files_to_read", "recent_messages"]},
    "integrity": {"type": "object", "required": ["payload_sha256"]}
  }
}
```

### 11.2 Payload mẫu

```json
{
  "schema_version": "iss-handover/v1",
  "handover_id": "ho_01J...",
  "created_at": "2026-11-19T09:42:00+07:00",
  "source": {
    "session_id": "sess_123",
    "native_thread_id": "thread_old",
    "turn_id": "turn_456",
    "parent_session_id": null
  },
  "reason": "threshold",
  "telemetry": {
    "source": "provider_usage_event",
    "input_tokens": 58000,
    "context_window": 64000,
    "measured_at": "2026-11-19T09:41:58+07:00"
  },
  "state": {
    "objective": "Mô tả mục tiêu đang làm, không thêm suy đoán.",
    "verified_facts": [{"text": "...", "ref": "db:message/123"}],
    "owner_decisions": [{"text": "...", "ref": "db:message/110"}],
    "completed": [{"text": "...", "ref": "git:commit/abc"}],
    "in_progress": [{"text": "...", "ref": "task:xyz"}],
    "risks": [{"text": "Chưa xác minh ...", "ref": "none"}],
    "open_questions": []
  },
  "continuation": {
    "next_step": "Một hành động kế tiếp duy nhất.",
    "files_to_read": ["server/compaction.py"],
    "recent_messages": [{"role": "user", "content": "...", "message_id": "m_1"}]
  },
  "integrity": {"payload_sha256": "sha256:..."}
}
```

### 11.3 Quy tắc dựng payload

- `verified_facts`, `owner_decisions`, `completed` phải kèm `ref`; nếu không có bằng chứng, chuyển sang `risks` hoặc `open_questions`.
- `recent_messages` chỉ là cửa sổ hồi phục ngắn, không phải transcript đầy đủ.
- Giới hạn kích thước áp dụng trước khi persist. Khi vượt ngưỡng, ưu tiên cắt log/tool output và message cũ, không cắt objective, decision, risk, next step hay reference.
- SHA-256 tính trên canonical JSON, loại trường hash của chính nó.

## 12. Bootstrap context mới

Context mới phải được dựng theo thứ tự:

1. System/developer policy đang hiệu lực.
2. Handover JSON đã validate và checksum đúng.
3. Compact summary hiện tại, nếu có.
4. Source references trong `files_to_read`, chỉ đọc khi cần cho bước kế tiếp.
5. `recent_messages` giới hạn theo policy.
6. Prompt tiếp tục ngắn, nêu rõ đây là trạng thái kế thừa, không yêu cầu model diễn lại lịch sử.

Nếu handover invalid, checksum sai hoặc source bắt buộc không đọc được, bootstrap fail-safe: không xác nhận continuation thành công, giữ audit `failed`, và quay về native thread cũ nếu nó còn khả dụng.

## 13. API nội bộ tham chiếu

```text
POST /internal/iss/evaluate
POST /internal/iss/compact
POST /internal/iss/handover
POST /internal/iss/execute
POST /internal/iss/bootstrap
GET  /internal/iss/lineage/{session_id}
GET  /internal/iss/audit/{handover_id}
```

### Contract tối thiểu cho `/execute`

```json
{
  "handover_id": "ho_01J...",
  "idempotency_key": "sess_123:turn_456:threshold",
  "preferred_action": "create_child_session",
  "fallback_action": "rotate_native_thread"
}
```

Response chỉ được trả `status: bootstrapped` sau khi target session/thread tạo thành công và bootstrap context đã persist. Các trạng thái trung gian phải trả rõ `reserved`, `executed`, `failed` hoặc `deferred`.

## 14. Adapter provider

| Năng lực provider | Chiến lược |
|---|---|
| Có input token và context window | Dùng ratio context và ngưỡng policy trực tiếp. |
| Có input token nhưng không có context window | Dùng absolute threshold đã cấu hình theo model, gắn nhãn nguồn telemetry. |
| Không có usage nhưng gateway có cảnh báo context | Chỉ kích hoạt recovery/compaction theo cảnh báo xác thực. |
| Không telemetry hay cảnh báo | Không tự kích hoạt threshold. Chỉ xử lý manual, new-workstream hoặc model-handoff. |
| Có native thread nhưng không có session API | Rotate native thread, giữ session UI. |
| Có API child session | Tạo child liên kết `parent_session_id`, chỉ sau Atomic Turn Lock. |

## 15. Khôi phục khi overflow

1. Bắt lỗi provider có mã tương đương `context_length_exceeded`.
2. Đóng hoặc khôi phục toàn bộ tool invocation còn dang dở theo tool contract.
3. Ghi audit recovery với diagnostic tối thiểu, không đẩy toàn bộ tool log vào prompt.
4. Dựng emergency handover từ system policy, compact summary, state đã persist và N message gần nhất còn đọc được.
5. Tạo/rotate context mới, bootstrap, rồi retry **tối đa một lần** với idempotency key nguyên gốc.
6. Nếu retry thất bại, trả lỗi có thể hành động được và giữ audit. Không vòng lặp retry.

## 16. Quan sát, metric và cảnh báo

### Metric

- `iss_evaluations_total{result,reason}`
- `iss_actions_total{action,status,provider}`
- `iss_context_ratio` và `iss_input_tokens`
- `iss_handover_bytes`, `iss_handover_validation_failures_total`
- `iss_bootstrap_duration_ms`, `iss_recovery_total`
- `iss_compaction_tokens_removed`, `iss_rotations_avoided_total`
- `iss_cost_estimate_before_after` khi provider có dữ liệu giá đáng tin cậy

### Cảnh báo

- Handover validation failure liên tiếp.
- Split/rotation cùng session vượt cooldown.
- Bootstrap failure sau execute thành công.
- Context overflow sau bootstrap hoặc retry recovery.
- Handover payload vượt giới hạn thường xuyên, báo hiệu schema/compaction chưa đủ tốt.

Không dùng metric ước lượng để công bố tiết kiệm chi phí như một số liệu đã xác minh.

## 17. Bảo mật và riêng tư

- Handover chỉ chứa dữ liệu cần để tiếp tục, áp dụng cùng policy redaction với transcript/tool output.
- Không ghi secret, token truy cập, cookie hay raw credential vào handover/audit.
- Source reference phải qua ACL khi bootstrap, không coi ID tham chiếu là quyền truy cập.
- Audit append-only cần phân quyền đọc riêng; payload có thể chứa tóm tắt dữ liệu nhạy cảm.
- Hash đảm bảo phát hiện thay đổi, không thay thế encryption-at-rest hoặc chữ ký khi cần chống chối bỏ.

## 18. Kế hoạch triển khai

### Pha 1: nền tảng an toàn

- Thêm telemetry model, Turn Coordinator/Atomic Turn Lock, migration database và audit append-only.
- Triển khai compaction tại chỗ, Handover Builder, JSON Schema validator, checksum và unit test.
- Chỉ ghi handover/audit ở chế độ shadow, chưa xoay thread tự động.

### Pha 2: xoay native thread

- Bật Decision Engine tại safe point cho provider có native thread.
- Bootstrap từ SQLite + compact summary + handover JSON.
- Bật cooldown, idempotency và dashboard lineage read-only.

### Pha 3: child session nếu nền tảng hỗ trợ

- Tích hợp API tạo session con có `parent_session_id`, `split_reason` và `handover_id`.
- Đảm bảo UI/WebSocket chuyển đúng target session, có rollback khi bootstrap fail.

### Pha 4: tối ưu policy

- A/B policy theo provider/model, đo overflow, chi phí và lỗi continuation.
- Chỉ thay ngưỡng mặc định sau khi metric có ý nghĩa thống kê và được chủ hệ thống duyệt.

## 19. Bộ kiểm thử bắt buộc

- Unit: trigger precedence, cooldown, token ratio, thiếu telemetry, compaction selection.
- Unit: JSON Schema, byte cap, canonical checksum, không cho facts/decisions thiếu reference.
- Unit: Atomic Turn Lock với tool `running`, `awaiting_confirmation`, retry và terminal failure.
- Integration: migration từ DB cũ, reservation idempotent, rollback, lineage parent-child.
- Integration: rotate native thread cho từng provider adapter; bootstrap có compact summary và recent messages.
- Integration: overflow recovery, retry đúng một lần, không nhân đôi tool side effect.
- Regression: transcript/source gốc không bị chỉnh/xoá; session UI vẫn truy cập được sau rotate.
- Load: nhiều session đồng thời, lock contention, payload lớn, lỗi DB giữa execute và bootstrap.

## 20. Checklist production readiness

- [ ] Provider adapter khai báo rõ nguồn và độ tin cậy telemetry.
- [ ] Atomic Turn Lock có kiểm thử với mọi loại tool side effect.
- [ ] Handover JSON validate, hash và bị giới hạn kích thước trước khi persist.
- [ ] Audit có idempotency key, trạng thái lifecycle và lineage truy vết được.
- [ ] Bootstrap failure không bị báo thành công.
- [ ] Không có split tự động khi thiếu telemetry và không có trigger cấu trúc hợp lệ.
- [ ] Dashboard/observability hiển thị action, reason, target và lỗi thực tế.
- [ ] Rollout có feature flag theo provider/model và phương án rollback.

## 21. Quyết định mặc định khuyến nghị

Với agent platform chưa có API tạo chat/session con, cấu hình mặc định hiệu quả nhất là: **compaction tại chỗ trước, sau đó rotate native thread tại safe point, giữ nguyên session UI**. Chỉ nâng lên child session khi backend/UI có API đã xác minh, quan hệ lineage được persist và bootstrap có thể báo thành công một cách kiểm chứng được.

Các ngưỡng token trong DPF này là policy vận hành, không phải một phần bất biến của protocol. Schema, Atomic Turn Lock, idempotency, audit và bootstrap có kiểm chứng mới là các phần phải giữ ổn định khi áp dụng cho hệ thống agent khác.
