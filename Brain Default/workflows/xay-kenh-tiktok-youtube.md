---
type: workflow
name: Xây kênh TikTok & YouTube Tự động
slug: xay-kenh-tiktok-youtube
team: tm_video_studio
triggers:
  - Tạo kịch bản TikTok/YouTube
  - Dựng video ngắn/dài từ clip thô
updated: '2026-11-21'
---

# Quy trình Xây kênh TikTok & YouTube

1. **Nghiên cứu & Hook (`dao-dien-kich-ban-video`):**
   - Nếu có link tham khảo, dùng `youtube-read` để trích xuất cấu trúc kịch bản.
   - Viết kịch bản theo khung: Hook (3s đầu) -> Body (giữ chân, nhịp 3-5s/cảnh) -> CTA. Đề xuất 3 Tiêu đề SEO + ý tưởng Thumbnail.
2. **Kiểm duyệt Chính sách (`kiem-duyet-chat-luong`):**
   - Rà soát từ khóa nhạy cảm chống bóp tương tác hoặc vi phạm bản quyền/cộng đồng của TikTok và YouTube.
3. **Sản xuất Hậu kỳ (`ky-thuat-dung-video`):**
   - Nếu có clip thô hoặc yêu cầu audio: kích hoạt `video-animation-toolkit` (FFmpeg) hoặc `voice-note`, xuất MP4 chuẩn 9:16 (TikTok/Shorts) hoặc 16:9 (YouTube).
4. **Bàn giao:** Xuất gói hoàn chỉnh gồm Kịch bản + Tiêu đề/Hashtags SEO + File MP4 (nếu có) trình chủ duyệt.
