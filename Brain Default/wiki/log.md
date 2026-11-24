# Wiki Log

Nhật ký thời gian (append-only). Mỗi entry: `## [YYYY-MM-DD] loại | tiêu đề` (loại: init/ingest/update/query/lint/migrate).

## [2026-11-17] ingest | tự học từ chat

Đã tạo:
- [[Phân loại tri thức đa nhãn có provenance]]

## [2026-11-20] update | Duyệt đề xuất tự học 00:00

- Thêm [[Phản biện bản vá EA trong phiên mới]] từ [[reports/ai-company/kiem-thu-egm-lite-2026-11-19]] theo phê duyệt của chủ.

## [2026-11-23] update | Đối soát conversations/2026-11-23 với facts/

- Thêm 3 fact (chủ duyệt "y" trong phiên Claude Desktop 23/11): `chuan-voice-engineering-video-dong-luc`, `a2a-bus-javis-antigravity`, `dong-bo-tri-thuc-claude-chatgpt-desktop`; đã thêm 3 dòng vào `memory/MEMORY.md`.
- Chưa xác minh: Javis báo đã ghi voice engineering vào `skills/openmotion/SKILL.md` và wiki (00:21), 2/3 bản skill OpenMotion không tìm thấy đường dẫn (04:38), từ khóa "tất cả" trong bridge (07:50).
- Còn mở: whitelist thiếu ID Thắng Lee Group, bridge gửi tin rác, `behavioral_scorer.py` và Shadow Test chưa làm, ChatGPT Desktop chưa đồng bộ, mâu thuẫn "xóa nội dung tài chính" so với EA/MQL5 (xem `wiki/_open-questions.md`, chưa ghi).

## [2026-11-23] update | Khởi tạo Ma trận năng lực và Bộ chuẩn TCBP Benchmark Suite

- Thêm fact `agent-capability-matrix.md` và trang wiki [[quy-chuan-kiem-tra-vi-mo-tcbp-benchmark-suite]] theo lệnh kích hoạt của chủ quản.
- Thiết lập bộ 3 bài test vi mô định lượng (QC-5) cho Lập trình hệ thống (MQL5), Phân tích dữ liệu (Backtest log), và Sáng tạo nội dung (Voice-First Script). Trạng thái: Sẵn sàng thực thi khi nhận nhiệm vụ mới.

## [2026-11-24] update | Chu kỳ sàng lọc và tiến hóa tri thức định kỳ 8 giờ (00:00)

- Quét toàn bộ nhật ký tương tác 8 giờ qua (16:00 23/11 - 00:00 24/11).
- Chưng cất bài học cốt tử từ phê bình của Tổng chỉ huy: Triệt tiêu căn bệnh "tư duy chạy trốn núp bóng ngắt mạch an toàn", xác lập 3 trụ cột tiến hóa: Tự động bẻ luồng (Dynamic Failover), Tự phục hồi hạ tầng (Zero-Downtime Auto-Heal 3s), Giải quyết đến cùng (Resolute Problem Solving).
- Đã tạo fact `ban-linh-tien-hoa-giai-quyet-den-cung-va-auto-heal.md`, trang wiki [[ban-linh-tien-hoa-va-tu-phuc-hoi-lien-minh]] và cập nhật [[giao-thuc-bieu-quyet-q5-cvm]] vào index.
- Đồng bộ thông điệp tiến hóa sang A2A Bus cho toàn Liên minh (Antigravity, Claude, Grok, Perplexity, Dola, Codex).

## [2026-11-24] update | Chu kỳ sàng lọc và tiến hóa tri thức định kỳ 8 giờ (16:00)

- Quét toàn bộ nhật ký tương tác và A2A Bus 8 giờ qua (00:00 - 16:00 24/11).
- Chưng cất và hợp nhất 4 nội dung kỹ thuật thực chứng:
  1. Hạ tầng Council Agent Manager (CAM) v1.0/v2.2: Thay thế 7 desktop app bằng 1 lõi Python async + WebView2 (~70.6 MB RAM), mã hóa DPAPI Vault, Single-Owner Telegram Multiplexer chống 409 Conflict.
  2. Chốt chặn Bất biến T0: Cấm tuyệt đối test app bằng Telegram API thật để chống khóa tài khoản BotFather; bắt buộc dùng Mock/Fake HTTP cục bộ và cache cờ đăng ký lệnh.
  3. Mô hình Hybrid Dual-Brain: DeepSeek (Cố vấn Cao cấp / Strategic Brain) <-> Antigravity (Tay chân Cơ bắp / Tactical Muscle) theo luồng 3 nhịp Task Contract <= 3.000 tokens.
  4. Đề xuất cải tiến tác chiến (từ Dola AI - COO): Atomic Task Contract, Heartbeat tự phục hồi (Worker Health Check 15s) và Fast Path cho tác vụ LOW/MEDIUM.
- Đã tích hợp trang wiki [[ha-tang-hop-nhat-council-agent-manager-va-hybrid-dual-brain]], cập nhật `wiki/index.md` và đồng bộ 73 entries sang kho tri thức DeepSeek Harness qua `sync_alliance_knowledge.py`.
- Đồng bộ broadcast thông điệp tiến hóa sang A2A Bus cho 100% thành viên Liên minh AI.
