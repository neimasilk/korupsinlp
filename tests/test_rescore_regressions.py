"""Regression tests for bugs found by the CROSS-ROUND rescore (script 24),
not by a fresh holdout round.

After parser fix round 5, `python -m scripts.24_holdout_rescore` re-scored all
80 archived annotations (R1-R4) against the current DB and flagged one 1->0
flip: 858 K/Pid.Sus/2022 [tuntutan] db=84 human=120. Cause: inside the
"Tuntutan Pidana" section, strategy 1a (the demand amar that may OMIT the word
"penjara", added for 12367 K/PID.SUS/2025) is tried exhaustively BEFORE
strategy 1b and therefore wins regardless of position. Here the JPU demand
reads "Menjatuhkan pidana ATAS DIRI Terdakwa dengan pidana penjara selama 10
tahun" - which 1a cannot match (it requires "terhadap"/"kepada") - so 1a
matched the PN amar quoted 2000 chars later ("Menjatuhkan pidana kepada
Terdakwa ... 7 tahun") while 1b's correct match sat at offset 294.

Fix: within a section, the EARLIEST valid match across strategies wins.
"""
from src.parser.fields import extract_kerugian_negara, extract_tuntutan_bulan

# 858 K/Pid.Sus/2022 — faithful reduction of the pdfminer text. The demand
# (10 tahun) is followed in the same section by the PN amar (7 tahun) and the
# PT corrected amar (5 tahun); only the first is the prosecution demand.
SNIPPET_ATAS_DIRI = (
    "Tuntutan Pidana Penuntut Umum pada Kejaksaan Negeri Manggarai Barat "
    "tanggal 14 Juni 2021 sebagai berikut : 1. Menyatakan Terdakwa CAITANO "
    "SOARES terbukti bersalah melakukan tindak pidana “Korupsi secara "
    "bersama-sama” sebagaimana Dakwaan Primair; 2. Menjatuhkan pidana "
    "atas diri Terdakwa dengan pidana penjara selama 10 (sepuluh) tahun dan "
    "denda sebesar Rp1.000.000.000,00 (satu miliar rupiah) dengan ketentuan "
    "jika denda tersebut tidak dibayar maka diganti dengan pidana kurungan "
    "selama 6 (enam) bulan; 3. Menetapkan agar Terdakwa tetap ditahan jenis "
    "Rutan; 4. Menetapkan agar Terdakwa dibebani untuk membayar biaya "
    "perkara; Membaca putusan Pengadilan Tindak Pidana Korupsi pada "
    "Pengadilan Negeri Kupang Nomor 20/Pid.Sus-TPK/2021/PN Kpg yang amarnya "
    "sebagai berikut : 1. Menyatakan Terdakwa CAITANO SOARES terbukti "
    "bersalah melakukan tindak pidana “Korupsi secara bersama-sama dan "
    "berlanjut”; 2. Menjatuhkan pidana kepada Terdakwa dengan pidana "
    "penjara selama 7 (tujuh) tahun dan denda sebesar Rp1.000.000.000,00 "
    "(satu miliar rupiah); Membaca putusan Pengadilan Tinggi Kupang yang "
    "memperbaiki amar angka 2, sehingga berbunyi sebagai berikut : 2) "
    "Menjatuhkan pidana kepada Terdakwa dengan pidana penjara selama 5 "
    "(lima) tahun dan denda sebesar Rp400.000.000,00 (empat ratus juta "
    "rupiah)"
)


# 2997 PK/PID.SUS/2025 — flagged by script 24 after parser fix round 7. The
# round-7 "label after figure" tier let a figure bypass the payment blockers,
# which was right for 2505 PK/2025 ("selisih PEMBAYARAN sebesar RpX yang
# merupakan kerugian") but wrong here: Rp31,8 M is what REMAINS after
# Rp13,1 M was recovered, while the established loss is Rp46,6 M. Restitution
# and recovery never reduce the established loss (same convention that decided
# 1288 K/Pid.Sus/2020 in the R5 adjudication).
SNIPPET_REMAINDER_AFTER_RECOVERY = (
    "bahwa akibat dari perbuatan Terpidana I, Terpidana II dan Terpidana III "
    "bersama-sama dengan saksi Sarli dan saksi Suyanto sebagaimana diuraikan "
    "tersebut di atas telah menimbulkan kerugian keuangan Negara sebesar "
    "Rp46.617.192.219,00 (empat puluh enam miliar enam ratus tujuh belas juta "
    "seratus sembilan puluh dua ribu dua ratus sembilan belas rupiah) "
    "berdasarkan Laporan Hasil Audit; bahwa dari 250 (dua ratus lima puluh) "
    "debitur tersebut telah terdapat pemulihan kerugian keuangan Negara "
    "sebesar Rp13.101.947.514,00 (tiga belas miliar seratus satu juta sembilan "
    "ratus empat puluh tujuh ribu lima ratus empat belas rupiah) sehingga "
    "masih terdapat jumlah pokok pinjaman yang belum dibayar oleh penerima KUR "
    "kepada Bank BNI sebesar Rp31.898.052.486,00 (tiga puluh satu miliar "
    "delapan ratus sembilan puluh delapan juta lima puluh dua ribu empat ratus "
    "delapan puluh enam rupiah) yang merupakan kerugian keuangan Negara"
)


def test_kerugian_ignores_remainder_after_recovery():
    """Established loss, not the balance left after partial recovery."""
    assert extract_kerugian_negara(SNIPPET_REMAINDER_AFTER_RECOVERY) == 46617192219.0


def test_tuntutan_atas_diri_not_overridden_by_later_pn_amar():
    """The demand (10 tahun) precedes the quoted PN amar (7 tahun) — earliest
    valid match in the section must win, not the strategy tried first."""
    assert extract_tuntutan_bulan(SNIPPET_ATAS_DIRI) == 120
