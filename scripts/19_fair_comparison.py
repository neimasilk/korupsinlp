"""Fair-comparison regression for Paper 4 revision (session 17).

Paper 4 claims "prosecutors exercise wider discretion than judges" by comparing
  tuntutan ~ log(kerugian)+P2+P3(+tahun)  R2=0.315/0.321   (predictors: case facts)
  vonis ~ tuntutan                        R2=0.600         (predictor: the anchor itself)
That comparison is apples-to-oranges. The fair test: same case-fact predictors, both DVs.
"""
import sqlite3
import numpy as np
import pandas as pd
import statsmodels.api as sm

DB = r"D:\documents\korupsinlp\data\korupsinlp.db"

conn = sqlite3.connect(DB)
df = pd.read_sql_query(
    """
    SELECT id, vonis_bulan, tuntutan_bulan, kerugian_negara, tahun, pertimbangan_text
    FROM verdicts
    WHERE tuntutan_bulan IS NOT NULL AND tuntutan_bulan > 0
      AND vonis_bulan   IS NOT NULL AND vonis_bulan > 0
      AND kerugian_negara IS NOT NULL AND kerugian_negara > 0
      AND tahun IS NOT NULL
    """,
    conn,
)
conn.close()

# Replicate Paper 4 cleaning: drop implausible kerugian < Rp 1 juta (parse errors)
n_before = len(df)
df = df[df["kerugian_negara"] >= 1_000_000].copy()
print(f"n = {len(df)} (dropped {n_before - len(df)} with kerugian < Rp 1 juta; "
      f"paper snapshot was n=290 — live DB has grown since)")

df["vonis_years"] = df["vonis_bulan"] / 12
df["tuntutan_years"] = df["tuntutan_bulan"] / 12
texts = df["pertimbangan_text"].fillna("").str.lower()
df["has_p2"] = texts.str.contains(r"pasal\s+2\b", regex=True).astype(int)
df["has_p3"] = texts.str.contains(r"pasal\s+3\b", regex=True).astype(int)
df["log_kerugian"] = np.log1p(df["kerugian_negara"])
df["tahun_c"] = df["tahun"] - df["tahun"].median()

FACTS = ["log_kerugian", "has_p2", "has_p3", "tahun_c"]


def fit(dv, xcols, label):
    X = sm.add_constant(df[xcols])
    m = sm.OLS(df[dv].values, X).fit()
    print(f"\n  {label}")
    print(f"    R2 = {m.rsquared:.4f}   adjR2 = {m.rsquared_adj:.4f}   n = {int(m.nobs)}")
    for v in xcols:
        print(f"    {v:>14}: b={m.params[v]:+.4f}  p={m.pvalues[v]:.5f}")
    return m


print("\n=== SAME PREDICTORS (case facts), BOTH DVs — the fair comparison ===")
mt = fit("tuntutan_years", FACTS, "tuntutan_years ~ log(kerugian) + P2 + P3 + tahun")
mv = fit("vonis_years",    FACTS, "vonis_years    ~ log(kerugian) + P2 + P3 + tahun")

print("\n=== ANCHOR MODEL (sanity check vs paper's 0.600) ===")
ma = fit("vonis_years", ["tuntutan_years"], "vonis_years ~ tuntutan_years")

print("\n=== LOG-LOG ELASTICITIES (w.r.t. kerugian) ===")
df["log_t"] = np.log(df["tuntutan_years"])
df["log_v"] = np.log(df["vonis_years"])
df["log_k"] = np.log(df["kerugian_negara"])
for dv, lab in [("log_t", "tuntutan"), ("log_v", "vonis")]:
    X = sm.add_constant(df[["log_k"]])
    m = sm.OLS(df[dv].values, X).fit()
    print(f"  elasticity({lab} ~ kerugian) = {m.params['log_k']:.4f} "
          f"(SE {m.bse['log_k']:.4f}, R2={m.rsquared:.3f})")

print("\n=== VERDICT ===")
gap = mt.rsquared - mv.rsquared
print(f"  R2(tuntutan|facts) = {mt.rsquared:.3f}  vs  R2(vonis|facts) = {mv.rsquared:.3f}"
      f"  (gap = {gap:+.3f})")
if abs(gap) < 0.05:
    print("  -> Conditional on case facts, demands and sentences are EQUALLY (un)predictable.")
    print("     'Prosecutors less predictable than judges' is NOT supported;")
    print("     correct claim: discretion enters once, upstream; judges add ~no new noise.")
elif gap > 0:
    print("  -> Sentences are LESS predictable from facts than demands are.")
    print("     The paper's claim is BACKWARDS as written.")
else:
    print("  -> Demands genuinely less predictable than sentences even from same facts.")
    print("     Paper's claim survives the fair comparison; rewrite methods to use this spec.")
