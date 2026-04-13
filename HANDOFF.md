# Handoff — Session 12 → Session 13

## Status: **Paper 2 Submission-Ready (PDF/DOCX generated), Corpus 693**

Paper 2 has been through: numerical sync → full PDF pertimbangan re-extraction → analysis update → critical review → all thesis killers fixed → PDF/DOCX generated. Ready for human review and submission.

## Session 12 Summary (13 commits)

### Phase 1: Verification + Proofread
- 69 tests pass, analysis script verified
- 20+ stale statistics corrected (OLS table, discount R2, TF-IDF delta, subsample)
- Fixed section numbering (duplicate 3.4), integrated 5 uncited references
- Added Declarations section (funding, COI, ethics, data availability)
- Added DOIs to 14/18 references

### Phase 2: Full PDF Pertimbangan Re-extraction
- Re-extracted pertimbangan text from ALL 433 PDFs (430 succeeded, 99.3%)
- Text quality: median 10,877 chars (was 1,190 from partial HTML — 10x improvement)
- All 367 analysis-ready cases now have pertimbangan text (was 350/364)
- 3 new verdicts scraped (MA page 1), 22 unparsed verdicts parsed
- DB total: 693 verdicts, 367 analysis-ready

### Phase 3: Analysis Update with Full Text
Fuller text changed P2/P3 classification (47% cases mention both articles). Model 3 (controlling for both) is now primary:

| Metric | Session 11 (partial text, n=350) | Session 12 (full PDF, n=367) |
|--------|----------------------------------|------------------------------|
| Model 3 P2 coef | b=0.690, p=0.003 | **b=0.730, p=0.002** |
| Cohen's d | 0.492 | **0.584** (stronger) |
| Keywords significant | 5/10 | **0/10** (decisive negative) |
| Discount R2 | -0.056 | **-0.012** |
| HC3 robust p | not reported | **0.001** |

### Phase 4: Critical Review + Thesis Killer Fixes
Ran comprehensive critical review identifying 10+ potential rejection risks. All fixed:

| Issue | Severity | Fix Applied |
|-------|----------|-------------|
| Causal language ("affects") | FATAL | → "is associated with" throughout |
| Discount 0.85 vs 0.78 inconsistency | FATAL | Explained (unfiltered vs outlier-excluded) |
| p-value conflation (p<0.001 vs p=0.002) | SERIOUS | Fixed to regression p=0.002 |
| "Irreducibly opaque" overclaim | SERIOUS | → "opaque from public documents" |
| "First" claim without Indonesian lit | SERIOUS | → "First large-scale computational" |
| No OLS diagnostics | SERIOUS | Added HC3 SE, VIF, Shapiro-Wilk, Breusch-Pagan |
| Endogeneity not discussed | SERIOUS | Added with 3 mitigating arguments |
| Selection bias too thin | SERIOUS | Expanded to full paragraph with bias direction |
| Temporal skew untested | SERIOUS | Tested: pre-2024 p=0.022, post-2024 p=0.030, interaction p=0.94 |
| Indonesian lit gap | SERIOUS | Acknowledged in limitations |
| NLP-heavy framing | SERIOUS | Trimmed 5.3, moved detail to supplementary |
| "Honest negative result" 3x | MINOR | Reduced to 1x |
| Duplicated "from public documents" | BUG | Fixed in final PDF proofread |

### Phase 5: CLSC Verification + Output Generation
- CLSC confirmed: Scopus Q2, CiteScore 2.19, SJR 0.364, **FREE** (subscription model, no APC)
- Abstract 165w (150-250 req), body ~5100w (10,000 limit), 18 refs APA w/ DOIs
- Generated: `paper2_draft.pdf` (16 pages), `paper2_draft.docx`, `paper2_supplementary.docx`, `paper2_cover_letter.docx`

## CRITICAL: First Thing Next Session

```bash
python -m pytest tests/ -q                    # 69 passed
python -m scripts.11_paper2_analysis          # Verify all numbers
```

## Data State (13 April 2026)
| Metric | Count |
|--------|-------|
| Total verdicts (DB) | 693 |
| Parsed | 693 |
| Analysis-ready (vonis+tuntutan) | 367 |
| With pertimbangan text (≥200 chars) | 430 |
| Analysis-ready WITH text | 367 (100%) |

## Branch State
- Branch: `autoresearch/apr9-textfeatures` (13 new commits this session)
- NOT merged to main (deliberate — experimental branch)

## Key Files
| File | Status |
|------|--------|
| `reports/paper2_draft.md` | Source — all numbers verified against analysis |
| `reports/paper2_draft.pdf` | 16-page PDF via pandoc+pdflatex |
| `reports/paper2_draft.docx` | Word version for CLSC submission |
| `reports/paper2_supplementary.md/.docx` | 8 supplementary tables |
| `reports/paper2_cover_letter.md/.docx` | CLSC cover letter |
| `reports/paper2_submission_metadata.md` | Keywords, highlights, declarations |
| `scripts/11_paper2_analysis.py` | Reproducible analysis (source of truth) |
| `src/db.py` | Added migrate_db(), pertimbangan_text in schema |

## What Needs To Be Done (Session 13)

### Priority 1: Human Review + Submit
1. Open `reports/paper2_draft.pdf` — human read-through
2. Fill in: university name, ORCID, email (cover letter + metadata)
3. Upload preprint to SSRN (establishes priority timestamp)
4. Submit to CLSC via Springer Editorial Manager (FREE)

### Priority 2: Corpus Scaling
- MA site pages 2+ unreliable — try off-peak hours (malam WIB)
- Target: 800+ verdicts for stronger subsample robustness
- After scraping: `python -m scripts.03_parse_sample` → `09_extract_pertimbangan` → `11_paper2_analysis`

### Priority 3: Paper 1 Update
- Paper 1 uses n=557 corpus, geographic finding still valid
- Consider updating to n=693 before submission

## Key Insights This Session

1. **Numbers drift silently.** Paper had 20+ stale stats from earlier corpus — systematic cross-check against analysis script is essential before any submission.

2. **Fuller text improves data but adds noise.** PDF extraction (10x more text) means judges discuss both alternative charges, making the simple `has_pasal_2` regex noisier. Model 3 (controlling for both) restores the clean result.

3. **Critical self-review prevents desk reject.** Causal language from observational data, numerical inconsistencies, and missing diagnostics would have triggered immediate rejection at a quantitative criminology journal. Fixing these pre-submission is far cheaper than a reject-resubmit cycle.

4. **The text feature negative result became definitive.** Keywords went from 5/10 seeds significant (marginal) to 0/10 (no improvement) — a cleaner, more publishable result.
