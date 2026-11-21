# Javis Index (tầng vận hành)

> Tự sinh từ file - ĐỪNG sửa tay. Chỉ mục mọi năng lực của Javis trong brain này để bất kỳ AI/engine đọc 1 chỗ là hiểu Javis làm được gì. Song song `wiki/index.md` (tri thức).

**Tổng quan:** 24 agents · 14 skills · 6 workflows (1 bật) · 0 loops (0 bật) · 32 plugins (30 chạy)

## Agents
- **Biên tập Video ngắn** (`bien-tap-video-ngan`) - Phân tích tư liệu và dựng video ngắn từ tệp cục bộ khi có công cụ và quyền chạy. · skills: video-animation-toolkit · tags: Nội dung, Video
- **Chuyên viên Cơ bản và Vĩ mô** (`chuyen-vien-co-ban-vi-mo`) - Theo dõi tin tức, lịch kinh tế và bối cảnh vĩ mô để nói cái gì có thể làm gãy kế hoạch giao dịch. · tags: tai-chinh, vi-mo, tin-tuc
- **Chuyên viên Dòng tiền và Tâm lý** (`chuyen-vien-dong-tien-tam-ly`) - Đọc khối lượng, funding, hợp đồng mở, tỷ lệ long short và độ căng của đám đông để cảnh báo bẫy thanh khoản. · tags: tai-chinh, dong-tien, tam-ly-thi-truong
- **Điều phối AI Company** (`dieu-phoi-ai-company`) - Điều phối yêu cầu đa phòng ban trong Brain này, chọn năng lực Javis phù hợp và tổng hợp đầu ra có kiểm soát. · skills: van-hanh-ai-company-on-dinh, chuyen-viec-sang-app-desktop · tags: ai, dieu-phoi, van-hanh
- **Điều phối Kế hoạch Ngày** (`dieu-phoi-ke-hoach-ngay`) - Biến ưu tiên đã chọn thành kế hoạch ngày có trình tự, mốc kiểm tra và điều kiện hoàn thành. · tags: van-hanh, nang-suat
- **Ghi biên bản Red/Blue Team** (`ghi-bien-ban-red-blue`) - Ghi lại điểm bất đồng giữa red team và blue team, phán quyết cuối và bài học rút ra sau mỗi vòng phản biện. · tags: ai, kiem-duyet, bien-ban
- **Giám đốc Đầu tư (CIO)** (`giam-doc-dau-tu`) - Chủ trì phiên họp đầu tư, cân mọi quan điểm, chốt đúng một trạng thái hành động kèm phiếu lệnh. · tags: tai-chinh, lanh-dao, quyet-dinh
- **Giám đốc Marketing ngành đào tạo lái xe** (`giam-doc-marketing-nganh-dao-tao-lai-xe`) - Xây dựng chiến lược marketing và nội dung giúp thu hút học viên phù hợp cho dịch vụ dạy lái xe số tự động.
- **Javis Core** (`javis-core`) - Trợ lý hệ thống nhận báo cáo và hỗ trợ công việc trong brain này.
- **Kiểm chứng dữ liệu** (`kiem-chung-du-lieu`) - Chặn mọi con số không có nguồn trước khi phiên họp bắt đầu, xác nhận hoặc bác từng số liệu. · tags: tai-chinh, kiem-chung, chat-luong
- **Kiểm duyệt & Chuẩn bị đăng** (`kiem-duyet-chuan-bi-dang`) - Rà soát nội dung, hoàn thiện gói đăng và trình chủ duyệt trước khi xuất bản.
- **Kiểm tra Khả thi Ngày** (`kiem-tra-kha-thi-ngay`) - Rà soát kế hoạch ngày để giảm quá tải, phát hiện phụ thuộc và chốt một phiên bản thực thi. · tags: van-hanh, nang-suat
- **Kiến trúc sư Antigravity** (`kien-truc-su-antigravity`) - Kiến trúc sư Trưởng & Master Optimizer: Tái cấu trúc mã nguồn phức tạp, tối ưu hóa thuật toán MQL5/Trading, xử lý dữ liệu backtest lớn qua data-query, và nghiệm thu regression độc lập. · model gemini-3.8-flash-high · skills: data-query · tags: Nhóm, Kỹ thuật
- **Kỹ sư EA - Claude** (`ky-su-ea---claude`) - Kỹ sư MQL5/MQL4: viết, sửa, tối ưu Expert Advisor, order/position/basket management, risk control. Sửa hệ thống có sẵn ưu tiên hơn viết mới. · model sonnet · tags: Nhóm
- **Nghiên cứu & Kiểm chứng** (`nghien-cuu-kiem-chung`) - Nghiên cứu nguồn đáng tin cậy, kiểm tra dữ kiện và phát hiện tuyên bố cần thận trọng trong nội dung.
- **Nhật ký và Thực thi** (`nhat-ky-thuc-thi`) - Nhắc stop loss và take profit, ghi nhật ký lệnh, chấm điểm lại sau khi lệnh đóng; không đặt lệnh hộ. · tags: tai-chinh, nhat-ky, ky-luat
- **Phản biện chéo - ChatGPT** (`phan-bien-cheo---chatgpt`) - Reviewer độc lập: phản biện đối kháng đầu ra của agent khác (code EA, chiến lược, content, affiliate) để tìm lỗi logic, giả định thiếu, rủi ro. · model gpt-6.2-sol · tags: Nhóm
- **Phản biện nội dung** (`phan-bien-noi-dung`) - Rà soát đối kháng bản nháp content để tìm lỗi, giả định thiếu và rủi ro trước bước kiểm chứng và biên tập. · tags: noi-dung, kiem-duyet, chat-luong
- **Phân tích thị trường an toàn** (`phan-tich-thi-truong-an-toan`) - Hỗ trợ theo dõi thị trường và phân tích kỹ thuật có kỷ luật, ưu tiên quản trị rủi ro; không tự thực hiện giao dịch. · tags: tai-chinh, phan-tich-ky-thuat, quan-tri-rui-ro
- **Phân tích Ưu tiên Ngày** (`phan-tich-uu-tien-ngay`) - Chuyển mục tiêu và việc tồn thành các ưu tiên ngày rõ ràng, giới hạn và có căn cứ. · tags: van-hanh, nang-suat
- **Quản trị Rủi ro** (`quan-tri-rui-ro`) - Người gác cổng rủi ro của văn phòng, có quyền phủ quyết mọi kế hoạch sai ngưỡng, cấp hoặc hạ quy mô vị thế. · tags: tai-chinh, quan-tri-rui-ro, phe-duyet
- **Thư ký Hội đồng** (`thu-ky-hoi-dong`) - Điều hành phiên họp theo trình tự, ghi biên bản trung thực ai nói gì, ai phản đối và vì sao. · tags: tai-chinh, thu-ky, bien-ban
- **Trợ lý Content cá nhân** (`tro-ly-content-ca-nhan`) - Lên kế hoạch, viết và kiểm duyệt content; chuẩn bị kịch bản, hướng dẫn dựng video ngắn và bàn giao bài đăng theo quy trình duyệt.
- **Trưởng phòng Nghiên cứu** (`truong-phong-nghien-cuu`) - Điều phối và chất vấn ba chuyên viên phân tích, tổng hợp quan điểm và làm nổi điểm bất đồng có ảnh hưởng tới quyết định. · tags: tai-chinh, nghien-cuu, dieu-phoi

## Skills
### AI
- **Chuyển việc sang app desktop** (`chuyen-viec-sang-app-desktop`) - Đẩy việc bị chặn sang ChatGPT Desktop hoặc Claude Desktop, gửi prompt và đọc trả lời tự động.
- **Ingest Source** (`ingest-source`) - Tiêu hoá một source thô vào Second Brain, chưng cất thành tri thức wiki tích luỹ.
- **Javis Builder** (`javis-builder`) - Tạo hoặc sửa năng lực của Javis: agent, skill, workflow, loop, plugin. Kèm mẫu file chuẩn và luật chống trùng.
- **Lint Wiki** (`lint-wiki`) - Rà soát sức khoẻ wiki của Second Brain, trả về danh sách vấn đề. Không tự sửa hàng loạt.
- **Notes** (`notes`) - Lưu tin nhắn hiện tại nguyên văn vào sources/ (kèm ảnh), tự chưng cất lên wiki nếu note đáng.
- **Query Wiki** (`query-wiki`) - Khai thác tri thức trong Second Brain: tổng hợp, so sánh, giả thuyết. Trả lời có trích dẫn.
- **Tách phiên thông minh** (`tach-phien-thong-minh`) - Nén ngữ cảnh có kiểm chứng và tạo bàn giao để tiếp tục trong phiên mới.
- **Vận hành AI Company ổn định** (`van-hanh-ai-company-on-dinh`) - Điều phối AI Company chịu lỗi nhiều tầng bằng checkpoint, phân loại lỗi, chuyển nguồn có giới hạn và khôi phục an toàn.
### Chung
- **data-query** (`data-query`) - Truy vấn dữ liệu lớn (JSON, CSV, JSONL) bằng SQLite ảo mà không làm tràn context window của mô hình. Tối ưu cho phân tích log backtest MQL5, lịch sử tick, danh sách lệnh và dữ liệu thị trường khối lượng lớn.
### Marketing
- **HTML sang Webcake** (`html-to-webcake`) - Chuyển trang HTML thành file .pke mở được trong trình dựng Webcake, giữ đúng màu, cỡ chữ, ảnh và bố cục của bản gốc.
### Năng suất
- **Tiết kiệm token Terminal (RTK)** (`token-saver-rtk`) - Dùng RTK để rút gọn đầu ra lệnh Terminal trong tác vụ kỹ thuật; giữ đủ chi tiết khi cần xác minh.
### Nội dung
- **Hoạt hình & Video** (`video-animation-toolkit`) - Phân tích video tham chiếu MP4/MOV, dựng và xuất video bằng FFmpeg, lập quy trình hoạt hình 2D/3D và motion graphics.
### Security
- **Security Audit** (`security-audit`) - Rà soát bảo mật mã nguồn, API, dịch vụ: tìm lỗ hổng có bằng chứng, kiểm chứng độc lập từng lỗi, báo cáo kèm cách sửa. Từ Cloudflare.
### Tài chính
- **Họp hội đồng đầu tư** (`hop-hoi-dong-dau-tu`) - Chạy một phiên họp phân tích thị trường đủ 6 pha, ra phiếu lệnh và biên bản.

## Workflows
### AI
- **Red/Blue Team Review - AI Company** (`red-blue-team-review`) - off · 3 bước [phan-bien-cheo---chatgpt -> nghien-cuu-kiem-chung -> ghi-bien-ban-red-blue] · Vòng phản biện đối kháng 3 bước cho mọi đầu ra của AI Company - red attack, blue patch, biên bản phán quyết.
### Năng suất
- **Kế hoạch ngày thực dụng** (`ke-hoach-ngay-thuc-dung`) - off · 3 bước [phan-tich-uu-tien-ngay -> dieu-phoi-ke-hoach-ngay -> kiem-tra-kha-thi-ngay] · Biến danh sách việc và mục tiêu thành kế hoạch ngày ngắn, khả thi và có bước chốt cuối ngày.
### Nội dung
- **Dựng video và trả MP4** (`dung-video-tra-mp4`) - active · 1 bước [bien-tap-video-ngan] · Tiếp nhận video, chốt brief và phương án, duyệt từng mốc dựng rồi trả MP4 đã kiểm tra.
- **Sản xuất Content & Video ngắn** (`san-xuat-content-video-ngan`) - off · 0 bước [] · Tạo bản nháp content đào tạo lái xe, kiểm duyệt có giới hạn và bàn giao chờ chủ duyệt.
### Tài chính
- **Phát triển EA - bản vá và phản biện** (`phat-trien-ea-ban-va`) - off · 0 bước [] · Kiểm tra Task Card, soạn bản vá EA và phản biện; không chạy MT5 hoặc đặt lệnh.
- **Phiên họp phân tích thị trường** (`phien-hop-phan-tich-thi-truong`) - off · 0 bước [] · Kiểm chứng dữ liệu, phân tích thị trường và bàn giao phán quyết rủi ro trong ba bước.

## Loops
_(chưa có)_

## Plugins (tool/hook native cho mọi engine)
- **Ủy thác Antigravity** (`antigravity-delegate`) - bundled/chạy · tools: javis_antigravity_delegate · Ủy thác tác vụ kỹ thuật nặng, viết code MQL5/Trading, phân tích và refactor lớn sang Antigravity (Google AI Pro - 0đ phí API).
- **Thời gian & ngày** (`datetime-vn`) - bundled/chạy · tools: javis_now, javis_date_add · Xem ngày giờ hiện tại theo múi giờ chọn ở Cài đặt và tính ngày tương đối (mai, mốt, N ngày nữa, tuần trước). Thuần stdlib, chỉ đọc, không cần mạng.
- **Điều khiển app trên máy** (`desktop-apps`) - bundled/chạy · tools: javis_app_list, javis_app_open, javis_app_close · Mở, đóng và liệt kê ứng dụng trên CHÍNH MÁY đang chạy Javis (Windows, macOS, Linux có màn hình) theo lời người dùng, ví dụ "mở Chrome", "tắt Excel", "đang mở app nào". Tự chặn và nói rõ khi Javis chạy trong Docker trên máy chủ, vì khi đó máy chạy Javis không phải máy của người dùng.
- **Tạo và xem ảnh (ChatGPT)** (`image-chatgpt`) - bundled/chạy · tools: javis_generate_image, javis_describe_image · Tạo ảnh từ mô tả bằng GÓI ChatGPT đang đăng nhập (OAuth) - không cần OpenAI API key. Dùng Codex Responses API + tool image_generation (gpt-image-2). Ảnh lưu vào attachments/ của vault để nhúng thẳng vào chat. Kèm tool XEM ảnh, để ChatGPT nhìn ảnh trong brain rồi tả lại bằng chữ, để cả engine không tự xem được ảnh (OpenRouter, Gemini API...) cũng biết trong ảnh có gì. Cần đã kết nối ChatGPT ở trang Model.
- **Trả lời khách từ Hội thoại** (`inbox-reply`) - bundled/chạy · tools: inbox_find, inbox_reply · Tìm hội thoại khách trên trang Hội thoại và gửi tin trả lời ngay vào đó, đúng kênh của cuộc chat (Messenger, Instagram, Telegram, Zalo...), như chủ gõ tay ở Hộp thư.
- **Đấu thêm MCP** (`javis-connect`) - bundled/chạy · tools: javis_add_mcp · Đấu một MCP server vào kho Kết nối của Javis ngay từ chat, để nó HIỆN ra trang Kết nối như mọi tài khoản khác. Trước tool này Javis chỉ còn đường `claude mcp add` - thứ rơi vào config riêng của Claude Code, không bộ não nào khác thấy và người dùng cũng không thấy trên trang Kết nối.
- **Tên và phong cách của Javis Core** (`javis-core-name`) - bundled/chạy · tools: javis_core_name · Cho người dùng đặt tên riêng và phong cách nói chuyện cho Javis Core của brain này, ngay trong chat. Tên hiện trên trang Cộng sự. Chỉ phiên của chủ thấy tool này.
- **GitHub trong khung chat** (`javis-github`) - bundled/chạy · tools: javis_github · Xem trạng thái repo GitHub của khung chat (nhánh, PR, CI, merge), xếp việc kế tiếp để Javis tự làm khi PR hiện tại đã merge xong, và review chéo PR khi người dùng yêu cầu.
- **Mục tiêu (Hệ thống cộng hưởng)** (`javis-goal`) - bundled/chạy · tools: javis_goal, javis_submit_deliverable · Cho bộ não tự lập một mục tiêu bền khi người dùng giao việc cần theo đuổi sau lượt chat, hoặc cập nhật mục tiêu đang mở khi người dùng bổ sung ý. Host kiểm đề xuất theo SMART và lưu có revision. Chỉ hiện ở brain đã bật Hệ thống cộng hưởng.
- **Tự cải tiến theo yêu cầu** (`javis-improve`) - bundled/chạy · tools: javis_improve · Khi chủ yêu cầu, Javis hay một trợ lý tự sửa chính nó và brain (trợ lý, skill, workflow, vòng lặp, bộ nhớ) có sao lưu và hoàn tác, sửa mã nguồn Javis qua GitHub, rồi tự cập nhật lên bản mới. Chỉ phiên của chủ thấy tool này.
- **Việc chạy nền** (`javis-job`) - bundled/chạy · tools: javis_job · Theo dõi lệnh chạy ngầm engine bỏ lại (render, build, tải về). Dặn trước "xong thì làm tiếp gì", xem việc đang chạy, dừng một việc. Xong là Javis tự báo về đúng khung chat và tự làm tiếp.
- **Cookies** (`javis-login`) - bundled/chạy · tools: javis_login · Mở trang web cần đăng nhập bằng phiên đăng nhập chủ đã cất ở trang Cookies. Chỉ trả nội dung trang, không bao giờ trả cookie.
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
- **Facebook Trang (Graph API)** (`meta-pages-graph`) - bundled/chạy · tools: fb_pages_list, fb_page_posts, fb_page_comments, fb_page_post, fb_page_photo, fb_page_album, fb_page_video, fb_page_edit, fb_page_delete, fb_page_reply · Quản lý Trang/Fanpage Facebook qua Graph API - liệt kê Trang, đọc bài và bình luận (chỉ đọc), đăng bài/ảnh/video/album, sửa chữ, xoá bài và trả lời bình luận (toàn quyền). Dùng Fanpage đã nối ở thẻ Facebook Messenger (trang Kết nối), hoặc kết nối "Facebook Trang" trong Kho nếu có.
- **Nhật ký dùng tool** (`tool-audit`) - bundled/tắt · tools: javis_tool_stats · hooks: post_tool_call · Đếm số lần MỖI tool được engine gọi (qua hook post_tool_call) và cho xem thống kê tool hay dùng. Đây là ví dụ minh hoạ cơ chế HOOK của plugin. Mặc định TẮT - bật qua POST /plugins/toggle (slug=tool-audit) để thử.
- **Tin thoại** (`voice-note`) - bundled/chạy · tools: javis_voice_note · Javis ghi một đoạn nói ngắn (tối đa 1000 ký tự) thành file mp3 trong attachments/voice/ rồi nhúng vào câu trả lời. Khung chat hiện trình phát, Telegram nhận file âm thanh. Dùng giọng Edge miễn phí theo ngôn ngữ của câu.
- **Đọc video YouTube** (`youtube-read`) - bundled/chạy · tools: javis_youtube_read · Đọc lời thoại (phụ đề) của video YouTube từ link để tóm tắt. Tự đổi qua 6 kiểu trình phát rồi tới yt-dlp khi YouTube chặn máy chủ. Không cần đăng nhập, không cần API key.
- **Debate Engine - Red/Blue Team** (`debate-engine`) - vault/tắt · tools: debate_engine · hooks: post_tool_call · Đưa lượt rà soát Red/Blue vào Kanban, kiểm tra ngân sách ước tính và tự ngắt khi thất bại liên tiếp.

## Cờ sức khoẻ
- Agent chưa workflow nào dùng: chuyen-vien-co-ban-vi-mo, chuyen-vien-dong-tien-tam-ly, dieu-phoi-ai-company, giam-doc-dau-tu, giam-doc-marketing-nganh-dao-tao-lai-xe, javis-core, kiem-chung-du-lieu, kiem-duyet-chuan-bi-dang, kien-truc-su-antigravity, ky-su-ea---claude, nhat-ky-thuc-thi, phan-bien-noi-dung, phan-tich-thi-truong-an-toan, quan-tri-rui-ro, thu-ky-hoi-dong, tro-ly-content-ca-nhan, truong-phong-nghien-cuu
