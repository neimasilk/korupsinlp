"""Script 01: Smoke test — can we reach the MA website and find verdict links?

Usage: python -m scripts.01_test_connection
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import BASE_URL, SEARCH_URL, TARGET_COURTS
from src.scraper.base import ScraperSession
from src.scraper.listing import build_search_url, extract_verdict_urls, get_total_pages


def main():
    session = ScraperSession()
    all_pass = True

    # Test 1: Base URL reachable
    print("=" * 60)
    print("TEST 1: Base URL reachability")
    print("=" * 60)
    result = session.test_connection(BASE_URL)
    print(f"  URL: {result['url']}")
    print(f"  Reachable: {result['reachable']}")
    print(f"  Status: {result['status_code']}")
    print(f"  Content-Type: {result['content_type']}")
    print(f"  Size: {result['content_length']} bytes")
    if result['error']:
        print(f"  Error: {result['error']}")
    if not result['reachable']:
        all_pass = False

    # Test 2: Search page reachable
    print("\n" + "=" * 60)
    print("TEST 2: Search page reachability")
    print("=" * 60)
    result = session.test_connection(SEARCH_URL)
    print(f"  URL: {result['url']}")
    print(f"  Reachable: {result['reachable']}")
    print(f"  Status: {result['status_code']}")
    if not result['reachable']:
        all_pass = False

    # Test 3: Search for tipikor verdicts at first target court
    print("\n" + "=" * 60)
    print("TEST 3: Search for tipikor verdicts")
    print("=" * 60)
    court_key = list(TARGET_COURTS.keys())[0]
    court_name = TARGET_COURTS[court_key]
    search_url = build_search_url(court_name, page=1)
    print(f"  Court: {court_name}")
    print(f"  URL: {search_url}")

    resp = session.get_safe(search_url)
    if resp is None:
        print("  FAILED: Could not fetch search results")
        all_pass = False
    else:
        urls = extract_verdict_urls(resp.text)
        total_pages = get_total_pages(resp.text)
        print(f"  Status: {resp.status_code}")
        print(f"  Verdict URLs found: {len(urls)}")
        print(f"  Total pages: {total_pages}")
        if urls:
            print(f"  Sample URL: {urls[0]}")
        else:
            print("  WARNING: No verdict URLs found — HTML structure may have changed")
            all_pass = False

    # Test 4: Fetch a verdict detail page (if we found any)
    if urls:
        print("\n" + "=" * 60)
        print("TEST 4: Fetch verdict detail page")
        print("=" * 60)
        detail_url = urls[0]
        print(f"  URL: {detail_url}")
        result = session.test_connection(detail_url)
        print(f"  Reachable: {result['reachable']}")
        print(f"  Status: {result['status_code']}")
        print(f"  Size: {result['content_length']} bytes")
        if not result['reachable']:
            all_pass = False

    # Summary
    print("\n" + "=" * 60)
    if all_pass:
        print("RESULT: ALL TESTS PASSED — GO for scraping")
    else:
        print("RESULT: SOME TESTS FAILED — investigate before proceeding")
    print("=" * 60)

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
