"""Fill the Common Paper Mutual NDA templates with user supplied values.

The source documents live in the repository level ``templates`` directory
(see task PL-4). Two files are used:

* ``Mutual-NDA-coverpage.md`` – the cover page, which holds the business terms.
* ``Mutual-NDA.md`` – the standard legal terms, which reference the cover page
  values through ``<span class="coverpage_link">…</span>`` elements.
"""
import re
from pathlib import Path

from django.conf import settings

COVER_PAGE_TEMPLATE = "Mutual-NDA-coverpage.md"
STANDARD_TERMS_TEMPLATE = "Mutual-NDA.md"

DEFAULT_PURPOSE = (
    "Evaluating whether to enter into a business relationship with the other party."
)

REQUIRED_FIELDS = {
    "party1_company": "Party 1 company is required.",
    "party1_name": "Party 1 print name is required.",
    "party2_company": "Party 2 company is required.",
    "party2_name": "Party 2 print name is required.",
    "effective_date": "Effective date is required.",
    "governing_law": "Governing law is required.",
    "jurisdiction": "Jurisdiction is required.",
}

_MNDA_TERM_FINITE_BLOCK = (
    "- [x]     Expires [1 year(s)] from Effective Date.\n"
    "- [ ]     Continues until terminated in accordance with the terms of the MNDA."
)
_MNDA_TERM_CONTINUES_BLOCK = (
    "- [ ]     Expires [1 year(s)] from Effective Date.\n"
    "- [x]     Continues until terminated in accordance with the terms of the MNDA."
)

_CONFIDENTIALITY_FINITE_BLOCK = (
    "- [x]     [1 year(s)] from Effective Date, but in the case of trade secrets until "
    "Confidential Information is no longer considered a trade secret under applicable laws.\n"
    "- [ ]     In perpetuity."
)
_CONFIDENTIALITY_PERPETUAL_BLOCK = (
    "- [ ]     [1 year(s)] from Effective Date, but in the case of trade secrets until "
    "Confidential Information is no longer considered a trade secret under applicable laws.\n"
    "- [x]     In perpetuity."
)


class NdaValidationError(Exception):
    """Raised when the submitted form data is not valid."""

    def __init__(self, errors):
        self.errors = errors
        super().__init__("Invalid NDA data")


def _read_template(name):
    path = Path(settings.COMMON_PAPER_TEMPLATES_DIR) / name
    return path.read_text(encoding="utf-8")


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _as_positive_int(value, field, label, errors):
    if value in (None, ""):
        errors[field] = f"{label} is required."
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        errors[field] = f"{label} must be a whole number."
        return None
    if number < 1:
        errors[field] = f"{label} must be at least 1."
        return None
    return number


def _format_years(number):
    return f"{number} year" if number == 1 else f"{number} years"


def _format_date(value):
    year, month, day = (int(part) for part in value.split("-"))
    month_name = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ][month - 1]
    return f"{month_name} {day}, {year}"


def validate(data):
    """Validate raw request data and return a normalised dict."""
    errors = {}

    for field, message in REQUIRED_FIELDS.items():
        if not str(data.get(field, "")).strip():
            errors[field] = message

    mnda_continues = _as_bool(data.get("mnda_term_continues"))
    confidentiality_perpetual = _as_bool(data.get("confidentiality_perpetual"))

    mnda_years = (
        None
        if mnda_continues
        else _as_positive_int(data.get("mnda_term_years", 1), "mnda_term_years", "MNDA term", errors)
    )
    confidentiality_years = (
        None
        if confidentiality_perpetual
        else _as_positive_int(
            data.get("confidentiality_years", 1),
            "confidentiality_years",
            "Term of confidentiality",
            errors,
        )
    )

    effective_date = None
    raw_date = str(data.get("effective_date", "")).strip()
    if raw_date:
        try:
            effective_date = _format_date(raw_date)
        except (ValueError, IndexError):
            errors["effective_date"] = "Effective date must be in YYYY-MM-DD format."

    if errors:
        raise NdaValidationError(errors)

    purpose = str(data.get("purpose", "")).strip() or DEFAULT_PURPOSE
    modifications = str(data.get("modifications", "")).strip()

    return {
        "party1_company": str(data.get("party1_company", "")).strip(),
        "party1_name": str(data.get("party1_name", "")).strip(),
        "party1_title": str(data.get("party1_title", "")).strip(),
        "party1_notice": str(data.get("party1_notice", "")).strip(),
        "party2_company": str(data.get("party2_company", "")).strip(),
        "party2_name": str(data.get("party2_name", "")).strip(),
        "party2_title": str(data.get("party2_title", "")).strip(),
        "party2_notice": str(data.get("party2_notice", "")).strip(),
        "purpose": purpose,
        "effective_date": effective_date,
        "mnda_continues": mnda_continues,
        "mnda_term_years": mnda_years,
        "confidentiality_perpetual": confidentiality_perpetual,
        "confidentiality_years": confidentiality_years,
        "governing_law": str(data.get("governing_law", "")).strip(),
        "jurisdiction": str(data.get("jurisdiction", "")).strip(),
        "modifications": modifications,
    }


def _table_cell(value):
    return value.replace("|", r"\|").replace("\n", " ").strip()


def _build_cover_page(data):
    cover = _read_template(COVER_PAGE_TEMPLATE)

    cover = re.sub(r"<label>.*?</label>", "", cover)
    cover = cover.replace(
        "[Evaluating whether to enter into a business relationship with the other party.]",
        data["purpose"],
    )
    cover = re.sub(r"\[Today.s date\]", data["effective_date"], cover)

    if data["mnda_continues"]:
        cover = cover.replace(_MNDA_TERM_FINITE_BLOCK, _MNDA_TERM_CONTINUES_BLOCK)
    else:
        years = _format_years(data["mnda_term_years"])
        cover = cover.replace(
            _MNDA_TERM_FINITE_BLOCK,
            f"- [x]     Expires {years} from Effective Date.\n"
            "- [ ]     Continues until terminated in accordance with the terms of the MNDA.",
        )

    if data["confidentiality_perpetual"]:
        cover = cover.replace(
            _CONFIDENTIALITY_FINITE_BLOCK, _CONFIDENTIALITY_PERPETUAL_BLOCK
        )
    else:
        years = _format_years(data["confidentiality_years"])
        cover = cover.replace(
            _CONFIDENTIALITY_FINITE_BLOCK,
            f"- [x]     {years} from Effective Date, but in the case of trade secrets until "
            "Confidential Information is no longer considered a trade secret under applicable laws.\n"
            "- [ ]     In perpetuity.",
        )

    cover = cover.replace("Governing Law: [Fill in state]", f"Governing Law: {data['governing_law']}")
    cover = re.sub(
        r"Jurisdiction: \[Fill in[^\]]*\]",
        f"Jurisdiction: {data['jurisdiction']}",
        cover,
    )
    cover = cover.replace(
        "List any modifications to the MNDA",
        f"MNDA Modifications: {data['modifications']}" if data["modifications"] else "None.",
    )

    table = "\n".join(
        [
            "|| PARTY 1 | PARTY 2 |",
            "|:--- | :--- | :--- |",
            "| Signature |  |  |",
            f"| Print Name | {_table_cell(data['party1_name'])} | {_table_cell(data['party2_name'])} |",
            f"| Title | {_table_cell(data['party1_title'])} | {_table_cell(data['party2_title'])} |",
            f"| Company | {_table_cell(data['party1_company'])} | {_table_cell(data['party2_company'])} |",
            f"| Notice Address | {_table_cell(data['party1_notice'])} | {_table_cell(data['party2_notice'])} |",
            f"| Date | {data['effective_date']} | {data['effective_date']} |",
        ]
    )

    start = cover.index("|| PARTY 1 | PARTY 2 |")
    end = cover.index("Common Paper Mutual Non-Disclosure Agreement (Version 1.0)")
    cover = cover[:start] + table + "\n\n" + cover[end:]

    return cover.strip() + "\n"


def _build_standard_terms(data):
    terms = _read_template(STANDARD_TERMS_TEMPLATE)

    if data["mnda_continues"]:
        mnda_term = "term continuing until terminated"
    else:
        mnda_term = f"term of {_format_years(data['mnda_term_years'])}"

    if data["confidentiality_perpetual"]:
        confidentiality = "period continuing in perpetuity"
    else:
        confidentiality = (
            f"period of {_format_years(data['confidentiality_years'])} "
            "from the Effective Date"
        )

    # Avoid the "the <date>" artifact in section 5.
    terms = terms.replace(
        'commences on the <span class="coverpage_link">Effective Date</span>',
        f"commences on {data['effective_date']}",
    )
    # Section 9 reads better with plain language for the repeated references.
    terms = terms.replace(
        'of such <span class="coverpage_link">Governing Law</span>', "of such laws"
    )
    terms = terms.replace(
        'jurisdiction of such <span class="coverpage_link">Jurisdiction</span>',
        "jurisdiction of such courts",
    )

    replacements = {
        "Purpose": data["purpose"].rstrip("."),
        "Effective Date": data["effective_date"],
        "MNDA Term": mnda_term,
        "Term of Confidentiality": confidentiality,
        "Governing Law": data["governing_law"],
        "Jurisdiction": data["jurisdiction"],
    }
    for key, value in replacements.items():
        terms = terms.replace(f'<span class="coverpage_link">{key}</span>', value)

    return terms.strip() + "\n"


def build_nda(data):
    """Return the completed MNDA as a single markdown document."""
    cover = _build_cover_page(data)
    terms = _build_standard_terms(data)
    return f"{cover}\n\n---\n\n{terms}"


def _slug(value):
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return slug or "Party"


def suggested_filename(data):
    return f"Mutual-NDA-{_slug(data['party1_company'])}-{_slug(data['party2_company'])}.md"
