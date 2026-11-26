# Teacher — khung huấn luyện đa hệ v0.1.1 (DESIGNED, chưa chạy thật)

Kho chính thức: vault Javis `teacher-agent/` (git). Sổ bài học dùng chung: `teacher-agent/bai-hoc.jsonl`. Cứu hộ và sửa code: Doctor Agent.

Huấn luyện viên (HLV) dùng **một khung chung** cho mọi hệ: model (Claude, GPT, Gemini, DeepSeek, model cục bộ), agent (Claude Code, Antigravity…), framework (LangGraph, CrewAI, AutoGen, n8n), tầng công cụ/tri thức (MCP, RAG) và AgentOS tự xây. Mỗi học viên một thư mục. CAM là học viên thí điểm `hv-001-cam`.

Trạng thái sống trong file. Mỗi phiên (kể cả scheduled task) đọc README → luật HLV → sổ học viên → thư mục học viên liên quan, làm việc, rồi ghi lại trạng thái + vết trước khi kết thúc.

## Cây thư mục
```
teacher-agent/
├─ README.md                    bản đồ kho (file này)
├─ KE-HOACH-HUAN-LUYEN-4-CAP.md kế hoạch 4 cấp + lộ trình 30 ngày
├─ luat-huan-luyen-vien.md      T0-T1 luật của HLV + sàn an toàn chung (chỉ L0 sửa)
├─ so-hoc-vien.jsonl            chỉ mục: mỗi dòng một học viên
├─ CHANGELOG.md · LINEAGE.md    phát hành của khung
├─ khung/                       dùng chung cho mọi học viên
│  ├─ chuan-cham.md             T1 định dạng đề, thang chấm, ngưỡng
│  ├─ golden-tests-loi.jsonl    sàn an toàn chung (mọi học viên phải qua)
│  ├─ golden-tests-hlv.jsonl    test cho chính HLV
│  ├─ quy-trinh-tiep-nhan.md    T2 nhận một hệ mới
│  ├─ quy-trinh-cuu-ho-he-la.md T2 cứu hộ hệ chưa quen (Doctor làm, HLV duyệt + chấm)
│  ├─ hoi-dong-cham.md          T2 đội chấm + ma trận khác hãng + ngân sách
│  └─ mau/                      ho-so-hoc-vien · CUP · benh-an-cuu-ho · nghiem-thu · kpi-tuan.csv
├─ adapters/                    T3 lớp nối từng nền tảng (README = sổ adapter)
├─ hoc-vien/<hv-NNN-ten>/       ho-so · luat-hoc-vien · thanh-vien.jsonl · golden-tests.jsonl
│                               kpi.csv · CHANGELOG · ket-qua/ · benh-an/ · cup/ · vet/
├─ lich/scheduled-tasks-de-xuat.md   6 task đề xuất (CHƯA tạo)
├─ bai-hoc.jsonl               sổ bài học theo model (có sẵn, chỉ thêm dòng)
└─ vet/YYYY-MM.jsonl            vết của chính HLV
```

## Ai được sửa gì
| Tầng | Nội dung | Ai sửa |
|---|---|---|
| T0-T1 | luật HLV, sàn chung, chuẩn chấm | Chỉ L0 |
| T2 | quy trình H0-H7, R-1-R6, tiếp nhận, mẫu | CUP, L0 duyệt |
| T3 | adapter, prompt/few-shot/ngưỡng/ô định tuyến của từng học viên | CUP, duyệt theo lô |
| T4 | sổ, KPI, vết, kết quả | HLV tự ghi (A3) |

Luật học viên thuộc về chủ hệ; HLV chỉ đọc và soạn đề từ đó, không sửa.
