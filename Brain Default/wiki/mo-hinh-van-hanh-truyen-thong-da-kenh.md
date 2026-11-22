# Mô hình Vận hành Truyền thông Đa kênh & Thương hiệu Cá nhân (Javis OS + Antigravity)

> Cập nhật: 2026-11-21  
> Mục tiêu: Phục vụ chuyên nghiệp và tự động hóa 100% chuỗi giá trị từ ý tưởng đến xuất bản trên **Facebook Fanpage, Zalo, TikTok, YouTube và Thương hiệu Cá nhân**, vận hành trên hạ tầng **0đ API phát sinh** (Google AI Pro qua Antigravity Delegate).

## 1. Cấu trúc Tổ chức (4 Phòng Ban - 9 Nhân Sự Chuyên Trách)

| Phòng ban (`team_id`) | Trưởng nhóm | Thành viên phối hợp | Phạm vi phụ trách |
|---|---|---|---|
| **Ban Điều hành Thương hiệu Cá nhân** (`tm_brand_director`) | `giam-doc-thuong-hieu` | `kien-truc-su-antigravity`, `kiem-duyet-chat-luong` | Định vị thương hiệu cá nhân, nhân bản ý tưởng đa kênh, phân tích dữ liệu lớn và kiểm duyệt chính sách. |
| **Phòng Sản xuất Video** (`tm_video_studio`) | `dao-dien-kich-ban-video` | `ky-thuat-dung-video`, `kiem-duyet-chat-luong` | Kịch bản TikTok (Hook 3s), YouTube Long-form/Shorts, SEO video, hậu kỳ MP4/Audio qua FFmpeg. |
| **Phòng Fanpage Facebook & Meta Ads** (`tm_facebook_growth`) | `quan-tri-fanpage-fb` | `chuyen-vien-meta-ads`, `kiem-duyet-chat-luong` | Lên lịch nội dung 4-1-1, phân tích Graph API, tối ưu chiến dịch Meta Ads. |
| **Phòng CSKH Đa kênh** (`tm_cskh_omnichannel`) | `truong-nhom-cskh` | `tro-ly-truc-page-zalo`, `giam-doc-thuong-hieu` | Trực Inbox/Comment Facebook, chăm sóc khách hàng trên Zalo OA/Cá nhân, kịch bản chuyển đổi. |

## 2. Hạ tầng Công nghệ Cốt lõi được Giữ nguyên & Nâng cấp
- **MCP Hub & Connectors:** `meta-pages-graph`, `meta-ads-graph`, `inbox-reply`, `messenger-health`, `youtube-read`, `voice-note`, `image-chatgpt`, `video-animation-toolkit` (FFmpeg), Zalo MCP.
- **Suy luận & Phân tích chuyên sâu (0đ API):** `javis_antigravity_delegate` (chạy trên Google AI Pro) + `data-query` (SQLite ảo in-memory phân tích báo cáo Ads/Traffic lớn).
- **Quản trị tri thức:** Obsidian-compatible Second Brain (`Brain Default`) kết hợp Git versioning tự động.
