# Kiến trúc 3 Tầng Bộ nhớ (AITEP v1.1.0 / RUULEE v6.0)

Cấu trúc phân tầng vật lý bảo đảm tương thích ngược 100% với `memory/facts/*.md` và `memory/MEMORY.md` của Javis OS:

- **`T0_immutable/`**: Chứa `core_charter_t0.md`, bản niêm phong `sealed/*.md` của các fact hạt nhân T0 và `manifest.sha256.json` (kiểm toán SHA-256 fail-closed). Chỉ Layer 0 được sửa.
- **`T1_governed/`**: Chứa `registry.json` quản trị các quy chế, kiến trúc và giao thức đã được Layer 0 phê duyệt; mọi thay đổi phải qua Impact Preview + CUP + Rollback.
- **`T2_adaptive/`**: Chứa `registry.json` theo dõi tri thức thích ứng (hồ sơ, sở thích, dự án, bài học vận hành) kèm trường `provenance`, `decay_days`, `half_life_days`, `review_after` và `confidence`.
- **`tier_manifest.json`**: Chỉ mục tổng hợp 100% tệp trong `memory/facts/` (bao gồm cả danh sách `superseded_facts` đã hợp nhất theo MDACPT mà không xóa lịch sử).
