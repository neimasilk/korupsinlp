# Handoff — Session 11 → Session 12

## Status: **Structured Text Features Beat TF-IDF; PN Data Blocked; Scraping Needed**

Major pivot from TF-IDF to domain-specific structured features yields first positive CV result. PN courts discovered to be unusable (no tuntutan in HTML). MA site unreliable today — scraping must retry.

## What Was Done (Session 11)

### 1. Critical Analysis & Research Design Review
Comprehensive critique of project blind spots, weak assumptions, and structural risks:
- MA selection bias more severe than acknowledged (only appealed cases)
- 9 planned papers is too many for solo researcher → recommended kill/merge
- Only H1 and H2 testable with current data
- `extract_faktor_pertimbangan()` was never used as features → fixed

### 2. Structured Text Features (BREAKTHROUGH)
**Pivoted from TF-IDF (30 experiments, all failed) to domain-specific keyword features:**

Phase progression:
| Approach | CV R² | vs Baseline | p-value | Status |
|----------|-------|-------------|---------|--------|
| TF-IDF best (α=0.05) | 0.460 | -0.072 | <0.0001 | SIGNIFICANTLY WORSE |
| TF-IDF moderate (α=10) | 0.513 | -0.019 | 0.027 | Still worse |
| All 16 structured features | 0.498 | +0.007 | 0.69 | Neutral |
| **Minimal: pasal_2 + gratifikasi** | **0.521** | **+0.030** | **0.055** | **Marginally significant** |

**Key findings:**
- Exhaustive feature subset search over 11 keyword features
- Only 2 features matter: `has_pasal_2` (charge type) and `has_gratifikasi` (crime type)
- Adding ANY other feature hurts or doesn't help
- Alpha=50 optimal (strong regularization prevents overfit at n=288)
- Text-derived pasal_2 >> structured pasal column (operative vs listed charges)

### 3. PN Data Investigation (BLOCKED)
- Verified PN court slugs work (pn-surabaya has 344+ verdicts for 2024)
- **CRITICAL DISCOVERY: PN HTML detail pages only publish MENGADILI section**
  - NO tuntutan, NO kerugian, NO pertimbangan text
  - NO PDF downloads for PN verdicts
  - PN verdicts CANNOT be used for regression analysis
- Parser fixed for PN merged text (selama8 → selama 8)
- Added `court_level` column to DB (ma/pn/pt)
- 2 PN verdicts scraped as proof-of-concept

### 4. Outlier Analysis
- 40 cases (13.2%) where judge gave MORE than prosecution asked
- Extreme cases: 2000% "discount" (Bandung), 400% (Jakarta Pusat)
- Extreme lenience: 3% discount (Tanjungkarang), 6% (Semarang)
- Outlier concentration: Tanjungkarang 40%, Semarang 30%, Palembang 25%

### 5. Infrastructure
- court_level column added to verdicts table
- All existing verdicts tagged as 'ma'
- Scraping script updated to set court_level from slug
- Parser merged text handling improved
- 69 tests passing

## CRITICAL: First Thing Next Session

```bash
source .venv/Scripts/activate  # or use conda
python -m pytest tests/ -q                # 69 passed
python -m autoresearch.train              # Should show cv_improvement ~ +0.023
```

Then retry MA scraping:
```bash
# Try year-filtered scraping for underrepresented years
python -m scripts.02_scrape_sample --count 200 --year 2021
python -m scripts.02_scrape_sample --count 200 --year 2022
python -m scripts.02_scrape_sample --count 200 --year 2023
python -m scripts.03_parse_sample
python -m scripts.09_extract_pertimbangan
```

## Current Branch State
- On branch: `autoresearch/apr9-textfeatures`
- 17 commits ahead of main (was 12 at start of session)
- Key commits this session:
  - `087a2a0` pivot from TF-IDF to structured text features
  - `2e278be` structured features achieve parity (alpha sweep)
  - `e088c52` minimal model beats baseline (pasal_2 + gratifikasi)
  - `1d2c8ef` parser fix for PN merged text

## Data State (10 April 2026)
| Metric | Count |
|--------|-------|
| Total verdicts | 561 (559 MA + 2 PN) |
| Parsed | 518 |
| Analysis-ready (vonis+tuntutan) | 302 |
| With pertimbangan text (≥200ch) | 349 |
| Analysis-ready WITH text | 288 |
| PDFs | 429 |
| Raw HTML | 559 |

## What Needs To Be Done (Session 12)

### Priority 1: Scale MA Corpus (MOST IMPORTANT)
288 analysis-ready verdicts is too small for robust conclusions.
- MA site was unreliable today — retry when site recovers
- Use year-filtered URLs: `--year 2021`, `--year 2022`, `--year 2023`
- Target: 500+ analysis-ready verdicts
- After scraping: parse + extract pertimbangan + re-run autoresearch

### Priority 2: Verify Structured Features on Larger Corpus
The pasal_2 + gratifikasi finding (p=0.055) needs verification at larger n:
- If still significant → strong paper finding
- If not → sample-size-dependent artifact

### Priority 3: Paper 2 Draft
Narrative is now clear — three-phase experiment story:
1. TF-IDF fails (bag-of-words wrong representation)
2. All structured features neutral (too many features)
3. Minimal model works (domain knowledge wins)
See `reports/paper2_outline.md` for updated outline.

### Priority 4: Paper 1 Final Check
- Submission-ready since Session 9
- Add outlier analysis findings (vonis > tuntutan cases)
- Target: ACL/EMNLP Resource track or LREC-COLING

## Key Insights This Session

1. **Domain knowledge >> statistical features**: Two binary keywords from pertimbangan text outperform 100 TF-IDF features because they encode legal concepts (charge type, crime category) that bag-of-words misses.

2. **Text-derived > structured metadata**: `pasal_2` from judge's reasoning text beats `pasal_2` from case metadata because the text captures the *operative* charge (what judge applied) vs. *all listed charges*.

3. **PN verdicts are a dead end for this project**: The MA directory only publishes MENGADILI sections for PN courts — no full text. Must scale via MA year-filtered scraping instead.

4. **40 cases where vonis > tuntutan**: Judges sometimes give MORE than prosecution asks — strong evidence for H1 (systematic disproportionality).

## Known Issues
- MA site unreliable (frequent timeouts, year-filtered URLs often return 500)
- PN verdicts can't be used for regression (no tuntutan/kerugian)
- 105 verdicts have no year information (tahun = NULL)
- Config currently set to MA_COURT_SLUGS (reverted from PN)
