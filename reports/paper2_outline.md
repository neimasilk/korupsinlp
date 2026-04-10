# Paper 2: Beyond Bag-of-Words — Domain-Specific Text Features for Sentencing Prediction

## Working Title
**"Two Words That Matter: Domain-Specific Text Features Outperform Bag-of-Words for Sentencing Prediction in Indonesian Corruption Cases"**

## Target Venue
- Primary: Artificial Intelligence and Law, or Journal of Empirical Legal Studies
- Alternative: ACL/EMNLP Findings (computational legal studies angle)

## Core Narrative

Paper 1 showed prosecution demand (tuntutan) explains ~60% of sentencing variance.
This paper systematically tests whether text from judicial reasoning (pertimbangan hakim)
can explain more. The answer is nuanced:

**Bag-of-words (TF-IDF) fails catastrophically** — 30 experiments show it significantly
HURTS prediction in cross-validation (p<0.0001). But **domain-specific binary features**
(just 2 keywords) achieve marginally significant improvement (p=0.055).

This is a methodological contribution: in small legal corpora, domain knowledge
encoded as structured features >> statistical text features.

## Key Results (10 April 2026)

### Phase 1: TF-IDF Experiments (30 experiments, 9 April 2026)
- Best single-split: val_r2=0.626 (100 TF-IDF + tuntutan + kerugian, Ridge α=0.05)
- **5×10-fold CV: R²=0.460, WORSE than baseline 0.532 (p<0.0001)**
- Tried: max_features 50-5000, ngrams, stopwords, SVD, Lasso, ElasticNet, RF, GBM
- All failed in CV. TF-IDF is fundamentally wrong representation for n=288.

### Phase 2: Structured Text Features (10 April 2026)
All 16 domain keywords + tuntutan:
- 5×10-fold CV: R²=0.498, vs baseline +0.007 (p=0.69, neutral)
- Better than TF-IDF but still not significant improvement

### Phase 3: Feature Selection (10 April 2026)
Exhaustive search over all subsets of size 1-4:
- **Best: tuntutan + has_pasal_2 + has_gratifikasi (3 features total)**
- 10-fold CV: R²=0.561 (+0.023 vs baseline)
- **5×10-fold CV: R²=0.521 (+0.030 vs baseline, p=0.055)**
- Forward selection shows NO additional feature improves this base

### Summary Table

| Approach | n_features | CV R² | vs Baseline | p-value |
|----------|-----------|-------|-------------|---------|
| M9 baseline (tuntutan-only) | 1 | 0.538 | — | — |
| TF-IDF best (α=0.05) | 102 | 0.460 | -0.072 | <0.0001 |
| TF-IDF moderate (α=10) | 102 | 0.513 | -0.019 | 0.027 |
| All 16 structured features | 18 | 0.498 | +0.007 | 0.69 |
| **Minimal: pasal_2 + gratifikasi** | **3** | **0.521** | **+0.030** | **0.055** |

### Feature Interpretation

| Feature | Ridge Coef | Interpretation |
|---------|-----------|----------------|
| tuntutan_years | +1.63 | Prosecution demand (dominant) |
| has_pasal_2 | +0.50 | Pasal 2 UU Tipikor (state loss, heavier charge) |
| has_gratifikasi | +0.20 | Gratification cases (higher severity) |

**Why these 2 keywords?**
- Pasal 2 (r=+0.42 with vonis) indicates "enrichment" charges — more serious than Pasal 3
  ("misuse of authority"). This distinction is mentioned in pertimbangan but NOT in structured
  fields (pasal column has complex strings not easily parsed into binary features).
- Gratifikasi (bribery by official receiving gifts) is a specific crime type associated
  with higher sentences. Only 2.3% prevalence but highly discriminative.

### Why TF-IDF Failed — Theoretical Explanation

1. **Curse of dimensionality**: 100+ features on 200 training samples guarantees overfit
2. **Wrong representation**: Legal text has discrete categories (charge type, factor type)
   that TF-IDF dilutes into continuous weights
3. **Formulaic language**: Judicial reasoning uses standard phrases regardless of severity.
   TF-IDF captures word frequency, but meaning comes from *which legal concept* is invoked
4. **Single-split delusion**: TF-IDF appeared to improve (val_r2=0.626) because validation
   set happened to be "easy" for text features. CV exposed this as overfit.

## Paper Structure

1. **Introduction**: Legal NLP has focused on large corpora. What works for small ones?
2. **Background**: Computational sentencing, TF-IDF in legal NLP, Indonesian corruption law
3. **Data**: ICVD corpus, 288 verdicts with pertimbangan text
4. **Method 1 — TF-IDF**: 30 systematic experiments via autoresearch framework
5. **Method 2 — Structured Features**: 16 domain-specific keyword features
6. **Method 3 — Feature Selection**: Exhaustive subset search + forward selection
7. **Results**: TF-IDF fails, structured neutral, minimal wins
8. **Discussion**: Why domain knowledge >> statistical features for small legal corpora
9. **Implications**: Practical guide for legal NLP with small datasets
10. **Conclusion**: Two binary keywords outperform 100 TF-IDF features

## Key Contribution

**Methodological**: Demonstrates that in small legal corpora (<500 documents), domain-specific
binary features systematically outperform bag-of-words approaches. Provides a framework
(autoresearch) for systematic feature evaluation that others can replicate.

**Substantive**: Charge type (Pasal 2 vs 3) and crime category (gratifikasi) add predictive
value beyond prosecution demand alone, suggesting judges consider legal classification
independently of the prosecution's framing.

## Additional Findings (Session 11)

### Sentence Embeddings Also Fail
- paraphrase-multilingual-MiniLM-L12-v2 (384-dim) + PCA
- PCA(5): -0.017, PCA(50): -0.097 (significantly worse)
- **Two binary keywords outperform 384-dimensional transformer embeddings**

### Why pasal_2 Works — Legal Interpretation
- Pasal 2 = "memperkaya diri" (enrichment) — more serious charge
- Pasal 3 = "menyalahgunakan kewenangan" (authority abuse) — less serious
- After controlling for tuntutan: d=0.45, p=0.001 (medium-large effect)
- P2 cases get +0.48yr more, P3 cases get -0.49yr less than predicted
- **Text-derived pasal_2 captures the operative charge; metadata captures all listed charges**

### Complementary Findings (for Discussion section)
- **Sentencing discount is unpredictable** (R²=-0.08): judicial discretion leaves no trace
- **Judge effects significant** (F=1.75, p=0.046): ~2.5yr range between judges
- **Geographic disparity** (preliminary): Palu -2yr vs Serang +1yr after controls
- **H3 temporal**: no erosion (discount stable, r=+0.02)
- **H4 clustering**: no corruption-type dualisme (d=0.14)
- **40 cases vonis > tuntutan** (13.9%): classification AUC=0.784

## Open Questions

1. Does minimal model hold at n=500+? Effect weakened from +0.030 to +0.012 as corpus grew
2. PN courts lack tuntutan in HTML — can only scale via MA year-filtered scraping
3. Judge effects may confound text features — need hierarchical model
4. Geographic effects need larger per-court samples (most <15)

## Required Next Steps

| Step | Effort | Priority |
|------|--------|----------|
| Write Paper 2 draft | 3-5 days | HIGH — narrative is clear |
| Scale MA corpus to 500+ analysis-ready | 1-2 weeks | HIGH |
| Re-run all approaches on larger corpus | 1 day | HIGH |
| Hierarchical model (random judge intercepts) | 1 day | MEDIUM |

## Scope Control

**IN scope**: TF-IDF vs structured vs embeddings comparison, feature selection,
Pasal 2/3 legal interpretation, genuine opacity finding, autoresearch framework
**MAYBE**: Judge effects, geographic disparity (if space allows)
**OUT of scope**: causal claims, temporal analysis, network analysis
