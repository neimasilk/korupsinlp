# Handoff — Session 10 → Session 11

## Status: **Autoresearch Complete — Honest Negative Finding on Text Features**

Dataset migrated from old machine, autoresearch framework exercised with 30+ experiments, cross-validation reveals text features do NOT improve prediction. Corpus scaling is the clear next priority.

## What Was Done (Session 10)

### 1. Dataset Migrated from Old Machine
- Extracted `inbox/korupsinlp.7z` → restored 557 verdicts, 429 PDFs, 616 raw HTML
- Fixed DB paths from old machine (`C:\Users\Amien.DESKTOP-MHGA6EC\`) to current
- Extracted pertimbangan text from PDFs: **349/367 (95.1%)**, mean 5,535 chars
- 69 tests passing

### 2. Autoresearch: 30+ Experiments on Text Features
Branch: `autoresearch/apr9-textfeatures`

**Progression of kept experiments:**
| # | val_r2 | Change |
|---|--------|--------|
| 1 | 0.546 | Baseline: TF-IDF(5000, bigrams) + tuntutan, Ridge(1.0) |
| 4 | 0.568 | max_features=200 (beats tuntutan-only baseline!) |
| 5 | 0.569 | max_features=100 |
| 7 | 0.576 | Unigrams only (bigrams = noise) |
| 11 | 0.580 | +kerugian_negara (text_all mode) |
| 18 | **0.622** | Ridge alpha=0.1 — BEATS BASELINE |
| 21 | **0.626** | Ridge alpha=0.05 — BEST SINGLE SPLIT |

**Key diagnosis**: Initial setup (5000 features, alpha=1.0) was overfitting badly (p >> n). Reducing to 100 features + lower alpha unlocked the improvement.

**What was tried and didn't work**: Lasso, ElasticNet, HuberRegressor, RandomForest, GradientBoosting, stopword removal, keyword counts, SVD compression, text truncation, binary TF-IDF.

### 3. Cross-Validation Reveals Overfit (CRITICAL)
5x10-fold repeated CV on the best model:

| Model | CV Mean R² | vs Baseline |
|-------|-----------|-------------|
| M9 baseline (fixed) | 0.532 | — |
| Ridge tuntutan only | 0.522 | -0.010 |
| **Best text model (a=0.05)** | **0.460** | **-0.072** |
| Best text model (a=10) | 0.513 | -0.019 |

**Text features significantly HURT in CV** (p < 0.0001, help in only 22% of folds). No alpha value makes text break even with baseline.

### 4. Feature Importance (Descriptive)
Despite not helping prediction, sensible word associations found:
- **Heavier sentences**: miliar (r=+0.23), negara (+0.19), keuangan (+0.15)
- **Lighter sentences**: kasasi (r=-0.15)
- These are proxies for case magnitude, already captured by structured features

### 5. Documentation Updated
- Paper 2 outline rewritten around honest negative finding
- EKSEKUSI updated with autoresearch results
- GTD inbox emptied (korupsinlp.7z + autoresearch inspiration processed)

## CRITICAL: First Thing Next Session

```bash
source .venv/Scripts/activate
python -m pytest tests/ -q                # Should be 69 passed
python -m autoresearch.train              # Should show val_r2 ~ 0.626
python -m autoresearch.cv_analysis        # Full CV analysis
```

## Current Branch State
- On branch: `autoresearch/apr9-textfeatures` (not merged to main)
- 12 commits ahead of main
- `autoresearch/results.tsv` is gitignored (30 experiment records)

## Data State (9 April 2026)
| Metric | Count |
|--------|-------|
| Total verdicts | 559 |
| Parsed | 518 |
| Pertimbangan text (>=200ch) | 349 |
| Analysis-ready (vonis+tuntutan+text) | 288 |
| PDFs | 429 |
| Raw HTML | 557 |

## What Needs To Be Done (Session 11)

### Priority 1: Scale Corpus (MOST IMPORTANT)
288 analysis-ready verdicts is too small for NLP. Need 1000+.
- Resume scraping: `python -m scripts.02_scrape_sample --count 500 --start-page 15`
- After scraping: `python -m scripts.03_parse_sample` then `python -m scripts.09_extract_pertimbangan`
- Re-run `python -m autoresearch.cv_analysis` on larger corpus

### Priority 2: Paper 1 Submission
- Draft is submission-ready since Session 9
- Needs final proofread and consistency check
- Target venue: ACL/EMNLP Resource track or LREC-COLING

### Priority 3: Paper 2 Draft
- Outline updated in `reports/paper2_outline.md`
- Narrative: "honest negative result" — text features don't help at n=288
- Write draft once corpus is scaled and re-tested

### Optional: Try PN Tipikor Courts
- `src/config.py` has PN_COURT_SLUGS (Bandung, Jakarta, Surabaya, etc.)
- PN verdicts have fuller text than MA kasasi decisions
- Change `COURT_SLUGS = PN_COURT_SLUGS` in config to scrape first-instance

## Known Issues
- 41 verdicts unparsed (HTML exists but not parsed — parsing was interrupted)
- `src/db.py` may need `migrate_db()` updates — DB has all columns via manual ALTER TABLE
- Autoresearch branch has not been merged to main (deliberate — experimental)
