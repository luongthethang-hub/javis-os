---
type: fact
title: Hợp nhất Dịch vụ Nền Alliance Bus Runner
created: 2026-11-24
tags: [fact, a2a_bus, runner, architecture, alliance]
source: chat 2026-11-24 (b36e5533)
---

# Dịch vụ Nền Duy Nhất: Alliance Bus Runner v1.0

- **Vị trí**: D:\AI AGENT\alliance-bus-runner\ (
unner.py, 
un_alliance_bus.bat).
- **Nhiệm vụ**:
  - Là daemon duy nhất thường trực giám sát toàn bộ hòm thư trao đổi A2A (inbox_deepseek.jsonl, inbox_antigravity.jsonl, inbox_javis.jsonl, thư mục oting/).
  - Phân luồng và kích hoạt tự động các bot trong Hội đồng Siêu nhóm khi có sự kiện hoặc bài toán cần phản biện/biểu quyết.
  - Loại bỏ hoàn toàn sự rời rạc của các script con, chống nghẽn luồng và tự động khôi phục sau restart.
