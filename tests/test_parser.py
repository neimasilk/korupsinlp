"""Tests for the parser module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from src.parser.fields import (
    extract_vonis_bulan,
    extract_tuntutan_bulan,
    extract_kerugian_negara,
    extract_pasal,
    extract_nama_terdakwa,
    extract_tahun,
    extract_daerah,
    extract_pemohon_kasasi,
    extract_faktor_pertimbangan,
    _strip_watermark,
)
from src.parser.normalizer import normalize_duration_to_months, normalize_rupiah, court_to_province
from src.parser.pipeline import parse_verdict


# === extract_vonis_bulan ===

class TestExtractVonis:
    def test_tahun_dan_bulan(self):
        text = "pidana penjara selama 4 (empat) tahun dan 6 (enam) bulan"
        assert extract_vonis_bulan(text) == 54  # 4*12 + 6

    def test_tahun_only(self):
        text = "penjara selama 2 (dua) tahun"
        assert extract_vonis_bulan(text) == 24

    def test_bulan_only(self):
        text = "penjara selama 18 (delapan belas) bulan"
        assert extract_vonis_bulan(text) == 18

    def test_seumur_hidup(self):
        text = "penjara seumur hidup"
        assert extract_vonis_bulan(text) == -1

    def test_pidana_mati(self):
        text = "pidana mati"
        assert extract_vonis_bulan(text) == -2

    def test_no_match(self):
        assert extract_vonis_bulan("tidak ada vonis") is None

    def test_empty(self):
        assert extract_vonis_bulan("") is None
        assert extract_vonis_bulan(None) is None


# === extract_kerugian_negara ===

class TestExtractKerugian:
    def test_standard_format(self):
        text = "kerugian keuangan negara sebesar Rp 1.500.000.000,00"
        result = extract_kerugian_negara(text)
        assert result == 1_500_000_000

    def test_with_dot_prefix(self):
        text = "merugikan keuangan negara sebesar Rp. 500.000.000,-"
        result = extract_kerugian_negara(text)
        assert result == 500_000_000

    def test_no_match(self):
        assert extract_kerugian_negara("tidak ada kerugian") is None


# === extract_tuntutan_bulan ===

class TestExtractTuntutan:
    def test_menuntut(self):
        text = "menuntut agar terdakwa dijatuhi pidana penjara selama 5 (lima) tahun"
        assert extract_tuntutan_bulan(text) == 60

    def test_dituntut(self):
        text = "dituntut dengan pidana penjara selama 2 tahun 6 bulan"
        assert extract_tuntutan_bulan(text) == 30


# === extract_pasal ===

class TestExtractPasal:
    def test_single_pasal(self):
        text = "melanggar Pasal 2 ayat (1)"
        result = extract_pasal(text)
        assert "2 ayat (1)" in result

    def test_multiple_pasal(self):
        text = "Pasal 3 jo. Pasal 18 ayat (1)"
        result = extract_pasal(text)
        assert result is not None


# === extract_tahun ===

class TestExtractTahun:
    def test_from_case_number(self):
        metadata = {"case_number": "123/Pid.Sus-TPK/2023/PN Jkt.Pst"}
        assert extract_tahun("", metadata) == 2023

    def test_from_tahun_register(self):
        metadata = {"case_number": "", "tahun_register": "2021"}
        assert extract_tahun("", metadata) == 2021

    def test_from_text(self):
        assert extract_tahun("putusan tahun 2022") == 2022


# === extract_daerah ===

class TestExtractDaerah:
    def test_from_metadata(self):
        metadata = {"lembaga_peradilan": "Pengadilan Negeri Surabaya"}
        assert extract_daerah("", metadata) == "Surabaya"

    def test_from_text(self):
        text = "Pengadilan Negeri Makassar yang memeriksa"
        assert extract_daerah(text) == "Makassar"


# === Normalizers ===

class TestNormalizers:
    def test_duration_tahun_bulan(self):
        assert normalize_duration_to_months("4 tahun 6 bulan") == 54

    def test_duration_bulan(self):
        assert normalize_duration_to_months("18 bulan") == 18

    def test_rupiah_standard(self):
        assert normalize_rupiah("Rp 1.500.000.000,00") == 1_500_000_000

    def test_rupiah_dash(self):
        assert normalize_rupiah("Rp. 500.000.000,-") == 500_000_000

    def test_court_to_province(self):
        assert court_to_province("Surabaya") == "Jawa Timur"
        assert court_to_province("Jakarta Pusat") == "DKI Jakarta"
        assert court_to_province("Unknown City") is None


# === Pipeline ===

class TestPipeline:
    def test_parse_verdict_with_full_data(self):
        metadata = {
            "case_number": "123/Pid.Sus-TPK/2022/PN Sby",
            "lembaga_peradilan": "Pengadilan Negeri Surabaya",
            "amar": "",
            "hakim_ketua": "Dr. Ahmad",
            "hakim_anggota": "Budi, Cahyo",
        }
        text = (
            "pidana penjara selama 4 (empat) tahun dan 6 (enam) bulan "
            "kerugian keuangan negara sebesar Rp 1.500.000.000,00 "
            "melanggar Pasal 2 ayat (1)"
        )
        result = parse_verdict(metadata, text)

        assert result["vonis_bulan"] == 54
        assert result["kerugian_negara"] == 1_500_000_000
        assert result["daerah"] == "Surabaya"
        assert result["tahun"] == 2022
        assert result["nama_hakim"] is not None


# === extract_pemohon_kasasi ===

class TestExtractPemohonKasasi:
    def test_kasasi_terdakwa(self):
        text = "kasasi yang dimohonkan oleh Terdakwa, telah memutus"
        assert extract_pemohon_kasasi(text) == "terdakwa"

    def test_kasasi_jpu(self):
        text = "kasasi yang dimohonkan oleh Penuntut Umum pada Kejaksaan"
        assert extract_pemohon_kasasi(text) == "penuntut_umum"

    def test_pk_terpidana(self):
        text = "peninjauan kembali yang dimohonkan oleh Terpidana"
        assert extract_pemohon_kasasi(text) == "terdakwa"

    def test_no_match(self):
        assert extract_pemohon_kasasi("tidak ada kasasi") is None

    def test_merged_text_dimohonkanoleh(self):
        """Merged PDF: 'dimohonkanoleh Penuntut Umum' (no space)."""
        text = "kasasi yang dimohonkanoleh Penuntut Umum pada Kejaksaan"
        assert extract_pemohon_kasasi(text) == "penuntut_umum"

    def test_merged_text_olehterdakwa(self):
        """Merged PDF: 'dimohonkan olehTerdakwa' (no space)."""
        text = "peninjauan kembali yang dimohonkan olehTerpidana, telah memutus"
        assert extract_pemohon_kasasi(text) == "terdakwa"


# === Watermark stripping ===

class TestWatermarkStrip:
    def test_strip_ma_watermark(self):
        text = "some text Direktori Putusan Mahkamah Agung Republik Indonesia\nputusan.mahkamahagung.go.id\n\nMahkamah Agung Republik Indonesia\n more text"
        cleaned = _strip_watermark(text)
        assert "Direktori Putusan" not in cleaned
        assert "some text" in cleaned
        assert "more text" in cleaned

    def test_no_watermark(self):
        text = "normal text without watermark"
        assert _strip_watermark(text) == text


# === Tuntutan with defendant name ===

class TestTuntutanWithName:
    def test_penjara_terhadap_terdakwa(self):
        """Tuntutan where defendant name appears between 'penjara' and 'selama'."""
        text = (
            "Tuntutan Pidana Penuntut Umum: "
            "2. Menjatuhkan pidana penjara terhadap Terdakwa "
            "AHMAD SYARIF, S.H. selama 5 (lima) tahun"
        )
        assert extract_tuntutan_bulan(text) == 60


# === MENGADILI vonis strategy ===

class TestVonisMengadili:
    def test_mengadili_spaced(self):
        """Vonis from M E N G A D I L I section."""
        text = (
            "Tuntutan Pidana: penjara selama 8 tahun "
            "M E N G A D I L I: "
            "Menjatuhkan pidana penjara selama 4 (empat) tahun"
        )
        assert extract_vonis_bulan(text) == 48  # from MENGADILI, not tuntutan

    def test_last_match_fallback(self):
        """Falls back to last penjara match when no MENGADILI and no prefix match."""
        # Both matches must be outside the first 500 chars (Strategy 2 prefix)
        padding = "x " * 300  # 600 chars
        text = (
            padding +
            "penjara selama 6 tahun " +
            padding +
            "penjara selama 3 tahun"
        )
        assert extract_vonis_bulan(text) == 36

    def test_kasasi_ditolak_uses_previous_mengadili(self):
        """When MA rejects kasasi, use the previous MENGADILI section sentence."""
        text = (
            "M E N G A D I L I: "
            "Menjatuhkan pidana kepada Terdakwa dengan pidana penjara selama 5 (lima) tahun "
            "dan pidana denda sebesar Rp50.000.000 "
            "M E N G A D I L I: "
            "Menolak permohonan kasasi dari Pemohon Kasasi "
            "Membebankan kepada Terdakwa membayar biaya perkara Rp2.500"
        )
        # Should get 60 (5yr) from first MENGADILI, not from last
        assert extract_vonis_bulan(text) == 60

    def test_kasasi_ditolak_quoted_pn_sentence(self):
        """Single MENGADILI (Menolak) — finds quoted PN sentence before it."""
        pn_quote = (
            "Putusan Pengadilan Negeri Surabaya yang amar putusannya sebagai berikut: "
            "1. Menyatakan terdakwa terbukti bersalah; "
            "2. Menjatuhkan pidana kepada terdakwa dengan pidana penjara selama 5 (lima) tahun "
            "dan denda sebesar Rp50.000.000; "
        )
        ma_mengadili = (
            "M E N G A D I L I: "
            "Menolak permohonan kasasi dari Pemohon Kasasi "
        )
        text = pn_quote + "x " * 100 + ma_mengadili
        assert extract_vonis_bulan(text) == 60

    def test_mengadili_sendiri_overrides(self):
        """MA MENGADILI SENDIRI takes precedence over lower court sentence."""
        text = (
            "M E N G A D I L I: "
            "Menjatuhkan pidana kepada Terdakwa dengan pidana penjara selama 5 (lima) tahun "
            "M E N G A D I L I: "
            "Menjatuhkan pidana kepada Terdakwa dengan pidana penjara selama 3 (tiga) tahun "
        )
        # Should get 36 (3yr) from last MENGADILI (MA's own sentence)
        assert extract_vonis_bulan(text) == 36

    def test_acquittal_bebas(self):
        """When MA acquits (membebaskan), return 0 instead of lower court sentence."""
        # PN sentence quoted earlier, then MA acquits
        pn_text = "penjara selama 5 (lima) tahun "
        ma_text = (
            "M E N G A D I L I: "
            "Mengabulkan permohonan kasasi dari Pemohon Kasasi "
            "MENGADILI SENDIRI: "
            "1. Menyatakan Terdakwa tidak terbukti; "
            "2. Membebaskan Terdakwa oleh karena itu dari segala dakwaan; "
        )
        text = pn_text + "x " * 200 + ma_text
        assert extract_vonis_bulan(text) == 0

    def test_acquittal_lepas(self):
        """When MA releases (melepaskan/ontslag), return 0."""
        pn_text = "penjara selama 10 (sepuluh) tahun "
        ma_text = (
            "M E N G A D I L I: "
            "Mengabulkan permohonan kasasi "
            "MENGADILI SENDIRI: "
            "1. Menyatakan Terdakwa terbukti melakukan perbuatan akan tetapi "
            "bukan merupakan tindak pidana; "
            "2. Melepaskan Terdakwa tersebut dari segala tuntutan hukum; "
        )
        text = pn_text + "x " * 200 + ma_text
        assert extract_vonis_bulan(text) == 0

    def test_partial_acquittal_with_conviction(self):
        """Freed from primary charge but convicted on subsidiary — return the sentence."""
        text = (
            "M E N G A D I L I: "
            "Mengabulkan permohonan kasasi "
            "MENGADILI SENDIRI: "
            "1. Membebaskan Terdakwa dari dakwaan Primair; "
            "2. Menyatakan Terdakwa terbukti melakukan dakwaan Subsidair; "
            "3. Menjatuhkan pidana kepada Terdakwa dengan pidana penjara selama 7 (tujuh) tahun "
        )
        # Should get 84 (7yr) — convicted on subsidiary charge
        assert extract_vonis_bulan(text) == 84

    def test_memperbaiki_sentence(self):
        """Memperbaiki: MA modifies the sentence. Use the modified sentence."""
        text = (
            "penjara selama 3 (tiga) tahun "  # original PT sentence in earlier text
            "x " * 200 +
            "M E N G A D I L I: "
            "Menolak permohonan kasasi dari Pemohon Kasasi "
            "Memperbaiki Putusan Pengadilan Tinggi mengenai pidana yang dijatuhkan "
            "kepada Terdakwa menjadi pidana penjara selama 2 (dua) tahun "
        )
        # Should get 24 (2yr) from memperbaiki, NOT 36 (3yr) from original
        assert extract_vonis_bulan(text) == 24

    def test_dual_kasasi_mengabulkan_jpu(self):
        """Both JPU and terdakwa filed kasasi. JPU accepted → MENGADILI SENDIRI."""
        text = (
            "penjara selama 4 (empat) tahun "  # lower court sentence
            "x " * 200 +
            "M E N G A D I L I: "
            "Menolak permohonan kasasi dari Pemohon Kasasi I/Terdakwa "
            "Mengabulkan permohonan kasasi dari Pemohon Kasasi II/PENUNTUT UMUM "
            "Membatalkan Putusan Pengadilan Tinggi "
            "MENGADILI SENDIRI: "
            "1. Menyatakan Terdakwa terbukti bersalah; "
            "2. Menjatuhkan pidana kepada Terdakwa dengan pidana penjara selama 6 (enam) tahun "
        )
        # Should get 72 (6yr) from MENGADILI SENDIRI, NOT 48 (4yr) from lower court
        assert extract_vonis_bulan(text) == 72


# === nama_terdakwa from PDF header ===

class TestNamaTerdakwaPDFHeader:
    def test_structured_header_with_bin(self):
        """Nama : X bin Y; Tempat Lahir : Z"""
        text = 'Nama  : ISWANTO, S.Pd.I., bin (almarhum) ISMANI; Tempat Lahir  : Rembang;'
        result = extract_nama_terdakwa(text)
        assert result == "ISWANTO, S.Pd.I., bin (almarhum) ISMANI"

    def test_structured_header_with_binti(self):
        text = 'Nama : H. RASKAMA ABDUL HALIM bin NARA; Tempat Lahir : Majalengka;'
        result = extract_nama_terdakwa(text)
        assert result == "H. RASKAMA ABDUL HALIM bin NARA"

    def test_merged_pdf_text(self):
        """No spaces — merged PDF extraction."""
        text = 'Nama:.SANDRAMARIATUN,S.H.,bintiH.HENDROMARTONO;TempatLahir:Surakarta;'
        result = extract_nama_terdakwa(text)
        assert result == "SANDRAMARIATUN,S.H.,bintiH.HENDROMARTONO"

    def test_header_with_almarhum(self):
        text = 'Nama : MUSTAFA AL HAMID bin (almarhum) ZAYD MUCHSIN AL HAMID;  Tempat Lahir : Probolinggo;'
        result = extract_nama_terdakwa(text)
        assert result == "MUSTAFA AL HAMID bin (almarhum) ZAYD MUCHSIN AL HAMID"

    def test_header_simple_name(self):
        text = 'Nama  : AZHAR bin ABDULLAH MAHMUD; Tempat Lahir  : Idi;'
        result = extract_nama_terdakwa(text)
        assert result == "AZHAR bin ABDULLAH MAHMUD"

    def test_vs_terdakwa_fallback(self):
        """Falls back to VS pattern when no header."""
        text = 'Penuntut Umum VS JOHN DOE (Terdakwa)'
        assert extract_nama_terdakwa(text) == "JOHN DOE"


# === extract_faktor_pertimbangan ===

class TestFaktorPertimbangan:
    def test_explicit_factors(self):
        text = (
            "Hal-hal yang memberatkan: "
            "- Terdakwa tidak mendukung program pemerintah; "
            "- Perbuatan Terdakwa merugikan keuangan negara; "
            "Hal-hal yang meringankan: "
            "- Terdakwa bersikap sopan di persidangan; "
            "- Terdakwa belum pernah dihukum; "
            "Menimbang bahwa berdasarkan pertimbangan tersebut"
        )
        result = extract_faktor_pertimbangan(text)
        assert result["has_factors"] is True
        assert len(result["memberatkan"]) == 2
        assert len(result["meringankan"]) == 2
        assert "merugikan" in result["memberatkan"][1].lower()

    def test_keadaan_format(self):
        text = (
            "Keadaan yang memberatkan: "
            "1. Perbuatan Terdakwa meresahkan masyarakat; "
            "Keadaan yang meringankan: "
            "1. Terdakwa mengakui perbuatannya; "
            "Mengingat Pasal 2"
        )
        result = extract_faktor_pertimbangan(text)
        assert result["has_factors"] is True
        assert len(result["memberatkan"]) >= 1
        assert len(result["meringankan"]) >= 1

    def test_no_factors(self):
        text = "telah cukup mempertimbangkan keadaan yang memberatkan dan meringankan"
        result = extract_faktor_pertimbangan(text)
        assert result["has_factors"] is False

    def test_empty_text(self):
        result = extract_faktor_pertimbangan("")
        assert result["has_factors"] is False
        assert result["memberatkan"] == []
        assert result["meringankan"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
