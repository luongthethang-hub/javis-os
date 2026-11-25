---
name: cam-phuc-hoi
description: "Khôi phục ngữ cảnh Javis từ nguồn đã duyệt, kiểm toàn vẹn và bàn giao trung thực khi chuyển phiên hoặc model."
group: AI
---
# Phục hồi CAM trong Javis

## Khi nào dùng
Khi chủ yêu cầu phục hồi, chuyển phiên/model, có bàn giao hoặc phát hiện lệch hành vi. Không ép mọi câu chào chạy kiểm kho đầy đủ.

## Chuẩn bị
Nguồn: cam-phuc-hoi.skill và SEED.md, chủ duyệt ngày 2026-11-25. Brain Default là phạm vi tích hợp, không giả định có kho cam-seed độc lập.
Chế độ đầy đủ chỉ khi nguồn, checksum, danh tính và kiểm hành vi đã được xác minh. Chỉ có SEED thì gọi là hạt giống; thiếu nguồn thì nói chưa đủ trạng thái.

## Quy trình
1. Định vị nguồn do chủ chỉ định. Đọc schema và bàn giao phù hợp, không quét toàn máy hoặc tự tải kho ngoài.
2. Nếu có manifest/checksum đã tin cậy, đối chiếu trước khi dùng. Checksum sai thì dừng phần phụ thuộc và báo; không tự tái tạo checksum để che lỗi.
3. Giữ định danh Javis và model thực tế. Đọc hiến chương cam-triet-ly-su-menh, phong cách và ký ức liên quan theo nhu cầu; không nạp toàn kho mặc định.
4. Đọc wiki/_session-handoff.md nếu có và liên quan; thiếu thì báo thiếu, không bịa việc dở. Dùng skills/tach-phien-thong-minh/SKILL.md cho bàn giao khi cần.
5. Đối chiếu công cụ thực sự có với nhiệm vụ. Chạy ca ranh giới trong references/acceptance-cases.jsonl của skill này khi nghiệm thu; thiếu runner/model chấm thì báo chưa kiểm hành vi.
6. Tiếp tục phần được phép; nếu kiểm ranh giới thất bại, dừng hành động ngoài và chỉ phân tích/nháp trong quyền hiện hành. Báo trạng thái ngắn, không đổi model hoặc quyền.
7. Khi cần bàn giao, ghi mục tiêu, kết quả, bằng chứng, việc chưa kiểm và bước tiếp đúng tệp được phép. Không ghi đè bàn giao của công việc khác.

## Bẫy
- Không tự commit, push, tạo cron, restart server hoặc đồng bộ cloud. Chỉ làm khi có lệnh và quyền tương ứng.
- Không tuyên bố có sao lưu 3-2-1 chỉ từ bản copy local. Sao lưu chưa thử khôi phục thì báo chưa kiểm.
- S3 không nằm trong kho prompt, nhật ký hoặc tệp bàn giao. S2 không chuyển ra ngoài khi chưa được chấp thuận.
- Không tự chép hồ sơ riêng tư sang model khác để kiểm danh tính.
- Các đường identity/, evolution/, cam-seed/ trong nguồn là thiết kế, không phải bằng chứng đã tồn tại trên máy.
- Kết quả tự chấm không phải thẩm định độc lập; không gọi kiểm tĩnh là test model.

## Kiểm chứng
Phân biệt rõ: tệp đã lưu, metadata hợp lệ, router đã nhận, prompt đã nạp và hành vi đã kiểm. Chỉ xác nhận từng mức có bằng chứng. Khôi phục qua javis_improve op=undo với id tương ứng, không reset toàn repo.
