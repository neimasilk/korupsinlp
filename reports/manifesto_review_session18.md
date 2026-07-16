# Review Manifesto vs Eksekusi — Session 18 (2026-07-16)

Review adversarial atas `MANIFESTO_KEADILAN_NUSANTARA.md` (per permintaan user), berpijak
pada ledger (SUBMISSIONS/GATES/DECISIONS/MAP/HANDOFF). Menghasilkan: Amandemen 1 manifesto
(§XII), `ROADMAP.md`, dan eksekusi Horizon 0. Ringkasan temuan:

## Yang terbukti bekerja dari manifesto

- Falsifiabilitas nyata: H2 difalsifikasi dan dicatat sebagai temuan sah (34+ eksperimen).
- Catatan kritis H1 ("kualitas ekstraksi menentukan kualitas klaim") memprediksi persis
  krisis instrumen G2 (akurasi vonis 73%, 2026-07-07).
- Batasan B1–B5 jujur dan berguna.

## Delapan kritik (semua ditindaklanjuti di Amandemen 1 / ROADMAP)

1. **Retorika skala meleset 3 orde besaran.** "Ratusan ribu putusan" vs realitas 693 dokumen,
   n analisis 237. Pada n ini manusia bisa membaca semuanya — argumen "hanya mesin yang bisa"
   belum berlaku. D13 mencatat warning gap manifesto↔riset yang diabaikan → desk-reject
   Paper 2 karena kontribusi. → Amandemen 1 butir 3: novelty dikoreksi ke "korpus pertama +
   pengukuran pertama", bukan skala.
2. **Manifesto tidak punya teori "MENGAPA".** H1–H6 tidak mendekomposisi pertanyaan sentral;
   kerangka Becker 4-term lahir belakangan di MAP.md sebagai tambalan. Akibat: semua paper
   berkerumun di satu term (severity) tanpa disadari 4 bulan. → Amandemen 1 butir 1.
3. **Daftar batu = streetlight drift terlembaga.** Batu 2–5 dipilih karena data tersedia,
   bukan karena edge belum terukur; tanpa kill criteria; H6 sudah dibunuh tapi masih berdiri
   di Batu 5. → Amandemen 1 butir 4 (aturan pemilihan batu).
4. **B2 "satu orang" adalah bottleneck aktif, bukan limitation pasif.** G3 sinyal eksternal=0,
   G5 pembaca eksternal=0, D11 OPEN; 4 bulan nol kontak manusia eksternal. → Amandemen 1
   butir 5; ROADMAP jalur HANYA-USER (±3 jam, ROI tertinggi program).
5. **Kontradiksi identitas tool-builder vs peneliti substantif.** B3 bilang "MRI untuk dokter"
   tapi flagship adalah klaim kriminologi substantif. → Amandemen 1 butir 9: tool-builder-first,
   urutan produk dataset→data paper→paper substantif.
6. **E4 vs E1 bertabrakan tanpa disadari**: rilis korpus = rilis data individu (nama terdakwa).
   → Amandemen 1 butir 6: argumen rekaman-publik ditulis eksplisit; rilis menunggu instrumen
   tervalidasi.
7. **"Metodologi yang tidak bisa dibantah" (§X.3) = overclaim** — instrumen sendiri baru
   terbukti 73% akurat. → Amandemen 1 butir 8: "auditable".
8. **Tidak ada teori publikasi**: audiens tak didefinisikan, "batu berpindah" tak punya
   definisi, data paper tak disebut padahal produk terdekat-selesai (G3 hijau satu-satunya).
   → Amandemen 1 butir 4 (definisi berpindah) + ROADMAP Horizon 1 Jalur A.

## Keputusan eksekusi session 18

- Holdout 20 kasus segar diluncurkan dengan perbaikan metodologi vs sesi 17: **blind
  annotation** (agent tidak melihat nilai parser; agree flags dihitung skrip, bukan agent).
  Sampler: `scripts/21_holdout_sample.py` (seed 20260716, 5 per tercile kerugian + 5 tanpa
  kerugian, exclude 50 kasus golden lama). Akurasi: `scripts/22_holdout_accuracy.py`.
- Milestone M1 = G2 hijau (vonis & kerugian ≥90%). Gagal → parser fix ronde 2 + holdout BARU.
