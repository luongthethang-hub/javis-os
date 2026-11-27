---
name: meta-cognition-channel-ops
description: "Quy trình Siêu nhận thức (Meta-Cognition) điều phối và nghiên cứu toàn bộ hệ sinh thái kênh của chủ sở hữu: Fanpage (owner_page), Trang cá nhân…"
---

# Meta-Cognition Channel Operations (4 Loại Kênh & 4 Pha Tự Nhận Thức)

Mọi tương tác trên Facebook phải phân tách rõ **4 loại kênh** trong Sổ Danh Bạ (`fb_ext_channel_registry`):
- `owner_page` (Fanpage chủ quản lý): Đọc bài/inbox + điền nháp bài/bình luận/trả lời khách (nhớ kiểm tra tư cách Trang).
- `owner_profile` (Trang cá nhân chế độ Chuyên nghiệp của chủ): Đọc bài + điền nháp bài/bình luận dưới tư cách Cá nhân.
- `group` (Nhóm Facebook — chủ làm Admin/Mod hoặc nhóm cộng đồng mục tiêu): Quét qua `fb_ext_discover_groups()`, đọc bài & câu hỏi nóng của khách, điền nháp chia sẻ giá trị (không spam link).
- `trending_source` (Tài khoản cá nhân / Creator / Trang đang lên xu hướng): **CHỈ ĐỌC & NGHIÊN CỨU (`monitor_only`)** qua `fb_ext_scan_trending(query=..., url=...)` — trích tác giả, link tài khoản, chỉ số tương tác và công thức hook để học & sản xuất nội dung cho kênh của chủ; **cấm cứng đăng bài lên tường người khác**.

## Pha 1 — Xác định Đúng Kênh & Mục tiêu
1. Gọi `fb_ext_channel_registry(op="list")` và `fb_ext_status()`.
2. Nếu chưa đủ danh sách kênh: gọi `fb_ext_discover_pages()` (Fanpage) và `fb_ext_discover_groups()` (Nhóm quản lý & tham gia).
3. Nếu mục tiêu là săn xu hướng/tài khoản đang lên: gọi `fb_ext_scan_trending(query=...)` hoặc truyền URL hồ sơ/nhóm/Reels cần soi, sau đó đề xuất lưu những tài khoản chất lượng vào sổ dưới loại `trending_source`.
4. Có `>= 2` kênh phù hợp mà yêu cầu chưa nêu rõ kênh đích -> dừng hỏi đúng 1 câu để chọn, không đoán bừa.

## Pha 2 — Tự tìm kiếm Nguồn lực (Resource Discovery)
1. **Second Brain (`memory/facts`, `wiki/`, `reports/`):** Quy tắc thương hiệu, giọng điệu, chiến dịch cũ.
2. **Thư mục cục bộ (`resource_paths` của kênh):** Đọc tài liệu hướng dẫn, biểu phí, quy định, danh sách ảnh/video thật (vd `D:\Cty NAM TAM ĐIỆP`).
3. **Dữ liệu sống từ Kênh & Xu hướng:** Kết hợp `fb_ext_read_page` / `fb_ext_read_inbox` trên kênh của chủ với `fb_ext_scan_trending` từ các tài khoản cá nhân/nhóm đang lên xu hướng để tạo nội dung vừa đúng sự thật nội bộ vừa bắt nhịp xu hướng.
4. Thiếu số liệu thật -> ghi `CẦN DỮ LIỆU`, tuyệt đối không bịa.

## Pha 3 — Tự kiểm Ngữ cảnh & Tư cách trước khi ghi (`fb_ext_inspect_controls`)
1. Xác nhận `channel_type_detected` khớp mục tiêu (`page_or_profile`, `group`, `business_suite`).
2. Nếu mục tiêu là `owner_page` và thấy `acting_as_personal_warning == true` -> **DỪNG cảnh báo chủ chuyển sang tư cách Fanpage** trước khi đăng/bình luận.
3. Nếu mục tiêu là `trending_source` -> chỉ được đọc, không gọi `fb_ext_draft_post`.
4. Mặc định giữ `auto_publish=false` / `send=false` (điền nháp trên Chrome cho chủ kiểm duyệt).

## Pha 4 — Tương tác Đúng chỗ & Học lại
1. Điều hướng chuẩn bằng `fb_ext_open_url(url=...)` rồi thực thi thao tác đích.
2. Lưu kênh mới tìm thấy (Fanpage, Nhóm, Tài khoản cá nhân xu hướng) vào `fb_ext_channel_registry(op="upsert", ...)` để các phiên sau gọi tức thì.
3. Báo cáo theo Hiến chương CAM (Sản phẩm, Bằng chứng E1, Đã/Chưa kiểm, Rủi ro, `<= 3` bước tiếp theo).
