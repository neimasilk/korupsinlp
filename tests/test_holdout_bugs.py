"""Regression tests for parser bugs found by holdout-20 validation (session 18).

Each snippet is verbatim text (or a faithful reduction) from the failing PDF.
The two per-defendant attribution failures (56/Pid.Sus-TPK/2025/PN Kpg,
4189 K/Pid.Sus/2024) are NOT tested here: choosing the court-attributed
component of a multi-defendant project loss is semantic, out of regex reach —
documented as a known limitation (DECISIONS D18) and handled by robustness
analysis in the paper, not by the extractor.
"""
from src.parser.fields import (
    extract_kerugian_negara,
    extract_tuntutan_bulan,
    _parse_rupiah,
)

# 29 K/Pid.Sus/2018 — parser grabbed the statutory Pasal 2/3 threshold (Rp100jt)
# instead of the actual loss introduced by "yakni sebesar".
SNIPPET_THRESHOLD = (
    "ternyata kerugian keuangan negara dalam perkara a quo telah melebihi "
    "jumlah Rp100.000.000,00 (seratus juta rupiah) yakni sebesar "
    "Rp1.984.423.036,00 (satu miliar sembilan ratus delapan puluh empat juta "
    "empat ratus dua puluh tiga ribu tiga puluh enam rupiah)"
)

# 1009 K/PID.SUS/2013 — abbreviation periods ("Cq.") between "negara" and the
# figure break the [^.] gap, AND the pdfminer text is merged without spaces
# ("keuangannegara ... tomohonsebesarrp59.700.000,00"). Verbatim from the PDF.
SNIPPET_DOTTED_GAP = (
    "kerugian keuangannegara, dalamhal ini pemerintah kota tomohoncq. "
    "dinas pertanian,perkebunan,peternakandan perikanankota "
    "tomohonsebesarrp59.700.000,00"
)

# 27 K/PID.SUS/2026 — "merugikan Keuangan Negara c.q. PT Antam" gap plus a
# malformed cents separator (dot instead of comma: ...127.04).
SNIPPET_DOT_CENTS = (
    "kegiatan Emas Cucian dan Lebur Cap Emas telah merugikan Keuangan Negara "
    "c.q. PT Antam (Persero) Tbk sebesar Rp3.308.079.265.127.04 (tiga triliun "
    "tiga ratus delapan miliar tujuh puluh sembilan juta dua ratus enam puluh "
    "lima ribu seratus dua puluh tujuh rupiah empat sen)"
)

# 12367 K/PID.SUS/2025 — the JPU demand amar omits the word "penjara"
# ("Menjatuhkan pidana terhadap Terdakwa ... selama 6 tahun dan 4 bulan");
# the old pattern fell through to a quoted PN sentence (5 tahun 4 bulan = 64).
SNIPPET_TUNTUTAN_NO_PENJARA = (
    "Membaca Tuntutan Pidana Penuntut Umum pada Kejaksaan Negeri Tanggamus "
    "tanggal 14 Agustus 2025 sebagai berikut: 1. Menyatakan Terdakwa SARJONO, "
    "S. Sos. bin (almarhum) MUKMIN telah terbukti secara sah dan meyakinkan "
    "bersalah melakukan tindak pidana korupsi sebagaimana dalam Dakwaan "
    "Primair. 2. Menjatuhkan pidana terhadap Terdakwa SARJONO, S. Sos. bin "
    "(almarhum) MUKMIN selama 6 (enam) tahun dan 4 (empat) bulan dikurangi "
    "selama terdakwa menjalani tahanan, dengan perintah supaya Terdakwa tetap "
    "ditahan; 3. Menghukum Terdakwa SARJONO untuk membayar denda sebesar "
    "Rp250.000.000,00 (dua ratus lima puluh juta rupiah) subsider 6 (enam) "
    "bulan kurungan; 4. Membebankan Terdakwa SARJONO untuk membayar uang "
    "pengganti sebesar Rp90.000.000,00 dengan ketentuan apabila uang "
    "pengganti tersebut tidak dibayar paling lama 1 (satu) bulan sesudah "
    "putusan pengadilan ini berkekuatan hukum tetap, maka harta bendanya "
    "dapat disita oleh jaksa. Membaca putusan Pengadilan Tindak Pidana "
    "Korupsi pada Pengadilan Negeri Tanjung Karang yang amarnya: Menjatuhkan "
    "pidana terhadap Terdakwa dengan pidana penjara selama 5 (lima) tahun "
    "dan 4 (empat) bulan dan denda sejumlah Rp250.000.000,00"
)


def test_kerugian_skips_statutory_threshold_figure():
    assert extract_kerugian_negara(SNIPPET_THRESHOLD) == 1984423036.0


def test_kerugian_tolerates_abbreviation_dots_before_sebesar():
    assert extract_kerugian_negara(SNIPPET_DOTTED_GAP) == 59700000.0


def test_kerugian_handles_dot_cents_and_cq_gap():
    assert extract_kerugian_negara(SNIPPET_DOT_CENTS) == 3308079265127.04


def test_parse_rupiah_dot_cents():
    assert _parse_rupiah("3.308.079.265.127.04") == 3308079265127.04
    # regular thousands-only strings must be unaffected
    assert _parse_rupiah("1.500.000.000") == 1500000000.0
    assert _parse_rupiah("1.500.000.000,00") == 1500000000.0


def test_tuntutan_amar_without_penjara_keyword():
    assert extract_tuntutan_bulan(SNIPPET_TUNTUTAN_NO_PENJARA) == 76
