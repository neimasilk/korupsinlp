"""Regression tests for parser bugs found by holdout R2 blind validation (session 18).

Snippets are verbatim (or faithful reductions) from the failing PDFs.
"""
from src.parser.fields import (
    extract_kerugian_negara,
    extract_vonis_bulan,
)
from src.parser.pipeline import parse_verdict

# 11256 K/PID.SUS/2025 — MA rejected both cassations WITH correction, lowering
# the prison term to 2 years. The correction preamble lists "pidana uang
# pengganti" among the corrected items, which sat inside the subsidiary-context
# window and made the parser reject the true sentence, falling back to the
# superseded PN/PT term (2y6m).
SNIPPET_MEMPERBAIKI_PREAMBLE = (
    "m e n g a d i l i: - menolak permohonan kasasi dari pemohon kasasi "
    "i/penuntut umum pada kejaksaan negeri purwakarta tersebut; - menolak "
    "permohonan kasasi dari pemohon kasasi ii/terdakwa hj. yeyet suliawati "
    "binti (almarhum) udin sutardi tersebut; - memperbaiki putusan pengadilan "
    "tindak pidana korupsi pada pengadilan tinggi bandung nomor "
    "24/pid.sus-tpk/2025/pt bdg tanggal 6 agustus 2025 yang menguatkan "
    "putusan pengadilan tindak pidana korupsi pada pengadilan negeri bandung "
    "nomor 25/pid.sus-tpk/2025/pn bdg tanggal 21 mei 2025 tersebut mengenai "
    "pidana yang dijatuhkan kepada terdakwa dan pidana uang pengganti menjadi "
    "sebagai berikut: 1. menjatuhkan pidana kepada terdakwa dengan pidana "
    "penjara selama 2 (dua) tahun dan pidana denda sebesar rp100.000.000,00 "
    "(seratus juta rupiah) dengan ketentuan apabila pidana denda tersebut "
    "tidak dibayar maka diganti dengan pidana kurungan selama 1 (satu) bulan"
)

# 8/PID.TPK/2026/PT BDG — appellate (PT) document whose final amar only
# AFFIRMS the PN sentence ("menguatkan putusan ... PN Bandung"); the operative
# term (4 years) exists solely in the quoted PN amar earlier in the document.
SNIPPET_MENGUATKAN = (
    "membaca putusan pengadilan tindak pidana korupsi pada pengadilan negeri "
    "bandung nomor 120/pid.sus-tpk/2025/pn bdg tanggal 28 januari 2026 yang "
    "amar lengkapnya sebagai berikut: 1. menyatakan terdakwa arif "
    "fatkhurohman tidak terbukti melakukan tindak pidana sebagaimana dalam "
    "dakwaan primer; 2. membebaskan terdakwa dari dakwaan primer; 3. "
    "menyatakan terdakwa terbukti secara sah dan meyakinkan bersalah "
    "melakukan tindak pidana korupsi dalam dakwaan subsidair; 4. menjatuhkan "
    "pidana kepada terdakwa oleh karena itu dengan pidana penjara selama 4 "
    "(empat) tahun dan denda sejumlah rp200.000.000,00; "
    "menimbang bahwa tuntutan penuntut umum menuntut supaya terdakwa "
    "dijatuhi pidana penjara selama 8 (delapan) tahun; "
    "m e n g a d i l i: - menerima permintaan banding dari penuntut umum "
    "tersebut; - menguatkan putusan pengadilan tindak pidana korupsi pada "
    "pengadilan negeri bandung nomor 120/pid.sus-tpk/2025/pn bdg tanggal 28 "
    "januari 2026, yang dimintakan banding tersebut; - menetapkan agar "
    "terdakwa tetap berada dalam tahanan;"
)

# 2305 K/Pid.Sus/2016 — acquittal upheld by majority vote. The final amar is
# MERGED with the following verb ("mengadilimenolak..."), which none of the
# MENGADILI header variants matched, so extraction fell through to a full-text
# sweep that picked up the DISSENTING judge's proposed sentence.
SNIPPET_MERGED_MENGADILI = (
    "membaca putusan pengadilan tindak pidana korupsi pada pengadilan negeri "
    "jayapura nomor 36/pid.sus.tpk/2015/pn.jap tanggal 25 januari 2016 yang "
    "amar lengkapnya sebagai berikut: 1. menyatakan terdakwa senyorita "
    "rosliana, skm tidak terbukti secara sah dan meyakinkan bersalah "
    "melakukan tindak pidana sebagaimana didakwakan dalam dakwaan primair "
    "dan subsidair; 2. membebaskan terdakwa oleh karena itu dari semua "
    "dakwaan penuntut umum; "
    "menimbang bahwa ketua majelis berpendapat lain (dissenting opinion) dan "
    "berpendapat terdakwa terbukti dan dijatuhi pidana penjara selama 2 (dua) "
    "tahun; menimbang, bahwa oleh karena terjadi perbedaan pendapat maka "
    "putusan diambil dengan suara terbanyak; "
    "mengadilimenolak permohonan kasasi dari pemohon kasasi: jaksa/penuntut"
    "umum pada kejaksaan negeri jayapura tersebut;membebankan biaya perkara "
    "kepada negara;"
)

# 438 K/Pid.Sus/2021 — gratifikasi case with NO established state loss. The
# bribe amount was captured because pattern 2's gap crossed a clause boundary
# (';') from a doctrinal "kerugian" mention into the bribe sentence.
SNIPPET_BRIBE_NOT_LOSS = (
    "menimbulkan kerugian pada keuangan negara maka perbuatan tersebut adalah "
    "tindak pidana korupsi;-bahwa terdakwa selaku jaksa fungsional pada "
    "kejaksaan negeri yogyakarta, menerima hadiah berupa uang "
    "rp221.740.000,00 (dua ratus dua puluh satu juta tujuh ratus empat puluh "
    "ribu rupiah) dari kontraktor"
)

# 1682 K/Pid.Sus/2021 — long project name pushes the gap between "kerugian
# keuangan negara" and "sebesar Rp" to ~225 chars (old limit: 160).
SNIPPET_LONG_GAP = (
    "jumlah kerugian keuangan negara dalam pelaksanaan pekerjaan peningkatan "
    "kapasitas/uprating dan optimalisasi instalasi pengolahan air minum (ipa) "
    "pdam tirta tarum cabang telukjambe kabupaten karawang tahun 2015 adalah "
    "sebesar rp2.687.012.333,10 (laporan hasil audit kantor akuntan publik)"
)

# 1107 PK/Pid.Sus/2024 — the court sums two audited components; the parser
# picked a component (Rp27jt) instead of the explicit "dengan demikian ...
# merugikan keuangan negara sebesar" total (Rp424,91jt).
SNIPPET_COMPONENT_TOTAL = (
    "terdapat adanya kekurangan pekerjaan untuk 2 (dua) unit kapal 30 gt "
    "sebesar rp397.910.000,00 (tiga ratus sembilan puluh tujuh juta sembilan "
    "ratus sepuluh ribu rupiah) dan pendapat ahli dari bpkp provinsi sulawesi "
    "selatan yang menyatakan adanya kerugian keuangan negara dalam item "
    "pekerjaan administrasi 2 (dua) unit kapal sebesar rp27.000.000,00 (dua "
    "puluh tujuh juta rupiah). dengan demikian perbuatan terpidana tersebut "
    "telah merugikan keuangan negara sebesar rp424.910.000,00 (empat ratus "
    "dua puluh empat juta sembilan ratus sepuluh ribu rupiah)"
)


def test_vonis_memperbaiki_preamble_mentioning_uang_pengganti():
    assert extract_vonis_bulan(SNIPPET_MEMPERBAIKI_PREAMBLE) == 24


def test_vonis_pt_menguatkan_takes_quoted_pn_sentence():
    assert extract_vonis_bulan(SNIPPET_MENGUATKAN) == 48


def test_vonis_merged_mengadili_header_acquittal_not_dissent():
    assert extract_vonis_bulan(SNIPPET_MERGED_MENGADILI) == 0


def test_kerugian_not_bribe_amount_across_clause_boundary():
    assert extract_kerugian_negara(SNIPPET_BRIBE_NOT_LOSS) is None


def test_kerugian_long_project_name_gap():
    assert extract_kerugian_negara(SNIPPET_LONG_GAP) == 2687012333.10


def test_kerugian_prefers_dengan_demikian_total_over_component():
    assert extract_kerugian_negara(SNIPPET_COMPONENT_TOTAL) == 424910000.0


def test_pipeline_nulls_kerugian_on_acquittal():
    result = parse_verdict({}, SNIPPET_MERGED_MENGADILI +
                           " didakwa merugikan keuangan negara sebesar "
                           "rp2.182.855.401,00 berdasarkan audit bpkp papua")
    assert result["vonis_bulan"] == 0
    assert result["kerugian_negara"] is None
