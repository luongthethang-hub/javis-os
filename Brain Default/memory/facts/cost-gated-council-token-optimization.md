---
type: system
provenance: agent
origin: antigravity-bridge
created: 2026-11-25
updated: 2026-11-25
---
Bài học E1 từ L0 Thắng Lee (2026-11-25): Không gọi API apikey.fan ở mọi lượt. Áp dụng 4 lớp tiết kiệm trong src/ruulee_council/orchestrator.py: (1) Cost Gate mặc định 0-token cục bộ cho lượt thường (chỉ gọi API khi entropy>=0.55, risk>=HIGH hoặc lỗi lặp>=2); (2) JSON compact + chưng cất bullet 750/650 ký tự UTF-8 + Haiku 3.5 cho Audit LOW/MEDIUM; (3) Early-Exit 2 nhịp khi Red Team trả NO_CRITICAL_ISSUE; (4) Disk Cache TTL 24h. Shadow Eval thực nghiệm giảm 3,999 -> 1,823 tokens (-54.41% cold run, -46.76% latency) và 0 tokens khi cache hit.
