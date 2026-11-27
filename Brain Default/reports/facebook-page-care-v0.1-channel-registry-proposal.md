# Facebook Page Care — Đề xuất Channel Registry / Resource Mapping v0.1

- Phạm vi: đề xuất chỉ đọc dựa duy nhất trên `reports/facebook-page-care-v0.1-channel-verification.md` và kết quả Sổ Danh Bạ `ok=true`, `count=0`, `channels=[]` đã ghi trong báo cáo đó.
- **Không ghi registry thật.** Các khóa `lead:*` chỉ là khóa theo dõi tạm trong báo cáo, không phải định danh kênh và không được dùng để đăng/gửi.
- Quy tắc: chỉ tạo khóa tài nguyên chính thức khi loại kênh và ID đã được xác minh; không suy diễn `pages_count=0` là tài khoản không quản lý Page.

## Bản đồ đề xuất

| Khóa tài nguyên đề xuất | Tên hiển thị | Loại | URL / ID | Capability / quyền đã có bằng chứng | Nguồn bằng chứng | Trạng thái xác minh | Blocker / bước kiểm tiếp |
|---|---|---|---|---|---|---|---|
| `lead:facebook:fitness-at-home` *(tạm, không registry-ready)* | Fitness At Home | **CHƯA XÁC MINH**; chỉ là lead được gọi là Page | URL: **THIẾU**; ID: **THIẾU** | Graph API: **chưa nối Fanpage**; Bridge không trả Page từ màn hình Group hiện tại; quyền quản lý: **CHƯA XÁC MINH** | TaskPacket chỉ cung cấp tên lead; `fb_pages_list` báo “Chưa nối Fanpage nào”; `fb_ext_discover_pages(auto_open_directory=false)` trả `pages_count=0` trên màn hình Group | **MỚI THẤY TÊN / CHƯA XÁC MINH** | Blocker: thiếu URL/ID tường minh và nguồn chứng minh quyền. Kiểm node/Page ID và quyền chỉ đọc khi có URL hoặc Graph API đã nối. |
| `lead:facebook:rang-sun` *(tạm, không registry-ready)* | Răng sún | **CHƯA XÁC MINH**; chỉ là lead được gọi là Page | URL: **THIẾU**; ID: **THIẾU** | Như trên; quyền quản lý: **CHƯA XÁC MINH** | Cùng nguồn và giới hạn như trên | **MỚI THẤY TÊN / CHƯA XÁC MINH** | Blocker: thiếu URL/ID tường minh và nguồn chứng minh quyền. Kiểm node/Page ID và quyền chỉ đọc khi có URL hoặc Graph API đã nối. |
| `lead:facebook:adam-rockie` *(tạm, không registry-ready)* | Adam Rockie | **CHƯA XÁC MINH**; chỉ là lead được gọi là Page | URL: **THIẾU**; ID: **THIẾU** | Như trên; quyền quản lý: **CHƯA XÁC MINH** | Cùng nguồn và giới hạn như trên | **MỚI THẤY TÊN / CHƯA XÁC MINH** | Blocker: thiếu URL/ID tường minh và nguồn chứng minh quyền. Kiểm node/Page ID và quyền chỉ đọc khi có URL hoặc Graph API đã nối. |
| `lead:facebook:moments-of-love-official` *(tạm, không registry-ready)* | Moments Of Love Official | **CHƯA XÁC MINH**; chỉ là lead được gọi là Page | URL: **THIẾU**; ID: **THIẾU** | Như trên; quyền quản lý: **CHƯA XÁC MINH** | Cùng nguồn và giới hạn như trên | **MỚI THẤY TÊN / CHƯA XÁC MINH** | Blocker: thiếu URL/ID tường minh và nguồn chứng minh quyền. Kiểm node/Page ID và quyền chỉ đọc khi có URL hoặc Graph API đã nối. |
| `facebook:group:712410908881271` *(registry-ready về danh tính, chưa đủ quyền)* | PHỔ CẬP AI 🚀✨ Vibe code, AI Agent, Skills, Cowork - Codex, Claude... | **Facebook Group** — không phải Fanpage | URL: `https://www.facebook.com/groups/712410908881271`; Group ID: `712410908881271` | Có phiên đăng nhập nhìn thấy tab; capability quản trị/đăng/kiểm duyệt và vai trò admin/mod/member: **CHƯA XÁC MINH** | `fb_ext_discover_pages(auto_open_directory=false)` trả trực tiếp tiêu đề và URL `/groups/712410908881271`; ID trích từ cấu trúc URL | **ĐÃ XÁC MINH loại + URL/ID; THIẾU XÁC MINH TƯ CÁCH** | Blocker: tool quét Group trả `UNKNOWN_ACTION`, chưa có nguồn vai trò chỉ đọc. Giữ ngoài danh sách Page; chỉ bổ sung role/capability khi có bằng chứng. |

## Resource mapping tối thiểu khi đưa vào registry thật

| Trường | Quy tắc v0.1 |
|---|---|
| `resource_key` | Page: `facebook:page:{page_id}`; Group: `facebook:group:{group_id}`. Không dùng tên làm định danh chính thức. |
| `display_name` | Tên quan sát được, kèm thời điểm/nguồn xác minh. |
| `channel_type` | Chỉ nhận `owner_page` khi đã xác minh là Page và có bằng chứng tư cách; Group dùng `group`, không nhập chung danh sách Page. |
| `canonical_url`, `platform_id` | Bắt buộc trước khi chuyển lead thành bản ghi chính thức. |
| `capabilities` | Ghi riêng từng năng lực đã chứng minh: `view`, `insights`, `inbox`, `publish`, `moderate`; không suy từ việc nhìn thấy tab. |
| `role/access_status` | Một trong: `verified`, `missing_access`, `unverified`, `tool_error`; phải dẫn nguồn. |
| `evidence` | Tên tool/nguồn, kết quả liên quan và thời điểm kiểm; lỗi công cụ phải tách khỏi thiếu quyền. |
| `resource_paths` | Chỉ thêm Page/Inbox/Insights URL sau khi từng đường dẫn được xác minh; hiện chưa có đường dẫn nào đủ bằng chứng. |

## Trạng thái nguồn và giới hạn

- Sổ Danh Bạ hiện `count=0`: chỉ có nghĩa chưa có bản ghi, **không** chứng minh tài khoản không quản lý Page.
- Graph API báo chưa nối Fanpage: phân loại là **thiếu kết nối nguồn**, không phải “Page không tồn tại”.
- Bridge kết nối và Safe Mode bật, nhưng đang ở màn hình Group; `pages_count=0` không phải bằng chứng kênh trống.
- `fb_ext_discover_groups` trả `UNKNOWN_ACTION`: phân loại là **lỗi công cụ**, không phải thiếu quyền hay không có Group.
- Không điều hướng/chọn tab ngầm, không sửa Bridge/cấu hình, không ghi/sửa/xóa registry.
