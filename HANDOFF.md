# Handoff — Session 22 (2026-08-05) → Next

## Status: **G4 EDITOR-SIM AJC HIJAU — SEND TO REVIEW.** Dijalankan sesuai prosedur gate:
agent SEGAR tanpa konteks pembelaan, diberi HANYA abstrak ronde-9 + cover letter baru
(`reports/paper4_cover_letter.md`) + aims&scope AJC → verdict **SEND TO REVIEW** (D29,
transkrip `reports/g4_editor_sim_ajc.md`). Cover letter Paper 4 dibuat (template Paper 2,
angka ronde-9: elasticity 0.124, n=262). **Blocker submit Paper 4 tersisa G3+G5 — keduanya
HANYA-USER** (email co-author / komentar SSRN / pembaca eksternal). Red flag editor (5)
adalah pertanyaan reviewer, bukan blocker: dokumentasi korpus n=262, komparabilitas benchmark
AS, spesifikasi eksak 3 formulasi R² (0.300/0.405-vs-0.498/0.642), sel kecil temporal/geografis,
overgeneralize Asia. #1 opsional pra-submit: parafrase abstrak soal R² biar tak terbaca inkonsisten.

> **Fakta keras di ledger**: `SUBMISSIONS.md`, `GATES.md`, `DECISIONS.md` (D14–D29),
> `MAP.md`, `ROADMAP.md`. File ini hanya narasi + instruksi kerja.

---

## Riwayat — Session 21 (2026-08-03)

## Status: **PAPER 4 DRAFT SUDAH DI-REFRESH KE RONDE-9.** Review mata elang menemukan draft
basi vs DB (n=290→262, vonis 0,137→0,145, R² 0,357/0,355→0,405/0,498, timah 300T→28,9T).
Refresh selesai: angka, tabel robustness, abstract, §3.1/§4.1–§4.4/§5.2/§5.3/§5.5/§6 semua
reconcile ke DB via `scripts/25_paper4_ronde9.py` (generator tunggal, reproducible). DOCX/PDF
di-rebuild. **Tiga temuan sekunder membalik arah** (jujur ditulis ulang, bukan dipalsukan):
§4.2 vonis kini LEBIH dapat diprediksi (hakim mengoreksi sebagian, bukan transmisi murni —
konsisten dgn Paper 3); §4.3 diskon vonis MELEBAR signifikan (bukan tetap); §4.4 geografis
persist lemah (bukan hilang). Headline survived & strengthened. **4 disclosure masuk**: timah,
holdout 98/91,7%, error-pengukuran, domain 919 PK. Detail D28.

**Blocker submit Paper 4 sekarang TINGGAL G3/G4/G5** — bukan lagi angka basi. G4 (editor-sim
AJC) bisa agent di sesi segar; **G3+G5 HANYA-USER** (email co-author/komentar SSRN/pembaca
eksternal) dan macet 4 bulan — itu bottleneck sesungguhnya.

> **Fakta keras di ledger**: `SUBMISSIONS.md`, `GATES.md`, `DECISIONS.md` (D14–D28),
> `MAP.md`, `ROADMAP.md`. File ini hanya narasi + instruksi kerja.

---

## ✅ PRIORITAS 1 (session 21) — REFRESH PAPER 4 KE RONDE-9 — SELESAI

- Review mata elang + verifikasi: `pytest` 254 passed, `scripts/24` rescore 0 regresi,
  `scripts/19` fair comparison cocok tabel R9.
- `scripts/25_paper4_ronde9.py` (baru): generator tunggal semua angka paper di sampel
  otoritatif (is_tipikor=1, drop<1jt, n=262) — bootstrap CI, practical-terms, robustness,
  fair comparison, temporal, geographic, marginal. **Wajib di-re-run tiap ronde parser baru.**
- Re-interpretasi §4.2 (vonis lebih dapat diprediksi → hakim mengoreksi sebagian) +
  3 reversed secondary findings + 4 disclosure. Grep verifikasi: 0 angka basi tersisa.

---

## Riwayat — Session 20 (2026-07-29)

## Status (s20): **G2 HIJAU. RONDE FIX 9 SELESAI.** Holdout R6 blind n=50 tetap vonis 98,0%,
kerugian 91,7% (angka instrumen tervalidasi, tak diubah). Ronde 9 mengoreksi 6 bug parser
+ 1 varian (3 timah, 9645, 10453, 905 tuntutan+nama, 919 PK), re-ekstraksi 693, audit
tipikor 465/14, **rescore 150 anotasi = 0 regresi** (1 re-adjudikasi 11312 transparan),
suite 254 passed. Pipeline bersih & idle.

**Tugas berikutnya (s20) = G3/G4/G5 Paper 4** — dan **G3+G5 hanya bisa user yang jalankan**
(email co-author, komentar SSRN, pembaca eksternal). Angka ronde-9 sudah siap masuk paper
(dengan disclosure timah, lihat bawah). G4 (editor-sim AJC) bisa agent di sesi segar.

> **Fakta keras di ledger**: `SUBMISSIONS.md`, `GATES.md`, `DECISIONS.md` (D14–D27),
> `MAP.md`, `ROADMAP.md`. File ini hanya narasi + instruksi kerja.

---

## ✅ PRIORITAS 1 — RONDE FIX 9 — SELESAI (session 20, 2026-07-29)

> **Hasil**: 6 bug parser + 1 varian difix (test-first, 8 regression test di
> `tests/test_holdout_r6_bugs.py`). Commits `4d56a5b` (6 bug) + `e9a8f91`
> (guard figur sisa-pemulihan, rescore-caught). Re-ekstraksi 693 → audit 465/14 →
> **rescore 0 regresi** → angka final di tabel bawah. Diagnosis rinci tiap kasus
> dipertahankan di bawah sebagai catatan; lihat juga D27.

> **⚠️ Keputusan substantif timah (WAJIB di-disclose di paper)**: ketiga perkara
> (11891/11179/11312) kasasinya DITOLAK, jadi figur judex facti Rp300T (audit BPKP)
> tetap operatif utk *restitusi*. TAPI audit 300T ±90% kerugian LINGKUNGAN (~Rp271T)
> yang MA tegaskan BUKAN kerugian keuangan negara rezim tipikor; MA menyatakan basis
> pidana "harus didasarkan pada kerugian keuangan negara senilai Rp28,9T". Untuk
> variabel `kerugian_keuangan_negara` & regressor basis-pidana, figur finansial
> 28,9T yang dipakai (Option A). Anotasi R3 11312 (dulu 300T) di-re-adjudikasi ke
> 28,9T via kolom adjudication (catatan asli diawetkan). Ini pilihan substantif,
> bukan trik — tulis eksplisit di §metode + robustness check dgn 300T di lampiran.

### Catatan historis diagnosis (sudah dikerjakan — detail D27)

**Timah** (peringkat 1–3 kerugian terbesar, titik ber-leverage tertinggi): audit BPKP
Rp300T mencakup kerugian lingkungan (~Rp271T) yang MA tolak; basis pidana & kerugian
keuangan negara = Rp28,9T. **Taksonomi 7 error D26, semua sudah ditangani ronde 9:**
1. Audit ditolak majelis (11891/11179/11312) → pola tier-2 "harus didasarkan pada … senilai"
   + "kelebihan pembayaran … tidak sebagaimana mestinya" (varian 11312). ✅
2. Uang pengganti terambil sbg kerugian (10453) → tier-2 "dalam perkara a quo terdapat … sebesar". ✅
3. Komponen menang atas total (9645) → pola yang sama. ✅
4. Tuntutan NULL tanpa header (905 KPK) → header merged `\s*`. ✅
5. Vonis ambil tuntutan saat PK ditolak (919) → quoted-sentence finder +loop bulan. ✅
6. Nama terdakwa salah (905) → header berspasi `N a m a:`. ✅
7. 493 PK/2020 (kerugian hanya di klausa UP per tahun anggaran) → **tidak fixable regex, DISCLOSE**. ⚠️

**Prosedur (sudah dijalankan, jangan ulang kecuali parser berubah lagi)**: test-first →
`scripts.03` (±60 mnt) → `scripts.23` (WAJIB, timpa is_tipikor) → `scripts.24` (0 regresi)
→ `scripts/19` (angka final, lihat tabel §Angka terkini). Dampak aktual ronde 9:
elastisitas vonis 0,1344→**0,1446** (+7,6%), tuntutan 0,1173→**0,1243** (+6,0%) — sedikit
lebih besar dari prediksi awal (+5,3%) karena n tumbuh +5.

**⚠️ Konsekuensi metodologis yang WAJIB ditulis di paper**: R6 mengukur parser ronde 8.
Ronde 9 mengubah parser SESUDAH pengukuran, jadi kalimat yang jujur adalah *"instrumen
divalidasi pada 50 kasus segar (vonis 98,0%, kerugian 91,7%); error yang ditemukan kemudian
dikoreksi, sehingga korpus rilis setidaknya seakurat angka ini"* — **JANGAN** klaim 98/91,7
sebagai akurasi parser final. **DILARANG menjalankan holdout R7** untuk "membuktikan"
perbaikan: D25 mengunci R6 sebagai ronde terakhir, dan mengulang setelah melihat hasil
persis pathology yang dihindari.

---

## 🟡 PRIORITAS 2 — temuan terbuka

- **Filter domain bocor**: `919 PK/Pid.Sus/2022` adalah perkara **UU Perkebunan Pasal 107**,
  bukan tipikor, tapi `is_tipikor=1` lolos script 23. Sengaja TIDAK dikeluarkan dari
  denominator R6 (hindari manipulasi post-hoc). Perlu audit ulang filter domain — berapa
  banyak lagi yang seperti ini? (bersambung dari D15/D17)
- **Duplikat korpus**: audit menyebut 4 nomor perkara duplikat (96 baris ekstra). Belum
  ditriase.

---

## ✅ Angka terkini (parser ronde 9, DB per 2026-07-29)

| | R5 | R6 | R7 | R8 | **R9** |
|---|---|---|---|---|---|
| n populasi analisis | 260 | 260 | 257 | 257 | **262** |
| elastisitas tuntutan~kerugian | 0.110 | 0.115 | 0.117 | 0.1173 | **0.1243** |
| elastisitas vonis~kerugian | 0.135 | 0.135 | 0.134 | 0.1344 | **0.1446** |
| anchor R² (vonis~tuntutan) | 0.645 | 0.658 | 0.651 | 0.6508 | **0.6422** |
| R²(tuntutan\|fakta) | 0.357 | 0.377 | 0.384 | 0.385 | **0.405** |
| R²(vonis\|fakta) | 0.466 | 0.466 | 0.465 | 0.465 | **0.498** |
| **gap** | −0.110 | −0.089 | −0.081 | −0.080 | **−0.093** |

*(kolom = ronde parser, bukan ronde holdout. R9 = ronde fix 9 selesai; n tumbuh
+5 dari korpus baru. Rescore 150 anotasi: 0 regresi, akurasi kerugian training-set
95,2%.)*

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

## Apa yang terjadi di session 20 (ringkas; detail D27)

Recovery pasca-restart komputer user (tidak ada kerjaan yang putus — s19 ter-commit
bersih di `e249a13`). Ronde fix 9 dikerjakan test-first:

1. **6 bug parser + 1 varian** (`4d56a5b`): 3 timah (audit-ditolak → 28,9T via pola
   tier-2 "harus didasarkan pada" + "kelebihan pembayaran tidak sebagaimana mestinya"
   untuk 11312 yang berbeda); 9645+10453 ("dalam perkara a quo terdapat ... sebesar"
   outrank komponen/UP); 905 tuntutan (header merged `TuntutanPidana` → `\s*`) + nama
   (header berspasi `N a m a:`); 919 PK (quoted-sentence finder +dukung "bulan").
2. **Rescore pasca re-ekstraksi menangkap 1 regresi nyata**: 2997 PK kembali ke 31,9M
   (pola a_quo baru menaikkan figur sisa-pemulihan). Fix: guard figur-sisa menolak
   elevasi tier-2 (`e9a8f91`, test `SNIPPET_AQUO_IS_REMAINDER`).
3. **Konflik artefak ditemukan & diadili**: 11312 anotasi R3 = 300T vs handoff s19 = 28,9T.
   Kedua sisi defensible (operativitas amar vs substantif kerugian-keuangan). Keputusan
   **Option A (28,9T)**: variabel = kerugian *KEUANGAN* negara, 300T ±90% lingkungan;
   + basis pidana per MA = 28,9T. Anotasi R3 di-re-adjudikasi (transparan). Caveat
   operativitas → disclosure paper + robustness 300T di lampiran.
4. **Re-ekstraksi 693 (pass-2) → audit 465/14 → rescore 0 regresi**. Elastisitas vonis
   0,1344→**0,1446**, gap −0,080→**−0,093**. Headline survived & strengthened.

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

G1 🟢 · G2 🟢 · **G4 🟢 (2026-08-05) · G3 🔴 · G5 🔴**. G3/G5 mustahil dikerjakan agent:

1. Email co-author hukum (UB/UMM/Unair)
2. Email penulis paper terdekat (komentar SSRN 6580258) — sinyal eksternal G3
3. 1 pembaca eksternal draft — G5
4. Kopi mantan jaksa
5. Akun Zenodo (rilis = korpus **v1.1 PASCA ronde 9**, jangan v1.0)

G4 (editor-sim AJC) bisa agent, tapi **jalankan di sesi SEGAR tanpa konteks pembelaan**,
diberi HANYA abstrak + cover letter + scope jurnal.

## Verifikasi cepat

```bash
python -m pytest tests/ -q                 # 254 passed, 2 xfailed
python -m scripts.23_tipikor_audit         # 465/14/0 — WAJIB tiap re-ekstraksi
python -m scripts.24_holdout_rescore       # 150 anotasi, harus 0 regresi
python scripts/19_fair_comparison.py       # n & elastisitas DB terkini
python scripts/25_paper4_ronde9.py         # SEMUA angka paper di n=262 — cek vs draft
```
- Branch `autoresearch/apr9-textfeatures` (rename ditunda, D10) · Backup DB ronde 9:
  `data/korupsinlp_pre_ronde9.db` (ronde 8) · SSRN: P2=6574140, P4=6580258
- Arsip validasi: `holdout_r1..r6_validated.csv` (+ `r6_validation_A–E`). Kolom
  `adjudication` di r3/r5/r6 memuat alasan per baris — sumber konvensi anotasi
  (r3 11312 kini berisi re-adjudikasi ronde 9).
- Test regresi parser: `test_holdout_bugs.py`, `_r2_`, `_r3_`, `_r4_`, `_r5_`,
  **`test_holdout_r6_bugs.py`** (ronde 9), `test_rescore_regressions.py`.
  Jalankan pada SETIAP perubahan parser.
