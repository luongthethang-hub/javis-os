---
type: workflow
name: Xây dựng Thương hiệu Cá nhân Đa nền tảng
slug: xay-dung-thuong-hieu-ca-nhan
status: 'off'
group: Nội dung
description: "Chuyển hóa 1 ý tưởng gốc thành gói nội dung đồng bộ 4 kênh (Facebook, Shorts/TikTok, YouTube, Zalo) kèm kiểm chứng sự thật."
steps:
  - agent: grok
    task: "Phân tích ý tưởng hoặc trải nghiệm gốc trong {{input}}. Tấn công loại bỏ các góc nhìn sáo rỗng, tìm 1 luận điểm sắc bén có tính đối thoại thực tế và liên hệ đúng xu hướng ngành hiện tại."
    max_retries: 2
  - agent: antigravity
    task: "Dựa trên luận điểm đã chốt ở {{prev}} và ý tưởng gốc {{input}}, nhân bản đồng bộ thành 4 định dạng: (1) 01 bài storytelling/chuyên sâu cho Facebook, (2) 01 kịch bản video ngắn 45 giây chuẩn Voice-First cho TikTok/Shorts, (3) 01 dàn ý video dài YouTube, (4) 01 tin chia sẻ ngắn cho tệp khách Zalo. Không dùng em dash."
    max_retries: 2
  - agent: perplexity
    task: "Đối soát tính xác thực dữ kiện, độ nhất quán thông điệp giữa 4 kênh trong {{prev}} và kiểm tra chính sách nền tảng. Đề xuất tên trang tri thức nên lưu vào wiki/ nếu nội dung có giá trị tích lũy dài hạn, rồi bàn giao gói CHỜ CHỦ DUYỆT."
    verify_agent: claude
    max_retries: 2
updated: '2026-11-24'
---

# Quy trình Xây dựng Thương hiệu Cá nhân Đa nền tảng

Workflow 3 bước phối hợp `grok` -> `antigravity` -> `perplexity` (đối soát bởi `claude`). Chuyển hóa 1 ý tưởng gốc thành 4 tài sản truyền thông đồng bộ.
