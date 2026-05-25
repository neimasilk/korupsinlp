"""Script 16: Prosecutorial Demand Analysis (Paper 4).

Research question: What drives prosecution demands in Indonesian corruption?
And: Does who appeals (prosecutor vs defendant) reveal systematic patterns?

Key insight: When the PROSECUTOR appeals to MA, they thought PN was too lenient.
When the DEFENDANT appeals, they thought PN was too harsh. This creates a
natural experiment about prosecutorial and judicial severity preferences.

Usage: python -m scripts.16_prosecutorial_analysis
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from autoresearch.prepare import load_corpus

SEED = 42
FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def text_lower(df):
    return df["pertimbangan_text"].fillna("").str.lower()


def print_section(title):
    print(f"\n\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def main():
    import sqlite3
    import statsmodels.api as sm
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Load full data with pemohon_kasasi
    conn = sqlite3.connect("data/korupsinlp.db")
    df = pd.read_sql_query("""
        SELECT id, vonis_bulan, tuntutan_bulan, kerugian_negara, pasal, daerah,
               tahun, pemohon_kasasi, pertimbangan_text
        FROM verdicts
        WHERE tuntutan_bulan IS NOT NULL AND tuntutan_bulan > 0
              AND vonis_bulan IS NOT NULL AND vonis_bulan > 0
    """, conn)
    conn.close()

    df["vonis_years"] = df["vonis_bulan"] / 12
    df["tuntutan_years"] = df["tuntutan_bulan"] / 12
    df["discount"] = df["vonis_years"] / df["tuntutan_years"]

    texts = df["pertimbangan_text"].fillna("").str.lower()
    df["has_p2"] = texts.str.contains(r"pasal\s+2\b", regex=True).astype(int)
    df["has_p3"] = texts.str.contains(r"pasal\s+3\b", regex=True).astype(int)
    df["has_kerugian"] = (df["kerugian_negara"] > 0).astype(int)
    df["log_kerugian"] = np.log1p(df["kerugian_negara"].fillna(0))
    df["log_tuntutan"] = np.log(df["tuntutan_years"])

    # Clean pemohon_kasasi
    df["appellant"] = df["pemohon_kasasi"].map({
        "penuntut_umum": "prosecutor",
        "terdakwa": "defendant"
    })

    n = len(df)
    print("=" * 70)
    print("  PAPER 4: PROSECUTORIAL DEMAND ANALYSIS")
    print(f"  Corpus: {n} verdicts with valid tuntutan + vonis")
    print("=" * 70)

    # ==================================================================
    #  1. WHAT PREDICTS PROSECUTION DEMAND?
    # ==================================================================
    print_section("1. DETERMINANTS OF PROSECUTION DEMAND (tuntutan)")

    # Focus: tuntutan as DV
    has_k = df[df["kerugian_negara"] > 0].copy()
    has_k["log_kerugian"] = np.log1p(has_k["kerugian_negara"])

    print(f"  n with kerugian data: {len(has_k)}")

    # Model 1: tuntutan ~ log(kerugian)
    X1 = sm.add_constant(has_k[["log_kerugian"]])
    m1 = sm.OLS(has_k["tuntutan_years"].values, X1).fit()
    print(f"\n  Model 1: tuntutan ~ log(kerugian_negara)")
    print(f"    R2 = {m1.rsquared:.4f}")
    print(f"    log_kerugian: b={m1.params['log_kerugian']:.4f}, p={m1.pvalues['log_kerugian']:.6f}")
    print(f"    Each 10x increase in kerugian -> +{m1.params['log_kerugian'] * np.log(10):.2f}yr tuntutan")

    # Model 2: + charge type
    X2 = sm.add_constant(has_k[["log_kerugian", "has_p2", "has_p3"]])
    m2 = sm.OLS(has_k["tuntutan_years"].values, X2).fit()
    print(f"\n  Model 2: tuntutan ~ log(kerugian) + P2 + P3")
    print(f"    R2 = {m2.rsquared:.4f}")
    for v in ["log_kerugian", "has_p2", "has_p3"]:
        print(f"    {v}: b={m2.params[v]:.4f}, p={m2.pvalues[v]:.6f}")

    # Model 3: + tahun (temporal trend)
    has_k["tahun_centered"] = has_k["tahun"] - has_k["tahun"].median()
    X3 = sm.add_constant(has_k[["log_kerugian", "has_p2", "has_p3", "tahun_centered"]])
    m3 = sm.OLS(has_k["tuntutan_years"].values, X3).fit()
    print(f"\n  Model 3: + tahun")
    print(f"    R2 = {m3.rsquared:.4f}")
    print(f"    tahun: b={m3.params['tahun_centered']:.4f}, p={m3.pvalues['tahun_centered']:.6f}")
    if m3.pvalues["tahun_centered"] < 0.05:
        direction = "INCREASING" if m3.params["tahun_centered"] > 0 else "DECREASING"
        print(f"    Prosecution demands are {direction} over time")
    else:
        print(f"    No significant temporal trend in prosecution demands")

    # ==================================================================
    #  2. KERUGIAN-TUNTUTAN PROPORTIONALITY
    # ==================================================================
    print_section("2. KERUGIAN-TUNTUTAN PROPORTIONALITY")

    print(f"  Is prosecution demand proportional to state financial loss?")
    print(f"")

    # Log-log model
    has_k2 = has_k[has_k["tuntutan_years"] > 0].copy()
    has_k2["log_tuntutan"] = np.log(has_k2["tuntutan_years"])
    has_k2["log_k"] = np.log(has_k2["kerugian_negara"])

    X_ll = sm.add_constant(has_k2[["log_k"]])
    m_ll = sm.OLS(has_k2["log_tuntutan"].values, X_ll).fit()

    print(f"  Log-log model: log(tuntutan) ~ log(kerugian)")
    print(f"    R2 = {m_ll.rsquared:.4f}")
    print(f"    Elasticity = {m_ll.params['log_k']:.4f}")
    print(f"")
    if m_ll.params["log_k"] < 0.5:
        print(f"    FINDING: Elasticity = {m_ll.params['log_k']:.3f} << 1.0")
        print(f"    Prosecution demands are HIGHLY INELASTIC to state loss.")
        print(f"    A 100x larger corruption case gets only ~{100**m_ll.params['log_k']:.1f}x longer demand.")
        print(f"    This is a MAJOR finding: proportionality is broken.")
    elif m_ll.params["log_k"] < 1:
        print(f"    Demands increase sub-linearly with loss (compression).")
    else:
        print(f"    Demands are proportional or super-proportional to loss.")

    # Quantify: what does a 10M vs 10B case look like?
    pred_10m = np.exp(m_ll.params["const"] + m_ll.params["log_k"] * np.log(10e6))
    pred_1b = np.exp(m_ll.params["const"] + m_ll.params["log_k"] * np.log(1e9))
    pred_100b = np.exp(m_ll.params["const"] + m_ll.params["log_k"] * np.log(100e9))
    print(f"\n  Predicted tuntutan by kerugian magnitude:")
    print(f"    Rp 10 juta (petty):      {pred_10m:.1f} years")
    print(f"    Rp 1 miliar (medium):    {pred_1b:.1f} years")
    print(f"    Rp 100 miliar (mega):    {pred_100b:.1f} years")
    print(f"    Ratio mega/petty:        {pred_100b/pred_10m:.1f}x")
    print(f"    If proportional, should be: {100e9/10e6:.0f}x")

    # ==================================================================
    #  3. WHO APPEALS AND WHY IT MATTERS
    # ==================================================================
    print_section("3. WHO APPEALS? PROSECUTOR vs DEFENDANT")

    app = df[df["appellant"].notna()].copy()
    print(f"  Total with appellant data: {len(app)}")

    for label in ["prosecutor", "defendant"]:
        sub = app[app["appellant"] == label]
        print(f"\n  {label.upper()} appeals (n={len(sub)}):")
        print(f"    Mean tuntutan: {sub['tuntutan_years'].mean():.2f} yr")
        print(f"    Mean vonis:    {sub['vonis_years'].mean():.2f} yr")
        print(f"    Mean discount: {sub['discount'].mean():.3f}")
        print(f"    % Pasal 2:     {100*sub['has_p2'].mean():.1f}%")
        k_sub = sub[sub["kerugian_negara"] > 0]
        if len(k_sub) > 0:
            print(f"    Median kerugian: Rp {k_sub['kerugian_negara'].median():,.0f}")

    # Statistical comparison
    pros = app[app["appellant"] == "prosecutor"]
    defe = app[app["appellant"] == "defendant"]

    t_tunt, p_tunt = stats.mannwhitneyu(pros["tuntutan_years"], defe["tuntutan_years"])
    t_vonis, p_vonis = stats.mannwhitneyu(pros["vonis_years"], defe["vonis_years"])
    t_disc, p_disc = stats.mannwhitneyu(pros["discount"], defe["discount"])

    print(f"\n  Mann-Whitney U tests (prosecutor vs defendant appeals):")
    print(f"    Tuntutan:  p={p_tunt:.6f} {'***' if p_tunt < 0.001 else ''}")
    print(f"    Vonis:     p={p_vonis:.6f} {'***' if p_vonis < 0.001 else ''}")
    print(f"    Discount:  p={p_disc:.6f} {'***' if p_disc < 0.001 else ''}")

    # ==================================================================
    #  4. PROSECUTORIAL SEVERITY BY REGION
    # ==================================================================
    print_section("4. GEOGRAPHIC VARIATION IN PROSECUTION DEMANDS")

    # Province-level prosecution demand patterns
    daerah_map = {
        "Jakarta Pusat": "DKI Jakarta", "PN JAKARTA PUSAT": "DKI Jakarta",
        "PT JAKARTA": "DKI Jakarta",
        "Surabaya": "Jawa Timur", "PN SURABAYA": "Jawa Timur",
        "Bandung": "Jawa Barat", "PN BANDUNG": "Jawa Barat",
        "Semarang": "Jawa Tengah", "PN SEMARANG": "Jawa Tengah",
        "Makassar": "Sulawesi Selatan", "PN MAKASSAR": "Sulawesi Selatan",
        "Medan": "Sumatera Utara", "PN MEDAN": "Sumatera Utara",
        "Kupang": "Nusa Tenggara Timur",
        "Banda Aceh": "Aceh",
        "Padang": "Sumatera Barat",
        "Samarinda": "Kalimantan Timur",
        "Pekanbaru": "Riau",
        "Mataram": "Nusa Tenggara Barat",
        "Palembang": "Sumatera Selatan",
        "Bengkulu": "Bengkulu",
        "Palu": "Sulawesi Tengah",
        "Kendari": "Sulawesi Tenggara",
    }
    df["province"] = df["daerah"].map(daerah_map)
    prov_data = df[df["province"].notna()].copy()

    prov_stats = prov_data.groupby("province").agg(
        n=("id", "count"),
        mean_tuntutan=("tuntutan_years", "mean"),
        mean_vonis=("vonis_years", "mean"),
        mean_discount=("discount", "mean"),
        pct_p2=("has_p2", "mean"),
    ).query("n >= 5").sort_values("mean_tuntutan", ascending=False)

    print(f"  Provinces with >= 5 cases (n={len(prov_stats)}):")
    print(f"  {'Province':<25s} {'n':>4s} {'Tuntutan':>9s} {'Vonis':>7s} {'Discount':>9s} {'%P2':>5s}")
    print(f"  {'-'*63}")
    for prov, row in prov_stats.iterrows():
        print(f"  {prov:<25s} {row['n']:>4.0f} {row['mean_tuntutan']:>8.1f}yr "
              f"{row['mean_vonis']:>6.1f}yr {row['mean_discount']:>9.3f} {100*row['pct_p2']:>4.0f}%")

    # Kruskal-Wallis on tuntutan by province
    groups = [g["tuntutan_years"].values for _, g in prov_data.groupby("province") if len(g) >= 5]
    if len(groups) >= 3:
        h, p = stats.kruskal(*groups)
        print(f"\n  Kruskal-Wallis (tuntutan by province): H={h:.1f}, p={p:.6f}")
        if p < 0.05:
            print(f"  SIGNIFICANT: prosecutors demand differently across regions")
        else:
            print(f"  Not significant: prosecution demands are geographically uniform")

    # After controlling for kerugian
    print(f"\n  Controlling for kerugian (residual tuntutan by province):")
    prov_k = prov_data[prov_data["kerugian_negara"] > 0].copy()
    prov_k["log_k"] = np.log1p(prov_k["kerugian_negara"])
    X_k = sm.add_constant(prov_k[["log_k"]])
    m_k = sm.OLS(prov_k["tuntutan_years"].values, X_k).fit()
    prov_k["tuntutan_resid"] = m_k.resid

    groups_resid = [g["tuntutan_resid"].values for _, g in prov_k.groupby("province") if len(g) >= 5]
    if len(groups_resid) >= 3:
        h2, p2 = stats.kruskal(*groups_resid)
        print(f"  Kruskal-Wallis (residual tuntutan): H={h2:.1f}, p={p2:.6f}")
        if p2 < 0.05:
            print(f"  REMAINS significant after controlling for loss magnitude")
            print(f"  Prosecutors in different regions demand differently for SAME loss")
        else:
            print(f"  Disappears: geographic variation is a composition effect (like Paper 2)")

    # ==================================================================
    #  5. TEMPORAL TRENDS IN PROSECUTION
    # ==================================================================
    print_section("5. TEMPORAL TRENDS IN PROSECUTION SEVERITY")

    year_stats = df.groupby("tahun").agg(
        n=("id", "count"),
        mean_tuntutan=("tuntutan_years", "mean"),
        mean_vonis=("vonis_years", "mean"),
        mean_discount=("discount", "mean"),
    ).query("n >= 5")

    print(f"  {'Year':>5s} {'n':>4s} {'Tuntutan':>9s} {'Vonis':>7s} {'Discount':>9s}")
    print(f"  {'-'*38}")
    for yr, row in year_stats.iterrows():
        print(f"  {yr:>5d} {row['n']:>4.0f} {row['mean_tuntutan']:>8.2f}yr "
              f"{row['mean_vonis']:>6.2f}yr {row['mean_discount']:>9.3f}")

    # Spearman trend
    rho_tunt, p_rho = stats.spearmanr(year_stats.index, year_stats["mean_tuntutan"])
    print(f"\n  Temporal trend (tuntutan): Spearman rho={rho_tunt:.3f}, p={p_rho:.4f}")

    rho_disc, p_disc2 = stats.spearmanr(year_stats.index, year_stats["mean_discount"])
    print(f"  Temporal trend (discount): Spearman rho={rho_disc:.3f}, p={p_disc2:.4f}")

    # ==================================================================
    #  6. THE APPEAL SELECTION MODEL
    # ==================================================================
    print_section("6. APPEAL SELECTION: Who Appeals and What Happens?")

    app2 = app.copy()
    app2["is_prosecutor_appeal"] = (app2["appellant"] == "prosecutor").astype(int)

    # What predicts who appeals?
    X_appeal = sm.add_constant(app2[["tuntutan_years", "has_p2", "discount"]])
    m_appeal = sm.Logit(app2["is_prosecutor_appeal"].values, X_appeal).fit(disp=0)

    print(f"  Logistic: P(prosecutor appeals) ~ tuntutan + P2 + discount")
    print(f"  Pseudo R2 = {m_appeal.prsquared:.4f}")
    for v in ["tuntutan_years", "has_p2", "discount"]:
        or_v = np.exp(m_appeal.params[v])
        print(f"    {v}: OR={or_v:.3f}, p={m_appeal.pvalues[v]:.4f}")

    print(f"\n  Interpretation:")
    if m_appeal.pvalues["discount"] < 0.05:
        if m_appeal.params["discount"] < 0:
            print(f"  Prosecutors are MORE likely to appeal when discount is LOW")
            print(f"  (i.e., when PN gave a sentence much lower than demanded)")
        else:
            print(f"  Prosecutors are MORE likely to appeal when discount is HIGH")

    # ==================================================================
    #  7. KEY FINDINGS SUMMARY
    # ==================================================================
    print_section("7. KEY FINDINGS FOR PAPER 4")

    print(f"  1. KERUGIAN-TUNTUTAN ELASTICITY: {m_ll.params['log_k']:.3f}")
    if m_ll.params["log_k"] < 0.5:
        print(f"     Prosecution demands are highly inelastic to loss magnitude.")
        print(f"     A Rp 100B case gets only ~{pred_100b/pred_10m:.1f}x the demand of a Rp 10M case")
        print(f"     (should be 10,000x if proportional)")
    print(f"")
    print(f"  2. WHO APPEALS: {len(pros)} prosecutor vs {len(defe)} defendant appeals")
    print(f"     Prosecutor appeals: mean tuntutan {pros['tuntutan_years'].mean():.1f}yr, discount {pros['discount'].mean():.3f}")
    print(f"     Defendant appeals:  mean tuntutan {defe['tuntutan_years'].mean():.1f}yr, discount {defe['discount'].mean():.3f}")
    print(f"")
    print(f"  3. R2 of tuntutan model (with kerugian + charge): {m2.rsquared:.3f}")
    print(f"     vs R2 of vonis model (Paper 2): 0.600")
    print(f"     Tuntutan is {'MORE' if m2.rsquared > 0.6 else 'LESS'} predictable than vonis")

    # ==================================================================
    #  8. PUBLICATION FIGURES
    # ==================================================================
    print_section("8. GENERATING PAPER 4 FIGURES")

    plt.rcParams.update({
        "font.size": 11, "axes.titlesize": 13,
        "axes.labelsize": 12, "figure.dpi": 150,
        "savefig.dpi": 300, "savefig.bbox": "tight",
    })

    # Figure 7: Kerugian vs Tuntutan (log-log) with proportionality line
    fig, ax = plt.subplots(figsize=(8, 6))
    k_plot = has_k2[has_k2["kerugian_negara"] > 1000].copy()  # exclude noise
    ax.scatter(k_plot["kerugian_negara"], k_plot["tuntutan_years"],
               alpha=0.3, s=20, c="steelblue")
    ax.set_xscale("log")
    ax.set_yscale("log")

    # Fit line
    x_range = np.logspace(6, 14, 100)
    y_pred = np.exp(m_ll.params["const"] + m_ll.params["log_k"] * np.log(x_range))
    ax.plot(x_range, y_pred, "r-", linewidth=2,
            label=f"Fit: elasticity={m_ll.params['log_k']:.3f}")

    ax.set_xlabel("State Financial Loss (Kerugian Negara, IDR)")
    ax.set_ylabel("Prosecution Demand (Tuntutan, years)")
    ax.set_title("Prosecution Demand vs State Loss: Broken Proportionality")
    ax.legend()

    # Format x-axis
    ax.set_xlim(1e6, 1e14)
    fig.savefig(FIG_DIR / "fig7_kerugian_tuntutan.png")
    plt.close()
    print(f"  Saved: {FIG_DIR / 'fig7_kerugian_tuntutan.png'}")

    # Figure 8: Prosecutor vs Defendant appeals
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A: Distribution of discount by appellant
    for label, color in [("prosecutor", "crimson"), ("defendant", "steelblue")]:
        sub = app[app["appellant"] == label]
        ax1.hist(sub["discount"], bins=30, alpha=0.5, color=color,
                 label=f'{label.title()} (n={len(sub)})', density=True)
    ax1.axvline(1.0, color="black", linestyle="--", alpha=0.5)
    ax1.set_xlabel("Sentencing Discount (vonis/tuntutan)")
    ax1.set_ylabel("Density")
    ax1.set_title("(a) Discount Distribution by Appellant")
    ax1.legend()

    # Panel B: Tuntutan distribution
    for label, color in [("prosecutor", "crimson"), ("defendant", "steelblue")]:
        sub = app[app["appellant"] == label]
        ax2.hist(sub["tuntutan_years"], bins=20, alpha=0.5, color=color,
                 label=f'{label.title()} (n={len(sub)})', density=True)
    ax2.set_xlabel("Prosecution Demand (years)")
    ax2.set_ylabel("Density")
    ax2.set_title("(b) Demand Distribution by Appellant")
    ax2.legend()

    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig8_appeal_patterns.png")
    plt.close()
    print(f"  Saved: {FIG_DIR / 'fig8_appeal_patterns.png'}")

    print(f"\n  Paper 4 analysis complete.")
    print(f"  NOVELTY: Nobody has analyzed prosecutorial demand determinants")
    print(f"  in Indonesian corruption, nor the appeal selection mechanism.")


if __name__ == "__main__":
    main()
