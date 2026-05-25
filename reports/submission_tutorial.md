# Tutorial Submission: SSRN + CLSC
## Step-by-Step untuk Mukhlis Amien

---

## BAGIAN A: UPLOAD SSRN (Preprint — Priority Timestamp)

### Estimasi waktu: 15-20 menit

### Step 1: Buat akun SSRN
- Buka https://www.ssrn.com/
- Klik "Register" (pojok kanan atas)
- Isi: Mukhlis Amien, amien@ubhinus.ac.id, Universitas Bhinneka Nusantara
- Verifikasi email

### Step 2: Submit New Paper
- Setelah login, klik **"Submit a paper"** atau **"My Papers" → "Start New Submission"**
- Pilih: **"Submit to SSRN"**

### Step 3: Isi Metadata
Isi form dengan informasi berikut:

**Title:**
```
Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences
```

**Authors:**
```
Mukhlis Amien
Universitas Bhinneka Nusantara - Department of Informatics
Email: amien@ubhinus.ac.id
```

**Abstract:** Copy-paste dari baris pertama `paper2_draft.md` setelah "## Abstract" (paragraf yang dimulai dengan "We computationally analyze 671 Indonesian Supreme Court...")

**Keywords (pisahkan dengan koma):**
```
Corruption sentencing, Judicial discretion, Computational legal analysis, Indonesia, Sentencing disparity, Text mining
```

**JEL Classification (opsional, tapi recommended):**
```
K14 - Criminal Law
K42 - Illegal Behavior and the Enforcement of Law
```

**Subject Area / Network:**
- Pilih: **Criminal Justice Research Network (CJRN)** atau **Legal Scholarship Network (LSN)**
- Jika ada opsi sub-network: "Criminology" atau "Law & Economics"

### Step 4: Upload PDF
- Upload file: `reports/paper2_draft.pdf`
- SSRN hanya menerima PDF (bukan DOCX)

### Step 5: Set Access
- Pilih: **"Open Access"** (free to read)
- Jangan pilih opsi berbayar

### Step 6: Submit
- Review semua field
- Klik Submit
- SSRN akan memproses dalam **24-48 jam**
- Kamu akan dapat email konfirmasi + SSRN paper ID (contoh: SSRN 4986221)

### Step 7: Catat
- **Simpan SSRN paper ID** — ini akan kamu disclose saat submit ke CLSC
- URL akan berbentuk: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=XXXXXXX`

---

## BAGIAN B: SUBMIT KE CLSC (Journal — Peer Review)

### Estimasi waktu: 30-45 menit

### Step 1: Buat akun Springer Editorial Manager
- Buka https://www.editorialmanager.com/cris/
- "CRIS" adalah kode CLSC di Editorial Manager
- Jika URL tidak bekerja, buka: https://link.springer.com/journal/10611 → klik **"Submit manuscript"**
- Klik **"Register"** → isi data:
  - First name: Mukhlis
  - Last name: Amien
  - Email: amien@ubhinus.ac.id
  - Institution: Universitas Bhinneka Nusantara
  - Country: Indonesia
  - ORCID: 0000-0002-1848-167X

### Step 2: Start New Submission
- Setelah login, klik **"New Submission"** atau **"Submit New Manuscript"**
- Article Type: pilih **"Original Paper"** atau **"Original Article"**

### Step 3: Isi Title
```
Charge Type, Judicial Opacity, and the Limits of Prediction: A Computational Analysis of Indonesian Corruption Sentences
```

### Step 4: Isi Abstract
Copy-paste paragraf abstract dari `paper2_draft.md`. Dimulai dari:
"We computationally analyze 671 Indonesian Supreme Court corruption verdicts..."
sampai "...judicial discretion remains opaque from public documents."

### Step 5: Keywords
Masukkan satu per satu:
1. Corruption sentencing
2. Judicial discretion
3. Computational legal analysis
4. Indonesia
5. Sentencing disparity
6. Text mining

### Step 6: Author Information
- Mukhlis Amien (corresponding author)
- Institution: Universitas Bhinneka Nusantara, Malang, East Java, Indonesia
- Department: Informatics
- Email: amien@ubhinus.ac.id
- ORCID: 0000-0002-1848-167X

### Step 7: Upload Files

Upload dalam urutan berikut:

| Urutan | File | Designation di Editorial Manager |
|--------|------|--------------------------------|
| 1 | `reports/paper2_draft.docx` | **Manuscript** |
| 2 | `reports/paper2_cover_letter.docx` | **Cover Letter** |
| 3 | `reports/paper2_supplementary.docx` | **Supplementary Material** atau **Electronic Supplementary Material** |

**PENTING:**
- Manuscript HARUS dalam format **.docx** (bukan PDF) — Springer requirement
- Cover letter upload terpisah
- Supplementary upload terpisah

### Step 8: Suggested Reviewers (biasanya opsional tapi recommended)

Isi 3-5 reviewer yang kamu rekomendasikan. Saran:

| Nama | Bidang | Alasan |
|------|--------|--------|
| Masha Medvedeva | Legal NLP, ECHR prediction | Universiteit Groningen — paper kita mengkritik dan extends karyanya |
| Simon Butt | Indonesian anti-corruption law | University of Sydney — kita cite Butt (2011) |
| Andre Lage-Freitas | Computational legal analysis, Brazilian courts | Universidade Federal de Alagoas — peer di computational legal analysis |

**Catatan:** Kamu tidak HARUS kenal mereka. Ini hanya saran untuk editor.

### Step 9: Cover Letter
Jika ada text box untuk cover letter (selain upload file), copy-paste isi dari `paper2_cover_letter.md`.

### Step 10: Declarations / Ethics / Conflicts

Biasanya ada form terpisah:

| Question | Answer |
|----------|--------|
| Funding | This research received no external funding |
| Conflicts of interest | The author declares no conflicts of interest |
| Ethics approval | This study analyzes publicly available court documents published by the Indonesian Supreme Court. No human subjects were involved and no ethics approval was required. |
| Data availability | The CorpusKorupsi structured dataset and analysis scripts will be made available upon publication |
| Preprint disclosure | **This manuscript has been posted as a preprint on SSRN [masukkan URL SSRN-mu]** |

### Step 11: Additional Comments to Editor (opsional)
```
This manuscript presents the first large-scale computational analysis of Indonesian corruption sentencing. A preprint version has been posted on SSRN [URL]. The structured dataset and reproducible analysis code will be made publicly available upon acceptance.
```

### Step 12: Review & Submit
- Editorial Manager akan generate PDF gabungan dari semua file
- Review PDF tersebut — pastikan tabel, formatting, referensi terlihat benar
- Jika OK, klik **"Approve Submission"** atau **"Submit"**

### Step 13: Konfirmasi
- Kamu akan dapat email konfirmasi dari Springer
- Manuscript ID akan diberikan (contoh: CRIS-D-26-00XXX)
- **Simpan Manuscript ID ini**

---

## CHECKLIST FINAL

### Sebelum SSRN:
- [ ] PDF tergenerate dengan benar (`paper2_draft.pdf`)
- [ ] Baca cepat PDF — format, tabel, referensi OK
- [ ] Akun SSRN dibuat

### Sebelum CLSC:
- [ ] SSRN sudah di-upload (catat URL/ID)
- [ ] DOCX tergenerate (`paper2_draft.docx`)
- [ ] Cover letter updated (`paper2_cover_letter.docx`)
- [ ] Supplementary ready (`paper2_supplementary.docx`)
- [ ] Akun Editorial Manager dibuat

### Setelah submit keduanya:
- [ ] Simpan SSRN paper ID: _______________
- [ ] Simpan CLSC manuscript ID: _______________
- [ ] Catat tanggal submit: _______________
- [ ] Laporkan ke Claude di session berikutnya

---

## TIMELINE YANG DIHARAPKAN

| Event | Kapan |
|-------|-------|
| SSRN live (preprint visible) | 1-2 hari setelah upload |
| CLSC acknowledgment email | 1-3 hari setelah submit |
| CLSC editor assignment | 1-2 minggu |
| CLSC first review decision | 2-4 bulan |
| Jika R1 (revision): resubmit deadline | Biasanya 4-8 minggu dari decision |

---

*Tutorial ini generated 14 April 2026 untuk Paper 2 submission.*
*Semoga lancar — satu batu pertama yang dipindahkan.*
