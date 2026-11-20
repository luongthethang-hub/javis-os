"""Prepare synthetic data and evaluate model output through local Ollama."""
import argparse
import json
import random
import re
import statistics
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INSTRUCTION = (
    "Trich xuat ma dang ky hien tai cua hoc vien tu noi dung ben duoi. "
    "Chi tra duy nhat ma do, dung chu hoa va dau gach ngang nhu du lieu. "
    "Bo qua ma lich hen, ma thanh toan va ma dang ky cu. "
    "Neu khong co ma dang ky hien tai, tra THIEU.\n\n"
)
TRAIN_LAYOUTS = [
    "Phieu tiep nhan | Ma dang ky hien tai: {new} | Ma lich hen: {booking}",
    "Tin nhan: Da doi ma dang ky tu {old} sang {new}. Ma thanh toan: {payment}.",
    "Ma lich hen: {booking}\nMa dang ky hien tai: {new}\nTrang thai: da tiep nhan.",
    "Nhan vien ghi chu: {new} la ma dang ky moi, {old} da huy.",
    "Ho so co ma thanh toan {payment}; ma dang ky hien tai la {new}.",
    "Cap nhat hoc vien\nMa dang ky cu: {old}\nMa dang ky hien tai: {new}",
]
TEST_LAYOUTS = [
    ("single", "Da nhap ho so. Ma dang ky hien tai = {new}."),
    ("distractor", "Lich hen [{booking}] | Dang ky [{new}] | Bien lai [{payment}]."),
    ("replacement", "Vui long bo ma {old}, ma dang ky thay the duoc xac nhan la {new}."),
    ("missing", "Bien lai [{payment}], lich hen [{booking}]. Chua cap ma dang ky mot cach chinh thuc."),
]
MISSING_LAYOUTS = [
    "Ma dang ky hien tai: chua co. Ma lich hen: {booking}. Ma thanh toan: {payment}.",
    "Ma dang ky cu {old} da huy. Dang cho cap ma moi.",
    "Moi co bien lai {payment}; ho so chua duoc gan ma dang ky.",
]


def build_data():
    rng = random.Random(20261120)
    used = set()

    def code(prefixes):
        while True:
            value = f"{rng.choice(prefixes)}-{rng.randrange(100, 1000)}"
            if value not in used:
                used.add(value)
                return value

    for split, count in (("train", 96), ("test", 16)):
        rows = []
        for index in range(count):
            current = code(("DK", "HS", "LX", "GH"))
            values = {
                "new": current, "old": code(("DK", "HS", "LX", "GH")),
                "booking": code(("LH", "CH")), "payment": code(("TT", "BL")),
            }
            if split == "test":
                kind, template = TEST_LAYOUTS[index % len(TEST_LAYOUTS)]
            elif index % 4 == 0:
                kind, template = "missing", MISSING_LAYOUTS[(index // 4) % len(MISSING_LAYOUTS)]
            else:
                kind, template = "provided", TRAIN_LAYOUTS[(index + index // 4) % len(TRAIN_LAYOUTS)]
            rows.append({
                "id": f"{split}-{index + 1:03}",
                "kind": kind,
                "input": INSTRUCTION + template.format(**values),
                "expected": "THIEU" if kind == "missing" else current,
            })
        target = ROOT / f"{split}.jsonl"
        with target.open("x", encoding="utf-8", newline="\n") as output:
            for row in rows:
                output.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"{split}: {len(rows)} examples", flush=True)


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def evaluate(model, name):
    cases = read_rows(ROOT / "test.jsonl")
    result_path = ROOT / f"{name}.jsonl"
    measured = read_rows(result_path) if result_path.exists() else []
    if any(row["model"] != model for row in measured):
        raise ValueError("Output already belongs to another model")
    complete = {row["id"] for row in measured}
    with result_path.open("a", encoding="utf-8", newline="\n") as output:
        for case in cases:
            if case["id"] in complete:
                continue
            request = urllib.request.Request(
                "http://127.0.0.1:11434/api/chat",
                headers={"Content-Type": "application/json"},
                data=json.dumps({
                    "model": model,
                    "messages": [{"role": "user", "content": case["input"]}],
                    "stream": False,
                    "think": False,
                    "keep_alive": "2m",
                    "options": {"temperature": 0, "seed": 20261120, "num_predict": 160, "num_ctx": 512},
                }).encode(),
            )
            started = time.monotonic()
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = json.load(response)
            visible = payload["message"]["content"].strip()
            expected = case["expected"]
            if expected == "THIEU":
                correct_content = bool(re.search(r"\bTHIEU\b", visible, flags=re.IGNORECASE))
            else:
                codes = set(re.findall(r"\b[A-Z]{2}-\d{3}\b", visible.upper()))
                correct_content = codes == {expected}
            row = {
                "id": case["id"], "kind": case["kind"], "model": model,
                "expected": expected, "output": visible, "exact": visible == expected,
                "content": correct_content, "seconds": round(time.monotonic() - started, 3),
                "done_reason": payload.get("done_reason"),
                "prompt_tokens": payload.get("prompt_eval_count"),
                "output_tokens": payload.get("eval_count"),
            }
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
            output.flush()
            measured.append(row)
            print(f"{row['id']} exact={row['exact']} seconds={row['seconds']}", flush=True)
    print(json.dumps({
        "model": model,
        "cases": len(measured),
        "exact": sum(row["exact"] for row in measured),
        "content": sum(row["content"] for row in measured),
        "median_seconds": round(statistics.median(row["seconds"] for row in measured), 3),
        "truncated": sum(row["done_reason"] == "length" for row in measured),
    }), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "evaluate"))
    parser.add_argument("--model", default="deepseek-r1:1.5b")
    parser.add_argument("--result", default="baseline")
    args = parser.parse_args()
    if args.mode == "prepare":
        build_data()
    else:
        evaluate(args.model, args.result)


if __name__ == "__main__":
    main()
