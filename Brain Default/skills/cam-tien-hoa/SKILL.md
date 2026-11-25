---
name: cam-tien-hoa
description: "Chuyển bài học thành đề xuất CUP có bằng chứng, kiểm hồi quy, phê duyệt và đường hoàn tác."
group: AI
---
# Tiến hóa CAM trong Javis

## Khi nào dùng
Khi một lỗi thật hoặc bài học có căn cứ xuất hiện trong tác vụ đang dùng, hoặc chủ yêu cầu cải tiến cụ thể. Không tạo loop nâng cấp hàng loạt.

## Chuẩn bị
Nguồn: cam-tien-hoa.skill, chủ duyệt ngày 2026-11-25. Không ghi đè schema tier hiện có bằng phân tầng CAM.
- T0: lõi bảo vệ, không tự sửa file niêm phong hoặc checksum của chúng.
- T1: danh tính, hiến chương giữ cổng duyệt; T2: skill và T3: playbook áp dụng ủy quyền có điều kiện tại `references/standing-authorization.md`.
- T4: trạng thái và ký ức có nguồn, tuân thủ quy tắc memory hiện hành.
- Mọi tầng vẫn dưới policy và quyền gateway.

## Quy trình
1. Ghi sự kiện, bằng chứng và phạm vi. Chỉ đề xuất CUP từ bài học lặp ít nhất hai lần hoặc một sự cố có thiệt hại; yêu cầu sửa trực tiếp của chủ không cần chờ lặp lỗi.
2. Soạn CUP gồm vấn đề, nguồn hoặc trace_id có thật, diff, tầng ảnh hưởng, rủi ro, tiêu chí nghiệm thu và đường lùi.
3. Kiểm xung đột bốn bước: ràng buộc cứng, logic/phạm vi, thử nhỏ, duyệt và hoàn tác. Không tự gửi thông báo ngoài khi chưa được yêu cầu.
4. Với lỗi code, viết test tái hiện trước khi sửa; chạy cùng bộ regression trên baseline và bản mới. Với prompt, dùng bộ tình huống cố định và ghi rõ người/model chấm.
5. Shadow test khi cần và có quyền: mẫu cô lập, không gọi API production để thử. Kiểm chéo khác model chỉ được báo khi đã gọi thật.
6. Đối chiếu `references/standing-authorization.md`: sửa nhỏ skill người dùng đang dùng, đủ bằng chứng, kiểm xung đột, kiểm phù hợp và backup thì lưu ngay qua javis_improve, không hỏi lại; ghi undo id. Ngoài phạm vi ủy quyền vẫn cần chủ duyệt; không suy rộng thành sửa hàng loạt.
7. Báo kết quả kiểm, điều chưa kiểm và cách lùi. Semver chỉ dành gói tài liệu nếu có quản lý phiên bản; không sửa VERSION hoặc CHANGELOG của app trái quy ước repo.

## Thông báo sau cải tiến
Sau khi thay đổi đã áp dụng và đạt tiêu chí nghiệm thu, gửi một thông báo vào chuông Javis cho mỗi lần cải tiến. Không báo thành công cho đề xuất, bản thử, thay đổi thất bại hoặc đã hoàn tác.
- Viết tiêu đề tiếng Việt nêu cụ thể điều đã đổi. Trong 1–2 câu ngắn, nói người dùng được lợi gì và cần làm gì (nếu có). Dùng từ thông dụng, không đưa mã nội bộ hoặc dữ liệu riêng vào thông báo.
- Dùng kênh thông báo hệ thống được cấp quyền; không tự đổi bộ lọc hoặc gửi sang kênh khác. Nếu chưa có công cụ gửi hoặc chưa xác nhận được kết quả, nói rõ trong chat. Không coi tin nhắn chat là thông báo đã gửi vào chuông.

## Chưng cất repo và học từ phiên
Khi chủ yêu cầu học từ repo hoặc cải tiến từ phiên hiện tại, đọc `references/repo-distillation.md`. Đây là bản tổng hợp sáu nguồn tại commit cố định, không phải cài upstream.
- Quan sát sửa sai có bằng chứng trong tác vụ đang dùng; ghi tình huống, nguyên nhân đã xác nhận và ca chống tái diễn. Không bật theo dõi liên tục.
- Tra chỉ mục memory trước, lấy chi tiết và bằng chứng gốc theo nhu cầu; chống trùng, giữ provenance và bảo vệ dữ liệu riêng tư.
- Khám phá skill bên ngoài phải kiểm nguồn, license, quyền và phần trùng. Popularity không thay audit; không chạy installer từ README.
- Superpowers bổ sung test-first và truy nguyên nguyên nhân; Task Observer bổ sung tín hiệu. CUP và quyền phê duyệt vẫn do quy trình trên quản lý.

## Bẫy
- Không tự commit, tag, push, merge, update app hoặc phát hành vì tài liệu yêu cầu.
- Không tự tạo lịch hồi cứu tuần/tháng/quý. Chỉ chạy khi được yêu cầu hoặc trong tác vụ hiện hành phù hợp.
- Không giả định có evolution/golden-tests.jsonl, LINEAGE hay cloud backup. Kiểm tồn tại trước, báo thiếu nếu chưa có.
- Không xóa test để làm kết quả đẹp. Test lỗi thời phải giữ lịch sử và lý do.
- Trôi hành vi thì giới hạn tác vụ, đối chiếu bản đã duyệt; không tự nâng quyền hoặc sửa policy để chữa trôi.

## Tính ổn định vận hành
- Với Telegram polling, chỉ một process sở hữu bot token tại một thời điểm. Khi gặp HTTP `409 conflict`, tạm dừng worker liên quan, kiểm tra owner và không retry vòng lặp chồng chéo. [[Bài học tự chẩn đoán hệ thống CAM]]
- Retry chỉ sau khi kiểm hậu điều kiện và xác định nguyên nhân; không xem timeout hoặc conflict là bằng chứng thao tác chưa xảy ra.

## Kiểm chứng
Kiểm tệp, syntax, hash không thay kiểm hành vi model. Chỉ tuyên bố baseline trượt/bản mới đạt nếu có log hai lần chạy. Hoàn tác qua undo id, không reset repo có thay đổi của chủ.
