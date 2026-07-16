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
| G2 INSTRUMEN | 🔴 **2 RONDE HOLDOUT SELESAI (2026-07-16), R3 MENENTUKAN** | Riwayat: n=30 (07-07) → fix D14. **R1 n=20 blind** (adjudicated): vonis 100%, tuntutan 95%, **kerugian 72%** → fix ronde 2 (`c2ac9a4`): ambang statutori, gap merged, dot-cents, tuntutan tanpa "penjara". **R2 n=20 blind** (adjudicated): tuntutan 100%, tahun 100%, daerah 100%, **vonis 85%** (regresi! kelas baru: preamble memperbaiki+uang pengganti; header "mengadilimenolak" merged → kutipan dissent terambil; dokumen PT "menguatkan"; ejaan "dakwaan primer"), **kerugian 79%** (komponen-vs-total; angka dissent di kasus bebas; angka suap di kasus gratifikasi; gap 225 char) → **fix ronde 3 (`0e0d8eb`)**: semua 6 kelas + aturan pipeline bebas→kerugian NULL; suite 230 passed; 6 PDF gagal diverifikasi end-to-end. Pola: ekor panjang kelas dokumen langka — tiap ronde memunculkan varian baru tapi frekuensinya menurun. Re-ekstraksi ronde 3 berjalan → **holdout R3 = verdict**. Aturan tetap: vonis & kerugian ≥90% adjudicated; holdout gagal = training. Adjudikasi konvensi (dicatat D18/D19): baris multi-terdakwa benar jika nama+tuntutan+vonis konsisten satu terdakwa; NULL ≙ "tidak ada kerugian ditetapkan". |
| G3 KONTRIBUSI | 🔴 | Klaim novelty ada; sinyal eksternal = 0. Rejection kedua (venue TBD, lihat SUBMISSIONS.md) adalah sinyal eksternal NEGATIF yang harus didiagnosis dulu — paste surat keputusan. |
| G4 EDITOR-SIM | 🔴 | Belum pernah dijalankan untuk venue berikutnya. |
| G5 HUMAN | 🔴 | 0 pembaca eksternal sejak program dimulai. |

**Konsekuensi**: Paper 4 TIDAK disubmit (venue perdana = AJC) sampai minimal G1+G2+G4 hijau.
G2 kini menuntut: fix 4 bug extractor (30 kasus tervalidasi jadi pytest fixture, test-first) →
re-ekstraksi 693 → re-run scripts 16/19 → validasi ulang holdout 20 kasus segar → update angka
paper. ⚠️ **Rilis Zenodo korpus v1.0 juga DIBLOKIR** — freeze 2026-07-07 memuat nilai yang
diketahui salah; rilis = v1.1 pasca re-ekstraksi.

## Paper dataset (baru — "KorpusKorupsi descriptor") — status 2026-07-07

| Gate | Status | Detail |
|---|---|---|
| G1 | 🔴 | Datasheet basi (557 vs 693); date_decided mojibake belum didokumentasi |
| G2 | 🔴 | Sama dengan Paper 4 G2 (golden set) |
| G3 | 🟢 | Novelty klaim untuk data paper = keberadaan korpus itu sendiri; tidak ada korpus putusan tipikor machine-readable lain |
| G4 | 🔴 | Belum |
| G5 | 🔴 | Belum |
