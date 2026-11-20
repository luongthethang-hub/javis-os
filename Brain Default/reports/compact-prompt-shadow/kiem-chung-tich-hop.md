# Kiểm chứng vòng 2 và phương án tích hợp mặc định

Ngày 20/11/2026. Phương án đề xuất là mở rộng chế độ `max` theo từng loại việc. Giai đoạn đầu chỉ thử lượt đọc độc lập có đúng một công cụ đọc đã được xác nhận. Giữ đường Codex hiện tại cho hội thoại đang nối mạch. Cấu hình đang chạy vẫn ở `max`. Tỷ lệ phân luồng `readonly_canary` hiện là 0.

## Quyền công cụ lúc thực thi

- Phép thử qua `_scope_tools` và `mcp_client.call_route` chạy 10 ca. Một lệnh đọc mẫu đến handler, chín ca bị chặn. Các ca bị chặn gồm thao tác ghi, tham số thiếu hoặc thừa, tên ngoài danh sách, công cụ MCP tổng quát và yêu cầu đọc sau khi quyền mẫu đã bị thu hồi.
- Kiểm tra hàm xử lý của plugin lịch hiện tại với kho loop và reminder giả lập. Đọc trả kết quả từ cả hai kho. Plugin đăng ký `min_mode=safe` vì cùng một công cụ có cả đọc và ghi. Thử đối chứng cho thấy hàm thô chọn nhánh `create` khi thiếu `op`. Với lớp chặn, chỉ đúng `{"op":"list"}` đến được hàm xử lý và không nhánh ghi nào được gọi. Các nhánh ghi trong phép đối chứng đều là hàm giả.
- Sửa bộ dựng để giữ đường đầy đủ khi tác vụ cần `javis_search_tools` hoặc `javis_run_tool`. Bản chạy lại chọn đường tinh gọn cho 13/32 ca, giảm 43,53% token ước tính trên chính bộ mẫu này. Tỷ lệ thấp hơn vòng 1 vì các ca kinh doanh và tài chính qua MCP tổng quát đã về đường đầy đủ.

## Cache và chất lượng nối phiên Codex

Chạy hai cặp đối chứng hoàn chỉnh với Codex app-server 0.169.0 và `gpt-6.2-sol`. Hai nhánh trong mỗi cặp dùng cùng câu hỏi, quyền và công cụ lịch mẫu. Lượt đầu gọi công cụ. Lượt thứ hai giữ tiến trình. Lượt thứ ba mở lại app-server và dùng `thread/resume`. Lần đo thứ hai đổi thứ tự hai nhánh, làm rõ lựa chọn Telegram chỉ có hiệu lực trong hội thoại và thêm phép kiểm tra chỉ dẫn lúc mở thread. Hai nhánh đều đạt nội dung kiểm tra trong mỗi cặp. Mỗi nhánh có một lần đọc trên ba lượt, không có lần thực thi bổ sung khi nối mạch.

| Cặp đo | Phiên bản | Tổng đầu vào | Đọc từ cache | Không cache |
|---|---|---:|---:|---:|
| 1 | Đầy đủ | 104.697 | 77.696 | 27.001 |
| 1 | Tinh gọn | 66.821 | 33.024 | 33.797 |
| 2 | Đầy đủ | 104.409 | 77.568 | 26.841 |
| 2 | Tinh gọn | 66.734 | 33.024 | 33.710 |
| Gộp | Đầy đủ | 209.106 | 155.264 | 53.842 |
| Gộp | Tinh gọn | 133.555 | 66.048 | 67.507 |

Số từ app-server có đối chiếu counters theo request, tám request mỗi nhánh. Tổng token đầu vào giảm 36,13%, token không cache tăng 25,38%. Bản tinh gọn gặp một lượt cache bằng 0 trong mỗi cặp: lượt nối mạch cùng tiến trình ở cặp 1 và lượt khởi động lại tiến trình ở cặp 2. Khi trúng cache, lượt nối mạch tinh gọn chỉ còn 217 đến 360 token không cache. Khi trượt cache, hai lượt tương ứng là 16.771 và 16.833. Mẫu này không xác định được nguyên nhân trượt cache, tỷ lệ trượt trên lưu lượng thực hay tác động đến hạn mức gói.

Riêng hai lượt mở phiên có gọi công cụ, token không cache giảm từ 52.507 xuống 33.326 (36,53%). Đây là số đo trên một loại tác vụ mẫu, dùng để chọn phạm vi thử đầu tiên.

Mỗi lần nối lại đều giữ mã báo cáo, giờ chạy và lựa chọn Telegram. Lượt sau khi khởi động lại lấy giờ hiện tại từ dữ kiện mới của gateway thay cho giờ ở lượt đầu. Ở cặp 2, cả hai bản còn lấy đúng mã đặt riêng trong developer instructions khi tạo thread. Các câu được chấm theo dữ kiện và điều kiện gọi công cụ. Bộ thử chưa bao phủ chat dài đã nén, đổi quyền trên gateway đang chạy hoặc nhiều loại tool trong một phiên.

Một lần chạy xen giữa hết thời gian chờ 25 giây khi nhánh đầy đủ nối lại. Tăng thời gian chờ toàn lượt lên 75 giây cho phép hoàn tất cặp thứ hai. Số từ lần dở dang không được gộp vào bảng. Ba bộ hồi quy `codex_steer_0213`, `readonly_path_phase6` và `subscription_usage` qua. `codex_context` in 16 dòng kiểm tra đạt nhưng tiến trình trả lỗi khi dọn `old.db` do khóa file Windows (`WinError 32`), nên bộ đó chưa xanh.

## Phương án đưa vào mặc định

1. Giữ đường tắt `max` cho hỏi đáp đơn giản. Bổ sung một tuyến đọc độc lập tại gateway theo mô hình `readonly_path`. Bắt đầu với đọc trạng thái lịch. Tách quyền đọc lịch thành capability cố định gọi nhánh đọc của plugin, dùng đúng brain và chủ phiên. Reuse cả hai nguồn loop và reminder. Không đưa schema hỗn hợp vào nhánh đọc. Lọc danh sách công cụ trước khi tạo route, kiểm tra quyền và tham số lại khi thực thi. Ưu tiên đối tượng đã được bộ định tuyến xác định chắc chắn. Thiếu bằng chứng phạm vi thì dùng tuyến hiện tại.
2. Giữ tuyến đang dùng cho hội thoại Codex tiếp nối. Nếu thử prompt tinh gọn trên thread Codex mới, đặt bộ quy tắc cố định trong `developerInstructions` và giữ phiên bản của nó suốt thread. Chuyển dữ kiện theo lượt qua kênh metadata có nguồn gốc từ gateway. Gắn scope và phiên bản chính sách với thread và warm process. Khi thay đổi quyền, kiểm tra lại lúc thực thi ngay. Khi cần đổi gói chỉ dẫn cố định, mở thread mới và bàn giao dữ kiện đã kiểm chứng, sau khi đường bàn giao đã qua kiểm thử. Không xoay thread chỉ để làm ấm cache.
3. So với tuyến `max` thực tế trong chế độ shadow tích hợp. Đo riêng lượt mới, nối mạch cùng tiến trình và nối mạch sau khởi động lại. Chấm quyền, tính đúng của dữ kiện, tổng đầu vào, token không cache, số vòng model và độ trễ. Với nguồn thật, dùng lại bằng chứng của lượt chính để chấm thay vì gọi công cụ ra ngoài lần hai. Giữ nhánh mới ở trạng thái thử nếu tập đủ điều kiện tăng token không cache hoặc có lỗi vượt quyền, mất mạch, dùng giờ cũ hay báo đã ghi khi chưa ghi. Khi đạt, chỉ chọn làm mặc định cho tập tình huống đủ điều kiện đã đo và giữ công tắc quay về tuyến cũ.

Tái lập từ Brain Default: chạy `verify_integration.py` bằng Python môi trường ảo của Javis để kiểm tra quyền và plugin với dữ liệu mẫu. Thêm `--codex-bin` trỏ tới binary Codex cài sẵn để chạy app-server, và `--compact-first` để đảo thứ tự. Phép thử app-server dùng thư mục tạm và xác nhận native MCP không phát công cụ. Bảng đối chứng vòng 1 không mô tả phiên bản đã siết phạm vi ở vòng 2.
