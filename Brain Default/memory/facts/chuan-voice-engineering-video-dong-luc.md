---
type: preference
created: 2026-11-23
updated: 2026-11-23
source: chat 2026-11-23 (00:21, nguồn log memory/conversations/2026-11-23.md); duyệt "y" của Thắng Lee trong phiên Claude Desktop 23/11
status: confirmed-by-owner, chua-kiem-chung-chay-lai
---
Chuẩn xử lý giọng đọc cho video ngắn thể loại động lực/bản lĩnh/chiến binh (kết hợp Quy trình B Voice-First, xem [[quy-trinh-tao-video-voice-first]]).

**Chuẩn giọng**
- Giọng nam `vi-VN-NamMinhNeural`, rate -3%, pitch -6Hz.
- Chuỗi DSP FFmpeg tạo độ khàn và nội lực: hạ tông bằng `asetrate` 1.5 bán âm (vùng 100-110Hz), boost +5.5 dB tại 125Hz, `treble` 6000Hz +4.0 dB kết hợp `aexciter`, nén dải động `compand`.

**Bẫy kỹ thuật Azure TTS**
- Lỗi `NoAudioReceived` do chữ `Đ` viết hoa đầu câu và một số từ nhạy cảm trong bộ lọc. Cách xử lý: chuẩn hóa kịch bản sang cụm từ hành động đanh thép.

**Phạm vi áp dụng:** video động lực/bản lĩnh có giọng đọc. Không áp dụng mặc định cho video review sản phẩm POV (không lời, ASMR).

**Ghi chú xác minh:** thông số lấy từ log phiên 23/11 (Javis tự báo kết xuất bản V2 `dong_luc_nguoi_que_v2.mp4`). Javis báo đã ghi vào `skills/openmotion/SKILL.md` và wiki nhưng chưa có bằng chứng: `wiki/log.md` không có entry 23/11. Cần mở `SKILL.md` để đối chiếu.
