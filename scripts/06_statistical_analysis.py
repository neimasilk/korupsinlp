"""Script 06: Statistical analysis for Paper 1.

Runs Welch's t-test on pemohon_kasasi groups, computes kerugian-vonis
correlation, descriptive stats, and generates figures.

Usage: python -m scripts.06_statistical_analysis
"""

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sqlite3
import numpy as np
from scipy import stats as sp_stats

from src.config import DB_PATH, REPORTS_DIR


def load_data():
    """Load parsed verdicts from DB."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT vonis_bulan, tuntutan_bulan, kerugian_negara, daerah, tahun,
               pemohon_kasasi, nama_terdakwa, pasal, nama_hakim,
               case_number, pdf_path
        FROM verdicts
        WHERE vonis_bulan IS NOT NULL AND vonis_bulan > 0
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def descriptive_stats(data):
    """Compute descriptive statistics for sentencing."""
    vonis_months = [r["vonis_bulan"] for r in data]
    vonis_years = [v / 12 for v in vonis_months]

    tuntutan = [r["tuntutan_bulan"] for r in data if r["tuntutan_bulan"] and r["tuntutan_bulan"] > 0]
    tuntutan_years = [t / 12 for t in tuntutan]

    # Discount ratio (vonis/tuntutan)
    ratios = []
    for r in data:
        if r["tuntutan_bulan"] and r["tuntutan_bulan"] > 0:
            ratios.append(r["vonis_bulan"] / r["tuntutan_bulan"])

    # Kerugian
    kerugian = [r["kerugian_negara"] for r in data if r["kerugian_negara"] and r["kerugian_negara"] > 0]

    print("=" * 60)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 60)

    print(f"\n--- Vonis (n={len(vonis_years)}) ---")
    print(f"  Mean:   {np.mean(vonis_years):.2f} years ({np.mean(vonis_months):.1f} months)")
    print(f"  Median: {np.median(vonis_years):.2f} years ({np.median(vonis_months):.1f} months)")
    print(f"  Std:    {np.std(vonis_years, ddof=1):.2f} years")
    print(f"  Min:    {np.min(vonis_years):.2f} years")
    print(f"  Max:    {np.max(vonis_years):.2f} years")
    print(f"  IQR:    {np.percentile(vonis_years, 25):.2f} - {np.percentile(vonis_years, 75):.2f} years")

    if tuntutan_years:
        print(f"\n--- Tuntutan (n={len(tuntutan_years)}) ---")
        print(f"  Mean:   {np.mean(tuntutan_years):.2f} years")
        print(f"  Median: {np.median(tuntutan_years):.2f} years")

    if ratios:
        print(f"\n--- Discount Ratio vonis/tuntutan (n={len(ratios)}) ---")
        print(f"  Mean:   {np.mean(ratios)*100:.1f}%")
        print(f"  Median: {np.median(ratios)*100:.1f}%")
        print(f"  Cases vonis > tuntutan: {sum(1 for r in ratios if r > 1)} ({sum(1 for r in ratios if r > 1)/len(ratios)*100:.1f}%)")

    if kerugian:
        print(f"\n--- Kerugian Negara (n={len(kerugian)}) ---")
        print(f"  Median: Rp {np.median(kerugian):,.0f}")
        print(f"  Min:    Rp {np.min(kerugian):,.0f}")
        print(f"  Max:    Rp {np.max(kerugian):,.0f}")

    return {
        "n_vonis": len(vonis_years),
        "mean_vonis_yr": np.mean(vonis_years),
        "median_vonis_yr": np.median(vonis_years),
        "std_vonis_yr": np.std(vonis_years, ddof=1),
        "mean_tuntutan_yr": np.mean(tuntutan_years) if tuntutan_years else None,
        "mean_ratio": np.mean(ratios) if ratios else None,
        "median_ratio": np.median(ratios) if ratios else None,
        "n_ratio": len(ratios),
        "n_kerugian": len(kerugian),
        "median_kerugian": np.median(kerugian) if kerugian else None,
    }


def pemohon_kasasi_analysis(data):
    """Welch's t-test comparing JPU vs Terdakwa kasasi sentencing."""
    jpu = [r["vonis_bulan"] / 12 for r in data if r["pemohon_kasasi"] == "penuntut_umum"]
    terdakwa = [r["vonis_bulan"] / 12 for r in data if r["pemohon_kasasi"] == "terdakwa"]
    unknown = [r for r in data if r["pemohon_kasasi"] not in ("penuntut_umum", "terdakwa")]

    print("\n" + "=" * 60)
    print("PEMOHON KASASI ANALYSIS")
    print("=" * 60)

    print(f"\n  JPU (penuntut_umum): n={len(jpu)}, mean={np.mean(jpu):.2f}yr, std={np.std(jpu, ddof=1):.2f}")
    print(f"  Terdakwa:           n={len(terdakwa)}, mean={np.mean(terdakwa):.2f}yr, std={np.std(terdakwa, ddof=1):.2f}")
    print(f"  Unknown/missing:    n={len(unknown)}")

    if len(jpu) >= 2 and len(terdakwa) >= 2:
        t_stat, p_value = sp_stats.ttest_ind(jpu, terdakwa, equal_var=False)
        cohens_d = (np.mean(jpu) - np.mean(terdakwa)) / math.sqrt(
            (np.std(jpu, ddof=1) ** 2 + np.std(terdakwa, ddof=1) ** 2) / 2
        )
        print(f"\n  Welch's t-test:")
        print(f"    t = {t_stat:.3f}")
        print(f"    p = {p_value:.4f}")
        print(f"    Cohen's d = {cohens_d:.3f}")
        print(f"    Significant at alpha=0.05? {'YES' if p_value < 0.05 else 'NO'}")

        # Also test discount ratios
        jpu_ratios = [r["vonis_bulan"] / r["tuntutan_bulan"]
                      for r in data
                      if r["pemohon_kasasi"] == "penuntut_umum"
                      and r["tuntutan_bulan"] and r["tuntutan_bulan"] > 0]
        terd_ratios = [r["vonis_bulan"] / r["tuntutan_bulan"]
                       for r in data
                       if r["pemohon_kasasi"] == "terdakwa"
                       and r["tuntutan_bulan"] and r["tuntutan_bulan"] > 0]

        if len(jpu_ratios) >= 2 and len(terd_ratios) >= 2:
            t2, p2 = sp_stats.ttest_ind(jpu_ratios, terd_ratios, equal_var=False)
            print(f"\n  Discount ratio (vonis/tuntutan) by pemohon:")
            print(f"    JPU mean ratio:      {np.mean(jpu_ratios)*100:.1f}% (n={len(jpu_ratios)})")
            print(f"    Terdakwa mean ratio: {np.mean(terd_ratios)*100:.1f}% (n={len(terd_ratios)})")
            print(f"    Welch's t = {t2:.3f}, p = {p2:.4f}")

        # Mann-Whitney U as non-parametric alternative
        u_stat, u_p = sp_stats.mannwhitneyu(jpu, terdakwa, alternative='two-sided')
        print(f"\n  Mann-Whitney U (non-parametric):")
        print(f"    U = {u_stat:.1f}, p = {u_p:.4f}")

        return {
            "n_jpu": len(jpu), "mean_jpu": np.mean(jpu),
            "n_terdakwa": len(terdakwa), "mean_terdakwa": np.mean(terdakwa),
            "t_stat": t_stat, "p_value": p_value, "cohens_d": cohens_d,
            "u_stat": u_stat, "u_p": u_p,
        }
    else:
        print("  Insufficient data for t-test")
        return None


def kerugian_bracket_analysis(data):
    """Analyze sentencing by kerugian negara brackets."""
    brackets = [
        ("<100M", 0, 1e8),
        ("100M-1B", 1e8, 1e9),
        ("1B-10B", 1e9, 1e10),
        ("10B-100B", 1e10, 1e11),
        (">100B", 1e11, float("inf")),
    ]

    print("\n" + "=" * 60)
    print("KERUGIAN-VONIS BRACKET ANALYSIS")
    print("=" * 60)

    bracket_data = []
    all_log_k = []
    all_vonis = []

    for label, lo, hi in brackets:
        group = [r for r in data
                 if r["kerugian_negara"] and lo <= r["kerugian_negara"] < hi
                 and r["vonis_bulan"] and r["vonis_bulan"] > 0]
        if group:
            vonis_yr = [r["vonis_bulan"] / 12 for r in group]
            mean_v = np.mean(vonis_yr)
            median_v = np.median(vonis_yr)
            print(f"  {label:>10s}: n={len(group):3d}, mean={mean_v:.2f}yr, median={median_v:.2f}yr")
            bracket_data.append({"label": label, "n": len(group), "mean": mean_v, "median": median_v})

            for r in group:
                all_log_k.append(math.log10(r["kerugian_negara"]))
                all_vonis.append(r["vonis_bulan"] / 12)

    # Spearman correlation (log_kerugian vs vonis)
    if len(all_log_k) >= 3:
        rho, p_rho = sp_stats.spearmanr(all_log_k, all_vonis)
        r_pearson, p_pearson = sp_stats.pearsonr(all_log_k, all_vonis)
        print(f"\n  Spearman rho (log10_kerugian ~ vonis): {rho:.3f}, p={p_rho:.4e}")
        print(f"  Pearson r   (log10_kerugian ~ vonis): {r_pearson:.3f}, p={p_pearson:.4e}")

        # Linear regression: vonis_yr = a * log10(kerugian) + b
        slope, intercept, r_val, p_reg, se = sp_stats.linregress(all_log_k, all_vonis)
        print(f"  Linear model: vonis = {slope:.2f} * log10(kerugian) + ({intercept:.2f})")
        print(f"  R-squared: {r_val**2:.3f}")
        return {
            "brackets": bracket_data,
            "spearman_rho": rho, "spearman_p": p_rho,
            "pearson_r": r_pearson, "pearson_p": p_pearson,
            "slope": slope, "intercept": intercept, "r_squared": r_val**2,
        }

    return {"brackets": bracket_data}


def geographic_analysis(data):
    """Top regions by case count."""
    from collections import Counter
    regions = Counter(r["daerah"] for r in data if r["daerah"])

    print("\n" + "=" * 60)
    print("GEOGRAPHIC DISTRIBUTION (top 15)")
    print("=" * 60)

    for region, count in regions.most_common(15):
        group_vonis = [r["vonis_bulan"] / 12 for r in data if r["daerah"] == region]
        mean_v = np.mean(group_vonis) if group_vonis else 0
        print(f"  {region:25s}: n={count:3d}, mean vonis={mean_v:.2f}yr")

    return dict(regions.most_common(20))


def temporal_analysis(data):
    """Cases by year with sentencing trends."""
    from collections import Counter
    years = Counter(r["tahun"] for r in data if r["tahun"])

    print("\n" + "=" * 60)
    print("TEMPORAL DISTRIBUTION")
    print("=" * 60)

    for year in sorted(years.keys()):
        group = [r["vonis_bulan"] / 12 for r in data if r["tahun"] == year]
        mean_v = np.mean(group) if group else 0
        print(f"  {year}: n={years[year]:3d}, mean vonis={mean_v:.2f}yr")

    return dict(sorted(years.items()))


def generate_figures(data):
    """Generate matplotlib figures for Paper 1."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n[!] matplotlib not installed — skipping figures")
        return

    fig_dir = REPORTS_DIR / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    vonis_yr = [r["vonis_bulan"] / 12 for r in data]
    ratios = [r["vonis_bulan"] / r["tuntutan_bulan"]
              for r in data if r["tuntutan_bulan"] and r["tuntutan_bulan"] > 0]

    # Figure 1: Vonis distribution histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vonis_yr, bins=30, edgecolor="black", alpha=0.7, color="#2196F3")
    ax.axvline(np.mean(vonis_yr), color="red", linestyle="--", label=f"Mean: {np.mean(vonis_yr):.1f}yr")
    ax.axvline(np.median(vonis_yr), color="orange", linestyle="--", label=f"Median: {np.median(vonis_yr):.1f}yr")
    ax.set_xlabel("Prison Sentence (years)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Corruption Sentences (MA Kasasi)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "fig1_vonis_distribution.png", dpi=150)
    plt.close()
    print(f"  Saved fig1_vonis_distribution.png")

    # Figure 2: Discount ratio distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist([r * 100 for r in ratios], bins=30, edgecolor="black", alpha=0.7, color="#4CAF50")
    ax.axvline(np.mean(ratios) * 100, color="red", linestyle="--", label=f"Mean: {np.mean(ratios)*100:.1f}%")
    ax.axvline(100, color="black", linestyle=":", label="vonis = tuntutan")
    ax.set_xlabel("Discount Ratio (vonis/tuntutan, %)")
    ax.set_ylabel("Count")
    ax.set_title("Sentencing Discount Distribution")
    ax.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / "fig2_discount_ratio.png", dpi=150)
    plt.close()
    print(f"  Saved fig2_discount_ratio.png")

    # Figure 3: Kerugian vs Vonis scatter (log scale)
    k_data = [(r["kerugian_negara"], r["vonis_bulan"] / 12) for r in data
              if r["kerugian_negara"] and r["kerugian_negara"] > 0]
    if k_data:
        k_vals, v_vals = zip(*k_data)
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ["#F44336" if r.get("pemohon_kasasi") == "penuntut_umum" else "#2196F3"
                  for r in data if r["kerugian_negara"] and r["kerugian_negara"] > 0]
        ax.scatter(k_vals, v_vals, alpha=0.5, c=colors, s=30)
        ax.set_xscale("log")
        ax.set_xlabel("State Financial Loss (Rp, log scale)")
        ax.set_ylabel("Prison Sentence (years)")
        ax.set_title("State Loss vs Sentence Severity")
        # Legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#F44336', markersize=8, label='JPU kasasi'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#2196F3', markersize=8, label='Terdakwa kasasi'),
        ]
        ax.legend(handles=legend_elements)
        plt.tight_layout()
        plt.savefig(fig_dir / "fig3_kerugian_vonis.png", dpi=150)
        plt.close()
        print(f"  Saved fig3_kerugian_vonis.png")

    # Figure 4: Pemohon kasasi comparison boxplot
    jpu_v = [r["vonis_bulan"] / 12 for r in data if r["pemohon_kasasi"] == "penuntut_umum"]
    terd_v = [r["vonis_bulan"] / 12 for r in data if r["pemohon_kasasi"] == "terdakwa"]
    if jpu_v and terd_v:
        fig, ax = plt.subplots(figsize=(6, 5))
        bp = ax.boxplot([jpu_v, terd_v], tick_labels=["JPU kasasi\n(prosecutor)", "Terdakwa kasasi\n(defendant)"],
                        patch_artist=True)
        bp["boxes"][0].set_facecolor("#F44336")
        bp["boxes"][1].set_facecolor("#2196F3")
        for box in bp["boxes"]:
            box.set_alpha(0.6)
        ax.set_ylabel("Prison Sentence (years)")
        ax.set_title("Sentences by Appeal Filer")
        plt.tight_layout()
        plt.savefig(fig_dir / "fig4_pemohon_kasasi_boxplot.png", dpi=150)
        plt.close()
        print(f"  Saved fig4_pemohon_kasasi_boxplot.png")

    # Figure 5: Temporal distribution
    from collections import Counter
    years = Counter(r["tahun"] for r in data if r["tahun"])
    if years:
        sorted_years = sorted(years.items())
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar([str(y) for y, _ in sorted_years], [c for _, c in sorted_years],
               color="#FF9800", edgecolor="black", alpha=0.7)
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Verdicts")
        ax.set_title("Temporal Distribution of MA Corruption Verdicts")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(fig_dir / "fig5_temporal.png", dpi=150)
        plt.close()
        print(f"  Saved fig5_temporal.png")


def main():
    data = load_data()
    print(f"Loaded {len(data)} verdicts with vonis > 0")

    desc = descriptive_stats(data)
    pk_result = pemohon_kasasi_analysis(data)
    kerugian_result = kerugian_bracket_analysis(data)
    geo = geographic_analysis(data)
    temporal = temporal_analysis(data)

    print("\n" + "=" * 60)
    print("GENERATING FIGURES")
    print("=" * 60)
    generate_figures(data)

    # Save summary JSON
    summary = {
        "n": len(data),
        "descriptive": desc,
        "pemohon_kasasi": pk_result,
        "kerugian": kerugian_result,
        "geographic_top10": dict(list(geo.items())[:10]),
    }
    summary_path = REPORTS_DIR / "analysis_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"\nSummary saved to {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
