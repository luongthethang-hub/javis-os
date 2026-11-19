---
type: workflow
name: Kế hoạch ngày thực dụng
slug: ke-hoach-ngay-thuc-dung
status: 'off'
group: Năng suất
description: Biến danh sách việc và mục tiêu thành kế hoạch ngày ngắn, khả thi và có bước chốt cuối ngày.
steps:
  - agent: phan-tich-uu-tien-ngay
    task: "Từ yêu cầu của chủ nhà: {{input}}. Phân loại việc, chọn tối đa ba ưu tiên có tác động cao nhất và nêu giả định còn thiếu. Không tạo lịch hoặc giao việc."
  - agent: dieu-phoi-ke-hoach-ngay
    task: "Từ bản ưu tiên này: {{prev}}. Lập kế hoạch thực thi trong ngày theo trình tự, có bước khởi động, điểm rà soát, thời gian đệm và định nghĩa hoàn thành. Dùng giờ cụ thể chỉ khi đầu vào đã có."
  - agent: kiem-tra-kha-thi-ngay
    task: "Rà soát kế hoạch sau: {{prev}}. Loại hoặc rút gọn phần quá tải, chốt bản thực thi với tối đa ba ưu tiên và thêm nghi thức chốt ngày. Không tự sửa lịch hay tạo nhiệm vụ."
updated: '2026-11-18'
---

Quy trình nhận một danh sách việc, mục tiêu hoặc bối cảnh ngày làm việc. Ba cộng sự lần lượt chọn ưu tiên, sắp kế hoạch thực hiện và kiểm tra khả thi để trả về một phiên bản ngắn gọn có thể làm ngay.

Quy trình đang tắt để chủ nhà xem trước và chủ động bật trên trang Quy trình.
