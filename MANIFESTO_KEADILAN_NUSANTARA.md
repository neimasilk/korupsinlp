# MANIFESTO KEADILAN NUSANTARA
## Memindahkan Gunung, Satu Batu pada Satu Waktu
### *Moving the Mountain*

*"Korupsi di Indonesia adalah gunung. Tidak ada satu orang yang bisa memindahkannya. Tapi setiap batu yang dipindahkan — setiap dataset yang dibuka, setiap pola yang ditemukan, setiap paper yang diterbitkan — membuat gunung itu sedikit lebih kecil, sedikit lebih terlihat, sedikit lebih sulit untuk dipertahankan oleh mereka yang hidup dari keberadaannya."*

---

**Penulis**: Mukhlis Amien
**Dimulai**: 18 Maret 2026
**Status**: Konstitusi — stabil, jarang berubah. **Amandemen 1: 16 Juli 2026** (lihat §XII)
**Eksekusi**: Lihat `ROADMAP.md` (peta jalan gate-driven) dan ledger: `SUBMISSIONS.md`, `GATES.md`, `DECISIONS.md`, `MAP.md`

---

## I. KEGELISAHAN

Saya tinggal di Malang. Saya dosen. Saya mengurus DUPAK, mengisi BKD, mengajar mata kuliah yang kurikulumnya ditentukan oleh birokrasi yang saya tidak selalu pahami logikanya. Saya hidup di dalam sistem yang digerakkan oleh anggaran negara — dan saya tahu, secara statistik, bahwa sebagian dari anggaran itu dicuri sebelum sampai ke tujuannya.

Ini bukan abstraksi. Ini konkret:

- Jalan di depan kampus yang berlubang karena anggaran perbaikan "menguap"
- Dana penelitian dosen yang prosesnya lebih rumit dari penelitiannya sendiri — karena setiap rupiah harus dijaga dari tangan yang ingin mengambilnya
- Mahasiswa yang lulus dan masuk birokrasi, lalu dalam 5 tahun menjadi bagian dari sistem yang sama
- Berita korupsi setiap hari di media — kepala daerah, hakim, jaksa, polisi, anggota DPR, menteri — lalu kita scroll ke bawah dan lupa

Yang membuat saya gelisah bukan bahwa korupsi ada. Semua orang tahu itu. Yang membuat saya gelisah adalah: **kita tidak tahu MENGAPA ia tidak berhenti.**

Bukan "mengapa orang korupsi" — itu pertanyaan psikologi yang jawabannya sederhana: karena bisa, karena insentifnya besar, karena risikonya kecil. Yang saya maksud lebih dalam dari itu:

**Mengapa SISTEM ini — dengan KPK, dengan pengadilan tipikor, dengan UU Tipikor, dengan reformasi birokrasi, dengan e-government, dengan semua upaya 25 tahun pasca-Reformasi — masih GAGAL menghentikan korupsi?**

Jawaban standar: "mentalitas," "budaya," "kurang hukuman." Tapi ini bukan jawaban. Ini pengakuan bahwa kita tidak tahu jawabannya.

Jawaban yang sesungguhnya tersembunyi di dalam data — data yang sudah ada, tersedia secara publik, tapi tidak pernah ada yang membacanya secara sistematis. Dan bukan hanya satu sumber data. Data itu tersebar: di ratusan ribu putusan pengadilan, di laporan audit BPK, di data APBD, di LHKPN pejabat, di catatan pengadaan barang/jasa, di statistik kriminal BPS. Setiap sumber hanya sepotong kecil. Tidak ada yang pernah merakitnya menjadi satu gambar utuh.

---

## II. TESIS

**Korupsi di Indonesia bukan masalah yang kekurangan opini. Ia kekurangan DATA — data yang diolah secara sistematis, komputasional, pada skala yang tidak mungkin dilakukan oleh manusia.**

Indonesia sesungguhnya kaya data tentang korupsinya sendiri. Putusan pengadilan dipublikasikan. Audit BPK terbuka. APBD bisa diakses. LHKPN pejabat tersedia. Tapi data-data ini:
- Tidak pernah dianalisis pada skala penuh
- Tidak pernah dihubungkan satu sama lain
- Tidak pernah ditanya dengan pertanyaan yang tepat oleh mesin yang bisa membaca semuanya sekaligus

Manifesto ini adalah deklarasi bahwa **seorang dosen teknik informatika di Malang bisa — dan akan — mulai membaca data itu dengan mesin.** Bukan untuk memberantas korupsi sendiri. Itu pekerjaan seumur hidup seluruh bangsa. Tapi untuk **menyediakan alat diagnostik** — agar kita tahu persis di mana penyakitnya, seberapa parahnya, dan apakah obat yang sudah diberikan selama 25 tahun terakhir benar-benar bekerja.

Kita tidak bisa menyembuhkan apa yang tidak bisa kita ukur.

Korupsi adalah gunung. Manifesto ini adalah komitmen untuk memindahkan gunung itu — **satu batu pada satu waktu.**

---

## III. GUNUNG DAN BATU-BATUNYA

### Gunung: Korupsi di Indonesia

Gunung ini terlalu besar untuk satu orang, satu proyek, atau satu generasi. Tapi gunung ini bisa dipetakan, diukur, dan dipindahkan — batu demi batu.

### Batu-batu yang bisa dipindahkan:

Setiap "batu" adalah satu proyek riset yang mandiri, publishable, dan berkontribusi pada pemahaman yang lebih utuh tentang gunung. Beberapa batu yang sudah teridentifikasi:

**Batu 1: Putusan Pengadilan Korupsi** *(batu pertama — sedang dikerjakan)*
Ratusan ribu putusan tipikor tersedia di Direktori Putusan Mahkamah Agung. Belum pernah dianalisis secara komputasional pada skala penuh. Di dalamnya tersembunyi pola: proporsionalitas vonis, disparitas geografis, bahasa hakim, jaringan aktor. → Lihat `ROADMAP.md`
*Status eksekusi (Amandemen 1): korpus v1 = 693 putusan tingkat MA — bukan "ratusan ribu". Angka itu deskripsi direktori dan aspirasi program, bukan pencapaian. Jalan ke skala sesungguhnya: putusan tingkat pertama (PN). Sampai itu ditempuh, novelty program bukan skala — ia adalah korpus machine-readable pertama dan pengukuran kuantitatif pertama atas proporsionalitas penuntutan-vonis untuk korupsi Indonesia.*

**Batu 2: Data Audit BPK**
BPK menerbitkan laporan audit keuangan daerah setiap tahun. Opini WTP, WDP, TMP, TW — dan catatan temuan audit. Belum pernah ada yang menghubungkan temuan audit BPK dengan kasus korupsi yang kemudian muncul dari daerah yang sama.

**Batu 3: Data APBD dan Pengadaan**
APBD per kabupaten tersedia dari DJPK Kemenkeu. Data pengadaan barang/jasa tersedia di LPSE. Pola anomali dalam pengadaan (harga markup, pemenang yang sama berulang, tender yang terlalu cepat) bisa dideteksi secara komputasional.

**Batu 4: LHKPN dan Kekayaan Pejabat**
Laporan Harta Kekayaan Penyelenggara Negara tersedia di KPK. Pertumbuhan kekayaan yang tidak proporsional terhadap gaji adalah sinyal. Belum pernah dianalisis secara sistematis pada skala penuh.

**Batu 5: Data Struktural — Resource Curse, Biaya Politik, Ketergantungan Fiskal**
Korupsi bukan fenomena acak. Ia berkorelasi dengan struktur ekonomi (daerah kaya SDA), struktur politik (biaya Pilkada), dan struktur fiskal (ketergantungan pada dana transfer). Menghubungkan data BPS/DJPK/KPU dengan data korupsi bisa menghasilkan "Corruption Darkness Index" — peta di mana korupsi kemungkinan tersembunyi.

**Batu-batu yang belum teridentifikasi:**
Manifesto ini tidak berpura-pura tahu semua batu yang harus dipindahkan. Seiring riset berjalan, batu-batu baru akan muncul. Mungkin dari data media sosial. Mungkin dari data perizinan. Mungkin dari sumber yang hari ini belum terpikirkan. Manifesto ini cukup luas untuk menampung semuanya — selama prinsip-prinsipnya dipegang.

### Aturan pemilihan batu *(Amandemen 1)*

Batu TIDAK dipilih karena datanya kebetulan tersedia — itu *streetlight drift*, mencari
kunci di bawah lampu jalan. Batu dipilih karena ia mengidentifikasi term yang belum
terukur dalam peta kausal program (`MAP.md`):

```
E[sanksi] = P(deteksi) × P(dituntut | deteksi) × P(divonis | dituntut) × severity(| divonis)
```

Tiga aturan: (1) maksimum SATU sumber data baru per tahun; (2) setiap batu punya
kriteria mati — kondisi yang, jika terpenuhi, batu ditinggalkan dan itu ditulis;
(3) sebuah batu dihitung "berpindah" hanya jika menghasilkan DOI dataset yang hidup
atau paper yang lolos peer review — draft bukan batu.

---

## IV. HIPOTESIS KERJA

Bukan kesimpulan, tapi peta kerja yang bisa difalsifikasi. Setiap hipotesis harus bisa salah — dan temuan bahwa hipotesis SALAH sama berharganya dengan temuan bahwa hipotesis benar.

**Kerangka kausal** *(Amandemen 1)*: Pertanyaan sentral §I — mengapa sistem gagal menghentikan korupsi — didekomposisi dalam kerangka deterrence (Becker): korupsi persisten jika sanksi-yang-diharapkan jauh lebih kecil dari keuntungannya, dan sanksi-yang-diharapkan adalah hasil kali empat term — P(deteksi) × P(dituntut|deteksi) × P(divonis|dituntut) × severity. Hipotesis-hipotesis di bawah adalah sudut pandang; kemajuan program diukur *per term*, di `MAP.md`. Empat bulan pertama eksekusi mengajarkan: tanpa kerangka ini, semua analisis berkerumun di satu term (severity) tanpa ada yang menyadarinya.

Konstitusi yang mengklaim "hipotesis boleh salah" wajib memajang bangkainya. Status per 16 Juli 2026 ditulis di bawah setiap hipotesis.

### H1: Disproporsionalitas Sistemik (*Systematic Disproportionality*)

Pola vonis korupsi tidak berkorelasi kuat dengan besaran kerugian negara. Variabel yang seharusnya tidak dominan (daerah, identitas hakim) memiliki pengaruh yang signifikan terhadap berat ringannya vonis.

**Prediksi:** Dalam model regresi yang mengontrol variabel legal (pasal, kerugian negara, mitigating/aggravating factors yang tertulis dalam putusan), variabel non-legal (daerah, hakim) tetap signifikan.

**Falsifikasi:** Setelah mengontrol faktor-faktor legal yang sah, variasi vonis dapat dijelaskan secara proporsional — R² tinggi, variabel non-legal tidak signifikan.

**Catatan kritis:** R² yang rendah BUKAN otomatis bukti disproporsionalitas. Ia bisa berarti model kehilangan variabel legal yang sah tapi belum diekstrak dari teks. **Kualitas ekstraksi variabel legal dari teks putusan menentukan kualitas klaim ini.**

> **Status (Amandemen 1): SEBAGIAN TERJAWAB — dengan pelintiran.** Disproporsionalitas ada, tapi masuk di hulu (tuntutan jaksa: elasticity terhadap kerugian ≈ 0.1), bukan di hakim (yang menjangkar kuat ke tuntutan). Dan catatan kritis di atas terbukti nubuat: validasi 2026-07 menemukan akurasi ekstraksi vonis hanya 73% — parser diperbaiki dan seluruh korpus diekstraksi ulang sebelum satu klaim pun boleh terbit. Instrumen menentukan klaim, persis seperti ditulis.

### H2: Normalisasi Linguistik (*Linguistic Normalization*)

Bahasa yang digunakan dalam putusan korupsi secara sistematis menormalisasi tindakan korupsi. Frasa tertentu berkorelasi dengan vonis ringan — dan frasa-frasa ini lebih sering muncul dalam putusan korupsi daripada putusan pidana umum.

**Prediksi:** Model NLP dapat memprediksi ringan/berat vonis dari teks pertimbangan hakim saja, tanpa fitur numerik.

**Falsifikasi:** Classifier gagal memprediksi vonis dari teks (akurasi ≤ chance level).

**Catatan kritis:** Jika classifier berhasil, ada dua interpretasi: (a) bahasa hakim mengandung bias, atau (b) bahasa hakim mencerminkan faktor legal yang sah tapi tidak dikuantifikasi. Membedakan (a) dari (b) membutuhkan analisis lebih lanjut — bukan klaim otomatis.

> **Status (Amandemen 1): FALSIFIED — dan itu temuan sah.** 34+ eksperimen (TF-IDF, embeddings, keyword, IndoBERT) pada n≈300 putusan MA: teks pertimbangan tidak menambah daya prediksi di atas fitur numerik. Falsifikasi terjadi persis lewat jalur yang diprediksi manifesto. Kemungkinan tetap terbuka pada korpus PN yang lebih besar dan lebih dekat ke fakta persidangan — tapi pada data yang ada, hipotesis ini mati dan tidak akan dihidupkan kembali tanpa data baru.

### H3: Erosi Temporal (*Temporal Erosion*)

Semangat antikorupsi memiliki siklus. Energi pasca-Reformasi 1998 digerus oleh "kelelahan reformasi" — dan ini terlihat dalam data vonis. Peristiwa politik (revisi UU KPK 2019, tahun Pilkada, pergantian pimpinan KPK) mempengaruhi pola vonis.

**Prediksi:** Rata-rata vonis memiliki pola temporal yang dipengaruhi oleh peristiwa politik.

**Falsifikasi:** Tren temporal menunjukkan vonis stabil atau semakin berat secara konsisten, tidak terpengaruh peristiwa politik.

> **Status (Amandemen 1): BELUM TERUJI** — dan sinyal awal berlawanan arah dengan intuisi: tuntutan justru naik 2014→2025. Uji formal terhadap peristiwa politik belum dijalankan.

### H4: Dualisme Struktural (*Structural Dualism*)

Korupsi "kecil" dan korupsi "besar" adalah fenomena yang berbeda secara fundamental — berbeda profil pelaku, modus, bahasa putusan, dan pola vonis. Memperlakukan keduanya sebagai satu fenomena mengaburkan analisis.

**Prediksi:** Clustering pada profil perkara menghasilkan kluster-kluster yang terpisah secara jelas.

**Falsifikasi:** Profil seragam di semua skala — tidak ada kluster yang bermakna.

> **Status (Amandemen 1): BELUM TERUJI.**

### H5: Kegagalan Umpan Balik (*Feedback Failure*)

Tidak ada yang mengukur apakah upaya pemberantasan korupsi bekerja. Efek deterren dari aktivitas KPK tidak terukur — dan mungkin tidak berjalan.

**Prediksi:** Tidak ada korelasi temporal antara aktivitas pemberantasan dan penurunan kasus.

**Falsifikasi:** Korelasi negatif signifikan — deterren bekerja.

**Catatan kritis:** Korelasi temporal bukan kausalitas. Framing harus jujur tentang batasan ini.

> **Status (Amandemen 1): TIDAK IDENTIFIABLE dari putusan saja.** Butuh data penindakan (Edge 1–2 di `MAP.md`: laporan KPK/Kejagung, tabulasi ICW). Pertanyaannya tetap di konstitusi; korpus putusan keluar sebagai metodenya. Inilah batu berikutnya setelah Batu 1 selesai — bukan karena datanya mudah, tapi karena ia term yang belum terukur.

### H6: Kegelapan Terukur (*Measurable Darkness*)

Semua ranking "daerah paling korup" yang beredar cacat karena mengukur *penindakan*, bukan *korupsi*. Normalisasi metrik (per kapita, per APBD, per jumlah PNS) akan mengubah ranking secara drastis. Daerah dengan nol kasus bisa jadi yang paling gelap.

**Prediksi:** Ranking provinsi berubah signifikan setelah normalisasi.

**Falsifikasi:** Ranking sama setelah normalisasi — metrik populer sudah benar.

> **Status (Amandemen 1): DIBUNUH (Juni 2026).** Dua alasan: tidak identifiable dari putusan saja, dan konsepnya ternyata sudah jenuh di literatur akuntansi publik — pelanggaran cek novelty. Dipertahankan di sini sebagai catatan sejarah dan sebagai bukti bahwa membunuh hipotesis sendiri adalah bagian dari metode, bukan kegagalan.

---

## V. EMPAT KEGELAPAN (*Four Darknesses*)

Mengapa kita tidak tahu apa yang seharusnya bisa kita ketahui — empat mekanisme yang menyembunyikan pola korupsi dari penglihatan:

### D1: Kegelapan Volume (*Volume Darkness*)
Data terlalu banyak untuk dibaca manusia. Ratusan ribu putusan, ribuan laporan audit, jutaan transaksi pengadaan. **Kelebihan data bukan transparansi — ia bisa menjadi bentuk baru ketertutupan.** Publik merasa "kan sudah terbuka" sementara tidak ada yang benar-benar membacanya.

### D2: Kegelapan Bahasa (*Language Darkness*)
Data ditulis dalam bahasa yang mengaburkan kenyataan. Bahasa hukum mereduksi korupsi menjadi masalah administrasi. "Menyalahgunakan wewenang" terdengar lebih jinak dari "mencuri uang rakyat." Bahasa audit mereduksi kegagalan menjadi "temuan."

### D3: Kegelapan Fragmentasi (*Fragmentation Darkness*)
Data tersebar di banyak lembaga: putusan di MA, perkara di KPK, audit di BPK, harta di LHKPN, anggaran di APBD, pengadaan di LPSE. Tidak ada satu pun platform yang menyatukannya. **Setiap lembaga melihat potongan kecil dari gambaran besar yang tidak pernah ada yang rakit.**

### D4: Kegelapan Seleksi (*Selection Darkness*)
Yang paling fundamental: data yang kita punya hanya mencerminkan **yang tertangkap.** Korupsi yang tidak sampai ke pengadilan, yang dihentikan di penyidikan, yang tidak pernah dilaporkan — tidak meninggalkan jejak di dataset mana pun. Kita selalu menganalisis ujung gunung es.

---

## VI. BATASAN YANG DIAKUI

Kejujuran tentang batasan bukan kelemahan — ia adalah kekuatan metodologis.

### B1: Selection Bias Fundamental
Seluruh analisis bersifat conditional: "**Di antara kasus yang terekam dalam data publik**, ditemukan pola X." Klaim tentang korupsi *secara umum* membutuhkan asumsi tambahan yang harus dinyatakan eksplisit.

### B2: Satu Orang, Bukan Tim
Riset ini dimulai oleh satu dosen teknik informatika. Tidak ada keahlian hukum, kriminologi, atau sosiologi dalam tim. Interpretasi temuan harus bersifat deskriptif dan kuantitatif — bukan normatif atau kausal. Kolaborasi sangat diinginkan tapi tidak menjadi prasyarat untuk memulai.

*Amandemen 1 — dikeraskan oleh pengalaman:* empat bulan eksekusi membuktikan B2 bukan sekadar batasan yang cukup diakui — ia bottleneck aktif. Satu-satunya desk-reject program menyebut kontribusi, dan yang memisahkan "latihan komputasi" dari "kontribusi kriminologi" di mata editor adalah persis keahlian domain yang tidak ada di tim. Maka aturannya berubah: **memulai tidak butuh kolaborator; menerbitkan klaim substantif di jurnal domain butuh minimal sinyal eksternal (pembaca, korespondensi, atau co-author) sebelum submit** — diformalkan sebagai gate G3/G5 di `GATES.md`.

### B3: Tool Builder, Bukan Hakim
Posisi riset ini: **tool builder.** Saya membangun mesin diagnostik — ahli hukum, ICW, KPK, jurnalis yang menginterpretasi hasilnya. Saya membangun MRI — ribuan dokter yang menggunakannya. Tapi tanpa MRI, mereka mendiagnosis dengan meraba-raba.

### B4: Data Publik, Bukan Data Lengkap
Seluruh riset hanya menggunakan data publik. Banyak informasi krusial (koneksi politik, tekanan terhadap hakim, aliran uang sebenarnya) tidak akan pernah tersedia dari sumber publik.

### B5: Korelasi, Bukan Kausalitas
Hampir seluruh metode bersifat korelasional atau deskriptif. Klaim kausal membutuhkan desain riset yang lebih ketat — dan hanya dijanjikan jika data mendukung.

---

## VII. KOMITMEN ETIS

### E1: Data Agregat di Atas Data Individu
Publikasi menyajikan data pada level **institusi dan daerah**, bukan pada level individu. Publikasi per-individu membutuhkan pertimbangan etis dan legal tambahan.

### E2: Deskripsi, Bukan Tuduhan
Bahasa riset harus deskriptif: "Pengadilan X memiliki rata-rata vonis Y tahun, Z% di bawah rata-rata nasional" — bukan "Pengadilan X melindungi koruptor." Data berbicara sendiri.

### E3: Interpretasi Multi-arah
Setiap temuan harus disertai interpretasi alternatif. Riset yang jujur menyajikan semua kemungkinan, bukan hanya yang paling dramatis.

### E4: Keterbukaan Radikal
Seluruh dataset, kode, dan temuan harus terbuka. Tidak ada paywall. Tidak ada klaim proprietary. Alat diagnostik untuk keadilan publik harus menjadi milik publik.

*Amandemen 1 — resolusi ketegangan E1↔E4 (yang semula tidak disadari konstitusi ini):*
korpus putusan memuat nama terdakwa — data level individu, persis yang E1 batasi. Resolusinya:
putusan adalah dokumen publik yang diterbitkan Mahkamah Agung sendiri; korpus adalah salinan
setia dan terverifikasi dari rekaman publik itu, bukan agregasi baru yang menambah paparan
individu. E1 tetap mengikat pada level *analisis dan klaim* (institusi/daerah, bukan individu).
Kebijakan rilis lengkap — termasuk argumen ini — wajib ditulis di datasheet setiap rilis korpus,
bukan diasumsikan. Dan keterbukaan radikal punya prasyarat yang baru dipelajari dengan mahal:
**data yang dirilis harus tervalidasi dulu** — merilis korpus dengan nilai yang diketahui salah
bukan keterbukaan, ia polusi. Rilis menunggu gate instrumen hijau.

### E5: Kesadaran Dampak
Temuan riset bisa disalahgunakan. Risiko ini diakui dan dimitigasi melalui publikasi akademik dan diskusi terbuka tentang implikasi.

---

## VIII. PRINSIP-PRINSIP PANDUAN

### Prinsip 1: Data, Bukan Opini
*Kita sudah punya terlalu banyak opini tentang korupsi dan terlalu sedikit data. Setiap klaim harus didukung oleh data yang bisa diverifikasi.*

### Prinsip 2: Data Berbicara Sendiri
*Kita tidak perlu menuduh siapa pun. Kita hanya perlu membiarkan data berbicara. Data itu sendiri sudah cukup — tanpa perlu menyimpulkan motivasi.*

### Prinsip 3: Komputasi sebagai Keberanian
*Membaca satu putusan adalah tugas manusia. Membaca puluhan ribu dan menemukan POLA — itu tugas mesin. Dan pola yang ditemukan oleh mesin lebih sulit dibantah oleh kekuasaan, karena ia bukan opini satu orang — ia adalah statistik dari seluruh sistem.*

### Prinsip 4: Satu Batu pada Satu Waktu
*Korupsi adalah gunung. Gunung tidak dipindahkan dengan satu ledakan. Ia dipindahkan satu batu pada satu waktu, oleh satu generasi pada satu waktu. Setiap paper, setiap dataset, setiap visualisasi — itu satu batu.*

### Prinsip 5: Falsifiable
*Hipotesis bisa salah. Temuan bahwa sistem BEKERJA sama berharganya dengan temuan bahwa sistem GAGAL. Kita mencari kebenaran, bukan konfirmasi.*

### Prinsip 6: Kejujuran Metodologis
*Setiap batasan dinyatakan, setiap asumsi dieksplisitkan, setiap interpretasi alternatif disajikan. Data yang solid dan transparan lebih berbahaya bagi korupsi daripada seribu klaim dramatis yang bisa dibantah.*

### Prinsip 7: Simple is Better
*Regresi sebelum deep learning. Satu provinsi sebelum seluruh Indonesia. Satu paper solid sebelum sepuluh draft. Kompleksitas hanya jika kesederhanaan terbukti tidak cukup.*

### Prinsip 8: Instrumen Sebelum Klaim *(Amandemen 1)*
*Tidak ada klaim tanpa instrumen tervalidasi, dan tidak ada submit dengan gate merah (`GATES.md`). Akurasi ekstraksi diukur pada sampel tervalidasi manusia — blind, stratified, dengan holdout segar — dan dilaporkan di dalam paper. Pelajaran Juli 2026: parser dengan akurasi vonis 73% nyaris membawa angka salah ke jurnal; yang menyelamatkan bukan kejeniusan, melainkan prosedur validasi yang dijalankan sebelum submit. Mesin diagnostik yang tidak dikalibrasi bukan MRI — ia pembangkit artefak.*

---

## IX. KONEKSI INTELEKTUAL

### Ke Computational Legal Studies Global
Riset ini bukan yang pertama menganalisis data hukum secara komputasional. Brasil, India, dan AS sudah memiliki tradisi *computational legal analysis*. Yang baru: **skala penuh untuk data korupsi Indonesia** — corpus yang belum pernah dianalisis secara sistematis.

### Ke Riset Penulis Sebelumnya
- **VOLCARCH:** Text mining corpus besar, pattern extraction dari dokumen historis. Yang tak terlihat — peradaban terkubur oleh abu vulkanik; keadilan terkubur oleh volume data yang tidak terbaca. Corpus berbeda, filosofi serupa.
- **Manifesto Bahasa Nusantara:** NLP Indonesian text, corpus analysis. Bahasa daerah mati tanpa suara di ruang digital; keadilan mati tanpa suara di balik bahasa hukum.
- **Manifesto Farmakope Nusantara:** Knowledge extraction, cross-referencing antar sumber terfragmentasi.
- **IndoBERT / Hate Speech Detection:** Fine-tuning bahasa Indonesia, text classification — langsung applicable.

---

## X. UNTUK PERISET YANG AKAN DATANG

Jika kamu membaca manifesto ini di masa depan — mungkin sebagai mahasiswa hukum yang kesal dengan skripsi, mungkin sebagai data scientist yang ingin proyeknya bermakna, mungkin sebagai aktivis yang lelah berteriak tanpa data:

1. **Data ada.** Putusan pengadilan, laporan audit, data anggaran — semuanya sudah daring. Ini adalah corpus yang menunggu untuk dianalisis. Mulai dari satu sumber. Satu tahun. Satu daerah.

2. **Alat ada.** Python, IndoBERT, scikit-learn. Kamu tidak perlu izin siapa pun. Aksesnya terbuka. Alatnya gratis.

3. **Keberanian yang dibutuhkan bukan keberanian melawan koruptor.** Keberanian yang dibutuhkan adalah keberanian akademik: mempublikasikan temuan yang mungkin membuat orang berkuasa tidak nyaman, dalam jurnal yang peer-reviewed, dengan metodologi yang *auditable* — setiap angka bisa dilacak kembali ke dokumen sumbernya oleh siapa pun. (Bukan "tidak bisa dibantah" — tidak ada metodologi yang tidak bisa dibantah, dan mengklaim itu adalah overclaim pertama yang akan dibantah. Yang bisa dijanjikan: setiap bantahan bisa diperiksa terhadap data terbuka.) Data yang kuat lebih berbahaya bagi korupsi daripada seribu demonstrasi. Dan bentuk keberanian akademik yang paling sering dihindari ternyata paling sederhana: mengirim draft ke manusia lain sebelum yakin ia sempurna.

4. **Kamu tidak sendirian.** ICW sudah melakukan ini secara manual selama bertahun-tahun. Transparency International memantau global. LeIP memetakan reformasi peradilan. Manifesto ini menambahkan satu lensa baru: **lensa komputasional** yang bisa melihat pola yang mata manusia tidak bisa.

5. **Satu batu sudah cukup.** Kamu tidak harus memindahkan gunung. Satu analisis yang solid — satu batu yang dipindahkan — sudah bisa mengubah percakapan.

---

## XI. PENUTUP

*Korupsi di Indonesia adalah gunung.*

*Seluruh bangsa ini tinggal di kakinya. Sebagian menderita karena gunung itu — anggaran yang dicuri, jalan yang tidak dibangun, sekolah yang tidak berdiri. Sebagian hidup dari gunung itu — karena gunung itu menyediakan mata pencaharian bagi mereka yang tahu cara menambangnya. Dan sebagian besar hanya melihat gunung itu setiap hari, terlalu terbiasa untuk merasa marah, terlalu kecil untuk merasa bisa melakukan apa pun.*

*Manifesto ini tidak berjanji memindahkan gunung itu. Tidak ada satu orang yang bisa.*

*Tapi gunung itu bisa diukur. Bisa dipetakan. Bisa dihitung berapa besar setiap batunya, di mana letaknya, siapa yang menaruhnya di sana. Dan setelah dipetakan, gunung itu bisa dipindahkan — satu batu pada satu waktu, oleh satu generasi pada satu waktu.*

*Batu pertama yang saya pilih: ratusan ribu putusan pengadilan yang tidak pernah ada yang baca. Batu berikutnya mungkin laporan audit, data anggaran, catatan pengadaan, atau sesuatu yang hari ini belum terpikirkan.*

*Yang penting bukan batunya. Yang penting adalah kita mulai memindahkan.*

*Mulai menggali.*

---

*Dimulai di Malang, 18 Maret 2026.*
*Untuk Indonesia yang lebih jujur tentang dirinya sendiri.*

---

## XII. LOG AMANDEMEN

Konstitusi yang tidak pernah diamandemen setelah bertabrakan dengan kenyataan bukan
konstitusi yang stabil — ia konstitusi yang diabaikan. Setiap amandemen dicatat di sini
dengan alasannya.

### Amandemen 1 — 16 Juli 2026

*Konteks: empat bulan eksekusi. Satu desk-reject (Paper 2/CLSC, alasan kontribusi),
satu krisis instrumen (akurasi vonis 73% → parser diperbaiki → 693 putusan diekstraksi
ulang), dua preprint SSRN, korpus 693 putusan, satu hipotesis terfalsifikasi. Amandemen
ini menyerap pelajaran-pelajaran itu ke dalam konstitusi.*

Perubahan:

1. **Kerangka kausal masuk konstitusi** (§IV): dekomposisi deterrence 4-term dari `MAP.md`
   menjadi tulang punggung; hipotesis adalah sudut pandang, kemajuan diukur per term.
2. **Status hipotesis dipajang** (§IV): H1 sebagian terjawab (disproporsionalitas di hulu),
   H2 FALSIFIED, H3–H4 belum teruji, H5–H6 tidak identifiable dari putusan saja
   (H6 dibunuh). Konstitusi falsifikasionis wajib memajang bangkainya.
3. **Kalibrasi retorika skala** (§III Batu 1): korpus = 693 putusan MA, bukan "ratusan
   ribu"; novelty program dikoreksi dari "skala" ke "korpus pertama + pengukuran pertama".
4. **Aturan pemilihan batu** (§III): dipilih per edge kausal, bukan per ketersediaan data;
   max satu sumber baru/tahun; kill criteria ditulis di muka; "berpindah" = DOI/peer-review.
5. **B2 dikeraskan** (§VI): klaim substantif level jurnal butuh sinyal eksternal pra-submit
   (gate G3/G5) — pelajaran langsung dari desk-reject.
6. **Resolusi E1↔E4** (§VII): argumen rilis data individu-sebagai-rekaman-publik ditulis
   eksplisit; rilis menunggu validasi instrumen.
7. **Prinsip 8: Instrumen Sebelum Klaim** (§VIII): tidak ada submit dengan gate merah.
8. **"Tidak bisa dibantah" → "auditable"** (§X): aspirasi yang jujur dan bisa ditepati.
9. **Identitas produk** (keputusan D12, tercermin di `ROADMAP.md`): tool-builder-first —
   urutan produk per batu: dataset ber-DOI + datasheet → data paper → paper substantif.
   Klaim substantif adalah *hasil* dari alat yang tervalidasi, bukan pengganti alatnya.

Yang TIDAK berubah: kegelisahan (§I), tesis (§II), empat kegelapan (§V), komitmen etis
selain E4 (§VII), prinsip 1–7 (§VIII), dan seluruh penutup. Gunung masih gunung;
batu masih dipindahkan satu per satu. Amandemen ini hanya memperbaiki cara memilih
batu dan cara membuktikan bahwa batu itu benar-benar berpindah.
