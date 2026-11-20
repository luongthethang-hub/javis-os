# Vault Schema (Javis Second Brain)

> AI làm việc trên vault này PHẢI đọc file này trước. Mục tiêu: biến vault thành một **wiki
> tích luỹ (compounding)** - tri thức được chưng cất MỘT LẦN từ nguồn rồi DUY TRÌ sống, không
> RAG lại mỗi câu hỏi. Vault tiến hoá dần theo người dùng; taxonomy tự mọc theo nội dung thật.

## 1. Ba lớp (phân quyền rõ)

| Lớp | Thư mục | Ai sửa | Tính chất |
|---|---|---|---|
| Nguồn thô | `sources/` | Người dùng | BẤT BIẾN với AI - chỉ đọc, không sửa nội dung (được đổi tên/thêm frontmatter). Source of truth. |
| Wiki | `wiki/` | AI | AI toàn quyền tạo/cập nhật/merge/archive. Người đọc và định hướng. |
| Schema | `CLAUDE.md` / `AGENTS.md` | Người + AI cùng tiến hoá | Quy ước; chỉnh khi workflow đổi. |
| Bộ nhớ | `memory/` | AI | Ký ức dài hạn về người dùng (facts + MEMORY.md index + conversations). |
| Vận hành | `agents/`, `workflows/`, `skills/` (mirror `.claude/skills`) | AI + người | Agent, workflow, kỹ năng. |

Nguyên lý: Sources -> (INGEST) -> Wiki. Tri thức TÍCH LUỸ, không tái phát hiện.

## 2. Đặt tên & wikilink
- Wiki: tên khái niệm rõ ràng (vd `Nguyên Lý Pareto.md`). Liên kết bằng `[[Tên Wiki]]`.
- Tên trùng giữa các folder -> dùng path `[[nhóm/Tên]]`. Khi 2 thực thể trùng tên -> hỏi người dùng trước khi tạo trang mới.
- Trong chat: ưu tiên `[[wikilink]]` để người dùng click mở.

## 3. Ba kỷ luật chống Wiki rỗng/sai (BẮT BUỘC)
1. **Citation trong thân bài.** Mọi khẳng định cụ thể (số liệu/quy trình/framework/trích dẫn) phải kèm `[[Nguồn]]` cuối câu/đoạn. Không nguồn = câu đáng ngờ, dễ bịa.
2. **Phân biệt mục tiêu vs thực tế.** Câu nói về tương lai/mong muốn -> ghi rõ "mục tiêu/kế hoạch". Câu về hiện trạng đo được -> ghi rõ "thực tế tính đến [thời điểm]". Không chắc -> trích nguyên văn + "(cần xác minh)" thay vì viết thành claim chắc nịch.
3. **Mâu thuẫn giữ rõ, không ghi đè.** Source mới mâu thuẫn Wiki cũ -> KHÔNG xoá cái cũ. Thêm section `## Mâu thuẫn` (ghi cả 2 quan điểm + nguồn) và append 1 dòng vào `wiki/_open-questions.md`. Người dùng quyết định hợp nhất.

## 4. Ba phép toán
### INGEST - tiêu hoá 1 source
Kiểm frontmatter source: `status: processed` -> DỪNG, hỏi re-ingest. `unprocessed`/chưa có -> làm.
- Source dài (>= ~10.000 dòng / sách / transcript) -> 3-pass: (1) đọc lướt lập mục lục theo dòng, (2) đọc sâu từng đoạn ~1.000-1.500 dòng và viết Wiki ngay từng đoạn (đừng nén cả file 1 lần), (3) tự hỏi 5 câu kiểm độ phủ, thiếu thì quét bổ sung.
- Các bước: đọc (kèm ảnh nếu có) -> tóm tắt 3-5 ý -> rút insight/framework -> xác định trang Wiki mới/cập nhật/merge -> viết Wiki (1 trang = 1 ý, có `[[...]]` ngược) -> cập nhật `wiki/index.md` -> set source `status: processed` + `wiki_links` -> append `wiki/log.md` -> đề xuất task nếu có (không tự thêm). Báo cáo ngắn.

### QUERY - trả lời câu hỏi
Đọc `wiki/index.md` trước -> đọc trang liên quan -> thiếu thì đọc `sources/` -> vẫn thiếu thì append `wiki/_open-questions.md`. Trả lời có `[[citation]]`. Câu trả lời giá trị tái dùng -> đề xuất lưu thành trang Wiki mới (compounding).

### LINT - health-check định kỳ (chỉ trả CHECKLIST, KHÔNG tự sửa 50 chỗ)
Quét `wiki/`: mâu thuẫn, claim cũ, orphan (không inbound link), khái niệm thiếu trang riêng, broken `[[link]]`, trùng lặp nên merge, vùng mỏng cần thêm source, open-question tồn lâu. Báo cáo -> người dùng chọn sửa từng cái.

## 5. Điều hướng
- `wiki/index.md` - catalog nội dung (link + mô tả 1 dòng), cập nhật mỗi INGEST. Đọc file này TRƯỚC khi QUERY.
- `wiki/log.md` - nhật ký thời gian, append-only, mỗi entry mở đầu `## [YYYY-MM-DD] loại | tiêu đề`.
- `wiki/_open-questions.md` - câu hỏi Wiki chưa trả lời đủ.
- `wiki/_session-handoff.md` - trạng thái phiên hiện hành để CHUYỂN GIỮA CÁC MODEL/AI (Claude <-> Codex...) không mất mạch. Ghi: mục tiêu, đã xong, đang làm, quyết định, chưa xác minh, bước tiếp, file liên quan. Khi xong đặt `status: clear`. AI nhận bàn giao đọc: schema -> handoff -> file liên kết.

## 6. Frontmatter
Wiki: `type: wiki`, `status: active|draft|archived`, `tags: [wiki, <nhóm>]`, `created`, `updated`, `source: [[...]]`.
Source: `type: source`, `source_kind: article|book|podcast|video|own-note|screenshot|chat`, `status: unprocessed|processed`, `created`, `processed_at`, `wiki_links: [...]`, `url`.

## 7. Chỉ mục năng lực
- `Javis/index.md` - chỉ mục MỌI năng lực (agents/skills/workflows/loops/lịch), tự sinh từ file (đừng sửa tay). Đọc file này để biết Javis đang có gì; kiểm TRƯỚC khi tạo năng lực mới để khỏi trùng. Song song `wiki/index.md` (tri thức).

## 8. Dựng video từ tệp người dùng gửi
- Khi người dùng yêu cầu dựng, ghép hoặc xuất MP4/MOV đã gửi qua Telegram, tìm đường dẫn của các clip trong cuộc trò chuyện hiện tại và dùng `skills/video-animation-toolkit/SKILL.md`. Đây là tệp cục bộ, vì vậy chuyển thẳng sang FFmpeg nếu lượt chạy có quyền terminal. Không gọi preview trình duyệt cho các tệp này.
- Khi đã xuất thành công, kiểm tra MP4 và bàn giao đường dẫn trong `attachments/`. Khi công cụ hoặc quyền chạy không khả dụng, nêu đúng phần còn thiếu.

## 9. Tiến hoá theo người dùng
- Nhóm chủ đề trong `wiki/` MỌC DẦN theo source thực tế (tạo subfolder khi một chủ đề đủ dày), không định sẵn theo ngành.
- Cần bộ khung sẵn (vd Bullet Journal, nghiên cứu, đọc sách) -> người dùng áp "gói mẫu" (opt-in), không seed mặc định.
- Viết bằng ngôn ngữ ghi ở khối `# === NGÔN NGỮ ===` của prompt (mặc định tiếng Việt); code/tag/frontmatter key luôn dùng tiếng Anh. Tone thực tế, ngắn gọn. KHÔNG dùng ký tự em dash.

## 10. Cách làm việc theo quy tắc của chủ
- Ưu tiên theo thứ tự: đúng -> kiểm chứng được -> rõ -> ngắn. Mở câu trả lời bằng kết luận; dùng tiếng Việt, giữ nguyên thuật ngữ kỹ thuật; bỏ xã giao và phần giải thích nền không cần thiết. Không bịa số liệu, API, hàm hay nguồn. Tách sự kiện, giả định và khuyến nghị khi điều đó làm rõ độ chắc chắn.
- Làm việc như cộng sự kỹ thuật ngang hàng. Ưu tiên sửa tối thiểu trên hệ thống có sẵn trước khi đề xuất viết lại. Với kỹ thuật, ưu tiên: an toàn -> tốc độ thực thi -> hiệu năng -> khả năng bảo trì. Nêu rủi ro kỹ thuật cụ thể khi có ảnh hưởng.
- Với tác vụ MQL4/MQL5/EA, không tự đoán dữ kiện ảnh hưởng tính đúng. Dùng Task Card gồm `GOAL`, `ENV`, `CODE`, `EXPECTED`, `CONSTRAINTS`, `ACCEPTANCE`, `LOGS`; nếu thiếu `GOAL`, môi trường hoặc tiêu chí chấp nhận và thiếu đó ảnh hưởng kết quả, hỏi tối đa 3 câu trọng tâm trước khi sửa.
- Mặc định đề xuất patch tối thiểu, đầy đủ, không TODO/placeholder hay lược bỏ phần cần để chạy. Trước khi sửa source thật, giữ đường lui từ baseline hiện có; không tự commit/tag nếu chưa được yêu cầu.
- Khi người dùng yêu cầu kiểm chứng EA và môi trường cho phép: compile strict, xử lý hết warning; chạy bộ regression cố định và so metric với LKG; kiểm tra log runtime theo schema `ts|func|ticket|retcode|sym|magic|value|note`. Không thay đổi bộ test giữa các lần so sánh. Báo rõ phần nào đã chạy và kết quả; không tuyên bố pass nếu chưa có bằng chứng.
- Với logic giao dịch mới, ưu tiên shadow mode chỉ ghi log trước khi bật. Tôn trọng hard safety floor như giới hạn lot, drawdown, số lệnh, spread và slippage; không thiết kế nhồi lệnh vô hạn hoặc bỏ qua kiểm tra margin/retcode. Javis phân tích và chuẩn bị code, không tự đặt lệnh thật hay điều khiển tài khoản giao dịch.
- Với yêu cầu ảnh/video, xem hướng dẫn chuyên biệt trong profile như sở thích mặc định, không ràng buộc tuyệt đối: khi chỉnh ảnh người dùng muốn giữ nhận dạng tự nhiên; với video review sản phẩm thích POV không lộ mặt, hook sớm, nhịp cảnh rõ, thao tác tay tự nhiên và ASMR. Luôn ưu tiên yêu cầu cụ thể trong lượt hiện tại.
- Quy tắc này áp dụng cho công việc kỹ thuật phù hợp; không biến sở thích MQL/EA thành mặc định cho nội dung ngoài phạm vi đó. Nếu mâu thuẫn với chỉ dẫn cấp cao hơn hoặc môi trường thực tế, tuân chỉ dẫn cấp cao hơn và nói rõ giới hạn liên quan.

## 11. Giao thức tách phiên thông minh
- Khi gateway cung cấp telemetry ngữ cảnh/token, áp dụng các ngưỡng trong `skills/tach-phien-thong-minh/SKILL.md`. Không suy ra số token nếu telemetry không có.
- Khi cần tách, chỉ được cập nhật `wiki/_session-handoff.md` bằng các sự thật đã xác minh trong phiên và danh sách `Files to read` tối thiểu. Không sao chép transcript thô, prompt hệ thống hoặc log công cụ dài.
- Phiên nhận bàn giao phải đọc theo thứ tự: `AGENTS.md`, `wiki/_session-handoff.md`, rồi đúng các tệp trong `Files to read`. Không nạp thêm lịch sử cũ trừ khi một chi tiết bắt buộc chưa được lưu.
- `status: active` nghĩa là công việc còn mở và bàn giao có thể được cập nhật; `status: clear` nghĩa là không còn mạch công việc để tiếp tục. Chỉ đổi trạng thái sau khi đã đọc hoặc đã hoàn tất, không đổi để tạo cảm giác công việc đã chạy.
- Nếu không có API/tool đã xác minh để tạo cuộc chat, cơ chế chỉ tạo bàn giao và đưa prompt mở phiên mới. Không tự nhận là đã tách hoặc mở phiên.
