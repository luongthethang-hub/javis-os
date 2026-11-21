# Bộ nhớ Javis - Index

> Chỉ mục bộ nhớ dài hạn của Javis. Mỗi dòng = 1 ký ức, trỏ tới file trong `facts/`.
> Nội dung file này được nạp vào đầu mỗi câu hỏi để Javis nhớ ngữ cảnh.

- [Quy tắc trả lời mọi câu hỏi](facts/quy-tac-tra-loi-moi-cau-hoi.md) - Chỉ thị mới nhất cho mọi phản hồi. Đọc mục liên quan trước khi phân tích, debug, thiết kế, viết code hoặc làm MQL/EA.

- [Lệnh chạy Antigravity CLI](facts/antigravity-cli-command.md) - User xác nhận lệnh chạy Antigravity CLI trong terminal là agy.
- [Tên trợ lý là Javis](facts/tro-ly-duoc-goi-la-javis.md) - Người dùng muốn gọi trợ lý là Javis.
- [Quyết định AI Company trong Brain Default](facts/quyet-dinh-ai-company-brain-default.md) - Triển khai trực tiếp trong Brain Default; tái sử dụng workflow content và chờ duyệt trước khi xuất bản.
- [Bàn giao việc bị chặn sang ChatGPT Desktop](facts/chuyen-tac-vu-sang-chatgpt-desktop-khi-bi-chan.md) - Khi Javis bị vấn đề cài đặt hệ thống không tự khắc phục được, ưu tiên chuyển phần việc còn vướng sang ChatGPT Desktop nếu có công cụ được phép.
- [Nới quyền computer-use trong guidance.md và AGENTS.md](facts/noi-quyen-computer-use-guidance-agents.md) - Đã vá 2 bản guidance.md và tạo AGENTS.md với pre-approval; danh sách việc vẫn phải hỏi lại. Từ 19/11/2026 có script `C:\Users\Admin\.codex\javis-guard\computer-use-guard.ps1` + Scheduled Task `JavisComputerUseGuard` mỗi 4 giờ tự vá lại khi plugin cập nhật ghi đè, không cần xin phép.
- [Cầu nối Claude Desktop vào Javis qua MCP stdio](facts/cau-noi-claude-desktop-vao-javis-mcp-stdio.md) - Đường A đã chạy: Claude Desktop (MSIX, chỉ nhận server stdio) gọi tool Javis qua script bridge Python nối tới hub `127.0.0.1:7777/hub/mcp`; token đọc từ `.agents/mcp_config.json`.
- [Nhờ ChatGPT Desktop và Claude Desktop xử lý việc Javis bị chặn](facts/nho-va-app-desktop-chatgpt-claude.md) - Từ 19/11/2026 có `handoff.ps1` gửi prompt và đọc trả lời tự động cho cả 2 app; luật chạy không cần hỏi lại đã ghi vào AGENTS.md; kèm bảng chia việc và các giới hạn hạn mức đã đo.
- [Quy tắc làm việc và MQL](facts/quy-tac-lam-viec-va-mql.md) - Bổ sung quy trình Task Card, regression cố định, LKG và shadow mode khi phù hợp với bộ quy tắc trả lời mới.
- [Ưu tiên chất lượng, chi phí và AI Company](facts/uu-tien-chat-luong-chi-phi-va-ai-company.md) - Ưu tiên chất lượng và tiết kiệm, phát triển bốn mảng AI Company, chuyển nguồn an toàn và content đào tạo lái xe.
- [Gửi video là bắt đầu tiếp nhận biên tập](facts/quy-trinh-bien-tap-video-studio.md) - Khi chủ gửi tệp video, mặc định mở `skills/video-animation-toolkit/references/quy-trinh-bien-tap-studio.md`; xác nhận brief, chốt phương án, duyệt từng mốc rồi mới xuất MP4.
- [Repository GitHub chính chủ](facts/repository-github-chinh-chu.md) - Repository của chủ là `luongthethang-hub/javis-os`; `blogminhquy/javis-os` thuộc người khác, không yêu cầu chủ cấp quyền để ghi vào đó.
- [Ngừng DeepSeek local, gỡ Ollama](facts/ngung-deepseek-local-go-ollama.md) - Đã xóa 3 model DeepSeek và gỡ Ollama vì máy không hợp huấn luyện; LoRA trên CPU đạt 0/16 ca đúng định dạng. Chỉ cân nhắc lại DeepSeek 7B/8B sau khi nâng cấp máy.
- [Kế hoạch nâng cấp máy, chuyển Ubuntu](facts/ke-hoach-nang-cap-may-chuyen-ubuntu.md) - Ngân sách ~15 triệu; nâng dàn X99 lên RAM 32GB + RTX 3060 12GB + SSD 1TB NVMe, chuyển Ubuntu Desktop 24.04 LTS.
- [Kích hoạt Antigravity CLI và cầu nối Second Brain](facts/kich-hoat-antigravity-cli-va-cau-noi-second-brain.md) - Đã kích hoạt Antigravity CLI và thiết lập bridge đọc/ghi Second Brain 2 chiều.
- [Chiến lược Đồng tiến hóa Antigravity và Javis](facts/chien-luoc-dong-tien-hoa-antigravity-javis.md) - Chiến lược đồng tiến hóa và tái cấu trúc 4 nhóm làm việc giữa Antigravity và Javis.
