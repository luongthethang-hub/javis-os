---
type: workflow
name: Red/Blue Team Review - AI Company
slug: red-blue-team-review
status: 'off'
group: AI
description: Vòng phản biện đối kháng 3 bước cho mọi đầu ra của AI Company - red attack, blue patch, biên bản phán quyết.
steps:
  - agent: phan-bien-cheo---chatgpt
    task: |
      [RED TEAM - TẤN CÔNG]
      Đầu ra cần kiểm tra: {{input}}

      Nhiệm vụ: phản biện đối kháng toàn diện đầu ra trên với vai trò red team. Tìm mọi lỗi logic, giả định thiếu, rủi ro ẩn, thiếu nhất quán, claim không có nguồn và điểm yếu kỹ thuật. Liệt kê từng điểm tấn công, không bỏ qua vì "nhỏ". Không đề xuất cách sửa - chỉ chỉ ra lỗi thật.
    verify_agent: quan-tri-rui-ro
    max_retries: 1

  - agent: nghien-cuu-kiem-chung
    task: |
      [BLUE TEAM - VÁ LỖI]
      Đầu ra gốc: {{input}}
      Phản biện red team: {{prev}}

      Với từng nhận định của Red Team, ghi số thứ tự và trích nguyên văn nhận định, rồi ghi phản hồi của Blue Team và căn cứ. Chọn một kết quả cho mỗi điểm: vá được, bác được, hoặc còn lỗi. Kèm bản đã chỉnh dưới dạng văn bản để chủ duyệt. Bước ghi biên bản nhận toàn bộ phần bàn giao này.
    max_retries: 1

  - agent: ghi-bien-ban-red-blue
    task: |
      [BIÊN BẢN PHÁN QUYẾT]
      Đầu ra gốc: {{input}}
      Bàn giao gồm nhận định của Red Team và phản hồi của Blue Team: {{prev}}

      Viết đúng một mã phán quyết ở dòng đầu, dạng văn bản thuần: DEBATE_VERDICT: PASS (Đạt), DEBATE_VERDICT: CONDITIONAL (Đạt có điều kiện) hoặc DEBATE_VERDICT: FAIL (Chưa đạt). Dòng mã chỉ gồm DEBATE_VERDICT: và một giá trị, không có diễn giải hay ký hiệu Markdown. Sau đó ghi biên bản theo định dạng của thư ký. Nếu thiếu dữ liệu quyết định hoặc còn lỗi cần xử lý trước khi bàn giao, dùng FAIL và nêu rõ điều kiện cần đáp ứng.
    max_retries: 1

updated: "2026-11-19"
---

## Mô tả

Workflow phản biện đối kháng 3 bước dùng cho toàn bộ AI Company - áp dụng cho mọi lĩnh vực: content, EA/trading, nghiên cứu thị trường, affiliate và kế hoạch chiến lược.

### Cách dùng

Chạy workflow với `{{input}}` là đầu ra cần kiểm tra:
- Bài content, kịch bản video, bản nháp đăng bài
- Bản vá EA, logic giao dịch, chiến lược
- Báo cáo nghiên cứu thị trường
- Kế hoạch affiliate, landing page

### Luồng 3 bước

```
Đầu ra gốc
    |
    v
[Bước 1] Phản biện chéo - ChatGPT  <-- RED TEAM: liệt kê lỗi, không đề xuất sửa
    |   (kiểm tra: Quản trị Rủi ro)
    v
[Bước 2] Nghiên cứu & Kiểm chứng   <-- BLUE TEAM: vá từng điểm hoặc bác bỏ có căn cứ
    |
    v
[Bước 3] Ghi biên bản Red/Blue Team <-- BIÊN BẢN: phán quyết Đạt / Chưa đạt + bài học
```

### Phán quyết

- **Đạt**: bàn giao thẳng sang Kiểm duyệt & Chuẩn bị đăng (hoặc bước tiếp tương ứng)
- **Đạt có điều kiện**: bàn giao kèm ghi chú, chủ duyệt quyết định
- **Chưa đạt**: trả về agent gốc vá thêm, chạy lại workflow

### Tích hợp vào luồng hiện có

Thêm bước `red-blue-team-review` vào trước bước duyệt cuối trong bất kỳ workflow nào:
- Content: sau khi `tro-ly-content-ca-nhan` viết xong, trước `kiem-duyet-chuan-bi-dang`
- EA: sau khi `ky-su-ea---claude` soạn bản vá, trước khi bàn giao chủ
- Nghiên cứu: sau khi `truong-phong-nghien-cuu` tổng hợp, trước khi chốt phán quyết
