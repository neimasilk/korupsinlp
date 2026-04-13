# Supplementary Materials

## Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences

---

### S1. TF-IDF Experiment Log (30 Experiments)

The following table summarizes all TF-IDF experiments conducted using the autoresearch framework. Each row represents one experiment where the text feature configuration was modified, committed, evaluated on a single train/validation split, and then assessed via 5x10-fold repeated cross-validation.

| # | Configuration | Single-split R2 | CV R2 | vs Baseline |
|---|--------------|----------------|-------|-------------|
| 1 | TF-IDF 5000, bigrams, a=1.0 | 0.546 | <0 | -0.55 |
| 2-3 | Reduce max_features (500, 200) | 0.56-0.57 | <0 | ~-0.50 |
| 4 | max_features=200, a=1.0 | 0.568 | 0.10 | -0.43 |
| 5 | max_features=100 | 0.569 | 0.11 | -0.42 |
| 7 | Unigrams only | 0.576 | 0.15 | -0.38 |
| 11 | +kerugian_negara | 0.580 | 0.18 | -0.35 |
| 18 | Ridge a=0.1 | 0.622 | 0.35 | -0.18 |
| 21 | Ridge a=0.05 (best single-split) | 0.626 | -0.06 | -0.59 |
| — | Lasso, ElasticNet | <0.56 | <0 | — |
| — | RandomForest, GBM | 0.50-0.55 | <0.30 | >-0.20 |
| — | Stopword removal | <0.57 | <0.10 | — |
| — | SVD compression (50-200d) | 0.55-0.58 | 0.15-0.32 | -0.20 to -0.38 |
| — | Text truncation (last 2000 chars) | <0.57 | <0.10 | — |
| — | Binary TF-IDF | <0.55 | <0 | — |

**Key observation**: The best single-split result (R2=0.626, experiment 21) appeared to beat the baseline (0.567). However, 5x10-fold CV revealed this as overfitting: the same model averaged R2=-0.06 across 50 folds, significantly worse than baseline (p<0.001). This "single-split delusion" is a cautionary tale for small-corpus NLP.

### S2. Transformer Embedding Results

| Model | Dimensions | PCA | CV R2 | vs Baseline |
|-------|-----------|-----|-------|-------------|
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 5 | 0.488 | -0.017 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 10 | 0.481 | -0.024 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 20 | 0.456 | -0.049 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 50 | 0.408 | -0.097 |

More PCA dimensions = worse performance, consistent with overfitting at n~300.

### S3. Domain Keyword Feature Prevalence

| Feature | Pattern | Prevalence | r(vonis) | r(residual) |
|---------|---------|-----------|----------|-------------|
| has_pasal_2 | "pasal 2" in pertimbangan | 47% | +0.42*** | +0.19** |
| has_pasal_3 | "pasal 3" in pertimbangan | 46% | -0.18** | -0.10 |
| has_miliar | "miliar" (billion) | 22% | +0.17** | +0.10 |
| has_mengembalikan | "mengembalikan/pengembalian" (returning funds) | 10% | +0.17** | -0.01 |
| has_gratifikasi | "gratifikasi" (bribery/gifts) | 2.1% | +0.13* | +0.11 |
| has_pencucian | "pencucian uang" (money laundering) | 3.0% | +0.17** | +0.10 |
| has_jabatan | "jabatan" (position/office) | 11% | +0.07 | +0.05 |
| has_suap | "suap" (bribery) | 2.6% | +0.11 | -0.03 |
| has_uang_pengganti | "uang pengganti" (restitution) | 18% | +0.04 | +0.02 |
| has_factor_list | aggravating factor header | 19% | +0.06 | -0.10 |
| n_memberatkan | count of "memberatkan" (aggravating) | mean=0.28 | +0.08 | -0.02 |
| n_meringankan | count of "meringankan" (mitigating) | mean=0.32 | +0.03 | -0.09 |
| text_length | character count of pertimbangan | mean=11,721 | +0.13* | +0.04 |

r(vonis) = Spearman correlation with sentence. r(residual) = correlation with residual from tuntutan model. * p<0.05, ** p<0.01, *** p<0.001.

### S4. Alpha Sweep (Ridge Regularization)

All 16 keyword features + tuntutan, 5x10-fold CV:

| Alpha | CV R2 | vs Baseline |
|-------|-------|-------------|
| 0.1 | 0.505 | -0.033 |
| 1.0 | 0.508 | -0.030 |
| 5.0 | 0.519 | -0.020 |
| 10 | 0.527 | -0.012 |
| 20 | 0.536 | -0.002 |
| **50** | **0.540** | **+0.001** |
| 100 | 0.521 | -0.018 |
| 200 | 0.466 | -0.072 |
| 500 | 0.339 | -0.200 |

### S5. Exhaustive Feature Subset Search

Best subsets (3x10-fold CV, tuntutan always included):

| Subset | CV R2 | vs Baseline |
|--------|-------|-------------|
| {pasal_2} | 0.520 | +0.015 |
| {pasal_2, gratifikasi} | 0.529 | +0.024 |
| {pasal_2, miliar, factor_list, gratifikasi} | 0.529 | +0.024 |
| {pasal_2, pasal_3, gratifikasi} | 0.529 | +0.024 |

Every subset containing pasal_2 yields positive improvement. No subset without pasal_2 exceeds +0.008.

### S6. Subsample Robustness for Pasal 2 OLS

| Subsample | n | b(Pasal 2) | 95% CI | p |
|-----------|---|-----------|--------|---|
| 50% | 175 | +0.934 | [+0.278, +1.589] | 0.006 |
| 60% | 210 | +0.730 | [+0.120, +1.341] | 0.019 |
| 70% | 245 | +0.752 | [+0.183, +1.321] | 0.010 |
| 80% | 280 | +0.768 | [+0.260, +1.276] | 0.003 |
| 90% | 315 | +0.835 | [+0.367, +1.303] | 0.001 |
| 100% | 350 | +0.734 | [+0.286, +1.182] | 0.001 |

The coefficient is significant at p<0.05 at every subsample size tested.

### S7. Model Robustness Across Estimators

4-feature model (tuntutan + pasal_2 + gratifikasi + pencucian_uang), 5x10 CV:

| Estimator | CV R2 | vs Baseline | p |
|-----------|-------|-------------|---|
| Ridge (a=20) | 0.549 | +0.021 | 0.010 |
| Ridge (a=10) | 0.549 | +0.021 | 0.005 |
| Ridge (a=5) | 0.549 | +0.020 | 0.004 |
| Lasso (a=0.01) | 0.548 | +0.020 | 0.003 |
| ElasticNet (a=0.1) | 0.548 | +0.019 | 0.008 |

All estimators give p<0.01 — the finding is model-agnostic.

### S8. Data Availability

The CorpusKorupsi dataset (structured fields, no raw text for copyright reasons), extraction pipeline source code, and analysis scripts are available at [repository URL]. The autoresearch framework and experiment logs are included for full reproducibility.
