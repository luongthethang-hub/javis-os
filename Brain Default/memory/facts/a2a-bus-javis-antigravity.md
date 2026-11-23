---
type: system
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23 (06:24, 06:27; nguồn log memory/conversations/2026-11-23.md)
---
Hộp thư A2A cục bộ (Local File Bus) giữa Javis và Antigravity: thư mục `memory/a2a_bus/`, gồm `inbox_antigravity.jsonl` (Javis gửi gói tin đồng bộ cho Antigravity) và `inbox_javis.jsonl` (Antigravity gửi đề xuất CUP, yêu cầu kiểm tra hoặc phản biện cho Javis).

**Vì sao:** Telegram Bot API chặn bot đọc tin nhắn của bot khác trong group, nên hai bot không giao tiếp A2A được qua văn bản Telegram.

**Cơ chế đồng bộ tri thức (theo Javis):**
- Nguồn sự thật duy nhất là vault Brain Default (`memory/facts/`, `wiki/`, `rules/`). Không chia sẻ context window giữa CLI và agent.
- Antigravity truy xuất qua `brain_bridge.py` (lệnh `search`, `add-fact`, `save-wiki`) tại `C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\javis-brain-bridge\scripts\`.
- Tri thức chỉ đồng bộ khi được ghi xuống đĩa.

**Ghi chú xác minh:** thư mục và file `.jsonl` được Javis báo đã tạo, chưa kiểm tra tồn tại thực tế.
