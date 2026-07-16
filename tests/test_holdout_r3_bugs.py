"""Regression tests for parser bugs found by holdout R3 blind validation (session 18).

All three failures are appellate-chain classes; snippets are faithful
reductions of the failing PDFs.
"""
from src.parser.fields import extract_vonis_bulan
from src.parser.pipeline import parse_verdict

# 10690 K/PID.SUS/2025 — the MA footer/disclaimer block ("dalam hal anda
# menemukan inakurasi ... halaman 75 dari 75 halaman putusan nomor ...")
# interrupts the memperbaiki amar EXACTLY between the number and "(sepuluh)
# tahun"; this footer variant was not covered by _MA_WATERMARK_RE.
SNIPPET_FOOTER_SPLIT_AMAR = (
    "m e n g a d i l i: - menolak permohonan kasasi dari pemohon kasasi "
    "i/terdakwa ir. budi noviantoro tersebut; - menolak permohonan kasasi "
    "dari pemohon kasasi ii/penuntut umum pada kejaksaan negeri kota madiun "
    "tersebut; - memperbaiki putusan pengadilan tindak pidana korupsi pada "
    "pengadilan tinggi surabaya nomor 46/pid.sus-tpk/2025/pt sby tanggal 15 "
    "juli 2025 yang mengubah putusan pengadilan tindak pidana korupsi pada "
    "pengadilan negeri surabaya nomor 3/pid.sus-tpk/2025/pn sby tersebut "
    "mengenai pidana yang dijatuhkan kepada terdakwa menjadi pidana penjara "
    "selama 10 \x0c Dalam hal Anda menemukan inakurasi informasi yang termuat "
    "pada situs ini atau informasi yang seharusnya ada, namun belum tersedia, "
    "maka harap segera hubungi Kepaniteraan Mahkamah Agung RI melalui :\n"
    "Email : kepaniteraan@mahkamahagung.go.id    Telp : 021-384 3348 "
    "(ext.318)\n\nHalaman 75\n\n halaman 75 dari 75 halaman putusan nomor "
    "10690 k/pid.sus/2025  (sepuluh) tahun dan pidana denda sebesar "
    "rp500.000.000,00 (lima ratus juta rupiah) dengan ketentuan apabila "
    "pidana denda tidak dibayar, maka diganti dengan pidana kurungan selama "
    "6 (enam) bulan;"
)

# 2960 PK/PID.SUS/2025 — the PK reasoning cites a COMPANION case decision
# ("putusan PN Mataram ... atas nama terpidana TRISMAN ... penjara 2 tahun")
# closer to the final MENGADILI than the defendant's own chain; the quoted-
# decision fallback must skip decisions naming a different person.
SNIPPET_COMPANION_QUOTE = (
    "p u t u s a n nomor 2960 pk/pid.sus/2025 demi keadilan berdasarkan "
    "ketuhanan yang maha esa mahkamah agung memeriksa perkara tindak pidana "
    "korupsi pada peninjauan kembali telah memutus perkara terpidana: "
    "ir. zainal abidin, m.si., tempat lahir lombok; "
    "membaca putusan pengadilan tindak pidana korupsi pada pengadilan tinggi "
    "mataram nomor 20/pid.sus-tpk/2024/pt mtr tanggal 3 oktober 2024 yang "
    "amarnya: menjatuhkan pidana kepada terdakwa ir. zainal abidin, m.si. "
    "dengan pidana penjara selama 7 (tujuh) tahun dan pidana denda sebesar "
    "rp300.000.000,00; "
    "menimbang bahwa pemohon peninjauan kembali mengajukan perbandingan "
    "dengan putusan pengadilan tindak pidana korupsi pada pengadilan negeri "
    "mataram nomor 7/pid.sus-tpk/2024/pn mtr tanggal 7 agustus 2024 atas "
    "nama terpidana trisman, s.t., m.p. tersebut, yang telah menjatuhkan "
    "pidana kepada terdakwa trisman, s.t., m.p. dengan pidana penjara selama "
    "2 (dua) tahun atas dakwaan yang terbukti secara sah; "
    "m e n g a d i l i : - menolak permohonan peninjauan kembali dari "
    "pemohon peninjauan kembali/terpidana ir. zainal abidin, m.si. tersebut; "
    "- menetapkan bahwa putusan yang dimohonkan peninjauan kembali tersebut "
    "tetap berlaku;"
)

# 2892 K/Pid.Sus/2024 — PT acquitted on "dakwaan KESATU primair" (ordinal
# between "dakwaan" and "primair") and convicted on subsidiair with 8 years;
# _is_full_acquittal treated it as a FULL acquittal, and the new
# acquittal->kerugian-NULL pipeline rule then wiped a correct loss figure.
SNIPPET_ORDINAL_PARTIAL_ACQUITTAL = (
    "membaca putusan pengadilan tinggi makassar nomor 56/pid.tpk/2023/pt mks "
    "yang amar lengkapnya sebagai berikut: 1. menyatakan terdakwa radytio "
    "wiratama putra sikado tidak terbukti secara sah dan meyakinkan bersalah "
    "melakukan tindak pidana sebagaimana dalam dakwaan kesatu primair; 2. "
    "membebaskan terdakwa dari dakwaan kesatu primair tersebut; 3. "
    "menyatakan terdakwa terbukti secara sah dan meyakinkan bersalah "
    "melakukan tindak pidana korupsi sebagaimana dalam dakwaan kesatu "
    "subsidair; 4. menjatuhkan pidana kepada terdakwa dengan pidana penjara "
    "selama 8 (delapan) tahun; "
    "menimbang bahwa terjadi kerugian keuangan negara sebesar "
    "rp5.001.112.450,00 (lima miliar satu juta seratus dua belas ribu empat "
    "ratus lima puluh rupiah) sesuai dengan laporan hasil audit khusus dari "
    "satuan pengawasan intern perum bulog; "
    "m e n g a d i l i: - menolak permohonan kasasi dari pemohon kasasi "
    "i/penuntut umum dan pemohon kasasi ii/terdakwa tersebut; - membebankan "
    "biaya perkara kepada terdakwa;"
)


def test_vonis_footer_disclaimer_splitting_amar():
    assert extract_vonis_bulan(SNIPPET_FOOTER_SPLIT_AMAR) == 120


def test_vonis_skips_companion_case_quote():
    assert extract_vonis_bulan(SNIPPET_COMPANION_QUOTE) == 84


def test_vonis_ordinal_partial_acquittal_not_full():
    assert extract_vonis_bulan(SNIPPET_ORDINAL_PARTIAL_ACQUITTAL) == 96


def test_pipeline_keeps_kerugian_when_acquittal_is_partial():
    result = parse_verdict({}, SNIPPET_ORDINAL_PARTIAL_ACQUITTAL)
    assert result["vonis_bulan"] == 96
    assert result["kerugian_negara"] == 5001112450.0
