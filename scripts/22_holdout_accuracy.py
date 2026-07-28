"""Script 22: Holdout-20 per-field accuracy (post-reextraction G2 check).

Unlike session 17 (agents saw parser values and set agree flags themselves), the
holdout annotation is BLIND: agents only saw case_number + PDF. Agreement is
computed here, programmatically, against the parser values sampled from the
post-reextraction DB (scripts/21). Mismatches are printed with evidence quotes
for human adjudication — an agent annotation error must not count against G2.

Coding: agree=1, disagree=0, A=both absent, AMBIGUOUS=excluded (reported).
ACQUITTED convention: truth is "no prison term"; parser NULL or 0 both agree.

Usage: python -m scripts.22_holdout_accuracy
"""
import re
from pathlib import Path

import pandas as pd
from statsmodels.stats.proportion import proportion_confint

ROOT = Path(__file__).resolve().parent.parent
GS = ROOT / "data" / "golden_set"
FIELDS = ["vonis", "tuntutan", "kerugian", "daerah", "tahun", "nama"]
PARSER_COL = {"vonis": "parser_vonis_bulan", "tuntutan": "parser_tuntutan_bulan",
              "kerugian": "parser_kerugian_negara", "daerah": "parser_daerah",
              "tahun": "parser_tahun", "nama": "parser_nama_terdakwa"}
HUMAN_COL = {"vonis": "human_vonis_bulan", "tuntutan": "human_tuntutan_bulan",
             "kerugian": "human_kerugian_negara", "daerah": "human_daerah",
             "tahun": "human_tahun", "nama": "human_nama_terdakwa"}


def norm_case(s):
    s = re.sub(r"\s+", " ", str(s).upper()).strip()
    return re.sub(r"\s*/\s*", "/", s)


def as_num(v):
    """Parse a numeric cell: float, ABSENT/empty -> None, ACQUITTED/AMBIGUOUS markers."""
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


def judge(field, parser_v, human_v):
    p = as_num(parser_v) if field in ("vonis", "tuntutan", "kerugian", "tahun") \
        else as_str(parser_v)
    h = as_num(human_v) if field in ("vonis", "tuntutan", "kerugian", "tahun") \
        else as_str(human_v)
    if h == "AMBIGUOUS" or p == "AMBIGUOUS":
        return "AMBIGUOUS"
    if h == "ACQUITTED":
        return "A" if (p is None or p == 0) else "0"
    if p is None and h is None:
        return "A"
    if p is None or h is None:
        return "0"
    if field == "kerugian":
        # Annotators write whole rupiah; the parser keeps the cents printed in
        # the verdict ("Rp25.356.820.524,74"). A 0.5 tolerance scored those as
        # disagreements even though the figures are identical to the rupiah
        # (holdout R6: 2218 PK/2025, 1694 K/2021).
        return "1" if abs(p - h) < 1.0 else "0"
    if field in ("vonis", "tuntutan", "tahun"):
        return "1" if abs(p - h) < 0.5 else "0"
    return "1" if str(p).upper() == str(h).upper() else "0"


def main():
    tpl = pd.read_csv(GS / "holdout_20_template.csv", dtype=str)
    # R1-R5 used two annotator batches; R6 (n=50) uses five. Read whatever
    # batches are present so the round size is not hard-coded here.
    batches = sorted(GS.glob("holdout_validation_[A-Z].csv"))
    assert batches, "no holdout_validation_<X>.csv batches found"
    print(f"Batch anotator: {', '.join(p.stem[-1] for p in batches)}")
    val = pd.concat([pd.read_csv(p, dtype=str) for p in batches],
                    ignore_index=True)
    tpl["key"] = tpl["case_number"].map(norm_case)
    val["key"] = val["case_number"].map(norm_case)
    keep = ["key"] + list(HUMAN_COL.values()) + \
           ["evidence_vonis", "evidence_tuntutan", "evidence_kerugian", "notes"]
    merged = tpl.drop(columns=[c for c in tpl.columns
                               if c.startswith(("human_", "evidence_")) or c == "notes"]) \
                .merge(val[keep], on="key", how="left")
    assert merged[HUMAN_COL["tahun"]].notna().all(), \
        "unmatched holdout rows — check case_number normalization in the batch CSVs"

    for f in FIELDS:
        merged[f + "_agree"] = [judge(f, r[PARSER_COL[f]], r[HUMAN_COL[f]])
                                for _, r in merged.iterrows()]
    out = GS / "holdout_20_validated.csv"
    merged.drop(columns=["key"]).to_csv(out, index=False)

    print(f"{'field':>10} {'agree':>6} {'n':>4} {'acc':>7} {'wilson95':>16}  ambiguous")
    for f in FIELDS:
        col = merged[f + "_agree"]
        scored = col[col.isin(["1", "0", "A"])]
        agree, n = scored.isin(["1", "A"]).sum(), len(scored)
        amb = (col == "AMBIGUOUS").sum()
        if n:
            lo, hi = proportion_confint(agree, n, method="wilson")
            print(f"{f:>10} {agree:>6} {n:>4} {agree/n:>6.1%} [{lo:>6.1%}, {hi:>6.1%}]  {amb}")

    print("\nMISMATCHES (adjudicate each against the PDF before the G2 verdict):")
    for _, r in merged.iterrows():
        for f in FIELDS:
            if r[f + "_agree"] == "0":
                ev = r.get(f"evidence_{f}", "") if f in ("vonis", "tuntutan", "kerugian") else ""
                print(f"\n  {r['case_number']} [{f}] parser={r[PARSER_COL[f]]} "
                      f"human={r[HUMAN_COL[f]]}\n    evidence: {ev}\n    notes: {r.get('notes','')}")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
