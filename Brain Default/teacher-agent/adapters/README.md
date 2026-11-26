# Sổ adapter

Trạng thái: THIẾT KẾ = chưa gọi thử lần nào. ĐÃ THẤY MCP = công cụ có mặt nhưng chưa giao gói thử. Chưa adapter nào ở mức ĐÃ GỌI THỬ (SOUL-01).

| Adapter | Loại | Cấp | S tối đa mặc định | Ghi chú chẩn đoán R2 hay gặp | Trạng thái |
|---|---|---|---|---|---|
| `claude.md` (Opus/Sonnet/Haiku, Claude Code) | API + agent CLI | AI, Agent, SubAgent | S2 | Prompt quá dài, tiền tố đổi làm tụt cache; Haiku giá ×5 khi >100K | THIẾT KẾ |
| `deepseek.md` (V4-Pro, V4.1-Flash) | API hosted | AI, SubAgent | S1 | Thinking bật mặc định làm đội chi phí; yếu khi tự làm chủ vòng lặp tool | THIẾT KẾ |
| `antigravity.md` (`agy`, gemini-3.8-flash-high — họ Google) | Agent CLI | Agent | S1 | Sửa lan ngoài phạm vi; báo xong khi test đỏ | THIẾT KẾ |
| `javis.md` (đội Codex, Luna, Sol, Grok, Gemini Flash, Antigravity, DeepSeek Flash, Sonnet 4.6 + Kanban) | AgentOS cục bộ | người chấm, thợ | theo thành viên | Giao trùng việc, gói không có đường nhận kết quả | ĐÃ THẤY MCP |
| `ollama.md` | Model tự chạy | AI, SubAgent | S2 | Template chat sai, num_ctx ngắn | THIẾT KẾ |
| openai-gpt | API | AI, Agent | S1 | Khác định dạng tool call; cần chuẩn hóa | Chưa soạn |
| gemini | API | AI, Agent | S1 | Ngữ cảnh dài, kiểm trích dẫn | Chưa soạn |
| langgraph | Framework | Agent, AgentOS | theo model | Trạng thái graph, checkpoint, vòng lặp không thoát | Chưa soạn |
| crewai | Framework đa agent | Agent, SubAgent, AgentOS | theo model | Vai chồng chéo, ủy quyền vòng tròn | Chưa soạn |
| autogen | Framework đa agent | Agent, AgentOS | theo model | Hội thoại agent không dừng, chi phí phình | Chưa soạn |
| n8n | Workflow | AgentOS | theo node | Node lỗi im lặng, retry trùng tác dụng | Chưa soạn |
| mcp | Giao thức công cụ | Agent (tầng công cụ) | theo server | Mô tả tool mơ hồ, injection qua kết quả tool | Chưa soạn |
| rag | Truy xuất | Agent, AgentOS | theo kho | Truy xuất sai đoạn, trích dẫn bịa, chỉ mục cũ | Chưa soạn |
| agentos-tu-xay | Hệ tự xây | AgentOS | theo hồ sơ | Bộ nhớ, lịch, cổng duyệt tự viết | Chưa soạn |

Adapter mới soạn khi có học viên thật dùng nền tảng đó (quy trình tiếp nhận bước T2), không soạn trước.
