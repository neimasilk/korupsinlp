# Handoff — Session 16 (2026-05-25) → Next

## Status: Paper 2 DESK-REJECTED by CLSC. Program reframed around Paper 4 (upstream prosecutorial proportionality failure). Paper 4 reworked & submit-ready.

---

## The big reframe this session

- **Paper 2 (CRIS-D-26-00272) was DESK-REJECTED by CLSC on 2026-05-22** on *novelty* grounds ("does not make the kind of novel theoretical or empirical contribution... we are looking for") — NOT methods. It sat ~5 weeks then was rejected = a considered decision. The previous handoff wrongly recorded it as "under review."
- **External confirmation of an ignored internal warning.** Session 14's own critique already flagged "R²=0.60 is normal globally" and "manifesto↔research gap." That warning was filed, then ignored while 4 more papers were produced from the same 367 MA verdicts.
- **Root diagnosis — "searching under the streetlight":** the portfolio answers *HOW judges sentence* (convenient data) instead of the manifesto's *WHY corruption persists*. Competing in crowded fields (sentencing → criminologists; audit-corruption → accountants) where others have better data positioning. The real moat is the verdict-text corpus + NLP.
- **Two pivots killed fast (fail-fast):** (1) Darkness Index — saturated in Indonesian public-sector accounting literature (BPK's own TAKEN journal published it); (2) reposition Paper 3 — regression-to-the-mean explains the compression + cassation confound, both unresolved.
- **New unifying thesis (touches the manifesto's "why"):** the proportionality failure is **UPSTREAM (prosecutorial), not judicial.** Judges anchor faithfully (R²=0.60, globally normal); the anchor itself (tuntutan) is inelastic to harm. Papers 2 & 3 become supporting evidence for ONE thesis, not 4 salami submissions.

## Paper 4 — reworked & submit-ready (commit 659af0c)

| Item | Before | After |
|------|--------|-------|
| Elasticity (tuntutan~kerugian) | 0.109 (uncleaned) | **0.126** cleaned, CI [0.102, 0.156], R²=0.285 |
| Data | Rp 100 parse error + PT Timah co-defendant triple inflating leverage | dropped/flagged; cleaning STRENGTHENS finding (robustness table in script 16) |
| Framing | naive "proportionality = elasticity 1.0" straw man | comparative: US Sentencing Guidelines §2B1.1 loss table (~0.25–0.30) + Dec-2025 USSC reform debate. Indonesia ~0.13 = half of even the explicitly loss-graduated system, unstructured |
| Artifacts | — | abstract/§2.1/§3.1/§4.1/§5/refs rewritten; fig7 relabeled; DOCX+PDF regenerated; SSRN 6580258 live |

## Venue decision (constraints: Scopus + FREE; Q irrelevant per user). Submit SEQUENTIALLY, never parallel.

1. **PRIMARY — Asian Journal of Criminology** (Springer, Scopus **Q1**/SSCI, subscription = free to publish). Regional fit attacks the exact cause of Paper 2's desk-reject (general journals ask "why does this matter globally?"; a regional journal treats Indonesian corruption as core).
2. **Backup — EJCPR** (European J. on Criminal Policy & Research; Springer, Scopus Q1, hybrid = free). Criminal-policy fit.
3. **Safety net — IJCJS** (Int'l J. of Criminal Justice Sciences; Diamond OA, fully free, Scopus Q3 + WoS; publishes Indonesian work). Guarantees Scopus placement.

## Portfolio triage

| Paper | Verdict | Action |
|-------|---------|--------|
| 2 (charge type/opacity) | Dead as flagship (desk-rejected, R²=0.60 normal) | Keep on SSRN 6574140; fold charge-type finding as supporting evidence |
| **4 (broken proportionality)** | **FLAGSHIP, submit-ready** | → Asian Journal of Criminology |
| 3 (bidirectional anchoring) | HOLD — RTM + cassation confound unresolved | Needs PN trial-level data for clean identification |
| 5 (corruption anatomy) | Weakest novelty | SSRN/hold |

## Immediate next actions

1. **Prepare AJC submission package** — format manuscript to AJC guidelines, cover letter (disclose SSRN 6580258 preprint + Paper 2 companion), structured abstract + keywords + JEL codes, 3–5 reviewer suggestions. (Claude can do this; user submits via own login.)
2. **Domain input wanted from user** for §5.1: institutional cause of prosecutorial inelasticity — Kejaksaan tuntutan culture? target-conviction incentives? asymmetry vs powerful defendants?
3. **Medium-term: PN (trial-level) scraping** — re-justified as the identification fix for the cassation confound in Papers 3 & 4, NOT "more sentencing papers."
4. Find a legal/criminology collaborator (the closed human-AI loop's blind spot is what the desk-reject exposed).

## Key lesson (also in project memory)

Internal adversarial review optimized for "will a reviewer find a methodological hole?" but never asked the gatekeeper's question "is this novel/significant enough to matter?" → add a **contribution-significance gate** before journal investment; get an external signal (preprint + a real criminologist) before the editor does.

## Verification

```bash
python -m pytest tests/ -q                      # 69 passed (as of session 12)
python -m scripts.16_prosecutorial_analysis     # elasticity 0.126 cleaned + robustness table + fig7/fig8
```
- Branch: `autoresearch/apr9-textfeatures`
- DOCX/PDF built with pandoc + xelatex (pandoc at `~/AppData/Local/Pandoc`)
- python: anaconda (`~/anaconda3/python`); no `.venv` present this session

## SSRN (both live)
- Paper 2: 6574140 · Paper 4: 6580258

## Recent commits
- `659af0c` Paper 4 rework: comparative reframe + cleaned elasticity (flagship)
- `faca620` sessions 13-17: 4 paper drafts, 7 scripts, 11 figures, critical reviews
