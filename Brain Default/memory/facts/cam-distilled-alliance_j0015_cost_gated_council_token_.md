---
type: fact
title: "[Liên minh] Cost Gated Council Token Optimization"
created: 2026-11-27
tags: [fact, cam-distilled, aitep, sync]
source: "cam:cam_primary:memory/facts/alliance_j0015_cost_gated_council_token_.md"
evidence: E1
cam_content_hash: 41bc785e9a56c8835f1d845e3d5531173de6a1c57333c7a9a2d165e3d1e8628f
cam_bundle_hash: 34caca1411c0e585
---

# [Liên minh] Cost Gated Council Token Optimization

---
slug: alliance_j0015_cost_gated_council_token_
title: [Liên minh] Cost Gated Council Token Optimization
evidence: E2
source: cam-council
updated: 2026-11-26T23:34:18+07:00
tags: [alliance, bridge, fact, knowledge-sync, sync]
---

# [Liên minh] Cost Gated Council Token Optimization

Bài học E1 từ L0 Thắng Lee (2026-11-25): Không gọi API apikey.fan ở mọi lượt. Áp dụng 4 lớp tiết kiệm trong src/ruulee_council/orchestrator.py: (1) Cost Gate mặc định 0-token cục bộ cho lượt thường (chỉ gọi API khi entropy>=0.55, risk>=HIGH hoặc lỗi lặp>=2); (2) JSON compact + chưng cất bullet 750/650 ký tự UTF-8 + Haiku 3.5 cho Audit LOW/MEDIUM; (3) Early-Exit 2 nhịp khi Red Team trả NO_CRITICAL_ISSUE; (4) Disk Cache TTL 24h. Shadow Eval thực nghiệm giảm 3,999 -> 1,823 tokens (-54.41% cold run, -46.76% latency) và 0 tokens khi cache hit.


---
Nguồn: ai-alliance/knowledge/entries/J0015-cost-gated-council-token-optimization.md · author=javis-core · updated=2026-11-26T00:03:39+07:00 · đồng bộ bởi DSH-CAM bridge.

