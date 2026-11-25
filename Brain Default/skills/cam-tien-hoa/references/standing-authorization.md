# Ủy quyền tiến hóa có điều kiện

Nguồn: lệnh chủ lúc 23:22 ngày 2026-11-25, Asia/Bangkok, web:c5891efc796348dbb651343acf8556e6.
Yêu cầu: cho toàn hệ thống tiếp cận nội dung tiến hóa, thực hiện ngay khi đủ điều kiện, không cần duyệt lại.
Phạm vi thực thi hiện tại: Brain Default. Đây là ủy quyền của chủ, không phải cấp quyền OS, gateway hoặc bằng chứng đã đồng bộ các ứng dụng ngoài.

## Tiếp cận tri thức
Mọi agent và hạng mục công việc sử dụng Brain Default có thể tham chiếu cam-tien-hoa và references/repo-distillation.md, trong giới hạn quyền đọc hiện hữu. Chỉ nạp phần liên quan, không nhồi toàn bộ nội dung vào mọi lượt.
Không truyền thông tin riêng tư sang engine, tài khoản hoặc dịch vụ khác chỉ vì được đọc tri thức. Các engine ngoài phải được kiểm kết nối và nạp thật trước khi báo đồng bộ.

## Được làm ngay, không hỏi lại
Trong tác vụ đang dùng, được áp dụng kỹ thuật đã chưng cất và sửa nhỏ skill người dùng đang dùng khi quy tắc cấp cao hơn cho phép. Không cần xin lại phê duyệt cùng phạm vi nếu đồng thời đủ điều kiện:
1. Có lỗi hoặc cơ hội cải tiến cụ thể, bằng chứng và nguồn; không suy diễn từ im lặng hoặc dữ liệu không đáng tin.
2. Thay đổi tối thiểu, trong Brain Default, không phát sinh hành động ngoài, chi phí mới hoặc thay đổi production.
3. Kiểm trùng, ràng buộc cứng và xung đột logic/phạm vi; không thay quyền hoặc làm suy yếu chốt an toàn.
4. Có baseline, diff, tiêu chí nghiệm thu và kiểm phù hợp đã chạy. Thiếu kiểm ảnh hưởng tính đúng thì chỉ đề xuất, không tự áp dụng.
5. Có backup và undo id qua javis_improve; không ghi đè thay đổi đồng thời của tác vụ khác.
6. Báo ngắn sau thay đổi: đã đổi gì, bằng chứng kiểm, giới hạn và mã hoàn tác. Thất bại thì giữ hoặc khôi phục baseline trong đúng phạm vi được phép.

## Không nằm trong ủy quyền này
- Không sửa T0, checksum niêm phong, danh tính, policy, secrets, ACL, sandbox hoặc cấu hình quyền của harness.
- Không sửa server, restart, update ứng dụng, commit, push, merge hoặc triển khai production.
- Không tự sửa skill hệ thống; không sửa hàng loạt agent/skill/workflow, không tạo vòng tự nâng cấp hoặc lịch nền.
- Không tự bật plugin, workflow, loop hoặc MCP; không phát sinh giao dịch, gửi tin, xuất bản hoặc xóa dữ liệu.
- Các việc bị chỉ dẫn cấp cao hơn yêu cầu duyệt vẫn phải duyệt. Không tự mở rộng chính ủy quyền này.

## Cách diễn giải xung đột
Trong phạm vi đủ điều kiện trên, lệnh mới thay yêu cầu chủ duyệt từng diff của tài liệu CAM cũ. Ngoài phạm vi đó giữ nguyên cổng duyệt.
Sửa skill tại thời điểm dùng không đồng nghĩa được nâng cấp hàng loạt. Yêu cầu truy cập mọi hạng mục không đồng nghĩa bật mọi công cụ.
Không có tiến trình mới được tạo bởi tài liệu này. Kiểm tĩnh không chứng minh tất cả engine đã đọc hoặc tuân thủ.
