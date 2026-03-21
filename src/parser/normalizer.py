"""Normalizers for currency, duration, and court-to-region mapping."""

import re

# Court name → region/province mapping
COURT_REGION_MAP = {
    "Jakarta Pusat": "DKI Jakarta",
    "Jakarta Selatan": "DKI Jakarta",
    "Jakarta Barat": "DKI Jakarta",
    "Jakarta Timur": "DKI Jakarta",
    "Jakarta Utara": "DKI Jakarta",
    "Surabaya": "Jawa Timur",
    "Bandung": "Jawa Barat",
    "Semarang": "Jawa Tengah",
    "Makassar": "Sulawesi Selatan",
    "Medan": "Sumatera Utara",
    "Palembang": "Sumatera Selatan",
    "Pekanbaru": "Riau",
    "Denpasar": "Bali",
    "Banjarmasin": "Kalimantan Selatan",
    "Pontianak": "Kalimantan Barat",
    "Manado": "Sulawesi Utara",
    "Jayapura": "Papua",
    "Kupang": "Nusa Tenggara Timur",
    "Mataram": "Nusa Tenggara Barat",
    "Ambon": "Maluku",
    "Samarinda": "Kalimantan Timur",
    "Padang": "Sumatera Barat",
    "Lampung": "Lampung",
    "Bengkulu": "Bengkulu",
    "Jambi": "Jambi",
    "Serang": "Banten",
    "Yogyakarta": "DI Yogyakarta",
    "Tanjung Karang": "Lampung",
    "Tanjungkarang": "Lampung",
    "Pangkalpinang": "Bangka Belitung",
    "Gorontalo": "Gorontalo",
    "Kendari": "Sulawesi Tenggara",
    "Purbalingga": "Jawa Tengah",
    "Mungkid": "Jawa Tengah",
    "Sintang": "Kalimantan Barat",
    "Koto Baru": "Sumatera Barat",
}


def normalize_duration_to_months(text: str) -> float | None:
    """Convert duration text to months.

    Handles: "4 tahun", "2 tahun 6 bulan", "18 bulan", etc.
    """
    if not text:
        return None

    text = text.lower().strip()
    total = 0.0
    found = False

    # Years
    m = re.search(r'(\d+)\s*(?:\([^)]+\)\s*)?tahun', text)
    if m:
        total += int(m.group(1)) * 12
        found = True

    # Months
    m = re.search(r'(\d+)\s*(?:\([^)]+\)\s*)?bulan', text)
    if m:
        total += int(m.group(1))
        found = True

    # Days (convert to fractional months)
    m = re.search(r'(\d+)\s*(?:\([^)]+\)\s*)?hari', text)
    if m:
        total += int(m.group(1)) / 30.0
        found = True

    return total if found else None


def normalize_rupiah(text: str) -> float | None:
    """Normalize Rupiah string to float value.

    "Rp 1.500.000.000,00" → 1500000000.0
    "Rp. 500.000.000,-" → 500000000.0
    """
    if not text:
        return None

    # Strip Rp prefix
    cleaned = re.sub(r'^rp\.?\s*', '', text.strip(), flags=re.IGNORECASE)
    # Remove trailing markers
    cleaned = re.sub(r'[,-]+$', '', cleaned)

    # Indonesian: dots as thousands, comma as decimal
    if '.' in cleaned and ',' in cleaned:
        cleaned = cleaned.replace('.', '').replace(',', '.')
    elif '.' in cleaned:
        parts = cleaned.split('.')
        if len(parts) > 2 or (len(parts) == 2 and len(parts[-1]) == 3):
            cleaned = cleaned.replace('.', '')
    elif ',' in cleaned:
        cleaned = cleaned.replace(',', '.')

    try:
        return float(cleaned)
    except ValueError:
        return None


def court_to_province(court_name: str) -> str | None:
    """Map court location to province."""
    if not court_name:
        return None

    # Direct lookup
    if court_name in COURT_REGION_MAP:
        return COURT_REGION_MAP[court_name]

    # Partial match
    for key, province in COURT_REGION_MAP.items():
        if key.lower() in court_name.lower():
            return province

    return None
