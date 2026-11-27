# Kiểm định độc lập toàn bộ artifact — `fb-growth-1625`

- **Mã việc:** `FB-GROWTH-1625-QA`
- **Phiên bản QA:** v1.0
- **Đầu ra kiểm:** artifact theo vai trò và local rehearsal pilot v1.0.
- **Người kiểm độc lập:** Kiểm định vận hành độc lập; không tạo các artifact được kiểm.
- **Người nghiệm thu biên bản:** Trưởng nhóm Chăm sóc Facebook.
- **Phạm vi:** đọc/đối chiếu file trong workspace và kiểm cú pháp asset local; không truy cập Facebook, không đăng/gửi/lên lịch, không ghi registry, không đổi quyền/cấu hình.
- **Trạng thái biên bản:** **CHỜ NGHIỆM THU**.
- **Chuẩn bằng chứng:** theo `reports/hien-chuong-van-hanh-cong-ty-cam-v1.md`: E1 = đọc/đo trực tiếp artifact trong lượt; E2 = TaskPacket/tin chủ cung cấp; E3 = suy luận từ E1/E2; E0 = chưa chạy. Không nâng suy luận thành E1.
- **Giới hạn:** workflow `workflows/cham-soc-fanpage-facebook.md` có `status: off`; không coi tài liệu, nhãn hay checklist là runtime enforcement.

## 1. Danh mục bằng chứng

| Evidence ID | Nguồn | Quan sát trực tiếp | Mức |
|---|---|---|---|
| EV-01 | `agents/truong-nhom-cham-soc-facebook.md` | Hợp đồng vai trò leader: chốt đầu ra/chủ việc/người kiểm, tách phần độc lập, không tự duyệt/đăng/đổi quyền | E1 |
| EV-02 | `agents/chuyen-gia-kenh-ket-noi-facebook.md` | Hợp đồng vai trò kênh: chỉ đọc, phân biệt Page/Group, không đoán, không ghi sổ/sửa Bridge | E1 |
| EV-03 | `agents/chuyen-gia-do-luong-facebook.md` | Hợp đồng đo lường: nguồn/cửa sổ/múi giờ, organic tách paid, thiếu dữ liệu không bịa số | E1 |
| EV-04 | `agents/chuyen-gia-noi-dung-cong-dong-facebook.md` | Hợp đồng nội dung: dùng nguồn xác minh, nháp trung tính khi thiếu Page, không PII, không gửi/đăng | E1 |
| EV-05 | TaskPacket `fb-growth-1625` của Chủ nhóm | Mục tiêu, giới hạn A3/LOW, checklist vai trò và cấm hành động ngoài | E2 |
| EV-06 | `reports/facebook-growth-1625-channel-evidence-v1.md` | Hai lần thử chỉ đọc; bốn tên trong “Trang của bạn” nhưng thiếu URL/ID/quyền; PHỔ CẬP AI là Group; bài thường chưa có mẫu đạt | E1 |
| EV-07 | `reports/facebook-page-care-v1.0-organic-14d-baseline.md` | Cửa sổ 14 ngày, nguồn/thời điểm, KPI likes/interactions/ERR/net follows/reach; tất cả N/A đúng lý do; edge thiếu reach/followers | E1 |
| EV-08 | `reports/facebook-growth-1625-content-audit-hypotheses-v1.md` | Audit bài gần đây N/A/NOT CHECKED; A/B chỉ đổi CTA; D+1/D+7 và keep/adjust/stop | E1 |
| EV-09 | `reports/facebook-growth-1625-leader-selection-pilot-v1.md` | Ma trận năm tiêu chí, chọn một local rehearsal không gắn Page, batch A/B, giới hạn asset, nguồn đo và luật quyết định | E1 |
| EV-10 | `reports/assets/facebook-growth-1625-neutral-abc-wireframe-v1.svg` | File tồn tại, đọc được, parse XML thành công; 1.706 byte; SHA-256 `526ce913fd254923b3f9b265063e56d3702781dee5cbbbeb9a97501cfd52a58b`; nhãn NOT PUBLISH-READY trong asset | E1 |
| EV-11 | `workflows/cham-soc-fanpage-facebook.md` | Workflow hiện `status: off` | E1 |
| EV-12 | Đối chiếu EV-01…EV-11 | Local rehearsal phù hợp với bằng chứng thiếu và không đoán Page đích | E3 |

## 2. Kết quả từng tiêu chí TaskPacket

Quy ước kết quả ca: **PASS / FAIL / NOT CHECKED** theo yêu cầu TaskPacket. Trạng thái cổng dùng đúng bộ trạng thái bắt buộc.

| # | Phiên bản / đầu vào | Kỳ vọng quan sát được | Thực tế quan sát | Evidence ID | Kết quả | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | Agent contracts hiện hành + TaskPacket | Có hợp đồng vai trò và ranh giới truy cập cho leader, kênh, đo lường, nội dung và QA độc lập | Bốn hợp đồng chuyên môn ghi rõ vai, nguồn, giới hạn; TaskPacket chỉ cho đọc/nháp và cấm đăng/gửi/đổi quyền. Hợp đồng QA nằm trong phiếu việc và biên bản này | EV-01–EV-05 | **PASS** cho artifact hợp đồng/ranh giới | **ĐẠT** |
| 2 | Brief/handoff của leader | Có bằng chứng leader đã brief tất cả vai về mục tiêu tăng trưởng, hợp đồng vai trò, ranh giới và handoff dựa bằng chứng | Có phát biểu điều phối chạy ba luồng và artifact đầu ra đúng vai, nhưng không có biên bản/ack theo từng vai chứng minh toàn bộ nội dung brief đã được truyền và hiểu | EV-01, EV-05; suy luận EV-12 | **NOT CHECKED** | **CHƯA ĐỦ BẰNG CHỨNG** |
| 3 | Bài thực hành thường: Page đủ bằng chứng | Vai kênh xử lý được một Page có URL/ID/quyền/Insights/hoạt động/asset | Không Page nào có đủ đầu vào; báo cáo kênh tự ghi bài thường NOT CHECKED/chưa có mẫu đạt. Không dùng dry run để giả PASS runtime | EV-06 | **NOT CHECKED** | **CHƯA ĐỦ BẰNG CHỨNG** |
| 4 | Edge Page-vs-Group | Không nhầm Group thành Fanpage; có ID/URL và giới hạn quyền | PHỔ CẬP AI được tách là Group ID `712410908881271`, loại khỏi pilot/baseline Page; vai trò Group vẫn chưa xác minh đúng mức | EV-06–EV-09 | **PASS** | **ĐẠT** |
| 5 | Edge thiếu reach/followers | Thiếu reach/followers phải N/A, không ghi 0/ước lượng; công thức không tính khi thiếu mẫu số | Baseline ghi N/A cho reach/net follows/likes và điều kiện thiếu/0 reach → N/A; không có số giả | EV-07 | **PASS** | **ĐẠT** |
| 6 | Bằng chứng kênh | Ghi nguồn chính xác, tối đa hai lần thử, không bypass; URL/ID/quyền thiếu phải công khai | Có hai lượt chỉ đọc, nguồn/tool/kết quả và giới hạn diễn giải; bốn lead thiếu URL/ID/quyền; không dùng Business Suite link để đoán | EV-06 | **PASS** cho báo cáo bằng chứng; quyền thực của bốn lead chưa kiểm | **ĐẠT** cho artifact; **CHƯA ĐỦ BẰNG CHỨNG** cho quyền thực |
| 7 | Baseline organic 14 ngày | Có likes nếu nguồn có, total interactions, interactions/reach, net follows, reach; nguồn/cửa sổ chính xác; N/A khi thiếu | Cửa sổ `[2026-11-14 00:00, 2026-11-28 00:00)` Asia/Ho_Chi_Minh được khóa; đủ định nghĩa trường và nguồn. Không có số vì thiếu Page/Insights | EV-07 | **PASS** cho phương pháp và biểu diễn thiếu; **NOT CHECKED** cho baseline số thực | **CHƯA ĐỦ BẰNG CHỨNG** để kết luận hiệu quả |
| 8 | Audit bài gần đây | Audit đúng Page, post URL/ID, hoạt động, hook/chủ đề/định dạng/CTA, chỉ số và quyền asset | Tất cả trường audit thực tế là N/A/NOT CHECKED vì chưa có Page node/post/Insights/manifest; tài liệu không suy đoán | EV-08 | **NOT CHECKED** | **CHƯA ĐỦ BẰNG CHỨNG** |
| 9 | Hai giả thuyết nội dung | Hai phương án so sánh được và chỉ đổi một yếu tố | A/B giữ nguyên caption trước CTA, asset/định dạng/chủ đề; chỉ CTA thay đổi. H0/H1 và điều kiện so sánh được ghi | EV-08, EV-09 | **PASS** cho thiết kế tĩnh | **ĐẠT** |
| 10 | Lựa chọn pilot | Leader so sánh ứng viên bằng bằng chứng, chọn đúng một phương án; không đoán Page | Ma trận bao phủ định danh/quyền, Insights, hoạt động, asset, baseline; chọn duy nhất local rehearsal trung tính vì không Page nào đủ bằng chứng | EV-09; kết luận phù hợp là EV-12 | **PASS** | **ĐẠT** |
| 11 | Batch trong workspace | Có caption, CTA và asset thực; nếu thiếu input phải là rehearsal, không publish-ready | Có hai caption/CTA và asset SVG local; asset parse XML thành công, hash được ghi; cả batch và asset mang nhãn NOT PUBLISH-READY | EV-09, EV-10 | **PASS** cho local rehearsal | **ĐẠT** |
| 12 | Asset rights | Có nguồn/chủ sở hữu/phạm vi quyền đủ cho mục đích đã tuyên bố; quyền xuất bản không được suy diễn | Asset là wireframe local tự tạo theo artifact và chỉ cấp phạm vi nội bộ; không có phê duyệt Page/brand owner, manifest publish hay bộ nhận diện | EV-09, EV-10 | **PASS** cho sử dụng nội bộ; **NOT CHECKED** cho quyền xuất bản | **CHƯA ĐỦ BẰNG CHỨNG** để publish-ready |
| 13 | D+1 / D+7 | Có cửa sổ, nguồn first-party, timestamp/timezone, KPI và xử lý reach thiếu/0 | D+1=24 giờ, D+7=168 giờ; yêu cầu post ID, organic unique reach, timestamp/timezone, bộ lọc organic; reach thiếu/0 → N/A | EV-08, EV-09 | **PASS** cho kế hoạch đo; chưa chạy đo thật | **ĐẠT** cho artifact; **CHƯA ĐỦ BẰNG CHỨNG** cho kết quả |
| 14 | Keep / adjust / stop | Có quy tắc quyết định, không bịa ngưỡng khi thiếu baseline | Có ba nhánh; ngưỡng tối thiểu giữ CẦN DỮ LIỆU, không gọi thắng khi reach/điều kiện không tương đương | EV-08, EV-09 | **PASS** | **ĐẠT** |
| 15 | Không tuyên bố tăng trưởng / không phê duyệt đăng | Artifact không biến rehearsal thành kết quả tăng trưởng hay phê duyệt ngoài | Không có tuyên bố tăng trưởng; mọi phần đều NOT PUBLISH-READY và yêu cầu phê duyệt riêng nếu sau này đủ điều kiện | EV-08–EV-10 | **PASS** | **ĐẠT** |
| 16 | Runtime enforcement | Không coi workflow gate/checklist là cơ chế cưỡng chế nếu chưa có log | Workflow đang `off`; không có log runtime guard. Các artifact nêu đúng rằng không được coi là enforcement | EV-09, EV-11 | **NOT CHECKED** về enforcement | **CHƯA ĐỦ BẰNG CHỨNG** |
| 17 | An toàn dữ liệu tĩnh | Không chứa dữ liệu khách, token/bí mật; bằng chứng được che phù hợp | Không thấy PII khách/token/bí mật trong các artifact kiểm; chỉ có tên tài nguyên và Group ID phục vụ định danh kênh | EV-06–EV-10 | **PASS** cho kiểm tra tĩnh | **ĐẠT** |

## 3. Kết luận độc lập

1. **Local rehearsal v1.0: ĐẠT cho sử dụng nội bộ/chỉ đọc.** Thiết kế A/B chỉ đổi CTA, có asset local thật, D+1/D+7 và keep/adjust/stop; kết luận này dựa đọc trực tiếp artifact **E1**, còn nhận định “lựa chọn rehearsal phù hợp” là suy luận **E3**.
2. **Huấn luyện/qualification toàn đội: CHƯA ĐỦ BẰNG CHỨNG.** Case thường chưa chạy được; bằng chứng brief/ack theo từng vai chưa có; audit bài thật, baseline số và quyền Page/asset xuất bản đều NOT CHECKED.
3. **Pilot thật/publish-ready và mở rộng tự động hóa: CHƯA ĐỦ BẰNG CHỨNG.** Không có Page URL/ID/capability, Insights, recent-post audit, brand inputs, quyền asset xuất bản hoặc runtime enforcement. **Không kiến nghị đăng/gửi/lên lịch/ghi registry/mở quyền.**
4. Không có tiêu chí FAIL do artifact không bịa hoặc vượt giới hạn; tuy nhiên các tiêu chí bắt buộc đang NOT CHECKED nên không được chuyển sang hành động phụ thuộc.

## 4. Lỗi chặn, chủ xử lý, điều kiện thử lại và rollback

| Lỗi chặn | Chủ xử lý | Điều kiện thử lại | Quay về quy trình trước |
|---|---|---|---|
| Thiếu bằng chứng brief/ack và kết quả case thường theo từng vai | Trưởng nhóm | Có phiếu brief phiên bản hóa, acknowledgment/kết quả từng vai và một Page giả/sandbox hoặc nguồn thật chỉ đọc đủ URL/ID/quyền | Giữ huấn luyện ở local rehearsal; không tuyên bố qualified runtime |
| Thiếu URL/Page ID/capability và Insights cho bốn lead | Kênh & Kết nối | Có canonical URL, Page ID và capability `view/insights/publish` từ nguồn first-party; tuân thủ giới hạn thử mới được chủ chốt | Giữ bốn khóa `lead:*`, không ghi registry hay chọn Page |
| Thiếu baseline số và audit bài thật | Đo lường + Nội dung | Có export first-party đúng cửa sổ/timezone và post URL/ID; không PII; audit/metric đối chiếu được | Dùng N/A/NOT CHECKED, không kết luận tăng trưởng |
| Thiếu brand inputs và quyền asset xuất bản | Nội dung + chủ sở hữu thương hiệu | Có trụ cột A/B/C, giọng thương hiệu, manifest nguồn/quyền/phạm vi và người duyệt | Giữ SVG trung tính chỉ nội bộ, NOT PUBLISH-READY |
| Workflow off, chưa có runtime guard/log phục hồi | Trưởng nhóm/quản trị quy trình | Nếu đánh giá automation: chạy sandbox bằng dữ liệu giả cho luồng đúng, thiếu bằng chứng, trùng mã, thiếu phê duyệt, timeout sau lưu; lưu log và kiểm rollback/idempotency | Duy trì quy trình thủ công, chỉ đọc và phê duyệt riêng |

## 5. Bàn giao cổng nghiệm thu

| Mã việc | Đầu ra/phiên bản | Từng tiêu chí | Bằng chứng | Kết quả từng tiêu chí | Trạng thái | Lỗi còn lại / điều kiện thử lại |
|---|---|---|---|---|---|---|
| `FB-GROWTH-1625-QA` | `reports/facebook-growth-1625-independent-qa-v1.md` v1.0 | 17 tiêu chí tại §2 | EV-01…EV-12 | PASS cho artifact hợp đồng, edge cases, bằng chứng kênh, phương pháp baseline, A/B, lựa chọn rehearsal, batch, kế hoạch đo và an toàn tĩnh; NOT CHECKED cho brief thực tế, case thường, baseline/audit thật, quyền xuất bản và runtime enforcement | **CHỜ NGHIỆM THU** | Trưởng nhóm nghiệm thu biên bản; chỉ thử lại các phần phụ thuộc khi đủ nguồn/đầu vào nêu tại §4 |

**Phần đã kiểm:** toàn bộ file vai trò, báo cáo kênh, baseline, audit/hypotheses, leader selection/pilot và asset SVG nêu ở EV-01…EV-11.  
**Phần chưa kiểm:** hành vi Facebook/runtime, quyền thật, nội dung bài gần đây, số Insights, quyền xuất bản asset, hiệu quả tăng trưởng và enforcement.  
**Ngoại lệ:** không có ngoại lệ được duyệt; không phát sinh gói xin duyệt đăng vì chưa có batch publish-ready.
