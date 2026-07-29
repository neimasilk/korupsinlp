"""Regression tests for parser bugs surfaced by holdout R6 (n=50) and the
corpus-wide rescan that followed (session 19 → Ronde Fix 9).

Each snippet is verbatim text (or a faithful reduction) from the failing PDF.
These bugs survived R6's 98.0%/91.7% blind holdout — they are the long tail of
rare document classes the 50-case sample did not draw. Per D25/D26 the R6
numbers stand as the *validated* instrument accuracy; these fixes make the
released corpus at least this accurate, they do NOT re-certify it (no R7).
"""
from src.parser.fields import (
    extract_kerugian_negara,
    extract_tuntutan_bulan,
    extract_vonis_bulan,
    extract_nama_terdakwa,
)

# ---------------------------------------------------------------------------
# Bug 1 — 11891/11179/11312 K/PID.SUS/2025 (timah). The BPKP audit (Rp300 T)
# INCLUDES environmental-recovery cost (Rp11.9 T) which the MA explicitly
# REJECTS, ruling the sentencing basis is the financial loss only (Rp28.9 T).
# The audit figure is audit-anchored (tier 1) and outranks the plain kerugian
# mention; the MA's dispositive ruling "harus didasarkan pada ... senilai" must
# outrank it. Verbatim from 11891 K/PID.SUS/2025.
SNIPPET_AUDIT_REJECTED = (
    "berdasarkan hasil perhitungan BPKP telah terjadi Kerugian Keuangan Negara "
    "sebesar Rp300.003.263.938.131,14 dengan rincian sebagai berikut. "
    "Bahwa berdasarkan pertimbangan-pertimbangan di atas, maka dasar untuk "
    "menjatuhkan pidana kepada Terdakwa harus didasarkan pada kerugian "
    "keuangan negara senilai Rp28.933.575.919.431,14 "
    "(dua puluh delapan triliun sembilan ratus tiga puluh tiga miliar lima "
    "ratus tujuh puluh lima juta sembilan ratus sembilan belas ribu empat ratus "
    "tiga puluh satu rupiah empat belas sen)"
)

# Bug 3 — 9645 K/PID.SUS/2025. A procurement COMPONENT (Rp722 jt) is repeated
# throughout the facts; the MA's summing conclusion "dalam perkara a quo
# terdapat kerugian keuangan Negara sebesar" (Rp12,8 M) is the established
# total and must outrank the component. Verbatim reduction.
SNIPPET_COMPONENT_VS_TOTAL = (
    "atas kerugian keuangan Negara dalam kegiatan Pengadaan Komoditi Beras "
    "Premium sebesar Rp722.142.200,00 (tujuh ratus dua puluh dua juta rupiah). "
    "sebagaimana dakwaan Kesatu Primair, dalam perkara a quo; Bahwa dalam "
    "perkara a quo terdapat kerugian keuangan Negara sebesar "
    "Rp12.835.112.730,00 (dua belas miliar delapan ratus tiga puluh lima juta "
    "seratus dua belas ribu tujuh ratus tiga puluh rupiah)"
)

# Bug 2 — 10453 K/PID.SUS/2025. The "uang pengganti" figure (Rp392 jt) the
# defendant was ordered to pay is tied to a "kerugian Negara" mention and wins
# by earliest-occurrence; the MA conclusion "dalam perkara a quo terdapat
# kerugian keuangan Negara sebesar" (Rp1,26 M) is the established loss.
SNIPPET_UP_VS_AQUO = (
    "dan Terdakwa bertanggung jawab atas kerugian Negara yang dipakainya "
    "yaitu sebesar Rp392.184.403,00 (tiga ratus sembilan puluh dua juta rupiah). "
    "telah dipertimbangkan secara cukup dan tepat yaitu bahwa dalam perkara "
    "a quo terdapat kerugian keuangan Negara sebesar Rp1.259.759.403,00 "
    "(satu miliar dua ratus lima puluh sembilan juta tujuh ratus lima puluh "
    "sembilan ribu empat ratus tiga rupiah)"
)

# Bug 4 — 905 K/Pid.Sus/2024 (363k-char KPK kasasi). No "Tuntutan Pidana"
# header exists as separate tokens: the PDF text is MERGED ("TuntutanPidana"),
# so the demand was dropped to NULL. Faithful reduction of the merged header
# + numbered demand amar.
SNIPPET_TUNTUTAN_MERGED_HEADER = (
    "MembacaTuntutanPidanaPenuntutUmumpadaKomisiPemberantasan Korupsi "
    "sebagaiberikut:1.Menyatakan TerdakwaPRASETIO NUGROHOtelah terbukti secara "
    "sah dan meyakinkan bersalah. 2.Menjatuhkan pidana terhadap "
    "TerdakwaPRASETIO NUGROHOdenganpidana penjara selama 11 (sebelas) tahun "
    "dan 3 (tiga) bulan sertapidanadenda sejumlah Rp1.000.000.000,00 "
    "(satiumiliar rupiah)subsidiair 6 (enam) bulan kurungan"
)

# Bug 6 — 905 K/Pid.Sus/2024. The identity block uses the MA spaced-letter
# artifact "N a m a:" (cf. "M E N G A D I L I"), which the plain "Nama" header
# regex misses, so a co-defendant cited in the evidence list was returned.
SNIPPET_NAMA_SPACED_HEADER = (
    "telah memutus perkara Terdakwa :N a m a:PRASETIO NUGROHO;"
    "Tempat lahir:Situbondo;Umur/tanggal lahir:43 tahun/29 Juni 1979;"
    "Jenis kelamin:Laki-laki"
)

# Bug 5 — 919 PK/Pid.Sus/2022 (a PK-rejected case). The standing sentence is
# the quoted kasasi amar, corrected in MONTHS ("8 bulan"), but the quoted-
# sentence finder only knew "tahun" — so it fell through and the demand's
# "1 tahun 6 bulan" (18) was grabbed as the vonis. (Case is non-tipikor — UU
# Perkebunan — but the quoted-bulan rule also serves genuine tipikor PK files.)
SNIPPET_PK_REJECTED_BULAN = (
    "Membaca Tuntutan Pidana ... 2. Menjatuhkan pidana terhadap Terdakwa "
    "tersebut oleh karena itu dengan pidana penjara selama 1 (satu) tahun "
    "dan 6 (enam) bulan. "
    "Membaca Putusan Pengadilan Negeri Kayuagung Nomor 318/Pid.Sus/2016 yang "
    "amar lengkapnya: 2. Menjatuhkan pidana terhadap Terdakwa tersebut oleh "
    "karena itu dengan pidana penjara selama 11 (sebelas) bulan. "
    "Membaca Putusan Mahkamah Agung Nomor 1090 K/Pid.Sus/2017 yang amar "
    "lengkapnya sebagai berikut: - Menolak permohonan kasasi dari Pemohon "
    "Kasasi/Terdakwa tersebut; - Memperbaiki Putusan Pengadilan Tinggi "
    "Palembang Nomor 15/PID/2017/PT PLG sekedar mengenai lamanya pidana, "
    "sehingga selengkapnya berbunyi sebagai berikut: 1. Menyatakan Terdakwa "
    "telah terbukti secara sah dan meyakinkan bersalah; 2. Menjatuhkan pidana "
    "terhadap Terdakwa tersebut oleh karena itu dengan pidana penjara selama "
    "8 (delapan) bulan; 3. Menetapkan barang bukti. "
    "M E N G A D I L I: Menolak permohonan peninjauan kembali dari Pemohon "
    "Peninjauan Kembali/Terpidana tersebut"
)


def test_kerugian_audit_rejected_by_majelis():
    """Bug 1: MA's dispositive ruling outranks the rejected audit total."""
    assert extract_kerugian_negara(SNIPPET_AUDIT_REJECTED) == 28933575919431.14


# Bug 1b — 11312 K/PID.SUS/2025 (companion timah file). The Rp28,9 T the MA
# applied appears ONLY as "kelebihan pembayaran yang tidak sebagaimana
# mestinya sebesar Rp..." (an improper excess payment = the established
# loss); the Rp300 T BPKP audit the MA rejected is stated three times. The
# excess-payment formula must outrank the rejected audit.
SNIPPET_KELEBIHAN_PEMBAYARAN = (
    "Penghitungan Kerugian Keuangan Negara, dalam perkara a quo sejumlah "
    "Rp300.003.263.938.131,14 (tiga ratus triliun rupiah). Bahwa membuat "
    "perjanjian dengan Terdakwa tidak melalui studi kelayakan yang memadai, "
    "sehingga terjadi kelebihan pembayaran yang tidak sebagaimana mestinya "
    "sebesar Rp28.933.575.919.431,14 (dua puluh delapan triliun sembilan ratus "
    "tiga puluh tiga miliar lima ratus tujuh puluh lima juta sembilan ratus "
    "sembilan belas ribu empat ratus tiga puluh satu rupiah empat belas sen)"
)


def test_kerugian_kelebihan_pembayaran_outranks_audit():
    """Bug 1b: 'kelebihan pembayaran ... tidak sebagaimana mestinya' is the loss."""
    assert extract_kerugian_negara(SNIPPET_KELEBIHAN_PEMBAYARAN) == 28933575919431.14


# Regression guard (ronde 9): the a-quo conclusion must NOT elevate a figure
# that is elsewhere stated as a recovery REMAINDER. 2997 PK/Pid.Sus/2025 — gross
# loss Rp46,6 M, partial recovery Rp13,1 M, remainder Rp31,9 M. The remainder is
# restated both as "masih tersisa kerugian ... sebesar" AND "dalam perkara a quo
# terdapat kerugian ... sebesar"; the gross established loss (46,6 M) must win.
SNIPPET_AQUO_IS_REMAINDER = (
    "telah menimbulkan kerugian keuangan Negara sebesar Rp46.617.192.219,00 "
    "(empat puluh enam miliar enam ratus tujuh belas juta rupiah). "
    "telah terdapat pemulihan kerugian keuangan Negara sebesar "
    "Rp13.101.947.514,00 dan masih tersisa kerugian Negara sebesar "
    "Rp31.898.052.486,00 (tiga puluh satu miliar delapan ratus sembilan puluh "
    "delapan juta rupiah) yang merupakan kerugian keuangan Negara. "
    "yang mana dalam perkara a quo terdapat kerugian keuangan Negara sebesar "
    "Rp31.898.052.486,00 (tiga puluh satu miliar delapan ratus sembilan puluh "
    "delapan juta rupiah)"
)


def test_kerugian_aquo_restatement_of_remainder_does_not_outrank_gross():
    """Ronde-9 regression: a remainder restated as the a-quo loss still loses."""
    assert extract_kerugian_negara(SNIPPET_AQUO_IS_REMAINDER) == 46617192219.0


def test_kerugian_aquo_conclusion_outranks_component():
    """Bug 3: 'dalam perkara a quo terdapat ... sebesar' is the MA total."""
    assert extract_kerugian_negara(SNIPPET_COMPONENT_VS_TOTAL) == 12835112730.0


def test_kerugian_aquo_conclusion_outranks_uang_pengganti():
    """Bug 2: same MA-conclusion phrase outranks the uang-pengganti figure."""
    assert extract_kerugian_negara(SNIPPET_UP_VS_AQUO) == 1259759403.0


def test_tuntutan_merged_header():
    """Bug 4: merged 'TuntutanPidana' header still yields the demand (135 mo)."""
    assert extract_tuntutan_bulan(SNIPPET_TUNTUTAN_MERGED_HEADER) == 135.0


def test_nama_spaced_identity_header():
    """Bug 6: 'N a m a:' spaced artifact resolves to the defendant."""
    assert extract_nama_terdakwa(SNIPPET_NAMA_SPACED_HEADER) == "PRASETIO NUGROHO"


def test_vonis_pk_rejected_standing_sentence_in_bulan():
    """Bug 5: PK rejected → standing kasasi sentence (8 bulan), not the demand."""
    assert extract_vonis_bulan(SNIPPET_PK_REJECTED_BULAN) == 8.0
