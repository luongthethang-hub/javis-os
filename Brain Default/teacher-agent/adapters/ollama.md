# Adapter: Ollama (model cục bộ) v0.1.1

1. **Loại:** model tự chạy trên máy L0 (thư mục `.ollama` có trên máy; danh sách model chưa kiểm).
2. **Cách gọi:** `ollama run <model>` hoặc HTTP `http://localhost:11434/api/chat` trên máy L0 — CHƯA XÁC MINH từ phiên HLV (cần Remote Control hoặc Javis gọi hộ).
3. **Cấp:** AI, SubAgent; người chấm D1-D2 rẻ cho học viên khác họ.
4. **Dữ liệu:** tối đa S2 (không rời máy). S3 vẫn cấm.
5. **Giá:** 0 API; tốn điện/thời gian máy. Ưu tiên cho kiểm schema, chấm D1-D2, thợ khối lượng.
6. **Lỗi hay gặp (R2):** template chat sai làm hỏng định dạng; lượng tử hóa thấp giảm chất lượng; ngữ cảnh mặc định ngắn (num_ctx) cắt cụt đề.
7. **Hãng khi ghép chấm:** theo họ model gốc (Gemma = Google, Llama = Meta, Qwen = Alibaba…).
8. **Trạng thái:** THIẾT KẾ.
