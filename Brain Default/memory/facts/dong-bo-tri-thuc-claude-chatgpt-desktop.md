---
type: system
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23 (07:54, 07:58, 08:03, 08:09; nguồn log memory/conversations/2026-11-23.md)
---
Trạng thái đồng bộ tri thức Javis với Claude Desktop và ChatGPT Desktop ngày 23/11/2026. Liên quan: [[cau-noi-claude-desktop-vao-javis-mcp-stdio]], [[nho-va-app-desktop-chatgpt-claude]].

**Claude Desktop:** plugin `javis` hiện trong Claude, nối MCP stdio tới hub cổng 7777. Log MCP dừng từ 22/11 15:08 (Javis khởi động lại làm ngắt cầu nối), nối lại lúc 08:05 và có 3 lượt gọi tool lúc 08:07 (theo Javis, đo từ log hệ thống).

**ChatGPT Desktop:** chưa hỗ trợ MCP cục bộ qua JSON. Đồng bộ qua `handoff.ps1` hoặc Custom Instructions/Project Knowledge. Chưa thực hiện.

**Đề xuất chưa xác nhận đã áp dụng:** "Claude Alliance Contract" (chỉ thị dán vào Custom Instructions của Claude: đọc `CLAUDE.md` và `MEMORY.md` trước tác vụ chuyên môn, ghi fact mới qua `javis_write_file`). Chủ cần quyết định có dán hay không.

**Điều kiện khi dùng:** nếu Javis khởi động lại, cầu nối stdio có thể không tự nối lại; khởi động lại Claude Desktop để khôi phục.
