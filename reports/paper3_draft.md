# Bidirectional Correction: How Indonesian Judges Override Low Prosecution Demands in Corruption Cases

## Abstract

How do judges process prosecution demands in sentencing? The anchoring literature predicts that prosecution demands set a reference point from which judges adjust. Using 367 Indonesian Supreme Court corruption verdicts, we find that the relationship between prosecution demand (*tuntutan*) and sentence (*vonis*) is not linear but significantly concave (quadratic term F=11.30, p<0.001). Judges compress the sentencing range to approximately 80% of the prosecution demand range, but this compression is not uniform: below a demand of approximately 2.4 years (bootstrap 95% CI [1.9, 2.9]), judges *increase* sentences beyond prosecution demands, while above this threshold, they apply an increasing discount reaching 35% at demands of 8-10 years. Upward departures — cases where judges exceed prosecution demands — constitute 13.6% of verdicts and are concentrated among low-demand cases (31% upward departure rate for demands under 4 years vs 2% for demands over 10 years). Logistic regression reveals that each one-year increase in prosecution demand reduces upward departure odds by 35% (OR=0.65, p<0.001), while Pasal 2 (enrichment) charges increase odds 3.6-fold (OR=3.63, p=0.001). The nonlinear anchoring effect survives controls for charge type (p<0.001), state financial loss (p=0.011), and heteroskedasticity-consistent standard errors (p=0.005). These findings suggest that Indonesian judges operate with an implicit sentencing norm for corruption and systematically correct prosecution demands perceived as too lenient — a form of bidirectional anchoring correction not previously documented in corruption sentencing.

## 1. Introduction

Sentencing research has long recognized that prosecution demands serve as anchors for judicial decision-making. Englich, Mussweiler, and Strack (2006) demonstrated experimentally that even *irrelevant* numerical anchors affect expert judges' sentencing decisions. In field studies of actual sentencing, prosecution demands consistently emerge as the strongest single predictor of sentence length (Author, 2026a; Strickson & De La Iglesia, 2020), with explained variance typically in the range of 40-70%.

However, the anchoring literature largely characterizes the judge-prosecution demand relationship as *unidirectional*: the demand anchors high, and judges adjust downward. The assumption of a uniform "sentencing discount" — where judges reduce prosecution demands by some relatively constant proportion — underlies much of the computational sentencing prediction literature. In a companion study of the same corpus (Author, 2026b), we reported that the sentencing discount (sentence/demand ratio, mean 0.78) is entirely unpredictable from available features (R²=-0.01), which we interpreted as judicial opacity.

In this paper, we challenge the uniform discount assumption by examining the *functional form* of the demand-sentence relationship. We find that the relationship is not linear but significantly concave: judges apply different discount rates depending on the magnitude of the prosecution demand. Specifically, judges *increase* sentences when prosecution demands are low and *decrease* sentences when demands are high — a pattern we term **bidirectional anchoring correction**.

This finding has two implications. First, it suggests that judges operate with an implicit sentencing norm — an internalized sense of appropriate sentence length for corruption — and systematically correct prosecution demands that deviate from this norm. Second, it refines the "judicial opacity" finding: the discount is not random but is partially structured by demand magnitude, a source of systematic variation that the linear model fails to capture.

### Research Questions

- **RQ1:** Is the relationship between prosecution demand and sentence length linear or nonlinear?
- **RQ2:** What characterizes cases in which judges exceed prosecution demands (upward departures)?
- **RQ3:** Is the nonlinear anchoring effect robust to controls for case characteristics, charge type, and time period?

## 2. Background

### 2.1 Anchoring in Sentencing

The anchoring effect in judicial decision-making is well established. Englich et al. (2006) showed that experienced judges' sentencing decisions were influenced by random numbers presented as prosecution demands, demonstrating that anchoring operates even on experts. In a broader review, Ulmer (2012) noted that unexplained variance in sentencing remains a persistent challenge across jurisdictions, with prosecution demands explaining substantial but incomplete portions of sentencing variation.

Anderson, Kling, and Stith (1999) documented significant interjudge sentencing disparity in US federal courts even after the introduction of structured sentencing guidelines, suggesting that judicial processing of sentencing inputs varies systematically across judges.

### 2.2 The Sentencing Discount

The ratio of sentence to prosecution demand — what we term the *sentencing discount* — has been studied primarily as a constant or near-constant phenomenon. In our companion analysis (Author, 2026b), the mean discount for Indonesian corruption sentences is 0.78 (judges give approximately 22% less than demanded), but the standard deviation is 0.47, indicating substantial variation.

A uniform discount model implies that judges apply roughly the same proportional reduction regardless of demand magnitude. If true, the demand-sentence relationship should be well described by a linear model with slope less than one. We test this assumption explicitly.

### 2.3 Upward Departures

Sentencing departures — cases where the sentence falls outside the expected range — have been extensively studied in the US federal system (Ulmer, 2012), where structured guidelines create formal departure categories. In unguided sentencing systems like Indonesia's, the concept of departure is less formally defined. We operationalize *upward departure* as any case where the sentence exceeds the prosecution demand (vonis > tuntutan).

Upward departures in corruption cases are particularly noteworthy given public discourse about "light sentencing" (*vonis ringan*) in Indonesian corruption cases. Indonesia Corruption Watch (ICW, 2025) reported an average corruption sentence of 3 years and 3 months in 2024, classified as "light" under Supreme Court Regulation No. 1/2020. Against this backdrop, cases where judges exceed prosecution demands represent instances of judicial severity that contradict the prevailing leniency narrative.

### 2.4 Indonesian Legal Context

Indonesian corruption sentencing operates without formal sentencing guidelines. Judges receive prosecution demands (*tuntutan pidana*) and determine sentences within statutory ranges specified by Law No. 31/1999 (as amended by Law No. 20/2001). The two most commonly charged articles are Pasal 2 (*memperkaya diri sendiri*; enrichment, 4-20 years) and Pasal 3 (*menyalahgunakan kewenangan*; authority abuse, 1-20 years). Supreme Court Regulation No. 1/2020 provides non-binding sentencing guidance but does not mandate specific sentence ranges for case characteristics.

## 3. Data and Methods

### 3.1 Corpus

We use CorpusKorupsi (Author, 2026a), comprising 367 analysis-ready Supreme Court corruption verdicts (valid sentence and prosecution demand) scraped from putusan3.mahkamahagung.go.id. Sentences range from 0.2 to 18.0 years (mean 4.75, SD 3.21); prosecution demands range from 0.2 to 20.0 years (mean 6.67, SD 4.02). Two cases with extreme discount ratios (>5.0) are excluded from regression analyses, leaving n=365.

### 3.2 Variables

| Variable | Description | n |
|----------|-------------|---|
| vonis_years | Prison sentence (years) | 367 |
| tuntutan_years | Prosecution demand (years) | 367 |
| tuntutan_sq | tuntutan_years squared | 367 |
| discount | vonis / tuntutan ratio | 367 |
| upward | Binary: vonis > tuntutan | 367 |
| has_pasal_2 | Pasal 2 in judicial reasoning | 367 |
| has_pasal_3 | Pasal 3 in judicial reasoning | 367 |
| kerugian_negara | State financial loss (IDR) | 291 |

### 3.3 Statistical Methods

**Nonlinear anchoring (RQ1).** We compare a linear model (vonis ~ tuntutan) with a quadratic model (vonis ~ tuntutan + tuntutan²) using an F-test. The crossover point (where predicted vonis equals tuntutan) is estimated analytically and bootstrapped (2,000 iterations). We also test piecewise linear regression and Chow's test for structural break.

**Upward departures (RQ2).** We model upward departure probability using logistic regression with tuntutan, Pasal 2, and Pasal 3 as predictors. Odds ratios and confidence intervals are reported.

**Robustness (RQ3).** The quadratic term is tested with controls for charge type (Pasal 2, Pasal 3), state financial loss (log-transformed), heteroskedasticity-consistent standard errors (HC3), and temporal subsamples (pre-2024 vs 2024+).

**Sentencing compression.** We quantify the degree to which judicial processing compresses the sentencing range relative to the prosecution demand range using the ratio of standard deviations and interquartile ranges.

## 4. Results

### 4.1 The Sentencing Discount Is Not Uniform

The sentencing discount varies systematically with prosecution demand magnitude:

| Demand band | n | Mean discount | Median | % Upward |
|---|---|---|---|---|
| 0-2 years | 26 | **1.132** | 0.917 | 30.8% |
| 2-4 years | 51 | **1.061** | 0.857 | 31.4% |
| 4-6 years | 99 | 0.750 | 0.750 | 16.2% |
| 6-8 years | 72 | 0.666 | 0.667 | 5.6% |
| 8-10 years | 44 | 0.649 | 0.625 | 6.8% |
| 10-15 years | 50 | 0.661 | 0.667 | 2.0% |
| 15-25 years | 23 | 0.704 | 0.706 | 0.0% |

For demands below 4 years, judges *on average* give sentences exceeding prosecution demands (discount > 1). For demands above 4 years, judges discount by 25-35%. The upward departure rate drops from ~31% for low-demand cases to 0% for the highest demands. This is inconsistent with a uniform discount model.

### 4.2 The Quadratic Anchoring Model

Adding a quadratic term significantly improves model fit:

| Model | R² | AIC | tuntutan² p |
|---|---|---|---|
| Linear: vonis ~ tuntutan | 0.608 | 1550.5 | — |
| Quadratic: vonis ~ tuntutan + tuntutan² | 0.620 | 1541.3 | **0.0009** |

F-test (quadratic vs linear): F=11.30, p<0.001. The quadratic specification explains an additional 1.2% of variance (R² improvement from 0.608 to 0.620), with a substantial improvement in model fit (Delta-AIC=9.2).

The estimated crossover point — where predicted sentence equals prosecution demand — is 2.4 years (bootstrap 95% CI [1.9, 2.9]). Below this threshold, the model predicts sentences exceeding demands; above it, sentences are discounted.

Piecewise linear regression with a cutpoint at 2 years shows different slopes below and above the threshold (below: b=−0.33; above: b=+0.63), but Chow's test for structural break is not significant (F=0.18, p=0.83), supporting the smooth quadratic model over a sharp breakpoint.

### 4.3 Upward Departures

Fifty cases (13.6%) have sentences exceeding prosecution demands. Logistic regression identifies two significant predictors:

| Predictor | Coefficient | OR | 95% CI | p |
|---|---|---|---|---|
| tuntutan_years | −0.431 | **0.650** | — | <0.001 |
| has_pasal_2 | +1.290 | **3.633** | — | 0.001 |
| has_pasal_3 | −0.547 | 0.579 | — | 0.132 |

Each one-year increase in prosecution demand reduces the odds of upward departure by 35%. Pasal 2 (enrichment) charges increase upward departure odds 3.6-fold, suggesting that judges are more likely to override prosecution demands perceived as too lenient in cases involving personal enrichment.

### 4.4 Sentencing Compression

Judges compress the sentencing range relative to prosecution demands. The standard deviation of sentences (3.22 years) is 80% of the standard deviation of demands (4.02 years). The interquartile range of sentences (4.00 years) is 89% of the demand IQR (4.50 years). This compression is not equivalent to a uniform discount; it is driven by the nonlinear processing documented above.

### 4.5 Robustness

The quadratic anchoring effect is robust to multiple specifications:

| Specification | tuntutan² p | Survives? |
|---|---|---|
| Base quadratic model | 0.0009 | Yes |
| + Pasal 2 + Pasal 3 controls | 0.0004 | Yes |
| + log(kerugian negara) | 0.011 | Yes |
| HC3 robust standard errors | 0.005 | Yes |
| Excluding extreme discounts (0.1-3.0) | 0.014 | Yes |
| Post-2024 subsample (n=229) | 0.0003 | Yes |
| Pre-2024 subsample (n=136) | 0.624 | **No** |

The effect is robust across all specifications except the pre-2024 temporal subsample (n=136), where the quadratic term is positive but non-significant (p=0.62). A bootstrap power analysis resolves this ambiguity: at n=136, power to detect the quadratic effect (at the magnitude observed in the full sample) is only approximately 50% at p<0.05, compared to 72% at n=229 and 88% at n=365. The pre-2024 non-significance is consistent with insufficient power rather than absence of effect. Furthermore, a temporal interaction test (tuntutan-squared multiplied by a post-2024 indicator) is not significant (p=0.561), meaning we cannot reject that the pattern is identical across time periods.

Additionally, an interaction between prosecution demand and Pasal 2 charge type is significant (p=0.035), indicating that the anchoring pattern differs slightly for enrichment cases — though the quadratic nonlinearity is present in both Pasal 2 (p=0.012) and Pasal 3-only (p=0.023) subsamples.

A permutation test (1,000 shuffled datasets) confirms that the quadratic effect is not an artifact of regression to the mean: 0% of permutations produce a comparable quadratic term at p<0.001.

The cubic specification adds no significant improvement (cubic term p=0.322, F-test vs quadratic p=0.322, AIC worse), confirming that the quadratic is the optimal polynomial. A log-log specification yields an elasticity of 0.77, independently confirming sentencing compression: a 1% increase in prosecution demand produces only a 0.77% increase in sentence.

## 5. Discussion

### 5.1 Bidirectional Anchoring Correction

Our central finding — that judges systematically increase sentences when prosecution demands are low and decrease them when demands are high — extends the anchoring literature beyond its typical unidirectional framing. Classic anchoring (Englich et al., 2006) predicts adjustment from a reference point, but the direction of adjustment is typically assumed to be downward from the anchor. Our data show *bidirectional* correction: judges pull both low and high demands toward an implicit sentencing range.

The crossover point of 2.4 years (CI [1.9, 2.9]) suggests that judges implicitly regard demands below approximately 2-3 years as insufficiently severe for corruption cases. For perspective, the statutory minimum for Pasal 2 (enrichment) is 4 years. Prosecution demands below this statutory minimum — which do occur in alternative charge configurations — appear to trigger judicial override.

The 3.6-fold increase in upward departure odds for Pasal 2 cases is particularly striking. It suggests that judges are especially likely to override lenient prosecution demands when the case involves personal enrichment — a form of judicial severity that has not been quantified in the Indonesian literature.

### 5.2 The Implicit Sentencing Norm

The compression of the sentencing range to ~80% of the prosecution demand range, combined with the bidirectional correction pattern, suggests that Indonesian judges operate with an **implicit sentencing norm** for corruption cases. This norm is not codified in any formal guideline (Supreme Court Regulation No. 1/2020 provides guidance but is non-binding), yet it produces a detectable statistical signature.

This finding has implications for the ongoing policy debate about sentencing guidelines in Indonesia. If judges already apply an implicit norm — compressing extreme demands toward a central range — then formal guidelines might formalize rather than fundamentally change existing judicial behavior. Conversely, the wide variation in individual judge slopes (−0.39 to 0.99 across judges with 5+ cases) suggests that the implicit norm is not uniformly shared, leaving room for formal guidelines to reduce disparity.

### 5.3 Limitations

**Temporal instability.** The quadratic effect is significant only in the post-2024 subsample (n=229, p<0.001) and not in the pre-2024 subsample (n=136, p=0.62). Bootstrap power analysis strongly favors the power explanation: at n=136, statistical power is approximately 50% — a coin flip. The temporal interaction test (p=0.561) cannot reject that the pattern is identical across periods. Nevertheless, we cannot definitively rule out a genuine temporal change. Future work with a larger historical corpus could provide a definitive test.

**Cassation-level data.** Our corpus consists of Supreme Court cassation decisions — cases that were appealed. The anchoring correction pattern may differ at the trial court level, where judges make initial sentencing decisions without the appellate context of correcting a lower court's judgment. The upward departures in our data may partly reflect the appellate court correcting trial-level leniency rather than correcting prosecution demands per se.

**The quadratic is a statistical convenience.** The true functional form of the demand-sentence relationship may be better described by a spline, a log transformation, or some other specification. The quadratic model is the simplest polynomial that captures nonlinearity; we do not claim that the underlying judicial process is literally quadratic.

**Endogeneity of charge type.** The Pasal 2 indicator is extracted from judicial reasoning text, creating potential circularity (discussed in Author, 2026b). The upward departure analysis should be interpreted as an association, not a causal claim about charge type.

## 6. Conclusion

We document a nonlinear anchoring pattern in Indonesian corruption sentencing: judges systematically correct prosecution demands perceived as too low (bidirectional correction), compress the sentencing range to ~80% of the demand range, and override prosecution demands in 13.6% of cases — primarily when demands are low and charges involve personal enrichment. The quadratic specification significantly outperforms the linear model (F=11.30, p<0.001) and survives controls for charge type, state financial loss, and heteroskedasticity.

These findings challenge the common assumption of a uniform sentencing discount and reveal structure in what appeared to be random judicial variation. The implicit sentencing norm they imply — with judges pulling extreme demands toward a central range — suggests that Indonesian corruption sentencing is more systematic than either the "judicial opacity" narrative or the "light sentencing" criticism would suggest. Judges do not simply rubber-stamp prosecution demands; they evaluate demands against an internalized standard and correct accordingly.

The CorpusKorupsi dataset and analysis code are publicly available at [repository URL].

## Declarations

**Funding.** This research received no external funding.
**Conflicts of interest.** The author declares no conflicts of interest.
**Ethics approval.** This study analyzes publicly available court documents. No human subjects were involved.
**Data availability.** The CorpusKorupsi structured dataset and analysis scripts are available at [repository URL].

## References

Anderson, J. M., Kling, J. R., & Stith, K. (1999). Measuring interjudge sentencing disparity: Before and after the federal sentencing guidelines. *Journal of Law and Economics*, 42(S1), 271-307. https://doi.org/10.1086/467425

Author (2026a). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns. [Companion paper]

Author (2026b). Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences. [Companion paper]

Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. *Personality and Social Psychology Bulletin*, 32(2), 188-200. https://doi.org/10.1177/0146167205282152

Indonesia Corruption Watch (2025). Sentencing trend monitoring report 2024. Jakarta: ICW.

Strickson, B., & De La Iglesia, B. (2020). Legal judgement prediction for UK Crown Court criminal cases. *Proceedings of ICAART*, 458-465.

Ulmer, J. T. (2012). Recent developments and new directions in sentencing research. *Justice Quarterly*, 29(1), 1-40. https://doi.org/10.1080/07418825.2011.583932
