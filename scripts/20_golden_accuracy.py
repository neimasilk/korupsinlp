"""Script 20: Merge golden-set expansion validation batches + per-field accuracy.

Usage: python scripts/20_golden_accuracy.py <batchA.csv> <batchB.csv>
Merges agent-validated batches with the 30-case template, computes per-field
agreement with Wilson 95% CI, and writes data/golden_set/golden_expansion_30_validated.csv.
Agreement coding: 1 or A (both absent) = agree; 0 = disagree; AMBIGUOUS = excluded, reported.
"""
import sys
from pathlib import Path

import pandas as pd
from statsmodels.stats.proportion import proportion_confint

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["vonis", "tuntutan", "kerugian", "daerah", "tahun", "nama"]
HUMAN_COL = {"vonis": "human_vonis_bulan", "tuntutan": "human_tuntutan_bulan",
             "kerugian": "human_kerugian_negara", "daerah": "human_daerah",
             "tahun": "human_tahun", "nama": "human_nama_terdakwa"}


def main():
    def norm(s):
        return (s.astype(str).str.upper().str.replace(r"\s+", " ", regex=True)
                 .str.replace(r"\s*/\s*", "/", regex=True).str.strip())

    batches = [pd.read_csv(p, dtype=str) for p in sys.argv[1:3]]
    val = pd.concat(batches, ignore_index=True)
    val["case_number"] = norm(val["case_number"])
    tpl = pd.read_csv(ROOT / "data/golden_set/golden_expansion_30_template.csv", dtype=str)
    tpl["case_number"] = norm(tpl["case_number"])
    merged = tpl.drop(columns=[c for c in tpl.columns if c.startswith("human_")
                               or c.startswith("evidence_") or c == "notes"]) \
                .merge(val, on="case_number", how="left")

    out = ROOT / "data/golden_set/golden_expansion_30_validated.csv"
    merged.to_csv(out, index=False)
    print(f"Merged {len(val)} validated / {len(tpl)} sampled -> {out}\n")

    print(f"{'field':>10} {'agree':>6} {'n':>4} {'acc':>7} {'wilson95':>16}  ambiguous")
    for f in FIELDS:
        col = merged[f"{f}_agree"].astype(str).str.strip().str.upper()
        amb = (col == "AMBIGUOUS").sum() + \
              merged[HUMAN_COL[f]].astype(str).str.contains("AMBIGUOUS").sum()
        scored = col[col.isin(["1", "0", "A"])]
        agree = scored.isin(["1", "A"]).sum()
        n = len(scored)
        if n:
            lo, hi = proportion_confint(agree, n, method="wilson")
            print(f"{f:>10} {agree:>6} {n:>4} {agree/n:>6.1%} [{lo:>6.1%}, {hi:>6.1%}]  {amb}")
    print("\nMismatches (parser vs truth):")
    for _, r in merged.iterrows():
        for f in FIELDS:
            if str(r.get(f"{f}_agree", "")).strip() == "0":
                print(f"  {r['case_number']} [{f}]: {r.get('notes', '')}")
    print("\nLegacy golden set (for the paper's combined table): vonis 20/20 (golden_20);"
          " tuntutan/kerugian/daerah/tahun/nama 5/5 each (golden_5).")


if __name__ == "__main__":
    main()
