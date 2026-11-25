# Javis Index (tầng vận hành)

> Tự sinh từ file - ĐỪNG sửa tay. Chỉ mục mọi năng lực của Javis trong brain này để bất kỳ AI/engine đọc 1 chỗ là hiểu Javis làm được gì. Song song `wiki/index.md` (tri thức).

**Tổng quan:** 9 agents · 25 skills · 5 workflows (0 bật) · 0 loops (0 bật) · 32 plugins (30 chạy)

## Agents
- **Antigravity** (`antigravity`) - Tactical Muscle / Blue Team: Viết & debug code, quét repo lớn, compile/test MQL5 & Python, chạy shell, dựng media OpenMotion; Kế vị Chủ tọa số 1 khi L1 treo quá 5s. · model gemini-3.8-flash-high · skills: data-query, openmotion · tags: HoiDong, BlueTeam, TacticalMuscle, PeerDirect
- **ChatGPT / Codex** (`codex`) - Kỹ sư Tự động hóa & Kiểm thử: Viết bộ test unit/integration, script tự động hóa pipeline, mô phỏng thuật toán và phối hợp Red Team. · model gpt-6.2-sol · tags: HoiDong, RedTeam, Automation, PeerDirect
- **Javis Core** (`javis-core`) - Trợ lý hệ thống nhận báo cáo và hỗ trợ công việc trong brain này. · skills: cam-triet-ly-su-menh, cam-cot-song, cam-tien-hoa, cam-tam-hon, cam-phuc-hoi · tags: AI, Vận hành
- **DeepSeek - Kiểm tra số liệu nhỏ** (`shopdonk-deepseek-data`) - Kiểm tra phép tính và tổng hợp dữ liệu có phạm vi rõ. · model deepseek-v4.1-flash · tags: AI, ShopDonk, Thử nghiệm
- **Gemini - Bản nháp cần kiểm tra** (`shopdonk-gemini-draft`) - Soạn bản nháp văn bản đơn giản để người dùng hoặc model khác kiểm tra. · model gemini-flash-3.8-high · tags: AI, ShopDonk, Thử nghiệm
- **Grok - Kiểm tra tính nhất quán** (`shopdonk-grok-check`) - Kiểm tra mâu thuẫn và dữ kiện thiếu trong văn bản ngắn. · model grok-4.7 · tags: AI, ShopDonk, Thử nghiệm
- **Luna - Phân tích có cấu trúc** (`shopdonk-luna-analysis`) - Phân tích yêu cầu nhỏ và tạo kết quả có cấu trúc, có căn cứ. · model gpt-6-luna · tags: AI, ShopDonk, Thử nghiệm
- **Sol - Kiểm thử tác vụ ngắn** (`shopdonk-sol-test`) - Thiết kế ca kiểm thử và kiểm tra đoạn mã, dữ liệu nhỏ. · model gpt-5.6-sol · tags: AI, ShopDonk, Thử nghiệm
- **Sonnet - Rà soát logic** (`shopdonk-sonnet-review`) - Rà soát logic và đặc tả của đoạn mã ngắn do người dùng cung cấp. · model claude-sonnet-4-6 · tags: AI, ShopDonk, Thử nghiệm

## Skills
### AI
- **cam-cot-song** (`cam-cot-song`) - Thực thi toàn trình theo ý định, tiêu chí nghiệm thu, điểm chạm chủ, ngân sách và giới hạn tự chủ.
- **cam-phuc-hoi** (`cam-phuc-hoi`) - Khôi phục ngữ cảnh Javis từ nguồn đã duyệt, kiểm toàn vẹn và bàn giao trung thực khi chuyển phiên hoặc model.
- **cam-tam-hon** (`cam-tam-hon`) - Giữ giọng Javis nhất quán, thấu cảm đúng ngữ cảnh, nhận lỗi và hỗ trợ không thao túng hoặc giả cảm xúc người.
- **cam-tien-hoa** (`cam-tien-hoa`) - Chuyển bài học thành đề xuất CUP có bằng chứng, kiểm hồi quy, phê duyệt và đường hoàn tác.
- **cam-triet-ly-su-menh** (`cam-triet-ly-su-menh`) - Hiến chương CAM cho Javis: nhận ý định, làm trọn, bảo vệ sự thật, an toàn và tài sản lâu dài của chủ.
- **Chuyển việc sang app desktop** (`chuyen-viec-sang-app-desktop`) - Đẩy việc bị chặn sang ChatGPT Desktop hoặc Claude Desktop, gửi prompt và đọc trả lời tự động.
- **Điều phối Đội nhóm & Token** (`dieu-phoi-doi-nhom`) - Phân rã việc theo TaskPacket, định tuyến agent theo thang A0-A4, Cascade tối đa 2 lỗi và nghiệm thu E1 trong Liên minh AI.
- **Ingest Source** (`ingest-source`) - Tiêu hoá một source thô vào Second Brain, chưng cất thành tri thức wiki tích luỹ.
- **Huấn luyện Agent Chuyên sâu (v1)** (`intensive-agent-training`) - Quy trình huấn luyện Agent đa bước theo RUULEE v6.0: TaskPacket handoff, thang tự chủ A0-A4, trí nhớ 3 tầng và kiểm toán trace_id.
- **Huấn luyện AI Chuyên sâu (v2)** (`intensive-ai-training`) - Quy trình 5 pha huấn luyện AI theo RUULEE v6.0: nén TaskPacket, định tuyến L1/L2 Cascade tối đa 2 lỗi, Red/Blue FMEA và Shadow Eval.
- **Javis Builder** (`javis-builder`) - Tạo hoặc sửa năng lực của Javis: agent, skill, workflow, loop, plugin. Kèm mẫu file chuẩn và luật chống trùng.
- **Lint Wiki** (`lint-wiki`) - Rà soát sức khoẻ wiki của Second Brain, trả về danh sách vấn đề. Không tự sửa hàng loạt.
- **Notes** (`notes`) - Lưu tin nhắn hiện tại nguyên văn vào sources/ (kèm ảnh), tự chưng cất lên wiki nếu note đáng.
- **Query Wiki** (`query-wiki`) - Khai thác tri thức trong Second Brain: tổng hợp, so sánh, giả thuyết. Trả lời có trích dẫn.
- **RUULEE Operational Charter v6.0** (`ruulee-operational-charter`) - Hiến chương lõi L0-L1-L2 RUULEE v6.0: thang tự chủ A0-A4, TaskPacket, Red/Blue QA, FMEA, Shadow Test, trace_id và CUP.
- **Tách phiên thông minh** (`tach-phien-thong-minh`) - Nén ngữ cảnh có kiểm chứng và tạo bàn giao để tiếp tục trong phiên mới.
- **ui-ux-thuc-chung** (`ui-ux-thuc-chung`) - Thiết kế và rà soát UI UX theo hệ thống có sẵn, accessibility, trạng thái tương tác và kiểm chứng responsive.
- **Vận hành AI Company ổn định** (`van-hanh-ai-company-on-dinh`) - Điều phối AI Company chịu lỗi nhiều tầng bằng checkpoint, phân loại lỗi, chuyển nguồn có giới hạn và khôi phục an toàn.
### Marketing
- **HTML sang Webcake** (`html-to-webcake`) - Chuyển trang HTML thành file .pke mở được trong trình dựng Webcake, giữ đúng màu, cỡ chữ, ảnh và bố cục của bản gốc.
### Năng suất
- **data-query** (`data-query`) - Truy vấn dữ liệu lớn (JSON, CSV, JSONL) bằng SQLite ảo chỉ đọc, chống tràn context cho log backtest MQL5 và dữ liệu tick.
- **Tiết kiệm token Terminal (RTK)** (`token-saver-rtk`) - Dùng RTK để rút gọn đầu ra lệnh Terminal trong tác vụ kỹ thuật; giữ đủ chi tiết khi cần xác minh.
### Nội dung
- **OpenMotion** (`openmotion`) - Tái tạo và dựng video bằng mã: phân rã video mẫu thành Motion.md, áp Brand Kit, xử lý âm thanh Voice-First và xuất MP4.
- **Hoạt hình & Video** (`video-animation-toolkit`) - Phân tích video tham chiếu MP4/MOV, dựng và xuất video bằng FFmpeg, lập quy trình hoạt hình 2D/3D và motion graphics.
### Security
- **Security Audit** (`security-audit`) - Rà soát bảo mật mã nguồn, API, dịch vụ: tìm lỗ hổng có bằng chứng, kiểm chứng độc lập từng lỗi, báo cáo kèm cách sửa. Từ Cloudflare.
### Tài chính
- **Họp hội đồng đầu tư** (`hop-hoi-dong-dau-tu`) - Chạy một phiên họp phân tích thị trường đủ 6 pha, ra phiếu lệnh và biên bản.

## Workflows
### AI
- **Red/Blue Team Review (RUULEE v6.0)** (`red-blue-team-review`) - off · 3 bước [antigravity -> grok -> claude] · Rà soát đối kháng 3 bước (Blue Team -> Red Team 6 vector -> Safety Auditor) trả phán quyết DEBATE_VERDICT chuẩn cho plugin debate-engine.
### Bán hàng
- **Chăm sóc Khách hàng Zalo & Inbox Đa kênh** (`cham-soc-khach-hang-zalo-inbox`) - off · 3 bước [javis-core -> dola -> claude] · Kiểm tra sức khỏe kênh Messenger/Zalo, phân loại hội thoại Lạnh/Ấm/Nóng và soạn phản hồi chuẩn giọng thương hiệu trình duyệt.
### Marketing
- **Chăm sóc & Phát triển Fanpage Facebook** (`cham-soc-fanpage-facebook`) - off · 3 bước [deepseek -> dola -> perplexity] · Đo hiệu suất Fanpage/Meta Ads, soạn bài 4-1-1 đúng thương hiệu và kiểm duyệt chính sách Meta trước khi trình chủ duyệt.
### Nội dung
- **Xây dựng Thương hiệu Cá nhân Đa nền tảng** (`xay-dung-thuong-hieu-ca-nhan`) - off · 3 bước [grok -> antigravity -> perplexity] · Chuyển hóa 1 ý tưởng gốc thành gói nội dung đồng bộ 4 kênh (Facebook, Shorts/TikTok, YouTube, Zalo) kèm kiểm chứng sự thật.
- **Xây kênh TikTok & YouTube Tự động** (`xay-kenh-tiktok-youtube`) - off · 3 bước [grok -> codex -> antigravity] · Nghiên cứu hook 3 giây, viết kịch bản Voice-First, kiểm duyệt chính sách và đóng gói đặc tả Motion.md sẵn sàng dựng MP4.

## Loops
_(chưa có)_

## Plugins (tool/hook native cho mọi engine)
- **Ủy thác Antigravity** (`antigravity-delegate`) - bundled/chạy · tools: javis_antigravity_delegate · Ủy thác tác vụ chiến lược nội dung, kịch bản TikTok/YouTube, kiểm toán Fanpage/Ads và tự động hóa sang Antigravity (Google AI Pro - 0đ phí API).
- **Thời gian & ngày** (`datetime-vn`) - bundled/chạy · tools: javis_now, javis_date_add · Xem ngày giờ hiện tại theo múi giờ chọn ở Cài đặt và tính ngày tương đối (mai, mốt, N ngày nữa, tuần trước). Thuần stdlib, chỉ đọc, không cần mạng.
- **Điều khiển app trên máy** (`desktop-apps`) - bundled/chạy · tools: javis_app_list, javis_app_open, javis_app_close · Mở, đóng và liệt kê ứng dụng trên CHÍNH MÁY đang chạy Javis (Windows, macOS, Linux có màn hình) theo lời người dùng, ví dụ "mở Chrome", "tắt Excel", "đang mở app nào". Tự chặn và nói rõ khi Javis chạy trong Docker trên máy chủ, vì khi đó máy chạy Javis không phải máy của người dùng.
- **Tạo và xem ảnh (ChatGPT)** (`image-chatgpt`) - bundled/chạy · tools: javis_generate_image, javis_describe_image · Tạo ảnh từ mô tả bằng GÓI ChatGPT đang đăng nhập (OAuth) - không cần OpenAI API key. Dùng Codex Responses API + tool image_generation (gpt-image-2). Ảnh lưu vào attachments/ của vault để nhúng thẳng vào chat. Kèm tool XEM ảnh, để ChatGPT nhìn ảnh trong brain rồi tả lại bằng chữ, để cả engine không tự xem được ảnh (OpenRouter, Gemini API...) cũng biết trong ảnh có gì. Cần đã kết nối ChatGPT ở trang Model.
- **Trả lời khách từ Hội thoại** (`inbox-reply`) - bundled/chạy · tools: inbox_find, inbox_reply · Tìm hội thoại khách trên trang Hội thoại và gửi tin trả lời ngay vào đó, đúng kênh của cuộc chat (Messenger, Instagram, Telegram, Zalo...), như chủ gõ tay ở Hộp thư.
- **Đấu thêm MCP** (`javis-connect`) - bundled/chạy · tools: javis_add_mcp · Đấu một MCP server vào kho Kết nối của Javis ngay từ chat, để nó HIỆN ra trang Kết nối như mọi tài khoản khác. Trước tool này Javis chỉ còn đường `claude mcp add` - thứ rơi vào config riêng của Claude Code, không bộ não nào khác thấy và người dùng cũng không thấy trên trang Kết nối.
- **Tên và phong cách của Javis Core** (`javis-core-name`) - bundled/chạy · tools: javis_core_name · Cho người dùng đặt tên riêng và phong cách nói chuyện cho Javis Core của brain này, ngay trong chat. Tên hiện trên trang Cộng sự. Chỉ phiên của chủ thấy tool này.
- **GitHub trong khung chat** (`javis-github`) - bundled/chạy · tools: javis_github · Xem trạng thái repo GitHub của khung chat (nhánh, PR, CI, merge), xếp việc kế tiếp để Javis tự làm khi PR hiện tại đã merge xong, và review chéo PR khi người dùng yêu cầu.
- **Mục tiêu (Hệ thống cộng hưởng)** (`javis-goal`) - bundled/chạy · tools: javis_goal, javis_submit_deliverable · Cho bộ não tự lập một mục tiêu bền khi người dùng giao việc cần theo đuổi sau lượt chat, hoặc cập nhật mục tiêu đang mở khi người dùng bổ sung ý. Host kiểm đề xuất theo SMART và lưu có revision. Chỉ hiện ở brain đã bật Hệ thống cộng hưởng.
- **Tự cải tiến theo yêu cầu** (`javis-improve`) - bundled/chạy · tools: javis_improve · Khi chủ yêu cầu, Javis hay một trợ lý tự sửa chính nó và brain (trợ lý, skill, workflow, vòng lặp, bộ nhớ) có sao lưu và hoàn tác, sửa mã nguồn Javis qua GitHub. Không tự cập nhật, lên bản mới do chủ bấm ở trang Cập nhật. Chỉ phiên của chủ thấy tool này.
- **Việc chạy nền** (`javis-job`) - bundled/chạy · tools: javis_job · Theo dõi lệnh chạy ngầm engine bỏ lại (render, build, tải về). Dặn trước "xong thì làm tiếp gì", xem việc đang chạy, dừng một việc. Xong là Javis tự báo về đúng khung chat và tự làm tiếp.
- **Cookies** (`javis-login`) - bundled/chạy · tools: javis_login · Mở trang web cần đăng nhập bằng phiên chủ đã cất ở trang Cookies, đọc hoặc bấm và điền form trong trình duyệt. Không bao giờ trả cookie.
- **Trí nhớ qua chat** (`javis-memory`) - bundled/chạy · tools: javis_memory · Cho Javis xem, sửa, quên ghi nhớ của brain, bật tắt việc lưu ghi nhớ mới, sửa hồ sơ chung và thu hồi bài học của trợ lý khi người dùng nhắn. Thay cho các danh sách trí nhớ và bài học từng nằm ở cột Cài đặt. Chỉ phiên của chủ thấy tool này.
- **Việc của tôi và thói quen** (`javis-mine`) - bundled/chạy · tools: javis_mytask · Thêm, sửa, xoá việc, lịch hẹn và thói quen trong tab Của tôi trên trang Nhiệm vụ (đổi việc lặp thành lịch hẹn, đổi giờ, đổi lặp, bỏ qua một lần), xem lịch và tích xong khi người dùng báo đã làm, ngay từ chat.
- **Chỉ huy thông báo** (`javis-notify`) - bundled/chạy · tools: javis_notify · Xem và đổi thông báo nào được báo. Mỗi nhóm thông báo có một chế độ (tất cả, đáng chú ý trở lên, chỉ tin khẩn, tắt); lọc hoặc luôn báo một loại tin; hoàn tác thay đổi của Javis Core.
- **Tạo plugin qua chat** (`javis-plugin`) - bundled/chạy · tools: javis_plugin · Cho Javis tạo, đọc và sửa plugin của người dùng ngay tại chỗ khi được nhờ trong chat, không phải tải file zip về rồi tải lên lại. Plugin mới hoặc vừa đổi mã luôn nằm TẮT, chủ đọc mã rồi tự bật ở trang Plugins. Chỉ phiên của chủ thấy tool này.
- **Project tự học** (`javis-project`) - bundled/chạy · tools: javis_project · Cho Javis tự ghi điều học được về một project trong lúc làm việc, tự gắn file và link kèm mô tả một dòng cho project, cộng sự hay nhóm, và sửa hướng dẫn riêng của project khi người dùng bảo. Chỉ phiên của chủ thấy tool này.
- **Bộ phán xử của bot nhóm** (`javis-reply-policy`) - bundled/chạy · tools: javis_reply_policy, javis_reply_policy_tune · Cho Javis đọc số liệu bộ phán xử (bot nói hay im trong nhóm, vì sao, bị chấm sai ở đâu) và chỉnh nó khi chủ nhờ, rồi hoàn lại được. Chỉ phiên của chủ thấy hai tool này, bot chăm khách không bao giờ thấy.
- **Đặt việc định kỳ & nhắc hẹn** (`javis-schedule`) - bundled/chạy · tools: javis_schedule · Tạo/liệt kê/huỷ việc chạy định kỳ và nhắc hẹn ngay từ chat. Tự chọn kho - việc lặp và bền thì ghi Javis/loops/<slug>.md để sửa được trong Obsidian; nhắc một lần hoặc lịch cron thì vào kho nhắc hẹn (đã có sẵn cron 5 trường). Thay cho việc gõ YAML tay hoặc curl.
- **Giao việc Kanban** (`javis-task`) - bundled/chạy · tools: javis_task · Giao một việc nền vào hàng đợi Kanban và xem việc đang chạy tới đâu, ngay từ chat. Trước tool này chỉ engine chạy được lệnh máy (Claude Code, Codex) mới giao việc được, vì đường duy nhất là curl POST /kanban/task - năm engine API đứng ngoài.
- **Quản lý nhóm chat** (`javis-team`) - bundled/chạy · tools: javis_team · Tạo, sửa, lưu trữ và xoá nhóm chat, thêm bớt trợ lý, chọn trưởng nhóm, tạo trợ lý mới với model riêng rồi ghép vào nhóm, ngay từ chat và trên mọi engine. Trước tool này phải vào trang Nhóm bấm tay, hoặc điều khiển trình duyệt.
- **Việc nền tự điều chỉnh** (`javis-tune`) - bundled/chạy · tools: javis_tune · Cho Javis xem và chỉnh cách việc nền tự chọn model theo lời người dùng trong chat (tiết kiệm token, làm cho chắc, việc này làm sai). Chỉ phiên của chủ thấy tool này.
- **Điều khiển dashboard** (`javis-ui`) - bundled/chạy · tools: javis_ui · Mở trang, mở file trong brain, mở một việc Kanban hoặc cuộn khung chat trên dashboard đang mở, theo lời người dùng nói hoặc gõ. Dashboard xác nhận đã làm xong ngay trong lượt; không có tab nào mở thì tool nói rõ.
- **Theo dõi trang web** (`javis-watch`) - bundled/chạy · tools: javis_watch · Canh một trang web theo lịch mà không tốn token - báo khi trang đổi, khi xuất hiện một cụm chữ hoặc khi có giá dưới ngưỡng (hiểu 1.250.000đ, 1,5 triệu, 250k, $20). Chỉ gọi AI khi bật tóm tắt.
- **Lịch sử quy trình** (`javis-workflow`) - bundled/chạy · tools: javis_workflow · Xem các lần chạy quy trình gần đây và kết quả từng lần, ngay từ chat. Trước tool này, chạy quy trình xong là kết quả mất, hỏi "quy trình chạy gần nhất ra sao" Javis không có gì để tra.
- **Kiểm tra Messenger** (`messenger-health`) - bundled/chạy · tools: messenger_check, messenger_repair · Rà kết nối bot Messenger của từng Fanpage (token Trang, quyền, webhook, Trang gắn app, bot đang trực) và sửa tự động phần webhook khi bot im lặng.
- **Meta Ads (Graph API)** (`meta-ads-graph`) - bundled/chạy · tools: meta_ads_accounts, meta_ads_insights, meta_ads_campaigns, meta_ads_get · Đọc số liệu quảng cáo Facebook/Instagram (tài khoản ads, chiến dịch, hiệu suất) qua Graph API, dùng token của kết nối "Meta Ads (tự tạo app)". CHỈ ĐỌC, không tiêu tiền.
- **Facebook Trang (Graph API)** (`meta-pages-graph`) - bundled/chạy · tools: fb_pages_list, fb_page_posts, fb_page_comments, fb_page_scheduled, fb_page_post, fb_page_photo, fb_page_album, fb_page_video, fb_page_edit, fb_page_delete, fb_page_reply · Quản lý Trang/Fanpage Facebook qua Graph API - liệt kê Trang, đọc bài, bình luận và bài đang chờ đăng (chỉ đọc), đăng hoặc hẹn giờ bài/ảnh/album, đăng video, sửa chữ, xoá bài và trả lời bình luận (toàn quyền). Dùng Fanpage đã nối ở thẻ Facebook Messenger (trang Kết nối), hoặc kết nối "Facebook Trang" trong Kho nếu có.
- **Nhật ký dùng tool** (`tool-audit`) - bundled/tắt · tools: javis_tool_stats · hooks: post_tool_call · Đếm số lần MỖI tool được engine gọi (qua hook post_tool_call) và cho xem thống kê tool hay dùng. Đây là ví dụ minh hoạ cơ chế HOOK của plugin. Mặc định TẮT - bật qua POST /plugins/toggle (slug=tool-audit) để thử.
- **Tin thoại** (`voice-note`) - bundled/chạy · tools: javis_voice_note · Javis ghi một đoạn nói ngắn (tối đa 1000 ký tự) thành file mp3 trong attachments/voice/ rồi nhúng vào câu trả lời. Khung chat hiện trình phát, Telegram nhận file âm thanh. Dùng giọng Edge miễn phí theo ngôn ngữ của câu.
- **Đọc video YouTube** (`youtube-read`) - bundled/chạy · tools: javis_youtube_read · Đọc lời thoại (phụ đề) của video YouTube từ link để tóm tắt. Tự đổi qua 6 kiểu trình phát rồi tới yt-dlp khi YouTube chặn máy chủ. Không cần đăng nhập, không cần API key.
- **Debate Engine - Red/Blue Team** (`debate-engine`) - vault/tắt · tools: debate_engine · hooks: post_tool_call · Đưa lượt rà soát Red/Blue vào Kanban, kiểm tra ngân sách ước tính và tự ngắt khi thất bại liên tiếp.

## Cờ sức khoẻ
- Workflow trỏ agent KHÔNG tồn tại: claude, deepseek, dola, grok, perplexity
- Agent chưa workflow nào dùng: shopdonk-deepseek-data, shopdonk-gemini-draft, shopdonk-grok-check, shopdonk-luna-analysis, shopdonk-sol-test, shopdonk-sonnet-review
