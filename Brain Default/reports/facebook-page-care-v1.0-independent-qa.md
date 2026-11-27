# Biên bản QA độc lập — Facebook Page Care v1.0

- **Mã việc:** FB-CARE-V1.0-QA
- **Trace:** `fb-growth-1625`
- **Đầu ra được kiểm:** `reports/facebook-page-care-v1.0-candidate-report-vi.md`
- **Hiện vật nguồn:**
  - `reports/facebook-page-care-v0.1-channel-verification.md`
  - `reports/facebook-page-care-v0.1-channel-registry-proposal.md`
  - `reports/facebook-page-care-v0.1-content-calendar.md`
  - `reports/facebook-page-care-v0.1-response-templates.md`
  - `reports/facebook-page-care-v0.1-kpi.md`
  - `reports/facebook-page-care-v0.1-content-calendar-qa.md`
- **Phiên bản kiểm:** ứng viên v1.0 và các hiện vật v0.1 nêu trên.
- **Người nghiệm thu độc lập:** Kiểm định vận hành độc lập; không phải người tạo các hiện vật được kiểm.
- **Phạm vi:** đọc và đối chiếu tĩnh file trong workspace; không truy cập/chỉnh sửa Facebook, không gửi/đăng, không ghi registry, không kiểm thử hệ thống thật.
- **Tiêu chí đạt:** đúng checklist được giao: bằng chứng URL/ID/quyền; tách Page/Group; không đoán; lịch đủ 7 ngày; đủ 3 mẫu; KPI có công thức/nguồn; baseline có căn cứ; chỉ đọc; không có dữ liệu nhạy cảm.
- **Mức bằng chứng:** **E1** cho nội dung đọc trực tiếp trong các file ở trên; **E3** cho suy luận về tính nhất quán giữa các file. Không có log thực thi để xác nhận hành vi runtime.
- **Người chấp nhận cuối:** Trưởng nhóm Chăm sóc Facebook; QA này không thay phê duyệt đăng/gửi hay thay đổi hệ thống.

## Kết quả từng tiêu chí

| # | Phiên bản / đầu vào | Kỳ vọng | Thực tế quan sát | Bằng chứng cụ thể | Kết quả | Trạng thái cổng |
|---|---|---|---|---|---|---|
| 1 | v1.0 + channel verification/mapping v0.1 | URL, ID và quyền của từng tài nguyên phải có nguồn; thiếu phải ghi rõ, không suy đoán | Bốn lead chỉ có tên và đều ghi thiếu URL/ID, quyền chưa xác minh; PHỔ CẬP AI có URL và Group ID, nhưng vai trò/capability vẫn chưa xác minh | Candidate §1–3; channel verification bảng “Kết quả xác minh”; mapping bảng “Bản đồ đề xuất” (**E1**) | **PASS** cho cách biểu diễn bằng chứng; quyền/URL/ID của 4 lead vẫn chưa xác minh | **ĐẠT** đối với kiểm soát không đoán; xem #2 cho dữ kiện còn thiếu |
| 2 | Bốn lead Page v1.0 | Có bằng chứng trực tiếp URL/Page ID và tư cách/quyền nếu muốn coi là Page được quản lý | Không có URL, Page ID hoặc bằng chứng quyền cho Fitness At Home, Răng sún, Adam Rockie, Moments Of Love Official; báo cáo không giả lập thay thế | Candidate §1, §3, §6.3, §8; channel verification (**E1**) | **NOT CHECKED** về quyền sở hữu/quản lý thực tế do thiếu nguồn | **CHƯA ĐỦ BẰNG CHỨNG** |
| 3 | PHỔ CẬP AI v1.0 | Phải phân biệt Group với Page, không đưa vào baseline Page | Được ghi là Group, URL `/groups/712410908881271`, ID `712410908881271`; nằm ngoài danh sách/baseline Page; vai trò không bị suy diễn | Candidate §1, §2 E3–E5, §3, §6.3; channel verification và mapping (**E1**) | **PASS** | **ĐẠT** |
| 4 | Channel evidence v0.1/v1.0 | Không diễn giải `pages_count=0`, registry rỗng hoặc lỗi tool thành “không có Page/Group” | Báo cáo nêu đúng giới hạn: màn hình là danh sách Group; registry rỗng chỉ là chưa có bản ghi; `UNKNOWN_ACTION` là lỗi công cụ | Candidate §1–2; channel verification “Bằng chứng công cụ và giới hạn”; mapping “Trạng thái nguồn” (**E1**) | **PASS** | **ĐẠT** |
| 5 | Content calendar v0.1 + tích hợp v1.0 | Đủ 7 ngày; mỗi ngày có mục tiêu/hook, định dạng, CTA, căn cứ và lưu ý kiểm duyệt; không tự điền thương hiệu | Có đủ Ngày 1–7 và đầy đủ các trường; dữ kiện chưa xác minh giữ placeholder; bản v1.0 tóm lược đúng | Content calendar toàn bộ 7 mục; QA lịch v0.1 PASS 10/10; candidate §4 (**E1**) | **PASS** | **ĐẠT** |
| 6 | Response templates v0.1 + tích hợp v1.0 | Đủ 3 mẫu; có điều kiện escalation, giới hạn lời hứa và bảo vệ PII; chưa gửi thật | Có đúng 3 mẫu: FAQ, phản hồi tiêu cực, chuyển người phụ trách; có escalation/điều cấm/placeholder; nhãn CHỜ DUYỆT và CHƯA GỬI | Response templates mục 1–3 và checklist; candidate §5 (**E1**) | **PASS** cho artifact tĩnh | **ĐẠT** |
| 7 | KPI v0.1 + tích hợp v1.0 | KPI engagement/reach/FRT/response có công thức, tử–mẫu, đơn vị, nguồn, cửa sổ và ngoại lệ; organic/paid tách riêng | E1, E2, R1, E3, T1, T2, T3 đều có công thức và nguồn; quy tắc cohort, D+7, mẫu số 0/thiếu, auto-reply và tách organic/paid được nêu rõ | KPI v0.1 §1–3; candidate §6.1–6.2 (**E1**) | **PASS** | **ĐẠT** |
| 8 | Baseline v0.1/v1.0 | Chỉ báo baseline có nguồn; thiếu dữ liệu phải N/A/CHƯA CÓ, không dùng số mẫu/ước lượng | Cả bốn lead ghi CHƯA CÓ BASELINE do thiếu URL/ID/quyền/export; Group bị loại; không có con số giả | KPI v0.1 §4–5; candidate §6.3 (**E1**) | **PASS** cho tính trung thực của bảng baseline; baseline thực tế chưa đo | **ĐẠT** đối với báo cáo; **CHƯA ĐỦ BẰNG CHỨNG** để kết luận hiệu quả |
| 9 | Toàn bộ hiện vật | Không chứa dữ liệu khách hàng, bí mật, token hoặc định danh cá nhân cụ thể | Không thấy tên khách, số điện thoại, email, địa chỉ, mã đơn, nội dung inbox thật, token hay bí mật; chỉ có placeholder và ID tài nguyên Facebook công khai theo báo cáo | Đọc trực tiếp toàn bộ các file liệt kê (**E1**) | **PASS** cho kiểm tra tĩnh | **ĐẠT** |
| 10 | Toàn bộ hiện vật | Phạm vi chỉ đọc/soạn nháp; không tuyên bố đã đăng/gửi/ghi registry/đổi cấu hình | Tất cả file đều ghi không đăng/gửi/ghi registry; candidate không tuyên bố hành động ngoài | Candidate trạng thái, §7, §10; phần phạm vi của từng artifact (**E1**) | **PASS** về nội dung khai báo; **NOT CHECKED** về hành vi runtime vì không có audit log độc lập | **CHƯA ĐỦ BẰNG CHỨNG** cho xác nhận runtime |
| 11 | Candidate report v1.0 | Báo cáo tích hợp phải phản ánh đúng artifact nguồn, nêu phần đã/không kiểm và không biến QA lịch thành phê duyệt đăng | Nội dung kênh, lịch, mẫu, KPI và blocker khớp artifact; §7 giữ mapping/mẫu/KPI/report ở NOT CHECKED trước lượt QA và giới hạn PASS lịch | Đối chiếu candidate §1–10 với sáu artifact nguồn (**E1**); kết luận nhất quán là suy luận **E3** | **PASS** | **ĐẠT** |
| 12 | Cơ chế workflow/guard | Không được tuyên bố workflow đang cưỡng chế nếu chưa có bằng chứng | Báo cáo không tuyên bố workflow đang bật hay có runtime guard | Candidate toàn văn (**E1**) | **PASS** cho cách diễn đạt; runtime enforcement **NOT CHECKED** | **CHƯA ĐỦ BẰNG CHỨNG** để mở rộng tự động hóa |

## Tổng hợp nghiệm thu

- **Artifact báo cáo v1.0:** **ĐẠT** cho mục đích báo cáo nội bộ, chỉ đọc và bản nháp. Nội dung tích hợp phản ánh đúng các file nguồn, không đoán dữ kiện và không chứa PII/bí mật quan sát được.
- **Xác minh Page/quyền và baseline thực:** **CHƯA ĐỦ BẰNG CHỨNG**. Bốn lead chưa có URL/Page ID/quyền; chưa có Insights/Inbox export nên không có baseline hay kết luận tăng trưởng.
- **Sẵn sàng đăng/gửi/ghi registry hoặc mở rộng tự động hóa:** **CHƯA ĐỦ BẰNG CHỨNG**. Không có Page đích đã xác minh, tài sản/quyền sử dụng, dữ kiện thương hiệu đã điền, log runtime guard hoặc phê duyệt hành động ngoài.
- **Lỗi chặn:** thiếu URL/Page ID và bằng chứng capability/quyền cho bốn lead; thiếu nguồn thương hiệu/tài sản; thiếu export đo lường; thiếu log runtime độc lập.
- **Chủ xử lý:** Kênh & Kết nối cung cấp bằng chứng tài nguyên/quyền; Nội dung & Cộng đồng cung cấp nguồn thương hiệu/tài sản; Đo lường cung cấp export và data dictionary; Trưởng nhóm quyết định/phê duyệt bước ngoài sau QA.

## Phần chưa chạy và ca thử lại

Đây là kiểm tra tĩnh, không phải ca chạy workflow. Các ca dữ liệu giả về thiếu bằng chứng, trùng mã, thiếu phê duyệt và timeout sau khi bên nhận đã lưu **chưa chạy**; do đó không có căn cứ kết luận cơ chế chặn, idempotency hoặc phục hồi hoạt động. Điều này không chặn sử dụng báo cáo nội bộ nhưng chặn kiến nghị tự động hóa/đăng-gửi.

**Điều kiện thử lại:**
1. Có nguồn chỉ đọc ghi rõ canonical URL, Page ID, vai trò và từng capability của Page được chọn; không quá hai lần thử và không bypass.
2. Có bản nội dung đã điền cho đúng Page, kèm nguồn từng tuyên bố, tài sản và bằng chứng quyền sử dụng; có export Insights/Inbox đúng cửa sổ/timezone nếu đánh giá baseline.
3. Nếu đánh giá automation, chạy sandbox/dữ liệu giả cho luồng đúng, thiếu bằng chứng, trùng mã, thiếu phê duyệt và timeout sau lưu; lưu log đầu vào–kết quả–rollback.

**Đường quay về quy trình trước:** giữ nguyên các file v0.1/v1.0 ở trạng thái nháp chỉ đọc; không đăng/gửi/lên lịch, không ghi registry, không đổi quyền/cấu hình. Nếu bản điền dữ liệu hoặc ca runtime trượt, quay lại placeholder trung tính và xử lý thủ công có phê duyệt.

## Bàn giao theo cổng bắt buộc

| Mã việc | Đầu ra/phiên bản | Tiêu chí | Bằng chứng | Kết quả | Trạng thái | Lỗi còn lại / điều kiện thử lại |
|---|---|---|---|---|---|---|
| FB-CARE-V1.0-QA | `reports/facebook-page-care-v1.0-independent-qa.md` v1.0 | 12 tiêu chí ở bảng trên | E1: đọc trực tiếp candidate và artifact nguồn; E3: đối chiếu nhất quán | 10 PASS về artifact/cách biểu diễn; 4 phạm vi con NOT CHECKED hoặc thiếu bằng chứng runtime/dữ liệu thực | **CHỜ NGHIỆM THU** | Trưởng nhóm nghiệm thu biên bản; không chuyển sang đăng/gửi/automation cho tới khi các điều kiện thử lại tương ứng được đáp ứng |
