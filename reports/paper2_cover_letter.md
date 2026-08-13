# Cover Letter — Artificial Intelligence and Law (Springer)

Dear Editor,

We submit for your consideration our manuscript entitled **"Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences"** for publication in *Artificial Intelligence and Law*.

This study presents the first large-scale computational analysis of Indonesian corruption sentencing, using a corpus of 693 Supreme Court verdicts (374 analysis-ready). We report three principal findings:

1. **Charge type is independently associated with sentencing severity.** After controlling for prosecution demand, cases classified under Pasal 2 (enrichment) of Indonesia's Anti-Corruption Law receive sentences 0.82 years longer than equivalent Pasal 3 (authority abuse) cases (b=0.818, p<0.001, Cohen's d=0.74). This association is temporally stable (pre-2024 and post-2024, interaction p=0.88) and is detected through text analysis of judicial reasoning rather than structured case metadata — demonstrating that unstructured reasoning text carries sentencing-relevant information that formal case classifications miss.

2. **The sentencing discount is opaque from public documents.** The ratio of sentence to prosecution demand (mean 0.80) cannot be predicted from any available feature (cross-validated R2=-0.03), suggesting that approximately 40% of sentencing variance reflects factors not recoverable from published verdicts.

3. **Text mining approaches systematically fail** to improve sentencing prediction at this corpus size, a negative result documented across 30+ experiments with TF-IDF, transformer embeddings, and domain-specific features. This calibrates expectations for computational legal analysis in data-scarce settings.

We believe this manuscript fits well within the scope of *Artificial Intelligence and Law*: it applies rigorous computational methods to a novel Southeast Asian legal dataset, addresses the interpretability limits of NLP on small legal corpora, and has direct policy implications for judicial transparency and sentencing consistency monitoring.

**Related work disclosure:** The author has a companion manuscript, *"Broken Proportionality: Prosecutorial Demands and State Financial Loss in Indonesian Corruption Cases"* (currently under review at Asian Journal of Criminology), which analyzes prosecutorial demand elasticity using the same corpus. The present manuscript is methodologically and substantively distinct: it examines charge-type effects and the predictability of the sentencing discount (judicial opacity), rather than prosecutorial demand proportionality. Both papers are cross-disclosed.

The manuscript has not been submitted elsewhere. Code and data are available for reproducibility. A preprint version has been posted on SSRN (Abstract ID: 6574140).

In accordance with Springer Nature's policy on AI-assisted tools, I disclose that Claude (Anthropic) was used as a computational research assistant for programming, literature search, and manuscript drafting. All analyses were independently verified through reproducible scripts, and I take full responsibility for all scientific claims and interpretations. Full details are provided in the Declarations section of the manuscript.

Sincerely,
Mukhlis Amien
Department of Informatics, Universitas Bhinneka Nusantara, Malang, Indonesia
Email: amien@ubhinus.ac.id
ORCID: 0000-0002-1848-167X
