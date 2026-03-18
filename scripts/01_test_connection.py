"""Script 01: Smoke test — can we reach the MA website and find verdict links?

Usage: python -m scripts.01_test_connection
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import BASE_URL, COURT_SLUGS
from src.scraper.base import ScraperSession
from src.scraper.listing import build_listing_url, extract_verdict_urls, get_total_pages
from src.scraper.detail import extract_metadata


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

    # Test 2: Listing page for korupsi verdicts
    print("\n" + "=" * 60)
    print("TEST 2: Korupsi listing page")
    print("=" * 60)
    court_slug = list(COURT_SLUGS.keys())[0]
    listing_url = build_listing_url(court_slug)
    result = session.test_connection(listing_url)
    print(f"  URL: {listing_url}")
    print(f"  Reachable: {result['reachable']}")
    print(f"  Status: {result['status_code']}")
    print(f"  Size: {result['content_length']} bytes")
    if not result['reachable']:
        all_pass = False

    # Test 3: Extract verdict URLs from listing
    urls = []
    print("\n" + "=" * 60)
    print("TEST 3: Extract verdict URLs from listing")
    print("=" * 60)
    resp = session.get_safe(listing_url)
    if resp:
        urls = extract_verdict_urls(resp.text)
        total_pages = get_total_pages(resp.text)
        print(f"  Verdict URLs found: {len(urls)}")
        print(f"  Total pages: {total_pages}")
        print(f"  Estimated total verdicts: ~{len(urls) * total_pages}")
        if urls:
            print(f"  Sample URL: {urls[0]}")
        else:
            print("  WARNING: No verdict URLs found — selector may need update")
            all_pass = False
    else:
        print("  FAILED: Could not fetch listing page")
        all_pass = False

    # Test 4: Fetch a verdict detail page
    if urls:
        print("\n" + "=" * 60)
        print("TEST 4: Fetch and parse verdict detail page")
        print("=" * 60)
        detail_url = urls[0]
        print(f"  URL: {detail_url}")
        resp = session.get_safe(detail_url)
        if resp:
            metadata = extract_metadata(resp.text)
            print(f"  Status: {resp.status_code}")
            print(f"  Case Number: {metadata.get('case_number', 'N/A')}")
            print(f"  Court: {metadata.get('lembaga_peradilan', 'N/A')}")
            print(f"  Amar: {metadata.get('amar', 'N/A')[:80]}")
            print(f"  Catatan Amar: {metadata.get('catatan_amar', 'N/A')[:80]}")
            print(f"  Has full_text: {bool(metadata.get('full_text'))}")
            print(f"  Has PDF URL: {bool(metadata.get('pdf_url'))}")
            print(f"  Fields found: {len(metadata)}")
            if not metadata.get('case_number'):
                print("  WARNING: Could not extract case number")
        else:
            print("  FAILED: Could not fetch detail page")
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
