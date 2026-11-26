# Thiết kế tái cấu trúc lõi CAM OS - bản trình L0 (26/11/2026, ~21:40 giờ VN)

Người soạn: thread Darklord "Tái cấu trúc lõi CAM OS". Trạng thái: CHỜ L0 DUYỆT. Chưa sửa dòng code nào của CAM.
Cơ sở: đọc trực tiếp repo tại HEAD d3c1b9d (E1), báo cáo Codex lượt 1 `cam-soat-cheo\ket-qua-20261126-500ac7a\codex_final.md` (E2), gói việc G1-G9, bệnh án, tiêu chí V1-V8.

## 1. Chẩn đoán: vì sao vá từng lỗ không đủ

CAM có khoảng 115 endpoint, 24 hệ con khởi tạo trong `CAMRuntime`, và hơn 20 chỗ tự gọi tiến trình con nằm rải trong 14 file.
Mỗi chỗ tự quyết có được chạy hay không. Các bước khóa 3a chỉ chặn từng cửa đã biết, nên Codex vẫn tìm ra 3 đường chạy mã tùy ý, và mình tìm thêm đường thứ 4:

- Đường mới (Codex chưa thấy vì module không nằm trong gói soát): `POST /api/nano/dispatch` với `role=task_runner` chạy `payload.command` bằng `asyncio.create_subprocess_shell` ngay trong thư mục CAM, không qua cổng lệnh nào (`cam_core/nano_agent_swarm.py:451-466`, định tuyến ở dòng 188-189). Mức: nghiêm trọng.
- API không có xác thực: mọi tiến trình trên máy, và cả trang web mở trong trình duyệt nếu lách được CORS, đều gọi được các endpoint ghi/xóa. CAM chỉ nghe `127.0.0.1` (`cam_core/paths.py:35`), nên không lộ ra mạng, nhưng chưa đủ.
- `CAM_POLICY=off` tắt toàn bộ chính sách, và chính `tests/conftest.py` đặt nó cho cả bộ test, nên test xanh không chứng minh khóa có tác dụng.
- `protected_paths` trong chính sách chỉ là dữ liệu, không hàm nào thi hành.

Kết luận: cần một "lõi hạt nhân" mà mọi tác động ra ngoài bắt buộc đi qua, thay vì thêm khóa thứ 15 vào cửa thứ 15.

## 2. Mục tiêu

- Một điểm chặn cho mỗi loại tác động: chạy tiến trình, gửi dữ liệu cho model, ghi dữ liệu thật, gọi API ghi.
- Mặc định CẤM. Mở bằng file chính sách có SHA, đổi bằng công cụ có bàn phím của L0.
- Test chứng minh đường runtime thật, không phải đối tượng giả; không test nào chạm dữ liệu thật, kể cả khi chỉ thu thập test.
- Giữ nguyên chức năng L0 đang dùng (chat, Hội đồng, bộ não, Telegram). Thứ gì phải tắt thì nói rõ.

## 3. Kiến trúc đích: lõi `cam_core/kernel/` với 4 cổng

1. **Cổng chạy tiến trình** (`kernel/exec_gate.py`): hàm duy nhất được gọi `subprocess`.
   - Chỉ nhận danh sách đối số, không bao giờ qua shell (`powershell -Command`, `create_subprocess_shell`, `shell=True` bị cấm toàn repo, có test quét mã nguồn).
   - Mỗi lời gọi khai mục đích (`git`, `cli_model`, `doctor`, `backup`...). Chính sách liệt kê file chạy được cho từng mục đích. Đường dẫn binary của agent lấy từ chính sách, không lấy từ roster hay API.
   - Hết giờ thì giết cả cây tiến trình (Windows Job Object), sửa Codex #12.
   - Ghi một dòng nhật ký mỗi lần chạy (không ghi đối số chứa nội dung prompt).
2. **Cổng dữ liệu ra model** (`kernel/egress_gate.py`): gộp G4 (cổng S, `sgate.py`) và G3 (bộ đếm chi phí V7).
   - Mọi adapter gọi model đều qua đây: chặn S2/S3 tới model hosted, ghi "Cổng dữ liệu chặn"; ghi 1 dòng chi phí mỗi lượt; vượt trần ngày thì cảnh báo.
3. **Cổng ghi dữ liệu** (`kernel/data_paths.py`): tách gốc mã nguồn khỏi gốc dữ liệu.
   - Mọi thư mục ghi được (brains, config, vault, logs, approvals, docs sinh tự động) lấy từ một gốc dữ liệu, đặt được bằng biến `CAM_DATA_ROOT`.
   - Hàm kiểm đường dẫn chuẩn hóa (`realpath`, không phân biệt hoa-thường, chặn junction) thi hành `protected_paths`, dùng chung cho hàng chờ bản vá, Forge, rollback. Sửa Codex #7.
   - Đây cũng là gốc của việc cô lập test G5: test chỉ cần trỏ `CAM_DATA_ROOT` vào thư mục tạm, kể cả với tiến trình con. Sửa Codex #13.
4. **Cổng API** (`kernel/api_guard.py`): middleware cho mọi endpoint không phải GET.
   - Token phiên sinh mỗi lần khởi động, giao diện nhận qua trang `index.html` do CAM phục vụ; thiếu token thì 401.
   - Kiểm `Host` (chống DNS rebinding) và `Origin`.
   - Endpoint nguy hiểm (khôi phục, xóa bộ não, tạo/sửa agent, chuyển giao, áp dụng đề xuất) cần thêm mã phép một lần của L0 từ `cam_approve.py`, không chỉ `confirmed=true`. Sửa Codex #4.

## 4. Những thứ bị tắt hoặc gỡ (cần L0 biết)

- Forge không chạy lệnh nữa (`/api/forge/command`, `/api/forge/pipeline` trả 403 kèm lời giải thích). Lý do: pytest tự nó là chạy mã tùy ý, nên "chỉ mở pytest" không phải biên an toàn (Codex #1). Forge vẫn đọc/ghi file trong workspace ngoài CAM.
- Vai trò `task_runner` của Nano bị gỡ khỏi bảng định tuyến (mã chuyển vào `backups/`, không xóa).
- `CAM_POLICY=off` bị gỡ khỏi runtime. Test dựng chính sách riêng bằng fixture. Sửa Codex #5.
- `require_l0`, `cmd_apply` không còn nhận hàm thay thế ở đường chạy thật; test dùng monkeypatch. `apply` kiểm mã trả về của `git apply`, bắt buộc `/api/health` đạt, commit lỗi thì gỡ bản vá. Sửa Codex #6 và #11.
- Agent ngoài agent chính: trạng thái sẵn sàng có hạn 30 phút. Agent chính cũng phải qua probe. Sửa Codex #8.
- `load_policy` không bao giờ ném lỗi, kiểm kiểu từng trường; thêm `.gitattributes` để `policy/` không bị đổi xuống dòng. Sửa Codex #9, #10.

## 5. Các bước (mỗi bước 1-3 commit nhỏ trên nhánh `refactor/kernel-20261126`)

- **B0. Chuẩn bị.** Zip các file sắp sửa vào `backups/`. Tạo nhánh. Xử lý 2 bản sửa chưa commit của bên khác (policy.py, registry.py): soát, giữ phần đúng thành commit riêng ghi rõ nguồn. Xử lý thư mục `scripts/` và 2 tác vụ hẹn giờ mới theo quyết định của L0 (V8).
- **B1. Gốc dữ liệu và cô lập test (G5).** `CAM_DATA_ROOT`, plugin pytest nạp trước mọi import, `cache_dir` vào thư mục tạm, `cam_doctor` hết ghi lúc import. Nghiệm thu: chụp mtime toàn repo trước/sau cả `--collect-only` lẫn chạy đủ, 0 tệp đổi. Gộp bản vá G5 của thread "Tự động vận hành hệ CAM" nếu có.
- **B2. Cổng chạy tiến trình.** Chuyển hết hơn 20 chỗ gọi tiến trình sang `exec_gate`; tắt lệnh Forge; gỡ `task_runner`. Test tái hiện 4 đường chạy mã tùy ý, cả 4 phải bị chặn.
- **B3. Cổng API.** Token, Host, Origin, mã phép L0 cho endpoint nguy hiểm; cập nhật `templates/ui/` gửi token. Test: gọi ghi không token trả 401; PATCH `binary_path` trả 4xx và hash roster không đổi.
- **B4. Chính sách và cổng L0.** Các mục ở phần 4.
- **B5. Cổng dữ liệu ra model (G4 + G3).** Cần CUP và L0 thêm vào `v8_plan` trước, vì là module mới.
- Mỗi bước: `pytest` xanh trong sandbox, bật CAM thật bằng `run_cam_headless.bat`, kiểm `/api/health` và API vừa sửa, đo V1-V5 bằng `cam_monitor`. Ô nào đỏ thì lùi commit đó.
- Ngoài phạm vi lõi, làm sau: G6 khung chat (giao diện), G7 và G8 chỉ đọc. G2 (từ chối prop_5e5e1f1e) là việc L0 gõ mã tại bàn phím, mình chuẩn bị lệnh sẵn.

## 6. Điểm kỳ vọng (ước tính, không phải số đo)

- Hiện tại 72/100: V1 10, V2 13, V3 11, V4 14, V5 8, V6 8, V7 2, UX 6, V8 xanh.
- Sau B0-B4: V1 15 (CAM bật, smoke thật), V2 15 (test tăng, đi qua đường runtime), V3 14, V4 15, V5 13 (4 đường chạy mã đã chặn, chính sách được thi hành). Khoảng 86.
- Sau B5: V7 lên 4, V5 lên 14. Khoảng 89. UX giữ 6 cho tới khi làm G6.
- V8: thêm `cam_core/kernel/` (4 file) là khối mới, phải được L0 duyệt vào `v8_plan` cùng bản thiết kế này.

## 7. San việc cho model khác (theo ma trận đã lập)

- Mình giữ: thiết kế, tích hợp, viết mã lõi, commit, chạy CAM thật.
- Antigravity (gọi được, kiểu gửi code nhận bản vá văn bản, trên bản sao): viết test tái hiện cho từng đường tấn công và test quét mã nguồn cấm `shell=True`; mình soát rồi mới đưa vào.
- Codex: soát khác hãng lượt 2 trên diff nhỏ của nhánh, sau B2 và sau B4. Đang lỗi 401, cần L0 chạy `codex logout` rồi `codex login`.
- DeepSeek (dsh): tóm tắt log, chờ L0 nhập key.

## 8. Rủi ro

- Tắt lệnh Forge làm mất tính năng "Hội đồng tự viết code chạy test". Đây chính là đường đã làm CAM hỏng ngày 25/11, nên mình đề nghị tắt hẳn; nếu L0 cần lại thì làm sau bằng sandbox tài khoản Windows riêng.
- Token API có thể làm giao diện cũ hoặc bot Telegram gọi API lỗi 401. B3 sẽ rà mọi chỗ gọi và có test bật CAM thật.
- Gốc dữ liệu đổi cách tính đường dẫn ở nhiều file. Giá trị mặc định giữ đúng vị trí cũ, nên dữ liệu thật không phải di chuyển.
- Bên khác tiếp tục sửa repo trong lúc làm thì phải dừng lại. Cần L0 giữ Antigravity, Doctor và bot Telegram ngoài repo CAM tới khi nhánh được nghiệm thu.

## 9. L0 cần quyết

- Duyệt thiết kế này (và `cam_core/kernel/` vào `v8_plan`).
- Đồng ý tắt hẳn lệnh Forge và vai trò `task_runner`.
- Xử lý thay đổi của bên khác lúc 20:41-21:13: 2 file lõi chưa commit, thư mục `scripts/`, tác vụ hẹn giờ `CAM_Proactive_Health_Audit` và `CAM_Headless_AutoStart`.
