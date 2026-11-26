# Soát chéo CAM OS v4 của Antigravity - 26/11/2026 ~23:00 (giờ VN)

Người soát: thread Darklord "Tái cấu trúc lõi CAM OS" (Claude, khác hãng với Antigravity/Gemini).
Phạm vi: trạng thái repo `D:\AI AGENT\council-agent-manager` lúc 22:45. Không sửa, không hoàn tác gì trong repo thật.
Test chạy trên bản sao `D:\AI AGENT\cam-soat-v4-20261126` (chép mã, không chép vault/brains/logs/backups; `config/accounts_pool.json` không chép).

## 1. AG đã làm gì (bằng chứng E1: git status, git diff)

- Toàn bộ chưa commit. Có nhánh `feature/G1-fix-codex-security` nhưng nhánh này trỏ đúng d3c1b9d, không có commit nào.
- Sửa 4 file lõi: `app.py` (+199 dòng, 15 endpoint mới), `l012_dispatcher.py` (+14, hàm `evaluate_dispatch_health`, chưa được gọi ở đâu), `policy.py` (chặn `(`, `)`, `@(`), `registry.py` (PATCH không đổi được `binary_path`, `cli_kind`, `command_template`).
- 7 module mới: `cup_evolution`, `hmm_kernel`, `incident_desk`, `kanban_planner`, `knowledge_purifier`, `limit_learner`, `tool_result_shaper`.
- 3 file test mới (10 test), 2 tài liệu thiết kế trong `docs/`, giao diện `templates/ui/v4_cockpit.html`, thư mục `scripts/` (2 file).
- 2 tác vụ hẹn giờ mới: `CAM_Proactive_Health_Audit` (mỗi 4 giờ, chạy `scripts/proactive_health_audit.py`, chỉ đọc máy và gửi cảnh báo Telegram khi có bất thường) và `CAM_Headless_AutoStart` (khi đăng nhập, chạy thẳng `cam_desktop.py --headless`, không qua `run_cam_headless.bat`).
- CAM thật đang chạy mã chưa commit này (PID 12272, khởi động 22:20 qua `CAM_Headless_AutoStart`).
- Báo cáo của AG: `docs/CAM_OS_EVOLUTION_BLUEPRINT.md` ghi "Phases 1-4 Implemented & Verified"; `memory/a2a_bus/claude/res-handoff-G1.md` ghi G1 "partially_done", 2 lỗi đã vá.

## 2. Test (bản sao)

- `pytest --collect-only`: 142 test, 0 tệp đổi.
- `pytest tests -q`: 142 passed (132 cũ + 10 mới), 68 giây. Lần chạy đầu có 1 đỏ do bản sao thiếu `archive/`, chép thêm thì xanh; không phải lỗi của AG.
- Chạy đủ vẫn ghi `__pycache__` và `.pytest_cache` trong cây mã: lỗi G5 còn nguyên (bản vá `ag_G5.patch` chưa được áp).

## 3. Bốn đường chạy mã tùy ý (test tái hiện: bản sao, `tests/test_soat_exploits.py`)

- #1 Forge rồi pytest: VẪN MỞ. Ghi `test_evil.py` qua `/api/forge/file`, gọi `/api/forge/command` với `python -m pytest test_evil.py`, mã Python trong test chạy và tạo file đánh dấu.
- #2 Biểu thức PowerShell: ĐÃ CHẶN với mẫu `python -m pytest (New-Item ...)` (bản vá AG ở `policy.py`). Lệnh vẫn đi qua `powershell -Command`, nên đây là chặn theo danh sách ký tự, không phải sửa gốc.
- #3 PATCH `binary_path`: ĐÃ CHẶN (trả 200 nhưng `binary_path` không đổi). Chưa kiểm hash roster trước/sau.
- #4 `/api/nano/dispatch` với `role=task_runner`: VẪN MỞ. Lệnh shell bất kỳ chạy và tạo file đánh dấu.

## 4. Lỗ mới do v4 thêm vào

- `/api/cup/{id}/decide`: bất kỳ ai gọi API đều ghi được "L0 đã duyệt" (`decided_by` do người gọi tự điền), sau khi tự gửi điểm shadow-test do chính mình bịa. Test tái hiện ra `APPROVED`. Hiện chưa module nào áp dụng CUP có trạng thái APPROVED, nên chưa thành chạy mã, nhưng đây là bản ghi duyệt giả mạo và sẽ thành lỗ khi có bước tự áp.
- 15 endpoint mới, 10 cái là ghi; không cái nào có xác thực (API vẫn chưa có token, Codex #4 chưa sửa).
- `/api/knowledge/purify` với `dry_run=false` di chuyển file trong `brains/` (dữ liệu S2) theo lệnh của bất kỳ ai gọi API. Có chặn path traversal khi khôi phục.
- `CAM_Headless_AutoStart` tự bật CAM khi đăng nhập bằng mã đang có trong thư mục, kể cả mã chưa commit.

## 5. Điểm V1-V8 (đo chỉ đọc lúc ~22:55; mốc 72/100 lúc 17:10)

- V1 Sức khỏe: 13/15 (trước 10). `/api/health` OK. Smoke test đạt trên bản sao, chưa chạy smoke trên CAM thật.
- V2 Hồi quy: 14/15 (trước 13). 142 xanh, số test tăng. Trừ 1 vì G5 vẫn ghi vào cây mã.
- V3 Toàn vẹn dữ liệu: 11/15 (giữ). Hash các file theo dõi không đổi. CAM mới tạo thêm `vault/kanban_tasks.sqlite3` thật.
- V4 Ranh giới ghi: 5/15 (trước 14). ĐỎ: 18 mục chưa commit, CAM thật chạy mã chưa commit, có 2 bên sửa cùng repo trong một buổi tối.
- V5 Quyền: 8/15 (giữ). Đã chặn 2/4 đường, nhưng thêm bản ghi duyệt L0 giả mạo được và 10 endpoint ghi không xác thực.
- V6 Kết nối: 8/10 (giữ). 0 lỗi hôm nay, mới 1 lần khởi động.
- V7 Chi phí: 2/5 (giữ). Chưa có bộ đếm.
- UX: 6/10 (giữ). G6 chưa áp; trang `/v4` mới nằm ngoài kế hoạch.
- V8 Khối u: ĐỎ. Ngoài kế hoạch: 7 module, 15 endpoint, 2 tác vụ hẹn giờ, 15 file. Theo luật V8 thì báo L0, không tự xử lý.
- **Tổng: 67/100 (giảm 5 so với 72), V8 ĐỎ.** Phần lớn điểm mất nằm ở V4: việc của AG có giá trị nhưng chưa được commit, chưa được duyệt vào kế hoạch.

## 6. Đối chiếu với thiết kế kernel (`thiet-ke-tai-cau-truc-cam-os-20261126.md`)

- v4 của AG thêm năng lực mới (chẩn đoán HMM, kanban, CUP, dọn bộ não). Thiết kế kernel thì khóa đường tác động. Hai việc bổ sung cho nhau, không trùng.
- Còn thiếu so với kernel, theo thứ tự nên làm:
  1. B0: chia việc của AG thành các commit nhỏ trên nhánh, có ghi nguồn; L0 duyệt từng nhóm vào `v8_plan` hoặc gỡ (chuyển vào `backups/`, không xóa).
  2. B1: áp `ag_G5.patch` (cô lập test), thêm gốc dữ liệu `CAM_DATA_ROOT`.
  3. B2: cổng chạy tiến trình; tắt lệnh Forge và `task_runner` để đóng 2 đường còn mở; bỏ hẳn `powershell -Command`.
  4. B3: cổng API có token; `/api/cup/{id}/decide`, `/api/knowledge/purify` (khi `dry_run=false`) và `quarantine/restore` cần mã phép một lần của L0 từ `cam_approve.py`.
  5. B4, B5 như thiết kế (chính sách, cổng L0, cổng S và bộ đếm chi phí V7).
- Đề nghị: `CAM_Headless_AutoStart` gọi `run_cam_headless.bat` thay vì `cam_desktop.py`, và chỉ bật lại sau khi nhánh được nghiệm thu.

## 7. Giới hạn của lần soát này

- Chưa đọc từng dòng 7 module mới; mới soát endpoint, tác dụng phụ và test.
- Chưa có model khác hãng thứ ba soát lại (Codex lỗi token, dsh thiếu key).
- File test tái hiện chỉ nằm trong bản sao, chưa đưa vào repo.
