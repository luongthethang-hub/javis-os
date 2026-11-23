# Báo cáo kỹ thuật: Bảo toàn tinh chỉnh Javis khi cập nhật & Đối soát Stash

Thời điểm kiểm chứng: 2026-11-23 17:05 UTC+7
Kho mã nguồn: `C:/Users/Admin/JavisOS`
Nhánh hoạt động: `feat/ai-company-reliability-local-20261119`

---

## 1. Kết luận nghiệm thu & Trạng thái hoàn thành

1. **Cơ chế bảo toàn tự động sau cập nhật:** Đã triển khai hoàn tất trong `server/update_preservation.py` và đấu nối trực tiếp vào `server/updater.py` (`stash_local_changes` và `restore_local_changes`).
2. **Kiểm thử hồi quy:**
   - `test_update_preservation.py`: PASS 100% (kiểm thử snapshot ngoài tree, 3-way merge, rollback giao dịch khi ghi lỗi, phát hiện xung đột, loại trừ file runtime/secret).
   - `test_updater_stash.py`: PASS 100% (kiểm thử 3-way merge giữ đồng thời tính năng mới của release và tinh chỉnh của người dùng; kiểm thử bảo vệ khi xung đột thực tế không làm mất stash).
3. **Hai Stash bất biến:** Cả `stash@{0}`, `stash@{1}` và `stash@{2}` được giữ nguyên vẹn 100% trong Git stash list, không pop, không drop, không reset mù.
4. **Guard plugin computer-use:** Tuân thủ giới hạn an toàn RUULEE T0/T1; không can thiệp script để phá bỏ rào chắn vendor của bên thứ ba.

---

## 2. Đối soát chi tiết 3 Stash

| Stash | Base Commit | File chính | Phân tích kỹ thuật & Trạng thái tích hợp |
|---|---|---|---|
| `stash@{0}` | `fe6c74c50e7cb55628e3276318a2e6b5bf83b578` | `compaction.py`, `sessions.py`, `telegram_bot.py`, `video_vision.py`, `main.py`, `aux_engine.py` | Các module compaction, session handover, telegram video đã được nhánh hiện tại tích hợp độc lập hoặc có module chuyên trách mới hơn. Riêng `main.py` và `aux_engine.py` chứa mã cũ xung đột với kiến trúc dual-brain hiện hành nên được giữ nguyên trong stash để tránh hạ cấp hệ thống. |
| `stash@{1}` | `7e9c2ec683ed99f777ac8b6dedc305fd797f0675` | `codex_models.py`, `team_runner.py`, `team_store.py`, `workflow_graph.py`, `main.py` | Các cải tiến team/workflow đã có sẵn trên nhánh hiện tại; `main.py` xung đột đã được tách riêng. Không áp đè để tránh mất code mới. |
| `stash@{2}` | Bản lưu trước đó | `codex_models.py`, `workflow_graph.py`, `main.py` | Tương tự stash@{1}, các tính năng cốt lõi đã có trên nhánh `feat/ai-company-reliability-local-20261119`. |

Bản sao lưu diff đầy đủ được lưu tại:
- `stash-0.patch` và `stash-0-conflicts.diff`
- `stash-1.patch` và `stash-1-main.diff`
- `hunk-inventory.json` và `hunk-inventory.md`

---

## 3. Kiến trúc cơ chế bảo toàn cập nhật (`server/update_preservation.py` & `server/updater.py`)

- **Bước 1 (Trước khi Stash):** Khi `updater.stash_local_changes()` phát hiện cây làm việc có thay đổi, hệ thống gọi `update_preservation.create_snapshot(ROOT, STATE_DIR)` để tạo snapshot dữ liệu ngoài cây mã nguồn (trong thư mục `STATE_DIR/update-preservation/<timestamp>-<pid>/`), tính hash SHA-256 từng file, lưu base blob từ HEAD và loại trừ các file runtime (`engine_down_notified.json`, `mcp-stdio-pids.json`) cũng như file nhạy cảm.
- **Bước 2 (Liên kết OID):** Sau khi `git stash push` thành công, OID của stash được gán vào `manifest.json` của snapshot qua `bind_snapshot(snapshot, stash_oid)`.
- **Bước 3 (Khôi phục 3 chiều - 3-Way Merge):** Khi `updater.restore_local_changes(stash_oid)` chạy:
  - Tìm snapshot tương ứng qua `find_snapshot(STATE_DIR, stash_oid)`.
  - Thực thi `update_preservation.restore_snapshot(ROOT, snapshot)`: thực hiện merge 3 chiều (`git merge-file -p --diff3`) giữa bản gốc HEAD cũ, bản sửa của người dùng, và bản phát hành mới.
  - **Trường hợp không xung đột:** Cả tính năng mới của release và tinh chỉnh của người dùng đều được ghi nhận đầy đủ vào file.
  - **Trường hợp xung đột:** Toàn bộ giao dịch bị hủy bỏ (atomic rollback), khôi phục nguyên vẹn file của release mới, tạo báo cáo xung đột `restore-report.json` và giữ nguyên bản sao trong `git stash` để người dùng chủ động xử lý, không bao giờ tự ý xóa hoặc làm mất mã.

---

## 4. Bằng chứng kiểm chứng thực tế

```bash
# 1. Kiểm thử module bảo toàn cập nhật
python tests/python/test_update_preservation.py
# Output:
# PASS: update preservation non-conflict, conflict report, new-release retention, transaction rollback
# PASS: update preservation scope, add/delete, integrity, runtime exclusion, and protected paths

# 2. Kiểm thử tích hợp updater với git stash thực tế
python tests/python/test_updater_stash.py
# Output:
# TẤT CẢ PASS: updater stash an toàn khi khôi phục xung đột và rollback
```
