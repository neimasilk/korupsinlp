# Datasheet: KorpusKorupsi v1.1

Following the framework of Gebru et al. (2021), "Datasheets for Datasets."

> **v1.1 (July 2026) supersedes v1.0.** v1.0 (frozen 2026-07-07) contained field values
> from a parser version later shown to have systematic extraction errors (see Validation)
> and was never publicly released. v1.1 is the first release version.
> `TBD-R5` marks numbers to be refreshed from the final database before release.

## Motivation

**For what purpose was the dataset created?**
To enable computational analysis of corruption sentencing patterns in Indonesia. No
structured, machine-readable dataset of Indonesian corruption verdicts previously
existed, despite the public availability of court decisions.

**Who created the dataset and on behalf of which entity?**
Mukhlis Amien, Universitas [redacted], Malang, Indonesia. Independent research project.

**Who funded the creation of the dataset?**
Self-funded. No external funding.

## Composition

**What do the instances represent?**
Each instance is one court decision document in a corruption case scraped from the
Supreme Court directory — predominantly Mahkamah Agung cassation (kasasi) and case
review (PK) decisions, with a small number of first-instance (PN) and appellate (PT)
tipikor decisions that appear in the same directory.

**How many instances are there in total?**
693 records. Domain audit (document-text based, never trusting the directory's
category label): 465 confirmed corruption cases (447 by database text, 8 by full-PDF
check, 10 by TPK register code), **14 confirmed NON-corruption** (7 civil/administrative
PDT/TUN cases, 7 Pid.Sus cases without corruption markers, including one pure narcotics
case), 119 unconfirmable without PDF, 95 with no text at all. All rows are released
with an `is_tipikor` flag (1/0/NULL); **analysis should filter `is_tipikor = 1`.**

**Known metadata-quality issues (kept transparent, not silently dropped):**
- 70 rows with NULL case_number and 25 with case_number `'?'` (early scrape batches);
- 2 genuinely duplicated case numbers (3 extra rows);
- `date_decided` contains mojibake for a subset of rows;
- `tahun` follows the REGISTRATION-year convention (the year printed in the case
  number), which can differ from the decision year, and for PK documents postdates
  the underlying trial.

**What data does each instance consist of?**
14 structured fields extracted from PDF verdict text and HTML metadata: identifiers
(corpus_id, case_number, date_decided), case characteristics (tahun, daerah, pasal,
is_tipikor), parties (nama_terdakwa, pemohon_kasasi, nama_hakim), sentencing
(vonis_bulan, tuntutan_bulan, kerugian_negara), and amar category.
See `data_dictionary.json` for field descriptions and missing-data rates (`TBD-R5`).

**Extraction conventions (important for correct use):**
- `vonis_bulan` = the FINAL operative prison term in months after the document's
  decision, tracing the appellate chain: kasasi rejected → the quoted lower-court
  sentence stands; "menolak dengan perbaikan" → the corrected term; MENGADILI SENDIRI
  → the MA's own term; PK → the term standing after the PK ruling. Acquittal = 0.
  Subsidiary imprisonment (in lieu of unpaid fines/restitution) is excluded.
- `tuntutan_bulan` = the prosecutor's demanded prison term in months.
- `kerugian_negara` = the state financial loss the court accepts (typically the
  BPKP/BPK/inspectorate audit figure), in Rupiah. It is NOT uang pengganti
  (restitution), NOT fines, NOT bribe/gratuity amounts, and NOT "kerugian
  perekonomian negara" (a distinct legal category). For acquittals the field is NULL
  by rule: a figure in an acquitted case is an allegation or dissent, not an
  established loss.
- Multi-defendant documents are represented by ONE defendant's consistent
  (nama, tuntutan, vonis, kerugian) tuple; see Validation for the residual
  attribution error this creates.
- `daerah` = city of the first-instance trial court, not the defendant's origin.

**Is any information missing from individual instances?**
Yes, substantially, and NOT at random: kerugian_negara coverage is ~40% (`TBD-R5`);
cases without a documented kerugian are structurally different (more bribery/
gratification — formal offenses with no state-loss element — with lower mean
sentences). Analyses conditioning on kerugian therefore use a selected subsample;
this is disclosed in the accompanying paper.

## Validation (NEW in v1.1)

**How accurate are the extracted fields?**
Four rounds of BLIND holdout validation (July 2026), 20 freshly sampled cases per
round, stratified by kerugian tercile + a no-kerugian stratum. Annotators (LLM agents
reading the full PDFs) never saw parser output; agreement was computed
programmatically and every mismatch was manually adjudicated against the PDF.
Each failed round drove a test-first parser fix; fixed rounds become regression
fixtures and are never reused for validation.

Accuracy of the RELEASED parser version on the latest fresh holdout (n=20, Wilson
95% CI) — `TBD-R5: replace with round-5 holdout numbers`:
- vonis_bulan: 95% [76–99] (round 4)
- tuntutan_bulan: 90% [70–97]
- kerugian_negara: 85% [64–95] (round 4, pre-round-5 fixes)
- daerah: 100% (after PN/PT-prefix normalization) · tahun: 100%

**Residual error taxonomy (what the ~10% consists of):**
1. **Per-defendant attribution** (semantic, not fixable by pattern matching): in
   multi-defendant documents the parser may return the project-wide loss where the
   court attributes only a component to the document's defendant, or mix defendants'
   tuple elements. Error direction: overstates kerugian for split cases.
2. **Document-internal inconsistencies**: digit transpositions between sections,
   conflicting court names — irreducible without external sources.
3. **Rare phrasing variants**: the long tail. Nineteen distinct failure classes were
   found and fixed across four rounds (statutory-threshold figures, dissenting-opinion
   sentences in majority-acquittal cases, MA footer blocks splitting amounts
   mid-number, comparator-case quotes, merged text without spaces, reversed word
   order, fine amounts near loss mentions, and others — full list in the repository's
   DECISIONS.md D14–D21 and tests/test_holdout*_bugs.py).

**Methodological caveat for reusers:** document weirdness is heavy-tailed. A static
golden set will overestimate extraction accuracy; repeated fresh holdouts are the
only honest measurement. The released accuracy figures come from holdout cases the
released parser version never trained on.

## Collection Process

**How was the data acquired?**
Scraped from putusan3.mahkamahagung.go.id (official public MA verdict repository),
March 2026; polite sequential scraper (2s delays). PDFs processed with pdfminer;
regex extraction targeting Indonesian legal document structure (MENGADILI sections,
Tuntutan Pidana, audit-anchored loss statements), with MA watermark/footer/page-marker
stripping.

**If the dataset relates to people, were they informed?**
See Ethics below.

**Over what timeframe?**
Scraping March 2026; verdicts span 2011–2026 registrations.

## Ethics & Release Policy (expanded in v1.1)

Court verdicts are public documents that the Mahkamah Agung itself publishes for
transparency; this corpus is a faithful, verified copy of that public record — not a
new aggregation that increases individual exposure. Defendant names are retained
because removing them would break verifiability against the source (auditable-by-
anyone is a design goal). However:
- The accompanying analyses make claims at the institution/region level only, never
  about individuals.
- The dataset must NOT be used for individual case prediction, litigation support,
  targeting or profiling of specific persons (see Uses below).
- Released values are validated (see Validation); v1.0, which contained values known
  to be wrong, was withheld — releasing unvalidated individual-level data is not
  transparency but pollution.

## Uses

**Has the dataset been used already?**
Yes: descriptive corpus analysis, sentencing-proportionality regressions (elasticity
of demands/sentences w.r.t. loss), demand-anchoring analysis, and 34+ registered
text-feature experiments (negative result: pertimbangan text adds no predictive power
over numeric features at this n; binary charge-type keywords add +0.03 CV R²).

**What should the dataset NOT be used for?**
- Individual case prediction or litigation support;
- identifying, profiling, or targeting specific defendants;
- causal claims about sentencing fairness without design for selection (only appealed
  cases reach the MA — collider risk is documented in the accompanying paper);
- generalizing to all Indonesian corruption cases (first-instance verdicts are
  largely absent);
- using `kerugian_negara` as if it were complete or exact: ~40% coverage, ~85–90%
  exact-match accuracy with a known error taxonomy (see Validation).

## Distribution

CSV + JSON via GitHub and Zenodo (DOI), CC-BY-4.0 (data), MIT (code). v1.1 is the
first public release; SHA256 checksums accompany the archive.

## Maintenance

Mukhlis Amien. Planned extensions: PN Tipikor first-instance verdicts (scaling +
fixing the cassation-selection confound), additional fields, periodic re-scrapes.
Pull requests welcome; parser changes must pass the full regression suite
(golden30 + holdout fixtures).

## References

Gebru, T., et al. (2021). Datasheets for Datasets. *CACM*, 64(12), 86-92.
