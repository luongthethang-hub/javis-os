---
id: ping-001
from: javis
risk: low
hop: 1
---

## Mục tiêu
Kiểm tra kết nối và khả năng thực thi tác vụ hai chiều giữa Javis và Claude Desktop qua giao thức a2a.

## Đầu vào
Không có.

## Tiêu chí hoàn thành
1. Đọc nội dung file này bằng `javis_read_file`.
2. Dùng công cụ `javis_write_file` để ghi file `memory/a2a_bus/claude/res-ping-001.md` với nội dung chuẩn Markdown:
```markdown
---
id: ping-001
status: done
evidence: memory/a2a_bus/claude/res-ping-001.md
---
Ping thành công. Kết nối a2a giữa Javis và Claude Desktop hoạt động bình thường.
```
3. Sau khi ghi file thành công, phản hồi đúng 1 dòng trạng thái: `DONE: res-ping-001.md da duoc tao.`
