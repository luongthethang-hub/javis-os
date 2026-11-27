#!/usr/bin/env python3
"""Script kiem chung toan: ma tran, xac suat, hoi quy, metric, qubit nho.

Chay: python scripts/verify_math.py <lenh> --json '{...}'
Cac lenh: mat, solve, prob, bayes, linreg, metrics, qubit
Dau ra JSON gom result, formula, steps, check.
Khong dung thu vien ngoai numpy.
"""
import json
import math
import sys

import numpy as np

TOL_DET = 1e-9
TOL_PROB = 1e-9


def _out(result, formula, steps, check, ok=True):
    print(json.dumps(
        {"ok": ok, "result": result, "formula": formula, "steps": steps, "check": check},
        ensure_ascii=False, indent=2, default=_jsonable))


def _jsonable(o):
    if isinstance(o, np.ndarray):
        return [_jsonable(i) for i in o.tolist()]
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, complex):
        return {"re": o.real, "im": o.imag}
    raise TypeError(str(type(o)))


def _round(x, nd=12):
    if isinstance(x, np.ndarray):
        return _round(x.tolist(), nd)
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        x = x.item()
    if isinstance(x, (int, float, complex)):
        if isinstance(x, complex):
            return {"re": round(x.real, nd), "im": round(x.imag, nd)}
        v = round(float(x), nd)
        return 0.0 if v == 0 else v
    if isinstance(x, list):
        return [_round(i, nd) for i in x]
    if isinstance(x, dict):
        return {k: _round(v, nd) for k, v in x.items()}
    return x


def cmd_mat(d):
    A = np.array(d["A"], dtype=float)
    steps = []
    res = {"shape": list(A.shape)}
    if A.shape[0] != A.shape[1]:
        res["rank"] = int(np.linalg.matrix_rank(A))
        res["note"] = "ma tran khong vuong, chi tinh hang va SVD"
    else:
        det = float(np.linalg.det(A))
        res["det"] = _round(det)
        eig = np.linalg.eigvals(A)
        res["eigenvalues"] = _round(np.sort_complex(eig))
        prod = complex(np.prod(eig))
        res["prod_eigenvalues"] = _round(prod)
        steps.append("det(A) so sanh tich tri rieng: %.12g vs %.12g"
                     % (det, prod.real if abs(prod.imag) < 1e-9 else prod))
        if abs(det) < TOL_DET:
            res["inverse"] = None
            res["rank"] = int(np.linalg.matrix_rank(A))
            res["note"] = "dinh thuc ~ 0, khong kha nghich"
        else:
            inv = np.linalg.inv(A)
            res["inverse"] = _round(inv)
            res["det_inverse"] = _round(1.0 / det)
            steps.append("det(inv A) = 1/det(A) = %.12g" % (1.0 / det))
        res["rank"] = int(np.linalg.matrix_rank(A))
        res["condition_number"] = _round(float(np.linalg.cond(A)))
    if A.shape[0] == A.shape[1]:
        s = np.linalg.svd(A, compute_uv=False)
        res["singular_values"] = _round(s)
        res["rank_svd"] = int(int(np.sum(s > TOL_DET * max(A.shape))))
    res["trace"] = _round(float(np.trace(A))) if A.shape[0] == A.shape[1] else None
    check = {}
    if res.get("inverse"):
        E = A @ np.array(res["inverse"], dtype=float)
        check["A_inv_A_identity_max_dev"] = _round(float(np.max(np.abs(E - np.eye(A.shape[0])))))
    return res, "det via LU; rank = so singular value > nguong hoac pivot; inv qua LU", steps, check


def cmd_solve(d):
    A = np.array(d["A"], dtype=float)
    b = np.array(d["b"], dtype=float)
    x = np.linalg.solve(A, b)
    r = A @ x - b
    return ({"x": _round(x),
             "residual_max_abs": _round(float(np.max(np.abs(r))))},
            "A x = b giai bang khu Gauss/LU", ["the nghiem lai: A·x - b phai ~ 0"],
            {"residual_max_abs": _round(float(np.max(np.abs(r))))})


def _binom_pmf(n, k, p):
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


def cmd_prob(d):
    kind = d.get("kind", "binomial")
    if kind == "binomial":
        n = int(d["n"]); k = int(d["k"]); p = float(d["p"])
        at_least = bool(d.get("at_least", False))
        if at_least:
            res_val = sum(_binom_pmf(n, i, p) for i in range(k, n + 1))
            formula = "P(X>=k) = sum_{i=k..n} C(n,i) p^i (1-p)^(n-i)"
            comp = 1 - sum(_binom_pmf(n, i, p) for i in range(0, k))
            check = {"complement_match": _round(comp - res_val, 12),
                     "complement_value": _round(comp)}
        else:
            res_val = _binom_pmf(n, k, p)
            formula = "P(X=k) = C(n,k) p^k (1-p)^(n-k)"
            check = {}
        total = sum(_binom_pmf(n, i, p) for i in range(n + 1))
        check["pmf_sums_to_1_dev"] = _round(total - 1, 12)
        return ({"probability": _round(res_val), "n": n, "k": k, "p": p, "at_least": at_least},
                formula,
                ["1 - CDF(k-1) dung cho at_least, khong phai P(X=k)"],
                check)
    if kind == "poisson":
        lam = float(d["lambda"]); k = int(d["k"])
        at_least = bool(d.get("at_least", False))
        pmf = lambda i: math.exp(-lam) * lam ** i / math.factorial(i)
        if at_least:
            v = sum(pmf(i) for i in range(k, 200))
            check = {"complement_match": _round(1 - sum(pmf(i) for i in range(k)) - v, 12)}
        else:
            v = pmf(k); check = {}
        return ({"probability": _round(v)}, "P(X=k) = e^-lam lam^k / k!", [], check)
    raise SystemExit("kind khong ho tro: %s" % kind)


def cmd_bayes(d):
    prior = float(d["prior"])
    like = float(d["likelihood"])
    fa = float(d["false_alarm"])
    num = prior * like
    den = num + (1 - prior) * fa
    post = num / den
    return ({"posterior": _round(post), "prior": prior, "likelihood": like, "false_alarm": fa},
            "P(H|E) = P(E|H)P(H) / [P(E|H)P(H) + P(E|~H)P(~H)]",
            ["chuan hoa: mau so = P(E), phai trong (0,1]"],
            {"evidence_probability": _round(den),
             "posterior_in_0_1": bool(0.0 <= post <= 1.0)})


def cmd_linreg(d):
    X = np.array(d["X"], dtype=float)
    y = np.array(d["y"], dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    if X.shape[0] != y.shape[0]:
        raise SystemExit("so dong X khac do dai y")
    Xd = np.hstack([np.ones((X.shape[0], 1)), X])
    coef, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    yhat = Xd @ coef
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return ({"intercept": _round(coef[0]), "coefficients": _round(coef[1:]),
             "r2": _round(r2), "y_hat": _round(yhat)},
            "beta = (X^T X)^-1 X^T y; R2 = 1 - SSres/SStot",
            ["X them cot 1 cho intercept"],
            {"r2_in_0_1": bool(-1e-9 <= r2 <= 1 + 1e-9),
             "residual_sum": _round(float(np.sum(y - yhat)))})


def cmd_metrics(d):
    yt = np.array(d["y_true"]).astype(int)
    yp = np.array(d["y_pred"]).astype(int)
    if yt.shape != yp.shape:
        raise SystemExit("y_true va y_pred lech do dai: %s vs %s" % (yt.shape, yp.shape))
    tp = int(np.sum((yt == 1) & (yp == 1)))
    tn = int(np.sum((yt == 0) & (yp == 0)))
    fp = int(np.sum((yt == 0) & (yp == 1)))
    fn = int(np.sum((yt == 1) & (yp == 0)))
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    acc = (tp + tn) / len(yt)
    return ({"tp": tp, "tn": tn, "fp": fp, "fn": fn,
             "precision": _round(prec), "recall": _round(rec),
             "accuracy": _round(acc), "f1": _round(2 * prec * rec / (prec + rec)) if prec + rec else None},
            "precision = TP/(TP+FP); recall = TP/(TP+FN); acc = (TP+TN)/N", [],
            {"confusion_total_matches_n": (tp + tn + fp + fn) == len(yt)})


def _gate(name, n):
    if name == "H":
        return np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
    if name == "X":
        return np.array([[0, 1], [1, 0]], dtype=complex)
    if name == "Y":
        return np.array([[0, -1j], [1j, 0]], dtype=complex)
    if name == "Z":
        return np.array([[1, 0], [0, -1]], dtype=complex)
    if name == "I":
        return np.eye(2, dtype=complex)
    raise SystemExit("cong khong ho tro: %s" % name)


def cmd_qubit(d):
    gates = [g.upper() for g in d["gates"]]
    n = 1
    for g in gates:
        if g == "CNOT":
            n = max(n, 2)
    if d.get("qubits"):
        n = int(d["qubits"])
    if n > 4:
        raise SystemExit("toi da 4 qubit")
    dim = 2 ** n
    psi = np.zeros(dim, dtype=complex)
    psi[0] = 1.0
    steps = []
    for g in gates:
        if g == "CNOT":
            U = np.zeros((4, 4), dtype=complex)
            U[0, 0] = U[1, 1] = U[3, 2] = U[2, 3] = 1
            if n > 2:
                full = np.eye(dim, dtype=complex)
                full[:4, :4] = U
                psi = full @ psi
            else:
                psi = U @ psi
        else:
            G = _gate(g, n)
            full = np.eye(dim, dtype=complex)
            k = 0
            if n == 1:
                full = G
            else:
                Kh = np.eye(2, dtype=complex)
                full = np.kron(G, np.eye(2 ** (n - 1), dtype=complex))
            psi = full @ psi
        steps.append("%s -> chuan %.12g" % (g, float(np.linalg.norm(psi))))
    probs = np.abs(psi) ** 2
    norm = float(np.linalg.norm(psi))
    shots = int(d.get("shots", 1000))
    return ({"n_qubits": n, "state": _round(psi), "probabilities": _round(probs),
             "basis": [format(i, "0%db" % n) for i in range(dim)],
             "shots_requested": shots},
            "|psi> = U_k ... U_1 |0>; P(i) = |<i|psi>|^2; tong P = 1",
            steps,
            {"norm": _round(norm), "prob_sum": _round(float(probs.sum())),
             "norm_ok": abs(norm - 1) < 1e-9, "prob_sum_ok": abs(probs.sum() - 1) < 1e-12})


CMDS = {"mat": cmd_mat, "solve": cmd_solve, "prob": cmd_prob, "bayes": cmd_bayes,
        "linreg": cmd_linreg, "metrics": cmd_metrics, "qubit": cmd_qubit}


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("lenh:", ", ".join(CMDS))
        return 0
    cmd = argv[0]
    if cmd not in CMDS:
        print("lenh khong ho tro: %s" % cmd, file=sys.stderr)
        return 2
    raw = None
    if "--json-file" in argv:
        with open(argv[argv.index("--json-file") + 1], "r", encoding="utf-8") as f:
            raw = f.read()
    if raw is None and "--json" in argv:
        raw = argv[argv.index("--json") + 1]
    if raw is None:
        raw = sys.stdin.read()
    data = json.loads(raw)
    try:
        res, formula, steps, check = CMDS[cmd](data)
    except Exception as e:  # bao loi ro, khong tra so rac
        print(json.dumps({"ok": False, "error": "%s: %s" % (type(e).__name__, e)},
                         ensure_ascii=False), file=sys.stderr)
        return 1
    _out(res, formula, steps, check)
    return 0


if __name__ == "__main__":
    sys.exit(main())
