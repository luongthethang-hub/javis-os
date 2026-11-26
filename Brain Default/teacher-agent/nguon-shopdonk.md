# Nguồn API giá rẻ ShopDonk (tra từ hội thoại L0-Javis 25/11/2026 22:48-23:00)

- Nhà cung cấp: ShopDonk (shopdonk.com/api), chuẩn OpenAI Compatible, đã nối vào Javis nhãn "ShopDonk", đặt làm dự phòng CUỐI sau các gói thuê bao.
- Giới hạn key: 120 yêu cầu/phút, 5 luồng đồng thời (dùng chung cho mọi tiến trình Javis). Key thực tế trả về 36 model, L0 chỉ cho dùng 6.
- 6 model L0 chọn + kết quả thử 5 vòng (E1, mẫu nhỏ, trung vị thời gian qua ShopDonk):
  | Model | Điểm | Thời gian | Cộng sự Javis | Vai phù hợp cho Teacher/Doctor |
  |---|---|---|---|---|
  | gpt-6-luna | 5/5 | 23,95 s | shopdonk-luna-analysis | Người soát khác hãng số 1 (phân tích có cấu trúc) |
  | gpt-5.6-sol | 5/5 | 23,47 s | shopdonk-sol-test | Viết ca kiểm thử, chấm golden test |
  | grok-4.7 | 5/5 | 41,38 s | shopdonk-grok-check | Người soát số 2: bắt mâu thuẫn (qua ShopDonk, không cần gói Grok riêng) |
  | deepseek-v4.1-flash | 5/5 | 26,07 s | shopdonk-deepseek-data | Tóm tắt log, đối chiếu số; KHÔNG viết code |
  | gemini-flash-3.8-high | 3/5 | 24,14 s | shopdonk-gemini-draft | Chỉ soạn nháp, luôn phải kiểm lại |
  | claude-sonnet-4-6 | 5/5 | 36,36 s | shopdonk-sonnet-review | Không gọi tool được; cùng hãng Claude nên KHÔNG tính là soát khác hãng |
- Báo cáo gốc: reports/model-benchmark-20261125/report.md và results.json.
- Lưu ý chi phí: API không trả số tiền; lượt thử dùng ~21.044 token vào, 2.142 token ra.

## Cảnh báo bảo mật (26/11 12:10)
Key ShopDonk nằm NGUYÊN VĂN trong memory/conversations/2026-11-25.md (dòng ~61), do L0 dán vào chat. Vault có git, nên key có thể đã vào lịch sử git. Đề xuất: L0 đổi key mới tại ShopDonk (A0), sau đó che dòng đó trong log, kiểm lịch sử git của vault.

## Luật dùng cho Teacher/Doctor (đề xuất, chờ L0 duyệt)
- Tối đa 2 luồng đồng thời (Javis giữ 3), dưới 30 yêu cầu/phút.
- Chỉ gửi dữ liệu S0-S1 (thiết kế, diff code đã lọc); không key, vault, brains, accounts.
- Soát khác hãng mặc định: Luna + Grok; Sol viết/chấm test; DeepSeek Flash tóm log.
- Ghi token mỗi lần gọi (V7); trần ngày do L0 đặt.
