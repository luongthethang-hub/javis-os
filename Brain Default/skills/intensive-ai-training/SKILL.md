---
name: Huấn luyện AI Chuyên sâu (v2)
description: "Quy trình 5 pha huấn luyện AI theo RUULEE v6.0: nén TaskPacket, định tuyến L1/L2 Cascade tối đa 2 lỗi, Red/Blue FMEA và Shadow Eval."
group: AI
---

# Quy trình Huấn luyện AI Chuyên sâu (AI Pipeline v2 - RUULEE v6.0)

Quy trình tối ưu năng lực mô hình, chất lượng suy luận, định tuyến chi phí mạnh/nhẹ và nén ngữ cảnh cho các tác vụ LLM cốt lõi trên JavisOS theo chuẩn **RUULEE v6.0** (tư duy native-first, không cài chồng framework ngoài).

## Khi nào dùng

- Đánh giá, tinh chỉnh hoặc nâng cấp chất lượng suy luận của prompt, bộ định tuyến model hoặc cấu hình LLM cốt lõi.
- Giảm chi phí token/độ trễ bằng cách tách tải giữa mô hình mạnh (L1) và mô hình nhẹ (L2) mà vẫn giữ độ chính xác.
- Thiết lập bài kiểm thử FMEA, Red/Blue Team hoặc Shadow Evaluation cho một tác vụ AI lặp lại.

## Chuẩn bị

- Xác định rõ tập tác vụ mục tiêu, baseline hiện tại (chất lượng, chi phí token, độ trễ) và ràng buộc cứng T0/T1.
- Đọc `skills/ruulee-operational-charter/references/l012-matrix-and-modules.md` nếu cần lược đồ `TaskPacket` và danh sách vector FMEA đầy đủ.
- Đối chiếu module native sẵn có trên JavisOS: `server/model_router.py`, `server/context_compressor.py`, `server/improvement_trial_runner.py`.

## Quy trình 5 Giai đoạn

### Giai đoạn 1: Nhận thức luận & Chuẩn hóa Dữ liệu (Metacognitive & Data Prep)
1. Đo mức bất định của tác vụ và phân loại mức bằng chứng đầu vào (`E1..E5`).
2. Nén ngữ cảnh và loại bỏ nhiễu hội thoại theo nguyên lý nén prompt (native qua `context_compressor.py` và cấu trúc `TaskPacket` <= 3.000 tokens).
3. Gắn nhãn độ khó và phạm vi rủi ro làm tập ground-truth phân tách tác vụ cho mô hình mạnh (L1) và mô hình nhẹ (L2).

### Giai đoạn 2: Định tuyến Mô hình & Cascade Escalation (Model Routing)
1. Định tuyến theo năng lực trước, chi phí sau (`model_router.py`): đẩy tác vụ xác định rõ, rủi ro thấp/trung bình sang L2.
2. Áp dụng **Cascade Escalation cứng:** nếu đầu ra của L2 không đạt schema, thiếu bằng chứng hoặc lỗi liên tiếp **tối đa 2 lần (`max_retries = 2`)**, lập tức nâng cấp lên L1 thay vì lặp vô tận.

### Giai đoạn 3: Đánh giá Đối kháng Red/Blue & Stress Test FMEA
1. Blue Team đề xuất lời giải/prompt chuẩn; Red Team (cô lập ngữ cảnh) rà soát 6 vector rủi ro: logic/toán, giả định ngầm, giá trị biên, an toàn dữ liệu, chi phí token và tuân thủ T0/T1.
2. Bơm bộ kiểm thử biên FMEA: chuỗi rỗng, `null`, lỗi mã hóa UTF-8/tiếng Việt có dấu, payload quá trần token, giả lập timeout/HTTP 429.

### Giai đoạn 4: Shadow Evaluation & Kiểm toán
1. Chạy song song prompt hoặc model ứng viên ở chế độ ẩn (không tạo tác dụng phụ tới người dùng) trên tập mẫu thực tế qua `improvement_trial_runner.py`.
2. Chấm điểm chất lượng, độ tuân thủ ràng buộc và phần trăm tiết kiệm token/độ trễ so với baseline; lưu nhật ký truy vết kèm `trace_id`.

### Giai đoạn 5: Tinh chỉnh Có Kiểm soát (CUP)
1. Tổng hợp sai lệch đo được (`E1`) thành đề xuất nâng cấp prompt/router cụ thể.
2. Gắn diff, số liệu Shadow Eval, đánh giá rủi ro và phương án hoàn tác trình Layer 0 phê duyệt trước khi áp dụng chính thức.

## Bẫy

- Không tăng ngưỡng retry lên 3 ở L2; luôn giữ cứng `max_retries = 2` để đồng nhất RUULEE v6.0.
- Không đánh giá chất lượng bằng cảm tính hoặc trên 1 ví dụ đơn lẻ; phải so cặp với baseline trên cùng bộ mẫu.
- Không để bộ prompt ứng viên chưa duyệt ghi đè trực tiếp cấu hình đang chạy của người dùng.

## Kiểm chứng

Một vòng huấn luyện AI chỉ đạt `VERIFIED_IN_SCOPE` khi có đủ:
- Bảng so sánh Trước/Sau có đơn vị rõ ràng (tỷ lệ pass schema, token trung bình, độ trễ).
- Kết quả chạy FMEA trên các ca biên và xác nhận Cascade kích hoạt đúng sau 2 lần lỗi.
- Bản ghi diff và đường dẫn hoàn tác sẵn sàng cho Layer 0.
