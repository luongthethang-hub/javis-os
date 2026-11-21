---
name: data-query
description: Truy vấn dữ liệu lớn (JSON, CSV, JSONL) bằng SQLite ảo mà không làm tràn context window của mô hình. Tối ưu cho phân tích log backtest MQL5, lịch sử tick, danh sách lệnh và dữ liệu thị trường khối lượng lớn.
---

# Data Query: Virtual SQLite Engine for Large Datasets

Skill này giải quyết triệt để bài toán **tràn context window** và **sai số tính toán** khi phân tích các tập dữ liệu lớn (vài nghìn đến hàng trăm nghìn bản ghi: log backtest trading, tick data, báo cáo giao dịch, API payload lớn).

Thay vì nạp toàn bộ file vào prompt của LLM, công cụ này tự động chuẩn hoá dữ liệu vào SQLite in-memory được bảo vệ an toàn (chỉ đọc) và cho phép thực thi truy vấn SQL để trích xuất chính xác số liệu tổng hợp.

## Vị trí công cụ

- Script thực thi: `scripts/data_query.py`
- Tương thích 100% Python Standard Library (không cần cài thêm pip packages).

## Cơ chế bảng dữ liệu

Khi nạp dữ liệu:
1. **`records`**: Bảng chính chứa từng dòng dữ liệu. `_row` là chỉ số dòng (1-based). Các dict lồng nhau được làm phẳng thành cột `parent_child`.
2. **`records_<field>`**: Bảng con được tự động tạo cho các trường là danh sách đối tượng (nested list of objects). Khóa ngoại `_record = records._row`.

## Các lệnh sử dụng phổ biến

### 1. Khám phá cấu trúc bảng và dữ liệu mẫu (`--describe`)
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/backtest_trades.json" `
  --describe
```

### 2. Truy vấn thống kê tổng hợp bằng SQL (`--sql`)
Tính tổng lợi nhuận, số lệnh thắng/thua, drawdown theo từng Symbol hoặc Strategy:
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/backtest_trades.json" `
  --sql "SELECT symbol, count(*) as total_trades, round(sum(profit), 2) as net_profit, round(avg(profit), 2) as avg_trade FROM records GROUP BY symbol ORDER BY net_profit DESC"
```

Tìm top 10 lệnh lỗ nặng nhất:
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/backtest_trades.json" `
  --sql "SELECT ticket, symbol, open_time, close_time, profit FROM records WHERE CAST(profit AS REAL) < 0 ORDER BY CAST(profit AS REAL) ASC LIMIT 10"
```

### 3. Xem lát cắt phân trang (`--slice`)
Xem nhanh 20 dòng bắt đầu từ dòng 50, chỉ lấy các cột quan trọng:
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/orders.csv" `
  --slice --offset 50 --limit 20 --fields "ticket,symbol,type,lots,profit"
```

### 4. Định dạng xuất JSON cho xử lý downstream (`--format json`)
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/trades.json" `
  --sql "SELECT symbol, sum(profit) FROM records GROUP BY symbol" `
  --format json
```

## Ràng buộc an toàn
- Authorizer của SQLite khóa cứng chế độ: **chỉ cho phép SELECT/READ**.
- Mọi câu lệnh phá hủy (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ATTACH`, `PRAGMA`) đều bị từ chối cấp độ engine.
- Đầu ra mặc định bị chặn ngưỡng ký tự (`--max-chars 7000`) để không làm phình context window.
