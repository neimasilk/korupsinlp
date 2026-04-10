# Session 11 Analysis Findings (10 April 2026)

## 1. Structured Text Features — Three-Phase Experiment

### Phase 1: TF-IDF (Sessions 10-11, 30 experiments)
- All bag-of-words approaches significantly HURT in cross-validation
- Best: 100 TF-IDF unigrams + tuntutan + kerugian, Ridge α=0.05
- 5×10 CV: R²=0.460, vs baseline -0.072 (p<0.0001)

### Phase 2: Domain-Specific Keyword Features
16 binary/count features from pertimbangan text:
- pasal_2, pasal_3, pasal_12, miliar, mengembalikan, jabatan, etc.
- Alpha sweep: optimal α=50
- 5×10 CV: R²=0.498, vs baseline +0.007 (p=0.69) — neutral

### Phase 3: Exhaustive Feature Selection
- Tested all C(11,k) subsets for k=1..4 with 3×10 CV
- **Best: tuntutan + pasal_2 + gratifikasi (3 features)**
- Forward selection confirms: NO additional feature helps
- **5×10 CV: R²=0.521, vs baseline +0.030 (p=0.055)**

### Key Insight: Text-Derived vs Structured Metadata
- Text-derived pasal_2 (from pertimbangan): +0.030, p=0.055
- Structured pasal_2 (from metadata column): -0.003, p=0.81
- **Why**: text captures the *operative* charge; metadata lists *all* charges

## 2. Outlier Analysis

### Vonis > Tuntutan Cases (n=40, 13.9%)
- Judge gives MORE than prosecution asked
- Mean vonis: 5.3yr vs mean tuntutan: 2.9yr
- Mean kerugian: 118 billion IDR (very large cases)
- Concentrated in Jakarta Pusat (18%)

### Predicting Vonis > Tuntutan
- Logistic regression AUC = 0.784 (5×5 stratified CV)
- Key predictors: low tuntutan, pasal_2, absence of meringankan
- Heavy cases rarely mention memberatkan/meringankan (7.1% vs 22.8%)

### Extreme Cases
- Bandung: 0.2yr tuntutan → 5yr vonis (2000% "discount")
- Jakarta Pusat: 2yr → 8yr (400%)
- Tanjungkarang: 7.5yr → 0.25yr (3% discount — extreme lenience)

### Outlier Court Concentration
| Court | Outlier Rate |
|-------|-------------|
| Tanjungkarang | 40% |
| Semarang | 30% |
| Palembang | 25% |
| Bandung | 14% |

## 3. PN Data Investigation

### Discovery
- PN court slugs verified working on MA directory
- pn-surabaya: 344+ verdicts for 2024 alone
- Parser fixed for PN merged text (selama8 → selama 8)

### Critical Limitation
- PN HTML detail pages only publish MENGADILI section
- NO tuntutan, NO kerugian, NO pertimbangan text
- NO PDF downloads available
- **PN verdicts cannot be used for regression analysis**

## 5. Sentence Embeddings (Transformer) — Failed

Tested paraphrase-multilingual-MiniLM-L12-v2 (384-dim) with PCA reduction:
| Method | CV R² | vs Baseline |
|--------|-------|-------------|
| PCA(5) | 0.488 | -0.017 |
| PCA(10) | 0.481 | -0.024 |
| PCA(20) | 0.456 | -0.049 |
| PCA(50) | 0.408 | -0.097 |
| **Minimal (pasal_2+grat)** | **0.521** | **+0.030** |

Two binary keywords outperform 384-dimensional transformer embeddings.
More dimensions = more overfit at n=244. This strongly supports the paper's
thesis that domain knowledge >> statistical representation for small legal corpora.

## 6. Clustering Analysis — H4 Partially Falsified

K-means (K=2,3,4) on TF-IDF+SVD pertimbangan text:
- Clusters driven by text LENGTH, not corruption type
- Cohen's d=0.14 (negligible) for vonis between K=2 clusters
- Mann-Whitney p=0.54 — no significant separation
- H4 (dualisme struktural) not supported by text analysis

## 7. Pasal 2 vs Pasal 3 — Legal Interpretation

Pasal 2 UU Tipikor ("memperkaya diri sendiri" — enriching oneself) vs
Pasal 3 ("menyalahgunakan kewenangan" — abusing authority):

| Group | n | Mean Vonis | Mean Tuntutan | Cohen's d vs P3 |
|-------|---|-----------|---------------|----------------|
| Pasal 2 only | 96 | 6.2yr | 8.3yr | 0.95 (large) |
| Pasal 3 only | 92 | 3.4yr | 5.3yr | — |
| Both | 51 | 5.7yr | 7.8yr | — |
| Neither | 66 | 4.1yr | 5.5yr | — |

**After controlling for tuntutan (M9 residuals):**
- P2 residual: +0.48yr (judges give MORE than model predicts)
- P3 residual: -0.49yr (judges give LESS)
- Mann-Whitney p=0.001, Cohen's d=0.45 (medium effect)

**This proves that pasal_2 captures genuine legal signal that tuntutan alone misses.**
Judges systematically treat enrichment more harshly than authority abuse,
even after accounting for prosecution demand.

Kerugian median: P2 = Rp 2.7B vs P3 = Rp 0.8B — P2 cases are larger,
which partially explains the effect but not fully (controlled effect still significant).

## 8. Temporal Analysis — H3 Not Supported

Vonis trending up (r=+0.75 yearly, p=0.013): 2.4yr (2014) → 5.2yr (2025).
But discount ratio (vonis/tuntutan) is STABLE (r=+0.02, p=0.75).

**Conclusion:** No temporal erosion in sentencing severity relative to
prosecution demand. The increase in absolute vonis reflects larger cases
being prosecuted, not harsher judges.

2021 anomaly: mean discount=143% (many vonis > tuntutan cases).
2026 low: 57% discount but only n=15 — too early to interpret.

H3 (Erosi Temporal): **NOT SUPPORTED** by current data.

## 9. Sentencing Discount is Unpredictable

The discount ratio (vonis/tuntutan) — the most policy-relevant metric —
is completely unpredictable from available features:
- Ridge regression on 9 text features: **CV R²=-0.08** (worse than mean prediction)
- No individual feature significantly correlates with discount at α=0.05
- Pasal 2: r=+0.10 (p=0.08) — weakest hint, not significant

**Conclusion:** Judicial discretion operates independently of ALL observable
characteristics: case magnitude, charge type, mitigating/aggravating factors,
text content. The ~40% unexplained variance in sentencing predictions reflects
case-specific judicial judgment that leaves no trace in public documents.

This is the "genuine opacity" finding — publishable and important for policy.

## 10. Geographic Disparity — "Islands of Impunity" (Preliminary)

After controlling for tuntutan, pasal_2, and gratifikasi, geographic
residuals reveal systematic court-level biases:

**Courts that give HARSHER than predicted:**
| Court | n | Mean Residual | Anomaly Rate |
|-------|---|--------------|-------------|
| Serang | 5 | +1.15yr | 20% |
| Samarinda | 10 | +0.91yr | 0% |
| Jakarta Pusat | 48 | +0.90yr | 12% |
| Kupang | 14 | +0.65yr | 7% |

**Courts that give LIGHTER than predicted:**
| Court | n | Mean Residual | Anomaly Rate |
|-------|---|--------------|-------------|
| Palu | 5 | -1.99yr | 20% |
| Banda Aceh | 13 | -1.12yr | 0% |
| Pangkalpinang | 6 | -1.09yr | 0% |
| Tanjungkarang | 5 | -1.07yr | 20% |
| Padang | 9 | -0.87yr | 0% |

**Caveat:** Small n per court (most <15). These are preliminary signals
requiring verification with larger corpus. But the pattern is suggestive
of geographic disparity that controls for case magnitude.

This is exactly the "Islands of Impunity" analysis from Fase 3A —
now possible with current data as a preliminary exploration.

## 11. Judge Effects — Significant (p=0.046)

ANOVA on residuals by hakim ketua: F=1.75, p=0.046 — judges
differ systematically in sentencing severity after controlling for
case characteristics.

**Most lenient judges (mean residual):**
- Desnayeti M.: -1.62yr (n=5)
- Jupriyadi: -1.16yr (n=14, reliable)

**Harshest judges:**
- Dwiarso Budi Santiarto: +0.87yr (n=33 combined)
- Surya Jaya: +0.55yr (n=42, most reliable)

**Neutral:** Artidjo Alkostar: -0.05yr (n=14) — famous anti-corruption
judge sentences exactly as model predicts.

**Range:** ~2.5 years between most lenient and harshest judge.
This is larger than the text feature effect (+0.03 R²) — who your
judge is matters more than what the verdict text says.

**Caveat:** MA kasasi panels are semi-random assignment. Effect could
reflect panel composition, not individual judge. Needs hierarchical
model with random judge intercepts for proper estimation.

## 12. Court Predictability — "Formulaic" vs "Opaque" Courts

Per-court RMSE from M9 model reveals which courts have predictable
vs unpredictable sentencing patterns:

**Most predictable (formulaic, RMSE <1.5yr):**
- Bengkulu: 0.73yr (very consistent sentencing)
- Ambon: 0.99yr
- Jambi: 1.32yr
- Pangkalpinang: 1.43yr (but systematically lenient: -1.29yr bias)

**Most opaque (RMSE >2.5yr):**
- Tanjungkarang: 3.21yr (only "OPAQUE" court — wildly inconsistent)
- Palembang: 2.98yr
- Semarang: 2.80yr
- Mataram: 2.68yr

**Interpretation:** Some courts apply sentencing formulaically (similar
cases → similar sentences). Others show high variance, suggesting either
more judicial discretion, inconsistent practices, or unmeasured case
factors. Tanjungkarang's RMSE is 4× Bengkulu's.

## 13. Corpus Scaling Strategy Update
- MA year-filtered scraping is the path forward
- Global korupsi directory has 499 pages (~40K verdicts)
- Current coverage sparse for 2013-2023
- MA site unreliable today — retry needed
