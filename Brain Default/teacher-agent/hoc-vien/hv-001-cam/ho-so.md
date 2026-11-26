# Hồ sơ học viên — hv-001-cam (HỌC VIÊN THÍ ĐIỂM)

- **Hệ:** CAM — hệ đa model phục vụ L0 · **Chủ hệ:** L0 (anh Thang)
- **Cấp:** AgentOS (điều phối) + Agent (Antigravity, Sonnet vòng lặp) + AI (5 model) + SubAgent (thợ TaskPacket)
- **Adapter:** `adapters/claude.md`, `adapters/deepseek.md`, `adapters/antigravity.md` (THIẾT KẾ), `adapters/javis.md` (ĐÃ THẤY MCP)
- **Người chấm:** thành viên Claude → Codex/Grok; DeepSeek → Codex/Grok; Antigravity (Google) → Codex/DeepSeek. Xem `khung/hoi-dong-cham.md`.
- **Luật học viên:** `luat-hoc-vien.md` · **Mâu thuẫn với sàn chung:** chưa thấy (luật CAM chặt hơn sàn)
- **Vai mong muốn:** đội đa model tự vận hành, định tuyến đúng ô, chi phí thấp, điểm chạm L0 ít
- **Dữ liệu tối đa:** S2 với Claude, S1 với DeepSeek hosted
- **Bậc tự chủ:** A4 · **Trạng thái:** CAM OS đang CỨU HỘ THẬT (từ 26/11): càng sửa càng hỏng, lỗi kết nối thường xuyên, agent thiếu quyền. **Doctor Agent** (dự án 'Claude - Doctor Agent') đang làm R1. HLV: duyệt phác đồ, chấm kết quả, không sửa code. H1 cấp AgentOS hoãn tới khi Doctor xong R6; H1 cấp AI của từng model chạy song song (không phụ thuộc CAM OS).
- **Bệnh án:** do Doctor giữ; HLV lưu bản chép/duyệt trong `benh-an/`.
- **Thành phần:** `thanh-vien.jsonl` (8 thành viên, điểm null)
