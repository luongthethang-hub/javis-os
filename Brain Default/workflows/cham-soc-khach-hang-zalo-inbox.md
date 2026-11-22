---
type: workflow
name: Chăm sóc Khách hàng Zalo & Inbox Đa kênh
slug: cham-soc-khach-hang-zalo-inbox
team: tm_cskh_omnichannel
triggers:
  - Trực tin nhắn Page & Zalo
  - Xử lý khiếu nại / Chốt hẹn khách hàng
updated: '2026-11-21'
---

# Quy trình Chăm sóc Khách hàng Zalo & Inbox

1. **Kiểm tra Trạng thái Kênh (`tro-ly-truc-page-zalo`):**
   - Dùng `messenger-health` và công cụ Zalo để bảo đảm token và webhook thông suốt.
2. **Quét & Phân loại Hội thoại (`tro-ly-truc-page-zalo`):**
   - Dùng `inbox-reply` và Zalo để đọc lịch sử tin nhắn, phân loại theo 3 nhóm: Mới quan tâm (Lạnh) / Đang hỏi giá-tư vấn (Ấm) / Chốt lịch-mua hàng (Nóng).
3. **Soạn Phản hồi Chuẩn hóa (`truong-nhom-cskh`):**
   - Áp dụng kịch bản tư vấn tự nhiên, đồng bộ giọng văn thương hiệu cá nhân của chủ (`giam-doc-thuong-hieu` giám sát).
   - Với khách Nóng hoặc tình huống nhạy cảm: đóng gói tóm tắt chuyển thẳng cho chủ duyệt trước khi gửi.
