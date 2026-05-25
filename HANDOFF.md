# Handoff — Session 14-15 → Session 16

## Status: **Paper 2 SUBMITTED (CLSC), Paper 4 on SSRN + hardened for journal, Papers 3+5 ready**

Monster sessions 14-15: CLSC submitted, SSRN Paper 4 uploaded (ID: 6580258), 6 analysis scripts, 3 paper drafts, critical review with 7 blind spots identified + 3 pivots executed, 11 publication figures, cross-national benchmark documented. Paper 4 thesis-killer review completed — all 3 killers addressed and paper strengthened.

## Paper Pipeline

| # | Paper | Status | Key Finding | Next Action |
|---|-------|--------|-------------|-------------|
| 2 | Charge Type + Opacity | **SUBMITTED** CLSC (CRIS-S-26-00344) + SSRN (6574140) | P2 b=+0.73, R2=0.60 | Wait for review |
| **4** | **Broken Proportionality** | **SSRN live (6580258), thesis-killer hardened** | **Elasticity=0.109, CI [0.078, 0.148]** | **Submit to EJCPR** |
| 3 | Bidirectional Anchoring | Draft updated + 4 figures | Quadratic F=11.30, power analysis | Hold until Paper 2 decision |
| 5 | Corruption Anatomy | Draft + robustness | Village penalty 4.7x, fiktif 33% | Hold until Paper 2 decision |
| DI | Darkness Index | Pilot fixed | Under-detected: JaTeng, Banten, Lampung | Need real BPS data |
| 1 | CorpusKorupsi | Needs restructure | Dataset contribution | Extract as data paper |

## IMMEDIATE NEXT: Submit Paper 4 to EJCPR

**Target:** European Journal on Criminal Policy and Research (Springer, Scopus Q2, FREE)
**Why:** "Criminal policy" = perfect fit for broken proportionality finding. Springer = Editorial Manager (familiar). Free for authors.
**Submission URL:** Find via https://www.springer.com/journal/10610 → Submit manuscript
**Files ready:** reports/paper4_draft.pdf (hardened), reports/paper4_draft.docx

### Paper 4 Thesis-Killer Hardening (completed session 15)

| Killer | Attack | Defense Added |
|--------|--------|---------------|
| Multi-dimensional severity | "Kerugian isn't the only severity measure" | Controlled for restitution (p=0.25, elasticity unchanged). Added paragraph: even granting multi-dimensionality, 0.109 is too extreme. |
| Tuntutan level ambiguity | "Maybe it's cassation-level demand" | Evidence it's PN-level: discount=0.78, 75% vonis < tuntutan. If cassation, discount should be ~1.0. |
| Statutory minimum floor | "Low elasticity = statutory floor, not prosecutors" | TURNED INTO STRENGTH: excluding tuntutan < 4yr, elasticity DROPS to 0.070. Floor actually helps proportionality. |
| Deterrence assumes rationality | "Corruption isn't rational calculation" | Softened: "within a rational-choice framework" + cited Lambsdorff institutional economics. |

### Paper 4 Robustness (all pass, script 18)
- Bootstrap 95% CI: [0.078, 0.148] — excludes 0 and 1
- Formal test H0=1.0: p=2.92e-197
- HC3 robust: p=6.53e-132
- All subsamples consistent (temporal, charge type, village, size)
- Outlier-resistant (Cook's d removal → elasticity increases to 0.137)
- Quadratic not significant — constant elasticity adequate

## SSRN Papers

| Paper | SSRN ID | URL | Status |
|-------|---------|-----|--------|
| Paper 2 | 6574140 | papers.ssrn.com/abstract=6574140 | Submitted 14 Apr |
| Paper 4 | 6580258 | papers.ssrn.com/abstract=6580258 | Submitted 15 Apr |

## Critical Review Findings (session 14)

1. **Gap Manifesto↔Research:** Sentencing analysis = end of pipeline. Manifesto asks about whole system.
2. **Cross-national benchmark:** R2=0.60 is NORMAL globally (matches Netherlands). "Opacity" needs reframing.
3. **Prosecutorial discretion is the upstream problem** — Paper 4 proves this (R2=0.315 vs 0.600).
4. **n=367 salami slicing risk** — don't submit Papers 3+5 simultaneously with Paper 2.
5. **PN-level data needed** — MA texts too prosedural for text mining.
6. **Need legal collaborator** — all interpretation from informatika perspective.

## Strategic Roadmap

| Timeframe | Action |
|-----------|--------|
| Session 16 | Submit Paper 4 to EJCPR |
| Week 1-2 | Start PN scraping infrastructure |
| Week 2-3 | Email 3-5 legal collaborator candidates |
| Week 3-6 | PN corpus building (target 1000+ verdicts) |
| Month 2-3 | Wait Paper 2 review → use feedback for Papers 3+5 |
| Month 3-4 | New papers from PN data |

## All Scripts

| Script | Purpose |
|--------|---------|
| scripts/11_paper2_analysis.py | Paper 2 main analysis |
| scripts/12_robustness_tests.py | Paper 2 robustness (7 tests) |
| scripts/13_anchoring_analysis.py | Paper 3 anchoring analysis |
| scripts/14_paper3_extended.py | Paper 3 extended (power, interaction, RTM) |
| scripts/15_darkness_index_pilot.py | Darkness Index pilot |
| scripts/16_prosecutorial_analysis.py | Paper 4 main analysis |
| scripts/17_corruption_anatomy.py | Paper 5 anatomy/typology |
| scripts/18_paper4_robustness.py | Paper 4 robustness (12 tests) |

## All Figures (reports/figures/)

| Figure | Paper | Content |
|--------|-------|---------|
| fig1_scatter_quadratic.png | Paper 3 | Scatter + quadratic fit + crossover |
| fig2_discount_bands.png | Paper 3 | Discount + upward departure by band |
| fig3_power_curve.png | Paper 3 | Power analysis curve |
| fig4_temporal_comparison.png | Paper 3 | Pre-2024 vs 2024+ quadratic |
| fig5_raw_vs_normalized.png | DI | Raw vs per-capita ranking |
| fig6_darkness_score.png | DI | Darkness score by province |
| fig7_kerugian_tuntutan.png | Paper 4 | Kerugian vs tuntutan log-log |
| fig8_appeal_patterns.png | Paper 4 | Prosecutor vs defendant appeals |
| fig9_corruption_anatomy.png | Paper 5 | Actor types + modus operandi |
| fig10_treatment_by_type.png | Paper 5 | Treatment by corruption cluster |
| fig11_elasticity_bootstrap.png | Paper 4 | Bootstrap distribution of elasticity |

## Verification Commands
```bash
python -m pytest tests/ -q                     # 69 passed
python -m scripts.11_paper2_analysis           # Paper 2
python -m scripts.13_anchoring_analysis        # Paper 3
python -m scripts.14_paper3_extended           # Paper 3 extended
python -m scripts.16_prosecutorial_analysis    # Paper 4
python -m scripts.17_corruption_anatomy        # Paper 5
python -m scripts.18_paper4_robustness         # Paper 4 robustness
```

## HUMAN ACTIONS
1. **Submit Paper 4 to EJCPR** (session 16 — Playwright assisted)
2. **Check email** for SSRN confirmations (Paper 2 + Paper 4) and CLSC acknowledgment
3. **Update SSRN profile** — add affiliation (Universitas Bhinneka Nusantara) + ORCID (0000-0002-1848-167X)
4. **Review Paper 4 final draft** — particularly the deterrence framing and "multi-dimensional severity" defense
5. **Consider legal collaborators** — hukum pidana at UI/UGM/UNAIR/UNDIP, researchers at LeIP/ICW
