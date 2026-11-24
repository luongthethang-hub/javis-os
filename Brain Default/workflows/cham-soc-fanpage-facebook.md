---
type: workflow
name: Chăm sóc & Phát triển Fanpage Facebook
slug: cham-soc-fanpage-facebook
status: 'off'
group: Marketing
description: "Đo hiệu suất Fanpage/Meta Ads, soạn bài 4-1-1 đúng thương hiệu và kiểm duyệt chính sách Meta trước khi trình chủ duyệt."
steps:
  - agent: deepseek
    task: "Đọc dữ liệu thực tế bài viết Fanpage và hiệu suất Meta Ads liên quan tới yêu cầu {{input}}. Phân tích bài thắng (Winning Content), chỉ số tương tác/chuyển đổi, khoảng trống nội dung và đề xuất 1 góc khai thác có căn cứ số liệu E1."
    tools: [meta_ads_accounts, meta_ads_insights, meta_ads_campaigns, fb_pages_list, fb_page_posts]
    max_retries: 2
  - agent: dola
    task: "Dựa trên phân tích số liệu ở {{prev}} và yêu cầu {{input}}, soạn 01 bài Fanpage Facebook chuẩn cấu trúc 4-1-1 (Tiêu đề dừng lướt -> Nội dung giá trị/câu chuyện thực tế -> CTA dẫn tương tác/Inbox/Zalo) kèm 01 mô tả ý tưởng ảnh minh họa. Giữ giọng tự nhiên, sắc bén, không dùng em dash."
    max_retries: 2
  - agent: perplexity
    task: "Kiểm duyệt bài viết ở {{prev}}: đối soát số liệu với thực tế, lọc từ ngữ vi phạm chính sách Meta Ads và tiêu chuẩn cộng đồng Facebook, gắn nhãn trạng thái CHỜ CHỦ DUYỆT và bàn giao bản sạch sẵn sàng đăng khi chủ đồng ý."
    verify_agent: claude
    max_retries: 2
updated: '2026-11-24'
---

# Quy trình Chăm sóc & Phát triển Fanpage Facebook

Workflow 3 bước sử dụng đội hình Hội đồng hiện hành (`deepseek` -> `dola` -> `perplexity` với `claude` thẩm định cuối). Mặc định để `status: 'off'`; chỉ đăng bài thật sau khi Layer 0 duyệt (cổng A1).
