---
type: decision
created: 2026-11-18
updated: 2026-11-20
source: chat 2026-11-18 (2098bbec)
---
Dự án AI Company OS được triển khai trực tiếp trong Brain Default của Javis OS, không tạo Brain mới. Ưu tiên tái sử dụng Agents/Workflows hiện có; Content workflow có Blue draft, một vòng Red Team, Research/Fact-check, biên tập và kết thúc chờ chủ duyệt. Không bật tự đăng, giao dịch MT5 hoặc tự sửa prompt/quyền trong phạm vi đã duyệt.

**Vì sao:** Founder đã duyệt Phương án 1 và 2, sau đó xác nhận muốn chỉnh sửa trực tiếp Brain Default.

**Áp dụng:** Tái sử dụng workflow `san-xuat-content-video-ngan`; mọi thay đổi phạm vi Affiliate, MT5 hoặc đăng tự động cần quyết định riêng.

## Đội hình chạy thử Gate 1, 2026-11-19
- Giữ danh sách trợ lý hiện có. Điều phối AI Company xử lý việc thường lệ, mời người kiểm chứng, phản biện hoặc quản trị rủi ro theo việc.
- Content mặc định gồm Trợ lý Content viết, Phản biện nội dung rà và Kiểm duyệt bàn giao chờ chủ duyệt. Giám đốc Marketing chốt hướng và kiêm đầu mối nghiên cứu Affiliate thử nghiệm. Khởi động thử nghiệm Affiliate cần offer, điều khoản và tracking đã xác nhận.
- Nghiên cứu thị trường mặc định gồm kiểm chứng dữ liệu, phân tích và quản trị rủi ro. Mời chuyên viên hoặc CIO khi có câu hỏi cụ thể cần xử lý.

## Phản biện Red/Blue Team

- Ngày 19/11/2026 lúc 23:09, chủ chốt triển khai mức đầy đủ cho toàn bộ AI Company. Quy trình gồm Red Team chỉ ra lỗi, Blue Team phản hồi và chỉnh bản, thư ký ghi các điểm bất đồng và phán quyết. Nguồn: [nhật ký hội thoại ngày 19/11](../conversations/2026-11-19.md).
- Phê duyệt lưu quyết định từ báo cáo tự học 00:00 ngày 20/11/2026. Tại thời điểm ghi, [quy trình Red/Blue Team](../../workflows/red-blue-team-review.md) và [Debate Engine](../../plugins/debate-engine/plugin.yaml) đều đang tắt.
