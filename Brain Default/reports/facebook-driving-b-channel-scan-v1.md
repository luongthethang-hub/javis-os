# Quét kênh Facebook v1 — học lái xe hạng B / Nam Tam Điệp

- **Phạm vi:** chỉ đọc; không đăng/gửi/lên lịch, không chọn tab ngầm, không đổi Bridge/cấu hình/quyền, không ghi Sổ Danh Bạ.
- **Thời điểm kiểm:** 2026-11-28 03:29:39 ICT (Asia/Bangkok, UTC+7), theo `javis_now`.
- **Nguồn tái sử dụng:** `reports/facebook-growth-1625-channel-evidence-v1.md`, `reports/facebook-page-care-v0.1-channel-verification.md`.
- **Giới hạn:** đủ 2 lượt kiểm logic: (1) nguồn Graph API + trạng thái/sổ kênh; (2) Chrome Bridge quét Pages Directory và Groups Directory. Không bypass.

## Bằng chứng nguồn và tình trạng công cụ

1. **Facebook Trang (Graph API):** `fb_pages_list` trả lỗi xác định **“Chưa nối Fanpage nào”**. Đây là thiếu kết nối Page vào nguồn Graph, **không phải** bằng chứng người dùng không quản lý Page.
2. **Chrome Bridge:** `fb_ext_status` trả `connected=true`, `paused=false`, `safe_mode=true`; tab Facebook hoạt động là `https://www.facebook.com/pages/?category=your_pages`; không có thao tác ghi trong giờ (`writes_last_hour=0`).
3. **Pages Directory:** `fb_ext_discover_pages(auto_open_directory=false)` xác nhận đúng trang `category=your_pages`. DOM dưới ngữ cảnh **“Trang của bạn”** hiển thị bốn tên: Fitness At Home, Răng sún, Adam Rockie, Moments Of Love Official. Extractor chỉ bóc được link Meta Business Suite chung, không bóc URL/ID riêng; vì vậy quyền cụ thể trên từng Page vẫn **CHƯA XÁC MINH**.
4. **Groups Directory:** `fb_ext_discover_groups` đọc `https://www.facebook.com/groups/joins/`, trả 6 nhóm với `role_hint=member`. Đây là bằng chứng tài khoản thấy/đã tham gia nhóm, **không chứng minh** owner/admin/moderator.
5. **Sổ kênh:** `fb_ext_channel_registry(op=list)` trả `count=0`; chỉ có nghĩa sổ hiện không có bản ghi, không có nghĩa không tồn tại Page/Group.

## Bản đồ Fanpage

| Tên | Loại | URL / ID | Bằng chứng sở hữu hoặc quyền | Trạng thái | Bước kiểm tiếp |
|---|---|---|---|---|---|
| Fitness At Home | Page lead | **CHƯA XÁC MINH** | Tên xuất hiện dưới “Trang của bạn”; chưa có node URL/ID hoặc capability cụ thể | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Cần URL hoặc Page ID tường minh, rồi đối chiếu quyền chỉ đọc qua Graph/Business Suite |
| Răng sún | Page lead | **CHƯA XÁC MINH** | Như trên | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Như trên |
| Adam Rockie | Page lead | **CHƯA XÁC MINH** | Như trên | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Như trên |
| Moments Of Love Official | Page lead | **CHƯA XÁC MINH** | Như trên | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Như trên |

> Link `https://www.facebook.com/latest/home` là Meta Business Suite chung do extractor trả về, **không** được gán cho bất kỳ Page nào.

## Bản đồ Nhóm Facebook

| Tên | Loại | URL / ID | Bằng chứng sở hữu hoặc quyền | Trạng thái | Bước kiểm tiếp |
|---|---|---|---|---|---|
| TUYỂN DỤNG QUẢN LÝ CỬA HÀNG - CỬA HÀNG TRƯỞNG | Group | `https://www.facebook.com/groups/tuyendungcuahangtruong` / ID **CHƯA XÁC MINH** | Groups Directory trả `role_hint=member` | **ĐÃ THẤY NHÓM; KHÔNG XÁC MINH SỞ HỮU** | Chỉ kiểm admin/mod khi có nguồn vai trò trực tiếp |
| In2 Donghua Hub ❤️‍🩹 | Group | `https://www.facebook.com/groups/1499926457116342` / `1499926457116342` | `role_hint=member` | **ĐÃ XÁC MINH LOẠI + URL/ID; KHÔNG XÁC MINH SỞ HỮU** | Như trên |
| Học nấu ăn cùng thầy Nghị ✅ | Group | `https://www.facebook.com/groups/1027966918504179` / `1027966918504179` | `role_hint=member` | **ĐÃ XÁC MINH LOẠI + URL/ID; KHÔNG XÁC MINH SỞ HỮU** | Như trên |
| Vũ Trụ AI - Ứng Dụng AI X10 Năng Suất Kinh Doanh | Group | `https://www.facebook.com/groups/vutruai` / ID **CHƯA XÁC MINH** | `role_hint=member` | **ĐÃ THẤY NHÓM; KHÔNG XÁC MINH SỞ HỮU** | Như trên |
| Queen Medusa [ BTTH ] | Group | `https://www.facebook.com/groups/890037165391702` / `890037165391702` | `role_hint=member` | **ĐÃ XÁC MINH LOẠI + URL/ID; KHÔNG XÁC MINH SỞ HỮU** | Như trên |
| PHỔ CẬP AI 🚀✨ Vibe code, AI Agent, Skills, Cowork - Codex, Claude... | **Group, không phải Fanpage** | Slug: `https://www.facebook.com/groups/phocapaivn`; tab trực tiếp: `https://www.facebook.com/groups/712410908881271`; ID `712410908881271` | Groups Directory trả `role_hint=member`; tab trực tiếp xác nhận URL số. Không có bằng chứng admin/mod | **ĐÃ XÁC MINH LOẠI + URL/ID; TƯ CÁCH CHƯA XÁC MINH** | Chỉ kiểm vai trò nếu có nguồn quyền trực tiếp; không đưa vào registry Page |

## Kết luận cho “Nam Tam Điệp”

- Không có Page hay Group tên **Nam Tam Điệp** trong dữ liệu Pages Directory/Groups Directory vừa quét và sổ kênh đang trống.
- Kết quả này chỉ là **KHÔNG THẤY TRONG NGUỒN ĐÃ QUÉT**, không chứng minh kênh không tồn tại.
- **Không được suy đoán** Nam Tam Điệp tương ứng với một trong bốn Page lead hay sáu Group. Chưa có đích kênh đủ bằng chứng để gắn bản nháp hoặc chuẩn bị đăng.

## Handoff

- Nội dung có thể tiếp tục ở dạng bản nháp local, ghi **KHÔNG GẮN KÊNH / NOT PUBLISH-READY**.
- Muốn xác minh đích Nam Tam Điệp cần một URL/ID tường minh hoặc nguồn Page quyền trực tiếp; sau đó kiểm loại tài nguyên, tên, ID và capability riêng. Không dùng số bài bằng 0 hoặc sổ trống để kết luận kênh trống/không tồn tại.
