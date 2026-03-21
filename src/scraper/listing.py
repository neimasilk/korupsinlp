"""Scrape listing pages to collect verdict URLs from Direktori Putusan MA."""

import re
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from src.config import BASE_URL, DIREKTORI_URL, KORUPSI_KATEGORI, RAW_DIR
from src.scraper.base import ScraperSession


def build_listing_url(court_slug: str, page: int = 1,
                      year: int | None = None) -> str:
    """Build a direktori listing URL for korupsi verdicts.

    URL patterns:
      Default: /direktori/index/pengadilan/{slug}/kategori/korupsi-1/page/{n}.html
      Year-filtered: .../tahunjenis/putus/tahun/{year}/page/{n}.html

    Year-filtered URLs produce smaller, faster-loading pages and are more
    reliable for pagination than the default (which fails on page 5+).
    """
    base = f"{DIREKTORI_URL}/pengadilan/{court_slug}/kategori/{KORUPSI_KATEGORI}"
    if year:
        base = f"{base}/tahunjenis/putus/tahun/{year}"
    if page > 1:
        return f"{base}/page/{page}.html"
    return f"{base}.html"


def extract_verdict_urls(html: str) -> list[str]:
    """Extract verdict detail page URLs from a listing page."""
    soup = BeautifulSoup(html, "lxml")
    urls = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Verdict detail pages: /direktori/putusan/{hash}.html
        if "/direktori/putusan/" in href:
            full_url = urljoin(BASE_URL, href)
            if full_url not in urls:
                urls.append(full_url)

    return urls


def get_total_pages(html: str) -> int:
    """Extract total pages from pagination links.

    Pagination pattern: .../page/{n}.html with "Last" link pointing to final page.
    """
    soup = BeautifulSoup(html, "lxml")
    max_page = 1

    for link in soup.find_all("a", href=True):
        href = link["href"]

        # Match /page/{n}.html
        m = re.search(r"/page/(\d+)\.html", href)
        if m:
            max_page = max(max_page, int(m.group(1)))

    return max_page


def _save_debug_html(html: str, label: str):
    """Save listing page HTML for debugging pagination failures."""
    debug_dir = RAW_DIR / "debug_listing"
    debug_dir.mkdir(parents=True, exist_ok=True)
    path = debug_dir / f"{label}.html"
    path.write_text(html, encoding="utf-8")
    return path


def scrape_listing(session: ScraperSession, court_slug: str,
                   max_verdicts: int = 100, start_page: int = 1,
                   year: int | None = None) -> list[str]:
    """Scrape listing pages for a court until we have enough verdict URLs.

    Args:
        start_page: Page to start from (higher = older verdicts).
        year: If set, use year-filtered URL pattern (more reliable pagination).

    Returns list of verdict detail page URLs.
    """
    all_urls = []
    page = start_page
    consecutive_empty = 0

    while len(all_urls) < max_verdicts:
        url = build_listing_url(court_slug, page, year=year)
        print(f"  [.] Fetching page {page}: {url}")
        resp = session.get_safe(url)

        if resp is None:
            print(f"  [!] Failed to fetch listing page {page}")
            break

        urls = extract_verdict_urls(resp.text)
        if not urls:
            # Save debug HTML to diagnose why no results
            debug_path = _save_debug_html(
                resp.text,
                f"{court_slug}_page{page}_year{year or 'all'}_empty"
            )
            print(f"  [i] No results at page {page} (HTML saved: {debug_path})")
            print(f"      Response size: {len(resp.text)} bytes, status: {resp.status_code}")
            consecutive_empty += 1
            if consecutive_empty >= 2:
                print(f"  [!] 2 consecutive empty pages — stopping")
                break
            page += 1
            continue

        consecutive_empty = 0
        all_urls.extend(urls)
        print(f"  [+] Page {page}: found {len(urls)} verdicts (total: {len(all_urls)})")

        total_pages = get_total_pages(resp.text)
        if page >= total_pages:
            break
        page += 1

    return all_urls[:max_verdicts]
