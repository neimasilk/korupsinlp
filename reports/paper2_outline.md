# Paper 2: Beyond Structured Features — Text Features and the Limits of Sentencing Prediction

## Working Title
**"What Explains the Other 40%? Text Features, Judge Effects, and the Limits of Computational Sentencing Analysis in Indonesian Corruption Cases"**

## Target Venue
- Primary: ICWSM, CSS Workshop, or Journal of Empirical Legal Studies
- Computational legal studies venue

## Core Narrative

Paper 1 showed tuntutan explains ~60% of sentencing variance (R²=0.60). This paper systematically tests whether *anything* can explain the remaining 40%.

**Key finding**: Nothing reliably does — not structured features, not judge identity, not TF-IDF text features. The 40% is likely *irreducible* with available data, driven by case-specific facts not captured in public verdicts.

## Autoresearch Results (30 experiments, 9 April 2026)

### Text features do NOT improve prediction
**30 systematic experiments** via the autoresearch framework, testing:
- TF-IDF settings: max_features (50-5000), ngrams (1-2), min_df, max_df, sublinear_tf, binary
- Models: Ridge, Lasso, ElasticNet, HuberRegressor, RandomForest, GradientBoosting
- Features: text_only, text+tuntutan, text+tuntutan+kerugian, keyword counts, SVD compression
- Regularization: alpha sweep 0.01 to 50.0
- Preprocessing: stopwords, text truncation

**Best single-split result**: val_r2=0.626 (100 TF-IDF unigrams + tuntutan + kerugian, Ridge alpha=0.05)
**But cross-validation reveals overfit**: 5×10-fold CV mean R²=0.460, significantly WORSE than baseline (0.532, p<0.0001)

| Model | CV Mean R² (5×10-fold) | vs M9 Baseline |
|-------|----------------------|----------------|
| M9 baseline (fixed) | 0.532 | — |
| Ridge tuntutan only | 0.522 | -0.010 |
| Best TF-IDF + all (α=10) | 0.513 | -0.019 |
| Best TF-IDF + all (α=0.05) | 0.460 | -0.072 |
| TF-IDF text only | -0.042 | -0.574 |

**No alpha value makes text features break even with baseline.**

### Descriptive text analysis (what words associate with sentence severity)
Despite not helping prediction, word analysis reveals sensible patterns:

**Words significantly correlated with HEAVIER sentences** (Spearman, p<0.05):
- "miliar" (r=+0.23): large state loss cases
- "negara" (r=+0.19): state-level corruption
- "keuangan" (r=+0.15): financial crimes
- "dakwaan" (r=+0.16): more specific charges
- "uang" (r=+0.16): money-related language

**Words associated with LIGHTER sentences** (Spearman, p<0.05):
- "kasasi" (r=-0.15): appeal-related language (procedural, not substantive)

**Prevalence gap** (heavy vs light quartile):
- "miliar" appears in 33% of heavy cases but only 15% of light — but this is a proxy for kerugian magnitude, which is already in the structured model

### Previous findings (structured features and judge effects)
| Source | % of total variance |
|--------|-------------------|
| Tuntutan | ~50% |
| Kerugian (independent) | ~12% |
| Judge identity | ~2% (ICC=0.036 after controls) |
| Other structured (pasal, amar) | <0.5% |
| Text features (TF-IDF) | **0% (negative in CV)** |
| **Unexplained** | **~36%** |

## Interpretation

Three explanations for why text doesn't help:

1. **Corpus too small** (n=288 with text): NLP needs more data. TF-IDF on 100 features with 200 training samples hits fundamental statistical limits. Scaling to 1000+ verdicts could change this.

2. **Pertimbangan is formulaic**: Judicial reasoning may follow templates that don't discriminate between light/heavy sentences. The same phrases ("perbuatan terdakwa tidak mendukung program pemberantasan korupsi") appear in nearly all cases regardless of severity.

3. **Genuine opacity**: The 40% truly reflects case-specific factors (defendant cooperation, specific evidence, political context) that leave no textual trace in public verdicts. This IS the paper's finding — judicial discretion is measurably opaque.

## Paper Structure

1. **Introduction**: Paper 1 found R²=0.60. What explains the rest?
2. **Related Work**: Computational sentencing analysis, text features in legal NLP
3. **Method**: Autoresearch framework, 30 experiments, cross-validation protocol
4. **Results - Structured**: Additional features (pasal, amar, judges) add <3%
5. **Results - Text**: TF-IDF features fail in CV despite appearing to help on single split
6. **Results - Descriptive**: Word associations (sensible but not predictive beyond structure)
7. **Discussion**: Why text fails — sample size vs formulaic language vs genuine opacity
8. **Implications**: For legal NLP, for anti-corruption policy, for corpus scaling
9. **Conclusion**: 40% of sentencing variance is irreducible with current data

## Key Contribution

**Honest negative result**: Systematically demonstrating that text features from Indonesian corruption verdicts do not improve sentencing prediction is a contribution to computational legal studies. Most papers only report when features work. This paper shows when they don't, why, and what it means.

## Required Next Steps

| Step | Effort | Priority |
|------|--------|----------|
| Write Paper 2 draft (narrative around findings) | 2-3 days | HIGH |
| Scale corpus to 1000+ verdicts | 1-2 weeks | HIGH |
| Re-run autoresearch on larger corpus | Overnight | HIGH |
| Try IndoBERT embeddings (if larger corpus helps TF-IDF) | 1 day | MEDIUM |
| Quantile regression | 2-3 hours | LOW |

## Scope Control

**IN scope**: autoresearch results, CV analysis, descriptive word analysis, scaling rationale
**MAYBE**: IndoBERT (only if larger corpus shows TF-IDF promise)
**OUT of scope**: causal inference, new data sources, network analysis
