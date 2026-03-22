# Handoff — Session 8 → Session 9

## Status: **Paper 1 Near-Final, Regression Analysis Complete**

Paper 1 draft substantially improved: proper Related Work with 17 real citations, multivariate regression section (6.7), acquittal analysis (6.6), Jakarta Pusat composition effect explained, and full References section. Regression script (07) created and passing. 54 tests passing. Key finding: only kerugian negara is significant in multivariate model — all other variables (pemohon, geography, year) are non-significant.

## What Was Done (Session 8)

### 1. Related Work — Fully Written with Real Citations
Replaced placeholder 3-paragraph section with comprehensive literature review:
- **Indonesian Legal NLP**: Nuranti & Yulianti (2020) BiLSTM+CRF NER, Nuranti et al. (2025) 2,687 annotated decisions, Yulianti et al. (2024) IndoLER dataset F1=0.923, Hasanah et al. (2023) tax court IndoBERT, Ibrahim et al. (2024) CNN-BiLSTM punishment prediction R²=0.589
- **Computational Sentencing**: Aletras et al. (2016) ECHR 79% accuracy, Medvedeva et al. (2020) 75% accuracy, Chen et al. (2019) Chinese courts, Amaral et al. (2022) Brazilian appeals, Ostling et al. (2023) Cambridge Law Corpus
- **Anti-Corruption**: Olken (2007) field experiment, Henderson & Kuncoro (2011), TI CPI 2024 (Indonesia rank 109), ICW 2024 report (avg 3yr 3mo, Rp300T losses)
- 17 references total in new References section

### 2. Multivariate Regression Analysis (n=254)

| Model | Predictors | R² | adj R² | BIC |
|-------|-----------|-----|--------|-----|
| M1 | log₁₀(kerugian) | 0.334 | 0.332 | 1237 |
| M2 | + pemohon | 0.335 | 0.329 | 1243 |
| M3 | + Jakarta Pusat | 0.338 | 0.330 | 1247 |
| M4 | + year | 0.339 | 0.328 | 1252 |
| M5 | + interaction | 0.342 | 0.329 | 1256 |

**Key findings**:
- Only log₁₀(kerugian) is significant (β=1.33, p<0.001) in all models
- Pemohon kasasi: p=0.77 (non-significant)
- Jakarta Pusat: p=0.23 (non-significant — effect is composition artifact)
- Year: p=0.65 (no temporal trend after controlling for kerugian)
- F-test M1 vs M4: p=0.65 — M1 (bivariate) is sufficient
- 10-fold CV: mean R²=0.25, MAE=2.09 years
- Quantile regression confirms: only kerugian significant at median

### 3. Pattern Analysis Added to Paper
- **Jakarta Pusat**: 31× higher median kerugian (Rp32B vs Rp1B), effect disappears in regression
- **Acquittals**: 17 cases, 71% terdakwa kasasi, geographically dispersed
- **Temporal trend**: 2014 2.3yr → 2025 5.2yr apparent but non-significant (p=0.65) after kerugian control

### 4. Code Changes
| File | Change |
|------|--------|
| `reports/paper1_draft.md` | Related Work (17 citations), Sections 6.6-6.7, Conclusion, References |
| `scripts/07_regression_analysis.py` | **NEW** — Full regression pipeline with OLS, quantile, CV, figures |
| `reports/regression_results.json` | Regression results with all model comparisons |
| `reports/figures/fig6_regression_scatter.png` | **NEW** — Scatter with JP highlighted |
| `reports/figures/fig7_residual_diagnostics.png` | **NEW** — Residual + Q-Q plots |

## CRITICAL: First Thing Next Session

```bash
source .venv/Scripts/activate
python -m pytest tests/ -q  # Should be 54 passed
python -m scripts.07_regression_analysis  # Verify regression
```

## What Needs To Be Done (Session 9)

### Step 1: Paper 1 Final Polish
- Add figure captions and cross-references throughout
- Table 1: example verdicts (diverse by region, kerugian, outcome)
- Proofread for venue formatting (ACL/EMNLP Resource track or LREC-COLING)
- Verify all citation details (some may need DOI/page numbers)
- Consider adding: Spearman partial correlation controlling for year

### Step 2: Paper 2 — Extended Regression Model
- Add pasal (articles charged) as categorical predictor
- Extract defendant role/position from text (if feasible)
- Hierarchical/mixed-effects model for regional variation
- Bootstrap confidence intervals for R²
- Compare OLS vs random forest vs gradient boosting

### Step 3: Data Quality
- 69 empty records: re-scrape or purge
- Investigate scanned PDFs (OCR feasibility)
- Expand golden set from 20 to 50 cases

### Step 4: Corpus Release Preparation
- Clean SQLite export for Zenodo/HuggingFace
- Write datasheet (Gebru et al. format)
- Generate corpus statistics report

## Known Issues
- Residuals are right-skewed (Shapiro p<0.001) — quantile regression is more appropriate than OLS
- 10-fold CV has high variance (R² range -0.42 to 0.56) — some folds have very different compositions
- ~34% of cases lack kerugian (suap/gratification cases) — regression only covers 254/327
- Kerugian Rp100 minimum suspicious — likely extraction artifact
- Some large PDFs take >5 minutes for pdfminer

## Key Research Findings (Updated)

1. **Kerugian negara is the ONLY significant sentencing predictor** at MA level (β=1.33, p<0.001, R²=0.33). No other variable we extracted adds significant predictive power.

2. **Pemohon kasasi does NOT predict sentence severity** (p=0.95 univariate, p=0.77 multivariate). Definitively null.

3. **Jakarta Pusat "harshness" is a composition effect** — driven by 31× higher median kerugian, not jurisdictional bias. Non-significant (p=0.23) after controlling for kerugian.

4. **No significant temporal trend** in sentencing (p=0.65) after controlling for kerugian. Apparent increase (2014: 2.3yr → 2025: 5.2yr) is likely driven by changing case composition.

5. **MA acquittal rate is ~5%** (17/344), 71% from terdakwa kasasi.

6. **Our mean sentence (4.63yr) is higher than ICW's 2024 all-court average (3.25yr)** — consistent with selection bias (only appealed cases reach MA).
