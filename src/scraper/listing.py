"""Scrape listing pages to collect verdict URLs from Direktori Putusan MA."""

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from src.config import BASE_URL, DIREKTORI_URL, KORUPSI_KATEGORI
from src.scraper.base import ScraperSession


def build_listing_url(court_slug: str, page: int = 1) -> str:
    """Build a direktori listing URL for korupsi verdicts.

    URL pattern: /direktori/index/pengadilan/{slug}/kategori/korupsi-1/page/{n}.html
    Page 1 omits the /page/ segment.
    """
    base = f"{DIREKTORI_URL}/pengadilan/{court_slug}/kategori/{KORUPSI_KATEGORI}"
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
        text = link.get_text(strip=True)

        # Match /page/{n}.html
        m = re.search(r"/page/(\d+)\.html", href)
        if m:
            max_page = max(max_page, int(m.group(1)))

    return max_page


def scrape_listing(session: ScraperSession, court_slug: str,
                   max_verdicts: int = 100, start_page: int = 1) -> list[str]:
    """Scrape listing pages for a court until we have enough verdict URLs.

    Args:
        start_page: Page to start from (higher = older verdicts).
                    Useful to skip recent verdicts that may not be uploaded yet.

    Returns list of verdict detail page URLs.
    """
    all_urls = []
    page = start_page

    while len(all_urls) < max_verdicts:
        url = build_listing_url(court_slug, page)
        print(f"  [.] Fetching page {page}: {url}")
        resp = session.get_safe(url)

        if resp is None:
            print(f"  [!] Failed to fetch listing page {page}")
            break

        urls = extract_verdict_urls(resp.text)
        if not urls:
            print(f"  [i] No more results at page {page}")
            break

        all_urls.extend(urls)
        print(f"  [+] Page {page}: found {len(urls)} verdicts (total: {len(all_urls)})")

        total_pages = get_total_pages(resp.text)
        if page >= total_pages:
            break
        page += 1

    return all_urls[:max_verdicts]
