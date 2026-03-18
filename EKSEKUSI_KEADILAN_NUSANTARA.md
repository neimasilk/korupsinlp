# EKSEKUSI KEADILAN NUSANTARA
## Rencana Operasional — Dokumen Hidup

**Status**: Aktif — diperbarui seiring perkembangan riset
**Konstitusi**: Lihat `MANIFESTO_KEADILAN_NUSANTARA.md` untuk visi dan prinsip
**Terakhir diperbarui**: 18 Maret 2026

---

## I. PRINSIP EKSEKUSI

1. **Simple is better.** Regresi sebelum deep learning. TF-IDF sebelum BERT.
2. **Fail fast.** Jika scraping tidak feasible dalam 2 minggu, pivot.
3. **Ship early.** Satu paper yang submitted lebih berharga dari lima draft.
4. **Scope kills.** Setiap fase harus menghasilkan satu output yang publishable.
5. **Baseline first.** Selalu mulai dari metode paling sederhana. Kompleksitas hanya jika baseline terbukti tidak cukup.

---

## II. FASE RISET

### Fase 0: Feasibility Study (2 minggu)
**Pertanyaan:** Apakah data bisa diambil dan di-parse?

**Task:**
- [ ] Scrape 100 putusan tipikor dari Direktori Putusan MA dari 5 pengadilan berbeda
- [ ] Analisis variasi format (HTML vs PDF, struktur heading, konsistensi field)
- [ ] Buat parser prototipe — ukur success rate per field:
  - Kerugian negara: bisa diekstrak? Dalam format apa?
  - Vonis (bulan penjara): bisa diekstrak?
  - Tuntutan jaksa: bisa diekstrak?
  - Daerah/pengadilan: bisa diekstrak?
  - Tahun: bisa diekstrak?
  - Nama hakim/jaksa: bisa diekstrak?
  - Pasal yang didakwakan: bisa diekstrak?
- [ ] Dokumentasi temuan: format apa yang dominan? Berapa % bisa di-parse otomatis?

**Gate:** Jika success rate parsing < 60% untuk field inti (kerugian negara, vonis, daerah, tahun), evaluasi ulang pendekatan sebelum lanjut.

**Output:** Laporan feasibility internal (bukan untuk publikasi).

---

### Fase 1: Corpus Building + Sentencing Analysis (6 bulan)
**Target paper:** J1 atau J4

#### Layer 1A: Corpus MVP
**Scope:** Putusan tipikor tingkat MA saja (~11.500 dokumen). BUKAN seluruh PN/PT.

**Sumber data:**
- Direktori Putusan Mahkamah Agung (putusan3.mahkamahagung.go.id)
- Kategori: Tipikor (Pidana Khusus → Tindak Pidana Korupsi)

**Pipeline:**
```
Scraping (BeautifulSoup/Scrapy)
  → Raw HTML/PDF storage
    → Parsing (regex + rule-based)
      → Structured database (SQLite/PostgreSQL)
```

**Field yang diekstrak (minimum viable):**
| Field | Prioritas | Metode Ekstraksi |
|-------|-----------|-----------------|
| Nomor putusan | P0 | Regex pada header |
| Tahun putusan | P0 | Regex pada tanggal |
| Pengadilan asal | P0 | Regex pada header |
| Provinsi/kabupaten | P0 | Mapping pengadilan → daerah |
| Vonis (bulan) | P0 | Regex pada amar putusan |
| Kerugian negara (Rp) | P0 | Regex + normalisasi |
| Tuntutan jaksa (bulan) | P1 | Regex pada bagian tuntutan |
| Pasal utama | P1 | Regex |
| Nama hakim (majelis) | P2 | Regex pada bagian akhir |
| Nama jaksa | P2 | Regex pada bagian identitas |
| Teks pertimbangan hakim | P2 | Section extraction |

P0 = harus ada untuk paper pertama. P1 = sangat diinginkan. P2 = bonus.

**Mitigasi risiko teknis:**
- Website down/blocking → scrape dalam batch kecil, jeda antar request, rotate user-agent
- Format tidak konsisten → buat multiple parser patterns, log failures, manual review untuk outliers
- PDF scanned → skip untuk fase 1 (hanya proses yang parseable), catat coverage rate

#### Layer 2A: Sentencing Analysis (Baseline)
**Metode — mulai dari yang paling sederhana:**

1. **Statistik deskriptif:**
   - Distribusi vonis (histogram)
   - Distribusi kerugian negara
   - Distribusi rasio vonis/tuntutan ("diskon")
   - Breakdown per tahun, per provinsi
   - Ini saja sudah bernilai — belum pernah ada yang membuat deskriptif ini untuk seluruh putusan MA tipikor

2. **Regresi (jika field cukup):**
   - Model: `vonis_bulan ~ log(kerugian_negara) + pasal + tahun + provinsi`
   - Interpretasi R²: berapa variasi vonis yang bisa dijelaskan oleh faktor-faktor yang seharusnya dominan?
   - **KRITIS:** Jika mitigating factors bisa diekstrak dari teks (pengembalian kerugian, kooperasi, peran terdakwa), masukkan sebagai kontrol. Jika tidak bisa diekstrak, nyatakan sebagai batasan eksplisit.
   - Feature importance: faktor mana yang paling memprediksi vonis?
   - Residual analysis: putusan mana yang anomali (vonis jauh dari prediksi)?

3. **Visualisasi:**
   - Heatmap Indonesia: rata-rata vonis per provinsi, dinormalisasi per log(kerugian negara)
   - Scatter plot: kerugian negara vs vonis, color-coded per provinsi/tahun
   - Time series: rata-rata vonis per tahun

**Paper target:**

| Opsi | Judul | Data Minimum | Jurnal Target |
|------|-------|-------------|---------------|
| J4 | "The Discount: Prosecutorial Demand vs Judicial Outcome in Indonesian Corruption Cases" | Vonis + tuntutan + kerugian negara + daerah + tahun | Journal of Empirical Legal Studies |
| J1 | "The Price of Corruption: Sentencing Proportionality in Indonesian Anti-Corruption Courts" | Vonis + kerugian negara + pasal + daerah + tahun + (mitigating factors) | Journal of Quantitative Criminology |

**Rekomendasi:** J4 lebih achievable karena "diskon" (rasio vonis/tuntutan) adalah metrik yang simple tapi powerful, tidak membutuhkan kontrol mitigating factors (karena tuntutan jaksa SUDAH memperhitungkan faktor-faktor itu).

---

### Fase 2: Judicial Language Mining (6 bulan setelah Fase 1)
**Prasyarat:** Corpus dari Fase 1 + teks pertimbangan hakim berhasil diekstrak
**Target paper:** J2 atau J5

#### Pendekatan bertahap:

1. **Baseline (minggu 1-4): TF-IDF + Logistic Regression**
   - Binary classification: vonis ringan (≤ median) vs berat (> median)
   - Input: teks pertimbangan hakim (bag of words / TF-IDF)
   - Jika akurasi >> chance → bahasa memang prediktif → lanjut ke step 2
   - Jika akurasi ≈ chance → bahasa tidak prediktif → H2 terfalsifikasi → ini JUGA paper yang publishable

2. **Interpretasi (minggu 4-8): Feature analysis**
   - N-gram yang paling prediktif untuk vonis ringan vs berat
   - Apakah frasa "menyesal," "tulang punggung keluarga," "kooperatif" memang dominan?
   - Perbandingan frekuensi frasa antar daerah → "dialek keringanan"?

3. **Model lanjut (minggu 8-16, HANYA jika baseline berhasil):**
   - IndoBERT fine-tuned — apakah ada peningkatan signifikan dari baseline?
   - Attention analysis: token mana yang paling berpengaruh pada prediksi?
   - BERTopic pada pertimbangan hakim: topik apa yang muncul? Bagaimana distribusinya berubah over time?

4. **Cross-domain (opsional, jika waktu ada):**
   - Bandingkan bahasa putusan tipikor vs pidana umum (pencurian, narkotika)
   - Apakah koruptor mendapat "bahasa yang lebih baik"?

**Catatan tentang Legal NLP:**
- IndoBERT dilatih pada teks umum. Bahasa hukum Indonesia adalah register berbeda. Jangan asumsikan fine-tuning otomatis bekerja.
- Jika IndoBERT tidak signifikan lebih baik dari TF-IDF → laporkan itu. Negative result tetap publishable dan penting.
- Pertimbangkan domain-adaptive pretraining jika corpus cukup besar.

**Paper target:**

| Opsi | Judul | Jurnal Target |
|------|-------|---------------|
| J5 | "The Language of Leniency: How Indonesian Courts Linguistically Normalize Corruption" | Law & Society Review |
| J2 | "Reading the Judge: NLP Analysis of Judicial Language in Indonesian Corruption Verdicts" | Artificial Intelligence and Law |

---

### Fase 3: Advanced Analysis (tahun 2+, HANYA jika Fase 1 & 2 menghasilkan paper)
**Prasyarat:** Minimal 1 paper submitted dari Fase 1 atau 2

#### 3A: Geographic Disparity Deep Dive
- Clustering kabupaten berdasarkan profil vonis
- Identifikasi "pulau impunitas"
- Korelasi dengan data BPS (APBD, kemiskinan, PNS)
- **Paper:** J3 "Islands of Impunity"

#### 3B: Temporal Analysis
- Interrupted time series: efek OTT KPK, revisi UU KPK, tahun Pilkada
- Apakah deterrence bekerja? Berapa lama efeknya?
- **Paper:** J8 "Does Anti-Corruption Work?"

#### 3C: Network Analysis (HATI-HATI)
- Bipartite graph hakim-vonis (level agregat per pengadilan, BUKAN per individu awal)
- Jaksa-hakim pairing analysis
- **Risiko etis tinggi** — publikasi per-individu butuh pertimbangan hukum UU ITE
- **Paper:** Hanya jika ada kolaborator ahli hukum

#### 3D: Darkness Index (AMBISIUS)
- Butuh data BPS, DJPK, KPU — masing-masing format berbeda
- Model prediktif expected corruption vs actual → gap = darkness
- **Paper:** J9 — hanya jika temuan sangat kuat dan Fase 1-2 sudah solid
- **Risiko:** Klaim terlalu berani untuk paper awal. Simpan untuk setelah reputasi established.

#### 3E: Infrastructure Paper
- Publikasi ICVD sebagai dataset terbuka
- Deskripsi pipeline, schema, coverage, limitation
- **Paper:** J7 — bisa disubmit kapan saja setelah database stabil

---

## III. PETA PAPER (DIPRIORITASKAN)

| Prioritas | Paper | Fase | Effort | Impact | Risiko |
|-----------|-------|------|--------|--------|--------|
| **1** | J4 "The Discount" | 1 | Rendah | Tinggi | Rendah |
| **2** | J5 "Language of Leniency" ATAU J2 "Reading the Judge" | 2 | Sedang | Tinggi | Sedang |
| **3** | J7 "ICVD Database" | 1-2 | Rendah | Sedang | Rendah |
| 4 | J1 "Price of Corruption" | 1+ | Sedang | Tinggi | Sedang (butuh mitigating factors) |
| 5 | J3 "Islands of Impunity" | 3A | Sedang | Tinggi | Sedang |
| 6 | J8 "Does Anti-Corruption Work?" | 3B | Tinggi | Sangat Tinggi | Tinggi (klaim kausal) |
| 7 | J6 "Bug or Feature?" | 3A+3B | Tinggi | Tinggi | Tinggi (butuh panel data) |
| 8 | J10 "Resource Curse" | 3D | Tinggi | Tinggi | Tinggi (butuh data multi-sumber) |
| 9 | J9 "Darkness Index" | 3D | Sangat Tinggi | Sangat Tinggi | Sangat Tinggi |

**Strategi:** Kirim J4 dulu. Jika diterima → kredibilitas established → J5/J2 → J7 → sisanya.

---

## IV. STACK TEKNIS

| Komponen | Tool | Catatan |
|----------|------|---------|
| Scraping | BeautifulSoup / Scrapy | Mulai BeautifulSoup, pindah Scrapy jika perlu scale |
| Storage | SQLite → PostgreSQL | SQLite untuk prototyping, PostgreSQL jika data > 10GB |
| Parsing | Regex + Python | Rule-based, bukan ML untuk parsing |
| Analisis statistik | pandas, scipy, statsmodels | |
| ML | scikit-learn, XGBoost | Mulai sklearn, XGBoost hanya jika perlu |
| NLP baseline | TF-IDF + sklearn | SELALU jalankan baseline ini dulu |
| NLP advanced | IndoBERT (Hugging Face) | HANYA jika baseline tidak cukup |
| Topic modeling | BERTopic | Fase 2 |
| Network | NetworkX | Fase 3 |
| Visualisasi | matplotlib, seaborn, folium | D3.js hanya jika bikin dashboard publik |
| Version control | Git + GitHub | Semua kode open source |

---

## V. KRITERIA FALSIFIKASI

| Hipotesis | Klaim | Metode | Falsifikasi | Fase |
|-----------|-------|--------|-------------|------|
| H1 | Vonis tidak proporsional | Regresi | R² tinggi setelah kontrol faktor legal → proporsional | 1 |
| H2 | Bahasa hakim prediktif | Text classification | Akurasi ≤ chance → tidak prediktif | 2 |
| H3 | Vonis menurun seiring waktu | Time series | Tren stabil/naik → tidak ada erosi | 1 |
| H4 | Korupsi kecil ≠ korupsi besar | Clustering | Profil seragam → tidak ada dualisme | 3 |
| H5 | Deterrence gagal | Granger causality | Korelasi negatif signifikan → deterrence bekerja | 3 |
| H6 | Ranking provinsi salah | Normalisasi metrik | Ranking sama → metrik populer benar | 1 |

**Prinsip:** Temuan bahwa hipotesis SALAH sama publishable dengan temuan bahwa hipotesis BENAR.

---

## VI. RISIKO & MITIGASI

| Risiko | Probabilitas | Dampak | Mitigasi |
|--------|-------------|--------|----------|
| Website MA memblokir scraping | Sedang | Tinggi | Batch kecil, jeda, rotate IP. Fallback: minta akses resmi via surat akademik |
| Format putusan terlalu bervariasi | Tinggi | Sedang | Multiple parsers, log failures, toleransi data loss, laporkan coverage rate |
| Kerugian negara tidak bisa diekstrak dari teks | Sedang | Tinggi | Ini field paling kritis — jika gagal, pivot ke analisis yang tidak butuh kerugian negara (e.g. discount analysis: vonis/tuntutan) |
| R² rendah karena missing variables, bukan disproporsionalitas | Tinggi | Tinggi | Frame sebagai "explained variance by legally mandated factors" — jujur tentang batasan |
| IndoBERT gagal pada teks hukum | Sedang | Rendah | Baseline TF-IDF sudah ada — IndoBERT adalah bonus, bukan keharusan |
| Risiko UU ITE dari publikasi per-hakim | Rendah | Sangat Tinggi | Publikasi level agregat (per pengadilan). Per-individu hanya dengan kolaborator hukum |
| Burnout — scope terlalu besar | Tinggi | Sangat Tinggi | **PALING PENTING:** satu fase, satu paper, satu output. Jangan mulai Fase 2 sebelum Fase 1 selesai |

---

## VII. LITERATURE REVIEW YANG HARUS DILAKUKAN

Sebelum menulis paper pertama, lakukan review 1 minggu untuk area berikut:

- [ ] **Computational sentencing analysis** — apa yang sudah dilakukan di US, UK, Brasil, India?
- [ ] **Legal NLP** — state of the art untuk text classification pada dokumen hukum
- [ ] **Indonesian corruption studies** — paper akademik terbaru tentang korupsi Indonesia (ICW reports, TI Indonesia, World Bank governance indicators)
- [ ] **Sentencing disparity** — metodologi standar untuk mengukur disparitas vonis
- [ ] **IndoBERT on legal text** — adakah yang sudah mencoba fine-tuning IndoBERT pada corpus hukum Indonesia?

---

## VIII. MILESTONE & CHECKPOINT

| Milestone | Target | Deliverable | Go/No-Go |
|-----------|--------|-------------|----------|
| M0 | Minggu 2 | Feasibility report | Parsing success rate ≥ 60% |
| M1 | Bulan 3 | Database MVP (field P0 untuk ≥ 5.000 putusan) | Coverage rate ≥ 50% |
| M2 | Bulan 5 | Analisis statistik deskriptif selesai | Ada temuan yang non-trivial |
| M3 | Bulan 6 | Draft paper J4 selesai | Reviewable oleh kolega |
| M4 | Bulan 7 | Paper J4 submitted | — |
| M5 | Bulan 9 | NLP baseline (TF-IDF) selesai | Akurasi > chance |
| M6 | Bulan 12 | Draft paper J5/J2 selesai | Reviewable oleh kolega |

---

**Dokumen ini akan diperbarui seiring perkembangan riset. Manifesto tidak berubah. Eksekusi berubah.**
