---
slug: chong-treo-javis-khi-chay-tien-trinh-nen
title: Chống treo Javis khi chạy script vòng lặp vô tận (Watchdog / Bridge / Server)
type: technical
created: 2026-11-24
updated: 2026-11-24
tags: [javis, anti-hang, watchdog, root-cause, zero-regression]
source: incident 2026-11-24 02:41
---

# Quy tắc bất biến chống treo Javis (Zero-Regression)

1. **Nguyên nhân gốc đã kiểm chứng (24/11/2026 02:39):**
   - Chạy đồng bộ `python ...\emergency_watchdog.py` (hoặc bất kỳ script có vòng lặp `while True` / long-polling / server) ngay trong lượt chat khiến `agy.EXE` chờ tiến trình con kết thúc vô thời hạn và khóa chết toàn bộ phiên Telegram của Javis.
2. **Cách làm bắt buộc:**
   - Mọi tiến trình chạy dài (`watchdog`, `bridge`, `serve`, `daemon`) BẮT BUỘC khởi chạy tách nền hoàn toàn (`Start-Process pythonw.exe ... -WindowStyle Hidden` hoặc `subprocess.Popen(..., creationflags=0x08000000)`), tuyệt đối không chạy trực tiếp `python <script>.py`.
3. **Cầu chì thời gian:**
   - Đã cấu hình `JAVIS_AGY_TIMEOUT=180` trong `C:\Users\Admin\JavisOS\.env` để tự ngắt mọi lượt kẹt quá 3 phút thay vì treo 720 giờ.
