"""Download and extract text from PDF verdict documents."""

from io import BytesIO
from pathlib import Path

from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

from src.config import PDF_DIR
from src.scraper.base import ScraperSession


def download_pdf(session: ScraperSession, pdf_url: str,
                 verdict_id: str) -> Path | None:
    """Download a PDF file. Returns path or None on failure."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = verdict_id.replace("/", "_").replace("\\", "_")
    path = PDF_DIR / f"{safe_name}.pdf"

    if path.exists():
        return path

    resp = session.get_safe(pdf_url)
    if resp is None:
        return None

    path.write_bytes(resp.content)
    return path


def extract_pdf_text(pdf_path: Path) -> str | None:
    """Extract text from a PDF file. Returns text or None if extraction fails."""
    try:
        text = extract_text(str(pdf_path))
        if text and text.strip():
            return text.strip()
        return None  # Empty text = likely scanned PDF
    except (PDFSyntaxError, Exception):
        return None


def is_scanned_pdf(pdf_path: Path) -> bool:
    """Check if a PDF is scanned (image-based) by trying text extraction."""
    text = extract_pdf_text(pdf_path)
    if text is None:
        return True
    # Heuristic: scanned PDFs have very little extractable text
    return len(text) < 100


def process_pdf(session: ScraperSession, pdf_url: str,
                verdict_id: str) -> dict:
    """Download and extract text from a PDF.

    Returns dict with keys: pdf_path, pdf_text, is_scanned, error
    """
    result = {
        "pdf_path": None,
        "pdf_text": None,
        "is_scanned": None,
        "error": None,
    }

    path = download_pdf(session, pdf_url, verdict_id)
    if path is None:
        result["error"] = "download_failed"
        return result

    result["pdf_path"] = str(path)

    text = extract_pdf_text(path)
    if text is None:
        result["is_scanned"] = True
        result["error"] = "no_text_extracted"
    else:
        result["pdf_text"] = text
        result["is_scanned"] = len(text) < 100
        if result["is_scanned"]:
            result["error"] = "likely_scanned"

    return result
