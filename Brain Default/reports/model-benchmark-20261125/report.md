# Benchmark ShopDonk ngày 25/11/2026

## Kết luận

30 yêu cầu hợp lệ, 5 bài cho mỗi model. Năm model đạt 5/5; Gemini đạt 3/5. Chưa thể xếp hạng sức mạnh tổng quát từ bộ thử nhỏ này.

## Phương pháp

- Endpoint: https://api.shopdonk.com/v1/chat/completions; chỉ dùng dữ liệu giả lập.
- 5 vòng: số học, lọc và cộng dữ liệu, phát hiện lỗi Python, không bịa thông tin thiếu, tool calling giả lập.
- Cùng đề cho 6 model trong từng vòng. Seed 25112026 ngẫu nhiên hóa tham số số học, dữ liệu, ticket và thứ tự model; không phải 5 lần lấy mẫu độc lập cho từng kỹ năng.
- Tối đa 5 yêu cầu đồng thời, không tự retry. max_tokens=700, streaming bật. Không chạy tool do model sinh ra.
- Đồng hồ đo từ lúc worker gửi request đến khi nhận xong; không tính thời gian chờ hàng đợi local. TTFT là lúc nhận content/tool delta đầu tiên.
- Đáp án được đối chiếu bằng mã, không dùng AI tự chấm. JSON có code fence được chấp nhận khi nội dung bên trong parse được.
- Thời gian là độ trễ đầu cuối qua reseller, gồm mạng và hàng đợi, không phải tốc độ thuần của model. TTFT gần tổng thời gian ở nhiều request nên không suy ra tokens/giây đáng tin cậy.

## Kết quả

| Model | Đạt | Trung vị hoàn tất (giây) | Trung vị TTFT (giây) | Tool call |
|---|---:|---:|---:|---|
| claude-sonnet-4-6 | 5/5 | 36,363 | 36,362 | Đạt |
| gpt-6-luna | 5/5 | 23,951 | 23,950 | Đạt |
| gpt-5.6-sol | 5/5 | 23,473 | 23,473 | Đạt |
| deepseek-v4.1-flash | 5/5 | 26,070 | 26,070 | Đạt |
| gemini-flash-3.8-high | 3/5 | 24,136 | 23,433 | Đạt |
| grok-4.7 | 5/5 | 41,376 | 41,376 | Đạt |

Gemini vòng dữ liệu: không có content để parse. Vòng Python: trả result=20 thay vì 21; fixed=23 đúng. Không suy luận nguyên nhân nội bộ của kết quả rỗng.

Claude đã tạo đúng tool call lần này. Kết quả này thay thế nhận định lịch sử rằng model này không gọi được tool, nhưng chỉ chứng minh một lần gọi giả lập thành công.

## Mức sử dụng và giới hạn

Provider báo tổng 21.044 prompt tokens và 2.142 completion tokens cho các request có trường usage. Một request rỗng không có usage trong bản ghi nên đây không phải tổng tính phí đầy đủ. Không có dữ liệu số tiền thực trả.

Trước lượt hợp lệ có 30 yêu cầu HTTP 401 do script đọc nguyên giá trị khóa mã hóa trong settings thay vì giải mã. Đây là lỗi harness, không phải năng lực model. Đã sửa đọc khóa trong bộ nhớ và chạy lại; không ghi khóa giải mã ra file. Không biết provider có ghi nhận chi phí cho yêu cầu 401 hay không.

120 RPM và 5 luồng là giới hạn do chủ cung cấp, chưa kiểm chứng bằng load test. Không thử bão hòa endpoint. Tên model và model trả về là nhãn của ShopDonk, không xác minh được backend thật.

Chưa test ngữ cảnh dài, MQL5/MT5, nội dung marketing, web thời gian thực, ảnh, nhiều lượt tool hoặc độ ổn định dài hạn. Vai trò cộng sự là đề xuất thử nghiệm hẹp, không phải chứng nhận chuyên môn.

## Cộng sự đã tạo

Sáu file mới, không ghi đè Hội đồng, không đổi model mặc định, không tạo team/cron/loop. Tất cả model_provider=openai-compat, tags AI/ShopDonk/Thử nghiệm.

- agents/shopdonk-sonnet-review.md: rà soát logic đoạn mã ngắn.
- agents/shopdonk-luna-analysis.md: phân tích có cấu trúc.
- agents/shopdonk-sol-test.md: kiểm thử tác vụ ngắn.
- agents/shopdonk-deepseek-data.md: kiểm tra số liệu nhỏ.
- agents/shopdonk-gemini-draft.md: bản nháp cần người/model khác kiểm tra; năng lực viết chưa được benchmark.
- agents/shopdonk-grok-check.md: kiểm tra tính nhất quán văn bản ngắn; không mặc định có web.

Đã kiểm tra YAML, model/provider, tags, file tồn tại và không chứa em dash. Chưa chạy nhiệm vụ từ dashboard qua từng cộng sự; kết nối API trực tiếp đã được kiểm tra, đường agent runtime chưa nghiệm thu end-to-end.

Hoàn tác: gỡ đúng sáu file mới theo agents-created.json sau khi chủ xác nhận; không tác động cộng sự cũ.

## Bằng chứng

- benchmark.py: chương trình và cách chấm; chạy bằng python -I với đường dẫn tuyệt đối.
- results.json: prompt, đáp án chuẩn, output thực, thời gian, usage từng request hợp lệ.
- summary.json: tổng hợp theo model.
- agents-created.json: danh sách file mới.

Không sửa mã nguồn repo Javis nên không chạy lint/test toàn repo. Kiểm chứng trong lượt này là 30 bài API và kiểm tra cấu trúc sáu file cộng sự.
