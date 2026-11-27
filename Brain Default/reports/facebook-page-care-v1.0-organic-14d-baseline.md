# Facebook Page Care — Baseline organic 14 ngày (bài thực hành vai Đo lường)

**Trace:** `fb-growth-1625`  
**Trạng thái:** DRY RUN CÓ BẰNG CHỨNG — chưa lập được baseline số; chờ QA độc lập  
**Thời điểm trích xuất:** `2026-11-28 03:21:36 UTC+07:00` (nguồn đồng hồ: `javis_now`, cấu hình `Asia/Bangkok`; cùng độ lệch UTC với cửa sổ báo cáo nhưng không đồng nhất nhãn múi giờ)  
**Cửa sổ baseline đã khóa:** `[2026-11-14 00:00:00, 2026-11-28 00:00:00)` theo `Asia/Ho_Chi_Minh` (14 ngày hoàn chỉnh gần nhất, không gồm ngày đang chạy).  
**Phạm vi:** chỉ Facebook Page đủ Page URL + Page ID + quyền đọc Insights; organic và paid tách riêng. PHỔ CẬP AI bị loại vì đã xác minh là Facebook Group ID `712410908881271`, không phải Fanpage.

## 1. Hai lần thử chỉ đọc

| Lần | Nguồn chính xác | Kết quả | Diễn giải hợp lệ |
|---|---|---|---|
| 1 | MCP `Facebook Trang (Graph API)` → `fb_pages_list`, gọi trong phiên này | Lỗi: `Chưa nối Fanpage nào` | Không có Page ID/quyền/Insights từ Graph API; không suy ra tài khoản không quản lý Page. |
| 2 | MCP `Facebook Chrome Bridge` → `fb_ext_discover_pages(auto_open_directory=false)` tại `https://www.facebook.com/pages/?category=your_pages` | `is_pages_directory=true`; công cụ trích 1 link `Meta Business Suite` (`https://www.facebook.com/latest/home`). Chuỗi ngữ cảnh có `Fitness At Home`, `Răng sún`, `Adam Rockie`, `Moments Of Love Official`, nhưng không trích URL/ID riêng của từng Page. | Đây là bằng chứng tên hiển thị dưới “Trang của bạn”, chưa đủ định danh Page và không chứa Insights. Không điều hướng/bypass hay thử lần 3. |

Đối chiếu artifact nguồn: `reports/facebook-page-care-v0.1-channel-verification.md` và `reports/facebook-page-care-v0.1-kpi.md`. Không dùng `pages_count=1` làm số lượng Page vì phần tử duy nhất được parser trả là link Meta Business Suite.

## 2. Kết quả baseline 14 ngày

Chỉ lập số cho Page **đủ định danh**. Trong lần chạy này không Page nào đạt điều kiện đó; bảng dưới giữ bốn lead để thể hiện đầy đủ trạng thái và edge case, không coi là bốn Page đã xác minh.

| Lead hiển thị | Page URL / ID / quyền Insights | Page likes (nếu nguồn có) | Total organic interactions | Organic interactions / reach | Net follows organic | Organic reach | Paid | Trạng thái |
|---|---|---:|---:|---:|---:|---:|---|---|
| Fitness At Home | N/A — chưa trích được URL/ID/quyền | N/A | N/A | N/A | N/A | N/A | Không truy xuất; không trộn | CHƯA CÓ BASELINE |
| Răng sún | N/A — chưa trích được URL/ID/quyền | N/A | N/A | N/A | N/A | N/A | Không truy xuất; không trộn | CHƯA CÓ BASELINE |
| Adam Rockie | N/A — chưa trích được URL/ID/quyền | N/A | N/A | N/A | N/A | N/A | Không truy xuất; không trộn | CHƯA CÓ BASELINE |
| Moments Of Love Official | N/A — chưa trích được URL/ID/quyền | N/A | N/A | N/A | N/A | N/A | Không truy xuất; không trộn | CHƯA CÓ BASELINE |

`N/A` ở đây nghĩa là **trường không khả dụng từ hai nguồn đã thử**, không phải 0. Không có số giả, số mẫu hay phép suy diễn nào được dùng.

## 3. Định nghĩa KPI để tái chạy khi có Insights

| KPI | Công thức / điều kiện | Đơn vị | Điều kiện nguồn |
|---|---|---|---|
| Page likes | Dùng trực tiếp trường Page likes/fans nếu export/API thực tế có; ghi nguyên tên trường | người/tài khoản theo định nghĩa Meta | N/A nếu nguồn không cung cấp; không thay bằng followers |
| Total organic interactions | `organic reactions + organic comments + organic shares + organic saves` | lượt | Cùng Page, cùng cửa sổ và cùng phạm vi organic. Thành phần thiếu → N/A hoặc công bố công thức rút gọn, không coi thiếu là 0 |
| Organic interactions/reach | `total organic interactions / organic reach × 100` | % | Chỉ tính khi tử và mẫu cùng cấp/cùng phạm vi, reach unique > 0. Thiếu/0 reach → N/A; không dùng impressions thay reach. Với dữ liệu cấp bài, ưu tiên median ERR bài và báo `n` như KPI v0.1 |
| Net follows organic | `organic follows gained − organic unfollows` | tài khoản ròng | Chỉ tính nếu nguồn có cả hai thành phần hoặc có trường net follows chính thức. Thiếu followers/unfollows → N/A |
| Organic reach | Dùng trực tiếp trường organic unique reach | người/tài khoản unique | Không cộng reach từng bài để suy ra Page reach; không cộng organic với paid |

Cửa sổ áp dụng cho KPI kỳ là đúng 14 ngày nêu trên. Nếu chỉ có KPI lifetime/snapshot, phải gắn nhãn riêng và không đưa vào baseline kỳ. Paid, nếu có, lấy từ Ads Manager/Marketing API thành bảng riêng với account timezone và attribution; tuyệt đối không ghép vào organic.

## 4. Dữ liệu tối thiểu để đo tiếp

1. Page URL chuẩn + Page ID + bằng chứng quyền đọc Insights cho đúng Page.
2. Export Meta Business Suite/Professional Dashboard hoặc Page Insights API cho cửa sổ đã khóa; có tên metric gốc, bộ lọc organic, timezone và extraction timestamp.
3. Các trường: Page likes (nếu có), reactions, comments, shares, saves, organic unique reach, follows gained và unfollows/net follows. Thiếu trường nào ghi N/A.
4. Lưu export gốc hoặc request/response đọc cùng mã băm/đường dẫn bằng chứng; không thu PII khách hàng.

## 5. Checklist tự kiểm để QA đánh giá vai trò

- [x] Cửa sổ đủ 14 ngày, biên thời gian và múi giờ IANA được ghi rõ.
- [x] Ghi thời điểm trích xuất và chênh lệch nhãn timezone của đồng hồ nguồn.
- [x] Tối đa đúng 2 lần thử chỉ đọc; không bypass, không điều hướng hay thao tác ngoài.
- [x] Chỉ dùng nguồn first-party đã gọi; ghi chính xác tool/URL/kết quả.
- [x] Không coi tên trong sidebar là đủ Page URL/ID/quyền.
- [x] Tách organic/paid; không cộng reach và không dùng impressions thay reach.
- [x] Likes, interactions, ERR, net follows, reach đều có công thức/đơn vị/điều kiện mẫu số.
- [x] Edge case thiếu reach hoặc followers ghi N/A, không ghi 0 và không suy diễn.
- [x] Loại PHỔ CẬP AI vì là Group.
- [x] Không tuyên bố tăng trưởng khi chưa đo; trạng thái là CHƯA CÓ BASELINE.

**Đề nghị QA:** kiểm trực tiếp artifact và chấm PASS/FAIL/NOT CHECKED từng mục; artifact này không tự tuyên bố PASS và workflow gate không được coi là đang enforce.
