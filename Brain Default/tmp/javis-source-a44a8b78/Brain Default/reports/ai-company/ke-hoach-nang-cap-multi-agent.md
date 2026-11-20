# Nâng cấp phối hợp multi-agent trong Javis OS

## Quyết định kỹ thuật

Dùng các thành phần đang có trong Javis: định tuyến model trong `server/model_router.py` và `server/aux_engine.py`, lưu trạng thái đồ thị trong `server/workflow_runtime.py`, giới hạn workflow tuần tự trong `server/execution_guard.py`, mẫu Task Capsule trong Brain Default và kết nối Graphify. Việc đầu tiên là bổ sung chuyển nguồn có giới hạn vào đường chạy workflow tuần tự, dùng chính engine chỉ xử lý văn bản của Javis.

### Phản biện và cách chốt

| Đề xuất | Phản biện | Quyết định |
|---|---|---|
| Đưa mọi tuyến qua một proxy HTTP mới | CLI thuê bao, phiên cần quyền riêng và Ollama có vòng đời khác API HTTP. Chuyển đồng loạt dễ tốn thêm lần thử và thay đổi quyền của tác vụ. | Dùng adapter và bộ định tuyến hiện có. Cân nhắc proxy riêng sau khi có một lỗi có thể tái hiện mà adapter hiện tại không xử lý được. |
| Chuyển nguồn ngay khi thấy 429/503 | Chuỗi văn bản có thể nhắc tới mã lỗi mà không phải lỗi thật. Một lượt đã phát nội dung hoặc gọi công cụ có thể tạo kết quả trùng khi phát lại. | Đợt đầu dùng mã lỗi do adapter trả, chỉ chuyển bước soạn văn bản khai báo đích trước. Dừng khi đã phát đầu ra hoặc gặp công cụ. |
| Gửi toàn bộ lịch sử sang model khác | Có thể gửi cả thông tin không cần thiết, làm tăng chi phí và thay đổi phạm vi dữ liệu được chia sẻ. | Đợt thử dùng đầu vào tổng hợp. Khi triển khai từng workflow, duyệt phạm vi dữ liệu cho cả hai provider. Chuyển đúng prompt của bước, kèm kết quả bước trước theo hợp đồng sẵn có. |
| Tự chạy lại toàn workflow khi bị gián đoạn | Không thể phân biệt chưa thực hiện với đã thực hiện nhưng mất phản hồi. | Mỗi bước đã xong có bằng chứng. Hành động có trạng thái không rõ cần đối chiếu trong hệ thống đích trước khi tiếp tục. |
| Dùng Graphify trước mọi lần đọc mã | Phép đo nội bộ ngày 19/11 tăng 61 token đầu vào ở một ca. Chỉ mục cũ có thể dẫn tới sửa nhầm vị trí. | So sánh theo từng loại việc và revision. Bật Graphify chọn lọc khi cần dò quan hệ nhiều tệp, xem file và test làm căn cứ cuối. |
| Từ chối mọi bản vá vượt 50 hoặc 100 dòng | Dòng mã chỉ là dấu hiệu. Có tác vụ cần thêm test hoặc sửa nhiều điểm để giữ hành vi nhất quán. | Dùng cảnh báo theo phạm vi của từng việc. Phản biện dựa vào yêu cầu, tệp được sửa, test, diff và lý do phát sinh. |

## Quy trình thực hiện

1. Ghi mục tiêu, kết quả cần bàn giao, những gì được phép làm và tiêu chí nghiệm thu. Ghi thành phần hiện có để tránh xây hai cơ chế cùng chức năng.
2. Lưu đối chứng trên cùng phiên bản mã. Dùng dữ liệu tổng hợp và tái hiện lỗi bằng adapter giả. Kiểm từng đầu vào, đường chạy, số lần gọi, sự kiện, kết quả và ghi lịch sử.
3. Chốt từng thay đổi trên nhánh riêng. Dùng vai phản biện xem trường hợp bất lợi trước khi sửa. Phần thực hiện phải giải thích bằng mã và bằng ca kiểm thử.
4. Kiểm thử hồi quy qua điểm vào thật của workflow, qua luồng không bật tính năng và qua các ca hủy. Đọc lại diff và đối chiếu với ma trận nghiệm thu.
5. Sau khi mã qua kiểm tra, chạy thử với một workflow có dữ liệu tổng hợp và hai tuyến AI đã được duyệt. Đo provider thực gọi, độ trễ, số yêu cầu, token có bằng chứng và chất lượng đầu ra.
6. Mở theo từng workflow sau khi đạt tiêu chí. Đảo lại bằng bỏ khai báo model dự phòng hoặc thay bản mã bằng baseline đã kiểm chứng. Khi mở rộng sang thao tác có tác động, kiểm riêng quyền và khả năng đối chiếu kết quả thực hiện.

## Các đợt triển khai

### 1. Chuyển nguồn cho vòng soạn văn bản

- Bật theo từng bước trong workflow tuần tự có `supplied_data_only: true` và `execution_guard.enabled: true`. Người cấu hình chỉ định `author_fallback: {provider: ..., model: ...}` bên trong bước soạn. Provider phải là tuyến API có trong Javis và khác nguồn chính tại thời điểm chạy.
- Chuyển tối đa một lần mỗi lượt workflow khi adapter trả lỗi có mã 429 hoặc 503, trước khi bước phát nội dung hoặc gọi công cụ. Đích dự phòng được cấp cùng prompt và cùng chế độ chỉ xử lý văn bản. Tôn trọng thời gian tổng, giới hạn bước model và số token provider đã báo.
- Bước trước chạy đúng một lần. Bước sau chỉ chạy nếu bước đang lỗi tạo được kết quả hợp lệ và đạt bước kiểm chứng hiện hữu. Giữ nguyên quy tắc định tuyến của người kiểm chứng.
- Giới hạn của đợt này là chuyển trong tiến trình đang chạy. Tiếp tục sau khi dịch vụ khởi động lại và xác nhận hành động có tác động thuộc đợt sau.

### 2. Khôi phục sau gián đoạn và bảo vệ hành động

- Dùng cơ chế checkpoint của workflow đồ thị. Lưu revision, mã bước, trạng thái, đầu ra đã kiểm và mã hành động ổn định. Chỉ phục hồi khi revision và dữ liệu khớp.
- Với một hành động có tác động, ghi ý định trước khi gọi. Nếu kết quả chưa rõ, đối chiếu hệ thống đích bằng khóa idempotency hoặc mã giao dịch. Khóa theo lượt khi nhận hai yêu cầu khôi phục đồng thời. Nếu không có bằng chứng đủ, dừng ở trạng thái chờ xác minh.
- Dùng fixture giả cho gửi tin, sửa tệp và ghi dữ liệu. Mỗi hành động được phép thực thi tối đa một lần khi gặp lỗi mạng, mất phản hồi hoặc tiến trình khởi động lại.

### 3. Đo hiệu quả Graphify và kiểm soát phạm vi bản vá

- Chạy đối chứng cùng revision, model, ngân sách và tiêu chí đúng. Ghép cặp các tác vụ tìm một điểm mã, dò phụ thuộc nhiều tệp và sửa lỗi thực tế. Ghi token đầu vào, cache, đầu ra, thời gian, số lần đọc tệp và kết quả test. Có thể mở rộng tới 50 tác vụ như tài liệu đề xuất khi bộ đo đã ổn định.
- Báo riêng kết quả theo loại tác vụ và số mẫu. Bật Graphify ở nhóm có lợi ích đo được mà chất lượng giữ nguyên. Nếu revision chỉ mục không khớp, đọc mã nguồn và chỉ mục lại khi cần.
- Cho bước rà kiểm diff và phạm vi tệp. Số dòng vượt mức dự kiến yêu cầu nêu lý do. Chặn khi bản vá vượt phạm vi đã chốt hoặc thiếu kiểm thử bắt buộc cho thay đổi đó.

### 4. Chạy tích hợp và theo dõi

- Đo lỗi phục hồi thành công, hành động lặp, độ trễ, số lần gọi, token và lỗi chất lượng. Ghi riêng các lần provider thiếu số usage. Tỷ lệ tiết kiệm nêu trong tài liệu là giả thuyết để đo.
- Chạy thử dữ liệu tổng hợp trước dữ liệu thật. Giữ một cấu hình có thể tắt theo từng workflow. Kiểm lại sau khi đổi phiên bản, adapter hoặc model.

## Ma trận kiểm thử

| Tình huống | Kết quả bắt buộc | Đợt |
|---|---|---|
| 503 ở bước giữa | Giữ kết quả đã xong, đích dự phòng chạy đúng một lần, bước sau nhận bản cuối | 1 |
| 429 hoặc lỗi đã qua retry ở adapter | Dựa vào mã có cấu trúc, chỉ thêm một lần chuyển nguồn | 1 |
| 400/401/403, thiếu mã hoặc đã phát đầu ra | Trả lỗi của bước, không gọi đích dự phòng | 1 |
| Bước khai báo công cụ, hoặc engine phát sự kiện gọi công cụ | Từ chối trước khi chạy hoặc dừng ngay ở rào thực thi | 1 |
| Đích dự phòng trả lỗi hoặc cấu hình trỏ cùng nguồn chính | Kết thúc có lý do, không chuyển vòng | 1 |
| Vượt giới hạn lượt hoặc token | Dừng trước lời gọi tiếp theo | 1 |
| Không khai báo model dự phòng | Workflow giữ đường chạy đã có | 1 |
| Bản dự phòng không đạt hợp đồng hoặc kiểm chứng | Dừng theo rào kiểm chứng, bước sau chưa chạy | 1 |
| Hủy lúc chuyển | Đóng luồng engine, lịch sử không ghi thành công | 1 |
| Khởi động lại, đổi revision hoặc có hai yêu cầu khôi phục đồng thời | Giữ trạng thái hợp lệ hoặc dừng với lý do rõ | 2 |
| Hành động thành công nhưng mất phản hồi | Đối chiếu trạng thái, số thao tác thực tế không vượt một | 2 |
| Đồ thị hết hạn, tác vụ ngắn hoặc diff vượt phạm vi | Ưu tiên bằng chứng từ mã nguồn, ghi rõ lý do cảnh báo hoặc chặn | 3 |

## Bằng chứng thực hiện

Baseline tại commit `48dad3a` của nhánh Execution Guard trên fork của chủ. Nhánh thực nghiệm riêng `feat/workflow-provider-failover` trong `tmp/maos-pilot`. Máy đang chạy bản cài riêng, đợt này nghiệm thu trên bản sao và dữ liệu tổng hợp.

### Cấu hình thử một bước

Ví dụ dưới đây giả định agent `writer` chọn một provider khác Ollama Local. Cấu hình dành cho bản thử khi đã có engine và model tương thích.

```yaml
supplied_data_only: true
execution_guard:
  enabled: true
  max_model_stages: 2
  max_reported_tokens: 3000
contract_steps:
  - agent: writer
    task: "Summarize the synthetic input in one line: {{input}}"
    max_retries: 0
    author_fallback:
      provider: ollama-local
      model: deepseek-r1:1.5b
```

Buộc provider đưa mã lỗi có cấu trúc. Khi hết ngân sách lượt hoặc token đã báo, chặn model dự phòng trước khi mở luồng gọi. Lượt chuyển là một bước model bổ sung. Số lần HTTP mà adapter tự thử lại được đo riêng theo dữ liệu thực tế của provider. Sự kiện `step_fallback` ghi bước, mã lỗi và đích đi. Thành công cần có đầu ra đạt hợp đồng cùng trạng thái `done`.

### Cách chạy kiểm thử

Từ thư mục nhánh thử, dùng Python 3.12 của Javis:

```text
python tests/python/test_execution_guard.py
python tests/python/test_execution_guard_workflow.py -v
python tests/python/test_signin_loss_route.py
python tests/python/test_agent_model_da_nha.py
python tests/python/test_workflow_chat.py
python tests/python/test_limit_resume.py
python tools/release.py check
git diff --check
```

Kiểm thử qua `execute_workflow` dùng kho và SQLite tạm. Ca adapter Gemini/Ollama giả lập đầu vào ở ranh giới mạng và dùng adapter API của Javis. Kiểm tra luồng chính đóng trước khi đích dự phòng bắt đầu, quyền công cụ giữ nguyên, dữ liệu đầu vào giống nhau và số token provider báo được tính mà không đếm hai lần.

### Kết quả đợt đầu

- Commit cục bộ `b8caa78` trên `feat/workflow-provider-failover`. Diff, biên dịch cú pháp Python và kiểm định changelog đạt. Nhánh thử nghiệm sạch sau commit.
- 35 kiểm thử trọng tâm đạt, gồm 19 kiểm thử giới hạn và 16 kiểm thử qua điểm vào workflow. Ca 503 ở bước giữa giữ đúng đầu ra bước đầu, gọi đích dự phòng một lần, kiểm chứng bằng cấu hình reviewer cũ rồi bàn giao sang bước cuối. Ca hủy đóng luồng và ghi lịch sử lỗi. Ca đã phát text, đã trả final, gặp công cụ, gặp 400/401/403 hoặc vượt giới hạn đều dừng. Ca reviewer bác bản dự phòng chặn bước sau.
- Năm bộ hồi quy bổ sung đạt: mất đăng nhập, định tuyến model của agent, workflow chat, khôi phục hạn mức và mở trang nhóm. Ba lỗi kiểm thử tái hiện ở cả bản gốc `48dad3a` lẫn nhánh thử: giả định Antigravity chưa có engine nền trong `test_aux_fallback.py`, SQLite còn mở khi dọn tệp trên Windows trong `test_pin_survives_fallback.py`, và kỳ vọng trạng thái bước song song trong `test_team_auto_retry_0436.py`.
- Kiểm thử qua HTTP loopback thực, Gemini giả lập lỗi 503 và đích tương thích Ollama giả lập phản hồi SSE. Đích nhận đúng một yêu cầu `/v1/chat/completions`, không có trường công cụ. Javis ghi 12 token đầu vào và 1 token đầu ra một lần, trả `done` với kết quả `READY`.
- Với Ollama thật trên máy này, Javis đã chọn đúng `deepseek-r1:1.5b` sau lỗi 503 mô phỏng. Hai lượt dừng bởi `execution_guard:idle_timeout` ở 45,06 và 80,05 giây trước khi có câu trả lời dùng được. Ollama báo model dùng 0 byte VRAM trong lần kiểm tra. Gọi trực tiếp bản local với giới hạn 24 token trả phần suy nghĩ, hết độ dài trước khi trả lời. Kết quả hiện tại xác nhận chuyển được tuyến và dừng đúng thời gian, chưa đủ để chọn model này làm tuyến dự phòng thực tế.

**Quyết định phát hành:** giữ thay đổi ở nhánh thử nghiệm. Mốc trước khi đưa vào bản đang chạy là một ca canary có model dự phòng vượt kiểm tra đầu ra trong ngân sách thời gian đã thống nhất. Khôi phục xuyên lần khởi động, chống lặp hành động ghi và phép đo Graphify nhiều tác vụ là các mốc kiểm thử tiếp theo.

### Bắt đầu cập nhật bản cài trên máy

Theo chỉ đạo mới của chủ, áp dụng phần mã của commit `b8caa78` vào bản cài bằng kiểm thử mô phỏng. Đánh giá Ollama được hoãn. Chỉ áp dụng ba tệp runtime của bản vá. Thêm dấu nhận biết `workflow_author_failover` vào phản hồi `/health` cục bộ hoặc đã xác thực để xác minh đúng tiến trình sau khi nạp lại.

- Kiểm tra bản vá áp dụng và đảo ngược được. Biên dịch cú pháp cả ba tệp đạt. Chạy lại 35 ca trên mã bản cài trong môi trường trạng thái tạm và kiểm tra dấu nhận biết ở điểm vào `/health`; tất cả đạt.
- Sao lưu bản gốc, mã băm và bản vá tại `tmp/javis-workflow-failover-eoc31n3e`. Sau khi sửa, mã băm mới được ghi vào `manifest.json`. Dùng các bản sao trong `before/server` nếu cần hoàn tác đúng ba tệp.
- Bộ nạp đã khởi chạy, trạng thái ghi nhận là `waiting_for_turn`. Nó kiểm tra công việc đang chạy trước khi gọi trình khởi động Javis và ghi kết quả vào `activation.json` trong cùng thư mục. Chỉ trạng thái `activated` xác nhận tiến trình đã nạp bản vá.
- Tuyến dự phòng chạy theo khai báo ở từng bước xử lý văn bản. Phạm vi đợt này là mã hệ thống và dấu nhận biết khi nạp.


### Kiểm thử Ollama và xác nhận bản cài 0.607.0

Ngày 20/11/2026, tiến trình bản cài đã nạp commit chuyển nguồn `b1b69269` lúc 12:24. Kiểm tra trực tiếp `/health` trả `workflow_author_failover: true`.

Commit `f7afd4a0` bỏ mô tả công cụ khỏi lời nhắc API ở lượt chỉ xử lý văn bản. Kiểm tra định dạng bỏ qua dòng trắng đầu nhưng vẫn so khớp nguyên văn dòng nội dung đầu tiên, kể cả viết hoa. Phần bàn giao giữ nguyên nội dung model trả.

- 35 ca mô phỏng đạt trên mã bản cài. Năm bộ hồi quy về API, kiểm chứng chỉ xử lý văn bản, mất đăng nhập, định tuyến agent và workflow chat cũng đạt trên nhánh có cùng commit.
- Với Ollama thật và lỗi nguồn chính mô phỏng, cả ba ca đều chuyển đúng một lần và không gọi công cụ. Ca mã `AB-24` sau lỗi 503 hoàn tất sau 20,84 giây. Ca `READY` sau lỗi 503 và ca `17` sau lỗi 429 bị chặn vì dòng nội dung đầu tiên sai định dạng, lần lượt sau 16,88 và 19,89 giây.
- Cùng lời nhắc gốc về `READY`, usage đầu vào do Ollama báo giảm từ 261 xuống 16 token sau chỉnh sửa. Kết quả vẫn sai cách viết hoa. Giữ nguyên khai báo model dự phòng của các workflow đang dùng.
- Mã `f7afd4a0` đã tích hợp cục bộ. Lúc ghi nhận, trình nạp lại đang chờ lượt chat kết thúc. Xem [trạng thái nạp lại](../../tmp/maos-ollama-format-deploy/activation.json).
