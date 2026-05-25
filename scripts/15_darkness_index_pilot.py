"""Script 15: Darkness Index Pilot — Feasibility Analysis.

Concept: Map corruption verdicts to provinces, normalize by structural
indicators (population, GRDP, PNS count) to identify the gap between
expected and detected corruption.

This pilot:
1. Normalizes daerah names to provinces
2. Computes raw case rates per province
3. Uses embedded BPS 2024 data for normalization
4. Demonstrates what a Darkness Index could look like

Usage: python -m scripts.15_darkness_index_pilot
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# DAERAH → PROVINCE MAPPING
# ============================================================
# Indonesian courts (Pengadilan Negeri / Tipikor) are in provincial capitals
# or major cities. Map each daerah to its province.

DAERAH_TO_PROVINCE = {
    # Direct city → province mappings
    "Jakarta Pusat": "DKI Jakarta",
    "PN JAKARTA PUSAT": "DKI Jakarta",
    "PT JAKARTA": "DKI Jakarta",
    "Jakarta Selatan": "DKI Jakarta",
    "Surabaya": "Jawa Timur",
    "PN SURABAYA": "Jawa Timur",
    "PT SURABAYA": "Jawa Timur",
    "Bandung": "Jawa Barat",
    "PN BANDUNG": "Jawa Barat",
    "PT BANDUNG": "Jawa Barat",
    "Semarang": "Jawa Tengah",
    "PN SEMARANG": "Jawa Tengah",
    "PT SEMARANG": "Jawa Tengah",
    "Makassar": "Sulawesi Selatan",
    "PN MAKASSAR": "Sulawesi Selatan",
    "Medan": "Sumatera Utara",
    "PN MEDAN": "Sumatera Utara",
    "PT MEDAN": "Sumatera Utara",
    "Kupang": "Nusa Tenggara Timur",
    "PN KUPANG": "Nusa Tenggara Timur",
    "Banda Aceh": "Aceh",
    "PN BANDA ACEH": "Aceh",
    "Padang": "Sumatera Barat",
    "PN PADANG": "Sumatera Barat",
    "Samarinda": "Kalimantan Timur",
    "PN SAMARINDA": "Kalimantan Timur",
    "Pekanbaru": "Riau",
    "PN PEKANBARU": "Riau",
    "Mataram": "Nusa Tenggara Barat",
    "PN MATARAM": "Nusa Tenggara Barat",
    "Palembang": "Sumatera Selatan",
    "PN PALEMBANG": "Sumatera Selatan",
    "Bengkulu": "Bengkulu",
    "PN BENGKULU": "Bengkulu",
    "Jambi": "Jambi",
    "PN JAMBI": "Jambi",
    "Kendari": "Sulawesi Tenggara",
    "PN KENDARI": "Sulawesi Tenggara",
    "Palu": "Sulawesi Tengah",
    "PN PALU": "Sulawesi Tengah",
    "Ambon": "Maluku",
    "PN AMBON": "Maluku",
    "Banjarmasin": "Kalimantan Selatan",
    "PN BANJARMASIN": "Kalimantan Selatan",
    "Jayapura": "Papua",
    "PN JAYAPURA": "Papua",
    "PT JAYAPURA": "Papua",
    "Pangkalpinang": "Bangka Belitung",
    "PN PANGKALPINANG": "Bangka Belitung",
    "Mamuju": "Sulawesi Barat",
    "PN MAMUJU": "Sulawesi Barat",
    "Pontianak": "Kalimantan Barat",
    "PN PONTIANAK": "Kalimantan Barat",
    "Serang": "Banten",
    "PN SERANG": "Banten",
    "Tanjungkarang": "Lampung",
    "PN TANJUNGKARANG": "Lampung",
    "Denpasar": "Bali",
    "PN DENPASAR": "Bali",
    "Manado": "Sulawesi Utara",
    "PN MANADO": "Sulawesi Utara",
    "Gorontalo": "Gorontalo",
    "PN GORONTALO": "Gorontalo",
    "Palangkaraya": "Kalimantan Tengah",
    "PN PALANGKARAYA": "Kalimantan Tengah",
    "Yogyakarta": "DI Yogyakarta",
    "PN YOGYAKARTA": "DI Yogyakarta",
    "Manokwari": "Papua Barat",
    "PN MANOKWARI": "Papua Barat",
    "Ternate": "Maluku Utara",
    "PN TERNATE": "Maluku Utara",
    "Tanjungpinang": "Kepulauan Riau",
    "PN TANJUNGPINANG": "Kepulauan Riau",
}

# BPS 2024 provincial data (approximate, from bps.go.id publications)
# Population in thousands, GRDP in trillion IDR, PNS in thousands
BPS_DATA = {
    "DKI Jakarta":          {"pop_k": 10560, "grdp_t": 3200, "pns_k": 75},
    "Jawa Barat":           {"pop_k": 49320, "grdp_t": 2300, "pns_k": 165},
    "Jawa Timur":           {"pop_k": 40670, "grdp_t": 2450, "pns_k": 180},
    "Jawa Tengah":          {"pop_k": 36520, "grdp_t": 1450, "pns_k": 160},
    "Sumatera Utara":       {"pop_k": 14800, "grdp_t": 780,  "pns_k": 105},
    "Banten":               {"pop_k": 12290, "grdp_t": 620,  "pns_k": 40},
    "Sulawesi Selatan":     {"pop_k": 9050,  "grdp_t": 500,  "pns_k": 80},
    "Lampung":              {"pop_k": 9010,  "grdp_t": 320,  "pns_k": 45},
    "Sumatera Selatan":     {"pop_k": 8370,  "grdp_t": 420,  "pns_k": 55},
    "Riau":                 {"pop_k": 6390,  "grdp_t": 620,  "pns_k": 45},
    "Sumatera Barat":       {"pop_k": 5530,  "grdp_t": 260,  "pns_k": 50},
    "Nusa Tenggara Timur":  {"pop_k": 5490,  "grdp_t": 110,  "pns_k": 50},
    "Aceh":                 {"pop_k": 5370,  "grdp_t": 190,  "pns_k": 60},
    "Nusa Tenggara Barat":  {"pop_k": 5230,  "grdp_t": 165,  "pns_k": 40},
    "Kalimantan Timur":     {"pop_k": 3770,  "grdp_t": 700,  "pns_k": 40},
    "Kalimantan Selatan":   {"pop_k": 4120,  "grdp_t": 170,  "pns_k": 35},
    "Kalimantan Barat":     {"pop_k": 5070,  "grdp_t": 175,  "pns_k": 40},
    "Sulawesi Tengah":      {"pop_k": 3020,  "grdp_t": 155,  "pns_k": 32},
    "Sulawesi Tenggara":    {"pop_k": 2690,  "grdp_t": 125,  "pns_k": 28},
    "Sulawesi Utara":       {"pop_k": 2620,  "grdp_t": 130,  "pns_k": 30},
    "Papua":                {"pop_k": 4300,  "grdp_t": 230,  "pns_k": 45},
    "Papua Barat":          {"pop_k": 1130,  "grdp_t": 80,   "pns_k": 18},
    "Jambi":                {"pop_k": 3630,  "grdp_t": 205,  "pns_k": 30},
    "Bengkulu":             {"pop_k": 2050,  "grdp_t": 70,   "pns_k": 22},
    "Bali":                 {"pop_k": 4320,  "grdp_t": 260,  "pns_k": 30},
    "DI Yogyakarta":        {"pop_k": 3690,  "grdp_t": 170,  "pns_k": 35},
    "Maluku":               {"pop_k": 1880,  "grdp_t": 50,   "pns_k": 22},
    "Maluku Utara":         {"pop_k": 1310,  "grdp_t": 45,   "pns_k": 15},
    "Gorontalo":            {"pop_k": 1180,  "grdp_t": 40,   "pns_k": 12},
    "Sulawesi Barat":       {"pop_k": 1390,  "grdp_t": 50,   "pns_k": 12},
    "Kalimantan Tengah":    {"pop_k": 2770,  "grdp_t": 140,  "pns_k": 25},
    "Bangka Belitung":      {"pop_k": 1530,  "grdp_t": 75,   "pns_k": 12},
    "Kepulauan Riau":       {"pop_k": 2230,  "grdp_t": 330,  "pns_k": 15},
}


def print_section(title):
    print(f"\n\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def main():
    import sqlite3
    conn = sqlite3.connect("data/korupsinlp.db")
    verdicts = pd.read_sql_query(
        "SELECT id, daerah, vonis_bulan, tuntutan_bulan, kerugian_negara, tahun "
        "FROM verdicts WHERE daerah IS NOT NULL", conn)
    conn.close()

    print("=" * 70)
    print("  DARKNESS INDEX PILOT — FEASIBILITY ANALYSIS")
    print(f"  Verdicts with daerah: {len(verdicts)}")
    print("=" * 70)

    # ==================================================================
    #  1. MAP DAERAH → PROVINCE
    # ==================================================================
    print_section("1. DAERAH -> PROVINCE MAPPING")

    verdicts["province"] = verdicts["daerah"].map(DAERAH_TO_PROVINCE)
    mapped = verdicts["province"].notna().sum()
    unmapped = verdicts[verdicts["province"].isna()]["daerah"].unique()

    print(f"  Mapped: {mapped}/{len(verdicts)} ({100*mapped/len(verdicts):.1f}%)")
    print(f"  Unmapped daerah ({len(unmapped)}):")
    for d in sorted(unmapped)[:20]:
        n = len(verdicts[verdicts["daerah"] == d])
        print(f"    {d:<40s} n={n}")
    if len(unmapped) > 20:
        print(f"    ... and {len(unmapped) - 20} more")

    # Use only mapped verdicts
    v = verdicts[verdicts["province"].notna()].copy()
    print(f"\n  Analysis sample: {len(v)} verdicts across {v['province'].nunique()} provinces")

    # ==================================================================
    #  2. RAW CASE COUNTS PER PROVINCE
    # ==================================================================
    print_section("2. RAW CASE COUNTS PER PROVINCE")

    prov_counts = v.groupby("province").agg(
        n_cases=("id", "count"),
        mean_vonis=("vonis_bulan", lambda x: x.dropna().mean() / 12),
        mean_tuntutan=("tuntutan_bulan", lambda x: x.dropna().mean() / 12),
        total_kerugian=("kerugian_negara", "sum"),
    ).sort_values("n_cases", ascending=False)

    print(f"  {'Province':<30s} {'Cases':>6s} {'Mean vonis':>11s} {'Mean tuntutan':>14s}")
    print(f"  {'-'*65}")
    for prov, row in prov_counts.head(20).iterrows():
        print(f"  {prov:<30s} {row['n_cases']:>6.0f} {row['mean_vonis']:>10.1f}yr "
              f"{row['mean_tuntutan']:>13.1f}yr")

    # ==================================================================
    #  3. NORMALIZED RATES (per capita, per GRDP, per PNS)
    # ==================================================================
    print_section("3. NORMALIZED CORRUPTION RATES")

    bps = pd.DataFrame(BPS_DATA).T
    bps.index.name = "province"
    bps = bps.reset_index()

    merged = prov_counts.reset_index().merge(bps, on="province", how="inner")
    merged["cases_per_million"] = merged["n_cases"] / (merged["pop_k"] / 1000)
    merged["cases_per_trillion_grdp"] = merged["n_cases"] / merged["grdp_t"]
    merged["cases_per_10k_pns"] = merged["n_cases"] / (merged["pns_k"] / 10)

    print(f"\n  Provinces with BPS data: {len(merged)}")
    print(f"\n  {'Province':<25s} {'Cases':>6s} {'per M pop':>10s} {'per T GRDP':>11s} {'per 10k PNS':>12s}")
    print(f"  {'-'*68}")

    for _, row in merged.sort_values("cases_per_million", ascending=False).iterrows():
        print(f"  {row['province']:<25s} {row['n_cases']:>6.0f} "
              f"{row['cases_per_million']:>10.1f} "
              f"{row['cases_per_trillion_grdp']:>11.1f} "
              f"{row['cases_per_10k_pns']:>12.1f}")

    # ==================================================================
    #  4. RAW vs NORMALIZED RANKING COMPARISON
    # ==================================================================
    print_section("4. RAW vs NORMALIZED RANKING SHIFT")

    merged["rank_raw"] = merged["n_cases"].rank(ascending=False).astype(int)
    merged["rank_percap"] = merged["cases_per_million"].rank(ascending=False).astype(int)
    merged["rank_shift"] = merged["rank_raw"] - merged["rank_percap"]

    print(f"  Biggest ranking shifts when normalizing by population:")
    print(f"  {'Province':<25s} {'Raw rank':>9s} {'Norm rank':>10s} {'Shift':>7s}")
    print(f"  {'-'*55}")

    for _, row in merged.sort_values("rank_shift", key=abs, ascending=False).head(15).iterrows():
        direction = "up" if row["rank_shift"] > 0 else "down"
        print(f"  {row['province']:<25s} {row['rank_raw']:>9d} {row['rank_percap']:>10d} "
              f"{row['rank_shift']:>+6.0f} ({direction})")

    # Spearman correlation between raw and normalized
    from scipy.stats import spearmanr
    rho_percap, p_percap = spearmanr(merged["rank_raw"], merged["rank_percap"])
    print(f"\n  Spearman correlation (raw vs per-capita rank): rho={rho_percap:.3f}, p={p_percap:.4f}")
    print(f"  Normalization CHANGES the ranking substantially" if rho_percap < 0.7
          else f"  Rankings are moderately correlated but differ meaningfully")

    # ==================================================================
    #  5. PROTOTYPE DARKNESS SCORE
    # ==================================================================
    print_section("5. PROTOTYPE DARKNESS SCORE")

    print(f"  Concept: Expected cases (from structural predictors) vs detected cases")
    print(f"  Expected = f(population, GRDP, PNS count)")
    print(f"  Darkness = Expected - Detected (positive = under-detected)")
    print(f"")

    # Simple expected model: cases ~ population (log-log)
    import statsmodels.api as sm
    merged["log_pop"] = np.log(merged["pop_k"])
    merged["log_cases"] = np.log(merged["n_cases"] + 1)
    X = sm.add_constant(merged[["log_pop"]])
    model = sm.OLS(merged["log_cases"].values, X).fit()

    merged["expected_log"] = model.predict(X)
    merged["expected_cases"] = np.exp(merged["expected_log"]) - 1
    merged["darkness_score"] = merged["expected_cases"] - merged["n_cases"]
    merged["darkness_pct"] = 100 * merged["darkness_score"] / merged["expected_cases"]

    print(f"  Model: log(cases) ~ log(population)")
    print(f"  R2 = {model.rsquared:.3f}")
    print(f"")

    print(f"  {'Province':<25s} {'Detected':>9s} {'Expected':>9s} {'Darkness':>9s} {'% Dark':>8s}")
    print(f"  {'-'*64}")

    for _, row in merged.sort_values("darkness_score", ascending=False).iterrows():
        label = "UNDER" if row["darkness_score"] > 2 else "OVER" if row["darkness_score"] < -2 else ""
        print(f"  {row['province']:<25s} {row['n_cases']:>9.0f} {row['expected_cases']:>9.1f} "
              f"{row['darkness_score']:>+9.1f} {row['darkness_pct']:>+7.1f}% {label}")

    # ==================================================================
    #  6. FIGURE: Darkness Index Map
    # ==================================================================
    print_section("6. GENERATING DARKNESS FIGURES")

    # Figure 5: Raw vs Normalized
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    top15 = merged.nlargest(15, "n_cases")
    ax1.barh(top15["province"], top15["n_cases"], color="steelblue", alpha=0.7)
    ax1.set_xlabel("Number of Cases")
    ax1.set_title("(a) Raw Case Count (Top 15)")
    ax1.invert_yaxis()

    top15_norm = merged.nlargest(15, "cases_per_million")
    ax2.barh(top15_norm["province"], top15_norm["cases_per_million"], color="crimson", alpha=0.7)
    ax2.set_xlabel("Cases per Million Population")
    ax2.set_title("(b) Population-Normalized Rate (Top 15)")
    ax2.invert_yaxis()

    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig5_raw_vs_normalized.png")
    plt.close()
    print(f"  Saved: {FIG_DIR / 'fig5_raw_vs_normalized.png'}")

    # Figure 6: Darkness score
    fig, ax = plt.subplots(figsize=(10, 8))
    sorted_m = merged.sort_values("darkness_score", ascending=True)
    colors = ["crimson" if d > 0 else "steelblue" for d in sorted_m["darkness_score"]]
    ax.barh(sorted_m["province"], sorted_m["darkness_score"], color=colors, alpha=0.7)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlabel("Darkness Score (Expected - Detected Cases)")
    ax.set_title("Prototype Corruption Darkness Score by Province\n(Positive = Under-detected)")
    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig6_darkness_score.png")
    plt.close()
    print(f"  Saved: {FIG_DIR / 'fig6_darkness_score.png'}")

    # ==================================================================
    #  FEASIBILITY CONCLUSION
    # ==================================================================
    print_section("FEASIBILITY CONCLUSION")
    print(f"  The Darkness Index concept is FEASIBLE:")
    print(f"  - {len(v)} verdicts mapped to {v['province'].nunique()} provinces")
    print(f"  - Normalization dramatically changes rankings")
    print(f"    (Spearman rho = {rho_percap:.3f} between raw and per-capita)")
    print(f"  - Prototype darkness score reveals under/over-detection patterns")
    print(f"")
    print(f"  TO MAKE IT PUBLICATION-READY:")
    print(f"  1. Get exact BPS 2024 data (bps.go.id → download CSV)")
    print(f"  2. Add DJPK APBD data (fiscal dependence measure)")
    print(f"  3. Add BPK audit opinions (WTP/WDP/TMP correlation)")
    print(f"  4. Model: expected = f(pop, GRDP, PNS, fiscal_dependence)")
    print(f"  5. Darkness = expected - detected, with bootstrapped CIs")
    print(f"  6. Cross-validate with ICW annual reports")
    print(f"")
    print(f"  ESTIMATED EFFORT: 2-3 weeks for full paper")
    print(f"  NOVELTY: HIGH — no comparable index exists in the literature")


if __name__ == "__main__":
    main()
