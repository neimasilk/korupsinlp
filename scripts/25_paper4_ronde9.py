"""Paper 4 headline numbers, ronde-9 (session 21).

Reproducible generator of every number cited in paper4_draft.md, computed on the
AUTHORITATIVE analysis sample: is_tipikor=1, valid tuntutan/vonis/kerugian/tahun,
drop implausible kerugian < Rp 1 juta (parse errors) -> n=262 (live DB per 2026-07-29).

This supersedes the ad-hoc numbers scattered across scripts 16 (broad sample, mixed n)
and the stale paper snapshot (n=290, pre-tipikor-filter, pre-ronde-9). All figures below
are what the paper must report. Run after any parser change + scripts.23 tipikor audit.

Usage:  python scripts/25_paper4_ronde9.py
"""
import sqlite3
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats as scipy_stats

DB = r"D:\documents\korupsinlp\data\korupsinlp.db"
RNG = np.random.default_rng(20260729)  # reproducible bootstrap


def load(drop_lt=1_000_000):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(
        """
        SELECT id, case_number, vonis_bulan, tuntutan_bulan, kerugian_negara,
               tahun, daerah, pertimbangan_text
        FROM verdicts
        WHERE tuntutan_bulan IS NOT NULL AND tuntutan_bulan > 0
          AND vonis_bulan   IS NOT NULL AND vonis_bulan > 0
          AND kerugian_negara IS NOT NULL AND kerugian_negara > 0
          AND tahun IS NOT NULL
          AND is_tipikor = 1
        """,
        conn,
    )
    conn.close()
    n0 = len(df)
    df = df[df["kerugian_negara"] >= drop_lt].copy()
    df["vonis_years"] = df["vonis_bulan"] / 12
    df["tuntutan_years"] = df["tuntutan_bulan"] / 12
    df["discount"] = df["vonis_years"] / df["tuntutan_years"]
    txt = df["pertimbangan_text"].fillna("").str.lower()
    df["has_p2"] = txt.str.contains(r"pasal\s+2\b", regex=True).astype(int)
    df["has_p3"] = txt.str.contains(r"pasal\s+3\b", regex=True).astype(int)
    df["has_restitution"] = txt.str.contains(
        r"pengembalian|pemulihan|mengganti kerugian", regex=True
    ).astype(int)
    df["log_k"] = np.log(df["kerugian_negara"])
    df["log_t"] = np.log(df["tuntutan_years"])
    df["log_v"] = np.log(df["vonis_years"])
    df["tahun_c"] = df["tahun"] - df["tahun"].median()
    return df, n0


def bootstrap_elasticity(df, dv_log, B=2000):
    """Bootstrap CI for log-log elasticity of dv_log w.r.t. log_k."""
    x = df["log_k"].values
    y = df[dv_log].values
    n = len(df)
    X = sm.add_constant(x)
    hat = sm.OLS(y, X).fit()
    point = hat.params[1]
    boots = np.empty(B)
    idx_all = np.arange(n)
    for b in range(B):
        idx = RNG.choice(idx_all, n, replace=True)
        xb = np.column_stack([np.ones(n), x[idx]])
        try:
            boots[b] = np.linalg.lstsq(xb, y[idx], rcond=None)[0][1]
        except Exception:
            boots[b] = np.nan
    boots = boots[~np.isnan(boots)]
    return point, np.percentile(boots, [2.5, 97.5])


def fit(dv, xcols, df):
    X = sm.add_constant(df[xcols])
    return sm.OLS(df[dv].values, X).fit()


def main():
    df, n0 = load()
    print("=" * 70)
    print("PAPER 4 — RONDE-9 NUMBERS (authoritative sample)")
    print("=" * 70)
    print(f"\n[Sample] is_tipikor=1, valid fields, drop <Rp1jt: n0={n0} -> n={len(df)}")

    # ---- 1. Elasticities + bootstrap CI ----
    print("\n[1] LOG-LOG ELASTICITY (w.r.t. kerugian)")
    for dv, lab in [("log_t", "tuntutan"), ("log_v", "vonis")]:
        m = fit(dv, ["log_k"], df)
        pt, ci = bootstrap_elasticity(df, dv)
        print(f"  {lab:8}: b={m.params['log_k']:.4f}  SE={m.bse['log_k']:.4f}  "
              f"R2={m.rsquared:.3f}  bootstrap95%CI=[{ci[0]:.3f}, {ci[1]:.3f}]")

    # ---- 2. Practical-terms table (predicted demand & sentence) ----
    print("\n[2] PREDICTED DEMAND/SENTENCE BY LOSS MAGNITUDE (from log-log)")
    mt = fit("log_t", ["log_k"], df)
    mv = fit("log_v", ["log_k"], df)
    base = 1e7
    print(f"  {'loss':>14} {'tuntutan':>9} {'vonis':>9} {'ratio_t':>7}")
    for L in [1e7, 1e8, 1e9, 1e10, 1e11]:
        lk = np.log(L)
        t = np.exp(mt.params[0] + mt.params[1] * lk)
        v = np.exp(mv.params[0] + mv.params[1] * lk)
        print(f"  Rp{L:>.0f}  {t:>7.1f}yr {v:>7.1f}yr {t/np.exp(mt.params[0]+mt.params[1]*np.log(base)):>6.2f}x")
    print(f"  mega/petty tuntutan ratio (1e11/1e7) = "
          f"{np.exp(mt.params[1]*(np.log(1e11)-np.log(1e7))):.2f}x  "
          f"(proportional would be 10000x)")

    # ---- 3. Robustness (elasticity of tuntutan) ----
    print("\n[3] ROBUSTNESS — elasticity(tuntutan ~ kerugian), alternative specs")
    rows = []
    full, _ = load(drop_lt=0)
    for label, d in [("Full (uncleaned, is_tipikor)", full),
                     ("Drop <Rp1jt  [PRIMARY]", df)]:
        m = fit("log_t", ["log_k"], d)
        rows.append((label, len(d), m.params["log_k"], m.rsquared))
    # + dedupe mega-case co-defendants (identical max kerugian, the 3 timah rows)
    maxk = df["kerugian_negara"].max()
    dedup = df[~((df["kerugian_negara"] == maxk) & df.duplicated("kerugian_negara"))].copy()
    # keep only one row at the max value
    at_max = df[df["kerugian_negara"] == maxk]
    dedup = pd.concat([df[df["kerugian_negara"] != maxk], at_max.head(1)]).sort_values("id")
    m = fit("log_t", ["log_k"], dedup)
    rows.append(("+ dedupe mega-case co-defs", len(dedup), m.params["log_k"], m.rsquared))
    # winsorize 1-99 pct on kerugian
    win = df.copy()
    lo, hi = win["kerugian_negara"].quantile([0.01, 0.99])
    win["kerugian_negara"] = win["kerugian_negara"].clip(lo, hi)
    win["log_k"] = np.log(win["kerugian_negara"])
    m = fit("log_t", ["log_k"], win)
    rows.append(("Winsorized 1-99 pct", len(win), m.params["log_k"], m.rsquared))
    print(f"  {'spec':<32} {'n':>4} {'elast':>7} {'R2':>6}")
    for lab, n, e, r in rows:
        print(f"  {lab:<32} {n:>4} {e:>7.3f} {r:>6.3f}")

    # ---- 4. Fair comparison + anchor ----
    print("\n[4] FAIR COMPARISON (same case-fact predictors, both DVs)")
    FACTS = ["log_k", "has_p2", "has_p3", "tahun_c"]
    mtf = fit("tuntutan_years", FACTS, df)
    mvf = fit("vonis_years", FACTS, df)
    ma = fit("vonis_years", ["tuntutan_years"], df)
    print(f"  R2(tuntutan|facts) = {mtf.rsquared:.3f}  (P2 b={mtf.params['has_p2']:+.3f} p={mtf.pvalues['has_p2']:.3f}, "
          f"P3 b={mtf.params['has_p3']:+.3f} p={mtf.pvalues['has_p3']:.3f}, tahun_c b={mtf.params['tahun_c']:+.3f} p={mtf.pvalues['tahun_c']:.3f})")
    print(f"  R2(vonis|facts)    = {mvf.rsquared:.3f}  (P2 b={mvf.params['has_p2']:+.3f} p={mvf.pvalues['has_p2']:.3f})")
    print(f"  R2(vonis|tuntutan) = {ma.rsquared:.3f}  [anchor]")
    print(f"  gap = R2(tuntutan)-R2(vonis) = {mtf.rsquared - mvf.rsquared:+.3f}")

    # ---- 5. Discount stats ----
    print("\n[5] SENTENCING DISCOUNT (vonis/tuntutan)")
    d = df["discount"]
    print(f"  mean={d.mean():.3f}  median={d.median():.3f}  "
          f"%vonis<tuntutan={(d<1).mean()*100:.1f}%  "
          f"restitution mentioned={df['has_restitution'].mean()*100:.0f}%")

    # ---- 6. Temporal ----
    print("\n[6] TEMPORAL (on n=%d elastic sample)" % len(df))
    rt = df.groupby("tahun")["tuntutan_years"].mean()
    print("  mean tuntutan by year:", {int(y): round(v, 2) for y, v in rt.items()})
    rho_t, p_t = scipy_stats.spearmanr(df["tahun"], df["tuntutan_years"])
    rho_d, p_d = scipy_stats.spearmanr(df["tahun"], df["discount"])
    print(f"  Spearman(tuntutan,year): rho={rho_t:.3f} p={p_t:.4f}")
    print(f"  Spearman(discount,year): rho={rho_d:.3f} p={p_d:.4f}")
    early = df[df["tahun"].between(2014, 2015)]["tuntutan_years"].mean()
    late = df[df["tahun"].between(2025, 2026)]["tuntutan_years"].mean()
    print(f"  mean tuntutan 2014-15={early:.1f}yr -> 2025-26={late:.1f}yr")

    # ---- 7. Geographic ----
    print("\n[7] GEOGRAPHIC (on n=%d elastic sample)" % len(df))
    g = df.dropna(subset=["daerah"]).copy()
    g = g[g["daerah"].astype(str).str.len() > 1]
    H_raw, p_raw = scipy_stats.kruskal(*[grp["tuntutan_years"].values for _, grp in g.groupby("daerah")])
    # residual after kerugian
    res = fit("tuntutan_years", ["log_k"], g).resid
    g["_res"] = res
    H_res, p_res = scipy_stats.kruskal(*[grp["_res"].values for _, grp in g.groupby("daerah")])
    print(f"  KW(tuntutan by daerah): raw H={H_raw:.1f} p={p_raw:.5f}  | "
          f"residual(after kerugian) H={H_res:.1f} p={p_res:.4f}")
    print(f"  n daerah groups={g['daerah'].nunique()}, n with province={len(g)}")

    # ---- 8. Marginal deterrence ----
    print("\n[8] MARGINAL DETERRENCE (Rp10jt -> Rp100B, from tuntutan log-log)")
    t10m = np.exp(mt.params[0] + mt.params[1] * np.log(1e7))
    t100b = np.exp(mt.params[0] + mt.params[1] * np.log(1e11))
    delta_yr = t100b - t10m
    delta_rp = 1e11 - 1e7
    print(f"  tuntutan(Rp10jt)={t10m:.1f}yr  tuntutan(Rp100B)={t100b:.1f}yr  "
          f"delta={delta_yr:.1f}yr  -> Rp{delta_rp/delta_yr/1e9:.1f}B per added prison-year")
    drop = 1 - (t10m / t100b) / ((1e11) / 1e7)  # price per rupiah relative to proportional
    print(f"  'price' (yr per rupiah) falls by ~{(1-((t100b/1e11)/(t10m/1e7)))*100:.2f}% from Rp10jt to Rp100B")

    # ---- 9. Sample composition (for methods) ----
    print("\n[9] SAMPLE COMPOSITION (for methods §3.1)")
    conn = sqlite3.connect(DB)
    tot = conn.execute("SELECT COUNT(*) FROM verdicts").fetchone()[0]
    tipikor = conn.execute("SELECT COUNT(*) FROM verdicts WHERE is_tipikor=1").fetchone()[0]
    conn.close()
    print(f"  total scraped verdicts in DB={tot}  is_tipikor=1={tipikor}")
    print(f"  with valid tuntutan+vonis+kerugian+tahun (tipikor)={n0}  -> drop<1jt -> n={len(df)}")
    print(f"  kerugian range: Rp{df['kerugian_negara'].min():,.0f} .. Rp{df['kerugian_negara'].max():,.0f}  "
          f"median Rp{df['kerugian_negara'].median():,.0f}")
    n_below_4 = (df["tuntutan_years"] < 4).sum()
    print(f"  tuntutan<4yr: n={n_below_4} (statutory-floor robustness subsample)")


if __name__ == "__main__":
    main()
