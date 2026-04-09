"""Cross-validation deep dive — are text features really helping?

This script runs 10-fold CV comparing:
1. Tuntutan-only baseline (M9: 0.49 + 0.63 * tuntutan)
2. Ridge on tuntutan only (fitted, not fixed coefficients)
3. Ridge on TF-IDF(100) + tuntutan + kerugian (best autoresearch config)
4. Ridge on TF-IDF(100) only (no structured features)
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, RepeatedKFold
from scipy.sparse import hstack
import re

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from autoresearch.prepare import load_corpus, evaluate, baseline_predict, BASELINE_R2


def preprocess_text(texts):
    def clean(text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'\d+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return texts.apply(clean)


def run_cv():
    corpus = load_corpus(require_text=True)
    print(f"Corpus size: {len(corpus)}")

    y = corpus['vonis_years'].values

    # Use RepeatedKFold for more stable estimates
    rkf = RepeatedKFold(n_splits=10, n_repeats=5, random_state=42)

    results = {
        'baseline_m9': [],      # Fixed M9 coefficients
        'ridge_tuntutan': [],   # Fitted Ridge on tuntutan only
        'ridge_text_tuntutan': [],  # TF-IDF + tuntutan
        'ridge_text_all': [],   # TF-IDF + tuntutan + kerugian
        'ridge_text_only': [],  # TF-IDF only
    }

    for fold_i, (train_idx, val_idx) in enumerate(rkf.split(corpus)):
        train_df = corpus.iloc[train_idx]
        val_df = corpus.iloc[val_idx]
        y_train = y[train_idx]
        y_val = y[val_idx]

        # 1. M9 baseline (fixed coefficients)
        m9_pred = baseline_predict(val_df)
        m9_metrics = evaluate(y_val, m9_pred)
        results['baseline_m9'].append(m9_metrics['val_r2'])

        # 2. Fitted Ridge on tuntutan only
        scaler_t = StandardScaler()
        X_train_t = scaler_t.fit_transform(train_df[['tuntutan_years']].values)
        X_val_t = scaler_t.transform(val_df[['tuntutan_years']].values)
        m_t = Ridge(alpha=0.05)
        m_t.fit(X_train_t, y_train)
        results['ridge_tuntutan'].append(evaluate(y_val, m_t.predict(X_val_t))['val_r2'])

        # Text preprocessing
        train_texts = preprocess_text(train_df['pertimbangan_text'])
        val_texts = preprocess_text(val_df['pertimbangan_text'])

        # TF-IDF
        vec = TfidfVectorizer(max_features=100, ngram_range=(1, 1), min_df=2,
                              max_df=0.9, sublinear_tf=True, use_idf=True)
        X_train_tfidf = vec.fit_transform(train_texts)
        X_val_tfidf = vec.transform(val_texts)

        # 3. TF-IDF + tuntutan
        scaler_s = StandardScaler()
        X_train_s = scaler_s.fit_transform(train_df[['tuntutan_years']].fillna(0).values)
        X_val_s = scaler_s.transform(val_df[['tuntutan_years']].fillna(0).values)
        X_train_tt = hstack([X_train_tfidf, X_train_s])
        X_val_tt = hstack([X_val_tfidf, X_val_s])
        m_tt = Ridge(alpha=0.05)
        m_tt.fit(X_train_tt, y_train)
        results['ridge_text_tuntutan'].append(evaluate(y_val, m_tt.predict(X_val_tt))['val_r2'])

        # 4. TF-IDF + tuntutan + kerugian
        scaler_a = StandardScaler()
        cols_all = train_df[['tuntutan_years', 'kerugian_negara']].fillna(0)
        cols_val_all = val_df[['tuntutan_years', 'kerugian_negara']].fillna(0)
        X_train_sa = scaler_a.fit_transform(cols_all.values)
        X_val_sa = scaler_a.transform(cols_val_all.values)
        X_train_ta = hstack([X_train_tfidf, X_train_sa])
        X_val_ta = hstack([X_val_tfidf, X_val_sa])
        m_ta = Ridge(alpha=0.05)
        m_ta.fit(X_train_ta, y_train)
        results['ridge_text_all'].append(evaluate(y_val, m_ta.predict(X_val_ta))['val_r2'])

        # 5. TF-IDF only
        m_to = Ridge(alpha=0.05)
        m_to.fit(X_train_tfidf, y_train)
        results['ridge_text_only'].append(evaluate(y_val, m_to.predict(X_val_tfidf))['val_r2'])

    print(f"\n{'='*65}")
    print(f"{'Model':<25} {'Mean R²':>10} {'Std':>8} {'Min':>8} {'Max':>8}")
    print(f"{'='*65}")
    for name, r2s in results.items():
        arr = np.array(r2s)
        print(f"{name:<25} {arr.mean():>10.4f} {arr.std():>8.4f} {arr.min():>8.4f} {arr.max():>8.4f}")
    print(f"{'='*65}")

    # Paired comparison: text_all vs baseline
    diff = np.array(results['ridge_text_all']) - np.array(results['baseline_m9'])
    from scipy import stats
    t_stat, p_val = stats.ttest_1samp(diff, 0)
    print(f"\nPaired t-test (text_all vs M9 baseline):")
    print(f"  Mean improvement: {diff.mean():.4f}")
    print(f"  t-stat: {t_stat:.3f}, p-value: {p_val:.4f}")
    print(f"  {'SIGNIFICANT' if p_val < 0.05 else 'NOT SIGNIFICANT'} at p<0.05")

    # Also compare text_tuntutan vs ridge_tuntutan
    diff2 = np.array(results['ridge_text_tuntutan']) - np.array(results['ridge_tuntutan'])
    t2, p2 = stats.ttest_1samp(diff2, 0)
    print(f"\nPaired t-test (text+tuntutan vs tuntutan-only Ridge):")
    print(f"  Mean improvement: {diff2.mean():.4f}")
    print(f"  t-stat: {t2:.3f}, p-value: {p2:.4f}")
    print(f"  {'SIGNIFICANT' if p2 < 0.05 else 'NOT SIGNIFICANT'} at p<0.05")

    # How often does text help?
    n_better = (diff > 0).sum()
    print(f"\nText features help in {n_better}/{len(diff)} folds ({n_better/len(diff)*100:.0f}%)")

    # Alpha sweep with CV
    print(f"\n{'='*50}")
    print("Alpha sweep (Ridge text_all, 10x5 CV):")
    print(f"{'='*50}")
    for alpha in [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0]:
        r2s = []
        for train_idx, val_idx in rkf.split(corpus):
            train_df_a = corpus.iloc[train_idx]
            val_df_a = corpus.iloc[val_idx]
            y_train_a = y[train_idx]
            y_val_a = y[val_idx]
            texts_tr = preprocess_text(train_df_a['pertimbangan_text'])
            texts_va = preprocess_text(val_df_a['pertimbangan_text'])
            v = TfidfVectorizer(max_features=100, ngram_range=(1,1), min_df=2,
                                max_df=0.9, sublinear_tf=True, use_idf=True)
            X_tr = v.fit_transform(texts_tr)
            X_va = v.transform(texts_va)
            sc = StandardScaler()
            s_tr = sc.fit_transform(train_df_a[['tuntutan_years', 'kerugian_negara']].fillna(0).values)
            s_va = sc.transform(val_df_a[['tuntutan_years', 'kerugian_negara']].fillna(0).values)
            X_tr_f = hstack([X_tr, s_tr])
            X_va_f = hstack([X_va, s_va])
            m = Ridge(alpha=alpha)
            m.fit(X_tr_f, y_train_a)
            r2s.append(evaluate(y_val_a, m.predict(X_va_f))['val_r2'])
        arr = np.array(r2s)
        delta = arr.mean() - 0.5318  # vs baseline
        marker = " ***" if delta > 0 else ""
        print(f"  alpha={alpha:<6} CV R²={arr.mean():.4f} (std={arr.std():.4f}) delta={delta:+.4f}{marker}")

    return results


if __name__ == "__main__":
    run_cv()
