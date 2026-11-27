# Toán lượng tử mức mô phỏng nhỏ

Phạm vi: 1 đến 3 qubit, mô phỏng vector trạng thái bằng numpy. Không có qiskit trên máy.
Đây là số học tuyến tính trên không gian Hilbert, không phải chạy phần cứng lượng tử.

## Trạng thái

- 1 qubit: |ψ> = α|0> + β|1>, vector [α, β] phức, |α|² + |β|² = 1.
- n qubit: vector 2^n phần tử, chuẩn 2 bằng 1. Cơ sở |00>, |01>, |10>, |11> theo thứ tự nhị phân.
- Mật độ xác suất đo: P(i) = |a_i|². Tổng phải bằng 1 (kiểm bắt buộc).
- Trạng thái chồng chập: nhiều hệ số khác 0. |+> = (|0> + |1>)/sqrt(2).

## Cổng 1 qubit (ma trận 2x2)

- X = [[0,1],[1,0]] (NOT). Y = [[0,-i],[i,0]]. Z = [[1,0],[0,-1]].
- H = (1/sqrt2)·[[1,1],[1,-1]]. H|0> = |+>.
- S = [[1,0],[0,i]]. T = [[1,0],[0,e^(iπ/4)]].
- Cổng phải là unita: U·U† = I. Kiểm khi tự nhập cổng lạ.

## Cổng nhiều qubit

- CNOT: giữ nguyên qubit điều khiển, lật qubit đích khi điều khiển = 1. Ma trận 4x4:
  [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]] với thứ tự |00>,|01>,|10>,|11>.
- Mở rộng lên n qubit: nhân tensor (kron) cổng với I ở các vị trí còn lại.
- Trạng thái Bell: H qubit 1 rồi CNOT(1,2) cho (|00> + |11>)/sqrt2. Vướng mắc cực đại.

## Đo

- Đo toàn bộ: chọn chỉ số i theo xác suất |a_i|², trạng thái sụp về |i>.
- Đo một qubit: cộng xác suất các chỉ số có bit đó = 0 hoặc 1 rồi chuẩn hoá lại phần còn lại.
- Nhiều shot chỉ là lấy mẫu lặp lại cùng phân phối; tần suất hội tụ về xác suất lý thuyết,
  sai số chuẩn xấp xỉ sqrt(p(1-p)/shots).

## Bất đẳng thức và kiểm tra

- Không sao chép trạng thái tuỳ ý (no-cloning).
- Bất đẳng thức CHSH: |S| <= 2 với biến ẩn cục bộ, tới 2·sqrt2 với vướng mắc cực đại.
- Kiểm chuẩn vector = 1 và ma trận unita trước khi báo kết quả.

## Bẫy

- Nhầm thứ tự bit (bit đầu là qubit 1 hay qubit cuối). Chốt thứ tự và ghi rõ.
- Quên liên hợp phức khi tính U†: phải chuyển vị VÀ liên hợp.
- Đo rồi vẫn dùng trạng thái cũ: sau khi đo, trạng thái đã sụp.
- Coi "xác suất đo 0.5" là bằng chứng vướng mắc: cần kiểm tương quan giữa các qubit.
