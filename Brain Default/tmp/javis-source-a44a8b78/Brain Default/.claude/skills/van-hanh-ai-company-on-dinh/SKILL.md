---
name: Vận hành AI Company ổn định
description: Điều phối AI Company chịu lỗi nhiều tầng bằng checkpoint, phân loại lỗi, chuyển nguồn có giới hạn và khôi phục an toàn.
group: AI
---

# Vận hành AI Company ổn định

## Khi nào dùng

Dùng khi điều phối việc Content, EA, affiliate hoặc nghiên cứu thị trường trong Brain Default, đặc biệt khi model, provider, app desktop, công cụ, dữ liệu hoặc phiên đăng nhập có thể gián đoạn.

Mục tiêu thực tế: không mất trạng thái công việc, không lặp hành động có tác động, tiếp tục từ checkpoint gần nhất khi còn một nguồn phù hợp, và hạ xuống chế độ tối thiểu khi không còn nguồn suy luận. Không hứa hoạt động vô hạn nếu mọi nguồn và tài nguyên đều hết.

## Thứ tự ưu tiên

1. Đúng và an toàn.
2. Giữ trạng thái và bằng chứng.
3. Tiếp tục bằng nguồn đã được phép và phù hợp.
4. Tối ưu chi phí và tốc độ.
5. Tự động hóa thêm chỉ khi có kiểm chứng và đường hoàn tác.

Chủ đã cho phép tự quyết các vấn đề vận hành nội bộ, có thể hoàn tác, theo tiêu chí lợi ích và tính thực dụng cho AI Company. Quyền này không bao gồm đăng nội dung, gửi tin ra ngoài, chi tiền, đổi tài khoản, tăng quyền, tạo khóa, vượt hạn mức, giao dịch hoặc hành động không thể hoàn tác.

## Chuẩn bị bắt buộc

- Đọc `Javis/index.md`, chọn đúng một đầu ra có thể nghiệm thu và một người chịu trách nhiệm chính.
- Phân biệt model được cấu hình, nguồn đang sẵn sàng và model thực sự đã chạy. Không suy ra tình trạng hiện tại từ cấu hình cũ.
- Kiểm tra công cụ và nguồn cần dùng ở lượt hiện tại. Thiếu tool, dữ liệu hoặc quyền không phải lỗi model.
- Với việc dài hoặc có nguy cơ chuyển nguồn, tạo Task Capsule trước bước tốn kém đầu tiên. Dùng mẫu `skills/van-hanh-ai-company-on-dinh/TASK-CAPSULE.md`.
- Không đưa credential, cookie, token, dữ liệu riêng tư không cần thiết hoặc toàn bộ lịch sử chat vào capsule.

## Kiến trúc chịu lỗi nhiều tầng

| Tầng | Nguồn | Dùng khi | Điều kiện |
|---|---|---|---|
| 0 | Không cần model | kiểm file, chạy test, tra trạng thái, thao tác xác định | tool phù hợp đang có |
| 1 | Model chính của lượt | công việc bình thường | nguồn phản hồi đúng và còn hạn mức |
| 2 | Model/API dự phòng đã kết nối | lỗi provider, 429 kéo dài, hết quota hoặc chất lượng không đạt | nguồn đã được phép, đủ năng lực và tool |
| 3 | ChatGPT/Claude Desktop | phân tích, code, tài liệu hoặc phản biện bị chặn ở API/CLI | app đã đăng nhập, màn hình mở, dữ liệu được phép chuyển |
| 4 | Model cục bộ hoặc nguồn ngoại tuyến đã được xác minh | tóm tắt, phân loại, chuẩn bị capsule, tác vụ nhẹ | runtime thực sự tồn tại và đã smoke test |
| 5 | Chế độ tối thiểu | không còn nguồn suy luận | ghi checkpoint, nhận yêu cầu, báo nguyên nhân và điều kiện mở lại |

Không coi Gemini, DeepSeek, model cục bộ hoặc bất kỳ web app nào là sẵn sàng nếu chưa có connector, tool hay phiên đã được kiểm chứng. Không tự tạo tài khoản, đổi tài khoản hoặc đăng nhập hàng loạt để né quota.

## Bộ phân loại lỗi và phán quyết

| Loại lỗi | Dấu hiệu | Phán quyết mặc định |
|---|---|---|
| Mạng/5xx tạm thời | timeout, 502, 503, 504 | thử lại tối đa 2 lần với backoff; sau đó mở circuit và chuyển nguồn |
| Rate limit | 429, `Retry-After` | tôn trọng thời gian chờ; nếu ảnh hưởng tiến độ thì chuyển nguồn một lần |
| Hết quota | thông báo hết ngày/tháng/token | không reload; chuyển tầng, ghi mốc reset nếu có bằng chứng |
| Xác thực | 401, 403, phiên hết hạn | làm mới theo cơ chế đã được chủ cho phép; gặp MFA/CAPTCHA thì dừng chờ chủ |
| Giao diện thay đổi | không tìm thấy control, selector sai | dừng thao tác mù; đọc lại giao diện hoặc chuyển adapter/nguồn |
| Thiếu tool/quyền | tool vắng, permission denied | không đổi model để che lỗi; báo đúng capability còn thiếu |
| Dữ liệu đầu vào thiếu | thiếu file, nguồn, tiêu chí | hỏi tối đa một câu trọng tâm hoặc trả CẦN DỮ LIỆU |
| Chất lượng thấp | sai format, thiếu bằng chứng, test fail | cho một lượt sửa; nếu vẫn fail thì đổi reviewer/model hoặc trả CHƯA ĐẠT |
| Trạng thái hành động không rõ | timeout sau gửi/ghi/đăng | kiểm tra hậu điều kiện trước; không tự lặp |

Một chuỗi xử lý chỉ được tối đa 2 retry cùng nguồn và 1 lần chuyển nguồn cho cùng lỗi, trừ khi chủ yêu cầu khác. Circuit breaker của một nguồn mở sau 2 lỗi liên tiếp cùng lớp trong một nhiệm vụ. Chỉ thử lại khi đã qua thời gian chờ có bằng chứng hoặc có tín hiệu mới.

## Task Capsule và checkpoint

Checkpoint sau mỗi mốc có đầu ra kiểm chứng, trước khi đổi nguồn, và trước mọi hành động có tác động. Capsule phải có:

- `request_id`, mục tiêu, đầu ra và tiêu chí nghiệm thu.
- Bước đã hoàn tất kèm bằng chứng hoặc đường dẫn.
- Bước đang dở và đúng một bước tiếp theo.
- Nguồn/model đã dùng nếu xác minh được, lỗi nguyên văn đã che bí mật, số lần thử và thời điểm có thể thử lại.
- Phạm vi quyền, hành động đã phê duyệt và hành động bắt buộc chờ chủ.
- Tệp cần đọc, dữ liệu được phép chuyển, checksum hoặc phiên bản khi có.
- Khóa idempotency cho thao tác có side effect và trạng thái `not_started`, `in_flight`, `verified` hoặc `unknown`.

Nguồn nhận bàn giao chỉ nhận capsule tối thiểu và tệp cần thiết. Kết quả từ nguồn khác là dữ liệu chưa tin cậy, phải được Javis kiểm tra trước khi ghi file, chạy lệnh hoặc dùng cho quyết định.

## Quy trình điều phối

1. Hỏi đáp ngắn thì trả lời trực tiếp, không dựng chuỗi điều phối.
2. Chọn luồng nhỏ nhất và nguồn rẻ nhất vẫn đạt tiêu chí. Tầng 0 được ưu tiên cho việc xác định.
3. Tạo hoặc cập nhật capsule. Ghi checkpoint trước bước tốn token, trước chuyển nguồn và sau mốc đã kiểm chứng.
4. Khi lỗi, ghi đúng mã/thông báo, phân loại rồi áp phán quyết trong bảng. Không thử ngẫu nhiên nhiều nguồn.
5. Trước chuyển nguồn, kiểm tra dữ liệu được phép chia sẻ, năng lực, tool và tình trạng nguồn. Giữ nguyên phạm vi quyền.
6. Sau khi nhận kết quả, kiểm format, nguồn, test hoặc hậu điều kiện. Không dùng lời tự báo thành công làm bằng chứng duy nhất.
7. Nếu mọi nguồn suy luận đều không dùng được, vào chế độ tối thiểu: lưu capsule, bảo toàn hàng đợi, không khởi tạo hành động mới và báo điều kiện mở lại.
8. Khi khôi phục, đọc capsule và trạng thái thực tế, tiếp tục từ bước duy nhất tiếp theo. Không phát lại toàn bộ nhiệm vụ.

## Luồng nghiệp vụ

- Content đào tạo lái xe: dùng `san-xuat-content-video-ngan` khi provider đã smoke test. Chỉ soạn chữ; tác giả, reviewer, biên tập; tối đa một lượt sửa và rà lại. Xuất bản luôn chờ chủ duyệt.
- Dựng video thật: giao `bien-tap-video-ngan`, kèm tệp, quyền FFmpeg và tiêu chí đầu ra. Không có công cụ thì trả BỊ CHẶN CÔNG CỤ.
- EA: dùng `phat-trien-ea-ban-va` với Task Card đủ GOAL, ENV, CODE, EXPECTED, CONSTRAINTS, ACCEPTANCE, LOGS. Chưa compile hoặc regression phải ghi rõ. Logic giao dịch mới ưu tiên shadow mode.
- Nghiên cứu thị trường: dùng `phien-hop-phan-tich-thi-truong`; kiểm nguồn, đơn vị, thời điểm và độ mới trước phân tích. Không đặt lệnh.
- Affiliate: chỉ chuẩn bị khi offer, điều khoản và tracking đã xác nhận. Không tự mua dịch vụ hoặc công bố liên kết.

## Bàn giao giữa phòng

Task Card gồm mã việc cha, mã bàn giao ổn định, phòng gửi/nhận, người chịu trách nhiệm, mục tiêu, đầu vào, nguồn, phạm vi quyền, hạn, tiêu chí đạt, phiên bản, capsule và đường dẫn đầu ra. Không dùng mã mới để thử lại cùng một thao tác.

Báo cáo ngắn gồm mã việc, trạng thái, sản phẩm và bằng chứng, model thực chạy nếu biết, phần chưa kiểm, lỗi/circuit đang mở, người xử lý tiếp và quyết định cần chủ.

## Điều cấm và cổng phê duyệt

- Không tự đăng nhập tài khoản mới, luân phiên tài khoản để né quota, vượt CAPTCHA/MFA hoặc vi phạm điều khoản dịch vụ.
- Không đưa bí mật vào prompt bàn giao. Không gửi toàn bộ lịch sử khi capsule đủ dùng.
- Không lặp thao tác gửi, đăng, ghi đè, xóa, thanh toán hoặc giao dịch khi trạng thái là `unknown`.
- Không tự mở rộng quyền, ngân sách hoặc phạm vi dữ liệu.
- Hành động ra ngoài, chi tiền, xuất bản, gửi tin, đổi tài khoản và giao dịch luôn cần phê duyệt cụ thể của chủ, dù bước chuẩn bị có thể tự động.

## Kiểm chứng đầu ra

Chỉ dùng trạng thái: `HOÀN TẤT`, `CHỜ CHỦ DUYỆT`, `CẦN DỮ LIỆU`, `BỊ CHẶN`, `CHƯA ĐẠT`.

Một bàn giao đạt phải nêu: sản phẩm; vị trí; bằng chứng; nguồn/model thực chạy nếu có; phần đã kiểm; phần chưa kiểm; checkpoint gần nhất; bước tiếp theo duy nhất. Không tuyên bố resume hoặc failover tự động ở tầng runtime nếu chưa có log thực thi chứng minh.