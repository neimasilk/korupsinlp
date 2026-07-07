# MAP.md — Peta Kausal Program (edge mana diidentifikasi data mana)

> **Aturan**: Setiap analisis/paper baru WAJIB menyebut edge mana yang diidentifikasinya
> SEBELUM dijalankan. Tidak bisa menyebut = streetlight drift (mode kegagalan F4).
> Sumber data baru dipilih berdasarkan edge yang belum terukur, bukan ketersediaan CSV.
> Maksimum SATU sumber data baru per tahun.

## Pertanyaan manifesto

**Mengapa sistem gagal menghentikan korupsi?** Dalam kerangka deterrence (Becker):

```
E[sanksi] = P(deteksi) × P(dituntut | deteksi) × P(divonis | dituntut) × severity(| divonis)
                │              │                       │                      │
              EDGE 1         EDGE 2                  EDGE 3                 EDGE 4
```

Korupsi persisten jika E[sanksi] << keuntungan. Program ini mengukur term demi term.

## Status per edge

| Edge | Term | Data yang mengidentifikasi | Status | Temuan |
|---|---|---|---|---|
| 4 | severity(\|divonis) | Korpus MA (v1.0); PN untuk fix seleksi kasasi | **TERUKUR** | Elasticity tuntutan~kerugian = 0.126; vonis~kerugian = 0.137; hakim anchor ke tuntutan (R²=0.60); teks tidak menambah prediksi (34+ eksperimen). **Severity flat terhadap skala korupsi — marginal deterrence ≈ 0 di term ini.** |
| 3 | P(divonis\|dituntut) | Amar di korpus (bebas/lepas vs pidana) + statistik banding MA | SEBAGIAN (amar ada di DB, belum dianalisis sistematis) | — |
| 2 | P(dituntut\|deteksi) | Laporan tahunan KPK/Kejagung, tabulasi ICW, SIPP | **BELUM DISENTUH — feasible, murah (data agregat)** | — |
| 1 | P(deteksi) | Tidak observable langsung. Proxy: temuan audit BPK → kasus; anomali procurement (opentender.net) → kasus | BELUM — Batu 2/3 manifesto | — |

## Konsekuensi strategis

1. **Semua paper sejauh ini hidup di Edge 4.** Menambah paper dari korpus yang sama =
   menambah resolusi pada satu term. Diminishing returns yang dirasakan itu nyata dan struktural.
2. **Batu berikutnya yang menjawab "MENGAPA": Edge 2 (funnel/atrisi).** Jika
   P(deteksi)×P(dituntut) berorde 10⁻³–10⁻⁴ DAN severity flat (sudah terbukti), maka
   "mengapa korupsi tidak berhenti" punya jawaban kuantitatif lengkap pertama untuk
   Indonesia: expected sanction mendekati nol dari DUA arah. Paper sintesis ini tidak
   bisa ditulis siapa pun tanpa korpus Edge 4 — itulah moat-nya.
3. **Scraping PN ≠ edge baru** — dia memperbaiki identifikasi Edge 4 (confound kasasi)
   dan menyediakan bahan text mining dengan n cukup. Layak, tapi jangan dihitung
   sebagai kemajuan ke arah "mengapa".

## Status hipotesis manifesto (kejujuran eksekusi)

| Hipotesis | Status | Catatan |
|---|---|---|
| H1 Disproporsionalitas | SEBAGIAN TERJAWAB (Edge 4) | Disproporsionalitas ada, tapi di hulu (tuntutan), bukan di hakim |
| H2 Normalisasi linguistik | **FALSIFIED** (temuan sah) | 34+ eksperimen; teks tidak prediktif pada n~300 MA |
| H3 Erosi temporal | BELUM TERUJI | Tuntutan justru naik 2014→2025; belum diuji terhadap peristiwa politik |
| H4 Dualisme struktural | BELUM TERUJI | Butuh clustering profil perkara |
| H5 Kegagalan umpan balik | **TIDAK IDENTIFIABLE dari putusan saja** | Butuh Edge 1-2 (data penindakan) |
| H6 Kegelapan terukur | **TIDAK IDENTIFIABLE dari putusan saja** | Butuh data struktural; konsep sudah jenuh di literatur akuntansi publik (Darkness Index dibunuh session 16) |
