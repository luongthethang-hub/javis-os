---
slug: a2a-bus-javis-deepseek
title: Giao thức kết nối 2 chiều Javis OS <-> DeepSeek (@DeepSeekThangLee_bot)
type: technical
created: 2026-11-24
updated: 2026-11-24
tags: [a2a-bus, javis, deepseek, telegram, protocol]
source: chat 2026-11-24 (1ea67e84)
---

# Giao thức kết nối 2 chiều Javis <-> DeepSeek (`@DeepSeekThangLee_bot`)

Vượt qua giới hạn Telegram Bot API chặn bot-to-bot bằng kênh đĩa cục bộ nguyên tử (`A2A Bus`) kết hợp tiến trình chạy nền `deepseek_bridge.py`.

## 1. Đường dẫn hộp thư 2 chiều
- **Javis -> DeepSeek (JSONL nhanh):** `C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus\inbox_deepseek.jsonl`
- **Javis -> DeepSeek (Tác vụ dài Markdown):** `C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus\deepseek\req-<id>.md`
- **DeepSeek -> Javis (JSONL phản hồi):** `C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus\inbox_javis.jsonl`
- **DeepSeek -> Javis (Kết quả file):** `C:\Users\Admin\JavisOS\brains\Brain Default\memory\a2a_bus\deepseek\res-<id>.md`

## 2. Định dạng gói tin chuẩn (JSONL)
- **Kiểm tra sống (`ping` -> `pong`):**
  `{"sender": "Javis", "timestamp": "...", "type": "ping", "data": {"req_id": "ping-001"}}`
- **Giao việc xử lý (`task` -> `task_response`):**
  `{"sender": "Javis", "timestamp": "...", "type": "task", "data": {"req_id": "t-001", "prompt": "..."}}`
- **Phát sóng ra Telegram qua `@DeepSeekThangLee_bot` (`relay_telegram` -> `relay_telegram_ack`):**
  `{"sender": "Javis", "timestamp": "...", "type": "relay_telegram", "data": {"req_id": "r-001", "chat_id": -1004479278576, "text": "..."}}`

## 3. Dịch vụ chạy nền
- Mã nguồn: `C:\Users\Admin\.gemini\antigravity\scratch\deepseek_bridge\bridge.py`
- Khởi chạy ngầm: `C:\Users\Admin\.gemini\antigravity\scratch\deepseek_bridge\start_hidden.vbs`
- Lệnh từ Telegram sang Javis: `/tojavis <nội dung>`
