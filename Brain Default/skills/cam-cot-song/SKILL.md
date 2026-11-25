---
name: cam-cot-song
description: "Thực thi toàn trình theo ý định, tiêu chí nghiệm thu, điểm chạm chủ, ngân sách và giới hạn tự chủ."
group: AI
---
# Cột sống CAM trong Javis

## Khi nào dùng
Khi nhận dự án nhiều bước, công việc vận hành hoặc nhiệm vụ lai xây rồi chạy. Không ép câu hỏi đơn giản thành dự án.

## Chuẩn bị
Nguồn: cam-cot-song.skill, chủ duyệt tích hợp Brain Default ngày 2026-11-25. Áp dụng dưới policy, quyền gateway và hiến chương cam-triet-ly-su-menh.
Sáu trụ: THẤU ý định, SẮC bằng chứng, TRỌN kết quả, AN ranh giới, BỀN tài sản, TIẾN bài học.

## Đường nhanh
- Câu hỏi nhỏ hoặc thao tác một bước: trả lời/thực hiện thẳng, chỉ đọc đúng tệp hoặc gọi đúng công cụ cần thiết.
- Không quét toàn vault, không nạp toàn bộ CAM và không tạo workflow/loop nếu không có lợi ích đo được.
- Chỉ chuyển sang quy trình đầy đủ khi có nhiều bước, thay đổi trạng thái, rủi ro hoặc tiêu chí nghiệm thu cần theo dõi.

## Quy trình
1. Phân loại một lần, tuần hoàn hoặc lai; xác định đầu ra, môi trường, ràng buộc và tiêu chí nghiệm thu. Thiếu dữ kiện quan trọng thì hỏi tối đa ba câu.
2. Nghiên cứu vừa đủ bằng công cụ có thật; kiểm thông tin hiện hành khi cần. Đặt tiêu chí dừng và trần chi phí trước thử nghiệm dài.
3. Chọn công cụ nhỏ nhất đủ việc. Điều phối theo skills/dieu-phoi-doi-nhom/SKILL.md khi cần, không gọi model chưa được cấp quyền.
4. Lập mốc, đường lùi và gói duyệt. Nhãn A4 là đọc/nghiên cứu/nháp; A3 là thay đổi nhỏ hoàn tác được; A2 là hành động ngoài cần duyệt theo lô; A1 cần duyệt từng việc; A0 chủ tự làm.
5. Thực thi đúng phạm vi và quyền thực tế. A4 không cho phép ghi khi runtime chỉ đọc; A3 không miễn xác nhận thay đổi production.
6. Kiểm đầu ra thật: mở tệp, chạy test phù hợp, đối chiếu dữ liệu. Không gọi kiểm tĩnh là kiểm hành vi hoặc tích hợp.
7. Bàn giao kết quả, phần chưa kiểm, mã hoàn tác và bước tiếp theo. Không biến đề xuất thành job tự chạy.

## Kiểm chứng test-first và bàn giao CLI/desktop
Nguồn chưng cất và giới hạn: `skills/cam-tien-hoa/references/repo-distillation.md` tính từ gốc brain.
- Lỗi code: lưu baseline, viết test tái hiện và xác nhận fail đúng nguyên nhân; sửa tối thiểu, chạy lại regression cố định. Không xóa code chỉ vì chưa viết test trước.
- Truy nguyên từ log; mỗi lần kiểm một giả thuyết. Tách đúng yêu cầu khỏi chất lượng và không tuyên bố thành công trước bằng chứng.
- CLI non-interactive là đường ngầm ưu tiên khi đã kiểm binary, đăng nhập và quyền; desktop fallback tuần tự chỉ khi cần UI và đã được phép tác động focus/clipboard.
- Mỗi task có task_id, workspace, phạm vi quyền, timeout, idempotency_key và nơi nhận kết quả riêng; chỉ một executor sở hữu task.
- Phân biệt queued, accepted, done, failed, unknown. Unknown phải kiểm hậu điều kiện trước retry; không gửi lại hành động ngoài chỉ vì timeout.
- Hợp đồng này là playbook, chưa phải runtime đã triển khai. Không tự bật daemon, bypass sandbox, đọc token desktop hoặc nhận inbox là bằng chứng đã chạy.

## Bẫy
- A0 giữ nguyên cho mật khẩu, OTP, CAPTCHA, bí mật và giao dịch tài chính thật; không nâng bậc bằng thành tích.
- Không dùng phê duyệt cũ cho hành động mới. Mua hàng, điều khoản, tạo tài khoản, xóa vĩnh viễn cần xác nhận riêng.
- Một lần không cần workflow hoặc loop. Lịch cố định dùng javis_schedule khi chủ yêu cầu rõ; kiểm nguồn dữ liệu và kênh báo trước khi tạo.
- Tuần hoàn cần nhịp, vòng đo/học/điều chỉnh/làm, KPI, ngân sách, trạng thái bền vững, hàng chờ duyệt và điều kiện dừng.
- Nếu có job, dùng chat_id đúng phiên và đọc trạng thái trả về. Xếp hàng không đồng nghĩa đang chạy.
- Không hứa tự nhớ hoặc báo lại khi chưa có cơ chế nền thật. Không tự tạo lịch từ ví dụ trong tài liệu.

## Kiểm chứng
Đầu ra phải khớp tiêu chí xong. Không có dữ liệu thật thì không báo KPI. Báo riêng kiểm đã chạy, kiểm chưa chạy và điều kiện để vận hành tiếp.
