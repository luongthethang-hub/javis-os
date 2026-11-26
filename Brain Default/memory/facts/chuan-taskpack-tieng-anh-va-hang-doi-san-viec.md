---
type: decision
created: 2026-11-26
updated: 2026-11-26
---
Chuẩn gói giao việc **TaskPacket v1 bằng tiếng Anh** và hàng đợi san việc cục bộ `Javis/scripts/cam_queue.py` đã được triển khai, kèm số đo thật.

**Số đo tiếng Việt so với tiếng Anh** (tiktoken, 4 cặp chỉ dẫn cùng nghĩa):
- `o200k_base`: 45 token tiếng Việt, 37 token tiếng Anh, giảm 17,8% trên mẫu.
- `cl100k_base`: 68 token tiếng Việt, 37 token tiếng Anh, giảm 45,6% trên mẫu.
- Đây là tỷ lệ trên mẫu ngắn, chưa tính chi phí dịch và sửa lỗi dịch.

**Thí nghiệm 3 cấu hình trên cùng bộ 3 tác vụ** (Audit code, Extract dữ liệu, Ops telemetry): baseline ngữ cảnh đầy đủ tiếng Việt 658 token; gói TaskPacket tiếng Anh kèm tham chiếu SHA-256 còn 134 token, giảm 79,6%; thêm san việc work-stealing vẫn 134 token và cân được tải (worker rảnh tự kéo việc, worker quá tải không bị nhồi thêm).

**Hàng đợi `cam_queue.py`** (SQLite, pull-based): `put`, `claim`, `submit`, `fail`, `status`. Đã kiểm: 8 worker tranh một việc chỉ 1 thắng, gửi trùng không tạo bản sao, worker ngoài `eligible_workers` bị từ chối, submit đúng chuyển task sang `review`. Độ trễ đo trên DB tạm: `claim` 95,3 ms/lượt (50 lượt), `put` 225,6 ms/gói (200 gói).

**Vì sao:** gửi cả lịch sử hội thoại làm phình ngữ cảnh và dồn việc vào một bot; gói gọn cộng san việc cắt được gần 80% token giao tiếp mà không mất dữ liệu, vì nội dung nặng lưu cục bộ và chỉ tham chiếu bằng mã băm.

**Áp dụng:** soạn sẵn chỉ dẫn nội bộ lặp lại bằng tiếng Anh, giữ nguyên lời người dùng khi sắc thái quan trọng, báo cáo và thông báo vẫn bằng tiếng Việt. Mã băm dùng để nhận diện phiên bản và phát hiện trùng, không dùng thay nội dung vì agent không suy ra được nội dung từ hash. Giới hạn hiện tại: hàng đợi chưa nối process worker đang chạy, chưa có polling nền, nên chưa gọi là tự vận hành.
