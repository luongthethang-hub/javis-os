# Quyết định của L0 - 26/11/2026 (giờ VN, UTC+7)

Nguồn: tin L0 trong dự án CLAUDE - Darklord, sau bàn giao ban-giao-darklord-20261126.md.
Nguyên văn L0:
- 16:59:07 "Duỵet"
- 16:59:37 "router bật"
- 17:00:34 "Cho phép tạo file quyet-dinh-L0-20261126.md trong teacher-agent"

Cách hiểu (do phiên điều phối Darklord diễn giải từ 2 tin đầu; L0 cho phép ghi file, chưa xác nhận lại từng mục):
1. Từ chối đề xuất prop_5e5e1f1e (theo khuyến nghị của Doctor Agent).
2. V7: GIỮ relay/router trả phí cho Claude trong CAM, KHÔNG chuyển sang CLI gói Pro/Max.
3. BẬT Auto memory cho Doctor Agent.

Ghi chú cho Doctor Agent:
- File này chỉ ghi lại quyết định. Chưa có thao tác nào được chạy trên CAM OS (chưa từ chối prop trong hệ, chưa đổi cấu hình relay, chưa bật Auto memory).
- Việc từ chối prop_5e5e1f1e và mọi thay đổi trong CAM OS do Doctor Agent thực hiện theo cơ chế duyệt chuẩn (cam_approve.py, cổng bàn phím của L0).
- Bật Auto memory là cài đặt của dự án Doctor Agent trên claude.ai, L0 tự bật.
- Nếu Doctor thấy cách hiểu mục 2 hoặc 3 không khớp ý L0 thì hỏi lại L0 trước khi làm.
- Giữ relay trả phí nên bộ đếm chi phí V7 càng cần làm sớm.

## Bổ sung 18:31 - Tái cấu trúc lõi CAM OS (ghi bởi thread Darklord "Tái cấu trúc lõi CAM OS")
Nguyên văn L0 lúc 18:31:20 (tin cmsg_01VAn1PaU8q3byskUNZrJB33HKsZ9cdFdKrDVDtkidcjMX trong dự án CLAUDE - Darklord):
- "Nhiệm vụ là Tái cấu trúc lõi hạt nhân của CAM OS ở mức quyền thực thi cao nhất, được phép đọc ghi chỉnh sửa toàn bộ CAM OS"

Hiệu lực:
4. Thread Darklord "Tái cấu trúc lõi CAM OS" được đọc, ghi, sửa toàn bộ CAM OS (D:\AI AGENT\council-agent-manager). Quyết định này thay luật cũ "chỉ Doctor Agent sửa code CAM OS" trong phạm vi việc tái cấu trúc.
5. Điều kiện kèm theo (luật L0 sẵn có): trình L0 bản thiết kế trước khi sửa lớn; nhánh git riêng, commit nhỏ; test cô lập, sao lưu dữ liệu trước; kiểm chéo khác hãng nếu gọi được; ô V1-V5 đỏ thì lùi ngay; chỉ merge vào master khi L0 nghiệm thu; không in key.

Ghi chú cho Doctor Agent (QUAN TRỌNG, chống sửa chồng):
- Từ 18:35 thread tái cấu trúc giữ khóa ghi repo CAM OS. Sổ Cái: khoa-ghi:cam-os = dang-giu.
- Doctor KHÔNG sửa code/dữ liệu CAM OS, không commit, không chạy cam_approve apply, cho tới khi khoa-ghi:cam-os chuyển "da-tra". Đọc và đo chỉ đọc vẫn được.
- Gói G1-G9 nay do thread tái cấu trúc gộp vào kế hoạch; G2 (từ chối prop_5e5e1f1e) vẫn cần L0 gõ mã ở cổng bàn phím.
- Kiểm tra trạng thái: cd "D:\AI AGENT\so-cai" ; python -m so_cai lien-ket khoa-ghi:cam-os
