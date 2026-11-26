# Gói việc cho Doctor Agent - 26/11/2026 ~17:10
Mỗi gói làm 1 commit. Quy trình: sao lưu vào backups/, chạy pytest cho xanh, bật CAM thật và kiểm /api/health, đo lại bằng cam_monitor. Ô nào trong V1-V5 chuyển đỏ thì lùi ngay.
Repo: D:\AI AGENT\council-agent-manager, HEAD d3c1b9d.
Nguồn: C:\Users\Admin\cam-soat-cheo\ket-qua-20261126-500ac7a\codex_final.md
Thứ tự: G1, G2, G5, G3, G4, G6. G7 và G8 chỉ đọc. G9 làm sau G1.

## G1. Chặn các lỗi Codex #1-#6
- #1 Forge rồi pytest: cam_core/app.py:929-984, command_gate.py, policy/cam_policy.json. pytest chỉ được chạy trên thư mục test cố định.
- #2 Biểu thức PowerShell (...), @(...), {...}: policy.py _CHAIN_CHARS, code_forge.py. Hướng sửa: chạy lệnh dạng danh sách đối số, không qua shell.
- #3 PATCH /api/agents/{id} đổi adapter_params.binary_path/cli_kind: app.py:1437, registry.py, adapters/cli_adapter.py.
- #4 API cục bộ không xác thực: bind 127.0.0.1, thêm token phiên cho các endpoint ghi.
- #5 CAM_POLICY=off: registry.py:145-146, l012_dispatcher.py:29.
- #6 Gọi vòng cổng L0: l0_gate.py, cam_approve.py.
- Nghiệm thu: 8 chuỗi trong chk_gate.py đều bị chặn, trừ `python -m pytest tests -q`. Có test tái hiện #1 và #3 bị chặn, chạy trong sandbox _isolation. PATCH binary_path trả 4xx, hash roster không đổi. Số test >= 132 + số test mới, 0 đỏ. V1-V5 và V8 xanh (mục mới phải được L0 thêm vào v8_plan trước).
- Rủi ro: khóa quá chặt làm hỏng Forge dùng thật. Chia 2-3 commit.
- Kiểm chéo: Codex, cộng Luna/Grok khi có key.

## G2. Từ chối prop_5e5e1f1e (quyết định L0 lúc 16:59)
- Dùng đường từ chối có sẵn (evolution engine hoặc cam_approve reject), L0 gõ mã 6 ký tự. Không sửa tay file JSON.
- Nghiệm thu: trạng thái rejected, có decided_at. Không ghi ký ức "đã nghiệm thu". BootGuard không bị đụng.

## G3. Bộ đếm chi phí V7 theo ngày
- Mỗi lượt gọi model ghi một dòng: giờ, agent, model, đích, token vào/ra, chi phí ước tính theo giá đã kiểm 26/11. Có trần ngày; vượt trần chỉ cảnh báo.
- File: adapters/ (adapter relay), cam_core/chat_engine.py, cam_monitor.v7.
- Nghiệm thu: 1 lượt chat thật tạo đúng 1 dòng; v7 xanh khi dưới trần; test chạy trong sandbox.
- Rủi ro: module mới cần CUP và cập nhật v8_plan. Không ghi tên relay hay key vào log.
- Kiểm chéo: Sol viết/chấm test, Codex soát.

## G4. Cổng S cam_core/sgate.py (bắt buộc trước khi bật agent thứ 2)
- Chặn dữ liệu S2 (brains/, accounts_pool, dữ liệu EA) và S3 (bí mật) gửi tới model hosted. Khi chặn ghi log "Cổng dữ liệu chặn".
- Nghiệm thu: mẫu S2/S3 bị chặn, S0/S1 đi qua, V5 đếm được số lần chặn.
- Rủi ro: chặn nhầm, regex dò bí mật bỏ sót. Cần CUP và cập nhật v8_plan.
- Kiểm chéo: Codex và Luna/Grok.

## G5. Rò rỉ cô lập test (Codex #13, có bằng chứng 17:07)
- pytest --collect-only đã ghi logs/repair_packet.md và .pytest_cache. tests/_isolation.py:71 chỉ chuyển hướng lúc chạy test, chưa phủ lúc import.
- Nghiệm thu: chụp mtime toàn repo trước/sau cả collect lẫn chạy đủ test: 0 tệp đổi. Thêm kiểm tra vào tests/test_isolation_guard.py.

## G6. U1 khung chat (theo ux-khung-chat.md)
- Enter gửi, Shift+Enter xuống dòng, không gửi nhầm khi IME tiếng Việt đang gõ dở. Tự giãn ô nhập, giữ nháp. Dán ảnh Ctrl+V, kéo thả. Copy từng tin, khối code, nhiều tin, toàn bộ, xuất .md.
- File: templates/ui/.
- Nghiệm thu: đạt checklist trên CAM thật có ảnh chụp; gõ Telex "Việt Nam" rồi Enter không bị gửi giữa chừng. Không thêm endpoint mới khi chưa có CUP.
- Kiểm chéo: Codex.

## G7. U0 (chỉ đọc)
- Đọc chat_sessions.db chế độ chỉ đọc và cam.log, xử lý cục bộ, không gửi model hosted.
- Nghiệm thu: bảng số lượt/ngày, giờ dùng, tính năng dùng; git và hash V3 không đổi.

## G8. Chưng cất góp ý L0
- Chỉ ra đường dẫn tệp kết quả của luồng đã báo "All 6 steps done" và đưa L0 đọc. owner_feedback.db chỉ đọc.

## G9. Soát khác hãng lượt 2
- Codex soát c8f0f53 và các commit G1-G5; thu nhỏ gói soát (lượt 1 tốn 11,7 triệu token).
- dsh và ShopDonk chờ L0 đặt key.
