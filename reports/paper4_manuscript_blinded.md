# Broken Proportionality: Prosecutorial Demands and State Financial Loss in Indonesian Corruption Cases

## Abstract

Does the punishment fit the crime in corruption cases? We estimate the elasticity of prosecution demands (*tuntutan*) with respect to state financial loss (*kerugian negara*) using 262 Indonesian Supreme Court corruption verdicts. The elasticity is 0.124 (bootstrap 95% CI [0.102, 0.150]): a 100-fold increase in state loss produces only a 1.8-fold increase in the prosecution demand. A Rp 10 million case draws a demand of 2.7 years; a Rp 100 billion case — ten thousand times the harm — draws only 8.6 years. Because punishment operates on a bounded scale while loss spans orders of magnitude, *some* compression is mathematically inevitable; the right benchmark is therefore comparative. Indonesia's elasticity is about 43% of the loss-severity gradient US federal courts actually deliver in practice (realized elasticity ≈0.29, computed from US Sentencing Commission outcome data; the guideline table itself implies 0.25–0.35) and is reached with no guidelines at all — loss explains about 30% of demand variation (R²=0.300). Under identical case-fact specifications, sentences are in fact somewhat *more* predictable than demands (R²=0.50 vs 0.40) while still tracking the demand closely (R²=0.64): discretion enters the system once, at the demand stage, and judges partially correct toward case facts rather than purely transmitting it — the sentence-loss elasticity (0.145) modestly exceeds, and is statistically indistinguishable from, the demand-loss elasticity (0.124). Demands have risen over time (from roughly 4.5 years in 2014–2015 to 7.5 years in 2025–2026), and the sentencing discount has widened modestly over the same period. A residual geographic signal persists even after controlling for case magnitude. The compressed elasticity means the marginal expected punishment for escalating corruption is negligible — the system grants an implicit volume discount on large-scale theft. Because the proportionality failure originates upstream in prosecutorial discretion, reform aimed only at judges would leave the binding constraint largely untouched.

## 1. Introduction

Punishment should fit the crime. In corruption cases, "the crime" has a clear metric: the state financial loss (*kerugian negara*). A prosecutor deciding how many years to demand for a defendant who stole Rp 10 million faces a qualitatively different case from one involving Rp 100 billion. The question is whether prosecutors actually treat them differently — and if so, by how much.

Sentencing research overwhelmingly studies judges, treating prosecution demands as a given (Author, 2026b; Medvedeva et al., 2020; Strickson & De La Iglesia, 2020). This is a blind spot. Prosecution demands set the anchor from which judges work: in Indonesian corruption cases, prosecution demand alone explains about 64% of sentencing variance (Author, 2026b). If the anchor itself is not proportional to the crime, judicial proportionality is impossible regardless of how carefully judges deliberate.

We test proportionality directly. Using 262 Indonesian Supreme Court corruption verdicts with documented state losses spanning seven orders of magnitude, we estimate the elasticity of prosecution demand with respect to kerugian negara. Indonesia is a useful setting because prosecutors operate without sentencing guidelines and the statutory range (1-20 years) is wide enough to accommodate the graduation observed in comparable systems.

The elasticity is 0.124. A Rp 100 billion case — ten thousand times the harm of a Rp 10 million case — draws a prosecution demand only 3.1 times longer. Some compression is unavoidable because punishment is bounded while loss is not; but as we show through comparison with the explicitly loss-graduated US sentencing system, Indonesia's compression is roughly twice as severe and entirely unstructured. The consequences run in several directions: small-scale corruption is punished harshly per rupiah stolen, mega-corruption receives an implicit volume discount, and the marginal cost of escalating corruption is close to zero. The problem sits upstream of the judge, in prosecutorial discretion — which means judicial reform alone cannot fix it.

### Research Questions

- **RQ1:** Is prosecutorial demand proportional to state financial loss? What is the elasticity of demand with respect to loss magnitude?
- **RQ2:** What explains variation in prosecution demands beyond state financial loss? How predictable are prosecution demands from available case features?
- **RQ3:** Are there temporal or geographic patterns in prosecutorial severity?

## 2. Theoretical Framework

### 2.1 The Proportionality Principle

The proportionality principle — that punishment severity should reflect crime severity — is a foundational concept in sentencing theory (von Hirsch, 1992; Ashworth, 2015). In corruption cases, state financial loss provides an unusually clear measure of harm: unlike violent crimes where severity is multi-dimensional, the economic damage from corruption is quantifiable in monetary terms. If any offense type should exhibit proportional punishment, it is corruption.

What benchmark should we hold prosecutorial demands to? A naive standard would be an elasticity of 1.0 — a tenfold increase in loss yielding a tenfold increase in demand. But this is the wrong benchmark, and we reject it explicitly. Punishment operates on a bounded scale (the statutory range is 1–20 years; in practice almost all demands fall between 2 and 12 years), while corruption losses in our data span more than seven orders of magnitude. No bounded punishment scale can be log-proportional (elasticity 1.0) across such a range; substantial compression is a mathematical necessity, not a policy failure. An elasticity well below 1.0 is therefore expected in *any* sentencing system.

The meaningful question is comparative: how steeply do systems that *deliberately* tie punishment to loss actually graduate it, and where does Indonesia fall relative to that? The paradigm case is the US Federal Sentencing Guidelines §2B1.1, whose 16-tier "loss table" explicitly maps state/victim loss to offense-level increases (United States Sentencing Commission, 2024). The table's structure implies an elasticity on the order of 0.25–0.35: across the table, an approximately 3,800-fold increase in loss raises the offense level by about 20 levels, corresponding to roughly a tenfold increase in sentence length.

A natural objection is that the table overstates what US courts actually deliver, since below-guideline sentences are the norm in high-loss fraud cases (Hewitt, 2016). We therefore benchmark against *realized* practice, not the table. Using the US Sentencing Commission's cross-tabulation of average imposed sentence by loss category for §2B1.1 offenders (FY2012, N=8,507; United States Sentencing Commission, 2013; reproduced in Bennett, Levinson & Hioki, 2017), a weighted log-log regression of average sentence on loss-bracket midpoint yields a realized elasticity of **0.288** (robust to weighting and midpoint conventions: 0.27–0.33; R²=0.98), compared with 0.35 for the guideline minimum in the same cells. Pervasive below-range sentencing compresses sentence *levels* — the sentence-to-guideline ratio falls from 1.25 in the smallest bracket to roughly 0.5–0.75 in the largest — but because that compression is spread over six orders of magnitude of loss, it flattens the log-log *slope* only modestly. Two caveats: the cross-tabulation predates the 2015 table revision, though FY2024 aggregate sentence-to-guideline ratios are essentially unchanged (0.71 vs 0.76); and above roughly USD 20 million the realized curve genuinely flattens (arc elasticity ≈0.18 in the extreme tail, resting on 14 offenders), so a comparison restricted to grand-corruption-scale losses alone would narrow the gap.

The US system is itself under active reform: in December 2025 the Sentencing Commission proposed collapsing the 16-tier table to 8 tiers precisely because of concerns that it over-weights loss (United States Sentencing Commission, 2025). The US thus represents a high-water mark of loss-based graduation — and even it is being pulled back. Against realized US practice, an Indonesian elasticity of 0.124 is about 43% of the loss-severity gradient the US system actually delivers, achieved with no guidelines whatsoever: compression at an extreme of the observed range, reached not by design but as an emergent property of unstructured discretion.

### 2.2 Deterrence and Marginal Cost

Economic deterrence theory (Becker, 1968) models criminal behavior as a rational choice: individuals commit crimes when the expected benefit exceeds the expected cost (probability of detection multiplied by punishment severity). For deterrence to function, the expected punishment must increase with the scale of the offense.

If prosecution demands are inelastic to state loss, the marginal expected punishment for additional corruption is near zero. A corrupt official deciding between diverting Rp 10 million and Rp 100 billion faces essentially the same prosecutorial demand — rendering the cost-benefit calculus heavily favorable toward larger-scale corruption. This creates a perverse incentive structure: the system punishes petty corruption relatively harshly while offering implicit leniency for mega-corruption.

### 2.3 Prosecutorial Anchoring

The anchoring literature (Tversky & Kahneman, 1974; Englich et al., 2006) suggests that decision-makers anchor to reference points and adjust insufficiently. Prosecutors may be anchored to a "normal" corruption demand range — an internalized sense of what constitutes an appropriate demand for corruption cases — and adjust minimally for case-specific factors including loss magnitude.

In a companion study (Author, 2026c), we documented bidirectional anchoring correction in judicial sentencing: judges pull extreme prosecution demands toward an implicit norm. The present study tests whether a parallel phenomenon exists on the prosecutorial side: do prosecutors compress their demands toward a central range regardless of case severity?

### 2.4 Prosecutorial Discretion

Prosecutors exercise enormous discretion in determining sentencing demands, yet this discretion receives far less scholarly attention than judicial discretion (Davis, 1969; Vorenberg, 1981). In Indonesia, no formal sentencing guidelines constrain prosecutorial demands. The Anti-Corruption Law (No. 31/1999 as amended by No. 20/2001) specifies statutory ranges — Pasal 2 (enrichment): 4-20 years; Pasal 3 (authority abuse): 1-20 years — but provides no formula linking loss magnitude to demand severity. This unstructured discretion creates the conditions for disproportionate outcomes.

## 3. Data and Methods

### 3.1 Corpus

We use CorpusKorupsi (Author, 2026a), a structured dataset of Indonesian Supreme Court corruption verdicts. Of 693 scraped verdicts, 465 are confirmed corruption (tipikor) cases by document-text audit rather than directory label (the scraping directory is global and admits non-corruption matters; we verify each verdict's substantive category). Of these, 265 carry a valid prosecution demand (*tuntutan* > 0), a final sentence (*vonis* > 0), and a documented state financial loss (*kerugian negara* > 0). Three carry an implausible loss below Rp 1 juta (almost certainly extraction errors, the smallest plausible value being Rp 2.2 juta); we drop them, yielding **n=262** for the primary estimate. Losses then range from Rp 2.2 juta to Rp 28.9 trillion (median Rp 2.1 billion), spanning over seven orders of magnitude.

**The mega-case (PT Timah).** The largest value in the data is the PT Timah tin-mining case, which appears three times because its case-level loss is attributed identically to three co-defendants. The case illustrates why loss quantification in corruption is contested. The BPKP audit cited a total figure of approximately Rp 300 trillion, but roughly Rp 271 trillion of that is environmental damage that the Supreme Court, on cassation, explicitly held *not* to be state financial loss under the corruption-crime regime; the Court fixed the criminal basis at **Rp 28.9 trillion** of state financial loss. We use Rp 28.9 trillion for the `kerugian_keuangan_negara` variable, because our estimand is the fiscal loss to which the corruption statute attaches. We retain the Rp 300 trillion figure as an alternative specification in a robustness check (Section 4.1). Because the three co-defendant rows are non-independent, we also de-duplicate them in a robustness check; with the corrected 28.9-trillion value this de-duplication barely moves the estimate (elasticity 0.124 → 0.125), confirming the headline does not rest on mega-case leverage.

**Extraction validation.** The three variables that anchor every result — *tuntutan*, *vonis*, and *kerugian negara* — are extracted from verdict text by a regex pipeline. We validated it on a stratified, blind holdout of 50 cases drawn from cases never used to develop the parser (pre-registered criterion and stopping rule fixed before sampling). Adjudicated accuracy against the source PDFs is 98.0% for *tuntutan*, 98.0% for *vonis*, and 91.7% for *kerugian* (Wilson 95% CI 80.4–96.7%, after excluding two genuinely ambiguous cases); region and year are 100%. We are therefore confident the corpus is at least as accurate as these figures. We report this honestly: the instrument was measured at one parser version, and a small number of extraction errors found subsequently were corrected, so the released corpus is no less accurate than the reported rates; we do not claim the parser is error-free.

### 3.2 Variables

| Variable | Description | n | Coverage |
|----------|-------------|---|----------|
| tuntutan_years | Prosecution demand (years) | 262 | 100% |
| kerugian_negara | State financial loss (IDR) | 262 | 100% |
| vonis_years | Sentence (years) | 262 | 100% |
| has_pasal_2 | Pasal 2 in judicial reasoning | 262 | 100% |
| has_pasal_3 | Pasal 3 in judicial reasoning | 262 | 100% |
| tahun | Year of MA decision | 262 | 100% |
| daerah | Court region | 262 | 100% |
| discount | vonis / tuntutan ratio | 262 | 100% |

### 3.3 Statistical Methods

**Proportionality test (RQ1).** We estimate the elasticity of prosecution demand with respect to state financial loss using a log-log regression: log(tuntutan) = a + b * log(kerugian). Under proportionality, b = 1.0. We test whether the estimated elasticity is significantly less than 1.0.

**Demand predictability (RQ2).** We model prosecution demand using OLS regression with state financial loss, charge type (Pasal 2, Pasal 3), and year as predictors. We compare the R-squared with the demand-sentence relationship (R-squared = 0.64 from Author, 2026b) to assess relative predictability.

**Temporal and geographic patterns (RQ3).** Temporal trends are assessed using Spearman rank correlation. Geographic variation is tested using Kruskal-Wallis on both raw and residual (controlling for loss magnitude) demands.

## 4. Results

### 4.1 Prosecution Demands Are Highly Inelastic to State Loss (RQ1)

The log-log elasticity of prosecution demand with respect to state financial loss is **0.124** (bootstrap 95% CI [0.102, 0.150], p<0.001, R²=0.300) on the cleaned sample (n=262). The entire confidence interval lies below both the elasticity implied by the US loss table (0.25–0.35) and the realized elasticity of US sentencing practice (≈0.29; Section 2.1) — even our upper bound (0.150) reaches barely half the gradient the US system actually delivers. Prosecution demands respond only weakly to the magnitude of harm.

In practical terms:

| State financial loss | Predicted demand | Ratio to baseline |
|---------------------|-----------------|-------------------|
| Rp 10 million | 2.7 years | 1.0x (baseline) |
| Rp 100 million | 3.6 years | 1.3x |
| Rp 1 billion | 4.8 years | 1.8x |
| Rp 10 billion | 6.4 years | 2.4x |
| Rp 100 billion | 8.6 years | 3.1x |

A Rp 100 billion corruption case — involving state loss 10,000 times greater than a Rp 10 million case — receives a prosecution demand only 3.1 times higher. Each additional order of magnitude of loss multiplies the demand by only about 1.33 (a 33% increase per tenfold rise in harm).

**Robustness.** The estimate is stable across data-cleaning choices, and the uncleaned tail points were deflating rather than inflating it:

| Specification | n | Elasticity | R² |
|---|---|---|---|
| Full (uncleaned, is_tipikor) | 265 | 0.092 | 0.198 |
| Drop parsing error (<Rp 1 juta) — *primary* | 262 | 0.124 | 0.300 |
| + de-duplicate mega-case co-defendants | 260 | 0.125 | 0.286 |
| Winsorized at 1st–99th percentile | 262 | 0.127 | 0.301 |

The low elasticity is also not an artifact of statutory constraints. The statutory maximum (20 years) binds only the very largest cases, and the statutory minimum for Pasal 2 (4 years) works *against* our finding: it forces small-case demands upward, inflating the apparent elasticity. Excluding cases with demands below 4 years (n=212) drops the elasticity further to 0.092 — compression is even more severe without the statutory floor. Controlling for whether the verdict mentions restitution (*pengembalian kerugian*, present in 32% of cases) does not change the elasticity. Substituting the PT Timah Rp 300 trillion audit figure for the Rp 28.9 trillion state-financial-loss value (Section 3.1) leaves the elasticity essentially unchanged, confirming the result does not hinge on the mega-case valuation.

### 4.2 Discretion Enters Upstream: Judges Partially Correct Toward Case Facts (RQ2)

How predictable are prosecution demands from observable case features — and, critically, how does that compare with sentences *under the same specification*? Comparing the demand model against the sentence-from-demand benchmark alone would be misleading: the 64% of sentencing variance explained by the demand (Author, 2026b) measures how faithfully judges follow a procedural anchor, not how tightly sentences track case facts. The fair comparison holds the predictor set constant (cleaned sample, n=262):

| Model (identical predictors where comparable) | R-squared |
|-------|-----------|
| tuntutan ~ log(kerugian) + Pasal 2 + Pasal 3 + year | 0.405 |
| vonis ~ log(kerugian) + Pasal 2 + Pasal 3 + year | 0.498 |
| vonis ~ tuntutan (anchor model; Author, 2026b) | 0.642 |

Conditional on observable case facts, sentences are *more* predictable than demands (R-squared 0.498 vs 0.405), not equally so. Conditional on the demand, sentences are highly predictable (R-squared 0.642). The pattern admits one coherent reading: **discretion enters the system once — at the demand stage — but judges do not merely transmit it**. They pull sentences modestly toward case facts, leaving sentences somewhat better tethered to the record than the demands they anchor to. This is partial correction, not pure propagation, and it is consistent with the bidirectional anchoring correction documented for judges in companion work (Author, 2026c). The same direction appears in the elasticities: the sentence-loss elasticity (0.145, SE 0.011) modestly exceeds the demand-loss elasticity (0.124, SE 0.012) — judges weight loss slightly more than prosecutors do — though the two are not statistically distinguishable. The proportionality failure documented in Section 4.1 therefore passes through judicial sentencing *damped* rather than amplified: judges blunt it, but they do not close it.

Within the demand model, charge type contributes modestly: Pasal 2 cases receive demands about 0.9 years higher (p=0.062), Pasal 3 cases about 0.5 years lower (p=0.295), and year adds borderline explanatory power (b=+0.11, p=0.085). Loss magnitude, even where significant, leaves the majority of demand variation unexplained.

### 4.3 Temporal Increase in Prosecutorial Severity (RQ3)

Prosecution demands have increased significantly over the observation period (Spearman rho=0.228, p<0.001 at the case level), from approximately 4.5 years in 2014-2015 to approximately 7.5 years in 2025-2026. Over the same period the sentencing discount (vonis/tuntutan) has widened modestly (Spearman rho=−0.143, p=0.021): sentences have not fully kept pace with the rising demands, so the typical gap between demand and sentence has grown rather than holding steady.

One reading: as anti-corruption rhetoric has intensified, prosecutors have raised their demands — and judges have let the discount widen rather than fully absorbing the increase, so actual sentences have risen more slowly still.

### 4.4 Geographic Variation Is a Composition Effect

Raw prosecution demands vary significantly across provinces (Kruskal-Wallis H=57.2, p<0.001 among the 15 provinces with at least five cases). After controlling for state financial loss, most of this variation is absorbed, but a residual geographic signal persists (H=24.8, p=0.036): regions are not interchangeable, though case magnitude explains the bulk of the raw differences. Regions with higher average demands (DKI Jakarta, Sumatera Selatan) handle larger-magnitude cases; what remains after controlling for magnitude is comparatively small.

The same largely-compositional pattern appears in judicial sentencing (Author, 2026b): most of what looks like regional disparity is case mix rather than systematically harsher or softer local prosecutors.

## 5. Discussion

### 5.1 Why Proportionality Fails

An obvious objection is that state financial loss is only one dimension of crime severity. Prosecutors legitimately consider the defendant's position, cooperation, modus operandi, and restitution when calibrating demands. A low elasticity with respect to kerugian alone does not necessarily indicate broken proportionality if other factors compensate. We address this in two ways. First, controlling for the available multi-dimensional indicators — charge type (Pasal 2 vs 3), restitution mentions, and region — does not change the elasticity. Second, even granting that severity is multi-dimensional, an elasticity of 0.124 is extreme relative to the comparative benchmark: it implies that a case involving ten thousand times more public harm receives only about three times the punishment demand, roughly half the graduation built into the US loss table. No plausible weighting of non-monetary severity factors can close a gap this large — and such factors would have to be *systematically anticorrelated* with loss to do so.

Three mechanisms may explain the compression:

**Anchoring to norms.** Prosecutors may anchor to an implicit "normal" corruption demand — approximately 5-8 years — and adjust insufficiently for case severity. This parallels the judicial anchoring documented in companion studies (Author, 2026b, 2026c). The statutory range of 1-20 years is broad enough to accommodate proportional demands, but prosecutors appear to use only a narrow band within this range.

**Evidentiary complexity.** Larger corruption cases typically involve more complex financial structures, making it more difficult to establish the full extent of state loss. Prosecutors may discount their demands to reflect evidentiary uncertainty, even when the documented loss is large.

**Defendant power asymmetry.** Mega-corruption cases typically involve powerful defendants — governors, ministers, directors of state enterprises — who can mount more aggressive legal defenses. Prosecutors may temper their demands in anticipation of more contested proceedings, a form of strategic adjustment documented in other contexts (Bibas, 2004).

### 5.2 Implications for Deterrence

If the expected additional punishment for increasing the scale of corruption from Rp 10 million to Rp 100 billion is only 5.8 years, the marginal cost of additional corruption is approximately Rp 17 billion per year of additional imprisonment. For a rational actor, this makes larger-scale corruption overwhelmingly favorable: the "price" of corruption, measured in prison time per rupiah stolen, decreases by approximately 99.97% as the scale increases from Rp 10 million to Rp 100 billion.

Within a rational-choice framework, this broken proportionality predicts weak deterrence against escalation: once a public official has crossed into corruption, the marginal punishment for increasing the scale is negligible. We do not claim that all corruption is rationally calculated — institutional culture, opportunity structures, and social norms all play roles (Lambsdorff, 2007). But to the extent that punishment signals matter at all, the current signal is perverse: the system imposes a near-flat tariff regardless of scale.

### 5.3 Prosecutorial Discretion as the Upstream Problem

Our finding that discretion enters the system once, at the demand stage (Section 4.2), shifts the focus of the proportionality problem upstream. Sentences are in fact somewhat *better* tethered to case facts than demands are (R-squared 0.498 vs 0.405 under identical specifications); what makes sentences *look* orderly is still their faithful anchoring to the demand (R-squared=0.64). The "judicial opacity" identified in Amien (2026b) is thus partly *inherited* from prosecutorial opacity — judges anchor to demands that are themselves not proportional to case severity — but only partly: by pulling sentences toward the facts, judges absorb some of the demand's noise rather than transmitting it wholesale.

Cross-national comparisons support this interpretation. Our sentence-from-demand R-squared of 0.64 is close to the Dutch sentencing benchmark (van Wingerden et al., 2016, R-squared=0.60 with multiple predictors) and exceeds the majority of 28 sentencing regression studies reviewed by Wittenbrink and Niehaus (2022). The roughly 36% of sentencing variance left unexplained is thus not a distinctively Indonesian phenomenon — it is consistent with judicial discretion levels observed globally.

What IS distinctive is the *degree* of compression at the prosecutorial stage. The demand-loss elasticity of 0.124 is well under half the gradient US federal courts actually deliver (realized elasticity ≈0.29; Section 2.1) — and the US is the most explicitly loss-graduated regime in comparative practice — yet Indonesia reaches this compression with no sentencing or charging guidelines at all. Where the US graduates punishment by loss through a deliberate, contested, and now-reforming 16-tier schedule (United States Sentencing Commission, 2024, 2025), Indonesian prosecutors compress the vast range of corruption severity into a narrow demand band as an unstructured by-product of discretion. That band then propagates through the judicial system — damped but not closed by judges — so a reform aimed only at judges would leave the binding constraint largely untouched.

### 5.4 Policy Implications

**Prosecutorial guidelines.** Formal guidelines linking prosecution demand to state financial loss — similar to US Sentencing Guidelines' loss tables — could restore proportionality. Such guidelines need not eliminate prosecutorial discretion entirely; even a requirement to justify deviations from a proportional baseline would increase transparency.

**Graduated prosecution.** The current flat demand structure could be replaced with a graduated system where demands increase more steeply with loss magnitude. The existing statutory ranges (1-20 years) are sufficient to accommodate proportional demands.

**Transparency.** Requiring prosecutors to document the relationship between their demands and case severity measures would create accountability without constraining discretion. Currently, the demand-setting process is opaque and unstructured.

### 5.5 Limitations

**Selection bias.** Our corpus consists of Supreme Court cassation decisions — appealed cases. The demand-loss elasticity may differ at the district court level, where the full population of corruption cases is processed. If the probability of cassation is itself correlated with both loss magnitude and demand severity (plausible in both directions: prosecutors appeal lenient outcomes, defendants appeal harsh ones), conditioning on cassation can distort the estimated elasticity in a direction that cannot be signed a priori. Replication on first-instance (PN Tipikor) verdicts is the identification fix and is planned as follow-up work. A second selection margin operates within the corpus: the estimation sample comprises only cases with a documented state-loss figure (n=262), which are predominantly embezzlement- and procurement-type cases; bribery and gratification cases typically lack a kerugian figure. In our corpus the documented-loss cases carry only marginally higher sentences than the rest (5.3 vs 4.7 years, Mann-Whitney p=0.053), so the sample is not strongly selected on severity — but the elasticity still characterizes corruption with quantified fiscal harm, not all corruption. A residual domain-classification concern remains: a small number of cases scraped into the corruption directory are substantively other matters (for example a Plantation Law case rather than a corruption offence); these are few and we exclude them where detected, but we cannot guarantee a perfectly clean denominator, and we deliberately did not remove individual cases post hoc from the estimation sample to avoid outcome-dependent manipulation.

**Kerugian negara measurement.** State financial loss figures are extracted from verdict text and may not reflect the actual harm. Loss quantification in corruption cases is contested — BPK, BPKP, and prosecution estimates can differ, and some figures bundle contested components (the PT Timah mega-case: the BPKP audit cited approximately Rp 300 trillion, but roughly Rp 271 trillion of that is environmental damage the Supreme Court excluded from the state-financial-loss basis, on which it fixed Rp 28.9 trillion; we use 28.9 trillion and treat 300 trillion as an alternative specification). Classical measurement error in log-loss would attenuate the estimated elasticity toward zero, so part of the measured compression could in principle be an errors-in-variables artifact. Two considerations bound this concern. First, because documented losses span more than seven orders of magnitude, the variance of true log-loss is large, so the attenuation factor var(true)/var(observed) remains high unless errors are themselves of order-of-magnitude scale: an error standard deviation of 0.5 log10 units (a factor-of-3 misstatement) would attenuate the elasticity by roughly 10%, far too little to explain the gap between 0.124 and any benchmark near 0.25. Second, the robustness checks in Section 4.1 — dropping the most contested mega-case observations — move the estimate *upward*, the opposite of what error-driven compression at the tails would produce. A related extraction concern bears on the demand–sentence predictability gap of Section 4.2: as the extraction pipeline was refined over successive validation rounds, the measured gap between demand and sentence predictability narrowed, indicating that part of the apparent excess unpredictability of demands was extraction noise rather than prosecutorial discretion. The gap does not vanish at the current extraction quality, but its magnitude should be read as sensitive to measurement. Measurement error plausibly shaves both estimates at the margin; it cannot manufacture the central finding.

**Confounders.** Variables not captured in our data — defendant cooperation, plea agreements, strength of evidence, defendant status, case complexity — may explain some of the demand variation we attribute to prosecutorial discretion. However, even if these confounders partially explain the low elasticity, the finding that R²=0.300 for the loss-demand relationship remains consequential: loss magnitude is a weak predictor of prosecution demand regardless of mechanism.

**Tuntutan level.** Our tuntutan variable may refer to the original district court demand or to the prosecution's position at cassation. Two observations suggest it is the original demand. First, the median sentencing discount (vonis/tuntutan = 0.75) implies judges consistently reduce demands by about a quarter — a pattern consistent with PN-level demands being discounted, not with cassation-level demands that would have been adjusted to approximate the expected outcome. Second, in 74% of cases vonis falls below tuntutan, inconsistent with cassation-level demands that would more closely track the eventual sentence. Nevertheless, we cannot rule out that some tuntutan values reflect cassation-stage adjustments, which would compress the demand range and bias our elasticity estimate downward.

## 6. Conclusion

We document a striking failure of proportionality in Indonesian corruption prosecution: the elasticity of prosecution demand with respect to state financial loss is only 0.124, meaning that a 10,000-fold increase in corruption scale produces only a 3.1-fold increase in the prosecution demand. Because punishment is bounded, some compression is inevitable; but Indonesia's elasticity is about 43% of the loss-severity gradient the US system delivers in realized practice (≈0.29) and is achieved without any guideline structure. This inelasticity is not explained by statutory caps or charge type, and only weakly by geography.

The broken proportionality creates a regressive prosecution structure where small-scale corruption is punished disproportionately harshly relative to harm, while mega-corruption receives an implicit "volume discount." This has direct implications for deterrence: the marginal punishment for escalating corruption is negligible, creating a rational-actor incentive to maximize the scale of corrupt acts.

Our findings shift the focus of corruption sentencing reform from judges to prosecutors. Judicial sentencing in Indonesia is well-anchored to prosecution demands (R-squared=0.64, consistent with cross-national benchmarks), and under identical case-fact specifications sentences are in fact somewhat better explained than demands (R-squared 0.498 vs 0.405) — discretion enters the system once, at the demand stage, and is damped but not closed by judges (sentence-loss elasticity 0.145 vs demand-loss elasticity 0.124). Restoring proportionality requires addressing prosecutorial discretion — through guidelines, transparency requirements, or graduated demand structures — not merely reforming judicial sentencing.

The CorpusKorupsi dataset and analysis code are publicly available at [repository URL].

## References

Ashworth, A. (2015). *Sentencing and Criminal Justice* (6th ed.). Cambridge University Press.

Author (2026a). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns. [Companion paper]

Author (2026b). Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences. SSRN Working Paper No. 6574140. https://ssrn.com/abstract=6574140

Author (2026c). Bidirectional Correction: How Indonesian Judges Override Low Prosecution Demands in Corruption Cases. [Companion paper]

Becker, G. S. (1968). Crime and Punishment: An Economic Approach. *Journal of Political Economy*, 76(2), 169-217. https://doi.org/10.1086/259394

Bennett, M. W., Levinson, J. D., & Hioki, K. (2017). Judging Federal White-Collar Fraud Sentencing: An Empirical Study Revealing the Need for Further Reform. *Iowa Law Review*, 102, 939-1000.

Bibas, S. (2004). Plea Bargaining outside the Shadow of Trial. *Harvard Law Review*, 117(8), 2463-2547.

Davis, K. C. (1969). *Discretionary Justice: A Preliminary Inquiry*. Louisiana State University Press.

Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. *Personality and Social Psychology Bulletin*, 32(2), 188-200.

Hewitt, J. (2016). Fifty Shades of Gray: Sentencing Trends in Major White-Collar Cases. *Yale Law Journal*, 125(4), 1018-1071.

Indonesia Corruption Watch (2025). Sentencing trend monitoring report 2024. Jakarta: ICW.

Lambsdorff, J. G. (2007). *The Institutional Economics of Corruption and Reform: Theory, Evidence, and Policy*. Cambridge University Press.

Medvedeva, M., Vols, M., & Wieling, M. (2020). Using machine learning to predict decisions of the European Court of Human Rights. *Artificial Intelligence and Law*, 28(2), 237-266.

Strickson, B., & De La Iglesia, B. (2020). Legal judgement prediction for UK Crown Court criminal cases. *Proceedings of ICAART*, 458-465.

Tversky, A., & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*, 185(4157), 1124-1131. https://doi.org/10.1126/science.185.4157.1124

Ulmer, J. T. (2012). Recent developments and new directions in sentencing research. *Justice Quarterly*, 29(1), 1-40.

United States Sentencing Commission (2013). *Sentencing and Guideline Application Information for §2B1.1 Offenders*. Symposium on Economic Crime. Washington, DC: USSC. https://www.ussc.gov/sites/default/files/pdf/research-and-publications/research-projects-and-surveys/economic-crimes/20130918-19-symposium/Sentencing_Guideline_Application_Info.pdf

United States Sentencing Commission (2024). *Guidelines Manual*, §2B1.1 (Theft, Property Destruction, and Fraud). Washington, DC: USSC.

United States Sentencing Commission (2025). *Proposed Amendments to the Federal Sentencing Guidelines: Economic Crime (§2B1.1 Loss Table)*. Washington, DC: USSC.

van Wingerden, S., van Wilsem, J., & Roosma, F. (2016). Sentencing in the Netherlands: Determinants of severity and judicial consistency. *European Journal of Criminology*, 13(4), 489-512.

von Hirsch, A. (1992). Proportionality in the Philosophy of Punishment. *Crime and Justice*, 16, 55-98. https://doi.org/10.1086/449204

Vorenberg, J. (1981). Decent Restraint of Prosecutorial Power. *Harvard Law Review*, 94(7), 1521-1573.

Wittenbrink, F., & Niehaus, S. (2022). Prediction of Criminal Sentencing: A Systematic Review of Models, Outcomes, and Methodological Issues. *European Journal of Criminology and Police Research*, 28, 349-371.
