# Từ yêu cầu nội dung đến phiếu tư vấn | Trường lái giả định

**Đích bàn giao:** Tư vấn viên nhận được một câu hỏi cụ thể do người học chủ động nêu, không phải danh sách người tương tác. “B1” là cách gọi trong tình huống giả định; “cuối tuần” là lúc người hỏi rảnh, không phải lịch trường mở lớp.

| Chặng · Người chịu trách nhiệm | Đầu vào | Sản phẩm bàn giao | Bên nhận chấp nhận khi |
|---|---|---|---|
| 1. Lập yêu cầu · Trưởng nhóm nội dung | Mục tiêu: giúp người mới hỏi về lịch học phù hợp khi chỉ rảnh cuối tuần. | Bản yêu cầu `BR-B1-01`. | Người soạn tìm thấy đủ 5 mục: đối tượng, nhu cầu, mục tiêu bài, lời mời hỏi tư vấn tự nguyện, giới hạn thông tin được dùng. |
| 2. Soạn · Người viết nội dung | `BR-B1-01` | `POST-DRAFT-B1-01` kèm mã bản yêu cầu. Bài phải có đủ 4 thành phần: câu mở đúng nhu cầu, thông tin được phép dùng, gợi ý hình, lời mời hỏi tư vấn tự nguyện. | Người duyệt đối chiếu đủ 4 thành phần với bản yêu cầu; lời mời phù hợp, ví dụ: “Bạn muốn được tư vấn về khung giờ nào?” Không viết rằng trường có lớp cuối tuần. |
| 3. Duyệt · Người duyệt độc lập với người viết | Bản nháp và bản yêu cầu tại chặng 2. | `RV-B1-01` kèm bản nháp đã xét, quyết định và lý do. | Điều phối viên chỉ nhận bản ghi **Duyệt mô phỏng** khi đủ 4 thành phần, đúng mục tiêu, không ép đăng ký, không bịa dữ kiện, cam kết hay dùng dữ liệu thật. Nếu thiếu thành phần, chỉ rõ thành phần và câu cần sửa rồi trả người viết; chưa chuyển tiếp. |
| 4. Tiếp nhận giả lập · Điều phối viên Fanpage | Gói duyệt chặng 3 và câu hỏi mẫu bên dưới. | Phiếu `TN-B1-01` ghi nguyên văn câu hỏi, kèm mã bài và mã duyệt. | Người xét đối chiếu được nguồn, thấy nhãn “giả lập”, câu trích đầy đủ, không có thông tin định danh hay diễn giải thay người hỏi. |
| 5. Xét điều kiện · Người xét yêu cầu tư vấn | `TN-B1-01` | Phiếu `TV-GIALAP-001` gồm 4 trường: mã nguồn `TN-B1-01`; nhu cầu “muốn học B1 vào cuối tuần, cần tư vấn về lịch phù hợp và thủ tục đăng ký”; nguyên văn câu hỏi; kết luận “đủ điều kiện tư vấn”. | Chỉ chuyển phiếu khi câu trích chứng minh **cả nhu cầu học cụ thể lẫn lời chủ động xin tư vấn**. Chỉ khen bài, hỏi mẹo lái xe hoặc hỏi về biển báo: không tạo phiếu tư vấn. Thiếu bằng chứng: giữ phiếu tiếp nhận ở trạng thái “Chưa chuyển”, ghi mục thiếu, không tự điền. |
| 6. Bàn giao · Tư vấn viên tiếp nhận | `TV-GIALAP-001` và phiếu nguồn `TN-B1-01`. | Dòng xác nhận mẫu: “Đã nhận mô phỏng: TV-GIALAP-001. Cần xác minh lịch học và thủ tục trước khi soạn trả lời.” | Hoàn tất khi tư vấn viên đối chiếu đủ 4 trường với nguồn và nêu đúng hai việc cần xác minh. Nếu lệch, trả người xét, ghi rõ trường cần sửa. |

**Câu hỏi giả lập:** “Em làm văn phòng chỉ rảnh thứ Bảy và Chủ nhật, chưa từng cầm lái bao giờ. Nhờ trường tư vấn giúp em lịch học B1 cuối tuần và thủ tục đăng ký với ạ.”

**Thẻ giữ chỗ dùng chung ở cả 6 chặng:** Lịch học: `[LỊCH_CHƯA_XÁC_MINH]`; học phí: `[PHÍ_CHƯA_XÁC_MINH]`; thủ tục: `[THỦ_TỤC_CHƯA_XÁC_MINH]`. Khi thiếu dữ kiện, dùng đúng thẻ trong ghi chú nội bộ; không chèn thẻ vào lời người hỏi hoặc nội dung dành cho người đọc.

**Phạm vi:** Duyệt mô phỏng không cho phép đăng, liên hệ hay thay đổi hệ thống. Phiếu đủ điều kiện tư vấn không phải xác nhận đủ điều kiện học hoặc đăng ký.