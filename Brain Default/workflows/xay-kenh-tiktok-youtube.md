---
type: workflow
name: Xây kênh TikTok & YouTube Tự động
slug: xay-kenh-tiktok-youtube
status: 'off'
group: Nội dung
description: "Nghiên cứu hook 3 giây, viết kịch bản Voice-First, kiểm duyệt chính sách và đóng gói đặc tả Motion.md sẵn sàng dựng MP4."
steps:
  - agent: grok
    task: "Nghiên cứu chủ đề hoặc link tham khảo trong {{input}} (đọc phụ đề YouTube nếu có link). Xây dựng kịch bản chuẩn Voice-First: Hook 3 giây đầu -> Body giữ nhịp 3-5 giây/cảnh -> CTA rõ ràng, kèm 3 tiêu đề SEO và 2 ý tưởng Thumbnail."
    tools: [javis_youtube_read]
    max_retries: 2
  - agent: codex
    task: "Kiểm duyệt kịch bản ở {{prev}}: rà soát từ khóa nhạy cảm dễ bị bóp tương tác hoặc vi phạm bản quyền/cộng đồng TikTok & YouTube; chuẩn hóa bảng phân cảnh theo mốc thời gian (giây) và phụ đề ngắn gọn dễ đọc."
    max_retries: 2
  - agent: antigravity
    task: "Đóng gói sản phẩm từ {{prev}} thành đặc tả kỹ thuật Motion.md tương thích pipeline OpenMotion / FFmpeg (Voice-First, chuẩn 9:16 cho TikTok/Shorts hoặc 16:9 cho YouTube, lưu ý xử lý chữ Đ đầu câu cho Azure TTS). Trình gói hoàn chỉnh ở trạng thái CHỜ CHỦ DUYỆT trước khi render/đăng."
    max_retries: 2
updated: '2026-11-24'
---

# Quy trình Xây kênh TikTok & YouTube Tự động

Workflow 3 bước phối hợp `grok` -> `codex` -> `antigravity` theo quy chuẩn Voice-First và OpenMotion. Mặc định `status: 'off'`, luôn trình chủ duyệt trước bước render hoặc xuất bản.
