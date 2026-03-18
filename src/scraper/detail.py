"""Scrape individual verdict detail pages."""

import json
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from src.config import BASE_URL, RAW_DIR
from src.scraper.base import ScraperSession


# Metadata field mapping: label text → dict key
FIELD_MAP = {
    "Nomor": "case_number",
    "Tingkat Proses": "tingkat_proses",
    "Klasifikasi": "classification",
    "Sub Klasifikasi": "sub_classification",
    "Kata Kunci": "kata_kunci",
    "Tahun": "tahun_register",
    "Tanggal Register": "tanggal_register",
    "Lembaga Peradilan": "lembaga_peradilan",
    "Jenis Lembaga Peradilan": "jenis_lembaga",
    "Hakim Ketua": "hakim_ketua",
    "Hakim Anggota": "hakim_anggota",
    "Panitera": "panitera",
    "Amar": "amar",
    "Catatan Amar": "catatan_amar",
    "Tanggal Musyawarah": "tanggal_musyawarah",
    "Tanggal Dibacakan": "tanggal_dibacakan",
    "Kaidah": "kaidah",
    "Status": "status",
    "Tanggal Upload": "tanggal_upload",
}


def extract_metadata(html: str) -> dict:
    """Extract metadata fields from a verdict detail page.

    Adapted from okkymabruri/putusan field extraction patterns.
    """
    soup = BeautifulSoup(html, "lxml")
    metadata = {}

    # Pattern 1: Table rows with label-value pairs
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).rstrip(":")
                value = cells[-1].get_text(strip=True)
                if label in FIELD_MAP and value:
                    metadata[FIELD_MAP[label]] = value

    # Pattern 2: Definition list (dl/dt/dd)
    for dl in soup.find_all("dl"):
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")
        for dt, dd in zip(dts, dds):
            label = dt.get_text(strip=True).rstrip(":")
            value = dd.get_text(strip=True)
            if label in FIELD_MAP and value:
                metadata[FIELD_MAP[label]] = value

    # Extract PDF link
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        if href.endswith(".pdf") or "/pdf/" in href:
            metadata["pdf_url"] = urljoin(BASE_URL, href)
            break

    # Extract the full text content (for parser)
    content_div = soup.find("div", class_=["entry-content", "content", "detail-putusan"])
    if content_div:
        metadata["full_text"] = content_div.get_text(separator="\n", strip=True)

    return metadata


def save_html(html: str, verdict_id: str) -> Path:
    """Save raw HTML to disk."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = verdict_id.replace("/", "_").replace("\\", "_")
    path = RAW_DIR / f"{safe_name}.html"
    path.write_text(html, encoding="utf-8")
    return path


def scrape_detail(session: ScraperSession, url: str) -> dict | None:
    """Scrape a single verdict detail page.

    Returns metadata dict or None on failure.
    """
    resp = session.get_safe(url)
    if resp is None:
        return None

    metadata = extract_metadata(resp.text)
    metadata["url"] = url

    # Save raw HTML using case number or URL hash as ID
    verdict_id = metadata.get("case_number", str(hash(url)))
    html_path = save_html(resp.text, verdict_id)
    metadata["html_path"] = str(html_path)

    return metadata
