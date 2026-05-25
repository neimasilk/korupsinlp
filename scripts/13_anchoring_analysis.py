"""Script 13: Anchoring Correction Analysis for Paper 3.

Research question: Do Indonesian judges apply a uniform sentencing discount,
or do they systematically correct prosecution demands toward an internal
reference point?

Key finding: The vonis-tuntutan relationship is concave (significant quadratic
term). Judges INCREASE sentences when tuntutan is low (<~4yr) and DECREASE
when tuntutan is high (>~4yr). This is bidirectional anchoring correction.

Usage: python -m scripts.13_anchoring_analysis
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from autoresearch.prepare import load_corpus

SEED = 42


def text_lower(df):
    return df["pertimbangan_text"].fillna("").str.lower()


def print_section(title):
    print(f"\n\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def main():
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import het_breuschpagan

    corpus = load_corpus(require_text=True).copy()
    texts = text_lower(corpus)
    corpus["has_p2"] = texts.str.contains(r"pasal\s+2\b", regex=True).astype(int)
    corpus["has_p3"] = texts.str.contains(r"pasal\s+3\b", regex=True).astype(int)
    corpus["discount"] = corpus["vonis_years"] / corpus["tuntutan_years"]
    corpus["upward"] = (corpus["vonis_years"] > corpus["tuntutan_years"]).astype(int)
    corpus["tuntutan_sq"] = corpus["tuntutan_years"] ** 2

    # Exclude extreme discount outliers (>5x) for discount analyses
    c = corpus[corpus["discount"].between(0, 5)].copy()
    n = len(c)

    print("=" * 70)
    print("  PAPER 3 ANALYSIS — Anchoring Correction Effect")
    print(f"  Corpus: {len(corpus)} total, {n} for analysis (discount 0-5)")
    print("=" * 70)

    # ==================================================================
    #  TABLE 1: DESCRIPTIVE — Discount by Tuntutan Band
    # ==================================================================
    print_section("TABLE 1: Discount by Prosecution Demand Band")

    bands = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 15), (15, 25)]
    print(f"  {'Band':<15s} {'n':>4s} {'Mean disc':>10s} {'Median':>8s} {'SD':>8s} "
          f"{'% Upward':>10s} {'Mean vonis':>11s}")
    print(f"  {'-'*70}")

    band_stats = []
    for lo, hi in bands:
        sub = c[(c["tuntutan_years"] >= lo) & (c["tuntutan_years"] < hi)]
        if len(sub) >= 3:
            up_pct = 100 * sub["upward"].mean()
            print(f"  {lo}-{hi} years{'':<5s} {len(sub):>4d} {sub['discount'].mean():>10.3f} "
                  f"{sub['discount'].median():>8.3f} {sub['discount'].std():>8.3f} "
                  f"{up_pct:>9.1f}% {sub['vonis_years'].mean():>11.2f}")
            band_stats.append({
                "band": f"{lo}-{hi}", "n": len(sub),
                "mean_disc": sub["discount"].mean(),
                "pct_up": up_pct,
                "mean_tunt": sub["tuntutan_years"].mean(),
                "mean_vonis": sub["vonis_years"].mean()
            })

    # ==================================================================
    #  TABLE 2: LINEAR vs QUADRATIC REGRESSION
    # ==================================================================
    print_section("TABLE 2: Linear vs Quadratic Models")

    y = c["vonis_years"].values

    # Model A: Linear (vonis ~ tuntutan)
    X_lin = sm.add_constant(c[["tuntutan_years"]])
    m_lin = sm.OLS(y, X_lin).fit()

    # Model B: Quadratic (vonis ~ tuntutan + tuntutan^2)
    X_quad = sm.add_constant(c[["tuntutan_years", "tuntutan_sq"]])
    m_quad = sm.OLS(y, X_quad).fit()

    print(f"\n  Model A (Linear): vonis ~ tuntutan")
    print(f"    R2 = {m_lin.rsquared:.4f}, AIC = {m_lin.aic:.1f}")
    print(f"    tuntutan: b={m_lin.params['tuntutan_years']:.4f}, p={m_lin.pvalues['tuntutan_years']:.6f}")
    print(f"    intercept: {m_lin.params['const']:.4f}")

    print(f"\n  Model B (Quadratic): vonis ~ tuntutan + tuntutan^2")
    print(f"    R2 = {m_quad.rsquared:.4f}, AIC = {m_quad.aic:.1f}")
    print(f"    tuntutan: b={m_quad.params['tuntutan_years']:.4f}, p={m_quad.pvalues['tuntutan_years']:.6f}")
    print(f"    tuntutan^2: b={m_quad.params['tuntutan_sq']:.6f}, p={m_quad.pvalues['tuntutan_sq']:.6f}")
    print(f"    intercept: {m_quad.params['const']:.4f}")

    # F-test: quadratic vs linear
    f_test = m_quad.compare_f_test(m_lin)
    print(f"\n  F-test (Quadratic vs Linear): F={f_test[0]:.2f}, p={f_test[1]:.6f}")
    delta_r2 = m_quad.rsquared - m_lin.rsquared
    print(f"  Delta R2: {delta_r2:.4f}")
    print(f"  Quadratic term significant: {'YES' if f_test[1] < 0.05 else 'NO'}")

    # Predicted crossover point (where predicted vonis = tuntutan)
    # a + b*t + c*t^2 = t => a + (b-1)*t + c*t^2 = 0
    a_coef = m_quad.params["const"]
    b_coef = m_quad.params["tuntutan_years"] - 1
    c_coef = m_quad.params["tuntutan_sq"]
    discriminant = b_coef**2 - 4 * c_coef * a_coef
    if discriminant >= 0:
        t1 = (-b_coef + np.sqrt(discriminant)) / (2 * c_coef)
        t2 = (-b_coef - np.sqrt(discriminant)) / (2 * c_coef)
        crossover = min(t for t in [t1, t2] if 0 < t < 25)
        print(f"\n  Crossover point (discount=1): tuntutan = {crossover:.1f} years")
        print(f"  Below {crossover:.0f}yr: judges tend to INCREASE sentences")
        print(f"  Above {crossover:.0f}yr: judges tend to DECREASE sentences")
    else:
        crossover = None
        print(f"\n  No real crossover point found")

    # ==================================================================
    #  TABLE 3: PIECEWISE LINEAR (below/above crossover)
    # ==================================================================
    print_section("TABLE 3: Piecewise Linear Regression")

    if crossover:
        cut = round(crossover)
        below = c[c["tuntutan_years"] < cut]
        above = c[c["tuntutan_years"] >= cut]

        X_lo = sm.add_constant(below[["tuntutan_years"]])
        m_lo = sm.OLS(below["vonis_years"].values, X_lo).fit()

        X_hi = sm.add_constant(above[["tuntutan_years"]])
        m_hi = sm.OLS(above["vonis_years"].values, X_hi).fit()

        print(f"  Cutpoint: {cut} years")
        print(f"\n  Below {cut}yr (n={len(below)}):")
        print(f"    slope = {m_lo.params['tuntutan_years']:.3f}, intercept = {m_lo.params['const']:.3f}")
        print(f"    R2 = {m_lo.rsquared:.4f}")
        print(f"    Interpretation: each 1yr tuntutan increase -> {m_lo.params['tuntutan_years']:.2f}yr vonis increase")

        print(f"\n  Above {cut}yr (n={len(above)}):")
        print(f"    slope = {m_hi.params['tuntutan_years']:.3f}, intercept = {m_hi.params['const']:.3f}")
        print(f"    R2 = {m_hi.rsquared:.4f}")
        print(f"    Interpretation: each 1yr tuntutan increase -> {m_hi.params['tuntutan_years']:.2f}yr vonis increase")

        # Chow test (structural break)
        rss_pooled = m_lin.ssr
        rss_split = m_lo.ssr + m_hi.ssr
        k = 2  # parameters per segment
        f_chow = ((rss_pooled - rss_split) / k) / (rss_split / (n - 2 * k))
        p_chow = 1 - stats.f.cdf(f_chow, k, n - 2 * k)
        print(f"\n  Chow test for structural break at {cut}yr:")
        print(f"    F = {f_chow:.2f}, p = {p_chow:.6f}")
        print(f"    Structural break: {'YES' if p_chow < 0.05 else 'NO'}")

    # ==================================================================
    #  TABLE 4: UPWARD DEPARTURE ANALYSIS
    # ==================================================================
    print_section("TABLE 4: Upward Departure Analysis")

    n_up = corpus["upward"].sum()
    print(f"  Upward departures: {n_up} / {len(corpus)} ({100*n_up/len(corpus):.1f}%)")
    print(f"  Mean upward case: vonis={corpus[corpus['upward']==1]['vonis_years'].mean():.2f}, "
          f"tuntutan={corpus[corpus['upward']==1]['tuntutan_years'].mean():.2f}")
    print(f"  Mean downward case: vonis={corpus[corpus['upward']==0]['vonis_years'].mean():.2f}, "
          f"tuntutan={corpus[corpus['upward']==0]['tuntutan_years'].mean():.2f}")

    # Logistic regression: upward ~ tuntutan + charge type
    X_logit = sm.add_constant(corpus[["tuntutan_years", "has_p2", "has_p3"]])
    m_logit = sm.Logit(corpus["upward"].values, X_logit).fit(disp=0)

    print(f"\n  Logistic regression: P(upward) ~ tuntutan + P2 + P3")
    for var in ["tuntutan_years", "has_p2", "has_p3"]:
        or_val = np.exp(m_logit.params[var])
        print(f"    {var}: coef={m_logit.params[var]:.3f}, OR={or_val:.3f}, p={m_logit.pvalues[var]:.4f}")

    print(f"    Pseudo R2 = {m_logit.prsquared:.4f}")
    print(f"\n  Interpretation: Each 1yr increase in tuntutan reduces odds of upward ")
    print(f"  departure by {(1-np.exp(m_logit.params['tuntutan_years']))*100:.1f}%")

    # ==================================================================
    #  TABLE 5: CONTROLLING FOR CASE CHARACTERISTICS
    # ==================================================================
    print_section("TABLE 5: Quadratic Effect Controlling for Case Characteristics")

    # Does the quadratic term survive after controlling for charge type?
    X_full = sm.add_constant(c[["tuntutan_years", "tuntutan_sq", "has_p2", "has_p3"]])
    m_full = sm.OLS(y, X_full).fit()

    print(f"  Model C: vonis ~ tuntutan + tuntutan^2 + P2 + P3")
    print(f"    R2 = {m_full.rsquared:.4f}")
    for var in ["tuntutan_years", "tuntutan_sq", "has_p2", "has_p3"]:
        ci = m_full.conf_int().loc[var]
        print(f"    {var}: b={m_full.params[var]:.4f} [{ci[0]:.4f}, {ci[1]:.4f}], "
              f"p={m_full.pvalues[var]:.6f}")

    print(f"\n  Quadratic term survives charge type control: "
          f"{'YES' if m_full.pvalues['tuntutan_sq'] < 0.05 else 'NO'}")

    # Add kerugian
    has_k = c[c["kerugian_negara"] > 0].copy()
    has_k["log_kerugian"] = np.log1p(has_k["kerugian_negara"])
    X_kerugian = sm.add_constant(has_k[["tuntutan_years", "tuntutan_sq", "has_p2", "has_p3", "log_kerugian"]])
    m_kerugian = sm.OLS(has_k["vonis_years"].values, X_kerugian).fit()
    print(f"\n  Model D: + log(kerugian) (n={len(has_k)})")
    print(f"    R2 = {m_kerugian.rsquared:.4f}")
    print(f"    tuntutan^2: b={m_kerugian.params['tuntutan_sq']:.6f}, p={m_kerugian.pvalues['tuntutan_sq']:.6f}")
    print(f"    Quadratic survives kerugian control: "
          f"{'YES' if m_kerugian.pvalues['tuntutan_sq'] < 0.05 else 'NO'}")

    # ==================================================================
    #  TABLE 6: JUDGE-LEVEL ANCHORING PATTERNS
    # ==================================================================
    print_section("TABLE 6: Judge-Level Anchoring Patterns")

    import sqlite3
    from src.config import DB_PATH

    conn = sqlite3.connect(str(DB_PATH))
    hakim_df = pd.read_sql_query(
        f"SELECT id, nama_hakim FROM verdicts WHERE id IN ({','.join(str(i) for i in c['id'])})", conn)
    conn.close()
    merged = c.merge(hakim_df, on="id", how="left")

    def get_ketua(x):
        if pd.isna(x):
            return "unknown"
        return x.split(";")[0].replace("Hakim Ketua", "").strip() or "unknown"

    merged["ketua"] = merged["nama_hakim"].apply(get_ketua)
    freq = merged["ketua"].value_counts()
    freq_judges = [j for j in freq.index if freq[j] >= 5 and j != "unknown"]

    print(f"  Judges with >= 5 cases: {len(freq_judges)}")
    print(f"\n  {'Judge':<30s} {'n':>4s} {'Mean disc':>10s} {'% Upward':>10s} {'Slope':>7s}")
    print(f"  {'-'*65}")

    judge_slopes = []
    for j in sorted(freq_judges):
        sub = merged[merged["ketua"] == j]
        slope = np.polyfit(sub["tuntutan_years"], sub["vonis_years"], 1)[0] if len(sub) >= 3 else np.nan
        up_pct = 100 * sub["upward"].mean()
        print(f"  {j[:30]:<30s} {len(sub):>4d} {sub['discount'].mean():>10.3f} "
              f"{up_pct:>9.1f}% {slope:>7.3f}")
        judge_slopes.append(slope)

    judge_slopes = [s for s in judge_slopes if not np.isnan(s)]
    if judge_slopes:
        print(f"\n  Mean judge slope: {np.mean(judge_slopes):.3f} (range [{min(judge_slopes):.3f}, {max(judge_slopes):.3f}])")
        print(f"  Overall slope: {m_lin.params['tuntutan_years']:.3f}")

    # ==================================================================
    #  TABLE 7: ROBUSTNESS
    # ==================================================================
    print_section("TABLE 7: Robustness Checks")

    # 7a: HC3 robust SE
    m_quad_hc3 = m_quad.get_robustcov_results(cov_type="HC3")
    print(f"  HC3 robust SE for quadratic term:")
    print(f"    OLS: b={m_quad.params['tuntutan_sq']:.6f}, SE={m_quad.bse['tuntutan_sq']:.6f}, "
          f"p={m_quad.pvalues['tuntutan_sq']:.6f}")
    print(f"    HC3: b={m_quad_hc3.params[2]:.6f}, SE={m_quad_hc3.bse[2]:.6f}, "
          f"p={m_quad_hc3.pvalues[2]:.6f}")

    # 7b: Bootstrap crossover CI
    np.random.seed(SEED)
    boot_crossovers = []
    for _ in range(2000):
        idx = np.random.choice(n, n, replace=True)
        Xb = X_quad.values[idx]
        yb = y[idx]
        try:
            mb = sm.OLS(yb, Xb).fit()
            ab = mb.params[0]
            bb = mb.params[1] - 1
            cb = mb.params[2]
            disc_b = bb**2 - 4*cb*ab
            if disc_b >= 0:
                roots = [(-bb + np.sqrt(disc_b))/(2*cb), (-bb - np.sqrt(disc_b))/(2*cb)]
                valid = [r for r in roots if 0 < r < 25]
                if valid:
                    boot_crossovers.append(min(valid))
        except Exception:
            pass

    if boot_crossovers:
        bc = np.array(boot_crossovers)
        print(f"\n  Bootstrap crossover point (2000 iterations):")
        print(f"    Mean: {bc.mean():.1f} years")
        print(f"    95% CI: [{np.percentile(bc, 2.5):.1f}, {np.percentile(bc, 97.5):.1f}] years")
        print(f"    Valid bootstraps: {len(bc)}/2000")

    # 7c: Temporal stability
    pre_2024 = c[c["tahun"] < 2024]
    post_2024 = c[c["tahun"] >= 2024]
    for label, sub in [("Pre-2024", pre_2024), ("2024+", post_2024)]:
        if len(sub) >= 30:
            sub_sq = sub.copy()
            sub_sq["tuntutan_sq"] = sub_sq["tuntutan_years"] ** 2
            Xs = sm.add_constant(sub_sq[["tuntutan_years", "tuntutan_sq"]])
            ms = sm.OLS(sub_sq["vonis_years"].values, Xs).fit()
            print(f"\n  {label} (n={len(sub)}):")
            print(f"    tuntutan^2: b={ms.params['tuntutan_sq']:.6f}, p={ms.pvalues['tuntutan_sq']:.4f}")

    # 7d: Excluding outlier discount
    c_strict = corpus[corpus["discount"].between(0.1, 3)].copy()
    c_strict["tuntutan_sq"] = c_strict["tuntutan_years"] ** 2
    X_strict = sm.add_constant(c_strict[["tuntutan_years", "tuntutan_sq"]])
    m_strict = sm.OLS(c_strict["vonis_years"].values, X_strict).fit()
    print(f"\n  Excluding extreme discounts (0.1-3.0, n={len(c_strict)}):")
    print(f"    tuntutan^2: b={m_strict.params['tuntutan_sq']:.6f}, p={m_strict.pvalues['tuntutan_sq']:.6f}")

    # ==================================================================
    #  TABLE 8: EFFECT SIZE — Compression Ratio
    # ==================================================================
    print_section("TABLE 8: Sentencing Compression")

    # How much does the judicial process compress the sentencing range?
    tunt_range = c["tuntutan_years"].max() - c["tuntutan_years"].min()
    vonis_range = c["vonis_years"].max() - c["vonis_years"].min()
    tunt_sd = c["tuntutan_years"].std()
    vonis_sd = c["vonis_years"].std()
    tunt_iqr = c["tuntutan_years"].quantile(0.75) - c["tuntutan_years"].quantile(0.25)
    vonis_iqr = c["vonis_years"].quantile(0.75) - c["vonis_years"].quantile(0.25)

    print(f"  Tuntutan: range={tunt_range:.1f}, SD={tunt_sd:.2f}, IQR={tunt_iqr:.2f}")
    print(f"  Vonis:    range={vonis_range:.1f}, SD={vonis_sd:.2f}, IQR={vonis_iqr:.2f}")
    print(f"  Compression ratio (SD): {vonis_sd/tunt_sd:.3f}")
    print(f"  Compression ratio (IQR): {vonis_iqr/tunt_iqr:.3f}")
    print(f"  Judges compress the sentencing range to ~{100*vonis_sd/tunt_sd:.0f}% "
          f"of prosecution demand range")

    # ==================================================================
    #  SUMMARY
    # ==================================================================
    print_section("KEY NUMBERS FOR PAPER 3")

    print(f"  Corpus: {n} (discount 0-5)")
    print(f"  Upward departures: {n_up}/{len(corpus)} ({100*n_up/len(corpus):.1f}%)")
    print(f"  Linear R2: {m_lin.rsquared:.4f}")
    print(f"  Quadratic R2: {m_quad.rsquared:.4f} (delta={delta_r2:.4f})")
    print(f"  Quadratic term: b={m_quad.params['tuntutan_sq']:.6f}, p={m_quad.pvalues['tuntutan_sq']:.6f}")
    print(f"  F-test (quad vs lin): F={f_test[0]:.2f}, p={f_test[1]:.6f}")
    if crossover:
        print(f"  Crossover: {crossover:.1f} years")
        if boot_crossovers:
            print(f"  Crossover 95% CI: [{np.percentile(bc, 2.5):.1f}, {np.percentile(bc, 97.5):.1f}]")
    print(f"  Compression ratio: {vonis_sd/tunt_sd:.3f} (SD), {vonis_iqr/tunt_iqr:.3f} (IQR)")
    print(f"  Upward departure OR(tuntutan): {np.exp(m_logit.params['tuntutan_years']):.3f} "
          f"(p={m_logit.pvalues['tuntutan_years']:.4f})")
    print(f"  Quadratic survives charge type control: "
          f"{'YES' if m_full.pvalues['tuntutan_sq'] < 0.05 else 'NO'}")


if __name__ == "__main__":
    main()
