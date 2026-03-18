# KorupsiNLP — CLAUDE.md

## Project Overview
Computational analysis of Indonesian corruption court verdicts (putusan tipikor).
Currently in **Fase 0: Feasibility Study** — can we scrape and parse the data?

## Architecture
```
src/config.py          — URLs, paths, delays, thresholds
src/db.py              — SQLite schema + CRUD
src/scraper/base.py    — HTTP session (SSL off, retry, rate-limit)
src/scraper/listing.py — Paginated listing scraper (direktori index)
src/scraper/detail.py  — Individual verdict metadata extraction
src/scraper/pdf_extractor.py — PDF download + text extraction
src/parser/fields.py   — Regex extractors per field
src/parser/normalizer.py — Currency, duration, court→region
src/parser/pipeline.py — Orchestrate parsing
src/analysis/feasibility.py — Compute success rates, GO/NO-GO
scripts/01-04          — Sequential execution scripts
```

## Data Source
- Website: `putusan3.mahkamahagung.go.id`
- SSL verify=False required (certificate issues)
- URL pattern: `/direktori/index/pengadilan/{slug}/kategori/korupsi-1/page/{n}.html`
- Detail: `/direktori/putusan/{hash}.html`
- PDF: `/direktori/download_file/{hash}/pdf/{hash}`
- ~53 verdicts per listing page, 420+ pages at MA level

## Key Conventions
- Python 3.10+, dependencies in pyproject.toml
- SQLite DB at `data/korupsinlp.db`
- Raw HTML saved to `data/raw/`, PDFs to `data/pdf/`
- `data/` is gitignored
- REQUEST_DELAY=2s, REQUEST_TIMEOUT=90s, polite sequential scraping
- Tests: `pytest tests/`

## Running
```bash
source .venv/Scripts/activate  # Windows Git Bash
python -m scripts.01_test_connection
python -m scripts.02_scrape_sample --count 100 --start-page 5
python -m scripts.03_parse_sample
python -m scripts.04_feasibility_report
```
