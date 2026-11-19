---
name: Họp hội đồng đầu tư
description: "Chạy một phiên họp phân tích thị trường đủ 6 pha, ra phiếu lệnh và biên bản."
group: Tài chính
---

# Họp hội đồng đầu tư

## Khi nào dùng

Chủ nhà hỏi kiểu: "phân tích XAUUSD hôm nay", "có nên vào lệnh EURUSD không", "cho văn phòng họp về mã này", "giá này vào được chưa", "review lại lệnh đang giữ". Cũng dùng khi họ muốn một quyết định giao dịch có phản biện chứ không phải một câu trả lời một chiều.
Không dùng cho: câu hỏi kiến thức chung về thị trường, hỏi thuế pháp lý, hay yêu cầu đặt lệnh hộ.

## Chuẩn bị

Kiểm ba thứ trước khi vào phiên:

1. Chuẩn bị bộ dữ liệu trước khi mở workflow. Ghi nguồn gốc, đơn vị, thời điểm chụp, múi giờ và hạn sử dụng. Với dữ liệu do chủ cung cấp, giữ nhãn này và ghi rõ điều gì chưa đối chiếu bên ngoài. Dữ liệu giả lập phải có nhãn mô phỏng.
2. Ghi mã, sàn, khung thời gian và thời điểm đánh giá. Đính kèm dữ liệu giá, sự kiện và dòng tiền phù hợp. Chỉ yêu cầu vốn và giới hạn rủi ro khi hồ sơ cần định cỡ.
3. Các ghế có mặt chưa: dùng `javis_team op=get` xem nhóm văn phòng còn đủ thành viên.

## Cách chạy

Phiên họp sáu pha, làm đúng thứ tự, không nhảy pha:

| Pha | Ai làm | Kết quả phải có |
|---|---|---|
| 1. Tiếp nhận | Thư ký Hội đồng | Đầu vào chuẩn hoá, phần còn thiếu |
| 2. Kiểm chứng | Kiểm chứng dữ liệu | Bảng con số ĐÃ KIỂM / CHƯA KIỂM / THIẾU |
| 3. Ba ghế trình bày | Kỹ thuật, Cơ bản vĩ mô, Dòng tiền | Mỗi ghế một khối ý kiến độc lập |
| 4. Tổng hợp và chất vấn | Trưởng phòng Nghiên cứu | Điểm thống nhất, điểm chống nhau, ngưỡng phân xử |
| 5. Phán quyết rủi ro | Quản trị Rủi ro | DUYỆT / DUYỆT CÓ ĐIỀU KIỆN / CHẶN, kèm size |
| 6. Chốt | Giám đốc Đầu tư | Một trong bốn trạng thái, phiếu lệnh, hiệu lực |

Bốn trạng thái chốt: VÀO LỆNH / CHỜ XÁC NHẬN / THEO DÕI / ĐỨNG NGOÀI.

## Quy trình

1. **Chạy phiên chính thức.** Mở workflow “Phiên họp phân tích thị trường” và chạy thủ công với bộ dữ liệu đã chuẩn bị. Workflow đưa cùng một hồ sơ kiểm chứng cho cả ba ghế, sau đó bàn giao đủ ba nhận định cho Trưởng phòng Nghiên cứu. Kết quả nằm trong lịch sử workflow.
2. **Trao đổi qua nhóm khi cần.** Dùng nhóm để làm rõ yêu cầu hoặc trao đổi về biên bản. Trước khi gọi đó là phiên hoàn chỉnh, kiểm tra đủ kết quả của sáu pha trong lịch sử workflow.
3. **Chặn cứng.** Quản trị Rủi ro CHẶN thì CIO không được lật. Chỉ chọn lại: giảm quy mô, dời điều kiện, hoặc ĐỨNG NGOÀI.
4. **Dừng ở kiểm chứng.** Nếu dữ liệu thiết yếu thiếu, mâu thuẫn hoặc quá hạn, dừng trước ba ghế chuyên viên và ghi rõ dữ liệu cần bổ sung.
5. **Đóng phiên.** Ghi nhật ký nếu chủ nhà đã vào lệnh (`nhat-ky-thuc-thi`), kèm nhắc stop loss và take profit.

## Bẫy

- **Số liệu tự sinh.** Ghế kỹ thuật rất dễ viết ra mức giá nghe hợp lý. Chỉ con số nào được chủ nhà cấp hoặc lấy từ connector mới được vào phiếu lệnh.
- **Ba ghế nói giống nhau.** Nếu ba khối ý kiến na ná nhau thì đó là dấu hiệu đang bịa góc nhìn, không phải thống nhất. Yêu cầu mỗi ghế nêu một mốc giá riêng.
- **Bỏ pha rủi ro.** Phiếu lệnh không có phán quyết rủi ro là phiếu lệnh vô giá trị, kể cả khi kèo rất đẹp.
- **Hỏi vòng vo.** Thiếu đầu vào thì hỏi một lượt đủ ý, không hỏi nhỏ giọt làm chủ nhà mệt.

## Kiểm chứng

Trước khi gửi kết luận, tự kiểm bốn điểm: kết luận có đúng một trạng thái chưa, mọi con số trong phiếu lệnh có nguồn chưa, có mục ý kiến thiểu số chưa, có mục dữ liệu còn thiếu chưa. Thiếu một điểm thì chưa gửi.
