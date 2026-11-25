# Chưng cất sáu nguồn được duyệt

Ngày: 2026-11-25. Chủ chọn phương án 1 tại web:c5891efc796348dbb651343acf8556e6.
Phạm vi: kiến thức vận hành trong Brain Default. Không cài executable, hooks, dịch vụ hoặc dataset của upstream.
Đây là bản tổng hợp diễn đạt lại, không phải bản sao đầy đủ hoặc chứng nhận an toàn mã nguồn.

## Nguồn cố định và ghi công
- ai-memory, akitaonrails, MIT: https://github.com/akitaonrails/ai-memory/tree/45a97cf8157ac646abc1633f430fc1a52a9f874a
- Find Skills, Vercel Labs, MIT: https://github.com/vercel-labs/skills/blob/57217cf86ba38148a57af9e90d14a4c049558330/skills/find-skills/SKILL.md
- Superpowers, obra, MIT: https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7
- Claude-Mem, thedotmack, Apache-2.0: https://github.com/thedotmack/claude-mem/tree/11b47f9f4b8dc3614fab7452647f578886468849
- UI UX Pro Max, nextlevelbuilder, MIT: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/8db36338810d0942567b97ce439affd1619fcf31
- One Skill to Rule Them All, Eoghan Henn / rebelytics.com, CC BY 4.0: https://github.com/rebelytics/one-skill-to-rule-them-all/tree/49d3c488af6311963e18e1a4fd9c309ff3c61b80

Căn cứ: README tại các commit trên; riêng Find Skills đọc SKILL.md. Giấy phép đối chiếu metadata GitHub. Chưa audit toàn bộ code hoặc dependency.
Phần học từ phiên được thích nghi từ Eoghan Henn / rebelytics.com, đã bỏ activation liên tục, hooks và cập nhật tự động. Ghi công và giấy phép cho phần thích nghi: https://creativecommons.org/licenses/by/4.0/ . Không hàm ý tác giả bảo trợ Javis.
Nếu sau này sao chép mã hoặc dataset, phải lấy và giữ LICENSE/NOTICE tương ứng trước khi phân phối; bản này không kèm mã/dataset upstream.

## Memory: ai-memory và Claude-Mem
- Giữ memory/MEMORY.md và facts hiện hữu làm nguồn chuẩn; không thêm kho ghi song song.
- Truy xuất tăng dần: chỉ mục ngắn, chi tiết liên quan, rồi bằng chứng gốc khi cần. Không nạp toàn bộ lịch sử.
- Mỗi bài học cần nguồn, thời điểm, phạm vi và phân biệt lời chủ, kết quả tool, suy luận model. Kết quả tool không tự trở thành quy tắc.
- Kiểm trùng theo ý nghĩa trước ghi. Khi nguồn mâu thuẫn, giữ cả hai và xin quyết định nếu ảnh hưởng hành vi.
- Không coi file cục bộ là đảm bảo xử lý local-only; kiểm đường gửi provider trước khi chuyển dữ liệu.
- Không chép token, cookie, OTP, thông tin riêng tư không cần thiết vào bài học. Không tự chạy retention, xóa hoặc hợp nhất hàng loạt.
- Một tác vụ sở hữu mỗi thay đổi; không để hai writer cùng sửa file. Nếu không có cơ chế khóa đã kiểm, thực hiện tuần tự.

## Kiểm chứng: Superpowers
- Ghi baseline và tiêu chí xong trước sửa. Lỗi code: tạo test tái hiện, xác nhận fail đúng nguyên nhân, sửa tối thiểu rồi chạy lại.
- Truy nguyên từ log và dữ liệu đầu vào; mỗi thử nghiệm kiểm một giả thuyết. Không đổi nhiều thứ để đoán lỗi.
- Tách kiểm đúng yêu cầu khỏi kiểm chất lượng. Chỉ báo kiểm đã chạy, với lệnh, kết quả và phần chưa kiểm.
- Không xóa code vì nó được viết trước test; không nhập quy tắc bắt buộc commit, worktree hay gọi subagent.

## Học từ phiên: One Skill to Rule Them All
- Trong tác vụ đang dùng, nhận diện sửa sai của chủ, thao tác lặp và thiếu năng lực có bằng chứng.
- Tín hiệu không phải kết luận. Ghi tối thiểu tình huống, lỗi, nguyên nhân đã xác nhận, sửa đề xuất, phạm vi và ca chống tái diễn.
- So với skill hiện có trước đề xuất. cam-tien-hoa sở hữu CUP và Knowledge Conflict Gate; không tạo observer riêng.
- Chỉ sửa khi chủ yêu cầu hoặc quy tắc hiện hành cho phép sửa tại thời điểm dùng. Không bật session hook, lịch rà soát hoặc auto-deploy.
- Không thu thập toàn bộ hội thoại mặc định; không coi im lặng hoặc một lỗi tool thoáng qua là sở thích lâu dài.

## Khám phá: Find Skills
- Xác định đầu ra cần đạt; kiểm Javis/index.md và skill gần nhất trước tìm bên ngoài.
- Tìm theo năng lực cụ thể, xác nhận owner/repo, commit, license, dependencies và side effects.
- Popularity không phải kiểm an toàn. Đọc nội dung, phát hiện trùng, đánh giá đường gửi dữ liệu, quyền và hooks.
- Chọn cập nhật skill cũ trước tạo mới; tách kỹ năng kiến thức khỏi công cụ thực thi.
- Không chạy npx, installer global hoặc bỏ xác nhận từ tài liệu nguồn. Dùng javis_improve cho cải tiến brain theo yêu cầu.

## UI UX Pro Max
- Chỉ nạp cho tác vụ giao diện; giữ framework, theme tokens và chức năng hiện có.
- Thiết kế theo người dùng, mục tiêu và các trạng thái loading/empty/error/success.
- Kiểm keyboard, focus rõ, accessible name, semantics, không truyền trạng thái chỉ bằng màu.
- Kiểm tương phản chữ thường tối thiểu 4.5:1, xuống dòng, phóng to, nội dung dài, giảm chuyển động và bảo toàn dữ liệu form.
- Mốc viewport tham khảo: 375, 768, 1024, 1440 px. Không tuyên bố đạt nếu chưa chạy kiểm.
- Không coi đã có search.py, catalog hoặc design engine upstream. Biểu đồ phải dùng dataviz; xuất Webcake dùng html-to-webcake.

## Cổng xung đột và nghiệm thu
1. Ràng buộc cứng: không sửa T0, permissions, server hoặc cấu hình harness.
2. Chủ sở hữu: memory hiện tại quản lý ký ức; cam-tien-hoa quản lý bài học; cam-cot-song quản lý thực thi; UI skill quản lý giao diện.
3. Thử nhỏ: kiểm tĩnh metadata, liên kết, phạm vi, trùng và các tình huống âm tính. Không thay kiểm hành vi model bằng kiểm tệp.
4. Lưu có backup qua javis_improve và ghi undo id. Không tự commit, restart hoặc tạo lịch.
