# Broken Proportionality: Prosecutorial Demands and State Financial Loss in Indonesian Corruption Cases

## Abstract

Does the punishment fit the crime in corruption cases? We estimate the elasticity of prosecution demands (*tuntutan*) with respect to state financial loss (*kerugian negara*) using 291 Indonesian Supreme Court corruption verdicts. The elasticity is 0.109 (bootstrap 95% CI [0.078, 0.148]): a 100-fold increase in state loss produces only a 1.7-fold increase in the prosecution demand. A Rp 10 million case draws a demand of 3.2 years; a Rp 100 billion case — ten thousand times the harm — draws 8.8 years. Prosecution demands are also less predictable than sentences (R-squared=0.315 vs 0.600), meaning prosecutors exercise wider discretion than judges. Demands have risen over time (from roughly 5 years in 2014 to 7.5 years in 2025) while the sentencing discount has held steady at about 22%. Geographic variation disappears after controlling for case magnitude. The near-zero elasticity means the marginal expected punishment for escalating corruption is negligible — the system implicitly discounts large-scale theft.

## 1. Introduction

Punishment should fit the crime. In corruption cases, "the crime" has a clear metric: the state financial loss (*kerugian negara*). A prosecutor deciding how many years to demand for a defendant who stole Rp 10 million faces a qualitatively different case from one involving Rp 100 billion. The question is whether prosecutors actually treat them differently — and if so, by how much.

Sentencing research overwhelmingly studies judges, treating prosecution demands as a given (Author, 2026b; Medvedeva et al., 2020; Strickson & De La Iglesia, 2020). This is a blind spot. Prosecution demands set the anchor from which judges work: in Indonesian corruption cases, prosecution demand alone explains 60% of sentencing variance (Author, 2026b). If the anchor itself is not proportional to the crime, judicial proportionality is impossible regardless of how carefully judges deliberate.

We test proportionality directly. Using 291 Indonesian Supreme Court corruption verdicts with documented state losses spanning six orders of magnitude, we estimate the elasticity of prosecution demand with respect to kerugian negara. Indonesia is a useful setting because prosecutors operate without sentencing guidelines and the statutory range (1-20 years) is wide enough to accommodate proportional demands.

The elasticity is 0.109. A Rp 100 billion case — ten thousand times the harm of a Rp 10 million case — draws a prosecution demand only 2.7 times longer. The gap between what proportionality requires and what prosecutors actually demand is enormous. The consequences run in several directions: small-scale corruption is punished too harshly per rupiah stolen, mega-corruption is punished too leniently, and the marginal cost of escalating corruption is close to zero. The problem sits upstream of the judge, in prosecutorial discretion — which means judicial reform alone cannot fix it.

### Research Questions

- **RQ1:** Is prosecutorial demand proportional to state financial loss? What is the elasticity of demand with respect to loss magnitude?
- **RQ2:** What explains variation in prosecution demands beyond state financial loss? How predictable are prosecution demands from available case features?
- **RQ3:** Are there temporal or geographic patterns in prosecutorial severity?

## 2. Theoretical Framework

### 2.1 The Proportionality Principle

The proportionality principle — that punishment severity should reflect crime severity — is a foundational concept in sentencing theory (von Hirsch, 1992; Ashworth, 2015). In corruption cases, state financial loss provides an unusually clear measure of harm: unlike violent crimes where severity is multi-dimensional, the economic damage from corruption is quantifiable in monetary terms. If any offense type should exhibit proportional punishment, it is corruption.

Perfect proportionality would imply an elasticity of 1.0: a tenfold increase in state loss yields a tenfold increase in punishment demand. In practice, some compression is expected due to statutory caps, diminishing marginal severity perception, and practical considerations. However, an elasticity near zero would indicate that prosecutors essentially ignore the magnitude of harm when calibrating their demands — a failure of proportionality that has systemic consequences.

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

We use CorpusKorupsi (Author, 2026a), a structured dataset of Indonesian Supreme Court corruption verdicts. From 693 scraped verdicts, 291 have both valid prosecution demands (tuntutan > 0) and documented state financial losses (kerugian negara > 0). State financial losses range from Rp 100 to Rp 300 trillion (median Rp 1.27 billion), spanning over twelve orders of magnitude.

### 3.2 Variables

| Variable | Description | n | Coverage |
|----------|-------------|---|----------|
| tuntutan_years | Prosecution demand (years) | 291 | 100% |
| kerugian_negara | State financial loss (IDR) | 291 | 100% |
| vonis_years | Sentence (years) | 291 | 100% |
| has_pasal_2 | Pasal 2 in judicial reasoning | 291 | 100% |
| has_pasal_3 | Pasal 3 in judicial reasoning | 291 | 100% |
| tahun | Year of MA decision | 291 | 100% |
| daerah | Court region | 291 | 100% |
| discount | vonis / tuntutan ratio | 291 | 100% |

### 3.3 Statistical Methods

**Proportionality test (RQ1).** We estimate the elasticity of prosecution demand with respect to state financial loss using a log-log regression: log(tuntutan) = a + b * log(kerugian). Under proportionality, b = 1.0. We test whether the estimated elasticity is significantly less than 1.0.

**Demand predictability (RQ2).** We model prosecution demand using OLS regression with state financial loss, charge type (Pasal 2, Pasal 3), and year as predictors. We compare the R-squared with the demand-sentence relationship (R-squared = 0.60 from Author, 2026b) to assess relative predictability.

**Temporal and geographic patterns (RQ3).** Temporal trends are assessed using Spearman rank correlation. Geographic variation is tested using Kruskal-Wallis on both raw and residual (controlling for loss magnitude) demands.

## 4. Results

### 4.1 Prosecution Demands Are Highly Inelastic to State Loss (RQ1)

The log-log elasticity of prosecution demand with respect to state financial loss is **0.109** (SE=0.019, p<0.001, R-squared=0.244). This falls far short of proportionality (1.0). Prosecution demands barely respond to the magnitude of harm.

In practical terms:

| State financial loss | Predicted demand | Ratio to baseline |
|---------------------|-----------------|-------------------|
| Rp 10 million | 3.2 years | 1.0x (baseline) |
| Rp 100 million | 3.8 years | 1.2x |
| Rp 1 billion | 5.3 years | 1.7x |
| Rp 10 billion | 6.4 years | 2.0x |
| Rp 100 billion | 8.8 years | 2.7x |

A Rp 100 billion corruption case — involving state loss 10,000 times greater than a Rp 10 million case — receives a prosecution demand only 2.7 times higher. The marginal increase in demand for each additional order of magnitude of loss is approximately 1.7 years.

The low elasticity is not an artifact of statutory constraints. The statutory maximum (20 years) constrains only the very largest cases, and the statutory minimum for Pasal 2 (4 years) actually works *against* our finding: it forces small-case demands upward, inflating the apparent elasticity. When we exclude cases with demands below 4 years (n=244), the elasticity drops further to 0.070 — the compression is even worse without the statutory floor. Controlling for whether the verdict mentions restitution (*pengembalian kerugian*, present in 35% of cases) does not change the elasticity (0.111 vs 0.113 uncontrolled, restitution coefficient p=0.251).

### 4.2 Prosecution Demands Are Less Predictable Than Sentences (RQ2)

A model including state financial loss, charge type, and year explains only **31.5%** of variation in prosecution demands (R-squared=0.315). This is substantially lower than the 60% of sentencing variance explained by prosecution demand alone (Author, 2026b).

| Model | R-squared |
|-------|-----------|
| tuntutan ~ log(kerugian) | 0.297 |
| tuntutan ~ log(kerugian) + Pasal 2 + Pasal 3 | 0.315 |
| tuntutan ~ log(kerugian) + Pasal 2 + Pasal 3 + year | 0.321 |
| vonis ~ tuntutan (Paper 2 benchmark) | 0.600 |

Adding charge type improves the model marginally: Pasal 2 cases receive demands 1.1 years higher than equivalent cases (p=0.019). Pasal 3 is not independently significant (p=0.109). Year adds no significant explanatory power (p=0.113).

Put differently: judges are well-anchored to what prosecutors ask for (R-squared=0.60), but prosecutors themselves are only loosely tethered to the objective severity of the case. The discretion gap lies upstream.

### 4.3 Temporal Increase in Prosecutorial Severity (RQ3)

Prosecution demands have increased significantly over the observation period (Spearman rho=0.773, p=0.005), from approximately 5 years in 2014-2015 to approximately 7.5 years in 2025-2026. However, the sentencing discount (vonis/tuntutan) has not changed (Spearman rho=0.145, p=0.670), indicating that judges absorb the increased demands proportionally rather than resisting the upward trend.

One reading: as anti-corruption rhetoric has intensified, prosecutors have raised their demands — but judges keep cutting by the same fraction, so the actual sentences have risen more slowly than the demands.

### 4.4 Geographic Variation Is a Composition Effect

Raw prosecution demands vary significantly across provinces (Kruskal-Wallis H=40.0, p<0.001). However, after controlling for state financial loss, the geographic variation disappears (H=22.2, p=0.104). Regions with higher average demands (DKI Jakarta, Sumatera Selatan) handle larger-magnitude cases, not systematically harsher prosecutors.

The same result appears in judicial sentencing (Author, 2026b): what looks like regional disparity is really case mix. Prosecutors in different regions are not systematically harsher or softer — they handle different kinds of cases.

## 5. Discussion

### 5.1 Why Proportionality Fails

An obvious objection is that state financial loss is only one dimension of crime severity. Prosecutors legitimately consider the defendant's position, cooperation, modus operandi, and restitution when calibrating demands. A low elasticity with respect to kerugian alone does not necessarily indicate broken proportionality if other factors compensate. We address this in two ways. First, controlling for the available multi-dimensional indicators — charge type (Pasal 2 vs 3), restitution mentions, and region — does not change the elasticity. Second, even granting that severity is multi-dimensional, an elasticity of 0.109 is extreme: it implies that a case involving ten thousand times more public harm receives less than three times the punishment demand. No plausible weighting of non-monetary severity factors can close a gap this large.

Three mechanisms may explain the compression:

**Anchoring to norms.** Prosecutors may anchor to an implicit "normal" corruption demand — approximately 5-8 years — and adjust insufficiently for case severity. This parallels the judicial anchoring documented in companion studies (Author, 2026b, 2026c). The statutory range of 1-20 years is broad enough to accommodate proportional demands, but prosecutors appear to use only a narrow band within this range.

**Evidentiary complexity.** Larger corruption cases typically involve more complex financial structures, making it more difficult to establish the full extent of state loss. Prosecutors may discount their demands to reflect evidentiary uncertainty, even when the documented loss is large.

**Defendant power asymmetry.** Mega-corruption cases typically involve powerful defendants — governors, ministers, directors of state enterprises — who can mount more aggressive legal defenses. Prosecutors may temper their demands in anticipation of more contested proceedings, a form of strategic adjustment documented in other contexts (Bibas, 2004).

### 5.2 Implications for Deterrence

If the expected additional punishment for increasing the scale of corruption from Rp 10 million to Rp 100 billion is only 5.6 years, the marginal cost of additional corruption is approximately Rp 18 billion per year of additional imprisonment. For a rational actor, this makes larger-scale corruption overwhelmingly favorable: the "price" of corruption, measured in prison time per rupiah stolen, decreases by approximately 99.97% as the scale increases from Rp 10 million to Rp 100 billion.

Within a rational-choice framework, this broken proportionality predicts weak deterrence against escalation: once a public official has crossed into corruption, the marginal punishment for increasing the scale is negligible. We do not claim that all corruption is rationally calculated — institutional culture, opportunity structures, and social norms all play roles (Lambsdorff, 2007). But to the extent that punishment signals matter at all, the current signal is perverse: the system imposes a near-flat tariff regardless of scale.

### 5.3 Prosecutorial Discretion as the Upstream Problem

Our finding that prosecution demands are less predictable than sentences (R-squared=0.315 vs 0.600) shifts the focus of the proportionality problem upstream. The "judicial opacity" identified in Author (2026b) — where 40% of sentencing variance is unexplained — may be partially inherited from prosecutorial opacity. Judges are anchored to demands that are themselves not proportional to case severity.

Cross-national comparisons support this interpretation. Our sentence-from-demand R-squared of 0.60 matches the Dutch sentencing benchmark (van Wingerden et al., 2016, R-squared=0.60 with multiple predictors) and exceeds the majority of 28 sentencing regression studies reviewed by Wittenbrink and Niehaus (2022). The approximately 40% unexplained sentencing variance is thus not a distinctively Indonesian phenomenon — it is consistent with judicial discretion levels observed globally.

What IS distinctively Indonesian is the broken proportionality at the prosecutorial stage. The demand-loss elasticity of 0.109 suggests that Indonesian prosecutors have compressed the vast range of corruption severity into a narrow demand band — a compression that then propagates through the anchored judicial system.

### 5.4 Policy Implications

**Prosecutorial guidelines.** Formal guidelines linking prosecution demand to state financial loss — similar to US Sentencing Guidelines' loss tables — could restore proportionality. Such guidelines need not eliminate prosecutorial discretion entirely; even a requirement to justify deviations from a proportional baseline would increase transparency.

**Graduated prosecution.** The current flat demand structure could be replaced with a graduated system where demands increase more steeply with loss magnitude. The existing statutory ranges (1-20 years) are sufficient to accommodate proportional demands.

**Transparency.** Requiring prosecutors to document the relationship between their demands and case severity measures would create accountability without constraining discretion. Currently, the demand-setting process is opaque and unstructured.

### 5.5 Limitations

**Selection bias.** Our corpus consists of Supreme Court cassation decisions — appealed cases. The demand-loss elasticity may differ at the district court level, where the full population of corruption cases is processed. If cases with extreme disproportionality are more likely to be appealed, our estimates may not generalize.

**Kerugian negara measurement.** State financial loss figures are extracted from verdict metadata and may not reflect the actual harm. Loss quantification in corruption cases is contested and sometimes reflects prosecutorial framing rather than objective measurement.

**Confounders.** Variables not captured in our data — defendant cooperation, plea agreements, strength of evidence, defendant status, case complexity — may explain some of the demand variation we attribute to prosecutorial discretion. However, even if these confounders partially explain the low elasticity, the finding that R-squared=0.244 for the loss-demand relationship remains consequential: loss magnitude is a weak predictor of prosecution demand regardless of mechanism.

**Tuntutan level.** Our tuntutan variable may refer to the original district court demand or to the prosecution's position at cassation. Two observations suggest it is the original demand. First, the mean sentencing discount (vonis/tuntutan = 0.78) implies judges consistently reduce demands by ~22% — a pattern consistent with PN-level demands being discounted, not with cassation-level demands that would have been adjusted to approximate the expected outcome. Second, in 75% of cases vonis falls below tuntutan, inconsistent with cassation-level demands that would more closely track the eventual sentence. Nevertheless, we cannot rule out that some tuntutan values reflect cassation-stage adjustments, which would compress the demand range and bias our elasticity estimate downward.

## 6. Conclusion

We document a striking failure of proportionality in Indonesian corruption prosecution: the elasticity of prosecution demand with respect to state financial loss is only 0.109, meaning that a 10,000-fold increase in corruption scale produces only a 2.7-fold increase in the prosecution demand. This inelasticity is not explained by statutory caps, geographic variation, or charge type.

The broken proportionality creates a regressive prosecution structure where small-scale corruption is punished disproportionately harshly relative to harm, while mega-corruption receives an implicit "volume discount." This has direct implications for deterrence: the marginal punishment for escalating corruption is negligible, creating a rational-actor incentive to maximize the scale of corrupt acts.

Our findings shift the focus of corruption sentencing reform from judges to prosecutors. Judicial sentencing in Indonesia is well-anchored to prosecution demands (R-squared=0.60, consistent with cross-national benchmarks). The proportionality failure originates upstream, in prosecutorial demand-setting, where only 31.5% of variation can be explained by available case features. Restoring proportionality requires addressing prosecutorial discretion — through guidelines, transparency requirements, or graduated demand structures — not merely reforming judicial sentencing.

The CorpusKorupsi dataset and analysis code are publicly available at [repository URL].

## Declarations

**Funding.** This research received no external funding.
**Conflicts of interest.** The author declares no conflicts of interest.
**Ethics approval.** This study analyzes publicly available court documents published by the Indonesian Supreme Court. No human subjects were involved and no ethics approval was required.
**Data availability.** The CorpusKorupsi structured dataset and analysis scripts will be made available upon publication.
**Use of AI-assisted tools.** The author used Claude (Anthropic, Claude Opus) as a computational research assistant for programming, statistical analysis, and manuscript drafting. All analyses were independently verified through reproducible scripts, and the author takes full responsibility for all scientific claims and interpretations.

## References

Ashworth, A. (2015). *Sentencing and Criminal Justice* (6th ed.). Cambridge University Press.

Author (2026a). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns. [Companion paper]

Author (2026b). Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences. *Crime, Law and Social Change* [under review].

Author (2026c). Bidirectional Correction: How Indonesian Judges Override Low Prosecution Demands in Corruption Cases. [Companion paper]

Becker, G. S. (1968). Crime and Punishment: An Economic Approach. *Journal of Political Economy*, 76(2), 169-217. https://doi.org/10.1086/259394

Bibas, S. (2004). Plea Bargaining outside the Shadow of Trial. *Harvard Law Review*, 117(8), 2463-2547.

Davis, K. C. (1969). *Discretionary Justice: A Preliminary Inquiry*. Louisiana State University Press.

Englich, B., Mussweiler, T., & Strack, F. (2006). Playing dice with criminal sentences: The influence of irrelevant anchors on experts' judicial decision making. *Personality and Social Psychology Bulletin*, 32(2), 188-200.

Indonesia Corruption Watch (2025). Sentencing trend monitoring report 2024. Jakarta: ICW.

Lambsdorff, J. G. (2007). *The Institutional Economics of Corruption and Reform: Theory, Evidence, and Policy*. Cambridge University Press.

Medvedeva, M., Vols, M., & Wieling, M. (2020). Using machine learning to predict decisions of the European Court of Human Rights. *Artificial Intelligence and Law*, 28(2), 237-266.

Strickson, B., & De La Iglesia, B. (2020). Legal judgement prediction for UK Crown Court criminal cases. *Proceedings of ICAART*, 458-465.

Tversky, A., & Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. *Science*, 185(4157), 1124-1131. https://doi.org/10.1126/science.185.4157.1124

Ulmer, J. T. (2012). Recent developments and new directions in sentencing research. *Justice Quarterly*, 29(1), 1-40.

van Wingerden, S., van Wilsem, J., & Roosma, F. (2016)."; Sentencing in the Netherlands: Determinants of severity and judicial consistency. *European Journal of Criminology*, 13(4), 489-512.

von Hirsch, A. (1992). Proportionality in the Philosophy of Punishment. *Crime and Justice*, 16, 55-98. https://doi.org/10.1086/449204

Vorenberg, J. (1981). Decent Restraint of Prosecutorial Power. *Harvard Law Review*, 94(7), 1521-1573.

Wittenbrink, F., & Niehaus, S. (2022). Prediction of Criminal Sentencing: A Systematic Review of Models, Outcomes, and Methodological Issues. *European Journal of Criminology and Police Research*, 28, 349-371.
