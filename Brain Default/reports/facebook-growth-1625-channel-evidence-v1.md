# Báo cáo bằng chứng kênh v1 — `fb-growth-1625`

- **Phạm vi:** chỉ đọc; tái sử dụng `reports/facebook-page-care-v0.1-channel-verification.md` và `reports/facebook-page-care-v0.1-channel-registry-proposal.md`; không làm lại kickoff, không ghi registry, không đổi tab/cấu hình/quyền, không đăng/gửi.
- **Thời điểm kiểm:** 2026-11-28 03:20 ICT (Asia/Bangkok, UTC+7), theo `javis_now`.
- **Giới hạn thử:** đã dùng đủ 2 lượt kiểm hợp lệ, không bypass.

## Hai lượt kiểm và bằng chứng

1. **Lượt 1 — nguồn Facebook trực tiếp:**
   - `fb_pages_list` (Graph API) trả lỗi xác định: **“Chưa nối Fanpage nào”**. Phân loại: thiếu kết nối nguồn Graph, không phải bằng chứng tài khoản không quản lý Page.
   - `fb_ext_discover_pages(auto_open_directory=false)` đọc đúng tab đang hoạt động `https://www.facebook.com/pages/?category=your_pages`, nhận diện `is_pages_directory=true`. Trong ngữ cảnh **“Trang của bạn”**, DOM liệt kê: **Fitness At Home, Răng sún, Adam Rockie, Moments Of Love Official**; nhưng extractor chỉ trả một mục liên kết **Meta Business Suite** (`https://www.facebook.com/latest/home`, `can_switch=false`), không trả URL/ID riêng của bốn tên.
   - Cùng kết quả trả tab Group PHỔ CẬP AI với URL tường minh `https://www.facebook.com/groups/712410908881271`.
2. **Lượt 2 — soi ngữ cảnh không bấm + nguồn lực local:**
   - `fb_ext_inspect_controls()` xác nhận tab hiện tại là `pages_directory`, không phải Group/Business Suite; `acting_as_personal_warning=false`, không thấy cảnh báo chuyển tư cách Trang. Kết quả này **không** xác nhận quyền quản trị, quyền insights hay quyền xuất bản trên từng Page.
   - Quét nguồn lực local theo bốn tên: không có `attachments/fanpages`; không tìm thấy asset khớp Fitness/Răng sún/Adam. Có hai tệp `video/moments.md` trong một pilot video khác, nhưng tên chung “moments” không đủ ánh xạ sang Moments Of Love Official và không chứng minh quyền sử dụng; do đó không dùng làm asset của Page.

## Bản đồ kênh và khả năng pilot

| Tên | Loại | URL / ID | Bằng chứng ownership / tư cách | Organic insights | Hoạt động gần đây | Tài sản nội dung được phép | Trạng thái | Bước kiểm tiếp |
|---|---|---|---|---|---|---|---|---|
| Fitness At Home | Page lead; loại Page chưa xác minh bằng URL/node | N/A / N/A | **Mới thấy tên:** xuất hiện dưới “Trang của bạn” trên Pages Directory; quyền cụ thể **NOT CHECKED** vì không có URL/ID và Graph chưa nối | N/A — không có Page node/Insights source | N/A — chưa có URL/node để đọc đúng kênh | N/A — không có asset local ánh xạ và quyền sử dụng | **CHƯA ĐỦ ĐIỀU KIỆN CHỌN PILOT** | Cần URL hoặc Page ID trực tiếp; sau đó đọc quyền/insights/posts và hồ sơ quyền asset |
| Răng sún | Page lead; chưa xác minh bằng URL/node | N/A / N/A | Như trên: tên ở “Trang của bạn”, không suy ra role/capability | N/A | N/A | N/A | **CHƯA ĐỦ ĐIỀU KIỆN CHỌN PILOT** | Như trên |
| Adam Rockie | Page lead; chưa xác minh bằng URL/node | N/A / N/A | Như trên: tên ở “Trang của bạn”, không suy ra role/capability | N/A | N/A | N/A | **CHƯA ĐỦ ĐIỀU KIỆN CHỌN PILOT** | Như trên |
| Moments Of Love Official | Page lead; chưa xác minh bằng URL/node | N/A / N/A | Như trên: tên ở “Trang của bạn”, không suy ra role/capability | N/A | N/A | N/A — hai `moments.md` thuộc pilot khác, không đủ bằng chứng ánh xạ/quyền | **CHƯA ĐỦ ĐIỀU KIỆN CHỌN PILOT** | Như trên; chỉ nhận asset khi có manifest/nguồn/quyền rõ ràng |
| PHỔ CẬP AI 🚀✨ … | **Facebook Group, không phải Fanpage** | `https://www.facebook.com/groups/712410908881271` / Group ID `712410908881271` | Đã xác minh loại + URL/ID từ tab trực tiếp; role admin/mod/member **CHƯA XÁC MINH** | N/A cho bài toán Page | NOT CHECKED | NOT CHECKED | **LOẠI KHỎI ỨNG VIÊN PAGE PILOT** | Chỉ kiểm role Group bằng nguồn riêng nếu có yêu cầu độc lập; không trộn vào registry Page |

## Mapping đề xuất (chưa ghi registry)

- Giữ bốn khóa lead tạm: `lead:facebook:fitness-at-home`, `lead:facebook:rang-sun`, `lead:facebook:adam-rockie`, `lead:facebook:moments-of-love-official`; tất cả **không registry-ready**.
- Chỉ chuyển thành `facebook:page:{page_id}` sau khi có URL/ID chuẩn và bằng chứng capability theo từng trường (`view`, `insights`, `publish`, `moderate`).
- PHỔ CẬP AI giữ riêng `facebook:group:712410908881271`; không đưa vào danh sách Page.

## Kết luận đào tạo / handoff

- **Bài thực hành thường (Page đủ bằng chứng): NOT CHECKED / chưa có mẫu đạt.** Không Page nào trong bốn lead có đủ URL/ID + quyền insights + hoạt động gần đây + asset rights để chọn pilot thật.
- **Edge case Page/Group: đạt về phân loại bằng chứng.** PHỔ CẬP AI được tách rõ là Group bằng URL `/groups/{id}`.
- Leader có thể tiếp tục phần không phụ thuộc dưới dạng **local rehearsal**, nhưng phải ghi **không publish-ready** và không gắn đích Page. Không được dùng tên hoặc link Business Suite chung để đoán Page đích.
