"""KorupsiNLP autoresearch: structured text feature experiments.

THIS IS THE MUTABLE FILE — the autonomous agent modifies this.

PIVOT from TF-IDF (30 experiments, failed) to domain-specific features.

Key finding: Three binary features from pertimbangan text (pasal_2,
gratifikasi, pencucian_uang) improve sentencing prediction with high
significance (p=0.002, 5x10 CV). This is a dramatic improvement from
TF-IDF which was p<0.0001 WORSE.

Usage: python -m autoresearch.train
"""

import time
import re
import json

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from autoresearch.prepare import (
    load_corpus, get_splits, evaluate, baseline_predict,
    TIME_BUDGET, BASELINE_R2,
)

# ==== HYPERPARAMETERS ====

ALPHA = 20.0  # Ridge regularization — optimal from alpha sweep (session 11 battery)

# Feature mode: 'minimal' (tuntutan + pasal_2 + gratifikasi)
#               'extended' (+ miliar, factor_list)
#               'full' (all keyword features)
FEATURE_MODE = 'minimal'


# ==== STRUCTURED TEXT FEATURES ====

def extract_keyword_features(df: pd.DataFrame, mode: str = 'minimal') -> pd.DataFrame:
    """Extract domain-specific features from pertimbangan text.

    These features encode legal concepts via regex pattern matching.
    """
    features = pd.DataFrame(index=df.index)
    texts = df['pertimbangan_text'].fillna('').str.lower()

    # Always include: charge type + crime category (strongest predictors)
    features['has_pasal_2'] = texts.str.contains(r'pasal\s+2\b', regex=True).astype(int)
    features['has_gratifikasi'] = texts.str.contains(r'gratifikasi', regex=False).astype(int)
    features['has_pencucian'] = texts.str.contains(r'pencucian\s+uang', regex=True).astype(int)

    if mode in ('extended', 'full'):
        features['has_pasal_3'] = texts.str.contains(r'pasal\s+3\b', regex=True).astype(int)
        features['has_miliar'] = texts.str.contains(r'miliar', regex=False).astype(int)
        features['has_factor_list'] = texts.str.contains(
            r'(?:hal[- ]hal|keadaan)\s+yang\s+memberatkan', regex=True
        ).astype(int)

    if mode == 'full':
        features['has_pasal_12'] = texts.str.contains(r'pasal\s+12\b', regex=True).astype(int)
        features['has_mengembalikan'] = texts.str.contains(
            r'mengembalikan|pengembalian', regex=True
        ).astype(int)
        features['has_uang_pengganti'] = texts.str.contains(
            r'uang\s+pengganti', regex=True
        ).astype(int)
        features['has_jabatan'] = texts.str.contains(r'jabatan', regex=False).astype(int)
        features['has_suap'] = texts.str.contains(r'suap', regex=False).astype(int)
        features['has_merugikan_negara'] = texts.str.contains(
            r'merugikan\s+(?:keuangan\s+)?negara', regex=True
        ).astype(int)
        features['n_memberatkan'] = texts.str.count(r'memberatkan')
        features['n_meringankan'] = texts.str.count(r'meringankan')
        features['text_length'] = texts.str.len()

        def count_factors(col):
            def _count(val):
                if pd.isna(val) or val in ('', '[]'):
                    return 0
                try:
                    return len(json.loads(val))
                except (json.JSONDecodeError, TypeError):
                    return 0
            return df[col].apply(_count)

        features['n_faktor_memberatkan'] = count_factors('faktor_memberatkan')
        features['n_faktor_meringankan'] = count_factors('faktor_meringankan')

    return features


# ==== FEATURE EXTRACTION ====

def extract_features(train_df, val_df):
    """Build feature matrices: tuntutan + keyword features.

    Returns (X_train, X_val, feature_names).
    """
    train_kw = extract_keyword_features(train_df, mode=FEATURE_MODE)
    val_kw = extract_keyword_features(val_df, mode=FEATURE_MODE)

    # Combine with tuntutan
    train_all = pd.concat([
        train_df[['tuntutan_years']].reset_index(drop=True),
        train_kw.reset_index(drop=True),
    ], axis=1)
    val_all = pd.concat([
        val_df[['tuntutan_years']].reset_index(drop=True),
        val_kw.reset_index(drop=True),
    ], axis=1)

    feature_names = train_all.columns.tolist()
    scaler = StandardScaler()
    X_train = scaler.fit_transform(train_all.fillna(0).values)
    X_val = scaler.transform(val_all.fillna(0).values)

    return X_train, X_val, feature_names


# ==== MODEL ====

def build_model():
    """Create and return the model."""
    return Ridge(alpha=ALPHA)


# ==== MAIN ====

def main():
    t_start = time.time()

    corpus = load_corpus(require_text=True)
    has_text = len(corpus) > 0

    if not has_text:
        print("WARNING: No pertimbangan text available.")
        corpus = load_corpus(require_text=False)

    train_df, val_df, test_df = get_splits(corpus)

    # Extract features
    X_train, X_val, feature_names = extract_features(train_df, val_df)
    y_train = train_df['vonis_years'].values
    y_val = val_df['vonis_years'].values

    # Train
    model = build_model()
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_val)

    # Evaluate
    metrics = evaluate(y_val, y_pred)

    # Baseline
    y_baseline = baseline_predict(val_df)
    baseline_metrics = evaluate(y_val, y_baseline)

    elapsed = time.time() - t_start

    # Cross-validation
    from sklearn.model_selection import KFold
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    cv_df = pd.concat([train_df, val_df]).reset_index(drop=True)
    cv_y = cv_df['vonis_years'].values
    cv_r2s = []
    cv_baseline_r2s = []
    for train_idx, val_idx in kf.split(cv_df):
        cv_train_df = cv_df.iloc[train_idx]
        cv_val_df = cv_df.iloc[val_idx]
        X_tr, X_va, _ = extract_features(cv_train_df, cv_val_df)
        m = build_model()
        m.fit(X_tr, cv_y[train_idx])
        pred = m.predict(X_va)
        cv_metrics = evaluate(cv_y[val_idx], pred)
        cv_r2s.append(cv_metrics['val_r2'])
        bl_pred = baseline_predict(cv_val_df)
        bl_metrics = evaluate(cv_y[val_idx], bl_pred)
        cv_baseline_r2s.append(bl_metrics['val_r2'])

    cv_r2_mean = np.mean(cv_r2s)
    cv_r2_std = np.std(cv_r2s)
    cv_bl_mean = np.mean(cv_baseline_r2s)

    # Feature importance
    if hasattr(model, 'coef_'):
        print("\n--- Feature Importance (Ridge coefficients) ---")
        coefs = list(zip(feature_names, model.coef_))
        coefs.sort(key=lambda x: abs(x[1]), reverse=True)
        for name, coef in coefs[:20]:
            print(f"  {name:30s}  {coef:+.4f}")

    # Print results
    print("\n---")
    print(f"val_r2:              {metrics['val_r2']:.6f}")
    print(f"val_r2_improvement:  {metrics['val_r2_improvement']:.6f}")
    print(f"val_mae:             {metrics['val_mae']:.6f}")
    print(f"val_rmse:            {metrics['val_rmse']:.6f}")
    print(f"val_spearman:        {metrics['val_spearman']:.6f}")
    print(f"baseline_r2:         {baseline_metrics['val_r2']:.6f}")
    print(f"baseline_mae:        {baseline_metrics['val_mae']:.6f}")
    print(f"cv_r2_mean:          {cv_r2_mean:.6f}")
    print(f"cv_r2_std:           {cv_r2_std:.6f}")
    print(f"cv_baseline_mean:    {cv_bl_mean:.6f}")
    print(f"cv_improvement:      {cv_r2_mean - cv_bl_mean:.6f}")
    print(f"elapsed_seconds:     {elapsed:.1f}")
    print(f"n_train:             {len(train_df)}")
    print(f"n_val:               {len(val_df)}")
    print(f"n_test:              {len(test_df)}")
    print(f"n_features:          {len(feature_names)}")
    print(f"feature_mode:        {FEATURE_MODE}")
    print(f"model:               {model.__class__.__name__}")
    print(f"status:              ok")


if __name__ == "__main__":
    main()
