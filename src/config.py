"""Configuration constants for KorupsiNLP scraper."""

from pathlib import Path

# === Paths ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PDF_DIR = DATA_DIR / "pdf"
REPORTS_DIR = PROJECT_ROOT / "reports"
DB_PATH = DATA_DIR / "korupsinlp.db"

# === Website ===
BASE_URL = "https://putusan3.mahkamahagung.go.id"
SEARCH_URL = f"{BASE_URL}/search.html"
TIPIKOR_KLASIFIKASI = "Tipikor"

# Target courts for sampling (5 cities)
TARGET_COURTS = {
    "jakarta": "Pengadilan Negeri Jakarta Pusat",
    "surabaya": "Pengadilan Negeri Surabaya",
    "makassar": "Pengadilan Negeri Makassar",
    "medan": "Pengadilan Negeri Medan",
    "bandung": "Pengadilan Negeri Bandung",
}

VERDICTS_PER_COURT = 20  # 20 × 5 = 100 total

# === Scraping ===
REQUEST_DELAY = 2.0  # seconds between requests
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0  # exponential backoff multiplier

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# SSL verification disabled — MA site has certificate issues
SSL_VERIFY = False

# === Parser P0 Fields ===
P0_FIELDS = ["vonis_bulan", "kerugian_negara", "daerah", "tahun"]
P1_FIELDS = ["tuntutan_bulan", "pasal", "nama_terdakwa"]
P2_FIELDS = ["nama_hakim", "nama_jaksa"]

# === Feasibility Thresholds ===
GO_THRESHOLD = 0.60       # ≥60% → GO
CONDITIONAL_THRESHOLD = 0.40  # 40-60% → Conditional
# <40% → NO-GO
