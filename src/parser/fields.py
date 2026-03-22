"""Regex extractors for key verdict fields."""

import re

# MA watermark/disclaimer text injected into PDF pages — strip to avoid
# breaking character-window-based extraction
_MA_WATERMARK_RE = re.compile(
    r'Direktori Putusan Mahkamah Agung Republik Indonesia\s*'
    r'putusan\.mahkamahagung\.go\.id\s*'
    r'(?:Mahkamah Agung Republik Indonesia\s*){0,5}'
    r'(?:Disclaimer\s*Kepaniteraan.*?(?:heli\.telepon@telepon\.co\.id|pelaksanaan fungsi peradilan\.)\s*'
    r'(?:Namun dalam hal-hal tertentu.*?\n)?)?',
    re.DOTALL,
)


def _strip_watermark(text: str) -> str:
    """Remove MA watermark/disclaimer blocks from PDF text."""
    return _MA_WATERMARK_RE.sub(' ', text)


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


def _find_all_mengadili(text_lower: str) -> list[int]:
    """Find all MENGADILI section positions in text."""
    positions = []
    for pat in [r'm\s+e\s+n\s+g\s+a\s+d\s+i\s+l\s+i', r'mengadili\s*:', r'mengadili\s*\n']:
        for m in re.finditer(pat, text_lower):
            # Don't add duplicates (close positions from different patterns)
            if not any(abs(m.start() - p) < 50 for p in positions):
                positions.append(m.start())
    return sorted(positions)


def _extract_mengadili_sentence(text_lower: str, start: int, end: int | None = None) -> float | None:
    """Extract prison sentence from a bounded MENGADILI section.

    Only extracts from "menjatuhkan pidana...penjara" pattern to avoid
    picking up subsidiary penalties or quoted sentences.
    """
    section = text_lower[start:end] if end else text_lower[start:start + 5000]

    # Priority: "menjatuhkan pidana...penjara selama X tahun"
    m = re.search(
        r'menjatuhkan\s+pidana\s+(?:kepada\s+terdakwa\s+)?'
        r'(?:oleh\s+karena\s+itu\s+)?(?:dengan\s+)?'
        r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        section,
    )
    if m:
        years = int(m.group(1))
        months = int(m.group(2)) if m.group(2) else 0
        return years * 12 + months

    # Bulan only in sentencing context
    m = re.search(
        r'menjatuhkan\s+pidana\s+(?:kepada\s+terdakwa\s+)?'
        r'(?:oleh\s+karena\s+itu\s+)?(?:dengan\s+)?'
        r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
        section,
    )
    if m:
        return float(m.group(1))

    return None


def _find_quoted_lower_court_sentence(text_lower: str, mengadili_pos: int) -> float | None:
    """Find the lower court sentence quoted before the MA MENGADILI section.

    When MA says "Menolak permohonan kasasi", the lower court sentence stands.
    The MA verdict quotes the PN/PT amar putusan earlier in the text, typically
    near patterns like "Putusan Pengadilan Negeri/Tinggi X" or "amar putusannya".
    We search backwards from the MENGADILI position.
    """
    # Search the text before the MENGADILI section for quoted court decisions
    # Look in the last 30,000 chars before MENGADILI (PN amar is typically quoted
    # in the case narrative)
    search_start = max(0, mengadili_pos - 30000)
    search_text = text_lower[search_start:mengadili_pos]

    # Find all "Putusan Pengadilan" references with subsequent penjara sentences
    court_patterns = [
        r'putusan\s+pengadilan\s+(?:negeri|tinggi|tindak\s+pidana)',
        r'amar\s+putusan(?:nya)?\s+(?:sebagai\s+berikut|adalah|berbunyi)',
    ]

    best_result = None
    best_pos = -1

    for pat in court_patterns:
        for m in re.finditer(pat, search_text):
            section = search_text[m.start():m.start() + 2000]
            pm = re.search(
                r'(?:menjatuhkan|menghukum)\s+pidana.*?penjara\s+'
                r'(?:selama\s+|menjadi\s+)?'
                r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
                r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
                section,
            )
            if pm and m.start() > best_pos:
                years = int(pm.group(1))
                months = int(pm.group(2)) if pm.group(2) else 0
                best_result = years * 12 + months
                best_pos = m.start()

    return best_result


def _find_sendiri_sentence(text_lower: str, mengadili_pos: int) -> float | None:
    """Find sentence in MENGADILI SENDIRI subsection within an MENGADILI section.

    MA verdicts often have nested subsections:
    M E N G A D I L I → Mengabulkan → MENGADILI SENDIRI → actual sentence
    or: M E N G A D I L I → ... → MENGADILI KEMBALI → MENGADILI SENDIRI → sentence
    """
    section = text_lower[mengadili_pos:mengadili_pos + 10000]
    # Find the LAST "mengadili sendiri" in the section (the MA's own)
    sendiri_matches = list(re.finditer(r'mengadili\s+sendiri', section))
    if not sendiri_matches:
        return None
    sendiri_pos = sendiri_matches[-1].start()
    sendiri_text = section[sendiri_pos:sendiri_pos + 5000]
    return _find_penjara(sendiri_text)


def _find_memperbaiki_sentence(text_lower: str, mengadili_pos: int) -> float | None:
    """Find sentence in Memperbaiki section within an MENGADILI section.

    When MA says "Memperbaiki Putusan X mengenai pidana...menjadi pidana penjara
    selama Y tahun", the modified sentence follows "menjadi".
    """
    section = text_lower[mengadili_pos:mengadili_pos + 5000]
    m = re.search(r'memperbaiki\s+putusan', section)
    if not m:
        return None
    memperbaiki_text = section[m.start():]
    return _find_penjara(memperbaiki_text)


def extract_vonis_bulan(text: str) -> float | None:
    """Extract prison sentence in months from verdict text.

    For kasasi PDFs, the text contains multiple MENGADILI sections:
    1. Lower court (PN) MENGADILI — the original verdict
    2. Appeals court (PT) MENGADILI — if applicable
    3. Supreme Court (MA) MENGADILI — the cassation decision

    Strategy (in priority order):
    1. Strict "menjatuhkan pidana...penjara" in last MENGADILI section
    2. MENGADILI SENDIRI subsection within last MENGADILI
    3. Memperbaiki subsection within last MENGADILI
    4. Previous MENGADILI section (for simple kasasi-ditolak)
    5. Quoted lower court sentence (last resort for menolak-only)
    6. General penjara sweep in MENGADILI sections
    7. Acquittal detection (membebaskan/melepaskan → 0)
    8. Fallback to catatan_amar prefix, then last-match in full text
    """
    if not text:
        return None

    text_lower = text.lower()

    # Strategy 1: Find all MENGADILI sections, use the correct one
    mengadili_positions = _find_all_mengadili(text_lower)

    if mengadili_positions:
        last_pos = mengadili_positions[-1]

        # 1a. Strict "menjatuhkan pidana" in last MENGADILI (5000 char window)
        result = _extract_mengadili_sentence(text_lower, last_pos)
        if result is not None:
            return result

        # 1b. MENGADILI SENDIRI subsection (handles nested sections,
        #     dual-kasasi cases where both menolak+mengabulkan appear)
        result = _find_sendiri_sentence(text_lower, last_pos)
        if result is not None:
            return result

        # 1c. Memperbaiki section (MA modifies specific aspect of sentence)
        result = _find_memperbaiki_sentence(text_lower, last_pos)
        if result is not None:
            return result

        # 1d. Previous MENGADILI section (simple kasasi-ditolak)
        if len(mengadili_positions) >= 2:
            prev_pos = mengadili_positions[-2]
            result = _extract_mengadili_sentence(text_lower, prev_pos, last_pos)
            if result is not None:
                return result

        # 1e. Quoted lower court sentence (menolak without memperbaiki)
        last_section = text_lower[last_pos:last_pos + 500]
        if 'menolak' in last_section[:200]:
            result = _find_quoted_lower_court_sentence(text_lower, last_pos)
            if result is not None:
                return result

        # 1f. General penjara sweep in MENGADILI sections
        for pos in reversed(mengadili_positions):
            result = _find_penjara(text_lower[pos:pos + 5000])
            if result is not None:
                return result

        # 1g. Acquittal detection
        acquittal_section = text_lower[last_pos:last_pos + 5000]
        if re.search(r'(?:membebaskan|melepaskan)\s+(?:terdakwa|terpidana)', acquittal_section):
            return 0

    # Strategy 2: Search in the first 500 chars (catatan_amar prefix from pipeline)
    prefix = text_lower[:500]
    result = _find_penjara(prefix)
    if result is not None:
        return result

    # Strategy 3: Use the LAST penjara match in the full text
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
    # next 2500 chars for penjara. Kasasi PDFs quote full tuntutan as numbered
    # list with long pasal citations before the sentence. Window must be large
    # enough to skip past "1. Menyatakan..." (pasal citations) to reach
    # "2. Menjatuhkan pidana penjara..."
    tuntutan_header = re.search(r'tuntutan\s+pidana', text_lower)
    if tuntutan_header:
        section = text_lower[tuntutan_header.start():tuntutan_header.start() + 2500]
        # Allow up to 150 chars between "penjara" and "selama" to skip
        # defendant names: "penjara terhadap Terdakwa X selama 2 tahun"
        m = re.search(
            r'(?:pidana\s+)?penjara\s+(?:.{0,150}?selama\s+)?'
            r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
            r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
            section,
        )
        if m:
            years = int(m.group(1))
            months = int(m.group(2)) if m.group(2) else 0
            return years * 12 + months

        m = re.search(
            r'(?:pidana\s+)?penjara\s+(?:.{0,150}?selama\s+)?'
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


def _clean_nama(name: str) -> str | None:
    """Clean extracted defendant name: strip titles, trim, validate."""
    name = name.strip().rstrip(",;.")
    # Remove leading dots (PDF artifact from merged text)
    name = name.lstrip(".")
    # Remove leading/trailing whitespace again
    name = name.strip()
    if len(name) < 3:
        return None
    return name


def extract_nama_terdakwa(text: str) -> str | None:
    """Extract defendant name from verdict text.

    Strategy order:
    1. Structured PDF header: "Nama : FULL_NAME;" (most reliable)
    2. Merged PDF header (no spaces): "Nama:FULL_NAME;"
    3. MA kasasi format: "VS NAMA (Terdakwa)"
    4. Standard: "Terdakwa NAMA"
    5. "atas nama NAMA"
    """
    if not text:
        return None

    # Strategy 1: Structured PDF header — "Nama  : FULL_NAME;"
    # This is the identity block at the top of every MA kasasi PDF.
    # Handles "Nama : X bin Y;" or "Nama : X, S.H., binti Y;"
    # Also handles "Nama lengkap : X;" variant
    # Terminated by semicolon before "Tempat Lahir" or "Tempat lahir"
    m = re.search(
        r'Nama\s*(?:lengkap\s*)?:\s*(.+?)\s*;\s*(?:Tempat\s*[Ll]ahir|TempatLahir)',
        text,
    )
    if m:
        name = _clean_nama(m.group(1))
        if name:
            return name

    # Strategy 2: Merged PDF text (no spaces between tokens)
    # e.g., "Nama:.SANDRAMARIATUN,S.H.,bintiH.HENDROMARTONO;"
    m = re.search(
        r'Nama:\.?([^;]{3,80});(?:TempatLahir|Tempat)',
        text,
    )
    if m:
        name = _clean_nama(m.group(1))
        if name:
            return name

    # Strategy 3: MA kasasi format: "Penuntut Umum VS NAMA_TERDAKWA (Terdakwa)"
    m = re.search(
        r'VS\s+(.+?)\s*\(Terdakwa\)',
        text,
    )
    if m:
        name = _clean_nama(m.group(1))
        if name:
            return name

    # Strategy 4: Standard: "Terdakwa NAMA"
    m = re.search(
        r'(?:terdakwa|Terdakwa)\s*:?\s*([A-Z][A-Z\s.,]+?)(?:\s*(?:bin|binti|als|alias)\s|[,;]|\s{2,})',
        text,
    )
    if m:
        name = _clean_nama(m.group(1))
        if name:
            return name

    # Strategy 5: "atas nama NAMA"
    m = re.search(
        r'atas\s+nama\s+([A-Z][A-Z\s.,]+?)(?:\s*(?:bin|binti|als|alias)\s|[,;]|\s{2,})',
        text,
    )
    if m:
        name = _clean_nama(m.group(1))
        if name:
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


def extract_pemohon_kasasi(text: str) -> str | None:
    """Extract who filed the kasasi/PK appeal.

    Returns 'terdakwa', 'penuntut_umum', or None.
    Critical for interpreting sentencing data — JPU kasasi means prosecutor
    thought sentence was too light (upward bias), terdakwa kasasi means
    defendant thought it was too heavy (downward bias).
    """
    if not text:
        return None

    cleaned = _strip_watermark(text)
    text_lower = cleaned.lower()[:5000]  # Only check header area

    # Kasasi/PK: "dimohonkan oleh Terdakwa/Terpidana/Penuntut Umum"
    # Handle merged PDF text: "dimohonkanoleh" or "olehterdakwa"
    m = re.search(
        r'(?:dimohonkan|diajukan)\s*oleh\s*(terdakwa|terpidana|penuntut\s*umum)',
        text_lower,
    )
    if m:
        who = m.group(1).strip()
        return 'penuntut_umum' if 'penuntut' in who else 'terdakwa'

    # Broader: "kasasi yang dimohonkan oleh" with possible line breaks
    m = re.search(
        r'kasasi\s+yang\s+dimohonkan\s*oleh\s*(terdakwa|terpidana|penuntut\s*umum)',
        text_lower,
    )
    if m:
        who = m.group(1).strip()
        return 'penuntut_umum' if 'penuntut' in who else 'terdakwa'

    # PK variant: "peninjauan kembali yang dimohonkan oleh"
    m = re.search(
        r'peninjauan\s*kembali\s+yang\s+dimohonkan\s*oleh\s*(terdakwa|terpidana|penuntut\s*umum)',
        text_lower,
    )
    if m:
        who = m.group(1).strip()
        return 'penuntut_umum' if 'penuntut' in who else 'terdakwa'

    return None


def extract_faktor_pertimbangan(text: str) -> dict:
    """Extract aggravating (memberatkan) and mitigating (meringankan) factors.

    MA kasasi verdicts may either:
    1. List factors explicitly: "Hal-hal yang memberatkan: - factor1; - factor2"
    2. Reference factors in summary: "telah mempertimbangkan keadaan yang
       memberatkan dan meringankan"
    3. Quote the lower court's factor list verbatim

    Returns dict with 'memberatkan' and 'meringankan' as lists of strings,
    plus 'has_factors' boolean indicating whether explicit factors were found.
    """
    result = {"memberatkan": [], "meringankan": [], "has_factors": False}
    if not text:
        return result

    cleaned = _strip_watermark(text)

    result["memberatkan"] = _extract_factor_list(cleaned, "memberatkan")
    result["meringankan"] = _extract_factor_list(cleaned, "meringankan")

    result["has_factors"] = bool(result["memberatkan"] or result["meringankan"])
    return result


def _extract_factor_list(text: str, factor_type: str) -> list[str]:
    """Extract a list of factors of given type from text.

    Looks for patterns like:
    - "Hal-hal yang memberatkan: - factor1; - factor2;"
    - "Keadaan yang memberatkan: 1. factor1; 2. factor2;"
    """
    text_lower = text.lower()

    header_patterns = [
        rf'(?:hal[- ]hal|keadaan)\s+yang\s+{factor_type}\s*:',
        rf'{factor_type}\s*:',
    ]

    for pat in header_patterns:
        m = re.search(pat, text_lower)
        if not m:
            continue

        start = m.end()
        # End at the other factor type header, or "Menimbang", or "MENGADILI"
        other_type = "meringankan" if factor_type == "memberatkan" else "memberatkan"
        end_patterns = [
            rf'(?:hal[- ]hal|keadaan)\s+yang\s+{other_type}',
            r'menimbang',
            r'm\s*e\s*n\s*g\s*a\s*d\s*i\s*l\s*i',
            r'mengingat',
            r'demikianlah',
        ]
        end = start + 2000
        for ep in end_patterns:
            em = re.search(ep, text_lower[start:start + 2000])
            if em:
                end = min(end, start + em.start())

        section = text[start:end]

        # Split by bullet/number delimiters
        factors = re.split(r'\s*(?:[-•]\s+|\d+\.\s+|;\s*[-•\d])', section)
        cleaned = []
        for f in factors:
            f = f.strip().rstrip(";.,")
            if len(f) > 10 and re.search(r'[a-zA-Z]', f):
                if len(f) > 300:
                    f = f[:300] + "..."
                cleaned.append(f)
        if cleaned:
            return cleaned

    return []
