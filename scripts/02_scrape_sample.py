"""Script 02: Scrape 100 verdicts from 5 courts (20 each).

Usage: python -m scripts.02_scrape_sample
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import TARGET_COURTS, VERDICTS_PER_COURT
from src.db import init_db, transaction, insert_verdict, log_scrape
from src.scraper.base import ScraperSession
from src.scraper.listing import scrape_listing
from src.scraper.detail import scrape_detail
from src.scraper.pdf_extractor import process_pdf


def main():
    init_db()
    session = ScraperSession()

    total_success = 0
    total_fail = 0

    for court_key, court_name in TARGET_COURTS.items():
        print(f"\n{'='*60}")
        print(f"COURT: {court_name}")
        print(f"{'='*60}")

        # Step 1: Get listing URLs
        print(f"\n[1] Scraping listing pages...")
        urls = scrape_listing(session, court_name, max_verdicts=VERDICTS_PER_COURT)
        print(f"    Found {len(urls)} verdict URLs")

        if not urls:
            print(f"    SKIP: No verdicts found for {court_name}")
            continue

        # Step 2: Scrape each detail page
        print(f"\n[2] Scraping detail pages...")
        for i, url in enumerate(urls, 1):
            print(f"    [{i}/{len(urls)}] {url[:80]}...", end=" ")

            metadata = scrape_detail(session, url)

            if metadata is None:
                print("FAIL")
                total_fail += 1
                with transaction() as conn:
                    log_scrape(conn, url, None, False, "detail_fetch_failed")
                continue

            print("OK", end="")

            # Step 3: Try PDF if available
            if metadata.get("pdf_url"):
                verdict_id = metadata.get("case_number", str(hash(url)))
                pdf_result = process_pdf(session, metadata["pdf_url"], verdict_id)
                metadata["pdf_path"] = pdf_result["pdf_path"]
                if pdf_result["pdf_text"]:
                    metadata["full_text"] = (
                        metadata.get("full_text", "") + "\n" + pdf_result["pdf_text"]
                    )
                    print(" +PDF", end="")
                elif pdf_result["is_scanned"]:
                    print(" (scanned)", end="")

            print()

            # Step 4: Store in DB
            with transaction() as conn:
                db_data = {
                    "url": url,
                    "court": court_name,
                    "case_number": metadata.get("case_number"),
                    "classification": metadata.get("classification"),
                    "sub_classification": metadata.get("sub_classification"),
                    "html_path": metadata.get("html_path"),
                    "pdf_url": metadata.get("pdf_url"),
                    "pdf_path": metadata.get("pdf_path"),
                    "lembaga_peradilan": metadata.get("lembaga_peradilan"),
                    "amar": metadata.get("amar"),
                    "nama_terdakwa": metadata.get("nama_terdakwa"),
                    "date_decided": metadata.get("tanggal_dibacakan"),
                }
                insert_verdict(conn, db_data)
                log_scrape(conn, url, 200, True)

            total_success += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"  Success: {total_success}")
    print(f"  Failed:  {total_fail}")
    print(f"  Total:   {total_success + total_fail}")
    print(f"  Rate:    {total_success/(total_success+total_fail)*100:.1f}%" if (total_success+total_fail) > 0 else "  Rate: N/A")

    return 0


if __name__ == "__main__":
    sys.exit(main())
