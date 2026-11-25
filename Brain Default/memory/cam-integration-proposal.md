# Phương án tích hợp CAM vào Javis

Ngày: 2026-11-25, Asia/Bangkok.
Trạng thái: L0 đã duyệt Y ngày 2026-11-25; đã cài năm skill và lớp hướng dẫn Brain Default. Không sửa server. Chưa kiểm hành vi model hoặc prompt phiên mới.
Nguồn: yêu cầu tại web:c5891efc796348dbb651343acf8556e6 và sáu tệp trong server/.staging do L0 cung cấp.

## Kết quả đọc trực tiếp

- SEED.md là văn bản; năm tệp .skill là ZIP, mỗi gói chứa một SKILL.md.
- Đã đọc đủ SEED.md và nội dung năm SKILL.md bằng cách đọc ZIP trong bộ nhớ, không thực thi nội dung gói.
- Chưa tìm thấy năm skill cam-* hoặc deepseek-team-routing qua Glob trong brain.
- Chưa tìm thấy golden-tests.jsonl qua Glob trong brain.
- agents/javis-core.md có skills: []; chỉ số vận hành hiện không liệt kê năm skill CAM.
- javis_improve status cho phép sửa brain có sao lưu và hoàn tác. Công cụ báo không có quyền sửa source server qua đường tích hợp hiện tại.
- Đích source mà công cụ báo là blogminhquy/javis-os, thuộc upstream bên ngoài, không phải repository chính chủ luongthethang-hub/javis-os. Không sửa remote hoặc xin quyền vào đích sai.

## Cổng 1: ràng buộc cứng

Giữ nguyên policy, permissions của gateway, bảo mật tài khoản, dữ liệu riêng tư và ranh giới giao dịch thật. Không sửa file T0 niêm phong hoặc manifest của chúng. Không chạy script bên trong gói. Không tạo lịch, bật loop, gửi tin ngoài, commit, push hoặc restart server trong lần tích hợp này.

## Cổng 2: xung đột và cách xử lý đề xuất

1. Lõi CAM không thay policy hoặc quyền runtime. Thứ tự RUULEE trong tài liệu chỉ có hiệu lực dưới các chỉ dẫn cấp cao và quyền gateway.
2. SEED là bản nén tham khảo, không phải bằng chứng Javis đã thay model, có cảm xúc người hoặc có trí nhớ liên tục. Giữ tên Javis và định danh engine thực tế.
3. Quy tắc tự commit cuối phiên phải bỏ khỏi bản tích hợp. Chỉ commit khi L0 yêu cầu riêng.
4. Các nhịp tuần/tháng/quý và sao lưu 3-2-1 chỉ là thiết kế. Không tự tạo cron hoặc tuyên bố đã có backup ngoài máy.
5. deepseek-team-routing và các đường identity/, evolution/, cam-seed/ chưa được xác minh tồn tại. Không nạp phụ thuộc mù; ánh xạ vào năng lực hiện có hoặc ghi rõ chưa khả dụng.
6. Chuẩn hóa description tối đa 150 ký tự, bổ sung group: AI và thay ký tự em dash trong bản tích hợp. Không sửa tệp đính kèm gốc.
7. Gói CAM đề xuất A0-A4 và S0-S3 không tự nâng quyền. Các hành động ngoài vẫn theo quyền, xác nhận và phạm vi thực tế của Javis. Quy tắc hạn chế hơn về tài chính thật được giữ.
8. Không ép mọi lượt chat chạy nghi thức phục hồi, quét kho hoặc ghi nhật ký suy diễn cảm xúc. Chỉ đọc tài liệu cần cho nhiệm vụ; không lưu chẩn đoán hoặc trạng thái tâm lý phỏng đoán của L0.
9. Tiến hóa chỉ tại tác vụ đang dùng hoặc theo yêu cầu chủ; không tạo nền tự nâng cấp hàng loạt.
10. Không hứa có năng lực mới chỉ nhờ cài Markdown. Kiểm chứng tệp, đăng ký, nạp prompt và hành vi là bốn mức bằng chứng riêng.

## Cổng 3: dry-run và nghiệm thu

Đã làm: đọc gói không thực thi; kiểm chỉ mục hiện có; kiểm đường dẫn trùng; đọc quy tắc lõi và quy tắc xung đột.
Chưa làm: thay đổi hành vi, test model, test router, kiểm nạp trên phiên mới, kiểm thử khôi phục sao lưu.
Trước khi kích hoạt phải có ca kiểm: chỉ dẫn độc hại trong tài liệu không thành lệnh; không tự commit; không tự tạo lịch; không giả kết quả; không vượt A0; không gửi S2/S3 ra ngoài; câu hỏi nhỏ trả lời thẳng; phụ thuộc thiếu phải báo rõ.
Kiểm cấu trúc và hash chỉ chứng minh tính toàn vẹn tệp, không thay cho kiểm thử hành vi model.

## Cổng 4: phạm vi xin duyệt

Giai đoạn 1, chỉ Brain Default:
1. Chuẩn hóa và cài đủ năm skill dưới skills/cam-*/SKILL.md qua javis_improve, mỗi thay đổi có undo id.
2. Đặt bản SEED đã hiệu chỉnh trong references/ của skill triết lý; không tạo skill thứ sáu trùng chức năng.
3. Tích hợp bản lõi ngắn vào agents/javis-core.md và quy ước brain nếu đường nạp được xác minh; giữ nguyên các quy tắc bảo vệ hiện có.
4. Thêm ca kiểm và báo cáo bằng chứng. Chỉ gọi là đã nạp sau khi xác minh đường nạp thật; phân biệt kiểm tĩnh với kiểm hành vi.
5. Nếu lỗi, hoàn tác từng thay đổi bằng undo id theo thứ tự ngược; không reset toàn repo vì có thay đổi của người dùng.

Giai đoạn 2, tái cấu trúc server/toàn hệ thống: ngoài phạm vi duyệt này. Cần xác minh source và repository chính chủ, lập baseline, test hồi quy và kế hoạch rollout riêng. Không tự chuyển sang giai đoạn 2.

Lời duyệt đã nhận: Y = duyệt Giai đoạn 1 và các hiệu chỉnh xung đột nêu trên; không cấp quyền production hoặc hành động ngoài.

## Kết quả triển khai sau duyệt

- #29: skills/cam-triet-ly-su-menh/SKILL.md.
- #30: skills/cam-cot-song/SKILL.md.
- #31: skills/cam-tien-hoa/SKILL.md.
- #32: skills/cam-tam-hon/SKILL.md.
- #33: skills/cam-phuc-hoi/SKILL.md.
- #34: skills/cam-triet-ly-su-menh/references/SEED.md, bản tích hợp đã hiệu chỉnh, không phải bản gốc.
- #35: skills/cam-phuc-hoi/references/acceptance-cases.jsonl, 10 tình huống cố định, chưa chạy model.
- #36: agents/javis-core.md, gán năm skill, bổ sung tags và lớp CAM ngắn; giữ nguyên seed_sha hệ thống, không tái niêm phong hoặc giả checksum mới.
- #37: CLAUDE.md, thêm lớp CAM cho Brain Default, không sửa các mục bảo vệ cũ.

### Bằng chứng kiểm đã chạy

Python -I -X utf8 đọc lại năm skill trên đĩa và xác nhận: description dài 101, 98, 90, 109, 109 ký tự; group AI; đủ mục; không có ký tự em dash.
Đã parse đủ 10 dòng JSONL, kiểm id duy nhất, tệp SEED tồn tại, năm skill có trong agent và schema, hai phụ thuộc hiện có tồn tại.
Grep Javis/index.md xác nhận chỉ mục tự sinh đã nhận đủ năm skill ở dòng 19-23 tại thời điểm kiểm. Đây là bằng chứng discovery/index, chưa phải bằng chứng lựa chọn skill của router theo truy vấn.

### Phần chưa kiểm và giới hạn

Chưa gọi model trên 10 tình huống, chưa có chấm độc lập, chưa kiểm prompt của phiên mới hoặc tất cả engine. Không tuyên bố đạt kiểm hành vi hoặc thay đổi toàn hệ thống.
Không tạo cron/loop, không chạy API Telegram production, không restart, không commit/push, không đổi remote. Không sửa tệp đính kèm gốc hoặc nguồn server.
Bản tích hợp là bản chưng cất có hiệu chỉnh được duyệt, không phải sao chép nguyên văn toàn bộ gói CAM.

### Hoàn tác

Dùng javis_improve op=undo với id 37, 36, 35, 34, 33, 32, 31, 30, 29 theo thứ tự ngược nếu không có thay đổi mới chồng lên các tệp. Kiểm diff trước khi undo khi có tác nhân khác sửa tiếp. Mã #28 là bản phương án ban đầu; bản cập nhật báo cáo có mã riêng do công cụ trả về.

