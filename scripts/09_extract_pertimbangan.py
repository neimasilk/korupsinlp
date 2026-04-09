"""Extract pertimbangan hukum (judicial reasoning) text from PDF verdicts.

One-time data preparation script. For each verdict with a PDF file,
extracts the pertimbangan section and stores it in the database.

Usage:
    python -m scripts.09_extract_pertimbangan
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DB_PATH, PDF_DIR
from src.db import get_connection, migrate_db
from src.parser.fields import extract_pertimbangan_text, _strip_watermark
from src.scraper.pdf_extractor import extract_pdf_text


def main():
    # Ensure schema has pertimbangan_text column
    migrate_db()

    conn = get_connection()
    try:
        # Get all verdicts with PDF paths
        rows = conn.execute(
            "SELECT id, url, pdf_path FROM verdicts WHERE pdf_path IS NOT NULL"
        ).fetchall()

        print(f"Found {len(rows)} verdicts with PDF paths")

        stats = {"total": len(rows), "extracted": 0, "too_short": 0, "no_text": 0, "no_file": 0}
        lengths = []

        for i, row in enumerate(rows):
            pdf_path = Path(row["pdf_path"])
            if not pdf_path.exists():
                stats["no_file"] += 1
                continue

            # Extract text from PDF
            pdf_text = extract_pdf_text(pdf_path)
            if not pdf_text:
                stats["no_text"] += 1
                continue

            # Strip watermarks and extract pertimbangan
            cleaned = _strip_watermark(pdf_text)
            pertimbangan = extract_pertimbangan_text(cleaned)

            if pertimbangan:
                stats["extracted"] += 1
                lengths.append(len(pertimbangan))
                conn.execute(
                    "UPDATE verdicts SET pertimbangan_text = ? WHERE id = ?",
                    (pertimbangan, row["id"]),
                )
            else:
                stats["too_short"] += 1

            if (i + 1) % 50 == 0:
                conn.commit()
                print(f"  Processed {i + 1}/{len(rows)}...")

        conn.commit()

        # Report
        print(f"\n=== Pertimbangan Extraction Results ===")
        print(f"Total with PDF:     {stats['total']}")
        print(f"Extracted:          {stats['extracted']} ({stats['extracted']/max(stats['total'],1)*100:.1f}%)")
        print(f"Too short (<200ch): {stats['too_short']}")
        print(f"No text in PDF:     {stats['no_text']}")
        print(f"PDF file missing:   {stats['no_file']}")

        if lengths:
            avg_len = sum(lengths) / len(lengths)
            min_len = min(lengths)
            max_len = max(lengths)
            print(f"\nText length stats:")
            print(f"  Mean:   {avg_len:,.0f} chars")
            print(f"  Min:    {min_len:,.0f} chars")
            print(f"  Max:    {max_len:,.0f} chars")
            print(f"  Median: {sorted(lengths)[len(lengths)//2]:,.0f} chars")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
