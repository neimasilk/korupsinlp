# Handoff — Session 11 → Session 12

## Status: **Paper 2 Submission-Ready, Corpus 671**

Paper 2 completely rewritten from "Two Words That Matter" (NLP methods, overclaimed) to "Charge Type, Judicial Opacity, and the Limits of Prediction" (sentencing analysis, honest). Target: Crime, Law and Social Change (Springer, Q1/Q2). All submission materials prepared.

## Session 11 Summary (50+ commits)

### Phase 1: Autoresearch Experiments (50+ experiments)
- Pivoted from TF-IDF (30 exp, all failed) to domain keywords
- Found 3 keywords (pasal_2, gratifikasi, pencucian_uang) as optimal
- Tested Ridge/Lasso/ElasticNet, GBM, interactions, embeddings — all worse
- Result: marginal improvement (+0.02 R2, 5/10 seeds significant)

### Phase 2: Critical Self-Review
- Identified 5 fatal problems with original "Two Words" framing
- d=1.07 was straw man, p-values unstable, test set negative
- Decided to reframe entirely: sentencing analysis, not NLP methods
- Pasal 2 OLS regression (b=+0.734, p=0.001) chosen as anchor finding

### Phase 3: Paper Rewrite + Submission Prep
- Complete rewrite: 4900 words, 22 subsections, 18 references
- Analysis script with OLS + bootstrap CIs (7 tables)
- Supplementary materials (8 tables: TF-IDF log, embeddings, etc.)
- Cover letter and submission metadata prepared
- All numbers verified: Pasal 2 significant at EVERY subsample n=170-350

### Phase 4: Corpus Scaling
- 559 → 671 verdicts (+112, +20%)
- Batch scraping script created (scripts/10_batch_scrape_global.py)
- PN courts discovered unusable (no tuntutan in HTML)
- MA site pages 1-4 fully scraped, deeper pages unreliable

## CRITICAL: First Thing Next Session

```bash
python -m pytest tests/ -q                    # 69 passed
python -m scripts.11_paper2_analysis          # All Paper 2 numbers
```

## Data State (10 April 2026)
| Metric | Count |
|--------|-------|
| Total verdicts | 671 |
| Analysis-ready (vonis+tuntutan) | 380 |
| With pertimbangan text | 407 |
| Analysis-ready WITH text | 350 |

## Branch State
- Branch: `autoresearch/apr9-textfeatures` (70+ commits, 50+ this session)
- NOT merged to main (deliberate — experimental branch)

## Key Files This Session
| File | Purpose |
|------|---------|
| `reports/paper2_draft.md` | Full manuscript (4900 words) |
| `scripts/11_paper2_analysis.py` | Reproducible analysis (OLS + bootstrap) |
| `reports/paper2_supplementary.md` | 8 supplementary tables |
| `reports/paper2_cover_letter.md` | CLSC cover letter |
| `reports/paper2_submission_metadata.md` | Keywords, highlights |
| `scripts/10_batch_scrape_global.py` | Batch scraper for corpus scaling |
| `reports/session11_findings.md` | 17 findings documented |

## What Needs To Be Done (Session 12)

### Priority 1: Final Proofread Paper 2
- Read through once more for flow and clarity
- Verify no overclaiming (grep for "significant" and "improve")
- Check reference formatting matches CLSC style
- Add ORCID and university affiliation

### Priority 2: Consider Submission
- CLSC submission portal: https://www.springer.com/journal/10611
- Format requirements: check CLSC author guidelines
- Prepare clean PDF or LaTeX version

### Priority 3: Scale Corpus (Lower Priority)
- MA site unreliable — try off-peak hours
- `python -m scripts.10_batch_scrape_global --pages 20`
- Parse new verdicts: `python -m scripts.03_parse_sample`

### Priority 4: Paper 1 Update
- Geographic claim needs clarification (composition effect)
- Numbers verified consistent at larger corpus

## Key Insight This Session

**Reframing saved the paper.** The original "Two Words That Matter" would have been rejected at any serious journal — d=1.07 was a straw man, p-values were unstable, the NLP contribution was textbook. The reframe to "Charge Type, Judicial Opacity, and the Limits" centers on genuinely strong findings (Pasal 2 b=+0.734, p=0.001; discount R2=-0.10) and presents text feature failure as an honest negative result. This is the paper that can actually get published.
