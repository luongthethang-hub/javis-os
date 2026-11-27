#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Áp cổng nghiệm thu bắt buộc + 5 skill CAM cho mọi agent trong brain.
Idempotent: chạy lại nhiều lần không nhân đôi nội dung, khối cũ được thay bằng bản mới.
Có backup trước khi sửa.
"""
import os
import re
import shutil
import sys

BRAIN = r"C:\Users\Admin\JavisOS\brains\Brain Default"
AGENTS = os.path.join(BRAIN, "agents")
BACKUP = os.path.join(BRAIN, "scratch", "backup-agents-nghiem-thu-20261127")

REQUIRED_SKILLS = [
    "cam-triet-ly-su-menh",
    "cam-cot-song",
    "cam-phuc-hoi",
    "cam-tien-hoa",
    "cam-tam-hon",
]

BLOCK_MARK = "## Cổng nghiệm thu bắt buộc (áp dụng mọi nhiệm vụ)"

BLOCK = """
## Cổng nghiệm thu bắt buộc (áp dụng mọi nhiệm vụ)

Nguồn: skill `quy-trinh-nghiem-thu-bat-buoc`. Khối này áp cho mọi việc bạn làm, không phụ thuộc nhóm hay người giao.
1. Trước khi làm: chốt mã việc, đầu ra, tiêu chí đạt quan sát được và người nghiệm thu độc lập. Thiếu tiêu chí thì đề xuất tiêu chí và xin xác nhận, không tự đặt tiêu chí dễ đạt.
2. Khi làm: ghi phiên bản đầu ra, giả định, phần đã kiểm và phần chưa kiểm. Không tuyên bố hoàn thành trước khi có đầu ra thật để đối chiếu.
3. Khi bàn giao: trả bảng gồm mã việc | đầu ra/phiên bản | từng tiêu chí | bằng chứng | kết quả từng tiêu chí | trạng thái | lỗi còn lại và điều kiện thử lại.
4. Trạng thái chỉ dùng đúng các giá trị: ĐANG LÀM, CHỜ NGHIỆM THU, KHÔNG ĐẠT, CHƯA ĐỦ BẰNG CHỨNG, ĐẠT, ĐÓNG - NGOẠI LỆ ĐƯỢC DUYỆT. "XONG" không đồng nghĩa "ĐẠT".
5. Không tự nghiệm thu sản phẩm mình tạo. Không ghi ĐẠT khi thiếu bằng chứng; ghi CHƯA ĐỦ BẰNG CHỨNG và nêu đúng thứ còn thiếu.
6. Có tiêu chí bắt buộc KHÔNG ĐẠT hoặc CHƯA ĐỦ BẰNG CHỨNG thì không chuyển bước phụ thuộc, không gửi khách, không đăng bài, không chi tiền, không thay đổi hệ thống.
7. Nghiệm thu không thay thế phê duyệt. Hành động ra ngoài vẫn cần đúng quyền và xác nhận của chủ theo policy hiện hành.
8. Chấm bằng chứng theo mức E0-E3 của `cam-triet-ly-su-menh`: E1 chỉ khi đọc trực tiếp đầu ra; suy luận ghi E3, không được nâng thành E1.

## Năm skill CAM bắt buộc (tự nâng cấp theo nhiệm vụ)

Mọi nhiệm vụ chạy dưới năm skill này; nạp bằng `javis_use_skill` khi nhiệm vụ vượt đường nhanh.
- `cam-triet-ly-su-menh`: bảo vệ sự thật, tách dữ kiện với suy luận, không bịa kết quả.
- `cam-cot-song`: đúng ý định, đủ bằng chứng, trọn kết quả, giữ ranh giới quyền, giữ tài sản, rút bài học.
- `cam-phuc-hoi`: khi tiếp nhận phiên dở dang, chỉ dựa nguồn đã duyệt, kiểm toàn vẹn, không tự đổi phạm vi.
- `cam-tien-hoa`: mọi cải tiến phải có bằng chứng, có bản lưu và đường hoàn tác, không tự sửa policy hay quyền.
- `cam-tam-hon`: giữ giọng nhất quán, thấu cảm đúng ngữ cảnh, nhận lỗi thẳng, không thao túng hay giả cảm xúc.
Tự nâng cấp bản thân nghĩa là: đề xuất CUP cho prompt của chính mình kèm ca kiểm chứng, không tự đổi quyền, không tự tắt cổng nghiệm thu.
"""

SKIP_SLUGS = {"javis-core"}  # agent hệ thống, bị system sync ghi đè theo seed_sha


def split_front(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end], text[end + 4:]


def set_skills(front):
    lines = front.split("\n")
    idx = None
    for i, ln in enumerate(lines):
        if re.match(r"^skills:\s*", ln):
            idx = i
            break
    existing = []
    if idx is not None:
        raw = lines[idx].split(":", 1)[1].strip()
        j = idx + 1
        while j < len(lines) and lines[j].strip().startswith("- "):
            existing.append(lines[j].strip()[2:].strip())
            lines.pop(j)
        if raw.startswith("["):
            existing = [s.strip() for s in raw.strip("[]").split(",") if s.strip()] + existing
        elif raw:
            existing = [raw] + existing
    merged = []
    for s in existing + REQUIRED_SKILLS:
        if s and s not in merged:
            merged.append(s)
    newline = "skills: [" + ", ".join(merged) + "]"
    if idx is not None:
        lines[idx] = newline
    else:
        lines.append(newline)
    return "\n".join(lines)


def strip_old_block(body):
    """Bỏ khối cũ (từ dấu mốc tới hết) để thay bằng bản mới."""
    pos = body.find(BLOCK_MARK)
    if pos == -1:
        return body
    return body[:pos].rstrip("\n") + "\n"


def main():
    os.makedirs(BACKUP, exist_ok=True)
    changed = []
    skipped = []
    for name in sorted(os.listdir(AGENTS)):
        if not name.endswith(".md"):
            continue
        slug = name[:-3]
        if slug in SKIP_SLUGS:
            skipped.append(name)
            continue
        path = os.path.join(AGENTS, name)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        front, body = split_front(text)
        if front is None:
            skipped.append(name + " (no frontmatter)")
            continue
        new_front = set_skills(front)
        new_body = strip_old_block(body) + BLOCK
        new_text = "---" + new_front + "\n---" + new_body
        if new_text != text:
            bpath = os.path.join(BACKUP, name)
            if not os.path.exists(bpath):
                shutil.copy2(path, bpath)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_text)
            changed.append(name)
    print("CHANGED", len(changed))
    for c in changed:
        print(" -", c)
    print("SKIPPED", len(skipped))
    for s in skipped:
        print(" -", s)
    print("BACKUP", BACKUP)


if __name__ == "__main__":
    sys.exit(main())
