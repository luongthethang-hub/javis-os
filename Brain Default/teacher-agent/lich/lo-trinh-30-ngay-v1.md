# Lộ trình 30 ngày - Teacher Agent huấn luyện CAM và 9 model (v1.0.0)

- **Ràng buộc xuyên suốt (`luat-huan-luyen-vien.md` mục 7):** Mọi gói việc có `tieu_chi_nghiem_thu` chốt trước khi giao; code phải chạy test/lint thật kèm lệnh + kết quả E1; người kiểm bắt buộc **khác hãng** với người làm; mọi lỗi ghi vào `bai-hoc.jsonl` và sinh golden test; sản phẩm xong gửi chủ bản đánh giá theo `khung/mau/nghiem-thu.md`. Số chưa đo gắn nhãn `E0`. HLV không tự sửa code; ca cứu hộ chuyển Doctor Agent.
- **Đội 9 model theo hãng:**
  - **Anthropic:** Opus 5.5, Sonnet 5.5, Sonnet 4.6 (Opus chỉ vào D4–D5, ranh giới và chẩn đoán code; không chấm học viên Anthropic).
  - **OpenAI:** Codex GPT-6.2, Luna GPT-6, Sol GPT-5.6.
  - **xAI:** Grok 4.7.
  - **Google:** Antigravity Gemini 3.8.
  - **DeepSeek:** DeepSeek V4.1-Flash.

---

## Tuần 1 (Ngày 1–7) — Dựng nền & Chẩn đoán 9 model + CAM

**Mục tiêu đo được (E0 chờ chạy):**
- 9/9 model (gồm Opus 5.5) có điểm chẩn đoán E1 trên bộ 20 câu chung + 6 bài code chấm tự động, lưu vào `hoc-vien/hv-001-cam/thanh-vien.jsonl`.
- Bảng chẩn đoán chất lượng code đủ 9 model × 4 cột: `% qua test`, `% sửa ngoài phạm vi`, `số vòng sửa`, `thời gian tới xanh`.
- 100% gói giao ra có tiêu chí nghiệm thu trước khi chạy; CAM OS có 3 chỉ số nền (`lỗi kết nối/ngày`, `tỷ lệ health 200`, `số lần chủ can thiệp/tuần`).

**Kế hoạch theo ngày (Làm → Kiểm khác hãng → Đầu ra):**
- **Ngày 1–2:** Khóa bộ file nền `evolution/kiem-tra-schema.py` và ngân hàng 20 golden test. Làm: `Antigravity` · Kiểm: `Luna` (OpenAI) · Đầu ra: pass exit `0/1` + JSONL hợp lệ.
- **Ngày 3–4:** Chẩn đoán chất lượng code 9/9 model (6 bài D1–D4 gồm kiểm tra sửa ngoài phạm vi & test đỏ). Làm nhóm OpenAI/xAI/Google/DeepSeek: `Opus 5.5` chấm; Làm nhóm Anthropic (`Opus 5.5`, `Sonnet 5.5`, `Sonnet 4.6`): `Codex GPT-6.2` + `Grok 4.7` chấm · Đầu ra: bảng 9×4 + `thanh-vien.jsonl`.
- **Ngày 5–6:** Đo 3 chỉ số nền CAM OS và lập hồ sơ bệnh án R1 cho lỗi lặp. Làm: `DeepSeek V4.1-Flash` gom log · Kiểm: `Sonnet 5.5` (Anthropic) · Đầu ra: `benh-an/cam-baseline.md`.
- **Ngày 7 (Điểm chạm Chủ #1 & #2 — gom lô + nghiệm thu Tuần 1):** Chủ duyệt bảng chẩn đoán 9 model và danh sách lỗi ưu tiên Tuần 2 (`<= 2` chạm/tuần).

---

## Tuần 2 (Ngày 8–14) — Giáo án & Luyện theo lỗ hổng

**Mục tiêu đo được:**
- Mỗi model yếu ở mục nào có tối thiểu 1 adapter T2 (CUP) và 3 bài luyện nhắm đúng lỗi thực tế từ `bai-hoc.jsonl`.
- Tỷ lệ sửa ngoài phạm vi gói giảm xuống `<= 5%`; 0 ca nộp code thiếu log test.

**Kế hoạch theo ngày:**
- **Ngày 8–9:** Soạn giáo án phân bậc D1–D5 theo từng nhóm lỗi. Làm: `Sonnet 5.5` (Anthropic) · Kiểm: `Luna` (OpenAI) · Đầu ra: `khung/giao-an-tuan2.md`.
- **Ngày 10–11:** Viết bản vá adapter T2 cho các model có điểm code `< 85%`. Làm: `Antigravity` (Google) · Kiểm: `Sol` (OpenAI) · Đầu ra: hồ sơ CUP T2 kèm diff.
- **Ngày 12–13:** Luyện thực chiến trên repo mẫu cô lập (2 vòng, ghi lỗi vào `bai-hoc.jsonl`). Làm: `Codex` + `Sol` + `DeepSeek` · Kiểm: `Grok 4.7` (xAI) + `Sonnet 4.6` (Anthropic) · Đầu ra: log luyện + golden test sinh mới.
- **Ngày 14 (Điểm chạm Chủ #1 — nghiệm thu Tuần 2):** Chủ duyệt gói CUP T2 đạt chuẩn trước khi đưa vào Shadow Test (`1` chạm/tuần).

---

## Tuần 3 (Ngày 15–21) — Chấm chính thức, Shadow Test & Tốt nghiệp CAM

**Mục tiêu đo được:**
- Đạt ngưỡng tốt nghiệp: `>= 90%` điểm tổng và **100% câu ranh giới** (`GT-01..GT-08`).
- Shadow Test đối chứng baseline vs bản cải tiến trên mẫu thật cô lập không làm tăng lỗi hoặc vượt trần token.

**Kế hoạch theo ngày:**
- **Ngày 15–16:** Chạy chấm chính thức bộ golden test (kể cả câu mới sinh ở Tuần 2). Làm: `Sol` (OpenAI) · Kiểm: `Opus 5.5` (Anthropic, chỉ chấm nhóm ngoài Anthropic) & `Grok 4.7` (xAI, chấm nhóm Anthropic) · Đầu ra: `bang-diem/tuan3.md`.
- **Ngày 17–18:** Chạy Shadow Test cho adapter T2 của CAM và Javis. Làm: `Antigravity` (Google) · Kiểm: `Luna` (OpenAI) · Đầu ra: báo cáo delta chất lượng & token.
- **Ngày 19–20:** Tổng hợp hồ sơ tốt nghiệp CAM và khóa bản `v1.0.0` (chưa mở rộng nếu thiếu 100% ranh giới). Làm: `DeepSeek V4.1-Flash` · Kiểm: `Sonnet 5.5` (Anthropic) · Đầu ra: hồ sơ tốt nghiệp.
- **Ngày 21 (Điểm chạm Chủ #1 — nghiệm thu Tuần 3):** Chủ ký duyệt tốt nghiệp CAM hoặc yêu cầu vá lại (`1` chạm/tuần).

---

## Tuần 4 (Ngày 22–30) — Diễn tập Cứu hộ & Tiếp nhận Học viên thứ 2

**Mục tiêu đo được:**
- 5/5 kịch bản cứu hộ (G5) đạt `7/7` bước R0–R6 trên môi trường mock, `0` vượt quyền.
- Tiếp nhận thành công học viên thứ 2 (`hv-002-javis` hoặc `hv-002-social`) qua đủ quy trình `khung/quy-trinh-tiep-nhan.md`.

**Kế hoạch theo ngày:**
- **Ngày 22–24:** Diễn tập 5 kịch bản cứu hộ (lặp tool, checkpoint hỏng, vỡ cache, prompt injection email, model đổi schema). Làm: `Doctor Agent` (`Sol` + `Sonnet 4.6`) · Kiểm: `Grok 4.7` (xAI) + `Antigravity` (Google) · Đầu ra: 5 biên bản chấm R0–R6.
- **Ngày 25–27:** Tiếp nhận và chẩn đoán đầu vào học viên thứ 2 bằng quy trình đã chuẩn hóa. Làm: `Luna` (OpenAI) · Kiểm: `Sonnet 5.5` (Anthropic) · Đầu ra: `hoc-vien/hv-002/ho-so.yaml` + `bang-diem/hv-002-dau-vao.md`.
- **Ngày 28–29:** Kiểm toán tổng kết 30 ngày, đối chiếu `CHANGELOG.md`, `bai-hoc.jsonl`, đề xuất lộ trình tháng 2. Làm: `DeepSeek V4.1-Flash` · Kiểm: `Opus 5.5` (Anthropic) · Đầu ra: báo cáo tổng kết 1 trang.
- **Ngày 30 (Điểm chạm Chủ #1 — nghiệm thu cuối tháng):** Chủ nghiệm thu tổng thể 30 ngày và duyệt kế hoạch mở rộng (`1` chạm/tuần).

---

## 6 Việc định kỳ đề xuất (chưa tự bật lịch)

1. **Quét schema & bí mật hằng ngày** · Nhịp: `08:00 hằng ngày` · Model: `Script Python (0 token)` · Nạp: danh sách file sửa trong 24h từ `vet/state.json` · Ghi: kết quả pass/fail và mốc thời gian mới vào `vet/state.json`.
2. **Gom bài học & sinh golden test** · Nhịp: `21:00 thứ 3 & thứ 6` · Model: `DeepSeek V4.1-Flash` (Kiểm: `Sonnet 4.6`) · Nạp: dòng mới từ `bai-hoc.jsonl` sau `last_lesson_id` · Ghi: cập nhật `last_lesson_id` và danh sách test chờ duyệt.
3. **Đo sức khỏe 9 model & tỷ lệ lỗi 400** · Nhịp: `mỗi 12 giờ` · Model: `Script + Sol` · Nạp: con trỏ dòng cuối `javis.log` trong `vet/health_cursor.json` · Ghi: chỉ số lỗi và con trỏ dòng mới vào `vet/health_cursor.json`.
4. **Kiểm tra gói kẹt Kanban & Hàng chờ** · Nhịp: `mỗi 4 giờ` · Model: `Antigravity / Script` · Nạp: `kanban.json` + `hang-cho.sqlite` từ `vet/queue_cursor.json` · Ghi: danh sách gói kẹt > 60 phút vào `vet/queue_cursor.json` (chỉ báo khi có ngoại lệ).
5. **Đối soát chéo điểm KPI tuần** · Nhịp: `19:00 Chủ nhật` · Model: `Luna` (Kiểm: `Grok 4.7`) · Nạp: `kpi.csv` + `bang-diem/` tuần hiện tại từ `vet/weekly_state.json` · Ghi: bản nháp báo cáo 1 trang và cập nhật `last_week_closed`.
6. **Diễn tập nhanh 1 ca ranh giới ngẫu nhiên** · Nhịp: `10:00 thứ 5 hằng tuần` · Model: `Grok 4.7` · Nạp: lịch sử ca đã diễn tập trong `vet/drill_state.json` · Ghi: kết quả pass/fail và xoay vòng sang ca kế tiếp trong `vet/drill_state.json`.
