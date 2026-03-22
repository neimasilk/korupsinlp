"""Script 07: Multivariate regression analysis.

Part A: Kerugian models (M1-M5) on n=251 (vonis>0, kerugian>0)
Part B: Tuntutan models (M6-M9) on n=302 (vonis>0, tuntutan>0) and n=236 (all three)
Part C: Sensitivity analyses (outliers, missing data, power)
Saves results to reports/regression_results.json and generates figures.

Usage: python -m scripts.07_regression_analysis
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sqlite3
import numpy as np
from scipy import stats as sp_stats

from src.config import DB_PATH, REPORTS_DIR


def load_regression_data():
    """Load cases with vonis > 0 and valid kerugian."""
    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute("""
        SELECT vonis_bulan / 12.0 as vonis_yr,
               kerugian_negara, pemohon_kasasi, daerah, tahun
        FROM verdicts
        WHERE vonis_bulan > 0
          AND kerugian_negara IS NOT NULL AND kerugian_negara > 0
          AND tahun IS NOT NULL
    """).fetchall()
    conn.close()

    vonis = np.array([r[0] for r in rows])
    log_k = np.array([np.log10(r[1]) for r in rows])
    is_jpu = np.array([1.0 if r[2] == "penuntut_umum" else 0.0 for r in rows])
    is_jp = np.array([1.0 if r[3] == "Jakarta Pusat" else 0.0 for r in rows])
    tahun = np.array([float(r[4]) for r in rows])
    tahun_c = tahun - 2020  # centered for interpretability

    return vonis, log_k, is_jpu, is_jp, tahun_c, len(rows)


def load_tuntutan_data():
    """Load cases with vonis > 0 and valid tuntutan."""
    conn = sqlite3.connect(str(DB_PATH))
    # Dataset with tuntutan only (n~302)
    rows_t = conn.execute("""
        SELECT vonis_bulan / 12.0, tuntutan_bulan / 12.0,
               pemohon_kasasi, daerah, tahun
        FROM verdicts
        WHERE vonis_bulan > 0 AND tuntutan_bulan > 0 AND tahun IS NOT NULL
    """).fetchall()
    # Dataset with all three (n~236)
    rows_all = conn.execute("""
        SELECT vonis_bulan / 12.0, tuntutan_bulan / 12.0, kerugian_negara,
               pemohon_kasasi, daerah, tahun
        FROM verdicts
        WHERE vonis_bulan > 0 AND tuntutan_bulan > 0
              AND kerugian_negara IS NOT NULL AND kerugian_negara > 0
              AND tahun IS NOT NULL
    """).fetchall()
    conn.close()
    return rows_t, rows_all


def run_tuntutan_models(rows_t, rows_all):
    """Fit tuntutan-based models (M6-M9) and discount model."""
    import statsmodels.api as sm

    models = {}

    # M6: vonis ~ log10(tuntutan) [n~302]
    vonis_t = np.array([r[0] for r in rows_t])
    log_tunt = np.array([np.log10(r[1]) for r in rows_t])
    X6 = sm.add_constant(log_tunt)
    m6 = sm.OLS(vonis_t, X6).fit()
    models["M6_tuntutan_only"] = (m6, ["const", "log10_tuntutan"], len(rows_t))

    # M9: vonis ~ tuntutan (linear, not log) [n~302]
    tunt_yr = np.array([r[1] for r in rows_t])
    X9 = sm.add_constant(tunt_yr)
    m9 = sm.OLS(vonis_t, X9).fit()
    models["M9_tuntutan_linear"] = (m9, ["const", "tuntutan_yr"], len(rows_t))

    # M7: vonis ~ log10(tuntutan) + log10(kerugian) [n~236]
    vonis_a = np.array([r[0] for r in rows_all])
    log_tunt_a = np.array([np.log10(r[1]) for r in rows_all])
    log_k_a = np.array([np.log10(r[2]) for r in rows_all])
    is_jpu_a = np.array([1.0 if r[3] == "penuntut_umum" else 0.0 for r in rows_all])
    is_jp_a = np.array([1.0 if r[4] == "Jakarta Pusat" else 0.0 for r in rows_all])
    tahun_a = np.array([float(r[5]) for r in rows_all]) - 2020

    X7 = sm.add_constant(np.column_stack([log_tunt_a, log_k_a]))
    m7 = sm.OLS(vonis_a, X7).fit()
    models["M7_tuntutan_kerugian"] = (m7, ["const", "log10_tuntutan", "log10_kerugian"], len(rows_all))

    # M8: full model with tuntutan [n~236]
    X8 = sm.add_constant(np.column_stack([log_tunt_a, log_k_a, is_jpu_a, is_jp_a, tahun_a]))
    m8 = sm.OLS(vonis_a, X8).fit()
    models["M8_tuntutan_full"] = (
        m8,
        ["const", "log10_tuntutan", "log10_kerugian", "is_jpu", "is_jp", "year_centered"],
        len(rows_all),
    )

    # Discount model: (vonis/tuntutan) ~ log10(kerugian) + pemohon + jp + year [n~236]
    ratio = vonis_a / np.array([r[1] for r in rows_all])
    Xd = sm.add_constant(np.column_stack([log_k_a, is_jpu_a, is_jp_a, tahun_a]))
    md = sm.OLS(ratio, Xd).fit()
    models["Md_discount"] = (
        md,
        ["const", "log10_kerugian", "is_jpu", "is_jp", "year_centered"],
        len(rows_all),
    )

    return models


def run_sensitivity(results_dict):
    """Outlier sensitivity, missing data comparison, power analysis."""
    import statsmodels.api as sm

    conn = sqlite3.connect(str(DB_PATH))
    sensitivity = {}

    # --- Outlier sensitivity ---
    # Full sample (M1 baseline after cleanup)
    rows_full = conn.execute("""
        SELECT vonis_bulan/12.0, kerugian_negara FROM verdicts
        WHERE vonis_bulan > 0 AND kerugian_negara IS NOT NULL AND kerugian_negara > 0
    """).fetchall()
    v_f = np.array([r[0] for r in rows_full])
    lk_f = np.array([np.log10(r[1]) for r in rows_full])
    m_full = sm.OLS(v_f, sm.add_constant(lk_f)).fit()

    # Exclude PT Timah cluster (kerugian > 100T)
    rows_no_pt = [(r[0], r[1]) for r in rows_full if r[1] < 100e12]
    v_np = np.array([r[0] for r in rows_no_pt])
    lk_np = np.array([np.log10(r[1]) for r in rows_no_pt])
    m_no_pt = sm.OLS(v_np, sm.add_constant(lk_np)).fit()

    # Exclude all kerugian > 100B
    rows_no_mega = [(r[0], r[1]) for r in rows_full if r[1] < 100e9]
    v_nm = np.array([r[0] for r in rows_no_mega])
    lk_nm = np.array([np.log10(r[1]) for r in rows_no_mega])
    m_no_mega = sm.OLS(v_nm, sm.add_constant(lk_nm)).fit()

    sensitivity["outlier"] = {
        "full": {"n": len(v_f), "slope": float(m_full.params[1]), "r2": float(m_full.rsquared)},
        "no_pt_timah": {"n": len(v_np), "slope": float(m_no_pt.params[1]), "r2": float(m_no_pt.rsquared)},
        "no_mega_100B": {"n": len(v_nm), "slope": float(m_no_mega.params[1]), "r2": float(m_no_mega.rsquared)},
    }

    # --- Missing data comparison ---
    with_k = conn.execute(
        "SELECT vonis_bulan/12.0 FROM verdicts WHERE vonis_bulan>0 AND kerugian_negara IS NOT NULL"
    ).fetchall()
    without_k = conn.execute(
        "SELECT vonis_bulan/12.0 FROM verdicts WHERE vonis_bulan>0 AND kerugian_negara IS NULL"
    ).fetchall()
    v_with = np.array([r[0] for r in with_k])
    v_without = np.array([r[0] for r in without_k])
    t_miss, p_miss = sp_stats.ttest_ind(v_with, v_without, equal_var=False)
    sensitivity["missing_data"] = {
        "with_kerugian": {"n": len(v_with), "mean": float(v_with.mean()), "std": float(v_with.std())},
        "without_kerugian": {"n": len(v_without), "mean": float(v_without.mean()), "std": float(v_without.std())},
        "welch_t": float(t_miss),
        "p_value": float(p_miss),
        "interpretation": "NOT_MCAR" if p_miss < 0.05 else "consistent_with_MCAR",
    }

    # --- Power analysis ---
    # For pemohon kasasi: minimum detectable effect at alpha=0.05, power=0.80
    # Using formula for two-sample t-test: MDE = (z_alpha + z_beta) * sigma * sqrt(1/n1 + 1/n2)
    jpu_rows = conn.execute(
        "SELECT vonis_bulan/12.0 FROM verdicts WHERE vonis_bulan>0 AND pemohon_kasasi='penuntut_umum'"
    ).fetchall()
    terd_rows = conn.execute(
        "SELECT vonis_bulan/12.0 FROM verdicts WHERE vonis_bulan>0 AND pemohon_kasasi='terdakwa'"
    ).fetchall()
    n1, n2 = len(jpu_rows), len(terd_rows)
    pooled_std = np.sqrt(
        (np.var([r[0] for r in jpu_rows]) * (n1 - 1) + np.var([r[0] for r in terd_rows]) * (n2 - 1))
        / (n1 + n2 - 2)
    )
    z_alpha = 1.96  # two-sided alpha=0.05
    z_beta = 0.84   # power=0.80
    mde = (z_alpha + z_beta) * pooled_std * np.sqrt(1/n1 + 1/n2)
    mde_cohens_d = mde / pooled_std

    sensitivity["power_analysis"] = {
        "pemohon_kasasi": {
            "n_jpu": n1,
            "n_terdakwa": n2,
            "pooled_std": float(pooled_std),
            "mde_years": float(mde),
            "mde_cohens_d": float(mde_cohens_d),
            "interpretation": f"Can detect effects >= {mde:.2f} years ({mde_cohens_d:.3f} d) at 80% power",
        }
    }

    conn.close()
    return sensitivity


def run_ols_models(vonis, log_k, is_jpu, is_jp, tahun_c):
    """Fit nested OLS models and return results."""
    import statsmodels.api as sm

    models = {}

    # M1: bivariate
    X1 = sm.add_constant(log_k)
    m1 = sm.OLS(vonis, X1).fit()
    models["M1_bivariate"] = (m1, ["const", "log10_kerugian"])

    # M2: + pemohon
    X2 = sm.add_constant(np.column_stack([log_k, is_jpu]))
    m2 = sm.OLS(vonis, X2).fit()
    models["M2_pemohon"] = (m2, ["const", "log10_kerugian", "is_jpu"])

    # M3: + Jakarta Pusat
    X3 = sm.add_constant(np.column_stack([log_k, is_jpu, is_jp]))
    m3 = sm.OLS(vonis, X3).fit()
    models["M3_jakarta"] = (m3, ["const", "log10_kerugian", "is_jpu", "is_jp"])

    # M4: + year
    X4 = sm.add_constant(np.column_stack([log_k, is_jpu, is_jp, tahun_c]))
    m4 = sm.OLS(vonis, X4).fit()
    models["M4_year"] = (m4, ["const", "log10_kerugian", "is_jpu", "is_jp", "year_centered"])

    # M5: + interaction
    interaction = log_k * is_jpu
    X5 = sm.add_constant(np.column_stack([log_k, is_jpu, is_jp, tahun_c, interaction]))
    m5 = sm.OLS(vonis, X5).fit()
    models["M5_interaction"] = (
        m5,
        ["const", "log10_kerugian", "is_jpu", "is_jp", "year_centered", "kerugian_x_jpu"],
    )

    return models, m1, m4


def run_quantile_regression(vonis, log_k, is_jpu, is_jp, tahun_c):
    """Fit median quantile regression."""
    import statsmodels.api as sm

    X = sm.add_constant(np.column_stack([log_k, is_jpu, is_jp, tahun_c]))
    qm = sm.QuantReg(vonis, X).fit(q=0.5)
    labels = ["const", "log10_kerugian", "is_jpu", "is_jp", "year_centered"]
    return {name: {"coef": float(qm.params[i]), "p": float(qm.pvalues[i])} for i, name in enumerate(labels)}


def run_cross_validation(vonis, log_k, is_jpu, is_jp, tahun_c):
    """10-fold cross-validation."""
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import cross_val_score

    X = np.column_stack([log_k, is_jpu, is_jp, tahun_c])
    lr = LinearRegression()
    r2_scores = cross_val_score(lr, X, vonis, cv=10, scoring="r2")
    mae_scores = -cross_val_score(lr, X, vonis, cv=10, scoring="neg_mean_absolute_error")
    return {
        "mean_r2": float(r2_scores.mean()),
        "std_r2": float(r2_scores.std()),
        "mean_mae": float(mae_scores.mean()),
        "std_mae": float(mae_scores.std()),
        "r2_folds": [float(s) for s in r2_scores],
    }


def residual_diagnostics(model):
    """Compute residual diagnostics."""
    import statsmodels.api as sm

    residuals = model.resid
    sw, sw_p = sp_stats.shapiro(residuals)
    jb, jb_p, skew, kurt = sm.stats.stattools.jarque_bera(residuals)
    dw = sm.stats.stattools.durbin_watson(residuals)
    return {
        "shapiro_w": float(sw),
        "shapiro_p": float(sw_p),
        "jarque_bera": float(jb),
        "jb_p": float(jb_p),
        "skew": float(skew),
        "kurtosis": float(kurt),
        "durbin_watson": float(dw),
    }


def generate_figures(vonis, log_k, is_jpu, is_jp, m1_model):
    """Generate regression diagnostic figures."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_dir = REPORTS_DIR / "figures"
        fig_dir.mkdir(exist_ok=True)

        # Fig 6: Scatter with regression line
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ["#e74c3c" if jp else "#3498db" for jp in is_jp]
        ax.scatter(log_k, vonis, c=colors, alpha=0.4, s=20)
        x_line = np.linspace(log_k.min(), log_k.max(), 100)
        y_line = m1_model.params[0] + m1_model.params[1] * x_line
        ax.plot(x_line, y_line, "k-", linewidth=2, label=f"OLS: R2={m1_model.rsquared:.3f}")
        ax.set_xlabel("log10(Kerugian Negara, Rp)")
        ax.set_ylabel("Vonis (years)")
        ax.set_title("Sentence vs State Loss (log scale)")
        ax.legend()

        # Custom legend
        from matplotlib.lines import Line2D

        legend_elements = [
            Line2D([0], [0], marker="o", color="w", markerfacecolor="#e74c3c", markersize=8, label="Jakarta Pusat"),
            Line2D([0], [0], marker="o", color="w", markerfacecolor="#3498db", markersize=8, label="Other regions"),
        ]
        ax.legend(handles=legend_elements + [Line2D([0], [0], color="k", linewidth=2, label=f"OLS: R2={m1_model.rsquared:.3f}")])
        plt.tight_layout()
        plt.savefig(fig_dir / "fig6_regression_scatter.png", dpi=150)
        plt.close()

        # Fig 7: Residual plot
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        residuals = m1_model.resid
        fitted = m1_model.fittedvalues

        axes[0].scatter(fitted, residuals, alpha=0.4, s=15)
        axes[0].axhline(y=0, color="r", linestyle="--")
        axes[0].set_xlabel("Fitted values (years)")
        axes[0].set_ylabel("Residuals (years)")
        axes[0].set_title("Residuals vs Fitted")

        sp_stats.probplot(residuals, plot=axes[1])
        axes[1].set_title("Q-Q Plot")

        plt.tight_layout()
        plt.savefig(fig_dir / "fig7_residual_diagnostics.png", dpi=150)
        plt.close()

        print(f"  Figures saved to {fig_dir}/")
        return True
    except ImportError:
        print("  matplotlib not available, skipping figures")
        return False


def main():
    print("=" * 60)
    print("Script 07: Multivariate Regression Analysis")
    print("=" * 60)

    # Load data
    vonis, log_k, is_jpu, is_jp, tahun_c, n = load_regression_data()
    print(f"\nRegression dataset: n={n}")
    print(f"  Vonis range: {vonis.min():.1f} - {vonis.max():.1f} years")
    print(f"  log10(kerugian) range: {log_k.min():.1f} - {log_k.max():.1f}")
    print(f"  JPU kasasi: {int(is_jpu.sum())} ({is_jpu.mean()*100:.1f}%)")
    print(f"  Jakarta Pusat: {int(is_jp.sum())} ({is_jp.mean()*100:.1f}%)")

    # OLS models
    print("\n--- Nested OLS Models ---")
    models, m1, m4 = run_ols_models(vonis, log_k, is_jpu, is_jp, tahun_c)

    print(f"\n{'Model':30s} {'R2':>8s} {'adj_R2':>8s} {'AIC':>10s} {'BIC':>10s}")
    for name, (model, _) in models.items():
        print(f"{name:30s} {model.rsquared:8.4f} {model.rsquared_adj:8.4f} {model.aic:10.1f} {model.bic:10.1f}")

    # Best model detail
    print("\n--- Model 4 Coefficients ---")
    m4_model, m4_labels = models["M4_year"]
    for i, name in enumerate(m4_labels):
        p = m4_model.pvalues[i]
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"  {name:20s}: b={m4_model.params[i]:8.3f} (SE={m4_model.bse[i]:.3f}), p={p:.4f} {sig}")

    # F-test M1 vs M4
    f_stat = ((m1.ssr - m4.ssr) / (m4.df_model - m1.df_model)) / (m4.ssr / m4.df_resid)
    f_p = 1 - sp_stats.f.cdf(f_stat, m4.df_model - m1.df_model, m4.df_resid)
    print(f"\n  F-test M1 vs M4: F={f_stat:.3f}, p={f_p:.4f}")
    print(f"  -> {'M1 sufficient (additional vars not significant)' if f_p > 0.05 else 'M4 significantly better'}")

    # Quantile regression
    print("\n--- Median Quantile Regression ---")
    qr_results = run_quantile_regression(vonis, log_k, is_jpu, is_jp, tahun_c)
    for name, vals in qr_results.items():
        print(f"  {name:20s}: b={vals['coef']:8.3f}, p={vals['p']:.4f}")

    # Cross-validation
    print("\n--- 10-Fold Cross-Validation ---")
    cv_results = run_cross_validation(vonis, log_k, is_jpu, is_jp, tahun_c)
    print(f"  Mean R2 = {cv_results['mean_r2']:.4f} +/- {cv_results['std_r2']:.4f}")
    print(f"  Mean MAE = {cv_results['mean_mae']:.3f} +/- {cv_results['std_mae']:.3f} years")

    # Diagnostics
    print("\n--- Residual Diagnostics (M4) ---")
    diag = residual_diagnostics(m4_model)
    print(f"  Shapiro-Wilk: W={diag['shapiro_w']:.4f}, p={diag['shapiro_p']:.6f}")
    print(f"  Jarque-Bera: JB={diag['jarque_bera']:.2f}, p={diag['jb_p']:.6f}")
    print(f"  Skew={diag['skew']:.3f}, Kurtosis={diag['kurtosis']:.3f}")
    print(f"  Durbin-Watson={diag['durbin_watson']:.3f}")

    # ===== PART B: TUNTUTAN MODELS =====
    print("\n" + "=" * 60)
    print("Part B: Tuntutan Models")
    print("=" * 60)

    rows_t, rows_all = load_tuntutan_data()
    print(f"\n  Tuntutan-only dataset: n={len(rows_t)}")
    print(f"  Tuntutan+kerugian dataset: n={len(rows_all)}")

    tunt_models = run_tuntutan_models(rows_t, rows_all)

    print(f"\n{'Model':30s} {'n':>5s} {'R2':>8s} {'adj_R2':>8s} {'AIC':>10s} {'BIC':>10s}")
    for name, (model, _, n_obs) in tunt_models.items():
        print(f"{name:30s} {n_obs:5d} {model.rsquared:8.4f} {model.rsquared_adj:8.4f} {model.aic:10.1f} {model.bic:10.1f}")

    # Detail for key tuntutan models
    for mname in ["M6_tuntutan_only", "M7_tuntutan_kerugian", "M8_tuntutan_full", "Md_discount"]:
        model, labels, n_obs = tunt_models[mname]
        print(f"\n--- {mname} (n={n_obs}) ---")
        for i, name in enumerate(labels):
            p = model.pvalues[i]
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            print(f"  {name:20s}: b={model.params[i]:8.3f} (SE={model.bse[i]:.3f}), p={p:.4f} {sig}")

    # ===== PART C: SENSITIVITY ANALYSES =====
    print("\n" + "=" * 60)
    print("Part C: Sensitivity & Robustness")
    print("=" * 60)

    sensitivity = run_sensitivity({})

    print("\n--- Outlier Sensitivity (M1: vonis ~ log10(kerugian)) ---")
    for label, vals in sensitivity["outlier"].items():
        print(f"  {label:20s}: n={vals['n']:3d}, slope={vals['slope']:.3f}, R2={vals['r2']:.4f}")

    print("\n--- Missing Data Comparison (vonis of cases with vs without kerugian) ---")
    md = sensitivity["missing_data"]
    print(f"  With kerugian:    n={md['with_kerugian']['n']}, mean={md['with_kerugian']['mean']:.2f}yr")
    print(f"  Without kerugian: n={md['without_kerugian']['n']}, mean={md['without_kerugian']['mean']:.2f}yr")
    print(f"  Welch's t={md['welch_t']:.3f}, p={md['p_value']:.4f}")
    print(f"  -> {md['interpretation']}")

    print("\n--- Power Analysis (pemohon kasasi null result) ---")
    pa = sensitivity["power_analysis"]["pemohon_kasasi"]
    print(f"  n_jpu={pa['n_jpu']}, n_terdakwa={pa['n_terdakwa']}")
    print(f"  Pooled SD = {pa['pooled_std']:.2f} years")
    print(f"  MDE at 80% power = {pa['mde_years']:.2f} years (d={pa['mde_cohens_d']:.3f})")
    print(f"  -> {pa['interpretation']}")

    # Figures
    print("\n--- Generating Figures ---")
    generate_figures(vonis, log_k, is_jpu, is_jp, models["M1_bivariate"][0])

    # ===== SAVE ALL RESULTS =====
    results = {
        "n_kerugian": n,
        "n_tuntutan": len(rows_t),
        "n_all_three": len(rows_all),
        "models": {},
        "quantile_median": qr_results,
        "cv_10fold": cv_results,
        "diagnostics": diag,
        "f_test_m1_vs_m4": {"f_stat": float(f_stat), "p": float(f_p)},
        "sensitivity": sensitivity,
    }

    # Kerugian models (M1-M5)
    for mname, (model, labels) in models.items():
        results["models"][mname] = {
            "r2": float(model.rsquared),
            "adj_r2": float(model.rsquared_adj),
            "aic": float(model.aic),
            "bic": float(model.bic),
            "f_stat": float(model.fvalue),
            "f_pvalue": float(model.f_pvalue),
            "n": n,
            "coefficients": {
                name: {
                    "coef": float(model.params[i]),
                    "se": float(model.bse[i]),
                    "p": float(model.pvalues[i]),
                    "ci_low": float(model.conf_int()[i][0]),
                    "ci_high": float(model.conf_int()[i][1]),
                }
                for i, name in enumerate(labels)
            },
        }

    # Tuntutan models (M6-M9, Md)
    for mname, (model, labels, n_obs) in tunt_models.items():
        results["models"][mname] = {
            "r2": float(model.rsquared),
            "adj_r2": float(model.rsquared_adj),
            "aic": float(model.aic),
            "bic": float(model.bic),
            "f_stat": float(model.fvalue),
            "f_pvalue": float(model.f_pvalue),
            "n": n_obs,
            "coefficients": {
                name: {
                    "coef": float(model.params[i]),
                    "se": float(model.bse[i]),
                    "p": float(model.pvalues[i]),
                    "ci_low": float(model.conf_int()[i][0]),
                    "ci_high": float(model.conf_int()[i][1]),
                }
                for i, name in enumerate(labels)
            },
        }

    out_path = REPORTS_DIR / "regression_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
