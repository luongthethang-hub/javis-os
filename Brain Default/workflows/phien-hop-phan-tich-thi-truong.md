---
type: workflow
name: Phiên họp phân tích thị trường
slug: phien-hop-phan-tich-thi-truong
status: 'off'
group: Tài chính
description: Kiểm chứng dữ liệu, phân tích thị trường và bàn giao phán quyết rủi ro trong ba bước.
supplied_data_only: true
steps: []
execution_guard:
  enabled: true
  wall_seconds: 1800
  idle_seconds: 240
  max_model_stages: 3
  max_tool_calls: 8
  max_reported_tokens: 100000
  max_output_chars: 140000
contract_steps:
  - id: evidence
    agent: kiem-chung-du-lieu
    max_retries: 0
    require_first_line: 'DATA_GATE: PASS'
    task: |
      Chuẩn hóa hồ sơ gốc: {{input}}. Xác định mục đích, mã, sàn, khung thời gian,
      mốc đánh giá kèm múi giờ, giới hạn độ mới, dữ liệu thiết yếu, nguồn, đơn vị và thời điểm chụp.
      Dòng đầu phải là DATA_GATE: STOP nếu trường thiết yếu thiếu, quá hạn hoặc mâu thuẫn.
      Nếu đủ, ghi DATA_GATE: PASS ở dòng đầu và bàn giao dữ liệu đã đối chiếu, nguồn, đơn vị,
      thời điểm và giới hạn. Gắn nhãn mô phỏng khi phù hợp. Đánh dấu dữ liệu chủ cung cấp
      chưa được xác minh bên ngoài. Không bổ sung dữ liệu.
  - id: analysis
    agent: phan-tich-thi-truong-an-toan
    max_retries: 0
    task: |
      Đọc hồ sơ đã kiểm: {{prev}}. Nêu cấu trúc giá, kịch bản, điều kiện vô hiệu
      và điểm thiếu. Chỉ dùng bối cảnh sự kiện và dòng tiền có trong hồ sơ.
      Nếu cần chuyên viên vĩ mô, dòng tiền hoặc CIO, nêu vai trò và câu hỏi cần giải quyết.
      Bàn giao kèm dữ liệu đã kiểm, nguồn, mốc thời gian, nhãn mô phỏng và giới hạn của nguồn.
      Không lập phiếu lệnh.
  - id: risk
    agent: quan-tri-rui-ro
    max_retries: 0
    task: |
      Đối chiếu bản phân tích kèm dữ liệu đã kiểm {{prev}} với hồ sơ gốc {{input}}.
      Bàn giao mốc đánh giá, nhận định chính, điều kiện vô hiệu, dữ liệu còn thiếu,
      vai trò cần tham vấn nếu có và một phán quyết DUYỆT / DUYỆT CÓ ĐIỀU KIỆN / CHẶN kèm lý do.
      Nếu CHẶN hoặc còn thiếu bằng chứng thiết yếu, chốt ĐỨNG NGOÀI.
      Với mô phỏng, ghi rõ MÔ PHỎNG và chỉ dùng THEO DÕI hoặc ĐỨNG NGOÀI.
      Phán quyết dành cho nghiên cứu. Không lập phiếu lệnh hoặc suy quy mô có thể giao dịch.
updated: '2026-11-19'
---

Luồng thường lệ chạy thủ công với ba vai trò. Dữ liệu thiếu hoặc quá hạn dừng ở cửa kiểm chứng.
Điều phối mời chuyên viên hoặc CIO từ Team Phân tích Thị trường khi có câu hỏi cụ thể cần xử lý.
Luồng chỉ dùng dữ liệu đầu vào và bàn giao kết quả nghiên cứu.
