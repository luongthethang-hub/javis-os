# Audit nội dung & giả thuyết thử nghiệm organic v1 — `fb-growth-1625`

**Phiên bản:** v1.0  
**Trạng thái:** **LOCAL DRY RUN / NOT PUBLISH-READY / CHỜ DUYỆT**  
**Phạm vi:** Chỉ phân tích và soạn nháp trong workspace; không đăng, gửi, lên lịch, dùng dữ liệu khách hàng hay tạo tương tác nhân tạo.  
**Nguồn tái sử dụng:**
- `reports/facebook-page-care-v0.1-content-calendar.md`
- `reports/facebook-page-care-v0.1-response-templates.md`
- `reports/facebook-growth-1625-channel-evidence-v1.md`
- `reports/facebook-page-care-v1.0-organic-14d-baseline.md`

## 1. Kết quả audit bài gần đây

| Trường kiểm | Kết quả | Căn cứ |
|---|---|---|
| Page đích | **N/A / NOT CHECKED** | Bốn tên Fitness At Home, Răng sún, Adam Rockie và Moments Of Love Official mới xuất hiện dưới “Trang của bạn”; chưa có URL/ID Page riêng. |
| Danh sách bài gần đây | **N/A / NOT CHECKED** | Không có Page node/URL đã xác minh để đọc đúng feed; không dùng link Business Suite chung để suy đoán. |
| Hoạt động/tần suất đăng | **N/A / NOT CHECKED** | Không có bài nguồn first-party đã định danh. |
| Hook, chủ đề, định dạng, CTA từng bài | **N/A / NOT CHECKED** | Không có post URL/ID hoặc nội dung bài đã xác minh. |
| Tương tác/reach bài | **N/A / NOT CHECKED** | Không có Insights; không coi dữ liệu thiếu là 0. |
| Quyền tài sản bài gần đây | **N/A / NOT CHECKED** | Không có manifest/nguồn/quyền asset ánh xạ tới Page. Hai tệp `moments.md` thuộc pilot khác không chứng minh quyền dùng cho Moments Of Love Official. |

**Kết luận audit:** Không đủ bằng chứng để nhận xét hiệu quả, chọn bài thắng hoặc đề xuất tối ưu riêng cho bất kỳ Page nào. Đã dùng lại kết quả hai lần thử chỉ đọc của luồng Kênh/Đo lường; phần Nội dung không thực hiện thêm lượt truy cập hay bypass. PHỔ CẬP AI là Group ID `712410908881271`, bị loại khỏi audit Fanpage.

## 2. Local rehearsal: cặp giả thuyết chỉ thay đổi một yếu tố

### 2.1 Thiết kế chung

- **Mục tiêu học:** kiểm tra cách diễn đạt CTA nào tạo tỷ lệ bình luận hữu ích cao hơn cho bài hỏi nhu cầu nội dung.
- **Mẫu tái sử dụng:** Ngày 1 — “Làm quen với cộng đồng” trong lịch 7 ngày v0.1; không làm lại lịch.
- **Yếu tố duy nhất thay đổi:** CTA cuối caption — CTA mở so với CTA có lựa chọn A/B/C.
- **Giữ nguyên giữa hai mẫu:** Page đích, thời điểm đăng, caption trước CTA, hook, ảnh, định dạng, kích thước/placement, chủ đề A/B/C, audience organic, thời lượng đo, quy tắc moderation và việc không boost.
- **Giả định:** Khi đã có Page hợp lệ, ba chủ đề A/B/C là trụ cột đã được thương hiệu duyệt và đủ khác nhau để người đọc lựa chọn; Page có khả năng phản hồi bình luận theo mẫu v0.1. Hiện các giả định này đều **CẦN DỮ LIỆU**.
- **Cách so sánh hợp lệ khi chạy thật:** hai bài phải được phân phối trong điều kiện tương đương; không đăng đồng thời cùng một Page nếu gây trùng lặp. Leader/đo lường phải chốt thiết kế thời điểm hoặc vòng lặp phù hợp dựa trên baseline. Không được tuyên bố quan hệ nhân quả nếu reach, thời điểm hay audience không tương đương.

### 2.2 Mẫu A — Đối chứng: CTA mở

- **Hook:** “Bạn muốn Trang chia sẻ điều gì nhiều hơn trong thời gian tới?”
- **Caption nháp:**  
  “Mỗi người ghé Trang có thể đang tìm một điều khác nhau. Trong thời gian tới, Trang dự kiến chia sẻ về **[A — CẦN DỮ LIỆU]**, **[B — CẦN DỮ LIỆU]** và **[C — CẦN DỮ LIỆU]**.”
- **CTA đối chứng:** “Bạn muốn xem chủ đề nào trước? Hãy để lại gợi ý ở bình luận.”
- **Định dạng:** 01 ảnh tĩnh, bố cục ba ô A/B/C.
- **Tài sản:** `[CẦN DỮ LIỆU: logo, màu, font, file nguồn, chủ sở hữu, loại giấy phép/phạm vi sử dụng, người duyệt]`.
- **Trạng thái:** **NOT PUBLISH-READY**.

### 2.3 Mẫu B — Biến thử: CTA lựa chọn rõ

- **Hook:** Giống hệt Mẫu A.
- **Caption nháp:** Giống hệt phần caption trước CTA của Mẫu A.
- **CTA biến thử:** “Bình luận **A, B hoặc C** để chọn chủ đề bạn muốn xem trước; nếu có gợi ý khác, hãy viết thêm một câu nhé.”
- **Định dạng:** Giống hệt Mẫu A — 01 ảnh tĩnh, cùng một file ảnh ba ô A/B/C.
- **Tài sản:** Dùng đúng tài sản của Mẫu A; các trường quyền vẫn **CẦN DỮ LIỆU**.
- **Trạng thái:** **NOT PUBLISH-READY**.

### 2.4 Giả thuyết có thể bác bỏ

- **H0:** CTA lựa chọn rõ không làm tăng tỷ lệ bình luận hợp lệ trên reach so với CTA mở.
- **H1:** CTA lựa chọn rõ làm tăng tỷ lệ bình luận hợp lệ trên reach so với CTA mở, vì giảm công sức quyết định và giúp người đọc biết chính xác cách phản hồi.
- **Không dùng làm kết luận chính:** tổng reaction, cảm nhận chủ quan hay số comment thô khi reach khác nhau.

## 3. Đo D+1 và D+7

**Mốc thời gian:** D+1 = 24 giờ và D+7 = 168 giờ kể từ thời điểm từng bài được đăng thật; dùng cùng timezone của Page/export và ghi timestamp chính xác. Hiện chưa có lịch đăng nên mốc tuyệt đối là **CẦN DỮ LIỆU**.

| Chỉ số | Công thức / cách ghi | D+1 | D+7 |
|---|---|---|---|
| Organic reach | Trường organic unique reach ở cấp bài; không dùng impressions thay thế | Ghi snapshot | Ghi snapshot cuối cửa sổ |
| Bình luận hợp lệ | Comment của người dùng trả lời chủ đề/đưa gợi ý; loại spam, comment của Page, trùng lặp và dữ liệu nhạy cảm khỏi tập phân tích, không chép nội dung cá nhân vào báo cáo | Đếm theo quy tắc cố định | Đếm lũy kế theo cùng quy tắc |
| Tỷ lệ bình luận hợp lệ / reach | `bình luận hợp lệ ÷ organic reach × 100` | KPI chính; reach thiếu/0 → N/A | KPI chính; reach thiếu/0 → N/A |
| Total organic interactions | `organic reactions + comments + shares + saves`; thành phần thiếu ghi N/A hoặc công bố công thức rút gọn | Chỉ số phụ | Chỉ số phụ |
| Organic interactions / reach | `total organic interactions ÷ organic reach × 100`; tử/mẫu phải cùng cấp và cùng phạm vi | Chỉ số phụ | Chỉ số phụ |
| Tín hiệu định tính | Tỷ trọng lựa chọn A/B/C và nhóm gợi ý khác, chỉ báo cáo tổng hợp không PII | Ghi sơ bộ | Mã hóa/tổng hợp cuối |

**Nguồn bắt buộc khi chạy thật:** Page Insights/Meta Business Suite export hoặc API first-party có post ID, bộ lọc organic, timezone và extraction timestamp. Không gộp paid; thiếu trường ghi **N/A**, không ghi 0.

## 4. Quy tắc keep / adjust / stop cho pilot tương lai

Chỉ áp dụng sau khi Page, bài, quyền asset và dữ liệu đo đã được xác minh; ngưỡng số tuyệt đối cần leader/đo lường chốt từ baseline nên hiện là **CẦN DỮ LIỆU**.

- **KEEP biến thử:** tại D+7, Mẫu B có tỷ lệ bình luận hợp lệ/reach cao hơn Mẫu A, cả hai có reach hợp lệ, không có sự cố moderation/brand safety, và chênh lệch đạt `[CẦN DỮ LIỆU: ngưỡng tối thiểu]`.
- **ADJUST / thử lại:** hướng chênh lệch tích cực nhưng reach quá thấp, điều kiện phân phối không tương đương, thiếu trường Insights, hoặc chênh lệch dưới ngưỡng. Không gọi là thắng.
- **STOP:** phát hiện sai Page, thiếu quyền tài sản/nguồn nội dung, rủi ro dữ liệu cá nhân/brand safety, reach bằng 0/không khả dụng ở cả hai mẫu, hoặc CTA tạo lượng spam/dữ liệu nhạy cảm vượt `[CẦN DỮ LIỆU: ngưỡng vận hành]`.
- **Không tuyên bố tăng trưởng:** đây là thiết kế rehearsal, chưa có xuất bản hay phép đo.

## 5. Vận hành bình luận nếu được duyệt chạy thật

Tái sử dụng `response-templates.md` v0.1:
- Câu hỏi chung → Mẫu 1 FAQ, chỉ trả lời bằng nguồn xác minh.
- Phản hồi tiêu cực/khiếu nại → Mẫu 2, không tranh luận hay hứa SLA/chính sách chưa duyệt.
- Dữ liệu nhạy cảm/cần người thật → Mẫu 3; không nhắc lại dữ liệu, chuyển kênh riêng đã xác minh.
- Giá, lịch, chính sách, SLA, bộ phận nhận và kênh riêng chưa xác nhận đều giữ **CẦN DỮ LIỆU**. Không phản hồi thật trong rehearsal.

## 6. Điều kiện để chuyển thành publish-ready

- [ ] Xác minh Page URL + ID + quyền publish/Insights; không dùng Group hoặc link Business Suite chung.
- [ ] Audit được bài gần đây từ đúng Page và ghi post URL/ID, cửa sổ, định dạng, CTA, chỉ số nguồn.
- [ ] Điền A/B/C từ trụ cột thương hiệu đã duyệt.
- [ ] Có asset manifest chứng minh quyền dùng logo/font/ảnh và người phê duyệt.
- [ ] Chốt giọng thương hiệu, lịch đăng và điều kiện phân phối tương đương.
- [ ] Chốt ngưỡng keep/adjust/stop dựa trên baseline hợp lệ.
- [ ] QA độc lập kiểm artifact và ghi PASS/FAIL/NOT CHECKED từng tiêu chí.
- [ ] Có phê duyệt riêng trước mọi đăng/lên lịch hoặc phản hồi thật.

## 7. Tự đánh giá bài thực hành vai Nội dung

- Audit chỉ dùng Page/nguồn xác minh: **NOT CHECKED** vì chưa có Page URL/ID hoặc bài xác minh; không suy đoán.
- Xử lý edge case Page/Group: **ĐẠT ở mức artifact** — loại PHỔ CẬP AI khỏi Fanpage pilot theo bằng chứng URL Group; chờ QA độc lập kết luận.
- Hai giả thuyết so sánh chỉ đổi một yếu tố: **ĐÃ SOẠN**, yếu tố là CTA; chờ QA độc lập.
- Có đối chứng, biến thử, CTA, định dạng, giả định, quyền tài sản, D+1/D+7: **ĐÃ GHI**, nhưng asset và dữ liệu Page vẫn **CẦN DỮ LIỆU**.
- Publish-ready: **KHÔNG**.

**Bàn giao:** v1.0 — **CHỜ NGHIỆM THU ĐỘC LẬP**. Artifact không tự tuyên bố PASS và không coi workflow gate đang enforce.