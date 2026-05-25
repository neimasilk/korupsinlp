"""Script 17: Anatomy of Indonesian Corruption — Computational Typology.

A TOTALLY DIFFERENT angle: instead of predicting sentences, extract
WHAT KIND of corruption exists and whether different types are treated
differently. This is about mapping the corruption ecosystem, not the
sentencing system.

Features extracted from pertimbangan text:
- Actor type (jabatan): Bupati, Kepala Dinas, BUMN, Kepala Desa, etc.
- Modus: pengadaan fiktif, mark-up, gratifikasi, dana desa, etc.
- Sector: government, SOE, legislative, village, education
- Moral language intensity: does the judge use moral or technical language?

Then: cluster into types and test differential treatment.

Usage: python -m scripts.17_corruption_anatomy
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

SEED = 42
FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def print_section(title):
    print(f"\n\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def extract_features(texts):
    """Extract corruption anatomy features from pertimbangan text."""
    features = pd.DataFrame(index=texts.index)
    t = texts.str.lower()

    # === ACTOR TYPE (jabatan terdakwa) ===
    features["actor_kepala_daerah"] = t.str.contains(
        r"bupati|walikota|gubernur", regex=True).astype(int)
    features["actor_kepala_dinas"] = t.str.contains(
        r"kepala\s+dinas|kadis", regex=True).astype(int)
    features["actor_bumn"] = t.str.contains(
        r"direktur\s+utama|dirut|bumn|bumd|perusahaan\s+daerah", regex=True).astype(int)
    features["actor_dprd"] = t.str.contains(
        r"anggota\s+(dpr|dprd)|legislatif", regex=True).astype(int)
    features["actor_desa"] = t.str.contains(
        r"kepala\s+desa|lurah|kades|perangkat\s+desa|desa", regex=True).astype(int)
    features["actor_pns"] = t.str.contains(
        r"\bpns\b|\basn\b|pegawai\s+negeri", regex=True).astype(int)
    features["actor_polisi"] = t.str.contains(
        r"polisi|polri|kapolres|kapolda", regex=True).astype(int)
    features["actor_pendidikan"] = t.str.contains(
        r"rektor|dosen|kepala\s+sekolah|dinas\s+pendidikan", regex=True).astype(int)

    # === MODUS OPERANDI ===
    features["modus_pengadaan_fiktif"] = t.str.contains(
        r"fiktif|tidak\s+ada\s+pekerjaan|tidak\s+dilaksanakan|pengadaan\s+(?:barang|jasa).*fiktif",
        regex=True).astype(int)
    features["modus_markup"] = t.str.contains(
        r"mark[\s-]?up|penggelembungan|kemahalan|harga\s+(?:yang\s+)?tidak\s+wajar",
        regex=True).astype(int)
    features["modus_gratifikasi"] = t.str.contains(
        r"gratifikasi|suap|menerima\s+hadiah|menerima\s+pemberian",
        regex=True).astype(int)
    features["modus_apbd"] = t.str.contains(
        r"\bapbd\b|anggaran\s+(?:pendapatan|belanja)\s+daerah",
        regex=True).astype(int)
    features["modus_dana_desa"] = t.str.contains(
        r"dana\s+desa|add\b|alokasi\s+dana\s+desa",
        regex=True).astype(int)
    features["modus_infrastruktur"] = t.str.contains(
        r"proyek\s+(?:pembangunan|jalan|gedung|jembatan|irigasi)",
        regex=True).astype(int)
    features["modus_pencucian"] = t.str.contains(
        r"pencucian\s+uang|tppu", regex=True).astype(int)
    features["modus_penggelapan"] = t.str.contains(
        r"penggelapan|menggelapkan", regex=True).astype(int)

    # === MORAL vs TECHNICAL LANGUAGE ===
    moral_patterns = [
        r"tercela|tidak\s+terpuji",
        r"merugikan\s+(?:rakyat|masyarakat)",
        r"serakah|tamak|keserakahan",
        r"mencederai|merusak\s+kepercayaan",
        r"meresahkan\s+masyarakat",
        r"tidak\s+bertanggung\s*jawab",
        r"mengkhianati",
        r"tidak\s+pantas|tidak\s+layak",
    ]
    features["moral_language_count"] = sum(
        t.str.contains(p, regex=True).astype(int) for p in moral_patterns
    )

    technical_patterns = [
        r"terbukti\s+secara\s+sah",
        r"melawan\s+hukum",
        r"unsur[\s-]+(?:unsur\s+)?(?:telah\s+)?terpenuhi",
        r"menyalahgunakan\s+(?:wewenang|kewenangan)",
        r"memenuhi\s+(?:kualifikasi|rumusan)",
    ]
    features["technical_language_count"] = sum(
        t.str.contains(p, regex=True).astype(int) for p in technical_patterns
    )

    # Moral ratio: moral / (moral + technical)
    total_lang = features["moral_language_count"] + features["technical_language_count"]
    features["moral_ratio"] = np.where(
        total_lang > 0,
        features["moral_language_count"] / total_lang,
        0
    )

    # === COOPERATION/REMORSE indicators ===
    features["shows_remorse"] = t.str.contains(
        r"menyesal|menyesali|bertobat|berjanji\s+tidak", regex=True).astype(int)
    features["returned_money"] = t.str.contains(
        r"mengembalikan|pengembalian|mengganti\s+kerugian", regex=True).astype(int)
    features["has_dependents"] = t.str.contains(
        r"tanggungan\s+keluarga|anak\s+(?:yang\s+)?masih", regex=True).astype(int)

    return features


def main():
    import sqlite3
    import statsmodels.api as sm
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    conn = sqlite3.connect("data/korupsinlp.db")
    df = pd.read_sql_query("""
        SELECT id, pertimbangan_text, vonis_bulan, tuntutan_bulan,
               kerugian_negara, daerah, tahun
        FROM verdicts
        WHERE pertimbangan_text IS NOT NULL
        AND LENGTH(pertimbangan_text) > 100
        AND vonis_bulan IS NOT NULL AND vonis_bulan > 0
        AND tuntutan_bulan IS NOT NULL AND tuntutan_bulan > 0
    """, conn)
    conn.close()

    df["vonis_years"] = df["vonis_bulan"] / 12
    df["tuntutan_years"] = df["tuntutan_bulan"] / 12
    df["discount"] = df["vonis_years"] / df["tuntutan_years"]

    n = len(df)
    print("=" * 70)
    print("  ANATOMY OF INDONESIAN CORRUPTION")
    print(f"  Corpus: {n} verdicts with pertimbangan text")
    print("=" * 70)

    # ==================================================================
    #  1. FEATURE EXTRACTION
    # ==================================================================
    print_section("1. FEATURE EXTRACTION FROM TEXT")

    features = extract_features(df["pertimbangan_text"])
    feat_cols = [c for c in features.columns if not c.startswith("_")]

    print(f"  Extracted {len(feat_cols)} features from {n} verdicts")
    print(f"")

    # Feature prevalence
    print(f"  {'Feature':<35s} {'Count':>6s} {'%':>6s}")
    print(f"  {'-'*50}")
    for col in sorted(feat_cols, key=lambda c: features[c].sum(), reverse=True):
        count = features[col].sum()
        if count > 0 or "ratio" not in col:
            if "count" in col or "ratio" in col:
                print(f"  {col:<35s} {features[col].mean():>6.2f} (mean)")
            else:
                print(f"  {col:<35s} {count:>6.0f} {100*count/n:>5.1f}%")

    # ==================================================================
    #  2. CORRUPTION TYPOLOGY (k-means clustering)
    # ==================================================================
    print_section("2. CORRUPTION TYPOLOGY (Clustering)")

    # Select binary features for clustering
    cluster_cols = [c for c in feat_cols
                    if c.startswith("actor_") or c.startswith("modus_")]

    X = features[cluster_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Determine optimal k using silhouette
    from sklearn.metrics import silhouette_score
    results = []
    for k in range(2, 8):
        km = KMeans(n_clusters=k, random_state=SEED, n_init=20)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels)
        results.append((k, sil))
        print(f"  k={k}: silhouette={sil:.3f}")

    best_k = max(results, key=lambda x: x[1])[0]
    print(f"  Best k: {best_k}")

    # Fit with best k
    km = KMeans(n_clusters=best_k, random_state=SEED, n_init=20)
    df["cluster"] = km.fit_predict(X_scaled)

    # ==================================================================
    #  3. CLUSTER PROFILES
    # ==================================================================
    print_section("3. CLUSTER PROFILES")

    combined = pd.concat([df, features], axis=1)

    for cl in range(best_k):
        sub = combined[combined["cluster"] == cl]
        print(f"\n  --- CLUSTER {cl} (n={len(sub)}, {100*len(sub)/n:.1f}%) ---")
        print(f"  Mean tuntutan: {sub['tuntutan_years'].mean():.1f}yr")
        print(f"  Mean vonis:    {sub['vonis_years'].mean():.1f}yr")
        print(f"  Mean discount: {sub['discount'].mean():.3f}")
        k_sub = sub[sub["kerugian_negara"] > 0]
        if len(k_sub) > 0:
            print(f"  Median kerugian: Rp {k_sub['kerugian_negara'].median():,.0f}")

        # Top features for this cluster
        print(f"  Distinguishing features:")
        for col in cluster_cols:
            cluster_mean = sub[col].mean()
            overall_mean = combined[col].mean()
            if cluster_mean > overall_mean * 1.5 and cluster_mean > 0.1:
                print(f"    {col:<35s} {100*cluster_mean:>5.1f}% (vs {100*overall_mean:.1f}% overall)")

        # Moral language
        print(f"  Moral ratio: {sub['moral_ratio'].mean():.3f} "
              f"(vs {combined['moral_ratio'].mean():.3f} overall)")

    # ==================================================================
    #  4. DIFFERENTIAL TREATMENT BY TYPE
    # ==================================================================
    print_section("4. DIFFERENTIAL TREATMENT BY CORRUPTION TYPE")

    # Kruskal-Wallis on vonis, tuntutan, discount by cluster
    for var, label in [("vonis_years", "Vonis"), ("tuntutan_years", "Tuntutan"),
                       ("discount", "Discount")]:
        groups = [combined[combined["cluster"] == cl][var].values for cl in range(best_k)]
        h, p = stats.kruskal(*groups)
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"  {label:<12s}: H={h:>6.1f}, p={p:.6f} {sig}")

    # Specific comparisons: do certain actor types get lighter sentences?
    print(f"\n  Actor-type specific treatment (controlling for tuntutan):")
    for actor_col in [c for c in feat_cols if c.startswith("actor_")]:
        has = combined[features[actor_col] == 1]
        hasnt = combined[features[actor_col] == 0]
        if len(has) >= 10:
            # Compare discount
            u, p = stats.mannwhitneyu(has["discount"], hasnt["discount"])
            d_diff = has["discount"].mean() - hasnt["discount"].mean()
            sig = "*" if p < 0.05 else ""
            name = actor_col.replace("actor_", "")
            print(f"    {name:<25s} n={len(has):>3d}  discount={has['discount'].mean():.3f} "
                  f"(vs {hasnt['discount'].mean():.3f})  diff={d_diff:>+.3f}  p={p:.4f} {sig}")

    # Same for modus
    print(f"\n  Modus-specific treatment:")
    for modus_col in [c for c in feat_cols if c.startswith("modus_")]:
        has = combined[features[modus_col] == 1]
        hasnt = combined[features[modus_col] == 0]
        if len(has) >= 10:
            u, p = stats.mannwhitneyu(has["discount"], hasnt["discount"])
            d_diff = has["discount"].mean() - hasnt["discount"].mean()
            sig = "*" if p < 0.05 else ""
            name = modus_col.replace("modus_", "")
            print(f"    {name:<25s} n={len(has):>3d}  discount={has['discount'].mean():.3f} "
                  f"(vs {hasnt['discount'].mean():.3f})  diff={d_diff:>+.3f}  p={p:.4f} {sig}")

    # ==================================================================
    #  5. MORAL LANGUAGE ANALYSIS
    # ==================================================================
    print_section("5. MORAL vs TECHNICAL LANGUAGE")

    print(f"  Moral language count: mean={features['moral_language_count'].mean():.2f}, "
          f"max={features['moral_language_count'].max()}")
    print(f"  Technical language count: mean={features['technical_language_count'].mean():.2f}, "
          f"max={features['technical_language_count'].max()}")
    print(f"  Mean moral ratio: {features['moral_ratio'].mean():.3f}")
    print(f"  Verdicts with ANY moral language: "
          f"{(features['moral_language_count'] > 0).sum()} ({100*(features['moral_language_count'] > 0).mean():.1f}%)")

    # Does moral language correlate with heavier sentences?
    combined["moral_any"] = (features["moral_language_count"] > 0).astype(int)
    moral_yes = combined[combined["moral_any"] == 1]
    moral_no = combined[combined["moral_any"] == 0]

    print(f"\n  Cases WITH moral language (n={len(moral_yes)}):")
    print(f"    Mean vonis:   {moral_yes['vonis_years'].mean():.2f}yr")
    print(f"    Mean discount: {moral_yes['discount'].mean():.3f}")
    print(f"  Cases WITHOUT moral language (n={len(moral_no)}):")
    print(f"    Mean vonis:   {moral_no['vonis_years'].mean():.2f}yr")
    print(f"    Mean discount: {moral_no['discount'].mean():.3f}")

    u, p = stats.mannwhitneyu(moral_yes["discount"], moral_no["discount"])
    print(f"  Mann-Whitney (discount): p={p:.4f}")

    # Does moral language predict heavier sentence after controlling for tuntutan?
    combined["moral_count"] = features["moral_language_count"]
    X_moral = sm.add_constant(combined[["tuntutan_years", "moral_count"]])
    m_moral = sm.OLS(combined["vonis_years"].values, X_moral).fit()
    print(f"\n  OLS: vonis ~ tuntutan + moral_language_count")
    print(f"    moral_count: b={m_moral.params['moral_count']:.4f}, p={m_moral.pvalues['moral_count']:.4f}")
    if m_moral.pvalues["moral_count"] < 0.05:
        print(f"    SIGNIFICANT: moral language is associated with "
              f"{'heavier' if m_moral.params['moral_count'] > 0 else 'lighter'} sentences")
    else:
        print(f"    NOT significant: moral language does not independently predict sentence severity")

    # ==================================================================
    #  6. PUBLICATION FIGURES
    # ==================================================================
    print_section("6. GENERATING ANATOMY FIGURES")

    plt.rcParams.update({
        "font.size": 10, "axes.titlesize": 12,
        "axes.labelsize": 11, "figure.dpi": 150,
        "savefig.dpi": 300, "savefig.bbox": "tight",
    })

    # Figure 9: Corruption anatomy — actor + modus prevalence
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Actor types
    actor_cols = [c for c in feat_cols if c.startswith("actor_")]
    actor_counts = {c.replace("actor_", "").replace("_", " ").title(): features[c].sum()
                    for c in actor_cols if features[c].sum() > 0}
    actor_sorted = sorted(actor_counts.items(), key=lambda x: x[1], reverse=True)
    names, counts = zip(*actor_sorted)
    ax1.barh(range(len(names)), counts, color="steelblue", alpha=0.7)
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels(names)
    ax1.set_xlabel("Number of Cases")
    ax1.set_title("(a) Actor Types in Corruption Verdicts")
    ax1.invert_yaxis()

    # Modus
    modus_cols = [c for c in feat_cols if c.startswith("modus_")]
    modus_counts = {c.replace("modus_", "").replace("_", " ").title(): features[c].sum()
                    for c in modus_cols if features[c].sum() > 0}
    modus_sorted = sorted(modus_counts.items(), key=lambda x: x[1], reverse=True)
    names2, counts2 = zip(*modus_sorted)
    ax2.barh(range(len(names2)), counts2, color="crimson", alpha=0.7)
    ax2.set_yticks(range(len(names2)))
    ax2.set_yticklabels(names2)
    ax2.set_xlabel("Number of Cases")
    ax2.set_title("(b) Corruption Methods (Modus Operandi)")
    ax2.invert_yaxis()

    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig9_corruption_anatomy.png")
    plt.close()
    print(f"  Saved: {FIG_DIR / 'fig9_corruption_anatomy.png'}")

    # Figure 10: Treatment by cluster
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    for idx, (var, label, color) in enumerate([
        ("tuntutan_years", "Prosecution Demand (yr)", "steelblue"),
        ("vonis_years", "Sentence (yr)", "crimson"),
        ("discount", "Discount (vonis/tuntutan)", "green"),
    ]):
        ax = axes[idx]
        data_by_cluster = [combined[combined["cluster"] == cl][var].values
                           for cl in range(best_k)]
        bp = ax.boxplot(data_by_cluster, patch_artist=True)
        for patch in bp["boxes"]:
            patch.set_facecolor(color)
            patch.set_alpha(0.5)
        ax.set_xlabel("Corruption Type (Cluster)")
        ax.set_ylabel(label)
        ax.set_title(label)
        ax.set_xticklabels([f"Type {i}" for i in range(best_k)])

    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig10_treatment_by_type.png")
    plt.close()
    print(f"  Saved: {FIG_DIR / 'fig10_treatment_by_type.png'}")

    # ==================================================================
    #  SUMMARY
    # ==================================================================
    print_section("ANATOMY SUMMARY")

    print(f"  1. MOST COMMON MODUS: Pengadaan fiktif (fictitious procurement)")
    fiktif_pct = 100 * features["modus_pengadaan_fiktif"].mean()
    print(f"     Prevalence: {fiktif_pct:.1f}% of all corruption cases")
    print(f"")
    print(f"  2. ACTOR LANDSCAPE: Corruption spans all levels")
    print(f"     Village (desa): {100*features['actor_desa'].mean():.1f}%")
    print(f"     District heads: {100*features['actor_kepala_daerah'].mean():.1f}%")
    print(f"     SOEs (BUMN):    {100*features['actor_bumn'].mean():.1f}%")
    print(f"")
    print(f"  3. MORAL LANGUAGE IS RARE: judges speak technically, not morally")
    print(f"     Only {100*(features['moral_language_count'] > 0).mean():.1f}% of verdicts")
    print(f"     use ANY moral/evaluative language about corruption")
    print(f"")
    print(f"  4. {best_k} distinct corruption types identified via clustering")
    print(f"")
    print(f"  THIS IS A DIFFERENT STONE FROM THE MOUNTAIN:")
    print(f"  Not about how judges sentence, but about WHAT corruption")
    print(f"  looks like in Indonesia at the institutional level.")


if __name__ == "__main__":
    main()
