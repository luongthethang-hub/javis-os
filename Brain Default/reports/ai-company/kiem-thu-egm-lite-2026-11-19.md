# Kiểm thử EGM Lite cho quy trình phát triển EA

Ngày 19/11/2026. **Quyết định: chưa nhân rộng EGM Lite hai lượt.** Giữ một lượt phản biện bản vá và ưu tiên chạy phiên mới với một gói đầu vào xác định. Chỉ cân nhắc lượt xem riêng Task Card đối với thay đổi có nhiều trạng thái rủi ro hoặc điều kiện khôi phục.

## Đối chứng

Thử trên bốn Task Card MQL5 mô phỏng, gồm khóa mở lệnh khi chạm mức sụt giảm vốn, làm tròn khối lượng, gửi lại yêu cầu và một refactor giữ nguyên hành vi. Ba ca đầu có tổng cộng bảy lỗi mã cài trước và sáu khoảng trống đặc tả hoặc độ phủ. Ca sạch giữ nguyên kết quả ở cả tám tổ hợp đầu vào.

Mỗi ca dùng ba cách rà trên cùng đặc tả và diff, cùng model `gpt-6.2-sol` và cùng mức suy luận thấp. Cách thứ nhất nhận thêm ghi chú hội thoại mô phỏng. Cách thứ hai nhận Task Card và diff trong một phiên mới. Cách thứ ba có hai phiên mới, một phiên chỉ nhận Task Card và một phiên nhận Task Card cùng diff. Mỗi reviewer không dùng công cụ. 16 lượt có 16 mã phiên khác nhau và đều trả kết quả. Chấm thủ công theo đáp án lưu trước khi chạy review. Khi một phát hiện chứa hai cơ chế riêng biệt, mỗi cơ chế được tính một lần. [Bộ thử](../../tmp/egm-pilot-a1c127e2/pilot.py) · [Đáp án](../../tmp/egm-pilot-a1c127e2/ground-truth.md)

| Cách rà | Lỗi mã bắt được | Khoảng trống bắt được | Báo sai ở ca sạch | Trung vị thời gian mỗi ca | Tổng token đầu vào |
|---|---:|---:|---:|---:|---:|
| Một lượt có ghi chú hội thoại | 7/7 | 6/6 | 0 | 13,4 giây | 73.200 |
| Một lượt phiên mới | 7/7 | 6/6 | 0 | 13,3 giây | 75.012 |
| Hai lượt phiên mới theo EGM Lite | 7/7 | 6/6 | 1 | 23,6 giây | 149.764 |

Thời gian cho mô hình hai lượt là tổng hai lượt trong từng ca, mô phỏng hai cổng nối tiếp. Số token là đầu vào Codex CLI ghi nhận, đã gồm token cache. Cách hai lượt tiêu thụ 30.468 token đầu vào ngoài cache, so với 19.204 của một lượt phiên mới. Hai lượt tốn khoảng gấp đôi tổng token đầu vào và thêm 10,3 giây trung vị so với một lượt phiên mới, tính trên các ca mô phỏng này. Đây là khối lượng sử dụng mô hình, không quy đổi thành tiền.

Tất cả các cách bắt được lỗi cho mở lệnh khi chưa khôi phục trạng thái, lỗi mở lệnh đúng ngưỡng và lỗi gửi lại khi chưa rõ kết quả. Lượt chỉ đọc Task Card đề xuất thêm cách kiểm sự kiện đồng hồ máy chủ lùi qua nửa đêm và cách diễn giải lưới lot ở biên số thực. Lượt đó cũng chặn ca sạch vì giả định bản chuẩn có thể mâu thuẫn với hợp đồng. Diff và toàn bộ tám tổ hợp của ca sạch không cho thấy mâu thuẫn ấy.

## Kiểm tra trên Codex CLI và Windows

- Smoke test chạy trên Codex CLI 0.169.0, dùng đăng nhập ChatGPT sẵn có.
- Nhật ký gốc xác nhận reviewer con thực sự khởi chạy và hoàn tất với `fork_turns: "none"`. Nó trả `PARENT=UNKNOWN` cho mã đánh dấu chỉ nằm trong lượt cha, đồng thời đọc được đúng mã trong `AGENTS.md` của dự án ngay cả khi không gọi công cụ. Phiên mới tách lượt hội thoại trong phép thử này. Muốn giới hạn dữ liệu đọc được cần thêm ràng buộc ở môi trường chạy. [Kết quả phép thử cách ly](../../tmp/egm-pilot-a1c127e2/native-verification.json) · [Tài liệu Codex của EGM](https://github.com/luongthethang-hub/elephant-goldfish-model/blob/70406c4/docs/codex.md#L40-L67)
- Trong thử nghiệm cổng rà diff, Codex CLI ở chế độ chỉ đọc gặp `CreateProcess: rejected: blocked by policy` khi tự đọc tệp qua shell. Khi trình chạy bên ngoài đọc các tệp chỉ định và truyền nội dung vào phiên, ca đủ hồ sơ khởi chạy đúng một reviewer tách lượt cha và xác nhận hai lỗi mã. Ca thiếu `AFTER.txt` trả `INCOMPLETE` và nhật ký xác nhận không gọi reviewer. [Kết quả cổng rà diff](../../tmp/egm-pilot-a1c127e2/protocol-verification.json) · [Đặc tả EGM Lite](https://github.com/luongthethang-hub/elephant-goldfish-model/blob/70406c4/skills/egm-lite/SKILL.md#L284-L353)
- Bộ test repo tại commit `70406c4d22cc7ea8299637c2c5b44625c48b3f08` trên Windows cho 370 đạt, 3 bỏ qua, 16 chưa đạt sau khi đưa Git Bash sẵn có vào PATH của tiến trình. Các ca chưa đạt vướng quyền tạo liên kết tượng trưng của Windows, `WinError 1314`. Gói OpenAI dựng từ repo và vượt qua kiểm tra tính toàn vẹn ZIP. [Log bộ test Windows](../../tmp/egm-pilot-a1c127e2/unit-windows.txt) · [Log kiểm tra nguyên nhân](../../tmp/egm-pilot-a1c127e2/unit-symlinks.txt) · [Quy trình test chính thức](https://github.com/luongthethang-hub/elephant-goldfish-model/blob/70406c4/TESTING.md)

## Điều kiện trước khi xét nhân rộng

Mẫu thử nhỏ, diff ngắn, cùng một model và mỗi cách chỉ chạy một lần trên từng ca. Baseline có hội thoại là đối chứng mô phỏng. Một lượt phiên mới gần với bước reviewer khai báo trong workflow EA. Thí nghiệm chạy trên Codex CLI. Chưa chạy workflow EA trong Javis, chưa cài plugin EGM, chưa chạy toàn bộ luồng native chính thức và chưa kiểm chứng compile `strict`, regression so bản chuẩn hoặc shadow/demo trên EA thật. [Cấu hình workflow EA](../../workflows/phat-trien-ea-ban-va.md)

Khi có Task Card EA thật và môi trường chạy tách biệt, dùng một reviewer phiên mới làm chuẩn. Chỉ thử thêm cổng đặc tả với việc ảnh hưởng giới hạn vốn, xử lý lệnh hoặc khôi phục trạng thái. Chỉ xét mở rộng khi cổng này tìm lặp lại được lỗi nghiêm trọng mà một reviewer bỏ sót, có ca tái hiện, và mức tăng thời gian cùng báo sai chấp nhận được. Compile `strict`, regression so bản chuẩn và shadow/demo vẫn là các cổng nghiệm thu của EA.
