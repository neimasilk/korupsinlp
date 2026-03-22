# Paper 1: Corpus Description & Sentencing Patterns
## Working Title
**"CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Decisions and Sentencing Patterns"**

## Target Venue
- Primary: ACL/EMNLP Resource & Evaluation track, or LREC-COLING
- Backup: Indonesian NLP workshop, or Southeast Asian NLP venue

## Core Contribution
1. **Novel dataset**: First large-scale structured corpus of Indonesian corruption verdicts (500+ MA kasasi/PK decisions, target: 1,000+)
2. **Extraction methodology**: Regex-based pipeline for Indonesian legal document parsing with 85.5% P0 field extraction rate
3. **Novel finding**: Pemohon kasasi (appeal filer) as confounding variable — 60% JPU kasasi vs 40% terdakwa kasasi, with systematically different sentencing patterns
4. **Descriptive findings**: First computational census of sentencing patterns, geographic distribution, and state losses in Indonesian corruption cases

## Outline

### 1. Introduction
- Corruption as Indonesia's persistent governance challenge (CPI rank, KPK data)
- Gap: no structured, machine-readable dataset of corruption verdicts despite public availability
- Contribution: corpus + extraction pipeline + descriptive analysis
- Research questions:
  - RQ1: What are the distributional characteristics of corruption sentencing at the MA level?
  - RQ2: How do sentences vary by geography, magnitude of state loss, and legal basis?
  - RQ3: Is there systematic "sentencing discount" (vonis < tuntutan) and what predicts it?

### 2. Related Work
- Indonesian legal NLP: Nuranti et al. (2020), prior work on Indonesian court documents
- Computational legal studies: sentencing analysis in US/EU contexts
- Southeast Asian legal corpora (if any)
- Anti-corruption data mining: limited literature, mostly policy-focused
- Key gap: no prior structured corpus from MA tipikor decisions

### 3. Data Source & Collection
- Source: putusan3.mahkamahagung.go.id (public, open access)
- Scope: MA kasasi/PK decisions in corruption category
- Selection bias: only appealed cases reach MA — explicit discussion of implications
- Non-deterministic pagination: multi-run scraping strategy, union+dedup
- PDF extraction as key enabler (HTML metadata insufficient)
- Collection statistics: total verdicts, PDF availability rate, temporal coverage

### 4. Extraction Pipeline
- Architecture: PDF text extraction → regex field extractors → normalization
- Fields extracted:
  - Sentence duration (vonis_bulan): MENGADILI section targeting
  - Prosecution demand (tuntutan_bulan): "Tuntutan Pidana" section header
  - State loss (kerugian_negara): Rupiah normalization (Indonesian format)
  - Region (daerah): court name → province mapping
  - Year, articles charged, defendant name, judges
- Design decisions: why regex over ML (interpretability, no training data, legal text regularity)

### 5. Quality Evaluation
- Golden set: 20 manually annotated verdicts (diverse by year, region, sentence length)
- Per-field precision, recall, F1
- Error analysis: systematic failure modes
  - False negatives: PDF format variations, scanned-only PDFs
  - False positives: tuntutan/vonis confusion, wrong section extraction
- Comparison: PDF vs HTML extraction rates

### 6. Corpus Statistics & Findings
#### 6.1 Sentencing Distribution
- Mean/median sentence duration
- Distribution shape (log-normal?)
- Minimum sentence (1 year) — legal minimum for Pasal 2/3 UU 31/1999
- Maximum sentences (15+ years)
- Comparison to statutory ranges

#### 6.2 State Loss (Kerugian Negara)
- Log-scale distribution from Rp27M to Rp300T
- Median ~Rp2B, heavy right tail
- Mega-corruption cases (>Rp1T): PT Timah, Jiwasraya-class
- Relationship between kerugian and vonis (log-linear?)

#### 6.3 Geographic Patterns
- Jakarta Pusat dominant (national-level cases)
- Provincial distribution map
- Regional sentencing variation (preliminary)

#### 6.4 Temporal Patterns
- MA publication bias toward recent years
- Caution against interpreting as crime trends

#### 6.5 Sentencing Discount
- vonis/tuntutan ratio distribution (mean 66.2%, median 60.0%, n=172)
- Cases where vonis > tuntutan: 15 cases (8.7%) — mostly JPU kasasi where MA increased sentences
- Predictors of discount magnitude (preliminary)

#### 6.6 Pemohon Kasasi Effect (NOVEL)
- **Key finding**: Who files the appeal fundamentally shapes the sentencing distribution
- JPU kasasi (prosecutor appeal, 60%): mean vonis 4.3yr, mean ratio 70.9% — prosecutors appeal when they want harsher sentences
- Terdakwa kasasi (defendant appeal, 40%): mean vonis 3.6yr, mean ratio 59.6% — defendants appeal when they want lighter sentences
- Implication: all MA kasasi sentencing analysis MUST stratify by pemohon_kasasi
- This is a confounding variable that previous Indonesian legal studies have not addressed

### 7. Limitations
- **Selection bias**: only MA kasasi/PK (appealed) cases, NOT first-instance PN verdicts
- **Extraction errors**: regex-based, not 100% accurate
- **PDF availability**: ~69% of verdicts have downloadable PDFs
- **Temporal coverage**: skewed toward recent years (2024-2026)
- **Kerugian extraction**: some cases have environmental damage included, inflating figures
- **No defendant demographics**: gender, age, position level hard to extract

### 8. Ethical Considerations
- All data from public court records (open access)
- Defendant names are public record but used only in aggregate
- Risk of misinterpretation: correlation ≠ causation in sentencing patterns
- Research designed to support anti-corruption policy, not individual case litigation

### 9. Conclusion & Future Work
- Paper 2: Predictive sentencing model (what predicts sentence severity?)
- Paper 3: NER + relation extraction for legal actors (judges, prosecutors, defendants)
- Paper 4: Temporal dynamics — are sentences getting harsher or more lenient?
- Integration with KPK enforcement data
- PN Tipikor first-instance data (35+ SIPP systems — very hard)

## Data Availability
- Corpus released on Zenodo/HuggingFace Datasets
- Extraction code on GitHub (MIT license)
- Golden set included for reproducibility

## Estimated Figures
1. Pipeline architecture diagram
2. Sentencing distribution histogram
3. Log-scale kerugian distribution
4. Geographic heatmap of Indonesia
5. Vonis vs kerugian scatter plot
6. Discount ratio distribution
7. Temporal distribution with caveats

## Key Numbers to Report (Session 7 final, n=327 with vonis>0, 557 total)
| Metric | Value |
|--------|-------|
| Verdicts (total scraped) | 557 |
| With case metadata | 488 (87.6%) |
| Parsed | 518 |
| Verdicts (with vonis>0) | 327 |
| Acquittals detected | 17 (5.0%) |
| Mean sentence | **4.63 years** |
| Median sentence | 4.0 years |
| Std deviation | 3.28 years |
| Range | 3 months — 18 years |
| Mean tuntutan | 6.58 years |
| Mean discount ratio | **84.1%** |
| Median discount ratio | 70.0% |
| Vonis > tuntutan | 40 (13.2%) |
| Median kerugian | Rp 1.41B |
| Max kerugian | Rp 300T (PT Timah) |
| Geographic coverage | 40+ daerah |
| Temporal range | 2011-2026 (14 years) |
| Pemohon kasasi: JPU | 181 (55%) — mean 4.78yr, ratio 77.8% |
| Pemohon kasasi: Terdakwa | 113 (35%) — mean 4.75yr, ratio 98.2% |
| Welch's t-test (vonis) | t=0.07, p=0.95, d=0.01 (NOT significant) |
| Spearman ρ (kerugian~vonis) | 0.56, p<10⁻²² |
| Pearson r | 0.58, p<10⁻²⁴ |
| Linear model R² | 0.33 |
| Golden set (n=20) | 100% vonis accuracy |

**Session 8 additions**: Related Work with 17 real citations, multivariate regression (Section 6.7),
acquittal analysis (Section 6.6), References section. Key regression finding: only log10(kerugian)
is significant (b=1.33, p<0.001); pemohon (p=0.77), JP (p=0.23), year (p=0.65) all non-significant.

### Multivariate Regression (n=254, Session 8)
| Model | R² | adj R² | BIC | Key finding |
|-------|-----|--------|------|-------------|
| M1: log10(kerugian) | 0.334 | 0.332 | 1237 | **Best by BIC** |
| M4: + pemohon + JP + year | 0.339 | 0.328 | 1252 | Additional vars not significant |
| F-test M1 vs M4 | | | | F=0.54, p=0.65 |
| 10-fold CV (M4) | | | | Mean R²=0.25, MAE=2.09yr |

### Kerugian-Vonis Brackets (n=254)
| Kerugian | n | Mean Vonis | Median Vonis |
|----------|---|------------|--------------|
| <100M | 21 | 2.8 yr | 2.0 yr |
| 100M-1B | 92 | 3.5 yr | 3.0 yr |
| 1B-10B | 76 | 4.6 yr | 5.0 yr |
| 10B-100B | 46 | 6.9 yr | 7.0 yr |
| >100B | 19 | 10.4 yr | 10.0 yr |
