"""Script 05: Validate parser against golden set (human annotations).

Usage: python -m scripts.05_validate_golden

Reads data/golden_set/golden_template.csv (must have human_* columns filled)
and computes precision, recall, and accuracy for each field.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

GOLDEN_PATH = Path("data/golden_set/golden_template.csv")

# Tolerance for numeric comparisons
NUMERIC_TOLERANCE = 0.05  # 5% tolerance for vonis/tuntutan
RUPIAH_TOLERANCE = 0.10   # 10% tolerance for kerugian (different rounding)


def main():
    if not GOLDEN_PATH.exists():
        print(f"Golden set not found: {GOLDEN_PATH}")
        print("Fill human_* columns in the CSV first.")
        return 1

    with open(GOLDEN_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Check if human annotations exist
    annotated = [r for r in rows if any(r.get(f"human_{f}") for f in
                 ["vonis_bulan", "tuntutan_bulan", "kerugian_negara", "daerah", "tahun"])]

    if not annotated:
        print("No human annotations found. Fill human_* columns first.")
        print(f"Template at: {GOLDEN_PATH}")
        return 1

    print(f"Validating {len(annotated)} annotated verdicts...\n")

    fields = ["vonis_bulan", "tuntutan_bulan", "kerugian_negara", "daerah", "tahun", "pasal", "nama_terdakwa"]

    results = {f: {"tp": 0, "fp": 0, "fn": 0, "correct": 0, "total": 0, "errors": []}
               for f in fields}

    for row in annotated:
        case = row["case_number"]

        for field in fields:
            parser_val = row.get(f"parser_{field}", "")
            human_val = row.get(f"human_{field}", "")

            if not human_val:
                continue  # Skip unannotated fields

            results[field]["total"] += 1

            parser_empty = not parser_val or parser_val in ("", "None")
            human_empty = human_val.strip() in ("", "None", "N/A", "-")

            if parser_empty and human_empty:
                results[field]["correct"] += 1  # Both agree: nothing there
                continue

            if parser_empty and not human_empty:
                results[field]["fn"] += 1  # Parser missed it
                results[field]["errors"].append(f"  FN {case}: parser=None, human={human_val}")
                continue

            if not parser_empty and human_empty:
                results[field]["fp"] += 1  # Parser hallucinated
                results[field]["errors"].append(f"  FP {case}: parser={parser_val}, human=None")
                continue

            # Both have values — check match
            if field in ("vonis_bulan", "tuntutan_bulan"):
                match = _numeric_match(parser_val, human_val, NUMERIC_TOLERANCE)
            elif field == "kerugian_negara":
                match = _numeric_match(parser_val, human_val, RUPIAH_TOLERANCE)
            elif field == "tahun":
                match = str(parser_val).strip() == str(human_val).strip()
            else:
                match = _text_match(parser_val, human_val)

            if match:
                results[field]["tp"] += 1
                results[field]["correct"] += 1
            else:
                results[field]["fp"] += 1
                results[field]["errors"].append(
                    f"  WRONG {case}: parser={parser_val}, human={human_val}")

    # Report
    print("=" * 60)
    print("GOLDEN SET VALIDATION RESULTS")
    print("=" * 60)

    for field in fields:
        r = results[field]
        if r["total"] == 0:
            continue

        accuracy = r["correct"] / r["total"]
        precision = r["tp"] / (r["tp"] + r["fp"]) if (r["tp"] + r["fp"]) > 0 else 0
        recall = r["tp"] / (r["tp"] + r["fn"]) if (r["tp"] + r["fn"]) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        status = "OK" if accuracy >= 0.8 else "??" if accuracy >= 0.6 else "XX"
        print(f"\n  {status} {field}")
        print(f"     Accuracy:  {accuracy:.1%} ({r['correct']}/{r['total']})")
        print(f"     Precision: {precision:.1%}")
        print(f"     Recall:    {recall:.1%}")
        print(f"     F1:        {f1:.1%}")
        print(f"     TP={r['tp']} FP={r['fp']} FN={r['fn']}")

        if r["errors"]:
            print("     Errors:")
            for e in r["errors"][:5]:
                print(f"       {e}")

    return 0


def _numeric_match(a: str, b: str, tolerance: float) -> bool:
    try:
        fa = float(a)
        fb = float(b)
        if fb == 0:
            return fa == 0
        return abs(fa - fb) / abs(fb) <= tolerance
    except (ValueError, TypeError):
        return str(a).strip() == str(b).strip()


def _text_match(a: str, b: str) -> bool:
    return a.strip().lower() == b.strip().lower()


if __name__ == "__main__":
    sys.exit(main())
