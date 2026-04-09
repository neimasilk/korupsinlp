"""Fixed evaluation harness for autoresearch experiments.

THIS FILE IS READ-ONLY — the autonomous agent must NOT modify it.

Provides:
- Constants (time budget, seed, baseline)
- Data loading from SQLite
- Deterministic train/val/test splits
- Evaluation metrics
- Baseline prediction (M9: tuntutan-only linear model)
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from sklearn.model_selection import train_test_split

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import DB_PATH
from src.db import get_connection

# === Fixed Constants (NEVER change these during experiments) ===

TIME_BUDGET = 60         # seconds — sklearn is fast, 60s is generous
RANDOM_SEED = 42         # reproducible splits
TEST_SIZE = 0.15         # held-out test set — NEVER touch during experiments
VAL_SIZE = 0.15          # validation set — used for keep/discard decisions
BASELINE_R2 = 0.600      # M9 tuntutan-only R², the number to beat

# M9 linear coefficients: vonis_years = INTERCEPT + SLOPE * tuntutan_years
M9_INTERCEPT = 0.49
M9_SLOPE = 0.63


def load_corpus(db_path: Path = DB_PATH, require_text: bool = True) -> pd.DataFrame:
    """Load the analysis-ready corpus from SQLite.

    Args:
        db_path: Path to SQLite database.
        require_text: If True, only return verdicts with pertimbangan_text.
            If False, return all verdicts with vonis + tuntutan (for structured-only mode).

    Filters:
    - vonis_bulan > 0 (exclude acquittals and missing)
    - tuntutan_bulan > 0 (need tuntutan for baseline)
    - pertimbangan_text IS NOT NULL and len >= 200 (if require_text=True)

    Returns DataFrame with columns:
        id, vonis_bulan, vonis_years, tuntutan_bulan, tuntutan_years,
        kerugian_negara, daerah, tahun, pemohon_kasasi, pasal,
        pertimbangan_text (may be NULL if require_text=False)
    """
    conn = get_connection(db_path)
    try:
        text_filter = ""
        if require_text:
            text_filter = "AND pertimbangan_text IS NOT NULL AND LENGTH(pertimbangan_text) >= 200"

        df = pd.read_sql_query(
            f"""
            SELECT id, vonis_bulan, tuntutan_bulan, kerugian_negara,
                   daerah, tahun, pemohon_kasasi, pasal,
                   pertimbangan_text,
                   faktor_memberatkan, faktor_meringankan
            FROM verdicts
            WHERE vonis_bulan > 0
              AND tuntutan_bulan > 0
              {text_filter}
            """,
            conn,
        )
    finally:
        conn.close()

    # Derived columns
    df["vonis_years"] = df["vonis_bulan"] / 12.0
    df["tuntutan_years"] = df["tuntutan_bulan"] / 12.0

    return df


def get_splits(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Create deterministic stratified train/val/test splits.

    Stratifies by binned vonis (4 quantile bins) to ensure each split
    has similar sentence distributions.

    Returns (train_df, val_df, test_df) with disjoint indices.
    """
    # Create stratification bins
    bins = pd.qcut(df["vonis_years"], q=4, labels=False, duplicates="drop")

    # First split: train+val vs test
    train_val_df, test_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=bins,
    )

    # Second split: train vs val
    bins_tv = pd.qcut(train_val_df["vonis_years"], q=4, labels=False, duplicates="drop")
    relative_val = VAL_SIZE / (1 - TEST_SIZE)
    train_df, val_df = train_test_split(
        train_val_df, test_size=relative_val, random_state=RANDOM_SEED, stratify=bins_tv,
    )

    return train_df.copy(), val_df.copy(), test_df.copy()


def baseline_predict(df: pd.DataFrame) -> np.ndarray:
    """M9 baseline: vonis_years = 0.49 + 0.63 * tuntutan_years.

    This is the tuntutan-only linear model from Paper 1 (R²=0.600).
    Text features must beat this to be meaningful.
    """
    return M9_INTERCEPT + M9_SLOPE * df["tuntutan_years"].values


def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Compute evaluation metrics. Primary metric: val_r2.

    Args:
        y_true: actual vonis in years
        y_pred: predicted vonis in years

    Returns dict with:
        val_r2: R² score (primary metric — higher is better)
        val_r2_improvement: val_r2 - BASELINE_R2
        val_mae: Mean Absolute Error in years
        val_rmse: Root Mean Squared Error in years
        val_spearman: Spearman rank correlation
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    spearman = scipy_stats.spearmanr(y_true, y_pred).statistic

    return {
        "val_r2": float(r2),
        "val_r2_improvement": float(r2 - BASELINE_R2),
        "val_mae": float(mae),
        "val_rmse": float(rmse),
        "val_spearman": float(spearman),
    }
