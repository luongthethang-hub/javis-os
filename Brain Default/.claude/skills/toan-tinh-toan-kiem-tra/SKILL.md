---
name: Toán tính toán và kiểm tra
description: Kiểm tra phép tính ma trận, xác suất, ML và trạng thái lượng tử bằng script, trả kết quả kèm công thức.
group: AI
---

# Toán tính toán và kiểm tra

Tính và KIỂM CHỨNG các bài toán ma trận, xác suất, machine learning cơ bản và trạng thái
lượng tử nhỏ. Mọi con số phải do script tính, không nhẩm.

## Khi nào dùng

- "Tính định thức / nghịch đảo / trị riêng / hạng / giải hệ phương trình ma trận này"
- "Xác suất ít nhất 3 lần trong 10 lần, p = 0.2", "cập nhật Bayes với tiên nghiệm 0.1"
- "Hồi quy tuyến tính cho mấy điểm này", "confusion matrix này ra precision/recall bao nhiêu"
- "Mạch lượng tử 2 qubit này ra xác suất đo thế nào", "chuẩn hoá vector trạng thái"
- Bất kỳ yêu cầu nào có số cụ thể mà kết quả phải khớp được bằng tay

Không dùng skill này cho: thống kê suy diễn cần dữ liệu lớn, tối ưu phi tuyến nhiều biến,
học sâu thật (không có GPU, không có framework). Những việc đó nói rõ là ngoài phạm vi.

## Chuẩn bị

- Python 3.12 có numpy 2.5 (đã kiểm trên máy này). KHÔNG có scipy, sympy, sklearn, pandas,
  qiskit: đừng đề xuất import chúng. Cần thêm thì nói chủ cài, đừng tự cài.
- Script tính sẵn: `scripts/verify_math.py` (cùng thư mục skill). Chạy
  `python scripts/verify_math.py <lệnh> --json '{...}'`.

## Cách chạy

```
python scripts/verify_math.py mat  --json '{"A": [[2,1],[1,3]]}'
python scripts/verify_math.py solve --json '{"A": [[2,1],[1,3]], "b": [5,10]}'
python scripts/verify_math.py prob --json '{"kind":"binomial","n":10,"k":3,"p":0.2,"at_least":true}'
python scripts/verify_math.py bayes --json '{"prior":0.1,"likelihood":0.9,"false_alarm":0.05}'
python scripts/verify_math.py linreg --json '{"X":[[1],[2],[3],[4]],"y":[2,4,6,8]}'
python scripts/verify_math.py metrics --json '{"y_true":[1,1,0,0],"y_pred":[1,0,1,0]}'
python scripts/verify_math.py qubit --json '{"gates":["H","CNOT"],"shots":1000}'
```
Không truyền `--json` thì script đọc JSON từ stdin. Đầu ra mặc định là JSON có `result`,
`formula`, `steps`, `check`.

## Quy trình

1. **Xác định dạng bài** và dữ kiện: kích thước ma trận, số qubit, tham số phân phối, nhãn
   thật/dự đoán. Thiếu dữ kiện chặn kết quả thì hỏi đúng một câu.
2. **Chọn công thức trước khi tính.** Ghi công thức, đơn vị, phạm vi áp dụng (xem
   `references/`). Sai công thức thì script chạy đúng vẫn ra đáp án sai.
3. **Gọi script** cho mọi phép tính. Ma trận từ 3x3 trở lên, tổ hợp lớn, hồi quy, trạng thái
   lượng tử: bắt buộc script, không nhẩm.
4. **Kiểm chứng chéo** bằng đường thứ hai: định thức so với tích trị riêng, nghiệm hệ so với
   A·x, xác suất so với tổng bằng 1, mô hình so với R² hoặc accuracy trên chính dữ liệu vào.
   Script đã in `check`; đọc và nêu nó ra.
5. **Trả lời**: kết luận trước, công thức, số liệu, phạm vi, sai số làm tròn.

## Tài liệu tham chiếu

- `references/ma-tran.md`: định thức, nghịch đảo, trị riêng, hạng, giải hệ, điều kiện số.
- `references/xac-suat.md`: nhị thức, Poisson, chuẩn, Bayes, kỳ vọng, phương sai.
- `references/machine-learning.md`: hồi quy tuyến tính, logistic, metric phân loại, overfit.
- `references/luong-tu.md`: qubit, cổng, chồng chập, vướng mắc, xác suất đo.

## Bẫy

- **Ma trận suy biến**: định thức 0, `numpy.linalg.inv` ném LinAlgError. Bắt lỗi, báo "không
  khả nghịch" kèm hạng, đừng trả số rác.
- **Nhầm `at_least` với đúng k**: "ít nhất 3" là 1 - CDF(2), không phải P(X=3). Nêu rõ đang tính.
- **Chuẩn hoá xác suất**: kiểm tổng bằng 1 trước khi dùng làm phân phối.
- **Sai đơn vị phần trăm**: 0.2 và 20% chênh 100 lần. Chốt đơn vị trong câu trả lời.
- **Làm tròn quá sớm**: giữ đủ chữ số khi tính, chỉ làm tròn ở câu kết luận và nói rõ số chữ số.
- **Nhãn lệch**: `metrics` phải kiểm độ dài y_true = y_pred, thiếu thì báo lỗi chứ không cắt bớt.
- **Lượng tử**: n qubit là vector 2^n chiều, đừng viết tay quá 3 qubit; kiểm chuẩn vector = 1.
- Không nói "đã chạy kiểm thử" nếu chưa thấy output script thật.

## Kiểm chứng

- Output script có `check` khớp (sai số <= 1e-9 với đại số tuyến tính, <= 1e-6 với xác suất).
- Trả lời có đủ ba phần: công thức, con số, phạm vi áp dụng.
- Nếu script lỗi: báo nguyên nhân quan sát được và phần chưa làm, không thay bằng số nhẩm.
