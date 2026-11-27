# Chặng tiếp nhận tương tác & ghi nhận câu hỏi ban đầu (Inbound Intake) - Kịch bản mô phỏng

Phạm vi: Quy trình nội bộ giả lập cho trường dạy lái xe hư cấu. Nội dung ở trạng thái CHỜ DUYỆT / CHỈ MÔ PHỎNG. Tuyệt đối không dùng dữ liệu thật, không thu thập danh tính (PII), không truy cập mạng xã hội hay liên hệ ra bên ngoài.

---

## 1. Vai trò chịu trách nhiệm
- **Người bàn giao (Chịu trách nhiệm thực hiện):** Điều phối tương tác Fanpage (Page Moderator / Interaction Coordinator).
- **Người tiếp nhận:** Bộ phận xét điều kiện tư vấn (Lead Qualifier / Tư vấn viên tuyển sinh).
- **Vai trò đối soát:** Người rà soát tính nhất quán (Consistency Reviewer), kiểm tra tính nguyên văn và ngăn ngừa suy diễn.

---

## 2. Đầu vào của chặng
- **Bài đăng nguồn mô phỏng:** `POST-DRAFT-B1-01` (Nội dung: Chuẩn bị buổi học lái B1 cuối tuần cho người bận rộn).
- **Tương tác đến giả lập (100% hư cấu, không danh tính thật):**
  - *Hình thức:* Bình luận công khai dưới bài đăng `POST-DRAFT-B1-01`.
  - *Nguyên văn câu hỏi giả lập:*
    > "Em làm văn phòng chỉ rảnh thứ Bảy và Chủ nhật, chưa từng cầm lái bao giờ. Nhờ trường tư vấn giúp em lịch học B1 cuối tuần và thủ tục đăng ký với ạ."

---

## 3. Phiếu ghi nhận tiếp nhận mô phỏng (Intake Ticket)
Điều phối Fanpage trích xuất và lập phiếu theo mẫu chuẩn:

- **Mã phiếu tiếp nhận:** `TN-B1-01`
- **Mã bài đăng nguồn:** `POST-DRAFT-B1-01`
- **Kênh tiếp nhận:** Bình luận công khai (Mô phỏng)
- **Trích dẫn nguyên văn:** "Em làm văn phòng chỉ rảnh thứ Bảy và Chủ nhật, chưa từng cầm lái bao giờ. Nhờ trường tư vấn giúp em lịch học B1 cuối tuần và thủ tục đăng ký với ạ."
- **Nhận diện thành phần quan sát được trên câu chữ:**
  - *Nhu cầu cốt lõi:* Học lái xe B1 cuối tuần (thứ Bảy, Chủ nhật), đối tượng người mới chưa từng lái.
  - *Hành động chủ động đề nghị tư vấn:* Có ("Nhờ trường tư vấn giúp em...").
  - *Kênh phản hồi mong muốn:* Chưa nêu kênh riêng (phát sinh từ bình luận).
- **Dữ liệu định danh cá nhân (PII):** Hoàn toàn không có (không họ tên, số điện thoại, địa chỉ thật).
- **Trạng thái xử lý ban đầu:** `Chuyển sang chặng xét điều kiện TV-GIALAP-XXX`.

---

## 4. Tiêu chí chuyển giao sang chặng xét điều kiện (Acceptance Criteria)
Bộ phận xét điều kiện chỉ tiếp nhận phiếu khi thỏa mãn đủ 5 tiêu chí:
1. **Tính nguyên văn:** Trích dẫn trọn vẹn câu chữ của câu hỏi giả lập, không tóm tắt hay sửa đổi ngữ nghĩa.
2. **Khớp nguồn bài viết:** Gắn đúng mã bài viết nguồn `POST-DRAFT-B1-01` để bảo đảm mạch nội dung xuyên suốt.
3. **Có hành động yêu cầu tư vấn rõ ràng:** Câu hỏi có chứa từ khóa chủ động đề nghị tư vấn ("tư vấn giúp em..."), phân biệt rõ với nhóm chỉ tương tác xã giao hay hỏi mẹo thuần túy.
4. **Không suy diễn thông tin:** Không tự điền số điện thoại, ngân sách, địa điểm hay cam kết lịch học khi người hỏi chưa đề cập.
5. **Tuân thủ an toàn dữ liệu:** Không chứa dữ liệu thật hay cam kết vượt quyền của nhà trường.

*Nếu thiếu một trong các tiêu chí trên, phiếu giữ ở trạng thái "Chưa chuyển - Giữ ở luồng tương tác công khai", không bàn giao sang bộ phận xét tư vấn.*

---

## 5. Dòng tóm tắt chặng (One-line handoff summary)
`[Chặng Tiếp nhận: Inbound Intake] | Vai trò: Điều phối Fanpage bàn giao cho Bộ phận xét điều kiện | Đầu vào: Bình luận dưới bài POST-DRAFT-B1-01 | Đầu ra: Phiếu tiếp nhận TN-B1-01 trích nguyên văn câu hỏi giả lập | Tiêu chí nhận việc: Đủ 5 mục (trích nguyên văn, đúng bài nguồn, có đề nghị tư vấn, không suy diễn, không PII).`
