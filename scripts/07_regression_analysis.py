"""Script 07: Multivariate regression analysis for Paper 2.

Fits nested OLS models: vonis ~ log10(kerugian) + pemohon_kasasi + jakarta_pusat + year.
Runs quantile regression, 10-fold CV, and residual diagnostics.
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

    # Figures
    print("\n--- Generating Figures ---")
    generate_figures(vonis, log_k, is_jp, is_jp, models["M1_bivariate"][0])

    # Save results
    results = {
        "n": n,
        "models": {},
        "quantile_median": qr_results,
        "cv_10fold": cv_results,
        "diagnostics": diag,
        "f_test_m1_vs_m4": {"f_stat": float(f_stat), "p": float(f_p)},
    }

    for mname, (model, labels) in models.items():
        results["models"][mname] = {
            "r2": float(model.rsquared),
            "adj_r2": float(model.rsquared_adj),
            "aic": float(model.aic),
            "bic": float(model.bic),
            "f_stat": float(model.fvalue),
            "f_pvalue": float(model.f_pvalue),
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
