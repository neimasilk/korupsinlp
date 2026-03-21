"""Download PDFs for verdicts that have pdf_url but no pdf_path."""

import sqlite3
from pathlib import Path

from src.scraper.base import ScraperSession
from src.config import PDF_DIR, DB_PATH


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT id, url, case_number, pdf_url
        FROM verdicts
        WHERE pdf_url IS NOT NULL AND (pdf_path IS NULL OR pdf_path = '')
    """).fetchall()

    print(f"Need to download {len(rows)} PDFs")

    session = ScraperSession(delay=1.5)
    success = 0
    fail = 0

    for i, r in enumerate(rows, 1):
        verdict_id = r["case_number"] or str(abs(hash(r["url"])))
        safe_name = verdict_id.replace("/", "_").replace(" ", "_")
        pdf_path = PDF_DIR / f"{safe_name}.pdf"

        if pdf_path.exists():
            conn.execute(
                "UPDATE verdicts SET pdf_path=? WHERE id=?",
                (str(pdf_path), r["id"]),
            )
            conn.commit()
            success += 1
            print(f"[{i}/{len(rows)}] EXISTS {safe_name}")
            continue

        print(f"[{i}/{len(rows)}] {safe_name}...", end="", flush=True)
        resp = session.get_safe(r["pdf_url"])
        if resp and len(resp.content) > 1000:
            pdf_path.write_bytes(resp.content)
            conn.execute(
                "UPDATE verdicts SET pdf_path=? WHERE id=?",
                (str(pdf_path), r["id"]),
            )
            conn.commit()
            success += 1
            print(f" OK ({len(resp.content) // 1024}KB)")
        else:
            fail += 1
            size = len(resp.content) if resp else 0
            print(f" FAIL ({size}B)")

    conn.close()
    print(f"\nDone: {success} success, {fail} failed")


if __name__ == "__main__":
    main()
