"""Regression tests for parser bugs found by holdout R5 blind validation.

Three vonis classes, all of which put a fabricated prison term on an acquitted
defendant or on an unanchored document (DECISIONS D23/D24):

  (a) the amar header uses a COMMA ("MENGADILI,Menolak") — no header pattern
      matched, so a 240k-char document had ZERO anchors and fell through to a
      whole-text sweep that picked up a COMPARISON case (196 PK/PID.SUS/2014);
  (b) the operative re-adjudication amar "MENGADILI SENDIRI" / "MENGADILI
      KEMBALI" was deliberately not treated as a header (to keep the prose
      "Mahkamah Agung akan mengadili sendiri perkara ini" out), so the MA's own
      amar was never anchored;
  (c) acquittal detection ran LAST, after the generic sentence sweep, so an
      ontslag/bebas amar lost to a dissenting opinion's proposed term or to the
      very sentence the MA had just annulled (4597 K/2021, 1052 K/2022,
      3247 K/2019).

Plus one kerugian class: the figure PRECEDES its label ("terdapat selisih
pembayaran sebesar RpX yang merupakan kerugian keuangan Negara").
"""
from src.parser.fields import (
    _find_all_mengadili,
    extract_kerugian_negara,
    extract_vonis_bulan,
)

# 196 PK/PID.SUS/2014 — "MENGADILI,Menolak" (comma, merged). The PK is
# rejected, so the kasasi sentence quoted above (7 tahun) stands. The old code
# found no header at all and swept up "1 (satu) tahun 4 (empat) bulan" from a
# comparison case cited in the PK petition.
SNIPPET_COMMA_HEADER = (
    "putusan Mahkamah Agung Nomor 1921 K/PID.SUS/2013: MENGADILI SENDIRI"
    "-Menyatakan TerdakwaNAZARSYAH, S.STPbinMUHAMMAD SEMAN,tersebut di atas "
    "terbukti secara sah dan meyakinkan bersalah melakukantindak pidana "
    "“KORUPSI SECARA BERSAMA-SAMA DANBERLANJUT”;-Menjatuhkan pidana "
    "oleh karena itu kepada Terdakwa tersebut dengan pidanapenjara selama 7 "
    "(tujuh)tahundan denda Rp500.000.000,00; "
    "Bahwa terpidana lain dalam perkara serupa hanya dijatuhi hukuman pidana "
    "penjara 1 (satu)tahun4(empat) bulan dan subsidairRp50.000.000,00; "
    "MENGADILI,Menolak permohonan Peninjauan Kembali dari Pemohon Peninjauan"
    "Kembali/Terpidana:NAZARSYAH, S.STP.binMUHAMMAD SEMANtersebut;"
    "Menetapkan bahwa putusan yang dimohonkan peninjauan kembalitersebut "
    "tetap berlaku;"
)

# 4597 K/Pid.Sus/2021 — MA grants the defendant's kasasi and releases him
# (ontslag). A dissenting opinion proposing 5 tahun follows the amar; the old
# code's sentence sweep reached it before acquittal detection ran.
SNIPPET_ONTSLAG_WITH_DISSENT = (
    "M E N G A D I L I: Mengabulkan permohonan kasasi dari Pemohon Kasasi/"
    "Terdakwa JUNAEDI tersebut; Membatalkan putusan Pengadilan Tinggi "
    "Tanjungpinang Nomor 5/PID.SUS-TPK/2021/PT TPG; MENGADILI SENDIRI: "
    "1. Menyatakan Terdakwa JUNAEDI terbukti melakukan perbuatan yang "
    "didakwakan Penuntut Umum, tetapi perbuatan itu tidak merupakan suatu "
    "tindak pidana; 2. Melepaskan Terdakwa JUNAEDI tersebut oleh karena itu "
    "dari segala tuntutan hukum (ontslag van alle rechtsvervolging); "
    "3. Memerintahkan Terdakwa segera dikeluarkan dari tahanan; "
    "4. Memulihkan hak-hak Terdakwa dalam kemampuan, kedudukan dan harkat "
    "serta martabatnya; Bahwa terhadap putusan tersebut Hakim Anggota "
    "menyatakan pendapat berbeda (dissenting opinion) yang berpendapat "
    "permohonan kasasi Terdakwa harus ditolak dan menjatuhkan pidana kepada "
    "Terdakwa dengan pidana penjara selama 5 (lima) tahun dan denda sebesar "
    "Rp200.000.000,00;"
)

# 1052 K/Pid.Sus/2022 — DUAL kasasi: the prosecutor's is rejected ("menolak"
# appears first) while the defendant's is granted and he is acquitted. The
# leading "menolak" sent the old code down the quoted-lower-court path and it
# returned the annulled 8-tahun PT sentence.
SNIPPET_DUAL_KASASI_ACQUITTAL = (
    "MENGADILI:−Menolak permohonan kasasi dari Pemohon Kasasi II/Penuntut "
    "Umumpada Kejaksaan Negeri Jakarta Pusat tersebut;−Mengabulkan "
    "permohonan kasasi dari Pemohon Kasasi I/TerdakwaFAKHRI HILMI tersebut;"
    "−Membatalkan putusan Pengadilan Tindak Pidana Korupsi pada"
    "Pengadilan Tinggi DKI Jakarta Nomor 28/Pid.Sus-TPK/2021/PT.DKItanggal 27 "
    "September 2021 yang menjatuhkan pidana penjara selama 8 (delapan) tahun "
    "tersebut;MENGADILI SENDIRI:1.Menyatakan Terdakwa FAKHRI HILMI tidak "
    "terbukti secara sah danmeyakinkan bersalah melakukan tindak pidana "
    "sebagaimana yangdidakwakan dalam dakwaan primair dan dakwaan subsidair;"
    "2.Membebaskan Terdakwa FAKHRI HILMI oleh karena itu dari semuadakwaan "
    "penuntut umum;3.Memulihkan hak Terdakwa dalam kemampuan, kedudukan, "
    "harkat serta martabatnya;"
)

# The prose form must NOT be picked up as an amar header — this is the reason
# "sendiri" was excluded in the first place.
SNIPPET_SENDIRI_PROSE = (
    "Menimbang bahwa berdasarkan pertimbangan di atas, Mahkamah Agung "
    "berpendapat permohonan kasasi beralasan sehingga Mahkamah Agung akan "
    "mengadili sendiri perkara ini dengan amar putusan sebagaimana yang akan "
    "disebutkan di bawah ini;"
)

# 2505 PK/PID.SUS/2025 — the figure comes BEFORE its label. The parser took
# the appraisal total (Rp329,7 M) that the PK annulled.
SNIPPET_SELISIH_LABEL_AFTER = (
    "bahwa perbuatan Terpidana secara bersama-sama tersebut telah merugikan "
    "keuangan negara dengan jumlah total Rp329.718.300.000,00 (tiga ratus dua "
    "puluh sembilan miliar tujuh ratus delapan belas juta tiga ratus ribu "
    "rupiah); padahal yang dibayarkan sebesar Rp190.696.190.674,00 (seratus "
    "sembilan puluh miliar enam ratus sembilan puluh enam juta seratus "
    "sembilan puluh ribu enam ratus tujuh puluh empat rupiah) sehingga "
    "terdapat selisih pembayaran sebesar Rp139.022.245.653,00 (seratus tiga "
    "puluh sembilan miliar dua puluh dua juta dua ratus empat puluh lima ribu "
    "enam ratus lima puluh tiga rupiah) yang merupakan kerugian keuangan "
    "Negara;"
)


def test_comma_amar_header_is_detected():
    """'MENGADILI,Menolak' must anchor an amar section."""
    heads = _find_all_mengadili(SNIPPET_COMMA_HEADER.lower())
    assert heads, "no amar header detected — document falls back to a whole-text sweep"


def test_mengadili_sendiri_header_is_detected():
    heads = _find_all_mengadili(SNIPPET_ONTSLAG_WITH_DISSENT.lower())
    low = SNIPPET_ONTSLAG_WITH_DISSENT.lower()
    assert any(low.startswith("mengadili sendiri", h) for h in heads), \
        "the operative MENGADILI SENDIRI amar was not anchored"


def test_mengadili_sendiri_prose_is_not_a_header():
    assert not _find_all_mengadili(SNIPPET_SENDIRI_PROSE.lower())


def test_pk_rejected_keeps_upheld_kasasi_sentence_not_comparison_case():
    assert extract_vonis_bulan(SNIPPET_COMMA_HEADER) == 84


def test_ontslag_beats_dissent_proposed_sentence():
    assert extract_vonis_bulan(SNIPPET_ONTSLAG_WITH_DISSENT) == 0


def test_dual_kasasi_acquittal_beats_annulled_lower_sentence():
    assert extract_vonis_bulan(SNIPPET_DUAL_KASASI_ACQUITTAL) == 0


def test_kerugian_label_after_figure():
    assert extract_kerugian_negara(SNIPPET_SELISIH_LABEL_AFTER) == 139022245653.0
