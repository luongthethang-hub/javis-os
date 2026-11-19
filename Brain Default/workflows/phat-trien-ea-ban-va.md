---
type: workflow
name: Phát triển EA - bản vá và phản biện
slug: phat-trien-ea-ban-va
status: 'off'
group: Tài chính
description: Kiểm tra Task Card, soạn bản vá EA và phản biện; không chạy MT5 hoặc đặt lệnh.
supplied_data_only: true
steps: []
execution_guard:
  enabled: true
  wall_seconds: 1200
  idle_seconds: 240
  max_model_stages: 2
  max_tool_calls: 8
  max_reported_tokens: 60000
  max_output_chars: 100000
  required_input_fields: ["GOAL","ENV","CODE","EXPECTED","CONSTRAINTS","ACCEPTANCE"]
contract_steps:
  - id: "patch"
    agent: "ky-su-ea---claude"
    max_retries: 0
    task: "Task Card JSON: {{input}}. Soạn bản vá tối thiểu, đầy đủ ngữ cảnh cho đúng MQL4/MQL5, build và account type đã cung cấp. Không suy đoán broker limits hay thông số thiếu. Nếu thiếu dữ kiện ảnh hưởng đúng/sai, mở đầu BLOCKED_INPUT và nêu tối đa ba mục cần bổ sung. Bàn giao patch, hành vi trước/sau, rủi ro, hướng dẫn compile strict, regression cố định so LKG và schema log. Phiên này không có compiler/shell/MT5: không nói đã ghi file, compile hoặc test; không xuất lệnh giao dịch."
  - id: "review"
    agent: "phan-bien-cheo---chatgpt"
    max_retries: 0
    task: "Rà Task Card {{input}} và bản vá {{steps.patch}}. Nếu đầu vào bị chặn, giữ trạng thái CẦN THÔNG TIN. Kiểm tra đúng yêu cầu, đơn vị lot/point, margin, retcode, chống lệnh lặp, safety floor và edge case. Chỉ rõ phát hiện theo vị trí và cách kiểm chứng. Kết luận ĐẠT THIẾT KẾ / CHƯA ĐẠT / THIẾU BẰNG CHỨNG; chưa compile thì ghi THIẾU BẰNG CHỨNG TRIỂN KHAI. Không tự tuyên bố cross-model nếu không có metadata lượt thực tế. Đây là bản rà, không phải chấp thuận chạy tài khoản. Không thực hiện thao tác ra ngoài."
updated: '2026-11-19'
---

Đầu vào là JSON Task Card. Phạm vi chỉ soạn mã và rà bản vá. Compile, regression, shadow/demo là các cổng tiếp theo chỉ chạy khi chủ cung cấp môi trường tách biệt và yêu cầu. Trading research dùng workflow phien-hop-phan-tich-thi-truong, không đi qua luồng EA này.
