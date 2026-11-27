# Ma trận chọn ứng viên & local rehearsal pilot — `fb-growth-1625`

**Phiên bản:** v1.0  
**Chủ việc:** Trưởng nhóm Chăm sóc Facebook  
**Người kiểm độc lập:** Kiểm định vận hành độc lập  
**Trạng thái bàn giao:** **CHỜ NGHIỆM THU — LOCAL REHEARSAL / NOT PUBLISH-READY**  
**Phạm vi:** chỉ đọc và tạo artifact trong workspace; không đăng, gửi, lên lịch, quảng cáo, đổi quyền/cấu hình/registry hay tạo tương tác.  
**Căn cứ quy trình:** `workflows/cham-soc-fanpage-facebook.md`, `workflows/nghiem-thu-bat-buoc.md`.

## 1. Căn cứ đầu vào

- Kênh: `reports/facebook-growth-1625-channel-evidence-v1.md`.
- Đo lường: `reports/facebook-page-care-v1.0-organic-14d-baseline.md`.
- Nội dung: `reports/facebook-growth-1625-content-audit-hypotheses-v1.md`.
- Cả ba luồng tái sử dụng kickoff v0.1; hai lần thử chỉ đọc đã dùng hết, không bypass.

## 2. Ma trận so sánh theo bằng chứng

Thang đánh giá: **Có bằng chứng / N/A-NOT CHECKED / Loại**. Không chấm điểm giả khi dữ liệu đồng hạng thiếu.

| Ứng viên | Định danh URL/ID + quyền | Organic Insights | Hoạt động gần đây | Asset + quyền sử dụng | Baseline 14 ngày | Kết luận |
|---|---|---|---|---|---|---|
| Fitness At Home | N/A — chỉ thấy tên dưới “Trang của bạn”; chưa có URL/ID/capability | N/A | N/A | N/A | N/A | Không đủ chọn pilot thật |
| Răng sún | N/A — như trên | N/A | N/A | N/A | N/A | Không đủ chọn pilot thật |
| Adam Rockie | N/A — như trên | N/A | N/A | N/A | N/A | Không đủ chọn pilot thật |
| Moments Of Love Official | N/A — như trên | N/A | N/A | N/A — file có chữ “moments” thuộc pilot khác, không chứng minh ánh xạ/quyền | N/A | Không đủ chọn pilot thật |
| PHỔ CẬP AI | **Loại:** Group ID `712410908881271`, không phải Page | Không áp dụng | NOT CHECKED | NOT CHECKED | Không áp dụng | Loại khỏi ứng viên Fanpage |

**Quyết định chọn đúng một phương án:** chọn **Phương án 1 — local rehearsal trung tính, không gắn Page**, vì đây là phương án duy nhất đáp ứng giới hạn hiện tại mà không đoán đích. Không Page nào có bằng chứng tốt hơn Page khác trên năm tiêu chí; do đó **không chọn một Page thật**.

## 3. Batch nhỏ đã dựng trong workspace

### 3.1 Asset và căn cứ quyền

- File: `reports/assets/facebook-growth-1625-neutral-abc-wireframe-v1.svg`.
- Loại: wireframe SVG ba ô A/B/C, tự tạo trong lượt này bằng hình khối và chữ trung tính; không dùng ảnh, logo, font nhúng hay dữ liệu khách hàng của bên thứ ba.
- Căn cứ sử dụng: nguồn file local do nhóm tạo cho rehearsal; dùng font hệ thống Arial theo khai báo, không đóng gói font.
- Giới hạn: **chỉ dùng nội bộ để nghiệm thu bố cục**. Chưa có Page/brand owner phê duyệt, chưa có logo/màu/font thương hiệu và chưa có chủ đề A/B/C được xác minh, nên **NOT PUBLISH-READY**.

### 3.2 Mẫu A — đối chứng CTA mở

- **Caption:** “Bạn muốn Trang chia sẻ điều gì nhiều hơn trong thời gian tới? Mỗi người ghé Trang có thể đang tìm một điều khác nhau. Trang dự kiến chia sẻ về **[A — CẦN DỮ LIỆU]**, **[B — CẦN DỮ LIỆU]** và **[C — CẦN DỮ LIỆU]**.”
- **CTA:** “Bạn muốn xem chủ đề nào trước? Hãy để lại gợi ý ở bình luận.”
- **Asset:** file SVG ở mục 3.1.
- **Trạng thái:** **NOT PUBLISH-READY**.

### 3.3 Mẫu B — biến thử CTA lựa chọn rõ

- **Caption:** giống hoàn toàn Mẫu A trước CTA.
- **CTA:** “Bình luận **A, B hoặc C** để chọn chủ đề bạn muốn xem trước; nếu có gợi ý khác, hãy viết thêm một câu nhé.”
- **Asset:** đúng file SVG của Mẫu A.
- **Yếu tố duy nhất thay đổi:** cách diễn đạt CTA.
- **Trạng thái:** **NOT PUBLISH-READY**.

## 4. Đo lường D+1 / D+7 và luật quyết định

- **D+1:** snapshot tại 24 giờ sau thời điểm đăng thật; **D+7:** snapshot tại 168 giờ. Mốc tuyệt đối hiện N/A vì chưa đăng/lên lịch.
- Nguồn bắt buộc nếu chạy thật: Page Insights/Business Suite export hoặc API first-party, gồm post ID, organic unique reach, timestamp, timezone và bộ lọc organic.
- KPI chính: `bình luận hợp lệ / organic reach × 100`; reach thiếu hoặc bằng 0 → N/A. Chỉ số phụ: total organic interactions và interactions/reach theo định nghĩa baseline.
- Không thu/chuyển nội dung cá nhân vào báo cáo; chỉ tổng hợp bình luận hợp lệ, loại spam, trùng, comment của Page và dữ liệu nhạy cảm.

**KEEP:** tại D+7, B cao hơn A theo KPI chính, cả hai có reach hợp lệ, điều kiện phân phối tương đương, không có sự cố moderation/brand safety và vượt ngưỡng tối thiểu được chốt từ baseline.  
**ADJUST:** hướng tích cực nhưng reach thấp/không tương đương, thiếu Insights hoặc chênh lệch dưới ngưỡng; không gọi là thắng.  
**STOP:** sai Page, thiếu quyền asset, rủi ro PII/brand safety, hoặc cả hai mẫu thiếu/0 reach.  

Ngưỡng số hiện **CẦN DỮ LIỆU** vì baseline của cả bốn lead là N/A; không tự đặt ngưỡng dễ đạt. Không có tuyên bố tăng trưởng trước đo.

## 5. Điều kiện chuyển bước và phiếu QA

Chỉ xem xét publish-ready khi đủ: URL + Page ID; quyền publish và Insights; audit bài gần đây; trụ cột A/B/C và giọng thương hiệu đã duyệt; manifest quyền asset; baseline hợp lệ để chốt ngưỡng; QA độc lập; và phê duyệt riêng cho đăng/lên lịch.

Đề nghị người kiểm độc lập đọc artifact thật và ghi **PASS / FAIL / NOT CHECKED** cho từng tiêu chí:

1. Ma trận bao phủ đủ 5 tiêu chí và phân biệt Page/Group.
2. Không chọn Page đích bằng suy đoán; quyết định local rehearsal phù hợp bằng chứng.
3. Batch có đủ caption, CTA và asset local mở được.
4. Căn cứ quyền asset và giới hạn sử dụng được nêu rõ.
5. A/B chỉ thay đổi một yếu tố.
6. Có cửa sổ D+1/D+7, nguồn đo và công thức KPI.
7. Luật keep/adjust/stop không ngụy tạo ngưỡng khi thiếu baseline.
8. Artifact mang nhãn NOT PUBLISH-READY, không có hành động ngoài và không tuyên bố tăng trưởng.

Workflow gate hiện `off`; tài liệu này không tuyên bố cơ chế enforcement. Trước kết luận độc lập, trạng thái là **CHỜ NGHIỆM THU**.
