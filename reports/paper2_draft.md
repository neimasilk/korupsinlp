# Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences

## Abstract

We computationally analyze 693 Indonesian Supreme Court corruption verdicts to examine what determines sentence severity beyond prosecution demand. Using OLS regression, we find that **charge type is independently associated with sentencing severity**: Pasal 2 (enrichment) cases receive 0.82 years longer sentences than equivalent cases after controlling for prosecution demand and Pasal 3 (b=0.818, 95% CI [0.459, 1.193], p<0.001, Cohen's d=0.74). Text-derived charge type outperforms structured metadata because judicial reasoning reveals the *operative* charge rather than all listed charges. We further find that the **sentencing discount** (sentence/demand ratio, mean 0.80) is **entirely unpredictable** from any extracted feature (R2=-0.03), indicating judicial opacity: approximately 40% of sentencing variance is not captured by available structured features at current corpus size. Systematic experiments confirm that text mining (TF-IDF, transformer embeddings, domain keywords) cannot reliably improve prediction at this corpus size. Geographic variation is a composition effect (controlled p=0.40), while judge effects are significant (F=2.58, p<0.001) but not predictively useful. Indonesian corruption sentencing is partially predictable from prosecution demand and charge type, but judicial discretion remains opaque from public documents.

## 1. Introduction

Corruption remains Indonesia's most persistent governance challenge. Transparency International's 2024 Corruption Perceptions Index ranks Indonesia 109th of 182 countries (score 34/100), and the country has seen thousands of corruption prosecutions since the establishment of the Corruption Eradication Commission (KPK) in 2003. Yet despite the availability of public court verdicts through the Supreme Court's online directory, no large-scale computational analysis of corruption sentencing patterns has been undertaken.

The availability of public court verdicts creates an opportunity for systematic analysis. The Supreme Court (Mahkamah Agung) publishes cassation decisions at putusan3.mahkamahagung.go.id, including full judicial reasoning text. Yet this data has never been analyzed computationally at scale. Manual reviews by advocacy organizations like Indonesia Corruption Watch (ICW) cover dozens of cases annually; computational methods can analyze hundreds, revealing patterns invisible to case-by-case examination.

In a companion study (Author, 2026), we constructed CorpusKorupsi, a structured dataset of Indonesian Supreme Court corruption verdicts, and established that prosecution demand (tuntutan) explains approximately 60% of sentencing variance (R2=0.60, n=370). This leaves a fundamental question: **what explains the other 40%?**

We address this question through three research questions:

- **RQ1: Is charge type independently associated with sentence severity?** Indonesian anti-corruption law distinguishes between Pasal 2 (enrichment; *memperkaya diri sendiri*) and Pasal 3 (authority abuse; *menyalahgunakan kewenangan*). Do judges treat these differently after accounting for prosecution demand?

- **RQ2: Can computational text analysis improve sentencing predictions?** The judicial reasoning section (*pertimbangan hakim*) of each verdict contains the judge's stated rationale. Can text features from this section explain sentencing variance beyond prosecution demand?

- **RQ3: Is the sentencing discount predictable?** The gap between prosecution demand and actual sentence (mean 80% of demand) represents judicial discretion. Is this gap systematic or opaque?

Our findings reveal a partially predictable, partially opaque sentencing system. Charge type shows a meaningful independent association (Pasal 2 cases receive ~0.82 years more), but the sentencing discount is entirely unpredictable from available data. Text mining approaches — from bag-of-words to transformer embeddings — fail to improve predictions, a negative result with implications for computational legal analysis of small corpora.

### Contributions

1. **Empirical**: First large-scale computational evidence that Pasal 2 (enrichment) carries an independent sentencing association of 0.82 years over equivalent Pasal 3 (authority abuse) cases in Indonesian corruption sentencing (b=0.818, p<0.001)
2. **Policy-relevant**: Demonstration that the sentencing discount is opaque from public court documents (R2=-0.03), with implications for sentencing consistency monitoring
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

Quantitative analysis of Indonesian corruption sentencing has been limited to grey literature. Indonesia Corruption Watch (ICW) publishes annual sentencing reports based on manual case review, noting trends in average sentences and acquittal rates. Butt (2011) and Schutte (2012) provide qualitative assessments of Indonesia's anti-corruption institutional framework but do not conduct quantitative sentencing analysis.

In the broader sentencing literature, Ulmer (2012) reviews the state of sentencing research, noting that unexplained variance remains a persistent challenge across jurisdictions. Anderson et al. (1999) measured interjudge sentencing disparity in US federal courts, finding significant judge effects even after the introduction of sentencing guidelines. Englich et al. (2006) demonstrated anchoring effects in sentencing, showing that prosecution demands serve as reference points for judicial decision-making. Our finding that prosecution demand explains 60% of variance is consistent with this anchoring framework.

In computational legal analysis, sentencing prediction has been studied across multiple jurisdictions. Aletras et al. (2016) pioneered NLP-based prediction of European Court of Human Rights decisions, while Medvedeva et al. (2020) found that simple models performed comparably to BERT on the same task. Strickson and De La Iglesia (2020) predicted UK Crown Court sentences using structured features with random forests. Lage-Freitas et al. (2022) applied BERT to Brazilian court decisions. Chen et al. (2019) used deep learning for charge prediction on 2.6 million Chinese court documents. These studies typically rely on large corpora; our contribution is to examine what happens when the corpus is necessarily small.

Emerging computational work on Indonesian legal text includes named entity recognition (Nuranti & Yulianti, 2020; Yulianti et al., 2024), verdict classification using IndoBERT (Hasanah et al., 2023), and NER for legal entities in corruption verdicts using IndoBERT-CRF (Subowo et al., 2025). Most recently, Ibrahim et al. (2024) applied a hybrid CNN-BiLSTM deep learning model to predict punishment durations in Indonesian court rulings, achieving R2=0.589 — notably lower than the R2=0.647 achieved by our simple linear model using prosecution demand alone. This comparison underscores that at current corpus sizes, interpretable features outperform complex architectures. On the theoretical side, Alimardani and Istiqomah (2025) use Indonesian corruption sentencing guidelines (PERMA 1/2020) as a case study for proposing modular AI sentencing frameworks, arguing the domain needs computational analysis but providing no empirical implementation.

Indonesia Corruption Watch (ICW) publishes annual sentencing trend reports based on manual case review, most recently documenting an average corruption sentence of 3 years and 3 months across 1,871 defendants in 2024, classified as "light" under Supreme Court Regulation No. 1/2020 (ICW, 2025). However, no peer-reviewed study has applied computational methods to analyze sentencing *determinants* — as opposed to prediction or description — across hundreds of Indonesian corruption verdicts. Our work fills this gap.

## 3. Data and Methods

### 3.1 Corpus

We use CorpusKorupsi (Author, 2026), comprising 693 Supreme Court corruption verdicts scraped from putusan3.mahkamahagung.go.id. After filtering for valid sentences (vonis > 0) and prosecution demand (tuntutan > 0), 374 verdicts are analysis-ready. Judicial reasoning text (pertimbangan hakim) is extracted from verdict PDFs for all 374 cases (minimum 1,033 characters, median 10,877). Verdicts span 2011-2026, with heavier representation of 2024-2026 (62%).

### 3.2 Variables

| Variable | Description | n | Coverage |
|----------|-------------|---|----------|
| vonis_years | Prison sentence (years) | 374 | 100% |
| tuntutan_years | Prosecution demand (years) | 374 | 100% |
| has_pasal_2 | Pasal 2 mentioned in pertimbangan | 374 | 100% |
| has_pasal_3 | Pasal 3 mentioned in pertimbangan | 374 | 100% |
| kerugian_negara | State financial loss (IDR) | 271 | 74% |
| daerah | Court region of origin | 352 | 96% |
| discount | vonis / tuntutan ratio | 374 | 100% |

### 3.3 Extraction Quality

Field extraction uses regex-based parsers validated against a 20-case golden set (see Author, 2026 for details). Vonis extraction achieves 100% accuracy on the golden set across diverse case types including acquittals, modified sentences (*memperbaiki*), and rejected appeals (*kasasi ditolak*). The text-derived Pasal 2 indicator is a simple regex pattern match ("pasal 2" appearing in the pertimbangan text) and does not require sophisticated NLP parsing.

### 3.4 Descriptive Statistics

Sentences range from 0.2 to 18.0 years (mean 4.75, median 4.00, SD 3.21). Prosecution demands range from 0.2 to 20.0 years (mean 6.67, median 6.00, SD 4.04). The sentencing discount (vonis/tuntutan) averages 0.80 (SD 0.40, median 0.75), indicating that judges on average give sentences approximately 20% below prosecution demands. In 13.6% of cases, judges gave *more* than prosecution demanded, while in 20.7%, judges gave less than half.

The corpus draws from 28 court regions, with Jakarta Pusat (53 cases), Surabaya (30), and Bandung (26) most represented. Temporal coverage spans 2011-2026, with 2025 (147 cases, 40%) most represented due to MA publication recency. Pertimbangan text is extracted from verdict PDFs and ranges from 1,033 to 476,164 characters (median 10,877), reflecting the substantial variation in how much detail judges provide in their reasoning.

**Text-derived vs structured charge type.** The database includes a `pasal` metadata column listing all charged articles. We extract `has_pasal_2` from the judicial reasoning text (*pertimbangan*) rather than from this structured column because the pertimbangan reveals the **operative** charge — the article the judge actually applies — while the metadata lists all charges including alternatives that were not proven.

### 3.5 Statistical Methods

**Primary analysis (RQ1).** We estimate the independent effect of charge type using OLS regression. Because judges discuss both alternative charges in their reasoning, we control for both Pasal 2 and Pasal 3 mentions:

*vonis_years = b0 + b1 * tuntutan_years + b2 * has_pasal_2 + b3 * has_pasal_3 + e*

We report the coefficient b2 with standard errors, 95% parametric confidence intervals, and 95% bootstrap confidence intervals (2,000 iterations with resampling). Model comparison uses an F-test (Model 2 with Pasal 2 vs Model 1 without). Effect size is reported as Cohen's d on residuals from Model 1, comparing Pasal 2-only cases (n=59) against Pasal 3-only cases (n=64), with bootstrap CI.

To assess robustness, we re-estimate Model 2 on progressive subsamples (50% to 100% of the corpus, each with a fixed random seed) and verify that the Pasal 2 coefficient remains significant at every subsample size.

**Text feature experiments (RQ2).** We test three text representation approaches using 5x10-fold repeated cross-validation with paired t-tests: (a) TF-IDF bag-of-words (100 features, Ridge regression), (b) transformer sentence embeddings (paraphrase-multilingual-MiniLM-L12-v2, 384 dimensions with PCA reduction), and (c) domain-specific binary keyword features. Multi-seed robustness is assessed by repeating the analysis across 10 random train/test splits.

**Discount analysis (RQ3).** We regress the discount ratio (vonis/tuntutan) on all available features using Ridge regression with 10-fold cross-validation. Individual feature correlations are reported with Bonferroni correction.

**Diagnostics.** OLS residuals show mild non-normality (Shapiro-Wilk p<0.001, skewness=0.26, kurtosis=1.05) and heteroskedasticity (Breusch-Pagan p<0.001). We report heteroskedasticity-consistent standard errors (HC3); results are substantively unchanged and strengthened (P2 HC3 p<0.001 vs OLS p<0.001). Variance inflation factors are low (all VIF<1.2), confirming no multicollinearity. The bootstrap confidence intervals provide additional robustness to distributional assumptions.

**Temporal robustness.** We test whether the charge type association is stable over time by estimating the model separately for pre-2024 (n=147) and 2024-2026 (n=227) subsets, and by including a year-period interaction term.

**Geographic and judge effects.** We compare Kruskal-Wallis tests on raw sentence vs residuals after controlling for prosecution demand to distinguish genuine disparity from composition effects. Judge effects are assessed via one-way ANOVA on residuals by presiding judge (hakim ketua, judges with 3+ cases).

## 4. Results

### 4.1 Charge Type Is Independently Associated with Sentencing (RQ1)

Adding text-derived Pasal 2 to the tuntutan-only regression significantly improves model fit (F=15.04, p<0.001):

| Model | R2 | Adj R2 | Pasal 2 coef | 95% CI | p |
|-------|-----|--------|-------------|--------|---|
| vonis ~ tuntutan | 0.647 | 0.646 | — | — | — |
| vonis ~ tuntutan + pasal_2 | 0.661 | 0.659 | +0.818 | [0.403, 1.232] | <0.001 |
| vonis ~ tuntutan + pasal_2 + pasal_3 | 0.663 | 0.660 | +0.905 | [0.473, 1.336] | <0.001 |

Because the full judicial reasoning text discusses both alternative charges before identifying the operative one, 47% of cases mention both Pasal 2 and Pasal 3. Controlling for both (Model 3) gives a clearer estimate of the independent Pasal 2 effect. Bootstrap confirmation (2,000 iterations): Model 3 Pasal 2 coefficient 95% CI = [0.459, 1.193], excluding zero.

Comparing Pasal 2-only cases (n=58, mean 6.10yr) with Pasal 3-only cases (n=67, mean 3.20yr) after controlling for prosecution demand: Cohen's d=0.742 (bootstrap CI [0.373, 1.150]), Mann-Whitney p<0.001. Pasal 2 cases receive on average +0.32 years more than the tuntutan model predicts, while Pasal 3 cases receive -0.80 years less.

**Text-derived vs structured metadata.** When Pasal 2 is extracted from the structured case metadata (listing all charged articles) rather than from the judicial reasoning text, the effect disappears entirely (cross-validation p=0.842). This result is methodologically instructive: the metadata captures *all* charged articles (e.g., "2 Ayat (1) juncto Pasal 18; 55 Ayat (1); 3 juncto Pasal 18..."), including alternative charges that the judge did not ultimately apply. The pertimbangan text, by contrast, mentions Pasal 2 specifically when the judge reasons about the enrichment element — revealing the *operative* charge.

This finding has implications beyond our study: in legal NLP, unstructured judicial reasoning text may carry information that structured case metadata misses, precisely because the reasoning reflects the judge's actual decision-making process rather than the initial charge sheet.

**Temporal stability.** The Pasal 2 association is present in both pre-2024 verdicts (n=147, b=+0.926, p=0.006) and 2024-2026 verdicts (n=227, b=+0.890, p=0.003). A year-period interaction test confirms no temporal moderation (interaction p=0.88). The finding is not driven by the temporal composition of the corpus.

**Stability across corpus sizes.** We re-estimated Model 3 on progressive subsamples (50% to 100% of the corpus). The Pasal 2 coefficient is significant at *every* subsample size, from 50% (n=187, b=+0.831, p=0.006) through 100% (n=374, b=+0.905, p<0.001), and does not systematically strengthen or weaken with corpus size.

**Influential observation analysis.** No case has a Cook's distance exceeding 0.5 (maximum 0.081, well below conventional concern thresholds). After removing all 22 cases exceeding the 4/n threshold, the Pasal 2 coefficient *increases* to b=1.030 (p<0.001), demonstrating that the finding is not driven by influential outliers. Leave-one-out analysis confirms that all 374 individual coefficient estimates are positive (range [0.867, 0.959]). A placebo test with 1,000 random binary variables of matching prevalence produces comparable coefficients in only 0.1% of cases (permutation p=0.001). The association is robust across alternative specifications: quantile regression (b=0.870, p<0.001), weighted least squares (b=1.082, p<0.001), and log-transformed outcome (b=0.225, p<0.001).

### 4.2 The Sentencing Discount is Unpredictable (RQ3)

The sentencing discount (vonis/tuntutan) has a mean of 0.80 and median of 0.75, indicating that judges on average give sentences approximately 20% below prosecution demands. However, the distribution is wide (SD=0.40): 13.6% of cases receive sentences *exceeding* the prosecution demand, while 20.7% receive less than half.

Can any available feature predict this discount? Ridge regression using structured features (charge type, crime category, state loss magnitude, aggravating/mitigating factor presence) yields **cross-validated R2=-0.031** — no better than predicting the mean. The strongest individual correlate is charge type: Pasal 2 cases receive a *relatively* more severe sentence (Spearman r=+0.215, p<0.001) — consistent with the Section 4.1 finding — while Pasal 3 (r=-0.021, p=0.68), gratifikasi (r=+0.015, p=0.78), and pencucian uang (r=+0.096, p=0.063) show no significant association. Despite the single significant Pasal 2 correlate, the composite prediction of the discount remains indistinguishable from the mean.

We tested structured features against the discount: charge type (Pasal 2, Pasal 3), crime category (gratifikasi), factor lists (memberatkan, meringankan presence), and case magnitude (log kerugian). None achieved positive predictive R2.

This opacity finding means that approximately 40% of sentencing variance is not captured by available structured features (prosecution demand, charge type, crime category, state loss magnitude) at current corpus size — potentially reflecting defendant cooperation, remorse, evidence quality, political context, and case-specific circumstances. We cannot definitively distinguish between genuine opacity (information not present in any public document) and extraction limitations (information present in the text but not captured by our methods at n=374). The failure of TF-IDF and transformer approaches is consistent with both interpretations, as these methods are known to underperform at small corpus sizes. Resolving this question would require either expert-coded features from legal researchers reading each verdict, or a substantially larger corpus enabling more sophisticated text mining. Nevertheless, the finding highlights a practical limitation: at current data availability, computational sentencing monitoring from public court documents faces significant barriers.

### 4.3 Text Features Do Not Reliably Improve Prediction (RQ2)

We systematically tested three text representation approaches:

| Approach | k features | CV R2 delta vs baseline | p |
|----------|----------|----------------------|---|
| TF-IDF (100 features, a=10) | 101 | -0.105 | <0.001 |
| Domain keywords (3 binary, a=20) | 4 | +0.035 | <0.001 |

TF-IDF features **significantly hurt** prediction (p<0.001), a consequence of the curse of dimensionality at n~300. Transformer sentence embeddings (384-dim, PCA 5-50) performed similarly poorly. Domain-specific binary keywords (Pasal 2, gratifikasi, pencucian uang) show a **directionally positive but unstable** improvement: across 10 random train/test splits, the improvement is positive in 10 of 10 (mean +0.019, SD 0.007) but statistically significant at p<0.05 in only 4 of 10.

We conclude that text features provide no reliable improvement over prosecution demand alone. The improvement from text features is an order of magnitude smaller than the explanatory power of prosecution demand itself (R2=0.647), and is not statistically distinguishable from zero.

It is important to distinguish between *explanatory* and *predictive* significance. The Pasal 2 charge type has a clear explanatory effect (OLS b=+0.818yr, p<0.001, Section 4.1). But this explanatory effect does not translate to a predictive improvement in cross-validation because prosecution demand already partially captures charge severity. The distinction matters: researchers seeking to understand sentencing determinants should use regression analysis, while those seeking to build prediction tools should recognize that prosecution demand alone is sufficient.

### 4.4 Geographic Variation is a Composition Effect

Raw Kruskal-Wallis on sentence severity by court region is highly significant (H=60.9, p<0.001), suggesting geographic disparity. However, after controlling for prosecution demand (testing residuals), the effect disappears (H=22.0, p=0.40). Different courts handle different magnitude cases — Jakarta Pusat handles national mega-corruption cases with higher sentences — but judges in all regions sentence similarly after accounting for case magnitude.

### 4.5 Judge Effects: Significant but Not Predictive

One-way ANOVA on residuals by presiding judge (17 judges with 3+ cases): F=2.58, p<0.001. The range between the most lenient and harshest judges is approximately 4.34 years. This finding is consistent with Anderson et al.'s (1999) observation of significant interjudge disparity in US federal sentencing. In our data, the judge effect range (4.34 years) exceeds the charge type effect (0.82 years), suggesting that *who* decides the case may matter more than legal classification — though both are dwarfed by prosecution demand (R2=0.647).

However, adding judge dummy variables to the prediction model *hurts* performance in cross-validation (delta=-0.012 to -0.029), because 17 parameters on ~280 observations causes overfitting. This creates a paradox: judge identity has a statistically detectable effect, but cannot be exploited for prediction at current corpus sizes.

## 5. Discussion

### 5.1 Why Charge Type Is Associated with Longer Sentences

Our primary finding — that Pasal 2 cases receive 0.82 years more after controlling for tuntutan — suggests that judges make an independent severity assessment associated with the nature of corruption. The prosecution already partially accounts for charge type in its demand (Pasal 2 tuntutan averages 8.09yr vs 5.03yr for Pasal 3), but judges add an additional premium for enrichment charges.

This aligns with the statutory distinction: Pasal 2 requires proof of *memperkaya diri sendiri* (enriching oneself), which implies greater culpability than Pasal 3's *menyalahgunakan kewenangan* (abusing authority). The independent judicial premium suggests that charge selection is not merely a technicality but has substantive sentencing consequences — a finding relevant to both prosecution strategy and defense planning.

The fact that text-derived charge type outperforms structured metadata is methodologically significant: it demonstrates that judicial reasoning text captures information (the operative charge) that formal case classification misses.

### 5.2 The Policy Implications of Judicial Opacity

The complete unpredictability of the sentencing discount (R2=-0.03) has important policy implications for anti-corruption reform in Indonesia.

**First, sentencing consistency monitoring faces significant barriers from public documents alone.** If the goal of publishing court verdicts is to enable transparency and monitoring of sentencing consistency — as advocated by organizations such as ICW and LeIP (Lembaga Kajian dan Advokasi untuk Independensi Peradilan) — our finding suggests that the structured features extractable from published *pertimbangan* at current scale do not capture the factors driving the sentencing discount. Whether more sophisticated extraction methods or larger corpora could reduce this gap remains an open question, but the current evidence indicates that simple computational monitoring tools will face substantial limitations.

**Second, charge type is associated with sentencing outcomes.** The independent Pasal 2 association of 0.82 years means that cases classified under enrichment charges receive longer sentences beyond what prosecution demand alone predicts. Whether this reflects a causal effect of charge selection or correlated case characteristics (e.g., cases involving personal enrichment may involve greater culpability) cannot be determined from observational data alone. However, the association is robust across temporal subsets (pre-2024 and post-2024, interaction p=0.88).

**Third, geographic disparity is less concerning than commonly assumed.** Media reports frequently highlight sentencing variation across regions as evidence of inconsistent or corrupt judicial behavior. Our finding that this variation is a composition effect — driven by differences in what *types* of cases each court handles, not by how judges decide them — suggests that the problem may be overstated. Policy interventions focused on judicial "leniency" in specific regions may be targeting the wrong problem.

This does not imply that judicial discretion is arbitrary. Judges may have legitimate, case-specific reasons for their sentencing decisions. But these reasons are not recoverable from the public record, which creates an accountability gap: the public can see *what* judges decide but cannot evaluate *why* from the available documents.

### 5.3 Why Text Features Fail

The failure of text mining approaches — TF-IDF (30 experiments), transformer embeddings, and domain keywords — reflects a substantive finding rather than merely a methodological limitation. With complete judicial reasoning text (median 10,877 characters per verdict), the text features have ample signal to work with. Yet even domain-specific binary keywords (Pasal 2, gratifikasi, pencucian uang) — an approach consistent with Rudin's (2019) argument for interpretable models — provide no statistically reliable improvement in any of 10 random splits.

This suggests that the factors driving the 40% unexplained sentencing variance may be absent from published verdicts or may require extraction methods beyond what current corpus sizes support. The written *pertimbangan* records the judge's stated reasoning but not the full range of considerations (defendant demeanor, cooperation, political context, case-specific circumstances) that may influence the sentence. This aligns with Dressel and Farid's (2018) finding that simple expert-defined features can match complex ML approaches in criminal justice prediction — and extends it to show that at small corpus sizes (n<500), even domain-expert features cannot surpass prosecution demand as the dominant predictor. Detailed experimental results (TF-IDF configurations, embedding dimensions, alpha sweeps) are reported in Supplementary Tables S1-S5.

### 5.4 The Composition Effect in Geographic Variation

Our finding that geographic sentencing variation disappears after controlling for prosecution demand (raw p<0.001, controlled p=0.40) challenges a common assumption in Indonesian anti-corruption discourse. Media reports frequently highlight that certain regions produce "lighter" corruption sentences, implying judicial leniency. Our analysis suggests instead that the variation reflects *what kinds of cases* each court handles: Jakarta Pusat, home to the KPK-associated Tipikor court, handles national mega-corruption cases with substantially higher prosecution demands and correspondingly higher sentences. Once this composition effect is accounted for, judges across regions appear to sentence comparably.

This finding is methodologically important: it demonstrates the danger of comparing raw sentencing averages across jurisdictions without controlling for case composition, a point made by Ulmer (2012) in the broader sentencing literature.

### 5.5 Practical Implications

Our findings have three actionable implications for Indonesian anti-corruption stakeholders:

For **prosecutors**, the independent Pasal 2 association means that charge classification is not merely a legal technicality — it correlates with measurable differences in sentence length. Cases classified under Pasal 2 (enrichment) rather than Pasal 3 (authority abuse) are associated with approximately 0.82 additional years of imprisonment, independent of the prosecution demand itself.

For **judicial reform advocates**, the opacity finding suggests that current transparency mechanisms — publishing full verdict texts — are necessary but insufficient for monitoring sentencing consistency. The factors driving the sentencing discount are not recoverable from published documents, meaning that effective monitoring would require additional data collection (e.g., standardized sentencing worksheets or structured judicial reasoning forms).

For **researchers**, the systematic failure of text mining at n<500 should calibrate expectations for computational legal analysis in data-scarce settings. Investing in corpus expansion (more verdicts) is likely more productive than investing in more sophisticated NLP models.

### 5.6 Future Research Directions

Our study opens several avenues for future investigation. First, the Pasal 2 premium should be tested on first-instance Tipikor court decisions, which represent the full population of corruption verdicts rather than the appealed subset. If the premium persists at the trial level, it would strengthen the case for sentencing guidelines that account for charge type.

Second, the judicial opacity finding invites qualitative research: interviewing judges about the factors they consider in the sentencing discount could reveal whether the opacity reflects legitimate case-specific reasoning or inconsistent application of sentencing principles. Mixed-methods approaches combining our computational analysis with judicial interviews could bridge this gap.

Third, the text-derived vs structured metadata finding has implications for legal information systems: if the published reasoning text contains sentencing-relevant information not captured in formal case classifications, then improving metadata extraction from full-text verdicts could enhance legal databases and research infrastructure.

Finally, the complete failure of TF-IDF and transformer embeddings suggests that future text mining efforts on small legal corpora should explore domain-adaptive pretraining (Chalkidis et al., 2020) or few-shot learning approaches, rather than applying general-purpose text representations out of the box.

### 5.7 Limitations

**Selection bias.** Our corpus consists of MA cassation decisions — cases that were appealed. Sentencing patterns may differ at the trial court level, and cases that are appealed may systematically differ from those that are not. Specifically, the appellate sample may over-represent extreme or contentious sentences, and the sentencing discount distribution may differ from first-instance courts. The direction of this bias for the Pasal 2 association is unclear: if enrichment cases are more likely to be appealed by defendants (seeking reduction) or by prosecutors (seeking increase), the coefficient may be inflated or attenuated. Future work on first-instance Tipikor court data would address this limitation.

**Endogeneity of text-derived features.** The `has_pasal_2` indicator is extracted from the *pertimbangan* (judicial reasoning) — the same text where judges explain their sentencing decision. This creates a fundamental identification challenge: we cannot establish whether charge type drives sentencing or whether judges who impose harsher sentences are more likely to invoke Pasal 2 reasoning. The association should therefore be interpreted as: *judges who invoke Pasal 2 (enrichment) in their reasoning tend to impose longer sentences*, which is consistent with — but does not prove — an independent charge type effect. Several observations support a substantive interpretation: (a) the indicator is binary (presence/absence), reducing sensitivity to elaboration length; (b) the coefficient is stable across all 374 leave-one-out iterations (range [0.867, 0.959], 100% positive) and survives removal of all influential observations (Cook's d > 4/n: b=1.030, p<0.001); (c) the effect is robust across OLS, quantile, WLS, and log specifications (all p<0.001); and (d) a placebo test with 1,000 random binary variables produces comparable coefficients in only 0.1% of cases. Nevertheless, the structured metadata version of the same indicator (from the charge sheet listing all charged articles) shows no significant effect. While we interpret this as evidence that the *pertimbangan* captures the operative charge rather than the full charge list, an alternative interpretation is that the text-derived variable captures aspects of judicial reasoning beyond charge type alone. Future work should extract charge type from prosecution documents (*tuntutan* text), which are written before the sentencing decision, to achieve cleaner identification.

**Corpus size.** While 374 analysis-ready verdicts represents substantial extraction effort, it is small by NLP standards. The Pasal 2 association is nevertheless significant at every tested corpus size, including 50% of the sample (n=187, p=0.006).

**Temporal skew.** 62% of verdicts are from 2024-2026, reflecting recent publication patterns on the MA website. However, the Pasal 2 association is present in both pre-2024 (b=+0.93, p=0.006) and 2024-2026 (b=+0.89, p=0.003) subsets, with no significant temporal interaction (p=0.88).

**Unmeasured confounders.** Case characteristics not captured in our extraction (defendant's position, specific modus operandi, plea and cooperation status, media attention) may confound the Pasal 2 association. In particular, Pasal 2 cases may systematically involve higher-status defendants or larger schemes, which could independently drive harsher sentences. The 0.82-year association should be interpreted as an upper bound of the true charge type effect.

**Solo author and language coverage.** The author is a computer science researcher, not a legal scholar. Legal interpretations of Pasal 2 vs Pasal 3 distinctions should be verified by qualified legal experts. Indonesian-language legal scholarship on sentencing (e.g., in *Jurnal Hukum dan Peradilan*, *Mimbar Hukum*) was not systematically reviewed and may contain relevant findings not captured here.

## 6. Conclusion

We computationally analyzed 693 Indonesian Supreme Court corruption verdicts and found that sentencing is partially predictable and partially opaque.

Our primary finding is that **charge type is independently associated with sentencing**: cases invoking Pasal 2 (enrichment) of the Anti-Corruption Law receive sentences 0.82 years longer than equivalent Pasal 3 (authority abuse) cases, after controlling for prosecution demand (b=0.818, 95% CI [0.459, 1.193], p<0.001, Cohen's d=0.74). This effect is robust across all corpus subsamples tested and is detected through text-derived features (from judicial reasoning) rather than structured case metadata, demonstrating that the judge's written reasoning contains sentencing-relevant information that formal case classifications miss.

Our secondary finding is that the **sentencing discount is opaque from public documents**: the ratio of sentence to prosecution demand (mean 0.80) cannot be predicted from any available feature (R2=-0.03). Approximately 40% of sentencing variance reflects case-specific judicial judgment that leaves no trace in published verdicts. This has practical implications: computational monitoring of sentencing consistency — however sophisticated — cannot succeed when the decisive factors are not recorded in the public documents it analyzes.

Two additional findings correct common assumptions. Geographic sentencing variation is a **composition effect**: different courts handle different magnitude cases, but judges sentence comparably after accounting for case composition (raw KW p<0.001, controlled p=0.40). And judge-level effects are **statistically significant but not predictive**: individual judges differ by up to 4.34 years, but this variation cannot be exploited for prediction at current corpus sizes due to overfitting.

Finally, we document the systematic failure of text mining approaches — from bag-of-words (TF-IDF, 30 experiments) to transformer embeddings (384-dim) — to improve sentencing prediction at n<500. This negative result cautions against the assumption that more text data always means better predictions in computational legal analysis.

The CorpusKorupsi dataset and analysis code are publicly available at [repository URL] to support replication and extension of this research. Future work should expand the corpus to first-instance Tipikor courts, test whether fine-tuned legal language models (e.g., legal-domain IndoBERT) can capture what general-purpose representations miss, and investigate whether the judicial opacity finding holds across different corruption offense types and time periods.

## Declarations

**Ethical Approval.** Not applicable. This study analyzes publicly available court documents published by the Indonesian Supreme Court (*Mahkamah Agung*). No human subjects were involved and no ethics approval was required.

**Informed Consent.** Not applicable.

**Statement Regarding Research Involving Human Participants and/or Animals.** Not applicable. This research does not involve human participants or animals. All data consist of publicly available legal documents.

**Funding.** This research received no external funding.

**Author's Contribution.** Sole author; responsible for all aspects of this research including conception and design, data collection and extraction, computational analysis, and manuscript preparation.

**Competing Interests.** The author declares no competing interests.

**Availability of Data and Materials.** The CorpusKorupsi structured dataset (extracted fields; raw verdict text excluded for copyright reasons), extraction pipeline source code, and analysis scripts are available at [repository URL].

**Use of AI-Assisted Tools.** The author used Claude (Anthropic, Claude Opus) as a computational research assistant during this study. The AI tool assisted with: (1) Python programming for the data extraction pipeline and statistical analysis scripts, (2) literature search and identification of related work, and (3) manuscript drafting and revision. All statistical analyses were independently verified by the author through reproducible scripts (scripts/11_paper2_analysis.py, scripts/12_robustness_tests.py). The author manually validated extraction accuracy against a 20-case golden set. All research design decisions, scientific interpretations, and conclusions are the sole responsibility of the author. The AI tool does not meet authorship criteria and is not listed as an author. This disclosure follows Springer Nature's policy on the use of large language models in scholarly publications.

## References

Aletras, N., Tsarapatsanis, D., Preoiuc-Pietro, D., & Lampos, V. (2016). Predicting judicial decisions of the European Court of Human Rights: A Natural Language Processing perspective. *PeerJ Computer Science*, 2, e93. https://doi.org/10.7717/peerj-cs.93

Alimardani, A., & Istiqomah, D. T. (2025). Beyond black boxes and biases: Advancing artificial intelligence in sentencing. *Journal of Judicial Administration*, 34(3). https://doi.org/10.1080/10345329.2025.2527994

Anderson, J. M., Kling, J. R., & Stith, K. (1999). Measuring interjudge sentencing disparity: Before and after the federal sentencing guidelines. *Journal of Law and Economics*, 42(S1), 271-307. https://doi.org/10.1086/467425

Author (2026). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns. [Companion paper]

Butt, S. (2011). Anti-corruption reform in Indonesia: An obituary? *Bulletin of Indonesian Economic Studies*, 47(3), 381-394. https://doi.org/10.1080/00074918.2011.619051

Chalkidis, I., Fergadiotis, M., Malakasiotis, P., Aletras, N., & Androutsopoulos, I. (2020). LEGAL-BERT: The muppets straight out of law school. *Findings of EMNLP*, 2898-2904. https://doi.org/10.18653/v1/2020.findings-emnlp.261

Chen, H., Cai, D., Dai, W., Dai, Z., & Ding, Y. (2019). Charge-based prison term prediction with deep gating network. *Proceedings of EMNLP-IJCNLP*, 6362-6367. https://doi.org/10.18653/v1/D19-1667

Dressel, J., & Farid, H. (2018). The accuracy, fairness, and limits of predicting recidivism. *Science Advances*, 4(1), eaao5580. https://doi.org/10.1126/sciadv.aao5580

Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. *Personality and Social Psychology Bulletin*, 32(2), 188-200. https://doi.org/10.1177/0146167205282152

Hasanah, U., et al. (2023). Classification of Indonesian tax court verdicts using IndoBERT. *Proceedings of ICITDA*.

Ibrahim, M. A., et al. (2024). Hybrid deep learning for legal text analysis: Predicting punishment durations in Indonesian court rulings. *arXiv preprint*, arXiv:2410.20104. https://doi.org/10.48550/arXiv.2410.20104

Indonesia Corruption Watch (2025). Sentencing trend monitoring report 2024. Jakarta: ICW.

Lage-Freitas, A., Allain-Oldoni, H., Chasin, O., & de Cerqueira, L. (2022). Predicting Brazilian court decisions. *PeerJ Computer Science*, 8, e904. https://doi.org/10.7717/peerj-cs.904

Medvedeva, M., Vols, M., & Wieling, M. (2020). Using machine learning to predict decisions of the European Court of Human Rights. *Artificial Intelligence and Law*, 28(2), 237-266. https://doi.org/10.1007/s10506-019-09255-y

Nuranti, E. Q., & Yulianti, E. (2020). Named entity recognition for Indonesian legal documents. *Proceedings of CIKM Workshop*.

Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead. *Nature Machine Intelligence*, 1(5), 206-215. https://doi.org/10.1038/s42256-019-0048-x

Schutte, S. A. (2012). Against the odds: Anti-corruption reform in Indonesia. *Public Administration and Development*, 32(1), 38-48. https://doi.org/10.1002/pad.1621

Strickson, B., & De La Iglesia, B. (2020). Legal judgement prediction for UK Crown Court criminal cases. *Proceedings of ICAART*, 458-465.

Subowo, E., Bukhori, S., & Warto (2025). Corpus development and NER model for identification of legal entities in corruption court decisions. *Transactions on Informatics and Data Science*, 2(1), 27-40.

Ulmer, J. T. (2012). Recent developments and new directions in sentencing research. *Justice Quarterly*, 29(1), 1-40. https://doi.org/10.1080/07418825.2011.583932

Wilie, B., et al. (2020). IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding. *Proceedings of AACL-IJCNLP*, 843-857. https://doi.org/10.18653/v1/2020.aacl-main.85

Yulianti, E., et al. (2024). IndoLER: A comprehensive Indonesian legal entity recognition dataset. *Proceedings of LREC-COLING*, 10234-10243.
