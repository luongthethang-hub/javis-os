---
slug: luat-phong-giam-doc-20261126
title: Luật làm việc chung Phòng Giám Đốc (bài học chung 26/11/2026)
type: rule
memory_tier: T1
provenance: darklord-distilled
evidence: E2
created: 2026-11-26
updated: 2026-11-26
decay_days: 365
tags: [fact, lien-minh-ai, phoi-hop, bai-hoc, an-toan, cam-os]
source: "project-files cam-van-hanh/bai-hoc-chung-20261126.md (Darklord, 26/11 ~18:30)"
---

# Luật làm việc chung Phòng Giám Đốc (cập nhật 26/11/2026)

Khối luật do Darklord chưng cất từ sự cố trong ngày, áp cho mọi thành viên. Khối này chỉ được THÊM, không xóa luật cũ.

1. Mỗi repo chỉ một bên được ghi. Bên khác chỉ đọc, quét, soát, hoặc soạn bản vá trên BẢN SAO (ví dụ `D:\AI AGENT\cam-banvao-ag`) để bên giữ quyền ghi duyệt.
2. Lượt kiểm tra/giám sát chỉ đọc: không chạy pytest (kể cả `--collect-only`, vì nó ghi `logs/repair_packet.md`), không gọi `cam_monitor measure`, không bật CAM.
3. Trước khi giao việc cho một thợ, gọi thử một lần bằng prompt vô hại ("Reply with OK"). Không gọi được thì đánh dấu "chờ đường gọi", không âm thầm làm thay.
4. Antigravity headless (`agy -p`) không được duyệt công cụ và máy không có terminal sandbox: chỉ giao việc "sinh văn bản" (nhận code trong prompt, trả unified diff hoặc bảng); bên gọi tự áp và chạy test trên bản sao. Không dùng `--dangerously-skip-permissions` cho việc giao từ CAM.
5. Codex: luôn gọi `-s read-only` khi soát (config mặc định đang là danger-full-access).
6. Phân tích/thiết kế: người viết và người soát khác hãng; L0 nghiệm thu cuối. "Xong" chưa phải "Đạt".
7. Không gửi dữ liệu S2 (`brains/`, accounts_pool, `*.db`, owner_feedback) hay S3 (key, token, mật khẩu) tới model hosted. Không in, không đọc file chứa key.
8. Sau khi máy khởi động lại: kiểm tiến trình chạy trùng (bridge.py bật cả từ Run key lẫn Startup) và tác vụ hẹn giờ lỗi (Sync_4h 0x800710E0).
9. Việc xong, quyết định L0, sự cố: ghi vào Sổ Cái, xem [[so-cai-he-log-chung]].
10. Sửa file nào cũng sao lưu trước (`.bak` kèm giờ) và ghi cách lùi.

## Mâu thuẫn
- Bản gốc luật 1 ghi "CAM OS chỉ Doctor Agent sửa và commit". Từ 18:31 L0 cho thread Darklord "Tái cấu trúc lõi CAM OS" giữ quyền ghi (Sổ Cái `khoa-ghi:cam-os = dang-giu`), xem [[quyet-dinh-l0-20261126]] mục 4-6. Đọc luật 1 là "chỉ bên đang giữ `khoa-ghi:cam-os`". Hai cách viết giữ nguyên cả hai; L0 quyết hợp nhất.
- Trạng thái áp dụng thực tế: ghi khối này vào `~/.codex/AGENTS.md` và luật plugin của agy bị chặn lúc 21:25, nên Codex/Antigravity chưa nạp bản này.
