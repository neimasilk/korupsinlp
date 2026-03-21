"""Script 03: Parse all scraped verdicts and measure per-field success rates.

Usage: python -m scripts.03_parse_sample
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import P0_FIELDS, P1_FIELDS, P2_FIELDS
from src.db import init_db, get_verdicts, transaction, update_verdict
from src.parser.pipeline import parse_verdict
from src.scraper.detail import extract_metadata
from src.scraper.pdf_extractor import extract_pdf_text


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
        # Re-extract metadata from saved HTML (contains all fields like
        # hakim_ketua, catatan_amar, tahun_register that aren't in DB)
        html_path = v.get("html_path")
        metadata = {}
        html_text = None

        if html_path and Path(html_path).exists():
            html_text = Path(html_path).read_text(encoding="utf-8", errors="ignore")
            metadata = extract_metadata(html_text)

        # Override with DB fields that may have been set during scraping
        if v.get("case_number"):
            metadata["case_number"] = v["case_number"]
        if v.get("lembaga_peradilan"):
            metadata["lembaga_peradilan"] = v["lembaga_peradilan"]

        # Extract PDF text if available — PDFs have full verdict text,
        # HTML detail pages only have metadata
        text = html_text
        parse_source = "html"
        pdf_path = v.get("pdf_path")
        if pdf_path and Path(pdf_path).exists():
            pdf_text = extract_pdf_text(Path(pdf_path))
            if pdf_text and len(pdf_text) > 200:
                text = pdf_text
                parse_source = "pdf"

        result = parse_verdict(metadata, text)
        result["parse_source"] = parse_source

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
                "pemohon_kasasi": result.get("pemohon_kasasi"),
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
            bar = "#" * int(rate * 20) + "." * (20 - int(rate * 20))
            status = "OK" if rate >= 0.6 else "??" if rate >= 0.4 else "XX"
            print(f"    {status} {f:20s} [{bar}] {rate:6.1%} ({field_success[f]}/{len(verdicts)})")

    print_field_group("P0 (Critical)", P0_FIELDS)
    print_field_group("P1 (Important)", P1_FIELDS)
    print_field_group("P2 (Nice-to-have)", P2_FIELDS)

    # P0 average
    p0_avg = sum(field_success[f] for f in P0_FIELDS) / (len(P0_FIELDS) * len(verdicts)) if verdicts else 0
    print(f"\n  P0 Average: {p0_avg:.1%}")

    # Full P0 coverage
    updated = get_verdicts()
    full_p0 = sum(
        1 for v in updated
        if all(v.get(f) is not None for f in P0_FIELDS)
    )
    print(f"  Full P0 Coverage: {full_p0}/{len(verdicts)} ({full_p0/len(verdicts)*100:.1f}%)" if verdicts else "")

    return 0


if __name__ == "__main__":
    sys.exit(main())
