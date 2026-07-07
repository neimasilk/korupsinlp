# Handoff — Session 17 (2026-07-07, sesi diakhiri ~16:00 auto-shutdown kantor) → Next

## Status: PARSER SUDAH DIPERBAIKI & DI-COMMIT (`ebcd238`). Re-ekstraksi 693 putusan BERJALAN saat handoff ditulis (214/693) — **KEMUNGKINAN TERPOTONG oleh shutdown. BACA "RECOVERY" DI BAWAH SEBELUM ANALISIS APA PUN.** Paper 2 = satu-satunya submission (desk-reject CLSC). Paper 4 BELUM PERNAH disubmit (terkonfirmasi via email SSRN — hanya preprint).

## ⚠️ RECOVERY RE-EKSTRAKSI (kerjakan PERTAMA di sesi berikutnya)

1. Cek kelengkapan: `python -c "import sqlite3; c=sqlite3.connect(r'data/korupsinlp.db'); print(c.execute(\"select count(*) from verdicts where date(parsed_at) >= '2026-07-07'\").fetchone()[0], '/693')"`
2. Jika < 693: DB dalam keadaan CAMPURAN (sebagian nilai parser lama, sebagian baru) — **JANGAN analisis**. Jalankan ulang sampai tuntas: `python -m scripts.03_parse_sample` (idempoten, re-parse semua baris, ±20-30 menit).
3. Backup DB pra-re-ekstraksi ada di `data/korupsinlp_pre_reparse_s17.db` (kalau butuh rollback/diff lama-vs-baru).
4. Setelah 693/693: `python -m scripts.16_prosecutorial_analysis` dan `python scripts/19_fair_comparison.py` → **bandingkan elasticity baru vs 0.126** (prediksi: naik, karena bug kerugian menukar angka audit dengan uang pengganti yang lebih kecil). Semua angka Paper 4 (abstrak, tabel §4, robustness, §5) harus di-update dari hasil baru.

> **Fakta keras program sekarang hidup di ledger, bukan di file ini**: `SUBMISSIONS.md`,
> `GATES.md`, `DECISIONS.md`, `MAP.md`. Baca keempatnya di awal sesi. File ini hanya narasi.

## Yang terjadi session 17

1. **Review kritis menyeluruh** → `reports/critical_review_session17.md`. Inti: (a) blind spot
   "mengapa korupsi" = peta kausal yang hilang, bukan teknik — korpus hanya mengukur 1 dari 4
   term expected-sanction; (b) 3 Truth-critique pra-submit Paper 4; (c) 4 mode kegagalan
   kolaborasi human-AI terdokumentasi (F1-F4) + mekanisasi perbaikannya; (d) mekanisme seleksi
   kritik Truth/Contribution/Reception.
2. **User mengonfirmasi semua paper rejected** → keputusan (D12): lanjut, tapi produk berubah —
   (1) dataset ber-DOI + data paper, (2) SATU flagship (Paper 4) lewat gate, (3) paper sintesis
   "why" dari Edge 2 (funnel). Bukan resubmit mekanis turun tangga.
3. **Paper 4 direvisi — G1 (Truth) HIJAU** (semua di `reports/paper4_draft.md`, belum di-rebuild DOCX/PDF):
   - **D1 benchmark AS**: agent riset USSC → realized elasticity AS = **0.288** (0.27–0.33, FY2012
     cross-tab N=8.507, R²=0.98). Headline SELAMAT & menguat: Indonesia 0.126 ≈ 44% dari gradien
     yang di-deliver AS di praktik. §2.1 ditulis ulang ke realized benchmark + caveat tail >$20M.
     Referensi baru: USSC 2013, Bennett et al. 2017, Hewitt 2016.
   - **D2 klaim diskresi**: regresi fair (`scripts/19_fair_comparison.py`, n=290):
     R²(tuntutan|fakta)=0.357 vs R²(vonis|fakta)=0.355 — klaim lama "prosecutors less predictable"
     SALAH; klaim baru lebih kuat: "diskresi masuk sekali di hulu, hakim merambatkan tanpa koreksi
     (elasticity vonis 0.137 ≈ tuntutan 0.126)". Abstrak/§4.2/§5.3/konklusi ditulis ulang.
   - **D3 attenuation** + **D5 seleksi kasasi & subsampel**: paragraf sensitivitas + disclosure di §5.5.
4. **Korpus v1.0 dibekukan**: `reports/corpus_release/korpuskorupsi_v1.csv` (693 records) +
   `SHA256SUMS_v1.0.txt`. Siap Zenodo — upload = aksi user (butuh akun). Datasheet masih basi (557).
5. **Golden set expansion DIMULAI, TERPOTONG**: sampel stratified 30 kasus →
   `data/golden_set/golden_expansion_30_template.csv` (24 dari populasi analisis per tercile
   kerugian + 6 tanpa-kerugian). 3 agent validasi dihentikan di tengah SEBELUM menulis CSV hasil
   — anotasi hilang, harus diluncurkan ulang (prompt: baca PDF penuh, ground truth independen,
   kutipan bukti, agree flags; lihat critical_review §III.1).
6. Higiene: CLAUDE.md dimutakhirkan (pointer ledger, skrip 01-19).

## UPDATE AKHIR SESI (2026-07-07 malam) — KRISIS INSTRUMEN DITEMUKAN

- **Koreksi fakta**: Paper 4 BELUM PERNAH disubmit ke jurnal (hanya SSRN 6580258; dikonfirmasi
  via email SSRN). Satu-satunya rejection program = Paper 2/CLSC. Ladder AJC→EJCPR→IJCJS utuh.
- **Validasi golden set n=30 stratified SELESAI** (2 agent Sonnet, mode hemat; hasil:
  `data/golden_set/golden_expansion_30_validated.csv`, skrip: `scripts/20_golden_accuracy.py`):
  **vonis 73.3%, kerugian 80.0%, tuntutan 93.3%**, daerah 93.3%, tahun/nama 96.7% (Wilson 95%).
  4 bug sistematis → DECISIONS.md **D14** (uang pengganti↔kerugian; vonis superseded/subsider +
  pola "menolak tapi memperbaiki"; putusan BEBAS diberi vonis; daerah fragment) dan **D15**
  (kontaminasi domain: kasus narkotika lolos ke korpus).
- **Konsekuensi**: G2 merah-terkonfirmasi; submit Paper 4 dan rilis Zenodo v1.0 DIBLOKIR.
  Elasticity 0.126 kemungkinan underestimate (kerugian tersubstitusi angka lebih kecil);
  arah temuan kompresi robust, angkanya akan berubah setelah re-ekstraksi.

## Yang selesai sesi ini (semuanya SUDAH di-commit)

- `dc65fff` — ledgers + review + revisi truth Paper 4 + corpus freeze (lihat commit message).
- `ebcd238` — **parser fix D14/D15, test-first, 9 putaran debug**: golden30 vonis 30/30,
  kerugian 30/30, daerah 30/30, tuntutan 29/30 (xfail multi-terdakwa), tahun 29/30 (xfail
  konvensi tahun registrasi); suite penuh **218 passed, 2 xfailed**; suite lama tetap 69/69.
  Bug kunci yang dipelajari (untuk konteks debug berikutnya): watermark MA menyela amar
  lintas halaman; teks PDF merged tanpa spasi; "dakwaan subsidiair" (tingkat dakwaan) ≠
  "subsidiair" (pidana pengganti); kutipan putusan sah selalu menyebut "Nomor" — pembeda
  dari kutipan permintaan JPU; amar bebas bisa dikutip di halaman 2 (jauh dari MENGADILI).
- Fixture permanen: `tests/fixtures/golden30/` + `tests/test_golden30.py` — jalankan pada
  SETIAP perubahan parser.

## Immediate next actions (urutan)

1. **Recovery re-ekstraksi** (lihat atas) → angka elasticity baru → update Paper 4.
2. **Validasi holdout 20 kasus SEGAR** (anti-overfit ke golden30): sampling stratified baru
   (pakai pola scripts di scratchpad/golden_sample.py → sudah hilang, tulis ulang ±20 baris,
   exclude 30+25 kasus lama), validasi via 2 agent Sonnet (prompt sama seperti sesi ini),
   hitung akurasi. Target: vonis/kerugian ≥90% → **G2 HIJAU**.
3. D15 wiring: `is_tipikor_document` sudah ada di fields.py tapi BELUM dipakai pipeline —
   tambahkan flag/filter saat re-parse atau post-hoc; audit berapa kasus non-tipikor di 693.
4. G4 editor-simulation vs scope AJC → rebuild DOCX/PDF (pandoc) → user submit perdana ke AJC.
5. Zenodo release = korpus v1.1 (pasca-fix, JANGAN rilis v1.0 yang sudah dibekukan — nilainya
   salah) + update datasheet (557→693, konvensi tahun, akurasi per-field) → dataset paper.
6. HANYA-USER: email co-author hukum (UB/UMM/Unair); 1 percakapan mantan jaksa (§5.1).
7. Setelah Paper 4 terkirim: scoping Edge 2 (funnel KPK/ICW) per MAP.md — batu "mengapa".

## Mode operasi (permintaan user, tersimpan di memori)

**Hemat token**: subagent mekanis → `model: sonnet`; Fable hanya untuk penalaran inti;
minimal agent; jangan re-read yang sudah di konteks. Standar ilmiah tidak dikompromikan.

## Verifikasi cepat

```bash
python -m pytest tests/ -q                    # 69 passed
python scripts/19_fair_comparison.py          # R² 0.357 vs 0.355; elasticity 0.126/0.137
```
- Branch: `autoresearch/apr9-textfeatures` (rename/merge = D10, masih OPEN)
- **SEMUA PEKERJAAN SESSION 17 BELUM DI-COMMIT** (review, ledgers, MAP, revisi paper4, script 19,
  template golden, corpus freeze, CLAUDE.md) — commit di awal sesi berikutnya setelah user setuju.

## SSRN (tetap live): Paper 2 = 6574140 · Paper 4 = 6580258
