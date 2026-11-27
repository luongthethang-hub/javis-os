# Xác suất

Bảng công thức cho `scripts/verify_math.py prob|bayes`. Mọi p trong khoảng [0,1], không dùng %.

## Cơ bản

- P(A^c) = 1 - P(A).
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B).
- Độc lập: P(A ∩ B) = P(A)·P(B).
- Xác suất có điều kiện: P(A|B) = P(A ∩ B)/P(B), P(B) > 0.

## Nhị thức B(n, p)

- P(X = k) = C(n,k)·p^k·(1-p)^(n-k).
- "Ít nhất k": P(X >= k) = Σ_{j=k..n} P(X = j) = 1 - Σ_{j=0..k-1} P(X = j).
- "Nhiều nhất k": P(X <= k) = Σ_{j=0..k}.
- Kỳ vọng = n·p, phương sai = n·p·(1-p), độ lệch chuẩn = sqrt(np(1-p)).
- Bài "ít nhất một lần trong n lần": 1 - (1-p)^n. Đây là trường hợp riêng, tính nhanh hơn.

## Poisson(lambda)

- P(X = k) = e^(-λ)·λ^k / k!. Dùng khi n lớn, p nhỏ, λ = n·p.
- Kỳ vọng = phương sai = λ.
- Cộng hai biến Poisson độc lập: λ = λ1 + λ2.

## Phân phối chuẩn N(mu, sigma)

- Chuẩn hoá z = (x - mu)/sigma.
- P(X <= x) = Φ(z); P(a < X < b) = Φ(z_b) - Φ(z_a).
- Đối xứng: Φ(-z) = 1 - Φ(z).
- Khoảng 68.27% trong 1 sigma, 95.45% trong 2 sigma, 99.73% trong 3 sigma.
- Xấp xỉ nhị thức bằng chuẩn khi n·p >= 5 và n·(1-p) >= 5, có hiệu chỉnh liên tục ±0.5.

## Bayes

- P(A|B) = P(B|A)·P(A) / P(B), với P(B) = P(B|A)P(A) + P(B|A^c)P(A^c).
- Tỉ số: posterior odds = prior odds · likelihood ratio.
- Bẫy kinh điển: bệnh hiếm, test nhạy 0.9 nhưng dương tính giả 0.05 thì hậu nghiệm vẫn thấp.

## Kỳ vọng và phương sai

- E[X] = Σ x_i·p_i. E[aX+b] = a·E[X] + b.
- Var(X) = E[X²] - (E[X])². Var(aX+b) = a²·Var(X).
- Var(X + Y) = Var(X) + Var(Y) + 2Cov(X,Y). Độc lập thì Cov = 0.
- Hệ số biến thiên = độ lệch chuẩn / kỳ vọng (kỳ vọng khác 0).

## Bẫy

- "Ít nhất" khác "đúng". Ghi rõ công thức đang dùng.
- Tổng phân phối phải bằng 1, kiểm trước khi dùng.
- Không cộng xác suất của các biến cố không xung khắc.
- Làm tròn 0.05 thành 0 khi tính tích nhiều bước thì sai lệch lớn; tính bằng log khi n lớn.
