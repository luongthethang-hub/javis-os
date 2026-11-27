# Registry bằng chứng kênh Facebook v1 — `facebook-growth-leadership-1656`

- **Phiên bản:** v1.0
- **Thời điểm kiểm sống:** 2026-11-28 03:34:31 UTC+7 (`Asia/Bangkok`) theo `javis_now`.
- **Phạm vi:** chỉ đọc; áp dụng `meta-cognition-channel-ops`; không đăng/gửi, không chọn hoặc điều hướng tab ngầm, không ghi Sổ Danh Bạ, không đổi Bridge/cấu hình/quyền.
- **Giới hạn thử:** tối đa 2 tuyến an toàn; đã dùng đủ 2 tuyến và không bypass.
- **Trạng thái sản phẩm:** **XONG v1** (registry bằng chứng đã lập). **CHƯA ĐẠT điều kiện chọn Page/pilot thật** vì không có Page nào đủ URL/ID + quyền truy cập + quyền Insights.

## 1. Hai tuyến kiểm an toàn và bằng chứng

### Tuyến 1 — Facebook Trang qua Graph API

- `fb_pages_list` trả lỗi xác định: **“Chưa nối Fanpage nào”**.
- Phân loại: **thiếu kết nối nguồn Page Graph API**, không phải bằng chứng tài khoản quản lý 0 Page và không phải bằng chứng bốn Page lead không tồn tại.
- Hệ quả: không lấy được Page ID, canonical URL, task/role hoặc quyền Insights từ Graph API.

### Tuyến 2 — Facebook Chrome Bridge, chỉ đọc, không điều hướng

- `fb_ext_status`: `connected=true`, `paused=false`, `safe_mode=true`; tab hoạt động `https://www.facebook.com/groups/joins/`; `pending_commands=0`, `writes_last_hour=0`.
- `fb_ext_channel_registry(op=list)`: `ok=true`, `count=0`, `channels=[]`. Chỉ chứng minh sổ hiện trống, không chứng minh tài khoản không có Page/Group.
- `fb_ext_discover_pages(auto_open_directory=false)`: không tự chuyển tab; trả ba tab Facebook đang mở, gồm tab trực tiếp **PHỔ CẬP AI** tại `https://www.facebook.com/groups/712410908881271`. Màn hình hoạt động là Groups Directory nên `pages_count=0`; không được diễn giải thành 0 Page.
- `fb_ext_discover_groups(url=https://www.facebook.com/groups/joins/)`: đọc được 6 Group, tất cả `role_hint=member`. `member` chỉ chứng minh tư cách tham gia/nhìn thấy theo extractor, không chứng minh owner/admin/moderator.
- Bằng chứng Pages Directory gần nhất cùng phiên làm việc được tái sử dụng từ `reports/facebook-growth-1625-channel-evidence-v1.md` (03:20 ICT) và `reports/facebook-driving-b-channel-scan-v1.md` (03:29:39 ICT): trong ngữ cảnh “Trang của bạn” xuất hiện bốn tên **Fitness At Home, Răng sún, Adam Rockie, Moments Of Love Official**, nhưng extractor không trả canonical URL/Page ID hoặc capability riêng. Vì lượt hiện tại không điều hướng/chọn tab ngầm, các tên này giữ mức **MỚI THẤY TÊN**, không nâng thành Page đã xác minh.
- Không có nguồn nào trong hai tuyến trả owner profile; trạng thái owner profile là **KHÔNG PHÁT HIỆN TRONG NGUỒN ĐÃ QUÉT**, không phải “không tồn tại”.

## 2. Registry v1 — Page leads

| Tên | Loại | URL / ID | Bằng chứng sở hữu / quyền truy cập | Quyền Insights | Trạng thái | Bước kiểm tiếp |
|---|---|---|---|---|---|---|
| Fitness At Home | **Page lead; loại node chưa xác minh** | **CHƯA XÁC MINH / CHƯA XÁC MINH** | Tên từng xuất hiện dưới “Trang của bạn” trong Pages Directory lúc 03:20; không có node URL/ID, role hay capability | **NOT CHECKED** — Graph API chưa nối; Bridge không trả Page node | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Cần canonical URL hoặc Page ID tường minh; sau đó đối chiếu riêng `view` và `insights` bằng nguồn first-party chỉ đọc |
| Răng sún | **Page lead; loại node chưa xác minh** | **CHƯA XÁC MINH / CHƯA XÁC MINH** | Như trên | **NOT CHECKED** | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Như trên |
| Adam Rockie | **Page lead; loại node chưa xác minh** | **CHƯA XÁC MINH / CHƯA XÁC MINH** | Như trên | **NOT CHECKED** | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Như trên |
| Moments Of Love Official | **Page lead; loại node chưa xác minh** | **CHƯA XÁC MINH / CHƯA XÁC MINH** | Như trên; các tệp local tên “moments” không đủ ánh xạ và không chứng minh quyền asset | **NOT CHECKED** | **MỚI THẤY TÊN / CHƯA XÁC MINH QUYỀN** | Như trên; asset chỉ nhận khi có manifest nguồn/quyền |

> Link Meta Business Suite chung hoặc `https://www.facebook.com/latest/home` không được gán làm URL cho bất kỳ Page nào.

## 3. Registry v1 — Groups nhìn thấy/đã tham gia

| Tên | Loại | URL / ID | Bằng chứng sở hữu / quyền truy cập | Quyền Insights | Trạng thái | Bước kiểm tiếp |
|---|---|---|---|---|---|---|
| TUYỂN DỤNG QUẢN LÝ CỬA HÀNG - CỬA HÀNG TRƯỞNG | Group | `https://www.facebook.com/groups/tuyendungcuahangtruong` / ID **CHƯA XÁC MINH** | Groups Directory, `role_hint=member` | N/A cho Page Insights | **ĐÃ THẤY GROUP; KHÔNG XÁC MINH SỞ HỮU/ADMIN** | Chỉ kiểm vai trò khi có nguồn role trực tiếp |
| In2 Donghua Hub ❤️‍🩹 | Group | `https://www.facebook.com/groups/1499926457116342` / `1499926457116342` | Groups Directory, `role_hint=member` | N/A | **ĐÃ XÁC MINH LOẠI + URL/ID; KHÔNG XÁC MINH SỞ HỮU** | Như trên |
| Học nấu ăn cùng thầy Nghị ✅ | Group | `https://www.facebook.com/groups/1027966918504179` / `1027966918504179` | Groups Directory, `role_hint=member` | N/A | **ĐÃ XÁC MINH LOẠI + URL/ID; KHÔNG XÁC MINH SỞ HỮU** | Như trên |
| Vũ Trụ AI - Ứng Dụng AI X10 Năng Suất Kinh Doanh | Group | `https://www.facebook.com/groups/vutruai` / ID **CHƯA XÁC MINH** | Groups Directory, `role_hint=member` | N/A | **ĐÃ THẤY GROUP; KHÔNG XÁC MINH SỞ HỮU/ADMIN** | Như trên |
| Queen Medusa [ BTTH ] | Group | `https://www.facebook.com/groups/890037165391702` / `890037165391702` | Groups Directory, `role_hint=member` | N/A | **ĐÃ XÁC MINH LOẠI + URL/ID; KHÔNG XÁC MINH SỞ HỮU** | Như trên |
| PHỔ CẬP AI 🚀✨ Vibe code, AI Agent, Skills, Cowork - Codex, Claude... | **Group — không phải Fanpage** | Slug `https://www.facebook.com/groups/phocapaivn`; URL số `https://www.facebook.com/groups/712410908881271`; **Group ID `712410908881271`** | Groups Directory trả `role_hint=member`; tab trực tiếp và cấu trúc `/groups/{id}` xác nhận loại + ID; không có bằng chứng admin/mod | N/A cho Page Insights | **ĐÃ XÁC MINH GROUP + URL/ID; TƯ CÁCH QUẢN TRỊ CHƯA XÁC MINH** | Giữ ngoài danh sách Page/pilot Page; chỉ kiểm role qua nguồn trực tiếp nếu thật sự cần |

## 4. Registry v1 — owner profile

| Tên | Loại | URL / ID | Bằng chứng | Trạng thái | Bước kiểm tiếp |
|---|---|---|---|---|---|
| Chưa xác định | owner_profile | **KHÔNG CÓ DỮ LIỆU** | Hai tuyến không trả profile cụ thể | **KHÔNG PHÁT HIỆN TRONG NGUỒN ĐÃ QUÉT / NOT CHECKED** | Chỉ kiểm khi có URL profile tường minh; không suy profile từ phiên đăng nhập |

## 5. Bài thực hành vai Kênh & Kết nối

**Đề bài:** Với dữ liệu sống hiện có, lập registry phân biệt Page/Group/profile; ghi URL/ID, ownership/access, Insights và giới hạn diễn giải; xác nhận PHỔ CẬP AI; không vượt hai tuyến hoặc thay đổi cấu hình.

| Tiêu chí | Bằng chứng | Kết quả |
|---|---|---|
| Dùng đúng 2 tuyến an toàn và không bypass | Graph API + Chrome Bridge; `writes_last_hour=0`; không auto-open | **PASS** |
| Không nhầm Group thành Fanpage | PHỔ CẬP AI được xác nhận Group ID `712410908881271`, loại khỏi Page registry | **PASS** |
| Không biến tên trong “Trang của bạn” thành URL/ID/quyền | Bốn lead giữ nhãn MỚI THẤY TÊN / CHƯA XÁC MINH | **PASS** |
| Không suy `pages_count=0` hoặc registry rỗng thành không có Page | Giới hạn diễn giải được ghi rõ | **PASS** |
| Xác minh Page thường đủ URL/ID + access + Insights | Không Page nào có đủ nguồn first-party | **NOT CHECKED** |
| Xác minh quyền owner/admin/mod của Group | Extractor chỉ trả `role_hint=member` | **NOT CHECKED** |
| Xác minh owner profile | Không có URL/profile node tường minh | **NOT CHECKED** |
| Có sai phân loại hoặc tuyên bố quyền không có bằng chứng | Không quan sát thấy trong artifact | **PASS** (không có tiêu chí FAIL) |

**Kết luận qualification:** Bài edge case Page-vs-Group và kiểm soát không suy diễn **PASS**. Case thường trên một owner Page đủ bằng chứng **NOT CHECKED**, nên vai Kênh chưa thể được coi là qualified cho bước chọn Page/pilot thật.

## 6. Blocker và bàn giao

1. Bốn Page lead thiếu canonical URL/Page ID và capability `view/insights`; Graph API Page chưa nối.
2. Không có Page node nên không được đọc bài gần đây, chọn “best Page”, lập baseline hoặc gắn pilot thật.
3. Sổ kênh vẫn giữ nguyên `count=0`; không có cấu hình/Bridge/registry nào bị thay đổi.
4. Bước an toàn tiếp theo khi có nguồn mới: nhận URL/Page ID tường minh hoặc nguồn first-party Page chỉ đọc → xác minh loại/node → đối chiếu role và quyền Insights riêng; không dùng tên trùng hoặc link Business Suite chung.

## 7. Nguồn tham chiếu

- Công cụ sống lúc 03:34:31 UTC+7: `fb_pages_list`, `fb_ext_status`, `fb_ext_channel_registry(list)`, `fb_ext_discover_pages(auto_open_directory=false)`, `fb_ext_discover_groups`.
- `reports/facebook-growth-1625-channel-evidence-v1.md`.
- `reports/facebook-driving-b-channel-scan-v1.md`.
- `reports/facebook-page-care-v0.1-channel-verification.md`.
- `reports/facebook-page-care-v1.0-candidate-report-vi.md` và QA tương ứng.
- `workflows/cham-soc-fanpage-facebook.md`, `workflows/nghiem-thu-bat-buoc.md` — đều `status: off`, không được coi là runtime enforcement.
