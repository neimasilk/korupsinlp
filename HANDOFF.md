# Handoff — Session 17 (2026-07-07) → Next

## Status: Paper 2 desk-rejected CLSC (satu-satunya yang pernah disubmit). **Paper 4 BELUM PERNAH disubmit** (terkoreksi 2026-07-07 — "semua paper reject" ternyata hanya Paper 2; lihat SUBMISSIONS.md). Program LANJUT dengan produk diubah. Fase A de-risk Paper 4 berjalan: G1 hijau, G2 (golden set) in progress.

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

## Immediate next actions (urutan)

1. **Commit seluruh kerja session 17** (belum ada yang di-commit).
2. **D14 parser fix, test-first**: 30 kasus tervalidasi → pytest fixtures; perbaiki 4 bug di
   src/parser/fields.py; D15 filter domain. Lalu **re-ekstraksi 693 → re-run scripts 16/19 →
   validasi holdout 20 kasus segar → update angka Paper 4** (elasticity, tabel, abstrak).
3. G4 editor-simulation vs scope AJC → rebuild DOCX/PDF → user submit perdana ke AJC.
4. Zenodo release = korpus v1.1 (pasca-fix) + update datasheet → dataset paper.
5. HANYA-USER: email co-author hukum (UB/UMM/Unair); 1 percakapan mantan jaksa (§5.1).
6. Setelah Paper 4 terkirim: scoping Edge 2 (funnel KPK/ICW) per MAP.md — batu "mengapa".

## Verifikasi cepat

```bash
python -m pytest tests/ -q                    # 69 passed
python scripts/19_fair_comparison.py          # R² 0.357 vs 0.355; elasticity 0.126/0.137
```
- Branch: `autoresearch/apr9-textfeatures` (rename/merge = D10, masih OPEN)
- **SEMUA PEKERJAAN SESSION 17 BELUM DI-COMMIT** (review, ledgers, MAP, revisi paper4, script 19,
  template golden, corpus freeze, CLAUDE.md) — commit di awal sesi berikutnya setelah user setuju.

## SSRN (tetap live): Paper 2 = 6574140 · Paper 4 = 6580258
