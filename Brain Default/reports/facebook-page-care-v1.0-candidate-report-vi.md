# Báo cáo ứng viên v1.0 — Khởi động chăm sóc Facebook Page

**Trạng thái:** ỨNG VIÊN v1.0 — CHỈ ĐỌC / BẢN NHÁP / CHƯA GHI REGISTRY / CHƯA ĐĂNG-GỬI  
**Phạm vi:** xác minh kênh, đề xuất ánh xạ tài nguyên, lịch nội dung 7 ngày, 3 mẫu phản hồi, khung KPI và trạng thái nghiệm thu.  
**Nguyên tắc:** không suy đoán URL/ID/quyền; không dùng số mẫu làm baseline; không trộn organic với paid; Facebook Group không được tính là Facebook Page.

## 1. Kết luận điều hành

1. **PHỔ CẬP AI** đã được xác minh là **Facebook Group**, không phải Page: `https://www.facebook.com/groups/712410908881271`, Group ID `712410908881271`. Tư cách admin/mod/member và năng lực quản trị vẫn **CHƯA XÁC MINH**.
2. Bốn lead **Fitness At Home, Răng sún, Adam Rockie, Moments Of Love Official** mới chỉ có tên; loại tài nguyên, URL, Page ID và quyền quản lý đều **CHƯA XÁC MINH**. Không có căn cứ để gọi đây là danh sách Page đầy đủ.
3. Graph API hiện báo chưa nối Fanpage. Bridge kết nối, Safe Mode bật nhưng đang ở ngữ cảnh danh sách Group; `pages_count=0` không chứng minh tài khoản không quản lý Page. Sổ Danh Bạ trả `count=0`, chỉ chứng minh sổ chưa có bản ghi.
4. Đã chuẩn bị lịch nội dung trung tính 7 ngày và 3 mẫu inbox/bình luận. Tất cả còn placeholder **CẦN DỮ LIỆU / CHỜ DUYỆT**; chưa đăng, lên lịch, bình luận hay gửi tin.
5. Đã định nghĩa KPI nội dung và chăm sóc với công thức, mẫu số, đơn vị, nguồn và ngoại lệ. Cả bốn lead đều **CHƯA CÓ BASELINE** vì chưa có Page ID/quyền/export kiểm chứng được. PHỔ CẬP AI bị loại khỏi baseline Page vì là Group.

## 2. Bảng bằng chứng và giới hạn diễn giải

| Mã | Nguồn/bằng chứng | Kết quả kiểm chứng được | Không được suy ra |
|---|---|---|---|
| E1 | `fb_pages_list` | Báo “Chưa nối Fanpage nào” | Không được kết luận không có Page hoặc bốn lead không tồn tại |
| E2 | `fb_ext_status` | Bridge `connected=true`, `paused=false`, `safe_mode=true`; ngữ cảnh hoạt động là danh sách Group | Không chứng minh quyền quản lý Page/Group |
| E3 | `fb_ext_discover_pages(auto_open_directory=false)` | Trả tab PHỔ CẬP AI với URL `/groups/712410908881271`; màn hình hiện tại trả `pages_count=0` | Không dùng `pages_count=0` làm bằng chứng tài khoản có 0 Page |
| E4 | Cấu trúc URL Facebook | `/groups/712410908881271` xác nhận loại Group và Group ID | Không xác nhận vai trò admin/mod/member |
| E5 | `fb_ext_discover_groups` | Lỗi `UNKNOWN_ACTION` | Không diễn giải thành không có Group hoặc thiếu quyền |
| E6 | `fb_ext_channel_registry(op=list)` | `ok=true`, `count=0`, `channels=[]` | Không chứng minh tài khoản không quản lý Page |
| E7 | TaskPacket của chủ nhóm | Cung cấp bốn tên lead | Không xác nhận loại, URL, ID hoặc quyền của từng lead |
| E8 | QA độc lập lịch nội dung | Đọc trực tiếp artifact, **PASS 10/10** tiêu chí tĩnh | Không phải phê duyệt đăng; dữ kiện sẽ điền, quyền ảnh và độ phù hợp từng Page vẫn NOT CHECKED |

Không lặp điều tra Chrome Bridge `t_fa7dae992ca3`; không điều hướng/chọn tab ngầm, không sửa Bridge/cấu hình và không ghi registry.

## 3. Kết quả xác minh kênh và registry/resource mapping đề xuất

| Khóa theo dõi/đề xuất | Tên | Loại | URL / ID | Quyền/capability | Trạng thái & blocker |
|---|---|---|---|---|---|
| `lead:facebook:fitness-at-home` | Fitness At Home | **CHƯA XÁC MINH** | **THIẾU / THIẾU** | **CHƯA XÁC MINH** | Chỉ có tên lead; thiếu URL/ID và bằng chứng quyền |
| `lead:facebook:rang-sun` | Răng sún | **CHƯA XÁC MINH** | **THIẾU / THIẾU** | **CHƯA XÁC MINH** | Như trên |
| `lead:facebook:adam-rockie` | Adam Rockie | **CHƯA XÁC MINH** | **THIẾU / THIẾU** | **CHƯA XÁC MINH** | Như trên |
| `lead:facebook:moments-of-love-official` | Moments Of Love Official | **CHƯA XÁC MINH** | **THIẾU / THIẾU** | **CHƯA XÁC MINH** | Như trên |
| `facebook:group:712410908881271` | PHỔ CẬP AI 🚀✨ Vibe code, AI Agent, Skills, Cowork - Codex, Claude... | **Group — không phải Page** | URL đã xác minh; ID `712410908881271` | Vai trò/capability **CHƯA XÁC MINH** | Danh tính đủ để đề xuất khóa Group; chưa đủ để ghi role/capability |

**Quy tắc registry đề xuất:**

- Page chỉ chuyển từ `lead:*` thành `facebook:page:{page_id}` khi có Page ID, URL chuẩn và bằng chứng tư cách/quyền.
- Group dùng `facebook:group:{group_id}` và nằm ngoài danh sách Page.
- Ghi riêng từng capability đã chứng minh: `view`, `insights`, `inbox`, `publish`, `moderate`; không suy quyền từ việc nhìn thấy tab.
- Trường tối thiểu: `resource_key`, `display_name`, `channel_type`, `canonical_url`, `platform_id`, `role/access_status`, `capabilities`, nguồn/thời điểm bằng chứng và `resource_paths` đã xác minh.
- Đây chỉ là **đề xuất**; chưa có bản ghi nào được tạo/sửa/xóa.

## 4. Lịch nội dung nháp 7 ngày

**Áp dụng:** `[TÊN PAGE — CẦN DỮ LIỆU]` sau khi xác minh Page URL/ID, quyền, định vị, nguồn nội dung và tài sản. Không chứa tuyên bố thực tế bên ngoài khi chưa có nguồn.

| Ngày | Mục tiêu / hook | Định dạng | CTA nháp | Căn cứ và chốt kiểm duyệt |
|---|---|---|---|---|
| 1 | Khảo sát: “Bạn muốn Trang chia sẻ điều gì nhiều hơn?” | Ảnh lựa chọn/poll giả lập | Bình luận chủ đề quan tâm | Cần danh mục chủ đề chính thức; không biến poll thành cam kết |
| 2 | Giới thiệu giá trị cốt lõi | Carousel 3 trang | Theo dõi và chọn chủ đề muốn xem trước | Cần sứ mệnh, trụ cột và bộ nhận diện đã duyệt |
| 3 | Mẹo ngắn theo lĩnh vực | Video dọc 15–30 giây/ảnh 3 bước | Lưu bài, gửi câu hỏi chung | Chỉ dùng mẹo có URL/tài liệu chuyên môn; lĩnh vực rủi ro cần cảnh báo và duyệt chuyên môn |
| 4 | Hậu trường một bước quy trình | Reel/album 3 ảnh | Hỏi cộng đồng muốn xem công đoạn nào | Cần SOP được phép công khai; kiểm bí mật, bản quyền, khuôn mặt và dữ liệu trong khung hình |
| 5 | FAQ đã xác nhận | Ảnh Q&A/carousel | Gửi câu hỏi chung, không đăng dữ liệu cá nhân | Cần FAQ/chính sách còn hiệu lực; giá/lịch/điều kiện phải khớp nguồn |
| 6 | Câu hỏi cộng đồng về thói quen phù hợp | Ảnh câu hỏi mở | Chia sẻ kinh nghiệm chung | Không có tuyên bố bên ngoài; cần trụ cột đã duyệt và cơ chế xử lý nội dung nhạy cảm |
| 7 | Tổng kết tuần/ưu tiên tuần sau | Carousel recap/ảnh tĩnh | Chọn chủ đề muốn đào sâu | Chỉ gọi là recap khi có bài thực sự xuất bản; không gọi “được yêu thích nhất” nếu thiếu số liệu |

**Cổng trước xuất bản:** xác minh đúng Page; điền giọng thương hiệu/trụ cột; mọi tuyên bố có nguồn còn hiệu lực; xác minh quyền ảnh/video; rà PII/bí mật; kiểm CTA theo năng lực trực; kiểm định lại bản đã điền. Hiện trạng: **CHỜ DUYỆT, CHƯA ĐĂNG/LÊN LỊCH**.

## 5. Ba mẫu phản hồi nháp

### Mẫu 1 — FAQ/thông tin chung

> Chào [CÁCH XƯNG HÔ ĐÃ DUYỆT], cảm ơn bạn đã quan tâm đến [TÊN PAGE/THƯƠNG HIỆU]. Về [CHỦ ĐỀ], thông tin đã được xác nhận là: [THÔNG TIN + NGUỒN/URL ĐÃ XÁC MINH]. Nếu chưa đủ dữ liệu, bên mình đã ghi nhận và sẽ chuyển bộ phận phụ trách kiểm tra thay vì cung cấp thông tin chưa xác minh. Bạn muốn tìm hiểu thêm về [A] hay [B]?

Chuyển người phụ trách nếu thiếu nguồn, cần tra cứu cá nhân hoặc liên quan giá/lịch/chính sách/cam kết chưa duyệt. Không tự báo giá, xác nhận lịch/tồn kho hoặc yêu cầu khách đăng PII.

### Mẫu 2 — Phản hồi tiêu cực/khiếu nại ban đầu

> Chào [CÁCH XƯNG HÔ], bên mình rất tiếc vì trải nghiệm bạn mô tả chưa như mong đợi. Bên mình đã ghi nhận [TÓM TẮT KHÔNG CÓ PII] và muốn kiểm tra kỹ trước khi phản hồi. Vui lòng không đăng số điện thoại, địa chỉ, mã đơn hoặc thông tin thanh toán tại bình luận. [HƯỚNG DẪN SANG KÊNH RIÊNG ĐÃ XÁC MINH].

Chuyển ngay nếu có nguy cơ an toàn/sức khỏe, gian lận/lộ dữ liệu, pháp lý/báo chí, thanh toán/bồi thường, quấy rối hoặc khách yêu cầu người thật. Không tranh luận, xóa/ẩn, thừa nhận trách nhiệm pháp lý hay hứa kết quả/thời hạn chưa xác minh.

### Mẫu 3 — Chuyển người phụ trách

> Chào [CÁCH XƯNG HÔ], nội dung này cần [BỘ PHẬN ĐÃ XÁC MINH] kiểm tra trực tiếp. Bên mình đã ghi nhận [TÓM TẮT KHÔNG CÓ DỮ LIỆU NHẠY CẢM] và sẽ chuyển theo quy trình. Không gửi mật khẩu, OTP, thông tin thẻ, ảnh giấy tờ hoặc dữ liệu sức khỏe tại bình luận. Nếu cần đối chiếu, chỉ cung cấp [DỮ LIỆU TỐI THIỂU ĐÃ DUYỆT] qua [KÊNH RIÊNG ĐÃ XÁC MINH]. Thời gian phản hồi: [SLA ĐÃ XÁC MINH — nếu thiếu: CẦN DỮ LIỆU].

Gói chuyển nội bộ chỉ gồm nhóm vấn đề, tóm tắt trung tính, mức ưu tiên, ID tham chiếu không lộ PII, bộ phận nhận và SLA. Hiện trạng cả ba mẫu: **CẦN DỮ LIỆU / CHỜ DUYỆT / CHƯA GỬI**.

## 6. KPI, công thức, đơn vị và nguồn

### 6.1 Quy ước báo cáo bắt buộc

- Mỗi dòng gắn đúng **Page ID + URL + khoảng ngày + múi giờ IANA + nguồn + thời điểm trích**.
- Báo riêng `organic` và `paid`; không cộng organic reach với paid reach để tạo unique total. Chỉ dùng total đã khử trùng lặp do Meta cung cấp.
- KPI bài dùng cohort bài xuất bản trong kỳ, snapshot D+7. KPI Page không được dựng bằng cách cộng unique reach của từng bài.
- Nguồn organic: Meta Business Suite/Professional Dashboard export hoặc Page Insights API đúng Page/quyền. Nguồn paid: Ads Manager/Marketing API, kèm attribution và account timezone. Nguồn chăm sóc: Business Suite Inbox/export hoặc nguồn hội thoại chính thức có timestamp và phân biệt người/auto.

### 6.2 Bảng KPI

| KPI | Công thức và điều kiện mẫu số | Đơn vị | Nguồn / cửa sổ | Ngoại lệ chính |
|---|---|---|---|---|
| **E1 Tổng tương tác** | `Reactions + Comments + Shares + Saves`; không có mẫu số | lượt | Post Insights organic; Ads/Marketing API paid; cohort kỳ, D+7 | Saves thiếu thì nêu công thức thực tế, không coi thiếu là 0; không tự cộng clicks/views |
| **E2 ERR theo reach** | Cấp bài: `E1 / reach unique cùng bài × 100`; chỉ khi reach > 0. Cohort báo median và `n` | % | Cùng nguồn/phạm vi organic hoặc paid; D+7 | Reach 0/thiếu → N/A; không dùng impressions; không trộn tử organic với mẫu paid/total |
| **R1 Reach unique** | Dùng trực tiếp metric reach unique; không tự tính từ impressions, không cộng reach bài để suy Page reach | người/tài khoản unique | Page/post Insights organic; Ads paid; tuần/tháng | Organic và paid có thể chồng lặp; total chỉ từ metric deduplicated của Meta |
| **E3 Tương tác TB/bài** | `ΣE1 / số bài hợp lệ`; mẫu số > 0, báo `n` | lượt/bài | Như E1, D+7 | Không có bài → N/A; kèm median để tránh che phân phối lệch |
| **T1 FRT người thật** | Từng yêu cầu: `t1 − t0`; kỳ báo median, thêm P90 khi `n ≥ 20`; mẫu gồm yêu cầu đủ điều kiện đã có phản hồi người thật | phút | Inbox/comment chính thức; cohort theo `t0`, theo dõi đến D+7 cuối kỳ | Auto-reply không tính; chưa phản hồi không vào median nhưng phải vào T2/backlog; Inbox và Comment báo riêng |
| **T2 Tỷ lệ trong SLA** | `số yêu cầu có FRT ≤ X / toàn bộ yêu cầu đủ điều kiện đã qua ít nhất X × 100`; mẫu gồm cả chưa phản hồi | %, kèm x/y | Như T1; chốt khi yêu cầu cuối kỳ đủ X | `X` chưa được duyệt → **CHƯA TÍNH**; thao tác gắn nhãn/chuyển tuyến không dừng đồng hồ |
| **T3 Response rate** | `số yêu cầu có phản hồi người thật trong 7 ngày / toàn bộ yêu cầu đủ điều kiện × 100`; mẫu số > 0 | %, kèm x/y | Như T1; chốt D+7 | Không đồng nhất với badge công khai của Facebook nếu khác định nghĩa |

**Yêu cầu đủ điều kiện:** inbox mới hoặc bình luận cấp gốc có yêu cầu cần Page xử lý. Loại spam/bot, trùng, reaction-only, mention không yêu cầu, nội dung của Page/nhân sự, test hoặc nội dung bị xóa trước khi có thể đọc; mọi loại trừ cần reason code và số tổng hợp. `t0` là yêu cầu đầu tiên trong phiên; `t1` là phản hồi đầu tiên có nội dung xử lý từ người thật. v1.0 dùng giờ đồng hồ 24/7; business-hours phải là series riêng có lịch trực đã duyệt.

### 6.3 Baseline

| Lead Page | Khoảng ngày | Múi giờ | Organic | Paid | Engagement/reach | FRT/response | Lý do |
|---|---|---|---|---|---|---|---|
| Fitness At Home | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | Thiếu URL/ID/quyền/export |
| Răng sún | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | Thiếu URL/ID/quyền/export |
| Adam Rockie | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | Thiếu URL/ID/quyền/export |
| Moments Of Love Official | CHƯA CÓ DỮ LIỆU | CHƯA XÁC NHẬN | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | CHƯA CÓ BASELINE | Thiếu URL/ID/quyền/export |

Không lập baseline Page cho PHỔ CẬP AI vì đây là Group. Không có số ước lượng hoặc số mẫu nào được trình bày như dữ liệu thật.

## 7. Trạng thái kiểm định độc lập

| Hạng mục | Trạng thái | Bằng chứng / giới hạn |
|---|---|---|
| Lịch nội dung 7 ngày v0.1 | **PASS** | QA độc lập E1, PASS 10/10 tiêu chí tĩnh tại `reports/facebook-page-care-v0.1-content-calendar-qa.md` |
| Dữ kiện sẽ điền, quyền ảnh/video, phù hợp từng Page | **NOT CHECKED** | Chưa có Page/brand/tài sản và nguồn thực để đối chiếu; PASS lịch không phải phê duyệt đăng |
| Xác minh kênh và mapping đề xuất | **NOT CHECKED / CHỜ NGHIỆM THU** | Có artifact nguồn, chưa thấy biên bản QA độc lập trong phạm vi báo cáo này |
| Ba mẫu phản hồi | **NOT CHECKED / CHỜ NGHIỆM THU** | Có artifact nguồn, chưa thấy biên bản QA độc lập |
| Bộ KPI | **NOT CHECKED / CHỜ NGHIỆM THU** | Kiểm định độc lập đã thông báo cần đọc trực tiếp artifact trước khi kết luận |
| Báo cáo tích hợp ứng viên v1.0 | **NOT CHECKED / CHỜ NGHIỆM THU** | Cần kiểm định độc lập đối chiếu với các artifact nguồn |

Không tuyên bố PASS cho phần chưa có bằng chứng QA.

## 8. Blocker và cách đo tiếp

1. **Kênh:** thiếu URL/Page ID và bằng chứng quyền cho bốn lead; Graph API chưa nối Fanpage. Cần nguồn chỉ đọc đúng Page để xác minh loại, ID, URL và capability.
2. **Nội dung:** thiếu định vị, giọng thương hiệu, trụ cột, FAQ/chính sách, nguồn tuyên bố, bộ nhận diện và quyền tài sản. Bản trung tính không được tự động chuyển thành bản đăng.
3. **Chăm sóc:** thiếu kênh riêng đã xác minh, bộ phận nhận, ma trận ưu tiên, dữ liệu tối thiểu được phép thu và SLA.
4. **Đo lường:** thiếu export Insights/Ads/Inbox-comment; chưa chốt kỳ baseline, timezone, ngưỡng SLA và quy tắc mở lại hội thoại.
5. **QA:** mapping, mẫu phản hồi, KPI và báo cáo tích hợp chưa có kết luận kiểm định độc lập.

**Cách đo tiếp sau khi đủ quyền/dữ liệu:** chốt Page ID/URL → chốt kỳ và timezone → xuất riêng Insights organic, Ads paid và event chăm sóc → lưu export gốc/data dictionary/bộ lọc → tính KPI đúng cohort và ngoại lệ → QA độc lập đối chiếu tử số, mẫu số, đơn vị, nguồn → chỉ khi đó ghi baseline.

## 9. Các quyết định thực sự cần chủ sở hữu phê duyệt/xác nhận

1. Xác nhận URL/Page ID đúng của từng lead hoặc phê duyệt kết nối nguồn Page chỉ đọc; không thể tự chọn theo tên trùng.
2. Chốt Page nào thuộc phạm vi vận hành sau khi quyền được chứng minh; PHỔ CẬP AI phải giữ là Group riêng.
3. Phê duyệt bộ dữ liệu thương hiệu/chính sách/tài sản dùng để điền lịch và mẫu phản hồi; sau đó duyệt riêng trước mọi hành động đăng/gửi thật.
4. Chốt múi giờ báo cáo (đề xuất `Asia/Ho_Chi_Minh`), kỳ baseline (đề xuất 28 ngày hoàn chỉnh gần nhất và 28 ngày liền trước), SLA `X`, lịch trực nếu dùng business-hours và quy tắc mở lại hội thoại.
5. Chỉ phê duyệt ghi registry sau khi từng tài nguyên đủ URL/ID/quyền; báo cáo này không thực hiện ghi.

## 10. Danh mục artifact nguồn

- `reports/facebook-page-care-v0.1-channel-verification.md`
- `reports/facebook-page-care-v0.1-channel-registry-proposal.md`
- `reports/facebook-page-care-v0.1-channel-ops-checklist.md`
- `reports/facebook-page-care-v0.1-content-calendar.md`
- `reports/facebook-page-care-v0.1-response-templates.md`
- `reports/facebook-page-care-v0.1-kpi.md`
- `reports/facebook-page-care-v0.1-content-calendar-qa.md`

**Xác nhận phạm vi hành động:** Không có bài đăng, lịch đăng, bình luận, tin nhắn, thay đổi quảng cáo, ghi registry, điều hướng/chọn tab ngầm, sửa Bridge/cấu hình hoặc lịch định kỳ nào được thực hiện trong báo cáo này.
