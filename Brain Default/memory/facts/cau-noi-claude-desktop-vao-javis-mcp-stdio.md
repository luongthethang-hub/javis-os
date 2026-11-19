---
source: chat 2026-11-19 (2098bbec)
---
# Cầu nối Claude Desktop → Javis (đường A, MCP cục bộ)

Ngày dựng: 19/11/2026. Chủ yếu cầu "đi đường A": Claude Desktop gọi tool của Javis qua MCP.

## Cấu hình thực tế
- File cấu hình: `C:\Users\Admin\AppData\Roaming\Claude\claude_desktop_config.json`
- Bản sao lưu trước khi sửa: `claude_desktop_config.json.bak-javis` (3.034 byte, bản gốc chưa có mcpServers)
- Mục thêm vào (khoá `mcpServers.javis`):
  - `type: "stdio"`
  - `command: C:\Users\Admin\JavisOS\.venv\Scripts\python.exe`
  - `args: ["C:\Users\Admin\JavisOS\brains\Brain Default\Javis\bridge\javis_mcp_stdio_bridge.py"]`
  - `env`: `JAVIS_BRAIN`, `PYTHONIOENCODING=utf-8`, `PYTHONUNBUFFERED=1`, `PYTHONUTF8=1`

## Vì sao phải có cầu nối stdio
- Bản Claude Desktop trên máy là MSIX (WindowsApps, `Claude_5.11492.5.0_x64`, deploymentMode 1p).
- Schema `mcpServers` của bản này chỉ nhận mục kiểu stdio: `command` / `args` / `env` (xem `v_=A({command,args,env,extensionId})` trong `app.asar`).
- Thử khai kiểu `type: "http"` + `url` → log báo `Skipped invalid MCP server config entries: { invalidServers: [ 'javis' ] }`, server bị loại.
- Nên phải có một tiến trình stdio đứng giữa: script `Javis/bridge/javis_mcp_stdio_bridge.py` nói JSON-RPC 2.0 qua stdin/stdout rồi chuyển tiếp sang hub HTTP `http://127.0.0.1:7777/hub/mcp`.

## Token
- Token KHÔNG chép vào file cấu hình Claude. Bridge đọc `C:\Users\Admin\JavisOS\brains\Brain Default\.agents\mcp_config.json` (mục `mcpServers.javis.headers`) mỗi lần khởi động, nên token chỉ nằm một chỗ.

## Bằng chứng đã chạy
- Test tay qua stdio: initialize, tools/list, tools/call `javis_list_dir` đều trả kết quả đúng.
- Log Claude Desktop (`...\Claude_pzs8sxrjxfjjc\LocalCache\Local\Claude\logs\mcp-server-javis.log`) ngày 18/11/2026 17:41 UTC:
  `Server started and connected successfully`, `Message from client: method="tools/list" id=1`, `Message from server: id=1 result`.

## Điều còn hở
- Khi hub Javis tắt máy chủ (7777), bridge vẫn khởi động nhưng mọi lệnh gọi tool trả lỗi "Javis hub unreachable". Claude Desktop phải mở lại (hoặc reconnect server) sau khi Javis lên lại.
- Chiều ngược lại (Claude Desktop → chat trong brain Javis) vẫn không có: đây chỉ là gọi tool, không phải chat vào brain.
