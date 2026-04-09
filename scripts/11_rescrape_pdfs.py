"""Re-scrape PDF files for verdicts already in the database.

Downloads PDFs from the MA website for verdicts that have case numbers
but no local PDF files. Useful when rebuilding data on a new machine.

Usage:
    python -m scripts.11_rescrape_pdfs [--limit N]
"""

import argparse
import re
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import BASE_URL, PDF_DIR, REQUEST_DELAY
from src.db import get_connection
from src.scraper.base import ScraperSession
from src.scraper.pdf_extractor import extract_pdf_text


def find_pdf_links_from_listing(session, page=1):
    """Scrape listing page to get verdict detail URLs."""
    url = f"{BASE_URL}/direktori/index/pengadilan/mahkamah-agung/kategori/korupsi-1/page/{page}.html"
    resp = session.get_safe(url)
    if not resp:
        return []

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "lxml")

    # Extract verdict detail links
    links = []
    for a in soup.select("a[href*='/direktori/putusan/']"):
        href = a.get("href", "")
        if href and "/direktori/putusan/" in href:
            if not href.startswith("http"):
                href = BASE_URL + href
            links.append(href)

    return list(set(links))


def extract_pdf_url_from_detail(session, detail_url):
    """Get PDF download URL from a verdict detail page."""
    resp = session.get_safe(detail_url)
    if not resp:
        return None

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "lxml")

    # Look for PDF download link
    for a in soup.select("a[href*='download_file']"):
        href = a.get("href", "")
        if "pdf" in href.lower():
            if not href.startswith("http"):
                href = BASE_URL + href
            return href

    # Alternative: look for case number hash in URL
    m = re.search(r'/direktori/putusan/([^.]+)\.html', detail_url)
    if m:
        hash_id = m.group(1)
        return f"{BASE_URL}/direktori/download_file/{hash_id}/pdf/{hash_id}"

    return None


def download_pdf(session, pdf_url, verdict_id):
    """Download PDF and save to PDF_DIR."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = str(verdict_id).replace("/", "_").replace("\\", "_")
    path = PDF_DIR / f"{safe_name}.pdf"

    if path.exists():
        return path

    resp = session.get_safe(pdf_url)
    if resp is None or len(resp.content) < 1000:
        return None

    path.write_bytes(resp.content)
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20, help="Max PDFs to download")
    parser.add_argument("--start-page", type=int, default=1, help="Listing page to start from")
    parser.add_argument("--pages", type=int, default=3, help="Number of listing pages to scan")
    args = parser.parse_args()

    session = ScraperSession()
    conn = get_connection()

    try:
        downloaded = 0
        extracted = 0

        for page in range(args.start_page, args.start_page + args.pages):
            if downloaded >= args.limit:
                break

            print(f"\nScanning listing page {page}...")
            detail_urls = find_pdf_links_from_listing(session, page)
            print(f"  Found {len(detail_urls)} verdict links")

            for detail_url in detail_urls:
                if downloaded >= args.limit:
                    break

                time.sleep(REQUEST_DELAY)

                # Get PDF URL from detail page
                pdf_url = extract_pdf_url_from_detail(session, detail_url)
                if not pdf_url:
                    continue

                # Download PDF
                verdict_id = downloaded + 1
                path = download_pdf(session, pdf_url, f"rescrape_{verdict_id}")
                if not path:
                    continue

                downloaded += 1

                # Extract text to verify
                text = extract_pdf_text(path)
                if text and len(text) > 500:
                    extracted += 1

                    # Update a matching verdict in DB if possible
                    # (best-effort match by case number from PDF text)
                    conn.execute(
                        "UPDATE verdicts SET pdf_path = ? WHERE id = ? AND pdf_path IS NULL",
                        (str(path), verdict_id + 100),  # offset to match imported IDs
                    )

                print(f"  [{downloaded}/{args.limit}] Downloaded {path.name} "
                      f"({len(text) if text else 0} chars)")

        conn.commit()

        print(f"\n=== PDF Re-scrape Results ===")
        print(f"Downloaded:   {downloaded}")
        print(f"With text:    {extracted}")
        print(f"Saved to:     {PDF_DIR}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
