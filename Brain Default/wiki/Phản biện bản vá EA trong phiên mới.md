---
type: wiki
status: active
tags: [wiki, mql5, kiem-thu]
created: 2026-11-20
updated: 2026-11-20
source: "[[reports/ai-company/kiem-thu-egm-lite-2026-11-19]]"
---

# Phản biện bản vá EA trong phiên mới

## Cách thực hiện

1. Chuẩn bị Task Card có hành vi mong đợi, các ca biên và tiêu chí nghiệm thu. Ghép Task Card với diff cùng các đoạn trước và sau thay đổi cần để đối chiếu. Nếu hồ sơ thiếu, bổ sung trước khi gọi reviewer. [[reports/ai-company/kiem-thu-egm-lite-2026-11-19]]
2. Mở một phiên phản biện mới, đưa vào hồ sơ đã chuẩn bị và yêu cầu dẫn dòng mã, chỉ rõ hành vi sai hoặc thiếu, cùng điều kiện tái hiện. Trong phép thử Windows, phiên mới tách lịch sử hội thoại của lượt cha nhưng vẫn nhận được chỉ dẫn dự án, nên phạm vi tệp và quyền đọc cần được kiểm soát ở môi trường chạy. [[reports/ai-company/kiem-thu-egm-lite-2026-11-19]]
3. Đối chiếu từng phát hiện với Task Card, diff và ca kiểm thử. Với EA thật, giữ các cổng nghiệm thu compile `strict`, regression so với bản chuẩn và shadow/demo. [[reports/ai-company/kiem-thu-egm-lite-2026-11-19]] [[workflows/phat-trien-ea-ban-va]]

## Kết quả mô phỏng ngày 19/11/2026

- Trên 4 ca MQL5 mô phỏng, một lượt phản biện phiên mới tìm được 7/7 lỗi mã và 6/6 khoảng trống đặc tả hoặc độ phủ, với 0 báo sai ở ca sạch. Hai lượt có cùng độ phủ và 1 báo sai ở ca sạch. Đối chứng một lượt có kèm ghi chú hội thoại cũng đạt 7/7 và 6/6. [[reports/ai-company/kiem-thu-egm-lite-2026-11-19]]
- Chưa có kết quả trên EA thật. Dùng một lượt phiên mới làm mốc thử nghiệm với Task Card EA thật. Chỉ cân nhắc thêm lượt rà đặc tả cho thay đổi liên quan giới hạn vốn, xử lý lệnh hoặc khôi phục trạng thái. Trước khi nhân rộng, cần chứng minh lượt bổ sung tìm lặp lại được lỗi nghiêm trọng mà một lượt bỏ sót. [[reports/ai-company/kiem-thu-egm-lite-2026-11-19]]
