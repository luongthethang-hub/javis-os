---
type: workflow
name: Nghiệm thu bắt buộc trước khi chốt việc
slug: nghiem-thu-bat-buoc
status: 'off'
group: Vận hành
description: "Chuẩn hóa bàn giao, kiểm định độc lập và chặn chuyển bước khi chưa đạt tiêu chí."
steps:
  - agent: truong-ban-van-hanh-lien-doi
    task: "Lập phiếu nghiệm thu cho việc sau: {{input}}. Ghi mã việc, đầu ra mong đợi, phạm vi, quyền thực tế, danh sách tiêu chí bắt buộc quan sát được, tiêu chí khuyến nghị, bằng chứng cần có và người nghiệm thu độc lập. Nếu thiếu tiêu chí thì đề xuất và nêu rõ đang chờ chủ xác nhận. Không tự đặt tiêu chí dễ đạt, không tuyên bố đạt."
    max_retries: 1
  - agent: kiem-dinh-van-hanh-doc-lap
    task: "Nghiệm thu độc lập theo phiếu ở {{prev}} và yêu cầu gốc {{input}}. Kiểm từng tiêu chí trên đầu ra thực tế; không dựa vào lời báo của người làm. Trả bảng: mã việc | đầu ra/phiên bản | tiêu chí | bằng chứng | kết quả từng tiêu chí | trạng thái | lỗi còn lại và điều kiện thử lại. Chỉ dùng trạng thái: ĐANG LÀM, CHỜ NGHIỆM THU, KHÔNG ĐẠT, CHƯA ĐỦ BẰNG CHỨNG, ĐẠT, ĐÓNG - NGOẠI LỆ ĐƯỢC DUYỆT. Ghi mức bằng chứng E0-E3 cho từng kết luận. Không ghi ĐẠT khi thiếu bằng chứng."
    verify_agent: bac-si-tham-dinh-kiem-thu-doc-lap-2
    max_retries: 1
  - agent: truong-ban-van-hanh-lien-doi
    task: "Tổng hợp phán quyết nghiệm thu trong {{prev}} thành báo cáo một trang cho chủ: trạng thái cuối, tiêu chí trượt hoặc chưa đủ bằng chứng, việc bị chặn, quyết định cần chủ duyệt và tối đa ba bước tiếp theo. Không chuyển bước phụ thuộc khi còn tiêu chí bắt buộc KHÔNG ĐẠT hoặc CHƯA ĐỦ BẰNG CHỨNG. Không tự phê duyệt hành động ra ngoài."
    max_retries: 1
updated: '2026-11-27'
---

# Nghiệm thu bắt buộc trước khi chốt việc (`nghiem-thu-bat-buoc`)

Quy trình dùng chung cho mọi nhóm, hiện tại và về sau. Mục đích là tách "đã làm xong" khỏi "đã được nghiệm thu đạt", và chặn việc chuyển sang bước phụ thuộc khi còn tiêu chí bắt buộc chưa đạt hoặc chưa đủ bằng chứng.

Ba bước: Trưởng ban lập phiếu tiêu chí, Kiểm định độc lập chấm trên đầu ra thật, Trưởng ban tổng hợp phán quyết và danh sách việc bị chặn.

Quy trình đang ở trạng thái `off` để chủ xem trước. Bật ở trang Quy trình khi đã đồng ý cách chấm. Bật quy trình không thay đổi quyền của bất kỳ agent nào.
