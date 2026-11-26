# Adapter: <tên nền tảng> v0.1.0

Adapter là lớp tinh chỉnh (T3) nối khung chung với một nền tảng. Lõi chấm không đổi; adapter chỉ nói *cách đưa đề vào, cách lấy đầu ra, cách đọc dấu vết*.

1. **Loại:** model API | model tự chạy | agent CLI | framework đa agent | workflow | AgentOS tự xây | RAG | MCP server
2. **Cách gọi:** lệnh/endpoint/SDK; biến môi trường cần (tên biến, không ghi giá trị); timeout; giới hạn tốc độ
3. **Cấp áp dụng:** AI / Agent / SubAgent / AgentOS
4. **Đưa đề vào:** system prompt ở đâu; few-shot ở đâu; cách cấp công cụ giả (mock) cho bài test hành động
5. **Lấy đầu ra + dấu vết:** văn bản, JSON, lời gọi tool, log, trace; định dạng chuẩn hóa về `{id_de, dau_ra, tool_calls[], so_token_in, so_token_out, chi_phi, thoi_gian}`
6. **Giới hạn dữ liệu:** S tối đa (hosted ngoài → mặc định S1)
7. **Giá:** in/out/cache; ngày kiểm trang giá
8. **Lỗi thường gặp & gợi ý chẩn đoán R2** cho nền tảng này
9. **Cách sandbox:** thư mục/nhánh/môi trường riêng; cách chắc chắn không có tác dụng ra ngoài
10. **Trạng thái:** THIẾT KẾ | ĐÃ GỌI THỬ (ngày) | ỔN ĐỊNH
