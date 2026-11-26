# CUP-<NNNN>: <tiêu đề ngắn>

- **Ngày:** YYYY-MM-DD · **Người đề xuất:** CAM/<model> · **Tầng:** T1 | T2 | T3 · **Bậc semver:** MAJOR | MINOR | PATCH
- **Học viên/hệ ảnh hưởng:** HV-… · **Trạng thái:** nháp | chờ duyệt | đã duyệt | từ chối | đã lùi

## 1. Vấn đề
Một đoạn: chuyện gì sai/thiếu, ai bị ảnh hưởng.

## 2. Bằng chứng (nhãn E)
| trace_id / bệnh án | Số đo | Nhãn E |
|---|---|---|
Điều kiện đủ để thành CUP: lặp ≥2 lần **hoặc** gây thiệt hại 1 lần.

## 3. Thay đổi đề xuất (diff)
```diff
- cũ
+ mới
```

## 4. Golden test mới (viết TRƯỚC khi sửa)
- `GT-…`: trượt trên bản cũ ☐ · đạt trên bản mới ☐

## 5. Kiểm hồi quy
- Tổng test: … · đạt cũ→mới: … → … · test cũ đạt nay trượt: 0 (bắt buộc)
- Shadow test (nếu ảnh hưởng chi phí/chất lượng): mẫu …, người chấm khác hãng …, kết quả …

## 6. Kiểm toàn hệ (không tối ưu một con số)
| An toàn | Trung thực | Chi phí/tác vụ | Điểm chạm L0/tuần |
|---|---|---|---|

## 7. Rủi ro và đường lùi
- Rủi ro: …
- Lùi: checkout tag `teacher-v…` / hoàn file … về bản …; ai làm, mất bao lâu.

## 8. Duyệt
☐ L0 duyệt ngày … (T3 có thể duyệt theo lô)
