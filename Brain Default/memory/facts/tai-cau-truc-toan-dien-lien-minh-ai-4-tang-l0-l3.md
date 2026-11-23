---
slug: tai-cau-truc-toan-dien-lien-minh-ai-4-tang-l0-l3
title: Đề án Nâng cấp & Tái cấu trúc Toàn diện Liên minh AI (Kiến trúc 4 Tầng L0-L3 & Rule Registry)
type: fact
created: 2026-11-23
source: inbox/telegram/Mã hóa giảm dung lượng.txt
tags: [architecture, alliance, l0-l3, rule-registry, task-envelope, sem, co-evolution]
---

# Đề án Nâng cấp & Tái cấu trúc Toàn diện Liên minh AI

Phê duyệt và áp dụng trực tiếp theo chỉ đạo của Tổng chỉ huy Thắng Lee ngày 23/11/2026.

## 1. Tái định vị & Tinh chỉnh Hệ thống 4 Tầng (L0 - L3)

### Layer 0 (L0) - Principal & Supreme Architect (Lương Thế Thắng)
- **Vai trò:** Tổng chỉ huy tối cao, Kiến trúc trưởng hệ thống.
- **Quyền hạn:** Nắm giữ toàn quyền phê duyệt T0/T1, chỉ đạo chiến lược, nghiệm thu kết quả cuối cùng.
- **Cơ chế tương tác:** Phê duyệt nhanh 1 ký tự (`Y`/`N`), nhận báo cáo Zero-Fluff, không can thiệp code thủ công.

### Layer 1 (L1) - Strategic Alliance Orchestrators (Javis OS & Claude Desktop)
- **Vai trò:** Bộ đôi Điều phối chiến lược & Kiểm toán hạt nhân.
  - **Javis OS (Second Brain & Dispatcher):** Tiếp nhận chỉ thị từ L0, phân tích Task Envelope, quản trị bộ nhớ dài hạn, định tuyến ma trận và phát ngôn đa kênh.
  - **Claude Desktop (Lead System Architect & Safety Auditor):** Phân tích kiến trúc sâu, kiểm toán rủi ro cao, đối soát Blue/Red Team độc lập.
- **Ràng buộc:** Giữ Kernel `<= 18.000 bytes`, tuân thủ nghiêm ngặt Context Gating `<= 3.000 tokens`.

### Layer 2 (L2) - Tactical Muscle & High-Performance Executors (Antigravity & ChatGPT/Codex)
- **Vai trò:** Cơ bắp kỹ thuật & Thực thi thực chiến.
  - **Antigravity CLI (Tactical Muscle):** Quét repo, đọc/ghi tệp, biên dịch MQL5/Python, chạy CLI/test, tự vá lỗi cú pháp.
  - **ChatGPT Desktop / Codex (Algorithm & Speed Specialist):** Giải quyết thuật toán tối ưu, xử lý batch dữ liệu, tạo mẫu thử nhanh.
- **Ràng buộc:** Bàn giao sản phẩm chạy được 100%, có bằng chứng kiểm thử thực tế, cấm placeholder (`// TODO`).

### Layer 3 (L3) - Rule Registry, Task Envelopes & Storage Substrates (Hạ tầng lưu trữ & Kỹ năng động)
- **Rule Registry:** Kho quy tắc mã hóa (`MQL5-001`, `ISS-001`, `COEV-001`, `PROD-001`...) nạp động theo trigger.
- **Task Envelope Bus:** Giao thức truyền tin chuẩn hóa giữa các tầng (`task_id`, `domain`, `constraints`, `required_skills`).
- **Lưu trữ 3 tầng Zero-Loss:** Handover JSON `<= 48KB` -> SQLite WAL -> Physical Storage/Google Drive Backup.

---

## 2. Ma trận Định tuyến Nhiệm vụ (Router Matrix)
| Miền tác vụ | Điều kiện kích hoạt | Bot chủ trì (L1/L2) | Skill/Rule nạp động (L3) | Ngân sách Token | Cơ chế Fallback |
|---|---|---|---|---|---|
| Lệnh điều phối / Chat nhanh | Intent đơn giản, tra cứu | Javis OS | Fast Flash / Core Kernel | `<= 1.5K` | Escalate L1 Claude |
| MQL5 EA / Algo Trading | Code, backtest, OnTick | Antigravity | `rules/mql5-trading.md` | `<= 4K` | Red Team Claude Audit |
| Kiến trúc & Tái cấu trúc Lõi | Refactor, audit bảo mật | Claude Desktop | `rules/dual-agent-coevolution.md` | `<= 3K` | L0 duyệt |
| Tự động hóa / Tooling Desktop | App, web, script tiện ích | Antigravity | `rules/product-engineering.md` | `<= 4K` | Shadow Test |

---

## 3. Chu trình Bảo trì & Tự tiến hóa (SEM - MDACPT)
- Định kỳ 8 giờ một lần, hệ thống tự động rà soát toàn bộ kho quy tắc và bộ nhớ:
  1. **Merge:** Hợp nhất các quy tắc trùng mục tiêu.
  2. **Demote:** Hạ cấp chi tiết ít dùng từ Kernel xuống Rule Registry.
  3. **Archive:** Đóng gói quy tắc cũ sang deprecated.
  4. **Compress:** Rút gọn cú pháp thành YAML/JSON ngắn gọn.
  5. **Prune:** Cắt tỉa tri thức rác.
  6. **Test:** Chạy kiểm thử hồi quy bảo đảm không suy giảm chất lượng.
