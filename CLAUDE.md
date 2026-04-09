# KorupsiNLP — CLAUDE.md

## Project Overview
Computational analysis of Indonesian corruption court verdicts (putusan tipikor).
Currently in **Fase 1: Corpus Building + Sentencing Analysis** — Paper 1 submission-ready.

## Architecture
```
src/config.py          — URLs, paths, delays, thresholds
src/db.py              — SQLite schema + CRUD
src/scraper/base.py    — HTTP session (SSL off, retry, rate-limit)
src/scraper/listing.py — Paginated listing scraper (direktori index)
src/scraper/detail.py  — Individual verdict metadata extraction
src/scraper/pdf_extractor.py — PDF download + text extraction
src/parser/fields.py   — Regex extractors per field (including pertimbangan)
src/parser/normalizer.py — Currency, duration, court→region
src/parser/pipeline.py — Orchestrate parsing
src/analysis/feasibility.py — Compute success rates, GO/NO-GO
scripts/01-09          — Sequential execution scripts
autoresearch/          — Autonomous experiment framework (see below)
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
python -m scripts.09_extract_pertimbangan  # Extract judicial reasoning text
python -m autoresearch.train               # Run one autoresearch experiment
```

## Autoresearch (Autonomous Experiment Framework)
Adapted from Andrej Karpathy's autoresearch concept for text feature experiments.

```
autoresearch/
├── program.md         — Research policy (human-written, agent reads each cycle)
├── prepare.py         — READ-ONLY: data loading, splits, evaluation metric
├── train.py           — MUTABLE: the only file the agent modifies
├── analyze_results.py — Post-experiment analysis & plots
└── results.tsv        — Experiment log (gitignored)
```

**How it works:**
1. Agent reads `program.md` for rules and goals
2. Agent modifies `train.py` (text preprocessing, features, model, hyperparams)
3. Agent commits the change
4. Agent runs `python -m autoresearch.train` and parses output
5. If val_r2 improved → keep commit. If not → git reset.
6. Repeat indefinitely (~100 experiments overnight)

**Key metric:** `val_r2` — must beat baseline 0.600 (tuntutan-only M9).
**Branch convention:** `autoresearch/<tag>` (e.g., `autoresearch/phase1-tfidf`)

## GTD Inbox Workflow
Uses GTD (Getting Things Done) by David Allen. The `inbox/` directory at project root
holds unprocessed reference materials, ideas, and inspirations.

**Processing rule:** Every item must be processed — extract insights, integrate into
the project, document where relevant — then delete the original. Inbox must be empty
after processing. Processed items are tracked in git commit messages.
