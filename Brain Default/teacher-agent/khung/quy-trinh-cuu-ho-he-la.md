# Quy trình cứu hộ một hệ lạ — T2 v0.1.1

**Phân vai (v0.1.1):** Doctor Agent thực hiện R0-R6 và là nơi duy nhất sửa code. HLV làm R-1 (phân luồng), cung cấp bộ test R1b/R5, duyệt chuyên môn phác đồ R4, chấm kết quả R5-R6 bằng người chấm khác hãng. HLV không mở luồng ghi vào hệ đang cứu.

Khác với cứu hộ học viên quen: HLV chưa có điểm gốc, chưa có golden test riêng, có thể chưa hiểu kiến trúc. Vì vậy thêm bước R-1 và siết R0.

| Bước | Việc | Đầu ra |
|---|---|---|
| **R-1 Nhận ca** | Phiếu nhận rút gọn (T1 của tiếp nhận): hệ gì, ai là chủ, đang gãy gì, từ bao giờ, ai được quyền dừng hệ. Chọn adapter. | `benh-an/BA-…md` mục 0 |
| **R0 Cầm máu** | Đề xuất chủ hệ dừng hành động rủi ro, chuyển chỉ đọc/soạn, chụp log + cấu hình + trạng thái. Doctor và HLV **chỉ đọc** ở bước này, không tự dừng tiến trình của hệ người khác khi chưa được chủ hệ đồng ý (A1). Không xóa gì. | Bản chụp + xác nhận chủ hệ |
| **R1 Khám** | Thu triệu chứng: lỗi, log, KPI, lời phàn nàn; dựng dòng thời gian; vẽ sơ đồ hệ (thành phần, model, công cụ, bộ nhớ, lịch, cổng duyệt) | Bảng thời gian + sơ đồ |
| **R1b Điểm gốc nhanh** | Chạy sàn an toàn chung (`golden-tests-loi.jsonl`) + 10 câu nghiệp vụ lấy từ chính việc hệ đang làm. Đây là "số trước" | Điểm E1 |
| **R2 Chẩn đoán gốc** | 6 lớp: prompt/skill · công cụ/kết nối · bộ nhớ/trạng thái · định tuyến/chi phí · dữ liệu · giá trị/ranh giới (trôi). Mỗi giả thuyết có nhãn E và cách kiểm. Gợi ý theo nền tảng ở adapter | Gốc được xác nhận |
| **R3 Tái hiện** | Golden test trượt trên hệ hiện tại. Chưa tái hiện = chưa sửa | GT riêng của hệ |
| **R4 Phác đồ** | Sửa nhỏ nhất, lớp thấp nhất (T3 trước T2), qua nhánh/PR/bản sao, có đường lùi. Chủ hệ duyệt trước khi áp | CUP |
| **R5 Hồi quy** | Toàn bộ golden test (sàn + riêng); test cũ trượt = chặn | Báo cáo |
| **R6 Hồi phục & bàn giao** | Nâng bậc dần; báo L0 + chủ hệ: nguyên nhân, đã sửa gì, số trước/sau, rủi ro còn lại, bài học. Hỏi chủ hệ có muốn chuyển thành học viên thường trực (vào tiếp nhận T4-T6) | Bàn giao + CUP cho khung nếu bài học dùng chung |

Mức nặng: **nặng** (rò rỉ dữ liệu, giao dịch sai, ranh giới vỡ) → R0 trong giờ, báo L0 ngay · **vừa** (lỗi lặp) → 24h · **nhẹ** (KPI xấu) → hồi cứu tuần.

Bài học dùng được cho mọi hệ → CUP vào `khung/`; bài học riêng → CUP vào thư mục học viên.
