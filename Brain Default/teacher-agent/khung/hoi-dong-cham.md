# Hội đồng chấm và luật ghép cặp khác hãng (T2) — v0.1.1

Luật cứng: **người chấm không được cùng hãng với model nền của học viên** (kể cả khác phiên bản, kể cả bọc trong agent). Câu V≥2 cần 2 người chấm thuộc 2 hãng khác nhau và khác hãng học viên.

## Hãng của từng người chấm/thợ
| Người | Model nền | Hãng | Nguồn | Chi phí biên |
|---|---|---|---|---|
| Codex | gpt-6.2-sol | OpenAI | Javis | gói thuê bao (E4) |
| Luna | gpt-6-luna | OpenAI | Javis | gói thuê bao (E4) |
| Sol | gpt-5.6-sol | OpenAI | Javis | gói thuê bao (E4) |
| Grok | Grok 4.7 | xAI | Javis | gói thuê bao (E4) |
| Gemini Flash | gemini-3.8-flash | Google | Javis | gói thuê bao (E4) |
| Antigravity | gemini-3.8-flash-high | **Google** | Javis | gói thuê bao (E4) |
| DeepSeek Flash | V4.1-Flash | DeepSeek | Javis | thấp |
| Sonnet 4.6 | claude-sonnet-4-6 | **Anthropic** | Javis | gói thuê bao (E4) |
| Ollama | theo model đã tải (Llama/Qwen/Gemma…) | theo họ model | máy L0 | 0 API |
| Opus 5.5 | claude-opus-5-5 | Anthropic | API trả phí / phiên Claude | cao — chỉ D4-D5 + ranh giới |

Chú ý: Antigravity là họ Google, Sonnet 4.6 là họ Anthropic. Model Ollama mang hãng của họ model gốc (Gemma = Google, Llama = Meta, Qwen = Alibaba).

## Ma trận ghép (người chấm chính → phụ)
| Học viên thuộc hãng | Chấm thường (D1-D3) | D4-D5 + ranh giới | Cấm |
|---|---|---|---|
| Anthropic (Opus/Sonnet/Haiku 5.5, Sonnet 4.6, CAM-Claude) | Codex → Grok | Codex + Grok (2 hãng) | Opus, Sonnet 4.6 |
| OpenAI (Codex/Luna/Sol) | Grok → DeepSeek | Opus + Grok | Codex, Luna, Sol |
| Google (Gemini Flash, Antigravity) | Codex → DeepSeek | Opus + Codex | Gemini Flash, Antigravity, Ollama-Gemma |
| xAI (Grok) | Codex → DeepSeek | Opus + Codex | Grok |
| DeepSeek (V4-Pro, V4.1-Flash) | Codex → Grok | Opus + Codex | DeepSeek |
| Ollama (họ X) | người không thuộc họ X: Codex → Grok | Opus + Codex (nếu X ≠ Anthropic/OpenAI) | họ X |
| Hệ đa model (vd CAM OS) | chấm theo thành phần sinh ra đầu ra; đầu ra trộn → 2 người chấm khác mọi hãng có mặt nếu được, không được thì ghi rõ hạn chế | | |

Kiểm bằng code trước, LLM chấm sau. Opus chỉ vào khi: D4-D5, câu ranh giới, hoặc hai người chấm lệch >1 điểm — và không bao giờ chấm học viên họ Anthropic.

## Ngân sách
- Ưu tiên: kiểm bằng code → Ollama → đội Javis → API trả phí (chỉ khi trong máy không có lựa chọn phù hợp).
- Trần an toàn 150 USD/30 ngày. **Báo L0 ngay khi chi API trả phí vượt 20 USD** (cộng dồn từ ngày 1), kèm lý do và dự báo.
- Mỗi lần chấm ghi: người chấm, hãng, nguồn (Javis/Ollama/API), chi phí thật nếu có.
