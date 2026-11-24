---
name: data-query
description: "Truy vấn dữ liệu lớn (JSON, CSV, JSONL) bằng SQLite ảo chỉ đọc, chống tràn context cho log backtest MQL5 và dữ liệu tick."
group: Năng suất
---

# Data Query: Virtual SQLite Engine for Large Datasets

Skill này giải quyết bài toán **tràn context window** và **sai số tính toán** khi phân tích tập dữ liệu lớn (log backtest trading, tick data, báo cáo giao dịch, API payload lớn) bằng cách nạp vào SQLite in-memory chỉ đọc và chạy truy vấn SQL chính xác.

## Khi nào dùng

- Phân tích tệp JSON, CSV, JSONL có hàng nghìn đến hàng trăm nghìn dòng (log backtest MQL5, lịch sử tick, danh sách lệnh, báo cáo doanh thu/ads lớn).
- Cần thống kê tổng hợp (`SUM`, `AVG`, `GROUP BY`, top N, lọc điều kiện) chính xác 100% mà không đẩy toàn bộ file thô vào prompt.

## Chuẩn bị

- Script thực thi: `scripts/data_query.py` (tương thích 100% Python Standard Library, không cần cài thêm package).
- Đường dẫn đầy đủ khi chạy từ plugin: `C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py`.

## Cơ chế bảng dữ liệu

1. **`records`**: Bảng chính chứa từng dòng dữ liệu (`_row` là chỉ số dòng bắt đầu từ 1). Các dict lồng nhau được làm phẳng thành cột `parent_child`.
2. **`records_<field>`**: Bảng con tự sinh cho trường là danh sách đối tượng, khóa ngoại `_record = records._row`.

## Cách chạy

### 1. Khám phá cấu trúc bảng và dữ liệu mẫu (`--describe`)
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/backtest_trades.json" `
  --describe
```

### 2. Truy vấn thống kê tổng hợp bằng SQL (`--sql`)
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/backtest_trades.json" `
  --sql "SELECT symbol, count(*) as total_trades, round(sum(profit), 2) as net_profit, round(avg(profit), 2) as avg_trade FROM records GROUP BY symbol ORDER BY net_profit DESC"
```

### 3. Xem lát cắt phân trang (`--slice`)
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/orders.csv" `
  --slice --offset 50 --limit 20 --fields "ticket,symbol,type,lots,profit"
```

### 4. Xuất JSON cho bước xử lý tiếp (`--format json`)
```powershell
python "C:\Users\Admin\.gemini\config\plugins\aio-engineer-profile\skills\data-query\scripts\data_query.py" `
  --file "path/to/trades.json" `
  --sql "SELECT symbol, sum(profit) FROM records GROUP BY symbol" `
  --format json
```

## Bẫy

- Authorizer của SQLite khóa cứng chế độ **chỉ cho phép SELECT/READ**; mọi lệnh ghi/xóa (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ATTACH`, `PRAGMA`) bị từ chối ở tầng engine.
- Đầu ra mặc định bị chặn ngưỡng `--max-chars 7000` để không làm phình context; luôn dùng `LIMIT` hoặc `GROUP BY` thay vì `SELECT *` toàn bảng.
