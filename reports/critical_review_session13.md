# Critical Review — KorupsiNLP Research Architecture
## Session 13 | 14 April 2026

**Reviewer role**: System/research designer — detecting structural failure risks, incoherence, weak assumptions, over-complexity.

**Scope**: Full project: Manifesto, EKSEKUSI, Paper 1, Paper 2, autoresearch framework, data pipeline, human-AI collaboration architecture.

**Verdict summary**: Paper 2 is publishable with targeted fixes (1 session). Paper 1 needs major restructuring. Manifesto is fine as inspiration but creates execution drag. The project has achieved remarkable output for a solo researcher — the risk now is *not shipping*, not quality.

---

## I. PUBLISHABILITY ASSESSMENT

### Paper 2: "Charge Type, Judicial Opacity, and the Limits of Prediction"

**Verdict: PUBLISHABLE — with 2 targeted fixes (estimated 2-3 hours)**

The paper is well-structured, methodologically sound for its claims, and addresses a genuine gap. The writing is professional, the statistics are verified, and the limitations section is unusually thorough.

**What makes it publishable:**
- Clear research questions with clear answers
- Honest negative results (text features fail) — rare and valued by reviewers
- Proper diagnostics (HC3 SE, VIF, Shapiro-Wilk, Breusch-Pagan, bootstrap CI)
- Temporal stability tested, subsample robustness demonstrated
- Geographic composition finding is a genuine methodological contribution
- Fits CLSC scope, word count, and format requirements
- FREE submission (no APC barrier)

**What could cause desk rejection if not fixed:**

| Issue | Risk Level | Fix Effort |
|-------|-----------|------------|
| Endogeneity of text-derived Pasal 2 understated | HIGH | 1 paragraph rewrite in 5.7 |
| "Opacity" overclaim (40% = genuine absence vs extraction limit) | MEDIUM | 2 sentences reframed in 5.2 |
| No Indonesian legal literature reviewed | LOW-MEDIUM | 1 sentence already in limitations |

**What reviewers will likely request in R1 (expected, not blocking):**
- More discussion of unmeasured confounders
- Comparison with ICW annual findings
- Larger golden set or inter-rater reliability
- Alternative operationalization of charge type (from tuntutan, not pertimbangan)

### Paper 1: "CorpusKorupsi"

**Verdict: NOT PUBLISHABLE in current form — needs major restructuring**

At 35,212 words, Paper 1 is a monograph, not a journal article. No peer-reviewed journal accepts 35,000-word papers.

| Target venue type | Word limit | Current gap |
|---|---|---|
| Standard journal (JELS, AI&Law, CLSC) | 8,000-12,000 | 3-4x over |
| Dataset paper (Data in Brief, Scientific Data) | 3,000-5,000 | 7-10x over |
| Long-form review (Annual Review of Criminology) | 15,000-20,000 | 2x over |

**Options:**
1. **Cut to ~8,000 words** as focused corpus + sentencing baseline paper → submit to JELS or AI&Law
2. **Split into**: (a) dataset descriptor (~4,000 words, *Data in Brief*) + (b) sentencing analysis (~8,000 words, Journal of Quantitative Criminology)
3. **Reframe as SSRN working paper** — no word limit, establishes priority, citeable

**Recommendation:** Option 3 now (SSRN), Option 1 or 2 later. Don't let Paper 1 block Paper 2 submission.

---

## II. STRUCTURAL RISKS

### RISK 1: Endogeneity of Text-Derived Pasal 2 (Severity: HIGH)

**The problem:** `has_pasal_2` is extracted from *pertimbangan hakim* — the same text where judges explain and justify their sentencing decision. This creates potential circularity: we use part of the decision output to "predict" the decision itself.

**Why this matters:** A reviewer in quantitative criminology will immediately ask: "Are judges who give longer sentences simply more likely to invoke Pasal 2 in their reasoning?" If this is the mechanism, the finding is not "charge type affects sentencing" but "judges who sentence harshly write about enrichment more."

**Current mitigations in the paper (Section 5.7):**
1. Binary indicator reduces sensitivity to elaboration length — *Partially valid but insufficient*
2. Structured metadata version shows no effect — *This actually worsens the problem* (see below)
3. Bootstrap CI excludes zero — *Irrelevant to endogeneity; precise estimate of biased coefficient is still biased*

**Why mitigation #2 backfires:** If the structured metadata (listing all charged articles) shows no effect, but the text-derived version does, then the text variable is capturing something *beyond* charge type. It might be capturing: judicial emphasis, reasoning depth, or the judge's decision-making frame — all of which are downstream of the sentencing decision, not upstream of it.

**Counter-argument (in paper's favor):** The finding is temporally stable (pre-2024 and post-2024), survives subsample robustness, and the statutory distinction between Pasal 2 and 3 is legally meaningful. It is *plausible* that charge type genuinely matters. The issue is identification, not plausibility.

**Recommended fix:**
1. **Immediate (for submission):** Strengthen the endogeneity discussion in Section 5.7. Replace the current 3-point mitigation with an honest acknowledgment:

> "The endogeneity of text-derived features represents the most important limitation of this study. Because `has_pasal_2` is extracted from the same judicial reasoning that justifies the sentence, we cannot establish causal direction. The association should be interpreted as: *judges who invoke Pasal 2 reasoning tend to impose longer sentences*, which is consistent with — but does not prove — an independent charge type effect. Future work should extract charge type from prosecution documents (tuntutan text), which are written before the sentencing decision, to achieve cleaner identification."

2. **Post-submission (for R1 or Paper 3):** Actually extract charge type from tuntutan text. This is a concrete, achievable improvement that would dramatically strengthen the finding.

---

### RISK 2: "40% Opacity" Conflates Extraction Failure with Genuine Opacity (Severity: MEDIUM)

**The problem:** The paper claims: "approximately 40% of sentencing variance reflects case-specific factors absent from published verdicts" (Abstract, Section 4.2, Section 5.2).

**What the data actually shows:** 40% of sentencing variance cannot be predicted by the *extracted features* (tuntutan, binary charge type, 3 keywords). The pertimbangan text has median 10,877 characters of nuanced legal reasoning. The extracted features capture a tiny fraction of this information.

**Information present in text but NOT captured by extraction:**
- Specific factual findings of the court
- Defendant's role, position, and specific circumstances
- Evidence quality and credibility assessments
- Specific legal reasoning chains (beyond binary keyword presence)
- Aggravating/mitigating factor details (only 6.3% of MA verdicts list these explicitly, but judges discuss them in narrative form)
- Degree of cooperation with investigators
- Restitution/pengembalian kerugian specifics
- Case-specific circumstances judges describe

**Why TF-IDF failure doesn't resolve this:** TF-IDF failing at n=300 is expected from statistical theory (curse of dimensionality, p/n ratio). It tells us about the *method's limitations at this sample size*, not about what *information the text contains*.

| Claim | Epistemological status |
|---|---|
| "40% is unexplained by our features" | Supported by data |
| "40% is absent from published verdicts" | Unsupported — requires evidence that better extraction still fails |
| "Computational monitoring cannot succeed" | Unsupported — requires testing at larger n with better methods |

**Recommended fix:** Reframe 2 key sentences:

In Abstract: Change "absent from published verdicts" → "not captured by available structured features at current corpus size"

In Section 5.2: Add after the opacity discussion:
> "We cannot definitively distinguish between genuine opacity (information not present in any public document) and extraction limitations (information present in the text but not captured by our methods at n=367). The failure of TF-IDF and transformer approaches is consistent with both interpretations, as these methods are known to underperform at small corpus sizes. Resolving this question would require either expert-coded features from a legal researcher reading each verdict, or a substantially larger corpus enabling more sophisticated text mining."

---

### RISK 3: Paper 1 Structural Problem (Severity: HIGH but not urgent)

35,212 words. Details in Section I above.

**Key point:** This does NOT block Paper 2 submission. Paper 2 references Paper 1 as "Author (2026)" companion paper. Whether Paper 1 is published, on SSRN, or "in preparation" is fine for CLSC submission.

---

### RISK 4: Data Source Fragility (Severity: MEDIUM, long-term)

The entire research program depends on putusan3.mahkamahagung.go.id, which:
- Has SSL certificate issues (SSL verify=False required)
- Pages 2+ of listing are unreliable
- Has no API
- Could restructure without notice
- Could block scraping at any time

**Current state:** 693 verdicts scraped, 367 analysis-ready. This is sufficient for Papers 1 and 2 but insufficient for text mining (which needs n>1000).

**Mitigations already in place:** Raw HTML and PDFs archived locally. Pipeline is reproducible.

**Not yet in place:** No alternative data source identified. No formal data access agreement with MA.

**Recommendation:** Accept this risk for now. Papers 1 and 2 don't need more data. Future corpus expansion should explore: (a) off-peak scraping, (b) formal request to MA via academic letter, (c) alternative sources (Hukumonline, JDIH).

---

### RISK 5: No External Validation (Severity: MEDIUM)

Zero input from:
- Legal experts (interpretation of Pasal 2/3 distinction)
- Practicing judges or prosecutors (validity of findings)
- Peer researchers (methodology review)
- Indonesian legal scholars (literature in Bahasa Indonesia)
- Statisticians (model specification)

**Impact:** The paper is essentially a single-author, single-discipline analysis of a legal phenomenon. This is publishable but reviewers will note it.

**Recommendation:** Find a legal collaborator. This is the single highest-impact action for the long-term research program. Even one co-author from Faculty of Law transforms the project's credibility. For Paper 2 submission now: the solo author limitation is already acknowledged in Section 5.7. Sufficient for initial submission.

---

## III. INCOHERENCE AND OVER-COMPLEXITY

### 3.1 Manifesto-Execution Gap

The Manifesto identifies 5 "stones" (data sources), 6 hypotheses (H1-H6), and 9+ paper ideas (J1-J10). Current execution:

| Element | Status |
|---|---|
| Stone 1 (court verdicts) | Active — 2 papers drafted |
| Stones 2-5 (BPK, APBD, LHKPN, structural) | Not started, no timeline |
| H1 (disproportionality) | Partially tested (R²=0.60, some factors matter) |
| H2 (linguistic normalization) | **Falsified** (text features don't predict) |
| H3-H6 | Not tested |
| Papers J1-J10 | 2 drafted (≈J4 and J2/J5 hybrid), 0 submitted |

**Assessment:** The manifesto is a beautiful inspiration document. It should remain as-is. But the operational planning (EKSEKUSI) should be radically simplified to reflect what one person can actually deliver:
- Fase 1-2: Papers 1 and 2 (current)
- Everything else: "Future work, contingent on papers 1-2 acceptance and collaborator recruitment"

### 3.2 EKSEKUSI Document is Stale

Last updated 9 April 2026. Current numbers are wrong:
- Says "557 putusan" → actual 693
- Says "349 pertimbangan text" → actual 430
- Says "30 eksperimen" → actual 36
- Fase statuses don't reflect Paper 2 being submission-ready

**Recommendation:** Either update it comprehensively or archive it and let HANDOFF.md serve as the living status document.

### 3.3 Autoresearch: Elegant Framework, Predictable Outcome

36 experiments testing TF-IDF variations at n~300. The outcome (failure) was predictable from:
- **Statistical theory:** 100 features on n=300 → p/n = 0.33 → overfitting guaranteed
- **Literature:** Medvedeva et al. (2020) found simple models match BERT even at n=11,000. At n=300, no text method will work.
- **Information theory:** If tuntutan explains 60% and the signal-to-noise ratio in judicial text is low, text features at this n cannot reliably extract the remaining variance.

**Assessment:** The framework itself is well-designed and reusable. The experiments served their purpose: they turned "TF-IDF probably won't work" into "TF-IDF definitively doesn't work, here's 36 experiments proving it." This IS publishable value. The cost was execution time, not research quality.

**For the future:** Before running autoresearch campaigns, do a 30-minute theoretical feasibility check: power analysis, p/n ratio, literature precedent. If theory says "won't work," one confirming experiment suffices.

---

## IV. WEAK ASSUMPTIONS TO EXAMINE

### 4.1 Golden Set Validation (n=20)

The 20-case golden set validates parser accuracy on tested patterns. But:
- 20 cases = 5.4% of analysis-ready corpus
- No stratified sampling documented (are all case types, court regions, time periods represented?)
- No inter-rater reliability (one researcher validates)
- No adversarial testing (deliberately difficult or edge-case verdicts)

**Risk level:** LOW for Paper 2 (which is primarily about regression, not parsing). MEDIUM for Paper 1 (which is about the corpus itself). The 100% accuracy claim is strong but the sample is small.

**Recommendation:** Expand golden set to 50 cases with stratified sampling before Paper 1 submission. Not needed for Paper 2.

### 4.2 "Prosecution Demand Already Captures Charge Severity"

The paper's identification strategy assumes that controlling for tuntutan removes the confounding effect of case severity. But tuntutan reflects many things simultaneously (kerugian, charge type, defendant profile, cooperation, evidence strength). The "residual" Pasal 2 effect after controlling for tuntutan could be:

| Interpretation | Implication |
|---|---|
| Charge type genuinely adds independent information | Paper's preferred interpretation |
| Tuntutan imperfectly captures charge severity (residual confounding) | Effect is artifact of imperfect control |
| Text variable captures judicial emphasis, not just charge type | Endogeneity (Risk 1) |

All three are consistent with the data. The paper acknowledges this implicitly but should be more explicit. The 0.73-year coefficient is best described as an "upper bound" — which the paper already does in Section 5.7 (unmeasured confounders paragraph).

### 4.3 Indonesian Legal Literature Gap

The paper cites Butt (2011), Schutte (2012), and ICW reports, but notes: "Indonesian-language legal scholarship on sentencing was not systematically reviewed." Journals like *Jurnal Hukum dan Peradilan*, *Mimbar Hukum*, and *Jurnal Yudisial* may contain:
- Existing analyses of Pasal 2 vs Pasal 3 sentencing patterns
- Qualitative studies of judicial reasoning in corruption cases
- Prior discussions of sentencing proportionality

**Risk:** The "first large-scale computational" claim is carefully scoped but could still be undermined if an Indonesian scholar has done something similar.

**Recommendation:** Spend 2 hours searching Google Scholar for: "analisis vonis korupsi", "disparitas putusan tipikor", "penjatuhan pidana korupsi", "Pasal 2 Pasal 3 tipikor." Even finding nothing strengthens the paper (documents the search). Finding something requires citation.

### 4.4 Temporal Skew (62% from 2024-2026)

The corpus is dominated by recent verdicts due to MA publication patterns. The temporal stability test (pre-2024 vs 2024+, interaction p=0.94) provides some reassurance, but:
- Pre-2024 subset (n=138) has limited statistical power
- The two periods may differ in case composition, not just time
- The corpus is essentially a cross-section disguised as a time series

**Assessment:** Adequately handled for Paper 2. The temporal stability test is the right approach, and the null interaction result is reported honestly. Would be stronger with more pre-2024 data, but this requires corpus expansion.

---

## V. HUMAN-AI COLLABORATION ARCHITECTURE EVALUATION

### Current Model

```
Session loop:
  [Human] → high-level instruction + manifesto context
    → [Claude] → code + analysis + writing + self-review
      → [Human] → review + approve/reject + redirect
        → repeat
```

### Strengths
- High throughput: 13 commits per session, multiple papers drafted
- Consistent methodology: Claude enforces statistical best practices
- Built-in documentation: HANDOFF.md ensures continuity across sessions
- Self-review capability: Session 12 "thesis killer" review caught 10+ issues

### Weaknesses

**1. Confirmation bias in generation-review loop.**
Claude generates analysis and interprets findings. Human reviews but typically approves direction. The space of *alternative analyses not tried* is never explored. Example: the paper never tests a quantile regression, never tries a Poisson model, never explores interaction effects beyond time period — not because these are wrong, but because Claude's initial analysis path was accepted.

**2. No adversarial testing as default.**
The Session 12 "thesis killer" exercise was excellent but was a one-time event. It should be a standard step in every analysis cycle: after generating a finding, Claude should immediately try to destroy it before presenting it to the human.

**3. Domain knowledge asymmetry.**
Claude has broad statistical/methodological knowledge but zero Indonesian legal expertise. The human has Indonesian institutional knowledge but delegates most analysis decisions. The collaboration doesn't systematically leverage the human's unique knowledge (e.g., "Is this how judges actually think about Pasal 2?" — a question only the human can begin to answer).

**4. No external validation loop.**
12 sessions, 0 external reviewers. The human-AI dyad is a closed system. Every finding has been generated by Claude and reviewed by one person. This is fine for initial exploration but risky for publication claims.

### Recommendations

**Short-term:**
- Make "thesis killer" review a standard final step before any paper finalization
- Human should actively contribute domain knowledge, not just review: "In my experience as a dosen, X is/isn't how courts work"
- Before submission: share draft with at least one colleague for informal review

**Medium-term:**
- Recruit a legal co-author who can independently validate interpretations
- Consider having a second AI session independently critique findings (adversarial review)

**Long-term:**
- Develop a standard operating procedure for each research cycle that includes: hypothesis → analysis → self-critique → human domain input → external review → publication decision

---

## VI. TESTING FRAMEWORK

### Current State: Code Correctness Only

| Layer | Tool | Status |
|---|---|---|
| Parser correctness | pytest (69 tests) | ✅ Complete |
| Extraction accuracy | Golden set (n=20) | ✅ Complete |
| Analysis reproducibility | scripts/11_paper2_analysis.py | ✅ Complete |
| Statistical robustness | Bootstrap, subsample, temporal split | ✅ Complete |

### Missing Layers

| Layer | Purpose | Priority |
|---|---|---|
| **Specification robustness** | Same finding across OLS, robust, quantile, Poisson | HIGH |
| **Influential observation analysis** | Cook's distance, DFFITS — no single case drives P2 finding | HIGH |
| **Placebo/permutation test** | Random binary keyword shows same effect? | MEDIUM |
| **Alternative operationalization** | P2 from tuntutan text vs pertimbangan | HIGH (for R1) |
| **Expert validation** | Legal expert codes 20 verdicts, compare with extraction | MEDIUM |
| **Leave-one-out** | Remove each case, re-estimate, check coefficient stability | LOW |
| **Inter-rater reliability** | Second coder validates golden set | LOW (for Paper 1) |

### Proposed Implementation

A new script `scripts/12_robustness_tests.py` could systematically run:
1. Specification tests: OLS, WLS, quantile regression (median), Poisson/negative binomial
2. Influential observations: Cook's distance plot, DFFITS, identify any case with Cook's d > 4/n
3. Placebo test: generate 1000 random binary variables, run same regression, check if any produces p<0.002
4. Coefficient stability: leave-one-out on Pasal 2 coefficient, report range

This would take ~1 session to implement and would substantially strengthen the paper for R1 response.

---

## VII. CRITIQUE SELECTION MECHANISM

### Principle: Not all critique should be acted on. The cost of acting must be weighed against the cost of not acting.

### Decision Framework

```
For each critique, evaluate:
  1. WHO will notice? (Desk editor, reviewer, reader, nobody)
  2. WHAT is the consequence? (Desk reject, major revision, minor revision, cosmetic)
  3. HOW MUCH effort to fix? (Hours, days, weeks)
  4. DOES IT BLOCK SUBMISSION? (Yes/No)

Decision:
  - Desk reject risk + fixable in hours → FIX NOW
  - R1 likely request + fixable in days → FIX NOW if possible, else note for R1
  - Strengthens paper + fixable in hours → FIX NOW
  - Strengthens paper + requires weeks → NOTE FOR R1
  - Philosophical/framing preference → IGNORE unless trivially fixable
  - Requires external resources (collaborator, data) → PLAN, don't block
```

### Applied to This Review's Critiques

| # | Critique | Who notices | Consequence | Fix effort | Action |
|---|---|---|---|---|---|
| 1 | Endogeneity understated | Reviewer | Major revision | 1 hour | **FIX NOW** |
| 2 | Opacity overclaim | Reviewer | Revision request | 30 min | **FIX NOW** |
| 3 | Paper 1 too long | N/A (not submitted) | Can't submit | Days-weeks | **DEFER** |
| 4 | Data source fragility | Nobody (external risk) | Long-term | N/A | **ACCEPT** |
| 5 | No external validation | Reviewer | Minor note | Weeks | **PLAN** |
| 6 | Manifesto-execution gap | Nobody | Cognitive overhead | 30 min | **SIMPLIFY EKSEKUSI** |
| 7 | EKSEKUSI stale | Nobody | Confusion | 30 min | **UPDATE OR ARCHIVE** |
| 8 | Autoresearch over-engineered | Nobody | Sunk cost | N/A | **IGNORE** |
| 9 | Golden set small | Reviewer (Paper 1) | Minor note | Days | **DEFER to Paper 1** |
| 10 | Indonesian lit gap | Reviewer | Revision request | 2 hours | **DO QUICK SEARCH** |
| 11 | Temporal skew | Reviewer | Already handled | 0 | **DONE** |
| 12 | No legal collaborator | Long-term | Credibility | Weeks | **START SEARCHING** |
| 13 | Specification robustness | Reviewer (R1) | Revision request | 1 session | **PREPARE FOR R1** |
| 14 | Influential observations | Reviewer | Could undermine finding | 2 hours | **DO BEFORE SUBMIT** |

### Immediate Action Items (Before Paper 2 Submission)

1. **Fix endogeneity paragraph** in Section 5.7 (~1 hour)
2. **Reframe opacity claims** in Abstract + Section 5.2 (~30 min)
3. **Run influential observation analysis** — Cook's distance on P2 finding (~2 hours)
4. **Quick Indonesian literature search** on Google Scholar (~2 hours)
5. **Fill in affiliation, ORCID, email** in cover letter + metadata (~15 min)

Total estimated effort: **~6 hours of focused work → then submit.**

---

## VIII. META-ASSESSMENT

### Where This Project Actually Is

This project has achieved remarkable output for a solo researcher working with Claude:
- 693 verdicts scraped and parsed from a difficult source
- Validated extraction pipeline (100% golden set accuracy)
- Two substantial papers drafted with rigorous methodology
- Honest documentation of negative results
- Reproducible analysis scripts

**The single biggest risk right now is not submitting.** Every day the paper sits unsubmitted is a day wasted. Reviewers will find issues — that's their job. The issues they find will be more targeted and more useful than any further self-review.

### What This Project Is NOT (and shouldn't try to be)

- A 10-year, 5-person research program (the manifesto imagines this; the reality is 1 person)
- A comprehensive solution to Indonesian corruption (it's a diagnostic tool)
- An NLP breakthrough (the text mining contribution is the negative result, not a model)
- A legal study (it's a computational study that touches legal questions)

### The Path Forward

```
Week 1:  Fix Paper 2 (endogeneity, opacity, influential obs) → Submit CLSC + SSRN
Week 2:  Indonesian lit search → update both papers if needed
Month 2: Paper 1 restructure (cut to 8,000 words or split)
Month 3: Paper 1 submit + start corpus expansion
Month 4+: Wait for reviews, expand corpus, find collaborator
```

### Final Note

"Santai dalam waktu, serius dalam standar ilmiah" — this principle is exactly right. The project doesn't need to rush, but it also doesn't need more polishing. The standard is: *would a competent reviewer at CLSC find this paper worth engaging with?* The answer is yes.

Ship it.

---

*Review generated: Session 13, 14 April 2026*
*Reviewed by: Claude (adversarial research designer mode)*
*For: Mukhlis Amien, KorupsiNLP principal investigator*
