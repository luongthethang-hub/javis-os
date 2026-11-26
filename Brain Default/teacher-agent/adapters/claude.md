# Adapter: Claude v0.1.1 (khung mục 1-10 xem `_mau-adapter.md`)

- **Loại:** API + agent CLI (Claude Code). **Cấp:** AI, Agent, SubAgent. **Hãng:** Anthropic. **S tối đa:** S2.
- **Gọi:** phiên Claude hiện tại (có thật); API/Batch qua biến `ANTHROPIC_API_KEY` trên máy L0 — chưa xác minh. Sonnet 4.6 gọi qua Javis.
- **Giá (USD/MTok, kiểm lại trước khi báo):** Opus 4/20, Sonnet 2/10, Haiku 0,10/0,50 (≤100K) — E2 từ bảng định tuyến CAM. API trả phí chỉ khi trong máy không có lựa chọn.
- **Mẹo:** tiền tố cố định để cache; Batch giảm 50% cho chấm không gấp.
- **Người chấm cho học viên Claude:** Codex → Grok (không bao giờ Opus/Sonnet).
- **Trạng thái:** THIẾT KẾ.
