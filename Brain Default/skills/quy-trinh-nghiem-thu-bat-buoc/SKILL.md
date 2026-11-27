---
name: Quy trình nghiệm thu bắt buộc
description: "Bàn giao và nghiệm thu độc lập mọi đầu việc của nhóm trước khi chốt hoặc chuyển tiếp."
group: AI
---

## Khi nào dùng
Áp dụng cho mọi đầu việc do nhóm hoặc thành viên nhóm thực hiện, hiện tại và tương lai; đặc biệt khi bàn giao, báo hoàn thành, chuyển bước hoặc thay đổi vận hành.

## Chuẩn bị
- Ghi mã việc, người giao, người thực hiện, người nghiệm thu và phiên bản đầu ra.
- Chốt tiêu chí nghiệm thu quan sát được trước khi thực hiện. Nếu thiếu tiêu chí, nhóm đề xuất tiêu chí và xin người giao xác nhận trước khi tuyên bố đạt.
- Người nghiệm thu phải độc lập với người tạo đầu ra. Nếu nhóm không có người độc lập, chuyển Ban Vận hành liên đội hoặc ghi rõ đang chờ nghiệm thu.
- Phân loại hành động có tác động ngoài: gửi khách, đăng bài, chi tiền, thay đổi quyền hoặc dữ liệu production cần phê duyệt theo quyền hiện hành; nghiệm thu không thay thế phê duyệt.

## Quy trình
1. Nhận yêu cầu và lập phiếu gồm mục tiêu, phạm vi, đầu vào, giới hạn, tiêu chí đạt, bằng chứng cần lưu và người chịu trách nhiệm.
2. Xác nhận tiêu chí trước khi làm. Tách các tiêu chí bắt buộc khỏi tiêu chí khuyến nghị.
3. Thực hiện trong phạm vi đã duyệt; ghi phiên bản đầu ra và mọi giả định hoặc sai lệch.
4. Bàn giao cho người nghiệm thu độc lập cùng danh sách tiêu chí và bằng chứng có thể kiểm tra.
5. Kiểm từng tiêu chí trên đầu ra thực tế. Ghi trạng thái ĐẠT, KHÔNG ĐẠT hoặc CHƯA KIỂM; không suy diễn từ báo cáo của người làm.
6. Nếu có tiêu chí bắt buộc KHÔNG ĐẠT hoặc CHƯA KIỂM, trả về người thực hiện, nêu lỗi, chủ xử lý và điều kiện thử lại. Không chuyển bước phụ thuộc.
7. Chỉ chốt ĐẠT khi toàn bộ tiêu chí bắt buộc đạt và người nghiệm thu ghi nhận bằng chứng. Người giao quyết định các ngoại lệ; không tự hạ tiêu chí.

## Trạng thái chuẩn
- `ĐANG LÀM`: chưa bàn giao.
- `CHỜ NGHIỆM THU`: đầu ra đã bàn giao, chưa có phán quyết.
- `KHÔNG ĐẠT`: có tiêu chí bắt buộc thất bại.
- `CHƯA ĐỦ BẰNG CHỨNG`: chưa thể kiểm ít nhất một tiêu chí.
- `ĐẠT`: tất cả tiêu chí bắt buộc được kiểm và đạt bởi người độc lập.
- `ĐÓNG - NGOẠI LỆ ĐƯỢC DUYỆT`: chỉ dùng khi người có thẩm quyền chấp thuận ngoại lệ; ghi rõ tiêu chí ngoại lệ, người duyệt và rủi ro còn lại. Không đổi nhãn thành ĐẠT.

## Mẫu bàn giao
`Mã việc | Đầu ra/phiên bản | Tiêu chí | Bằng chứng | Kết quả từng tiêu chí | Người làm | Người nghiệm thu | Trạng thái | Lỗi còn lại/điều kiện thử lại`

## Bẫy
- `XONG` chỉ mô tả người thực hiện đã dừng việc; không có nghĩa `ĐẠT`.
- Không tự nghiệm thu sản phẩm mình tạo. Không dùng lời khẳng định hoặc ảnh chụp trạng thái thay cho kiểm tra đầu ra khi có thể kiểm trực tiếp.
- Không ghi `ĐẠT` khi thiếu log, dữ liệu, quyền truy cập hoặc bước kiểm cần thiết; ghi `CHƯA ĐỦ BẰNG CHỨNG`.
- Không dùng quy trình này để tự cấp quyền, phê duyệt hành động ngoài hoặc sửa tiêu chí sau khi thấy kết quả.
- Với nhóm mới, trưởng nhóm phải đưa quy trình này vào hướng dẫn nhóm trước khi nhận việc; nếu chưa thể cấu hình, ghi nhận đây là giới hạn triển khai, không tuyên bố đã cưỡng chế hệ thống.

## Kiểm chứng
Trước khi đóng mỗi việc, đối chiếu mã việc, phiên bản, từng tiêu chí, bằng chứng và danh tính người nghiệm thu. Lưu rõ kiểm đã chạy, chưa chạy và ngoại lệ được duyệt.