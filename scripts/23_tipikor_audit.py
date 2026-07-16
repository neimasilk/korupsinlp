"""Script 23: D15 domain-contamination audit — flag non-tipikor documents in the corpus.

A pure narcotics case (961 K/Pid.Sus/2026) leaked into the corpus because the global
scrape trusted the directory's category label. This audit re-derives the domain flag
from DOCUMENT TEXT ONLY (never the directory classification — that label is the thing
that failed): quick pass over DB text fields (amar, catatan_amar, pertimbangan_text),
pdfminer full-text fallback for quick-pass failures that have a PDF.

Fills verdicts.is_tipikor (1/0, NULL = unverifiable: no text and no PDF) and writes
data/tipikor_audit.csv for the failures.

Usage: python -m scripts.23_tipikor_audit
"""
import csv
import re
import sqlite3
from pathlib import Path

from pdfminer.high_level import extract_text

from src.db import migrate_db
from src.parser.fields import is_tipikor_document

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "korupsinlp.db"
OUT = ROOT / "data" / "tipikor_audit.csv"


def main():
    migrate_db(DB)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """SELECT id, case_number, amar, catatan_amar, pertimbangan_text, pdf_path,
                  tuntutan_bulan, vonis_bulan, kerugian_negara
           FROM verdicts"""
    ).fetchall()

    quick_pass, casenum_rescued, pdf_rescued = [], [], []
    casetype_fail, pdf_fail, suspect, unverifiable = [], [], [], []
    for r in rows:
        cn = (r["case_number"] or "").upper()
        db_text = " ".join(filter(None, [r["amar"], r["catatan_amar"],
                                         r["pertimbangan_text"]]))
        if is_tipikor_document(db_text):
            quick_pass.append(r)
            continue
        # Case-number register codes are authoritative both ways:
        # Pid.Sus-TPK = the tipikor register; PDT/TUN = civil/administrative.
        if "TPK" in cn:
            casenum_rescued.append(r)
            continue
        if re.search(r"\bK?/?(PDT|TUN)/", cn) or " K/PDT/" in " " + cn \
                or "K/TUN/" in cn or "/PDT/" in cn:
            casetype_fail.append(r)
            continue
        pdf = r["pdf_path"]
        if pdf and Path(pdf).exists():
            try:
                full = extract_text(pdf)
            except Exception as e:
                print(f"  pdfminer failed on {r['case_number']}: {e}")
                full = ""
            if is_tipikor_document(full):
                pdf_rescued.append(r)
            else:
                pdf_fail.append(r)  # full text read, no corruption markers
        elif db_text.strip():
            suspect.append(r)  # text without markers, no PDF to confirm
        else:
            unverifiable.append(r)
    failed = casetype_fail + pdf_fail

    in_elas = [r for r in failed
               if r["tuntutan_bulan"] and r["vonis_bulan"]
               and (r["kerugian_negara"] or 0) >= 1_000_000]

    cur = con.cursor()
    for r in quick_pass + pdf_rescued + casenum_rescued:
        cur.execute("UPDATE verdicts SET is_tipikor = 1 WHERE id = ?", (r["id"],))
    for r in failed:
        cur.execute("UPDATE verdicts SET is_tipikor = 0 WHERE id = ?", (r["id"],))
    for r in suspect + unverifiable:
        cur.execute("UPDATE verdicts SET is_tipikor = NULL WHERE id = ?", (r["id"],))
    con.commit()

    dupes = con.execute(
        """SELECT case_number, COUNT(*) c FROM verdicts
           GROUP BY case_number HAVING c > 1 ORDER BY c DESC"""
    ).fetchall()

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "case_number", "pdf_path", "in_elasticity_population", "status"])
        for r, status in [(r, "NON_TIPIKOR_CASETYPE") for r in casetype_fail] + \
                         [(r, "NON_TIPIKOR_PDF_VERIFIED") for r in pdf_fail] + \
                         [(r, "SUSPECT_NO_PDF") for r in suspect] + \
                         [(r, "UNVERIFIABLE_NO_TEXT") for r in unverifiable]:
            w.writerow([r["id"], r["case_number"], r["pdf_path"],
                        int(r in in_elas), status])

    print(f"\nTotal {len(rows)}")
    print(f"  tipikor OK      : {len(quick_pass)} text + {len(pdf_rescued)} pdf-rescued "
          f"+ {len(casenum_rescued)} casenum(TPK)-rescued "
          f"= {len(quick_pass) + len(pdf_rescued) + len(casenum_rescued)}")
    print(f"  NON-TIPIKOR     : {len(casetype_fail)} by case type (PDT/TUN) "
          f"+ {len(pdf_fail)} by full-text check = {len(failed)}")
    print(f"  suspect (no PDF): {len(suspect)}   unverifiable (no text): {len(unverifiable)}")
    print(f"  duplicate case_numbers in corpus: {len(dupes)} "
          f"({sum(d[1] for d in dupes) - len(dupes)} extra rows)")
    print(f"Non-tipikor inside elasticity population (n=237 sample): {len(in_elas)}")
    print("\nNON-TIPIKOR (definite):")
    for r in failed:
        mark = " <-- IN ANALYSIS SAMPLE" if r in in_elas else ""
        print(f"  {r['case_number']}{mark}")
    print(f"\nDetail -> {OUT}")
    con.close()


if __name__ == "__main__":
    main()
