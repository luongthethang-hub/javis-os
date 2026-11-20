# Task Capsule - mẫu bàn giao chịu lỗi

> Sao chép mẫu này vào thư mục đầu ra của nhiệm vụ. Chỉ ghi sự thật đã kiểm chứng. Không chèn credential, cookie, token hoặc lịch sử chat thô.

```yaml
schema_version: 1
request_id: ""
parent_job_id: ""
updated_at: "YYYY-MM-DD HH:mm Z"
status: active # active|blocked|awaiting_approval|completed
owner: ""
objective: ""
deliverable: ""
acceptance:
  - ""
scope:
  allowed:
    - ""
  forbidden:
    - ""
privacy:
  data_allowed_to_transfer:
    - ""
  data_redacted:
    - ""
execution:
  configured_source: ""
  verified_runtime_source: ""
  attempts: 0
  last_error_class: "" # transient|rate_limit|quota|auth|ui_drift|missing_capability|missing_data|quality|unknown_state
  last_error_verbatim_redacted: ""
  retry_after: ""
  circuit: closed # closed|open|half_open
progress:
  verified_completed:
    - step: ""
      evidence: ""
  current_step: ""
  next_single_step: ""
artifacts:
  - path: ""
    version_or_checksum: ""
    verified: false
side_effects:
  - action: ""
    idempotency_key: ""
    state: not_started # not_started|in_flight|verified|unknown
    evidence: ""
approvals:
  granted:
    - ""
  waiting_for_owner:
    - ""
open_risks:
  - ""
files_to_read:
  - ""
```

## Quy tắc cập nhật

1. Ghi trước bước tốn token, trước chuyển nguồn, sau mỗi mốc kiểm chứng và trước hành động có tác động.
2. `verified_completed` chỉ chứa kết quả có bằng chứng. Ý kiến của model không phải bằng chứng thực thi.
3. Nếu thao tác có side effect bị timeout, đặt `state: unknown`; kiểm tra hậu điều kiện trước khi thử lại.
4. Mỗi lần chuyển nguồn giữ nguyên `request_id`, phạm vi quyền và khóa idempotency.
5. `next_single_step` chỉ có đúng một bước, đủ cụ thể để nguồn mới làm tiếp mà không phát lại toàn bộ nhiệm vụ.
6. Khi hoàn tất, đặt `status: completed` và ghi vị trí sản phẩm cùng bằng chứng nghiệm thu.