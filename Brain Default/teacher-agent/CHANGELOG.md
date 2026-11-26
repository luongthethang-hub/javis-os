# CHANGELOG — khung Teacher

MAJOR = T0/T1 · MINOR = T2 · PATCH = T3. Mỗi mục: ngày · CUP · tầng · tóm tắt · golden test thêm · người duyệt · đường lùi.

## v0.1.1 — 2026-11-26 (L0 duyệt lô A kèm 4 sửa; chờ L0 xem trước khi bật task)
- (1) Đội: thêm `khung/hoi-dong-cham.md` (đội Javis + Ollama, ma trận ghép khác hãng), `adapters/javis.md`, `adapters/ollama.md`. Ngân sách: code → Ollama → Javis → API trả phí; Opus chỉ D4-D5 + ranh giới; trần 150 USD, báo L0 khi vượt 20 USD.
- (2) Luật HLV mục 7 "Cổng chất lượng và rút kinh nghiệm"; nhóm chấm "chất lượng code" là cổng nhị phân; sổ bài học dùng chung `teacher-agent/bai-hoc.jsonl`; mẫu `khung/mau/nghiem-thu.md`.
- (3) Doctor Agent là nơi duy nhất sửa code; HLV duyệt phác đồ + chấm; ST-4 chuyển ca cho Doctor; CAM vào trạng thái cứu hộ (Doctor R1).
- (4) Bỏ mọi cặp chấm cùng hãng: Opus được chấm bởi Codex/Grok/DeepSeek; Haiku/Sonnet không do Opus chấm; Antigravity tính là họ Google.
- Golden test thêm: GT-CODE-001…003, GT-PHOIHOP-001…002, GT-CAMOS-001…002, GH-007…009; sửa GH-006.
- Bổ sung (26/11, theo L0): vùng cấm dự án "CLAUDE - Darklord" trong luật HLV mục 3 và phần chung của mọi scheduled task.
- Kho: chuyển sang vault Javis `teacher-agent/` (có git; commit do L0/Javis chạy).
- Đường lùi: nội dung v0.1.0 còn trong tài liệu kế hoạch v0.1.0 (Claude Doc) và mục v0.1.0 dưới đây; từ v0.1.1 lùi bằng git tag trong vault.

## v0.1.0 — 2026-11-25 (DESIGNED, chờ L0 duyệt)
- CUP-0001 khởi tạo khung đa hệ
- T1: luật HLV tách khỏi luật học viên; sàn an toàn chung; chuẩn chấm 3 lớp đề
- T2: H0-H7, R0-R6, quy trình tiếp nhận (T1-T7), cứu hộ hệ lạ (R-1-R6), mẫu hồ sơ/CUP/bệnh án/KPI
- T3: sổ adapter 13 nền tảng (3 điền sẵn: claude, deepseek, antigravity — chưa gọi thử)
- Golden test: GL-001…011 (sàn), GH-001…006 (HLV), CAM-* 7 câu (học viên thí điểm)
- Học viên: hv-001-cam (H0)
- Người duyệt: chờ L0 · Đường lùi: không có bản cha
