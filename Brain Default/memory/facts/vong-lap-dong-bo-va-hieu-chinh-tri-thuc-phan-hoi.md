---
type: fact
provenance: agent
origin: javis-orchestrator
created: 2026-11-23
updated: 2026-11-23
source: user-idea-telegram-2026-11-23
status: verified
---
# Vòng lặp Đồng bộ & Hiệu chỉnh Tri thức Phản hồi (Feedback-Driven Knowledge Calibration Loop - FKCL)

Quy chuẩn tự động hội tụ tri thức đa tác tử giữa Javis (Thủ lĩnh/Second Brain) và các Model AI đối tác (Claude Desktop, Antigravity, Codex):

1. **Thu thập Phản hồi & Bóc tách Đóng góp (Feedback Ingestion):**
   - Khi Model AI đối tác thực hiện đồng bộ hoặc phản biện, Javis tự động bóc tách các điểm hoài nghi, ngoại lệ biên hoặc đề xuất cải tiến từ phản hồi của Model.

2. **Cổng Kiểm toán Ràng buộc Hạt nhân (Nuclear / T0 Gate):**
   - Mọi đóng góp được đối soát nghiêm ngặt với các quy tắc bất biến T0 (Bảo mật, an toàn tài khoản/Telegram, quản trị rủi ro MQL5, không bịa đặt dữ liệu, trần ngân sách rules).
   - Nếu vi phạm T0: Lập tức từ chối điểm đó, neo chặt luận cứ kỹ thuật.
   - Nếu hợp lý (T1/T2): Tinh chỉnh nguồn tri thức Second Brain (Fact, Wiki, Rules), làm rõ phạm vi áp dụng (Scope) và ngoại lệ (Exceptions).

3. **Vòng lặp Tái Đồng bộ (Iterative Convergence):**
   - Javis cập nhật tri thức xuống đĩa vật lý, sau đó phát yêu cầu Model AI đối tác đồng bộ lại với nguồn đã tinh chỉnh.
   - Lặp lại quy trình cho đến khi Model AI đối tác xác nhận trạng thái hội tụ (`status: synced` / `status: done`).

4. **Cơ chế Ngắt An toàn & Cứu hộ (Circuit Breaker & 10-Min Timeout):**
   - Giới hạn cứng: Thời gian hiệu chỉnh tối đa **10 phút** hoặc tối đa **3 vòng lặp** bế tắc không đạt đồng thuận.
   - Khi chạm trần hoặc phát hiện bất đồng không thể dung hòa: Tự động đóng băng tiến trình, giữ nguyên snapshot an toàn và phát báo cáo khẩn cấp lên Layer 0 (Thắng Lee) qua Telegram kèm 2-3 phương án giải quyết để trọng tài quyết định.

5. **Tổng hợp & Báo cáo Hội tụ (Post-Sync Summary):**
   - Khi hoàn tất, xuất báo cáo ngắn gọn: Số vòng lặp đã qua, danh sách điểm tri thức đã tinh chỉnh, và bằng chứng xác nhận từ Model đối tác.
