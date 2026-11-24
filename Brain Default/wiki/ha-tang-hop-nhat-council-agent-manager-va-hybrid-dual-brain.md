---
type: wiki
status: active
tags: [wiki, lien-minh-ai, cam, deepseek, antigravity, hybrid-dual-brain, kien-truc]
created: 2026-11-24
updated: 2026-11-24
source: [[facts/council-agent-manager-cam]], [[facts/giao-thuc-cam-telegram-va-da-tai-khoan]], [[facts/cam-test-truc-tiep-len-telegram-api-chong-khoa-botfather]], [[facts/giao-thuc-co-van-deepseek-antigravity]]
---

# Hạ tầng Hợp nhất Council Agent Manager (CAM) & Giao thức Hybrid Dual-Brain

## 1. Bối cảnh và Động lực Tinh gọn
Trước ngày 24/11/2026, Liên minh AI duy trì 7 ứng dụng desktop độc lập (Claude Desktop, ChatGPT Desktop, Codex, Grok, DeepSeek, Antigravity, Javis) gây tiêu tốn từ 6.9 đến 8.0 GB RAM và xung đột chiếm dụng tài nguyên hệ thống.
Nhằm tối ưu hóa triệt để theo chỉ đạo thực dụng của Tổng chỉ huy Layer 0 (Lương Thế Thắng), toàn bộ hạ tầng đã được tái cấu trúc thành giải pháp hợp nhất [[Council Agent Manager (CAM)]] và mô hình tác chiến hai nhịp [[Hybrid Dual-Brain]].

## 2. Kiến trúc Council Agent Manager (CAM)
- **Tiêu thụ tài nguyên tối thiểu:** 1 tiến trình lõi Python async + Native WebView2 tiêu thụ ~70.6 MB RAM nền (giảm tải hơn 98% RAM so với mở đồng thời 7 app desktop).
- **Mã hóa an toàn DPAPI Vault:** 100% token/API key được mã hóa theo Windows DPAPI trong `vault/secrets.vault.json`, triệt tiêu hoàn toàn nguy cơ rò rỉ plaintext secret.
- **Single-Owner Telegram Multiplexer:** Toàn bộ bot thành viên L2 (`@Claude`, `@Grok`, `@Perplexity`, `@Dola`, `@DeepSeek`) chạy chung 1 vòng lặp `asyncio` và 1 `httpx.AsyncClient` pool trong CAM (`cam_core/telegram_mux.py`), phòng chống triệt để lỗi HTTP 409 Conflict.
- **Phản hồi tức thì Zero-LLM (< 0.5s):** Các lệnh điều phối vi mô (`/status`, `/brain`, `/tojavis`, `/help`) được xử lý trực tiếp không qua gọi model, tiết kiệm token tối đa.

## 3. Chốt chặn Bất biến T0 về Kiểm thử Telegram API
Từ sự cố rate-limit thực tế ngày 24/11/2026 với `@BotFather`, Liên minh ban hành 4 quy tắc kỹ thuật cứng:
1. **Cấm test app bằng Telegram API thật:** 100% kiểm thử (`pytest`, Shadow Test, dry-run) bắt buộc dùng Mock/Fake HTTP cục bộ; tuyệt đối không gửi `sendMessage` hoặc `setMyCommands` thật để debug.
2. **Không gọi lặp `setMyCommands`:** Chỉ đăng ký danh sách lệnh 1 lần duy nhất sau khi tạo bot và lưu cờ cache trên đĩa.
3. **Dãn cách khởi động đa bot:** Khởi động tuần tự dãn cách `>= 3s/bot`, bảo đảm duy nhất 1 poller giữ token.
4. **Pre-Flight Anti-Ban Gate:** Luôn đối soát giới hạn tần suất của bên thứ ba trước mọi hành động tự động hóa.

## 4. Mô hình Tác chiến Hybrid Dual-Brain (DeepSeek <-> Antigravity)
Phân định ranh giới rõ ràng giữa Năng lực Suy luận Sâu và Năng lực Thực thi Cơ bắp:
- **DeepSeek (`@DeepSeekThangLee_bot` - Strategic Brain):** Đóng vai trò Cố vấn Cao cấp, chịu trách nhiệm thiết kế kiến trúc, giải thuật định lượng MQL5, phân tích phản biện và thẩm định nghiệm thu.
- **Antigravity (`@AntiGravityThanglee_bot` - Tactical Muscle):** Chịu trách nhiệm quét codebase, viết code, chạy terminal, thao tác tệp và kiểm thử thực tế E1.
- **Quy trình 3 nhịp Task Contract (Gating <= 3.000 tokens):**
  1. *Nhịp 1 (Strategic Blueprint):* Antigravity tóm tắt bài toán gọn gửi Cố vấn DeepSeek nhận phương án và tiêu chí nghiệm thu.
  2. *Nhịp 2 (Tactical Execution):* Antigravity trực tiếp code và kiểm thử trong sandbox.
  3. *Nhịp 3 (Verification Audit):* Gửi tóm tắt diff và bằng chứng test E1 để DeepSeek thẩm duyệt trước khi báo cáo Layer 0.

## 5. Đề xuất Nâng cấp Hệ thống (CUP Pipeline)
Đúc kết từ đánh giá tác chiến của Dola AI (COO):
- **Atomic Task Contract:** Bổ sung Checksum và danh sách Invariants vào payload A2A Bus để chống chạy ngầm sinh lỗi.
- **Heartbeat Worker Health Check (15s):** Tự động phát hiện crash/restart và khôi phục từ checkpoint gần nhất.
- **Fast Path:** Tự động thực thi ngay các tác vụ LOW/MEDIUM (chỉ đọc hoặc tạo tệp tạm) để giảm độ trễ và tối ưu năng lực Hội đồng.
