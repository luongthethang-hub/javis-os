---
type: workflow
name: Phiên họp phân tích thị trường
slug: phien-hop-phan-tich-thi-truong
status: 'off'
group: Tài chính
description: Kiểm chứng hồ sơ dữ liệu, lấy ba nhận định độc lập và chốt biên bản nghiên cứu có phán quyết rủi ro.
supplied_data_only: true
steps: []
execution_guard:
  enabled: true
  wall_seconds: 1800
  idle_seconds: 240
  max_model_stages: 8
  max_tool_calls: 8
  max_reported_tokens: 100000
  max_output_chars: 140000
contract_steps:
  - id: intake
    agent: thu-ky-hoi-dong
    task: >-
      Chuẩn hoá yêu cầu và ghi lại hồ sơ, gồm mã, sàn, khung thời gian, mục đích,
      thời điểm đánh giá kèm múi giờ, thời hạn chấp nhận của dữ liệu, nguồn và thời điểm chụp,
      giá/nến, bối cảnh sự kiện và dữ liệu dòng tiền phù hợp. Nếu có yêu cầu định cỡ,
      giữ thông tin vốn, giới hạn rủi ro và đơn vị. Ghi rõ hồ sơ mô phỏng nếu có.
      Ghi THIẾU ở trường không có. Không bổ sung dữ kiện mới. Yêu cầu và dữ liệu: {{input}}
  - id: evidence
    agent: kiem-chung-du-lieu
    require_first_line: "DATA_GATE: PASS"
    task: >-
      Kiểm tra hồ sơ sau: {{steps.intake}}. Đối chiếu lại dữ kiện và nguồn với hồ sơ gốc: {{input}}.
      Trả dòng đầu chính xác DATA_GATE: PASS nếu hồ sơ đủ cho ba chuyên viên, dữ liệu thiết yếu
      có nguồn, đơn vị, thời điểm và còn hạn theo mốc đánh giá. Dữ liệu mô phỏng được chấp nhận
      cho phiên mô phỏng nếu gắn nhãn rõ. Nếu thiếu dữ liệu thiết yếu, nguồn, mốc thời gian,
      giới hạn độ mới hoặc có dữ liệu thiết yếu hết hạn hay mâu thuẫn thì dòng đầu phải là
      DATA_GATE: STOP. Ghi rõ mục thiếu hoặc quá hạn và cần bổ sung gì.
      Khi PASS, bàn giao chính các giá trị, nguồn, đơn vị và thời điểm đã kiểm để ba chuyên viên
      có đủ dữ kiện làm độc lập. Nêu trường nào chỉ do chủ cung cấp và chưa được xác minh bên ngoài.
  - id: technical
    agent: phan-tich-thi-truong-an-toan
    task: >-
      Đọc hồ sơ dùng chung: {{steps.evidence}}. Nộp nhận định kỹ thuật độc lập,
      gồm cấu trúc giá, điều kiện vô hiệu, nguồn và điểm thiếu. Không thêm dữ liệu ngoài hồ sơ.
  - id: macro
    agent: chuyen-vien-co-ban-vi-mo
    task: >-
      Đọc hồ sơ dùng chung: {{steps.evidence}}. Nộp nhận định vĩ mô độc lập,
      gồm tác động sự kiện, thời điểm và điều kiện vô hiệu, nguồn và điểm thiếu.
      Không thêm dữ liệu ngoài hồ sơ.
  - id: flow
    agent: chuyen-vien-dong-tien-tam-ly
    task: >-
      Đọc hồ sơ dùng chung: {{steps.evidence}}. Nộp nhận định dòng tiền độc lập.
      Dùng số liệu phù hợp với công cụ, nêu giới hạn của chỉ báo thay thế, nguồn và điều kiện vô hiệu.
      Không suy funding hay OI từ dữ liệu giao ngay, không thêm số ngoài hồ sơ.
  - id: research
    agent: truong-phong-nghien-cuu
    task: |
      Tổng hợp có phản biện. Giữ riêng từng luận điểm, điểm bất đồng, phản ví dụ và điều kiện vô hiệu.
      Nếu thiếu một nhận định, nêu rõ. Giữ nhãn mô phỏng và các điểm chưa xác minh. Không tự duyệt rủi ro.
      Hồ sơ đã kiểm: {{steps.evidence}}
      Nhận định kỹ thuật: {{steps.technical}}
      Nhận định vĩ mô: {{steps.macro}}
      Nhận định dòng tiền: {{steps.flow}}
  - id: risk
    agent: quan-tri-rui-ro
    task: |
      Đánh giá rủi ro nghiên cứu. Ghi một phán quyết DUYỆT / DUYỆT CÓ ĐIỀU KIỆN / CHẶN và lý do.
      Nếu có đề xuất định cỡ, chặn khi thiếu SL, thông số đơn vị hoặc giới hạn cần thiết.
      Không suy ra quy mô có thể giao dịch từ kết quả mô phỏng.
      Hồ sơ đã kiểm: {{steps.evidence}}
      Bản nghiên cứu: {{steps.research}}
  - id: conclusion
    agent: giam-doc-dau-tu
    task: |
      Bàn giao biên bản và chốt đúng một trạng thái nghiên cứu. Nếu rủi ro CHẶN, kết luận ĐỨNG NGOÀI.
      Với phiên mô phỏng, ghi rõ MÔ PHỎNG và chỉ dùng THEO DÕI hoặc ĐỨNG NGOÀI. Nếu thiếu bằng chứng
      thiết yếu thì không lập phiếu cho giao dịch. Ghi tóm tắt cả ba góc nhìn, bất đồng, phán quyết
      rủi ro, mốc đánh giá và dữ liệu còn thiếu.
      Hồ sơ đã kiểm: {{steps.evidence}}
      Bản nghiên cứu: {{steps.research}}
      Phán quyết rủi ro: {{steps.risk}}
updated: '2026-11-19'
---

Chạy thủ công với bộ dữ liệu đã chuẩn bị. Cửa kiểm chứng dừng phiên khi dữ liệu thiếu hoặc quá hạn.
Ba chuyên viên nhận cùng hồ sơ. Trưởng phòng Nghiên cứu nhận đủ ba nhận định ở bước tổng hợp.
Phiên chỉ dùng dữ liệu đầu vào, dành cho nghiên cứu và mô phỏng.
