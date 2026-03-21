"""Regex extractors for key verdict fields."""

import re


def _find_penjara(text_lower: str) -> float | None:
    """Find prison sentence duration in a text fragment."""
    # Tahun [dan bulan]
    m = re.search(
        r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        text_lower,
    )
    if m:
        years = int(m.group(1))
        months = int(m.group(2)) if m.group(2) else 0
        return years * 12 + months

    # Bulan only
    m = re.search(
        r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
        text_lower,
    )
    if m:
        return float(m.group(1))

    return None


def extract_vonis_bulan(text: str) -> float | None:
    """Extract prison sentence in months from verdict text.

    For kasasi PDFs, the text contains multiple 'penjara' mentions:
    1. Tuntutan section (prosecution demand) — NOT what we want
    2. Lower court decision quote — NOT what we want
    3. MENGADILI section (MA's actual decision) — THIS is the vonis

    Strategy: search the MENGADILI section first, then catatan_amar prefix,
    then fall back to LAST match in full text.
    """
    if not text:
        return None

    text_lower = text.lower()

    # Strategy 1: Find MENGADILI section (the actual court decision)
    # MA verdicts use "M E N G A D I L I" (spaced) or "MENGADILI"
    mengadili_patterns = [
        r'm\s+e\s+n\s+g\s+a\s+d\s+i\s+l\s+i',
        r'mengadili\s*:',
        r'mengadili\s*\n',
    ]
    for pat in mengadili_patterns:
        m = re.search(pat, text_lower)
        if m:
            amar_section = text_lower[m.start():]
            result = _find_penjara(amar_section)
            if result is not None:
                return result

    # Strategy 2: Search in the first 500 chars (catatan_amar prefix from pipeline)
    prefix = text_lower[:500]
    result = _find_penjara(prefix)
    if result is not None:
        return result

    # Strategy 3: Use the LAST penjara match in the full text
    # (the final sentence is more likely to be the actual vonis)
    all_matches = list(re.finditer(
        r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        text_lower,
    ))
    if all_matches:
        m = all_matches[-1]
        years = int(m.group(1))
        months = int(m.group(2)) if m.group(2) else 0
        return years * 12 + months

    all_matches = list(re.finditer(
        r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
        text_lower,
    ))
    if all_matches:
        return float(all_matches[-1].group(1))

    # Seumur hidup
    if re.search(r'penjara\s+seumur\s+hidup', text_lower):
        return -1

    # Pidana mati
    if re.search(r'pidana\s+mati', text_lower):
        return -2

    return None


def extract_tuntutan_bulan(text: str) -> float | None:
    """Extract prosecution demand in months.

    Looks for "tuntutan pidana" section header, then finds penjara within it.
    Kasasi PDFs quote the full tuntutan as a numbered list, so periods in
    "1." "2." etc. must be allowed — we use a character limit instead of [^.].
    """
    if not text:
        return None

    text_lower = text.lower()

    # Strategy 1: Find "tuntutan pidana" section header, then search within
    # next 800 chars for penjara. This handles kasasi PDFs that quote the
    # full prosecution demand as a numbered list.
    tuntutan_header = re.search(r'tuntutan\s+pidana', text_lower)
    if tuntutan_header:
        section = text_lower[tuntutan_header.start():tuntutan_header.start() + 800]
        m = re.search(
            r'(?:pidana\s+)?penjara\s+(?:selama\s+)?'
            r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
            r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
            section,
        )
        if m:
            years = int(m.group(1))
            months = int(m.group(2)) if m.group(2) else 0
            return years * 12 + months

        m = re.search(
            r'(?:pidana\s+)?penjara\s+(?:selama\s+)?'
            r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
            section,
        )
        if m:
            return float(m.group(1))

    # Strategy 2: Original pattern — menuntut/dituntut near penjara (no period between)
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
    - "Rp300.000.000,00" (no space after Rp)
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

    # Pattern: "UP Rp..." (uang pengganti — proxy for kerugian negara)
    m = re.search(
        r'(?:uang\s+pengganti|up)\s+(?:sebesar\s+)?rp\.?\s*([\d.,]+)',
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
    "300.000.000" → 300000000.0
    """
    # Remove trailing ,- or ,00
    cleaned = re.sub(r'[,-]+$', '', amount_str)
    # Indonesian format: dots as thousands separator, comma as decimal
    if '.' in cleaned and ',' in cleaned:
        cleaned = cleaned.replace('.', '').replace(',', '.')
    elif '.' in cleaned:
        parts = cleaned.split('.')
        if len(parts) > 2:
            cleaned = cleaned.replace('.', '')
        elif len(parts) == 2 and len(parts[-1]) == 3:
            cleaned = cleaned.replace('.', '')
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

    # Match "Pasal X", "Pasal X Ayat (Y)", "Pasal X jo Pasal Y", "Pasal X UU PTPK"
    matches = re.findall(
        r'(?:pasal|Pasal)\s+(\d+\s*(?:[Aa]yat\s*\(\d+\))?'
        r'(?:\s*(?:jo\.?|juncto)\s*(?:pasal|Pasal)\s*\d+\s*'
        r'(?:[Aa]yat\s*\(\d+\))?)*'
        r'(?:\s+(?:UU\s+\w+|KUHP))?)',
        text,
    )

    if not matches:
        return None

    unique = list(dict.fromkeys(m.strip() for m in matches))
    return "; ".join(unique[:10])


def extract_nama_terdakwa(text: str) -> str | None:
    """Extract defendant name from verdict text.

    Handles patterns:
    - "Terdakwa NAMA BIN NAMA"
    - "VS NAMA (Terdakwa)" — MA kasasi format
    - "atas nama NAMA"
    """
    if not text:
        return None

    # MA kasasi format: "Penuntut Umum VS NAMA_TERDAKWA (Terdakwa)"
    m = re.search(
        r'VS\s+(.+?)\s*\(Terdakwa\)',
        text,
    )
    if m:
        name = m.group(1).strip().rstrip(",;.")
        if len(name) > 3:
            return name

    # Standard: "Terdakwa NAMA"
    m = re.search(
        r'(?:terdakwa|Terdakwa)\s*:?\s*([A-Z][A-Z\s.,]+?)(?:\s*(?:bin|binti|als|alias)\s|[,;]|\s{2,})',
        text,
    )
    if m:
        name = m.group(1).strip().rstrip(",;.")
        if len(name) > 3:
            return name

    # "atas nama NAMA"
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
    if metadata:
        # From case number like "384 K/PID.SUS/2026" or "123/Pid.Sus-TPK/2023/PN Jkt.Pst"
        case_num = metadata.get("case_number") or ""
        # Try /year/ pattern first (PN format)
        m = re.search(r'/(\d{4})/', case_num)
        if m:
            year = int(m.group(1))
            if 2000 <= year <= 2030:
                return year
        # Try year at end of case number (MA format: "384 K/PID.SUS/2026")
        m = re.search(r'/(\d{4})$', case_num)
        if m:
            year = int(m.group(1))
            if 2000 <= year <= 2030:
                return year

        # Direct tahun field
        tahun = metadata.get("tahun_register") or ""
        if tahun and str(tahun).isdigit():
            year = int(tahun)
            if 2000 <= year <= 2030:
                return year

    # From text: look for year near relevant keywords
    if text:
        m = re.search(r'(?:putusan|perkara|tahun|Nomor)\s*(?::?\s*).*?(\d{4})', text[:500])
        if m:
            year = int(m.group(1))
            if 2000 <= year <= 2030:
                return year

    return None


def _clean_daerah(name: str) -> str:
    """Clean up common daerah extraction artifacts from PDF text."""
    # PDF text extraction sometimes merges city name with next word
    # e.g., "Padangkarena" = "Padang" + "karena"
    known_suffixes = [
        "karena", "tanggal", "nomor", "dalam", "dengan", "yang",
        "pada", "untuk", "telah", "tersebut", "sebagai",
    ]
    lower = name.lower()
    for suffix in known_suffixes:
        if lower.endswith(suffix) and len(lower) > len(suffix) + 2:
            cleaned = name[:len(name) - len(suffix)]
            if len(cleaned) >= 3:
                return cleaned
    # Strip "Negeri " prefix if accidentally captured
    if name.startswith("Negeri "):
        return name[7:]
    return name


def extract_daerah(text: str, metadata: dict | None = None) -> str | None:
    """Extract region/court location from metadata or text.

    For MA kasasi verdicts, the origin court is referenced in the text
    (e.g., "PN Smg" = Semarang, or from related case numbers).
    """
    if metadata:
        lembaga = metadata.get("lembaga_peradilan") or ""
        if lembaga and lembaga.upper() != "MAHKAMAH AGUNG":
            # Direct court name
            m = re.search(r'(?:Pengadilan\s+(?:Negeri|Tinggi|Tindak Pidana Korupsi)\s+)(.+)', lembaga, re.IGNORECASE)
            if m:
                return _clean_daerah(m.group(1).strip())
            return lembaga

    # Extract origin court from text — MA verdicts reference the lower court
    if text:
        # Pattern: "PN {City}" or "Pengadilan Negeri {City}"
        m = re.search(
            r'(?:Pengadilan\s+(?:Negeri|Tindak\s+Pidana\s+Korupsi(?:\s+pada\s+Pengadilan\s+Negeri)?)\s+)'
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            text,
        )
        if m:
            return _clean_daerah(m.group(1).strip())

        # Short form: case number like "19/Pid.Sus-TPK/2025/PN Smg"
        m = re.search(r'/PN\s+([A-Z][A-Za-z.]+)', text)
        if m:
            raw = m.group(1).strip().rstrip('.')
            return _expand_court_abbrev(_clean_daerah(raw))

    return None


# Common MA court abbreviations → full city name
_COURT_ABBREVS = {
    "Smg": "Semarang",
    "Sby": "Surabaya",
    "Bdg": "Bandung",
    "Mdn": "Medan",
    "Mks": "Makassar",
    "Jkt.Pst": "Jakarta Pusat",
    "Jkt.Sel": "Jakarta Selatan",
    "Jkt.Bar": "Jakarta Barat",
    "Jkt.Tim": "Jakarta Timur",
    "Jkt.Ut": "Jakarta Utara",
    "Dps": "Denpasar",
    "Bjm": "Banjarmasin",
    "Ptk": "Pontianak",
    "Plg": "Palembang",
    "Pbr": "Pekanbaru",
    "Pdg": "Padang",
    "Kpg": "Kupang",
    "Mtr": "Mataram",
    "Smr": "Samarinda",
    "Jmb": "Jambi",
    "Bgl": "Bengkulu",
    "Amb": "Ambon",
    "Mnd": "Manado",
    "Jpr": "Jayapura",
    "Srg": "Serang",
    "Yyk": "Yogyakarta",
    "Tjk": "Tanjung Karang",
}


def _expand_court_abbrev(abbrev: str) -> str:
    """Expand court abbreviation to full city name."""
    return _COURT_ABBREVS.get(abbrev, abbrev)
