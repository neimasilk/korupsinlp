"""Import corpus CSV back into SQLite database.

Use this when the database needs to be rebuilt from the exported corpus
(e.g., after moving to a new machine where data/ was gitignored).

Usage:
    python -m scripts.10_import_corpus_csv
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from src.config import DB_PATH, DATA_DIR
from src.db import init_db, get_connection, migrate_db


def main():
    csv_path = Path("reports/corpus_release/korpuskorupsi_v1.csv")
    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return

    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"  {len(df)} rows, {len(df.columns)} columns")

    # Initialize database
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    init_db()
    migrate_db()

    conn = get_connection()
    try:
        # Check if verdicts already exist
        existing = conn.execute("SELECT COUNT(*) as c FROM verdicts").fetchone()["c"]
        if existing > 0:
            print(f"  Database already has {existing} verdicts — skipping import")
            return

        # Map CSV columns to database columns
        col_map = {
            "corpus_id": "id",
            "case_number": "case_number",
            "date_decided": "date_decided",
            "tahun": "tahun",
            "daerah": "daerah",
            "nama_terdakwa": "nama_terdakwa",
            "pemohon_kasasi": "pemohon_kasasi",
            "pasal": "pasal",
            "vonis_bulan": "vonis_bulan",
            "tuntutan_bulan": "tuntutan_bulan",
            "kerugian_negara": "kerugian_negara",
            "amar": "amar",
            "nama_hakim": "nama_hakim",
        }

        inserted = 0
        for _, row in df.iterrows():
            data = {}
            for csv_col, db_col in col_map.items():
                val = row.get(csv_col)
                if pd.notna(val):
                    data[db_col] = val

            # Need a URL (unique key) — use corpus_id as placeholder
            data["url"] = f"imported/corpus_id/{row['corpus_id']}"

            cols = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            conn.execute(
                f"INSERT OR IGNORE INTO verdicts ({cols}) VALUES ({placeholders})",
                list(data.values()),
            )
            inserted += 1

        conn.commit()
        print(f"  Imported {inserted} verdicts into {DB_PATH}")

        # Verify
        count = conn.execute("SELECT COUNT(*) as c FROM verdicts").fetchone()["c"]
        valid = conn.execute(
            "SELECT COUNT(*) as c FROM verdicts WHERE vonis_bulan > 0"
        ).fetchone()["c"]
        with_tuntutan = conn.execute(
            "SELECT COUNT(*) as c FROM verdicts WHERE tuntutan_bulan > 0"
        ).fetchone()["c"]
        print(f"\n  Total in DB:      {count}")
        print(f"  With vonis > 0:   {valid}")
        print(f"  With tuntutan:    {with_tuntutan}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
