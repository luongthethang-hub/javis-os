"""Validated import and versioned, memory-mapped tick storage."""

import csv
import hashlib
import json
import mmap
import re
import struct
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from math import isfinite
from pathlib import Path
from tempfile import TemporaryDirectory

RECORD = struct.Struct("<qqqqQId")
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
MAX_TIME = 253402300799999
MAX_PRICE = 10**14


def epoch_ms(moment):
    delta = moment - EPOCH
    return delta // timedelta(milliseconds=1)


def iso_datetime(value):
    moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if moment.utcoffset() is None or moment.microsecond % 1000:
        raise ValueError("Thời gian ISO phải có timezone và độ chính xác tối đa 1 ms.")
    return moment


def price_units(value, scale):
    decimal = Decimal(str(value))
    if not decimal.is_finite() or decimal < 0 or decimal > MAX_PRICE:
        raise ValueError("Giá nằm ngoài miền hỗ trợ.")
    numerator, denominator = decimal.as_integer_ratio()
    units, rest = divmod(numerator * scale, denominator)
    if rest or units > MAX_PRICE:
        raise ValueError("Giá vượt độ chính xác hoặc giới hạn của bộ dữ liệu.")
    return units


def checked_tick(time_ms, bid, ask, last, volume, flags, volume_real):
    if not 0 < time_ms <= MAX_TIME:
        raise ValueError("time_msc nằm ngoài miền hỗ trợ.")
    if bid and ask and ask < bid:
        raise ValueError("Ask thấp hơn Bid.")
    if not 0 <= volume < 2**64 or not 0 <= flags < 2**32:
        raise ValueError("volume hoặc flags nằm ngoài miền hỗ trợ.")
    if not isfinite(volume_real) or volume_real < 0:
        raise ValueError("volume_real phải hữu hạn và không âm.")
    return time_ms, bid, ask, last, volume, flags, volume_real


def csv_rows(path, digits, utc_offset):
    scale = 10**digits
    with path.open("rb") as raw:
        bom = raw.read(3)
    encoding = "utf-16" if bom.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
    with path.open(encoding=encoding, newline="") as source:
        first = source.readline()
        delimiter = next((ch for ch in ("\t", ";", ",") if ch in first), ",")
        source.seek(0)
        reader = csv.reader(source, delimiter=delimiter, strict=True)
        headers = [name.strip().strip("<>").lower() for name in next(reader, [])]
        fields = set(headers)
        native = {"date", "time"} <= fields
        required = {"bid", "ask"} | ({"date", "time"} if native else {"time_msc"})
        if not required <= fields or len(fields) != len(headers):
            raise ValueError("Cần cột time_msc,bid,ask hoặc DATE,TIME,BID,ASK của MT5.")
        if native and utc_offset is None:
            raise ValueError("CSV MT5 cần --utc-offset, ví dụ +02:00, cho đoạn có offset cố định.")
        zone = None
        if native:
            if not re.fullmatch(r"[+-](?:[01][0-9]|2[0-3]):[0-5][0-9]", utc_offset):
                raise ValueError("--utc-offset phải có dạng +HH:MM hoặc -HH:MM.")
            signed = 1 if utc_offset[0] == "+" else -1
            zone = timezone(signed * timedelta(hours=int(utc_offset[1:3]), minutes=int(utc_offset[4:])))
        previous = (0, 0, 0)
        for row in reader:
            if not row or all(not item.strip() for item in row):
                continue
            try:
                if len(row) != len(headers):
                    raise ValueError("Sai số lượng cột.")
                data = dict(zip(headers, (item.strip() for item in row)))
                raw_flags = data.get("flags", "") or "0"
                flags = int(raw_flags, 16 if raw_flags.lower().startswith("0x") else 10)
                if native:
                    entry = f"{data['date']} {data['time']}"
                    pattern = "%Y.%m.%d %H:%M:%S"
                    if "." in data["time"]:
                        pattern += ".%f"
                    moment = datetime.strptime(entry, pattern).replace(tzinfo=zone)
                    if moment.microsecond % 1000:
                        raise ValueError("Tick có độ chính xác nhỏ hơn 1 ms.")
                    time_ms = epoch_ms(moment)
                else:
                    time_ms = int(data["time_msc"])

                prices = []
                for i, (key, bit) in enumerate((("bid", 2), ("ask", 4), ("last", 8))):
                    value = data.get(key, "")
                    if not value and not native and key in ("bid", "ask"):
                        raise ValueError(f"Cột {key} trống. Dùng 0 cho quote không khả dụng.")
                    units = price_units(value, scale) if value else 0
                    if not value and native and not flags & bit:
                        units = previous[i]
                    prices.append(units)
                previous = tuple(prices)
                real = data.get("volume_real", "") or data.get("volume", "") or "0"
                size = Decimal(real)
                if not size.is_finite() or size < 0 or size >= 2**64:
                    raise ValueError("Volume nằm ngoài miền hỗ trợ.")
                raw_volume = data.get("volume", "")
                base_volume = Decimal(raw_volume) if raw_volume else Decimal(0)
                if not base_volume.is_finite() or base_volume < 0 or base_volume >= 2**64:
                    raise ValueError("Volume nằm ngoài miền hỗ trợ.")
                if not native and base_volume != int(base_volume):
                    raise ValueError("Cột volume cần là số nguyên. Dùng volume_real cho phần lẻ.")
                yield checked_tick(time_ms, *prices, int(base_volume), flags, float(size))
            except (ValueError, ArithmeticError) as exc:
                raise ValueError(f"CSV dòng {reader.line_num}: {exc}") from exc


def mt5_import(terminal, symbol, date_from, date_to, chunk_minutes, timeout_ms, output):
    try:
        import MetaTrader5 as mt5
    except ImportError as exc:
        raise ValueError("Cần gói MetaTrader5 cho lệnh import-mt5. Có thể dùng import-csv.") from exc
    if not terminal.is_file():
        raise ValueError("Không tìm thấy terminal64.exe tại đường dẫn đã cho.")
    start = epoch_ms(date_from)
    end = epoch_ms(date_to)
    if not 0 < start < end <= MAX_TIME:
        raise ValueError("Cần khoảng thời gian dương [from, to).")
    if output.exists():
        raise FileExistsError(f"Thư mục đầu ra đã tồn tại: {output}")
    if not mt5.initialize(str(terminal), timeout=timeout_ms):
        raise ValueError(f"MetaTrader5 initialize thất bại: {mt5.last_error()}")
    try:
        info = mt5.symbol_info(symbol)
        if info is None or not info.visible:
            raise ValueError("Cần symbol chính xác đang hiển thị trong Market Watch.")
        if not 0 <= info.digits <= 10:
            raise ValueError("Digits nằm ngoài miền hỗ trợ.")
        scale = 10**info.digits
        terminal_info = mt5.terminal_info()
        if terminal_info is None:
            raise ValueError(f"Không đọc được terminal_info: {mt5.last_error()}")
        meta = {
            "source_type": "mt5-copy_ticks_range",
            "terminal_build": int(terminal_info.build),
            "package_version": mt5.__version__,
            "requested_start_ms": start,
            "requested_end_ms_exclusive": end,
            "chart_mode": int(info.chart_mode),
            "time_basis": "mt5-api-time_msc",
            "empty_windows": 0,
            "requested_windows": 0,
        }

        def rows():
            span = chunk_minutes * 60_000
            for left in range(start, end, span):
                right = min(end, left + span)
                # Python binding accepts datetimes at second granularity on some builds.
                low = EPOCH + timedelta(seconds=left // 1000)
                high = EPOCH + timedelta(seconds=(right - 1) // 1000 + 1)
                batch = mt5.copy_ticks_range(symbol, low, high, mt5.COPY_TICKS_ALL)
                meta["requested_windows"] += 1
                code, detail = mt5.last_error()
                if batch is None or code != 1:
                    raise ValueError(f"MetaTrader5 copy_ticks_range thất bại tại {low.isoformat()}: {(code, detail)}")
                accepted = 0
                for tick in batch:
                    stamp = int(tick["time_msc"])
                    if not left <= stamp < right:
                        continue
                    accepted += 1
                    yield checked_tick(
                        stamp, price_units(tick["bid"], scale), price_units(tick["ask"], scale),
                        price_units(tick["last"], scale), int(tick["volume"]), int(tick["flags"]),
                        float(tick["volume_real"]),
                    )
                if not accepted:
                    meta["empty_windows"] += 1

        return write_dataset(output, symbol, int(info.digits), rows(), meta)
    finally:
        mt5.shutdown()


def write_dataset(output, symbol, digits, rows, source):
    if not symbol.strip() or len(symbol) > 80 or not 0 <= digits <= 10:
        raise ValueError("Cần symbol dài 1-80 ký tự và digits từ 0 đến 10.")
    if output.exists():
        raise FileExistsError(f"Thư mục đầu ra đã tồn tại: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".tick-import-", dir=output.parent) as temp:
        stage = Path(temp) / "data"
        stage.mkdir()
        digest = hashlib.sha256()
        first = last = count = valid = repeats = max_gap = 0
        with (stage / "ticks.bin").open("wb", buffering=1024 * 1024) as ticks:
            for row in rows:
                time_ms, bid, ask, *_ = row
                if time_ms < last:
                    raise ValueError(f"Tick thứ {count + 1} sai thứ tự thời gian.")
                raw = RECORD.pack(*row)
                ticks.write(raw)
                digest.update(raw)
                if count:
                    repeats += time_ms == last
                    max_gap = max(max_gap, time_ms - last)
                first = first or time_ms
                last = time_ms
                count += 1
                valid += bool(bid and ask)
        if not count or not valid:
            raise ValueError("Không có tick với cả Bid và Ask khả dụng.")
        manifest = {
            "format": 1, "record_bytes": RECORD.size, "symbol": symbol, "digits": digits,
            "ticks": count, "valid_quotes": valid, "same_ms_transitions": repeats,
            "max_gap_ms_including_closures": max_gap, "first_ms": first, "last_ms": last,
            "sha256": digest.hexdigest(), "source": source,
        }
        (stage / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        stage.rename(output)
    return manifest


@contextmanager
def read_dataset(directory):
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if (manifest.get("format") != 1 or manifest.get("record_bytes") != RECORD.size
            or not isinstance(manifest.get("ticks"), int) or manifest["ticks"] < 1
            or not isinstance(manifest.get("digits"), int) or not 0 <= manifest["digits"] <= 10):
        raise ValueError("Manifest tick không tương thích.")
    with (directory / "ticks.bin").open("rb") as file:
        expected_size = manifest["ticks"] * RECORD.size
        if file.seek(0, 2) != expected_size:
            raise ValueError("Kích thước ticks.bin lệch manifest.")
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mapped:
            yield manifest, mapped

