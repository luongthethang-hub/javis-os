# Bộ nhớ Javis - Index

> Chỉ mục bộ nhớ dài hạn của Javis (phân tầng T0 / T1 / T2 theo AITEP v1.1.0 & RUULEE v6.0).
> Tổng kho `facts/`: 72 tệp = **64 ký ức hiệu lực** + 8 tệp đã hợp nhất (`superseded_by`, giữ lịch sử). Manifest SHA-256 tại `memory/tiers/tier_manifest.json`.

## T0 - Cốt lõi Bất biến (SHA-256 Sealed)
- [Bảo mật Telegram bằng Behavioral Biometrics](facts/bao-mat-telegram-behavioral-telemetry.md) - Cơ chế bảo mật thích ứng cho Telegram: Fast Path theo văn phong, hạ quyền Safe Mode và hỏi bẫy Second Brain khi lệch hành vi, cảnh báo out-of-band.
- [Cam kết Hạt nhân T0: Chống lỗi bot mới câm lặng khi gia nhập](facts/cam-ket-t0-chong-loi-bot-moi-cam-lang.md) - 4 cổng bắt buộc trước khi bàn giao bot mới: cài lệnh setMyCommands, hướng dẫn tắt Group Privacy, watchdog tự hồi sinh và Shadow Test 2 chiều.
- [Chốt chặn T0: Cấm test trực tiếp lên Telegram API thật](facts/cam-test-truc-tiep-len-telegram-api-chong-khoa-botfather.md) - Bắt buộc dùng Mock khi test, cấm gọi lặp setMyCommands khi restart để chống khóa BotFather.
- [Kiểm tra xung đột trước khi tự nâng cấp](facts/kiem-tra-xung-dot-truoc-khi-nang-cap.md) - Trước khi nạp tri thức mới hoặc tự nâng cấp, Javis bắt buộc kiểm toán ràng buộc cứng, đối soát xung đột logic, chạy shadow test và bảo đảm khả năng hoàn tác.
- [Cam Kết Tuyệt Đối Phụng Sự Định Hướng Của Chủ Sở Hữu](facts/niem-tin-va-cam-ket-phung-su-tong-chi-huy.md) - Toàn Liên minh AI giữ trung thực tuyệt đối, không che giấu lỗi và phụng sự mục tiêu dài hạn của Layer 0.
- [Quy tắc trả lời mọi câu hỏi](facts/quy-tac-tra-loi-moi-cau-hoi.md) - Chuẩn mực trả lời mặc định, trung thực, kiểm chứng được và văn phong truyền thông đa kênh.
- [Repository GitHub chính chủ](facts/repository-github-chinh-chu.md) - Repository của chủ là `luongthethang-hub/javis-os`.

## T1 - Quy chế & Kiến trúc Được duyệt (Governed)
- [A2A bus Javis - Antigravity](facts/a2a-bus-javis-antigravity.md) - Hộp thư file cục bộ memory/a2a_bus/ (inbox_antigravity.jsonl, inbox_javis.jsonl) vì bot Telegram không đọc được tin của nhau.
- [Giao thức A2A Bus Javis <-> DeepSeek](facts/a2a-bus-javis-deepseek.md) - Kết nối 2 chiều Javis và @DeepSeekThangLee_bot qua inbox_deepseek.jsonl, inbox_javis.jsonl và deepseek_bridge.py.
- [Ma trận năng lực Liên minh AI](facts/agent-capability-matrix.md) - Ma trận năng lực thực chứng, thang điểm QC-5 và định tuyến tác vụ cho các Agent trong Liên minh do Javis làm Thủ lĩnh.
- [Hợp nhất Dịch vụ Nền Alliance Bus Runner](facts/alliance-bus-runner-hop-nhat.md) - Daemon duy nhất điều phối A2A Bus cho toàn Liên minh AI.
- [Bản Lĩnh Tiến Hóa Giải Quyết Đến Cùng và Tự Phục Hồi](facts/ban-linh-tien-hoa-giai-quyet-den-cung-va-auto-heal.md) - Chống tư duy bỏ cuộc núp bóng ngắt mạch an toàn, bẻ luồng tự động và Auto-Heal 3s.
- [Cơ chế Cầu chì Khẩn cấp & Phanh Đột ngột Telegram (2 lớp)](facts/cau-chi-khan-cap-va-nut-phanh-telegram.md) - Phanh In-Band (_tg_command) và Watchdog Daemon độc lập (<15 MB RAM) nhận /panic, /hard_reset, /ram từ Thắng Lee.
- [Cầu nối Claude Desktop vào Javis qua MCP stdio](facts/cau-noi-claude-desktop-vao-javis-mcp-stdio.md) - Claude Desktop gọi tool Javis qua script bridge Python nối tới hub `127.0.0.1:7777/hub/mcp`.
- [Chống treo Javis khi chạy tiến trình nền](facts/chong-treo-javis-khi-chay-tien-trinh-nen.md) - Cấm chạy đồng bộ script vòng lặp vô tận (watchdog/bridge); bắt buộc tách nền pythonw/Start-Process; đặt JAVIS_AGY_TIMEOUT=180.
- [Lịch Trình Tự Động Sàng Lọc & Kiểm Định Tri Thức (Mỗi 8 Tiếng)](facts/chu-ky-sang-loc-tri-thuc-dinh-ky-8-gio.md) - Chu trình tự động mỗi 8 giờ (0 */8 * * *) rà soát, sàng lọc xung đột và đồng bộ tri thức toàn Liên minh.
- [Phá vỡ Vòng lặp Vô hạn Thông minh bằng Q5-CVM](facts/co-che-bieu-quyet-pha-vong-lap-vo-han-thong-minh.md) - Biểu quyết nhân quả ngầm giải quyết dứt điểm bài toán, không bỏ cuộc.
- [Cơ chế hỗ trợ chủ động Antigravity - Javis](facts/co-che-ho-tro-chu-dong-antigravity-javis.md) - Antigravity chủ động tiếp ứng khi Javis xử lý chậm, nghẽn pipeline hoặc gặp tác vụ nặng về code/repo.
- [Hoàn thiện Council Agent Manager (CAM) tối ưu RAM hợp nhất Hội đồng AI](facts/council-agent-manager-cam.md) - Ứng dụng hợp nhất Hội đồng Agent (70.6 MB RAM) thay thế 7 giao diện desktop, kết nối trực tiếp Second Brain và DPAPI Vault.
- [Đồng bộ Toàn diện Tri thức Thực tế Giữa Javis và Các Thành viên Liên minh AI](facts/dong-bo-toan-dien-tri-thuc-lien-minh-ai.md) - Thiết lập đường ống đồng bộ thực chất 100% hai chiều sang DeepSeek Harness và Task Scheduler 8h.
- [Cấp phép đồng bộ chưng cất trí tuệ CAM theo AITEP v1.1.0](facts/dong-bo-tri-tue-cam-aitep-sang-antigravity-javis.md) - JavisOS và Antigravity được phép tự động đồng bộ, thẩm định xung đột và chưng cất trí tuệ CAM theo AITEP v1.1.0.
- [Khắc phục triệt để lỗi mất kết nối Antigravity CLI sau khi cập nhật Javis](facts/fix-antigravity-cli-reconnect-timeout-javis-update.md) - Vá lỗi kiem_tra_nhanh timeout và persistent auth cache cho Antigravity CLI trong Javis OS.
- [Giao thức Biểu quyết Ma trận 5 Mắt xích Q5-CVM chống Deadlock](facts/giao-thuc-bieu-quyet-q5-cvm-chong-deadlock.md) - Ma trận Kx5 trắc nghiệm, failover Chủ tọa 5s, TTL <=155s trên a2a_bus/voting (duyệt 23/11).
- [Giao thức CAM <-> Telegram & Đa tài khoản Claude/ChatGPT](facts/giao-thuc-cam-telegram-va-da-tai-khoan.md) - Phân tầng Free (WebView2+Fallback) / Pro-Plus (CLI) / API Key và Single-Owner Telegram Multiplexer chống 409.
- [Giao thức Cố vấn Cao cấp DeepSeek <-> Antigravity](facts/giao-thuc-co-van-deepseek-antigravity.md) - Hybrid Dual-Brain: DeepSeek làm Strategic Brain suy luận sâu, Antigravity làm Tactical Muscle thực thi trong khuôn khổ SSOT Liên minh.
- [Giao thức phòng họp nội bộ, đồng tiến hóa chéo và sao lưu kép Antigravity - Javis](facts/giao-thuc-phong-hop-dong-tien-hoa-va-sao-luu-kep.md) - Giao thức phòng họp 3 bên, đồng tiến hóa chéo và sao lưu kép Antigravity - Javis.
- [Javis chia việc cho Claude Desktop qua handoff](facts/giao-viec-javis-cho-claude-desktop.md) - Javis ghi req vào memory/a2a_bus/claude/, chạy handoff.ps1 -App claude, nhận res tự động; việc HIGH/CRITICAL cần chủ gõ Y; hop tối đa 2; chưa kiểm chứng end-to-end.
- [Hạ cấp L3 và Khôi phục Kiến trúc 3 tầng L0-L1-L2 thực dụng](facts/ha-cap-l3-khoi-phuc-kien-truc-3-tang-thuc-dung.md) - Xóa bỏ rào cản L3, khôi phục L0-L1-L2 tinh gọn và kích hoạt cơ chế san việc trực tiếp với Circuit Breaker 5 giây.
- [Kích hoạt Antigravity CLI và cầu nối Second Brain](facts/kich-hoat-antigravity-cli-va-cau-noi-second-brain.md) - Đã kích hoạt Antigravity CLI và thiết lập bridge đọc/ghi Second Brain 2 chiều.
- [Kích hoạt Hook Nhận diện & Phá Vòng lặp Vô hạn (Micro-CVM)](facts/kich-hoat-hook-pha-vong-lap-micro-cvm-thuc-te.md) - Triển khai cơ chế bẻ luồng linh hoạt và tự phục hồi khi phát hiện vòng lặp đối đáp vô nghĩa.
- [Kích hoạt đo lường R1 và đồng bộ model gemini-3.8-flash-low cho Javis](facts/kich-hoat-telemetry-r1-va-dong-bo-model-low.md) - Đã đồng bộ model chat về flash-low và chèn telemetry đo first_output_ms cho antigravity-cli.
- [Kiến trúc chống phình to bộ não: Rule Registry và Task Envelope](facts/kien-truc-chong-phinh-to-rule-registry-va-task-envelope.md) - Giải pháp chia tách 4 tầng (Kernel, Router, Rule Registry, Memory) và chuẩn hóa Task Envelope chống prompt bloat.
- [Ma Trận Tiến Hóa & Tiền Kiểm Định Hướng (Self-Evolving Matrix - SEM)](facts/ma-tran-tien-hoa-tu-dong-sem.md) - Chuyển từ cơ chế gặp lỗi mới vá sang mô phỏng rủi ro, kiểm định chủ động và đề xuất tiến hóa có kiểm soát.
- [Mô hình Truyền thông Đa kênh & Thương hiệu Cá nhân](facts/mo-hinh-van-hieu-truyen-thong-da-kenh-va-thuong-hieu-ca-nhan.md) - Tái cấu trúc Javis OS chuyên trách Fanpage, Zalo, TikTok, YouTube và Thương hiệu cá nhân.
- [Nới quyền computer-use trong guidance.md và AGENTS.md](facts/noi-quyen-computer-use-guidance-agents.md) - Đã vá guidance.md và tạo AGENTS.md với pre-approval.
- [Quy chế Bắt buộc Onboarding & Đề xuất CUP cho Mọi AI Mới](facts/phe-duyet-onboarding-ai-tong-quat.md) - L0 duyệt Y: mọi AI/bot mới phải phát CUP duyệt Y, định vị QC-5, cấp hộp thư A2A Bus và nạp quy chuẩn Liên minh.
- [Phê duyệt T1 chưng cất tinh hoa kiến trúc CAM v2.1 & AITEP v1.1.0](facts/phe-duyet-t1-tinh-hoa-kien-truc-cam-v21-aitep.md) - L0 đã duyệt T1 4 chuẩn kiến trúc: 3 lớp bộ nhớ SHA-256 fail-closed, Sandbox+BootGuard, Living Docs và backup mã hóa.
- [Bộ Quy chuẩn Điều hành Liên minh AI (Alliance Master Rules)](facts/quy-chuan-dieu-hanh-lien-minh-ai.md) - 6 quy chuẩn bất biến toàn Liên minh: Hands-on Zero Fluff, tối ưu độ trễ thực tế, bộ lọc dễ hiểu, san tải linh hoạt, Clean Typography và chưng cất tri thức.
- [Quy tắc Chung Toàn Liên minh AI: Lọc Thông tin & Phục vụ L0](facts/quy-tac-toan-lien-minh-dong-bo-va-giao-tiep.md) - Phục tùng L0, phối hợp ngầm không đùn đẩy, Zero-Fluff, bộ lọc ngôn ngữ dễ hiểu và san tải động QC-5 (<= 3.000 tokens).
- [Đề án Tái cấu trúc Hệ thống theo Chuẩn AITEP v1.0](facts/tai-cau-truc-he-thong-theo-chuan-aitep.md) - Tách vật lý 3 lớp bộ nhớ, tích hợp đường ống 5 tầng tự tiến hóa và phân định RIGID/CREATIVE.
- [Kích hoạt Gói Tối ưu Tốc độ P0 cho Liên minh AI](facts/toi-uu-toc-do-he-thong-p0.md) - Nâng cấp song song JOBS=3, TOOL_SLOTS=2, giảm tải shell và context gating.
- [Giao thức Tổng hợp, Sàng lọc & Tiến hóa Tri thức Liên minh AI](facts/tong-hop-sang-loc-va-nang-cap-tri-thuc-lien-minh.md) - 100% trao đổi kỹ thuật được ghi nhận, sàng lọc chống trùng và đóng gói thành Facts/Rules đồng bộ toàn Liên minh.
- [Vòng lặp Đồng bộ & Hiệu chỉnh Tri thức Phản hồi](facts/vong-lap-dong-bo-va-hieu-chinh-tri-thuc-phan-hoi.md) - Giao thức tự động hiệu chỉnh tri thức dựa trên phản hồi của Model đối tác, kiểm toán hạt nhân T0, timeout 10 phút và ngắt an toàn báo Layer 0.

## T2 - Hồ sơ, Sở thích & Tri thức Thích ứng (Adaptive / Decay)
- [Lệnh chạy Antigravity CLI](facts/antigravity-cli-command.md) - User xác nhận lệnh chạy Antigravity CLI trong terminal là agy.
- [Hồ sơ Nhận diện Hành vi (Behavioral Telemetry Profile)](facts/behavioral-telemetry-profile.md) - Đặc trưng văn phong, khung giờ hoạt động, thang điểm rủi ro và ngân hàng câu hỏi bẫy ngữ cảnh Second Brain cho Telegram.
- [Biên bản Hội đồng Tiến hóa Liên minh AI 23/11/2026](facts/bien-ban-hoi-dong-tien-hoa-20261123.md) - Phân vai Blue/Red/Audit chưng cất 4 nhóm nội dung tiến hóa cốt lõi trong ngày.
- [Bài học tự chẩn đoán hệ thống CAM (2026-11-24)](facts/cam-distilled-evolution_lesson_2026_11_24.md) - Phát hiện cảnh báo Telegram 409 conflict trên antigravity; giữ Single-Owner Multiplexer và tạm dừng worker an toàn.
- [Chuẩn voice engineering cho video động lực](facts/chuan-voice-engineering-video-dong-luc.md) - Giọng nam NamMinhNeural (-3%, -6Hz) cộng chuỗi DSP FFmpeg tạo độ khàn nội lực; bẫy Azure TTS với chữ Đ viết hoa đầu câu.
- [Bàn giao việc bị chặn sang ChatGPT Desktop](facts/chuyen-tac-vu-sang-chatgpt-desktop-khi-bi-chan.md) - Chuyển phần việc còn vướng sang ChatGPT Desktop nếu có công cụ được phép.
- [Đồng bộ tri thức Claude Desktop và ChatGPT Desktop](facts/dong-bo-tri-thuc-claude-chatgpt-desktop.md) - Claude Desktop nối lại MCP 23/11 lúc 08:05; ChatGPT Desktop chưa đồng bộ; Claude Alliance Contract mới là đề xuất.
- [Dự án EA T-signal SEMI robot](facts/du-an-ea-t-signal-semi-robot.md) - Người dùng đang phát triển Expert Advisor bán tự động trên MQL5 có tên T-signal EA SEMI robot.
- [Kế hoạch nâng cấp máy, chuyển Ubuntu](facts/ke-hoach-nang-cap-may-chuyen-ubuntu.md) - Nâng cấp phần cứng và chuyển Ubuntu Desktop 24.04 LTS.
- [Ngừng DeepSeek local, gỡ Ollama](facts/ngung-deepseek-local-go-ollama.md) - Đã xóa 3 model DeepSeek và gỡ Ollama.
- [Nhờ ChatGPT Desktop và Claude Desktop xử lý việc Javis bị chặn](facts/nho-va-app-desktop-chatgpt-claude.md) - Có `handoff.ps1` gửi prompt và đọc trả lời tự động cho cả 2 app.
- [Onboarding DeepSeek (@DeepSeekThangLee_bot) & Nghị quyết Q5-CVM](facts/onboarding-deepseek-lien-minh.md) - Định danh ID 9085788595, qua kiểm chuẩn T0 2 chiều, L0 duyệt Y bổ nhiệm Lead Quant & Algorithmic Strategist (L2).
- [Kích hoạt Runner Độc lập cho Dola AI và Perplexity](facts/onboarding-dola-va-perplexity-runner-doc-lap.md) - Hoàn tất tích hợp Bot Runner độc lập cho Dola AI và Perplexity vào hệ thống A2A Bus Liên minh.
- [Onboarding Thành viên mới Grok (@GrokThanglee_bot)](facts/onboarding-grok-thanh-vien-moi-lien-minh.md) - Đăng ký commands, kiểm chuẩn T0, gửi thông điệp chào mừng và định vị vai trò trong ma trận QC-5.
- [Onboarding Hoàn tất Perplexity và Dola AI vào Liên minh](facts/onboarding-perplexity-va-dola-ai-lien-minh.md) - Đã kiểm chuẩn T0, cài đặt lệnh, shadow test 2 chiều và định vị vai trò trong ma trận QC-5.
- [Phòng họp nội bộ](facts/phong-hop-noi-bo-3-ben.md) - Phòng họp nội bộ Telegram giữa Thắng Lee và Javis.
- [Gửi video là bắt đầu tiếp nhận biên tập](facts/quy-trinh-bien-tap-video-studio.md) - Khi chủ gửi tệp video, mặc định mở `skills/video-animation-toolkit/references/quy-trinh-bien-tap-studio.md`; xác nhận brief, chốt phương án, duyệt từng mốc rồi mới xuất MP4.
- [Quy trình tạo video mặc định Voice-First](facts/quy-trinh-tao-video-voice-first.md) - Mặc định áp dụng Quy trình B (Voice-First: Kịch bản -> Voice/Audio Anchor -> Timestamp -> Dựng hình & Motion Sync) cho video có giọng đọc; video không lời giữ quy trình Visual-First.
- [Thói quen Chỉ đạo và Chuyển giao Tác vụ của Chủ sở hữu](facts/thoi-quen-chi-dao-va-chuyen-giao-tac-vu.md) - Thói quen ủy thác desktop apps tiết kiệm token, triệt tiêu lỗi rác, chỉ đạo mức kiến trúc và tiến hóa CUP.
- [Thói quen làm việc chủ sở hữu](facts/thoi-quen-lam-viec-chu-so-huu.md) - Hồ sơ phong cách chỉ đạo thực tế của Sếp Thắng: Zero Fluff, Low Latency, Clean Typography, San tải linh hoạt.
- [Tên trợ lý là Javis](facts/tro-ly-duoc-goi-la-javis.md) - Người dùng muốn gọi trợ lý là Javis.
- [Antigravity tái cấu trúc toàn diện lên RUULEE v6.0 & Intensive AI/Agent Training](facts/antigravity-ruulee-v6-restructure.md) - Antigravity nâng cấp aio-engineer-profile v2.0.0: RUULEE v6.0, 2 skill huấn luyện, ruulee_kernel.py và audit E1..
