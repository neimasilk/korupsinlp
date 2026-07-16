# Handoff — Session 18 (2026-07-16, update ke-2) → Next

## Status: RE-EKSTRAKSI RONDE 5 BERJALAN saat handoff ditulis (background `python -m scripts.03_parse_sample`, ±60 menit). **JIKA TERPOTONG, BACA "RECOVERY" DI BAWAH.** Semua parser fix ronde 2–5 SUDAH di-commit. G2: vonis 95% LOLOS (holdout R4); kerugian 85% → fix ronde 5 committed (`4d965f0`) → **holdout R5 = verdict G2 = milestone M1.**

> **Fakta keras di ledger**: `SUBMISSIONS.md`, `GATES.md`, `DECISIONS.md` (D14–D20),
> `MAP.md`, `ROADMAP.md`. File ini hanya narasi + recovery.

## ⚠️ RECOVERY — urutan WAJIB (state machine, lanjutkan dari langkah yang belum)

1. **Cek re-ekstraksi selesai**: `SELECT COUNT(*) FROM verdicts WHERE parsed_at LIKE '2026-07-%'`
   harus 693 dengan timestamp TERBARU (ronde 5 dimulai setelah commit `4d965f0`).
   Terpotong → jalankan ulang `python -m scripts.03_parse_sample` (idempoten, ±60 mnt).
2. **WAJIB `python -m scripts.23_tipikor_audit`** — pipeline menimpa flag is_tipikor;
   rescue TPK/PDT/TUN hanya ada di script 23. (Ekspektasi: 465 OK / 14 non-tipikor /
   0 kontaminasi sampel analisis.)
3. `python scripts/19_fair_comparison.py` → angka terkini. Lintasan sejauh ini
   (arah SANGAT stabil, magnitudo bergeser kecil per ronde fix):
   n: 237→248→255→261 · elasticity tuntutan~kerugian: 0.097→0.111→0.114→0.111 ·
   vonis~kerugian: ~0.13 · anchor R²: 0.647→0.663 · R²(vonis|fakta) − R²(tuntutan|fakta):
   −0.069→−0.076→−0.102 → **vonis LEBIH terprediksi dari fakta; klaim asli Paper 4
   ("prosecutors less predictable") DIDUKUNG di semua versi data bersih.**
4. **`python -m scripts.24_holdout_rescore`** (BARU, session 18 akhir) — re-skor 80
   anotasi R1–R4 vs DB terkini: cek REGRESI (kasus yang dulu benar wajib tetap benar;
   flip 1→0 = fix merusak sesuatu) + akurasi training-set (upper bound). Regresi → fix
   dulu sebelum R5.
5. **Holdout R5** (verdict G2): `python -m scripts.21_holdout_sample` (exclude kini 130:
   golden 50 + R1–R4 80) → 2 agent Sonnet BLIND. Prompt = versi R4 (lihat transkrip / poin
   kunci: hanya case_number+pdf_path; header MEMBACA TUNTUTAN vs PUTUSAN; dissent bukan
   amar; kutipan "atas nama" orang lain = kasus pembanding, abaikan; multi-terdakwa pilih
   SATU konsisten nama+tuntutan+vonis+kerugian, prefer Terdakwa I; bebas → kerugian ABSENT;
   kerugian ≠ uang pengganti/denda/suap/"kerugian perekonomian negara"; case_number output
   = string persis, BUKAN indeks) → `python -m scripts.22_holdout_accuracy` → **adjudikasi
   MANUAL tiap mismatch vs PDF** (aturan terdokumentasi di GATES.md + D18/D19).
6. **Verdict G2**: kerugian ≥90% adjudicated → **G2 HIJAU** (vonis sudah 95% di R4;
   fix ronde 5 tidak menyentuh jalur vonis — hasil R4 tetap berlaku; verifikasi via
   script 24 tanpa regresi vonis). Gagal lagi → lihat "KEPUTUSAN USER" di bawah.
7. G2 hijau → GATES.md update → **H0.3 update Paper 4** dengan angka DB FINAL (bukan
   preliminer): §4.2/§5.3/abstrak (arah = klaim asli), akurasi per-field golden50+holdout
   masuk paper, paragraf metodologi "distribusi keanehan dokumen berekor panjang; holdout
   berulang satu-satunya validasi jujur; bug parser mengaburkan temuan". Re-run
   `python -m scripts.16_prosecutorial_analysis` + `scripts.18` (robustness/figures).
   Lalu G4 editor-sim AJC (sesi agent segar) → rebuild DOCX/PDF → user submit.

## ⚠️ KEPUTUSAN USER jika kerugian R5 mendarat 85–90% lagi

Statistik jujur: pada n=20/ronde, akurasi sejati ~90% memantul di sekitar ambang
(Wilson ±10pp). Residual yang TIDAK fixable regex = atribusi per-terdakwa dokumen
multi-terdakwa (semantik). Opsi: (a) ronde fix+holdout lagi (frame sisa ~160 kasus,
±600rb token agent/ronde); (b) definisi ulang gate berbasis bukti terkumpul: vonis/
tuntutan/daerah/tahun lolos + kerugian dilaporkan dengan taksonomi error lengkap +
robustness excluding multi-terdakwa + bound atenuasi D3 di paper. Pilihan (b) WAJIB
ditulis di DECISIONS sebagai keputusan user, bukan keputusan agent.

## Ringkas 4 ronde holdout (blind + adjudikasi; detail D18–D20 + GATES.md)

| Ronde | vonis | kerugian | Kelas baru ditemukan → fix |
|---|---|---|---|
| R1 | 100% | 72% | ambang statutori; gap merged/dots; dot-cents; tuntutan tanpa "penjara" → `c2ac9a4` |
| R2 | 85% | 79% | preamble memperbaiki+uang pengganti; "mengadilimenolak" merged → dissent terambil; dokumen PT "menguatkan"; ejaan "primer"; komponen-vs-total; angka suap; bebas→kerugian NULL → `0e0d8eb` |
| R3 | 85% | **90%** | footer MA menyela amar di tengah angka; page-marker lama; kutipan kasus pembanding "atas nama" orang lain; "dakwaan kesatu primair" ordinal → `a341166` |
| R4 | **95%** | 85% | "sehingga total kerugian negara"; "negara dirugikan sebesar"; denda & ambang SEMA "sampai dengan" → `4d965f0` |

Suite test: **237 passed, 2 xfailed** — golden30 + 19 test regresi dari 4 ronde
(tests/test_holdout_bugs.py, _r2_, _r3_, _r4_). Jalankan pada SETIAP perubahan parser.

## Yang juga selesai session 18 (commit 7d71dc3…4d965f0)

- Review manifesto adversarial → `reports/manifesto_review_session18.md` (8 kritik).
- **Manifesto Amandemen 1** (§XII): kerangka Becker, status hipotesis dipajang, kalibrasi
  skala, aturan batu, B2 dikeraskan, E1↔E4, Prinsip 8, "auditable".
- **ROADMAP.md** dibuat (gate-driven; M1 = G2 hijau; jalur HANYA-USER dipisah).
- **D15 FIXED**: audit tipikor 693 → sampel analisis 0 kontaminasi; D17 (metadata kotor,
  70 NULL case_number — bahan datasheet v1.1).
- **D6 FIXED**: results.tsv un-gitignored + rekonsiliasi 0.626 = artefak seleksi adaptif;
  CV verdict mengunci H2 FALSIFIED.
- **D10 sebagian**: EKSEKUSI = arsip SUPERSEDED; CLAUDE.md dimutakhirkan.
- Metodologi holdout diperbaiki vs s17: **blind** (agent tak lihat parser), agree dihitung
  skrip (22), adjudikasi manual, arsip per-ronde (holdout_rN_*), rescore lintas-ronde (24).

## HANYA-USER (±3 jam, bottleneck program, tertunda 4 bulan)

1 email co-author hukum (UB/UMM/Unair) · 1 email penulis paper terdekat (komentar SSRN
6580258) · 1 pembaca eksternal draft · 1 kopi mantan jaksa · akun Zenodo (rilis = v1.1
PASCA fix, jangan v1.0).

## Verifikasi cepat

```bash
python -m pytest tests/ -q                 # 237 passed, 2 xfailed
python scripts/19_fair_comparison.py       # n & elasticity DB terkini
python -m scripts.24_holdout_rescore       # regresi lintas-ronde
```
- Branch `autoresearch/apr9-textfeatures` (rename ditunda, D10) · Backup DB lama:
  `data/korupsinlp_pre_reparse_s17.db` · SSRN: P2=6574140, P4=6580258
