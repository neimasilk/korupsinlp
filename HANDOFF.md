# Handoff — Session 19 (2026-07-28) → Next

## Status saat handoff ditulis: RE-EKSTRAKSI RONDE 8 BERJALAN (background `python -m scripts.03_parse_sample`, ±60 mnt, saat ditulis 550/693). **JIKA TERPOTONG, BACA "RECOVERY".** Semua parser fix ronde 6–8 SUDAH di-commit. **G2 GAGAL di holdout R5** (vonis 85%, kerugian 80%) → ronde fix 7+8 selesai → **keputusan gate menunggu USER (lihat "KEPUTUSAN USER").**

> **Fakta keras di ledger**: `SUBMISSIONS.md`, `GATES.md`, `DECISIONS.md` (D14–D24),
> `MAP.md`, `ROADMAP.md`. File ini hanya narasi + recovery.

## ⚠️ RECOVERY — urutan WAJIB (state machine, lanjutkan dari langkah yang belum)

1. **Cek re-ekstraksi ronde 8 selesai**: `SELECT COUNT(*) FROM verdicts WHERE parsed_at > '2026-07-28T12'`
   harus 693. Terpotong → jalankan ulang `python -m scripts.03_parse_sample` (idempoten, ±60 mnt).
   Commit parser terakhir yang harus sudah berlaku: `dfc6ec4` (ronde 8).
2. **WAJIB `python -m scripts.23_tipikor_audit`** — pipeline menimpa flag is_tipikor;
   rescue TPK/PDT/TUN hanya ada di script 23. (Ekspektasi stabil 7 ronde: 465 OK /
   14 non-tipikor / 0 kontaminasi sampel analisis.)
3. **`python -m scripts.24_holdout_rescore`** — 100 anotasi R1–R5 vs DB terkini.
   **Harus 0 REGRESI.** Ada regresi → fix test-first dulu, jangan lanjut.
   (Ronde 7 sempat memperbaiki 2505 sambil merusak 2997; hanya script 24 yang melihatnya.)
4. `python scripts/19_fair_comparison.py` → angka final ronde 8.
5. **Bawa "KEPUTUSAN USER" di bawah ke user.** Jangan pilih sendiri.

## ⚠️ KEPUTUSAN USER — satu-satunya blocker program saat ini

G2 GAGAL di R5 (D23). Ronde fix 7+8 sudah menutup 3 kelas vonis + 2 kelas kerugian
yang ditemukan R5. Pilihan:

- **(a) Holdout R6** — sampler sudah mengecualikan 120 kasus (golden 50 + R1–R5 100 →
  cek `scripts/21_holdout_sample.py` GOLDEN_FILES). 2 agent Sonnet blind (±600rb token)
  → `scripts.22_holdout_accuracy` → adjudikasi manual vs PDF. Menguji apakah fix 7+8
  benar-benar menaikkan akurasi ATAU hanya menukar kelas error.
- **(b) Redefinisi gate berbasis bukti terkumpul** — vonis/tuntutan/daerah/tahun lolos +
  kerugian dilaporkan dengan taksonomi error lengkap (D18–D24) + robustness excluding
  multi-terdakwa + bound atenuasi D3 di paper. **WAJIB ditulis di DECISIONS sebagai
  keputusan user, bukan keputusan agent.**

**Bahan untuk memutuskan (jangan sembunyikan dari user):** akurasi holdout SEGAR tidak
konvergen lintas 5 ronde — vonis 100→85→85→95→85, kerugian 72→79→90→85→80. Asumsi
"ekor panjang yang menipis" tidak lolos ujinya sendiri. Pada n=20 Wilson terlalu lebar
untuk memisahkan 85% dari 90%, jadi R6 pun belum tentu memutuskan. Argumen pro-(a):
kelas R5 spesifik dan sudah tertutup, jadi R6 menguji hipotesis yang jelas.

## Yang terjadi di session 19

**Recovery handoff s18 tuntas** (langkah 1–6): re-ekstraksi R5 terverifikasi selesai
(mulai 14:36:17, tepat setelah commit fix `4d965f0` 14:35:40), audit tipikor bersih.

**Ronde fix 6** (`e94aa05`) — dari regresi yang ditangkap script 24, BUKAN dari holdout.
858 K/Pid.Sus/2022 tuntutan db=84 human=120: strategi 1a `extract_tuntutan_bulan`
(amar tuntutan tanpa kata "penjara") dicoba tuntas SEBELUM 1b sehingga menang tanpa
memandang posisi; dokumen memakai "menjatuhkan pidana **atas diri** Terdakwa" yang tak
tertangkap 1a → 1a menjangkau ~2000 char ke depan dan menyambar amar PN yang dikutip.
Fix: 1a+1b dinilai bersama, **match valid paling awal menang**. Tuntutan training-set
93.7% → 97.5% (memperbaiki 3 kasus, bukan 1). Detail D22.

**Holdout R5** (blind, 2 agent, n=20, 16 mismatch diadjudikasi manual vs PDF) →
**G2 GAGAL**: vonis **85%** (REGRESI dari R4 95%), kerugian **80%**, tuntutan 95%,
daerah/tahun/nama 100%. 8 error parser dikonfirmasi + 8 flip 0→1 (konvensi/error
anotator). Alasan per baris ada di kolom `adjudication` pada
`data/golden_set/holdout_r5_validated.csv`. Detail D23.

**D24 — temuan terpenting sesi ini.** Bug vonis R5 bukan cuma statistik akurasi: pemindaian
seluruh populasi analisis (baca ulang 260 PDF) menemukan **3 terdakwa yang DIBEBASKAN/LEPAS
tercatat dengan vonis fiktif** — 1052 K/2022 (Fakhri Hilmi, kasasi terdakwa dikabulkan, bebas
dari semua dakwaan; DB=96 bulan = **vonis PT yang justru DIBATALKAN**), 3247 K/2019 (DB=12),
4597 K/2021 (ontslag; DB=60) — plus **6 dokumen tanpa jangkar amar** (692 K/2015, 631 K/2015,
196 PK/2014, 2240 K/2014, 1964 K/2015, 149/Pid.Sus-TPK/2025/PN Sby). Total ±9/260 = 3,5%.
Vonis = VARIABEL TERIKAT regresi inti Paper 4, jadi ini TIDAK bisa diselesaikan dengan
disclosure; perbaikan wajib di kedua opsi keputusan.

**Ronde fix 7** (`cefae19`) — 3 kelas vonis + 1 kelas kerugian, test-first, diverifikasi
pada PDF ASLI (bukan cuplikan):
(1) header `MENGADILI,Menolak` (KOMA) tak cocok pola mana pun → NOL jangkar di dokumen
240rb char → fallback menyapu angka kasus PEMBANDING;
(2) `MENGADILI SENDIRI`/`MENGADILI KEMBALI` kini menjadi jangkar — dulu sengaja
dikecualikan agar prosa "MA akan mengadili sendiri perkara ini" tak tertangkap, sekarang
diterima HANYA jika diikuti verba amar (prosa tetap tidak cocok, ada testnya);
(3) **deteksi bebas dipindah ke DEPAN sapuan kalimat** — dulu jalan paling akhir sehingga
amar pembebasan kalah dari usulan dissent atau dari vonis yang baru saja dianulir; dijaga
POSISI, jadi "bebas primair lalu dipidana subsidair" tetap menghasilkan vonis;
(4) kerugian: angka MENDAHULUI labelnya ("terdapat selisih pembayaran sebesar RpX **yang
merupakan** kerugian keuangan Negara").
Hasil: 4597 60→0, 1052 96→0, 3247 12→0, 1254 PK 12→0, 196 PK 12→84, 2505 PK Rp329,7M→Rp139,0M.

**Ronde fix 8** (`dfc6ec4`) — script 24 menangkap regresi yang DIBUAT ronde 7:
2997 PK/2025 kerugian 46,6M→31,9M. Bypass blocker ronde 7 terlalu lebar; Rp31,9M adalah
SISA setelah pemulihan Rp13,1M. Bypass dipersempit ke "membayar"/"pembayaran" saja +
guard konteks pemulihan. Konvensi yang ditegakkan: **pengembalian/pemulihan/perbaikan oleh
terdakwa TIDAK mengurangi kerugian yang ditetapkan** (sama dengan adjudikasi 1288 K/2020).

**Script 24 diperbaiki**: menghormati override adjudikasi (bandingkan nilai parser terarsip)
sehingga kasus yang sudah diputus tidak terbaca sebagai regresi permanen. R5 didaftarkan
ke `scripts/21` (exclusion) dan `scripts/24` (rescore).

## Angka (lintasan; arah SANGAT stabil, magnitudo bergeser per ronde)

| | R5 | R6 | R7 | R8 |
|---|---|---|---|---|
| n populasi analisis | 260 | 260 | **257** | TBD |
| elastisitas tuntutan~kerugian | 0.110 | 0.115 | 0.117 | TBD |
| elastisitas vonis~kerugian | 0.135 | 0.135 | 0.134 | TBD |
| anchor R² (vonis~tuntutan) | 0.645 | 0.658 | 0.651 | TBD |
| R²(tuntutan\|fakta) | 0.357 | 0.377 | 0.384 | TBD |
| R²(vonis\|fakta) | 0.466 | 0.466 | 0.465 | TBD |
| **gap** | −0.110 | −0.089 | **−0.081** | TBD |
| rescore vonis (100 anotasi, batas ATAS) | — | 94% | **97%** | TBD |

**Wajib masuk paper**: klaim asli Paper 4 ("prosecutors less predictable") DIDUKUNG di
semua versi data bersih — arah tidak pernah berbalik. TAPI gap menyempit monoton seiring
parser membaik (0.110→0.089→0.081): sebagian "tuntutan lebih sulit diprediksi" ternyata
error pengukuran pada tuntutan, bukan diskresi jaksa. Magnitudo harus dinyatakan sensitif
terhadap kualitas ekstraksi; jangan klaim angka gap sebagai temuan keras.

## Setelah gate diputuskan → H0.3 update Paper 4

Angka DB FINAL (bukan preliminer) ke §4.2/§5.3/abstrak; akurasi per-field golden50 +
holdout R1–R5 masuk paper; paragraf metodologi "distribusi keanehan dokumen berekor
panjang; holdout berulang + rescore lintas-ronde satu-satunya validasi jujur; bug parser
mengaburkan temuan; 3 putusan bebas sempat membawa vonis fiktif ke populasi analisis".
Re-run `scripts.16_prosecutorial_analysis` + `scripts.18`. Lalu G4 editor-sim AJC (sesi
agent SEGAR) → rebuild DOCX/PDF → user submit.

## HANYA-USER (±3 jam, bottleneck program, tertunda 4 bulan)

1 email co-author hukum (UB/UMM/Unair) · 1 email penulis paper terdekat (komentar SSRN
6580258) · 1 pembaca eksternal draft · 1 kopi mantan jaksa · akun Zenodo (rilis = v1.1
PASCA fix, jangan v1.0). G3 & G5 masih 🔴 dan HANYA user yang bisa menghijaukan.

## Verifikasi cepat

```bash
python -m pytest tests/ -q                 # 246 passed, 2 xfailed
python -m scripts.23_tipikor_audit         # 465/14/0 — WAJIB tiap re-ekstraksi
python -m scripts.24_holdout_rescore       # 100 anotasi, harus 0 regresi
python scripts/19_fair_comparison.py       # n & elastisitas DB terkini
```
- Branch `autoresearch/apr9-textfeatures` (rename ditunda, D10) · Backup DB lama:
  `data/korupsinlp_pre_reparse_s17.db` · SSRN: P2=6574140, P4=6580258
- Test regresi parser: `tests/test_holdout_bugs.py`, `_r2_`, `_r3_`, `_r4_`, `_r5_`,
  `test_rescore_regressions.py`. Jalankan pada SETIAP perubahan parser.
