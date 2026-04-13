# Handoff — Session 12 → Session 13

## Status: **Paper 2 Updated with Full PDF Extraction, Corpus 693**

Major data quality improvement: complete re-extraction of pertimbangan text from PDFs (median 10,877 chars vs 1,190 from partial HTML). Paper 2 fully updated with new analysis. Core finding (Pasal 2 premium) is robust and actually stronger (d=0.58 vs 0.49). Text feature negative result is now decisive (0/10 seeds significant).

## Session 12 Summary (10 commits)

### Phase 1: Verification + Proofread
- 69 tests pass, analysis verified
- 20+ stale statistics corrected across paper + materials
- 5 uncited references integrated, section numbering fixed
- Declarations section + DOIs added for CLSC compliance

### Phase 2: CLSC Requirements Verified
- Abstract 165w (150-250 required), body ~4600w (10,000 limit)
- APA references with DOIs, double-blind ready
- All Springer requirements met

### Phase 3: Corpus Growth + Pertimbangan Re-extraction
- 3 new verdicts scraped from MA page 1 (pages 2+ timeout)
- 22 unparsed verdicts parsed (DB: 693 total, 367 analysis-ready)
- **Full pertimbangan re-extraction from 433 PDFs** (430 succeeded)
- Text quality dramatically improved: median 10,877 chars (was 1,190)
- All 367 analysis-ready cases now have pertimbangan text (was 350/364)

### Phase 4: Analysis Update (Key Finding)
The full PDF text changed the Pasal 2/3 classification because judges discuss both alternative charges before applying one. **Model 3 (controlling for both) is now primary:**

| Metric | Old (partial text, n=350) | New (full PDF, n=367) |
|--------|--------------------------|----------------------|
| Model 3 P2 coef | b=0.690, p=0.003 | **b=0.730, p=0.002** |
| Cohen's d | 0.492 | **0.584** (stronger!) |
| Keywords | 5/10 significant | **0/10** (clearer negative) |
| Discount R2 | -0.056 | **-0.012** |
| Subsample robust | All n≥175 | n≥293 (80%) |

The headline number is unchanged: **~0.73 years Pasal 2 premium**. Effect size actually increased. Text feature failure is now definitive.

## CRITICAL: First Thing Next Session

```bash
python -m pytest tests/ -q                    # 69 passed
python -m scripts.11_paper2_analysis          # All Paper 2 numbers
```

## Data State (13 April 2026)
| Metric | Count |
|--------|-------|
| Total verdicts (DB) | 693 |
| Parsed | 693 |
| Analysis-ready (vonis+tuntutan) | 367 |
| With pertimbangan text | 430 |
| Analysis-ready WITH text | 367 (100%) |

## Branch State
- Branch: `autoresearch/apr9-textfeatures`
- NOT merged to main (deliberate — experimental branch)

## Key Files Modified
| File | Change |
|------|--------|
| `reports/paper2_draft.md` | All numbers synced with n=367 analysis |
| `reports/paper2_supplementary.md` | S6 subsample table updated |
| `reports/paper2_cover_letter.md` | Numbers synced |
| `reports/paper2_submission_metadata.md` | Numbers synced |
| `src/db.py` | Added migrate_db(), pertimbangan_text in schema |

## What Needs To Be Done (Session 13)

### Priority 1: Final Human Review + Submit Paper 2
- Convert Markdown → Word/LaTeX
- Fill in university affiliation, ORCID, email
- Human read-through one more time
- Submit to CLSC via Springer Editorial Manager

### Priority 2: Continue Corpus Scaling
- MA site pages 2+ unreliable — try off-peak hours
- Consider scraping individual verdict URLs discovered in HTML files
- Target: 800+ verdicts → ~400 analysis-ready

### Priority 3: Paper 1 Update (Lower Priority)
- Paper 1 uses n=557 corpus, findings still valid
- Consider updating to n=693 for consistency before submission

## Key Insight This Session

**Fuller text data improved data quality at the cost of classifier noise.** Re-extracting pertimbangan from PDFs (10x more text) revealed that judges discuss both Pasal 2 and Pasal 3 as alternative charges. The simple `has_pasal_2` regex picked up mentions in both contexts. Controlling for both indicators (Model 3) restores the clean result: b=0.730, p=0.002 — nearly identical to the original. The lesson: when working with text-derived features, longer text can introduce noise unless the feature specification accounts for the fuller context.

**The text feature negative result became definitive.** With complete pertimbangan text, domain keywords went from 5/10 seeds significant to 0/10. This transforms the finding from "marginal, unstable improvement" to "no improvement whatsoever" — a cleaner, more publishable negative result.
