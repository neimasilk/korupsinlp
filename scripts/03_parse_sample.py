"""Script 03: Parse all scraped verdicts and measure per-field success rates.

Usage: python -m scripts.03_parse_sample
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import P0_FIELDS, P1_FIELDS, P2_FIELDS
from src.db import init_db, get_verdicts, transaction, update_verdict
from src.parser.pipeline import parse_verdict


def main():
    init_db()
    verdicts = get_verdicts()

    if not verdicts:
        print("No verdicts in database. Run 02_scrape_sample.py first.")
        return 1

    print(f"Parsing {len(verdicts)} verdicts...\n")

    parsed_count = 0
    field_success = {f: 0 for f in P0_FIELDS + P1_FIELDS + P2_FIELDS}

    for v in verdicts:
        # Load full text from HTML file if available
        text = None
        html_path = v.get("html_path")
        if html_path and Path(html_path).exists():
            text = Path(html_path).read_text(encoding="utf-8", errors="ignore")

        # Build metadata dict from DB fields
        metadata = {
            "case_number": v.get("case_number", ""),
            "lembaga_peradilan": v.get("lembaga_peradilan", ""),
            "amar": v.get("amar", ""),
            "nama_terdakwa": v.get("nama_terdakwa"),
            "hakim_ketua": None,
            "hakim_anggota": None,
            "tahun_register": None,
        }

        result = parse_verdict(metadata, text)

        # Update DB
        with transaction() as conn:
            update_data = {
                "vonis_bulan": result["vonis_bulan"],
                "tuntutan_bulan": result["tuntutan_bulan"],
                "kerugian_negara": result["kerugian_negara"],
                "pasal": result["pasal"],
                "daerah": result["daerah"],
                "tahun": result["tahun"],
                "nama_terdakwa": result.get("nama_terdakwa") or v.get("nama_terdakwa"),
                "nama_hakim": result["nama_hakim"],
                "nama_jaksa": result["nama_jaksa"],
                "parsed_at": result["parsed_at"],
                "parse_source": result["parse_source"],
                "parse_errors": result["parse_errors"],
            }
            update_verdict(conn, v["url"], update_data)

        # Track success
        for field in field_success:
            if result.get(field) is not None:
                field_success[field] += 1

        parsed_count += 1

    # Report
    print(f"Parsed: {parsed_count}/{len(verdicts)}\n")

    print("=" * 50)
    print("PER-FIELD SUCCESS RATES")
    print("=" * 50)

    def print_field_group(name, fields):
        print(f"\n  {name}:")
        for f in fields:
            rate = field_success[f] / len(verdicts) if verdicts else 0
            bar = "█" * int(rate * 20) + "░" * (20 - int(rate * 20))
            status = "✓" if rate >= 0.6 else "△" if rate >= 0.4 else "✗"
            print(f"    {status} {f:20s} {bar} {rate:6.1%} ({field_success[f]}/{len(verdicts)})")

    print_field_group("P0 (Critical)", P0_FIELDS)
    print_field_group("P1 (Important)", P1_FIELDS)
    print_field_group("P2 (Nice-to-have)", P2_FIELDS)

    # P0 average
    p0_avg = sum(field_success[f] for f in P0_FIELDS) / (len(P0_FIELDS) * len(verdicts)) if verdicts else 0
    print(f"\n  P0 Average: {p0_avg:.1%}")

    # Full P0 coverage
    full_p0 = sum(
        1 for v in get_verdicts()
        if all(v.get(f) is not None for f in P0_FIELDS)
    )
    print(f"  Full P0 Coverage: {full_p0}/{len(verdicts)} ({full_p0/len(verdicts)*100:.1f}%)" if verdicts else "")

    return 0


if __name__ == "__main__":
    sys.exit(main())
