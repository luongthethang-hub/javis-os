# Bài thực hành Đo lường — xu hướng, baseline và KPI pilot Facebook 7 ngày

- **Trace ID:** `facebook-growth-leadership-1656`
- **Phiên bản:** v1.0 — 28/11/2026
- **Ngày/giờ truy cập nguồn:** 28/11/2026, `Asia/Ho_Chi_Minh` (UTC+7)
- **Phạm vi:** nghiên cứu web công khai + thiết kế đo; chỉ đọc/soạn nháp, không đăng, gửi, chi tiền hay đổi cấu hình.
- **Kênh/Page:** **CHƯA XÁC MINH** trong đầu vào của vai Đo lường; không gắn kết quả với PHỔ CẬP AI vì tài nguyên này đã xác minh là **Group**, không phải Page.
- **Nguồn số hiệu suất:** **CHƯA CÓ DỮ LIỆU** Page/Insights/Ads; không có baseline hay kết quả D+1/D+7 thực.
- **Trạng thái:** **XONG** artifact phương pháp; **ĐẠT/PASS** cho bài thực hành tĩnh; baseline số, pilot thật và tác động tăng trưởng **NOT CHECKED / CHƯA ĐỦ BẰNG CHỨNG**.

## 1. Nhật ký nguồn còn sống

| ID | Nguồn trực tiếp/chính thức | Quan sát trong lượt | Phạm vi bằng chứng | Trạng thái |
|---|---|---|---|---|
| T1 | Bộ Công an — chuyên mục Giấy phép lái xe: https://bocongan.gov.vn/chinh-sach-phap-luat/tag/1076 | Trang trả nội dung trực tiếp. Bài 16/08/2024 nêu Luật TTATGT đường bộ 2024 có hiệu lực 01/01/2025 và thay đổi phân hạng GPLX; bài 03/03/2025 nêu Thông tư 12/2025/TT-BCA hiệu lực 01/03/2025. | Dữ kiện pháp lý toàn quốc; không phải dữ liệu nhu cầu/viral. | **PASS** |
| T2 | PBGDPL Hà Nội — “Quy định sát hạch, cấp GPLX từ 01/3/2025”: https://pbgdpl.hanoi.gov.vn/quy-dinh-moi/-/asset_publisher/sxBNLsQSLyY8/content/quy-inh-sat-hach-cap-giay-phep-lai-xe-tu-ngay-01-3-2025 | Trang trả nội dung trực tiếp. Với hạng B, nội dung công bố gồm lý thuyết trên máy tính, thực hành trong hình, thực hành trên đường và mô phỏng; liệt kê các nhóm kiến thức/kỹ năng. | Nguồn cơ quan nhà nước dẫn Thông tư 12/2025; không phải bằng chứng riêng Nam Tam Điệp. | **PASS** |
| T3 | Bộ Công an — đề xuất đổi mới sát hạch: https://bocongan.gov.vn/chinh-sach-phap-luat/bai-viet/bo-cong-an-de-xuat-doi-moi-sat-hach-lai-xe-theo-huong-thuc-chat-lay-ky-nang-thuc-te-lam-trong-tam-1782464069 | Trang trả nội dung trực tiếp; đăng 03/07/2026. Nguồn ghi rõ đây là **dự thảo** thay Thông tư 12/2025, định hướng hạn chế học mẹo, tăng đánh giá kỹ năng thực tế; các con số/cấu trúc nêu trong bài là đề xuất. | Tín hiệu chính sách; không được trình bày như quy định chắc chắn đang có hiệu lực. | **PASS với nhãn DỰ THẢO** |
| M1 | Meta Business Help — Insights desktop: https://www.facebook.com/business/help/700570830721044/?id=765488040896522 | Kết quả tìm kiếm nguồn chính thức còn sống mô tả Insights giúp hiểu kết quả hoạt động organic và paid; truy cập nội dung trực tiếp qua bộ đọc web trả HTTP 400. | Chỉ xác nhận định hướng nguồn đo; không dùng để khẳng định tên trường/giá trị metric. | **NOT CHECKED** chi tiết trang |
| M2 | Meta Business Help — reach: https://www.facebook.com/business/help/1109973216315602/ | Kết quả tìm kiếm nguồn chính thức còn sống; truy cập trực tiếp qua bộ đọc web trả HTTP 400. | Không suy định nghĩa trường cụ thể từ snippet. | **NOT CHECKED** chi tiết trang |
| M3 | Meta for Developers — Page Insights: https://developers.facebook.com/docs/graph-api/reference/insights/ | Kết quả tìm kiếm nguồn chính thức cảnh báo một số Page Insights metrics bị deprecated từ 15/06/2026; truy cập trực tiếp qua bộ đọc web trả HTTP 400. | Khi có quyền phải lưu API version/data dictionary và kiểm metric thực còn trả về; không hard-code tên metric cũ. | **PASS** cho cảnh báo thay đổi; **NOT CHECKED** danh sách metric |

**Số lần thử nguồn Meta:** (1) mở trực tiếp các trang chính thức; (2) tìm lại trên web để xác nhận URL/snippet. Không bypass đăng nhập/chống bot.

## 2. Dữ kiện khác với suy luận

### Dữ kiện đủ căn cứ

1. Khung GPLX/sát hạch đã thay đổi từ đầu năm 2025 (T1, T2).
2. Nội dung công bố về sát hạch hạng B bao phủ nhiều lớp năng lực, không chỉ lý thuyết: trong hình, trên đường và xử lý tình huống (T2).
3. Bài Bộ Công an ngày 03/07/2026 cho thấy **hướng dự thảo** nhấn mạnh đánh giá thực chất, kỹ năng thực tế và hạn chế học mẹo (T3).
4. Không có bằng chứng trực tiếp trong bộ nguồn này về lượng tìm kiếm, nhu cầu học, mức quan tâm Facebook hay xu hướng tương tác riêng tại Nam Tam Điệp.

### Suy luận biên tập — chưa phải kết quả thị trường

- Góc “học chắc kỹ năng thực tế, không chỉ học mẹo” phù hợp với dữ kiện chính sách. **Độ tin cậy cao về độ phù hợp chủ đề**, nhưng hiệu quả tương tác **CHƯA CÓ DỮ LIỆU**.
- Checklist phân biệt “đang áp dụng” với “đang đề xuất” có thể hữu ích và giảm hiểu nhầm. Đây là giả thuyết nội dung, chưa chứng minh tăng like/follow.
- CTA hỏi “kỹ năng nào khó nhất?” tạo tín hiệu bình luận có thể đo; không được suy ra nhu cầu tuyển sinh hay ý định mua.
- Không được tuyên bố: “đang viral”, “người Nam Tam Điệp đổ xô học”, “nhu cầu tăng X%”, “bài chắc chắn tăng tương tác/like/follow”.

## 3. Khung baseline trước pilot

### 3.1 Điều kiện mở baseline

Chỉ tính khi có đủ: canonical Page URL + Page ID; quyền đọc Insights; export first-party; khoảng ngày và `Asia/Ho_Chi_Minh`; thời điểm trích; API/export version và data dictionary; bộ lọc organic/paid. Nếu thiếu một trường định danh hoặc không tách được nguồn, ghi **CHƯA CÓ DỮ LIỆU**, không điền 0.

### 3.2 Cửa sổ đề xuất

- **Baseline chính:** 28 ngày hoàn chỉnh liền trước thời điểm pilot, `[D-28 00:00, D0 00:00)` theo `Asia/Ho_Chi_Minh`.
- **Kỳ đối chiếu mùa vụ ngắn:** 28 ngày ngay trước baseline, `[D-56 00:00, D-28 00:00)` nếu có dữ liệu.
- **Cohort bài tương đồng:** bài organic cùng chủ đề/định dạng trong baseline; báo `n`, median và IQR. Nếu `n < 5`, chỉ mô tả, không đặt ngưỡng thắng định lượng.
- **Paid:** bảng riêng theo Ads Manager/Marketing API và account timezone. Không cộng organic reach với paid reach để dựng unique total; total chỉ dùng metric deduplicated do Meta cung cấp.

### 3.3 Bảng baseline hiện tại

| Thành phần | Organic | Paid | Trạng thái |
|---|---:|---:|---|
| Page ID/URL và kỳ đo | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | NOT CHECKED |
| Reach unique | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | NOT CHECKED |
| Reactions Like / tổng reactions | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | NOT CHECKED |
| Comments, shares, saves (nếu export có) | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | NOT CHECKED |
| Follows, unfollows, net follows | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | NOT CHECKED |
| ERR theo reach | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | NOT CHECKED |

## 4. KPI và công thức khóa trước pilot

| KPI | Công thức | Đơn vị / điều kiện mẫu số | Phạm vi |
|---|---|---|---|
| **K1 — Tổng tương tác nội dung** | `reactions + comments + shares + saves_available` | lượt; không mẫu số. Chỉ cộng trường export thực có; nếu thiếu saves phải ghi công thức thực tế, không thay bằng 0. Không tự cộng clicks/views. | Báo riêng organic và paid, theo từng post/snapshot. |
| **K2 — ERR theo reach (KPI chính)** | `K1 / reach_unique_cùng_post × 100` | %; chỉ tính khi reach unique > 0. Reach thiếu/0 → N/A. | Không trộn tử organic với mẫu paid/total. |
| **K3 — Like reaction rate** | `số reaction loại Like / reach_unique_cùng_post × 100` | %; reach > 0 và export tách được reaction Like. Nếu chỉ có tổng reactions → N/A cho K3. | Đây là Like reaction trên nội dung, không đồng nhất Page likes. |
| **K4 — CTA comment rate** | `bình luận hợp lệ trả lời CTA / reach_unique_cùng_post × 100` | %; reach > 0. Bình luận hợp lệ được chốt trước: bình luận cấp gốc, không spam/bot/trùng/nội dung của Page/test. Báo tử/mẫu. | Đo chất lượng phản hồi cho CTA. |
| **K5 — New follows** | `follows trong cửa sổ` | tài khoản; chỉ dùng trường Insights thực có cùng cửa sổ. | Page-level; không quy nguyên nhân cho một post nếu nguồn không có attribution post-level. |
| **K6 — Net follows** | `follows − unfollows` | tài khoản; chỉ khi cả hai trường cùng phạm vi/cửa sổ tồn tại. Nếu không → N/A. | Organic/paid chỉ tách nếu nguồn cung cấp attribution đáng tin cậy; nếu không ghi `unattributed Page-level`. |
| **K7 — Follow conversion** | `post-attributed follows / reach_unique_cùng post × 100` | %; chỉ tính nếu Meta/export thực trả post-attributed follows và reach > 0. | Thiếu trường attribution → N/A, tuyệt đối không lấy biến động follower Page gán cho bài. |
| **K8 — Page likes delta** | `Page likes cuối snapshot − Page likes đầu snapshot` | lượt thích Trang; chỉ khi Page còn hiển thị/xuất được cùng định nghĩa. | Chỉ số phụ Page-level, không thay cho Like reaction và không tuyên bố do bài gây ra. |

**Quy tắc tên trường:** tại lúc export, lưu `metric_label`, `metric_key`, API/export version, period, source và định nghĩa hiển thị. Do cảnh báo deprecation ở M3, tên trường trên không phải cam kết API key.

## 5. Snapshot D+1 và D+7

- Gọi `t_publish` là timestamp đăng thật đã xác minh.
- **D+1:** snapshot tích lũy tại `t_publish + 24 giờ` (dung sai thu thập ±30 phút, ghi giờ thực tế).
- **D+7:** snapshot tích lũy tại `t_publish + 168 giờ` (dung sai ±2 giờ, ghi giờ thực tế).
- Mỗi dòng phải có Page ID/URL, post ID/URL, biến thể A/B, `t_publish`, `t_snapshot`, timezone, source/export version, organic/paid flag.

### Công thức snapshot và tăng thêm

- `K_i(D+1) = KPI i tính từ dữ liệu tích lũy [t_publish, t_publish+24h]`.
- `K_i(D+7) = KPI i tính từ dữ liệu tích lũy [t_publish, t_publish+168h]`.
- Với KPI dạng đếm: `increment_D1_to_D7 = count(D+7) − count(D+1)`; chỉ tính khi hai snapshot cùng định nghĩa/version/phạm vi.
- Với KPI tỷ lệ: **tính lại từ tử và mẫu D+7**, không cộng/trừ hai tỷ lệ. Có thể báo `percentage-point change = rate(D+7) − rate(D+1)` như mô tả, không gọi là lift nhân quả.
- Nếu snapshot trễ, dùng timestamp thực và không giả là đúng 24/168 giờ.

### So sánh A/B an toàn

- Chỉ gọi là so sánh hợp lệ khi cùng Page, chủ đề, asset/format, nhóm thời gian tương đương và **chỉ đổi một yếu tố**; ghi chênh lệch reach và mọi paid support.
- `delta_ERR_pp = ERR_B − ERR_A`; đồng thời báo tử số, mẫu số và reach từng biến thể.
- Like/follow là KPI phụ. Không chọn “thắng” nếu một biến thể có paid delivery, reach chênh lớn/không tương đương, dữ liệu thiếu, hoặc `n` quá nhỏ.
- Chưa có baseline nên ngưỡng KEEP/ADJUST/STOP định lượng là **CẦN DỮ LIỆU**. STOP an toàn nếu có thông tin sai/rủi ro, quyền asset không hợp lệ hoặc không đo tách nguồn được; đây không phải kết luận hiệu suất.

## 6. Mẫu bàn giao đo

| Page ID/URL | Post/variant | Snapshot | Organic reach | Paid reach | K1 | K2 ERR | K3 Like rate | K4 CTA rate | New/net follows | Nguồn/version | Trạng thái |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| CHƯA XÁC MINH | CHƯA CÓ POST | D+1 | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | N/A | N/A | N/A | N/A | N/A | CHƯA CÓ | NOT CHECKED |
| CHƯA XÁC MINH | CHƯA CÓ POST | D+7 | CHƯA CÓ DỮ LIỆU | CHƯA CÓ DỮ LIỆU | N/A | N/A | N/A | N/A | N/A | CHƯA CÓ | NOT CHECKED |

## 7. Tự chấm bài thực hành vai Đo lường

| Tiêu chí | Kết quả | Bằng chứng / giới hạn |
|---|---|---|
| Nguồn trực tiếp/chính thức còn sống, ngày truy cập | **PASS** | T1–T3 được đọc trực tiếp ngày 28/11/2026; M1–M3 ghi rõ mức kiểm. |
| Tách dữ kiện và suy luận | **PASS** | §2; không biến tín hiệu chính sách thành nhu cầu/viral. |
| Page/Group và đúng kênh | **PASS** | Không đưa Group PHỔ CẬP AI vào baseline Page; Page đích vẫn CHƯA XÁC MINH. |
| Tách organic/paid | **PASS** phương pháp | §3–§6; số thật **NOT CHECKED**. |
| KPI interaction/like/follow, công thức/đơn vị/mẫu số | **PASS** | K1–K8; reach thiếu/0 → N/A. |
| D+1/D+7, timezone và version | **PASS** | §5; khóa 24h/168h, UTC+7 và lưu version. |
| Baseline số thực | **NOT CHECKED** | Thiếu Page ID/URL, Insights/export và quyền đọc. |
| Hiệu quả/tăng trưởng pilot | **NOT CHECKED** | Chưa đăng và chưa tới checkpoint; không có kết quả tương lai được tuyên bố. |

## 8. Kết luận và điều kiện thử lại

Artifact **XONG và PASS cho thiết kế đo tĩnh**, chưa chứng minh pilot hay tăng trưởng **ĐẠT**. Để thử lại phần số thực: xác minh Page/capability đọc Insights → lưu export organic và paid riêng cùng data dictionary/version → tính baseline 28 ngày → sau đăng đã được duyệt, chụp D+1/D+7 → QA độc lập đối chiếu tử, mẫu, timestamp và nguồn. Không phát sinh hành động công khai trong lượt này.
