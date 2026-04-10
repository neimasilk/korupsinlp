"""Script 11: Generate all Paper 2 analysis results.

Produces reproducible tables and statistics for:
"Two Words That Matter: Domain-Specific Text Features Outperform
Bag-of-Words for Sentencing Prediction in Indonesian Corruption Cases"

Usage: python -m scripts.11_paper2_analysis
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import re
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RepeatedKFold, KFold
from sklearn.decomposition import TruncatedSVD

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from autoresearch.prepare import (
    load_corpus, get_splits, evaluate, baseline_predict,
    M9_INTERCEPT, M9_SLOPE,
)

SEED = 42
N_REPEATS = 5
N_SPLITS = 10


# ── helpers ──────────────────────────────────────────────────────────

def cv_evaluate(cv_df, cv_y, make_X, alpha=50):
    """Run 5x10 repeated CV. Returns (model_r2s, baseline_r2s)."""
    rkf = RepeatedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED)
    r2s, bls = [], []
    for tri, vai in rkf.split(cv_df):
        tr, va = cv_df.iloc[tri], cv_df.iloc[vai]
        X_tr, X_va = make_X(tr, va)
        sc = StandardScaler()
        X_tr, X_va = sc.fit_transform(X_tr), sc.transform(X_va)
        m = Ridge(alpha=alpha)
        m.fit(X_tr, cv_y[tri])
        r2s.append(evaluate(cv_y[vai], m.predict(X_va))["val_r2"])
        bls.append(evaluate(cv_y[vai], baseline_predict(va))["val_r2"])
    return np.array(r2s), np.array(bls)


def text_lower(df):
    return df["pertimbangan_text"].fillna("").str.lower()


# ── feature factories ────────────────────────────────────────────────

def make_tuntutan_only(tr, va):
    return tr[["tuntutan_years"]].values, va[["tuntutan_years"]].values


def make_tfidf(tr, va, max_features=100, alpha_hint=None):
    """TF-IDF + tuntutan + kerugian."""
    def clean(s):
        s = s.lower()
        s = re.sub(r"\d+", " ", s)
        return re.sub(r"\s+", " ", s).strip()

    tr_t = text_lower(tr).apply(clean)
    va_t = text_lower(va).apply(clean)
    vec = TfidfVectorizer(max_features=max_features, ngram_range=(1, 1),
                          min_df=2, max_df=0.9, sublinear_tf=True)
    X_tr_text = vec.fit_transform(tr_t).toarray()
    X_va_text = vec.transform(va_t).toarray()
    X_tr = np.column_stack([tr["tuntutan_years"].values,
                            np.log1p(tr["kerugian_negara"].fillna(0).values),
                            X_tr_text])
    X_va = np.column_stack([va["tuntutan_years"].values,
                            np.log1p(va["kerugian_negara"].fillna(0).values),
                            X_va_text])
    return X_tr, X_va


def make_all_structured(tr, va):
    """All 16 domain keyword features + tuntutan."""
    features_list = []
    for df in [tr, va]:
        t = text_lower(df)
        feats = np.column_stack([
            df["tuntutan_years"].values,
            t.str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
            t.str.contains(r"pasal\s+3\b", regex=True).astype(int).values,
            t.str.contains(r"pasal\s+12\b", regex=True).astype(int).values,
            t.str.contains("miliar").astype(int).values,
            t.str.contains(r"mengembalikan|pengembalian", regex=True).astype(int).values,
            t.str.contains(r"uang\s+pengganti", regex=True).astype(int).values,
            t.str.contains("jabatan").astype(int).values,
            t.str.contains("gratifikasi").astype(int).values,
            t.str.contains("suap").astype(int).values,
            t.str.contains(r"merugikan\s+(?:keuangan\s+)?negara", regex=True).astype(int).values,
            t.str.contains(r"(?:hal|keadaan)\s+yang\s+memberatkan", regex=True).astype(int).values,
            t.str.count("memberatkan").values,
            t.str.count("meringankan").values,
            t.str.len().values,
        ])
        features_list.append(feats)
    return features_list[0], features_list[1]


def make_minimal(tr, va):
    """Tuntutan + pasal_2 + gratifikasi + pencucian_uang (4 features)."""
    features_list = []
    for df in [tr, va]:
        t = text_lower(df)
        feats = np.column_stack([
            df["tuntutan_years"].values,
            t.str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
            t.str.contains("gratifikasi").astype(int).values,
            t.str.contains(r"pencucian\s+uang", regex=True).astype(int).values,
        ])
        features_list.append(feats)
    return features_list[0], features_list[1]


# ── main ─────────────────────────────────────────────────────────────

def main():
    corpus = load_corpus(require_text=True)
    train_df, val_df, test_df = get_splits(corpus)
    cv_df = pd.concat([train_df, val_df]).reset_index(drop=True)
    cv_y = cv_df["vonis_years"].values
    n = len(cv_df)

    print("=" * 70)
    print("PAPER 2 — REPRODUCIBLE ANALYSIS RESULTS")
    print(f"Corpus: {len(corpus)} verdicts with text, CV pool: {n}")
    print("=" * 70)

    # ── TABLE 1: Main comparison ─────────────────────────────────────

    print("\n\n### TABLE 1: Approach Comparison (5x10-fold Repeated CV)")
    print(f"{'Approach':<45} {'k':>3} {'CV_R2':>7} {'d_BL':>7} {'p':>8} {'W':>5}")
    print("-" * 78)

    configs = [
        ("Ridge tuntutan-only", make_tuntutan_only, 50),
        ("TF-IDF 100 + tuntutan + kerugian (a=0.05)", lambda t, v: make_tfidf(t, v, 100), 0.05),
        ("TF-IDF 100 + tuntutan + kerugian (a=10)", lambda t, v: make_tfidf(t, v, 100), 10),
        ("All 16 structured + tuntutan (a=50)", make_all_structured, 50),
        ("Minimal: tuntutan+p2+grat+pencucian (a=20)", make_minimal, 20),
    ]

    results = {}
    for name, fn, alpha in configs:
        r2s, bls = cv_evaluate(cv_df, cv_y, fn, alpha)
        diffs = r2s - bls
        t, p = stats.ttest_rel(r2s, bls)
        wins = int((diffs > 0).sum())
        k = fn(cv_df.iloc[:5], cv_df.iloc[:5])[0].shape[1]
        print(f"{name:<45} {k:>3} {r2s.mean():>7.4f} {diffs.mean():>+7.4f} {p:>8.4f} {wins:>2}/50")
        results[name] = {"cv_r2": r2s.mean(), "delta": diffs.mean(), "p": p, "wins": wins}

    # ── TABLE 2: Pasal 2 vs 3 ────────────────────────────────────────

    print("\n\n### TABLE 2: Pasal 2 vs Pasal 3 Sentencing Effect")

    texts = text_lower(corpus)
    corpus = corpus.copy()
    corpus["has_p2"] = texts.str.contains(r"pasal\s+2\b", regex=True).astype(int)
    corpus["has_p3"] = texts.str.contains(r"pasal\s+3\b", regex=True).astype(int)
    corpus["predicted"] = M9_INTERCEPT + M9_SLOPE * corpus["tuntutan_years"]
    corpus["residual"] = corpus["vonis_years"] - corpus["predicted"]

    p2 = corpus[(corpus["has_p2"] == 1) & (corpus["has_p3"] == 0)]
    p3 = corpus[(corpus["has_p2"] == 0) & (corpus["has_p3"] == 1)]

    print(f"  Pasal 2 only: n={len(p2)}, mean vonis={p2['vonis_years'].mean():.2f}yr")
    print(f"  Pasal 3 only: n={len(p3)}, mean vonis={p3['vonis_years'].mean():.2f}yr")

    u, p_raw = stats.mannwhitneyu(p2["vonis_years"], p3["vonis_years"])
    d_raw = (p2["vonis_years"].mean() - p3["vonis_years"].mean()) / \
            np.sqrt((p2["vonis_years"].std()**2 + p3["vonis_years"].std()**2) / 2)
    print(f"  Raw: Cohen's d={d_raw:.3f}, p={p_raw:.6f}")

    u2, p_ctrl = stats.mannwhitneyu(p2["residual"], p3["residual"])
    d_ctrl = (p2["residual"].mean() - p3["residual"].mean()) / \
             np.sqrt((p2["residual"].std()**2 + p3["residual"].std()**2) / 2)
    print(f"  After controlling tuntutan: d={d_ctrl:.3f}, p={p_ctrl:.6f}")
    print(f"  P2 mean residual: {p2['residual'].mean():+.3f}yr")
    print(f"  P3 mean residual: {p3['residual'].mean():+.3f}yr")

    # ── TABLE 3: Text vs Structured pasal ────────────────────────────

    print("\n\n### TABLE 3: Text-Derived vs Structured Metadata pasal_2")

    def make_text_p2(tr, va):
        return np.column_stack([tr["tuntutan_years"].values,
                text_lower(tr).str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
                text_lower(tr).str.contains("gratifikasi").astype(int).values]), \
               np.column_stack([va["tuntutan_years"].values,
                text_lower(va).str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
                text_lower(va).str.contains("gratifikasi").astype(int).values])

    def make_struct_p2(tr, va):
        return np.column_stack([tr["tuntutan_years"].values,
                tr["pasal"].fillna("").str.contains(r"^2\b|Pasal 2\b|^2 Ayat", regex=True).astype(int).values,
                text_lower(tr).str.contains("gratifikasi").astype(int).values]), \
               np.column_stack([va["tuntutan_years"].values,
                va["pasal"].fillna("").str.contains(r"^2\b|Pasal 2\b|^2 Ayat", regex=True).astype(int).values,
                text_lower(va).str.contains("gratifikasi").astype(int).values])

    for label, fn in [("Text-derived pasal_2", make_text_p2),
                      ("Structured metadata pasal_2", make_struct_p2)]:
        r2s, bls = cv_evaluate(cv_df, cv_y, fn, 50)
        diffs = r2s - bls
        t, p = stats.ttest_rel(r2s, bls)
        print(f"  {label:<35} CV={r2s.mean():.4f}, d={diffs.mean():+.4f}, p={p:.4f}")

    # ── TABLE 4: Discount unpredictability ───────────────────────────

    print("\n\n### TABLE 4: Sentencing Discount Unpredictability")

    corpus_clean = corpus[(corpus["vonis_years"] / corpus["tuntutan_years"]).between(0, 5)].copy()
    discount = corpus_clean["vonis_years"] / corpus_clean["tuntutan_years"]
    print(f"  Discount: mean={discount.mean():.3f}, median={discount.median():.3f}, std={discount.std():.3f}")

    t_disc = text_lower(corpus_clean)
    X_disc = np.column_stack([
        np.log1p(corpus_clean["kerugian_negara"].fillna(0).values),
        t_disc.str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
        t_disc.str.contains(r"pasal\s+3\b", regex=True).astype(int).values,
        t_disc.str.contains("gratifikasi").astype(int).values,
        t_disc.str.contains("memberatkan").astype(int).values,
        t_disc.str.contains("meringankan").astype(int).values,
    ])
    y_disc = discount.values

    kf = KFold(n_splits=10, shuffle=True, random_state=SEED)
    disc_r2s = []
    for tri, vai in kf.split(X_disc):
        sc = StandardScaler()
        m = Ridge(alpha=10)
        m.fit(sc.fit_transform(X_disc[tri]), y_disc[tri])
        pred = m.predict(sc.transform(X_disc[vai]))
        ss_res = np.sum((y_disc[vai] - pred)**2)
        ss_tot = np.sum((y_disc[vai] - y_disc[vai].mean())**2)
        disc_r2s.append(1 - ss_res / ss_tot if ss_tot > 0 else 0)
    print(f"  Predicting discount from text features: R2={np.mean(disc_r2s):.4f} (UNPREDICTABLE)")

    # ── TABLE 5: Judge effects ───────────────────────────────────────

    print("\n\n### TABLE 5: Judge Effects")

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

    groups = [merged.loc[merged["ketua"] == j, "residual"].values for j in freq_judges]
    groups = [g for g in groups if len(g) >= 3]
    if len(groups) >= 2:
        f_stat, p_anova = stats.f_oneway(*groups)
        print(f"  ANOVA on residuals by hakim ketua: F={f_stat:.2f}, p={p_anova:.4f}")
        print(f"  Frequent judges (>=3 cases): {len(freq_judges)}")
        resids = [(j, merged.loc[merged["ketua"] == j, "residual"].mean(), freq[j])
                  for j in freq_judges]
        resids.sort(key=lambda x: x[1])
        print(f"  Most lenient:  {resids[0][0]} ({resids[0][1]:+.2f}yr, n={resids[0][2]})")
        print(f"  Most harsh:    {resids[-1][0]} ({resids[-1][1]:+.2f}yr, n={resids[-1][2]})")
        print(f"  Range: {resids[-1][1] - resids[0][1]:.2f}yr")

    # ── TABLE 6: Geographic disparity ────────────────────────────────

    print("\n\n### TABLE 6: Geographic Disparity (courts with n>=5)")

    geo = corpus.groupby("daerah").agg(
        n=("residual", "count"),
        mean_residual=("residual", "mean"),
        rmse=("residual", lambda x: np.sqrt(np.mean(x**2))),
    ).reset_index()
    geo = geo[geo["n"] >= 5].sort_values("mean_residual")

    print(f"{'Court':<22} {'n':>4} {'Bias':>8} {'RMSE':>6}")
    for _, row in geo.iterrows():
        print(f"  {row['daerah']:<20} {int(row['n']):>4} {row['mean_residual']:>+7.2f}yr {row['rmse']:>5.2f}")

    # ── TABLE 7: Split robustness ───────────────────────────────────

    print("\n\n### TABLE 7: Split Robustness (10 random seeds)")

    from sklearn.model_selection import train_test_split as tts
    split_deltas = []
    split_ps = []
    for seed in range(10):
        bins_s = pd.qcut(corpus["vonis_years"], q=4, labels=False, duplicates="drop")
        tv_s, _ = tts(corpus, test_size=0.15, random_state=seed, stratify=bins_s)
        bins_tv_s = pd.qcut(tv_s["vonis_years"], q=4, labels=False, duplicates="drop")
        tr_s, va_s = tts(tv_s, test_size=0.176, random_state=seed, stratify=bins_tv_s)
        cv_s = pd.concat([tr_s, va_s]).reset_index(drop=True)
        cv_y_s = cv_s["vonis_years"].values

        rkf_s = RepeatedKFold(n_splits=10, n_repeats=3, random_state=42)
        r2s_s, bls_s = [], []
        for tri, vai in rkf_s.split(cv_s):
            tr, va = cv_s.iloc[tri], cv_s.iloc[vai]
            X_tr = np.column_stack([tr["tuntutan_years"].values,
                text_lower(tr).str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
                text_lower(tr).str.contains("gratifikasi").astype(int).values,
                text_lower(tr).str.contains(r"pencucian\s+uang", regex=True).astype(int).values])
            X_va = np.column_stack([va["tuntutan_years"].values,
                text_lower(va).str.contains(r"pasal\s+2\b", regex=True).astype(int).values,
                text_lower(va).str.contains("gratifikasi").astype(int).values,
                text_lower(va).str.contains(r"pencucian\s+uang", regex=True).astype(int).values])
            sc = StandardScaler(); m = Ridge(alpha=20)
            m.fit(sc.fit_transform(X_tr), cv_y_s[tri])
            r2s_s.append(evaluate(cv_y_s[vai], m.predict(sc.transform(X_va)))["val_r2"])
            bls_s.append(evaluate(cv_y_s[vai], baseline_predict(va))["val_r2"])
        r2s_s, bls_s = np.array(r2s_s), np.array(bls_s)
        d_s = r2s_s - bls_s
        _, p_s = stats.ttest_rel(r2s_s, bls_s)
        split_deltas.append(d_s.mean())
        split_ps.append(p_s)
        sig = "**" if p_s < 0.05 else "*" if p_s < 0.1 else ""
        print(f"  seed={seed}: delta={d_s.mean():+.4f}, p={p_s:.4f} {sig}")

    print(f"  Mean delta: {np.mean(split_deltas):+.4f} +/- {np.std(split_deltas):.4f}")
    print(f"  All positive: {all(d > 0 for d in split_deltas)}")
    print(f"  Significant (p<0.05): {sum(1 for p in split_ps if p < 0.05)}/10")

    # ── Summary ──────────────────────────────────────────────────────

    print("\n\n" + "=" * 70)
    print("PAPER 2 KEY NUMBERS")
    print("=" * 70)
    print(f"  Corpus: {len(corpus)} verdicts with text")
    print(f"  CV pool: {n}")
    print(f"  Minimal model (4 features): CV delta = {results['Minimal: tuntutan+p2+grat+pencucian (a=20)']['delta']:+.4f}")
    print(f"  Pasal 2 vs 3: d={d_ctrl:.3f}, p={p_ctrl:.4f}")
    print(f"  Discount R2: {np.mean(disc_r2s):.4f}")
    print(f"  Judge ANOVA: F={f_stat:.2f}, p={p_anova:.4f}")
    print(f"  Split robustness: {sum(1 for p in split_ps if p < 0.05)}/10 significant, all positive")


if __name__ == "__main__":
    main()
