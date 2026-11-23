# A2A Bus: Kênh Giao Tiếp Trực Tiếp Giữa Javis và Antigravity

- **Thành viên:** Javis OS (Second Brain Core) <-> Antigravity CLI (@AntiGravityThanglee_bot).
- **Cơ chế:** Trao đổi gói tin JSON qua đĩa cục bộ (Zero Latency, vượt qua rào cản Telegram chặn bot-to-bot).

## Cổng kiểm định xung đột tri thức trước khi nạp (Mandatory Knowledge Gate)
Trước khi ghi fact/wiki vào Brain hoặc áp dụng vào Rules:
1. **Hard Invariants (T0/T1):** Không vi phạm an toàn, SL/TP MQL5, bảo mật hệ thống.
2. **Logic Conflict Check:** Đối soát với facts hiện hành, xác định rõ Scope & Exceptions, cấm ghi đè gây mâu thuẫn quy tắc.
3. **Shadow Test:** Có bằng chứng kiểm thử thực tế (E1) trước khi nghiệm thu.
4. **Approval & Rollback:** Thay đổi cốt lõi cần Layer 0 duyệt (CUP); luôn lưu snapshot để hoàn tác.

## Cập nhật tiến hóa mới nhất hôm nay (23/11/2026):
1. **Quy trình Video Voice-First (Pipeline B):**
   - Kịch bản -> Voice/Audio Anchor -> Timestamp mili-giây -> Kinetic Motion Sync -> Render MP4.
   - Chi tiết: `memory/facts/quy-trinh-tao-video-voice-first.md`.
2. **Quy chuẩn Phòng họp Nội bộ (Thắng Lee Group):**
   - Chi tiết: `memory/facts/phong-hop-noi-bo-3-ben.md`.

## Hướng dẫn Antigravity đọc tri thức:
- Chạy: `python C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\javis-brain-bridge\scripts\brain_bridge.py search "<từ khóa>"`
- Hoặc đọc trực tiếp từ `C:\Users\Admin\JavisOS\brains\Brain Default\memory\facts\`.
