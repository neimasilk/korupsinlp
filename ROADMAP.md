# ROADMAP.md — Peta Jalan Program (gate-driven, bukan semangat-driven)

> **Aturan**: (1) Urutan ditentukan gate GATES.md, bukan antusiasme — produk yang gate-nya
> paling hampir hijau dirilis lebih dulu. (2) Jalur AGENT dan jalur HANYA-USER dipisah
> eksplisit — bottleneck program saat ini adalah aksi manusia, bukan komputasi; item
> HANYA-USER tidak boleh diblokir oleh item agent, dan sebaliknya. (3) Setiap horizon punya
> definisi SELESAI yang bisa diverifikasi. (4) Roadmap ini turunan dari review manifesto
> 2026-07-16 (lihat `reports/manifesto_review_session18.md`) + MAP.md + GATES.md; konflik
> antara roadmap dan ledger → ledger menang.

## Milestone terdekat (definisi tunggal, tidak bisa ditawar)

**M1 = G2 hijau**: holdout 20 kasus segar, blind annotation, akurasi vonis & kerugian
≥90% terhadap DB pasca re-ekstraksi. Jika <90% → parser fix ronde 2 + holdout BARU
(20 kasus segar lagi — holdout yang gagal menjadi training, tidak boleh dipakai ulang).

## Horizon 0 — minggu ini (jalur AGENT, target: M1 + angka bersih)

| # | Item | Definisi selesai | Status |
|---|---|---|---|
| H0.1 | Validasi holdout 20 kasus segar (blind, 2 agent, agree flags dihitung skrip bukan agent) | `scripts/22_holdout_accuracy.py` mencetak akurasi + Wilson CI; keputusan G2 tercatat di GATES.md | **BERJALAN 2026-07-16** |
| H0.2 | D15: wire `is_tipikor_document` ke pipeline + audit kontaminasi 693 | Daftar kasus non-tipikor + flag di DB; angka n populasi analisis final | BERJALAN 2026-07-16 |
| H0.3 | Update Paper 4 dengan angka bersih (elasticity 0.097, n=237, anchor R²=0.647; §4.2/§5.3/abstrak ditulis ulang — arah kembali ke klaim asli via spec fair) | paper4_draft.md konsisten dengan DB baru; robustness 16/18 re-run | menunggu H0.1 hijau |
| H0.4 | D6: rekonstruksi results.tsv autoresearch | File lengkap, rekonsiliasi 0.626-vs-0.600 tertulis | antre |
| H0.5 | Amandemen 1 Manifesto (lihat bawah) | Committed | **SELESAI 2026-07-16** |

## Horizon 1 — 2–4 minggu (dua jalur paralel + jalur HANYA-USER)

**Jalur A — dataset (produk tercepat; G3-nya sudah hijau):**
1. Datasheet update: 557→693, akurasi per-field dari golden set + holdout, konvensi tahun
   registrasi, mojibake date_decided, kebijakan etika rilis (resolusi E1↔E4 — putusan
   adalah dokumen publik MA; argumen ditulis eksplisit, bukan diasumsikan).
2. Zenodo v1.1 (JANGAN v1.0 — nilai diketahui salah) → DOI.
3. Data paper (dataset descriptor) → submit. Kandidat venue: Data in Brief / Journal of
   Open Humanities Data / LREC-COLING data track — riset venue dulu, jangan asal.
   **Definisi selesai: DOI hidup + manuskrip data paper terkirim.**

**Jalur B — Paper 4 (flagship):**
1. G4 editor-sim vs scope AJC: sesi agent SEGAR, hanya abstrak+cover letter+scope. YES → lanjut.
2. Rebuild DOCX/PDF (pandoc) → user submit perdana ke AJC.
   **Definisi selesai: manuskrip terkirim ke AJC (bukan "siap dikirim").**

**Jalur HANYA-USER (D11/G3/G5 — total ±3 jam, ROI tertinggi seluruh program):**
| Aksi | Estimasi | Membuka gate |
|---|---|---|
| 1 email ke calon co-author hukum (UB/UMM/Unair) | 30 menit | D11, jangka panjang G3 |
| 1 email ke penulis paper terdekat Paper 4 (minta komentar preprint SSRN) | 30 menit | G3 sinyal eksternal |
| 1 kolega (siapa pun, non-hukum boleh) baca draft Paper 4 | 0 menit (delegasi) | G5 |
| 1 percakapan mantan jaksa/hakim (validasi §5.1) | 1–2 jam | Kualitas interpretasi |
| Buat akun Zenodo (untuk Jalur A) | 15 menit | D9/E4 |

## Horizon 2 — semester ini: paper "MENGAPA" (Edge 2, per MAP.md)

Funnel atrisi penindakan dari data agregat publik (laporan tahunan KPK, Kejagung, tabulasi
ICW, SIPP). Target estimand: P(dituntut|deteksi) dan P(divonis|dituntut) per orde besaran.
Gabungan dengan Edge 4 (severity flat, sudah terukur) = jawaban kuantitatif lengkap pertama
untuk "mengapa korupsi tidak berhenti" di Indonesia: expected sanction ≈ 0 dari dua arah.
- Prasyarat: Paper 4 terkirim (jangan mulai sebelum itu — fokus).
- Scoping 1 sesi: sumber data per term, ketersediaan, format. Baru putuskan GO/NO-GO.
- Ini SATU-SATUNYA sumber data baru 2026 (aturan MAP.md: max satu per tahun).

## Horizon 3 — kondisional (setelah H2 GO/NO-GO)

- **Scraping PN** (bukan edge baru; memperbaiki confound kasasi Edge 4 + n untuk text
  mining): hanya jika reviewer AJC memintanya ATAU paper funnel butuh denominator per daerah.
- Paper 3 (anchoring) keluar dari HOLD hanya jika data PN ada.
- Paper 5: tetap SSRN; tidak ada effort baru.

## Anti-goals (hal yang TIDAK dikerjakan, agar tertulis)

- TIDAK resubmit Paper 2 ke venue lain tanpa perubahan produk (D12).
- TIDAK menambah eksperimen text-features Edge 4 (H2 sudah FALSIFIED; 34+ eksperimen cukup).
- TIDAK memulai Batu 2/3/4 (BPK/APBD/LHKPN) sebelum paper funnel selesai — MAP.md
  melarang streetlight drift; batu dipilih per edge, bukan per ketersediaan CSV.
- TIDAK merilis korpus v1.0 yang dibekukan 2026-07-07 (nilai salah; rilis = v1.1).

## Log

| Tanggal | Event |
|---|---|
| 2026-07-16 | Roadmap dibuat (session 18) dari review manifesto + ledger. Holdout 20 diluncurkan (blind). Amandemen 1 manifesto ditulis. |
