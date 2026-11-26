# Adapter: Javis (đội đa model trên máy L0) v0.1.1

1. **Loại:** AgentOS cục bộ có đội model, hàng đợi Kanban, vault git (Second Brain).
2. **Cách gọi:** MCP `javis` trên máy L0 (đã thấy trạng thái announced 26/11). Giao việc qua Kanban vào nhóm **"Hội đồng Huấn luyện - Teacher Agent"** (`tm_398ab42dc2571a64`). Cách gọi chi tiết từng thành viên: CHƯA XÁC MINH.
3. **Cấp áp dụng:** người chấm và thợ của HLV; cũng có thể là học viên (AgentOS) sau này.
4. **Thành viên:** Codex (gpt-6.2-sol), Luna (gpt-6-luna), Sol (gpt-5.6-sol), Grok 4.7, Gemini Flash 3.8, Antigravity (gemini-3.8-flash-high), DeepSeek V4.1-Flash, Sonnet 4.6. Hãng xem `khung/hoi-dong-cham.md`.
5. **Luật giao gói (từ bài học 26/11, GT-PHOIHOP-002):**
   - Trước khi giao: liệt kê việc đang chạy ở mọi kênh (Kanban, các luồng claude.ai), không giao trùng mục tiêu.
   - Giao thử 1 gói, xác nhận **đọc lại được kết quả** từ phiên HLV, rồi mới giao hàng loạt.
   - Mỗi gói phải có đường nhận kết quả (chat_id hoặc đường dẫn file kết quả trong vault).
   - Gói chấm: không chứa tên học viên (chấm mù), có `tieu_chi_nghiem_thu` cố định.
6. **Đầu ra chuẩn hóa:** `{id_de, nguoi_cham, hang, diem, ly_do, nguon:"javis", chi_phi}` ghi vào `teacher-agent/hoc-vien/<id>/ket-qua/`.
7. **Giới hạn dữ liệu:** theo từng thành viên: Claude ≤S2; GPT/Grok/Gemini/DeepSeek hosted ≤S1; Ollama ≤S2 (trong máy). S3 không đi đâu.
8. **Giá:** chủ yếu gói thuê bao đã trả (chi phí biên ~0, E4). Ghi hạn mức còn lại nếu Javis báo được.
9. **Sandbox:** gói code chạy trong thư mục/nhánh riêng; không bao giờ trên repo CAM OS (Doctor Agent là nơi duy nhất sửa code CAM).
10. **Trạng thái:** ĐÃ THẤY MCP — chưa giao gói thử nào.
