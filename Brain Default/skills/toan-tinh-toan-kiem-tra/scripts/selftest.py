"""Kiem chung script verify_math.py bang cac ca co dap an biet truoc.

Chay: python scripts/selftest.py
Moi ca so sanh ket qua script voi gia tri dung tinh tay/doc lap.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "verify_math.py"

CASES = [
    ("mat", {"A": [[2, 1], [1, 3]]}, "det", 5.0),
    ("mat", {"A": [[1, 2], [2, 4]]}, "rank", 1),          # suy bien: det = 0
    ("mat", {"A": [[0, 2], [3, 0]]}, "det", -6.0),
    ("solve", {"A": [[2, 1], [1, 3]], "b": [5, 10]}, "x", [1.0, 3.0]),
    ("prob", {"kind": "binomial", "n": 10, "k": 3, "p": 0.2, "at_least": True}, "probability", None),
    ("bayes", {"prior": 0.1, "likelihood": 0.9, "false_alarm": 0.05}, "posterior", 0.9 * 0.1 / (0.9 * 0.1 + 0.05 * 0.9)),
    ("linreg", {"X": [[1], [2], [3], [4]], "y": [2, 4, 6, 8]}, "r2", 1.0),
    ("metrics", {"y_true": [1, 1, 0, 0], "y_pred": [1, 0, 1, 0]}, "accuracy", 0.5),
    ("qubit", {"gates": ["H", "CNOT"], "shots": 1000}, "probabilities", [0.5, 0.0, 0.0, 0.5]),
]


def run(cmd, payload):
    p = subprocess.run([sys.executable, str(SCRIPT), cmd, "--json", json.dumps(payload)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None, p.stderr.strip()
    return json.loads(p.stdout), None


def close(a, b, tol=1e-9):
    if isinstance(a, list):
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(b, list):
        return False
    return abs(float(a) - float(b)) <= tol


def main():
    fails = 0
    # ca nhị thức: đáp án tính tay độc lập bằng biến cố bù
    p_ge3 = 1 - sum(__import__("math").comb(10, i) * 0.2 ** i * 0.8 ** (10 - i) for i in range(3))
    CASES[4] = ("prob", CASES[4][1], "probability", p_ge3)
    for cmd, payload, field, expect in CASES:
        got, err = run(cmd, payload)
        if err:
            print("FAIL %s %s -> loi: %s" % (cmd, payload, err))
            fails += 1
            continue
        val = got["result"].get(field)
        ok = close(val, expect) if expect is not None else True
        chk = got.get("check") or {}
        chk_ok = all(True if not isinstance(v, bool) else v for v in chk.values())
        status = "PASS" if ok and chk_ok else "FAIL"
        if status == "FAIL":
            fails += 1
        print("%s %-8s %-14s = %s (mong doi %s) check=%s" % (status, cmd, field, val, expect, chk))
    print("\n%d/%d ca dat" % (len(CASES) - fails, len(CASES)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
