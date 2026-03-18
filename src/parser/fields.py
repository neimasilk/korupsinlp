"""Regex extractors for key verdict fields."""

import re


def extract_vonis_bulan(text: str) -> float | None:
    """Extract prison sentence in months from verdict text.

    Handles patterns like:
    - "pidana penjara selama 4 (empat) tahun"
    - "penjara selama 2 tahun 6 bulan"
    - "penjara 18 (delapan belas) bulan"
    - "1 (satu) tahun dan 6 (enam) bulan"
    """
    if not text:
        return None

    text_lower = text.lower()

    # Pattern: X tahun (dan/,) Y bulan
    m = re.search(
        r'(?:pidana\s+)?penjara\s+selama\s+'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        text_lower,
    )
    if m:
        years = int(m.group(1))
        months = int(m.group(2)) if m.group(2) else 0
        return years * 12 + months

    # Pattern: X bulan (standalone)
    m = re.search(
        r'(?:pidana\s+)?penjara\s+selama\s+'
        r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
        text_lower,
    )
    if m:
        return float(m.group(1))

    # Pattern: seumur hidup
    if re.search(r'penjara\s+seumur\s+hidup', text_lower):
        return -1  # Sentinel for life sentence

    # Pattern: pidana mati
    if re.search(r'pidana\s+mati', text_lower):
        return -2  # Sentinel for death sentence

    return None


def extract_tuntutan_bulan(text: str) -> float | None:
    """Extract prosecution demand in months.

    Looks for "menuntut ... penjara selama ..." or "dituntut ... penjara ..."
    """
    if not text:
        return None

    text_lower = text.lower()

    # Find the tuntutan section
    tuntutan_match = re.search(
        r'(?:menuntut|dituntut|tuntutan)[^.]*?'
        r'penjara\s+selama\s+'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        text_lower,
    )
    if tuntutan_match:
        years = int(tuntutan_match.group(1))
        months = int(tuntutan_match.group(2)) if tuntutan_match.group(2) else 0
        return years * 12 + months

    # Bulan only in tuntutan context
    tuntutan_match = re.search(
        r'(?:menuntut|dituntut|tuntutan)[^.]*?'
        r'penjara\s+selama\s+'
        r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
        text_lower,
    )
    if tuntutan_match:
        return float(tuntutan_match.group(1))

    return None


def extract_kerugian_negara(text: str) -> float | None:
    """Extract state financial loss in Rupiah.

    Handles patterns like:
    - "kerugian keuangan negara sebesar Rp 1.500.000.000"
    - "Rp. 1.500.000.000,00"
    - "Rp1.500.000.000,-"
    - "kerugian negara ... Rp 1,5 miliar"
    """
    if not text:
        return None

    text_lower = text.lower()

    # Look for kerugian negara context
    patterns = [
        r'kerugian\s+(?:keuangan\s+)?negara[^.]{0,100}?'
        r'rp\.?\s*([\d.,]+)',
        r'merugikan\s+(?:keuangan\s+)?negara[^.]{0,100}?'
        r'rp\.?\s*([\d.,]+)',
    ]

    for pattern in patterns:
        m = re.search(pattern, text_lower)
        if m:
            amount_str = m.group(1)
            amount = _parse_rupiah(amount_str)
            if amount and amount > 0:
                return amount

    # Broader: any Rp amount near "kerugian"
    m = re.search(
        r'kerugian[^.]{0,200}?rp\.?\s*([\d.,]+)',
        text_lower,
    )
    if m:
        amount = _parse_rupiah(m.group(1))
        if amount and amount > 0:
            return amount

    return None


def _parse_rupiah(amount_str: str) -> float | None:
    """Parse Indonesian Rupiah string to float.

    "1.500.000.000,00" → 1500000000.0
    "1.500.000.000,-" → 1500000000.0
    """
    # Remove trailing ,- or ,00
    cleaned = re.sub(r'[,-]+$', '', amount_str)
    # Indonesian format: dots as thousands separator, comma as decimal
    # Check if it uses Indonesian format (dots for thousands)
    if '.' in cleaned and ',' in cleaned:
        # Dots are thousands, comma is decimal
        cleaned = cleaned.replace('.', '').replace(',', '.')
    elif '.' in cleaned:
        # All dots — could be thousands separators
        # If multiple dots, they're thousands separators
        parts = cleaned.split('.')
        if len(parts) > 2:
            cleaned = cleaned.replace('.', '')
        elif len(parts) == 2 and len(parts[-1]) == 3:
            # e.g., "1.500" — likely thousands separator
            cleaned = cleaned.replace('.', '')
        # else keep as-is (decimal point)
    elif ',' in cleaned:
        cleaned = cleaned.replace(',', '.')

    try:
        return float(cleaned)
    except ValueError:
        return None


def extract_pasal(text: str) -> str | None:
    """Extract charged articles (pasal) from verdict text."""
    if not text:
        return None

    # Look for "Pasal X" patterns, collecting unique ones
    matches = re.findall(
        r'(?:pasal|Pasal)\s+(\d+\s*(?:ayat\s*\(\d+\))?'
        r'(?:\s*(?:jo\.?|juncto)\s*(?:pasal|Pasal)\s*\d+\s*'
        r'(?:ayat\s*\(\d+\))?)*)',
        text,
    )

    if not matches:
        return None

    # Deduplicate and join
    unique = list(dict.fromkeys(m.strip() for m in matches))
    return "; ".join(unique[:10])  # Cap at 10 to avoid noise


def extract_nama_terdakwa(text: str) -> str | None:
    """Extract defendant name from verdict text."""
    if not text:
        return None

    # Common pattern: "Terdakwa NAMA BIN/BINTI NAMA"
    m = re.search(
        r'(?:terdakwa|Terdakwa)\s*:?\s*([A-Z][A-Z\s.,]+?)(?:\s*(?:bin|binti|als|alias)\s|[,;]|\s{2,})',
        text,
    )
    if m:
        name = m.group(1).strip().rstrip(",;.")
        if len(name) > 3:
            return name

    # Pattern: "atas nama NAMA"
    m = re.search(
        r'atas\s+nama\s+([A-Z][A-Z\s.,]+?)(?:\s*(?:bin|binti|als|alias)\s|[,;]|\s{2,})',
        text,
    )
    if m:
        name = m.group(1).strip().rstrip(",;.")
        if len(name) > 3:
            return name

    return None


def extract_tahun(text: str, metadata: dict | None = None) -> int | None:
    """Extract year from case number or metadata."""
    # Try metadata first
    if metadata:
        # From case number like "123/Pid.Sus-TPK/2023/PN Jkt.Pst"
        case_num = metadata.get("case_number", "")
        m = re.search(r'/(\d{4})/', case_num)
        if m:
            year = int(m.group(1))
            if 2000 <= year <= 2030:
                return year

        # Direct tahun field
        tahun = metadata.get("tahun_register", "")
        if tahun and tahun.isdigit():
            year = int(tahun)
            if 2000 <= year <= 2030:
                return year

    # From text: look for year near "putusan" or "perkara"
    if text:
        m = re.search(r'(?:putusan|perkara|tahun)\s*(?::?\s*)(\d{4})', text.lower())
        if m:
            year = int(m.group(1))
            if 2000 <= year <= 2030:
                return year

    return None


def extract_daerah(text: str, metadata: dict | None = None) -> str | None:
    """Extract region/court location from metadata or text."""
    if metadata:
        lembaga = metadata.get("lembaga_peradilan", "")
        if lembaga:
            # Extract city from court name: "Pengadilan Negeri Surabaya" → "Surabaya"
            m = re.search(r'(?:Pengadilan\s+(?:Negeri|Tinggi)\s+)(.+)', lembaga)
            if m:
                return m.group(1).strip()
            return lembaga

    if text:
        m = re.search(
            r'Pengadilan\s+(?:Negeri|Tinggi)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            text,
        )
        if m:
            return m.group(1).strip()

    return None
