"""Script 12: Robustness tests for Paper 2 Pasal 2 finding.

Tests:
  1. Cook's distance — no single case drives the finding
  2. DFFITS — same, alternative measure
  3. Leave-one-out coefficient stability
  4. Placebo test — random binary variable doesn't produce same effect
  5. HC3 robust standard errors (already in paper, re-confirmed here)
  6. Alternative specifications: quantile regression, WLS

Usage: python -m scripts.12_robustness_tests
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

    corpus = load_corpus(require_text=True).copy()
    texts = text_lower(corpus)
    corpus["has_p2"] = texts.str.contains(r"pasal\s+2\b", regex=True).astype(int)
    corpus["has_p3"] = texts.str.contains(r"pasal\s+3\b", regex=True).astype(int)

    y = corpus["vonis_years"].values
    X = sm.add_constant(corpus[["tuntutan_years", "has_p2", "has_p3"]])
    model = sm.OLS(y, X).fit()
    n = len(corpus)

    print("=" * 70)
    print("  ROBUSTNESS TESTS — Pasal 2 Finding")
    print(f"  Model 3: vonis ~ tuntutan + has_p2 + has_p3, n={n}")
    print(f"  Pasal 2 coef: b={model.params['has_p2']:.3f}, p={model.pvalues['has_p2']:.6f}")
    print("=" * 70)

    # ==================================================================
    #  TEST 1: Cook's Distance
    # ==================================================================
    print_section("TEST 1: Cook's Distance")

    influence = model.get_influence()
    cooks_d = influence.cooks_distance[0]
    threshold = 4 / n

    n_influential = np.sum(cooks_d > threshold)
    max_cook = np.max(cooks_d)
    max_idx = np.argmax(cooks_d)

    print(f"  Threshold (4/n): {threshold:.4f}")
    print(f"  Max Cook's d: {max_cook:.4f} (case index {max_idx})")
    print(f"  Cases > threshold: {n_influential} / {n} ({100*n_influential/n:.1f}%)")

    # Typical concern: Cook's d > 0.5 or > 1.0
    print(f"  Cases > 0.5: {np.sum(cooks_d > 0.5)}")
    print(f"  Cases > 1.0: {np.sum(cooks_d > 1.0)}")

    # Top 5 most influential
    top5 = np.argsort(cooks_d)[-5:][::-1]
    print(f"\n  Top 5 most influential cases:")
    print(f"  {'Rank':<5} {'Cook_d':<10} {'vonis':<8} {'tuntutan':<10} {'P2':<4} {'P3':<4} {'residual':<10}")
    for rank, idx in enumerate(top5, 1):
        row = corpus.iloc[idx]
        resid = model.resid[idx]
        print(f"  {rank:<5} {cooks_d[idx]:<10.4f} {row['vonis_years']:<8.1f} "
              f"{row['tuntutan_years']:<10.1f} {int(row['has_p2']):<4} {int(row['has_p3']):<4} "
              f"{resid:<+10.2f}")

    # Remove all influential cases and re-estimate
    mask_clean = cooks_d <= threshold
    X_clean = X[mask_clean]
    y_clean = y[mask_clean]
    model_clean = sm.OLS(y_clean, X_clean).fit()

    print(f"\n  After removing {n_influential} influential cases (n={mask_clean.sum()}):")
    print(f"    Pasal 2 coef: b={model_clean.params['has_p2']:.3f}, "
          f"p={model_clean.pvalues['has_p2']:.6f}")
    print(f"    Change: {model_clean.params['has_p2'] - model.params['has_p2']:+.3f}")
    print(f"    SURVIVES: {'YES' if model_clean.pvalues['has_p2'] < 0.05 else 'NO'}")

    # ==================================================================
    #  TEST 2: DFFITS
    # ==================================================================
    print_section("TEST 2: DFFITS")

    dffits_vals = influence.dffits[0]
    p = X.shape[1]  # number of parameters
    dffits_threshold = 2 * np.sqrt(p / n)

    n_dffits = np.sum(np.abs(dffits_vals) > dffits_threshold)
    print(f"  Threshold (2*sqrt(p/n)): {dffits_threshold:.4f}")
    print(f"  Cases exceeding threshold: {n_dffits} / {n} ({100*n_dffits/n:.1f}%)")
    print(f"  Max |DFFITS|: {np.max(np.abs(dffits_vals)):.4f}")

    # ==================================================================
    #  TEST 3: Leave-One-Out Coefficient Stability
    # ==================================================================
    print_section("TEST 3: Leave-One-Out Pasal 2 Coefficient")

    loo_coefs = []
    for i in range(n):
        mask = np.ones(n, dtype=bool)
        mask[i] = False
        m_loo = sm.OLS(y[mask], X.values[mask]).fit()
        loo_coefs.append(m_loo.params[2])  # has_p2 is index 2

    loo_coefs = np.array(loo_coefs)
    print(f"  Full model coef: {model.params['has_p2']:.4f}")
    print(f"  LOO mean: {loo_coefs.mean():.4f}")
    print(f"  LOO min: {loo_coefs.min():.4f}")
    print(f"  LOO max: {loo_coefs.max():.4f}")
    print(f"  LOO range: {loo_coefs.max() - loo_coefs.min():.4f}")
    print(f"  LOO std: {loo_coefs.std():.4f}")
    print(f"  Max deviation from full: {np.max(np.abs(loo_coefs - model.params['has_p2'])):.4f}")

    # What fraction of LOO estimates are still positive?
    pct_positive = 100 * np.mean(loo_coefs > 0)
    print(f"  LOO coefs > 0: {pct_positive:.1f}%")

    # ==================================================================
    #  TEST 4: Placebo Test (Permutation)
    # ==================================================================
    print_section("TEST 4: Placebo Test (1000 Random Binary Variables)")

    np.random.seed(SEED)
    n_perms = 1000
    placebo_coefs = []
    placebo_pvals = []

    for _ in range(n_perms):
        fake_p2 = np.random.binomial(1, corpus["has_p2"].mean(), size=n)
        fake_p3 = np.random.binomial(1, corpus["has_p3"].mean(), size=n)
        X_fake = sm.add_constant(np.column_stack([
            corpus["tuntutan_years"].values, fake_p2, fake_p3
        ]))
        m_fake = sm.OLS(y, X_fake).fit()
        placebo_coefs.append(m_fake.params[2])
        placebo_pvals.append(m_fake.pvalues[2])

    placebo_coefs = np.array(placebo_coefs)
    placebo_pvals = np.array(placebo_pvals)

    real_coef = model.params["has_p2"]
    pct_exceed = 100 * np.mean(np.abs(placebo_coefs) >= np.abs(real_coef))

    print(f"  Real Pasal 2 coef: {real_coef:.3f}")
    print(f"  Placebo mean coef: {placebo_coefs.mean():.3f} (should be ~0)")
    print(f"  Placebo std: {placebo_coefs.std():.3f}")
    print(f"  Placebo |coef| >= real |coef|: {pct_exceed:.1f}% (permutation p-value)")
    print(f"  Placebo p < 0.05: {100*np.mean(placebo_pvals < 0.05):.1f}% (expected ~5%)")
    print(f"  Placebo p < 0.002: {100*np.mean(placebo_pvals < 0.002):.1f}% (our threshold)")

    # ==================================================================
    #  TEST 5: HC3 Robust Standard Errors
    # ==================================================================
    print_section("TEST 5: HC3 Robust Standard Errors")

    model_hc3 = model.get_robustcov_results(cov_type="HC3")
    # HC3 result uses integer indexing (has_p2 is column index 2)
    hc3_b = model_hc3.params[2]
    hc3_se = model_hc3.bse[2]
    hc3_p = model_hc3.pvalues[2]
    print(f"  OLS:  b={model.params['has_p2']:.3f}, SE={model.bse['has_p2']:.3f}, "
          f"p={model.pvalues['has_p2']:.6f}")
    print(f"  HC3:  b={hc3_b:.3f}, SE={hc3_se:.3f}, p={hc3_p:.6f}")
    print(f"  HC3 strengthens result: {'YES' if hc3_p < model.pvalues['has_p2'] else 'NO'}")

    # ==================================================================
    #  TEST 6: Alternative Specifications
    # ==================================================================
    print_section("TEST 6: Alternative Specifications")

    # 6a: Quantile regression (median)
    try:
        qr = sm.QuantReg(y, X).fit(q=0.5)
        print(f"  Quantile regression (median):")
        print(f"    Pasal 2 coef: b={qr.params['has_p2']:.3f}, p={qr.pvalues['has_p2']:.6f}")
    except Exception as e:
        print(f"  Quantile regression failed: {e}")

    # 6b: WLS (inverse variance weights based on tuntutan)
    weights = 1 / (1 + corpus["tuntutan_years"].values)
    model_wls = sm.WLS(y, X, weights=weights).fit()
    print(f"\n  WLS (weight = 1/(1+tuntutan)):")
    print(f"    Pasal 2 coef: b={model_wls.params['has_p2']:.3f}, p={model_wls.pvalues['has_p2']:.6f}")

    # 6c: Log-transformed outcome
    y_log = np.log1p(y)
    model_log = sm.OLS(y_log, X).fit()
    print(f"\n  Log(1+vonis) specification:")
    print(f"    Pasal 2 coef: b={model_log.params['has_p2']:.3f}, p={model_log.pvalues['has_p2']:.6f}")

    # ==================================================================
    #  SUMMARY
    # ==================================================================
    print_section("ROBUSTNESS SUMMARY")

    results = [
        ("Cook's distance", f"Max={max_cook:.4f}, >{threshold:.4f}: {n_influential}",
         "YES" if model_clean.pvalues["has_p2"] < 0.05 else "NO"),
        ("DFFITS", f"Exceeding: {n_dffits}/{n}", "INFO"),
        ("Leave-one-out", f"Range [{loo_coefs.min():.3f}, {loo_coefs.max():.3f}], "
         f"{pct_positive:.0f}% positive", "YES" if pct_positive == 100 else "PARTIAL"),
        ("Placebo test", f"Permutation p={pct_exceed:.1f}%",
         "YES" if pct_exceed < 5 else "NO"),
        ("HC3 robust SE", f"p={hc3_p:.6f}",
         "YES" if hc3_p < 0.05 else "NO"),
        ("Quantile (median)", f"b={qr.params['has_p2']:.3f}, p={qr.pvalues['has_p2']:.6f}",
         "YES" if qr.pvalues["has_p2"] < 0.05 else "NO"),
        ("WLS", f"b={model_wls.params['has_p2']:.3f}, p={model_wls.pvalues['has_p2']:.6f}",
         "YES" if model_wls.pvalues["has_p2"] < 0.05 else "NO"),
        ("Log specification", f"b={model_log.params['has_p2']:.3f}, p={model_log.pvalues['has_p2']:.6f}",
         "YES" if model_log.pvalues["has_p2"] < 0.05 else "NO"),
    ]

    print(f"\n  {'Test':<25} {'Detail':<45} {'Survives?'}")
    print(f"  {'-'*80}")
    for name, detail, survives in results:
        print(f"  {name:<25} {detail:<45} {survives}")

    all_survive = all(s == "YES" for _, _, s in results if s != "INFO")
    print(f"\n  OVERALL: {'ALL TESTS PASS — finding is robust' if all_survive else 'SOME TESTS FAIL — investigate'}")


if __name__ == "__main__":
    main()
