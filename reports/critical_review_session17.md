# Review Kritis — Arsitektur Riset KorupsiNLP
## Session 17 | 7 Juli 2026

**Peran reviewer**: System/research designer — deteksi dini kegagalan, risiko struktural, incoherence, over-complexity, asumsi lemah; evaluasi arsitektur kolaborasi human–AI; framework testing; mekanisme seleksi kritik.

**Basis**: Manifesto, EKSEKUSI, HANDOFF session 16, review session 13, draft Paper 4, dan **audit keadaan aktual repo** (DB, skrip, tes, golden set, git) — bukan hanya klaim dokumen.

**Prinsip yang dipegang**: simple is better, fail fast, pivot early, santai dalam waktu — serius dalam standar ilmiah.

---

## 0. VONIS RINGKAS

1. **Ketidakpuasan Anda ("masih banyak blind spot soal MENGAPA korupsi tinggi") secara struktural BENAR — dan penyebabnya bukan kurang teknik data mining, melainkan tidak adanya peta kausal.** Korpus putusan hanya bisa mengukur SATU dari empat komponen "mengapa korupsi menguntungkan": severity hukuman *conditional on* tertangkap-dituntut-divonis. Tiga komponen lainnya (probabilitas deteksi, probabilitas penuntutan, atrisi perkara) tidak ada di data putusan dan tidak akan pernah ada. Reframe Session 16 ("upstream, prosecutorial") memindahkan lampu sorot satu langkah ke hulu — tapi masih di bawah lampu jalan yang sama. Solusinya bukan pivot; solusinya **memetakan secara eksplisit edge mana yang bisa diidentifikasi oleh data mana**, lalu memilih "batu" berikutnya berdasarkan peta itu, bukan berdasarkan kenyamanan data. (§I)

2. **Paper 4 (flagship) punya TIGA kelemahan teknis yang harus dibereskan SEBELUM submit ke AJC** — dua di antaranya berpotensi mematikan klaim utama jika reviewer ekonomi/kriminologi kuantitatif memeriksanya: (a) benchmark AS memakai elasticity *implied by the guideline table*, bukan elasticity *terealisasi* di praktik pengadilan AS — jika elasticity riil AS ≈ 0.15 (plausible, karena hakim AS rutin depart ke bawah pada kasus loss besar), klaim "setengah dari AS" runtuh; (b) perbandingan R² 0.315 vs 0.600 adalah apples-to-oranges dan kesimpulan "prosecutors exercise wider discretion than judges" tidak sahih dari perbandingan itu; (c) attenuation bias dari measurement error kerugian negara belum dibound. Semua bisa dibereskan dalam hitungan hari. **Jangan ulangi pola Paper 2: submit → gatekeeper eksternal menemukan apa yang review internal lewati.** (§II)

3. **Kelemahan tersembunyi paling murah untuk diperbaiki: golden set.** Audit menemukan `vonis_bulan` tervalidasi 20/20, tapi `tuntutan_bulan`, `kerugian_negara`, `daerah`, `tahun` hanya tervalidasi pada **5 kasus**. Seluruh angka flagship (elasticity 0.126!) mengalir melalui dua extractor yang validasinya n=5. Ini fondasi semua paper. Ekspansi ke 50 kasus stratified = 1–2 hari kerja, men-de-risk seluruh portofolio. (§III)

4. **Arsitektur kolaborasi human–AI sudah menghasilkan 4 mode kegagalan yang TERDOKUMENTASI di repo ini sendiri** — transfer status yang salah antar sesi, kritik yang di-file lalu diabaikan, review yang mengoptimasi target yang salah, dan drift pertanyaan mengikuti kenyamanan data. Semuanya punya perbaikan yang bisa dimekanisasi dan diuji, bukan sekadar niat. (§IV–V)

5. **Daftar bunuh/arsipkan** (obsolete, redundan, atau menyesatkan agent sesi berikutnya): EKSEKUSI sebagai dokumen status, CLAUDE.md yang basi, limbo Paper 1, branch name `autoresearch/*` yang sudah tidak mendeskripsikan pekerjaan, dan datasheet korpus yang menjanjikan Zenodo DOI tapi tidak pernah dirilis. (§VI)

---

## I. KRITIK STRUKTURAL TERBESAR: PETA KAUSAL YANG HILANG

### Masalahnya

Manifesto bertanya: *mengapa sistem gagal menghentikan korupsi?* Dalam kerangka Becker (yang sudah dipakai Paper 4 §2.2), jawaban komputasionalnya adalah **expected sanction**:

```
E[sanksi] = P(deteksi) × P(dituntut | deteksi) × P(divonis | dituntut) × severity(| divonis)
```

Korpus putusan — MA maupun PN — hanya mengukur **term terakhir**. Paper 4 sudah membuktikan term itu flat terhadap kerugian (elasticity 0.126). Itu temuan bagus. Tapi tiga term pertama — yang menurut literatur deterrence justru lebih menentukan (certainty > severity) — **tidak ada di data putusan dan tidak akan pernah ada di sana**. D4 (Kegelapan Seleksi) di manifesto sudah menyatakan ini sejak awal; eksekusinya tidak pernah menggambar konsekuensinya.

Inilah sumber ketidakpuasan Anda. Bukan karena teknik NLP-nya kurang canggih — 36 eksperimen autoresearch sudah membuktikan teknik bukan bottleneck-nya. Melainkan karena **setiap paper baru dari korpus yang sama hanya menambah resolusi pada satu term, sementara pertanyaan manifesto butuh keempat term**.

### Rekomendasi: MAP.md (setengah hari kerja)

Buat satu artefak satu halaman: model kausal persistensi korupsi dengan edge eksplisit, dan untuk setiap edge — sumber data yang bisa mengidentifikasinya, status (terukur / bisa diukur / tidak akan pernah terukur dari data publik):

| Term | Data yang mengidentifikasi | Status |
|---|---|---|
| severity(\|divonis) | Korpus MA (+PN untuk fix seleksi kasasi) | **TERUKUR** — Paper 4 |
| P(divonis\|dituntut) | Putusan bebas/lepas + statistik banding | Sebagian (amar di DB) |
| P(dituntut\|deteksi) | Laporan tahunan KPK/Kejagung, data ICW, SIPP | **BELUM DISENTUH** — feasible |
| P(deteksi) | Tidak observable langsung; proxy: temuan BPK→kasus, anomali procurement→kasus | Batu 2/3 manifesto — belum disentuh |

Aturan main baru: **setiap analisis baru harus menyebutkan edge mana yang diidentifikasinya SEBELUM dijalankan.** Kalau tidak bisa menyebutkan, itu streetlight drift.

### Konsekuensi untuk prioritas data

- **Scraping PN** = memperbaiki identifikasi term yang SUDAH terukur (fix confound kasasi Papers 3 & 4). Layak, sudah direncanakan, lanjutkan — dengan gate fail-fast (§VII).
- **Data atrisi/funnel** (statistik penindakan KPK per tahun per daerah, tabulasi ICW, jumlah perkara masuk vs putus) = mengukur term yang BELUM PERNAH terukur. Effort-nya jauh lebih kecil dari scraping PN (data agregat, bukan ratusan ribu PDF), dan inilah yang menjawab "mengapa" secara langsung: kalau P(deteksi)×P(dituntut) ternyata di orde 10⁻³–10⁻⁴ DAN severity flat, maka "mengapa korupsi tidak berhenti" punya jawaban kuantitatif lengkap pertama untuk Indonesia — expected sanction untuk mega-korupsi mendekati nol dari DUA arah. Itu paper yang menyatukan seluruh program dan tidak bisa ditulis oleh kriminolog manapun tanpa korpus Anda.
- **Anti-scope rule** (karena metafora "batu" mengundang akumulasi): maksimum SATU sumber data baru per tahun, dipilih berdasarkan edge di MAP.md, bukan berdasarkan ketersediaan CSV.

---

## II. PAPER 4 — TIGA RISIKO TEKNIS PRA-SUBMIT

Paper 4 secara keseluruhan jauh lebih kuat dari Paper 2: pertanyaannya lebih orisinal, framing komparatifnya cerdas, robustness table-nya rapi. Justru karena statusnya flagship, tiga hal ini harus beres dulu.

### II.1 Benchmark AS: table-implied vs realized (RISIKO TERTINGGI — bisa mematikan headline)

Klaim sentral abstrak: elasticity Indonesia 0.126 ≈ "roughly half" dari AS (0.25–0.30). Tapi angka AS itu **diturunkan dari tabel guideline §2B1.1** — apa yang *seharusnya* terjadi jika hakim mengikuti tabel. Elasticity yang *terealisasi* di pengadilan AS hampir pasti lebih rendah: USSC sendiri melaporkan mayoritas kasus economic crime disentence **di bawah** guideline range, dan departure ke bawah paling besar justru di kasus loss tinggi (kritik Rakoff dkk.; amandemen fraud 2015; proposal reformasi Des 2025 yang paper ini sendiri kutip). Jika elasticity riil AS ≈ 0.13–0.18, perbandingannya berubah dari "Indonesia setengah dari AS" menjadi "Indonesia setara dengan AS" — dan headline mati.

**Perbaikan** (setengah hari): hitung atau cari elasticity terealisasi AS dari data USSC (Interactive Data Analyzer / Sourcebook; sentence length × loss amount tersedia agregat). Dua kemungkinan hasil, dua-duanya OK:
- Realized AS tetap > Indonesia → klaim bertahan, dan paper jadi KEBAL terhadap serangan ini karena membandingkan realized-to-realized.
- Realized AS ≈ Indonesia → headline diganti: "bahkan sistem dengan loss table eksplisit gagal menggraduasi hukuman — Indonesia mencapai kegagalan yang sama tanpa pernah mencoba." Masih publishable, lebih jujur, dan sebenarnya lebih menarik secara teoretis (unstructured discretion konvergen ke hasil yang sama dengan structured discretion yang dilanggar).

Jangan submit sebelum tahu berada di cabang yang mana.

### II.2 R² 0.315 vs 0.600: perbandingan yang tidak sahih (RISIKO SEDANG — fix 1 jam)

§4.2 dan §5.3 menyimpulkan "prosecutors exercise wider discretion than judges" dari membandingkan:
- `tuntutan ~ log(kerugian) + pasal + tahun` → R²=0.315 (prediktor: **fakta perkara**)
- `vonis ~ tuntutan` → R²=0.600 (prediktor: **anchor prosedural**, bukan fakta perkara)

Ini membandingkan dua hal berbeda. Vonis terlihat "predictable" karena hakim menyalin tuntutan — bukan karena hakim lebih disiplin terhadap fakta perkara. Perbandingan yang fair: jalankan `vonis ~ log(kerugian) + pasal + tahun` (tanpa tuntutan). Hampir pasti R²-nya ≈ 0.25–0.32, setara dengan tuntutan.

**Dan itu justru MEMPERKUAT tesis paper**: diskresi masuk ke sistem SEKALI, di hulu; hakim tidak menambah maupun mengoreksi. Kalimat yang benar bukan "prosecutors less predictable than judges" melainkan "conditional on case facts, demands and sentences are equally unpredictable; conditional on the demand, sentences are highly predictable — discretion enters once, upstream." Satu regresi tambahan, satu paragraf ditulis ulang, klaim jadi kebal.

### II.3 Attenuation bias dari measurement error kerugian (RISIKO SEDANG — fix 1–2 jam)

Kerugian negara diukur dengan error besar (BPK vs BPKP vs estimasi penuntut bisa beda orde; Rp 300T PT Timah memuat Rp 271T kerugian lingkungan — konstruk yang contested). Classical measurement error pada regressor log-log membias elasticity **ke arah nol** — sebagian "kompresi" bisa jadi artefak errors-in-variables. Dan benchmark AS (tabel) tidak punya measurement error, jadi perbandingannya asimetris.

Pembelaannya kuat dan bisa dihitung: dengan rentang 7+ orde magnitude, var(log kerugian) sangat besar, sehingga reliability ratio tetap tinggi kecuali error-nya sendiri berorde magnitude. Contoh: error SD 0.5 log10 (salah 3×) hanya mengattenuasi ~10%; untuk menjelaskan gap 0.13→0.25 dibutuhkan error SD > 1.5 log10 (salah 30×) — tidak plausible untuk mayoritas kasus. **Tulis paragraf sensitivitas ini di §5.** Tanpa paragraf itu, reviewer ekonometri melempar kritik ini dan Anda tidak punya jawaban tertulis; dengan paragraf itu, kritik terjawab sebelum diajukan.

### II.4 Dua disclosure kecil (masing-masing 2 kalimat)

- **Seleksi ke kasasi**: elasticity di level MA ≠ elasticity di tahap penuntutan jika probabilitas kasasi berkorelasi dengan loss dan tuntutan (collider). Sudah diketahui (justifikasi scraping PN), pastikan limitation §5 menyatakannya eksplisit dengan arah bias yang tidak diketahui.
- **Seleksi subsampel kerugian**: n=290 hanya kasus dengan kerugian terdokumentasi (kasus embezzlement-type); kasus gratifikasi/suap (tanpa kerugian) tersisih — dan datasheet mencatat kasus tanpa kerugian punya vonis lebih rendah (3.67 vs 4.92 thn, p=0.002). Elasticity berlaku untuk populasi "korupsi dengan kerugian negara terukur," bukan semua korupsi.

---

## III. AUDIT REPO — FAKTA YANG MENGGEROGOTI KREDIBILITAS DIAM-DIAM

Temuan audit langsung (DB, file, git), diurutkan berdasarkan bahaya:

### III.1 Golden set: fondasi semua angka, tervalidasi n=5 untuk field kunci

`golden_20_verified.csv`: `vonis_bulan` 20/20 benar. Tapi `tuntutan_bulan`, `kerugian_negara`, `daerah`, `tahun`, `nama` hanya dianotasi pada **5 dari 20 baris** (5/5 benar). Elasticity 0.126 = fungsi dari extractor tuntutan dan kerugian — dua-duanya divalidasi pada LIMA kasus. `extract_vonis_bulan` punya cascade 8 strategi dengan fallback window karakter tetap; extractor kerugian memilih satu angka dari teks yang sering memuat beberapa angka kerugian berbeda.

**Fix (1–2 hari, prioritas di atas submit Paper 4):** ekspansi golden set ke 50 kasus stratified (per periode, per rentang kerugian, per parse_source html/pdf), anotasi SEMUA field, laporkan per-field accuracy + CI di paper. Bisa pakai LLM sebagai second coder dengan adjudikasi manual pada disagreement — murah dan menghasilkan inter-coder agreement yang bisa dilaporkan.

### III.2 Jejak eksperimen negatif tidak lengkap — dan sedikit kontradiktif

- `results.tsv` (gitignored!) memuat **34 baris**, semuanya era TF-IDF (9 April). EKSEKUSI mengklaim "36 eksperimen." Eksperimen pasca-pivot ke binary domain features (10 April, yang menghasilkan klaim p=0.002 di Paper 2) **tidak pernah dicatat** di results.tsv.
- Best val_r2 di results.tsv = **0.6256** — sedikit DI ATAS baseline 0.600. "Decisive negative — semua gagal" di EKSEKUSI tidak persis cocok dengan lognya sendiri. Kemungkinan besar 0.626 vs 0.600 tidak signifikan (dan itulah interpretasi yang benar) — tapi klaim negatif yang dikutip di paper harus bisa ditelusuri ke log yang lengkap dan konsisten.

**Fix (1 jam):** un-gitignore results.tsv (ini artefak riset, bukan data mentah), tambahkan baris eksperimen pasca-pivot secara retrospektif dari git history, dan satu catatan yang merekonsiliasi 0.6256-vs-0.600 (uji signifikansi delta, atau nyatakan tidak stabil antar split).

### III.3 Angka korpus tidak punya versi beku

Papers memakai n=367/290/291; datasheet memakai 557; DB live sekarang **693** (639 MA, 430 pertimbangan). Tidak ada artefak beku yang bisa dirujuk — setiap scraping baru mengubah "korpus" yang dikutip paper yang sudah di SSRN.

**Fix (setengah hari):** bekukan `corpus_v1.0.csv` + hash + git tag; semua paper mengutip versi beku. Scraping berikutnya menghasilkan v1.1. Ini prasyarat rilis Zenodo (§VI.5) sekaligus menyelesaikan kekacauan n.

### III.4 Kebersihan kecil yang menyesatkan agent sesi berikutnya

- **CLAUDE.md basi** (masih "Paper 1 submission-ready", "scripts/01-09" padahal ada 18 skrip dengan nomor tabrakan 10/10 dan 11/11). CLAUDE.md adalah dokumen dengan leverage tertinggi di repo — SETIAP sesi agent membacanya. Dokumen basi = setiap sesi mulai dengan model dunia yang salah. Update 10 baris.
- `date_decided` di DB berisi teks Indonesia mentah + mojibake (`max='�'`) — tidak terdokumentasi di mana pun; analisis bergantung pada `tahun`. Satu baris di datasheet.
- Branch `autoresearch/apr9-textfeatures` sudah 3 bulan tidak mendeskripsikan pekerjaan (paper-writing, bukan autoresearch). Merge ke main atau rename.

---

## IV. ARSITEKTUR KOLABORASI HUMAN–AI: EMPAT MODE KEGAGALAN TERDOKUMENTASI

Ini bukan risiko hipotetis — keempatnya SUDAH TERJADI dan tercatat di repo ini:

| # | Mode kegagalan | Insiden nyata | Akar |
|---|---|---|---|
| F1 | **State-transfer failure** — fakta eksternal terkorupsi antar sesi | Handoff session 15 mencatat Paper 2 "under review" padahal desk-rejected (HANDOFF 16 baris 9 mengakuinya) | Status eksternal disimpan sebagai prosa naratif, tanpa verifikasi terhadap sumber (email) |
| F2 | **Critique-decay** — kritik di-file lalu mati diam-diam | Warning session 14 ("R²=0.60 normal global"; "gap manifesto↔riset") diabaikan; 4 paper diproduksi dari korpus yang sama | Kritik tidak punya status blocking; mengabaikan tidak butuh keputusan eksplisit |
| F3 | **Wrong optimization target** — review internal mengoptimasi target yang salah | Review "thesis-killer" mengoptimasi "apakah reviewer menemukan lubang metodologis" — editor menolak dengan pertanyaan berbeda: "apakah kontribusinya cukup" | Framework seleksi kritik session 13 bertanya "WHO will notice?" — pemodelan lawan, bukan pencarian kebenaran |
| F4 | **Streetlight drift** — kenyamanan data menentukan pertanyaan | Portofolio menjawab "HOW judges sentence" (data mudah) bukan "WHY corruption persists" (pertanyaan manifesto) | Tidak ada mekanisme yang memaksa setiap analisis menyatakan posisinya terhadap pertanyaan manifesto |

### Perbaikan yang dimekanisasi (bukan niat, tapi artefak + ritual)

- **F1 → `SUBMISSIONS.md` (ledger, bukan prosa):** satu baris per submission: tanggal, venue, status, **kutipan verbatim email keputusan**, tanggal verifikasi terakhir. Ritual awal sesi: agent membaca ledger dan meminta user mengonfirmasi status yang berumur >2 minggu terhadap inbox email. Handoff naratif tidak boleh jadi satu-satunya pembawa fakta eksternal.
- **F2 → `DECISIONS.md`:** setiap kritik (internal maupun review saya ini) berakhir di salah satu dari tiga status eksplisit: **FIXED / DISCLOSED (sebagai limitation) / REJECTED dengan alasan tertulis + tanggal revisit**. Tidak ada status keempat "dibaca lalu menguap." Session 14 warning mati karena silence itu legal; buat silence ilegal.
- **F3 → pisahkan tiga review dengan target berbeda** (§V): Truth review, Contribution review, Reception review. Yang menewaskan Paper 2 adalah tidak adanya Contribution review yang independen.
- **F4 → MAP.md** (§I): analisis baru wajib menyebut edge kausalnya sebelum dijalankan.

### Asimetri kapabilitas: sedang dipakai TERBALIK

Konfigurasi sekarang: agent mengerjakan statistik + penulisan + kritik-diri + framework triase kritiknya sendiri (loop tertutup epistemik — error-nya berkorelasi). Human me-review arah dan... menyetujui. Sementara **keunggulan komparatif human yang tidak bisa direplikasi agent manapun justru kosong**:

1. **Merekrut satu co-author hukum pidana** (UB satu kota dengan Anda; UMM; Unair) — sudah 4 sesi jadi "next action," belum ada satu email pun terkirim. Ini blind spot yang PERSIS diekspos desk-reject.
2. **Satu percakapan dengan mantan jaksa/hakim tipikor** — pertanyaan §5.1 Paper 4 ("mengapa tuntutan inelastis: kultur tuntutan Kejaksaan? insentif target-conviction? asimetri terhadap terdakwa berkuasa?") tidak bisa dijawab dari data mana pun, tapi bisa dijawab dari satu jam kopi di Malang.
3. **Membaca 10 putusan secara close-reading** — Anda satu-satunya anggota tim yang membaca bahasa hukum Indonesia secara natif dengan konteks institusional. Sepuluh putusan dibaca manusia bisa menghasilkan hipotesis yang 693 putusan yang di-regresi tidak akan pernah munculkan.

Aturan alokasi baru: **jam kerja human hanya untuk yang agent tidak bisa: relasi eksternal, interpretasi institusional, keputusan klaim, submit.** Semua yang lain (kode, literatur, draft, robustness) delegasikan penuh.

### Variasi kapabilitas agent antar sesi

Model dan konteks berbeda antar sesi; kualitas handoff adalah single point of failure (terbukti oleh F1). Mitigasi: fakta keras hidup di ledger yang machine-checkable (SUBMISSIONS.md, GATES.md, results.tsv, corpus version tag), bukan di prosa handoff. Handoff tetap untuk narasi dan konteks; ledger untuk fakta. Sesi mana pun, model apa pun, bisa memverifikasi ledger dalam satu menit.

---

## V. FRAMEWORK TESTING BERLAPIS (agent–agent, agent–human, human–human)

Piramida untuk program riset (bukan cuma kode), dengan status sekarang:

| Layer | Menguji | Status | Aksi |
|---|---|---|---|
| **L0 Kode** | Extractor benar secara sintaktik | ✅ pytest 69 passed | Pertahankan; tambah test untuk setiap bug parser baru |
| **L1 Ekstraksi** | Parser benar terhadap ground truth | 🔴 n=5 untuk field kunci | Golden set 50 stratified, semua field, second coder (§III.1) |
| **L2 Statistik** | Temuan robust terhadap spesifikasi | 🟡 Battery bagus (Cook's d, LOO, placebo, HC3, quantile) | Tambah **specification curve** untuk klaim flagship: satu skrip, semua spesifikasi defensible, distribusi elasticity — mematikan kritik garden-of-forking-paths sebelum diajukan |
| **L3 Identifikasi** | Klaim kausal/mekanisme valid | 🔴 Ad-hoc (endogeneity Paper 2 baru dibahas setelah dikritik) | **Threat table** per paper: ancaman → arah bias → mitigasi → status OPEN/CLOSED. Paper tidak submit dengan threat OPEN yang tidak di-disclose |
| **L4 Kontribusi** | Layak menembus gatekeeper | 🔴 Inilah yang gagal di Paper 2 | **Gate kontribusi** per paper (di GATES.md): (a) klaim novelty 1 kalimat + 3 paper terdekat + mengapa berbeda; (b) sinyal eksternal ≥1 (download/komentar SSRN, balasan email penulis paper terdekat, opini kolega); (c) editor-simulation: sesi agent SEGAR tanpa akses ke pembelaan paper, diberi HANYA abstrak + cover letter + scope statement jurnal, ditanya satu hal: "would you send this to review?" |
| **L5 Eksternal-human** | Manusia selain PI membaca | 🔴 0 manusia eksternal pernah membaca paper yang disubmit | Gate biner: ≥1 pembaca eksternal sebelum submit. Rilis dataset (§VI.5) adalah saluran termurah |

**Aturan klasifikasi kegagalan** (mindset regression-test untuk riset): setiap kegagalan yang lolos sampai gatekeeper eksternal WAJIB melahirkan satu check baru di layer yang melewatkannya, dicatat di DECISIONS.md. Desk-reject Paper 2 = kegagalan L4 → gate L4 lahir. Kalau AJC menolak Paper 4 dengan alasan yang review ini sudah sebutkan, itu kegagalan proses, bukan kegagalan nasib.

**Testing agent–agent**: saat memakai multi-review, verdicts harus dihasilkan **tanpa konteks bersama** (fresh session, tidak melihat jawaban satu sama lain). Kesepakatan antar agent yang berbagi konteks hampir tidak bernilai (prior yang sama); **disagreement antar agent independen adalah sinyal yang paling layak dibaca manusia.**

**Metrik kesehatan proses** (lihat tiap 5 sesi): jumlah gate merah per paper, umur kritik OPEN tertua, rasio submit→desk-reject, jumlah pembaca eksternal kumulatif, rasio jam-human di zona "hanya-human-bisa."

---

## VI. MEKANISME SELEKSI KRITIK (upgrade dari session 13)

Framework session 13 ("WHO will notice? berapa effort?") adalah triase **resepsi** — dan bekerja untuk tujuannya, tapi dia MELOLOSKAN kegagalan Paper 2 karena novelty-gap bukan sesuatu yang "reviewer notice"; itu sesuatu yang membuat klaim tidak layak. Upgrade: **klasifikasi dulu, baru triase.**

```
Kritik masuk → klasifikasi:

[T] TRUTH-CRITIQUE — menyangkut apakah klaim BENAR
    (identifikasi, measurement, integritas data, validitas benchmark)
    → TIDAK BOLEH di-ignore dengan alasan effort/siapa-yang-lihat.
      Hanya 3 jalan keluar: FIX / DISCLOSE sebagai limitation / KILL klaimnya.

[C] CONTRIBUTION-CRITIQUE — menyangkut apakah klaim PENTING
    (novelty, positioning, "so what")
    → Diadili oleh sinyal EKSTERNAL, bukan oleh dyad human-AI yang sama
      yang menghasilkan papernya. (Pelajaran Paper 2.)

[R] RECEPTION-CRITIQUE — menyangkut bagaimana klaim DITERIMA
    (framing, format, venue, gaya)
    → Triase ROI ala session 13. Boleh di-ignore. 

Aturan tambahan: setiap IGNORE/REJECT ditulis di DECISIONS.md dengan
alasan + tanggal revisit. Mengabaikan boleh; mengabaikan DIAM-DIAM tidak.
```

### Makan masakan sendiri: klasifikasi kritik-kritik review INI

| Kritik | Kelas | Rekomendasi | Effort |
|---|---|---|---|
| Benchmark AS table vs realized (II.1) | **T** | FIX sebelum submit | 0.5 hari |
| R² apples-oranges (II.2) | **T** | FIX sebelum submit | 1 jam |
| Attenuation bias (II.3) | **T** | DISCLOSE (paragraf sensitivitas) | 1–2 jam |
| Golden set n=5 (III.1) | **T** | FIX sebelum submit | 1–2 hari |
| Seleksi kasasi + subsampel kerugian (II.4) | **T** | DISCLOSE | 30 menit |
| results.tsv tidak lengkap (III.2) | **T** | FIX | 1 jam |
| Peta kausal hilang (§I) | **C** | FIX (MAP.md) — ini akar ketidakpuasan Anda | 0.5 hari |
| Funnel/atrisi sebagai batu berikutnya (§I) | **C** | PLAN — jangan mulai sebelum Paper 4 terkirim | — |
| Ledger F1–F4 (§IV) | proses | FIX (3 file, sekali buat) | 1–2 jam |
| Editor-simulation gate (§V) | proses | ADOPT untuk Paper 4 sebelum submit | 1 sesi |
| CLAUDE.md/branch/EKSEKUSI basi (III.4, VII) | higiene | FIX | 1 jam |
| Corpus freeze + Zenodo (III.3, VII) | **C**+etika | FIX — janji manifesto E4 yang belum ditepati | 0.5–1 hari |
| Rekrut kolaborator + percakapan jaksa (§IV) | **C** | HANYA-HUMAN — tidak bisa saya kerjakan | jam kopi |

Perhatikan: TIDAK ADA kritik [T] di atas yang butuh lebih dari 2 hari. Total jalan menuju "Paper 4 layak submit dengan standar yang tidak akan mengulang Paper 2" ≈ **4–6 hari kerja agent + 1 keputusan human.**

---

## VII. DAFTAR BUNUH / SEDERHANAKAN / PERTAHANKAN

### Bunuh / arsipkan (tanpa merusak kolaborasi aktif)

1. **EKSEKUSI sebagai dokumen status** — sudah dua kali basi meski sudah dua kali diingatkan (session 13 memperingatkan; diupdate sekali; basi lagi — statusnya masih pra-desk-reject). Dua dokumen status = satu terlalu banyak, terbukti empiris. Arsipkan sebagai dokumen historis; HANDOFF.md + ledger = satu-satunya sumber status. Bagian EKSEKUSI yang masih hidup (prinsip eksekusi, kriteria falsifikasi) sudah terduplikasi di manifesto.
2. **Paper 1 (35k kata)** — 3 bulan di limbo "needs restructuring." Putuskan SEKALI: ekstrak dataset descriptor 3–4k kata (jadi companion rilis Zenodo, target *Data in Brief*/*Scientific Data*), arsipkan sisanya sebagai laporan teknis SSRN. Berhenti membawanya sebagai beban kognitif.
3. **Paper 5** — sudah divonis "weakest novelty" di triase sendiri. SSRN, park, stop.
4. **Branch name + framework autoresearch** — framework sudah menunaikan tugasnya (negative result terdokumentasi… setelah results.tsv dilengkapi, §III.2). Arsipkan, merge branch ke main. Jangan hapus kodenya — desainnya bagus dan reusable untuk korpus PN nanti (di situ n-nya akan cukup untuk text mining).
5. **Hipotesis manifesto**: tandai status di MAP.md — H2 FALSIFIED (temuan sah!), H1 sebagian terjawab, H3 belum, H4 belum, H5–H6 TIDAK IDENTIFIABLE dari data putusan saja (butuh funnel/struktural). Manifesto tidak diubah (dia konstitusi); yang diubah adalah kejujuran eksekusi tentang hipotesis mana yang hidup.

### Sederhanakan

6. **CLAUDE.md** — update ke realitas (18 skrip, status paper, PN belum ada). 10 baris.
7. **Nomor skrip tabrakan** (dua `10_`, dua `11_`) — rename sekali, selesai.

### Pertahankan — jangan disentuh

8. **Manifesto** — dokumen inspirasi yang bagus, dan bagian VI (batasan) + VII (etika) lebih jujur daripada rata-rata paper yang terbit. Biarkan.
9. **Ritual HANDOFF antar sesi** — F1 diperbaiki dengan ledger, bukan dengan membuang handoff.
10. **Robustness battery scripts 12/18** — aset nyata, jadikan template untuk semua paper berikutnya.
11. **Kebijakan submit sekuensial + SSRN-first** — benar, jangan dilonggarkan.
12. **Prinsip fail-fast yang sudah bekerja** — pembunuhan Darkness Index dan reposisi Paper 3 adalah contoh proses yang SEHAT. Program ini bisa membunuh idenya sendiri; itu jarang dan berharga.

### Satu janji manifesto yang belum ditepati

13. **E4 Keterbukaan Radikal**: datasheet v1.0 sudah ditulis (bagus, mengikuti Gebru et al.) tapi **korpus tidak pernah dirilis** — tidak ada DOI, tidak ada repo publik, dan angka datasheet sudah basi (557 vs 693). Rilis `corpus_v1.0` beku ke Zenodo adalah: janji manifesto, artefak citeable, magnet kolaborator, saluran QA eksternal gratis, DAN pembeda kredibilitas di mata editor AJC ("data and code openly available at DOI..."). Setengah hari kerja. Ini item dengan rasio dampak/effort tertinggi kedua setelah fix golden set.

---

## VIII. URUTAN EKSEKUSI YANG DIREKOMENDASIKAN

**Fase A — de-risk flagship (4–6 hari agent, sebelum submit AJC):**
1. Golden set 50 stratified + per-field accuracy (III.1)
2. Benchmark AS realized (II.1) → tentukan headline
3. Regresi `vonis ~ fakta perkara` + tulis ulang §4.2/§5.3 (II.2)
4. Paragraf attenuation + 2 disclosure (II.3, II.4)
5. Corpus freeze v1.0 + rilis Zenodo + update datasheet (III.3, VII.13)
6. Editor-simulation gate pada draft final (§V)
7. Submit AJC (human)

**Fase B — infrastruktur proses (1 sesi, boleh paralel dengan A):**
8. MAP.md + GATES.md + DECISIONS.md + SUBMISSIONS.md
9. Higiene: CLAUDE.md, results.tsv, branch, arsip EKSEKUSI, rename skrip

**Fase C — hanya-human (paralel, tanpa deadline tapi dengan komitmen):**
10. Satu email rekrutmen co-author hukum pidana (UB/UMM/Unair)
11. Satu percakapan mantan jaksa/hakim tipikor untuk §5.1
12. Kirim abstrak Paper 4 ke 2–3 penulis paper terdekat (Brazil/China corruption sentencing) — sinyal eksternal L4

**Fase D — batu berikutnya (setelah Paper 4 terkirim):**
13. Gate feasibility PN: 2 minggu, 1 pengadilan, 100 putusan, kill criteria ditulis SEBELUM mulai (parse rate tuntutan+kerugian+mitigating ≥60% atau bunuh/redesign)
14. Scoping data funnel/atrisi (KPK/ICW/SIPP) — batu yang menjawab "MENGAPA"

---

## IX. CATATAN PENUTUP

Program ini TIDAK sakit. Dalam 3.5 bulan: 693 putusan, pipeline tervalidasi (walau tipis), 5 draft, 2 preprint SSRN, satu desk-reject yang direspons dengan reframe yang benar, dan dua ide yang berhasil dibunuh cepat. Itu output yang sangat sehat untuk satu orang + satu agent.

Yang sakit adalah tiga hal yang lebih halus: (1) **fondasi ekstraksi lebih tipis daripada bangunan di atasnya** — golden set n=5 menopang elasticity yang mau dikirim ke jurnal Q1; (2) **loop epistemik tertutup** — generator, kritikus, dan hakim triase kritik adalah entitas yang sama, dan mekanisme eksternalnya (kolaborator, rilis data, sinyal komunitas) semuanya masih di kolom "rencana"; (3) **pertanyaan manifesto belum punya peta** — sehingga setiap sesi eksplorasi berisiko menghasilkan batu dari tambang yang sama, bukan batu dari bagian gunung yang belum tersentuh.

Ketiganya murah untuk diperbaiki. Tidak ada yang butuh pivot dramatis. "Santai dalam waktu, serius dalam standar ilmiah" — versi operasionalnya untuk 3 bulan ke depan: **satu paper (Paper 4) yang melewati gate yang tidak dilewati Paper 2, satu dataset publik ber-DOI, satu co-author manusia, satu peta kausal.** Empat artefak itu lebih memindahkan gunung daripada lima draft berikutnya dari korpus yang sama.

---

*Review: Session 17, 7 Juli 2026 — Claude (mode system/research designer, adversarial)*
*Untuk: Mukhlis Amien, PI KorupsiNLP*
*Status kritik: menunggu triase user via mekanisme §VI — setiap butir berakhir FIXED / DISCLOSED / REJECTED-dengan-alasan di DECISIONS.md*
