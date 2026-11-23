---
type: fact
title: Kích hoạt đo lường R1 và đồng bộ model gemini-3.8-flash-low cho Javis
created: 2026-11-24
status: active
tags: [fact, optimization, latency, telemetry, fast-path]
source: chat 2026-11-24 (b36e5533)
---

# Kích hoạt đo lường R1 và đồng bộ model gemini-3.8-flash-low cho Javis

## 1. Bối cảnh
Nghiên cứu ngày 24/11/2026 (`inbox/telegram/nghien-cuu-javis-toc-do-cau-hoi-don-gian.md`) chỉ ra:
- Phản hồi câu hỏi dễ mất 9–28s do chưa có telemetry đo `antigravity-cli` và model bị trỏ lệch sang `flash-high`.
- Layer 0 (Thắng Lee) đã duyệt lệnh thực thi tối ưu hóa.

## 2. Các hành động kỹ thuật đã thực hiện (24/11/2026)
1. **Khóa cứng Model Routing:**
   - Cập nhật cấu hình `model.main` trong `server/settings.json` về `gemini-3.8-flash-low` thông qua API POST `/settings`.
   - Kiểm tra `GET /chat/route`: xác nhận đã nhận diện chính xác `selected_model: gemini-3.8-flash-low` (chấm dứt việc chạy ngầm `flash-high` gây chậm).
2. **Kích hoạt Telemetry R1 (Instrument):**
   - Đã chèn `_note_first_output("antigravity-cli", False)` vào luồng sự kiện `acli.query()` trong `server/main.py`.
   - Ghi nhận đầy đủ `first_output_ms` và nhật ký `[turn timing]` trên log của server cho engine `antigravity-cli`.
   - Biên dịch kiểm tra an toàn bằng `python -m py_compile server/main.py` thành công 100%.

## 3. Bước tiếp theo
- Theo dõi các mốc thời gian thực tế ghi nhận trong log `[turn timing]`.
- Tiếp tục thiết kế và thử nghiệm R2 (mở rộng Fast Path cho `simple_qa` có kiểm soát) và R4 (cắt giảm context nạp sẵn).
