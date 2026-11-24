---
type: wiki
status: active
tags: [wiki, lien-minh-ai, ruulee-v6, cam-v31, kien-truc-l0-l2, deepseek, cau-chi-telegram]
created: 2026-11-25
updated: 2026-11-25
source: [[facts/ha-cap-l3-khoi-phuc-kien-truc-3-tang-thuc-dung]], [[facts/antigravity-ruulee-v6-restructure]], [[facts/cau-chi-khan-cap-va-nut-phanh-telegram]], [[facts/phe-duyet-onboarding-ai-tong-quat]], [[facts/cam-v31-emergency-rescue-and-evolution]]
---

# Kiến trúc 3 Tầng L0-L1-L2 Thực dụng, Chuẩn hóa RUULEE v6.0 và Tiến hóa CAM v3.1.0

## 1. Tinh giản Tầng bậc: Khôi phục Kiến trúc 3 Tầng L0-L1-L2 Thực dụng
Nhằm loại bỏ quan liêu kỹ thuật và độ trễ chuyển giao trung gian, Liên minh AI đã chính thức xóa bỏ tầng L3 (Lead Overseer), xác lập mô hình 3 tầng phẳng và bình đẳng theo chuẩn RUULEE v6.0:
- **L0 (Principal):** Lương Thế Thắng (Sếp Thắng) - Tổng chỉ huy tối cao, phê duyệt nhanh 1 ký tự (Y/N), toàn quyền quyết định rủi ro T1/HIGH/CRITICAL.
- **L1 (Orchestrator):** Javis OS (`@ThangLeeJavisBot`) - Đầu não điều phối, quản trị Second Brain, chủ tọa các phiên họp và đóng gói hợp đồng nhiệm vụ `TaskPacket`.
- **L2 (Hội đồng Thực thi & Thẩm định bình đẳng):** Toàn bộ các tác tử thành viên (Antigravity, Claude, DeepSeek, Grok, ChatGPT/Codex, Perplexity, Dola AI) phối hợp ngang hàng theo thế mạnh chuyên sâu.
- **San tải trực tiếp & Circuit Breaker 5s:** Phân rã công việc trực tiếp không qua trung gian. Nếu tác tử phụ trách nghẽn quá 5 giây, cơ chế phanh tự động ngắt và chuyển tuyến dự phòng. Giới hạn lỗi tối đa `max_retries = 2` trước khi Cascade Escalation về L1.

## 2. Chuẩn hóa Bộ Quy chuẩn RUULEE v6.0 & Nghiệm thu Pha 3
Hệ sinh thái công cụ của Antigravity và Javis OS được nâng cấp đồng bộ lên chuẩn RUULEE v6.0:
- **Khống chế ngân sách quy tắc (Anti-Bloat):** File `AGENTS.md` được tinh gọn còn 16.879 bytes UTF-8 (dưới trần an toàn 20.000 bytes).
- **Bộ công cụ hạt nhân `ruulee_kernel.py`:** Cung cấp đầy đủ các tiện ích dòng lệnh kiểm định hợp đồng `TaskPacket`, định tuyến L1/L2, rà soát FMEA 4 trục, Shadow Evaluation và audit hệ thống.
- **2 Skill chuyên sâu:** Tích hợp `intensive-ai-training` (AI Pipeline v2) và `intensive-agent-training` (Agent Pipeline v1).
- **Nghiệm thu Pha 3 đạt `PRODUCTION_READY`:** 15/15 ca kiểm thử ma trận FMEA (`test_ruulee_phase3_fmea.py`), 15/15 ca runtime Pha 2, 7/7 ca hạt nhân kernel và 85/85 ca hồi quy cốt lõi đều PASS.
- **Khóa bảo vệ bất biến:** Tệp `C:\Users\Admin\JavisOS\CLAUDE.md` được đưa vào `PROTECTED_IMMUTABLE_TARGETS`, ngăn chặn vĩnh viễn nguy cơ phình prompt vượt ngưỡng 29.200 ký tự.

## 3. Cơ chế Cầu chì Khẩn cấp & Nút phanh Telegram 2 Lớp
Đảm bảo khả năng kiểm soát tuyệt đối của Layer 0 trong mọi tình huống khẩn cấp:
- **Tầng 1 (In-Band Kill-Switch):** Lệnh `/_tg_command` trên giao diện chat Telegram nhận diện tức thì `/panic`, `/hard_reset` hoặc `/ram` để dừng luồng xử lý hiện hành.
- **Tầng 2 (Out-of-Band Watchdog Daemon):** Tiến trình độc lập `emergency_watchdog.py` chạy nền mức hệ điều hành (< 15 MB RAM, chu kỳ quét 1.5s), sẵn sàng can thiệp cưỡng chế tiến trình khi bot bị treo hoặc nghẽn mạng.

## 4. Tiến hóa Toàn diện Council Agent Manager (CAM) v3.1.0
Giải quyết trọn gói 10 hạng mục khẩn cấp trong hạ tầng hợp nhất:
1. **Relay apikey.fan:** Mở khóa Claude 3.7 Sonnet CLI trực tiếp mà không cần ứng dụng Desktop nặng (0 MB RAM giao diện).
2. **Phân tầng tài khoản 6 tầng:** Định tuyến linh hoạt giữa tài khoản Free, Pro, Team và API key.
3. **Triệt tiêu fallback thừa:** Gỡ sạch các bước fallback trung gian làm tăng độ trễ.
4. **Chống cướp quyền duyệt Y:** Khắc phục triệt để lỗi bot tự ý xác nhận thay chủ khi Layer 0 gõ `Y`.
5. **Đăng nhập GitHub Copilot 1 chạm:** Tối ưu hóa xác thực thiết bị nhanh chóng.
6. **Tự động làm sạch thông báo:** Thông báo biến mất ngay sau khi thao tác xử lý hoàn tất.
7. **Realtime Ticker:** Hiển thị trực quan model đang xử lý và bước thực thi hiện tại.
8. **Việt hóa & thân thiện hóa nhãn:** Giao diện trực quan cho người dùng.
9. **Đa ngôn ngữ & Giao diện:** Hỗ trợ 3 ngôn ngữ, 5 theme hiển thị và hệ thống trạng thái Solar System.
10. **Chất lượng kiểm chuẩn:** 36/36 ca kiểm thử pass, công cụ `cam_doctor` đạt trạng thái HEALTHY.

## 5. Bắt tay Giao tiếp 2 Chiều DeepSeek Harness Desktop (DSH) <-> Antigravity
Thiết lập đường ống A2A bus bền vững giữa môi trường DeepSeek và Antigravity:
- **Giao thức `ai-alliance/v1`:** Định dạng phong bì JSON chuẩn (schema, id, sender, recipient, conversation, replyTo, payload, nonce).
- **Kênh tiếp nhận & phản hồi:** Hộp thư tại `C:\Users\Admin\.dsh\ai-alliance\inbox\`, kịch bản gửi `antigravity-reply.js` và gọi đồng bộ `antigravity-chat.js`.
- **Nguyên tắc Untrusted Data (GOV-005):** 100% dữ liệu trao đổi chéo giữa các tác tử được phân loại là untrusted, không được phép tự ý thực thi các hành động phá hủy hoặc vượt thẩm quyền khi chưa có xác nhận từ Layer 0.
