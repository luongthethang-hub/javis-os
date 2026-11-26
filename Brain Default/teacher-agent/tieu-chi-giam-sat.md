# Tiêu chí giám sát hệ thống (lõi T1, chỉ L0 sửa) - v1, 26/11/2026

Nguyên tắc L0: "Giám sát không có tiêu chí cụ thể, mang tính hệ thống thì rất dễ phân nhánh lan man sang hướng tiêu cực, phá hủy, thành khối u."
Bài học thật: popup Hội đồng của CAM tự mọc quyền sửa code vì không tiêu chí nào canh giữ.

1. Không có tiêu chí thì không giám sát, không sửa. Mỗi hệ có bảng tiêu chí trong hồ sơ, L0 duyệt.
2. Mỗi tiêu chí đủ 6 ô: mã · cách đo (lệnh/test) · ngưỡng xanh/vàng/đỏ · tần suất · hành động khi đỏ · ai duyệt.
3. Bộ lõi V1-V8 cho mọi hệ:
   - V1 Sức khỏe: health OK + smoke test bật hệ thật xanh.
   - V2 Hồi quy: toàn bộ test xanh, số test không giảm.
   - V3 Toàn vẹn dữ liệu: hash dữ liệu thật không đổi ngoài thao tác đã duyệt.
   - V4 Ranh giới ghi: một luồng ghi; git sạch, mọi thay đổi nằm trong commit đã duyệt.
   - V5 Quyền: file chính sách khớp hash; không agent vượt quyền; đếm lần bị từ chối.
   - V6 Kết nối: lỗi/ngày theo đích, dưới ngưỡng.
   - V7 Chi phí/lượt dùng: trong trần.
   - V8 Khối u: file, module, agent, endpoint, tác vụ nền, quyền mới ngoài kế hoạch đã duyệt -> ĐỎ, báo L0, không tự xử lý.
4. Chống lan man: mỗi phiên khám có 1 câu hỏi chẩn đoán, phạm vi thư mục, ngân sách thời gian/lượt dùng ghi trước. Phát hiện ngoài phạm vi chỉ ghi "danh sách tồn", không đuổi theo, không tự mở việc mới.
5. Mỗi phát hiện gắn mã tiêu chí + bằng chứng (lệnh, số). Không gắn được thì chỉ là quan sát.
6. Báo cáo chuẩn: bảng V1-V8 xanh/vàng/đỏ, khác gì lần trước, mỗi ô đỏ một hành động đề xuất, việc L0 cần quyết.
7. Sửa chữa cũng bị giám sát: mỗi bước chữa giữ V1-V5 xanh; làm đỏ ô nào thì lùi ngay.
8. Áp cho Doctor Agent, Teacher Agent và mọi học viên/bệnh nhân. Đề xuất sửa qua CUP.
