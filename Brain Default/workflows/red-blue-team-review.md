---
type: workflow
name: Red/Blue Team Review (RUULEE v6.0)
slug: red-blue-team-review
status: 'off'
group: AI
description: "Rà soát đối kháng 3 bước (Blue Team -> Red Team 6 vector -> Safety Auditor) trả phán quyết DEBATE_VERDICT chuẩn cho plugin debate-engine."
steps:
  - agent: antigravity
    task: "Vai trò Blue Team (chỉ đọc, không sửa file): Phân tích đề xuất, thiết kế hoặc mã nguồn trong {{input}}. Trình bày rõ kiến trúc/lập luận cốt lõi, danh sách giả định (E4), điểm phụ thuộc và bằng chứng hiện có (E1..E5). Trả về bản tóm tắt ngắn gọn <= 400 từ."
    max_retries: 2
  - agent: grok
    task: "Vai trò Red Team đối kháng (cô lập ngữ cảnh, chỉ đọc): Tấn công phản biện phương án ở {{prev}} theo đúng 6 vector RUULEE v6.0: (1) lỗi logic/toán, (2) giả định ngầm không cơ sở, (3) giá trị biên/race condition/FMEA, (4) bảo mật/mất dữ liệu/gãy API, (5) chi phí token/RAM/độ trễ, (6) mâu thuẫn T0/T1. Nêu từng lỗ hổng kèm mức độ nghiêm trọng (CRITICAL/HIGH/MEDIUM/LOW)."
    max_retries: 2
  - agent: claude
    task: "Vai trò Safety Auditor & Trọng tài cuối (chỉ đọc): Đối soát bản phân tích Blue Team và phản biện Red Team trong {{prev}} với yêu cầu gốc {{input}} theo tiêu chuẩn T0/T1 RUULEE v6.0. BẮT BUỘC dòng đầu tiên của câu trả lời khớp chính xác một trong ba giá trị: DEBATE_VERDICT: PASS hoặc DEBATE_VERDICT: CONDITIONAL hoặc DEBATE_VERDICT: FAIL (không thêm tiền tố hay markdown ở dòng 1). Từ dòng 2 trở đi: tóm tắt tối đa 5 gạch đầu dòng gồm lý do phán quyết, rủi ro còn lại và điều kiện bắt buộc trước khi thực thi."
    verify_agent: perplexity
    max_retries: 2
updated: '2026-11-24'
---

# Quy trình Rà soát Đối kháng Red/Blue Team (`red-blue-team-review`)

Workflow chuẩn dùng cùng plugin `debate-engine` (chỉ đọc, không tạo tác dụng phụ ngoài). Khi chủ bật cả plugin `debate-engine` và workflow này (`status: active`), mọi lượt rà soát sẽ chạy qua 3 bước độc lập:

1. **Blue Team (`antigravity`):** Tóm tắt phương án, bằng chứng và giả định cốt lõi.
2. **Red Team (`grok`):** Tấn công phản biện cô lập theo 6 vector rủi ro RUULEE v6.0.
3. **Safety Auditor (`claude`, đối soát độc lập bởi `perplexity`):** Xuất dòng đầu tiên đúng định dạng `DEBATE_VERDICT: PASS|CONDITIONAL|FAIL` để `debate-engine` hạch toán tự động.
