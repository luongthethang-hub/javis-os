---
id: evo-bootstrap-2026-11-19
owner: dieu-phoi-ai-company
team: CEO SubAgents (tm_abf04e8e74479b9e)
status: todo
created: 2026-11-19
created_by: Claude (chat) theo yêu cầu của Thắng
---

# GIAI ĐOẠN 1 - KHỞI TẠO HỆ THỐNG TỰ TIẾN HÓA
(chỉ rà soát + đề xuất, chưa tự sửa hàng loạt)

## Bối cảnh
Chủ (Thắng) là Algorithmic Trading Developer / kỹ sư MQL5-MQL4 EA (order/position/basket management, risk control). Mục tiêu hệ thống: trading, EA, content, affiliate; hướng tới hệ thống đa năng, thông minh nhất có thể. Chủ đang dùng API và muốn chuyển sang gói thuê bao để giảm chi phí.

## Nhiệm vụ
1. Rà soát hiện trạng: agent, team, skill, workflow, schedule, MCP đã đấu. Chỉ ra trùng lặp, thiếu vai, agent chưa có model riêng. Ghi kết quả vào wiki/ hoặc inbox/proposals/.
2. Đề xuất phân bổ model theo vai, ưu tiên provider chạy bằng gói thuê bao (anthropic-cli cho Claude, openai-oauth cho ChatGPT) thay vì API key trả theo token. Kiểm chứng thật từng provider còn đăng nhập/khả dụng bằng 1 việc ngắn; báo rõ cái nào lỗi, không giả định.
3. Thiết kế vòng lặp phản biện chéo Claude <-> ChatGPT: tối đa 3 lượt mỗi việc, có timeout, ghi biên bản ai đề xuất / ai phản đối / lý do.
4. Đề xuất vòng tiến hóa: sau mỗi việc đóng, chấm điểm kết quả, ghi bài học vào wiki/, đề xuất sửa prompt/skill/workflow (qua skill javis-builder, chống trùng). Mọi thay đổi lên agent/skill/workflow hiện có phải nằm ở inbox/proposals/ chờ Chủ duyệt; không tự ghi đè.
5. Đề xuất lịch chạy định kỳ qua javis_schedule với muc_quyen = suggest hoặc auto (KHÔNG full).
6. Lập mảng việc theo 4 mảng: Trading/EA, Content, Affiliate, Hạ tầng; mỗi mảng nêu agent phụ trách, đầu vào/đầu ra, chỉ số đo hiệu quả.

## RÀNG BUỘC CỨNG
- Không đặt lệnh, không sửa lệnh, không thao tác tài khoản giao dịch/MT5; chỉ phân tích, ghi nhật ký, đề xuất.
- Không hành động ra ngoài (gửi tin, đăng bài, tạo đơn, thanh toán, đổi cấu hình tài khoản) khi chưa có Chủ duyệt.
- Không thêm MCP/nguồn chạy bằng lệnh, không đổi mức quyền, không xóa file/team/agent.
- Không bịa số liệu/API; điều gì không chắc ghi "không xác định" kèm cách kiểm chứng.
- Giữ ngân sách: không tạo vòng lặp vô hạn; báo ngay khi chạm giới hạn hạn mức gói thuê bao.

## Đầu ra
Báo cáo ngắn (<=400 từ): Kết luận -> Phương án -> Rủi ro -> Điều kiện áp dụng, kèm đường dẫn file đề xuất chi tiết, bằng tiếng Việt (giữ thuật ngữ kỹ thuật tiếng Anh). Kết thúc bằng "Bước tiếp theo" cần Chủ quyết.
