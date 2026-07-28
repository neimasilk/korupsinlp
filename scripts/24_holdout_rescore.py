"""Script 24: Re-score ALL archived holdout annotations against the CURRENT DB.

Purpose after each parser-fix round:
  (a) regression check — any case that agreed in its own round must still
      agree now (a 1->0 flip means a fix broke something the fixtures missed);
  (b) training-set accuracy of the current parser on all annotated cases
      (UPPER bound — these cases drove the fixes; the fresh holdout round
      remains the only unbiased estimate).

Usage: python -m scripts.24_holdout_rescore
"""
import re
import sqlite3
from pathlib import Path

import pandas as pd
from statsmodels.stats.proportion import proportion_confint

ROOT = Path(__file__).resolve().parent.parent
GS = ROOT / "data" / "golden_set"
DB = ROOT / "data" / "korupsinlp.db"
ROUNDS = ["holdout_r1_validated.csv", "holdout_r2_validated.csv",
          "holdout_r3_validated.csv", "holdout_r4_validated.csv",
          "holdout_r5_validated.csv", "holdout_r6_validated.csv"]
FIELDS = ["vonis", "tuntutan", "kerugian", "daerah", "tahun"]
DB_COL = {"vonis": "vonis_bulan", "tuntutan": "tuntutan_bulan",
          "kerugian": "kerugian_negara", "daerah": "daerah", "tahun": "tahun"}
HUMAN_COL = {"vonis": "human_vonis_bulan", "tuntutan": "human_tuntutan_bulan",
             "kerugian": "human_kerugian_negara", "daerah": "human_daerah",
             "tahun": "human_tahun"}


def norm_case(s):
    s = re.sub(r"\s+", " ", str(s).upper()).strip()
    return re.sub(r"\s*/\s*", "/", s)


def as_num(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = str(v).strip()
    if not s or s.upper().startswith("ABSENT") or s.lower() == "nan":
        return None
    if "AMBIGUOUS" in s.upper():
        return "AMBIGUOUS"
    if s.upper().startswith("ACQUITTED"):
        return "ACQUITTED"
    m = re.match(r"^-?[\d.]+", s.replace(",", ""))
    return float(m.group(0)) if m else "AMBIGUOUS"


def as_str(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    s = re.sub(r"\s+", " ", str(v)).strip()
    if not s or s.upper().startswith("ABSENT") or s.lower() == "nan":
        return None
    if "AMBIGUOUS" in s.upper():
        return "AMBIGUOUS"
    return s


def norm_daerah(v):
    """PN KUPANG / PT BANDUNG ~ Kupang / Bandung (adjudication convention)."""
    s = as_str(v)
    if s in (None, "AMBIGUOUS"):
        return s
    return re.sub(r"^(?:PN|PT)\s+", "", s.upper())


def judge(field, parser_v, human_v):
    if field == "daerah":
        p, h = norm_daerah(parser_v), norm_daerah(human_v)
    elif field in ("vonis", "tuntutan", "kerugian", "tahun"):
        p, h = as_num(parser_v), as_num(human_v)
    else:
        p, h = as_str(parser_v), as_str(human_v)
    if h == "AMBIGUOUS" or p == "AMBIGUOUS":
        return "AMBIGUOUS"
    if h == "ACQUITTED":
        return "A" if (p is None or p == 0) else "0"
    if p is None and h is None:
        return "A"
    # NULL vs annotator's explicit 0 = "no loss established" (adjudication)
    if field == "kerugian" and p is None and h == 0:
        return "A"
    if p is None or h is None:
        return "0"
    if field == "kerugian":
        # Cents tolerance — annotators write whole rupiah, the parser keeps the
        # cents the verdict prints (holdout R6).
        return "1" if abs(p - h) < 1.0 else "0"
    if field in ("vonis", "tuntutan", "tahun"):
        return "1" if abs(p - h) < 0.5 else "0"
    return "1" if str(p).upper() == str(h).upper() else "0"


def _adjudicated(row, field):
    """True if this field's archived agreement came from a manual adjudication
    that overruled the annotator (parser judged correct against the PDF)."""
    note = row.get("adjudication")
    if note is None or (isinstance(note, float) and pd.isna(note)):
        return False
    return f"{field}:" in str(note) and \
        str(row.get(f"{field}_agree", "")).strip() in ("1", "A")


def _same_value(field, archived, current):
    """Has the parser value moved since the adjudication was made?"""
    if field in ("vonis", "tuntutan", "kerugian", "tahun"):
        a, c = as_num(archived), as_num(current)
        if isinstance(a, float) and isinstance(c, float):
            return abs(a - c) < 0.5
        return a == c
    a, c = as_str(archived), as_str(current)
    return (a or "").upper() == (c or "").upper()


def main():
    con = sqlite3.connect(DB)
    db = pd.read_sql_query(
        "SELECT case_number, vonis_bulan, tuntutan_bulan, kerugian_negara,"
        " daerah, tahun FROM verdicts", con)
    con.close()
    db["key"] = db["case_number"].map(norm_case)
    db = db.drop_duplicates("key")

    frames = []
    for i, f in enumerate(ROUNDS, 1):
        path = GS / f
        if not path.exists():
            continue
        df = pd.read_csv(path, dtype=str)
        df["round"] = f"R{i}"
        frames.append(df)
    val = pd.concat(frames, ignore_index=True)
    val["key"] = val["case_number"].map(norm_case)
    merged = val.merge(db, on="key", how="left", suffixes=("", "_db"))

    print(f"Re-scoring {len(merged)} archived annotations vs current DB\n")
    print(f"{'field':>10} {'agree':>6} {'n':>4} {'acc':>7} {'wilson95':>16}")
    regressions = []
    for fld in FIELDS:
        results = []
        for _, r in merged.iterrows():
            verdict = judge(fld, r[DB_COL[fld]], r[HUMAN_COL[fld]])
            # An adjudicated override (human cell judged WRONG against the PDF)
            # must not be re-litigated by raw comparison — otherwise it reads as
            # a permanent regression. Valid only while the DB value is unchanged
            # from the one that was adjudicated.
            if _adjudicated(r, fld):
                if _same_value(fld, r.get(f"parser_{DB_COL[fld]}"), r[DB_COL[fld]]):
                    verdict = str(r.get(f"{fld}_agree", verdict)).strip()
            results.append(verdict)
            old = str(r.get(f"{fld}_agree", "")).strip()
            if verdict == "0" and old in ("1", "A"):
                regressions.append((r["round"], r["case_number"], fld,
                                    r.get(DB_COL[fld], "?"), r[HUMAN_COL[fld]]))
        scored = [x for x in results if x in ("1", "0", "A")]
        agree = sum(1 for x in scored if x in ("1", "A"))
        n = len(scored)
        if n:
            lo, hi = proportion_confint(agree, n, method="wilson")
            print(f"{fld:>10} {agree:>6} {n:>4} {agree/n:>6.1%} [{lo:>6.1%}, {hi:>6.1%}]")

    print(f"\nREGRESSIONS (agreed in own round, disagree now): {len(regressions)}")
    for rd, cn, fld, pv, hv in regressions:
        print(f"  {rd} {cn} [{fld}] db={pv} human={hv}")


if __name__ == "__main__":
    main()
