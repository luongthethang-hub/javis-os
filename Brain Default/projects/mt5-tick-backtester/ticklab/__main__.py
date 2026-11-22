"""CLI for import, verification, simulation and comparison."""
import argparse
import csv
import hashlib
import json
import statistics
import sys
from dataclasses import asdict
from itertools import zip_longest
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

from . import __version__
from .data import csv_rows, epoch_ms, iso_datetime, mt5_import, read_dataset, write_dataset
from .replay import PARITY_FIELDS, TRADE_FIELDS, Settings, replay


def show(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))


def range_args(parser):
    parser.add_argument("--from", dest="start", type=iso_datetime)
    parser.add_argument("--to", dest="end", type=iso_datetime)


def replay_args(parser):
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--bar-minutes", type=int, default=1)
    parser.add_argument("--fast", type=int, default=2)
    parser.add_argument("--slow", type=int, default=3)
    parser.add_argument("--stop-points", type=int, default=100)
    parser.add_argument("--target-points", type=int, default=150)
    parser.add_argument("--slippage-points", type=int, default=0)
    parser.add_argument("--fee-points", type=int, default=0)
    parser.add_argument("--direction", choices=("both", "long", "short"), default="both")
    range_args(parser)


def report(directory, manifest, mapped, settings, limits):
    if directory.exists():
        raise FileExistsError(f"Thư mục đầu ra đã tồn tại: {directory}")
    directory.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".tick-run-", dir=directory.parent) as temp:
        stage = Path(temp) / "run"
        stage.mkdir()
        with (stage / "trades.csv").open("w", encoding="utf-8", newline="") as ledger:
            writer = csv.writer(ledger)
            writer.writerow(TRADE_FIELDS)
            started = perf_counter()
            metrics = replay(mapped, settings, writer.writerow, start_ms=limits[0], end_ms=limits[1])
            elapsed = perf_counter() - started
        candles = metrics.pop("bars_tail")
        markers = metrics.pop("markers_tail")
        result = {
            "engine_version": __version__, "dataset": manifest,
            "from_ms_inclusive": limits[0], "to_ms_exclusive": limits[1],
            "settings": asdict(settings), "metrics": metrics,
            "execution_model": "OTC quote side, fixed adverse slippage, forced close at final usable quote",
            "seconds_replay_with_trade_csv": elapsed,
        }
        (stage / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        payload = {"summary": result, "candles": candles, "markers": markers}
        markup = Path(__file__).with_name("report.html").read_text(encoding="utf-8")
        safe_json = json.dumps(payload, ensure_ascii=True, allow_nan=False).replace("<", r"\u003c")
        (stage / "report.html").write_text(markup.replace("/*TICKLAB_DATA*/null", safe_json), encoding="utf-8")
        stage.rename(directory)
    return result


def compare(expected_path, actual_path):
    def trades(file):
        reader = csv.DictReader(file)
        if not set(PARITY_FIELDS) <= set(reader.fieldnames or ()):
            raise ValueError("CSV đối chiếu thiếu cột bắt buộc: " + ", ".join(PARITY_FIELDS))
        for row in reader:
            side = row["side"].lower().strip()
            reason = row["reason"].strip().upper()
            if side not in ("long", "short") or reason not in ("SL", "TP", "END"):
                raise ValueError(f"CSV đối chiếu dòng {reader.line_num}: side hoặc reason không hợp lệ.")
            try:
                numeric = [int(row[field]) for field in PARITY_FIELDS[1:-1]]
            except (TypeError, ValueError) as exc:
                raise ValueError(f"CSV đối chiếu dòng {reader.line_num}: trường số không hợp lệ.") from exc
            if min(numeric) <= 0 or numeric[0] > numeric[1]:
                raise ValueError(f"CSV đối chiếu dòng {reader.line_num}: thời gian hoặc giá không hợp lệ.")
            yield dict(zip(PARITY_FIELDS, (side, *numeric, reason)))

    mismatch = pairs = nexpected = nactual = 0
    first = None
    with expected_path.open(encoding="utf-8-sig", newline="") as expected:
        with actual_path.open(encoding="utf-8-sig", newline="") as actual:
            for index, (a, b) in enumerate(zip_longest(trades(expected), trades(actual)), 1):
                nexpected += a is not None
                nactual += b is not None
                pairs += a is not None and b is not None
                if a != b:
                    mismatch += 1
                    if first is None:
                        first = {"trade_index": index, "expected": a, "actual": b}
    return {
        "match": not mismatch and pairs > 0, "expected_trades": nexpected, "actual_trades": nactual,
        "aligned_rows": pairs, "mismatched_rows": mismatch, "first_mismatch": first,
        "empty_comparison": not (nexpected or nactual), "fields": list(PARITY_FIELDS),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m ticklab")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    csv_input = commands.add_parser("import-csv", help="Nhập CSV tick chuẩn hoặc bản xuất từ MT5")
    csv_input.add_argument("input", type=Path)
    csv_input.add_argument("output", type=Path)
    csv_input.add_argument("--symbol", required=True)
    csv_input.add_argument("--digits", type=int, required=True, choices=range(11))
    csv_input.add_argument("--utc-offset")
    csv_input.add_argument("--source", choices=("csv", "mt5-export", "synthetic"), default="csv")
    mt5 = commands.add_parser("import-mt5", help="Đọc tick bằng API chính thức")
    mt5.add_argument("output", type=Path)
    mt5.add_argument("--terminal", type=Path, required=True)
    mt5.add_argument("--symbol", required=True)
    mt5.add_argument("--chunk-minutes", type=int, default=60, choices=range(1, 1441), metavar="N")
    mt5.add_argument("--timeout-ms", type=int, default=10000)
    mt5.add_argument("--from", dest="start", type=iso_datetime, required=True)
    mt5.add_argument("--to", dest="end", type=iso_datetime, required=True)
    verify = commands.add_parser("verify", help="Kiểm tra SHA-256 của bộ tick")
    verify.add_argument("dataset", type=Path)
    run = commands.add_parser("run", help="Chạy replay và xuất báo cáo")
    replay_args(run)
    run.add_argument("output", type=Path)
    bench = commands.add_parser("bench", help="Đo replay trên cache đã nạp")
    replay_args(bench)
    bench.add_argument("--repeats", type=int, default=5)
    check = commands.add_parser("compare", help="So khớp từng giao dịch theo thứ tự")
    check.add_argument("expected", type=Path)
    check.add_argument("actual", type=Path)
    args = parser.parse_args(argv)

    if args.command == "import-csv":
        source = {"source_type": args.source, "file": args.input.name, "utc_offset_for_date_time": args.utc_offset}
        show(write_dataset(args.output, args.symbol, args.digits, csv_rows(args.input, args.digits, args.utc_offset), source))
    elif args.command == "import-mt5":
        if args.timeout_ms <= 0:
            raise ValueError("timeout phải dương.")
        show(mt5_import(args.terminal, args.symbol, args.start, args.end, args.chunk_minutes, args.timeout_ms, args.output))
    elif args.command == "verify":
        with read_dataset(args.dataset) as (manifest, mapped):
            digest = hashlib.sha256(mapped).hexdigest()
            show({"match": digest == manifest.get("sha256"), "sha256": digest, "ticks": manifest["ticks"]})
            return 0 if digest == manifest.get("sha256") else 1
    elif args.command == "compare":
        result = compare(args.expected, args.actual)
        show(result)
        return 0 if result["match"] else 1
    else:
        names = ("bar_minutes", "fast", "slow", "stop_points", "target_points", "slippage_points", "fee_points", "direction")
        settings = Settings(**{name: getattr(args, name) for name in names})
        limits = tuple(epoch_ms(value) if value is not None else None for value in (args.start, args.end))
        with read_dataset(args.dataset) as (manifest, mapped):
            if args.command == "run":
                show(report(args.output, manifest, mapped, settings, limits))
            else:
                if not 1 <= args.repeats <= 100:
                    raise ValueError("repeats phải nằm trong [1, 100].")
                config = {"chart_limit": 0, "start_ms": limits[0], "end_ms": limits[1]}
                expected = replay(mapped, settings, **config)
                samples = []
                for _ in range(args.repeats):
                    started = perf_counter()
                    actual = replay(mapped, settings, **config)
                    samples.append(perf_counter() - started)
                    if actual != expected:
                        raise ValueError("Kết quả replay thay đổi giữa các lần chạy.")
                median = statistics.median(samples)
                show({
                    "benchmark": "warm mmap; replay only; single process",
                    "source_type": manifest["source"]["source_type"], "symbol": manifest["symbol"],
                    "settings": asdict(settings), "ticks_per_run": expected["ticks"], "trades": expected["trades"],
                    "from_ms_inclusive": limits[0], "to_ms_exclusive": limits[1],
                    "sample_seconds": samples, "median_seconds": median,
                    "median_ticks_per_second": expected["ticks"] / median,
                })
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, ArithmeticError, csv.Error, KeyError, TypeError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        sys.exit(2)

