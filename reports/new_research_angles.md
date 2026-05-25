# New Research Angles — Beyond Papers 1 & 2
## Session 13 | 14 April 2026

---

## OVERVIEW

Three categories of new angles discovered:
1. **From existing data** — no new scraping needed
2. **From cross-referencing with public structural data** — easy merge
3. **From entirely new data sources** — requires new infrastructure

---

## ANGLE 1: THE ANCHORING CORRECTION EFFECT (dari data yang ada)

### Discovery

The relationship between prosecution demand (tuntutan) and sentence (vonis) is NOT linear — it's **concave** with a significant quadratic term (F=11.30, p=0.0009).

Judges don't apply a fixed discount. They **correct prosecution demands toward an internal reference point:**

| Tuntutan band | n | Mean discount | % Upward (vonis > tuntutan) |
|---|---|---|---|
| 0-2 years | 26 | **1.132** (judges ADD 13%) | 30.8% |
| 2-4 years | 51 | **1.061** (judges ADD 6%) | 31.4% |
| 4-6 years | 99 | 0.750 (judges cut 25%) | 16.2% |
| 6-8 years | 72 | 0.666 (judges cut 33%) | 5.6% |
| 8-10 years | 44 | 0.649 (judges cut 35%) | 6.8% |
| 10-15 years | 50 | 0.661 (judges cut 34%) | 2.0% |
| 15-25 years | 23 | 0.704 (judges cut 30%) | 0.0% |

**Crossover point:** ~4 years tuntutan. Below this, judges tend to INCREASE sentences. Above this, they DECREASE.

### Why this matters

This is much more than simple anchoring (Englich et al., 2006). Anchoring predicts that prosecution demand sets a reference point and judges adjust from it. Our finding shows **bidirectional correction**: judges have their OWN reference range and PULL prosecution demands toward it.

**Implication:** Judges may operate with an implicit "fair sentence" for corruption (roughly 4-6 years) and systematically correct prosecution demands that deviate too far from this range. This is evidence of a **judicial norm** that is not written in any guideline.

### Publishability

| Factor | Assessment |
|---|---|
| Novelty | HIGH — bidirectional anchoring correction never shown for corruption |
| Data | Already in hand — no new scraping |
| Method | Simple extension of existing regressions |
| Effort | ~1 week |
| Connection to literature | Direct extension of Englich et al. (2006) |
| Policy relevance | HIGH — implies judges have implicit sentencing norms |

**Potential title:** "Judicial Correction of Prosecutorial Anchors: Nonlinear Sentencing Patterns in Indonesian Corruption Cases"

**Target journals:**
- Behavioral Sciences & the Law (Wiley, Q2)
- Journal of Empirical Legal Studies (Wiley, Q1)
- Law and Human Behavior (APA, Q1)

**Could also be folded into Paper 2** as an additional section, or into a restructured Paper 1.

---

## ANGLE 2: THE DARKNESS INDEX PILOT (data struktural publik)

### Concept

Nobody has built a "Corruption Darkness Index" — a measure of the GAP between expected and detected corruption. Transparency International's CPI measures perceptions, not actual corruption. This concept is **genuinely novel and unoccupied in the literature.**

### Data availability (confirmed by research)

| Source | Data | Format | Effort to acquire |
|---|---|---|---|
| **BPS** (bps.go.id) | Poverty rate, GRDP, PNS count per kabupaten | HTML tables, some Excel | LOW — download & parse |
| **DJPK Kemenkeu** (djpk.kemenkeu.go.id) | APBD per kabupaten: revenue, expenditure, realization | **CSV export confirmed** | LOW — direct download |
| **BPK** (bpk.go.id) | Audit opinions (WTP/WDP/TMP/TW) per kabupaten | Tabular summaries | LOW-MEDIUM |
| **KorupsiNLP corpus** | Corruption case counts per daerah | Already in hand | ZERO |

### What becomes possible

1. **Normalized corruption rates:** Cases per capita, per GRDP, per PNS — changes every "most corrupt province" ranking
2. **Audit paradox test:** Regions with WTP (clean audit) that still produce corruption cases. BPK itself has noted this paradox.
3. **Fiscal dependence predictor:** Do regions more dependent on dana transfer (vs own-source revenue) have more corruption cases?
4. **Budget anomaly × corruption:** Does the gap between APBD plan and realization predict future corruption cases?
5. **Prototype Darkness Index:** Expected corruption (from structural predictors) minus detected corruption = "darkness"

### Prior work

- Political budget cycle research exists for Indonesia (499 districts, 2011-2017) but nobody cross-references with corruption verdicts
- No computational Darkness Index exists anywhere — we can own this concept
- BPK's own article "Opini WTP dan Korupsi" acknowledges the audit-corruption disconnect but provides no quantitative analysis

### Publishability

| Factor | Assessment |
|---|---|
| Novelty | VERY HIGH — nobody has built this |
| Data | CSV/tabular, publicly available |
| Method | Regression, normalization, maybe spatial analysis |
| Effort | 2-4 weeks (data collection + merge + analysis) |
| Connection to literature | TI CPI critique, governance indicators literature |
| Policy relevance | VERY HIGH — redefines how we measure corruption |

**Potential title:** "Measuring the Darkness: A Corruption Darkness Index for Indonesian Districts Using Public Financial and Judicial Data"

**Target journals:**
- Governance (Wiley, Q1 — high impact but very competitive)
- Public Administration and Development (Wiley, Q2)
- Journal of Financial Crime (Emerald, Q2)

---

## ANGLE 3: CROSS-NATIONAL COMPARISON (Indonesia × Brazil)

### Discovery

Recent research:
- **Vilaca (2025, AJPS):** Analyzed 3,154 Lava Jato cases in Brazil showing antipolitical class bias in sentencing
- **China:** 7,304 corruption judgment analysis; fiscal pressure on sentencing
- **Indonesia (us):** 367 analysis-ready MA corruption verdicts

Brazil and Indonesia are **natural comparisons**: both middle-income, both have dedicated anti-corruption courts, both have extensive public verdict data, both struggle with systemic corruption.

### What could be compared

| Dimension | Indonesia (our data) | Brazil (from literature) |
|---|---|---|
| Sentencing anchor (prosecution demand) | R²=0.60 | Unknown — we could test |
| Charge type effect | Pasal 2 vs Pasal 3, +0.73yr | Lava Jato charges |
| Geographic variation | Composition effect (p=0.20) | Regional variation? |
| Judicial opacity | Discount R²=-0.01 | Unknown |
| Corpus size | 367 | 3,154 |

### Feasibility

Depends on whether Brazilian data is available. Lage-Freitas et al. (2022) used Brazilian court data — their corpus may be accessible. Even a literature-based comparison (no new data) is publishable as a comparative review.

**Effort:** 2-4 weeks if literature-based; 2-3 months if data-based.

**Target:** Comparative Political Studies, Governance, or a law review.

---

## ANGLE 4: UPWARD DEPARTURES (dari data yang ada)

### Discovery

50 cases (13.6%) where judges gave MORE than prosecution demanded. Key patterns:
- Concentrated in low-tuntutan cases (31% of 0-4yr tuntutan → upward departure)
- Higher Pasal 2 rate (72% vs 62% for downward)
- Mean upward vonis: 5.60yr, mean upward tuntutan: 3.78yr

### Why interesting

Upward departures are almost never studied in corruption sentencing. They represent cases where judges believe the prosecution was TOO LENIENT. In a system often criticized for light sentences, these cases show judges can push BACK against prosecutorial leniency.

**Potential title:** "When Judges Exceed Prosecution Demands: Upward Departures in Indonesian Corruption Sentencing"

**Effort:** 1 week from existing data. Could be a short note or letter rather than full article.

---

## ANGLE 5: LLM-BASED STRUCTURED EXTRACTION (resolving opacity)

### The question

Paper 2 claims 40% of sentencing variance is "opaque." But is this genuine opacity or extraction limitation? LLM extraction could resolve this.

### What could be extracted

From pertimbangan text, an LLM could systematically extract:
- Defendant's specific position/jabatan (bupati, kepala dinas, pegawai, etc.)
- Specific modus operandi (mark-up pengadaan, fiktif, gratifikasi, etc.)
- Cooperation level (structured rating, not just keyword)
- Restitution amount and compliance
- Number of co-defendants
- Whether defendant was convicted at first instance or only at appeal

### Feasibility assessment (from text sample)

**Problem:** MA-level pertimbangan is mostly PROCEDURAL — discusses whether the lower court applied law correctly. Substantive sentencing reasoning (defendant circumstances, specific aggravating/mitigating details) is minimal at cassation level.

**Implication:** LLM extraction on MA data will yield limited additional information. The approach would be more powerful on PN-level (first instance) verdicts, which contain the detailed sentencing reasoning.

**Recommendation:** Test on 20 MA pertimbangan texts first. If LLM extraction yields meaningful new variables → scale up. If MA texts are too procedural → pivot to PN data collection. Save this angle for after Paper 2 submission.

---

## ANGLE 6: PROCUREMENT DATA CROSS-REFERENCE (opentender.net)

### Discovery

opentender.net provides 1.8M+ Indonesian procurement tenders since 2008 in Open Contracting Data Standard. Built by ICW + LKPP, licensed ODbL.

### Novel angle

Match procurement anomalies (repeat winners, single bidders, price markup patterns) to regions that produce corruption verdicts. Nobody has closed this loop in Indonesia.

### Feasibility

MEDIUM. Data is structured and available, but 1.8M records requires serious data engineering and the matching logic needs careful design.

**Recommendation:** Pilot with one province first. If signal exists → scale.

---

## PRIORITY RANKING

| # | Angle | Novelty | Feasibility | Impact | New data needed? | Time |
|---|---|---|---|---|---|---|
| **1** | Anchoring Correction | HIGH | VERY HIGH | HIGH | No | 1 week |
| **2** | Darkness Index pilot | VERY HIGH | HIGH | VERY HIGH | Yes (CSV) | 2-4 weeks |
| **3** | Upward Departures | MEDIUM | VERY HIGH | MEDIUM | No | 1 week |
| **4** | Cross-national (Brazil) | HIGH | MEDIUM | HIGH | Maybe | 2-4 weeks |
| **5** | LLM Extraction | HIGH | MEDIUM | HIGH | No (but limited at MA) | 2-3 weeks |
| **6** | Procurement cross-ref | HIGH | LOW-MEDIUM | VERY HIGH | Yes (large) | 1-2 months |

### Recommended next paper: **Anchoring Correction (Angle 1)**

Why:
- Zero additional data needed
- 1 week of work
- Clear, novel finding (p=0.0009)
- Connects to established literature
- Policy-relevant
- Can be written as short paper or letter

### Recommended ambitious project: **Darkness Index (Angle 2)**

Why:
- Genuinely novel concept — nobody has built this
- "Own the term" opportunity
- Data is publicly available in structured formats
- Directly fulfills Manifesto vision (Batu 5, H6)
- High policy impact
- Could attract collaborators and media attention

---

## KEY INSIGHT

Paper 2 menganalisis **bagaimana** hakim memvonis koruptor (sentencing mechanics). Angle-angle baru ini menjawab pertanyaan yang LEBIH BESAR:

- **Angle 1 (Anchoring):** Apakah hakim punya "tarif tak tertulis" untuk korupsi?
- **Angle 2 (Darkness Index):** Di mana korupsi yang TIDAK tertangkap?
- **Angle 3 (Cross-national):** Apakah pola Indonesia unik atau universal?
- **Angle 4 (Upward Departures):** Kapan hakim MELAWAN tuntutan yang terlalu ringan?

Setiap angle adalah "batu" yang berbeda dari gunung yang sama.

---

*Generated: Session 13, 14 April 2026*
