# Publication Strategy — KorupsiNLP
## 14 April 2026

---

## VERDIKT JUJUR

**Paper 2 layak publish.** Bukan "hampir" — ia sudah di level yang reviewer akan engage serius. Yang kurang bukan risetnya, tapi 2-3 titik lemah yang bisa diperbaiki dalam satu sesi kerja.

**Tapi window-nya sedang menutup.** Ada kerja serupa yang mulai muncul (lihat Bagian III). Setiap minggu tanpa preprint = risiko kehilangan klaim "first large-scale computational."

---

## I. KEPUTUSAN STRATEGIS

### Preprint: SSRN, bukan arXiv

| Faktor | SSRN | arXiv | SocArXiv |
|--------|------|-------|----------|
| **Audience** | Legal/criminology scholars | CS/NLP researchers | Social scientists broadly |
| **Relevance** | Criminal Justice Research Network — tepat | cs.CL atau cs.CY — tidak tepat | Law category — ok |
| **Endorsement** | Tidak perlu | Perlu endorser untuk first-time | Tidak perlu |
| **Speed** | 24-48 jam | 24-48 jam (jika ada endorser) | <2 hari (moderated) |
| **Dikenal di Indonesia** | Ya, terutama dosen hukum | Ya, tapi untuk CS | Belum banyak |
| **Owned by** | Elsevier (risiko: pernah hapus paper) | Cornell (stabil) | OSF/community (stabil) |
| **DOI** | Tidak (tapi dapat SSRN ID) | Ya (arXiv ID) | Ya (via OSF) |

**Rekomendasi: SSRN sebagai primary preprint.**

Alasannya:
1. Paper 2 kontribusi utamanya **kriminologi** (charge type effect, opacity, geographic composition) — bukan NLP
2. Target audience adalah researcher hukum/kriminologi yang cari preprint → mereka cek SSRN, bukan arXiv
3. Tidak perlu endorser (arXiv butuh endorser untuk first-time submitter di category baru)
4. Dosen hukum Indonesia familiar dengan SSRN
5. Menetapkan priority timestamp secepat mungkin

**arXiv?** Tidak untuk Paper 2. TAPI — jika nanti ada Paper 3 yang fokus NLP (misalnya "Why Text Mining Fails on Small Legal Corpora: Evidence from Indonesian Corruption Verdicts"), itu baru cocok di arXiv cs.CL.

**SocArXiv?** Alternatif valid. Open source, community-run, tidak ada risiko Elsevier. Bisa posting di kedua (SSRN + SocArXiv) — tidak ada larangan.

### Journal: CLSC tetap pilihan terbaik

**Konfirmasi dari riset:**

| Kriteria | CLSC Status | Verifikasi |
|----------|-------------|------------|
| Word limit | 10,000 kata | Paper 2 ~5,100 kata body — aman |
| Biaya | GRATIS (subscription model) | Confirmed — no APC |
| Scopus Q | Q2, CiteScore 2.19, SJR 0.364 | Current data |
| Preprint policy | **Springer explicitly allows preprints** | "Posting of preprints is not considered prior publication" |
| Format | Word (.docx), APA references | Sudah tersedia |
| Topical fit | Corruption, sentencing, computational methods | Core scope |
| Timeline | ~3-6 bulan first decision (typical Springer) | Estimate |

**Mengapa bukan jurnal lain?**

| Jurnal | Pro | Kontra | Verdict |
|--------|-----|--------|---------|
| J. Quantitative Criminology (Q1) | Prestige tinggi | Sangat kompetitif, butuh n>1000 | Terlalu ambisius untuk first paper |
| AI & Law (Q1/Q2, Springer) | Cocok untuk computational method | Paper ini bukan tentang method baru | Save untuk Paper 3 (NLP-focused) |
| Asian J. Criminology (Springer) | Konteks regional | Audience lebih kecil | Backup jika CLSC reject |
| J. Financial Crime (Emerald, Q2) | Topik corruption | Lebih business/compliance-focused | Kurang cocok |
| European J. Criminal Policy & Research | Sentencing analysis | Kurang relevan untuk Indonesia | Terlalu Euro-centric |

**Verdict: CLSC adalah sweet spot** — cukup prestisius untuk DUPAK/BKD, cukup achievable untuk first paper, topik cocok, gratis.

---

## II. YANG HARUS DIPERBAIKI SEBELUM SUBMIT

### Fix 1: Endogeneity paragraph (KRITIS — 1 jam)

**Masalah:** `has_pasal_2` diekstrak dari pertimbangan hakim = bagian dari keputusan itu sendiri. Paper saat ini klaim mitigated by 3 observations, tapi mitigasinya lemah.

**Fix:** Tulis ulang paragraf endogeneity di Section 5.7. Akui secara jujur:
- Circularity is real and fundamental
- Association should be interpreted as "judges who invoke Pasal 2 reasoning tend to sentence more harshly"
- Future work: extract from tuntutan text (prosecution document, written before verdict)

### Fix 2: Opacity reframe (PENTING — 30 menit)

**Masalah:** "40% absent from published verdicts" ≠ "40% not captured by our extraction."

**Fix:** Ubah 2-3 kalimat di Abstract + Section 5.2:
- "absent from published verdicts" → "not captured by available structured features at current corpus size"
- Tambah 1 kalimat: inability to distinguish genuine opacity from extraction limitations

### Fix 3: Influential observations (PENTING — 2 jam)

**Masalah:** Belum ada Cook's distance analysis. Bisa jadi 3-5 outlier yang drive seluruh Pasal 2 finding.

**Fix:** Run Cook's distance. Jika semua Cook's d < 4/n → aman. Jika ada influential points → report dan show finding survives removal.

### Fix 4: Indonesian literature search (RECOMMENDED — 2 jam)

**Masalah:** Paper mengakui Indonesian legal literature tidak di-review. Ada karya yang sudah emerge.

**Fix:** Quick Google Scholar search:
- "analisis vonis korupsi"
- "disparitas putusan tipikor"  
- "penjatuhan pidana korupsi"
- "Pasal 2 Pasal 3 tipikor"

Cite apa yang ditemukan. Even finding nothing strengthens the "gap" claim.

### Fix 5: Add competing/related work yang baru ditemukan (RECOMMENDED — 1 jam)

Tambahkan ke literature review:

| Paper | Relevansi | Bagaimana kita berbeda |
|-------|-----------|----------------------|
| **Ibrahim et al. (2024)** arXiv:2410.20104 — CNN+BiLSTM on Indonesian court rulings, R²=0.589 | Directly comparable — deep learning approach to same problem | Our SIMPLE linear model (R²=0.60) BEATS their deep learning. Confirms our argument: simple features > complex models at small n |
| **Syahranuddin (2025)** ICCMS — Qualitative sentencing proportionality analysis | Same topic, different method | Ours is quantitative + computational at scale, theirs is qualitative case analysis |
| **ICW 2024 Report** — 1,871 defendants, avg 3yr 3mo, downward trend | Provides context for our corpus | Our MA-level data shows mean 4.75yr (higher because MA = appealed cases). ICW covers all levels |
| **Haryani** Jurnal Daulat Hukum — Judicial reasoning in appellate corruption cases | Overlapping topic | Ours is computational at scale, theirs is legal analysis of select cases |

**Khusus Ibrahim et al.: Ini talking point KUAT.** Their deep learning (CNN+BiLSTM+attention) on Indonesian court rulings gets R²=0.589. Our simple OLS with just tuntutan gets R²=0.60. This confirms our thesis: "investing in more sophisticated NLP models is less productive than using simple, interpretable features."

---

## III. LANDSCAPE KOMPETISI — Window Sedang Menutup

### Siapa lagi yang mengerjakan ini?

| Researcher/Org | Apa yang mereka lakukan | Threat level |
|---|---|---|
| **Ibrahim et al. (2024)** | Deep learning on general Indonesian court rulings | MEDIUM — different scope (general, not corruption-specific) |
| **Syahranuddin (2025)** | Qualitative corruption sentencing analysis | LOW — conference proceeding, qualitative, not computational |
| **ICW (annual)** | Manual case review, sentencing trends | LOW — grey literature, not peer-reviewed, manual scale |
| **Hasanah et al. (2023)** | IndoBERT on tax court verdicts | LOW — tax, not corruption |
| **Nuranti & Yulianti (2020), Yulianti et al. (2024)** | Legal NER for Indonesian documents | LOW — infrastructure, not sentencing analysis |

### Klaim "first" kita masih aman — TAPI:

Klaim kita: **"First large-scale computational analysis of Indonesian corruption sentencing."**

Ini masih valid karena:
- Ibrahim et al. = general court rulings, bukan spesifik corruption
- Syahranuddin = qualitative, bukan computational at scale
- ICW = manual review, bukan systematic computational
- Tidak ada yang punya structured corpus of corruption verdicts

**Tapi window ini menutup.** Ada trend global menuju computational legal analysis, dan Indonesia mulai catch up. Jika kita tidak publish dalam 3-6 bulan, someone else will do something similar.

**Kesimpulan: URGENCY tinggi untuk preprint. SSRN minggu ini.**

---

## IV. TIMELINE EKSEKUSI

### Minggu ini (14-20 April 2026)

| Hari | Task | Effort |
|------|------|--------|
| Hari 1 | Fix 1: Endogeneity paragraph rewrite | 1 jam |
| Hari 1 | Fix 2: Opacity reframe (Abstract + 5.2) | 30 menit |
| Hari 1 | Fix 3: Cook's distance analysis | 2 jam |
| Hari 2 | Fix 4: Indonesian lit search | 2 jam |
| Hari 2 | Fix 5: Add Ibrahim et al., Syahranuddin, ICW 2024 | 1 jam |
| Hari 2 | Fill in: nama universitas, ORCID, email (cover letter + metadata) | 15 menit |
| Hari 3 | Regenerate PDF + DOCX | 30 menit |
| Hari 3 | **Upload SSRN** (Criminal Justice Research Network) | 1 jam |
| Hari 4-5 | **Submit CLSC** via Springer Editorial Manager | 1-2 jam |

**Total effort: ~10 jam kerja = 2 hari penuh atau 3-4 hari santai.**

### Bulan 1-2 (Mei-Juni 2026) — Sambil menunggu review

| Task | Priority | Notes |
|------|----------|-------|
| Restructure Paper 1 → 8,000 kata | HIGH | Potong atau split |
| Email 5 dosen hukum pidana (Brawijaya, UMM, Unair, UGM, UI) untuk co-authorship | HIGH | Satu legal co-author mengubah trajectory |
| Corpus expansion: off-peak scraping | MEDIUM | Target 800-1000 analysis-ready |
| Prepare robustness tests (scripts/12_robustness_tests.py) | MEDIUM | Siap untuk R1 response |
| Extract charge type from tuntutan text | MEDIUM | Strongest possible R1 response |

### Bulan 3-6 (Juli-Oktober 2026) — Respond to reviews

| Scenario | Action |
|----------|--------|
| **Accept (rare first round)** | Celebrate. Finalize. Start Paper 3 |
| **Minor revision** | Fix what reviewers ask. Resubmit in 2 weeks |
| **Major revision** | Use prepared robustness tests. Tuntutan-derived P2. Larger corpus if available |
| **Reject with encouragement** | Revise based on feedback. Resubmit to CLSC or redirect to Asian J. Criminology |
| **Desk reject** | Rare if paper is formatted correctly. Redirect to AI & Law or J. Financial Crime |

---

## V. MENGAPA BUKAN arXiv?

Dielaborasi karena ini pertanyaan spesifik:

### arXiv TIDAK cocok untuk Paper 2 karena:

1. **Audience mismatch.** arXiv cs.CL readers want: novel NLP methods, SOTA benchmarks, model architectures. Paper 2 offers: a criminological finding about charge type + an honest negative result about NLP. The NLP community will see this as "simple regression with failed text features" — boring. The criminology community will see this as "first computational evidence of charge type premium in Indonesian corruption" — exciting.

2. **First-time endorsement barrier.** arXiv requires an endorser for first-time authors in each category. Finding an endorser for cs.CL or cs.CY takes time and social capital. SSRN has no such barrier.

3. **Framing conflict.** To succeed on arXiv, the paper would need to be reframed as an NLP contribution (e.g., "Why Text Mining Fails on Small Legal Corpora"). That's a different paper than what we have, which is framed as a criminological contribution that uses computational methods.

4. **Ibrahim et al. already occupies the arXiv space.** Their paper (arXiv:2410.20104) already shows "deep learning on Indonesian court rulings." Our paper's value is showing that simple models beat deep learning — but this point is better made in a journal paper that reaches the criminology community, not on arXiv where it reads as "we tried simpler methods."

### Kapan arXiv AKAN cocok:

- **Paper 3** (jika ada): "The Curse of Dimensionality in Legal NLP: Why Text Mining Fails at Small Corpus Sizes" — methodological NLP contribution, appropriate for arXiv cs.CL
- **Corpus release** (Paper 1 restructured as dataset paper): possibly arXiv cs.CL if framed as NLP resource

---

## VI. STRATEGI MULTI-PAPER

### Paper landscape saat ini:

| Paper | Status | Venue | Priority |
|-------|--------|-------|----------|
| **Paper 2**: Charge Type, Opacity, Limits | Needs ~10hr fixes → submit | SSRN → CLSC | **SEKARANG** |
| **Paper 1**: CorpusKorupsi (35k words) | Needs major restructuring | SSRN (as-is) → later split for journal | Bulan 2-3 |
| **Paper 3** (potential): NLP negative result | Not written | arXiv cs.CL → AI & Law | Bulan 6+ |

### Urutan optimal:

1. **Paper 2 dulu.** Ini paper yang paling siap dan paling time-sensitive (competition emerging). It's also the paper with the strongest, most novel finding (Pasal 2 premium).

2. **Paper 1 ke SSRN as-is** (35k words sebagai working paper). SSRN tidak ada word limit. Ini menetapkan priority untuk corpus description dan baseline findings. Nanti restructure untuk journal submission.

3. **Paper 3 later** — jika ada waktu, kebutuhan, dan corpus lebih besar. Fokus NLP methodology, suitable for arXiv + AI & Law.

---

## VII. CHECKLIST SEBELUM SUBMIT

### SSRN Upload Checklist

- [ ] Title, abstract, keywords finalized
- [ ] Author name + affiliation filled in
- [ ] PDF version generated (clean, no track changes)
- [ ] SSRN account created (papers.ssrn.com)
- [ ] Select network: Criminal Justice Research Network (CJRN)
- [ ] JEL codes (if applicable): K14 (Criminal Law), K42 (Illegal Behavior and Enforcement)
- [ ] Upload PDF
- [ ] Note: SSRN processes in 24-48 hours

### CLSC Submission Checklist

- [ ] Manuscript in .docx format (not PDF)
- [ ] Word count < 10,000 (currently ~5,100 — aman)
- [ ] References in APA format with DOIs
- [ ] Cover letter prepared (reports/paper2_cover_letter.docx)
- [ ] Declarations section included (funding, COI, ethics, data)
- [ ] Springer Editorial Manager account created
- [ ] Disclose SSRN preprint in submission notes
- [ ] Suggest 3-5 reviewers (names + emails of scholars in computational legal analysis or Indonesian corruption studies)
- [ ] Supplementary materials uploaded separately

---

*Strategy document generated: Session 13, 14 April 2026*
