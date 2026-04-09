"""Analyze autoresearch experiment results.

Reads results.tsv and generates summary statistics + progress plot.

Usage: python -m autoresearch.analyze_results
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

RESULTS_PATH = Path(__file__).parent / "results.tsv"


def main():
    if not RESULTS_PATH.exists():
        print("No results.tsv found. Run some experiments first.")
        return

    df = pd.read_csv(RESULTS_PATH, sep="\t")

    print(f"=== Autoresearch Results Summary ===")
    print(f"Total experiments:  {len(df)}")

    kept = df[df["status"] == "keep"]
    discarded = df[df["status"] == "discard"]
    crashed = df[df["status"] == "crash"] if "crash" in df["status"].values else pd.DataFrame()

    print(f"Kept:               {len(kept)}")
    print(f"Discarded:          {len(discarded)}")
    if len(crashed):
        print(f"Crashed:            {len(crashed)}")

    if len(df) > 0:
        print(f"\nval_r2 stats:")
        valid = df[df["status"].isin(["keep", "discard"])]
        if len(valid):
            print(f"  Best:    {valid['val_r2'].max():.6f}")
            print(f"  Worst:   {valid['val_r2'].min():.6f}")
            print(f"  Mean:    {valid['val_r2'].mean():.6f}")
            print(f"  Median:  {valid['val_r2'].median():.6f}")

    if len(kept) > 0:
        print(f"\nKept experiments (chronological):")
        for _, row in kept.iterrows():
            print(f"  {row['commit'][:7]}  val_r2={row['val_r2']:.6f}  {row.get('description', '')}")

        # Running best
        running_best = kept["val_r2"].expanding().max()
        print(f"\nRunning best val_r2:")
        for i, (_, row) in enumerate(kept.iterrows()):
            marker = " *" if row["val_r2"] == running_best.iloc[i] and (i == 0 or running_best.iloc[i] > running_best.iloc[i-1]) else ""
            print(f"  {row['commit'][:7]}  {running_best.iloc[i]:.6f}{marker}")

    # Try to generate plot if matplotlib available
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 6))

        # All experiments
        all_valid = df[df["status"].isin(["keep", "discard"])]
        x = range(len(all_valid))
        colors = ["green" if s == "keep" else "lightgray" for s in all_valid["status"]]
        ax.scatter(x, all_valid["val_r2"], c=colors, alpha=0.6, s=30)

        # Running best line
        if len(kept) > 0:
            kept_indices = [i for i, s in enumerate(all_valid["status"]) if s == "keep"]
            kept_r2 = [all_valid.iloc[i]["val_r2"] for i in kept_indices]
            running = [max(kept_r2[:j+1]) for j in range(len(kept_r2))]
            ax.step(kept_indices, running, where="post", color="green", linewidth=2, label="Running best")

        # Baseline
        ax.axhline(y=0.600, color="red", linestyle="--", alpha=0.5, label="Baseline (M9 R²=0.600)")

        ax.set_xlabel("Experiment #")
        ax.set_ylabel("val_r2")
        ax.set_title("KorupsiNLP Autoresearch Progress")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plot_path = Path(__file__).parent / "progress.png"
        fig.savefig(plot_path, dpi=150, bbox_inches="tight")
        print(f"\nProgress plot saved to {plot_path}")
        plt.close()

    except ImportError:
        print("\nmatplotlib not available — skipping plot generation")
        print("Install with: pip install matplotlib")


if __name__ == "__main__":
    main()
