# Đề xuất phản biện chéo Claude và ChatGPT

Trạng thái đề xuất chờ Chủ duyệt. Phạm vi là bản nháp, diff và bằng chứng nội bộ của một việc. Thời hạn dưới đây là ngưỡng đề xuất cho đợt thử, có thể điều chỉnh sau khi đo.

## Ba lượt và thời hạn

Quy trình bắt đầu khi có bản giao. Điều phối ghi mã việc, mục tiêu, tiêu chí chấp nhận, phiên bản hoặc hash, đường dẫn bản giao và nguồn bằng chứng. Giữ bản gốc để đối chiếu. Hai vai có thể đổi chiều theo việc nếu mỗi vai đã xác nhận được tuyến chạy thuê bao tương ứng.

| Lượt | Người thực hiện | Kết quả cần lưu |
|---|---|---|
| 1 | Reviewer dùng họ model còn lại | Rà độc lập, ghi từng điểm phản đối theo mức độ, vị trí, bằng chứng, ảnh hưởng và cách kiểm lại. Chốt được ngay nếu đủ bằng chứng và không có lỗi chặn. |
| 2 | Tác giả | Trả lời từng phát hiện, ghi lý do đồng ý hoặc phản đối. Nếu sửa, giao phiên bản mới, diff và bằng chứng kiểm lại. |
| 3 | Reviewer ở lượt 1 | Kiểm lại diff và các phát hiện còn mở trên phiên bản mới nhất. Chốt `ĐẠT`, `CHƯA ĐẠT` hoặc `THIẾU BẰNG CHỨNG`. |

Giới hạn 5 phút mỗi lượt và 15 phút từ lúc mở phản biện, tính cả thời gian chờ. Lượt chạy lỗi hoặc hết hạn vẫn tính vào trần 3 lượt. Khi hết hạn, đóng vòng, giữ kết quả một phần và bỏ qua kết quả về muộn trong phán quyết đã chốt. Dùng `CHƯA ĐẠT` nếu đã có lỗi chặn được chứng minh, dùng `THIẾU BẰNG CHỨNG` nếu thiếu kết quả để kết luận. Nếu có bản sửa sau lượt 2 mà lượt 3 không chạy được, ghi rõ bản mới chưa được rà lại. Chủ duyệt kết quả cuối cùng.

## Xác nhận hai họ model và xử lý lỗi tuyến chạy

- Trước khi áp dụng, chạy một việc ngắn trên mỗi tuyến thuê bao qua **chính đường chạy của nhóm**, dùng dữ liệu mẫu và yêu cầu một kết quả kiểm tra được. Lưu thời điểm, mã lượt, engine, provider, model thực chạy do runtime ghi nhận, chế độ xác thực thuê bao và trạng thái hoàn tất hoặc lỗi. Kiểm tra tên model trong frontmatter chỉ xác định tuyến dự kiến.
- Với từng việc, chỉ ghi **đã xác nhận phản biện chéo mô hình** khi có bằng chứng runtime cho cả lượt tạo bản đang xét và lượt rà phiên bản đó, một model thuộc họ Anthropic Claude và một thuộc họ OpenAI. Nếu tác giả sửa, kiểm tra lại bằng chứng cho bản sửa và lượt rà lại. Tên agent, cấu hình hoặc lời model tự khai chỉ dùng làm thông tin tham khảo.
- Nếu tuyến báo hết hạn đăng nhập, hết quota, model không được hỗ trợ hoặc timeout, ghi nguyên lỗi khi có và báo ngay trong nhóm. Nếu còn lượt và thời gian, có thể dùng một tuyến thuê bao đã kiểm chứng và đã được Chủ duyệt. Nếu chỉ đủ điều kiện rà độc lập theo vai trò bằng cùng họ model hoặc thiếu dữ liệu runtime, ghi **chưa xác nhận phản biện chéo mô hình**. Nếu không còn tuyến được phép, giữ bản giao, chốt trạng thái theo bằng chứng và trả Chủ quyết. Dừng khi hết ngân sách lượt hoặc thời gian. Giữ nguyên cấu hình, tuyến API trả theo token, quyền và ứng dụng trong phạm vi đã duyệt.

### Bằng chứng hiện có

- Tệp agent hiện ghi `anthropic-cli` / `sonnet` cho Kỹ sư EA và `openai-oauth` / `gpt-6.2-sol` cho Reviewer. Bản rà soát hiện trạng ghi Reviewer là `gpt-5.5`. Đây là hai ghi nhận cấu hình khác nhau, cần xác nhận bằng lượt chạy thực tế. [Kỹ sư EA](../../agents/ky-su-ea---claude.md), [Reviewer](../../agents/phan-bien-cheo---chatgpt.md), [Bản rà soát hiện trạng](evo-bootstrap-data-check.md).
- Tin hệ thống #231 và #232 ghi `Codex: The 'gpt-5.5' model is not supported when using Codex with a ChatGPT account.` Lỗi xác nhận cấu hình model đó bị từ chối ở các lượt được báo. Khả dụng của Claude và tuyến OpenAI với model hiện ghi trong tệp vẫn **không xác định**. Hai phép thử trên sẽ kiểm chứng riêng từng tuyến.

## Biên bản tối thiểu

Lưu cùng thư mục đầu ra nội bộ của việc, một dòng cho mỗi lượt và mỗi phát hiện liên quan. Phân biệt lỗi quan sát được, giả định và phần thiếu bằng chứng.

| Mã việc / bản / lượt | Người đề xuất / nội dung | Người phản đối / lý do | Mức độ / vị trí / bằng chứng | Phản hồi / cách kiểm lại | Provider / model thực chạy / mã log | Kết quả / lỗi còn mở |
|---|---|---|---|---|---|---|
| Điền thông tin thực tế | Agent và nội dung hoặc cách sửa | Agent, lập luận và điều kiện đổi kết luận | Ghi diff, nguồn hoặc log có thể đối chiếu | Cách sửa, người thực hiện và kết quả kiểm | Ghi `không xác định` nếu thiếu log | Phán quyết theo đúng phiên bản |

**Bước tiếp theo**

Chủ quyết có duyệt thử hai tuyến bằng hai việc mẫu, sau đó dùng một bản giao nội bộ để thử giới hạn 3 lượt và 15 phút hay không.
