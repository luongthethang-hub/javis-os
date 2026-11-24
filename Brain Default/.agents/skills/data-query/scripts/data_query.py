#!/usr/bin/env python3
"""
data_query.py: Trình truy vấn dữ liệu lớn (JSON / CSV / JSONL) bằng SQLite ảo.
Trích xuất từ kiến trúc tool_result_query của Javis OS, tối ưu hóa cho Antigravity.
Giải quyết triệt để bài toán tràn context window và sai số khi phân tích log backtest,
tick data hoặc báo cáo giao dịch khối lượng lớn.
Zero-dependency (chỉ dùng Python standard library).
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MAX_OUTPUT_CHARS = 7000
MAX_ROWS_OUT = 200
SQL_TIMEOUT_S = 10.0


def _clean_col_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", str(name).strip()).strip("_")
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"col_{cleaned}"
    return cleaned.lower()


def _flatten_record(record: dict, prefix: str = "") -> Tuple[dict, dict]:
    """Tách 1 bản ghi thành: (cột phẳng cho records, các list đối tượng con cho bảng phụ)."""
    flat = {}
    children = {}

    for k, v in record.items():
        col = f"{prefix}_{k}" if prefix else k
        col_clean = _clean_col_name(col)

        if isinstance(v, dict):
            sub_flat, sub_children = _flatten_record(v, prefix=col_clean)
            flat.update(sub_flat)
            children.update(sub_children)
        elif isinstance(v, list):
            if v and isinstance(v[0], dict):
                children[col_clean] = v
            else:
                flat[col_clean] = json.dumps(v, ensure_ascii=False)
                flat[f"{col_clean}_count"] = len(v)
        else:
            flat[col_clean] = v

    return flat, children


def _load_data_source(file_path: Optional[str], raw_data: Optional[str], json_path: Optional[str]) -> List[dict]:
    content = ""
    if file_path:
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
        content = p.read_text(encoding="utf-8", errors="replace").strip()
    elif raw_data:
        content = raw_data.strip()
    else:
        content = sys.stdin.read().strip()

    if not content:
        return []

    # Thử parse JSON
    if content.startswith("{") or content.startswith("["):
        try:
            parsed = json.loads(content)
            if json_path:
                parts = [x for x in json_path.strip("/").split("/") if x]
                curr = parsed
                for part in parts:
                    if isinstance(curr, dict) and part in curr:
                        curr = curr[part]
                    elif isinstance(curr, list) and part.isdigit() and int(part) < len(curr):
                        curr = curr[int(part)]
                    else:
                        break
                parsed = curr

            if isinstance(parsed, list):
                return [x for x in parsed if isinstance(x, dict)]
            elif isinstance(parsed, dict):
                # Tự động tìm mảng bản ghi đầu tiên nếu không chỉ định json_path
                for val in parsed.values():
                    if isinstance(val, list) and val and isinstance(val[0], dict):
                        return val
                return [parsed]
        except Exception:
            pass

    # Thử parse JSONL
    if "\n" in content and (content.startswith("{") or "{" in content):
        records = []
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    records.append(item)
            except Exception:
                continue
        if records:
            return records

    # Thử parse CSV
    try:
        reader = csv.DictReader(io.StringIO(content))
        return list(reader)
    except Exception:
        raise ValueError("Không nhận diện được định dạng dữ liệu (yêu cầu JSON, JSONL hoặc CSV).")


def _build_database(records: List[dict]) -> Tuple[sqlite3.Connection, List[str]]:
    conn = sqlite3.connect(":memory:")
    child_tables = set()

    if not records:
        conn.execute("CREATE TABLE records (_row INTEGER PRIMARY KEY)")
        return conn, []

    # Phân tích schema của bảng chính và các bảng con
    flat_rows = []
    child_rows: Dict[str, List[dict]] = {}

    for idx, r in enumerate(records, start=1):
        flat, children = _flatten_record(r)
        flat["_row"] = idx
        flat_rows.append(flat)

        for child_name, items in children.items():
            child_tables.add(child_name)
            child_rows.setdefault(child_name, [])
            for c_idx, c_item in enumerate(items, start=1):
                c_flat, _ = _flatten_record(c_item)
                c_flat["_record"] = idx
                c_flat["_child_row"] = c_idx
                child_rows[child_name].append(c_flat)

    # 1. Tạo bảng chính: records
    all_cols = set()
    for row in flat_rows:
        all_cols.update(row.keys())
    col_list = sorted([c for c in all_cols if c != "_row"])
    col_defs = ["_row INTEGER PRIMARY KEY"] + [f'"{c}" TEXT' for c in col_list]
    conn.execute(f"CREATE TABLE records ({', '.join(col_defs)})")

    # Insert vào bảng chính
    for row in flat_rows:
        present_cols = [c for c in row if c in all_cols]
        placeholders = ", ".join(["?"] * len(present_cols))
        col_names = ", ".join([f'"{c}"' for c in present_cols])
        vals = [str(row[c]) if row[c] is not None else None for c in present_cols]
        conn.execute(f"INSERT INTO records ({col_names}) VALUES ({placeholders})", vals)

    # 2. Tạo các bảng con
    for child_name, rows in child_rows.items():
        c_cols = set()
        for r in rows:
            c_cols.update(r.keys())
        c_col_list = sorted([c for c in c_cols if c not in ("_record", "_child_row")])
        c_col_defs = ["_record INTEGER", "_child_row INTEGER"] + [f'"{c}" TEXT' for c in c_col_list]
        conn.execute(f"CREATE TABLE records_{child_name} ({', '.join(c_col_defs)})")

        for r in rows:
            present_c = [c for c in r if c in c_cols]
            c_placeholders = ", ".join(["?"] * len(present_c))
            c_col_names = ", ".join([f'"{c}"' for c in present_c])
            c_vals = [str(r[c]) if r[c] is not None else None for c in present_c]
            conn.execute(f"INSERT INTO records_{child_name} ({c_col_names}) VALUES ({c_placeholders})", c_vals)

    conn.commit()

    # Thiết lập Authorizer: CHỈ CHO PHÉP ĐỌC
    def authorizer(action, arg1, arg2, dbname, source):
        # 1 = SQLITE_SELECT, 21 = SQLITE_READ, 31 = SQLITE_FUNCTION
        if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION):
            return sqlite3.SQLITE_OK
        # Cho phép đọc schema qua PRAGMA table_info
        if action == getattr(sqlite3, "SQLITE_PRAGMA", 19) and str(arg1).lower() in ("table_info", "table_xinfo"):
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY

    conn.set_authorizer(authorizer)
    return conn, sorted(list(child_tables))


def _format_markdown_table(headers: List[str], rows: List[List[Any]]) -> str:
    if not headers or not rows:
        return "*(Không có dữ liệu)*"

    str_rows = [[str(val if val is not None else "") for val in row] for row in rows]
    widths = [len(h) for h in headers]
    for row in str_rows:
        for idx, val in enumerate(row):
            widths[idx] = max(widths[idx], len(val))

    header_line = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    sep_line = "|-" + "-|-".join("-" * widths[i] for i in range(len(headers))) + "-|"
    data_lines = ["| " + " | ".join(val.ljust(widths[i]) for i, val in enumerate(row)) + " |" for row in str_rows]

    return "\n".join([header_line, sep_line] + data_lines)


def run_describe(conn: sqlite3.Connection, child_tables: List[str]) -> dict:
    tables = ["records"] + [f"records_{c}" for c in child_tables]
    info = {}

    for t in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        cursor = conn.execute(f"PRAGMA table_info({t})")
        cols = [row[1] for row in cursor.fetchall()]

        samples = []
        if count > 0:
            sample_cursor = conn.execute(f"SELECT * FROM {t} LIMIT 3")
            sample_rows = sample_cursor.fetchall()
            samples = [dict(zip(cols, s)) for s in sample_rows]

        info[t] = {
            "total_rows": count,
            "columns": cols,
            "sample_records": samples,
        }

    return info


def run_sql(conn: sqlite3.Connection, sql: str, max_chars: int = MAX_OUTPUT_CHARS, fmt: str = "table") -> str:
    # Basic check against mutation keywords
    sql_check = sql.strip().lower()
    if not (sql_check.startswith("select") or sql_check.startswith("with")):
        raise ValueError("Chỉ hỗ trợ câu lệnh SELECT (hoặc CTE WITH ... SELECT).")

    cursor = conn.cursor()
    cursor.execute(sql)
    headers = [d[0] for d in cursor.description] if cursor.description else []
    rows = cursor.fetchmany(MAX_ROWS_OUT)

    if fmt == "json":
        res_list = [dict(zip(headers, r)) for r in rows]
        out_text = json.dumps(res_list, indent=2, ensure_ascii=False)
    else:
        out_text = _format_markdown_table(headers, rows)

    if len(out_text) > max_chars:
        out_text = out_text[:max_chars] + f"\n\n*(Kết quả bị giới hạn tại {max_chars} ký tự để bảo toàn context window)*"

    return out_text


def run_slice(conn: sqlite3.Connection, offset: int, limit: int, fields: Optional[List[str]], fmt: str = "table") -> str:
    cols_clause = ", ".join([f'"{f}"' for f in fields]) if fields else "*"
    sql = f"SELECT {cols_clause} FROM records LIMIT {limit} OFFSET {offset}"
    return run_sql(conn, sql, fmt=fmt)


def main():
    parser = argparse.ArgumentParser(description="Data Query: SQLite Virtual Engine for Large Data")
    parser.add_argument("--file", help="Đường dẫn file dữ liệu (JSON, CSV, JSONL)")
    parser.add_argument("--data", help="Dữ liệu dạng chuỗi JSON thô")
    parser.add_argument("--path", help="JSON pointer tới mảng dữ liệu (vd: /data hoặc /trades)")
    parser.add_argument("--describe", action="store_true", help="Hiển thị cấu trúc bảng và dữ liệu mẫu")
    parser.add_argument("--sql", help="Câu lệnh SELECT truy vấn dữ liệu")
    parser.add_argument("--slice", action="store_true", help="Xem lát cắt phân trang")
    parser.add_argument("--offset", type=int, default=0, help="Vị trí bắt đầu xem phân trang")
    parser.add_argument("--limit", type=int, default=20, help="Số dòng xem phân trang")
    parser.add_argument("--fields", help="Danh sách cột cần xem (phân cách bằng dấu phẩy)")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Định dạng kết quả xuất")
    parser.add_argument("--max-chars", type=int, default=MAX_OUTPUT_CHARS, help="Giới hạn ký tự tối đa của đầu ra")

    args = parser.parse_args()

    try:
        records = _load_data_source(args.file, args.data, args.path)
        conn, child_tables = _build_database(records)

        if args.describe:
            info = run_describe(conn, child_tables)
            print(json.dumps(info, indent=2, ensure_ascii=False))
        elif args.sql:
            print(run_sql(conn, args.sql, max_chars=args.max_chars, fmt=args.format))
        elif args.slice:
            fields_list = [f.strip() for f in args.fields.split(",")] if args.fields else None
            print(run_slice(conn, args.offset, args.limit, fields_list, fmt=args.format))
        else:
            # Mặc định thực hiện describe
            info = run_describe(conn, child_tables)
            print(json.dumps(info, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Lỗi truy vấn: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
