"""One-off script: build tests/fixtures/golden30/*.txt + expected.json from golden_set CSVs."""
import json
import re
from pathlib import Path

import pandas as pd
from pdfminer.high_level import extract_text

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "golden30"
FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

validated = pd.read_csv(ROOT / "data/golden_set/golden_expansion_30_validated.csv", dtype=str)


def sanitize(case_number: str) -> str:
    return re.sub(r"[/\s]+", "_", case_number.strip())


def parse_int_field(val):
    if val is None or (isinstance(val, float)):
        return None
    val = val.strip()
    if val == "ABSENT" or val.startswith("ABSENT"):
        return None
    if val == "ACQUITTED":
        return 0
    if "AMBIGUOUS" in val.upper():
        return "SKIP"
    m = re.match(r"^-?\d+(\.\d+)?", val)
    if m:
        num = m.group(0)
        return int(num) if "." not in num else float(num)
    raise ValueError(f"Unparsed field value: {val!r}")


def parse_float_field(val):
    if val is None:
        return None
    val = val.strip()
    if val.startswith("ABSENT"):
        return None
    if "AMBIGUOUS" in val.upper():
        return "SKIP"
    m = re.match(r"^-?\d+(\.\d+)?", val)
    if m:
        return float(m.group(0))
    raise ValueError(f"Unparsed kerugian value: {val!r}")


def parse_daerah(val):
    if val is None:
        return None
    val = val.strip()
    if val == "ABSENT" or val.startswith("ABSENT"):
        return None
    if "AMBIGUOUS" in val.upper():
        return "SKIP"
    return val


def parse_tahun(val):
    if val is None:
        return None
    val = val.strip()
    if val == "ABSENT" or val.startswith("ABSENT"):
        return None
    if "AMBIGUOUS" in val.upper():
        return "SKIP"
    return int(float(val))


expected = []
failed_extractions = []

for _, row in validated.iterrows():
    case_number = row["case_number"]
    pdf_path = row["pdf_path"]
    sanitized = sanitize(case_number)
    txt_path = FIXTURE_DIR / f"{sanitized}.txt"

    try:
        text = extract_text(pdf_path)
    except Exception as e:
        failed_extractions.append((case_number, pdf_path, str(e)))
        text = ""

    txt_path.write_text(text, encoding="utf-8")

    is_tipikor = case_number.strip().upper() != "961 K/PID.SUS/2026"

    entry = {
        "case_file": f"{sanitized}.txt",
        "case_number": case_number,
        "vonis_bulan": parse_int_field(row["human_vonis_bulan"]),
        "tuntutan_bulan": parse_int_field(row["human_tuntutan_bulan"]),
        "kerugian_negara": parse_float_field(row["human_kerugian_negara"]),
        "daerah": parse_daerah(row["human_daerah"]),
        "tahun": parse_tahun(row["human_tahun"]),
        "is_tipikor": is_tipikor,
        "notes": row["notes"] if isinstance(row["notes"], str) else None,
    }
    expected.append(entry)

with open(FIXTURE_DIR / "expected.json", "w", encoding="utf-8") as f:
    json.dump(expected, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(expected)} txt fixtures + expected.json to {FIXTURE_DIR}")
if failed_extractions:
    print("FAILED EXTRACTIONS:")
    for cn, p, e in failed_extractions:
        print(f"  {cn} ({p}): {e}")
else:
    print("No extraction failures.")
