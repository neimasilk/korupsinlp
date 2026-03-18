"""Compute feasibility metrics from parsed verdicts."""

from src.config import P0_FIELDS, P1_FIELDS, P2_FIELDS, GO_THRESHOLD, CONDITIONAL_THRESHOLD


def compute_field_success_rates(verdicts: list[dict]) -> dict[str, float]:
    """Compute per-field success rate (fraction of verdicts where field is non-null)."""
    if not verdicts:
        return {}

    all_fields = P0_FIELDS + P1_FIELDS + P2_FIELDS
    rates = {}

    for field in all_fields:
        count = sum(1 for v in verdicts if v.get(field) is not None)
        rates[field] = count / len(verdicts)

    return rates


def compute_p0_coverage(verdicts: list[dict]) -> float:
    """Fraction of verdicts that have ALL P0 fields populated."""
    if not verdicts:
        return 0.0

    full_count = sum(
        1 for v in verdicts
        if all(v.get(f) is not None for f in P0_FIELDS)
    )
    return full_count / len(verdicts)


def compute_format_stats(verdicts: list[dict]) -> dict:
    """Analyze format distribution: HTML vs PDF, scanned vs text."""
    total = len(verdicts)
    if total == 0:
        return {}

    has_html_text = sum(1 for v in verdicts if v.get("full_text"))
    has_pdf = sum(1 for v in verdicts if v.get("pdf_path"))
    is_scanned = sum(1 for v in verdicts if v.get("is_scanned"))

    return {
        "total": total,
        "has_html_text": has_html_text,
        "has_pdf": has_pdf,
        "is_scanned": is_scanned,
        "html_text_rate": has_html_text / total,
        "pdf_rate": has_pdf / total,
        "scanned_rate": is_scanned / total if has_pdf > 0 else 0,
    }


def go_nogo_decision(p0_rates: dict[str, float]) -> tuple[str, str]:
    """Make GO/NO-GO decision based on P0 field success rates.

    Returns (decision, explanation).
    """
    if not p0_rates:
        return "NO-GO", "No data to evaluate."

    # Average P0 success rate
    p0_avg = sum(p0_rates.get(f, 0) for f in P0_FIELDS) / len(P0_FIELDS)
    min_field = min(P0_FIELDS, key=lambda f: p0_rates.get(f, 0))
    min_rate = p0_rates.get(min_field, 0)

    if p0_avg >= GO_THRESHOLD and min_rate >= CONDITIONAL_THRESHOLD:
        decision = "GO"
        explanation = (
            f"Average P0 success rate: {p0_avg:.1%}. "
            f"Weakest field: {min_field} ({min_rate:.1%}). "
            f"All P0 fields above conditional threshold ({CONDITIONAL_THRESHOLD:.0%}). "
            "Proceed to Fase 1: Corpus Building."
        )
    elif p0_avg >= CONDITIONAL_THRESHOLD:
        decision = "CONDITIONAL GO"
        explanation = (
            f"Average P0 success rate: {p0_avg:.1%}. "
            f"Weakest field: {min_field} ({min_rate:.1%}). "
            "Consider narrowing scope — e.g., focus on vonis+tuntutan discount analysis "
            "where both fields have higher success rates."
        )
    else:
        decision = "NO-GO"
        explanation = (
            f"Average P0 success rate: {p0_avg:.1%} — below {CONDITIONAL_THRESHOLD:.0%} threshold. "
            f"Weakest field: {min_field} ({min_rate:.1%}). "
            "Recommend: formal data request to Mahkamah Agung, or pivot to alternative data source."
        )

    return decision, explanation


def generate_report_data(verdicts: list[dict]) -> dict:
    """Generate all data needed for the feasibility report."""
    field_rates = compute_field_success_rates(verdicts)
    p0_rates = {f: field_rates.get(f, 0) for f in P0_FIELDS}
    decision, explanation = go_nogo_decision(p0_rates)

    return {
        "total_verdicts": len(verdicts),
        "field_success_rates": field_rates,
        "p0_coverage": compute_p0_coverage(verdicts),
        "format_stats": compute_format_stats(verdicts),
        "decision": decision,
        "explanation": explanation,
    }
