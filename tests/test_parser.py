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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
