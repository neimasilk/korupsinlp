# Handoff — Session 18 (2026-07-16) → Next

## Status: RE-EKSTRAKSI RONDE 2 BERJALAN saat handoff ditulis (153/693, ±11 dok/menit — task background `python -m scripts.03_parse_sample`). **KEMUNGKINAN TERPOTONG. BACA "RECOVERY" DI BAWAH SEBELUM ANALISIS APA PUN.** Semua pekerjaan lain sesi ini SUDAH di-commit (7d71dc3, c2ac9a4, 2eaa12d, f98ecf4).

> **Fakta keras program hidup di ledger, bukan file ini**: `SUBMISSIONS.md`, `GATES.md`,
> `DECISIONS.md`, `MAP.md`, dan (baru) `ROADMAP.md`. Baca kelimanya di awal sesi.
> File ini hanya narasi + recovery.

## ⚠️ RECOVERY — urutan WAJIB setelah re-ekstraksi selesai/terpotong

1. **Cek selesai**: `SELECT COUNT(*) FROM verdicts WHERE parsed_at LIKE '2026-07-16%'`
   → harus 693. Kurang = re-ekstraksi terpotong → jalankan ulang
   `python -m scripts.03_parse_sample` (idempoten, re-parse semua; ±60 menit).
2. **WAJIB re-run `python -m scripts.23_tipikor_audit`** — pipeline menimpa flag
   `is_tipikor` audit dengan versi teks-saja; logika rescue register TPK + PDT/TUN
   HANYA ada di script 23, tidak di pipeline. Lupa langkah ini = kasus TPK sah
   ter-flag 0 dan populasi analisis menyusut diam-diam.
3. `python scripts/19_fair_comparison.py` → angka baru (n akan berubah dari 237 —
   parser fix ronde 2 menambah coverage kerugian; angka lama preliminer: elasticity
   0.097, anchor R²=0.647, R²(vonis|fakta)=0.423 > R²(tuntutan|fakta)=0.319).
4. **Holdout R2** (penentu G2): `python -m scripts.21_holdout_sample` (sudah exclude
   70 kasus lama: golden 50 + holdout R1 20) → luncurkan 2 agent Sonnet BLIND
   (prompt sama sesi ini: hanya case_number+pdf_path, TANPA nilai parser; konvensi
   field lengkap ada di prompt sesi ini / lihat scripts/22 docstring). **Tambahan
   prompt dari pelajaran R1**: peringatkan agent membedakan kutipan di bawah header
   "MEMBACA TUNTUTAN" (= tuntutan JPU) vs "MEMBACA PUTUSAN ... PN" (= vonis) —
   error anotator R1 (11852) persis di situ.
5. `python -m scripts.22_holdout_accuracy` → **adjudikasi MANUAL setiap mismatch
   terhadap PDF** (R1: 1 dari 20 "mismatch" ternyata error anotator, parser benar).
6. **Verdict G2**: vonis & kerugian ≥90% (adjudicated) → G2 HIJAU → update GATES.md.
   Gagal → holdout R2 jadi training (JANGAN dipakai ulang), fix ronde 3, holdout R3.
   Ekspektasi jujur: 2 kasus atribusi per-terdakwa di R1 = ~10% sampel; jika R2
   menarik kasus serupa, kerugian bisa mendarat 85-90% — keputusan "refine gate
   spec vs hold the line" saat itu = keputusan user, tulis di DECISIONS.

## Yang terjadi session 18

1. **Review manifesto adversarial** (permintaan user) → `reports/manifesto_review_session18.md`
   (8 kritik: retorika skala 3-orde; teori "mengapa" absen dari konstitusi; batu =
   streetlight drift; B2 bottleneck aktif — 4 bulan 0 kontak eksternal; kontradiksi
   identitas tool-builder; E1↔E4 tabrakan; "tidak bisa dibantah" = overclaim; teori
   publikasi absen).
2. **Manifesto Amandemen 1** (§XII, 9 butir — semua kritik ditindaklanjuti): kerangka
   Becker masuk §IV + status hipotesis dipajang per-hipotesis; Batu 1 dikalibrasi
   (693, bukan ratusan ribu); aturan pemilihan batu (per edge; max 1 sumber/tahun;
   berpindah = DOI/peer-review); B2 dikeraskan (klaim substantif butuh G3/G5);
   resolusi E1↔E4 (rekaman-publik + rilis menunggu instrumen valid); Prinsip 8
   "Instrumen Sebelum Klaim"; §X.3 "auditable".
3. **ROADMAP.md dibuat**: M1 = G2 hijau; Horizon 0 (minggu ini) → 1 (dataset+Paper 4+
   HANYA-USER) → 2 (paper "mengapa" Edge 2) → 3 (kondisional); anti-goals eksplisit.
4. **D15 FIXED**: `is_tipikor` wired (db.py + pipeline + filter script 19); audit 693
   (`scripts/23`): 465 tipikor OK / 14 pasti non-tipikor (7 PDT/TUN + 7 Pid.Sus 2026,
   termasuk narkotika 961) / 119 suspect no-PDF / 95 no-text. **Sampel elasticity
   n=237: 0 kontaminasi.** D17 baru (metadata: 70 NULL case_number, 25 '?', 2 duplikat
   → wajib masuk datasheet v1.1). Detail: `data/tipikor_audit.csv`.
5. **Holdout R1 n=20 BLIND selesai + diadjudikasi** (perbaikan metodologi vs s17:
   agent tak melihat nilai parser; agree dihitung `scripts/22`, bukan oleh agent):
   **vonis 20/20 (100%)** — 1 "mismatch" = error anotator (11852, kutipan tuntutan
   tertukar amar PN; parser BENAR); **tuntutan 19/20 (95%)**; **kerugian 13/18 (72%,
   1 AMBIGUOUS**: 460 K/2015 dokumen inkonsisten internal 424.842rb vs 424.824rb);
   daerah 19/20; tahun 20/20; nama ~80% (bukan field klaim). File:
   `data/golden_set/holdout_20_{template,validation_A,validation_B,validated}.csv`.
6. **Parser fix ronde 2** (`c2ac9a4`, test-first `tests/test_holdout_bugs.py`, suite
   223 passed 2 xfailed): (a) angka ambang statutori Pasal 2/3 ("melebihi jumlah
   Rp100jt yakni sebesar RpX" → threshold-blocker di kiri-figur + pola sebesar-anchored);
   (b) gap ber-titik + teks merged ("keuangannegara...tomohoncq...sebesarrp59jt" →
   \s* + [\s\S] gap); (c) dot-cents cacat ("3.308.079.265.127.04" → grup akhir 2-digit
   = sen); (d) tuntutan tanpa kata "penjara" ("menjatuhkan pidana terhadap Terdakwa X
   selama 6 tahun 4 bulan"). **TIDAK di-fix (semantik, D18)**: atribusi kerugian
   per-terdakwa dokumen multi-terdakwa (2/18 R1; parser ambil total proyek, pengadilan
   pakai komponen per-terdakwa utk kategori Perma 1/2020) → disclosed + robustness
   excluding multi-terdakwa di paper; arah error konservatif utk klaim kompresi.
7. **D6 FIXED**: results.tsv un-gitignored + 5 baris pasca-pivot direkonstruksi.
   Rekonsiliasi: best single-split 0.6256 = artefak seleksi adaptif; CV verdict:
   TF-IDF −0.072 (p<1e-4 BURUK), structured +0.007 (ns), 3 keyword biner tipe-dakwaan
   +0.030 (p=0.002 — fitur fakta legal, bukan gaya bahasa) → **H2 FALSIFIED utuh**;
   kutip selalu angka CV, jangan val-split.
8. **D10 sebagian**: EKSEKUSI ditandai SUPERSEDED (arsip); CLAUDE.md dimutakhirkan
   (ROADMAP + skrip 20-23). Sisa: rename branch → tunda sampai Paper 4 terkirim.

## Setelah G2 hijau (urutan ROADMAP.md Horizon 0-1)

1. **H0.3 Update Paper 4** dengan angka DB final (bukan preliminer!): elasticity, n,
   anchor R², §4.2/§5.3/abstrak ditulis ulang — data bersih mendukung klaim ASLI
   ("prosecutors less predictable") via spec fair; + paragraf metodologi "bug parser
   mengaburkan temuan, instrumen bersih menajamkannya" + akurasi per-field golden50+
   holdout di paper. Re-run `scripts.16` (+ `scripts.18` bila ada) untuk robustness/fig.
2. G4 editor-sim vs scope AJC (sesi agent SEGAR, hanya abstrak+cover letter) →
   rebuild DOCX/PDF (pandoc) → user submit perdana AJC.
3. Jalur dataset paralel: datasheet v1.1 (693, akurasi per-field, konvensi tahun
   registrasi, D17 metadata, kebijakan etika E1↔E4) → Zenodo v1.1 (JANGAN v1.0) →
   data paper (G3 sudah hijau).
4. **HANYA-USER (±3 jam, ROI tertinggi, tertunda 4 bulan)**: 1 email co-author hukum
   (UB/UMM/Unair); 1 email penulis paper terdekat (komentar SSRN); 1 pembaca eksternal
   draft; 1 kopi mantan jaksa; akun Zenodo.

## Mode operasi (permintaan user, tersimpan di memori)

Hemat token: subagent mekanis = sonnet; Fable untuk penalaran inti; anotasi holdout
WAJIB blind + adjudikasi manual. Standar ilmiah tidak dikompromikan.

## Verifikasi cepat

```bash
python -m pytest tests/ -q                    # 223 passed, 2 xfailed
python scripts/19_fair_comparison.py          # n & elasticity DB terkini
python -m scripts.23_tipikor_audit            # restore flag is_tipikor pasca re-parse
```
- Branch: `autoresearch/apr9-textfeatures` (rename ditunda, D10)
- Backup DB pra-fix-s17: `data/korupsinlp_pre_reparse_s17.db`
- SSRN (tetap live): Paper 2 = 6574140 · Paper 4 = 6580258
