# Paper 2: Beyond Structured Features — Judge Effects and the Limits of Sentencing Prediction

## Working Title
**"What Explains the Other 40%? Judge-Level Variation and the Limits of Structured Sentencing Prediction in Indonesian Corruption Cases"**

## Target Venue
- Primary: ICWSM, CSS Workshop, or Journal of Empirical Legal Studies
- If text features work: ACL/EMNLP Findings

## Core Narrative

Paper 1 showed that tuntutan + kerugian explain 62% of sentencing variance (R²=0.62). This paper asks: **what explains the remaining 38%?**

We systematically test three hypotheses:
1. **Additional structured features** (pasal charged, number of charges, amar category, Pasal 55 conspiracy) — **RESULT: nothing adds beyond tuntutan+kerugian (R² 0.615 -> 0.618)**
2. **Judge-level variation** (ICC ≈ 0.10, mixed-effects model) — **10% of total variance is between-judge**
3. **Text-based features** (TF-IDF, IndoBERT embeddings) — **TBD, this is the key experiment**

The paper's contribution is empirically quantifying the "opacity of judicial discretion" — showing exactly where structured analysis fails and text analysis is needed.

## Key Preliminary Results (Session 9)

### Structured features are exhausted
| Feature | Univariate effect | After tuntutan+kerugian control |
|---------|------------------|-------------------------------|
| Pasal 55 (conspiracy) | +1.77yr (p<0.01) | p=0.44 (NS) |
| Number of charges | r=0.13 (p=0.046) | p=0.56 (NS) |
| Amar category (Kabul) | No difference | p=0.47 (NS) |
| Pasal 2 vs 3 | Not viable (72% cite both) | — |
| **Combined (all 3 new)** | — | **R² 0.615 -> 0.618** |

### Judge-level variation (TESTED)
- 149 unique judges (presiding), 15 with 3+ cases in regression sample
- **Crude ICC = 0.097** (~10% from one-way ANOVA) — but this is confounded by case assignment
- **Mixed-effects ICC = 0.036** (~3.6% after controlling for tuntutan + kerugian) — MUCH smaller
- Judge random effects range: -0.28yr (Yohanes Priyana) to +0.40yr (Dwiarso Budi Santiarto)
- This is only ±5 months difference between most extreme judges
- **Conclusion**: Judges are remarkably consistent. The apparent "judge effect" was case-assignment confounding.
- Mixed model pseudo-R²: 0.637 vs OLS 0.617 = +2.0pp improvement (modest)

### Variance decomposition (ACTUAL)
| Source | % of total variance | Method |
|--------|-------------------|--------|
| Tuntutan | ~50% | Partial R² (M9 vs null) |
| Kerugian (independent of tuntutan) | ~12% | Delta R² (M_combined vs M9) |
| Judge identity | ~2% | Delta pseudo-R² (mixed vs OLS) |
| Other structured features (pasal, amar) | <0.5% | Delta R² (NS, p>0.44) |
| **Unexplained (case-specific)** | **~36%** | Residual |

## Proposed Methods

### Phase 1: Mixed-Effects Model [feasible now]
- `vonis ~ tuntutan + log_kerugian + (1|judge)` using statsmodels MixedLM
- Challenge: 3-judge panels — need to decide: use ketua majelis (presiding) only, or crossed random effects?
- Expected: R² improvement of 5-10% over OLS

### Phase 2: Text Features [requires new code]
- Extract full PDF text for 320 cases with PDF + vonis
- Feature extraction:
  a) TF-IDF on "pertimbangan hukum" section
  b) IndoBERT [cls] embeddings (mean pooling)
  c) Specific keyword features (kerja sama, merugikan, jabatan, etc.)
- Model: structured features + text features → vonis
- Compare: structured-only (R²=0.62) vs text-only vs combined
- If combined R² > 0.70: text captures judicial reasoning beyond structured fields
- If combined R² ≈ 0.62: text doesn't add — discretion truly opaque

### Phase 3: Quantile Regression [builds on Paper 1]
- Paper 1 showed residuals are right-skewed (Shapiro p<0.001)
- Quantile regression at tau = 0.25, 0.50, 0.75 with all features
- Does judge effect vary across quantiles? (harsher at extremes?)

## Research Questions

- **RQ1**: Do additional structured case features (pasal, charges, amar) predict sentencing beyond prosecution demand and state loss? [Answer: NO]
- **RQ2**: How much sentencing variation is attributable to judge identity vs case characteristics?
- **RQ3**: Can text features (pertimbangan hukum) capture the unexplained judicial discretion component?
- **RQ4**: Does the sentencing function vary across the sentence distribution (quantile effects)?

## Required Data/Tools

| Need | Status | Effort |
|------|--------|--------|
| Current corpus (557 verdicts) | Ready | — |
| Mixed-effects model | statsmodels MixedLM | 2-3 hours |
| PDF text loading | pdfminer already works | 1 hour |
| TF-IDF features | scikit-learn | 2-3 hours |
| IndoBERT embeddings | Needs torch + transformers | 4-6 hours |
| Quantile regression | statsmodels already works | 1-2 hours |

## Scope Control

**IN scope**: mixed-effects, TF-IDF, quantile regression
**MAYBE**: IndoBERT (if TF-IDF shows promise)
**OUT of scope**: causal inference, PN expansion, new scraping, network analysis

## Key Risk

- **IndoBERT on legal text may not work well** — legal Indonesian is very different from general Indonesian. Pre-trained models may not capture legal jargon. Mitigation: test TF-IDF first (no model dependency).
- **Judge random effects may be confounded** — if certain judges always handle mega-cases, the "judge effect" is actually a "case selection effect." Mitigation: control for kerugian in the random effects model.
- **n=320 may be too small for text features** — especially with IndoBERT (768-dim embeddings). Mitigation: use PCA or simple bag-of-words first.
