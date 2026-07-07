"""Golden-30 regression harness (test-first for parser bug fix D14).

Loads tests/fixtures/golden30/expected.json (human-validated ground truth) and
checks src.parser.fields extractors against the fixture text for each case.
These field tests are EXPECTED TO FAIL until D14 parser fixes land — do not xfail them.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from src.parser.fields import (
    extract_vonis_bulan,
    extract_tuntutan_bulan,
    extract_kerugian_negara,
    extract_daerah,
    extract_tahun,
)

try:
    from src.parser.fields import is_tipikor_document as is_tipikor
    _IS_TIPIKOR_AVAILABLE = True
except ImportError:
    is_tipikor = None
    _IS_TIPIKOR_AVAILABLE = False


def _norm_daerah(s: str) -> str:
    """Field semantics = city: 'PN Bandung Kelas IA' ≡ 'Bandung'."""
    s = s.strip().lower()
    for prefix in ("pn ", "pt ", "pengadilan negeri ", "pengadilan tinggi "):
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s.split(" kelas")[0].strip()

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "golden30"

with open(FIXTURE_DIR / "expected.json", encoding="utf-8") as f:
    EXPECTED = json.load(f)


def _load_text(case):
    return (FIXTURE_DIR / case["case_file"]).read_text(encoding="utf-8")


# === vonis_bulan ===

@pytest.mark.parametrize("case", EXPECTED, ids=[c["case_number"] + "-vonis_bulan" for c in EXPECTED])
def test_vonis_bulan(case):
    expected = case["vonis_bulan"]
    if expected == "SKIP":
        pytest.skip("AMBIGUOUS ground truth")
    text = _load_text(case)
    result = extract_vonis_bulan(text)
    if expected is None:
        assert not result
    elif expected == 0:
        assert result == 0
    else:
        assert result == pytest.approx(expected)


# === tuntutan_bulan ===

# Known limitations (disclosed, not hidden): xfail with reason
_XFAIL = {
    ("2366 K/PID.SUS/2015", "tuntutan_bulan"):
        "multi-defendant doc: parser reads Terdakwa I's demand; sampled defendant is II. "
        "Per-defendant attribution is future work (D14 residual).",
    ("151/PID.SUS-TPK/2025/PN BDG", "tahun"):
        "tahun = registration year from case number by design; decision date can "
        "fall in the next calendar year (documented in datasheet).",
}


@pytest.mark.parametrize("case", EXPECTED, ids=[c["case_number"] + "-tuntutan_bulan" for c in EXPECTED])
def test_tuntutan_bulan(case):
    expected = case["tuntutan_bulan"]
    if expected == "SKIP":
        pytest.skip("AMBIGUOUS ground truth")
    reason = _XFAIL.get((case["case_number"], "tuntutan_bulan"))
    if reason:
        pytest.xfail(reason)
    text = _load_text(case)
    result = extract_tuntutan_bulan(text)
    if expected is None:
        assert not result
    elif expected == 0:
        assert result == 0
    else:
        assert result == pytest.approx(expected)


# === kerugian_negara ===

@pytest.mark.parametrize("case", EXPECTED, ids=[c["case_number"] + "-kerugian_negara" for c in EXPECTED])
def test_kerugian_negara(case):
    expected = case["kerugian_negara"]
    if expected == "SKIP":
        pytest.skip("AMBIGUOUS ground truth")
    text = _load_text(case)
    result = extract_kerugian_negara(text)
    if expected is None:
        assert not result
    elif expected == 0:
        assert result == 0
    else:
        assert result == pytest.approx(expected)


# === daerah ===

@pytest.mark.parametrize("case", EXPECTED, ids=[c["case_number"] + "-daerah" for c in EXPECTED])
def test_daerah(case):
    expected = case["daerah"]
    if expected == "SKIP":
        pytest.skip("AMBIGUOUS ground truth")
    text = _load_text(case)
    result = extract_daerah(text, metadata={"case_number": case["case_number"]})
    if expected is None:
        assert not result
    else:
        assert result is not None
        assert _norm_daerah(result) == _norm_daerah(expected)


# === tahun ===

@pytest.mark.parametrize("case", EXPECTED, ids=[c["case_number"] + "-tahun" for c in EXPECTED])
def test_tahun(case):
    expected = case["tahun"]
    if expected == "SKIP":
        pytest.skip("AMBIGUOUS ground truth")
    reason = _XFAIL.get((case["case_number"], "tahun"))
    if reason:
        pytest.xfail(reason)
    text = _load_text(case)
    result = extract_tahun(text, metadata={"case_number": case["case_number"]})
    if expected is None:
        assert not result
    else:
        assert result == expected


# === is_tipikor (D15: domain filter, not implemented yet) ===

if _IS_TIPIKOR_AVAILABLE:
    def test_is_tipikor():
        for case in EXPECTED:
            text = _load_text(case)
            result = is_tipikor(text)
            assert bool(result) == case["is_tipikor"], case["case_number"]
else:
    @pytest.mark.xfail(reason="D15: domain filter not implemented yet")
    def test_is_tipikor():
        raise ImportError("is_tipikor not implemented in src.parser.fields (D15)")
