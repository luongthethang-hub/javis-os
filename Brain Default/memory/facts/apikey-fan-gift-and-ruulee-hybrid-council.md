---
type: system
provenance: agent
origin: antigravity-bridge
created: 2026-11-25
updated: 2026-11-25
---
L0 Thắng Lee cấp nguồn API apikey.fan (đã mã hóa Windows DPAPI trong D:\AI AGENT\council-agent-manager\vault\secrets.vault.json dưới tên provider:apikey_fan, agent:claude và agent:codex; cấm lưu plaintext vào markdown). Thực nghiệm E1 tại https://api.apikey.fan: (1) Anthropic /v1/messages chạy sống claude-opus-4-5, claude-sonnet-4-5-20250929, claude-3-7-sonnet-20250219, claude-3-5-haiku-20241022; (2) OpenAI /v1/chat/completions chạy sống gpt-6.2-astra, gpt-6.2-sol, gpt-6.1-sol, gpt-5.6-sol; (3) DeepSeek trả HTTP 404 trên khóa này nên dùng dsh cục bộ làm chính và tự động failover sang gpt-6.2-astra. Đã triển khai Hội đồng Tác chiến RUULEE v6.0 tại D:\AI AGENT\Antigravity Project\src\ruulee_council\ kế thừa correlation_id & text-only L2 từ Javis, DPAPI Vault & benchmark routing từ CAM, kiểm chuẩn TaskPacket <=3000 tokens, max_retries=2 Cascade, Blue/Red 6-Axis/Audit và Q5-CVM.
