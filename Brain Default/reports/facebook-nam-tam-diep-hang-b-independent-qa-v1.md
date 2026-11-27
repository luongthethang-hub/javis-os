# Kiểm định độc lập — quét kênh và bản nháp học lái xe hạng B Nam Tam Điệp

- **Mã việc:** FB-DRIVING-B-NAM-TAM-DIEP-V1-QA
- **Phiên bản kiểm:** QA v1.0
- **Artifact được kiểm trực tiếp:**
  1. `reports/facebook-driving-b-channel-scan-v1.md`
  2. `reports/facebook-nam-tam-diep-hang-b-trend-evidence-v1.md`
  3. `reports/facebook-nam-tam-diep-hang-b-content-checklist-v1.md`
  4. `reports/facebook-nam-tam-diep-hang-b-draft-v1.md` — caption v1.0
- **Phạm vi quyền:** đọc, kiểm chứng nguồn công khai, lập biên bản nội bộ. Không đăng, gửi, lên lịch, ghi registry, đổi cấu hình hoặc mở quyền.
- **Tiêu chí đã chốt:** phân loại Page/Group; URL/ID; bằng chứng sở hữu; chất lượng nguồn xu hướng; phù hợp Nam Tam Điệp; CTA; asset rights; kiểm duyệt; ranh giới quyền.
- **Người nghiệm thu độc lập biên bản:** Trưởng nhóm Chăm sóc Facebook; người kiểm không phải tác giả bốn artifact nêu trên.
- **Giả định:** nội dung log công cụ được chép trong artifact quét kênh là đúng bản bàn giao; QA này không tái thao tác Facebook thật.
- **Đã kiểm:** toàn văn bốn artifact; mở trực tiếp ba URL nguồn S1–S3 trên web; đối chiếu caption với các căn cứ và giới hạn.
- **Chưa kiểm:** quyền/ownership Facebook thực; URL/ID bốn Page; vai trò admin/mod sáu Group; kênh Nam Tam Điệp; văn bản pháp lý gốc/hợp nhất còn hiệu lực; asset cuối và manifest; lịch sử nội dung/brand voice; hành vi runtime khi publish.

## 1. Thang bằng chứng

- **E1:** đọc trực tiếp artifact hoặc URL công khai trong lượt QA.
- **E3:** suy luận từ E1; không nâng thành E1.
- Nguồn chuẩn: `reports/hien-chuong-van-hanh-cong-ty-cam-v1.md` và các URL ghi trong báo cáo xu hướng.

## 2. Kết quả từng tiêu chí

| # | Phiên bản | Đầu vào | Kỳ vọng quan sát được | Thực tế | Bằng chứng và mức | Kết quả |
|---:|---|---|---|---|---|---|
| 1 | Channel scan v1 | Danh sách tài nguyên quét | Page và Group được tách rõ; không gọi Group là Page | 4 mục ghi “Page lead”; 6 mục ghi Group; PHỔ CẬP AI ghi rõ Group, không phải Fanpage | Đọc trực tiếp bảng trong channel scan **E1** | **PASS** |
| 2 | Channel scan v1 | URL/ID tài nguyên | Có URL/ID thì ghi; thiếu phải ghi CHƯA XÁC MINH, không suy đoán | 4 Page đều ghi CHƯA XÁC MINH; 4/6 Group có ID số, 2 Group chỉ có slug và ID CHƯA XÁC MINH | Channel scan **E1** | **PASS** về cách biểu diễn; độ đúng URL/ID Facebook thực **NOT CHECKED** |
| 3 | Channel scan v1 | Bằng chứng sở hữu/quyền | Không đồng nhất “thấy tên/member” với owner/admin | Artifact nói rõ “Trang của bạn” chưa chứng minh capability cụ thể; `role_hint=member` không chứng minh owner/admin/mod | Channel scan **E1**; kết luận giới hạn quyền **E3** | **PASS** về kiểm soát suy diễn; sở hữu thực **NOT CHECKED** |
| 4 | Channel scan v1 | Kênh Nam Tam Điệp | Không thấy phải ghi đúng phạm vi nguồn, không kết luận không tồn tại | Ghi “không thấy trong nguồn đã quét”, không gán bừa một Page/Group | Channel scan, mục Kết luận **E1** | **PASS** |
| 5 | Trend evidence v1 | Nguồn S1 | Nguồn cơ quan nhà nước, ngày và nội dung chính khớp | URL Bộ Công an mở được; hiển thị Thông tư 12/2025 ban hành 28/02/2025, hiệu lực 01/03/2025 và thay đổi phân hạng từ 01/01/2025 | Web fetch trực tiếp S1 **E1** | **PASS** |
| 6 | Trend evidence v1 | Nguồn S2 | Các lớp sát hạch hạng B được nguồn hỗ trợ | Trang PBGDPL Hà Nội mở được; nêu lý thuyết, trong hình, trên đường và mô phỏng cho hạng B | Web fetch trực tiếp S2 **E1** | **PASS** |
| 7 | Trend evidence v1 | Nguồn S3 | Phải gắn “dự thảo/đề xuất”, không viết thành quy định hiện hành | URL Bộ Công an mở được, tiêu đề và thân bài nói đang xây dựng dự thảo; báo cáo và caption không biến chi tiết này thành quy định hiện hành | Web fetch S3 + artifact **E1** | **PASS** |
| 8 | Trend evidence v1 | Tuyên bố xu hướng | Chỉ gọi là xu hướng chính sách; không suy diễn nhu cầu/viral/tăng trưởng địa phương | Báo cáo giới hạn rõ: không có dữ liệu tìm kiếm, Insights, tuyển sinh hay khảo sát Nam Tam Điệp | Trend evidence **E1**; đánh giá tính thận trọng **E3** | **PASS** |
| 9 | Trend evidence v1 | Hiệu lực pháp lý hiện tại | Có văn bản gốc/hợp nhất còn hiệu lực nếu khẳng định pháp lý tại ngày đăng | QA mới đọc bài truyền thông cơ quan nhà nước; chưa đọc văn bản gốc/hợp nhất và S4 timeout | Trend evidence + nhật ký QA **E1** | **NOT CHECKED** |
| 10 | Draft v1.0 | Địa phương hóa | Chỉ dùng địa danh ở mức có căn cứ; không bịa sân thi/tuyến/nhu cầu | Caption chỉ nói “người… tại Nam Tam Điệp”, không nêu địa điểm, tuyến, lượng nhu cầu hay điểm thi | Draft v1.0 **E1** | **PASS** |
| 11 | Draft v1.0 | Nội dung kỹ năng | Bám nguồn, không cam kết hoặc tư vấn pháp lý | 4 nhóm gồm lý thuyết, trong hình, đường thực tế, văn hóa/an toàn; có cảnh báo quy định thay đổi | Draft + S2 **E1** | **PASS** |
| 12 | Draft v1.0 | CTA | CTA không thu PII, không hứa tư vấn/lịch khi chưa có năng lực trực | CTA chỉ hỏi nhóm kỹ năng khó nhất và dặn không chia sẻ thông tin cá nhân | Draft v1.0 **E1** | **PASS** |
| 13 | Draft/checklist v1 | Asset | Có phương án an toàn và yêu cầu quyền; asset cuối phải có manifest | Có gợi ý infographic tự thiết kế/ảnh được cấp phép; chưa có file cuối, giấy phép hay manifest | Draft/checklist **E1** | **NOT CHECKED** đối với quyền asset cuối |
| 14 | Draft/checklist v1 | Kiểm duyệt | Phân biệt hiện hành–dự thảo; cấm claim chưa chứng minh; kiểm lại nguồn trước đăng | Checklist và draft ghi đủ; caption không chứa số liệu dự thảo, học phí, lịch, tỷ lệ đỗ, bao đỗ | Draft/checklist **E1** | **PASS** |
| 15 | Draft v1.0 | Phù hợp thương hiệu/kênh | Có URL/ID, lịch sử nội dung và brand voice để đối chiếu | Chưa có kênh đích, bài gần đây, tên thương hiệu hay bộ nhận diện | Channel scan + draft **E1** | **NOT CHECKED** |
| 16 | Toàn bộ v1 | Ranh giới quyền | Gắn nhãn nội bộ, không coi PASS là duyệt đăng; không có thao tác ngoài | Các artifact đều ghi KHÔNG GẮN KÊNH / NOT PUBLISH-READY và cần phê duyệt riêng | Bốn artifact **E1** | **PASS** |
| 17 | Toàn bộ v1 | Bằng chứng không thao tác ngoài | Có log độc lập chứng minh không đăng/gửi/lên lịch/đổi cấu hình | Channel scan chép `writes_last_hour=0`; không có log publish/runtime độc lập trong gói QA | Channel scan **E1** cho nội dung artifact; suy luận không có thao tác **E3** | **NOT CHECKED** ở cấp hệ thống |

## 3. Ca kiểm soát ngoại lệ

| Ca | Đầu vào giả/quan sát | Kỳ vọng | Thực tế | Bằng chứng | Kết quả |
|---|---|---|---|---|---|
| Luồng đúng | Caption hiện tại chỉ hỏi kỹ năng khó nhất | Không thu PII, không hứa dịch vụ | Khớp kỳ vọng | Draft v1.0 **E1** | **PASS** |
| Thiếu bằng chứng | Không có URL/ID kênh và manifest asset | Chặn publish-ready | Artifact gắn NOT PUBLISH-READY | Draft/checklist **E1** | **PASS** |
| Thiếu phê duyệt | Không có phê duyệt đăng | Không đăng/gửi/lên lịch | Artifact chỉ kiến nghị và yêu cầu duyệt riêng | Bốn artifact **E1** | **PASS** về thiết kế tài liệu; enforcement runtime **NOT CHECKED** |
| Trùng mã | Hai tài nguyên có cùng Page/Group ID | Phát hiện và chặn ghi registry | Không có registry/batch ghi và không chạy workflow | Không có đầu ra runtime | **NOT CHECKED** |
| Timeout sau khi bên nhận đã lưu | Mô phỏng retry sau lưu | Không đăng/ghi trùng; có idempotency/reconciliation | Không có workflow gửi/đăng trong phạm vi | Không có đầu ra runtime | **NOT CHECKED** |

## 4. Lỗi chặn, chủ xử lý và điều kiện thử lại

1. **Kênh đích/ownership/capability chưa xác minh — chặn xuất bản.** Chủ xử lý: phụ trách Kênh & Kết nối. Thử lại khi có URL/ID tường minh và bằng chứng quyền/capability chỉ đọc hoặc publish đúng phạm vi.
2. **Asset cuối chưa có manifest/quyền — chặn xuất bản.** Chủ xử lý: phụ trách Nội dung & Cộng đồng. Thử lại khi có file cuối, nguồn/chủ sở hữu, giấy phép, phạm vi Facebook, thời hạn, consent và người duyệt.
3. **Hiệu lực pháp lý tại ngày đăng chưa đối chiếu văn bản gốc/hợp nhất — chặn claim pháp lý cụ thể.** Chủ xử lý: biên tập/đầu mối chuyên môn. Thử lại bằng văn bản chính thức còn hiệu lực tại ngày dự kiến đăng.
4. **Brand fit và năng lực trực chưa kiểm — chặn CTA nhắn tin/tuyển sinh.** Thử lại sau khi có lịch sử bài, brand voice, người trực và quy trình PII/escalation.
5. **Runtime chống đăng trùng/thiếu duyệt/timeout chưa thử — chặn mọi mở rộng tự động hóa.** Chỉ thử bằng sandbox/dữ liệu giả, không dùng hệ thống thật.

## 5. Kết luận và bàn giao

| Mã việc | Đầu ra/phiên bản | Tiêu chí | Bằng chứng | Kết quả | Trạng thái | Lỗi còn lại/điều kiện thử lại |
|---|---|---|---|---|---|---|
| FB-DRIVING-B-NAM-TAM-DIEP-V1-QA | 4 artifact v1 + QA v1.0 | Phân loại, nguồn, caption, CTA, kiểm duyệt, ranh giới quyền | Đọc trực tiếp artifact và ba URL S1–S3 **E1**; nhận định tổng hợp **E3** | Đủ dùng làm nháp nội bộ; chưa đủ publish-ready | **CHỜ NGHIỆM THU** | Các lỗi chặn 1–5 ở trên |

**Kiến nghị cho Trưởng nhóm:** chấp nhận gói này cho **sử dụng nội bộ/chỉ đọc và soạn nháp**. Không kiến nghị đăng, gửi, lên lịch, ghi registry, mở quyền hoặc mở rộng tự động hóa. Các tiêu chí ownership, kênh Nam Tam Điệp, asset rights, brand fit, hiệu lực pháp lý tại ngày đăng và runtime vẫn **CHƯA ĐỦ BẰNG CHỨNG/NOT CHECKED**.

**Đường quay về quy trình trước:** tiếp tục giữ bản nháp local không gắn kênh; không chuyển sang gói publish. Nếu bất kỳ kiểm tra lại nào trượt, bỏ thay đổi dự kiến và quay về checklist/content draft v1.0 ở trạng thái NOT PUBLISH-READY.
