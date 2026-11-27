# Facebook Page Care — Bộ KPI đo lường v0.1

**Trạng thái:** CHƯA CÓ BASELINE — CHỜ NGHIỆM THU ĐỘC LẬP  
**Phạm vi:** Định nghĩa đo lường cho Facebook Page; không áp dụng cho Facebook Group, quảng cáo ngoài phạm vi hay dữ liệu khách hàng sao chép. Không đăng/gửi, không đổi quảng cáo hoặc cấu hình.  
**Đơn vị báo cáo bắt buộc:** từng Page đã xác minh bằng Page ID + URL; khoảng ngày; múi giờ IANA (đề xuất `Asia/Ho_Chi_Minh`, UTC+07:00, nhưng phải xác nhận trước khi chạy); nguồn và thời điểm trích xuất.

## 1. Quy tắc dữ liệu

1. **Không gộp kênh:** mỗi dòng kết quả thuộc đúng một Page ID. PHỔ CẬP AI (Group ID `712410908881271`) là Group, không đưa vào bộ số Page.
2. **Không trộn organic và quảng cáo:** báo riêng `organic`, `paid`; chỉ thêm `total` nếu nguồn cung cấp tổng không trùng lặp hoặc có cách khử trùng lặp được chứng minh. Không cộng organic reach với paid reach để suy ra unique total reach.
3. **Khóa cửa sổ đo:** tuần lịch từ 00:00 thứ Hai đến trước 00:00 thứ Hai kế tiếp theo múi giờ đã chốt. Báo cáo tháng dùng tháng lịch cùng múi giờ. Khi so sánh, dùng cửa sổ có cùng độ dài và quy tắc.
4. **Khóa cohort nội dung:** KPI bài đăng dùng các bài **được xuất bản trong cửa sổ**; chụp số ở mốc cố định D+7 kể từ lúc đăng để bài cuối kỳ có thời gian tích lũy tương đương. Báo cáo vận hành nhanh có thể chụp cuối kỳ nhưng phải gắn nhãn “chưa trưởng thành”.
5. **Không trộn cấp dữ liệu:** số liệu cấp bài dùng cho KPI nội dung; số liệu cấp Page dùng cho tổng quan Page. Không cộng số unique giữa các bài để suy ra unique Page reach.
6. **Nguồn ưu tiên:** Meta Business Suite/Professional Dashboard export cho đúng Page và kỳ đo; hoặc Page Insights API khi Page đã kết nối và quyền đọc hợp lệ. Inbox dùng Meta Business Suite Inbox/export hoặc nguồn hội thoại chính thức có timestamp. Lưu tên trường đúng như bản export/API tại thời điểm trích vì Meta có thể đổi tên/khả dụng metric.
7. **Quảng cáo:** Ads Manager/export hoặc Marketing API theo Page ID/post ID, attribution setting và account timezone được ghi rõ. Không dùng số Ads để thay cho organic Insights. Chi phí/ROAS không thuộc v0.1.
8. **Kiểm soát chất lượng:** lưu file export gốc hoặc mã truy vấn, thời điểm trích, Page ID, bộ lọc, timezone, attribution (nếu paid) và công thức biến đổi; không lưu nội dung tin nhắn hay dữ liệu định danh khách trong báo cáo KPI.

## 2. KPI tương tác và reach

### KPI E1 — Tổng tương tác nội dung

- **Định nghĩa:** tổng hành động tương tác hợp lệ trên các bài thuộc cohort.
- **Công thức:** `Tổng tương tác = Reactions + Comments + Shares + Saves`.
- **Tử số/thành phần:** tổng từng cấu phần do Facebook trả về; báo kèm từng cấu phần, không chỉ báo tổng.
- **Mẫu số:** không có.
- **Đơn vị:** lượt tương tác.
- **Cửa sổ:** cohort bài xuất bản trong tuần/tháng; snapshot D+7. Tách `organic` và `paid` khi nguồn có breakdown đáng tin cậy; nếu một cấu phần không có breakdown thì ghi `KHÔNG TÁCH ĐƯỢC`, không phân bổ ước tính.
- **Nguồn:** post-level Insights export/API cho organic; Ads Manager/Marketing API cho paid, đối chiếu bằng post ID/creative ID.
- **Tần suất:** hàng tuần; tổng hợp tháng từ dữ liệu bài gốc đã khử trùng lặp.
- **Ngoại lệ:** không tự cộng link clicks/video views vào E1; không tính reply của Page như comment của người dùng nếu nguồn cho phép loại; bài bị xóa/ẩn ghi riêng; Saves thiếu trong nguồn thì công thức thực tế phải ghi rõ `Reactions + Comments + Shares`, không coi giá trị thiếu là 0.

### KPI E2 — Tỷ lệ tương tác theo reach (ERR)

- **Định nghĩa:** mức tương tác trên số người/tài khoản đã tiếp cận nội dung.
- **Công thức cấp bài:** `ERR bài (%) = Tổng tương tác hợp lệ của bài / Reach unique của bài × 100`.
- **Công thức báo cáo cohort:** báo **median ERR của các bài đủ mẫu số**; kèm số bài hợp lệ `n`. Có thể báo thêm phân vị P25–P75. Không dùng `Σ tương tác / Σ reach từng bài` như tỷ lệ unique toàn Page vì một người có thể xuất hiện ở nhiều bài.
- **Tử số:** E1 của cùng bài, cùng nguồn/phân loại organic hoặc paid và cùng thời điểm snapshot.
- **Mẫu số:** reach unique của chính bài đó; chỉ tính khi reach > 0 và cùng phạm vi với tử số.
- **Đơn vị:** phần trăm (%).
- **Cửa sổ:** cohort tuần/tháng, snapshot D+7.
- **Nguồn:** post-level Insights export/API; paid lấy Ads Manager/Marketing API với định nghĩa kết quả và attribution được ghi rõ.
- **Tần suất:** hàng tuần và hàng tháng.
- **Ngoại lệ:** reach = 0 hoặc thiếu → `N/A`, loại khỏi median và ghi số bài bị loại; không dùng impressions thay reach; không gộp organic numerator với total/paid denominator; bài boost phải có breakdown hoặc báo riêng “blended/không tách được”.

### KPI R1 — Reach unique

- **Định nghĩa:** số người/tài khoản duy nhất Facebook ghi nhận đã thấy nội dung trong phạm vi metric được chọn.
- **Công thức:** dùng trực tiếp trường reach unique từ nguồn; **không tự tính** từ impressions và không cộng reach của nhiều bài để suy ra reach unique cấp Page.
- **Tử số:** không áp dụng.
- **Mẫu số:** không áp dụng.
- **Đơn vị:** người/tài khoản unique theo định nghĩa nguồn.
- **Cửa sổ:** tuần lịch và tháng lịch; ghi rõ là post-level cohort hay Page-level period.
- **Nguồn:** Page/post Insights export/API cho organic; Ads Manager/Marketing API cho paid. Total chỉ lấy từ trường total/deduplicated do Meta cung cấp.
- **Tần suất:** hàng tuần; chốt hàng tháng.
- **Ngoại lệ:** organic/paid audience có thể chồng lặp; vì vậy không cộng hai số để tạo total. Ghi rõ khác biệt timezone giữa Ads account và Page report nếu chưa đồng nhất được.

### KPI E3 — Tương tác trung bình mỗi bài (KPI hỗ trợ)

- **Công thức:** `Σ E1 của các bài hợp lệ / số bài đã xuất bản hợp lệ`.
- **Tử số:** tổng E1 của cohort tại cùng mốc D+7.
- **Mẫu số:** bài đã xuất bản trong cohort, loại bài test/lỗi đã được đánh dấu trước; mẫu số > 0.
- **Đơn vị:** lượt/bài.
- **Tần suất/cửa sổ/nguồn:** như E1.
- **Ngoại lệ:** không có bài → `N/A`; phải báo `n`; không dùng KPI này để che phân phối lệch, nên kèm median tương tác/bài.

## 3. KPI chăm sóc và thời gian phản hồi

### Quy tắc cohort hội thoại

- Một **yêu cầu đủ điều kiện** là inbox mới hoặc bình luận cấp gốc có câu hỏi/yêu cầu cần Page xử lý, phát sinh trong cửa sổ đo.
- Loại khỏi mẫu số: spam/bot, tin trùng, reaction-only, mention không yêu cầu xử lý, tin do Page/nhân sự tạo, hội thoại test, nội dung đã xóa trước khi có thể đọc. Mọi loại trừ phải có reason code và số lượng tổng hợp.
- `t0`: timestamp yêu cầu đủ điều kiện đầu tiên của khách trong một phiên xử lý. Nếu khách gửi nhiều tin liên tiếp trước khi Page trả lời, dùng tin đầu tiên.
- `t1`: timestamp phản hồi công khai/riêng tư đầu tiên **có nội dung xử lý** từ người trực Page. Auto-reply/instant reply/away message không được coi là phản hồi người thật; có thể báo riêng.
- Một hội thoại mới được mở lại sau thời gian đóng hoặc theo quy tắc phiên đã chốt phải trở thành yêu cầu mới; quy tắc mở lại phải nhất quán toàn kỳ.
- Thời gian được tính theo **giờ đồng hồ 24/7** ở v0.1. Nếu sau này dùng business hours, phải có lịch trực/ngày nghỉ đã duyệt và báo thành series khác, không trộn với 24/7.

### KPI T1 — Thời gian phản hồi đầu tiên của người thật (FRT)

- **Công thức từng yêu cầu:** `FRT = t1 − t0`.
- **KPI kỳ:** `Median FRT = median(FRT của các yêu cầu đã có phản hồi người thật)`; báo thêm P90 nếu `n ≥ 20`.
- **Tử số:** không áp dụng theo dạng tỷ lệ; đầu vào là tổng thời lượng `t1 − t0` của từng yêu cầu.
- **Mẫu số:** số yêu cầu đủ điều kiện đã có phản hồi người thật trong cohort; mẫu số > 0.
- **Đơn vị:** phút (có thể hiển thị giờ:phút).
- **Cửa sổ:** yêu cầu có `t0` trong tuần/tháng; theo dõi đến cuối cửa sổ quan sát cố định 7 ngày sau khi kỳ kết thúc để tránh bỏ yêu cầu cuối kỳ.
- **Nguồn:** Meta Business Suite Inbox/export hoặc API/nguồn hội thoại chính thức có timestamp và phân biệt sender; bình luận lấy nguồn comment/moderation chính thức. Báo Inbox và Comment riêng, không gộp nếu quy trình trực khác nhau.
- **Tần suất:** theo dõi hàng ngày; báo tuần và tháng.
- **Ngoại lệ:** yêu cầu chưa phản hồi không nằm trong median nhưng bắt buộc nằm trong KPI T2 và backlog; timestamp thiếu/không phân biệt auto-reply → `KHÔNG ĐỦ DỮ LIỆU`; số âm hoặc lệch clock → lỗi dữ liệu; chỉnh sửa comment không đặt lại `t0` trừ khi nguồn chứng minh đó là yêu cầu mới.

### KPI T2 — Tỷ lệ được phản hồi trong ngưỡng SLA

- **Công thức:** `SLA response rate (%) = số yêu cầu đủ điều kiện có phản hồi người thật trong ngưỡng X / tổng yêu cầu đủ điều kiện đã đủ thời gian quan sát × 100`.
- **Tử số:** yêu cầu có `FRT ≤ X`; auto-reply không tính.
- **Mẫu số:** toàn bộ yêu cầu đủ điều kiện trong cohort đã qua ít nhất X kể từ `t0`, gồm cả chưa phản hồi; mẫu số > 0.
- **Đơn vị:** phần trăm (%), kèm `x/y` và `n`.
- **Cửa sổ:** tuần/tháng theo `t0`; chốt sau khi yêu cầu cuối kỳ đã đủ X. **Ngưỡng X: CẦN CHỦ TRANG/đơn vị vận hành phê duyệt**; cho đến lúc đó không tính T2 và không tự đặt ngưỡng.
- **Nguồn/tần suất:** như T1; hàng ngày để vận hành, tuần/tháng để báo cáo.
- **Ngoại lệ:** ngoài giờ vẫn tính trong series 24/7; nếu có series business-hours phải ghi lịch và công thức riêng. Yêu cầu chuyển bộ phận vẫn tính đến phản hồi đầu tiên có nội dung, không dừng đồng hồ ở thao tác gắn nhãn/chuyển tuyến.

### KPI T3 — Tỷ lệ phản hồi (không phụ thuộc SLA)

- **Công thức:** `Response rate (%) = số yêu cầu đủ điều kiện có phản hồi người thật trong cửa sổ quan sát 7 ngày / tổng yêu cầu đủ điều kiện × 100`.
- **Tử số:** yêu cầu có ít nhất một phản hồi người thật trong 7 ngày từ `t0`.
- **Mẫu số:** toàn bộ yêu cầu đủ điều kiện có `t0` trong cohort; mẫu số > 0.
- **Đơn vị:** phần trăm (%), kèm `x/y`.
- **Nguồn:** như T1.
- **Tần suất:** tuần/tháng, chốt D+7 sau cuối kỳ.
- **Ngoại lệ:** yêu cầu khách tự rút/xóa vẫn giữ trong mẫu số nếu Page đã có cơ hội đọc; nếu chưa thể đọc thì loại bằng reason code. Không đồng nhất T3 với chỉ số “response rate/time” hiển thị công khai của Facebook nếu Meta không cung cấp cùng định nghĩa và phạm vi.

## 4. Baseline v0.1

| Page | Khoảng ngày | Múi giờ | Organic | Paid | Engagement/reach baseline | FRT/response baseline | Nguồn |
|---|---|---|---|---|---|---|---|
| Fitness At Home | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | URL/ID/quyền Page và export chưa được xác minh |
| Răng sún | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | URL/ID/quyền Page và export chưa được xác minh |
| Adam Rockie | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | URL/ID/quyền Page và export chưa được xác minh |
| Moments Of Love Official | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | URL/ID/quyền Page và export chưa được xác minh |

**Không lập baseline cho PHỔ CẬP AI:** nguồn xác minh đây là Facebook Group, không phải Page. Không có số mẫu hay số ước lượng nào được dùng thay dữ liệu thật.

## 5. Dữ liệu cần bổ sung để lập baseline

1. Page URL + Page ID + bằng chứng quyền đọc Insights cho từng Page.
2. Khoảng baseline được chốt (khuyến nghị 28 ngày hoàn chỉnh gần nhất, và kỳ 28 ngày liền trước để đối chiếu) cùng timezone IANA.
3. Post/Page Insights export có post ID, publish time, content type, organic reach, paid reach/total reach đúng theo trường Meta đang cung cấp, reactions, comments, shares, saves và thời điểm snapshot.
4. Nếu có paid: Ads export có Page/post/creative mapping, account timezone, attribution setting và breakdown cần thiết; thiếu breakdown thì giữ paid riêng, không phân bổ.
5. Inbox/comment event export tối thiểu gồm mã hội thoại đã băm hoặc ID nội bộ không lộ PII, kênh (Inbox/Comment), sender type, event type, timestamp, auto/human flag, eligibility và exclusion reason; không cần nội dung tin nhắn.
6. Ngưỡng SLA `X`, lịch trực nếu muốn báo business-hours, quy tắc mở lại hội thoại và danh sách reason code được đơn vị vận hành phê duyệt.

## 6. Mẫu dòng bàn giao kết quả

`Page ID | Page URL | kỳ đo | timezone | nguồn/export time | organic/paid | KPI | tử số | mẫu số | kết quả + đơn vị | n | ngoại lệ | trạng thái kiểm định`

Mọi ô không đủ bằng chứng ghi `CHƯA CÓ DỮ LIỆU`, `N/A` (mẫu số bằng 0) hoặc `KHÔNG TÁCH ĐƯỢC`; không thay bằng 0 nếu nguồn thiếu.

## 7. Giới hạn và trạng thái nghiệm thu

- Bốn tên Page hiện chỉ là lead chưa xác minh URL/ID/quyền; Graph API chưa nối Fanpage, nên chưa có dữ liệu KPI kiểm chứng được.
- Bridge đang ở ngữ cảnh danh sách Group; `pages_count=0` không chứng minh không có Page và không được dùng làm baseline.
- Tính khả dụng/tên metric Facebook có thể đổi theo sản phẩm, quyền và phiên bản API; trước mỗi lần chạy phải đối chiếu data dictionary của export/API thực tế.
- Artifact này mới định nghĩa phương pháp; chưa được người kiểm định độc lập chấm. Trạng thái: **CHỜ NGHIỆM THU ĐỘC LẬP**.
