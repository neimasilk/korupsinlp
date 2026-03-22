# Handoff — Session 9 → Session 10

## Status: **Paper 1 Submission-Ready Draft Complete**

Paper 1 draft comprehensively rewritten with tuntutan regression (the strongest predictor, R²=0.60), sensitivity analysis, power analysis, MNAR documentation, and Table 1. The "sole predictor" narrative has been replaced with a two-level mediation structure: kerugian → tuntutan → vonis. 54 tests passing, regression script clean.

## What Was Done (Session 9)

### 1. Critical Methodological Fix: Tuntutan Added to Regression

Tuntutan (prosecution demand) was already extracted (n=302) but never used in regression. This was the single biggest gap — tuntutan has r=0.775 with vonis, far stronger than kerugian (r=0.58).

| Model | Predictors | R² | n | Key finding |
|-------|-----------|-----|---|-------------|
| M1 | log₁₀(kerugian) | 0.347 | 251 | Kerugian baseline |
| M6 | log₁₀(tuntutan) | 0.418 | 302 | Tuntutan > kerugian |
| M9 | tuntutan (linear, years) | **0.600** | 302 | **Best model** |
| M7 | log₁₀(tuntutan) + log₁₀(kerugian) | 0.492 | 236 | Both p<0.001 |
| M8 | + pemohon + JP + year | 0.496 | 236 | Additional vars NS |
| Md | discount ratio | 0.013 | 236 | Unpredictable |

**Key insight**: Judges sentence at ~63% of tuntutan (vonis = 0.49 + 0.63 × tuntutan). Both tuntutan and kerugian retain independent significance when combined → mediation structure. Discount ratio (vonis/tuntutan) is unpredictable by any extracted variable (R²=0.01).

### 2. Data Hygiene
- 3 suspicious kerugian values (Rp100, Rp6450, Rp750K) set to NULL — likely extraction artifacts
- Regression dataset: n=251 (kerugian), n=302 (tuntutan), n=236 (both)
- Figure generation bug fixed (is_jp passed twice → is_jpu, is_jp)

### 3. Sensitivity & Robustness Analysis
- **Outlier**: PT Timah removal minimal (R² 0.347→0.349); mega-case removal substantial (R²→0.222)
- **Missing data**: NOT MCAR (p=0.002) — cases without kerugian have lower vonis (3.67 vs 4.92yr)
- **Power**: MDE=1.09yr at 80% power for pemohon kasasi null finding
- **Cross-validation**: M1 10-fold mean R²=0.26, MAE=2.06yr

### 4. Paper 1 Draft Rewrite
- Abstract rewritten with tuntutan finding and mediation structure
- Contributions expanded to 5 items (two-level model, unpredictable discount)
- **Section 6.7 completely rewritten**: 6 subsections covering kerugian models, tuntutan models, combined model, discount model, sensitivity, and summary
- Table 1 added: 7 diverse example verdicts
- Section 6.5: JP p-value updated (0.23→0.54)
- Section 6.4: Kerugian coefficient updated (1.41→1.60, R²=0.35)
- Limitations rewritten: MNAR finding, outlier sensitivity, unexplained variance, power analysis
- Conclusion rewritten: 4 numbered findings led by tuntutan dominance
- Future work: added "tuntutan determinants" research direction

### 5. Code Changes
| File | Change |
|------|--------|
| `scripts/07_regression_analysis.py` | Fixed figure bug, added tuntutan models (M6-M9, Md), sensitivity, power analysis |
| `reports/paper1_draft.md` | Major rewrite of Abstract, Contributions, 6.4-6.7, Limitations, Conclusion |
| `reports/paper1_outline.md` | Updated with Session 9 regression table and sensitivity results |
| `reports/regression_results.json` | All models M1-M9, Md, sensitivity, power analysis |

## CRITICAL: First Thing Next Session

```bash
source .venv/Scripts/activate
python -m pytest tests/ -q  # Should be 54 passed
python -m scripts.07_regression_analysis  # Verify regression
```

## What Needs To Be Done (Session 10)

### Step 1: Paper 1 Final Submission Prep
- Proofread for internal consistency (all numbers match regression_results.json)
- Add figure captions and cross-references
- Format for target venue (ACL/EMNLP Resource track or LREC-COLING)
- Verify all 17 citation details (DOI/page numbers)
- Consider: Spearman partial correlation, VIF for multicollinearity check in M7

### Step 2: Paper 2 — Extended Prediction Model
- Add pasal as predictor (276 Pasal 2 vs 15 Pasal 3 — too skewed for binary, but subcategories?)
- Extract defendant role/position from text
- Quantile regression (formally, not just robustness check)
- Compare OLS vs random forest vs gradient boosting
- Mixed-effects model for regional clustering

### Step 3: Corpus Release
- Clean SQLite export for Zenodo/HuggingFace
- Write datasheet (Gebru et al. format)
- Generate corpus statistics report
- README for dataset users

### Step 4: Data Quality Expansion
- 69 empty records: re-scrape or purge
- Expand golden set (20 → 50 cases)
- Investigate scanned PDFs (OCR feasibility)

## Known Issues
- Residuals right-skewed (Shapiro p<0.001) — quantile regression more appropriate
- 10-fold CV has high variance (R² range -0.65 to 0.59)
- Missing kerugian is NOT random (MNAR, p=0.002) — regression biased toward embezzlement cases
- Mega-case sensitivity: without >Rp100B cases, kerugian R² drops to 0.22
- M7 (tuntutan+kerugian) R²=0.49 is lower than M9 (tuntutan linear) R²=0.60 — different sample sizes (236 vs 302)

## Key Research Findings (Session 9 Final)

1. **Tuntutan is the strongest predictor** (R²=0.60 linear). Vonis ≈ 0.49 + 0.63 × tuntutan.
2. **Kerugian retains independent significance** (p<0.001) after controlling for tuntutan → mediation structure.
3. **Judicial discount is opaque** — vonis/tuntutan ratio unpredictable (R²=0.01).
4. **Pemohon, geography, year: all non-significant** after case magnitude control.
5. **Missing data is NOT random** — regression sample biased toward embezzlement with higher sentences.
6. **Mega-cases drive kerugian-vonis relationship** — R² drops from 0.35 to 0.22 without them.
