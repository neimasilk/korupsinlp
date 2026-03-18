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

# Direktori URL patterns (discovered from live site)
# Listing: /direktori/index/pengadilan/{court_slug}/kategori/korupsi-1.html
# Pagination: .../page/{n}.html
# Year filter: .../tahunjenis/putus/tahun/{year}.html
# Detail: /direktori/putusan/{hash}.html
# PDF: /direktori/download_file/{hash}/pdf/{hash}
DIREKTORI_URL = f"{BASE_URL}/direktori/index"
KORUPSI_KATEGORI = "korupsi-1"

# Court slugs (verified working against live site)
# Focus on MA level — kasasi decisions from courts nationwide
COURT_SLUGS = {
    "mahkamah-agung": "Mahkamah Agung",
}

# For future expansion: PN-level courts (some timeout on large result sets)
PN_COURT_SLUGS = {
    "pn-bandung": "PN Bandung",
    "pn-jakarta-pusat": "PN Jakarta Pusat",
    "pn-surabaya": "PN Surabaya",
    "pn-makassar": "PN Makassar",
    "pn-medan": "PN Medan",
}

SAMPLE_SIZE = 100  # Total verdicts to scrape for feasibility

# === Scraping ===
REQUEST_DELAY = 2.0  # seconds between requests
REQUEST_TIMEOUT = 90  # seconds (MA site can be slow)
MAX_RETRIES = 3
RETRY_BACKOFF = 3.0  # exponential backoff multiplier

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
