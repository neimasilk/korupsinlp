"""Orchestrate parsing of verdict data."""

import json
from datetime import datetime

from src.parser.fields import (
    extract_vonis_bulan,
    extract_tuntutan_bulan,
    extract_kerugian_negara,
    extract_pasal,
    extract_nama_terdakwa,
    extract_tahun,
    extract_daerah,
    extract_pemohon_kasasi,
    _strip_watermark,
)
from src.parser.normalizer import court_to_province


def parse_verdict(metadata: dict, text: str | None = None) -> dict:
    """Parse all fields from a verdict's metadata and text.

    Args:
        metadata: Dict from detail page scraping (HTML metadata fields).
        text: Full text content (from HTML or PDF).

    Returns:
        Dict with parsed fields and parse_errors list.
    """
    errors = []
    result = {}

    # Use full_text from metadata if no text provided
    if text is None:
        text = metadata.get("full_text", "")

    # Combine text sources for extraction
    combined = text or ""
    amar = metadata.get("amar", "")
    catatan_amar = metadata.get("catatan_amar", "")
    if amar:
        combined = amar + "\n" + combined
    if catatan_amar:
        combined = catatan_amar + "\n" + combined

    # Strip MA watermark/disclaimer from PDF text — these blocks inflate
    # character offsets and break window-based extraction
    combined = _strip_watermark(combined)

    # === P0 Fields ===

    # Vonis (prison sentence in months)
    result["vonis_bulan"] = extract_vonis_bulan(combined)
    if result["vonis_bulan"] is None:
        errors.append("vonis_bulan: not found")

    # Kerugian negara (state loss in Rupiah)
    result["kerugian_negara"] = extract_kerugian_negara(combined)
    if result["kerugian_negara"] is None:
        errors.append("kerugian_negara: not found")

    # Daerah (region)
    result["daerah"] = extract_daerah(combined, metadata)
    if result["daerah"] is None:
        errors.append("daerah: not found")

    # Tahun (year)
    result["tahun"] = extract_tahun(combined, metadata)
    if result["tahun"] is None:
        errors.append("tahun: not found")

    # === P1 Fields ===

    # Tuntutan (prosecution demand in months)
    result["tuntutan_bulan"] = extract_tuntutan_bulan(combined)
    if result["tuntutan_bulan"] is None:
        errors.append("tuntutan_bulan: not found")

    # Pasal (charged articles)
    result["pasal"] = extract_pasal(combined)
    if result["pasal"] is None:
        errors.append("pasal: not found")

    # Nama terdakwa
    result["nama_terdakwa"] = extract_nama_terdakwa(combined)
    if result["nama_terdakwa"] is None:
        # Try from metadata
        result["nama_terdakwa"] = metadata.get("nama_terdakwa")
        if result["nama_terdakwa"] is None:
            errors.append("nama_terdakwa: not found")

    # === P2 Fields ===

    # Nama hakim (from metadata)
    hakim_parts = []
    if metadata.get("hakim_ketua"):
        hakim_parts.append(metadata["hakim_ketua"])
    if metadata.get("hakim_anggota"):
        hakim_parts.append(metadata["hakim_anggota"])
    result["nama_hakim"] = "; ".join(hakim_parts) if hakim_parts else None
    if result["nama_hakim"] is None:
        errors.append("nama_hakim: not found")

    # Nama jaksa — usually not in metadata, need text extraction
    result["nama_jaksa"] = _extract_jaksa(combined)
    if result["nama_jaksa"] is None:
        errors.append("nama_jaksa: not found")

    # Pemohon kasasi — who filed the appeal (terdakwa vs penuntut_umum)
    result["pemohon_kasasi"] = extract_pemohon_kasasi(combined)

    # === Derived fields ===
    if result["daerah"]:
        result["provinsi"] = court_to_province(result["daerah"])

    # Parse source
    result["parse_source"] = "html"
    result["parse_errors"] = json.dumps(errors)
    result["parsed_at"] = datetime.now().isoformat()

    return result


def _extract_jaksa(text: str) -> str | None:
    """Extract prosecutor name from verdict text."""
    import re

    if not text:
        return None

    m = re.search(
        r'(?:jaksa|penuntut\s+umum)\s*:?\s*([A-Z][A-Za-z\s.,]+?)(?:[,;]|\s{2,}|$)',
        text,
    )
    if m:
        name = m.group(1).strip().rstrip(",;.")
        if len(name) > 3:
            return name

    return None
