---
slug: kich-hoat-hook-pha-vong-lap-micro-cvm-thuc-te
title: Đã Kích hoạt Hook Nhận diện Vòng lặp và Phá Vòng lặp Linh hoạt (Micro-CVM) vào Runtime
type: fact
created: 2026-11-24
updated: 2026-11-24
tags: [q5-cvm, anti-loop, runtime, antigravity, hook, auto-heal]
source: chat 2026-11-24 (Triển khai theo chỉ đạo Tổng chỉ huy)
---

# Kích hoạt Hook Nhận diện & Phá Vòng lặp Vô hạn (Micro-CVM)

Đã chuyển hóa 100% tài liệu lý thuyết `co-che-bieu-quyet-pha-vong-lap-vo-han-thong-minh.md` thành mã nguồn thực thi sống tại tầng runtime của Javis:

1. **Module Cảm biến (`server/anti_loop_guard.py`):**
   - Theo dõi từng luồng sự kiện gọi công cụ và thời gian sinh token.
   - Nhận diện ngay lập tức khi 1 công cụ bị gọi lặp lại 2 lần liên tiếp với cùng tham số lỗi (trạng thái lặp vòng vô tận).
   - Kích hoạt cơ chế Micro-CVM kết nối động cơ `D:\AI AGENT\q5-voting-engine\q5_vote.py`.

2. **Tích hợp Tầng Đọc Luồng (`server/antigravity_cli.py`):**
   - Móc nối trực tiếp vào vòng lặp đọc sự kiện CLI `proc.stdout.readline`.
   - Khi phát hiện vòng lặp: Tự động phát tín hiệu can thiệp, bẻ luồng sang phương án B/phương án thay thế thay vì để tiến trình rơi vào trạng thái chờ mù 720h.
