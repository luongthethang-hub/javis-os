<!-- Sinh bởi Antigravity (agy 1.5.18), model gemini-3.8-flash-low, 26/11/2026 18:17, chế độ chỉ văn bản (đầu vào: đoạn trích ±15 dòng do Claude cắt từ bản sao b2e3a1a). Tokens: in 71349, out 4338. Kết luận của model là dữ liệu, chưa được kiểm lại. -->

### 1. Bảng rà soát các điểm gọi shell/tiến trình/thực thi động

#### Bảng 1: Mã nguồn chính (`cam_core/`, `adapters/`, công cụ quản trị)

| file:dòng | lệnh/ hàm gọi | lệnh dựng từ đâu | nhận đầu vào từ API/WebSocket/người dùng/model? | shell=True hoặc chuỗi ghép? | mức | lỗi Codex # liên quan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `adapters/cli_adapter.py:95` | `asyncio.create_subprocess_exec(*exec_cmd)` | `cmd` (list) truyền vào hàm; nếu Windows + file `.cmd`/`.bat` thì bọc `["cmd.exe", "/c", *cmd]` | **Có** (từ `PATCH /api/agents/{agent_id}` cấu hình `binary_path`/`cli_kind` hoặc khi gọi chat CLI) | Không `shell=True` nhưng trên Win32 bọc qua `cmd.exe /c *cmd` | **Cao** | #3 |
| `adapters/cli_adapter.py:681` | `subprocess.Popen(cmd)` | `cmd = ["cmd.exe", "/c", "start", ..., f'"{binary}" setup-token']` | **Có** (từ API `POST /api/agents/{agent_id}/auth` qua `payload` + cấu hình `binary`) | Chuỗi ghép với biến `binary` đưa vào `cmd.exe /k` | **Cao** | #3 |
| `adapters/cli_adapter.py:691` | `subprocess.Popen(cmd)` | `cmd = ["cmd.exe", "/c", "start", ..., f'"{binary}" login --device-auth']` | **Có** (từ API `POST /api/agents/{agent_id}/auth` qua `payload` + cấu hình `binary`) | Chuỗi ghép với biến `binary` đưa vào `cmd.exe /k` | **Cao** | #3 |
| `adapters/cli_adapter.py:701` | `subprocess.Popen(cmd)` | `cmd = ["cmd.exe", "/c", "start", ..., f'"{binary}" login']` | **Có** (từ API `POST /api/agents/{agent_id}/auth` qua `payload` + cấu hình `binary`) | Chuỗi ghép với biến `binary` đưa vào `cmd.exe /k` | **Cao** | #3 |
| `adapters/cli_adapter.py:711` | `subprocess.Popen(cmd)` | `cmd = ["cmd.exe", "/c", "start", ..., f'"{binary}"']` | **Có** (từ API `POST /api/agents/{agent_id}/auth` qua `payload` + cấu hình `binary`) | Chuỗi ghép với biến `binary` đưa vào `cmd.exe /k` | **Cao** | #3 |
| `adapters/web_session_adapter.py:126` | `subprocess.Popen(cmd)` | Danh sách tham số với đường dẫn trình duyệt `edge` và f-string `target_url`, `profile_dir` | **Có** (từ cấu hình URL agent / API mở webview) | Chuỗi ghép f-string trong list đối số | **TB** | #3 |
| `adapters/web_session_adapter.py:141` | `subprocess.Popen([sys.executable, "-c", worker_code])` | `worker_code` sinh bằng f-string chứa `self.config.name`, `target_url`, `self.profile_dir` | **Có** (từ cấu hình agent / URL webview) | Chuỗi ghép mã Python chạy qua `python -c` | **TB** | #3 |
| `adapters/web_session_adapter.py:261` | `subprocess.run(["gh", "auth", "token"])` | Cố định `["gh", "auth", "token"]` | **Không** (lệnh cố định kích hoạt khi gọi auth Copilot) | Danh sách đối số cố định, không `shell=True` | **Thấp** | Không |
| `cam_approve.py:38` | `subprocess.run(["git", *args])` | `["git", *args]` | **Chưa rõ** (nhận qua CLI args nội bộ của script `cam_approve.py`) | Danh sách đối số | **Thấp** | #6 |
| `cam_approve.py:44` | `subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"])` | Cố định chạy pytest trên thư mục `tests` | **Không** (tham số cố định trong hàm `default_checks`) | Danh sách đối số cố định | **Thấp** | #1, #6 |
| `cam_core/brain_manager.py:71` | `subprocess.run([git_bin, *args])` | `git_bin` từ `shutil.which` + `args` truyền vào nội bộ | **Chưa rõ** (tùy thuộc caller của `_run_git` trong BrainManager) | Danh sách đối số | **Thấp** | Không |
| `cam_core/chat_engine.py:444` | `await self.forge.run_command(cmd_match)` | Cắt từ tin nhắn người dùng gõ trong chat (`chạy lệnh:`, `powershell:`, v.v.) | **Có** (trực tiếp từ tin nhắn chat người dùng / API chat) | Chuỗi ghép truyền sang `code_forge.run_command` | **Cao** | #1, #2 |
| `cam_core/cloud_backup.py:337` | `subprocess.run([gh, "auth", "token"])` | Cố định `[gh, "auth", "token"]` | **Không** (lệnh cố định để lấy token local) | Danh sách đối số cố định | **Thấp** | Không |
| `cam_core/cloud_backup.py:403` | `subprocess.run([git_bin, *args])` | Danh sách tham số `git add -A` hoặc commit f-string chứa `active_brain_id`, `now_iso()` | **Chưa rõ** (`active_brain_id` có thể bắt nguồn từ API brains) | Chuỗi ghép trong danh sách đối số commit | **TB** | Không |
| `cam_core/cloud_backup.py:404` | `subprocess.run([git_bin, "push", "-u", remote_url, "HEAD:main"])` | `remote_url` ghép từ token và repo config | **Có** (từ cấu hình repo GitHub kết nối) | Chuỗi ghép trong đối số `remote_url` | **TB** | Không |
| `cam_core/code_forge.py:103` | `subprocess.run([git_bin, *args])` | `git_bin` + `args` từ các phương thức Forge (vd: `git init`) | **Chưa rõ** (tùy caller của `_run_git_sync`) | Danh sách đối số | **Thấp** | Không |
| `cam_core/code_forge.py:264` | `asyncio.create_subprocess_exec(*shell_cmd)` | `["powershell.exe", "-NoProfile", "-Command", cmd_str]` (hoặc `bash -lc`) | **Có** (từ API `/api/forge/command`, `/api/forge/pipeline`, hoặc từ chat engine) | **Có** (chạy qua PowerShell `-Command` / chuỗi lệnh ghép) | **Cao** | #1, #2 |
| `cam_core/evolution_engine.py:488` | `subprocess.run([sys.executable, "-m", "pytest", "-q"])` | Cố định `[sys.executable, "-m", "pytest", "-q"]` trong sandbox tạm | **Không** (lệnh cố định, nhưng chạy trên mã nguồn sao chép tạm từ repo) | Danh sách đối số cố định | **TB** | #1 |
| `cam_core/nano_agent_swarm.py:460` | `asyncio.create_subprocess_shell(cmd)` | Lấy trực tiếp từ `payload.get("command")` trong task runner | **Có** (từ API `/api/nano/dispatch` hoặc payload bảo trì) | **shell=True** (`create_subprocess_shell`) trực tiếp từ chuỗi đầu vào | **Cao** | #1, #2 |
| `cam_core/plan_detector.py:190` | `subprocess.run(exec_cmd)` | Cố định `["cmd.exe", "/c", "claude", "auth", "status", "--json"]` | **Không** (lệnh cố định phát hiện plan) | Chạy qua `cmd.exe /c` nhưng danh sách tham số tĩnh | **Thấp** | Không |
| `cam_core/plan_detector.py:415` | `subprocess.run([gh_bin, "auth", "status"])` | Cố định `[gh_bin, "auth", "status"]` | **Không** (lệnh cố định) | Danh sách đối số cố định | **Thấp** | Không |
| `cam_core/tool_installer.py:68` | `subprocess.run([resolved, "--version"])` | `resolved` tìm qua `shutil.which(tool_name)` | **Có** (từ `tool_name` gửi vào API check tool) | Danh sách đối số (`tool_name` do người dùng/API truyền) | **TB** | Không |
| `cam_core/tool_installer.py:92` | `subprocess.run([sys.executable, "-m", "pip", "show", clean])` | `sys.executable` + `-m pip show` + `clean` | **Có** (từ API check tool / install) | Danh sách đối số chứa tham số đầu vào | **TB** | Không |
| `cam_core/tool_installer.py:128` | `asyncio.create_subprocess_exec(gh_bin, "search", "repos", clean_q, ...)` | `clean_q` từ tham số tìm kiếm GitHub | **Có** (từ API `/api/forge/tools/search-github`) | Danh sách đối số | **Thấp** | Không |
| `cam_core/tool_installer.py:278` | `asyncio.create_subprocess_exec(*cmd)` | `cmd` dựng dạng `git clone --depth 1 <url> <dest>` | **Có** (từ API `/api/forge/tools/install` qua target URL) | Danh sách đối số chứa URL / đường dẫn người dùng gửi | **TB** | #1 |
| `cam_core/virtual_cursor.py:217` | `subprocess.Popen([sys.executable, str(overlay_script), str(self._udp_port)])` | Script overlay nội bộ và cổng UDP ngẫu nhiên | **Không** (tiến trình overlay hệ thống nội bộ) | Danh sách đối số nội bộ | **Thấp** | Không |
| `cam_doctor.py:96` | `subprocess.run([node, "--check", str(js)])` | Cố định node check trên danh sách file `.js` trong repo | **Không** (quét file repo nội bộ) | Danh sách đối số cố định | **Thấp** | Không |
| `cam_doctor.py:246` | `subprocess.run([sys.executable, "-m", "pytest", "-q"])` | Cố định `pytest -q` trong root repo | **Không** (lệnh cố định nội bộ) | Danh sách đối số cố định | **Thấp** | #1 |
| `cam_monitor.py:36` | `subprocess.run(cmd)` | `cmd` (list) truyền vào nội bộ trong monitor | **Chưa rõ** (tùy caller của `_run`) | Danh sách đối số | **Thấp** | Không |
| `cam_monitor.py:245` | `_run(["powershell", "-NoProfile", "-Command", "Get-ScheduledTask ..."])` | Chuỗi lệnh PowerShell cố định quét Scheduled Task | **Không** (lệnh kiểm kê hệ thống cố định) | Chạy chuỗi lệnh qua PowerShell `-Command` | **Thấp** | #2 |
| `cam_sentinel.py:141` | `subprocess.run([sys.executable, str(doctor_py), "--fast"])` | Script nội bộ `cam_doctor.py` | **Không** (lệnh cứu hộ cố định) | Danh sách đối số cố định | **Thấp** | Không |
| `cam_sentinel.py:162` | `subprocess.run([sys.executable, str(doctor_py), "--rollback"])` | Script nội bộ `cam_doctor.py` | **Không** (lệnh cứu hộ cố định) | Danh sách đối số cố định | **Thấp** | Không |
| `cam_sentinel.py:191` | `subprocess.Popen(cmd)` | `[sys.executable, "cam_desktop.py", "--headless"]` | **Không** (khởi động lại server CAM nội bộ) | Danh sách đối số cố định | **Thấp** | Không |

---

#### Bảng 2: Thư mục kiểm thử (`tests/`)

| file:dòng | lệnh/ hàm gọi | lệnh dựng từ đâu | nhận đầu vào từ API/WebSocket/người dùng/model? | shell=True hoặc chuỗi ghép? | mức | lỗi Codex # liên quan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tests/test_lock_3a4_apply_grant.py:58` | `subprocess.run([sys.executable, "-c", child])` | Mã Python tĩnh test logic thoát khi không có bàn phím | **Không** (mã test cố định) | Chuỗi mã tĩnh truyền qua `-c` | **Thấp** | #6 |
| `tests/test_lock_3a5_approvals.py:35` | `subprocess.run(["git", *args])` | Tham số init/config git test fixture | **Không** (dữ liệu test cố định) | Danh sách đối số | **Thấp** | Không |
| `tests/test_lock_3a5_approvals.py:37` | `subprocess.run(["git", "add", "-A"])` | Lệnh git cố định | **Không** (test fixture) | Danh sách đối số | **Thấp** | Không |
| `tests/test_lock_3a5_approvals.py:38` | `subprocess.run(["git", "commit", "-q", "-m", "init"])` | Lệnh git cố định | **Không** (test fixture) | Danh sách đối số | **Thấp** | Không |
| `tests/test_lock_3a5_approvals.py:43` | `subprocess.run(["git", "log", "--oneline"])` | Lệnh git cố định | **Không** (test fixture) | Danh sách đối số | **Thấp** | Không |
| `tests/test_lock_3a5_approvals.py:62` | `subprocess.run(["git", "log", "-1", "--format=%B"])` | Lệnh git cố định | **Không** (test fixture) | Danh sách đối số | **Thấp** | Không |
| `tests/test_smoke_real_boot.py:83` | `subprocess.Popen([sys.executable, "-c", CHILD, ...])` | Biến `CHILD` (chuỗi mã khởi động CAM test) | **Không** (mã fixture kiểm thử khói) | Danh sách đối số kèm mã `-c` | **Thấp** | #4 |

*(Ghi chú: các dòng `tests/test_cam_core.py:191`, `tests/test_cam_tool_and_handover.py:157`, `tests/test_lock_3a1_embedded_tools.py:32` là assert/regex test logic, không trực tiếp gọi hàm thực thi tiến trình).*

---

### 2. Thống kê theo mức rủi ro

- **Mã nguồn chính (`cam_core/`, `adapters/`, scripts):**
  - **Cao:** 7 chỗ (`cli_adapter.py:95, 681, 691, 701, 711`, `chat_engine.py:444`, `code_forge.py:264`, `nano_agent_swarm.py:460`).
  - **Trung bình (TB):** 7 chỗ (`web_session_adapter.py:126, 141`, `cloud_backup.py:403, 404`, `evolution_engine.py:488`, `tool_installer.py:68, 92, 278`).
  - **Thấp:** 19 chỗ.
- **Thư mục kiểm thử (`tests/`):**
  - **Thấp:** 7 chỗ.

---

### 3. Danh sách không kiểm được từ đoạn trích (cần đọc thêm file)

1. `cam_core/command_gate.py`: Cần đọc để kiểm tra toàn bộ regex/allowlist của `check_command(cmd)` (chặn hay chưa chặn biểu thức PowerShell `(...)`, `@(...)`, `{...}`, và cách chặn pytest ngoài thư mục chỉ định - Codex #1, #2).
2. `policy/cam_policy.json` & `cam_core/policy.py`: Cần đọc để kiểm tra danh sách `_CHAIN_CHARS` và cấu hình phân quyền tool cho từng agent.
3. `cam_core/registry.py`: Cần đọc để xác định cách lưu trữ/khởi tạo `binary_path`, `cli_kind` và cờ `CAM_POLICY=off` (Codex #3, #5).
4. `cam_core/l012_dispatcher.py`: Cần đọc dòng 29 xem có nhánh bỏ qua kiểm tra chính sách khi `CAM_POLICY=off` hay không (Codex #5).
5. `cam_core/l0_gate.py`: Cần đọc để xem cơ chế phát hành/tiêu thụ grant và nguy cơ bị gọi vòng lặp qua mặt L0 (Codex #6).
6. `cam_core/app.py` (tại các dòng xử lý endpoint `/api/forge/command`, `/api/nano/dispatch`, `/api/agents/{agent_id}`): Cần đọc chi tiết body hàm để xác minh cơ chế xác thực phiên và kiểm tra quyền trước khi đẩy vào adapter/forge (Codex #3, #4).
7. `chk_gate.py`: Cần đọc để đối chiếu 8 chuỗi test nghiệm thu cổng kiểm soát.
