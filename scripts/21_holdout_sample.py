"""Script 21: Sample 20 FRESH holdout cases for post-reextraction parser validation.

Anti-overfit check demanded by GATES.md G2: golden30 drove the D14 parser fix, so
accuracy must be confirmed on cases the fix never saw. Design mirrors session 17
expansion (stratified by kerugian tercile + no-kerugian stratum), scaled to 20:
  15 from the elasticity population (5 per kerugian tercile), 5 with kerugian NULL.
Excludes every case already in any golden set (30 expansion + 20 + 5 legacy).
Parser values are read from the CURRENT (post-reextraction) DB — accuracy is
measured against the values the paper will actually use.

Usage: python -m scripts.21_holdout_sample
Output: data/golden_set/holdout_20_template.csv
"""
import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "korupsinlp.db"
OUT = ROOT / "data" / "golden_set" / "holdout_20_template.csv"
SEED = 20260716

GOLDEN_FILES = [
    "golden_expansion_30_template.csv",
    "golden_20_verified.csv",
    "golden_5_verified.csv",
    "holdout_r1_validated.csv",  # holdout R1 drove parser fix round 2 -> now training
    "holdout_r2_validated.csv",  # holdout R2 drove parser fix round 3 -> now training
    "holdout_20_template.csv",   # current round's template -> also excluded
]


def norm(s: str) -> str:
    s = re.sub(r"\s+", " ", str(s).upper()).strip()
    return re.sub(r"\s*/\s*", "/", s)


def main():
    rng = np.random.default_rng(SEED)

    exclude = set()
    for f in GOLDEN_FILES:
        df = pd.read_csv(ROOT / "data" / "golden_set" / f, dtype=str)
        exclude |= {norm(c) for c in df["case_number"]}
    print(f"Excluding {len(exclude)} previously-validated cases")

    con = sqlite3.connect(DB)
    all_pdf = pd.read_sql_query(
        """SELECT case_number, pdf_path, vonis_bulan, tuntutan_bulan,
                  kerugian_negara, daerah, tahun, nama_terdakwa
           FROM verdicts WHERE pdf_path IS NOT NULL""",
        con,
    )
    con.close()

    all_pdf["case_norm"] = all_pdf["case_number"].map(norm)
    all_pdf = all_pdf[~all_pdf["case_norm"].isin(exclude)]
    all_pdf = all_pdf[all_pdf["pdf_path"].map(lambda p: Path(p).exists())]

    elas = all_pdf[
        (all_pdf["tuntutan_bulan"] > 0)
        & (all_pdf["vonis_bulan"] > 0)
        & (all_pdf["kerugian_negara"] >= 1_000_000)
    ].copy()
    no_ker = all_pdf[all_pdf["kerugian_negara"].isna()]
    print(f"Sampling frames: elasticity {len(elas)}, no-kerugian {len(no_ker)}")

    elas["tercile"] = pd.qcut(elas["kerugian_negara"], 3, labels=[0, 1, 2])
    picks = []
    for t in [0, 1, 2]:
        stratum = elas[elas["tercile"] == t]
        picks.append(stratum.iloc[rng.choice(len(stratum), 5, replace=False)])
    picks.append(no_ker.iloc[rng.choice(len(no_ker), 5, replace=False)])
    sample = pd.concat(picks, ignore_index=True)

    tpl = pd.DataFrame({
        "case_number": sample["case_number"],
        "pdf_path": sample["pdf_path"],
        "parser_vonis_bulan": sample["vonis_bulan"],
        "parser_tuntutan_bulan": sample["tuntutan_bulan"],
        "parser_kerugian_negara": sample["kerugian_negara"],
        "parser_daerah": sample["daerah"],
        "parser_tahun": sample["tahun"],
        "parser_nama_terdakwa": sample["nama_terdakwa"],
    })
    for col in ["human_vonis_bulan", "human_tuntutan_bulan", "human_kerugian_negara",
                "human_daerah", "human_tahun", "human_nama_terdakwa",
                "evidence_vonis", "evidence_tuntutan", "evidence_kerugian", "notes"]:
        tpl[col] = ""
    tpl.to_csv(OUT, index=False)
    print(f"Wrote {len(tpl)} holdout cases -> {OUT}")
    print(tpl[["case_number", "parser_kerugian_negara"]].to_string(index=False))


if __name__ == "__main__":
    main()
