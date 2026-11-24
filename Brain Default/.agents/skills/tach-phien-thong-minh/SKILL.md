---
name: Tách phiên thông minh
description: "Nén ngữ cảnh có kiểm chứng và tạo bàn giao để tiếp tục trong phiên mới."
group: AI
---

# Tách phiên thông minh

## Khi nào dùng

Kích hoạt khi một cuộc hội thoại dài, có nhiều công cụ/tệp, hoặc gateway báo ngữ cảnh lớn. Dùng đặc biệt khi:

- đầu vào của phiên từ 12M token trở lên;
- phiên có nhiều hơn 3 mạch công việc độc lập;
- trước khi bắt đầu một hạng mục lớn mới không phụ thuộc đáng kể vào tranh luận cũ;
- cần đổi model, chuyển sang ChatGPT Desktop hoặc Codex Desktop;
- người dùng yêu cầu giảm chi phí ngữ cảnh hoặc tách phiên.

Không tách giữa một thao tác nguyên tử đang dở, một câu trả lời còn phải dựa vào các chi tiết chưa được lưu, hoặc khi yêu cầu hiện tại chỉ cần trả lời ngắn.

## Chuẩn bị

1. Đọc `AGENTS.md` và `wiki/_session-handoff.md` nếu tệp này có nội dung trạng thái mở.
2. Chỉ dùng bằng chứng đã có trong phiên, tệp vault và kết quả tool. Không biến suy đoán thành quyết định đã chốt.
3. Xác định phạm vi: một phiên chỉ giữ một mục tiêu chính hoặc một nhóm việc phụ thuộc chặt chẽ.

## Quy trình

1. Thu tín hiệu: ưu tiên telemetry token/ngữ cảnh do gateway cung cấp. Nếu không có, chỉ dùng các dấu hiệu cấu trúc đã quan sát được như luồng độc lập mới, đổi model hoặc yêu cầu tách phiên. Không quy đổi số lượt chat hay độ dài cảm nhận thành số token.
2. Quyết định: không tách nếu đang ở thao tác nguyên tử hoặc còn dữ kiện bắt buộc chưa được ghi. Nếu đủ điều kiện, chọn một lý do duy nhất: `threshold`, `new-workstream`, `model-handoff` hoặc `manual`.
3. Phân loại nội dung phiên thành: mục tiêu đang làm, dữ kiện đã xác minh, quyết định của chủ, việc đã hoàn tất, việc đang dở, câu hỏi mở, rủi ro/chưa xác minh và tệp liên quan.
4. Loại khỏi bàn giao: lời xã giao, lịch sử thử sai không còn giá trị, log công cụ dài, hướng dẫn hệ thống và bản sao của nội dung đã nằm trong tệp.
5. Ghi hoặc cập nhật `wiki/_session-handoff.md` theo mẫu bên dưới. Nếu đang có bàn giao `status: active`, chỉ thay đúng phần liên quan và giữ các mục chưa giải quyết. `Files to read` chỉ gồm các tệp thực sự cần cho bước tiếp theo.
6. Kiểm chứng trước khi đề nghị tách: đọc lại tệp bàn giao, xác nhận có mục tiêu, trạng thái thật, đúng một bước tiếp theo, ít nhất một tệp liên quan khi có tệp, và các điểm chưa xác minh được gắn nhãn.
7. Báo người dùng rằng nên mở phiên mới, kèm một prompt khởi động tối đa 120 từ. Không nói đã tự mở/tự tách phiên nếu không có công cụ chứng minh việc đó.
8. Ở phiên mới, AI phải đọc `AGENTS.md`, rồi `wiki/_session-handoff.md`, sau đó chỉ đọc những tệp được liệt kê trong `Files to read`. Khi đã tiếp nhận xong, giữ `status: active` nếu công việc còn mở hoặc đổi `clear` nếu không còn việc.
9. Khi một luồng độc lập xuất hiện, tạo một bàn giao riêng theo `branch_id` thay vì kéo toàn bộ lịch sử của luồng chính sang.

## Ma trận kích hoạt

| Tín hiệu đã xác minh | Hành động bắt buộc | Giới hạn |
|---|---|---|
| Từ 12M đến dưới 25M token đầu vào, sắp vào pha việc lớn | Cập nhật bàn giao trước pha mới | Có thể tiếp tục trong phiên hiện tại nếu việc vẫn phụ thuộc chặt chẽ |
| Từ 25M đến dưới 40M token | Tạo và kiểm tra bàn giao, đề nghị phiên mới trước pha tiếp theo | Không nạp thêm transcript thô |
| Từ 40M token trở lên | Tạo bàn giao khẩn cấp, dừng mở rộng lịch sử cũ | Chỉ tra lại chi tiết chưa lưu nếu đó là điều kiện bắt buộc |
| Luồng độc lập, đổi model hoặc người dùng yêu cầu tách | Tạo/cập nhật bàn giao theo lý do tương ứng | Không cần số token |
| Không có telemetry và không có dấu hiệu cấu trúc | Không tự kích hoạt | Tiếp tục trả lời yêu cầu hiện tại |

## Mẫu bàn giao

```markdown
---
type: session-handoff
status: active
updated: YYYY-MM-DD HH:mm
branch_id: <slug-ngan>
context_reason: threshold|new-workstream|model-handoff|manual
---

# Bàn giao phiên: <mục tiêu ngắn>

## Mục tiêu hiện hành
- ...

## Sự thật đã xác minh
- ... [nguồn hoặc tệp]

## Quyết định của chủ
- ...

## Đã hoàn tất
- ...

## Đang làm
- ...

## Chưa xác minh hoặc rủi ro
- ...

## Bước tiếp theo duy nhất
- ...

## Files to read
- `đường/dẫn/tệp`

## Không cần mang sang
- ...
```

## Ngưỡng và nguyên tắc

- `>=12M` token đầu vào: tạo bàn giao trước khi làm thêm một pha việc lớn.
- `>=25M`: dừng kéo thêm lịch sử thô; chỉ tiếp tục sau khi đã tạo bàn giao và dùng phiên mới cho pha tiếp theo.
- `>=40M`: coi là khẩn cấp. Không nạp lại transcript cũ trừ khi một chi tiết chưa lưu là điều kiện bắt buộc để hoàn thành yêu cầu hiện tại.
- Một bàn giao nên dưới 1.200 từ, ưu tiên liên kết tệp thay vì chép lại nội dung.
- Với mã nguồn, chỉ nêu đường dẫn, commit/LKG nếu biết và thay đổi cần làm. Không dán toàn bộ mã vào bàn giao.

## Bẫy

- Tóm tắt không thay thế source of truth. Quyết định, số liệu và kết quả test quan trọng phải trỏ đến tệp hoặc kết quả gốc.
- Không tự xoá hoặc sửa transcript, nguồn thô và lịch sử chat.
- Không hứa việc sẽ tiếp tục ở phiên mới. Phiên mới chỉ bắt đầu khi người dùng mở nó hoặc nền tảng thực sự tạo được phiên đó.
- Không dùng tách phiên để né một câu hỏi đang cần trả lời ngay.

## Kiểm chứng

Trước khi kết thúc, đọc lại `wiki/_session-handoff.md` và kiểm tra có đủ: mục tiêu, trạng thái thật, bước tiếp theo, ít nhất một đường dẫn khi có tệp liên quan, và mọi điểm chưa xác minh đều được đánh dấu.
