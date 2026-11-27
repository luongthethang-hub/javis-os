# Facebook Page Care — căn cứ và checklist vận hành/nghiệm thu v0.1

## Phạm vi
- Chỉ đọc quy trình/skill hiện có; không chạy hoặc bật workflow.
- Không điều tra lại Chrome Bridge hay tác vụ `t_fa7dae992ca3`.
- Không ghi Sổ Danh Bạ, không đăng/gửi/bình luận, không đổi cấu hình.

## Căn cứ đã đọc
| Nguồn | Phiên bản/trạng thái quan sát được | Bằng chứng áp dụng |
|---|---|---|
| `workflows/cham-soc-fanpage-facebook.md` | `slug: cham-soc-fanpage-facebook`; `status: off`; frontmatter `updated: 2026-11-24` | Dòng 5 xác nhận đang tắt; dòng 10–18 quy định đọc dữ liệu thật, phân tích có E1, soạn 4-1-1, kiểm chính sách và thẩm định; dòng 25 yêu cầu chỉ đăng sau Layer 0/cổng A1. |
| `skills/meta-cognition-channel-ops/SKILL.md` | Tệp hiện hành; không có trường version/updated trong frontmatter | Dòng 8–12 tách `owner_page`, `owner_profile`, `group`, `trending_source`; dòng 15–18 yêu cầu đọc sổ/trạng thái rồi discovery và không đoán kênh; dòng 20–24 yêu cầu tìm nguồn lực, thiếu số liệu ghi `CẦN DỮ LIỆU`; dòng 26–30 kiểm loại kênh/tư cách và giữ `auto_publish=false`, `send=false`; dòng 35 yêu cầu báo cáo sản phẩm, E1, đã/chưa kiểm, rủi ro. Skill đã được nạp qua gateway bằng `javis_use_skill` cho nhiệm vụ này. |
| `workflows/nghiem-thu-bat-buoc.md` | `slug: nghiem-thu-bat-buoc`; `status: off`; frontmatter `updated: 2026-11-27` | Dòng 10–17: lập phiếu tiêu chí quan sát được, kiểm độc lập trên đầu ra thật, không chuyển bước khi thiếu bằng chứng/không đạt; dòng 28 xác nhận workflow đang tắt. |
| `skills/quy-trinh-nghiem-thu-bat-buoc/SKILL.md` | Tệp hiện hành; không có trường version/updated trong frontmatter | Dòng 11–14 yêu cầu chốt tiêu chí, người nghiệm thu độc lập và phê duyệt riêng cho tác động ngoài; dòng 20–23 yêu cầu bàn giao bằng chứng, chấm từng tiêu chí; dòng 25–31 định nghĩa trạng thái; dòng 37–40 cấm đồng nhất “xong” với “đạt” và cấm đạt khi thiếu log/dữ liệu/quyền. |

> Giới hạn truy cập: đường dẫn dự kiến `workflows/handoff/nghiem-thu-bat-buoc.md` không tồn tại. Bản workflow thực tế đọc được tại `workflows/nghiem-thu-bat-buoc.md`; bản skill thực tế tại `skills/quy-trinh-nghiem-thu-bat-buoc/SKILL.md`. Không có version/hash cho hai tệp skill nên không suy đoán phiên bản.

## Checklist vận hành chỉ đọc
- [ ] Ghi mục tiêu, phạm vi, đầu vào, giới hạn và kênh đích.
- [ ] Đọc `fb_ext_channel_registry(op="list")` và `fb_ext_status()` khi công cụ Facebook thật khả dụng.
- [ ] Nếu danh sách chưa đủ, discovery Pages và Groups riêng; không coi tên lead là Page đã xác minh.
- [ ] Phân loại từng mục đúng một loại: `owner_page` / `owner_profile` / `group` / `trending_source`; PHỔ CẬP AI phải được giữ là `group`, không nhập vào danh sách Fanpage.
- [ ] Với URL tường minh, xác minh URL/ID, loại kênh và tư cách truy cập bằng thao tác đọc; không chọn tab ngầm.
- [ ] Ghi riêng các trạng thái: **đã xác minh**, **mới thấy tên**, **thiếu quyền**, **lỗi công cụ**.
- [ ] Không suy diễn “0 bài” là kênh trống; ghi phạm vi đọc và giới hạn công cụ.
- [ ] Tra nguồn lực theo thứ tự: Second Brain → `resource_paths` → dữ liệu sống; mọi số liệu thiếu ghi `CẦN DỮ LIỆU`.
- [ ] Nếu có từ hai kênh phù hợp mà chưa nêu kênh đích, dừng chọn kênh thay vì đoán.
- [ ] Nếu có thao tác nháp ở bước sau, kiểm `channel_type_detected` và tư cách; giữ `auto_publish=false`, `send=false`.
- [ ] Không upsert registry trong nhiệm vụ này; chỉ **đề xuất** mapping tên → loại → URL/ID → `resource_paths` → bằng chứng → trạng thái.
- [ ] Báo cáo theo CAM: sản phẩm, bằng chứng E1, đã/chưa kiểm, rủi ro, tối đa ba bước tiếp.

## Checklist nghiệm thu độc lập
- [ ] Phiếu có mã việc, người giao, người làm, người nghiệm thu độc lập và phiên bản đầu ra.
- [ ] Tiêu chí bắt buộc quan sát được được chốt trước; tiêu chí khuyến nghị tách riêng.
- [ ] Có bảng kênh gồm: tên | loại | URL/ID | bằng chứng | trạng thái | bước kiểm tiếp.
- [ ] Mọi kết luận Page/Group, URL/ID và quyền truy cập có bằng chứng trực tiếp; lead chỉ có tên không được nâng thành “đã xác minh”.
- [ ] PHỔ CẬP AI được phân biệt rõ là Group, không lẫn Fanpage.
- [ ] Thiếu URL/quyền/dữ liệu và lỗi công cụ được ghi rõ; không đoán và không dùng 0 bài làm bằng chứng kênh trống.
- [ ] Có dấu vết đã dùng skill channel-ops và đã đọc workflow chăm sóc Page, nhưng cả hai workflow vẫn `off`/không chạy.
- [ ] Không có hành động ngoài: đăng, gửi, bình luận, đổi Ads, ghi registry, sửa Bridge/cấu hình hoặc tạo lịch lặp.
- [ ] Người nghiệm thu kiểm trên artifact/bằng chứng thật, chấm từng tiêu chí `ĐẠT` / `KHÔNG ĐẠT` / `CHƯA KIỂM` (quy đổi trạng thái hồ sơ theo skill khi chốt).
- [ ] Chỉ chốt `ĐẠT` khi toàn bộ tiêu chí bắt buộc được người độc lập kiểm và đạt; nếu thiếu bằng chứng dùng `CHƯA ĐỦ BẰNG CHỨNG` hoặc `CHỜ NGHIỆM THU`.

## Trạng thái v0.1
- Artifact này là bản trích tiêu chí, chưa phải kết quả xác minh Fanpage.
- Chưa bàn giao/chưa có phán quyết của người nghiệm thu độc lập trong bước này.
