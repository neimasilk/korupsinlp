# CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns

## Abstract

We present CorpusKorupsi, the first large-scale structured corpus of Indonesian corruption court verdicts extracted from the Supreme Court (Mahkamah Agung) public repository. From 557 cassation and case-review decisions spanning 2011–2026, we extract seven structured fields — prison sentence, prosecution demand, state financial loss, region, year, defendant name, and legal articles — using a regex-based pipeline validated against a 20-case golden set (100% vonis accuracy). We document a two-level sentencing structure: **prosecution demand (tuntutan) is the strongest predictor of sentence severity** (R²=0.60 linear, n=302), while **state financial loss (kerugian negara) predicts both tuntutan and vonis** (ρ=0.56, R²=0.35). When both are included, each retains independent significance (p<0.001), suggesting judges consider raw case magnitude beyond the prosecution's framing. We find **no significant effect** of appeal filer identity (pemohon kasasi, p=0.95, d=0.01, power to detect ≥1.09yr), geographic jurisdiction (p=0.52), or year (p=0.74) after controlling for case magnitude. The sentencing discount (vonis/tuntutan ratio, mean 84%) is not predicted by any extracted variable (R²=0.01), suggesting judicial discretion operates independently of observable case characteristics. Our corpus, extraction pipeline, and golden set are released to support computational legal studies in the Indonesian context.

## 1. Introduction

Corruption remains Indonesia's most persistent governance challenge, with Transparency International ranking it 109th out of 182 countries in the 2024 Corruption Perceptions Index (score: 34/100). The Corruption Eradication Commission (KPK) and Attorney General's office have prosecuted thousands of cases, generating a large body of publicly available court verdicts. Yet no structured, machine-readable dataset exists for computational analysis of sentencing patterns.

The Indonesian Supreme Court (Mahkamah Agung, MA) publishes verdicts at putusan3.mahkamahagung.go.id, including full PDF text of cassation (kasasi) and case review (peninjauan kembali, PK) decisions. These contain rich structured information — defendant names, legal articles charged, prosecution demands, sentences imposed, state losses incurred — embedded in semi-structured Indonesian legal prose.

We address three research questions:

- **RQ1**: What are the distributional characteristics of corruption sentencing at the MA cassation level?
- **RQ2**: How do sentences vary by geography, magnitude of state financial loss, and appeal filer identity?
- **RQ3**: Is there a systematic "sentencing discount" (sentence < prosecution demand) and what predicts its magnitude?

### Contributions

1. **CorpusKorupsi**: First large-scale structured corpus of Indonesian corruption verdicts (557 MA decisions, 327 with valid sentences, spanning 2011–2026)
2. **Extraction pipeline**: Regex-based field extraction validated against a 20-case golden set with 100% vonis accuracy across diverse case types (acquittals, memperbaiki, dual-kasasi, kasasi-ditolak)
3. **Two-level sentencing model**: Tuntutan (prosecution demand) explains 60% of sentencing variance (R²=0.60, n=302) — far more than kerugian negara alone (R²=0.35, n=251). Both retain independent significance when combined (p<0.001 each, R²=0.49, n=236). This reveals a mediation structure: kerugian → tuntutan → vonis.
4. **Methodological finding**: Pemohon kasasi (appeal filer identity) does NOT predict sentence severity (p=0.95, d=0.01, MDE=1.09yr at 80% power). This must be controlled for in any MA sentencing analysis due to selection effects.
5. **Descriptive findings**: Sentencing discount (vonis/tuntutan ratio, mean 84%) is unpredictable by any extracted variable (R²=0.01), suggesting judicial discretion is independent of observable case characteristics

## 2. Related Work

### 2.1 Indonesian Legal NLP
Computational analysis of Indonesian legal documents has grown in recent years but remains focused on narrow tasks. Nuranti and Yulianti (2020) developed a BiLSTM+CRF named entity recognition system for Indonesian criminal court decisions, annotating 1,003 general criminal judgments. This was extended by Nuranti et al. (2025), who systematically extracted legal entities from 2,687 Indonesian judicial decisions across three court levels using a hierarchical BIO tagging scheme with 50+ entity types. Yulianti et al. (2024) built IndoLER, an Indonesian legal entity recognition dataset of ~1,000 decision documents with 20 fine-grained entity types, finding that IndoBERT+CRF achieved F1=0.923. In the tax law domain, Hasanah et al. (2023) classified Indonesian tax court verdicts using IndoBERT, achieving 75.8% accuracy.

Ibrahim et al. (2024) applied hybrid deep learning (CNN-BiLSTM with attention) to predict punishment durations in Indonesian court rulings, achieving R²=0.589 on a first-instance corpus. Our work differs fundamentally: we construct a *structured corpus* from Supreme Court cassation decisions rather than predicting sentences from text, and we focus on extracting interpretable fields (kerugian negara, pemohon kasasi) rather than end-to-end prediction.

Despite this growing body of work, no prior study has produced a structured, multi-field corpus from MA corruption verdicts, nor identified the pemohon kasasi confound that affects all cassation-level sentencing analyses.

### 2.2 Computational Sentencing Analysis
Predicting and analyzing judicial decisions computationally is a well-established research direction in Western legal systems. Aletras et al. (2016) achieved 79% accuracy predicting European Court of Human Rights violations using textual features, finding that factual circumstances were the strongest predictor — consistent with legal realist theory. Medvedeva et al. (2020) extended this work, achieving 75% average accuracy across 9 ECHR articles, but demonstrated that temporal prediction (training on past, predicting future) significantly degraded performance (58–68%). In the US context, machine learning has been applied to sentencing risk assessment (e.g., COMPAS), raising fairness concerns (Dressel & Farid, 2018).

For structured sentencing analysis — as opposed to text classification — Chen et al. (2019) analyzed sentencing patterns in Chinese courts, and Amaral et al. (2022) used deep learning to predict Brazilian federal court appeal outcomes, outperforming human experts. Large-scale legal corpora include the Cambridge Law Corpus (Ostling et al., 2023) with 250,000+ UK court cases, and MULTI-EURLEX with 65,000 EU laws in 23 languages.

Southeast Asian legal NLP remains notably underrepresented. Apart from the Indonesian works cited above, only a Philippine legal IR dataset has been reported. Our work contributes the first structured sentencing corpus from this region.

### 2.3 Anti-Corruption Research
Quantitative anti-corruption research in Indonesia has been primarily policy-oriented. Olken (2007) demonstrated through a field experiment across 600+ Indonesian village road projects that increasing audit probability from 4% to 100% reduced missing expenditures by 8 percentage points. Henderson and Kuncoro (2011) used firm-level data to show that corruption by local officials declined between 2001–2004, modulated by political party composition. Indonesia currently ranks 109th of 182 countries on Transparency International's Corruption Perceptions Index (CPI 2024, score: 34/100).

Closest to our work is ICW's (Indonesia Corruption Watch) annual sentencing trend monitoring. ICW's 2024 report analyzed 1,768 corruption verdicts (49% of published decisions), finding an average sentence of 3 years 3 months with total state losses of ~Rp300 trillion but only Rp16 trillion recovered. Their 2023 report similarly found average imprisonment of 2 years 8 months across 1,649 verdicts. However, ICW's analysis is descriptive and manual — they do not release structured data, do not control for confounding variables like pemohon kasasi, and do not model the kerugian-vonis relationship quantitatively.

Our work bridges computational legal NLP and anti-corruption research by providing (1) a structured, reproducible corpus, (2) validated extraction methodology, and (3) quantitative modeling of sentencing determinants — none of which exist in the current literature.

## 3. Data Source and Collection

### 3.1 Source
All data is sourced from putusan3.mahkamahagung.go.id, the official Supreme Court verdict repository (public, open access). We focus on the corruption (korupsi) category within the MA court, yielding cassation (kasasi) and case review (PK) decisions.

### 3.2 Selection Bias
**Critical caveat**: Our corpus represents only cases that reached the Supreme Court via appeal. This introduces systematic selection bias:
- Only cases where either the prosecutor (JPU) or defendant filed for cassation are included
- Cases resolved at the district court (PN) level are excluded
- More contentious cases (perceived unjust sentences) are overrepresented
- This cannot be interpreted as representative of *all* corruption sentencing

### 3.3 Collection Method
We implement a polite sequential scraper with 2-second inter-request delays:
1. **Listing pages**: Paginated index yielding ~53 verdict URLs per page
2. **Detail pages**: HTML metadata extraction (case number, judges, classification)
3. **PDF download**: Full verdict text in PDF format (87.3% availability)
4. **PDF text extraction**: pdfminer-based extraction with MA watermark stripping

### 3.4 Corpus Statistics (current)
| Metric | Value |
|--------|-------|
| Total verdicts scraped | 557 |
| With case metadata | 488 (87.6%) |
| Verdicts parsed | 518 |
| With valid sentence | 327 (63.1%) |
| Acquittals detected | 17 (3.3%) |
| Temporal range | 2011–2026 |
| Geographic coverage | 40+ court regions |
| Year-filtered pagination | Required for reliable scraping beyond page 17 |

## 4. Extraction Pipeline

### 4.1 Architecture
PDF text → MA watermark stripping → regex field extractors → normalization → SQLite storage

### 4.2 Field Extraction Strategies

**Prison sentence (vonis_bulan)**: Multi-strategy extraction with priority ordering: (1) strict "menjatuhkan pidana...penjara" in the last MENGADILI section, (2) MENGADILI SENDIRI subsection detection for cases where MA re-sentences, (3) Memperbaiki subsection for cases where MA modifies specific aspects, (4) previous MENGADILI section for kasasi-ditolak, (5) quoted lower court sentence, (6) acquittal detection ("membebaskan"/"melepaskan" → 0). The MENGADILI section is identified by spaced ("M E N G A D I L I") and unspaced patterns. This multi-strategy approach handles diverse MA decision types: mengabulkan (granted), menolak (rejected), memperbaiki (modified), and dual-kasasi (both parties appeal).

**Prosecution demand (tuntutan_bulan)**: "Tuntutan Pidana" section header with 2,500-character search window. Handles defendant name insertion between "penjara" and "selama" (up to 150 chars tolerance).

**State financial loss (kerugian_negara)**: Indonesian Rupiah parsing with dot-as-thousands, comma-as-decimal normalization. Multiple context patterns: "kerugian keuangan negara", "merugikan negara", "uang pengganti".

**Defendant name (nama_terdakwa)**: PDF header structured extraction ("Nama : X;") as primary strategy, with fallback to "VS X (Terdakwa)" MA format and "Terdakwa X" standard pattern.

**Appeal filer (pemohon_kasasi)**: "dimohonkan oleh Terdakwa/Penuntut Umum" pattern from PDF header (first 5,000 chars).

### 4.3 Design Decision: Regex vs ML
We chose regex-based extraction over machine learning because: (1) legal documents follow highly regular formatting conventions, (2) no labeled training data exists, (3) regex extractors are fully interpretable and auditable — critical for legal research, (4) extraction errors are systematic and correctable.

## 5. Quality Evaluation

### 5.1 Per-Field Extraction Rates (n=359 with case data)
| Field | Rate | Status |
|-------|------|--------|
| vonis_bulan | 82.2% (295) | P0 |
| kerugian_negara | 66.3% (238) | P0 |
| daerah | 90.3% (324) | P0 |
| tahun | 100.0% (359) | P0 |
| tuntutan_bulan | 76.9% (276) | P1 |
| pasal | 84.1% (302) | P1 |
| nama_terdakwa | 83.0% (298) | P1 |
| pemohon_kasasi | 81.9% (294) | P1 |
| nama_hakim | 100.0% (359) | P2 |
| **P0 Average** | **84.7%** | |

Note: Rates are computed over verdicts with case metadata (n=359). Verdicts without PDF text have lower extraction rates (fields require full text). Of the 295 with valid vonis, 281 have vonis>0 and 14 are acquittals (vonis=0).

### 5.2 Golden Set Validation (n=20)
We validate against 20 human-verified verdicts spanning diverse case types: MENGADILI SENDIRI (MA's own sentencing), kasasi-ditolak (appeal rejected), memperbaiki (sentence modified), dual-kasasi (both parties appeal), PK (case review), and acquittals.

**Vonis accuracy: 100% (20/20)**, including:
- 5 MENGADILI SENDIRI cases (standard extraction)
- 5 Memperbaiki cases (modified sentence extraction)
- 3 Kasasi-ditolak cases (quoted lower court sentence)
- 2 Dual-kasasi cases (SENDIRI subsection within MENGADILI)
- 3 PK cases (peninjauan kembali)
- 2 Acquittal cases (membebaskan/melepaskan → 0)

Other fields (validated on subset): tuntutan 100% (5/5), kerugian 100% (4/4), daerah 100% (5/5), tahun 100% (5/5), nama_terdakwa 80% (4/5).

### 5.3 Known Failure Modes (Addressed)
1. **Kasasi ditolak**: When MA rejects the appeal, the lower court sentence stands. Pipeline detects "Menolak permohonan kasasi" and extracts the quoted lower court sentence. An earlier version fell back to subsidiary penalties — this bug systematically deflated vonis for terdakwa kasasi cases and created an artificial pemohon_kasasi effect.
2. **Memperbaiki**: When MA modifies the sentence ("Memperbaiki Putusan...mengenai pidana...menjadi"), pipeline now extracts the modified sentence directly from the Memperbaiki section.
3. **Dual-kasasi**: When both prosecutor and defendant file kasasi, the MENGADILI section contains both "Menolak" (for one party) and "Mengabulkan" (for the other). Pipeline now prioritizes the MENGADILI SENDIRI subsection over the menolak pattern.
4. **Acquittals**: Pipeline detects "membebaskan" or "melepaskan" (ontslag van alle rechtsvervolging) and returns 0, preventing fallback to lower-court sentences.
5. **Merged PDF text**: Some PDFs extract without spaces, handled by merged-text regex variants.
6. **Kerugian not stated**: ~25% of cases don't explicitly state the state financial loss figure.

## 6. Findings

**Table 1**: Example verdicts illustrating corpus diversity (kerugian bracket, region, pemohon, discount ratio).

| Region | Year | Kerugian | Tuntutan | Vonis | Ratio | Pemohon |
|--------|------|----------|----------|-------|-------|---------|
| Jakarta Pusat | 2025 | Rp300T | 18.0 yr | 14.0 yr | 78% | JPU |
| Jakarta Pusat | 2024 | Rp8.0T | 15.0 yr | 15.0 yr | 100% | JPU |
| Pekanbaru | 2025 | Rp24.6B | 8.0 yr | 9.0 yr | 112% | JPU |
| Banda Aceh | 2024 | Rp1.7B | 5.0 yr | 5.0 yr | 100% | Terdakwa |
| Semarang | 2025 | Rp392M | 8.5 yr | 0.5 yr | 6% | JPU |
| Padang | 2026 | Rp52M | 2.7 yr | 1.0 yr | 38% | JPU |
| Yogyakarta | 2025 | Rp15M | 2.0 yr | 2.0 yr | 100% | JPU |

*Notes*: Rp300T = PT Timah mega-corruption (includes Rp271T environmental damage). Ratio >100% indicates MA increased sentence beyond prosecution demand. Ratio 6% (Semarang) illustrates extreme judicial discount.

### 6.1 Sentencing Distribution (n=327, excluding acquittals)
- Mean sentence: **4.63 years** (median: 4.0 years)
- Range: 3 months to 18 years
- Std deviation: 3.28 years
- IQR: 2.0 – 6.0 years
- Mean prosecution demand: **6.58 years**
- Mean discount ratio: **84.1%** (median: 70.0%)
- Distribution is right-skewed (log-normal shape)
- Acquittals: 17 cases (5.0%) where MA overturned conviction

### 6.2 Pemohon Kasasi as Confounding Variable (Novel Finding)
We identify **pemohon kasasi** (appeal filer identity) as a critical variable for interpreting MA sentencing data:

| Pemohon Kasasi | n | Mean Vonis | Mean Ratio (v/t) |
|----------------|---|------------|------------------|
| JPU (prosecutor) | 181 (55%) | 4.78 yr | 77.8% |
| Terdakwa (defendant) | 113 (35%) | 4.75 yr | 98.2% |
| Unknown/missing | 33 (10%) | — | — |

**Key finding**: Welch's t-test reveals **no significant difference** in sentencing outcomes between JPU and terdakwa kasasi groups (t=0.07, p=0.95, Cohen's d=0.01). Mann-Whitney U test confirms (U=9876, p=0.62). Discount ratios show a descriptive difference (JPU 77.8% vs Terdakwa 98.2%) but this is not statistically significant (p=0.27).

The fundamental difference is not in outcomes but in *selection mechanism*:

- **JPU kasasi**: Prosecutor considers the PN sentence too light → files for harsher sentence. When MA accepts (mengabulkan), the sentence may increase. When MA rejects (menolak), the original "light" sentence stands.
- **Terdakwa kasasi**: Defendant considers the PN sentence too heavy → files for lighter sentence. When MA accepts, the sentence may decrease. When MA rejects, the original "heavy" sentence stands.

**Methodological implication**: Pemohon kasasi must be reported and controlled for in any MA sentencing analysis, not because outcomes differ, but because the *selection mechanism* into each group is fundamentally different. Failure to account for this makes any aggregate statistic uninterpretable.

**Correction note**: An earlier version of our extraction pipeline showed a dramatic apparent difference (JPU: 70.9% ratio vs Terdakwa: 59.6%). This was entirely an extraction artifact — subsidiary penalties were being extracted instead of actual sentences for kasasi-ditolak cases. Three iterative bug fixes (kasasi-ditolak quoted sentences, memperbaiki sections, dual-kasasi handling, acquittal detection) were required to reach the correct null finding. This serves as a cautionary tale for computational legal analysis.

### 6.3 Sentencing Discount
- Mean vonis/tuntutan ratio: **84.1%** (median: 70.0%)
- Sentences are on average ~16% lighter than prosecution demands
- Cases where vonis > tuntutan: 40 (13.2%), predominantly JPU kasasi where MA increased the sentence beyond tuntutan

### 6.4 State Loss and Sentencing
Strong positive correlation between kerugian negara and sentence severity (Spearman ρ=0.56, p<10⁻²², Pearson r=0.58):

| Kerugian Bracket | n | Mean Vonis | Median Vonis |
|-----------------|---|------------|--------------|
| <Rp100M | 21 | 2.8 yr | 2.0 yr |
| Rp100M–1B | 92 | 3.5 yr | 3.0 yr |
| Rp1B–10B | 76 | 4.6 yr | 5.0 yr |
| Rp10B–100B | 46 | 6.9 yr | 7.0 yr |
| >Rp100B | 19 | 10.4 yr | 10.0 yr |

Linear regression: vonis (years) = 1.60 × log₁₀(kerugian) − 10.12, R²=0.35 (n=251, after excluding 3 suspected extraction artifacts with kerugian < Rp1M). Each order-of-magnitude increase in state loss corresponds to ~1.6 additional years of imprisonment.

### 6.5 Geographic Distribution
40+ court regions represented. Jakarta Pusat has dramatically higher mean sentences (7.07yr vs 4.63yr overall, Welch's t=4.87, p<0.0001), with a median kerugian of Rp32.2B compared to Rp1.0B for other regions (31× higher). Top regions by case count: Jakarta Pusat (47), Surabaya (32), Bandung (23), Makassar (20), Medan (16).

**Critically, the Jakarta Pusat effect disappears when controlling for kerugian**: in a multivariate regression (Section 6.7), the Jakarta Pusat coefficient becomes non-significant (p=0.54). The higher sentences reflect the concentration of national mega-corruption cases (PT Timah Rp300T, Johnny Plate/BTS Rp8T, Jiwasraya Rp3.3T) rather than jurisdictional harshness.

### 6.6 Acquittal Patterns
Of 17 acquittals (5.0% of 344 cases with vonis≥0), 12 (71%) were filed by the defendant (terdakwa kasasi), 3 by the prosecutor (JPU kasasi), and 2 unknown. This asymmetry is expected: defendants appealing convictions are more likely to succeed than prosecutors appealing for harsher sentences. Acquittals span 2019–2025 with no obvious temporal trend, and are geographically dispersed (Jakarta Pusat 3, Medan 2, Makassar 1, Pekanbaru 2, and 9 other regions).

### 6.7 Regression Analysis

To assess which factors independently predict sentence severity, we fit a series of OLS models. We begin with kerugian-only models, then introduce tuntutan (prosecution demand) — which proves to be the strongest predictor — and finally test robustness.

#### 6.7.1 Kerugian-Only Models (n=251)

We fit nested OLS models on cases with valid kerugian (n=251, after excluding 3 suspected extraction artifacts with kerugian < Rp1M):

| Model | Predictors | R² | adj R² | BIC |
|-------|-----------|-----|--------|-----|
| M1 | log₁₀(kerugian) | 0.347 | 0.345 | 1217 |
| M2 | + pemohon_kasasi | 0.347 | 0.342 | 1222 |
| M3 | + Jakarta Pusat | 0.348 | 0.340 | 1227 |
| M4 | + year | 0.349 | 0.338 | 1233 |

Only log₁₀(kerugian) is significant (b=1.60, p<0.001). Pemohon kasasi (p=0.95), Jakarta Pusat (p=0.54), and year (p=0.74) are all non-significant. An F-test comparing M1 to M4 confirms the additional variables do not improve fit (F=0.16, p=0.92). The parsimonious model (M1) is preferred by BIC.

Quantile regression (median) confirms the OLS pattern: only log₁₀(kerugian) is significant (b=1.52, p<0.001), with all other predictors non-significant.

#### 6.7.2 Tuntutan Models: The Strongest Predictor (n=302)

Prosecution demand (tuntutan) is available for 302 cases. Two specifications reveal its dominance:

| Model | Predictors | R² | adj R² | n | BIC |
|-------|-----------|-----|--------|---|-----|
| M6 | log₁₀(tuntutan) | 0.418 | 0.416 | 302 | 1415 |
| M9 | tuntutan (linear, years) | **0.600** | 0.599 | 302 | 1301 |

The linear specification (M9: vonis = 0.49 + 0.63 × tuntutan_years, R²=0.60) outperforms the log specification (M6: R²=0.42), indicating that judges discount tuntutan by a roughly constant *proportion* rather than by a fixed amount. Each additional year of prosecution demand yields ~0.63 additional years of sentence — a systematic ~37% discount.

This R²=0.60 substantially exceeds kerugian alone (R²=0.35), establishing tuntutan as the strongest predictor of sentence severity in our dataset.

#### 6.7.3 Combined Model: Mediation Structure (n=236)

When tuntutan and kerugian are both available (n=236), both retain independent significance:

| Model | Predictors | R² | adj R² | BIC |
|-------|-----------|-----|--------|-----|
| M7 | log₁₀(tuntutan) + log₁₀(kerugian) | 0.492 | 0.488 | 1082 |
| M8 | + pemohon + JP + year | 0.496 | 0.485 | 1096 |

In M7, both log₁₀(tuntutan) (b=5.79, p<0.001) and log₁₀(kerugian) (b=0.82, p<0.001) are significant. Adding pemohon kasasi (p=0.28), Jakarta Pusat (p=0.32), and year (p=0.97) in M8 adds no predictive power. This suggests a **mediation structure**: kerugian influences tuntutan (prosecution calibrates demand to case magnitude), and tuntutan influences vonis (judges follow prosecution framing) — but kerugian also independently affects vonis beyond its effect through tuntutan. Judges consider raw case magnitude, not only the prosecutor's demand.

#### 6.7.4 Discount Ratio: Unpredictable Judicial Discretion

The vonis/tuntutan ratio (mean 84%) captures how much judges discount the prosecution demand. We model this ratio as a function of kerugian, pemohon, JP, and year (n=236):

**Discount model (Md)**: R²=0.013, F=0.76, p=0.55. No predictor is significant (all p>0.11). The magnitude of judicial discounting is effectively unpredictable from extracted case characteristics. This suggests that the ~37% average discount reflects case-specific judicial reasoning (defendant cooperation, mitigating factors, judge disposition) that our structured fields do not capture.

#### 6.7.5 Sensitivity and Robustness

**Outlier influence**: The 3 PT Timah cases (identical Rp300T kerugian) have minimal impact — removing them changes R² from 0.347 to 0.349 (n=248). However, removing all mega-cases (kerugian > Rp100B, n=19) drops R² from 0.347 to 0.222 (n=232), indicating that the kerugian-vonis relationship is substantially driven by extreme cases. The coefficient remains significant (b=1.52, p<0.001) but weakened.

**Missing data**: Cases without kerugian (n=76) have significantly lower mean vonis (3.67yr) than cases with kerugian (4.92yr, Welch's t=3.11, p=0.002). This indicates that missing kerugian is **not missing completely at random** (MCAR). Many cases without explicit kerugian figures involve gratification (suap) rather than embezzlement — structurally different cases with different sentencing dynamics. Our regression sample (n=251) is therefore biased toward embezzlement-type cases with higher sentences.

**Power analysis**: For the pemohon kasasi null finding (p=0.95), our sample (n_JPU=181, n_terdakwa=113, pooled SD=3.25yr) provides 80% power to detect effects ≥1.09 years (Cohen's d≥0.34). Since the observed difference is 0.03 years (d=0.01), our null claim is credible for effects of practical significance (≥1 year).

**Cross-validation**: 10-fold CV on the kerugian-only model (M1) yields mean R²=0.26 (SD=0.33) and mean MAE=2.06 years, indicating moderate but variable out-of-sample performance.

#### 6.7.6 Summary

The regression analysis reveals a two-level sentencing structure:

1. **Tuntutan dominates** (R²=0.60): Judges primarily follow prosecution demand, discounting by ~37% on average
2. **Kerugian independently contributes** (R²=0.35 alone; p<0.001 after tuntutan control): Case magnitude matters beyond prosecutorial framing
3. **Geographic, temporal, and pemohon effects are absent** after controlling for case magnitude
4. **Judicial discretion is opaque**: The discount ratio (how much judges deviate from tuntutan) is unpredictable from any extracted variable

### 6.8 Pertimbangan Hakim (Judicial Considerations)
Only 6.3% of MA kasasi verdicts contain explicit aggravating/mitigating factor lists. This is a structural limitation: MA cassation reviews the *legality* of lower court decisions, not the *factual* merits. Factor extraction requires PN-level first-instance verdicts.

## 7. Limitations

1. **Selection bias**: Only MA cassation/PK cases (appealed), not first-instance PN verdicts. Our corpus overrepresents contentious cases where one party considered the lower court outcome unjust.
2. **Missing data is not random**: Cases without kerugian have significantly lower mean vonis (3.67yr vs 4.92yr, p=0.002), likely reflecting structural differences between gratification (suap) and embezzlement cases. Our regression sample (n=251) is biased toward embezzlement-type cases. Three suspected extraction artifacts (kerugian < Rp1M) were excluded.
3. **Outlier sensitivity**: Removing mega-cases (kerugian > Rp100B, n=19) drops the kerugian-vonis R² from 0.35 to 0.22. The relationship, while consistently significant, is substantially driven by extreme cases.
4. **Pemohon kasasi confound**: 55/35/10% JPU/terdakwa/unknown split. While the null finding for pemohon is supported by power analysis (MDE=1.09yr), effects smaller than 1 year cannot be ruled out.
5. **Extraction errors**: Regex-based. While golden set shows 100% vonis accuracy on 20 diverse cases, systematic failures remain possible on untested patterns.
6. **Temporal skew**: 2025 overrepresented (136/327, 42%) due to MA publication patterns and scraping recency — substantially mitigated by year-filtered scraping (2014–2024) with 14 years now represented.
7. **Kerugian extraction**: Environmental damage sometimes included, inflating figures (e.g., PT Timah Rp300T includes Rp271T environmental). ~30% of cases have no kerugian extracted — many are gratification cases where no state loss figure applies.
8. **Factor extraction limited**: Only ~6% of MA kasasi verdicts contain explicit aggravating/mitigating factor lists (structural limitation of cassation vs first-instance).
9. **Unexplained variance**: Even the best model (M9, tuntutan linear) leaves 40% of variance unexplained. Factors not captured by our pipeline — pasal charged, defendant role, cooperation, judge identity — likely contribute substantially. The discount ratio model (R²=0.01) demonstrates that judicial discretion operates through channels opaque to our extraction.

## 8. Ethical Considerations

All data is from publicly available court records. Defendant names are public record and used only for corpus integrity (deduplication). Analysis is presented in aggregate. This research is designed to support evidence-based anti-corruption policy, not individual case litigation.

## 9. Conclusion and Future Work

CorpusKorupsi provides the first structured, machine-readable corpus of Indonesian Supreme Court corruption verdicts. Our key findings are:

1. **Prosecution demand dominates sentencing** (R²=0.60): Judges sentence at approximately 63% of tuntutan, making the prosecution's demand the single strongest predictor of outcome. This has immediate policy implications — if sentences track tuntutan, then prosecutorial behavior (what prosecutors demand) may matter more than judicial behavior (how judges decide).

2. **State financial loss independently matters** (R²=0.35 alone; p<0.001 after tuntutan control): Kerugian negara predicts both tuntutan and vonis, and retains independent significance when both are modeled together. Each log-order increase in state loss adds ~1.6 years. This mediation structure (kerugian -> tuntutan -> vonis) suggests judges consider raw case magnitude beyond the prosecutor's framing.

3. **Judicial discretion is opaque**: The discount ratio (vonis/tuntutan, mean 84%) is unpredictable from any extracted variable (R²=0.01). Whatever drives judges to deviate from tuntutan — defendant cooperation, mitigating factors, individual disposition — cannot be captured by our structured fields.

4. **Geographic, temporal, and pemohon effects are absent**: The Jakarta Pusat effect (p=0.54), temporal trends (p=0.74), and pemohon kasasi identity (p=0.95, MDE=1.09yr) all vanish after controlling for case magnitude. These are composition effects, not substantive influences.

Compared to ICW's annual sentencing monitoring (descriptive and manual), our approach offers reproducibility, structured data, and confound-controlled analysis. Our mean sentence of 4.63 years (MA cassation) exceeds ICW's 2024 finding of 3.25 years across all court levels, consistent with selection bias from cassation cases.

**Future work**:
- **Paper 2**: Extended predictive model incorporating pasal (articles charged), defendant role, and cooperation indicators via NLP extraction, with quantile regression for the non-normal residuals identified here
- **PN Tipikor expansion**: First-instance verdicts with full pertimbangan hakim (judicial reasoning) — where aggravating/mitigating factors are explicitly stated — for factor analysis
- **NER pipeline**: Named entity recognition for legal actors (judges, prosecutors, defendants) and their networks, building on Nuranti et al. (2025)
- **Tuntutan determinants**: What predicts prosecution demand itself? Modeling tuntutan ~ kerugian + pasal + defendant_role would illuminate the prosecutorial decision that effectively sets sentence range

## Data Availability
Corpus, extraction code, and golden set will be released on GitHub (MIT license) and Zenodo/HuggingFace Datasets upon publication.

## References

Aletras, N., Tsarapatsanis, D., Preoţiuc-Pietro, D., & Lampos, V. (2016). Predicting judicial decisions of the European Court of Human Rights: A Natural Language Processing perspective. *PeerJ Computer Science*, 2, e93.

Amaral, G. N., et al. (2022). Using deep learning to predict outcomes of legal appeals better than human experts: A study with data from Brazilian federal courts. *PLOS ONE*, 17(7), e0272287.

Chen, D. L., et al. (2019). Judicial analytics and the great transformation of American law. *Artificial Intelligence and Law*, 27, 15–42.

Dressel, J., & Farid, H. (2018). The accuracy, fairness, and limits of predicting recidivism. *Science Advances*, 4(1), eaao5580.

Hasanah, U., et al. (2023). Analysis of Indonesian language dataset for tax court cases: Multiclass classification of court verdicts. *Jurnal Riset Informatika*, 5(2), 147–156.

Henderson, J. V., & Kuncoro, A. (2011). Corruption and local democratization in Indonesia: The role of Islamic parties. *Journal of Development Economics*, 94(2), 164–180.

Ibrahim, M. A., et al. (2024). Hybrid deep learning for legal text analysis: Predicting punishment durations in Indonesian court rulings. *arXiv preprint*, arXiv:2410.20104.

ICW (Indonesia Corruption Watch). (2024). Sentencing trend monitoring report 2024. Jakarta: ICW.

ICW (Indonesia Corruption Watch). (2023). Sentencing trend monitoring report 2023. Jakarta: ICW.

Medvedeva, M., Vols, M., & Wieling, M. (2020). Using machine learning to predict decisions of the European Court of Human Rights. *Artificial Intelligence and Law*, 28, 237–266.

Nuranti, E. Q., & Yulianti, E. (2020). Legal entity recognition in Indonesian court decision documents using Bi-LSTM and CRF approaches. In *Proc. ICACSIS 2020*, pp. 429–436.

Nuranti, E. Q., Intizhami, N. S., Yulianti, E., Latief, A. M. I., & Al Ghozy, O. I. (2025). A systematical procedure to extracting legal entities from Indonesian judicial decisions. *MethodsX*, 14, 103179.

Olken, B. A. (2007). Monitoring corruption: Evidence from a field experiment in Indonesia. *Journal of Political Economy*, 115(2), 200–249.

Ostling, R., et al. (2023). The Cambridge Law Corpus: A dataset for legal AI research. *arXiv preprint*, arXiv:2309.12269.

Transparency International. (2024). Corruption Perceptions Index 2024. Berlin: Transparency International.

Yulianti, E., et al. (2024). Named entity recognition on Indonesian legal documents: A dataset and study using transformer-based models. *International Journal of Electrical and Computer Engineering*, 14(5), 5737–5748.
