"""SQLite database schema and CRUD operations."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from src.config import DB_PATH


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def transaction(db_path: Path = DB_PATH):
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: Path = DB_PATH):
    """Create tables if they don't exist."""
    with transaction(db_path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS verdicts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                court TEXT,
                case_number TEXT,
                date_decided TEXT,
                classification TEXT,
                sub_classification TEXT,
                html_path TEXT,
                pdf_url TEXT,
                pdf_path TEXT,
                scraped_at TEXT DEFAULT (datetime('now')),

                -- Metadata from detail page
                nama_terdakwa TEXT,
                lembaga_peradilan TEXT,
                amar TEXT,

                -- Parsed fields
                vonis_bulan REAL,
                tuntutan_bulan REAL,
                kerugian_negara REAL,
                pasal TEXT,
                daerah TEXT,
                tahun INTEGER,
                nama_hakim TEXT,
                nama_jaksa TEXT,

                -- Parse metadata
                parsed_at TEXT,
                parse_source TEXT,  -- 'html' or 'pdf'
                parse_errors TEXT   -- JSON list of errors
            );

            CREATE TABLE IF NOT EXISTS scrape_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                status_code INTEGER,
                success INTEGER NOT NULL DEFAULT 0,
                error TEXT,
                timestamp TEXT DEFAULT (datetime('now'))
            );

            CREATE INDEX IF NOT EXISTS idx_verdicts_court ON verdicts(court);
            CREATE INDEX IF NOT EXISTS idx_verdicts_tahun ON verdicts(tahun);
            CREATE INDEX IF NOT EXISTS idx_verdicts_daerah ON verdicts(daerah);
        """)


def insert_verdict(conn: sqlite3.Connection, data: dict) -> int:
    """Insert a verdict record. Returns the row id."""
    cols = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    cursor = conn.execute(
        f"INSERT OR IGNORE INTO verdicts ({cols}) VALUES ({placeholders})",
        list(data.values()),
    )
    return cursor.lastrowid


def update_verdict(conn: sqlite3.Connection, url: str, data: dict):
    """Update a verdict by URL."""
    sets = ", ".join(f"{k} = ?" for k in data.keys())
    conn.execute(
        f"UPDATE verdicts SET {sets} WHERE url = ?",
        [*data.values(), url],
    )


def log_scrape(conn: sqlite3.Connection, url: str, status_code: int | None,
               success: bool, error: str | None = None):
    conn.execute(
        "INSERT INTO scrape_log (url, status_code, success, error) VALUES (?, ?, ?, ?)",
        (url, status_code, int(success), error),
    )


def get_verdicts(db_path: Path = DB_PATH, court: str | None = None) -> list[dict]:
    """Fetch all verdicts, optionally filtered by court."""
    conn = get_connection(db_path)
    try:
        if court:
            rows = conn.execute(
                "SELECT * FROM verdicts WHERE court = ?", (court,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM verdicts").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_scrape_stats(db_path: Path = DB_PATH) -> dict:
    """Get scraping success/failure counts."""
    conn = get_connection(db_path)
    try:
        row = conn.execute("""
            SELECT
                COUNT(*) as total,
                SUM(success) as successes,
                COUNT(*) - SUM(success) as failures
            FROM scrape_log
        """).fetchone()
        return dict(row)
    finally:
        conn.close()
