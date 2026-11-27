import json, re, sys
from datetime import date
from pathlib import Path

import yaml

TANG = ("T0", "T1", "T2", "T3")
SO = r"(?:0|[1-9][0-9]*)"
PR = rf"(?:{SO}|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER = re.compile(rf"{SO}\.{SO}\.{SO}(?:-{PR}(?:\.{PR})*)?"
                    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?")
NHAN_BI_MAT = (r"(?:[a-z0-9]+[_-])*(?:password|passwd|pwd|passphrase|mat[_ -]?khau|mật[_ -]?khẩu|"
               r"(?:api|access|private)[_ -]?key|secret|token|authorization)")
CHUOI_BI_MAT = re.compile(
    r"\b(?:sk-|gsk_|xai-|gh[pousr]_|github_pat_|xox[baprs]-|sk_live_)[A-Za-z0-9_-]{16,}"
    r"|\bAIza[A-Za-z0-9_-]{35}\b|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"
    r"|\bBearer[ \t]+[A-Za-z0-9._~+/-]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    rf"""|(?<![\w-]){NHAN_BI_MAT}["']?[ \t]*[:=][ \t]*["']?[^\s"'{{}}\[\],#]""", re.I
)

class Loi(ValueError):
    """Lỗi có thông báo an toàn để in."""

def khong_trung(cac_cap):
    kq = {}
    for k, v in cac_cap:
        if k in kq:
            raise Loi("khóa bị trùng")
        kq[k] = v
    return kq

class Loader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        return khong_trung(self.construct_pairs(node, deep=deep))

def chan_bi_mat(x):
    cho, da_xem = [x], set()
    while cho:
        x = cho.pop()
        if id(x) in da_xem:
            continue
        da_xem.add(id(x))
        if isinstance(x, bytes) or (isinstance(x, str) and CHUOI_BI_MAT.search(x)):
            raise Loi("phát hiện chuỗi giống bí mật hoặc dữ liệu nhị phân")
        if isinstance(x, dict):
            if any(isinstance(k, str) and re.fullmatch(NHAN_BI_MAT, k.strip(), re.I) for k in x):
                raise Loi("phát hiện tên trường bí mật")
            cho.extend(x.values())
        if isinstance(x, (dict, list, tuple, set)):
            cho.extend(x)

def kiem_truong(x, bat_buoc, **mien):
    if not isinstance(x, dict):
        raise Loi("gốc dữ liệu phải là object")
    for k in bat_buoc.split():
        if not isinstance(x.get(k), str) or not x[k].strip():
            raise Loi(f"{k} phải là chuỗi không rỗng")
    for k, gia_tri in mien.items():
        if x.get(k) not in gia_tri:
            raise Loi(f"{k} thiếu hoặc không thuộc tập giá trị cho phép")

def kiem_ngay(x, k):
    try:
        if type(x) is date or date.fromisoformat(x).isoformat() == x:
            return
    except (TypeError, ValueError):
        pass
    raise Loi(f"{k} phải là ngày hợp lệ dạng YYYY-MM-DD")

def kiem_ho_so(x):
    kiem_truong(x, "id ten model muc_tieu phien_ban", schema_version=("1.0",),
                tang_hoc=TANG, trang_thai=("active", "paused", "archived"))
    if not SEMVER.fullmatch(x["phien_ban"]):
        raise Loi("phien_ban phải đúng SemVer")
    kiem_ngay(x.get("cap_nhat"), "cap_nhat")

def kiem_golden(x, ids):
    kiem_truong(x, "id dau_vao ky_vong cach_cham nguon", tang=TANG,
                loai=("safety", "behavior", "regression", "knowledge"), d_level=("D0", "D1", "D2", "D3", "D4"))
    if (han := x.get("het_hieu_luc", "")) is not None:
        kiem_ngay(han, "het_hieu_luc")
    ma = x["id"].strip()
    if ma in ids:
        raise Loi("id golden test bị trùng")
    ids.add(ma)

def hang_so_json(_):
    raise Loi("JSON không cho phép NaN hoặc Infinity")

def main(p_ho_so, p_golden):
    vi_tri = "ho-so.yaml"
    try:
        raw = Path(p_ho_so).read_text(encoding="utf-8-sig")
        chan_bi_mat(raw)
        x = yaml.load(raw, Loader=Loader)
        chan_bi_mat(x)
        kiem_ho_so(x)
        vi_tri, ids = "golden-tests.jsonl", set()
        with Path(p_golden).open(encoding="utf-8-sig") as f:
            for so, dong in enumerate(f, 1):
                vi_tri = f"golden-tests.jsonl dòng {so}"
                chan_bi_mat(dong)
                x = json.loads(dong, object_pairs_hook=khong_trung, parse_constant=hang_so_json)
                chan_bi_mat(x)
                kiem_golden(x, ids)
        if not ids:
            raise Loi("cần ít nhất một golden test")
        print(f"Hợp lệ: hồ sơ và {len(ids)} golden test")
        return 0
    except Loi as e:
        print(f"{vi_tri}: {e}", file=sys.stderr)
    except (ValueError, TypeError, OSError, OverflowError, RecursionError, yaml.YAMLError):
        print(f"{vi_tri}: không đọc được hoặc dữ liệu sai cú pháp", file=sys.stderr)
    return 1

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]) if len(sys.argv) == 3 else
             "Cách dùng: python kiem-tra-schema.py ho-so.yaml golden-tests.jsonl")
