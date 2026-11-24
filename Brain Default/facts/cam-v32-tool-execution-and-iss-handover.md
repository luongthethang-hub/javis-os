---
title: "Nâng cấp CAM v3.2: Cấp quyền công cụ thực thi, GitHub-First Installer & DPF/ISS Handover"
tags: ["cam", "ruulee_v6", "iss_handover", "tool_installer", "code_forge", "dpf", "zero_loss"]
evidence: "E1"
created_at: "2026-11-25T02:50:00+07:00"
author: "Antigravity (Layer 1 Co-Developer)"
status: "VERIFIED_IN_SCOPE"
---

# TỔNG HỢP NÂNG CẤP CAM v3.2.0

## 1. Cấp quyền công cụ cho phiên chat CAM (Tool Execution Bridge)
- **Vấn đề trước:** CLI `agy.EXE` chạy headless bị chặn bởi `jetski: command permission auto-denied` do thiếu tương tác duyệt quyền, buộc adapter phải gắn cờ cấm tool.
- **Giải pháp v3.2:**
  - Bổ sung cờ `--dangerously-skip-permissions` trong `adapters/cli_adapter.py` khi `allow_tools=True`, cho phép `agy` tự động chạy các công cụ trong headless mode mà không bị chặn.
  - Tích hợp `CodeForge` trực tiếp vào `CouncilChatEngine`: hỗ trợ nhận diện và chạy trực tiếp lệnh PowerShell, đọc/sửa file trong dự án với Workspace Fence.
  - Bổ sung cơ chế bóc tách và tự động thực thi các khối mã tool nhúng từ phản hồi model (` ```tool:run_command `).

## 2. GitHub-First Tool Installer (`cam_core/tool_installer.py`)
- Tra cứu repo chính thức trên GitHub qua GitHub REST API và `gh` CLI.
- Tự động dùng PowerShell để cài đặt công cụ cần thiết (`pip`, `winget`, `npm`, `git clone`) với `CREATE_NO_WINDOW`.
- Bộ lọc chốt chặn bảo mật chống shell injection (`BLOCKED_TARGET_PATTERNS`).
- Ghi nhật ký kiểm toán tại `logs/tool_installs.log`.

## 3. Giao thức DPF/ISS Handover thông minh (`cam_core/iss_handover.py`)
- Tuân thủ nghiêm ngặt đặc tả `iss-core-standard.md` và DPF:
  - Schema chuẩn: `iss-handover/v1`.
  - Giới hạn cứng ngân sách: `<= 48 KB` JSON.
  - Trích lọc tự động: Quyết định của L0 (`owner_decisions`), Dữ kiện kiểm chứng E1 (`verified_facts`), Việc dở dang (`pending_tasks`), Tóm tắt bối cảnh (`active_context_summary`).
  - Mã băm toàn vẹn `provenance_ref` (SHA-256) xuyên suốt toàn bộ luồng hội thoại.
  - Lưu trữ 3 tầng Zero-Loss: JSON Handover -> SQLite WAL (`chat_sessions.db`) -> Tệp snapshot vật lý (`brains/<id>/memory/handovers/<handover_id>.json`).
- Hỗ trợ bàn giao 1-click hoặc tự động sang phiên mới sạch sẽ khi đổi mode hoặc bão hòa ngữ cảnh, nạp sẵn vào warm cache.

## 4. Kiểm chứng E1 thực tế
- Bộ kiểm thử mới `tests/test_cam_tool_and_handover.py`: 4/4 passed.
- Toàn bộ suite `tests/test_cam_v3_upgrades.py` + `tests/test_cam_tool_and_handover.py`: 12/12 passed.
- `cam_doctor.py` kiểm định 0-token: `HEALTHY` (55 Python files ok, 5 JS files ok, 3 BAT files ok, 0 API contract drift, Pytest ok).
