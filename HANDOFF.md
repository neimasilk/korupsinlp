# Handoff — Fase 1 Session 4 → Session 5

## Status: **Fase 1 — Corpus Building in progress**

205 verdicts scraped, 182 PDFs downloaded (100% success), 103 PDF-parsed so far. 80 new PDFs awaiting re-parse. Major parser improvements and new field (pemohon_kasasi) added.

## What Was Done (Session 4)

### 1. Scraping Scaled (148 → 205 verdicts)
- Second scrape run: pages 1,4,5,6 → 53 new verdicts
- Third scrape run: pages 7-15 → 57 new verdicts (detail scrape interrupted mid-way by MA server slowness)
- 80 new PDFs downloaded (100% success rate, total 182 PDFs)
- **80 new PDFs need re-parsing** (script 03 must be run next session)

### 2. Critical Parser Fix: Tuntutan Extraction (27.7% → 64.2%)
Three fixes combined:
1. **Window expansion**: 800 → 2500 chars after "Tuntutan Pidana" header (kasasi PDFs have long pasal citations before the sentence)
2. **MA watermark stripping**: PDF pages contain ~500 chars of Direktori Putusan disclaimer that inflates offsets. New `_strip_watermark()` regex removes these globally in pipeline
3. **Defendant name tolerance**: "penjara terhadap Terdakwa [NAME] selama X tahun" — regex now allows up to 150 chars between "penjara" and "selama" to skip defendant names

Result: tuntutan_bulan went from 27.7% (41/148) to 64.2% (95/148) on old dataset.

### 3. New Field: pemohon_kasasi (Who Filed the Appeal)
- Extracts "dimohonkan oleh Terdakwa/Penuntut Umum" from PDF header
- DB column added, extractor in `fields.py`, wired in pipeline
- **Major finding on 102 PDF-parsed verdicts:**
  - 52% kasasi filed by JPU (Penuntut Umum) — prosecutors wanting harsher sentences
  - 40% filed by Terdakwa (defendant)
  - 8% unknown
- **This is a confounding variable** — JPU vs terdakwa kasasi are fundamentally different processes

### 4. Research Critique & Findings

**Sentencing by pemohon kasasi (suggestive, not yet significant):**

| Pemohon | Mean Vonis | Mean Ratio (v/t) | n |
|---------|-----------|------------------|---|
| JPU | 4.5 yr | 79.9% | 43-52 |
| Terdakwa | 3.6 yr | 63.7% | 38-40 |

Welch's t-test: t=1.04, p>0.05 (need more data to confirm)

**Kerugian-vonis correlation:** r=0.44 (moderate positive, n=85)

| Kerugian Bracket | Mean Vonis | n |
|-----------------|------------|---|
| <100M | 3.1 yr | 7 |
| 100M-1B | 3.6 yr | 28 |
| 1B-10B | 3.9 yr | 28 |
| 10B-100B | 5.3 yr | 15 |
| >100B | 8.4 yr | 7 |

**PT Timah Rp300T verified real** — includes Rp271T environmental damage.

**Risks identified (research critique):**
1. Selection bias deeper than acknowledged — 52% are JPU kasasi (upward vonis bias)
2. H1 (Disproporsionalitas) not testable without mitigating/aggravating factor extraction
3. Discount analysis needs stratification by pemohon_kasasi
4. Paper venue: target LREC-COLING, not main ACL (regex pipeline insufficient novelty for main track)
5. Manifesto over-scope: kill H2/H3/H5/H6 until Paper 1 published

### 5. Watermark Stripping (Global)
- `_strip_watermark()` added to `fields.py` — removes MA disclaimer blocks
- Applied globally in `pipeline.py` before all extractors
- Improves all field extraction on PDF text

### 6. Tests Expanded (25 → 34 tests, all passing)
New tests for:
- `extract_pemohon_kasasi` (terdakwa, JPU, PK terpidana)
- `_strip_watermark` (with/without watermark)
- Tuntutan with defendant name between penjara/selama
- MENGADILI section vonis strategy
- Last-match fallback for vonis

### 7. Paper 1 Outline (Drafted)
At `reports/paper1_outline.md`:
- "CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Decisions and Sentencing Patterns"
- 3 RQs, 9 sections, 7 planned figures
- pemohon_kasasi finding as novel contribution

### 8. Code Changes
| File | Change |
|------|--------|
| `src/parser/fields.py` | +`_strip_watermark()`, +`extract_pemohon_kasasi()`, tuntutan window 800→2500, regex `.{0,150}?` for defendant names |
| `src/parser/pipeline.py` | Global watermark stripping, +pemohon_kasasi extraction |
| `src/db.py` | +`pemohon_kasasi TEXT` column |
| `scripts/03_parse_sample.py` | +pemohon_kasasi in update_data |
| `tests/test_parser.py` | +9 new tests (34 total) |
| `reports/paper1_outline.md` | New: Paper 1 outline |
| `scripts/05_validate_golden.py` | New: golden set validation |
| `scripts/download_pdfs.py` | New: batch PDF download |

## CRITICAL: First Thing Next Session

```bash
source .venv/Scripts/activate
python -m scripts.03_parse_sample    # Re-parse all 205 with new PDFs
python -m scripts.04_feasibility_report
```

This will parse the 80 new PDFs that were downloaded but not yet processed.

## What Needs To Be Done (Session 5)

### Step 1: Re-parse (IMMEDIATE)
Run script 03 to parse the 80 new PDFs. Expected: ~182 PDF-parsed verdicts (up from 103).

### Step 2: Golden Set Annotation (HUMAN TASK)
- Template at `data/golden_set/golden_template.csv`
- Read 20 PDFs manually, fill `human_*` columns
- Run `python -m scripts.05_validate_golden`
- Target: >80% accuracy per P0 field

### Step 3: Continue Scaling
- Scrape pages 16-30+ (third run was interrupted at detail scraping)
- Target: 500+ verdicts with PDFs
- Each page yields ~20 new verdicts

### Step 4: Improve Extraction
- nama_terdakwa at 58.8% — needs better PDF header parsing
- Vonis > tuntutan outliers (10 cases) — verify with golden set
- Extract mitigating/aggravating factors from pertimbangan hakim (needed for H1)

### Step 5: Paper 1 Draft
- Fill in outline with updated numbers from 200+ verdicts
- Generate figures (histograms, scatter, maps)
- Pemohon kasasi as novel contribution
- Write methodology + limitations sections

## Known Issues
- 80 new PDFs not yet parsed (must run script 03 first)
- 10 cases where vonis > tuntutan — some are extraction errors, some real (JPU kasasi)
- MA server extremely slow on detail pages (97-200s response time)
- nama_jaksa effectively impossible from kasasi data (1.4%)
- Temporal coverage skewed to 2024-2026
- Pasal classification needs improvement (76% classified as "Other")

## Key Research Constraint
**ALL data is MA kasasi/PK decisions.** 52% are JPU kasasi (prosecutor appeal for harsher sentence), 40% terdakwa kasasi. This selection must be controlled for in all analysis. Geographic and sentencing patterns must be stratified by pemohon_kasasi.
