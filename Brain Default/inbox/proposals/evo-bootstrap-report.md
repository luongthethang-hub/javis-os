# Đề xuất khởi tạo hệ thống tự tiến hóa

## Kết luận
Có nền tảng phù hợp để thử nghiệm có kiểm soát: 22 agents, 11 skills, 3 workflows (1 bật), 0 loops; chưa thấy bản sao hiển nhiên. Có vùng giao nhau giữa CIO / Trưởng phòng Nghiên cứu / Phân tích thị trường và giữa Marketing / Content, cần chốt ranh giới. 20/22 agents dùng model chính. Khả dụng Claude subscription và OpenAI OAuth chưa kiểm chứng; các log hiện có còn mâu thuẫn về model Reviewer, và lỗi `gpt-5.5` bị từ chối đã được ghi nhận.

## Phương án
Thử riêng từng tuyến thuê bao bằng việc mẫu ngắn, ghi engine/model thực chạy, thời điểm và lỗi. Sau đó thử phản biện chéo tối đa 3 lượt, tối đa 5 phút/lượt và 15 phút/vòng; lưu phiên bản, bằng chứng, người đề xuất/phản đối và phán quyết. Dùng 4 mảng: Trading/EA do Kỹ sư EA, kiểm chứng dữ liệu và rủi ro; Content do Trợ lý Content cùng workflow đang bật; Affiliate tạm dùng Content + Phản biện nội dung; Hạ tầng do Điều phối tổng hợp, chưa có chuyên trách. Đánh giá việc đã đóng theo rubric 10 điểm, lỗi an toàn chặn kết quả. Đề xuất reminder tuần quyền `suggest`, giới hạn 20 việc, chỉ tạo sau khi xử lý nguy cơ trùng reminder tự học 8 giờ. Chi tiết tại [rà soát dữ liệu](evo-bootstrap-data-check.md), [phản biện chéo](evo-bootstrap-cross-review.md), [4 mảng](evo-bootstrap-4-mang.md), [đánh giá và lịch](evo-bootstrap-evaluation-schedule.md).

## Rủi ro
Provider, connector cụ thể, baseline KPI và hiệu quả thực tế chưa xác định. Lịch bổ sung có thể trùng; thiếu log làm phản biện chéo hoặc điểm đánh giá không đáng tin. KPI hiện chỉ là đề xuất.

## Điều kiện áp dụng
Chỉ ghi nhận cross-review mô hình khi log runtime xác nhận hai họ model trên đúng phiên bản. Không đổi cấu hình, quyền, agent hay lịch trong giai đoạn thử; mọi chỉnh sửa capability để chờ duyệt. Không thực hiện giao dịch hoặc hành động bên ngoài.

## Bước tiếp theo
Chủ quyết có duyệt chạy hai việc mẫu kiểm tra tuyến Claude và OpenAI, rồi thử một vòng phản biện nội bộ theo giới hạn trên không; đồng thời chốt có bổ sung lịch tuần hay thay reminder 8 giờ.
