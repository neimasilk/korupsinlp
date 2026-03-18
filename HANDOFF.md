# Handoff — Fase 0 Session 1 → Session 2

## What Was Done
1. **Full project structure created** — pyproject.toml, venv, all src/scripts/tests
2. **Live-tested against putusan3.mahkamahagung.go.id** — discovered real URL patterns
3. **Script 01 passes all 4 tests** — site reachable, listing works (53 verdicts/page, 420 pages), detail page parsed (17 fields), PDF URL found
4. **Scraped 10 verdicts (pilot)** — 100% HTTP success rate, 5/10 had full content (5 were "belum diunggah" — too recent)
5. **Parsed with regex extractors** — iteratively fixed patterns against real data

## Parse Rates (on 5 verdicts with content)
| Field | Rate | Notes |
|-------|------|-------|
| tahun | 5/5 (100%) | Fixed regex for MA case number format `384 K/PID.SUS/2026` |
| daerah | 5/5 (100%) | Extracts origin court from related case numbers (`/PN Smg` → Semarang) |
| vonis_bulan | 3/5 (60%) | Added "penjara 8 (delapan) tahun" pattern (no selama/menjadi) |
| kerugian_negara | 1/5 (20%) | Added "UP Rp..." (uang pengganti) pattern. Most kerugian only in PDF full text |
| nama_hakim | 5/5 (100%) | From metadata table |
| nama_terdakwa | 4/5 (80%) | Added "VS NAMA (Terdakwa)" MA format |
| pasal | 1/5 (20%) | Only in catatan_amar for some cases |

## What Needs To Be Done (Session 2)

### Immediate: Fix listing pagination
- Page 5+ returned 0 results — `extract_verdict_urls()` may not match on later pages, or the page content differs
- Debug by fetching page 2/3 and checking HTML structure
- Alternative: use year-filtered URLs like `.../tahunjenis/putus/tahun/2024.html` which produced smaller, faster-loading pages

### Then: Scrape 100 verdicts
- Start from **older pages** (page 3-10) or year-filtered (2023/2024) to avoid "belum diunggah" empty pages
- Run `python -m scripts.02_scrape_sample --count 100 --start-page 3`

### Then: Parse + Report
- Run scripts 03 and 04
- Key question: is kerugian_negara extractable from HTML alone or do we need PDF text?
- If PDF needed: many are scanned (no text) — this affects feasibility

### Known Issues
- Some verdicts have minimal catatan_amar ("Tolak", "PK=TOLAK") — no sentence data extractable
- kerugian_negara mostly absent from HTML summary — only in full verdict PDF
- nama_jaksa: 0% success — not in metadata, rarely in catatan_amar
- The site is slow/flaky — some requests timeout at 90s, especially for large result pages

## Files Modified Since Last Commit
All changes are fixes from live-testing: URL patterns, regex patterns, timeout values, error handling. See `git diff` for details.
