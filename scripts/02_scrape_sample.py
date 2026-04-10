"""Script 02: Scrape 100 verdicts from MA korupsi listings.

Usage: python -m scripts.02_scrape_sample [--count N]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import COURT_SLUGS, SAMPLE_SIZE
from src.db import init_db, transaction, insert_verdict, log_scrape
from src.scraper.base import ScraperSession
from src.scraper.listing import scrape_listing
from src.scraper.detail import scrape_detail
from src.scraper.pdf_extractor import process_pdf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=SAMPLE_SIZE,
                        help="Number of verdicts to scrape")
    parser.add_argument("--start-page", type=int, default=1,
                        help="Listing page to start from (higher = older verdicts)")
    parser.add_argument("--year", type=int, default=None,
                        help="Filter by decision year (e.g. 2023). More reliable pagination.")
    args = parser.parse_args()

    init_db()
    session = ScraperSession()

    total_success = 0
    total_fail = 0

    for court_slug, court_name in COURT_SLUGS.items():
        print(f"\n{'='*60}")
        print(f"COURT: {court_name} (slug: {court_slug})")
        print(f"{'='*60}")

        # Step 1: Get listing URLs
        year_info = f", year={args.year}" if args.year else ""
        print(f"\n[1] Scraping listing pages for up to {args.count} verdicts (from page {args.start_page}{year_info})...")
        urls = scrape_listing(session, court_slug, max_verdicts=args.count,
                              start_page=args.start_page, year=args.year)
        print(f"    Found {len(urls)} verdict URLs")

        if not urls:
            print(f"    SKIP: No verdicts found for {court_name}")
            continue

        # Step 2: Scrape each detail page
        print(f"\n[2] Scraping detail pages...")
        for i, url in enumerate(urls, 1):
            print(f"    [{i}/{len(urls)}] ", end="")

            metadata = scrape_detail(session, url)

            if metadata is None:
                print(f"FAIL {url[:60]}")
                total_fail += 1
                with transaction() as conn:
                    log_scrape(conn, url, None, False, "detail_fetch_failed")
                continue

            case_num = metadata.get("case_number", "?")
            print(f"OK {case_num}", end="")

            # Step 3: Try PDF if available
            if metadata.get("pdf_url"):
                verdict_id = metadata.get("case_number", str(abs(hash(url))))
                pdf_result = process_pdf(session, metadata["pdf_url"], verdict_id)
                metadata["pdf_path"] = pdf_result["pdf_path"]
                if pdf_result["pdf_text"]:
                    # Append PDF text to full_text
                    existing = metadata.get("full_text", "")
                    metadata["full_text"] = (existing + "\n" + pdf_result["pdf_text"]).strip()
                    print(" +PDF", end="")
                elif pdf_result["is_scanned"]:
                    print(" (scanned)", end="")

            print()

            # Step 4: Store in DB
            with transaction() as conn:
                # Derive court level from slug
                court_level = "pn" if court_slug.startswith("pn-") else "ma"
                db_data = {
                    "url": url,
                    "court": court_name,
                    "court_level": court_level,
                    "case_number": metadata.get("case_number"),
                    "classification": metadata.get("classification"),
                    "sub_classification": metadata.get("sub_classification"),
                    "html_path": metadata.get("html_path"),
                    "pdf_url": metadata.get("pdf_url"),
                    "pdf_path": metadata.get("pdf_path"),
                    "lembaga_peradilan": metadata.get("lembaga_peradilan"),
                    "amar": metadata.get("amar"),
                    "catatan_amar": metadata.get("catatan_amar"),
                    "nama_terdakwa": metadata.get("nama_terdakwa"),
                    "date_decided": metadata.get("tanggal_dibacakan"),
                }
                insert_verdict(conn, db_data)
                log_scrape(conn, url, 200, True)

            total_success += 1

    # Summary
    total = total_success + total_fail
    print(f"\n{'='*60}")
    print(f"SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"  Success: {total_success}")
    print(f"  Failed:  {total_fail}")
    print(f"  Total:   {total}")
    if total > 0:
        print(f"  Rate:    {total_success/total*100:.1f}%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
