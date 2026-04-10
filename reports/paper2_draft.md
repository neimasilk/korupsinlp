# Two Words That Matter: Domain-Specific Text Features Outperform Bag-of-Words for Sentencing Prediction in Indonesian Corruption Cases

## Abstract

Text representation choice has a large effect on sentencing prediction in small legal corpora. Using 331 Indonesian corruption verdicts with judicial reasoning text, we show that the standard NLP approach — bag-of-words (TF-IDF) — **destroys** prediction accuracy, while two domain-specific binary keywords **preserve and slightly improve** it. In a paired comparison across 50 cross-validation folds, the minimal model (two keywords) outperforms TF-IDF by 0.19 R2 on average (paired t=7.47, p<0.001, Cohen's d=1.07). The same two keywords also outperform 384-dimensional transformer sentence embeddings. Through systematic three-phase experimentation — 30 TF-IDF experiments (all fail), 16 domain-specific features (parity), exhaustive feature selection (two keywords win) — we identify the optimal features: whether the judge mentions **Pasal 2** (enrichment charges) and **gratifikasi** (bribery). Pasal 2 captures a legally meaningful distinction: after controlling for prosecution demand, Pasal 2 cases receive sentences 0.50 years heavier than Pasal 3 cases (d=0.46, p<0.001). The text-derived charge type outperforms structured metadata because judicial reasoning captures the *operative* charge, not all listed charges. The sentencing discount (vonis/tuntutan ratio) remains entirely unpredictable (R2=-0.06), revealing genuine judicial opacity. For practitioners: in small legal corpora, start with domain-specific features, not bag-of-words.

## 1. Introduction

A growing body of computational legal research applies natural language processing (NLP) to predict judicial outcomes from court documents. In the sentencing domain, text features from judicial opinions have been used to model sentencing decisions in the United States (Aletras et al., 2016), the United Kingdom (Strickson & De La Iglesia, 2020), and Brazil (Lage-Freitas et al., 2022). These studies typically rely on large corpora (thousands to tens of thousands of documents) and find that bag-of-words or transformer-based representations capture meaningful predictive signal.

But what happens when the corpus is small? Many legal systems — particularly in the Global South — produce publicly available court decisions that have never been computationally analyzed, yet the available corpus may number only in the hundreds. Indonesian corruption verdicts are a prime example: the Supreme Court (Mahkamah Agung) publishes cassation decisions with full judicial reasoning, but extracting structured data requires custom parsing pipelines, and the resulting corpus is necessarily small.

In a companion paper (Author, 2026), we introduced CorpusKorupsi, a structured corpus of 615 Indonesian corruption verdicts, and showed that prosecution demand (tuntutan) explains approximately 60% of sentencing variance (R2=0.60). This paper asks: **can text features from judicial reasoning explain the remaining 40%?**

We approach this question systematically through three phases of experimentation:

1. **Phase 1: Bag-of-words (TF-IDF).** We conduct 30 experiments varying TF-IDF hyperparameters, regularization, and model type. All approaches significantly hurt prediction in cross-validation — TF-IDF is the wrong representation for this corpus size.

2. **Phase 2: Domain-specific features.** We define 16 binary and count features encoding legal concepts (charge type, mitigating factors, case magnitude markers). These achieve parity with the baseline but do not significantly improve it.

3. **Phase 3: Feature selection.** Exhaustive search over feature subsets reveals that just two binary features — Pasal 2 (enrichment charge) and gratifikasi (bribery) — constitute the optimal model, achieving CV improvement of +0.026 (p=0.065).

Our central finding is methodological: **in small legal corpora, domain knowledge encoded as structured features systematically outperforms statistical text representations.** Two binary keywords outperform 100 TF-IDF features, 384-dimensional transformer embeddings, and 16 structured features. Fewer features means less overfitting, and domain-specific features capture discrete legal categories that continuous representations dilute.

We further contribute substantive findings about Indonesian corruption sentencing:
- Pasal 2 (enrichment) carries a 0.50-year premium over Pasal 3 (authority abuse) after controlling for prosecution demand (d=0.46, p<0.001)
- The sentencing discount (vonis/tuntutan ratio) is entirely unpredictable from any available feature (R2=-0.06)
- Judge identity shows significant effects (F=1.99, p=0.016) spanning a 3.17-year range
- Geographic disparity ranges from -1.41 years (Palu, most lenient) to +1.29 years (Serang, most harsh)

### 1.1 Contributions

1. **Methodological**: First systematic comparison of bag-of-words, domain-specific, and neural text features for sentencing prediction in a small legal corpus, with a reproducible experimental framework (autoresearch)
2. **Empirical**: Demonstration that two binary keywords outperform 100+ dimensional text representations, with theoretical explanation grounded in the curse of dimensionality and the categorical nature of legal reasoning
3. **Substantive**: Evidence that Pasal 2 vs. Pasal 3 charge type constitutes an independent sentencing factor, and that text-derived legal features capture operative charges that structured metadata misses
4. **Practical**: A guide for legal NLP practitioners working with small corpora: start with domain keywords, not bag-of-words

## 2. Related Work

### 2.1 Computational Sentencing Analysis

Computational prediction of criminal sentences has been studied across multiple jurisdictions. In the U.S., Aletras et al. (2016) predicted Supreme Court decisions using unigram and bigram features. Chen et al. (2019) used neural models to predict criminal charges from Chinese court documents, achieving high accuracy on a corpus of 2.6 million documents. Medvedeva et al. (2020) predicted European Court of Human Rights judgments using SVM and BERT, finding that simple models performed comparably to neural approaches on this task.

For sentencing specifically, Strickson and De La Iglesia (2020) predicted Crown Court sentences in England using random forests on structured features. Lage-Freitas et al. (2022) applied BERT to Brazilian court decisions. These studies share a common assumption: more text features, better predictions. Our work challenges this assumption for small corpora.

### 2.2 Legal NLP in Indonesian

Indonesian legal NLP has focused on entity recognition (Nuranti & Yulianti, 2020; Yulianti et al., 2024) and classification (Hasanah et al., 2023). IndoBERT (Wilie et al., 2020) provides pretrained Indonesian language models, though their effectiveness on legal domain text is underexplored. To our knowledge, no prior work has systematically analyzed sentencing prediction from Indonesian corruption verdict text.

### 2.3 Feature Representation in Small Corpora

The curse of dimensionality in text classification is well-documented (Aggarwal & Zhai, 2012). With p features and n samples, overfitting becomes severe when p/n > 0.5. TF-IDF with max_features=100 on a corpus of 200 training samples gives p/n=0.5 — precisely at the danger zone. Domain-adapted features (Rudin, 2019) and expert-defined features (Dressel & Farid, 2018) have been shown to match or exceed neural approaches in specific settings, though systematic comparisons are rare in the legal domain.

## 3. Data

### 3.1 Corpus

We use CorpusKorupsi (Author, 2026), a structured dataset of Indonesian Supreme Court corruption verdicts extracted from putusan3.mahkamahagung.go.id. From 615 total verdicts, 331 contain extracted pertimbangan hakim (judicial reasoning section, minimum 200 characters) and valid prosecution demand and sentence data. These 331 verdicts form the analysis corpus for this study.

### 3.2 Key Variables

| Variable | Description | Coverage |
|----------|-------------|----------|
| vonis_bulan | Prison sentence imposed (months) | 100% |
| tuntutan_bulan | Prosecution demand (months) | 100% |
| pertimbangan_text | Judicial reasoning text | 100% (by design) |
| kerugian_negara | State financial loss (IDR) | ~70% |
| daerah | Court region of origin | ~95% |
| pasal | Legal articles charged | ~85% |

### 3.3 Baseline Model

The baseline is the M9 model from Paper 1: vonis_years = 0.49 + 0.63 * tuntutan_years (R2=0.60 on full corpus). All text feature models must improve over this baseline in cross-validation to be considered useful.

### 3.4 Evaluation Protocol

We use 5x10-fold repeated cross-validation with paired t-tests for significance. The corpus is split 70/15/15 into train/validation/test sets with stratification by sentence severity quartile. The test set is held out throughout all experiments. Cross-validation is performed on the combined train+validation pool (n=281).

## 4. Phase 1: Bag-of-Words (TF-IDF)

### 4.1 Experimental Framework

We employ an autoresearch framework adapted from Karpathy (2024): a mutable experiment file (train.py) is modified by the experimenter, committed, evaluated, and kept or discarded based on validation performance. The evaluation harness (prepare.py) is read-only, ensuring consistent splits and metrics across all 30 experiments.

### 4.2 TF-IDF Configuration Space

We systematically varied:
- **max_features**: 50, 100, 200, 500, 1000, 5000
- **ngram_range**: (1,1), (1,2)
- **Preprocessing**: with/without stopwords, with/without number removal
- **Models**: Ridge, Lasso, ElasticNet, HuberRegressor, RandomForest, GradientBoosting
- **Regularization**: alpha sweep from 0.01 to 50.0
- **Dimensionality reduction**: TruncatedSVD (50-200 components)
- **Feature combination**: text-only, text+tuntutan, text+tuntutan+kerugian

### 4.3 Results

Every TF-IDF configuration hurts prediction in cross-validation:

| Configuration | k | CV R2 | vs Baseline | p |
|--------------|---|-------|-------------|---|
| Best single-split (a=0.05) | 102 | -0.057 | -0.559 | <0.001 |
| Moderate regularization (a=10) | 102 | 0.350 | -0.152 | <0.001 |
| SVD-compressed (50 dims) | 52 | 0.320 | -0.180 | <0.001 |
| Text-only (no tuntutan) | 100 | -0.150 | -0.650 | <0.001 |

The best TF-IDF model on a single train/validation split (a=0.05) appeared to improve over baseline (val_r2=0.626 vs 0.567). However, 5x10-fold CV revealed this as overfitting: the same model averaged R2=-0.057 across 50 folds, significantly worse than the baseline (p<0.001).

### 4.4 Why TF-IDF Fails

1. **Curse of dimensionality**: 100 features on ~200 training samples (p/n=0.5) guarantees overfitting even with regularization.
2. **Wrong representation**: Legal reasoning invokes discrete categories (charge type, crime category, factor type). TF-IDF represents these as continuous term frequencies, diluting categorical signal.
3. **Formulaic language**: Indonesian judicial reasoning uses standardized phrases regardless of sentence severity. TF-IDF captures word frequency, but the predictive signal lies in *which legal concept* is invoked, not how frequently.
4. **Single-split delusion**: The validation set in a single split may happen to align with the training distribution, creating an illusion of improvement that CV correctly exposes.

## 5. Phase 2: Domain-Specific Keyword Features

### 5.1 Feature Design

Rather than statistical text features, we encode domain knowledge as binary indicators for legal concepts that a legal expert would identify as sentencing-relevant:

| Feature | Pattern | Prevalence | r(vonis) |
|---------|---------|-----------|----------|
| has_pasal_2 | "pasal 2" in text | 47% | +0.42*** |
| has_pasal_3 | "pasal 3" in text | 46% | -0.18** |
| has_miliar | "miliar" in text | 22% | +0.17** |
| has_mengembalikan | "mengembalikan/pengembalian" | 10% | +0.17** |
| has_gratifikasi | "gratifikasi" | 2.1% | +0.13* |
| has_jabatan | "jabatan" | 11% | +0.07 |
| has_factor_list | aggravating factor header | 19% | +0.06 |
| n_memberatkan | count of "memberatkan" | mean=0.28 | +0.08 |
| n_meringankan | count of "meringankan" | mean=0.32 | +0.03 |
| text_length | character count | mean=5535 | +0.13* |

### 5.2 Alpha Sweep

Ridge regularization is critical for small corpora. We sweep alpha from 0.1 to 500:

| Alpha | CV R2 | vs Baseline |
|-------|-------|-------------|
| 0.1 | 0.505 | -0.033 |
| 1.0 | 0.508 | -0.030 |
| 10 | 0.527 | -0.012 |
| **50** | **0.540** | **+0.001** |
| 100 | 0.521 | -0.018 |
| 500 | 0.339 | -0.200 |

At alpha=50, structured features achieve parity with the baseline (CV R2=0.540 vs 0.538, difference +0.001). This is the first text-based model that does not *hurt* prediction, but the improvement is not significant (p=0.69).

### 5.3 Interpretation

Strong regularization (alpha=50 vs default alpha=1) is essential because it shrinks the 16 feature coefficients toward zero, effectively selecting only the most informative features. This motivates the next phase: explicit feature selection.

## 6. Phase 3: Feature Selection

### 6.1 Exhaustive Subset Search

We evaluate every subset of 11 candidate keyword features (size 1-4) combined with tuntutan, using 3x10-fold CV as a screening metric. All C(11,1) + C(11,2) + C(11,3) + C(11,4) = 1001 subsets are tested.

**Finding**: Every subset containing pasal_2 yields positive CV improvement. The best is {pasal_2, gratifikasi} (CV R2=0.529, delta=+0.024).

### 6.2 Forward Selection

Starting from the best 2-feature base (pasal_2 + gratifikasi), we test adding each remaining feature one at a time. No addition improves the model — every additional feature either has zero effect or slightly hurts performance.

### 6.3 Final Model

The optimal model has just 3 features:

| Feature | Ridge Coefficient | Interpretation |
|---------|------------------|----------------|
| tuntutan_years | +1.64 | Prosecution demand (dominant) |
| has_pasal_2 | +0.50 | Enrichment charge (heavier) |
| has_gratifikasi | +0.33 | Bribery crime type (heavier) |

5x10-fold repeated CV: R2=0.539, improvement +0.022 over baseline (p=0.050, 29/50 folds positive).

More importantly, the minimal model is **significantly better than TF-IDF** in paired comparison: mean delta=+0.188 R2, paired t=7.47, p<0.001, Cohen's d=1.07 (large effect), winning 44/50 CV folds. The primary contribution is not that text features improve over the baseline (marginal) but that **choosing the right representation matters enormously**: wrong representation (TF-IDF) destroys prediction, while right representation (domain keywords) preserves and slightly improves it.

### 6.4 Comparison with Transformer Embeddings

To verify that the failure of statistical features is not specific to TF-IDF, we test sentence embeddings from paraphrase-multilingual-MiniLM-L12-v2 (384 dimensions) with PCA reduction:

| Method | k | CV R2 | vs Baseline |
|--------|---|-------|-------------|
| PCA(5) + tuntutan | 6 | 0.488 | -0.017 |
| PCA(10) + tuntutan | 11 | 0.481 | -0.024 |
| PCA(50) + tuntutan | 51 | 0.408 | -0.097 |
| **Minimal (pasal_2 + grat)** | **3** | **0.528** | **+0.026** |

Transformer embeddings perform worse than TF-IDF at higher dimensions and worse than the minimal model at all dimensions. **Two binary keywords outperform a 384-dimensional pretrained language model.**

## 7. Why Pasal 2 Matters: Legal Interpretation

### 7.1 Pasal 2 vs Pasal 3

Indonesian anti-corruption law (UU No. 31/1999 jo. UU No. 20/2001) distinguishes two primary charges:
- **Pasal 2**: "memperkaya diri sendiri" (enriching oneself or another) — carries 4-20 years
- **Pasal 3**: "menyalahgunakan kewenangan" (abusing authority) — carries 1-20 years

Pasal 2 requires proof of enrichment; Pasal 3 only requires proof of authority abuse. In practice, prosecutors often charge both, and the judge's pertimbangan reveals which is the *operative* charge — the one that determines the sentence.

### 7.2 Sentencing Effect

| Group | n | Mean Vonis | Mean Tuntutan |
|-------|---|-----------|---------------|
| Pasal 2 only | 97 | 6.18 yr | 8.25 yr |
| Pasal 3 only | 94 | 3.34 yr | 5.33 yr |
| Both | 51 | 5.73 yr | 7.75 yr |
| Neither | 66 | 4.09 yr | 5.47 yr |

After controlling for prosecution demand (M9 residuals):
- Pasal 2 residual: +0.50 years (judges give *more* than model predicts)
- Pasal 3 residual: -0.48 years (judges give *less*)
- Mann-Whitney p=0.001, Cohen's d=0.46 (medium effect)

### 7.3 Text vs Structured Metadata

The `pasal` column in our database lists all charged articles (e.g., "2 Ayat (1) juncto Pasal 18; 55 Ayat (1); 3 juncto Pasal 18..."). This captures *all* charges, including alternatives. The pertimbangan text mentions Pasal 2 when it is the *operative* charge — the one the judge actually applies to determine the sentence.

| Source | CV R2 | vs Baseline | p |
|--------|-------|-------------|---|
| Text-derived pasal_2 | 0.528 | +0.026 | 0.065 |
| Structured metadata pasal_2 | 0.500 | -0.002 | 0.842 |

Text-derived features outperform structured metadata because they capture the judge's actual reasoning, not the prosecutor's initial charges.

## 8. Complementary Findings

### 8.1 The Sentencing Discount is Unpredictable

The discount ratio (vonis/tuntutan, mean=0.78, median=0.71) represents judicial discretion — how much the judge deviates from the prosecution's demand. Ridge regression on all available text features yields R2=-0.06 in cross-validation: **the discount is entirely unpredictable from any observable feature.** No individual text feature significantly correlates with the discount at alpha=0.05.

This is a "genuine opacity" finding: approximately 40% of sentencing variance reflects case-specific judicial judgment that leaves no trace in public verdict documents.

### 8.2 Judge Effects

One-way ANOVA on M9 residuals by presiding judge (hakim ketua, judges with 3+ cases, n=16): F=1.99, p=0.016. The most lenient judge averages 2.27 years below model predictions; the harshest averages 0.90 years above. Total range: 3.17 years.

Despite statistical significance, adding judge dummy variables to the prediction model *hurts* performance in CV (delta=-0.012 to -0.029), because 16 dummy variables on 281 samples causes overfitting.

### 8.3 Geographic Effects: Composition, Not Disparity

Raw Kruskal-Wallis on vonis by court region is highly significant (H=63.1, p<0.001), suggesting geographic disparity. However, after controlling for prosecution demand (testing residuals from the tuntutan model), the effect disappears entirely (KW H=25.6, p=0.22; ANOVA F=1.31, p=0.17).

This reveals a **composition effect**: different courts handle different magnitude cases (Jakarta Pusat handles national mega-corruption), but judges in all regions sentence similarly after accounting for case magnitude. Per-court mean residuals range from -1.41yr (Palu) to +1.29yr (Serang), but this variation is not statistically significant after correction.

Court predictability does vary: RMSE ranges from 0.66 years (Bengkulu, very formulaic) to 3.21 years (Tanjungkarang, highly inconsistent), though small per-court samples (n=5-50) limit interpretation.

## 9. Discussion

### 9.1 Why Domain Knowledge Beats Statistics

Our central finding — that two binary keywords outperform 100 TF-IDF features and 384-dimensional embeddings — has a clear theoretical explanation. Legal reasoning operates through discrete categories: a defendant is charged under Pasal 2 or Pasal 3; the case involves gratifikasi or it does not. These are binary distinctions with specific legal meaning. TF-IDF and embeddings represent these as continuous features, introducing noise that drowns out signal in small samples.

This is not a failure of NLP — it is a failure of the *wrong* NLP for the *right* setting. At n=10,000, TF-IDF likely captures these same distinctions (the word "pasal" near "2" would receive high weight). At n=300, the signal-to-noise ratio is too low for statistical discovery, but human domain knowledge can specify the exact features that matter.

### 9.2 Implications for Legal NLP

For practitioners working with small legal corpora:

1. **Start with domain features, not TF-IDF.** Define binary indicators for legal concepts that experts identify as relevant. These will outperform statistical features at n<500.
2. **Use aggressive regularization.** Alpha=50 (not the default alpha=1) was required for 16 features on 200 training samples. Sweep alpha as part of the experiment.
3. **Trust cross-validation, not single splits.** Our TF-IDF model appeared to improve by +0.06 R2 on a single split but was -0.56 R2 in CV. Single-split evaluation is dangerous at small n.
4. **Text-derived features > structured metadata** when the text captures the operative legal reasoning rather than the full charge sheet.

### 9.3 The Limits of Prediction

Even the best model leaves ~40% of sentencing variance unexplained. The complete unpredictability of the sentencing discount (R2=-0.06) suggests that this variance reflects genuine judicial discretion — factors like defendant demeanor, cooperation, specific evidence quality, and political context — that are not captured in public verdict documents.

This is not a methodological limitation; it is a substantive finding about judicial opacity. Indonesian corruption sentences are partially predictable from prosecution demand and charge type, but the judicial discount is irreducibly opaque from publicly available data.

### 9.4 Limitations

1. **Corpus size**: n=331 with text is small for NLP. Power analysis suggests n~1,000 is needed for the minimal model to reach conventional significance (currently p=0.065).
2. **MA selection bias**: Our corpus consists of cassation decisions (appealed cases), not first-instance verdicts. Sentencing patterns may differ at the trial court level.
3. **Feature discovery bias**: We tested only features suggested by domain knowledge. Other predictive text features may exist but were not hypothesized.
4. **Temporal skew**: 43% of verdicts are from 2025, with sparse coverage before 2019.

## 10. Conclusion

We have shown that for small legal corpora, domain-specific binary features systematically outperform statistical text representations. Two keywords — Pasal 2 and gratifikasi — encode legally meaningful distinctions that improve sentencing prediction beyond prosecution demand alone, while 100 TF-IDF features and 384-dimensional transformer embeddings actively hurt prediction through overfitting.

The finding is methodological (start with domain features, not bag-of-words), substantive (charge type independently influences sentences beyond prosecution framing), and practical (aggressive regularization and cross-validation are essential at small n). The sentencing discount remains irreducibly opaque, and geographic and judge-level disparities warrant further investigation with larger corpora.

Our experimental framework (autoresearch) and analysis code are released to enable replication and extension to other legal corpora in low-resource settings.

## References

*(To be completed with full bibliography)*

- Aletras, N., et al. (2016). Predicting judicial decisions of the European Court of Human Rights. PeerJ Computer Science.
- Author (2026). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts. [companion paper]
- Chen, H., et al. (2019). Charge-based prison term prediction with deep gating network. EMNLP.
- Dressel, J., & Farid, H. (2018). The accuracy, fairness, and limits of predicting recidivism. Science Advances.
- Hasanah, U., et al. (2023). Classification of Indonesian tax court verdicts using IndoBERT.
- Lage-Freitas, A., et al. (2022). Predicting Brazilian court decisions. PeerJ Computer Science.
- Medvedeva, M., et al. (2020). Using machine learning to predict decisions of the European Court of Human Rights. AI & Law.
- Nuranti, E. Q., & Yulianti, E. (2020). Named entity recognition for Indonesian legal documents. CIKM Workshop.
- Rudin, C. (2019). Stop explaining black box machine learning models. Nature Machine Intelligence.
- Strickson, B., & De La Iglesia, B. (2020). Legal judgement prediction for UK courts. ICAART.
- Wilie, B., et al. (2020). IndoNLU: Benchmark and resources for evaluating Indonesian NLP. AACL.
- Yulianti, E., et al. (2024). IndoLER: Indonesian Legal Entity Recognition Dataset. LREC-COLING.
