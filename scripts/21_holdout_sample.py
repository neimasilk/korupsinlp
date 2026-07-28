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
    "holdout_r3_validated.csv",  # holdout R3 drove parser fix round 4 -> now training
    "holdout_r4_validated.csv",  # holdout R4 drove parser fix round 5 -> now training
    "holdout_r5_validated.csv",  # holdout R5 (G2 FAILED: vonis 85%, kerugian 80%) -> now training
    "holdout_r6_validated.csv",  # holdout R6 n=50 (G2 PASSED) -> now training
    "holdout_20_template.csv",   # current round's template -> also excluded
]

# Cases that were never ANNOTATED but still drove parser fixes, so they are
# training data in substance (DECISIONS D24: the corpus-wide acquittal /
# missing-amar-anchor scan that motivated fix round 7, plus the round-8
# regression driver). Leaving them in a "fresh" holdout would inflate accuracy
# on exactly the classes just repaired.
FIX_DRIVER_CASES = [
    "1052 K/Pid.Sus/2022", "3247 K/Pid.Sus/2019", "4597 K/Pid.Sus/2021",
    "692 K/PID.SUS/2015", "631 K/PID.SUS/2015", "196 PK/PID.SUS/2014",
    "2240 K/PID.SUS/2014", "1964 K/Pid.Sus/2015", "149/Pid.Sus-TPK/2025/PN Sby",
    "2997 PK/PID.SUS/2025",
]


def norm(s: str) -> str:
    s = re.sub(r"\s+", " ", str(s).upper()).strip()
    return re.sub(r"\s*/\s*", "/", s)


def main(n: int = 20):
    """Sample `n` fresh holdout cases, ~72% from the elasticity population
    (split evenly across kerugian terciles) and the rest from the no-kerugian
    stratum — the R1-R5 proportions (15/5), scaled."""
    rng = np.random.default_rng(SEED)
    per_tercile = int(round(n * 0.72 / 3))
    n_no_ker = n - 3 * per_tercile

    exclude = set()
    for f in GOLDEN_FILES:
        df = pd.read_csv(ROOT / "data" / "golden_set" / f, dtype=str)
        exclude |= {norm(c) for c in df["case_number"]}
    n_annotated = len(exclude)
    exclude |= {norm(c) for c in FIX_DRIVER_CASES}
    print(f"Excluding {len(exclude)} cases: {n_annotated} annotated + "
          f"{len(exclude) - n_annotated} unannotated fix-drivers (D24)")

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
        assert len(stratum) >= per_tercile, f"tercile {t} too small: {len(stratum)}"
        picks.append(stratum.iloc[rng.choice(len(stratum), per_tercile, replace=False)])
    assert len(no_ker) >= n_no_ker, f"no-kerugian stratum too small: {len(no_ker)}"
    picks.append(no_ker.iloc[rng.choice(len(no_ker), n_no_ker, replace=False)])
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
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20,
                    help="holdout size (R1-R5 used 20; R6 pre-registered at 50)")
    main(ap.parse_args().n)
