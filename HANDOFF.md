# Handoff — Fase 1 Session 4 → Session 5

## Status: **Fase 1 — Corpus Building in progress**

148 verdicts scraped, 102 with PDF (100% download success). Parser re-run with all fixes applied. Paper 1 outline drafted.

## What Was Done (Session 4)

### 1. Second Scrape Run (Success)
- Added 53 new verdicts (95 → 148 total) from pages 1,4,5,6
- 28 new PDFs downloaded (100% success rate)
- Total: 102 verdicts with PDF, 46 HTML-only
- Confirmed: pagination non-deterministic (multi-run strategy works)

### 2. Full Re-Parse with Fixed Extractors
All 148 verdicts re-parsed with:
- MENGADILI section strategy for vonis (fixed tuntutan/vonis confusion)
- "Tuntutan Pidana" section header for tuntutan
- `_clean_daerah()` for PDF text artifacts
- Expanded COURT_REGION_MAP

**Updated numbers (148 verdicts):**
```
P0 Fields:
  vonis_bulan      69.6%  (103/148)  GO
  kerugian_negara  60.8%   (90/148)  GO
  daerah           84.5%  (125/148)  GO
  tahun            87.2%  (129/148)  GO
  P0 Average:      75.5%            GO

  Joint P0 (all):  58.8%  (87/148)  — below 60% due to HTML-only verdicts
  Joint P0 (PDF):  83.3%  (85/102)  — true quality metric

P1 Fields:
  tuntutan_bulan   27.7%   (41/148)
  pasal            71.6%  (106/148)
  nama_terdakwa    58.8%   (87/148)

P2 Fields:
  nama_hakim       87.2%  (129/148)
  nama_jaksa        1.4%    (2/148)
```

**Critical insight:** PDF-parsed verdicts are 83.3% joint P0 vs 4.3% for HTML-only. For Fase 1 corpus, should ONLY count PDF-parsed verdicts as usable.

### 3. Statistical Analysis (102 PDF-parsed verdicts)
Key findings for Paper 1:

| Metric | Value |
|--------|-------|
| Mean sentence | 4.2 years (50.1 months) |
| Median sentence | 4.0 years (48 months) |
| Range | 1.0 — 15.0 years |
| Median kerugian | Rp 2.07 billion |
| Max kerugian | Rp 300 trillion (PT Timah Tbk — verified real) |
| Mean discount ratio | 54.9% (vonis/tuntutan) |
| Median discount | 50.0% |
| Pearson r (log_kerugian vs vonis) | 0.44 (moderate positive) |

**Vonis by kerugian bracket:**
| Kerugian Bracket | Mean Vonis | n |
|-----------------|------------|---|
| <100M | 3.1 years | 7 |
| 100M-1B | 3.6 years | 28 |
| 1B-10B | 3.9 years | 28 |
| 10B-100B | 5.3 years | 15 |
| >100B | 8.4 years | 7 |

**By primary charge (UU 31/1999):**
| Article | Mean Vonis | n | Notes |
|---------|-----------|---|-------|
| Pasal 2 (kerugian negara) | 4.1 yr | 75 | Dominant (76%) |
| Pasal 3 (penyalahgunaan) | 5.8 yr | 4 | Small n |
| Pasal 11/12 (suap) | 3.1 yr | 9 | Lightest sentences |

**Discount by region (n≥2):**
- Medan/Padang: ~36-40% ratio (biggest discounts)
- Jakarta Pusat: 53% ratio
- Makassar: 61% ratio (least discount)

**Notable cases:**
- 2 cases where vonis > tuntutan (rare — legally interesting)
- 4 mega-corruption cases (kerugian > Rp 1T), all Jakarta Pusat
- PT Timah Tbk: Rp 300T kerugian includes Rp 271T environmental damage

### 4. Golden Set Framework (Ready for Human)
- Template at `data/golden_set/golden_template.csv` (20 verdicts)
- Validation script at `scripts/05_validate_golden.py`
- Needs human annotation: read PDFs, fill `human_*` columns
- Script computes per-field precision/recall/F1 with error examples

### 5. Paper 1 Outline (Drafted)
- At `reports/paper1_outline.md`
- Title: "CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Decisions and Sentencing Patterns"
- 9 sections, 3 research questions, 7 planned figures
- Targets: LREC-COLING, ACL Resource track

### 6. Code Changes
| File | Change |
|------|--------|
| `src/parser/fields.py` | MENGADILI 3-strategy vonis extractor, _clean_daerah() |
| `src/parser/normalizer.py` | +8 court-region mappings |
| `scripts/05_validate_golden.py` | New: golden set validation |
| `reports/paper1_outline.md` | New: Paper 1 outline |

## What Needs To Be Done (Session 5)

### Step 1: Golden Set Annotation (HUMAN TASK — CRITICAL)
- Read 20 PDFs manually
- Fill human_* columns in `data/golden_set/golden_template.csv`
- Run `python -m scripts.05_validate_golden`
- Target: >80% accuracy per P0 field

### Step 2: Scale Scraping
- Run scraper on pages 7-20+ (multi-run, different days)
- Target: 500+ verdicts with PDFs
- Download all PDFs immediately after scraping
- Parse after each batch

### Step 3: Improve Extraction
Based on golden set results, fix top error patterns:
- tuntutan_bulan at 27.7% — needs more regex patterns for kasasi format variations
- nama_terdakwa at 58.8% — need better name extraction from kasasi headers
- pasal classification — improve primary article identification

### Step 4: Paper 1 Draft
- Fill in outline with real numbers
- Generate figures (histograms, scatter plots, maps)
- Write methodology section
- Ethics section re: public data

### Step 5: Pre-registration
- Register hypotheses on OSF before running full analysis
- Key hypotheses: kerugian-vonis relationship, geographic variation, temporal trends

## Known Issues
- HTML-only verdicts (46/148) are effectively useless — 4.3% joint P0
- Pasal classification misses 86/99 cases (fall to "Other") — extractor returns raw numbers without "Pasal" prefix
- Temporal coverage skewed to 2024-2026 (recency bias from MA listing)
- nama_jaksa effectively impossible from kasasi data (1.4%)
- Need upsert for re-scraping (currently INSERT OR IGNORE)
- Pagination non-deterministic — must do 3-5 scrape runs

## Key Research Constraint
**ALL data is MA kasasi/PK decisions — biased toward appealed cases.** First-instance PN Tipikor verdicts are not available at scale on the MA website. All research designs must account for this selection bias explicitly.
