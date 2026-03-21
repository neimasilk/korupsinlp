# Paper 1: Corpus Description & Sentencing Patterns
## Working Title
**"CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Decisions and Sentencing Patterns"**

## Target Venue
- Primary: ACL/EMNLP Resource & Evaluation track, or LREC-COLING
- Backup: Indonesian NLP workshop, or Southeast Asian NLP venue

## Core Contribution
1. **Novel dataset**: First large-scale structured corpus of Indonesian corruption verdicts (target: 3,000+ cases from Mahkamah Agung)
2. **Extraction methodology**: Regex-based pipeline for Indonesian legal document parsing (benchmarked against human golden set)
3. **Descriptive findings**: First computational census of sentencing patterns, geographic distribution, and state losses in Indonesian corruption cases

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
- vonis/tuntutan ratio distribution (mean ~55%, median 50%)
- Cases where vonis > tuntutan (rare, legally interesting)
- Predictors of discount magnitude (preliminary)

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

## Key Numbers to Report (current n=102 PDF-parsed)
| Metric | Value |
|--------|-------|
| Verdicts (PDF-parsed) | 102 |
| Mean sentence | 4.2 years |
| Median sentence | 4.0 years |
| Mean discount ratio | 54.9% |
| Median kerugian | Rp 2.07B |
| Max kerugian | Rp 300T (PT Timah) |
| Geographic coverage | 25+ provinces |
| Temporal range | 2011-2026 |
