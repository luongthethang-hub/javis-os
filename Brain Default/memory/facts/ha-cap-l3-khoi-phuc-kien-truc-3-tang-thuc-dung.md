---
slug: ha-cap-l3-khoi-phuc-kien-truc-3-tang-thuc-dung
title: Hạ cấp L3 và khôi phục Kiến trúc 3 tầng L0-L1-L2 thực dụng với cơ chế San việc Trực tiếp
type: fact
created: 2026-11-23
tags: [alliance, architecture, l0-l2, offloading, recovery]
source: chat 2026-11-23 (Tổng chỉ huy Thắng Lee duyệt Y)
---

# Khôi phục Kiến trúc 3 tầng L0-L1-L2 thực dụng

Được Tổng chỉ huy Lương Thế Thắng phê duyệt chính thức ngày 23/11/2026 sau khi phát hiện mô hình 4 tầng L0-L3 gây phân mảnh và tê liệt cơ chế san việc thực tế.

## 1. Cơ cấu 3 tầng tinh gọn (Zero-Fluff Architecture)
- **Layer 0 (L0) - Principal:** Lương Thế Thắng. Tổng chỉ huy tối cao, kiến trúc trưởng chiến lược, duyệt nhanh 1 ký tự (`Y`/`N`), không can thiệp kỹ thuật thủ công.
- **Layer 1 (L1) - Orchestrator (Javis OS):** Trung tâm điều phối, tiếp nhận yêu cầu, quản lý Second Brain, phân rã bài toán và kích hoạt san việc tức thì.
- **Layer 2 (L2) - Tactical Muscle (Liên minh thực thi bình đẳng):**
  - **Antigravity CLI:** Quét repo, đọc/ghi file, test, shell, compile MQL5/Python.
  - **Claude (@ThangleeClaude_bot):** Kiểm toán an toàn, tư vấn kiến trúc lõi, phản biện logic.
  - **Grok (@GrokThanglee_bot):** Red Team đối kháng, quét thông tin real-time, phản biện mở.
  - **ChatGPT / Codex:** Tối ưu thuật toán định lượng, script tiện ích.

## 2. Quy chuẩn San việc Trực tiếp (Direct Fallback Protocol)
1. **Ngưỡng ngắt mạch 5 giây (5s Circuit Breaker):** Nếu bot chủ trì không phản hồi hoặc bận tiến trình quá 5 giây, bot kế cận trong ma trận năng lực QC-5 tự động tiếp quản xử lý ngay lập tức.
2. **Loại bỏ trung gian Desktop nặng nề:** Giao tiếp qua bus dữ liệu và API thời gian thực, không phụ thuộc vào script cướp chuột/bàn phím Desktop cho các tác vụ điều phối.
3. **Context chuyển giao tối giản:** Khống chế nghiêm ngặt <= 3.000 tokens gồm mục tiêu, dữ liệu tóm tắt và tiêu chí nghiệm thu.

## 3. Kế thừa từ Đề án L0-L3 (đã hạ cấp)
- Bảo toàn chu trình bảo trì tri thức **MDACPT** (Merge, Demote, Archive, Compress, Prune, Test) định kỳ 8 giờ và nguyên tắc Rule Registry / TaskPacket (<= 3.000 tokens) ngay trong kiến trúc 3 tầng L0-L1-L2 mà không tách thêm tầng L3 gây phân mảnh.
