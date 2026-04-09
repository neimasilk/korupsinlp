"""KorupsiNLP autoresearch: text feature experiments.

THIS IS THE MUTABLE FILE — the autonomous agent modifies this.
Everything is fair game: text preprocessing, feature extraction,
model choice, hyperparameters, feature combination strategy.

Usage: python -m autoresearch.train
"""

import time
import re

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack, issparse

from autoresearch.prepare import (
    load_corpus, get_splits, evaluate, baseline_predict,
    TIME_BUDGET, BASELINE_R2,
)

# ==== HYPERPARAMETERS (agent can change all of these) ====

# TF-IDF settings
MAX_FEATURES = 100
NGRAM_RANGE = (1, 1)
MIN_DF = 2
MAX_DF = 0.9
SUBLINEAR_TF = True
USE_IDF = True

# Model settings
ALPHA = 0.05  # Ridge regularization

# Feature combination: 'text_only', 'text_tuntutan', 'text_all'
FEATURE_MODE = 'text_all'


# ==== TEXT PREPROCESSING (agent can change this) ====

def preprocess_text(texts: pd.Series) -> pd.Series:
    """Clean and normalize pertimbangan text."""
    def clean(text):
        if not isinstance(text, str):
            return ""
        # Lowercase
        text = text.lower()
        # Remove numbers (dates, case numbers, amounts — noise for text features)
        text = re.sub(r'\d+', ' ', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return texts.apply(clean)


# ==== FEATURE EXTRACTION (agent can change this) ====

def extract_features(train_texts, val_texts, train_df, val_df):
    """Convert text + structured features to model inputs.

    Returns (X_train, X_val, feature_names).
    """
    # TF-IDF on pertimbangan text
    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=NGRAM_RANGE,
        min_df=MIN_DF,
        max_df=MAX_DF,
        sublinear_tf=SUBLINEAR_TF,
        use_idf=USE_IDF,
    )
    X_train_text = vectorizer.fit_transform(train_texts)
    X_val_text = vectorizer.transform(val_texts)
    feature_names = vectorizer.get_feature_names_out().tolist()

    if FEATURE_MODE == 'text_only':
        return X_train_text, X_val_text, feature_names

    # Add structured features
    struct_cols = ['tuntutan_years']
    if FEATURE_MODE == 'text_all':
        if 'kerugian_negara' in train_df.columns:
            struct_cols.append('kerugian_negara')

    scaler = StandardScaler()
    X_train_struct = scaler.fit_transform(
        train_df[struct_cols].fillna(0).values
    )
    X_val_struct = scaler.transform(
        val_df[struct_cols].fillna(0).values
    )

    X_train = hstack([X_train_text, X_train_struct])
    X_val = hstack([X_val_text, X_val_struct])
    feature_names += struct_cols

    return X_train, X_val, feature_names


# ==== MODEL (agent can change this) ====

def build_model():
    """Create and return the model."""
    return Ridge(alpha=ALPHA)


# ==== MAIN ====

def main():
    t_start = time.time()

    # Load data (fixed by prepare.py)
    # Try with pertimbangan text first; fall back to structured-only mode
    corpus = load_corpus(require_text=True)
    has_text = len(corpus) > 0

    if not has_text:
        print("WARNING: No pertimbangan text available. Running in structured-only mode.")
        print("         Re-scrape PDFs and run scripts/09_extract_pertimbangan.py first.")
        corpus = load_corpus(require_text=False)

    train_df, val_df, test_df = get_splits(corpus)

    # Preprocess text (if available)
    if has_text:
        train_texts = preprocess_text(train_df['pertimbangan_text'])
        val_texts = preprocess_text(val_df['pertimbangan_text'])

        # Extract features
        X_train, X_val, feature_names = extract_features(
            train_texts, val_texts, train_df, val_df
        )
    else:
        # Structured-only fallback: just tuntutan
        scaler = StandardScaler()
        X_train = scaler.fit_transform(train_df[['tuntutan_years']].values)
        X_val = scaler.transform(val_df[['tuntutan_years']].values)
        feature_names = ['tuntutan_years']
    y_train = train_df['vonis_years'].values
    y_val = val_df['vonis_years'].values

    # Train
    model = build_model()
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_val)

    # Evaluate
    metrics = evaluate(y_val, y_pred)

    # Also compute baseline for comparison
    y_baseline = baseline_predict(val_df)
    baseline_metrics = evaluate(y_val, y_baseline)

    elapsed = time.time() - t_start

    # Cross-validation for robustness check
    from sklearn.model_selection import KFold
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    # Combine train+val for CV (leave test untouched)
    cv_df = pd.concat([train_df, val_df]).reset_index(drop=True)
    cv_texts = preprocess_text(cv_df['pertimbangan_text'])
    cv_y = cv_df['vonis_years'].values
    cv_r2s = []
    cv_baseline_r2s = []
    for train_idx, val_idx in kf.split(cv_df):
        cv_train_texts = cv_texts.iloc[train_idx]
        cv_val_texts = cv_texts.iloc[val_idx]
        cv_train_df = cv_df.iloc[train_idx]
        cv_val_df = cv_df.iloc[val_idx]
        X_tr, X_va, _ = extract_features(cv_train_texts, cv_val_texts, cv_train_df, cv_val_df)
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

    # Print results in fixed format for machine parsing
    print("---")
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
