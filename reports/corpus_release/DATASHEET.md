# Datasheet: KorpusKorupsi v1.0

Following the framework of Gebru et al. (2021), "Datasheets for Datasets."

## Motivation

**For what purpose was the dataset created?**
To enable computational analysis of corruption sentencing patterns in Indonesia. No structured, machine-readable dataset of Indonesian corruption verdicts previously existed, despite the public availability of court decisions.

**Who created the dataset and on behalf of which entity?**
Mukhlis Amien, Universitas [redacted], Malang, Indonesia. Independent research project, not funded by any external entity.

**Who funded the creation of the dataset?**
Self-funded. No external funding.

## Composition

**What do the instances represent?**
Each instance is one Supreme Court (Mahkamah Agung) decision in a corruption case, either a cassation (kasasi) or case review (peninjauan kembali, PK) decision.

**How many instances are there in total?**
557 records. Of these, 488 have case metadata, 344 have extracted sentences (327 with prison sentences > 0, 17 acquittals), and 69 are empty scrapes (server errors during collection).

**Does the dataset contain all possible instances?**
No. The dataset represents a sample of MA corruption decisions available on putusan3.mahkamahagung.go.id as of March 2026. The MA website contains approximately 22,000+ corruption-category pages; our corpus covers a fraction obtained through paginated scraping with year-filtered queries (2011-2026). Additionally, only cases appealed to the MA are included — first-instance PN Tipikor verdicts are excluded.

**What data does each instance consist of?**
13 structured fields extracted from PDF verdict text and HTML metadata:
- **Identifiers**: corpus_id, case_number, date_decided
- **Case characteristics**: tahun (year), daerah (region), pasal (legal articles)
- **Parties**: nama_terdakwa (defendant name), pemohon_kasasi (appeal filer), nama_hakim (judges)
- **Sentencing**: vonis_bulan (sentence in months), tuntutan_bulan (prosecution demand), kerugian_negara (state financial loss in Rupiah)
- **Metadata**: amar (verdict summary category)

See `data_dictionary.json` for complete field descriptions and missing data rates.

**Is there a label or target associated with each instance?**
No single designated label. For sentencing analysis, `vonis_bulan` serves as the outcome variable.

**Is any information missing from individual instances?**
Yes, substantially. Field completeness ranges from 49% (kerugian_negara) to 100% (corpus_id). Missing data is NOT random — cases without kerugian have significantly lower mean sentences (3.67yr vs 4.92yr, p=0.002), likely because they involve gratification/bribery rather than embezzlement. See Section 6.7.5 of the accompanying paper for analysis.

**Are there any errors, sources of noise, or redundancies?**
- 3 suspected kerugian extraction artifacts (< Rp1M) have been set to NULL
- 3 PT Timah cases share identical Rp300T kerugian (a single mega-corruption case with multiple defendants)
- Some kerugian values include environmental damage (e.g., PT Timah Rp300T includes Rp271T environmental)
- Regex-based extraction has known failure modes documented in Section 5.3 of the paper
- 69 records are empty scrapes (server errors) with no useful data

**Is the dataset self-contained?**
Yes. All structured fields are included. Raw PDF text and HTML are not included in the release but can be re-obtained from the public source.

## Collection Process

**How was the data associated with each instance acquired?**
Scraped from putusan3.mahkamahagung.go.id (official public MA verdict repository). HTML metadata extracted from listing and detail pages. Structured fields extracted from PDF verdict text using regex-based pipeline.

**What mechanisms or procedures were used to collect the data?**
Polite sequential web scraper with 2-second inter-request delays. PDFs downloaded and processed with pdfminer for text extraction. Regex extractors target specific sections of Indonesian legal document format (MENGADILI, Tuntutan Pidana, etc.).

**If the dataset relates to people, were they informed?**
The dataset contains defendant names, which are public record in Indonesian court verdicts. Court decisions are published by the MA specifically for public access and transparency. No consent was sought as this is publicly available government data.

**Over what timeframe was the data collected?**
Scraping performed March 20-22, 2026. Verdicts span decisions from 2011 to 2026.

## Preprocessing/Cleaning/Labeling

**Was any preprocessing applied?**
- PDF text extracted using pdfminer with MA watermark stripping
- Indonesian Rupiah amounts normalized (dot-as-thousands, comma-as-decimal)
- Duration expressions normalized to months (tahun/bulan/hari)
- Court names mapped to province-level regions
- 3 suspected kerugian artifacts (< Rp1M) set to NULL

**Was the "raw" data saved?**
Raw HTML and PDF files are stored locally but not included in the public release due to size. They can be re-obtained from the source URL.

**Is the software used to preprocess the data available?**
Yes. The full extraction pipeline is released as open source (MIT license) at the accompanying GitHub repository.

## Uses

**Has the dataset been used for any tasks already?**
Yes, in the accompanying paper: descriptive corpus analysis, OLS regression of sentencing determinants, sensitivity analysis, and missing data characterization.

**Is there a repository that links to any or all papers that use this dataset?**
The accompanying GitHub repository will maintain a list of publications.

**What (other) tasks could the dataset be used for?**
- Predictive sentencing models (predicting vonis from case characteristics)
- Named entity recognition training for Indonesian legal text
- Judge-level sentencing variation analysis
- Geographic corruption pattern mapping
- Temporal trend analysis (with appropriate controls for composition effects)
- Comparative legal studies (Indonesian vs other jurisdictions)

**Is there anything about the composition that might impact future uses?**
- **Selection bias**: Only MA cassation/PK cases. Not representative of all corruption sentencing.
- **Temporal skew**: 2025 is overrepresented (42% of sentenced cases).
- **Missing data bias**: Cases without kerugian are structurally different (more likely gratification).
- **Mega-case influence**: Extreme outliers (Rp300T PT Timah) strongly influence statistical relationships.

**Are there tasks for which the dataset should NOT be used?**
- Individual case prediction or litigation support
- Identifying or targeting specific defendants
- Drawing causal conclusions about sentencing fairness without appropriate controls
- Generalizing to all Indonesian corruption cases (only MA appeals are included)

## Distribution

**How is the dataset distributed?**
CSV and JSON formats via GitHub repository and Zenodo (with DOI).

**When was the dataset first released?**
2026 (upon publication of accompanying paper).

**What license is the dataset distributed under?**
CC-BY-4.0 for the data. MIT for the extraction code.

## Maintenance

**Who is supporting/hosting/maintaining the dataset?**
Mukhlis Amien (primary author).

**Will the dataset be updated?**
Potentially. Future versions may include additional verdicts, expanded field extraction, and PN Tipikor first-instance verdicts.

**If others want to extend/augment/build on this dataset, is there a mechanism?**
Pull requests to the GitHub repository are welcome. The extraction pipeline is designed to be extensible.

## References

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daume III, H., & Crawford, K. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86-92.
