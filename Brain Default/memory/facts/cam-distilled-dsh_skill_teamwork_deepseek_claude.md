---
type: fact
title: "[DSH] Skill: teamwork-deepseek-claude"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/dsh_skill_teamwork_deepseek_claude.md"
evidence: E1
cam_content_hash: 90887b230666fe54443981b42c210034688d6874e62fb8252b9950fbeddd5344
cam_bundle_hash: 34caca1411c0e585
---

# [DSH] Skill: teamwork-deepseek-claude

---
slug: dsh_skill_teamwork_deepseek_claude
title: [DSH] Skill: teamwork-deepseek-claude
evidence: E1
source: cam-council
updated: 2026-11-26T23:37:22+07:00
tags: [dsh, skill, ruulee]
---

# [DSH] Skill: teamwork-deepseek-claude

Quy trình phối hợp đội DeepSeek ↔ Claude dựa trên ma trận năng lực 9 trục và ma trận độ khó 8 trục: định tuyến owner/reviewer, pattern phối hợp, budget token, xử lý xung đột và hiệu chuẩn chi phí bằng ruulee_route.

Skill tại: C:\Users\Admin\.dsh\skills\teamwork-deepseek-claude\SKILL.md

# Teamwork DeepSeek ↔ Claude

Quy trình này biến việc "hai AI cùng làm" thành **hợp đồng có chủ sở hữu, người phản biện, ngân sách
và bằng chứng**. Quyết định định tuyến do tool `ruulee_route` sinh ra, không do cảm tính.

## 1. Hiện trạng kết nối (kiểm tra 2026-11-26, E1)

- **Hub là CAM** (`D:\AI AGENT\council-agent-manager`, `http://127.0.0.1:8787`), không còn Javis.
  Kernel gọi CAM qua tool `ruulee_cam` (health/agents/chat/team/fact).
- CAM yêu cầu `X-CAM-Token` cho mọi lệnh ghi; token mỗi lần khởi động nằm ở
  `D:\AI AGENT\council-agent-manager\vault\api_session.token` — tool tự đọc, không cần cấu hình.
- Claude seat: `ONLINE`, `setup_token_1y`, relay `anthropic_relay_api`; chat 1-1 trả lời ~1,7s.
- DeepSeek seat trong CAM đang **tắt** (vault chứa key sai nhà cung cấp → `dsh` 401); DeepSeek thực
  thi trực tiếp bằng DSH kernel. OpenRouter seat cũng tắt (key 401).
