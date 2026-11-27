# Machine learning cơ bản

Bảng công thức cho `scripts/verify_math.py linreg|metrics`. Không có sklearn trên máy: dùng
numpy theo công thức dưới đây.

## Hồi quy tuyến tính bình phương nhỏ nhất

- Mô hình: y = X·w + b, hoặc y = X·w với cột 1 chèn sẵn.
- Nghiệm: w = (X^T·X)^-1 · X^T·y.
- Chỉ dùng được khi X^T·X khả nghịch; cột phụ thuộc tuyến tính (đa cộng tuyến) thì dùng
  `numpy.linalg.lstsq` (giả nghịch đảo) thay vì tự nghịch đảo.
- Hệ số xác định R² = 1 - SS_res/SS_tot, với SS_res = Σ(y - ŷ)², SS_tot = Σ(y - ȳ)².
- RMSE = sqrt(mean((y - ŷ)²)). MAE = mean(|y - ŷ|).
- R² = 1 là khớp hoàn hảo trên tập huấn luyện, không có nghĩa dự báo tốt.

## Logistic

- z = w·x + b, p = 1/(1 + e^(-z)), ngưỡng quyết định thường 0.5.
- Log-loss = -mean(y·log(p) + (1-y)·log(1-p)). Dùng kẹp p vào [1e-12, 1-1e-12].
- Không giải được bằng công thức đóng: dùng gradient descent hoặc Newton. Nêu số vòng lặp.

## Metric phân loại

Với nhãn dương = 1:

- Accuracy = (TP + TN) / tổng.
- Precision = TP / (TP + FP), Recall = TP / (TP + FN).
- F1 = 2·P·R / (P + R).
- Specificity = TN / (TN + FP).
- Ma trận nhầm lẫn 2x2: hàng là nhãn thật, cột là nhãn dự đoán.

**Bẫy mất cân bằng:** dữ liệu 95% âm, mô hình đoán toàn âm cho accuracy 0.95 mà recall = 0.
Luôn báo kèm precision/recall khi tỉ lệ lớp lệch, đừng chỉ báo accuracy.

## Overfit và kiểm chứng

- Chia train/validation/test. Không đánh giá trên tập đã huấn luyện rồi kết luận.
- Khoảng cách lớn giữa R² train và R² validation là dấu hiệu overfit.
- K fold cross validation: k = 5 hoặc 10, metric báo trung bình và độ lệch chuẩn giữa các fold.
- Nhiều đặc trưng, ít mẫu: ưu tiên mô hình ít tham số hoặc chuẩn hoá (regularization).

## Bẫy

- Chia tỉ lệ phần trăm khác tỉ lệ thập phân (0.2 so với 20) gây lệch 100 lần.
- Quên chuẩn hoá đặc trưng trước khi so sánh trọng số: trọng số lớn chưa chắc quan trọng.
- Báo hệ số tương quan như quan hệ nhân quả.
- Chia tập không ngẫu nhiên theo thời gian: dữ liệu tương lai lọt vào tập huấn luyện.
