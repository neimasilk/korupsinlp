# GATES.md — Gate Blocking per Paper (tidak ada submit dengan gate merah)

> **Aturan**: Paper tidak boleh disubmit selama ada gate 🔴. Gate hanya bisa dihijaukan
> dengan bukti, bukan dengan niat. Agent wajib mencetak status gate di awal setiap sesi
> yang menyentuh paper terkait. (Pelajaran F2/F3: kritik yang di-file lalu diabaikan;
> review yang mengoptimasi "lolos reviewer" padahal editor bertanya "cukup penting?")

## Definisi gate (berlaku semua paper)

| Gate | Isi | Bukti yang menghijaukan |
|---|---|---|
| G1 TRUTH | Semua Truth-critique di DECISIONS.md berstatus FIXED/DISCLOSED | Baris DECISIONS.md |
| G2 INSTRUMEN | Field yang dipakai klaim utama tervalidasi ≥50 kasus stratified, akurasi per-field dilaporkan | File golden set + angka akurasi |
| G3 KONTRIBUSI | (a) Klaim novelty 1 kalimat + 3 paper terdekat + beda-nya; (b) ≥1 sinyal eksternal (balasan penulis paper terdekat / komentar SSRN / kolega membaca) | Teks di paper + bukti sinyal |
| G4 EDITOR-SIM | Sesi agent SEGAR (tanpa konteks pembelaan), diberi HANYA abstrak + cover letter + scope jurnal, menjawab "send to review?" → YES | Transkrip verdict |
| G5 HUMAN EKSTERNAL | ≥1 manusia selain PI membaca draft | Nama + tanggal |

## Paper 4 — "Broken Proportionality" (flagship) — status 2026-07-07

| Gate | Status | Detail |
|---|---|---|
| G1 TRUTH | 🟢 | Semua Truth-critique Paper 4 FIXED (DECISIONS D1, D2, D3, D5) per 2026-07-07: benchmark realized AS (0.288) terpasang, klaim diskresi ditulis ulang (diskresi masuk sekali di hulu), paragraf attenuation + 2 disclosure seleksi masuk §5.5. |
| G2 INSTRUMEN | 🟢 **HIJAU (2026-07-28) — holdout R6 blind n=50: vonis 98,0% [89,5–99,6], kerugian 91,7% [80,4–96,7]**, tuntutan 98,0%, daerah 100%, tahun 100%. Kriteria (vonis ≥90% DAN kerugian ≥90%) **DIPRA-REGISTRASI di D25 sebelum sampling**, beserta aturan penghenti ronde-terakhir — jadi hasil ini tidak bisa dituduh hasil lempar-ulang. Bukti: `data/golden_set/holdout_r6_validated.csv` (+ batch anotator r6_validation_A–E). Diagnosis kunci: gate lama "≥90% pada n=20" secara statistik tak mampu mensertifikasi instrumen 90% (P(gagal)=32%), dan definisi G2 sendiri menuntut ≥50 kasus — 5 ronde n=20 sebelumnya mengukur derau. Detail D26; taksonomi 7 error tersisa juga di D26 | Riwayat: n=30 (07-07) → fix D14. **R1 n=20 blind** (adjudicated): vonis 100%, tuntutan 95%, **kerugian 72%** → fix ronde 2 (`c2ac9a4`): ambang statutori, gap merged, dot-cents, tuntutan tanpa "penjara". **R2 n=20 blind** (adjudicated): tuntutan 100%, tahun 100%, daerah 100%, **vonis 85%** (regresi! kelas baru: preamble memperbaiki+uang pengganti; header "mengadilimenolak" merged → kutipan dissent terambil; dokumen PT "menguatkan"; ejaan "dakwaan primer"), **kerugian 79%** (komponen-vs-total; angka dissent di kasus bebas; angka suap di kasus gratifikasi; gap 225 char) → **fix ronde 3 (`0e0d8eb`)**: semua 6 kelas + aturan pipeline bebas→kerugian NULL; suite 230 passed; 6 PDF gagal diverifikasi end-to-end. Pola: ekor panjang kelas dokumen langka — tiap ronde memunculkan varian baru tapi frekuensinya menurun. Re-ekstraksi ronde 3 berjalan → **holdout R3 = verdict**. Aturan tetap: vonis & kerugian ≥90% adjudicated; holdout gagal = training. Adjudikasi konvensi (dicatat D18/D19): baris multi-terdakwa benar jika nama+tuntutan+vonis konsisten satu terdakwa; NULL ≙ "tidak ada kerugian ditetapkan". |
| G3 KONTRIBUSI | 🟢 **HIJAU (2026-08-11)** | Klaim novelty ada di cover letter ("first large-scale computational analysis of Indonesian corruption prosecution, using a novel corpus") + intro memposisikan vs prior work (sentencing research studies judges — Medvedeva 2020, Strickson & De La Iglesia 2020; US loss-graduated benchmark). **Sinyal eksternal (b): Go Frendi Gunawan — co-author baru, membaca draft & menyetujui ikut sebagai penulis** (konfirmasi user 11 Agt 2026) = sinyal "kolega membaca". Bersamaan menutup D11 (rekrut co-author hukum/domain). |
| G4 EDITOR-SIM | 🟢 **HIJAU (2026-08-05)** | Agent SEGAR tanpa konteks pembelaan, diberi HANYA abstrak ronde-9 + cover letter (`reports/paper4_cover_letter.md`) + aims&scope AJC → verdict **SEND TO REVIEW**. Transkrip: `reports/g4_editor_sim_ajc.md` (D29). |
| G5 HUMAN | 🟢 **HIJAU (2026-08-11)** | **Go Frendi Gunawan membaca draft** (co-author, State Alchemists) — konfirmasi user 11 Agt 2026. Bukti: nama + tanggal di sini; draft dibaca sebagai calon co-author sebelum disetujui. |

**Konsekuensi**: Paper 4 TIDAK disubmit (venue perdana = AJC) sampai semua gate hijau.
Per 2026-07-29 G1+G2 hijau. **2026-08-05: G4 editor-sim AJC HIJAU** (SEND TO REVIEW,
D29). **2026-08-11: G3 + G5 HIJAU** — Go Frendi Gunawan ditambahkan sebagai **co-author**
(keputusan user 11 Agt), membaca draft & menyetujui (G3 sinyal eksternal + G5 pembaca
manusia). **SEMUA GATE HIJAU per 2026-08-11 → Paper 4 ✅ SUBMITTED ke AJC 11 Agt 2026**
(SUBMISSIONS.md). Menunggu keputusan editor (~21 hari). Backup venue: EJCPR → IJCJS.
**Ronde fix 9 SELESAI
(2026-07-29)**: 3 perkara timah + 3 bug lain dikoreksi (lihat HANDOFF.md §session 20);
elastisitas vonis~kerugian 0,134→**0,145**, tuntutan 0,117→**0,124**, gap −0,080→**−0,093**;
rescore 150 anotasi 0 regresi; suite 254 passed. Angka ronde-9 siap masuk paper dengan
disclosure timah (300T audit ≠ kerugian *keuangan* negara; robustness 300T di lampiran).
⚠️ **Rilis Zenodo korpus v1.0 juga DIBLOKIR** — rilis = v1.1 pasca ronde 9.

**[2026-08-03, D28]** Draft Paper 4 sudah di-refresh ke angka ronde-9 + re-interpretasi §4.2
(vonis LEBIH dapat diprediksi daripada tuntutan — hakim mengoreksi sebagian, bukan transmisi
murni; konsisten dgn Paper 3) + 4 disclosure (timah 28,9T/holdout 98-91,7%/error-pengukuran/
domain 919). Paper↔DB konsisten (grep 0 angka basi); generator angka reproducible =
`scripts/25_paper4_ronde9.py`. **Maka blocker submit Paper 4 TINGGAL G3/G5** — bukan lagi
angka basi. G4 (editor-sim AJC) sudah HIJAU 2026-08-05 (D29, SEND TO REVIEW). G3+G5 HANYA-USER.

## Paper dataset (baru — "KorpusKorupsi descriptor") — status 2026-07-07

| Gate | Status | Detail |
|---|---|---|
| G1 | 🔴 | Datasheet basi (557 vs 693); date_decided mojibake belum didokumentasi |
| G2 | 🔴 | Sama dengan Paper 4 G2 (golden set) |
| G3 | 🟢 | Novelty klaim untuk data paper = keberadaan korpus itu sendiri; tidak ada korpus putusan tipikor machine-readable lain |
| G4 | 🔴 | Belum |
| G5 | 🔴 | Belum |
