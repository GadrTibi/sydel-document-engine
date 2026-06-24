from __future__ import annotations

import re
import unicodedata
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
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
# Regimes matrimoniaux explicites (retours client 2026-06-11, ticket SELARL
# dentiste 1.2) : seul le regime legal / communaute declenche la logique
# documentaire DOC-005/DOC-006 ; les trois autres regimes maries n'entrainent
# aucun document complementaire.
MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE: Final = "Marié(e) sous le régime légal / communauté"
MATRIMONIAL_STATUS_PRESETS: Final = (
    "Célibataire",
    MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE,
    "Marié(e) sous le régime de la séparation de biens",
    "Marié(e) sous le régime de la communauté universelle",
    "Marié(e) sous le régime de la participation aux acquêts",
    "Pacsé(e)",
    "Divorcé(e)",
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
# Règle globale (Rafael 2026-06-23) : les noms de mois en SORTIE sont toujours
# correctement accentués (février, août, décembre). Les MAPS de parsing (nom -> n°)
# restent sans accent : le parseur normalise (NFKD) l'entrée avant lookup.
_MONTHS: Final = (
    "",
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)


_MONTH_ACCENT_FIXES: Final = (
    (re.compile(r"\baout\b", re.IGNORECASE), "août"),
    (re.compile(r"\bf[ée]vrier\b", re.IGNORECASE), "février"),
    (re.compile(r"\bd[ée]cembre\b", re.IGNORECASE), "décembre"),
)


def accentuate_french_months(text: str) -> str:
    """Re-accentue les noms de mois mal saisis dans une chaine de SORTIE (LIVE-03).

    « 31 decembre 2026 » -> « 31 décembre 2026 ». Les champs de date d'exercice sont des
    text_input LIBRES : une saisie sans accent partirait verbatim dans le DOCX. On re-accentue
    DONC EN AMONT (a la construction du contexte cote front), pas dans le generateur (qui doit
    rester un echo fidele du modele de reference SELARL — il contient « 31 decembre » sans
    accent, typo source a faire trancher par Albane). Seuls les 3 mois a accent sont concernes
    (aout/fevrier/decembre) ; insensible a la casse, preserve la capitale initiale, idempotent.
    Convention globale Rafael 2026-06-23 (cf. _MONTHS pour les sorties derivees d'un objet date)."""
    if not text:
        return text
    out = text
    for pattern, accented in _MONTH_ACCENT_FIXES:
        out = pattern.sub(
            lambda m, a=accented: a.capitalize() if m.group(0)[:1].isupper() else a,
            out,
        )
    return out


_NUM_VOIE_RE: Final = re.compile(
    r"^\s*(\d+\s*(?:bis|ter|quater)?)\s+(.+)$",
    re.IGNORECASE,
)


def split_numero_voie(value: str) -> tuple[str, str]:
    """Decoupe « 10 rue Test » en (« 10 », « rue Test »).

    Le champ unique « Numero et voie » (retours client 2026-06-11, ticket 1.5)
    alimente les generateurs qui consomment numero et voie separement. Sans
    numero en tete (lieu-dit...), tout part dans la voie.
    """
    cleaned = (value or "").strip()
    match = _NUM_VOIE_RE.match(cleaned)
    if match is None:
        return "", cleaned
    return match.group(1).strip(), match.group(2).strip()


def derive_gender_from_civilite(civilite: str) -> Gender:
    normalized = _normalize_label(civilite)
    if normalized in {"madame", "mme", "mademoiselle", "mlle"}:
        return Gender.FEMININ
    return Gender.MASCULIN


def situation_display(value: str, genre: object) -> str:
    """Statut matrimonial ACCENTUE et accorde au genre (« marié »/« mariée »).

    Helper partage (O24-11 / MINEUR 2b) : convertit la valeur collapsee non
    accentuee (« marie », « pacse », « divorce ») posee par les slices en libelle
    accentue accorde. Une valeur inconnue est renvoyee telle quelle (l'appelant
    peut deja avoir un libelle propre). Source unique pour shell._situation_display
    et les slices (SPFPL...) afin de ne jamais laisser fuir un « marie » nu."""
    feminine = genre == Gender.FEMININ
    return {
        "marie": "mariée" if feminine else "marié",
        "pacse": "pacsée" if feminine else "pacsé",
        "divorce": "divorcée" if feminine else "divorcé",
        "veuf": "veuve" if feminine else "veuf",
        "celibataire": "célibataire",
    }.get(value, value)


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
    # N1 (Rafael/Vincent 2026-06-24) : entier -> mise en lettres. DECIMAL -> "" : la valeur
    # nominale PEUT etre decimale (la FIGURE « 1,25 » est bien rendue par calculate_nominal_value),
    # mais la mise en LETTRES monetaire (« un euro et vingt-cinq centimes ») n'est PAS ratifiee et
    # provoquait un DOUBLE « euro » la ou le template porte deja l'unite (Akainu BLOQUANT
    # 2026-06-24 : statuts civils/SEL/SELAS). On attend le wording exact (cf. QUESTIONS_RAFAEL :
    # forme decimale + convention unite par template) avant de l'emettre. NE PAS reintroduire ici.
    if number is None or number != number.to_integral_value():
        return ""
    return integer_to_french_words(int(number))


def calculate_nominal_value(capital_social: object, nb_parts_total: object) -> str:
    capital = _decimal_from_value(capital_social)
    nb_parts = _decimal_from_value(nb_parts_total)
    if capital is None or nb_parts is None or nb_parts == 0:
        return ""
    # N1 (retour Rafael 2026-06-24) : la contrainte « valeur nominale entiere » a ete RETIREE
    # (rien dans les sources de verite ne l'exige ; c'etait une garde dogfood 2026-06-22).
    # Une valeur nominale PEUT etre non entiere (ex. 1,25). On arrondit au centime pour ne
    # jamais imprimer une decimale infinie (1000/3) dans l'acte ; plus aucun blocage en amont.
    quotient = (capital / nb_parts).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    # Format francais : virgule decimale (« 1,25 »), sans grouper (un entier reste « 333 »,
    # byte-identique au gold ; seule la decimale neuve prend la virgule). _decimal_from_value
    # reparse la virgule, donc la mise en lettres reste correcte.
    return format_numeric_value(quotient).replace(".", ",")


def is_capital_divisible(capital_social: object, nb_parts_total: object) -> bool:
    """RETIRE le 2026-06-24 (retour Rafael N1) : la contrainte « valeur nominale entiere »
    n'etait dans AUCUNE source de verite (garde dogfood 2026-06-22). Une valeur nominale PEUT
    etre non entiere ; `calculate_nominal_value` arrondit desormais au centime, donc plus de
    decimale infinie a craindre. No-op (toujours True) ; les blocs appelants sont neutralises
    et seront supprimes a la passe de nettoyage. NE PAS reintroduire de blocage de divisibilite.
    """
    return True


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
        normalized = _normalize_label(label)
        if "universelle" in normalized:
            return "communaute universelle"
        if "participation" in normalized:
            return "participation aux acquets"
        return "separation de biens"
    return status


def regime_communautaire_from_status(label: str) -> bool:
    """Le regime legal / communaute est le seul a declencher DOC-005/DOC-006.

    Derive du libelle de situation matrimoniale (plus de case a cocher dediee,
    R10/R11 Rafael 2026-06-23 / LIVE-02).
    """
    normalized = _normalize_label(label)
    return normalized.startswith("marie") and (
        "legal" in normalized or "communaute" in normalized
    ) and "universelle" not in normalized


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
    # NFKD -> insensible aux accents (« communauté » -> « communaute ») : les libelles ACCENTUES
    # des presets (R8, Rafael 2026-06-24) matchent toujours (startswith « marie », « communaute »…).
    decomposed = unicodedata.normalize("NFKD", value)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.strip().lower().replace(".", "")
