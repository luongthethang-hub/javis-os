---
type: technical
provenance: agent
origin: antigravity-bridge
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23 (9bb9fbc4)
---
Khi bất kỳ bot nào trong Liên minh AI (Javis, Antigravity, Claude, ChatGPT/Codex) xử lý tác vụ chậm, nghẽn pipeline hoặc quá tải:
- **Cơ chế san tải động theo ma trận:** Kích hoạt san tải chéo dựa trên Ma trận năng lực thực chứng (QC-5), chuyển phần việc bị nghẽn sang bot có thế mạnh phù hợp nhất thay vì cố định một chiều.
- **Tiết kiệm token & Context Gating:** Áp dụng strict context gating (tối đa <= 3.000 tokens/lượt chuyển giao), chỉ gửi abstract, contract và diff tóm tắt qua A2A Bus / handoff; cấm nạp context thô gây lãng phí tài nguyên.
- **Tương trợ thông minh không dẫm chân:** Bot nhận san tải xử lý độc lập phần việc được giao, đẩy kết quả về đĩa/Second Brain để bot chủ trì tổng hợp phản hồi liền mạch cho người dùng.
