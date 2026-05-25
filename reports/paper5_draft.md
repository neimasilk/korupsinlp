# Fictitious Procurement, the Village Penalty, and the Silence of Moral Language: A Computational Anatomy of Indonesian Corruption

## Abstract

What does corruption look like in Indonesia, and does the justice system respond equally to different types? We computationally extract corruption profiles from 367 Indonesian Supreme Court verdicts using regex-based feature extraction on judicial reasoning texts (*pertimbangan hakim*). Three findings emerge. First, **fictitious procurement** (*pengadaan fiktif*) is the dominant corruption method, appearing in 33% of verdicts — suggesting a systemic vulnerability in public procurement. Second, we identify a **village penalty**: village-level (*desa*) corruption cases receive 4.7 times more prison years per billion rupiah stolen than elite corruption cases involving gratification and money laundering (median 5.0 vs 1.1 years per billion, p=0.016). Village corruptors also receive lower sentencing discounts (0.645 vs 0.882 for elite cases, p=0.030). Third, **moral language is nearly absent** from judicial reasoning: only 8.7% of verdicts contain any evaluative language (e.g., "reprehensible," "greedy"), while technical-legal language dominates (e.g., "proven according to law" in 34%, "against the law" in 33%). K-means clustering identifies four distinct corruption types — general, gratification-elite, legislative-APBD, and village-procurement — that differ significantly in prosecution demands (p=0.009) and sentences (p=0.007) but not in judicial discount (p=0.574), suggesting that differential treatment originates with prosecutors rather than judges. These findings reveal a regressive justice system where small-scale village corruption is punished more severely per unit of harm than large-scale elite corruption, and where the language of adjudication systematically strips moral content from the most morally charged category of crime.

## 1. Introduction

Indonesia processes thousands of corruption cases annually, yet systematic knowledge about what these cases *look like* — who the perpetrators are, what methods they use, how much they steal, and whether the justice system responds differently to different types — remains surprisingly limited. Indonesia Corruption Watch (ICW, 2025) provides annual summaries based on manual review, and occasional qualitative studies examine specific cases (Butt, 2011). But no study has computationally analyzed the *content* of corruption verdicts at scale to map the corruption ecosystem.

This gap matters because corruption is not monolithic. A village head who diverts Rp 400 million in village development funds operates in a fundamentally different context from a minister who receives Rp 40 billion in gratification. The legal framework may be the same (Law No. 31/1999), but the scale, method, institutional context, and social harm differ by orders of magnitude. If the justice system treats these cases identically — or worse, treats small-scale corruption more harshly — this has profound implications for both deterrence and distributive justice.

We address this gap by extracting structured corruption profiles from 367 Indonesian Supreme Court (*Mahkamah Agung*) corruption verdicts. Using regex-based feature extraction on judicial reasoning texts, we identify actor types (who corrupts), methods (how they corrupt), and linguistic patterns (how judges describe corruption). We then test whether different corruption types receive different treatment from the justice system.

Our central finding is a **village penalty**: corruption cases involving village-level actors and funds receive disproportionately harsh punishment relative to the harm caused, while elite corruption involving gratification and money laundering receives relatively lenient treatment per unit of state loss. This finding complements our companion study documenting broken proportionality in prosecution demands (Author, 2026d), showing that the regressive pattern operates across both prosecutorial and judicial stages.

### Research Questions

- **RQ1:** What are the dominant corruption methods and actor types in Indonesian Supreme Court verdicts?
- **RQ2:** Do different corruption types receive different treatment from the justice system?
- **RQ3:** How do judges linguistically characterize corruption — through moral or technical language?

## 2. Background

### 2.1 Corruption Typology

Corruption studies have long recognized heterogeneity in corruption types. Heidenheimer's (1970) distinction between "petty" and "grand" corruption, while simplistic, captures a fundamental dimension: scale. More sophisticated typologies incorporate the method (bribery, embezzlement, procurement fraud), the sector (public, SOE, legislative), and the institutional context (centralized vs decentralized) (Lambsdorff, 2007).

In Indonesia, the institutional landscape of corruption has shifted dramatically since decentralization in 2001. The transfer of authority and budgets to over 500 district governments (*kabupaten/kota*) created new corruption opportunities at the local level (Lewis, 2017). Village funds (*dana desa*), introduced in 2015 with annual allocations exceeding Rp 70 trillion nationally, created a further layer of vulnerability at the village level. ICW (2025) reports that village heads (*kepala desa*) are now among the most frequently prosecuted corruption actors.

### 2.2 Procurement Fraud

Public procurement is widely recognized as the government activity most vulnerable to corruption (OECD, 2016). In Indonesia, procurement reform has been a priority since the establishment of LKPP (National Public Procurement Agency) and the introduction of electronic procurement (*e-procurement*). Nevertheless, procurement fraud — particularly fictitious procurement (*pengadaan fiktif*), where goods or services are paid for but never delivered — remains a persistent problem.

### 2.3 Sentencing Disparities Across Crime Types

Differential treatment of crime types within the same legal category raises questions about justice and proportionality. If the punishment per unit of harm varies systematically across corruption subtypes, this may reflect legitimate distinctions in culpability or illegitimate disparities in prosecutorial and judicial attention. Distinguishing between these requires quantitative evidence.

### 2.4 Judicial Language and Normalization

The sociology of law has long recognized that legal language shapes perceptions of crime (Garfinkel, 1956). When judges describe corruption using technical-neutral language ("misuse of authority") rather than moral-evaluative language ("theft from the public"), the language itself may normalize the offense. This hypothesis — which we term *linguistic normalization* — has not been tested computationally on corruption verdicts.

## 3. Data and Methods

### 3.1 Corpus

CorpusKorupsi (Author, 2026a) comprises 367 analysis-ready Supreme Court corruption verdicts with full judicial reasoning text (*pertimbangan hakim*). Texts range from 1,033 to 476,164 characters (median 10,877).

### 3.2 Feature Extraction

We extract three categories of features using regex patterns on lowercased pertimbangan text:

**Actor types** (8 categories): kepala daerah (bupati/walikota/gubernur), kepala dinas, BUMN/BUMD, DPRD members, village actors (kepala desa/perangkat desa), PNS/ASN, police, education sector.

**Methods** (8 categories): fictitious procurement (*pengadaan fiktif*), price mark-up, gratification/bribery, APBD manipulation, village fund diversion, infrastructure project fraud, money laundering, embezzlement.

**Language** (2 indices): moral language count (8 patterns including "tercela," "serakah," "merugikan rakyat") and technical language count (5 patterns including "terbukti secara sah," "melawan hukum").

### 3.3 Clustering

We identify corruption types using K-means clustering on the 16 binary actor and method features, with optimal k selected by silhouette score.

### 3.4 Differential Treatment

We test whether corruption types differ in prosecution demands, sentences, and sentencing discount using Kruskal-Wallis tests. We quantify the "punishment per billion" as a proportionality measure: years of imprisonment per Rp 1 billion in state financial loss.

## 4. Results

### 4.1 The Corruption Landscape (RQ1)

**Dominant method: Fictitious procurement (33%).** One-third of all Supreme Court corruption verdicts involve goods or services that were paid for but never delivered. This single method accounts for more cases than gratification (9.5%), mark-up (5.7%), and money laundering (4.1%) combined.

**Actor landscape spans all institutional levels:**

| Actor Type | Prevalence | Typical Method |
|-----------|-----------|---------------|
| Village (desa/lurah) | 26.4% | Dana desa, pengadaan fiktif |
| BUMN/BUMD | 21.3% | Various |
| Kepala daerah | 18.8% | APBD, gratifikasi |
| PNS/ASN | 14.4% | Various |
| Kepala dinas | 10.6% | Pengadaan, APBD |
| Education sector | 9.5% | Dana BOS, pengadaan |
| Police | 5.7% | Gratifikasi |
| DPRD members | 3.8% | APBD |

Village-level corruption (26.4%) is the single largest actor category — more prevalent than BUMN corruption (21.3%) or regional head corruption (18.8%).

### 4.2 The Village Penalty (RQ2)

Village corruption cases (n=43) are treated more harshly per unit of harm than elite corruption cases (n=36, defined as gratification, bribery, or money laundering cases):

| Metric | Village (n=43) | Elite (n=36) | p |
|--------|---------------|-------------|---|
| Median kerugian | Rp 446 million | Rp 4.59 billion | — |
| Mean tuntutan | 4.64 years | 8.18 years | — |
| Mean vonis | 2.83 years | 6.24 years | — |
| Mean discount | 0.645 | 0.882 | 0.030 |
| **Prison years per billion** | **5.0 years** | **1.1 years** | **0.016** |

Village corruptors serve **4.7 times more prison time per billion rupiah stolen** than elite corruptors. The median village case involves Rp 446 million in state loss (approximately USD 28,000) and receives a sentence of 3 years. The median elite case involves Rp 4.59 billion (USD 287,000) — ten times more — but receives only twice the prison time.

The village penalty operates through two mechanisms. First, prosecutors demand relatively more for village cases per unit of loss (4.64 years for Rp 446 million vs 8.18 years for Rp 4.59 billion). Second, judges apply a lower discount to village cases (0.645 vs 0.882, p=0.030). Both effects compound to produce severely regressive punishment.

After controlling for prosecution demand and state financial loss, the village indicator is marginally significant (b=-0.657, p=0.089), suggesting that the penalty is partially mediated through prosecutorial behavior — consistent with the finding that prosecutorial demand-setting is the upstream source of disproportionality (Author, 2026d).

### 4.3 Four Corruption Types

K-means clustering (k=4, silhouette=0.347) identifies four distinct types:

**Type 0: General corruption (n=298, 81%).** Mixed cases without dominant actor or method pattern. Mean tuntutan 6.6 years, mean vonis 4.7 years.

**Type 1: Gratification-elite (n=36, 10%).** Dominated by gratification (83%), money laundering (39%), police involvement (22%). Highest demands (8.4 years) and sentences (6.3 years). Highest moral language ratio (0.126).

**Type 2: Legislative-APBD (n=14, 4%).** DPRD members (100%), APBD manipulation (57%), regional heads (64%). Moderate demands (5.5 years) but low kerugian (median Rp 100 million).

**Type 3: Village-procurement (n=19, 5%).** Dana desa (100%), village actors (90%), fictitious procurement (58%). Lowest demands (4.8 years) and sentences (3.4 years).

These types differ significantly in prosecution demands (H=11.6, p=0.009) and sentences (H=12.2, p=0.007), but NOT in sentencing discount (H=2.0, p=0.574). **Differential treatment originates with prosecutors, not judges.**

### 4.4 The Silence of Moral Language (RQ3)

Only 8.7% of verdicts contain any moral or evaluative language about the corruption. The dominant register is technical-legal:

| Language Type | Prevalence | Example |
|--------------|-----------|---------|
| "Proven according to law" | 34.1% | *terbukti secara sah* |
| "Against the law" | 33.3% | *melawan hukum* |
| "Misuse of authority" | 14.8% | *menyalahgunakan wewenang* |
| "Self-enrichment" | 17.5% | *memperkaya diri* |
| **"Reprehensible"** | **3.6%** | *tercela* |
| **"Harming the people"** | **2.9%** | *merugikan rakyat/masyarakat* |
| **"Greedy"** | **1.5%** | *serakah/tamak* |

Moral language does not independently predict sentence severity (b=0.032, p=0.889 in OLS controlling for prosecution demand). When judges do use moral language, it does not translate into harsher outcomes — it is decorative rather than operative.

This finding supports the linguistic normalization hypothesis: the language of corruption adjudication in Indonesia systematically strips moral content from criminal acts involving billions in stolen public funds, treating corruption with the same sterile bureaucratic register as minor regulatory violations.

## 5. Discussion

### 5.1 The Regressive Structure of Corruption Justice

Our findings reveal a justice system that is regressive across multiple dimensions. The village penalty — 4.7x more prison time per billion stolen — compounds the broken proportionality documented in Author (2026d). Together, these findings paint a coherent picture: the Indonesian corruption justice system punishes the least powerful offenders most severely per unit of harm, while providing an implicit "volume discount" for large-scale elite corruption.

This regressivity has two possible interpretations. The *structural* interpretation holds that village cases are simpler, with clear evidence and unambiguous losses, making prosecution and conviction easier. Elite cases are more complex, with contested loss quantification and sophisticated legal defenses, leading to lower effective punishment. The *political* interpretation holds that the justice system reflects power asymmetries: village heads lack the political connections and legal resources to negotiate lighter treatment.

Both interpretations are consistent with our data; disentangling them requires information about case processing that verdict data alone cannot provide.

### 5.2 Procurement as Systemic Vulnerability

The finding that 33% of corruption cases involve fictitious procurement — making it the single most common corruption method — has direct policy implications. Despite more than a decade of procurement reform (e-procurement, LKPP oversight, transparency requirements), fictitious procurement remains the dominant mode of corruption in judicial data.

This suggests either that existing procurement controls are insufficient, that they have displaced corruption to harder-to-detect methods, or that the cases reaching the Supreme Court are disproportionately procurement-related. The first interpretation supports accelerated procurement reform; the latter two suggest selection effects that warrant further investigation.

### 5.3 The Language of Normalization

That 91.3% of corruption verdicts contain no moral language is itself a finding about institutional culture. Judges adjudicating cases involving the theft of public funds — funds intended for schools, roads, hospitals, and village development — describe these acts using the same dispassionate register they might use for commercial disputes.

We do not claim that judges *should* use emotional language. Legal precision has value. But the near-total absence of moral framing in corruption verdicts, combined with the finding that the rare moral language has no effect on outcomes (p=0.889), suggests that the judicial institution has normalized corruption to the point where it is processed as a routine administrative matter rather than a moral offense against the public.

### 5.4 Limitations

**Regex-based extraction.** Our feature extraction uses regex patterns, which capture surface-level text patterns but may miss nuanced references. More sophisticated NLP approaches (named entity recognition, semantic role labeling) could improve extraction quality.

**Supreme Court selection.** Our corpus consists of cassation decisions, which are a selected subset of all corruption cases. Village cases may be over-represented in appeals if conviction rates differ by type.

**Corpus size.** With n=367, subgroup analyses (particularly for Types 2 and 3) have limited statistical power.

**Missing variables.** Defendant characteristics (age, education, prior record), case processing variables (time from arrest to verdict, number of hearings), and political context are not captured.

## 6. Conclusion

We provide the first computational typology of Indonesian corruption from Supreme Court verdicts. Three findings stand out. First, fictitious procurement is the dominant corruption method (33%), highlighting a systemic vulnerability in public procurement. Second, the village penalty — 4.7x more prison time per billion stolen compared to elite corruption — reveals a regressive justice system where the least powerful offenders are punished most severely per unit of harm. Third, moral language is nearly absent from judicial reasoning (91.3% of verdicts), suggesting institutional normalization of corruption.

These findings shift the conversation from "how judges sentence corruption" to "what corruption looks like and whether the system responds justly across types." The answer, for now, is that it does not: the Indonesian corruption justice system, as reflected in Supreme Court verdicts, punishes petty village corruption with disproportionate severity while processing the theft of billions through the sterile language of bureaucratic routine.

## Declarations

**Funding.** This research received no external funding.
**Conflicts of interest.** The author declares no conflicts of interest.
**Ethics approval.** This study analyzes publicly available court documents. No human subjects were involved.
**Data availability.** The CorpusKorupsi dataset and analysis scripts are available at [repository URL].
**Use of AI-assisted tools.** The author used Claude (Anthropic) as a computational research assistant. All analyses were independently verified through reproducible scripts.

## References

Author (2026a). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts. [Companion paper]

Author (2026d). Broken Proportionality: Prosecutorial Demands and State Financial Loss in Indonesian Corruption Cases. [Companion paper]

Butt, S. (2011). Anti-corruption reform in Indonesia: An obituary? *Bulletin of Indonesian Economic Studies*, 47(3), 381-394.

Garfinkel, H. (1956). Conditions of successful degradation ceremonies. *American Journal of Sociology*, 61(5), 420-424.

Heidenheimer, A. J. (1970). *Political Corruption: Readings in Comparative Analysis*. Holt, Rinehart and Winston.

Indonesia Corruption Watch (2025). Sentencing trend monitoring report 2024. Jakarta: ICW.

Lambsdorff, J. G. (2007). *The Institutional Economics of Corruption and Reform*. Cambridge University Press.

Lewis, B. (2017). Does local government proliferation improve public service delivery? *Journal of Urban Economics*, 97, 1-18.

OECD (2016). *Preventing Corruption in Public Procurement*. OECD Publishing.
