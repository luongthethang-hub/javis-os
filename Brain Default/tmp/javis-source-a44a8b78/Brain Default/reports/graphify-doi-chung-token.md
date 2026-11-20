# Đối chứng token Graphify

Đo ngày 19/11/2026, giờ Asia/Bangkok. Kết luận cho mẫu này: ngữ cảnh có Graphify dùng thêm 61 token đầu vào (+0,22%). Chưa đủ bằng chứng để kết luận mức tiết kiệm cho luồng Javis hoàn chỉnh.

- Một cặp, hai phiên Codex mới với cùng model `gpt-6.2-sol`, mức suy luận thấp, cùng câu hỏi về luồng `GET /usage/summary` và cách tính `avg_per_turn`. Model nhận cùng các đoạn mã đã kiểm chứng và một kết quả tra cứu ban đầu, rồi trả lời trong một lượt.
- Nhánh thường dùng kết quả `rg`. Nhánh Graphify dùng kết quả thật của `query_graph` từ MCP Javis (BFS, độ sâu 2, ngân sách 500 token cho kết quả; công cụ báo cắt bớt kết quả). Đo bằng dữ liệu sử dụng do Codex trả về. Hai câu trả lời đều trỏ đúng nơi giao diện gọi API, trình xử lý, hàm tổng hợp, công thức và trường hợp 0 lượt.
- Không Graphify: 27.295 token đầu vào, 219 đầu ra. Có Graphify: 27.356 đầu vào, 230 đầu ra. Đây là tổng token đầu vào tính cả phần đã lưu đệm. Hai phiên có mức lưu đệm khác nhau, nên không suy ra chênh lệch phí.
- Phép đo này tính phần ngữ cảnh đã chuẩn bị và câu trả lời. Phép thử tương tác nhiều lượt chưa tạo được đối chứng hợp lệ: tìm mã bị chặn bởi `CreateProcess: rejected: blocked by policy`, còn phiên Codex thử gọi MCP trả `MCP tool call requires approval, but approval policy is never.` Không dùng số token của các lần thử lỗi làm bằng chứng hiệu quả.
- Bản mã và chỉ mục báo HEAD `fe6c74c50e7cb55628e3276318a2e6b5bf83b578`. Bản làm việc của `server/main.py` có chỉnh sửa ngoài xử lý Usage đang đo. Ba tệp được kiểm chứng là `dashboard/usage.js`, `server/main.py`, `server/usage_index.py`. Khi mã/đồ thị đã đổi, dùng mẫu này như kết quả lịch sử.
- Các lượt kiểm tra đã biết ngày 19/11/2026 (Asia/Bangkok), loại khỏi số sử dụng thường lệ: `23:36:43 query_graph`, `23:36:47 get_node`, `23:40:22 graph_stats`, `23:42:35 query_graph`.
