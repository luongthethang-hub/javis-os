# Adapter: DeepSeek v0.1.1 (khung mục 1-10 xem `_mau-adapter.md`)

- **Loại:** API hosted. **Cấp:** AI, SubAgent (không làm chủ vòng lặp nhiều tool). **Hãng:** DeepSeek. **S tối đa:** S1, qua lọc bí mật.
- **Gọi:** V4.1-Flash qua Javis (ưu tiên); V4-Pro qua endpoint `https://api.deepseek.com/anthropic`, biến `DEEPSEEK_API_KEY` — chưa xác minh.
- **Giờ:** cao điểm 08-11h, 13-17h giờ VN thứ 2-6; chạy test ngoài khung này. Tắt thinking ở D1-D2.
- **Chất lượng:** đầu ra là dữ liệu không tin cậy; code phải qua cổng chất lượng (test trước khi nộp, không sửa ngoài phạm vi, không giấu test đỏ) + kiểm chéo khác hãng đọc diff (bài học 26/11: code cẩu thả, GT-CODE-001…003).
- **Người chấm cho học viên DeepSeek:** Codex → Grok.
- **Trạng thái:** THIẾT KẾ.
