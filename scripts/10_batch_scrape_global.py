"""Script 10: Batch scrape from global korupsi directory.

Scrapes ALL korupsi verdicts from the MA global directory
(not court-specific). Handles unreliable site with retries.

Usage: python -m scripts.10_batch_scrape_global --pages 10 --start-page 1
"""

import argparse
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import urllib3
from bs4 import BeautifulSoup

from src.config import BASE_URL, RAW_DIR
from src.db import init_db, transaction, insert_verdict, log_scrape
from src.scraper.base import ScraperSession
from src.scraper.detail import extract_metadata, save_html
from src.scraper.pdf_extractor import process_pdf

urllib3.disable_warnings()

GLOBAL_LISTING_URL = f"{BASE_URL}/direktori/index/kategori/korupsi-1"


def get_listing_page(page: int, timeout: int = 150) -> str | None:
    """Fetch a global korupsi listing page with retries."""
    if page == 1:
        url = f"{GLOBAL_LISTING_URL}.html"
    else:
        url = f"{GLOBAL_LISTING_URL}/page/{page}.html"

    for attempt in range(3):
        try:
            r = requests.get(
                url, verify=False, timeout=timeout,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            if r.status_code == 200 and len(r.text) > 15000:
                return r.text
        except Exception:
            pass
        time.sleep(5 * (attempt + 1))

    return None


def extract_new_urls(html: str, existing: set[str]) -> list[str]:
    """Extract verdict URLs not already in DB."""
    soup = BeautifulSoup(html, "lxml")
    urls = []
    for a in soup.find_all("a", href=True):
        if "/direktori/putusan/" in a["href"]:
            full = a["href"] if a["href"].startswith("http") else f"{BASE_URL}{a['href']}"
            if full not in existing and full not in urls:
                urls.append(full)
    return urls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=10,
                        help="Number of listing pages to scrape")
    parser.add_argument("--start-page", type=int, default=1,
                        help="First page to scrape")
    parser.add_argument("--max-per-page", type=int, default=20,
                        help="Max verdicts to scrape per listing page")
    args = parser.parse_args()

    init_db()
    session = ScraperSession()

    # Load existing URLs
    conn = sqlite3.connect(str(RAW_DIR.parent / "korupsinlp.db"))
    existing = set(row[0] for row in conn.execute("SELECT url FROM verdicts").fetchall())
    conn.close()

    total_success = 0
    total_fail = 0

    for page in range(args.start_page, args.start_page + args.pages):
        print(f"\n{'='*50}")
        print(f"PAGE {page}")
        print(f"{'='*50}")

        html = get_listing_page(page)
        if html is None:
            print(f"  [!] Failed to fetch page {page}")
            continue

        new_urls = extract_new_urls(html, existing)
        print(f"  Found {len(new_urls)} new verdict URLs")

        for i, url in enumerate(new_urls[:args.max_per_page]):
            print(f"  [{i+1}/{min(len(new_urls), args.max_per_page)}] ", end="", flush=True)
            time.sleep(3)

            try:
                r = requests.get(
                    url, verify=False, timeout=120,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                if len(r.text) < 15000:
                    print("error page")
                    total_fail += 1
                    continue

                metadata = extract_metadata(r.text)
                case = metadata.get("case_number", "?")
                lembaga = metadata.get("lembaga_peradilan", "")

                # Determine court level
                if "MAHKAMAH AGUNG" in lembaga.upper():
                    court_level = "ma"
                elif lembaga.upper().startswith("PN"):
                    court_level = "pn"
                elif lembaga.upper().startswith("PT"):
                    court_level = "pt"
                else:
                    court_level = "ma"

                verdict_id = case.replace("/", "_").replace(" ", "_") if case != "?" else str(abs(hash(url)))
                html_path = save_html(r.text, verdict_id)

                # Try PDF
                pdf_path = None
                if metadata.get("pdf_url"):
                    time.sleep(2)
                    try:
                        pdf_result = process_pdf(session, metadata["pdf_url"], verdict_id)
                        pdf_path = pdf_result.get("pdf_path")
                        if pdf_result.get("pdf_text"):
                            old = metadata.get("full_text", "")
                            metadata["full_text"] = (old + "\n" + pdf_result["pdf_text"]).strip()
                            print("+PDF ", end="")
                    except Exception:
                        pass

                with transaction() as conn:
                    db_data = {
                        "url": url,
                        "court": lembaga,
                        "court_level": court_level,
                        "case_number": case,
                        "html_path": str(html_path),
                        "pdf_url": metadata.get("pdf_url"),
                        "pdf_path": pdf_path,
                        "lembaga_peradilan": lembaga,
                        "amar": metadata.get("amar"),
                        "catatan_amar": metadata.get("catatan_amar"),
                        "date_decided": metadata.get("tanggal_dibacakan"),
                    }
                    insert_verdict(conn, db_data)
                    log_scrape(conn, url, 200, True)

                existing.add(url)
                total_success += 1
                print(f"OK {case}")

            except Exception as e:
                print(f"FAIL {str(e)[:40]}")
                total_fail += 1

    print(f"\n{'='*50}")
    print(f"BATCH SCRAPE COMPLETE")
    print(f"  Success: {total_success}")
    print(f"  Failed:  {total_fail}")
    print(f"  Total:   {total_success + total_fail}")


if __name__ == "__main__":
    sys.exit(main() or 0)
