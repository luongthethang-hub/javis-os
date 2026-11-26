# -*- coding: utf-8 -*-
"""Doi chieu memory/facts/*.md voi 3 tang bo nho (T0/T1/T2) va tier_manifest.json.

Chay: python Javis/scripts/tier_reconcile.py            # kiem tra, khong ghi
      python Javis/scripts/tier_reconcile.py --apply    # ghi (co backup)

Quy tac:
- T0: chi doc manifest.sha256.json, kiem hash, KHONG sua (chi Layer 0 duoc sua).
- T1: la quy che/kien truc/chi thi cua Layer 0. Script CHI liet ke vao
  `pending_t1_review` trong tier_manifest, KHONG tu them vao T1_governed.
- T2: ho so, so thich, du an, bai hoc van hanh. Duoc phep bo sung ban ghi.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

BRAIN = Path(r"C:\Users\Admin\JavisOS\brains\Brain Default")
FACTS = BRAIN / "memory" / "facts"
TIERS = BRAIN / "memory" / "tiers"
T1_REG = TIERS / "T1_governed" / "registry.json"
T2_REG = TIERS / "T2_adaptive" / "registry.json"
T0_MANIFEST = TIERS / "T0_immutable" / "manifest.sha256.json"
MANIFEST = TIERS / "tier_manifest.json"

# Nhung fact mang tinh quy che/kien truc/chi thi L0, phai qua phe duyet T1.
T1_HINTS = ("system", "directive", "architecture", "governance")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_front(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip("'\"")
    return out


def title_of(text: str, slug: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()[:120]
    return slug


def summary_of(text: str) -> str:
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
    for para in body.split("\n\n"):
        p = para.strip().replace("\n", " ")
        if p and not p.startswith("#"):
            return p[:200]
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    args = ap.parse_args()

    t0 = json.loads(T0_MANIFEST.read_text(encoding="utf-8"))
    t1 = json.loads(T1_REG.read_text(encoding="utf-8"))
    t2 = json.loads(T2_REG.read_text(encoding="utf-8"))
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))

    # 1. Kiem T0 fail-closed: thieu tep hoac lech hash thi dung.
    t0_bad = []
    for item in t0.get("files", []):
        p = BRAIN / item["path"]
        if not p.exists() or sha256_file(p) != item["sha256"]:
            t0_bad.append(item["path"])
    if t0_bad:
        print("FAIL: T0 lech hash hoac thieu tep:", t0_bad)
        return 2

    def slugset(reg):
        return {it["slug"] for it in reg.get("items", [])}

    t1_slugs, t2_slugs = slugset(t1), slugset(t2)
    # core_charter_t0.md nam trong T0_immutable, khong nam trong facts/, nen chi dem
    # nhung tep T0 co ban sao trong memory/facts/ (7 fact hat nhan da niem phong).
    t0_slugs = {
        Path(i["path"]).stem
        for i in t0.get("files", [])
        if i.get("path", "").endswith(".md") and (FACTS / Path(i["path"]).name).exists()
    }
    sup = {s["slug"] for s in man.get("superseded_facts", [])}

    files = sorted(FACTS.glob("*.md"))
    missing_t2, pending_t1 = [], []
    for f in files:
        slug = f.stem
        if slug in t0_slugs or slug in t1_slugs or slug in t2_slugs or slug in sup:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = read_front(text)
        ftype = fm.get("type", "")
        if any(h in ftype.lower() for h in T1_HINTS):
            pending_t1.append(slug)
            continue
        missing_t2.append((f, fm, text, ftype))

    print(f"facts={len(files)} T0={len(t0_slugs)} T1={len(t1_slugs)} T2={len(t2_slugs)} superseded={len(sup)}")
    print(f"thieu trong T2: {len(missing_t2)} | cho duyet T1: {len(pending_t1)}")
    for slug in pending_t1:
        print("  pending_t1:", slug)

    if not args.apply:
        return 0

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    for p in (T2_REG, MANIFEST):
        shutil.copy2(p, p.with_suffix(p.suffix + f".bak-{stamp}"))

    for f, fm, text, ftype in missing_t2:
        slug = f.stem
        created = fm.get("created", args.today)[:10]
        t2["items"].append(
            {
                "slug": slug,
                "title": title_of(text, slug),
                "summary": summary_of(text),
                "tier": "T2",
                "type": ftype or "fact",
                "file": f"memory/facts/{f.name}",
                "created": created,
                "updated": fm.get("updated", created)[:10],
                "provenance": fm.get("provenance", "agent"),
                "sha256": sha256_file(f),
                "size_bytes": f.stat().st_size,
                "decay_days": 90,
                "half_life_days": 45,
                "review_after": (dt.date.fromisoformat(created) + dt.timedelta(days=90)).isoformat()
                if re.match(r"^\d{4}-\d{2}-\d{2}$", created)
                else args.today,
                "confidence": 0.8,
            }
        )

    t2["items"].sort(key=lambda x: x["slug"])
    t2["count"] = len(t2["items"])
    t2["generated_at"] = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
    T2_REG.write_text(json.dumps(t2, ensure_ascii=False, indent=2), encoding="utf-8")

    man["generated_at"] = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
    man["totals"] = {
        "all_fact_files": len(files),
        "active_facts": len(files) - len(sup),
        "t0_immutable": len(t0_slugs),
        "t1_governed": len(t1["items"]),
        "t2_adaptive": len(t2["items"]),
        "superseded": len(sup),
    }
    man["t0_bundle_sha256"] = t0.get("bundle_sha256", man.get("t0_bundle_sha256"))
    man["pending_t1_review"] = sorted(set(man.get("pending_t1_review", [])) | set(pending_t1))
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")

    print("APPLY xong:", json.dumps(man["totals"], ensure_ascii=False))
    print("backup:", f"*.bak-{stamp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
