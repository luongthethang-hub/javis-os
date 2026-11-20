---
type: workflow
name: Dựng video và trả MP4
slug: dung-video-tra-mp4
status: active
group: Nội dung
description: Tiếp nhận video, chốt brief và phương án, duyệt từng mốc dựng rồi trả MP4 đã kiểm tra.
execution_guard:
  enabled: true
  wall_seconds: 720
  idle_seconds: 270
  max_model_stages: 1
  max_tool_calls: 25
  max_reported_tokens: 22000
  max_output_chars: 30000
steps:
- id: render
  agent: bien-tap-video-ngan
  required_tools:
  - Bash
  require_first_line: TIẾN ĐỘ BIÊN TẬP
  max_retries: 0
  task: >-
    Đọc skills/video-animation-toolkit/references/quy-trinh-bien-tap-studio.md trước khi xử lý.
    Yêu cầu hiện tại và ngữ cảnh phiên: {{input}}.
    Dùng đúng tư liệu được chỉ định hoặc đính kèm. Nếu mới nhận video, đối chiếu đủ bốn nhóm brief,
    ghi rõ còn thiếu nhóm nào và hỏi nhóm cần làm rõ tiếp theo. Các mặc định đề xuất phải được xác nhận.
    Mỗi lượt chỉ tiến tới mốc cần chủ duyệt tiếp theo. Xác nhận của chủ phải khớp video, phiên bản
    và mốc hiện tại. Tóm tắt trạng thái ngắn ở đầu kết quả, gồm giai đoạn, tư liệu, mốc đã duyệt và
    mốc đang chờ; phần chi tiết giữ lại thông số và phương án cần cho lượt sau. Khi thiếu bằng chứng
    hoặc đổi tư liệu, xác nhận lại đúng phần liên quan. Với yêu cầu cắt nhanh cụ thể làm đúng phạm vi yêu cầu.
    Mở đầu mọi kết quả bằng dòng TIẾN ĐỘ BIÊN TẬP. Sau đó nêu rõ đang chờ gì, đã gửi bản nháp,
    gặp lỗi gì hoặc đã bàn giao. Chỉ ghi ĐÃ KIỂM TRA MP4 sau khi bản cuối đúng quy trình và tệp
    đã được kiểm tra. Trả liên kết Markdown tương đối, thông số và các tệp bổ trợ cần giao.
    Cuối lượt có thể phát JAVIS_LESSON cho bài học tái dùng đã được kiểm chứng.
updated: '2026-11-19'
---

Gửi MP4/MOV trong chat Cộng sự hoặc mở chat với Biên tập Video ngắn để bắt đầu tiếp nhận. Tiếp tục trong cùng cuộc trò chuyện để duyệt từng mốc. Mỗi lượt trả tình trạng của mốc hiện tại; bản MP4 cuối được bàn giao riêng sau khi chủ duyệt bản nháp và tệp qua kiểm tra.
