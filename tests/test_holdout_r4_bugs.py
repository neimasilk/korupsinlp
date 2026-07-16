"""Regression tests for kerugian bugs found by holdout R4 blind validation.

Vonis passed R4 at 95% — these three are all kerugian phrasing classes.
"""
from src.parser.fields import extract_kerugian_negara

# 1958 K/Pid.Sus/2021 — component picked over the explicit summed total
# introduced by "sehingga total kerugian negara".
SNIPPET_SEHINGGA_TOTAL = (
    "perbuatan terdakwa mengakibatkan kerugian negara untuk tahun 2016 dan "
    "2017 sebesar rp400.036.812,00 (empat ratus juta tiga puluh enam ribu "
    "delapan ratus dua belas rupiah) ditambah kekurangan perhitungan "
    "rp73.071.242,00 (tujuh puluh tiga juta tujuh puluh satu ribu dua ratus "
    "empat puluh dua rupiah) sehingga total kerugian negara rp473.107.955,00 "
    "(empat ratus tujuh puluh tiga juta seratus tujuh ribu sembilan ratus "
    "lima puluh lima rupiah) sesuai laporan hasil audit bpkp"
)

# 3040 K/Pid.Sus/2021 — reversed word order: "negara dirugikan sebesar RpX"
# (MA's own finding in kasasi reasoning), not matched by kerugian/merugikan
# patterns.
SNIPPET_NEGARA_DIRUGIKAN = (
    "bahwa atas perbuatan terdakwa bersama drs. hadi suharto, m.si., dan "
    "drs. hendra siswa pudjiana, negara dirugikan sebesar "
    "rp1.154.310.000,00 (satu miliar seratus lima puluh empat juta tiga "
    "ratus sepuluh ribu rupiah)"
)

# 1969 K/Pid.Sus/2020 — the 300-char sebesar-anchor gap crossed from a
# kerugian mention into a FINE clause ("pidana denda masing-masing sebesar
# rp200.000.000,00"); fines are not state losses. The real figure follows.
SNIPPET_DENDA_NOT_LOSS = (
    "menimbulkan kerugian keuangan negara serta menghukum para terdakwa "
    "rianto dan lasmi islamiah dengan pidana penjara masing-masing selama 4 "
    "(empat) tahun dan 6 (enam) bulan, serta pidana denda masing-masing "
    "sebesar rp200.000.000,00 (dua ratus juta rupiah) yang mana apabila "
    "denda tersebut tidak dibayarkan diganti dengan pidana kurungan; "
    "menimbang: - kerugian keuangan negara dalam kegiatan pengelolaan bibit "
    "sawit kecambah tahun anggaran 2017 di desa limbung, kabupaten bangka "
    "barat yang diakibatkan perbuatan dan kesalahan para terdakwa bersama "
    "dengan sdr. supendi selaku direktur cv. anugerah sebesar rp204.979.000 "
    "(dua ratus empat juta sembilan ratus tujuh puluh sembilan ribu rupiah)"
)


def test_kerugian_prefers_sehingga_total_over_component():
    assert extract_kerugian_negara(SNIPPET_SEHINGGA_TOTAL) == 473107955.0


def test_kerugian_reversed_negara_dirugikan():
    assert extract_kerugian_negara(SNIPPET_NEGARA_DIRUGIKAN) == 1154310000.0


def test_kerugian_skips_fine_amount():
    assert extract_kerugian_negara(SNIPPET_DENDA_NOT_LOSS) == 204979000.0
