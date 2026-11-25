# Tiếp nhận sáu repo và cầu nối CLI/desktop

Ngày 2026-11-25. Yêu cầu: web:c5891efc796348dbb651343acf8556e6 lúc 23:04.
Trạng thái cập nhật sau lựa chọn 1 của chủ: đã cài bản chưng cất kiến thức sáu nguồn vào Brain Default qua thay đổi #41-#44. Không tải/cài/chạy executable upstream, không đổi hooks hoặc daemon.

## Định danh nguồn ứng viên

1. ai-memory: https://github.com/akitaonrails/ai-memory. Tên còn có nhiều dự án khác; cần chủ xác nhận.
2. find skills: https://github.com/vercel-labs/skills, tệp skills/find-skills/SKILL.md. Cần phân biệt skill khám phá với CLI cài đặt.
3. superpower: https://github.com/obra/superpowers. Giả định theo tên thông dụng, cần xác nhận.
4. claude men: giả định là claude-mem, https://github.com/thedotmack/claude-mem; cần xác nhận, không cài theo lỗi chính tả.
5. uix pro max: giả định là https://github.com/nextlevelbuilder/ui-ux-pro-max-skill; cần xác nhận.
6. task observer: có ít nhất ba loại khác nhau. https://github.com/rebelytics/one-skill-to-rule-them-all là meta-skill cải tiến skill; https://github.com/mkarami313/claude-task-observer theo dõi lệnh/vòng lặp; https://github.com/danielgruederich/task-observer là giao diện theo dõi. Không tự chọn repo để cài.

## Phát hiện từ nguồn công khai

Các khẳng định dưới đây là mô tả README do WebFetch tóm tắt, chưa audit mã hoặc pin commit; không coi là chứng nhận an toàn.

- ai-memory: một writer SQLite, Markdown/wiki có Git và index có thể dựng lại; MCP, hooks, dịch vụ nền; Windows native thử nghiệm theo README. Setup có thể đổi cấu hình agent và startup.
- claude-mem: hooks, worker, SQLite, tìm kiếm; có xử lý observation bằng model và telemetry theo README. Không mặc định coi local storage đồng nghĩa local-only processing.
- superpowers: thiết kế, kế hoạch nhỏ, TDD, debug, review và xác minh; có cơ chế bootstrap/hook và quy trình bắt buộc. Không nhập chỉ dẫn cấp quyền hoặc thay quy tắc Git.
- find-skills: tìm, trình lựa chọn, cài sau đồng ý. Lượt cài và sao không thay audit nguồn/mã.
- UI UX Pro Max: hướng dẫn và dữ liệu design, tìm kiếm Python; đọc README không mang theo toàn bộ dataset hoặc công cụ.
- Task Observer của Rebelytics: quan sát, đề xuất cải tiến, review/staging; license README ghi CC BY 4.0, cần ghi công Eoghan Henn / rebelytics.com khi dùng phần phái sinh. Không tự bật observer/hook.

## Phân vùng chống xung đột đề xuất

- Javis memory hiện tại vẫn là nguồn chuẩn. Chưng cất ai-memory/claude-mem chỉ lấy truy xuất phân tầng, provenance, một writer, dedup, retention và quyền riêng tư. Không cài hai memory daemon cùng ghi.
- cam-tien-hoa sở hữu CUP và phê duyệt. Task Observer chỉ bổ sung tín hiệu quan sát có bằng chứng, không sinh nền tự nâng cấp.
- Skill vận hành hiện có sở hữu kế hoạch, điều phối và rollback. Superpowers chỉ bổ sung test-first và root-cause, không tạo bộ quy tắc toàn cục song song.
- Javis Builder sở hữu khám phá/cài capability; find-skills là nguồn tham khảo, không chạy npx hoặc cài global tự động.
- UI UX là năng lực riêng; không thay html-to-webcake, OpenMotion hoặc các quy tắc dataviz. Mã/dataset nếu cần phải cài riêng, audit và giữ license.
- Thay đổi lớp lõi chỉ sau khi duyệt diff và có undo id. Không sửa sealed T0, source server hoặc permissions trong bước intake.

## Máy cục bộ đã kiểm trực tiếp

Get-Command tìm thấy agy.EXE, codex.ps1, claude.ps1. Chưa kiểm login, quota hoặc job execution.
Get-Process với bộ lọc Antigravity|Codex|Claude|DeepSeek|ChatGPT không trả dòng tiến trình khớp tại thời điểm kiểm. Điều này không chứng minh app chưa cài hoặc không có process mang tên khác.
Chưa gửi prompt desktop, chưa chiếm focus cửa sổ, chưa chạy headless job hoặc đọc credentials.

## Phạm vi full quyền

Full chỉ là thực thi trong workspace, công cụ và phạm vi chủ đã cấp; không đồng nghĩa Administrator, lấy token desktop, bỏ xác nhận hoặc tắt sandbox.
CLI có thể chạy không cửa sổ nếu CLI hỗ trợ non-interactive. UI desktop không tự trở thành headless API; bridge cần được kiểm trên phiên đăng nhập thật.
Không vượt quota bằng đổi app cùng tài khoản; background liên tục trên subscription có thể trái điều khoản nhà cung cấp, cần lựa chọn API hoặc nguồn được phép khi phù hợp.

## Kết quả khảo sát cầu nối

Kiểm trực tiếp help: agy có --print và stream-json; codex có exec, exec --remote và app-server; claude có --print. Chỉ chạy help, chưa gọi model. Codex app-server được CLI đánh dấu experimental; không tự bật cổng nghe hoặc daemon.

Khảo sát chỉ đọc bởi subagent, chưa chạy end-to-end:
- Javis/server/antigravity_cli.py:1738-1741 có subprocess ẩn cửa sổ; đây là CLI, không điều khiển IDE desktop.
- D:/AI AGENT/council-agent-manager/adapters/cli_adapter.py:657-695 có Codex exec và DeepSeek dsh headless. Chưa kiểm binary dsh/login ở lượt này.
- Javis/scripts/handoff.ps1:91-138 cần foreground, clipboard, phím; không headless. Nhánh NoSend vẫn có thể sửa ô soạn, không phải dry-run chỉ đọc.
- Handoff dùng transcript ổn định và last.txt chung, không phù hợp chạy đồng thời cùng app; cần task_id và kết quả riêng.
- D:/AI AGENT/alliance-bus-runner/runner.py:43-74 được khảo sát là đếm dòng/log, chưa phải executor dispatch task.
- Claude Desktop có tài liệu kiểm trước đây; không thay kiểm live lần này. ChatGPT desktop chưa có bằng chứng nghiệm thu hiện tại.

Khuyến nghị kiến trúc: một owner mỗi task; tái sử dụng executor Javis/CAM thay vì thêm daemon. Hợp đồng task_id, workspace, quyền, timeout, idempotency_key, trạng thái queued/accepted/done/failed/unknown; unknown phải kiểm hậu điều kiện trước retry. CLI là đường ngầm chính; desktop handoff là fallback tuần tự khi thực sự cần UI và chủ cho phép tác động focus. Chưa triển khai hợp đồng này vào runtime.

## Bước còn thiếu

Chủ đã xác nhận sáu URL và Task Observer học từ phiên (Rebelytics). Đã đọc README tại commit cố định và Find Skills SKILL.md qua WebFetch; metadata license qua GitHub API. Chưa audit toàn bộ code hoặc đọc đầy đủ LICENSE/NOTICE; không sao chép mã/dataset upstream.

## Triển khai sau duyệt phương án 1
- #41: skills/cam-tien-hoa/references/repo-distillation.md, tổng hợp sáu nguồn, SHA đầy đủ, ghi công và phân vùng chống xung đột.
- #42: skills/cam-tien-hoa/SKILL.md, gắn học từ phiên, retrieval có nguồn và khám phá skill có kiểm soát.
- #43: skills/cam-cot-song/SKILL.md, test-first, root-cause và hợp đồng CLI/desktop ở mức playbook, chưa triển khai executor.
- #44: skills/ui-ux-thuc-chung/SKILL.md, năng lực UI UX riêng không trùng Webcake/video/dataviz.
- Không sửa skill hệ thống javis-builder; không sửa T0, permissions, server, agent model hoặc Git.

Kiểm tĩnh bằng python -I: 8/8 kiểm đạt (tệp, không em dash, metadata, độ dài description, sáu nguồn pin SHA, attribution, liên kết và giới hạn runtime). Description ba skill: 90, 98, 109 ký tự. Lần gọi đầu qua PowerShell lỗi quoting/SyntaxError; đã chạy lại bằng Bash heredoc thành công.
Chưa chạy kiểm hành vi model, mirror/router phiên mới, browser UI, login hoặc job CLI/desktop thật. Không coi phần chưng cất là đã cài đầy đủ sáu repo hoặc đã kết nối bốn engine.
Hoàn tác tích hợp: javis_improve op=undo theo thứ tự #44, #43, #42, #41; các lần sửa báo cáo có undo id riêng.
Bước tiếp theo: kiểm nạp skill ở phiên mới và nghiệm thu một task vô hại mỗi engine trước khi triển khai hợp đồng vào runtime.
