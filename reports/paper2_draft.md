# Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences

## Abstract

We computationally analyze 648 Indonesian Supreme Court corruption verdicts to examine what determines sentence severity beyond prosecution demand. Using OLS regression on structured and text-derived features, we find that **charge type independently affects sentencing**: cases invoking Pasal 2 (enrichment) of the Anti-Corruption Law receive sentences 0.72 years longer than equivalent cases, after controlling for prosecution demand (b=0.724, 95% bootstrap CI [0.255, 1.203], p=0.002). The effect is medium-sized (Cohen's d=0.50, CI [0.22, 0.79]) and driven by the legal distinction between Pasal 2 (enrichment, carrying 4-20 years) and Pasal 3 (authority abuse, 1-20 years). Notably, text-derived charge type outperforms structured case metadata because judicial reasoning reveals the *operative* charge, while metadata lists all charges including alternatives. We further find that the **sentencing discount** (the ratio of sentence to prosecution demand, mean 0.78) is **entirely unpredictable** from any available feature (cross-validated R2=-0.10), suggesting genuine judicial opacity: approximately 40% of sentencing variance reflects case-specific factors that leave no trace in published verdicts. Systematic experiments with bag-of-words (TF-IDF), transformer embeddings, and domain-specific keyword features confirm that text mining cannot reliably improve sentencing prediction beyond prosecution demand at this corpus size (n=341), though the direction is consistently positive across random splits (10/10 positive, 4/10 significant). Geographic sentencing variation is a composition effect that disappears after controlling for prosecution demand (Kruskal-Wallis p<0.001 raw, p=0.16 controlled), while judge-level effects are statistically significant (ANOVA F=1.94, p=0.020) but span only ~3 years and are not predictively useful. Our findings suggest that Indonesian corruption sentencing is partially predictable from prosecution demand and charge type, but judicial discretion in the sentencing discount is irreducibly opaque from public court documents.

## 1. Introduction

Corruption remains Indonesia's most persistent governance challenge. Transparency International's 2024 Corruption Perceptions Index ranks Indonesia 109th of 182 countries (score 34/100), and the country has seen thousands of corruption prosecutions since the establishment of the Corruption Eradication Commission (KPK) in 2003. Yet despite the availability of public court verdicts through the Supreme Court's online directory, no large-scale computational analysis of corruption sentencing patterns has been undertaken.

In a companion study (Author, 2026), we constructed CorpusKorupsi, a structured dataset of Indonesian Supreme Court corruption verdicts, and established that prosecution demand (tuntutan) explains approximately 60% of sentencing variance (R2=0.60, n=370). This leaves a fundamental question: **what explains the other 40%?**

We address this question through three research questions:

- **RQ1: Does charge type independently affect sentence severity?** Indonesian anti-corruption law distinguishes between Pasal 2 (enrichment; *memperkaya diri sendiri*) and Pasal 3 (authority abuse; *menyalahgunakan kewenangan*). Do judges treat these differently after accounting for prosecution demand?

- **RQ2: Can computational text analysis improve sentencing predictions?** The judicial reasoning section (*pertimbangan hakim*) of each verdict contains the judge's stated rationale. Can text features from this section explain sentencing variance beyond prosecution demand?

- **RQ3: Is the sentencing discount predictable?** The gap between prosecution demand and actual sentence (mean 78% of demand) represents judicial discretion. Is this gap systematic or opaque?

Our findings reveal a partially predictable, partially opaque sentencing system. Charge type adds a meaningful independent effect (Pasal 2 cases receive ~0.72 years more), but the sentencing discount is entirely unpredictable from available data. Text mining approaches — from bag-of-words to transformer embeddings — fail to improve predictions, an honest negative result that we document systematically to guide future research on small legal corpora.

### Contributions

1. **Empirical**: First quantitative evidence that Pasal 2 (enrichment) carries an independent sentencing premium of 0.72 years over equivalent Pasal 3 (authority abuse) cases in Indonesian corruption sentencing (d=0.50, p=0.002)
2. **Policy-relevant**: Demonstration that the sentencing discount is irreducibly opaque from public court documents (R2=-0.10), with implications for sentencing consistency monitoring
3. **Methodological**: Systematic documentation that text features (TF-IDF, transformer embeddings, domain keywords) do not reliably improve corruption sentencing prediction at n<500, an honest negative result for the legal NLP community
4. **Analytical**: Evidence that apparent geographic sentencing disparity is a composition effect, not judicial bias, and that judge-level variation is real but not predictively useful

## 2. Legal and Institutional Background

### 2.1 The Indonesian Anti-Corruption Legal Framework

Indonesia's primary anti-corruption statute is Law No. 31 of 1999 on the Eradication of Corruption (*Undang-Undang Pemberantasan Tindak Pidana Korupsi*), as amended by Law No. 20 of 2001. The law distinguishes several offense types, of which two are most commonly charged:

**Pasal 2** (*memperkaya diri sendiri atau orang lain*; enriching oneself or another person) carries a sentence of 4 to 20 years imprisonment and requires proof that the defendant enriched themselves or others through acts against the law, resulting in state financial loss. This is considered the more serious charge.

**Pasal 3** (*menyalahgunakan kewenangan*; abusing authority) carries 1 to 20 years and requires proof that the defendant, as a public official, abused their authority, opportunity, or means available to them. This is considered less severe as it does not require proof of personal enrichment.

In practice, prosecutors often charge defendants under both articles in alternative counts (*dakwaan alternatif* or *dakwaan subsidair*), allowing the judge to determine which is proven. The judge's selection of the operative article — revealed in the *pertimbangan hakim* (judicial reasoning) section of the verdict — determines the applicable sentencing range.

### 2.2 The Sentencing Process

Indonesian corruption sentencing follows a structured process: the prosecution submits a sentencing demand (*tuntutan*), the defense responds, and the panel of judges deliberates and issues a verdict (*putusan*) with a stated sentence (*vonis*) and written reasoning (*pertimbangan*). The reasoning section typically includes aggravating factors (*hal-hal yang memberatkan*) and mitigating factors (*hal-hal yang meringankan*).

### 2.3 The Cassation Process

The Supreme Court (*Mahkamah Agung*, MA) hears corruption cases at the cassation (*kasasi*) and case review (*peninjauan kembali*, PK) levels. Our corpus consists of these appellate-level decisions, which represent cases where either the defendant or the prosecution was dissatisfied with the lower court verdict. This introduces a selection effect: our data reflects sentencing *among appealed cases*, not the full population of corruption sentences. We discuss the implications of this selection in Section 5.4.

### 2.4 Prior Sentencing Studies

Quantitative analysis of Indonesian corruption sentencing has been limited to grey literature. Indonesia Corruption Watch (ICW) publishes annual sentencing reports based on manual case review, noting trends in average sentences and acquittal rates. However, no peer-reviewed study has applied computational methods to analyze sentencing determinants across hundreds of verdicts. Our work fills this gap by providing the first regression-based analysis of corruption sentencing factors using a structured, computationally extracted corpus.

## 3. Data and Methods

### 3.1 Corpus

We use CorpusKorupsi (Author, 2026), comprising 648 Supreme Court corruption verdicts scraped from putusan3.mahkamahagung.go.id. After filtering for valid sentences (vonis > 0) and prosecution demand (tuntutan > 0), 371 verdicts are analysis-ready. Of these, 341 contain extracted judicial reasoning text (pertimbangan hakim, minimum 200 characters), forming the text analysis corpus. Verdicts span 2011-2026, with heavier representation of 2024-2026 (58%).

### 3.2 Variables

| Variable | Description | n | Coverage |
|----------|-------------|---|----------|
| vonis_years | Prison sentence (years) | 371 | 100% |
| tuntutan_years | Prosecution demand (years) | 371 | 100% |
| has_pasal_2 | Pasal 2 mentioned in pertimbangan | 341 | Text corpus |
| has_pasal_3 | Pasal 3 mentioned in pertimbangan | 341 | Text corpus |
| kerugian_negara | State financial loss (IDR) | 271 | 73% |
| daerah | Court region of origin | 349 | 94% |
| discount | vonis / tuntutan ratio | 371 | 100% |

**Text-derived vs structured charge type.** The database includes a `pasal` metadata column listing all charged articles. We extract `has_pasal_2` from the judicial reasoning text (*pertimbangan*) rather than from this structured column because the pertimbangan reveals the **operative** charge — the article the judge actually applies — while the metadata lists all charges including alternatives that were not proven.

### 3.3 Statistical Methods

**Primary analysis (RQ1).** We estimate the independent effect of charge type using OLS regression: vonis_years = b0 + b1 * tuntutan_years + b2 * has_pasal_2 + e. We report the coefficient b2 with heteroscedasticity-consistent standard errors, 95% confidence intervals (both parametric and bootstrap with 2,000 iterations), and compare Model 2 (with Pasal 2) against Model 1 (tuntutan only) using an F-test. Effect size is reported as Cohen's d on residuals, comparing Pasal 2-only cases against Pasal 3-only cases.

**Text feature experiments (RQ2).** We test three text representation approaches using 5x10-fold repeated cross-validation with paired t-tests: (a) TF-IDF bag-of-words (100 features, Ridge regression), (b) transformer sentence embeddings (paraphrase-multilingual-MiniLM-L12-v2, 384 dimensions with PCA reduction), and (c) domain-specific binary keyword features. Multi-seed robustness is assessed by repeating the analysis across 10 random train/test splits.

**Discount analysis (RQ3).** We regress the discount ratio (vonis/tuntutan) on all available features using Ridge regression with 10-fold cross-validation. Individual feature correlations are reported with Bonferroni correction.

**Geographic and judge effects.** We compare Kruskal-Wallis tests on raw sentence vs residuals after controlling for prosecution demand to distinguish genuine disparity from composition effects. Judge effects are assessed via one-way ANOVA on residuals by presiding judge (hakim ketua, judges with 3+ cases).

## 4. Results

### 4.1 Charge Type Independently Affects Sentencing (RQ1)

Adding text-derived Pasal 2 to the tuntutan-only regression significantly improves model fit (F=9.89, p=0.002):

| Model | R2 | Adj R2 | Pasal 2 coef | 95% CI | p |
|-------|-----|--------|-------------|--------|---|
| vonis ~ tuntutan | 0.593 | 0.592 | — | — | — |
| vonis ~ tuntutan + pasal_2 | 0.605 | 0.603 | +0.724 | [0.271, 1.176] | 0.002 |
| vonis ~ tuntutan + pasal_2 + pasal_3 | 0.610 | 0.607 | +0.667 | [0.214, 1.120] | 0.004 |

Bootstrap confirmation (2,000 iterations): Pasal 2 coefficient 95% CI = [0.255, 1.203], excluding zero.

Comparing Pasal 2-only cases (n=98, mean 6.18yr) with Pasal 3-only cases (n=96, mean 3.34yr) after controlling for prosecution demand: Cohen's d=0.50 (bootstrap CI [0.22, 0.79]), Mann-Whitney p<0.001. Pasal 2 cases receive on average +0.50 years more than the tuntutan model predicts, while Pasal 3 cases receive -0.55 years less.

**Text-derived vs structured metadata.** When Pasal 2 is extracted from the structured case metadata (listing all charged articles) rather than from the judicial reasoning text, the effect disappears entirely (OLS p=0.842 in cross-validation). This is because the metadata captures *all* charges including alternatives, while the pertimbangan text reveals the *operative* charge — the article the judge actually applied.

### 4.2 The Sentencing Discount is Unpredictable (RQ3)

The sentencing discount (vonis/tuntutan, mean=0.78, median=0.71, SD=0.48) represents judicial discretion. Ridge regression using all available text and structured features yields **cross-validated R2=-0.10** — worse than predicting the mean. No individual feature significantly correlates with the discount after Bonferroni correction. The closest associations are Pasal 2 (r=+0.10, uncorrected p=0.058) and Pasal 3 (r=-0.11, p=0.048), but neither survives correction for multiple testing.

This "genuine opacity" finding means that approximately 40% of sentencing variance reflects case-specific judicial judgment — including factors such as defendant cooperation, evidence quality, and contextual circumstances — that leave no trace in published verdict documents.

### 4.3 Text Features Do Not Reliably Improve Prediction (RQ2)

We systematically tested three text representation approaches:

| Approach | k features | CV R2 delta vs baseline | p |
|----------|----------|----------------------|---|
| TF-IDF (100 features, a=10) | 101 | -0.158 | <0.001 |
| Domain keywords (3 binary, a=20) | 4 | +0.012 | 0.067 |

TF-IDF features **significantly hurt** prediction (p<0.001), a consequence of the curse of dimensionality at n~300. Transformer sentence embeddings (384-dim, PCA 5-50) performed similarly poorly. Domain-specific binary keywords (Pasal 2, gratifikasi, pencucian uang) show a **consistently positive but unstable** improvement: across 10 random train/test splits, the improvement is positive in all 10 (mean +0.019, SD 0.005) but statistically significant at p<0.05 in only 4 of 10.

We conclude that text features provide a marginal, directionally positive but not reliably significant improvement over prosecution demand alone. The improvement from text features (+0.02 R2) is an order of magnitude smaller than the explanatory power of prosecution demand itself (R2=0.60), and is insufficient for practical use.

### 4.4 Geographic Variation is a Composition Effect

Raw Kruskal-Wallis on sentence severity by court region is highly significant (H=60.7, p<0.001), suggesting geographic disparity. However, after controlling for prosecution demand (testing residuals), the effect disappears (H=28.3, p=0.16). Different courts handle different magnitude cases — Jakarta Pusat handles national mega-corruption cases with higher sentences — but judges in all regions sentence similarly after accounting for case magnitude.

### 4.5 Judge Effects: Significant but Not Predictive

One-way ANOVA on residuals by presiding judge (16 judges with 3+ cases): F=1.94, p=0.020. The most lenient judge averages 2.27 years below model predictions; the harshest averages 0.90 years above — a range of approximately 3 years. However, adding judge dummy variables to the prediction model *hurts* performance in cross-validation due to overfitting at n~300. Judge effects are statistically real but cannot be exploited for prediction at current corpus sizes.

## 5. Discussion

### 5.1 Why Charge Type Matters Beyond Prosecution Demand

Our primary finding — that Pasal 2 cases receive 0.72 years more after controlling for tuntutan — suggests that judges make an independent severity assessment based on the nature of corruption. The prosecution already partially accounts for charge type in its demand (Pasal 2 tuntutan averages 8.25yr vs 5.33yr for Pasal 3), but judges add an additional premium for enrichment charges.

This aligns with the statutory distinction: Pasal 2 requires proof of *memperkaya diri sendiri* (enriching oneself), which implies greater culpability than Pasal 3's *menyalahgunakan kewenangan* (abusing authority). The independent judicial premium suggests that charge selection is not merely a technicality but has substantive sentencing consequences — a finding relevant to both prosecution strategy and defense planning.

The fact that text-derived charge type outperforms structured metadata is methodologically significant: it demonstrates that judicial reasoning text captures information (the operative charge) that formal case classification misses.

### 5.2 The Policy Implications of Judicial Opacity

The complete unpredictability of the sentencing discount (R2=-0.10) has important policy implications. If the goal of publishing court verdicts is transparency and sentencing consistency monitoring, our finding suggests that the published *pertimbangan* does not contain sufficient information to predict or evaluate judicial discretion in the sentencing discount. The factors driving the discount — likely including defendant demeanor, cooperation with authorities, specific evidence characteristics, and case-specific contextual factors — are not reflected in the published text.

This does not imply that judicial discretion is arbitrary. Judges may have legitimate, case-specific reasons for their sentencing decisions. But these reasons are not recoverable from the public record, meaning that external monitoring of sentencing consistency — a goal of both KPK and judicial reform advocates — cannot be accomplished computationally from published verdicts alone.

### 5.3 Why Text Features Fail at Small N

The systematic failure of TF-IDF and transformer embeddings, and the marginal performance of domain keywords, reflects a fundamental tension: at n~300, there are too few observations to estimate the effect of high-dimensional text features reliably. TF-IDF with 100 features yields a feature-to-sample ratio of 0.5 — precisely where overfitting becomes severe. Aggressive regularization (Ridge alpha=10-50) mitigates but does not solve the problem.

Domain keywords partially succeed because they encode expert knowledge about which specific legal concepts matter (charge type, crime category), reducing the feature space to 3-4 binary indicators. However, even this minimal representation provides only a marginal improvement, confirming that the unexplained variance is genuinely opaque rather than merely a representation problem.

### 5.4 Limitations

**Selection bias.** Our corpus consists of MA cassation decisions — cases that were appealed. Sentencing patterns may differ at the trial court level, and cases that are appealed may systematically differ from those that are not (e.g., more controversial or extreme sentences may be more likely to be appealed).

**Corpus size.** While 371 analysis-ready verdicts represents substantial extraction effort, it is small by NLP standards. Power analysis suggests n~1,000 is needed for the keyword improvement to reach reliable significance.

**Solo author.** The author is a computer science researcher, not a legal scholar. Legal interpretations of Pasal 2 vs Pasal 3 distinctions should be verified by qualified legal experts.

**Temporal skew.** 58% of verdicts are from 2024-2026, reflecting recent publication patterns on the MA website. Historical sentencing patterns may differ.

**Unmeasured confounders.** Case characteristics not captured in our extraction (defendant's position, specific modus operandi, plea and cooperation status) may explain some of the "opaque" variance.

## 6. Conclusion

We computationally analyzed 648 Indonesian Supreme Court corruption verdicts and found that sentencing is partially predictable and partially opaque. Prosecution demand explains 60% of sentence variance; charge type (Pasal 2 enrichment vs Pasal 3 authority abuse) adds a significant independent effect of 0.72 years (p=0.002). But the sentencing discount — the gap between prosecution demand and judicial decision — is entirely unpredictable from any available text or structured feature (R2=-0.10).

Geographic sentencing variation is a composition effect, not judicial bias. Judge-level effects are statistically significant but not predictively useful. Text mining approaches including TF-IDF, transformer embeddings, and domain-specific keywords fail to reliably improve sentencing predictions at this corpus size, providing a documented negative result for the legal NLP community.

Our findings have implications for anti-corruption policy: charge selection (Pasal 2 vs 3) independently affects sentencing outcomes, sentencing consistency cannot be monitored computationally from published verdicts, and apparent geographic disparity in corruption sentencing reflects case composition rather than judicial bias.

The CorpusKorupsi dataset and analysis code are publicly available to support replication and extension of this research.

## References

Aletras, N., Tsarapatsanis, D., Preoiuc-Pietro, D., & Lampos, V. (2016). Predicting judicial decisions of the European Court of Human Rights: A Natural Language Processing perspective. *PeerJ Computer Science*, 2, e93.

Anderson, J. M., Kling, J. R., & Stith, K. (1999). Measuring interjudge sentencing disparity: Before and after the federal sentencing guidelines. *Journal of Law and Economics*, 42(S1), 271-307.

Author (2026). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns. [Companion paper]

Butt, S. (2011). Anti-corruption reform in Indonesia: An obituary? *Bulletin of Indonesian Economic Studies*, 47(3), 381-394.

Chen, H., Cai, D., Dai, W., Dai, Z., & Ding, Y. (2019). Charge-based prison term prediction with deep gating network. *Proceedings of EMNLP-IJCNLP*, 6362-6367.

Dressel, J., & Farid, H. (2018). The accuracy, fairness, and limits of predicting recidivism. *Science Advances*, 4(1), eaao5580.

Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. *Personality and Social Psychology Bulletin*, 32(2), 188-200.

Hasanah, U., et al. (2023). Classification of Indonesian tax court verdicts using IndoBERT. *Proceedings of ICITDA*.

Lage-Freitas, A., Allain-Oldoni, H., Chasin, O., & de Cerqueira, L. (2022). Predicting Brazilian court decisions. *PeerJ Computer Science*, 8, e904.

Medvedeva, M., Vols, M., & Wieling, M. (2020). Using machine learning to predict decisions of the European Court of Human Rights. *Artificial Intelligence and Law*, 28(2), 237-266.

Nuranti, E. Q., & Yulianti, E. (2020). Named entity recognition for Indonesian legal documents. *Proceedings of CIKM Workshop*.

Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence*, 1(5), 206-215.

Schutte, S. A. (2012). Against the odds: Anti-corruption reform in Indonesia. *Public Administration and Development*, 32(1), 38-48.

Strickson, B., & De La Iglesia, B. (2020). Legal judgement prediction for UK Crown Court criminal cases. *Proceedings of ICAART*, 458-465.

Ulmer, J. T. (2012). Recent developments and new directions in sentencing research. *Justice Quarterly*, 29(1), 1-40.

Wilie, B., et al. (2020). IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding. *Proceedings of AACL-IJCNLP*, 843-857.

Yulianti, E., et al. (2024). IndoLER: A comprehensive Indonesian legal entity recognition dataset. *Proceedings of LREC-COLING*, 10234-10243.
