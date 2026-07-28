# Handoff — Session 19 (2026-07-28) → Next

## Status: **G2 HIJAU.** Holdout R6 blind n=50 LOLOS kriteria pra-registrasi: **vonis 98,0%, kerugian 91,7%**. Pipeline bersih & idle, tidak ada proses berjalan. Suite 246 passed. Rescore 150 anotasi: 0 regresi.

**Tugas berikutnya = RONDE FIX 9** (sudah terdiagnosis lengkap, tinggal dikerjakan — lihat
bagian itu). Sesudahnya Paper 4 tinggal G3/G4/G5, dan **G3+G5 hanya bisa user yang jalankan.**

> **Fakta keras di ledger**: `SUBMISSIONS.md`, `GATES.md`, `DECISIONS.md` (D14–D26),
> `MAP.md`, `ROADMAP.md`. File ini hanya narasi + instruksi kerja.

---

## 🔴 PRIORITAS 1 — RONDE FIX 9 (wajib sebelum angka masuk paper)

**Tiga perkara timah membawa kerugian 10x terlalu tinggi dan menempati peringkat 1–3
kerugian terbesar di populasi analisis** — bukan satu pencilan, tapi seluruh ujung atas
distribusi, yaitu titik ber-leverage tertinggi dalam regresi log-log.

| Perkara | DB sekarang | Seharusnya |
|---|---|---|
| 11891 K/PID.SUS/2025 | Rp300.003.263.938.131 | Rp28.933.575.919.431 |
| 11179 K/PID.SUS/2025 | idem | idem |
| 11312 K/PID.SUS/2025 | idem | idem |

Angka Rp300 T adalah audit BPKP yang **MENCAKUP biaya pemulihan lingkungan Rp11,9 T**, dan
**MA secara eksplisit MENOLAKNYA**: *"dasar untuk menjatuhkan pidana kepada Terdakwa harus
didasarkan pada kerugian keuangan negara senilai Rp28.933.575.919.431,14"* — alasannya
kerugian lingkungan tunduk pada rezim hukum berbeda.

**Dampak terukur** (dihitung sesi ini, elastisitas log-log n=257):

| | sekarang | dikoreksi | selisih |
|---|---|---|---|
| elastisitas vonis~kerugian | 0.1344 | **0.1415** | +5,3% relatif |
| elastisitas tuntutan~kerugian | 0.1173 | **0.1228** | +4,7% relatif |

Headline Paper 4 SELAMAT (Indonesia tetap ±separuh benchmark AS 0.288), tapi desimal kedua
berubah — tidak boleh masuk paper tanpa dikoreksi.

**Kelas error lain dari R6 yang layak difix bersamaan (semua sudah diverifikasi vs PDF, D26):**
1. **Audit yang ditolak majelis** (11179 dkk) — butuh aturan: bila majelis menyatakan angka
   audit tidak dipakai/"harus didasarkan pada", ambil angka yang dipakai majelis.
2. **Uang pengganti terambil sebagai kerugian** (10453 K/2025: parser Rp392.184.403 = uang
   pengganti; benar Rp1.259.759.403 "terdapat kerugian keuangan Negara sebesar").
3. **Komponen menang atas total** (9645 K/2025: parser Rp722.142.200 satu pos pengadaan;
   benar Rp12.835.112.730 "dalam perkara a quo terdapat kerugian keuangan Negara sebesar").
   → pola berulang: frasa **"dalam perkara a quo terdapat kerugian keuangan Negara sebesar"**
   adalah pernyataan simpulan MA dan layak masuk tier-2 conclusion_pattern.
4. **Dokumen tanpa header "Tuntutan Pidana"** (905 K/2024, perkara KPK 363rb char, 0
   kemunculan header) → tuntutan NULL. Perlu jalur cadangan: daftar bernomor
   "Menjatuhkan pidana terhadap Terdakwa <NAMA> dengan pidana penjara selama ..." di
   sepertiga awal dokumen, sebelum blok amar mana pun.
5. **Angka tuntutan terambil sebagai vonis saat PK ditolak** (919 PK/2022: parser 18 =
   tuntutan; rantai benar tuntutan 18 → PN 11 → berikutnya 8 → PK ditolak → **8**).
6. **Nama terdakwa perkara lain terambil** (905 K/2024: parser BUDIMAN GANDI SUPARMAN;
   amar final menyebut PRASETIO NUGROHO).
7. *(Tidak fixable regex, DISCLOSE saja)* 493 PK/2020: kerugian hanya muncul di dalam klausa
   uang pengganti, per tahun anggaran, tanpa total gabungan.

**⚠️ Konsekuensi metodologis yang WAJIB ditulis di paper**: R6 mengukur parser ronde 8.
Ronde 9 mengubah parser SESUDAH pengukuran, jadi kalimat yang jujur adalah *"instrumen
divalidasi pada 50 kasus segar (vonis 98,0%, kerugian 91,7%); error yang ditemukan kemudian
dikoreksi, sehingga korpus rilis setidaknya seakurat angka ini"* — **JANGAN** klaim 98/91,7
sebagai akurasi parser final. **DILARANG menjalankan holdout R7** untuk "membuktikan"
perbaikan: D25 mengunci R6 sebagai ronde terakhir, dan mengulang setelah melihat hasil
persis pathology yang dihindari.

### Prosedur ronde fix (jangan dipotong)
1. Test-first di `tests/test_holdout_r6_bugs.py`.
2. `python -m scripts.03_parse_sample` (idempoten, ±60 mnt).
3. `python -m scripts.23_tipikor_audit` — **WAJIB**, pipeline menimpa is_tipikor.
4. `python -m scripts.24_holdout_rescore` — **harus 0 REGRESI** (150 anotasi).
5. `python scripts/19_fair_comparison.py` → angka final, perbarui tabel di bawah.

---

## 🟡 PRIORITAS 2 — temuan terbuka

- **Filter domain bocor**: `919 PK/Pid.Sus/2022` adalah perkara **UU Perkebunan Pasal 107**,
  bukan tipikor, tapi `is_tipikor=1` lolos script 23. Sengaja TIDAK dikeluarkan dari
  denominator R6 (hindari manipulasi post-hoc). Perlu audit ulang filter domain — berapa
  banyak lagi yang seperti ini? (bersambung dari D15/D17)
- **Duplikat korpus**: audit menyebut 4 nomor perkara duplikat (96 baris ekstra). Belum
  ditriase.

---

## ✅ Angka terkini (parser ronde 8, DB per 2026-07-28 12:47)

| | R5 | R6 | R7 | R8 |
|---|---|---|---|---|
| n populasi analisis | 260 | 260 | 257 | **257** |
| elastisitas tuntutan~kerugian | 0.110 | 0.115 | 0.117 | **0.1173** |
| elastisitas vonis~kerugian | 0.135 | 0.135 | 0.134 | **0.1344** |
| anchor R² (vonis~tuntutan) | 0.645 | 0.658 | 0.651 | **0.6508** |
| R²(tuntutan\|fakta) | 0.357 | 0.377 | 0.384 | **0.385** |
| R²(vonis\|fakta) | 0.466 | 0.466 | 0.465 | **0.465** |
| **gap** | −0.110 | −0.089 | −0.081 | **−0.080** |

*(kolom = ronde parser, bukan ronde holdout)*

**Wajib masuk paper**: klaim asli Paper 4 ("prosecutors less predictable") DIDUKUNG di semua
versi data bersih — arah tidak pernah berbalik dalam 8 ronde. TAPI gap menyempit monoton
seiring parser membaik (0.110→0.089→0.081→0.080): sebagian "tuntutan lebih sulit diprediksi"
ternyata error pengukuran, bukan diskresi jaksa. Nyatakan magnitudo sebagai sensitif terhadap
kualitas ekstraksi; jangan jual angka gap sebagai temuan keras.

## Akurasi instrumen untuk dilaporkan di paper (R6, n=50 segar, blind, teradjudikasi)

| field | akurasi | Wilson 95% |
|---|---|---|
| vonis | 98,0% | [89,5 – 99,6] |
| tuntutan | 98,0% | [89,5 – 99,6] |
| kerugian | 91,7% | [80,4 – 96,7] (2 AMBIGUOUS dikeluarkan) |
| daerah | 100% | [92,9 – 100] |
| tahun | 100% | [92,9 – 100] |

---

## Apa yang terjadi di session 19 (ringkas; detail D22–D26)

1. Recovery handoff s18 tuntas; re-ekstraksi R5 terverifikasi.
2. **Ronde 6** (`e94aa05`): regresi tuntutan yang ditangkap script 24 (bukan holdout) —
   strategi 1a menang tanpa memandang posisi. Fix: match valid paling awal menang.
3. **Holdout R5** (n=20) → **G2 GAGAL** (vonis 85%, kerugian 80%). D23.
4. **D24**: pemindaian 260 PDF menemukan **3 terdakwa BEBAS dengan vonis fiktif** (1052 K/2022
   Fakhri Hilmi DB=96 bulan = vonis PT yang DIBATALKAN; 3247 K/2019; 4597 K/2021) + 6 dokumen
   tanpa jangkar amar. Vonis = variabel terikat → tak bisa diselesaikan dengan disclosure.
5. **Ronde 7** (`cefae19`): header `MENGADILI,Menolak` (koma); `MENGADILI SENDIRI/KEMBALI`
   jadi jangkar (prosa tetap ditolak, ada testnya); **deteksi bebas dipindah ke DEPAN sapuan
   kalimat**; kerugian label-mengikuti-angka.
6. **Ronde 8** (`dfc6ec4`): script 24 menangkap regresi buatan ronde 7 (2997 PK: sisa setelah
   pemulihan Rp31,9 M terambil, benar Rp46,6 M). Bypass blocker dipersempit.
7. **D25 pra-registrasi** lalu **R6 n=50** → **G2 HIJAU**. Diagnosis kunci: aturan lama
   "≥90% pada n=20" mustahil mensertifikasi instrumen 90% (P(gagal)=32%), dan G2 sendiri
   menuntut ≥50 kasus — 5 ronde sebelumnya mengukur derau.

**Pelajaran struktural yang jangan hilang**: (a) rescore lintas-ronde (script 24) WAJIB tiap
ronde — dua kali ia menangkap kerusakan yang holdout ronde-berjalan mustahil lihat; (b)
akurasi per-field pada n kecil MENYEMBUNYIKAN kerusakan tingkat-korpus — tiap kelas error
vonis wajib dipindai ke seluruh populasi; (c) kasus yang dipakai mendiagnosis fix adalah data
latih meski tak pernah dianotasi (dua nyaris lolos ke sampel R6).

---

## 🔵 HANYA-USER — bottleneck sebenarnya (tertunda 4 bulan, TIDAK bergerak sesi ini)

G1 🟢 · G2 🟢 · **G3 🔴 · G4 🔴 · G5 🔴**. Delapan ronde perbaikan parser tidak menyentuh
G3/G5 sedikit pun, dan keduanya mustahil dikerjakan agent:

1. Email co-author hukum (UB/UMM/Unair)
2. Email penulis paper terdekat (komentar SSRN 6580258) — sinyal eksternal G3
3. 1 pembaca eksternal draft — G5
4. Kopi mantan jaksa
5. Akun Zenodo (rilis = korpus **v1.1 PASCA ronde 9**, jangan v1.0)

G4 (editor-sim AJC) bisa agent, tapi **jalankan di sesi SEGAR tanpa konteks pembelaan**,
diberi HANYA abstrak + cover letter + scope jurnal.

## Verifikasi cepat

```bash
python -m pytest tests/ -q                 # 246 passed, 2 xfailed
python -m scripts.23_tipikor_audit         # 465/14/0 — WAJIB tiap re-ekstraksi
python -m scripts.24_holdout_rescore       # 150 anotasi, harus 0 regresi
python scripts/19_fair_comparison.py       # n & elastisitas DB terkini
```
- Branch `autoresearch/apr9-textfeatures` (rename ditunda, D10) · Backup DB lama:
  `data/korupsinlp_pre_reparse_s17.db` · SSRN: P2=6574140, P4=6580258
- Arsip validasi: `holdout_r1..r6_validated.csv` (+ `r6_validation_A–E`). Kolom
  `adjudication` di r5/r6 memuat alasan per baris — sumber konvensi anotasi.
- Test regresi parser: `test_holdout_bugs.py`, `_r2_`, `_r3_`, `_r4_`, `_r5_`,
  `test_rescore_regressions.py`. Jalankan pada SETIAP perubahan parser.
