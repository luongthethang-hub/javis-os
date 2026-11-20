---
type: session-handoff
status: active
updated: 2026-11-19 09:03
branch_id: giam-chi-phi-ngu-canh
context_reason: threshold
---

# Bàn giao phiên: cơ chế tách phiên thông minh

## Mục tiêu hiện hành
- Giảm chi phí ngữ cảnh khi một phiên hội thoại phình to, đặc biệt trường hợp gateway báo 49.8M token đầu vào.

## Sự thật đã xác minh
- Vault đã có quy ước dùng `wiki/_session-handoff.md` để chuyển giữa model/AI trong `AGENTS.md`.
- Chưa có plugin người dùng nào đang được cài để đo token hoặc tự tạo phiên mới.
- Javis hiện không có bằng chứng về một API/tool cho phép tự tạo hoặc tự chuyển cuộc chat mới.

## Quyết định của chủ
- Yêu cầu nghiên cứu và xây dựng ngay cơ chế tự động tách phiên thông minh để giảm chi phí ngữ cảnh.
- Khi quyền truy cập mã nguồn plugin/lõi hoặc API hội thoại được xác thực, nối cơ chế này vào tầng thực thi.

## Đã hoàn tất
- Tạo skill `skills/tach-phien-thong-minh/SKILL.md` với ngưỡng 12M, 25M và 40M token, mẫu bàn giao, quy trình tiếp nhận và quy tắc giữ bằng chứng.
- Khởi tạo tệp bàn giao này để giữ ngữ cảnh tối thiểu cho pha tiếp theo.
- Triển khai ISS v2 vào Javis OS: migration SQLite và các trường audit `split_reason`, `handover_summary_json`, `token_count_at_split`, `split_at`; handover JSON có schema phiên bản; ghi atomically sau khi một lượt hoàn tất và trước khi xoay native thread của Grok CLI, Codex và Claude Code.
- Giữ nguyên dashboard session thay vì tự tạo child session không thể mở trên UI. Native thread mới được bootstrap từ transcript SQLite và `compact_summary` có sẵn.
- Kiểm chứng ban đầu bằng `python tests/run.py compaction`, `test_ba_don_bay_token.py` và `test_claude_cli_moi_lai_mach.py`.
- Nâng ISS thành primitive vận hành có audit append-only: bảng `context_handovers`, ghi snapshot phiên và ledger trong cùng transaction SQLite; thêm API đọc nội bộ `get_context_handovers(...)`.
- Thêm regression cho schema handover, migration và thứ tự ledger; ngày 19/11/2026 đã chạy xanh `python tests/run.py compaction -v` và `python tests/run.py claude_cli_moi_lai_mach -v`.
- Bổ sung vào `AGENTS.md` giao thức thực thi: chỉ dùng telemetry đã có, giới hạn tệp đọc, ý nghĩa trạng thái và giới hạn khi chưa có API tạo chat.
- Bổ sung vào skill quy trình thu tín hiệu, điểm kiểm chứng trước khi đề nghị tách và ma trận kích hoạt theo ngưỡng/dấu hiệu cấu trúc.

## Đang làm
- Cơ chế đã nhất quán ở tầng quy tắc, skill và tệp bàn giao. Chưa thể tự mở phiên mới vì chưa có tool/API được xác minh cho hành động đó.
- Đã kiểm phạm vi tệp được cho phép trong bàn giao: chỉ có ba tệp quy tắc/bàn giao, không có mã nguồn plugin/lõi hoặc API hội thoại để tích hợp an toàn.

## Chưa xác minh hoặc rủi ro
- Chưa xác minh gateway có phát số token đầu vào cho engine/plugin ở từng lượt hay không.
- Nếu không có telemetry token, ngưỡng phải được kích hoạt từ cảnh báo gateway hoặc dấu hiệu cấu trúc của phiên, không được tự bịa số đo.

## Bước tiếp theo duy nhất
- Cung cấp đường dẫn mã nguồn plugin/lõi hoặc đặc tả API hội thoại đã xác thực, rồi áp dụng bản vá tiếp nhận telemetry token và tạo lời nhắc tách phiên.

## Files to read
- `AGENTS.md`
- `skills/tach-phien-thong-minh/SKILL.md`
- `wiki/_session-handoff.md`

## Không cần mang sang
- Log liệt kê thư mục và các lần thử tool không cung cấp năng lực quản lý phiên.
