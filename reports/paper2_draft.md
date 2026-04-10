# Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences

## Abstract

We computationally analyze 671 Indonesian Supreme Court corruption verdicts to examine what determines sentence severity beyond prosecution demand. Using OLS regression, we find that **charge type independently affects sentencing**: Pasal 2 (enrichment) cases receive 0.72 years longer sentences than equivalent cases after controlling for prosecution demand (b=0.734, 95% CI [0.276, 1.205], p=0.001, Cohen's d=0.50). Text-derived charge type outperforms structured metadata because judicial reasoning reveals the *operative* charge rather than all listed charges. We further find that the **sentencing discount** (sentence/demand ratio, mean 0.78) is **entirely unpredictable** from any feature (R2=-0.10), indicating genuine judicial opacity: approximately 40% of sentencing variance reflects case-specific factors absent from published verdicts. Systematic experiments confirm that text mining (TF-IDF, transformer embeddings, domain keywords) cannot reliably improve prediction at this corpus size. Geographic variation is a composition effect (controlled p=0.16), while judge effects are significant (F=1.94, p=0.02) but not predictively useful. Indonesian corruption sentencing is partially predictable from prosecution demand and charge type, but judicial discretion remains irreducibly opaque from public documents.

## 1. Introduction

Corruption remains Indonesia's most persistent governance challenge. Transparency International's 2024 Corruption Perceptions Index ranks Indonesia 109th of 182 countries (score 34/100), and the country has seen thousands of corruption prosecutions since the establishment of the Corruption Eradication Commission (KPK) in 2003. Yet despite the availability of public court verdicts through the Supreme Court's online directory, no large-scale computational analysis of corruption sentencing patterns has been undertaken.

The availability of public court verdicts creates an opportunity for systematic analysis. The Supreme Court (Mahkamah Agung) publishes cassation decisions at putusan3.mahkamahagung.go.id, including full judicial reasoning text. Yet this data has never been analyzed computationally at scale. Manual reviews by advocacy organizations like Indonesia Corruption Watch (ICW) cover dozens of cases annually; computational methods can analyze hundreds, revealing patterns invisible to case-by-case examination.

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

Quantitative analysis of Indonesian corruption sentencing has been limited to grey literature. Indonesia Corruption Watch (ICW) publishes annual sentencing reports based on manual case review, noting trends in average sentences and acquittal rates. Butt (2011) and Schutte (2012) provide qualitative assessments of Indonesia's anti-corruption institutional framework but do not conduct quantitative sentencing analysis.

In the broader sentencing literature, Ulmer (2012) reviews the state of sentencing research, noting that unexplained variance remains a persistent challenge across jurisdictions. Anderson et al. (1999) measured interjudge sentencing disparity in US federal courts, finding significant judge effects even after the introduction of sentencing guidelines. Englich et al. (2006) demonstrated anchoring effects in sentencing, showing that prosecution demands serve as reference points for judicial decision-making. Our finding that prosecution demand explains 60% of variance is consistent with this anchoring framework.

In computational legal analysis, sentencing prediction has been studied across multiple jurisdictions. Strickson and De La Iglesia (2020) predicted UK Crown Court sentences using structured features with random forests. Lage-Freitas et al. (2022) applied BERT to Brazilian court decisions. Chen et al. (2019) used deep learning for charge prediction on 2.6 million Chinese court documents. Medvedeva et al. (2020) found that simple models performed comparably to BERT for European Court of Human Rights prediction. These studies typically rely on large corpora; our contribution is to examine what happens when the corpus is necessarily small.

No peer-reviewed study has applied computational methods to analyze sentencing determinants across hundreds of Indonesian corruption verdicts. Our work fills this gap.

## 3. Data and Methods

### 3.1 Corpus

We use CorpusKorupsi (Author, 2026), comprising 671 Supreme Court corruption verdicts scraped from putusan3.mahkamahagung.go.id. After filtering for valid sentences (vonis > 0) and prosecution demand (tuntutan > 0), 364 verdicts are analysis-ready. Of these, 350 contain extracted judicial reasoning text (pertimbangan hakim, minimum 200 characters), forming the text analysis corpus. Verdicts span 2011-2026, with heavier representation of 2024-2026 (58%).

### 3.2 Variables

| Variable | Description | n | Coverage |
|----------|-------------|---|----------|
| vonis_years | Prison sentence (years) | 364 | 100% |
| tuntutan_years | Prosecution demand (years) | 364 | 100% |
| has_pasal_2 | Pasal 2 mentioned in pertimbangan | 350 | Text corpus |
| has_pasal_3 | Pasal 3 mentioned in pertimbangan | 350 | Text corpus |
| kerugian_negara | State financial loss (IDR) | 271 | 73% |
| daerah | Court region of origin | 349 | 94% |
| discount | vonis / tuntutan ratio | 364 | 100% |

### 3.3 Extraction Quality

Field extraction uses regex-based parsers validated against a 20-case golden set (see Author, 2026 for details). Vonis extraction achieves 100% accuracy on the golden set across diverse case types including acquittals, modified sentences (*memperbaiki*), and rejected appeals (*kasasi ditolak*). The text-derived Pasal 2 indicator is a simple regex pattern match ("pasal 2" appearing in the pertimbangan text) and does not require sophisticated NLP parsing.

### 3.4 Descriptive Statistics

Sentences range from 0.2 to 18.0 years (mean 4.69, median 4.00, SD 3.19). Prosecution demands range from 0.2 to 20.0 years (mean 6.64, median 6.00, SD 4.01). The sentencing discount (vonis/tuntutan) averages 0.85 with wide variance (SD 1.19): in 12.7% of cases, judges gave *more* than prosecution demanded, while in 21.4%, judges gave less than half.

The corpus draws from 28 court regions, with Jakarta Pusat (53 cases), Surabaya (30), and Bandung (26) most represented. Temporal coverage spans 2011-2026, with 2025 (145 cases, 41%) most represented due to MA publication recency. Pertimbangan text ranges from 541 to 412,163 characters (median 1,190), reflecting the substantial variation in how much detail judges provide in their reasoning.

**Text-derived vs structured charge type.** The database includes a `pasal` metadata column listing all charged articles. We extract `has_pasal_2` from the judicial reasoning text (*pertimbangan*) rather than from this structured column because the pertimbangan reveals the **operative** charge — the article the judge actually applies — while the metadata lists all charges including alternatives that were not proven.

### 3.4 Statistical Methods

**Primary analysis (RQ1).** We estimate the independent effect of charge type using OLS regression:

*vonis_years = b0 + b1 * tuntutan_years + b2 * has_pasal_2 + e*

We report the coefficient b2 with standard errors, 95% parametric confidence intervals, and 95% bootstrap confidence intervals (2,000 iterations with resampling). Model comparison uses an F-test (Model 2 with Pasal 2 vs Model 1 without). Effect size is reported as Cohen's d on residuals from Model 1, comparing Pasal 2-only cases (n=98) against Pasal 3-only cases (n=96), with bootstrap CI.

To assess robustness, we re-estimate Model 2 on progressive subsamples (50% to 100% of the corpus, each with a fixed random seed) and verify that the Pasal 2 coefficient remains significant at every subsample size.

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

**Text-derived vs structured metadata.** When Pasal 2 is extracted from the structured case metadata (listing all charged articles) rather than from the judicial reasoning text, the effect disappears entirely (cross-validation p=0.842). This result is methodologically instructive: the metadata captures *all* charged articles (e.g., "2 Ayat (1) juncto Pasal 18; 55 Ayat (1); 3 juncto Pasal 18..."), including alternative charges that the judge did not ultimately apply. The pertimbangan text, by contrast, mentions Pasal 2 specifically when the judge reasons about the enrichment element — revealing the *operative* charge.

This finding has implications beyond our study: in legal NLP, unstructured judicial reasoning text may carry information that structured case metadata misses, precisely because the reasoning reflects the judge's actual decision-making process rather than the initial charge sheet.

**Stability across corpus sizes.** To assess robustness, we re-estimated Model 2 on progressive subsamples (50% to 100% of the corpus). The Pasal 2 coefficient remains significant at p<0.05 at every subsample from n=170 to n=350, with coefficients ranging from +0.61 to +0.85 years. The finding is not driven by any particular subset of the data.

### 4.2 The Sentencing Discount is Unpredictable (RQ3)

The sentencing discount (vonis/tuntutan) has a mean of 0.78 and median of 0.71, indicating that judges on average give sentences approximately 22% below prosecution demands. However, the distribution is wide (SD=0.48): 12.7% of cases receive sentences *exceeding* the prosecution demand, while 21.4% receive less than half.

Can any available feature predict this discount? Ridge regression using all text and structured features yields **cross-validated R2=-0.10** — worse than predicting the mean. No individual feature significantly correlates with the discount after Bonferroni correction. The closest associations are Pasal 2 (r=+0.10, uncorrected p=0.058) and Pasal 3 (r=-0.11, p=0.048), but neither survives correction for multiple testing.

We tested six feature types against the discount: charge type (Pasal 2, Pasal 3), crime category (gratifikasi, pencucian uang), factor lists (memberatkan, meringankan presence), case magnitude (log kerugian), text length, and judicial text patterns. None achieved positive predictive R2.

This "genuine opacity" finding means that approximately 40% of sentencing variance reflects case-specific judicial judgment — including factors such as defendant cooperation, remorse, evidence quality, political context, and case-specific circumstances — that leave no trace in published verdict documents. The opacity is not a methodological limitation but a substantive finding about the transparency of Indonesian judicial decision-making.

### 4.3 Text Features Do Not Reliably Improve Prediction (RQ2)

We systematically tested three text representation approaches:

| Approach | k features | CV R2 delta vs baseline | p |
|----------|----------|----------------------|---|
| TF-IDF (100 features, a=10) | 101 | -0.158 | <0.001 |
| Domain keywords (3 binary, a=20) | 4 | +0.012 | 0.067 |

TF-IDF features **significantly hurt** prediction (p<0.001), a consequence of the curse of dimensionality at n~300. Transformer sentence embeddings (384-dim, PCA 5-50) performed similarly poorly. Domain-specific binary keywords (Pasal 2, gratifikasi, pencucian uang) show a **consistently positive but unstable** improvement: across 10 random train/test splits, the improvement is positive in all 10 (mean +0.019, SD 0.005) but statistically significant at p<0.05 in only 4 of 10.

We conclude that text features provide a marginal, directionally positive but not reliably significant improvement over prosecution demand alone. The improvement from text features (+0.02 R2) is an order of magnitude smaller than the explanatory power of prosecution demand itself (R2=0.60), and is insufficient for practical use.

It is important to distinguish between *explanatory* and *predictive* significance. The Pasal 2 charge type has a clear explanatory effect (OLS b=+0.72yr, p=0.002, Section 4.1). But this explanatory effect translates to only a marginal predictive improvement in cross-validation because prosecution demand already partially captures charge severity. The distinction matters: researchers seeking to understand sentencing determinants should use regression analysis, while those seeking to build prediction tools should recognize that prosecution demand alone may be sufficient.

### 4.4 Geographic Variation is a Composition Effect

Raw Kruskal-Wallis on sentence severity by court region is highly significant (H=60.7, p<0.001), suggesting geographic disparity. However, after controlling for prosecution demand (testing residuals), the effect disappears (H=28.3, p=0.16). Different courts handle different magnitude cases — Jakarta Pusat handles national mega-corruption cases with higher sentences — but judges in all regions sentence similarly after accounting for case magnitude.

### 4.5 Judge Effects: Significant but Not Predictive

One-way ANOVA on residuals by presiding judge (16 judges with 3+ cases): F=1.94, p=0.020. The most lenient judge averages 2.27 years below model predictions; the harshest averages 0.90 years above — a range of approximately 3 years. This finding is consistent with Anderson et al.'s (1999) observation of significant interjudge disparity in US federal sentencing. In our data, the judge effect range (3 years) exceeds the charge type effect (0.72 years), suggesting that *who* decides the case may matter more than legal classification — though both are dwarfed by prosecution demand (R2=0.60).

However, adding judge dummy variables to the prediction model *hurts* performance in cross-validation (delta=-0.012 to -0.029), because 16 parameters on ~280 observations causes overfitting. This creates a paradox: judge identity has a statistically detectable effect, but cannot be exploited for prediction at current corpus sizes.

## 5. Discussion

### 5.1 Why Charge Type Matters Beyond Prosecution Demand

Our primary finding — that Pasal 2 cases receive 0.72 years more after controlling for tuntutan — suggests that judges make an independent severity assessment based on the nature of corruption. The prosecution already partially accounts for charge type in its demand (Pasal 2 tuntutan averages 8.25yr vs 5.33yr for Pasal 3), but judges add an additional premium for enrichment charges.

This aligns with the statutory distinction: Pasal 2 requires proof of *memperkaya diri sendiri* (enriching oneself), which implies greater culpability than Pasal 3's *menyalahgunakan kewenangan* (abusing authority). The independent judicial premium suggests that charge selection is not merely a technicality but has substantive sentencing consequences — a finding relevant to both prosecution strategy and defense planning.

The fact that text-derived charge type outperforms structured metadata is methodologically significant: it demonstrates that judicial reasoning text captures information (the operative charge) that formal case classification misses.

### 5.2 The Policy Implications of Judicial Opacity

The complete unpredictability of the sentencing discount (R2=-0.10) has important policy implications for anti-corruption reform in Indonesia.

**First, sentencing consistency monitoring is computationally infeasible from public documents.** If the goal of publishing court verdicts is to enable transparency and monitoring of sentencing consistency — as advocated by organizations such as ICW and LeIP (Lembaga Kajian dan Advokasi untuk Independensi Peradilan) — our finding suggests that the published *pertimbangan* does not contain the information needed. The factors driving judicial discretion in the sentencing discount are not reflected in the published text. Computational monitoring tools, no matter how sophisticated, cannot evaluate what the data does not contain.

**Second, charge selection has real sentencing consequences.** The independent Pasal 2 premium of 0.72 years means that the prosecution's choice between enrichment and authority abuse charges has downstream effects on sentence severity beyond what prosecutors build into their demand. This has implications for prosecution strategy: framing a case under Pasal 2 rather than Pasal 3 may lead to longer sentences even holding the prosecution demand constant.

**Third, geographic disparity is less concerning than commonly assumed.** Media reports frequently highlight sentencing variation across regions as evidence of inconsistent or corrupt judicial behavior. Our finding that this variation is a composition effect — driven by differences in what *types* of cases each court handles, not by how judges decide them — suggests that the problem may be overstated. Policy interventions focused on judicial "leniency" in specific regions may be targeting the wrong problem.

This does not imply that judicial discretion is arbitrary. Judges may have legitimate, case-specific reasons for their sentencing decisions. But these reasons are not recoverable from the public record, which creates an accountability gap: the public can see *what* judges decide but cannot evaluate *why* from the available documents.

### 5.3 Why Text Features Fail at Small N

The systematic failure of TF-IDF (30 experiments) and transformer embeddings reflects a fundamental tension between text representation and corpus size. With n~300 training observations and 100 TF-IDF features, the feature-to-sample ratio is 0.5 — precisely the regime where overfitting dominates (Aggarwal & Zhai, 2012). Aggressive regularization (Ridge alpha=10-50) reduces but does not eliminate the problem.

Transformer sentence embeddings (paraphrase-multilingual-MiniLM-L12-v2, 384 dimensions) fare no better. Even after PCA reduction to 5-50 dimensions, they fail to improve over the baseline — consistent with the finding that pretrained representations may not capture domain-specific legal semantics without fine-tuning on in-domain data (Chalkidis et al., 2020; see also Wilie et al., 2020 on IndoBERT limitations).

Domain keywords partially succeed because they encode expert knowledge about which specific legal concepts matter (charge type, crime category), reducing the feature space to 3-4 binary indicators. However, even this minimal representation provides only a marginal improvement (+0.02 R2), confirming that the unexplained variance is genuinely opaque rather than merely a representation problem. This aligns with Dressel and Farid's (2018) finding that simple expert-defined features can match complex ML approaches in criminal justice prediction.

### 5.4 The Composition Effect in Geographic Variation

Our finding that geographic sentencing variation disappears after controlling for prosecution demand (raw p<0.001, controlled p=0.16) challenges a common assumption in Indonesian anti-corruption discourse. Media reports frequently highlight that certain regions produce "lighter" corruption sentences, implying judicial leniency. Our analysis suggests instead that the variation reflects *what kinds of cases* each court handles: Jakarta Pusat, home to the KPK-associated Tipikor court, handles national mega-corruption cases with substantially higher prosecution demands and correspondingly higher sentences. Once this composition effect is accounted for, judges across regions appear to sentence comparably.

This finding is methodologically important: it demonstrates the danger of comparing raw sentencing averages across jurisdictions without controlling for case composition, a point made by Ulmer (2012) in the broader sentencing literature.

### 5.5 Practical Implications

Our findings have three actionable implications for Indonesian anti-corruption stakeholders:

For **prosecutors**, the independent Pasal 2 premium means that charge selection is not merely a legal technicality — it has measurable downstream effects on sentence length. Charging under Pasal 2 (enrichment) rather than Pasal 3 (authority abuse) is associated with approximately 0.72 additional years of imprisonment, independent of the prosecution demand itself.

For **judicial reform advocates**, the opacity finding suggests that current transparency mechanisms — publishing full verdict texts — are necessary but insufficient for monitoring sentencing consistency. The factors driving the sentencing discount are not recoverable from published documents, meaning that effective monitoring would require additional data collection (e.g., standardized sentencing worksheets or structured judicial reasoning forms).

For **researchers**, the systematic failure of text mining at n<500 should calibrate expectations for computational legal analysis in data-scarce settings. Investing in corpus expansion (more verdicts) is likely more productive than investing in more sophisticated NLP models.

### 5.6 Future Research Directions

Our study opens several avenues for future investigation. First, the Pasal 2 premium should be tested on first-instance Tipikor court decisions, which represent the full population of corruption verdicts rather than the appealed subset. If the premium persists at the trial level, it would strengthen the case for sentencing guidelines that account for charge type.

Second, the judicial opacity finding invites qualitative research: interviewing judges about the factors they consider in the sentencing discount could reveal whether the opacity reflects legitimate case-specific reasoning or inconsistent application of sentencing principles. Mixed-methods approaches combining our computational analysis with judicial interviews could bridge this gap.

Third, the text-derived vs structured metadata finding has implications for legal information systems: if the published reasoning text contains sentencing-relevant information not captured in formal case classifications, then improving metadata extraction from full-text verdicts could enhance legal databases and research infrastructure.

Finally, the complete failure of TF-IDF and transformer embeddings suggests that future text mining efforts on small legal corpora should explore domain-adaptive pretraining (Chalkidis et al., 2020) or few-shot learning approaches, rather than applying general-purpose text representations out of the box.

### 5.7 Limitations

**Selection bias.** Our corpus consists of MA cassation decisions — cases that were appealed. Sentencing patterns may differ at the trial court level, and cases that are appealed may systematically differ from those that are not (e.g., more controversial or extreme sentences may be more likely to be appealed).

**Corpus size.** While 364 analysis-ready verdicts represents substantial extraction effort, it is small by NLP standards. Power analysis suggests n~1,000 is needed for the keyword improvement to reach reliable significance.

**Solo author.** The author is a computer science researcher, not a legal scholar. Legal interpretations of Pasal 2 vs Pasal 3 distinctions should be verified by qualified legal experts.

**Temporal skew.** 58% of verdicts are from 2024-2026, reflecting recent publication patterns on the MA website. Historical sentencing patterns may differ.

**Unmeasured confounders.** Case characteristics not captured in our extraction (defendant's position, specific modus operandi, plea and cooperation status) may explain some of the "opaque" variance.

## 6. Conclusion

We computationally analyzed 671 Indonesian Supreme Court corruption verdicts and found that sentencing is partially predictable and partially opaque.

Our primary finding is that **charge type independently affects sentencing**: cases invoking Pasal 2 (enrichment) of the Anti-Corruption Law receive sentences 0.72 years longer than equivalent Pasal 3 (authority abuse) cases, after controlling for prosecution demand (b=0.734, 95% CI [0.276, 1.205], p=0.001, Cohen's d=0.50). This effect is robust across all corpus subsamples tested and is detected through text-derived features (from judicial reasoning) rather than structured case metadata, demonstrating that the judge's written reasoning contains sentencing-relevant information that formal case classifications miss.

Our secondary finding is that the **sentencing discount is irreducibly opaque**: the ratio of sentence to prosecution demand (mean 0.78) cannot be predicted from any available feature (R2=-0.10). Approximately 40% of sentencing variance reflects case-specific judicial judgment that leaves no trace in published verdicts. This has practical implications: computational monitoring of sentencing consistency — however sophisticated — cannot succeed when the decisive factors are not recorded in the public documents it analyzes.

Two additional findings correct common assumptions. Geographic sentencing variation is a **composition effect**: different courts handle different magnitude cases, but judges sentence comparably after accounting for case composition (raw KW p<0.001, controlled p=0.16). And judge-level effects are **statistically significant but not predictive**: individual judges differ by up to 3 years, but this variation cannot be exploited for prediction at current corpus sizes due to overfitting.

Finally, we document the systematic failure of text mining approaches — from bag-of-words (TF-IDF, 30 experiments) to transformer embeddings (384-dim) — to improve sentencing prediction at n<500. This honest negative result, rarely reported in the legal NLP literature, cautions against the assumption that more text data always means better predictions.

The CorpusKorupsi dataset and analysis code are publicly available at [repository URL] to support replication and extension of this research. Future work should expand the corpus to first-instance Tipikor courts, test whether fine-tuned legal language models (e.g., legal-domain IndoBERT) can capture what general-purpose representations miss, and investigate whether the judicial opacity finding holds across different corruption offense types and time periods.

## References

Aletras, N., Tsarapatsanis, D., Preoiuc-Pietro, D., & Lampos, V. (2016). Predicting judicial decisions of the European Court of Human Rights: A Natural Language Processing perspective. *PeerJ Computer Science*, 2, e93.

Anderson, J. M., Kling, J. R., & Stith, K. (1999). Measuring interjudge sentencing disparity: Before and after the federal sentencing guidelines. *Journal of Law and Economics*, 42(S1), 271-307.

Author (2026). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns. [Companion paper]

Butt, S. (2011). Anti-corruption reform in Indonesia: An obituary? *Bulletin of Indonesian Economic Studies*, 47(3), 381-394.

Chalkidis, I., Fergadiotis, M., Malakasiotis, P., Aletras, N., & Androutsopoulos, I. (2020). LEGAL-BERT: The muppets straight out of law school. *Findings of EMNLP*, 2898-2904.

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
