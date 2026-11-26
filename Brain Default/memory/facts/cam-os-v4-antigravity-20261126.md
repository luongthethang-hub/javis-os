---
slug: cam-os-v4-antigravity-20261126
title: CAM OS v4.0 do Antigravity nâng cấp (26/11/2026) - chưa commit, chưa nghiệm thu, nằm ngoài khóa ghi
type: project
memory_tier: T2
provenance: artifact-read
evidence: E2
created: 2026-11-26
updated: 2026-11-26
decay_days: 30
tags: [fact, cam-os, v4, antigravity, hmm-kernel, su-co, chua-nghiem-thu]
source: "docs/CAM_OS_EVOLUTION_BLUEPRINT.md, docs/CAM_UNIFIED_ARCHITECTURE_SPEC.md, git status repo CAM; Sổ Cái su-co:sua-chong-cam-20261126-2041"
---

# CAM OS v4.0 do Antigravity nâng cấp

## Antigravity tự báo (E2, chưa ai chạy lại)
Bản thiết kế `docs/CAM_OS_EVOLUTION_BLUEPRINT.md` (22:20) ghi trạng thái "VERIFIED_IN_SCOPE (Phases 1-4)", dung hợp đề xuất Javis + Antigravity:
- Tri thức 3 lớp `sources/ wiki/ memory/facts/` + `memory/quarantine/<run_id>/` có rollback manifest: `cam_core/knowledge_purifier.py`.
- HMM-Core `cam_core/hmm_kernel.py`: đo RAM/handle qua Win32 ctypes, mô hình Markov ẩn (Viterbi/Forward) suy trạng thái HEALTHY/DEGRADED/LOOP_STUCK/RESOURCE_LEAK/CRITICAL_FAULT, ma trận hành động fail-closed (OBSERVE, ISOLATE_WORKER, AUTO_HEAL_3S, ESCALATE_L0_CUP).
- Module khác: `tool_result_shaper`, `limit_learner`, `incident_desk`, `kanban_planner`, `cup_evolution`; giao diện `templates/ui/v4_cockpit.html`; test `tests/test_cam_v4_phase1.py`, `_phase2_3.py`, `_phase4.py`.
- Script `scripts/force_alliance_sync.py` (ghi SSOT liên minh ra 10 đích, kể cả `~/.claude/CLAUDE.md`) và `scripts/proactive_health_audit.py`.

## Thực tế đo được lúc 22:47 26/11 (E1)
- Toàn bộ là thay đổi CHƯA COMMIT trên nhánh `feature/G1-fix-codex-security`: sửa `cam_core/app.py`, `l012_dispatcher.py`, `policy.py`, `registry.py`, docs; thêm 7 module, 3 tệp test, `scripts/`.
- Được ghi trong lúc thread "Tái cấu trúc lõi CAM OS" đang giữ `khoa-ghi:cam-os`. Sổ Cái mở sự cố `su-co:sua-chong-cam-20261126-2041` (nghi Antigravity qua bot Telegram `bridge.py`, agy chạy `--dangerously-skip-permissions`). Task Scheduler có thêm `CAM_Proactive_Health_Audit` và `CAM_Headless_AutoStart` sau 18:09.
- Thread tái cấu trúc đã dừng sửa, không đụng các thay đổi này, chờ L0.

## Cách dùng tri thức này
- Chưa coi v4 là phiên bản chạy của CAM. CAM chính thức vẫn là v3.1.0 + các commit chữa tới d3c1b9d.
- Chưa có pytest, khởi động CAM thật và `/api/health` do bên thứ ba chạy cho v4; "VERIFIED" là Antigravity tự chấm.
- Ý tưởng kiến trúc (purifier, HMM-Core, cockpit) có thể làm đầu vào cho bản thiết kế tái cấu trúc, sau khi L0 quyết giữ hay lùi các thay đổi chưa commit.

Liên quan: [[quyet-dinh-l0-20261126]], [[luat-phong-giam-doc-20261126]], [[so-cai-he-log-chung]].
