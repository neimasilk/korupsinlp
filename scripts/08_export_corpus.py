"""Script 08: Export clean corpus for release.

Exports structured data from SQLite to CSV and JSON formats suitable for
Zenodo/HuggingFace release. Excludes internal paths and raw HTML/PDF data.

Usage: python -m scripts.08_export_corpus
"""

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sqlite3

from src.config import DB_PATH, REPORTS_DIR

# Fields to export (order matters for CSV)
EXPORT_FIELDS = [
    "corpus_id",       # clean sequential ID
    "case_number",     # MA case number (e.g., "384 K/PID.SUS/2026")
    "date_decided",    # decision date string
    "tahun",           # year (integer)
    "daerah",          # region/court jurisdiction
    "nama_terdakwa",   # defendant name (public record)
    "pemohon_kasasi",  # appeal filer: penuntut_umum | terdakwa
    "pasal",           # legal articles charged
    "vonis_bulan",     # sentence in months (0 = acquittal, NULL = not extracted)
    "tuntutan_bulan",  # prosecution demand in months
    "kerugian_negara", # state financial loss in Rupiah
    "amar",            # verdict summary category
    "nama_hakim",      # panel of judges
]

DATA_DICTIONARY = {
    "corpus_id": {
        "type": "integer",
        "description": "Sequential identifier (1-based) for corpus ordering",
    },
    "case_number": {
        "type": "string",
        "description": "MA case number, e.g., '384 K/PID.SUS/2026'. Format: [number] K/PID.SUS/[year] for kasasi, [number] PK/PID.SUS/[year] for peninjauan kembali.",
        "missing": "69 records (12.4%) have no case number — empty scrapes from server errors",
    },
    "date_decided": {
        "type": "string",
        "description": "Decision date in Indonesian format, e.g., '28 Januari 2026'",
    },
    "tahun": {
        "type": "integer",
        "description": "Year of MA decision (extracted from case number or date). Range: 2011-2026.",
        "missing": "103 records (18.5%) — mostly empty scrapes",
    },
    "daerah": {
        "type": "string",
        "description": "Court jurisdiction/region, mapped from Pengadilan Negeri name to province-level. 40+ unique values. Example: 'Jakarta Pusat', 'Surabaya', 'Bandung'.",
        "missing": "162 records (29.1%) — cases without PDF or unrecognized court names",
    },
    "nama_terdakwa": {
        "type": "string",
        "description": "Defendant's full name as stated in the verdict (public record). May include titles (S.E., S.T., Drs., H., etc.) and patronymic (bin/binti).",
        "missing": "215 records (38.6%)",
    },
    "pemohon_kasasi": {
        "type": "string",
        "description": "Who filed the cassation appeal. Values: 'penuntut_umum' (prosecutor/JPU), 'terdakwa' (defendant). Critical confounding variable for sentencing analysis.",
        "missing": "235 records (42.2%)",
    },
    "pasal": {
        "type": "string",
        "description": "Legal articles charged, semicolon-separated. Most cite Pasal 2 or 3 of UU 31/1999 jo UU 20/2001 (Anti-Corruption Law).",
        "missing": "207 records (37.2%)",
    },
    "vonis_bulan": {
        "type": "float",
        "description": "Prison sentence imposed by MA, in months. 0 = acquittal (membebaskan/melepaskan). NULL = not extracted. Range: 0-216 months (0-18 years).",
        "missing": "213 records (38.2%) — includes empty scrapes and extraction failures",
    },
    "tuntutan_bulan": {
        "type": "float",
        "description": "Prosecution demand (tuntutan pidana), in months. The sentence the prosecutor requested.",
        "missing": "237 records (42.5%)",
    },
    "kerugian_negara": {
        "type": "float",
        "description": "State financial loss (kerugian keuangan negara) in Indonesian Rupiah. Range: ~Rp15M to Rp300T. NULL for gratification/bribery cases where no state loss figure is stated. 3 suspected extraction artifacts (<Rp1M) have been set to NULL.",
        "missing": "284 records (51.0%) — many legitimately have no kerugian (suap cases)",
    },
    "amar": {
        "type": "string",
        "description": "Verdict summary category from MA metadata. Values include: 'Kabul' (granted), 'Tolak' (rejected), 'Tolak Perbaikan' (rejected with modification), 'Tidak dapat diterima' (inadmissible).",
    },
    "nama_hakim": {
        "type": "string",
        "description": "Panel of MA judges, semicolon-separated. Typically 3 judges per panel.",
    },
}


def export_corpus():
    """Export clean corpus to CSV and JSON."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT id, case_number, date_decided, tahun, daerah, nama_terdakwa,
               pemohon_kasasi, pasal, vonis_bulan, tuntutan_bulan, kerugian_negara,
               amar, nama_hakim
        FROM verdicts
        ORDER BY tahun ASC, id ASC
    """).fetchall()

    print(f"Total records: {len(rows)}")

    # Assign corpus IDs
    records = []
    for i, row in enumerate(rows, 1):
        record = {"corpus_id": i}
        for field in EXPORT_FIELDS[1:]:  # skip corpus_id
            val = row[field]
            # Clean up: replace empty strings with None
            if isinstance(val, str) and val.strip() == "":
                val = None
            record[field] = val
        records.append(record)

    # Count non-null per field
    print("\nField completeness:")
    for field in EXPORT_FIELDS:
        n_present = sum(1 for r in records if r[field] is not None)
        pct = n_present / len(records) * 100
        print(f"  {field:20s}: {n_present:4d}/{len(records)} ({pct:.1f}%)")

    # Export directory
    export_dir = REPORTS_DIR / "corpus_release"
    export_dir.mkdir(exist_ok=True)

    # CSV export
    csv_path = export_dir / "korpuskorupsi_v1.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPORT_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    print(f"\nCSV exported: {csv_path} ({len(records)} rows)")

    # JSON export (array of objects)
    json_path = export_dir / "korpuskorupsi_v1.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"JSON exported: {json_path}")

    # Data dictionary
    dict_path = export_dir / "data_dictionary.json"
    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(DATA_DICTIONARY, f, ensure_ascii=False, indent=2)
    print(f"Data dictionary: {dict_path}")

    # Summary statistics for quick reference
    vonis_records = [r for r in records if r["vonis_bulan"] is not None and r["vonis_bulan"] > 0]
    acquittals = [r for r in records if r["vonis_bulan"] is not None and r["vonis_bulan"] == 0]

    summary = {
        "corpus_name": "KorpusKorupsi v1.0",
        "description": "Structured corpus of Indonesian Supreme Court corruption verdicts",
        "source": "putusan3.mahkamahagung.go.id",
        "total_records": len(records),
        "with_valid_sentence": len(vonis_records),
        "acquittals": len(acquittals),
        "temporal_range": f"{min(r['tahun'] for r in records if r['tahun'])}-{max(r['tahun'] for r in records if r['tahun'])}",
        "regions": len(set(r["daerah"] for r in records if r["daerah"])),
        "mean_sentence_years": round(sum(r["vonis_bulan"] for r in vonis_records) / len(vonis_records) / 12, 2),
        "median_sentence_years": round(sorted(r["vonis_bulan"] for r in vonis_records)[len(vonis_records) // 2] / 12, 1),
        "license": "CC-BY-4.0 (data), MIT (code)",
        "citation": "Amien, M. (2026). CorpusKorupsi: A Computational Corpus of Indonesian Supreme Court Corruption Verdicts and Sentencing Patterns.",
    }
    summary_path = export_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Summary: {summary_path}")

    print(f"\n--- Release Package ---")
    print(f"  Records: {summary['total_records']}")
    print(f"  With sentence: {summary['with_valid_sentence']}")
    print(f"  Acquittals: {summary['acquittals']}")
    print(f"  Temporal range: {summary['temporal_range']}")
    print(f"  Regions: {summary['regions']}")
    print(f"  Mean sentence: {summary['mean_sentence_years']} years")

    conn.close()
    return records


if __name__ == "__main__":
    export_corpus()
