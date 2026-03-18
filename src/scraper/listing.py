"""Scrape listing pages to collect verdict URLs."""

import re
from urllib.parse import urljoin, urlencode

from bs4 import BeautifulSoup

from src.config import BASE_URL, SEARCH_URL, TIPIKOR_KLASIFIKASI
from src.scraper.base import ScraperSession


def build_search_url(court: str, page: int = 1) -> str:
    """Build the search URL for tipikor verdicts at a given court."""
    params = {
        "q": "",
        "t_pidn": "",
        "t_pn": court,
        "t_cat": TIPIKOR_KLASIFIKASI,
        "t_subcat": "",
        "t_tp": "",
        "page": page,
    }
    return f"{SEARCH_URL}?{urlencode(params)}"


def extract_verdict_urls(html: str) -> list[str]:
    """Extract verdict detail page URLs from a search results page."""
    soup = BeautifulSoup(html, "lxml")
    urls = []

    # Verdict links are typically in search result entries
    # Pattern adapted from okkymabruri/putusan
    for link in soup.select("a[href]"):
        href = link.get("href", "")
        # Verdict detail pages match pattern: /direktori/putusan/...
        if "/direktori/putusan/" in href:
            full_url = urljoin(BASE_URL, href)
            if full_url not in urls:
                urls.append(full_url)

    return urls


def get_total_pages(html: str) -> int:
    """Extract total number of pages from pagination."""
    soup = BeautifulSoup(html, "lxml")

    # Look for pagination info
    pagination = soup.select(".pagination a, .page-link")
    if not pagination:
        return 1

    max_page = 1
    for link in pagination:
        text = link.get_text(strip=True)
        if text.isdigit():
            max_page = max(max_page, int(text))
        # Also check href for page numbers
        href = link.get("href", "")
        match = re.search(r"page=(\d+)", href)
        if match:
            max_page = max(max_page, int(match.group(1)))

    return max_page


def scrape_listing(session: ScraperSession, court: str,
                   max_verdicts: int = 20) -> list[str]:
    """Scrape listing pages for a court until we have enough verdict URLs.

    Returns list of verdict detail page URLs.
    """
    all_urls = []
    page = 1

    while len(all_urls) < max_verdicts:
        url = build_search_url(court, page)
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
