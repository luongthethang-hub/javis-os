# Ma trận và đại số tuyến tính

Bảng công thức dùng cho `scripts/verify_math.py mat|solve`. Ma trận A cỡ n x n, vector x, b.

## Định thức

- 1x1: det = a11. 2x2: det = a11·a22 - a12·a21.
- Khai triển Laplace: det(A) = Σ_j (-1)^(1+j) · a1j · det(M1j).
- det(A) = tích các trị riêng (kể bội). Dùng làm kiểm chứng chéo với `eig`.
- det(A·B) = det(A)·det(B). det(A) = 0 <=> A suy biến.

## Nghịch đảo

- Chỉ tồn tại khi det ≠ 0.
- 2x2: A^-1 = (1/det) · [[d, -b], [-c, a]] với A = [[a,b],[c,d]].
- Kiểm chứng: A · A^-1 = I, sai số <= 1e-9.
- Ma trận gần suy biến (số điều kiện lớn) thì nghịch đảo mất chính xác; nêu số điều kiện.

## Hạng và hệ phương trình

- rank(A) = số trị riêng khác 0 (với ma trận vuông thực) = số pivot sau khử Gauss.
- Hệ A·x = b: nghiệm duy nhất khi det ≠ 0. Vô nghiệm hoặc vô số nghiệm khi det = 0; kiểm
  rank(A) so với rank([A|b]).
- Cramer: x_i = det(A_i)/det(A), A_i là A thay cột i bằng b. Chỉ dùng cho n nhỏ vì chi phí giai thừa.
- Kiểm chứng: thay x vào A·x và so với b.

## Trị riêng, vector riêng

- Định nghĩa: A·v = λ·v, v ≠ 0.
- Đa thức đặc trưng: det(A - λI) = 0. Nghiệm là trị riêng.
- Trace(A) = Σ λ_i. det(A) = Π λ_i. Hai đẳng thức này là kiểm chứng chéo bắt buộc.
- Ma trận đối xứng thực: trị riêng thực, vector riêng trực giao.
- Chuẩn hoá vector riêng về norm 2 bằng 1 trước khi báo.

## Phép toán khác

- Nhân ma trận: (A·B)_ij = Σ_k a_ik·b_kj. Số phép nhân n^3.
- Chuyển vị (A^T)_ij = a_ji. (A·B)^T = B^T·A^T.
- Ma trận trực giao: A^T·A = I. Ma trận Markov: mỗi hàng không âm, tổng hàng = 1.
- Chuẩn Frobenius: ||A||_F = sqrt(Σ a_ij²). Chuẩn phổ = trị riêng lớn nhất của A^T·A, căn bậc hai.
- Số điều kiện cond(A) = ||A||·||A^-1||, xấp xỉ tỉ lệ trị riêng lớn nhất / nhỏ nhất.

## Bẫy

- Nhầm thứ tự nhân: A·B ≠ B·A nói chung.
- Chia cho định thức đã làm tròn 0.
- Báo trị riêng phức khi ma trận không đối xứng mà không nói rõ.
