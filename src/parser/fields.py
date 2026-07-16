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

# Page-footer variant: "Dalam hal Anda menemukan inakurasi ... Telp : 021-384
# 3348 (ext.318) ... Halaman N dari N halaman Putusan Nomor ...". This block
# splits amar sentences mid-number at page breaks (holdout R3, 10690 K/2025).
_MA_FOOTER_RE = re.compile(
    r'\f?\s*dalam hal anda menemukan inakurasi[\s\S]{0,400}?'
    r'\(ext\.\s*318\)\s*'
    # page markers, longest variant first so "halaman N" never eats the
    # start of "halaman N dari M halaman putusan nomor <case-no>"; the case
    # number = 1-2 tokens, bounded so the regex never eats the resumed amar
    r'(?:(?:halaman\s+\d+\s+dari\s+\d+\s+halaman\s+putusan\s+nomor\s*'
    r'[\w./-]+(?:\s+[\w./-]+)?|halaman\s+\d+)\s*)*',
    re.IGNORECASE,
)


# Old-style page marker ("Hal.20dari55hal. Put. No. 692 K/PID.SUS/2015"),
# printed on every page of older PDFs and merged mid-sentence into amar text.
# The case-number tail is tightly bounded (\d{4} year) so merged text that
# follows it ("...2015PUTUSANNOMOR...") is never eaten.
_MA_PAGEMARK_RE = re.compile(
    r'hal\.\s*\d+\s*dari\s*\d+\s*hal\.?\s*put\.?\s*no\.?\s*'
    r'\d+\s*[a-z]{1,3}[./][\w.]+/\d{4}',
    re.IGNORECASE,
)


def _strip_watermark(text: str) -> str:
    """Remove MA watermark/disclaimer blocks from PDF text."""
    text = _MA_WATERMARK_RE.sub(' ', text)
    text = _MA_FOOTER_RE.sub(' ', text)
    return _MA_PAGEMARK_RE.sub(' ', text)


# Left-context markers indicating a prison term is a SUBSIDIARY clause
# (imprisonment in lieu of unpaid uang pengganti), not the primary sentence.
# Keep narrow & specific — generic words (denda) appear in legitimate amars.
_SUBSIDIARY_BLOCKERS = (
    "uang pengganti", "tidak membayar", "tidak dibayar",
    "kurungan pengganti", "diganti dengan pidana", "diganti pidana",
    "tidak mencukupi",
)


def _is_subsidiary_context(text_lower: str, pos: int, window: int = 120) -> bool:
    """True if the penjara match at pos sits in a subsidiary-penalty clause.

    Window is deliberately tight: the trigger phrase ("apabila uang pengganti
    tidak dibayar ... diganti dengan pidana penjara") sits in the same clause;
    a wide window bleeds in the PREVIOUS numbered item of an amar list.

    "subsidair/subsidiair/subsider" marks a subsidiary PENALTY — except in
    "dakwaan subsidiair", which is a CHARGE tier and must not block.
    """
    left = text_lower[max(0, pos - window):pos]
    # A blocker phrase is void if an amar-item boundary follows it inside the
    # window: "memperbaiki ... pidana uang pengganti menjadi sebagai berikut:
    # 1. menjatuhkan pidana ... penjara 2 tahun" lists uang pengganti among
    # the CORRECTED items — the sentence after the reset is primary, not
    # subsidiary (holdout R2 bug 11256 K/PID.SUS/2025).
    _reset = re.compile(r'sebagai\s*berikut|menjatuhkan|menghukum')
    for b in _SUBSIDIARY_BLOCKERS:
        i = left.rfind(b)
        if i >= 0 and not _reset.search(left, i + len(b)):
            return True
    for m in re.finditer(r'subsid[a-z]*', left):
        if 'dakwaan' in left[max(0, m.start() - 12):m.start()]:
            continue
        if not _reset.search(left, m.end()):
            return True
    return False


def is_tipikor_document(text: str) -> bool:
    """Domain filter: does this verdict concern corruption at all?

    Guards against non-tipikor Pid.Sus cases (narcotics, etc.) leaking into
    the corpus via the global scrape (DECISIONS.md D15).
    """
    if not text:
        return False
    tl = text.lower()
    markers = ("korupsi", "tipikor", "31 tahun 1999", "20 tahun 2001",
               "pemberantasan tindak pidana korupsi")
    return any(m in tl for m in markers)


def _find_penjara(text_lower: str, exclude_subsidiary: bool = True) -> float | None:
    """Find prison sentence duration in a text fragment.

    Handles both spaced ("penjara selama 8 tahun") and merged
    ("penjara selama8 (delapan) Tahun") text from PN catatan_amar.
    Skips subsidiary clauses (imprisonment in lieu of unpaid uang pengganti)
    unless exclude_subsidiary=False.
    """
    # Tahun [dan bulan] — \s* allows merged text; "masing-masing" handles
    # multi-defendant amars ("penjara masing-masing selama 4 tahun")
    for m in re.finditer(
        r'(?:pidana\s+)?penjara\s*(?:masing-masing\s*)?(?:selama\s*|menjadi\s*)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s*(?:dan\s*)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        text_lower,
    ):
        if exclude_subsidiary and _is_subsidiary_context(text_lower, m.start()):
            continue
        years = int(m.group(1))
        months = int(m.group(2)) if m.group(2) else 0
        return years * 12 + months

    # Bulan only
    for m in re.finditer(
        r'(?:pidana\s+)?penjara\s*(?:masing-masing\s*)?(?:selama\s*|menjadi\s*)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
        text_lower,
    ):
        if exclude_subsidiary and _is_subsidiary_context(text_lower, m.start()):
            continue
        return float(m.group(1))

    return None


def _is_full_acquittal(section: str) -> bool:
    """True if section contains a FULL acquittal amar.

    "Membebaskan ... dari dakwaan primair" alone is a PARTIAL acquittal
    (conviction on subsidiair follows); "primair dan subsidiair" or
    "semua/seluruh dakwaan" (or no qualifier) is a full acquittal.
    """
    m = re.search(r'(?:membebaskan|melepaskan)\s+(?:para\s+)?(?:terdakwa|terpidana)', section)
    if not m:
        return False
    after = section[m.start():m.start() + 400]
    # Spelling varies: "primair"/"primer"/"pertama"; an ordinal may intervene
    # ("dakwaan KESATU primair" — holdout R3, 2892 K/2024)
    # No trailing \b: merged text ("dakwaan primairpenuntut umum") is common
    if re.search(r'dakwaan\s+(?:\w+\s+)?(?:prim(?:air|er)|pertama)', after) \
            and not re.search(
                r'prim(?:air|er)\s+dan\s+(?:dakwaan\s+)?subsid'
                r'|semua\s+dakwaan|seluruh\s+dakwaan',
                after):
        return False
    return True


def _find_all_mengadili(text_lower: str) -> list[int]:
    """Find all MENGADILI section positions in text."""
    positions = []
    # Variants: spaced header, colon, newline, merged-with-hyphen
    # ("MENGADILI-Menolak"), and fully merged with the first amar verb
    # ("mengadilimenolak..." — holdout R2, 2305 K/Pid.Sus/2016). "sendiri" is
    # deliberately NOT in the verb lookahead: "mengadili sendiri" appears in
    # prose/dissent argument, not as a header.
    for pat in [r'm\s+e\s+n\s+g\s+a\s+d\s+i\s+l\s+i', r'mengadili\s*:',
                r'mengadili\s*\n', r'mengadili\s*[-–—]',
                r'mengadili\s*(?=menolak|mengabulkan|menyatakan|membebaskan'
                r'|memperbaiki|menguatkan|menerima|menghukum|menjatuhkan'
                r'|membatalkan|menetapkan)']:
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
    # Use 10000 char window (PN catatan_amar can have long merged text)
    section = text_lower[start:end] if end else text_lower[start:start + 10000]

    # Priority: "menjatuhkan/menghukum pidana ... penjara selama X tahun".
    # Bounded [\s\S] gap tolerates "kepada/terhadap Terdakwa <nama+gelar>";
    # subsidiary clauses (uang pengganti) are skipped via context check.
    for m in re.finditer(
        r'(?:menjatuhkan|menghukum)\s*pidana[\s\S]{0,150}?'
        r'penjara\s*(?:selama\s*|menjadi\s*)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s*(?:dan\s*)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        section,
    ):
        if _is_subsidiary_context(section, m.start(1)):
            continue
        years = int(m.group(1))
        months = int(m.group(2)) if m.group(2) else 0
        return years * 12 + months

    # Bulan only in sentencing context
    for m in re.finditer(
        r'(?:menjatuhkan|menghukum)\s*pidana[\s\S]{0,150}?'
        r'penjara\s*(?:selama\s*|menjadi\s*)?'
        r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
        section,
    ):
        if _is_subsidiary_context(section, m.start(1)):
            continue
        return float(m.group(1))

    return None


def _find_quoted_lower_court_sentence(text_lower: str, mengadili_pos: int) -> float | None:
    """Find the lower court sentence quoted before the MA MENGADILI section.

    When MA says "Menolak permohonan kasasi", the lower court sentence stands.
    The MA verdict quotes the PN/PT amar putusan earlier in the text, typically
    near patterns like "Putusan Pengadilan Negeri/Tinggi X" or "amar putusannya".
    We search backwards from the MENGADILI position.
    """
    # Search the WHOLE text before the MENGADILI section for quoted court
    # decisions — in long documents (large dakwaan sections) the quoted amar
    # can sit 100k+ chars before the MA amar. The closest decision quote with
    # an extractable sentence wins, so early procedural mentions are harmless.
    search_text = text_lower[:mengadili_pos]

    # Quoted decision references, in chain order: the LAST (closest to
    # MENGADILI) quoted decision is the one whose amar stands when MA rejects.
    # Includes "putusan mahkamah agung" — in PK documents the standing amar is
    # the prior kasasi decision, not PN/PT. Requiring "Nomor" nearby filters
    # out party REQUESTS ("amar sebagai berikut...") that quote no decision.
    court_patterns = [
        r'putusan\s*(?:pengadilan\s*(?:negeri|tinggi|tipikor|tindak\s*pidana)'
        r'|mahkamah\s*agung)[\s\S]{0,120}?nomor',
    ]

    best_result = None
    best_pos = -1

    for pat in court_patterns:
        for m in re.finditer(pat, search_text):
            # Skip quotes of what a party REQUESTED (JPU memori kasasi:
            # "memohon agar ... menjatuhkan pidana ...") — not a decision.
            # Tight window: the request verb directly precedes "putusan";
            # wider windows catch verbs from unrelated preceding sentences.
            req_left = search_text[max(0, m.start() - 60):m.start()]
            if any(w in req_left for w in ("supaya", "memohon", "menuntut agar",
                                           "mohon agar", "agar kiranya")):
                continue
            section = search_text[m.start():m.start() + 2000]
            # Skip COMPANION-case citations: a quoted decision "atas nama
            # terpidana/terdakwa X" where X is not a party named in the
            # document head belongs to someone else's chain (holdout R3,
            # 2960 PK/2025 quoting a comparator defendant's sentence).
            an = re.search(
                r'atas\s+nama\s+(?:para\s+)?(?:terpidana|terdakwa)\s+([^;]{0,60})',
                section[:400],
            )
            if an:
                # First plain-alphabetic word >=4 chars = the name's core
                # (skips titles like "ir."/"h."/"s.t." which carry dots)
                words = [w.strip('.,') for w in an.group(1).split()]
                words = [w for w in words if len(w) >= 4 and w.isalpha()]
                core = words[0] if words else ""
                # Party-identity block = text before the first "membaca"
                # (the reading list); a name absent there is another case's
                head_end = text_lower.find('membaca')
                head = text_lower[:head_end if 0 < head_end < 4000 else 4000]
                if core and core not in head:
                    continue
            found = None
            # FULL acquittal amar first — the 2000-char window can reach past
            # a bebas amar into quoted tuntutan text with penjara numbers
            if _is_full_acquittal(section):
                found = 0
            # "Memperbaiki ... menjadi ... penjara X" inside the quoted amar:
            # the corrected value is the standing one
            fm = None if found is not None else re.search(
                r'memperbaiki[\s\S]{0,400}?menjadi[\s\S]{0,200}?'
                r'penjara(?:[\s\S]{0,80}?selama)?\s*'
                r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
                r'(?:\s*(?:dan\s*)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
                section)
            if fm and not _is_subsidiary_context(section, fm.start(1)):
                found = int(fm.group(1)) * 12 + (int(fm.group(2)) if fm.group(2) else 0)
            if found is None:
                for pm in re.finditer(
                    r'(?:menjatuhkan|menghukum|dijatuhi)\s*pidana[\s\S]{0,300}?penjara'
                    r'(?:[\s\S]{0,80}?selama|\s*menjadi)?\s*'
                    r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
                    r'(?:\s*(?:dan\s*)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
                    section,
                ):
                    if _is_subsidiary_context(section, pm.start(1)):
                        continue
                    years = int(pm.group(1))
                    months = int(pm.group(2)) if pm.group(2) else 0
                    found = years * 12 + months
                    break
            # A quoted FULL acquittal amar counts as sentence 0
            if found is None and _is_full_acquittal(section):
                found = 0
            if found is not None and m.start() > best_pos:
                best_result = found
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
    section = text_lower[mengadili_pos:mengadili_pos + 8000]
    m = re.search(r'memperbaiki\s+putusan', section)
    if not m:
        return None
    memperbaiki_text = section[m.start():]
    # Priority: the corrected value follows "menjadi" ("...menjadi pidana
    # penjara selama X tahun") — most specific signal of the NEW sentence
    mj = re.search(
        r'menjadi[\s\S]{0,200}?penjara(?:[\s\S]{0,80}?selama)?\s*'
        r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
        r'(?:\s*(?:dan\s*)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
        memperbaiki_text,
    )
    if mj and not _is_subsidiary_context(memperbaiki_text, mj.start(1)):
        years = int(mj.group(1))
        months = int(mj.group(2)) if mj.group(2) else 0
        return years * 12 + months
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

    # Page-break watermark blocks can interrupt an amar mid-sentence
    text_lower = _strip_watermark(text).lower()

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

        # 1d. Menolak (kasasi rejected) / Menguatkan (banding affirmed): the
        #     standing sentence is the QUOTED lower-court amar, NOT a previous
        #     MENGADILI section (which may be a superseded PN/PT verdict).
        #     Acquittal-upheld handled here too. "Menguatkan" covers PT-level
        #     documents whose amar only affirms (holdout R2, 8/PID.TPK/2026).
        last_section = text_lower[last_pos:last_pos + 500]
        if 'menolak' in last_section[:300] or 'menguatkan' in last_section[:300]:
            result = _find_quoted_lower_court_sentence(text_lower, last_pos)
            if result is not None:
                return result
            # JPU kasasi against an acquittal, rejected → acquittal stands.
            # The acquitted amar may be quoted anywhere (often page 2), so scan
            # the whole text; skip REQUEST phrasings (pledoi "memohon ... agar
            # membebaskan"). Partial bebas (primair-only) is filtered by
            # _is_full_acquittal.
            before = text_lower[:last_pos + 2000]
            for bm in re.finditer(
                r'(?:membebaskan|melepaskan)[\s\S]{0,40}?(?:terdakwa|terpidana)',
                before,
            ):
                left = before[max(0, bm.start() - 200):bm.start()]
                if any(w in left for w in ("memohon", "supaya", "agar ", "menuntut")):
                    continue
                if _is_full_acquittal(before[bm.start():bm.start() + 400]):
                    return 0

        # 1e. Acquittal in the MA's own amar
        if _is_full_acquittal(text_lower[last_pos:last_pos + 5000]):
            return 0

        # 1f. Previous MENGADILI section (only when not a menolak/menguatkan
        #     case — otherwise this returns the superseded lower-court figure)
        if 'menolak' not in last_section[:300] \
                and 'menguatkan' not in last_section[:300] \
                and len(mengadili_positions) >= 2:
            prev_pos = mengadili_positions[-2]
            result = _extract_mengadili_sentence(text_lower, prev_pos, last_pos)
            if result is not None:
                return result

        # 1g. General penjara sweep in MENGADILI sections (subsidiary-aware)
        for pos in reversed(mengadili_positions):
            result = _find_penjara(text_lower[pos:pos + 5000])
            if result is not None:
                return result

    # Strategy 2: Search in the first 500 chars (catatan_amar prefix from pipeline)
    prefix = text_lower[:500]
    result = _find_penjara(prefix)
    if result is not None:
        return result

    # Strategy 3: Use the LAST non-subsidiary penjara match in the full text
    all_matches = [
        m for m in re.finditer(
            r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
            r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
            r'(?:\s+(?:dan\s+)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
            text_lower,
        ) if not _is_subsidiary_context(text_lower, m.start())
    ]
    if all_matches:
        m = all_matches[-1]
        years = int(m.group(1))
        months = int(m.group(2)) if m.group(2) else 0
        return years * 12 + months

    all_matches = [
        m for m in re.finditer(
            r'(?:pidana\s+)?penjara\s+(?:selama\s+|menjadi\s+)?'
            r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
            text_lower,
        ) if not _is_subsidiary_context(text_lower, m.start())
    ]
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

    # Strategy 1: Find "tuntutan pidana" section headers, then search within
    # next 2500 chars for a NON-SUBSIDIARY penjara. Kasasi PDFs quote full
    # tuntutan as a numbered list; the subsidiary clause ("...jika uang
    # pengganti tidak dibayar, dipidana penjara 1 tahun") must be skipped.
    # Iterate over ALL headers — the first may be a passing reference.
    for tuntutan_header in re.finditer(r'tuntutan\s+pidana', text_lower):
        section = text_lower[tuntutan_header.start():tuntutan_header.start() + 4000]
        # 1a. Canonical demand amar, which may OMIT the word "penjara"
        # ("Menjatuhkan pidana terhadap Terdakwa X ... selama 6 tahun dan
        # 4 bulan") — holdout bug 12367 K/PID.SUS/2025. The gap covers the
        # defendant's name/titles; reject if a non-prison penalty type or a
        # subsidiary clause sits inside it.
        for m in re.finditer(
            r'menjatuhkan\s+pidana\s+(?:terhadap|kepada)\s*(.{0,150}?)selama\s*'
            r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
            r'(?:\s*(?:dan\s*)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
            section,
        ):
            gap = m.group(1)
            if any(w in gap for w in ("denda", "kurungan", "pengganti", "percobaan")):
                continue
            if _is_subsidiary_context(section, m.start()):
                continue
            years = int(m.group(2))
            months = int(m.group(3)) if m.group(3) else 0
            return years * 12 + months

        # 1b. Allow up to 150 chars between "penjara" and "selama" to skip
        # defendant names; \s* (not \s+) tolerates merged PDF text
        # ("penjara selama6(enam)tahun")
        for m in re.finditer(
            r'(?:pidana\s*)?penjara\s*(?:.{0,150}?selama\s*)?'
            r'(\d+)\s*(?:\([^)]+\)\s*)?tahun'
            r'(?:\s*(?:dan\s*)?(\d+)\s*(?:\([^)]+\)\s*)?bulan)?',
            section,
        ):
            if _is_subsidiary_context(section, m.start()):
                continue
            years = int(m.group(1))
            months = int(m.group(2)) if m.group(2) else 0
            return years * 12 + months

        for m in re.finditer(
            r'(?:pidana\s*)?penjara\s*(?:.{0,150}?selama\s*)?'
            r'(\d+)\s*(?:\([^)]+\)\s*)?bulan',
            section,
        ):
            if _is_subsidiary_context(section, m.start()):
                continue
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

    # Contexts where an Rp figure near "kerugian" is NOT the established loss:
    # restitution (uang pengganti), partial repayment, payment orders.
    blockers = ("uang pengganti", "pengembalian", "mengembalikan", "dikembalikan",
                "menyetor", "dititipkan", "membayar", "pembayaran",
                # bribe/gratuity amounts are not state-loss figures
                "hadiah", "gratifikasi berupa")
    # Contexts marking the audited/established loss figure
    audit_anchors = ("laporan hasil audit", "hasil audit", "penghitungan kerugian",
                     "bpkp", "inspektorat", "badan pemeriksa keuangan", "akuntan")

    # A figure directly preceded by comparative/threshold language is a legal
    # bound (e.g. the Pasal 2/3 Rp100jt boundary: "telah melebihi jumlah
    # Rp100.000.000,00 yakni sebesar Rp1,98M"), not the established loss.
    threshold_terms = ("melebihi", "lebih dari", "kurang dari", "di atas",
                       "di bawah", "paling sedikit", "paling banyak",
                       "minimal", "maksimal", "setidak-tidaknya")

    # Tier 2: the court's own summing conclusion ("Dengan demikian ...
    # merugikan keuangan negara sebesar RpX") outranks component figures
    # cited from audit items (holdout R2 bug 1107 PK/Pid.Sus/2024).
    conclusion_pattern = (
        r'dengan\s*demikian[\s\S]{0,120}?'
        r'merugikan\s*(?:keuangan\s*)?negara\s*sebesar\s*rp\.?\s*([\d.,]+)'
    )

    patterns = [
        # [^.;] — clause-bound: crossing ';' bled a doctrinal "kerugian"
        # mention into a bribe amount (holdout R2 bug 438 K/Pid.Sus/2021)
        r'(?:kerugian|merugikan)\s+(?:keuangan\s+)?negara[^.;]{0,100}?'
        r'rp\.?\s*([\d.,]+)',
        r'kerugian[^.;]{0,200}?rp\.?\s*([\d.,]+)',
        # "sebesar Rp" is a strong anchor, so the gap may safely cross
        # abbreviation periods ("Cq. Dinas...", "c.q. PT Antam") that break
        # the [^.] gaps above — holdout bugs 1009 K/2013, 27 K/2026.
        # \s* (not \s+) tolerates merged PDF text ("keuangannegara...
        # tomohonsebesarrp59.700.000,00"). Gap 300: long project names
        # (holdout R2 bug 1682 K/Pid.Sus/2021, gap ~225).
        r'(?:kerugian|merugikan)\s*(?:keuangan\s*)?negara'
        r'[\s\S]{0,300}?sebesar\s*rp\.?\s*([\d.,]+)',
    ]

    # Collect ALL candidates (first match is often a restitution recap);
    # decide by tier (conclusion > audit-anchored > plain), then by how often
    # a value is repeated.
    candidates = []  # (amount, position, tier)
    seen_pos = set()
    for tier_boost, pattern in [(2, conclusion_pattern)] + [(0, p) for p in patterns]:
        for m in re.finditer(pattern, text_lower):
            if m.start(1) in seen_pos:
                continue
            seen_pos.add(m.start(1))
            left = text_lower[max(0, m.start() - 150):m.start()]
            if any(b in left or b in m.group(0) for b in blockers):
                continue
            fig_left = text_lower[max(0, m.start(1) - 35):m.start(1)]
            if any(t in fig_left for t in threshold_terms):
                continue
            amount = _parse_rupiah(m.group(1))
            if not amount or amount <= 0:
                continue
            ctx = text_lower[max(0, m.start() - 250):m.end() + 250]
            tier = tier_boost or (1 if any(a in ctx for a in audit_anchors) else 0)
            candidates.append((amount, m.start(), tier))

    if not candidates:
        return None

    top = max(t for _, _, t in candidates)
    pool = [c for c in candidates if c[2] == top]
    counts: dict[float, int] = {}
    for amount, _, _ in pool:
        counts[amount] = counts.get(amount, 0) + 1
    best_count = max(counts.values())
    modal = {a for a, c in counts.items() if c == best_count}
    for amount, _, _ in pool:  # earliest occurrence among modal values
        if amount in modal:
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
            # Malformed cents separator: "3.308.079.265.127.04" — a final
            # 2-digit group cannot be a thousands group (always 3 digits)
            if len(parts[-1]) == 2:
                cleaned = "".join(parts[:-1]) + "." + parts[-1]
            else:
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
    # Merged PDF text can glue SEVERAL words to the city name
    # ("Padangpadatanggal") — strip suffixes repeatedly until stable
    stripped = True
    while stripped:
        stripped = False
        lower = name.lower()
        for suffix in known_suffixes:
            if lower.endswith(suffix) and len(lower) > len(suffix) + 2:
                candidate = name[:len(name) - len(suffix)]
                if len(candidate) >= 3:
                    name = candidate
                    stripped = True
                    break
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
        # Page-break watermarks can interrupt the court phrase mid-sentence
        text = _strip_watermark(text)
        # Function words that regex fragments sometimes capture as a "city"
        blocklist = {"dalam", "yang", "pada", "tersebut", "negeri", "tinggi",
                     "telah", "untuk", "dengan", "sebagai", "kelas", "direktori"}

        # Priority: the Tipikor trial venue ("Tindak Pidana Korupsi pada
        # Pengadilan Negeri X") — beats other PN mentions (asal terdakwa etc.)
        for pat in [
            r'Tindak\s+Pidana\s+Korupsi\s+pada\s+Pengadilan\s+Negeri\s+'
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:Pengadilan\s+(?:Negeri|Tindak\s+Pidana\s+Korupsi(?:\s+pada\s+Pengadilan\s+Negeri)?)\s+)'
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]:
            for m in re.finditer(pat, text):
                cleaned = _clean_daerah(m.group(1).strip())
                if cleaned and cleaned.lower() not in blocklist and len(cleaned) >= 3:
                    return cleaned

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


def extract_pertimbangan_text(text: str) -> str | None:
    """Extract judicial reasoning section from verdict text.

    Looks for text between 'Menimbang' (or 'PERTIMBANGAN HUKUM') and 'MENGADILI'.
    Returns None if section is too short (<200 chars) or not found.
    """
    if not text:
        return None

    text_lower = text.lower()

    # Find start: 'pertimbangan hukum' or first 'menimbang'
    start = -1
    for marker in ['pertimbangan hukum', 'menimbang']:
        idx = text_lower.find(marker)
        if idx >= 0:
            start = idx
            break
    if start < 0:
        return None

    # Find end: 'M E N G A D I L I' or 'MENGADILI'
    end = -1
    for pattern in [r'M\s*E\s*N\s*G\s*A\s*D\s*I\s*L\s*I', r'MENGADILI']:
        m = re.search(pattern, text[start:])
        if m:
            end = start + m.start()
            break
    if end < 0:
        return None

    section = text[start:end].strip()

    # Minimum length filter
    if len(section) < 200:
        return None

    # Normalize whitespace
    section = re.sub(r'\s+', ' ', section).strip()
    return section
