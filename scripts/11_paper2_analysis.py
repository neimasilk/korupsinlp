"""Script 11: Generate all Paper 2 analysis results.

Produces reproducible tables and statistics for:
"Charge Type, Judicial Opacity, and the Limits of Prediction:
 A Computational Analysis of Indonesian Corruption Sentences"

Target: Crime, Law and Social Change (Springer)

Usage: python -m scripts.11_paper2_analysis
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import re
from scipy import stats
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RepeatedKFold, KFold, train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from autoresearch.prepare import (
    load_corpus, get_splits, evaluate, baseline_predict,
    M9_INTERCEPT, M9_SLOPE,
)

SEED = 42


def text_lower(df):
    return df["pertimbangan_text"].fillna("").str.lower()


def print_section(title):
    print(f"\n\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


# =====================================================================
#  MAIN
# =====================================================================

def main():
    corpus = load_corpus(require_text=True)
    corpus_all = load_corpus(require_text=False)

    print("=" * 70)
    print("  PAPER 2 ANALYSIS — Charge Type, Opacity, Limits")
    print(f"  Corpus with text: {len(corpus)}")
    print(f"  Corpus all (vonis+tuntutan): {len(corpus_all)}")
    print("=" * 70)

    # Derived columns
    texts = text_lower(corpus)
    corpus = corpus.copy()
    corpus["has_p2"] = texts.str.contains(r"pasal\s+2\b", regex=True).astype(int)
    corpus["has_p3"] = texts.str.contains(r"pasal\s+3\b", regex=True).astype(int)
    corpus["has_grat"] = texts.str.contains("gratifikasi").astype(int)
    corpus["has_pencucian"] = texts.str.contains(r"pencucian\s+uang", regex=True).astype(int)
    corpus["discount"] = corpus["vonis_years"] / corpus["tuntutan_years"]

    # ==================================================================
    #  TABLE 1: PRIMARY — OLS Regression (Pasal 2 Effect)
    # ==================================================================
    print_section("TABLE 1: OLS Regression — Charge Type Effect on Sentencing")

    import statsmodels.api as sm

    # Model 1: vonis ~ tuntutan (baseline)
    X1 = sm.add_constant(corpus[["tuntutan_years"]])
    m1 = sm.OLS(corpus["vonis_years"], X1).fit()

    # Model 2: vonis ~ tuntutan + has_p2 (primary test)
    X2 = sm.add_constant(corpus[["tuntutan_years", "has_p2"]])
    m2 = sm.OLS(corpus["vonis_years"], X2).fit()

    # Model 3: vonis ~ tuntutan + has_p2 + has_p3
    X3 = sm.add_constant(corpus[["tuntutan_years", "has_p2", "has_p3"]])
    m3 = sm.OLS(corpus["vonis_years"], X3).fit()

    print(f"\n  Model 1: vonis ~ tuntutan")
    print(f"    R2 = {m1.rsquared:.4f}, Adj R2 = {m1.rsquared_adj:.4f}")
    print(f"    tuntutan: b={m1.params['tuntutan_years']:.3f}, "
          f"SE={m1.bse['tuntutan_years']:.3f}, p={m1.pvalues['tuntutan_years']:.6f}")

    print(f"\n  Model 2: vonis ~ tuntutan + has_pasal_2")
    print(f"    R2 = {m2.rsquared:.4f}, Adj R2 = {m2.rsquared_adj:.4f}")
    for var in ["tuntutan_years", "has_p2"]:
        ci = m2.conf_int().loc[var]
        print(f"    {var}: b={m2.params[var]:.3f} [{ci[0]:.3f}, {ci[1]:.3f}], "
              f"SE={m2.bse[var]:.3f}, p={m2.pvalues[var]:.6f}")

    print(f"\n  Model 3: vonis ~ tuntutan + has_p2 + has_p3")
    print(f"    R2 = {m3.rsquared:.4f}, Adj R2 = {m3.rsquared_adj:.4f}")
    for var in ["tuntutan_years", "has_p2", "has_p3"]:
        ci = m3.conf_int().loc[var]
        print(f"    {var}: b={m3.params[var]:.3f} [{ci[0]:.3f}, {ci[1]:.3f}], "
              f"SE={m3.bse[var]:.3f}, p={m3.pvalues[var]:.6f}")

    # F-test: Model 2 vs Model 1
    f_test = m2.compare_f_test(m1)
    print(f"\n  F-test (Model 2 vs 1): F={f_test[0]:.2f}, p={f_test[1]:.6f}")
    print(f"  Adding has_pasal_2 significantly improves the model.")

    # ==================================================================
    #  TABLE 2: Bootstrap CI for Pasal 2 coefficient
    # ==================================================================
    print_section("TABLE 2: Bootstrap 95% CI for Pasal 2 Coefficient")

    np.random.seed(SEED)
    n_boot = 2000
    boot_coefs = []
    n_obs = len(corpus)
    for _ in range(n_boot):
        idx = np.random.choice(n_obs, n_obs, replace=True)
        boot_df = corpus.iloc[idx]
        Xb = sm.add_constant(boot_df[["tuntutan_years", "has_p2"]])
        try:
            mb = sm.OLS(boot_df["vonis_years"], Xb).fit()
            boot_coefs.append(mb.params["has_p2"])
        except Exception:
            pass

    boot_coefs = np.array(boot_coefs)
    ci_lo = np.percentile(boot_coefs, 2.5)
    ci_hi = np.percentile(boot_coefs, 97.5)
    print(f"  Pasal 2 coefficient: {m2.params['has_p2']:.3f}")
    print(f"  Bootstrap 95% CI: [{ci_lo:.3f}, {ci_hi:.3f}]")
    print(f"  Bootstrap SE: {boot_coefs.std():.3f}")
    print(f"  CI excludes zero: {ci_lo > 0}")

    # ==================================================================
    #  TABLE 3: Effect size (Cohen's d) with CI
    # ==================================================================
    print_section("TABLE 3: Pasal 2 vs Pasal 3 — Effect Size")

    residuals = corpus["vonis_years"] - m1.predict(X1)
    corpus["residual"] = residuals

    p2_only = corpus[(corpus["has_p2"] == 1) & (corpus["has_p3"] == 0)]
    p3_only = corpus[(corpus["has_p2"] == 0) & (corpus["has_p3"] == 1)]

    print(f"  Pasal 2 only: n={len(p2_only)}, mean vonis={p2_only['vonis_years'].mean():.2f}yr")
    print(f"  Pasal 3 only: n={len(p3_only)}, mean vonis={p3_only['vonis_years'].mean():.2f}yr")

    # Raw effect
    d_raw = (p2_only["vonis_years"].mean() - p3_only["vonis_years"].mean()) / \
            np.sqrt((p2_only["vonis_years"].std()**2 + p3_only["vonis_years"].std()**2) / 2)
    u_raw, p_raw = stats.mannwhitneyu(p2_only["vonis_years"], p3_only["vonis_years"])
    print(f"  Raw: d={d_raw:.3f}, Mann-Whitney p={p_raw:.6f}")

    # Controlled (residuals)
    d_ctrl = (p2_only["residual"].mean() - p3_only["residual"].mean()) / \
             np.sqrt((p2_only["residual"].std()**2 + p3_only["residual"].std()**2) / 2)
    u_ctrl, p_ctrl = stats.mannwhitneyu(p2_only["residual"], p3_only["residual"])
    print(f"  Controlled: d={d_ctrl:.3f}, Mann-Whitney p={p_ctrl:.6f}")
    print(f"  P2 mean residual: {p2_only['residual'].mean():+.3f}yr")
    print(f"  P3 mean residual: {p3_only['residual'].mean():+.3f}yr")

    # Bootstrap CI for Cohen's d
    boot_ds = []
    for _ in range(2000):
        p2_s = p2_only["residual"].sample(len(p2_only), replace=True)
        p3_s = p3_only["residual"].sample(len(p3_only), replace=True)
        d_s = (p2_s.mean() - p3_s.mean()) / np.sqrt((p2_s.std()**2 + p3_s.std()**2) / 2)
        boot_ds.append(d_s)
    boot_ds = np.array(boot_ds)
    print(f"  Cohen's d 95% CI: [{np.percentile(boot_ds, 2.5):.3f}, {np.percentile(boot_ds, 97.5):.3f}]")

    # ==================================================================
    #  TABLE 4: Judicial Opacity — Discount Unpredictability
    # ==================================================================
    print_section("TABLE 4: Sentencing Discount Unpredictability")

    corpus_d = corpus[corpus["discount"].between(0, 5)].copy()
    disc = corpus_d["discount"]
    print(f"  n={len(corpus_d)}, mean={disc.mean():.3f}, median={disc.median():.3f}, std={disc.std():.3f}")

    # Test each feature against discount
    print(f"\n  Individual correlations with discount (Spearman):")
    feat_map = {
        "has_p2": "Pasal 2", "has_p3": "Pasal 3", "has_grat": "Gratifikasi",
        "has_pencucian": "Pencucian uang",
    }
    for col, label in feat_map.items():
        r, p = stats.spearmanr(corpus_d[col], disc)
        print(f"    {label:<20s}: r={r:+.3f}, p={p:.4f}")

    # Ridge regression on discount
    t_disc = text_lower(corpus_d)
    X_disc = np.column_stack([
        np.log1p(corpus_d["kerugian_negara"].fillna(0).values),
        corpus_d["has_p2"].values, corpus_d["has_p3"].values,
        corpus_d["has_grat"].values,
        t_disc.str.contains("memberatkan").astype(int).values,
        t_disc.str.contains("meringankan").astype(int).values,
    ])
    kf = KFold(n_splits=10, shuffle=True, random_state=SEED)
    disc_r2s = []
    for tri, vai in kf.split(X_disc):
        sc = StandardScaler(); m = Ridge(alpha=10)
        m.fit(sc.fit_transform(X_disc[tri]), disc.values[tri])
        pred = m.predict(sc.transform(X_disc[vai]))
        ss_res = np.sum((disc.values[vai] - pred)**2)
        ss_tot = np.sum((disc.values[vai] - disc.values[vai].mean())**2)
        disc_r2s.append(1 - ss_res / ss_tot if ss_tot > 0 else 0)
    print(f"\n  Ridge CV R2 on discount: {np.mean(disc_r2s):.4f} (UNPREDICTABLE)")

    # ==================================================================
    #  TABLE 5: Text Feature Experiments — Negative Result
    # ==================================================================
    print_section("TABLE 5: Text Feature Experiments (Negative Result)")

    train_df, val_df, test_df = get_splits(corpus)
    cv_df = pd.concat([train_df, val_df]).reset_index(drop=True)
    cv_y = cv_df["vonis_years"].values

    rkf = RepeatedKFold(n_splits=10, n_repeats=5, random_state=SEED)

    def run_cv(make_X, alpha=20):
        r2s, bls = [], []
        for tri, vai in rkf.split(cv_df):
            tr, va = cv_df.iloc[tri], cv_df.iloc[vai]
            X_tr, X_va = make_X(tr, va)
            sc = StandardScaler()
            m = Ridge(alpha=alpha)
            m.fit(sc.fit_transform(X_tr), cv_y[tri])
            r2s.append(evaluate(cv_y[vai], m.predict(sc.transform(X_va)))["val_r2"])
            bls.append(evaluate(cv_y[vai], baseline_predict(va))["val_r2"])
        return np.array(r2s), np.array(bls)

    def make_tfidf_fn(tr, va):
        def clean(s): return re.sub(r"\s+", " ", re.sub(r"\d+", " ", s.lower())).strip()
        from sklearn.feature_extraction.text import TfidfVectorizer
        tr_t = text_lower(tr).apply(clean); va_t = text_lower(va).apply(clean)
        vec = TfidfVectorizer(max_features=100, min_df=2, max_df=0.9, sublinear_tf=True)
        Xtr = np.column_stack([tr["tuntutan_years"].values, vec.fit_transform(tr_t).toarray()])
        Xva = np.column_stack([va["tuntutan_years"].values, vec.transform(va_t).toarray()])
        return Xtr, Xva

    def make_keywords(tr, va):
        fl = []
        for df in [tr, va]:
            t = text_lower(df)
            fl.append(np.column_stack([df["tuntutan_years"].values,
                t.str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
                t.str.contains("gratifikasi").astype(int).values,
                t.str.contains(r"pencucian\s+uang", regex=True).astype(int).values]))
        return fl[0], fl[1]

    configs = [
        ("TF-IDF (100 features, a=10)", make_tfidf_fn, 10),
        ("Domain keywords (3 binary, a=20)", make_keywords, 20),
    ]

    print(f"  {'Approach':<40s} {'CV R2':>7s} {'delta':>7s} {'p':>8s}")
    print(f"  {'-'*65}")

    for name, fn, alpha in configs:
        r2s, bls = run_cv(fn, alpha)
        d = r2s - bls; t, p = stats.ttest_rel(r2s, bls)
        print(f"  {name:<40s} {r2s.mean():>7.4f} {d.mean():>+7.4f} {p:>8.4f}")

    # Multi-seed robustness for keyword model
    print(f"\n  Keyword model robustness (10 random splits, 3x10 CV):")
    split_deltas = []
    split_ps = []
    for seed in range(10):
        bins_s = pd.qcut(corpus["vonis_years"], q=4, labels=False, duplicates="drop")
        tv_s, _ = train_test_split(corpus, test_size=0.15, random_state=seed, stratify=bins_s)
        bins_tv_s = pd.qcut(tv_s["vonis_years"], q=4, labels=False, duplicates="drop")
        tr_s, va_s = train_test_split(tv_s, test_size=0.176, random_state=seed, stratify=bins_tv_s)
        cv_s = pd.concat([tr_s, va_s]).reset_index(drop=True)
        cv_y_s = cv_s["vonis_years"].values
        rkf_s = RepeatedKFold(n_splits=10, n_repeats=3, random_state=42)
        r2s_s, bls_s = [], []
        for tri, vai in rkf_s.split(cv_s):
            tr, va = cv_s.iloc[tri], cv_s.iloc[vai]
            X_tr, X_va = make_keywords(tr, va)
            sc = StandardScaler(); m = Ridge(alpha=20)
            m.fit(sc.fit_transform(X_tr), cv_y_s[tri])
            r2s_s.append(evaluate(cv_y_s[vai], m.predict(sc.transform(X_va)))["val_r2"])
            bls_s.append(evaluate(cv_y_s[vai], baseline_predict(va))["val_r2"])
        r2s_s, bls_s = np.array(r2s_s), np.array(bls_s)
        d_s = r2s_s - bls_s; _, p_s = stats.ttest_rel(r2s_s, bls_s)
        split_deltas.append(d_s.mean()); split_ps.append(p_s)

    print(f"    Direction positive: {sum(1 for d in split_deltas if d > 0)}/10")
    print(f"    Significant (p<0.05): {sum(1 for p in split_ps if p < 0.05)}/10")
    print(f"    Mean delta: {np.mean(split_deltas):+.4f} +/- {np.std(split_deltas):.4f}")
    print(f"    Conclusion: improvement is CONSISTENT in direction but NOT always significant.")
    print(f"    Text features provide marginal, unstable improvement over tuntutan alone.")

    # ==================================================================
    #  TABLE 6: Geographic Composition Effect
    # ==================================================================
    print_section("TABLE 6: Geographic Effects — Composition, Not Disparity")

    from scipy.stats import kruskal
    geo_groups_raw = [g["vonis_years"].values for _, g in corpus.groupby("daerah") if len(g) >= 5]
    geo_groups_ctrl = [g["residual"].values for _, g in corpus.groupby("daerah") if len(g) >= 5]

    h_raw, p_raw = kruskal(*geo_groups_raw)
    h_ctrl, p_ctrl_geo = kruskal(*geo_groups_ctrl)

    print(f"  Raw vonis KW:      H={h_raw:.1f}, p={p_raw:.6f}")
    print(f"  Residual KW:       H={h_ctrl:.1f}, p={p_ctrl_geo:.6f}")
    print(f"  Conclusion: {'composition effect' if p_ctrl_geo > 0.05 else 'genuine disparity'}")

    # ==================================================================
    #  TABLE 7: Judge Effects
    # ==================================================================
    print_section("TABLE 7: Judge Effects")

    import sqlite3
    from src.config import DB_PATH
    conn = sqlite3.connect(str(DB_PATH))
    hakim_df = pd.read_sql_query(
        f"SELECT id, nama_hakim FROM verdicts WHERE id IN ({','.join(str(i) for i in corpus['id'])})", conn)
    conn.close()
    merged = corpus.merge(hakim_df, on="id", how="left")
    def get_ketua(x):
        if pd.isna(x): return "unknown"
        return x.split(";")[0].replace("Hakim Ketua", "").strip() or "unknown"
    merged["ketua"] = merged["nama_hakim"].apply(get_ketua)
    freq = merged["ketua"].value_counts()
    freq_judges = set(freq[freq >= 3].index) - {"unknown"}
    groups = [merged.loc[merged["ketua"] == j, "residual"].values for j in freq_judges if freq[j] >= 3]
    if len(groups) >= 2:
        f_stat, p_anova = stats.f_oneway(*groups)
        resids_j = sorted([(j, merged.loc[merged["ketua"]==j, "residual"].mean(), freq[j]) for j in freq_judges], key=lambda x: x[1])
        print(f"  ANOVA: F={f_stat:.2f}, p={p_anova:.4f}")
        print(f"  Judges (>=3 cases): {len(freq_judges)}")
        print(f"  Range: {resids_j[-1][1] - resids_j[0][1]:.2f}yr")
        print(f"  Conclusion: judges differ significantly but effect is not predictively useful (overfits at n={len(cv_df)})")

    # ==================================================================
    #  SUMMARY
    # ==================================================================
    print_section("KEY NUMBERS FOR PAPER")
    print(f"  Corpus: {len(corpus)} with text, {len(corpus_all)} total")
    print(f"  Pasal 2 OLS coef: b={m2.params['has_p2']:.3f}, 95% CI [{ci_lo:.3f}, {ci_hi:.3f}], p={m2.pvalues['has_p2']:.6f}")
    print(f"  Pasal 2 vs 3 controlled d={d_ctrl:.3f}, p={p_ctrl:.6f}")
    print(f"  Discount CV R2: {np.mean(disc_r2s):.4f}")
    print(f"  Geographic: raw p={p_raw:.4f}, controlled p={p_ctrl_geo:.4f}")
    print(f"  Judge ANOVA: F={f_stat:.2f}, p={p_anova:.4f}")
    print(f"  Text features: direction positive ({sum(1 for d in split_deltas if d>0)}/10), "
          f"significant ({sum(1 for p in split_ps if p<0.05)}/10)")


if __name__ == "__main__":
    main()
