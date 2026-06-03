from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Final

from sydel_doc_engine.domain.enums import Gender

DEFAULT_MANDATAIRE_CIVILITE: Final = "Monsieur"
DEFAULT_MANDATAIRE_PRENOM: Final = "Jordan"
DEFAULT_MANDATAIRE_NOM: Final = "ELBAZ"
DEFAULT_MANDATAIRE_FONCTION: Final = "gérant"
DEFAULT_MANDATAIRE_CABINET: Final = "SYDEL"
DEFAULT_PRESTATAIRE_SIGNATURE_ELECTRONIQUE: Final = "Yousign"
DEFAULT_SEUIL_ACHAT_MATERIEL: Final = "5000"
DEFAULT_SEUIL_EMPRUNT: Final = "10000"
DEFAULT_TITRE_AFFICHAGE: Final = "Docteur"
NATIONALITY_PRESETS: Final = (
    "Française",
    "Belge",
    "Portugaise",
    "Suisse",
    "Luxembourgeoise",
    "Autre",
)
MATRIMONIAL_STATUS_PRESETS: Final = (
    "Celibataire",
    "Marie(e)",
    "Pacs(e)",
    "Divorce(e)",
    "Veuf / veuve",
)

_SMALL_NUMBERS: Final = {
    0: "zero",
    1: "un",
    2: "deux",
    3: "trois",
    4: "quatre",
    5: "cinq",
    6: "six",
    7: "sept",
    8: "huit",
    9: "neuf",
    10: "dix",
    11: "onze",
    12: "douze",
    13: "treize",
    14: "quatorze",
    15: "quinze",
    16: "seize",
}
_TENS: Final = {
    20: "vingt",
    30: "trente",
    40: "quarante",
    50: "cinquante",
    60: "soixante",
}
_MONTHS: Final = (
    "",
    "janvier",
    "fevrier",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "aout",
    "septembre",
    "octobre",
    "novembre",
    "decembre",
)


def derive_gender_from_civilite(civilite: str) -> Gender:
    normalized = _normalize_label(civilite)
    if normalized in {"madame", "mme", "mademoiselle", "mlle"}:
        return Gender.FEMININ
    return Gender.MASCULIN


def format_numeric_value(value: object) -> str:
    number = _decimal_from_value(value)
    if number is None:
        return str(value).strip() if value is not None else ""
    if number == number.to_integral_value():
        return str(int(number))
    return format(number.normalize(), "f")


def format_grouped_numeric_value(value: object) -> str:
    number = _decimal_from_value(value)
    if number is None:
        return str(value).strip() if value is not None else ""
    if number == number.to_integral_value():
        return f"{int(number):,}".replace(",", " ")
    return format(number.normalize(), "f").replace(".", ",")


def number_words_from_value(value: object) -> str:
    number = _decimal_from_value(value)
    if number is None or number != number.to_integral_value():
        return ""
    return integer_to_french_words(int(number))


def calculate_nominal_value(capital_social: object, nb_parts_total: object) -> str:
    capital = _decimal_from_value(capital_social)
    nb_parts = _decimal_from_value(nb_parts_total)
    if capital is None or nb_parts is None or nb_parts == 0:
        return ""
    return format_numeric_value(capital / nb_parts)


def format_french_date(value: date | None) -> str:
    if not isinstance(value, date):
        return ""
    return value.strftime("%d/%m/%Y")


def parse_french_date(value: object) -> date | None:
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped:
        return None
    match = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", stripped)
    if match is None:
        return None
    day, month, year = (int(part) for part in match.groups())
    try:
        return date(year, month, day)
    except ValueError:
        return None


def matrimonial_status_value(label: str) -> str:
    normalized = _normalize_label(label)
    if normalized.startswith("marie"):
        return "marie"
    if normalized.startswith("pacs"):
        return "pacse"
    if normalized.startswith("divorce"):
        return "divorce"
    if normalized.startswith("veuf"):
        return "veuf"
    return "celibataire"


def regime_matrimonial_from_status(label: str, regime_communautaire: bool) -> str:
    if regime_communautaire:
        return "regime de communaute"
    status = matrimonial_status_value(label)
    if status == "marie":
        return "separation de biens"
    return status


def integer_to_french_words(value: int) -> str:
    if value < 0:
        return "moins " + integer_to_french_words(abs(value))
    if value < 17:
        return _SMALL_NUMBERS[value]
    if value < 20:
        return "dix-" + _SMALL_NUMBERS[value - 10]
    if value < 100:
        return _two_digit_words(value)
    if value < 1000:
        return _hundreds_words(value)
    if value < 1_000_000:
        thousands, remainder = divmod(value, 1000)
        prefix = "mille" if thousands == 1 else f"{integer_to_french_words(thousands)} mille"
        return prefix if remainder == 0 else f"{prefix} {integer_to_french_words(remainder)}"
    millions, remainder = divmod(value, 1_000_000)
    prefix = (
        "un million"
        if millions == 1
        else f"{integer_to_french_words(millions)} millions"
    )
    return prefix if remainder == 0 else f"{prefix} {integer_to_french_words(remainder)}"


def date_to_french_words(value: date | None) -> str:
    if not isinstance(value, date):
        return ""
    return (
        f"{integer_to_french_words(value.day)} "
        f"{_MONTHS[value.month]} "
        f"{integer_to_french_words(value.year)}"
    )


def today() -> date:
    return date.today()


def _two_digit_words(value: int) -> str:
    if value < 70:
        ten, unit = divmod(value, 10)
        ten_value = ten * 10
        if unit == 0:
            return _TENS[ten_value]
        if unit == 1:
            return f"{_TENS[ten_value]} et un"
        return f"{_TENS[ten_value]}-{_SMALL_NUMBERS[unit]}"
    if value < 80:
        remainder = value - 60
        if remainder == 11:
            return "soixante et onze"
        return f"soixante-{integer_to_french_words(remainder)}"
    remainder = value - 80
    if remainder == 0:
        return "quatre-vingts"
    return f"quatre-vingt-{integer_to_french_words(remainder)}"


def _hundreds_words(value: int) -> str:
    hundred, remainder = divmod(value, 100)
    if hundred == 1:
        prefix = "cent"
    else:
        prefix = f"{_SMALL_NUMBERS[hundred]} cent"
    if remainder == 0:
        return prefix + ("s" if hundred > 1 else "")
    return f"{prefix} {integer_to_french_words(remainder)}"


def _decimal_from_value(value: object) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return None
        cleaned = cleaned.replace("\u00a0", " ").replace(" ", "")
        cleaned = cleaned.replace(",", ".")
        cleaned = re.sub(r"[^0-9.-]", "", cleaned)
        if not cleaned:
            return None
        try:
            return Decimal(cleaned)
        except InvalidOperation:
            return None
    return None


def _normalize_label(value: str) -> str:
    return value.strip().lower().replace(".", "")
