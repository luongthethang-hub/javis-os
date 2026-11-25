---
title: "CAM Out-of-Band Emergency Rescue Sentinel (Port 8789) & Nano Rescue Swarm"
tags: ["cam", "sentinel", "out_of_band", "rescue", "nano_swarm", "self_healing"]
evidence: "E1"
created_at: "2026-11-25T06:57:00+07:00"
author: "Antigravity (Layer 1 Co-Developer)"
status: "VERIFIED_IN_SCOPE"
---

# CAM OUT-OF-BAND RESCUE SENTINEL (`cam_sentinel.py`)

## 1. Giải quyết điểm mù sập toàn hệ thống
- **Vấn đề cũ:** Watchdog và Nano Swarm nằm bên trong tiến trình CAM (`8787`), nên khi CAM treo/crash thì công cụ cứu hộ cũng chết theo.
- **Giải pháp:** Tách **CAM Rescue Sentinel** thành tiến trình độc lập hoàn toàn trên cổng **8789** (`cam_sentinel.py`), không import `cam_core.app`.

## 2. Đội hình Nano Rescue Swarm Ngoại tuyến (4 Rescuers)
1. `NanoRescuer_Process`: Quét và kill các tiến trình treo chiếm cổng `8787` bằng `psutil`.
2. `NanoRescuer_Locks`: Dọn dẹp các file khóa bị kẹt trong `vault/locks/*.lock` (ví dụ `keepalive_grok.lock`).
3. `NanoRescuer_Doctor`: Chạy `cam_doctor.py --fast` (0-token); nếu phát hiện lỗi cú pháp/hỏng mã nguồn sẽ tự động gọi `--rollback` từ BootGuard.
4. `NanoRescuer_Reviver`: Khởi chạy lại `cam_desktop.py --headless` với `DETACHED_FLAGS` (`CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP`) và probe `http://127.0.0.1:8787/api/health` đến khi `200 OK`.

## 3. Giao diện & API Cứu hộ Từ xa (Port 8789)
- `GET /`: Emergency Web Rescue Console (1-click hồi sinh CAM).
- `GET /api/sentinel/status`, `POST /api/sentinel/rescue`, `POST /api/sentinel/doctor`, `POST /api/sentinel/kill-stale`, `GET /api/sentinel/logs`.
- Launchers chuẩn Windows CRLF/ASCII: `run_sentinel.bat` (chạy nền 24/7) và `rescue_cam.bat` (cứu hộ 1-click).

## 4. Kiểm chứng E1
- `tests/test_cam_sentinel_rescue.py`: `3/3 passed`; tổng 4 suite (`test_cam_v3_upgrades.py`, `test_cam_tool_and_handover.py`, `test_cam_nano_swarm.py`, `test_cam_sentinel_rescue.py`): `19/19 passed`.
- `cam_sentinel.py --rescue-now` thực tế: dọn lock `keepalive_grok.lock`, `cam_doctor` HEALTHY, khởi chạy lại CAM thành công (`200 OK` trong `4951ms`, tổng `6981ms`).
- `cam_doctor.py --fast`: `HEALTHY` (58 Python, 5 JS, 5 BAT, 0 API drift).
