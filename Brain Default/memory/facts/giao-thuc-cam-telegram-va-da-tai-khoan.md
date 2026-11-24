---
slug: giao-thuc-cam-telegram-va-da-tai-khoan
title: Giao thức Liên kết CAM <-> Telegram & Phương án Đa Tài khoản Claude / ChatGPT
type: system
created: 2026-11-24
updated: 2026-11-24
tags: [cam, telegram, claude, chatgpt, account-tier, multiplexer, reliability]
source: boardroom-directive-2026-11-24
---

# Giao thức Liên kết CAM <-> Telegram & Phương án Đa Tài khoản

## 1. Phương án kết nối theo từng loại tài khoản Claude & ChatGPT
- **Gói Free (`claude_free_web` / `chatgpt_free_web`):**
  - Không dùng `cli_native` (vì Free không có Claude Code CLI / Codex CLI).
  - Dùng `adapter_type: "web_session"` (WebView2 persistent profile tại `vault/webview_profiles/<id>`, 0 MB RAM khi ngủ) kết hợp `allow_javis_fallback: true` để bot Telegram vẫn trả lời 24/7 khi cửa sổ Web ngủ.
- **Gói Pro / Plus / Max (`claude_cli` / `codex_cli`):**
  - Dùng `adapter_type: "cli_native"` (`claude setup-token` 1 năm hoặc `codex login`), tự gia hạn qua Session Watchdog trước khi hết hạn 90 phút.
- **Gói API Key (`api_adapter`):**
  - Lưu `sk-ant-api03-...` hoặc `sk-...` mã hóa Windows DPAPI trong `vault/secrets.vault.json`, gọi thẳng API không bao giờ văng phiên.

## 2. Giao thức Liên kết CAM <-> Telegram (Nhanh, Thông suốt, Không 409)
1. **Single-Owner Multiplexer:** Toàn bộ bot L2 (`Claude, Grok, Perplexity, Dola, DeepSeek`) chạy chung 1 vòng lặp `asyncio` + 1 `httpx.AsyncClient` pool trong CAM (`cam_core/telegram_mux.py`), tốn ~5-10 MB RAM thay vì nhiều tiến trình rời rạc.
2. **Chống 409 Conflict tuyệt đối (`process_guard`):** Trước khi poll bất kỳ token nào, CAM kiểm tra tiến trình cũ; nếu có bridge cũ (như `telegram_bridge` của Antigravity), CAM tự giữ `STANDBY` thay vì tranh `getUpdates`.
3. **Phản hồi tức thì Zero-LLM (`< 0.5s`):** Các lệnh `/status`, `/brain <q>`, `/tojavis <msg>`, `/help` xử lý trực tiếp không gọi LLM.
4. **Tự phục hồi mạng:** Exponential backoff `2s..60s` khi rớt mạng hoặc HTTP 429, lưu offset nguyên tử (`tg_offsets.json`) không mất tin và không lặp tin.
5. **T0 Nuclear Gate:** Tự động kiểm tra `getMe` + cài `setMyCommands` khi khởi động.
