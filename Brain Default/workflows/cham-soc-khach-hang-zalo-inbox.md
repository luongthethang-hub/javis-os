---
type: workflow
name: Chăm sóc Khách hàng Zalo & Inbox Đa kênh
slug: cham-soc-khach-hang-zalo-inbox
status: 'off'
group: Bán hàng
description: "Kiểm tra sức khỏe kênh Messenger/Zalo, phân loại hội thoại Lạnh/Ấm/Nóng và soạn phản hồi chuẩn giọng thương hiệu trình duyệt."
steps:
  - agent: javis-core
    task: "Kiểm tra trạng thái kết nối kênh Messenger/Zalo và quét hội thoại liên quan tới {{input}}. Phân loại rõ 3 nhóm khách: Mới quan tâm (Lạnh), Đang hỏi giá/tư vấn (Ấm), Chốt lịch/Khiếu nại/Nhạy cảm (Nóng). Không tự gửi tin ra ngoài ở bước này."
    tools: [messenger_check, inbox_find]
    max_retries: 2
  - agent: dola
    task: "Từ danh sách hội thoại đã phân loại ở {{prev}}, soạn phương án phản hồi tự nhiên, đúng giọng thương hiệu cá nhân của chủ cho từng nhóm khách. Với khách Nóng hoặc tình huống khiếu nại/nhạy cảm, tách riêng thành phiếu tóm tắt ngắn trình Layer 0 quyết định."
    max_retries: 2
  - agent: claude
    task: "Kiểm toán toàn bộ dự thảo phản hồi ở {{prev}}: rà soát rủi ro phát ngôn, cam kết sai sự thật, rò rỉ thông tin cá nhân/PII và chính sách nền tảng. Chốt danh sách phản hồi sạch kèm trạng thái CHỜ CHỦ DUYỆT trước khi gửi thật."
    max_retries: 2
updated: '2026-11-24'
---

# Quy trình Chăm sóc Khách hàng Zalo & Inbox Đa kênh

Workflow 3 bước kết nối `javis-core` -> `dola` -> `claude`. Mặc định `status: 'off'` và chỉ chuẩn bị bản nháp đã kiểm toán để bảo vệ cổng hành động ngoài (A1).
