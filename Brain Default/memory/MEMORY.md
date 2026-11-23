# Bộ nhớ Javis - Index

> Chỉ mục bộ nhớ dài hạn của Javis. Mỗi dòng = 1 ký ức, trỏ tới file trong `facts/`.
> Nội dung file này được nạp vào đầu mỗi câu hỏi để Javis nhớ ngữ cảnh.

- [Quy tắc trả lời mọi câu hỏi](facts/quy-tac-tra-loi-moi-cau-hoi.md) - Chuẩn mực trả lời mặc định, trung thực, kiểm chứng được và văn phong truyền thông đa kênh.
- [Lệnh chạy Antigravity CLI](facts/antigravity-cli-command.md) - User xác nhận lệnh chạy Antigravity CLI trong terminal là agy.
- [Tên trợ lý là Javis](facts/tro-ly-duoc-goi-la-javis.md) - Người dùng muốn gọi trợ lý là Javis.
- [Kích hoạt Antigravity CLI và cầu nối Second Brain](facts/kich-hoat-antigravity-cli-va-cau-noi-second-brain.md) - Đã kích hoạt Antigravity CLI và thiết lập bridge đọc/ghi Second Brain 2 chiều.
- [Gửi video là bắt đầu tiếp nhận biên tập](facts/quy-trinh-bien-tap-video-studio.md) - Khi chủ gửi tệp video, mặc định mở `skills/video-animation-toolkit/references/quy-trinh-bien-tap-studio.md`; xác nhận brief, chốt phương án, duyệt từng mốc rồi mới xuất MP4.
- [Cầu nối Claude Desktop vào Javis qua MCP stdio](facts/cau-noi-claude-desktop-vao-javis-mcp-stdio.md) - Claude Desktop gọi tool Javis qua script bridge Python nối tới hub `127.0.0.1:7777/hub/mcp`.
- [Nhờ ChatGPT Desktop và Claude Desktop xử lý việc Javis bị chặn](facts/nho-va-app-desktop-chatgpt-claude.md) - Có `handoff.ps1` gửi prompt và đọc trả lời tự động cho cả 2 app.
- [Nới quyền computer-use trong guidance.md và AGENTS.md](facts/noi-quyen-computer-use-guidance-agents.md) - Đã vá guidance.md và tạo AGENTS.md với pre-approval.
- [Bàn giao việc bị chặn sang ChatGPT Desktop](facts/chuyen-tac-vu-sang-chatgpt-desktop-khi-bi-chan.md) - Chuyển phần việc còn vướng sang ChatGPT Desktop nếu có công cụ được phép.
- [Repository GitHub chính chủ](facts/repository-github-chinh-chu.md) - Repository của chủ là `luongthethang-hub/javis-os`.
- [Ngừng DeepSeek local, gỡ Ollama](facts/ngung-deepseek-local-go-ollama.md) - Đã xóa 3 model DeepSeek và gỡ Ollama.
- [Kế hoạch nâng cấp máy, chuyển Ubuntu](facts/ke-hoach-nang-cap-may-chuyen-ubuntu.md) - Nâng cấp phần cứng và chuyển Ubuntu Desktop 24.04 LTS.
- [Mô hình Truyền thông Đa kênh & Thương hiệu Cá nhân](facts/mo-hinh-van-hieu-truyen-thong-da-kenh-va-thuong-hieu-ca-nhan.md) - Tái cấu trúc Javis OS chuyên trách Fanpage, Zalo, TikTok, YouTube và Thương hiệu cá nhân.
- [Dự án EA T-signal SEMI robot](facts/du-an-ea-t-signal-semi-robot.md) - Người dùng đang phát triển Expert Advisor bán tự động trên MQL5 có tên T-signal EA SEMI robot.
- [Quy trình tạo video mặc định Voice-First](facts/quy-trinh-tao-video-voice-first.md) - Mặc định áp dụng Quy trình B (Voice-First: Kịch bản -> Voice/Audio Anchor -> Timestamp -> Dựng hình & Motion Sync) cho video có giọng đọc; video không lời giữ quy trình Visual-First.
- [Bảo mật Telegram bằng Behavioral Biometrics](facts/bao-mat-telegram-behavioral-telemetry.md) - Cơ chế bảo mật thích ứng cho Telegram: Fast Path theo văn phong, hạ quyền Safe Mode và hỏi bẫy Second Brain khi lệch hành vi, cảnh báo out-of-band.
- [Hồ sơ Nhận diện Hành vi (Behavioral Telemetry Profile)](facts/behavioral-telemetry-profile.md) - Đặc trưng văn phong, khung giờ hoạt động, thang điểm rủi ro và ngân hàng câu hỏi bẫy ngữ cảnh Second Brain cho Telegram.
- [Phòng họp nội bộ](facts/phong-hop-noi-bo-3-ben.md) - Phòng họp nội bộ Telegram giữa Thắng Lee và Javis.
- [Giao thức phòng họp nội bộ, đồng tiến hóa chéo và sao lưu kép Antigravity - Javis](facts/giao-thuc-phong-hop-dong-tien-hoa-va-sao-luu-kep.md) - Giao thức phòng họp 3 bên, đồng tiến hóa chéo và sao lưu kép Antigravity - Javis.
- [Kiểm tra xung đột trước khi tự nâng cấp](facts/kiem-tra-xung-dot-truoc-khi-nang-cap.md) - Trước khi nạp tri thức mới hoặc tự nâng cấp, Javis bắt buộc kiểm toán ràng buộc cứng, đối soát xung đột logic, chạy shadow test và bảo đảm khả năng hoàn tác.
- [Chuẩn voice engineering cho video động lực](facts/chuan-voice-engineering-video-dong-luc.md) - Giọng nam NamMinhNeural (-3%, -6Hz) cộng chuỗi DSP FFmpeg tạo độ khàn nội lực; bẫy Azure TTS với chữ Đ viết hoa đầu câu.
- [A2A bus Javis - Antigravity](facts/a2a-bus-javis-antigravity.md) - Hộp thư file cục bộ memory/a2a_bus/ (inbox_antigravity.jsonl, inbox_javis.jsonl) vì bot Telegram không đọc được tin của nhau.
- [Đồng bộ tri thức Claude Desktop và ChatGPT Desktop](facts/dong-bo-tri-thuc-claude-chatgpt-desktop.md) - Claude Desktop nối lại MCP 23/11 lúc 08:05; ChatGPT Desktop chưa đồng bộ; Claude Alliance Contract mới là đề xuất.
- [Javis chia việc cho Claude Desktop qua handoff](facts/giao-viec-javis-cho-claude-desktop.md) - Javis ghi req vào memory/a2a_bus/claude/, chạy handoff.ps1 -App claude, nhận res tự động; việc HIGH/CRITICAL cần chủ gõ Y; hop tối đa 2; chưa kiểm chứng end-to-end.
- [Ma trận năng lực Liên minh AI](facts/agent-capability-matrix.md) - Ma trận năng lực thực chứng, thang điểm QC-5 và định tuyến tác vụ cho các Agent trong Liên minh do Javis làm Thủ lĩnh.
- [Khắc phục triệt để lỗi mất kết nối Antigravity CLI sau khi cập nhật Javis](facts/fix-antigravity-cli-reconnect-timeout-javis-update.md) - Vá lỗi kiem_tra_nhanh timeout và persistent auth cache cho Antigravity CLI trong Javis OS.
- [Vòng lặp Đồng bộ & Hiệu chỉnh Tri thức Phản hồi](facts/vong-lap-dong-bo-va-hieu-chinh-tri-thuc-phan-hoi.md) - Giao thức tự động hiệu chỉnh tri thức dựa trên phản hồi của Model đối tác, kiểm toán hạt nhân T0, timeout 10 phút và ngắt an toàn báo Layer 0.
