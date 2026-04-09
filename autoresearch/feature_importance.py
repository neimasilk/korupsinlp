"""Feature importance analysis — which words associate with lighter/heavier sentences?

Even though text features don't improve prediction over tuntutan (cross-validation
confirms this), we can still analyze which words have the strongest association
with sentence severity. This is valuable for descriptive/interpretive purposes.

Output: top words associated with heavier and lighter sentences.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack
import re

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from autoresearch.prepare import load_corpus, get_splits


def preprocess_text(texts):
    def clean(text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'\d+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return texts.apply(clean)


def analyze():
    corpus = load_corpus(require_text=True)
    train_df, val_df, test_df = get_splits(corpus)

    # Use full train+val for analysis (test still locked)
    analysis_df = pd.concat([train_df, val_df]).reset_index(drop=True)
    texts = preprocess_text(analysis_df['pertimbangan_text'])
    y = analysis_df['vonis_years'].values

    print(f"Analysis corpus: n={len(analysis_df)}")
    print(f"Sentence range: {y.min():.1f} — {y.max():.1f} years (mean={y.mean():.1f})")

    # === APPROACH 1: Ridge coefficients on TF-IDF ===
    print(f"\n{'='*60}")
    print("APPROACH 1: Ridge coefficients (TF-IDF + tuntutan + kerugian)")
    print(f"{'='*60}")

    vec = TfidfVectorizer(max_features=100, ngram_range=(1, 1), min_df=2,
                          max_df=0.9, sublinear_tf=True, use_idf=True)
    X_text = vec.fit_transform(texts)
    feature_names = vec.get_feature_names_out().tolist()

    scaler = StandardScaler()
    X_struct = scaler.fit_transform(
        analysis_df[['tuntutan_years', 'kerugian_negara']].fillna(0).values
    )

    X = hstack([X_text, X_struct])
    all_names = feature_names + ['tuntutan_years', 'kerugian_negara']

    model = Ridge(alpha=0.05)
    model.fit(X, y)

    # Get coefficients
    coefs = model.coef_
    coef_df = pd.DataFrame({
        'feature': all_names,
        'coefficient': coefs,
        'abs_coef': np.abs(coefs),
    }).sort_values('abs_coef', ascending=False)

    print(f"\nStructured feature coefficients:")
    for _, row in coef_df[coef_df['feature'].isin(['tuntutan_years', 'kerugian_negara'])].iterrows():
        print(f"  {row['feature']:<25} {row['coefficient']:>+8.4f}")

    print(f"\nTop 15 words predicting HEAVIER sentences (positive coefficients):")
    text_coefs = coef_df[~coef_df['feature'].isin(['tuntutan_years', 'kerugian_negara'])]
    heavy = text_coefs[text_coefs['coefficient'] > 0].sort_values('coefficient', ascending=False).head(15)
    for _, row in heavy.iterrows():
        print(f"  {row['feature']:<25} {row['coefficient']:>+8.4f}")

    print(f"\nTop 15 words predicting LIGHTER sentences (negative coefficients):")
    light = text_coefs[text_coefs['coefficient'] < 0].sort_values('coefficient', ascending=True).head(15)
    for _, row in light.iterrows():
        print(f"  {row['feature']:<25} {row['coefficient']:>+8.4f}")

    # === APPROACH 2: Simple correlation between word presence and vonis ===
    print(f"\n{'='*60}")
    print("APPROACH 2: Spearman correlation (word TF-IDF vs vonis_years)")
    print(f"{'='*60}")

    from scipy.stats import spearmanr
    correlations = []
    X_dense = X_text.toarray()
    for i, word in enumerate(feature_names):
        corr, pval = spearmanr(X_dense[:, i], y)
        correlations.append({
            'word': word,
            'spearman_r': corr,
            'p_value': pval,
            'significant': pval < 0.05,
        })

    corr_df = pd.DataFrame(correlations).sort_values('spearman_r', ascending=False)

    n_sig = corr_df['significant'].sum()
    print(f"\nSignificant correlations (p<0.05): {n_sig}/{len(corr_df)}")

    print(f"\nTop 10 words correlated with HEAVIER sentences:")
    for _, row in corr_df.head(10).iterrows():
        sig = '*' if row['significant'] else ' '
        print(f"  {sig} {row['word']:<25} r={row['spearman_r']:>+.4f} (p={row['p_value']:.4f})")

    print(f"\nTop 10 words correlated with LIGHTER sentences:")
    for _, row in corr_df.tail(10).iloc[::-1].iterrows():
        sig = '*' if row['significant'] else ' '
        print(f"  {sig} {row['word']:<25} r={row['spearman_r']:>+.4f} (p={row['p_value']:.4f})")

    # === APPROACH 3: Word frequency in light vs heavy sentences ===
    print(f"\n{'='*60}")
    print("APPROACH 3: Word prevalence in light vs heavy sentences")
    print(f"{'='*60}")

    # Split into light (bottom 25%) and heavy (top 25%) sentences
    q25 = np.percentile(y, 25)
    q75 = np.percentile(y, 75)
    light_mask = y <= q25
    heavy_mask = y >= q75
    n_light = light_mask.sum()
    n_heavy = heavy_mask.sum()
    print(f"Light sentences (≤{q25:.1f}yr): n={n_light}")
    print(f"Heavy sentences (≥{q75:.1f}yr): n={n_heavy}")

    # Binary presence in each group
    X_binary = (X_dense > 0).astype(float)
    light_rate = X_binary[light_mask].mean(axis=0)
    heavy_rate = X_binary[heavy_mask].mean(axis=0)
    diff = heavy_rate - light_rate

    diff_df = pd.DataFrame({
        'word': feature_names,
        'light_pct': light_rate * 100,
        'heavy_pct': heavy_rate * 100,
        'diff_pct': diff * 100,
    }).sort_values('diff_pct', ascending=False)

    print(f"\nWords much MORE common in heavy sentences:")
    for _, row in diff_df.head(10).iterrows():
        print(f"  {row['word']:<25} heavy={row['heavy_pct']:>5.1f}% light={row['light_pct']:>5.1f}% diff={row['diff_pct']:>+5.1f}%")

    print(f"\nWords much MORE common in light sentences:")
    for _, row in diff_df.tail(10).iloc[::-1].iterrows():
        print(f"  {row['word']:<25} heavy={row['heavy_pct']:>5.1f}% light={row['light_pct']:>5.1f}% diff={row['diff_pct']:>+5.1f}%")


if __name__ == "__main__":
    analyze()
