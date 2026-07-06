from __future__ import annotations

import re
import unicodedata
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import Final

from sydel_doc_engine.domain.enums import Gender

# Fonctions PURES nombre -> mots DEPLACEES vers utils.grammar le 2026-07-06
# (re-architecture « containment » de la mise en lettres monetaire). On les RE-IMPORTE
# ici pour que tous les imports/tests historiques (`from ...field_derivations import
# integer_to_french_words`, etc.) continuent de marcher a l'identique. grammar NE DEPEND
# PAS de field_derivations (pas d'import circulaire).
from sydel_doc_engine.utils.grammar import (
    _decimal_from_value,
    format_numeric_value,
    integer_to_french_words,
    monetary_words_from_value,
)
from sydel_doc_engine.utils.months import FRENCH_MONTHS

__all__ = [  # noqa: RUF022 - ordre logique (helpers monetaires re-exportes en tete)
    "_decimal_from_value",
    "format_numeric_value",
    "integer_to_french_words",
    "monetary_words_from_value",
]

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

# _SMALL_NUMBERS / _TENS et le batisseur d'entiers en lettres ont ete DEPLACES vers
# utils.grammar le 2026-07-06 (containment monetaire) ; `integer_to_french_words` est
# re-importe en tete de module.

# Règle globale (Rafael 2026-06-23) : les noms de mois en SORTIE sont toujours
# correctement accentués (février, août, décembre). Les MAPS de parsing (nom -> n°)
# restent sans accent : le parseur normalise (NFKD) l'entrée avant lookup.
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
    Convention globale Rafael 2026-06-23 (cf. FRENCH_MONTHS pour les sorties d'une date)."""
    if not text:
        return text
    out = text
    for pattern, accented in _MONTH_ACCENT_FIXES:
        out = pattern.sub(
            lambda m, a=accented: a.capitalize() if m.group(0)[:1].isupper() else a,
            out,
        )
    return out


# ST3 (Albane 2026-06-26) : « pour la date de naissance, si le chiffre est de 1 a 9,
# au lieu de "1 janvier" mettre "01" ». La date de naissance est saisie en TEXTE LIBRE
# (« 1 janvier 1980 » / « 1er janvier 1980 ») et part verbatim dans la comparution. On
# zero-pade le JOUR en tete (« 01 janvier 1980 ») sans toucher le reste de la chaine.
# Le « er » de « 1er » est retire (un jour zero-pade « 01er » serait fautif). Idempotent
# (« 01 » reste « 01 »), insensible aux espaces de tete.
_BIRTHDATE_DAY_RE: Final = re.compile(r"^(\s*)(\d{1,2})(\s*(?:er|ER))?(\s+\S)")


def pad_birthdate_day(text: str) -> str:
    """Zero-pade le jour (1->9) d'une date de naissance textuelle (ST3).

    « 1 janvier 1980 » -> « 01 janvier 1980 » ; « 1er mars 1990 » -> « 01 mars 1990 ».
    Une chaine sans jour numerique en tete, ou deja sur 2 chiffres, est renvoyee telle
    quelle. Ne touche QUE le jour de tete (le millesime « 1980 » n'est pas affecte)."""
    if not text:
        return text

    def _pad(match: re.Match[str]) -> str:
        lead, day, _ordinal, tail = match.groups()
        return f"{lead}{int(day):02d}{tail}"

    return _BIRTHDATE_DAY_RE.sub(_pad, text, count=1)


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


# format_numeric_value a ete DEPLACE vers utils.grammar (containment 2026-07-06) et
# re-importe en tete de module.


def format_grouped_numeric_value(value: object) -> str:
    number = _decimal_from_value(value)
    if number is None:
        return str(value).strip() if value is not None else ""
    if number == number.to_integral_value():
        return f"{int(number):,}".replace(",", " ")
    return format(number.normalize(), "f").replace(".", ",")


def number_words_from_value(value: object) -> str:
    """Mise en lettres d'une valeur numerique pour les slots « _lettres ».

    - ENTIER -> mots seuls SANS unite (« dix », « cent »). Byte-identique au gold ;
      l'unite « euro(s) » est accolee separement par les templates (via
      `grammar.euro_word(figure)` ou un « euros » litteral). NE PAS toucher.
    - DECIMAL -> la FIGURE en format FR (« 0,01 », « 1 500,50 »). PAS de phrase
      monetaire ici (revert « containment » 2026-07-06). C'est le SEUL comportement
      SUR pour TOUTE recomposition « lettres + euro » separee : un decimal donne
      « 0,01 euros » (figure + unite), jamais « un centime d'euro euro ».

    La phrase monetaire décimale « un centime d'euro » (Albane 7.5) est produite
    UNIQUEMENT par `grammar.montant_lettres_avec_unite` (qui la CALCULE depuis la
    figure au point de composition), jamais par ce helper generique.
    """
    number = _decimal_from_value(value)
    if number is None:
        return ""
    if number == number.to_integral_value():
        return integer_to_french_words(int(number))
    return format_numeric_value(number).replace(".", ",")


def prix_lettres_from_value(value: object) -> str:
    """Mise en lettres d'un PRIX (hors scope Albane 7.5, contrairement a la valeur nominale).

    Le wording MONETAIRE d'un prix decimal n'est PAS ratifie -> prix ENTIER = mots nus
    (« un », « mille »), prix DECIMAL = FIGURE en lettres (« 2,5 »). Depuis le revert
    « containment » 2026-07-06, `number_words_from_value` rend AUSSI la figure sur un
    decimal, donc ce helper est FONCTIONNELLEMENT equivalent ; on le GARDE tel quel
    (verrou EXPLICITE, harmless) pour documenter que le prix ne doit JAMAIS basculer en
    phrase monetaire (double « euro » la ou l'acte accorde l'unite a part via
    `euro_word` / `_accord_euro`). Akainu M1/M2 2026-07-06 (regression prix SPFPL + SCM).
    """
    number = _decimal_from_value(value)
    if number is None:
        return ""
    if number == number.to_integral_value():
        return integer_to_french_words(int(number))
    return format_numeric_value(number).replace(".", ",")


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


# Mois (sans accent : l'entree est normalisee NFKD avant lookup) -> numero.
_MOIS_NUM: Final = {
    "janvier": 1, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11,
    "decembre": 12,
}

_ASSOCIE_BIRTHDATE_RE: Final = re.compile(
    r"\s*(\d{1,2})\s*(?:er)?\s+([A-Za-zàâäéèêëîïôöûüç]+)\s+(\d{4})\s*",
    re.IGNORECASE,
)


def parse_associe_birthdate(value: object) -> date | None:
    """Derive la date de naissance ISO a partir de l'UNIQUE saisie associe.

    L'associe saisit sa date en TEXTE (« 1 janvier 1980 », parite source pour la
    comparution). La DNC du dirigeant (DOC-001) exige une date reelle : on la derive
    de ce MEME champ (#8, onglet 24 : plus de double saisie via un picker dedie).
    Accepte « 1 janvier 1980 », « 1er janvier 1980 » et « JJ/MM/AAAA ». Helper PARTAGE
    (selas_multi, sas, sasu_holding) — un seul parseur, jamais duplique."""
    parsed = parse_french_date(value)
    if parsed is not None:
        return parsed
    if not isinstance(value, str):
        return None
    match = _ASSOCIE_BIRTHDATE_RE.fullmatch(value.strip())
    if match is None:
        return None
    day, month_name, year = match.groups()
    normalized = "".join(
        c
        for c in unicodedata.normalize("NFKD", month_name.lower())
        if not unicodedata.combining(c)
    )
    month = _MOIS_NUM.get(normalized)
    if month is None:
        return None
    try:
        return date(int(year), month, int(day))
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


def situation_maritale_complete(
    label: str,
    genre: object,
    *,
    conjoint_civilite: str | None = None,
    conjoint_prenom: str | None = None,
    conjoint_nom: str | None = None,
) -> str:
    """Situation matrimoniale complete pour la comparution (ST4, Albane 2026-06-26).

    « j'ai mis un associe marie sous un regime specifique et dans les statuts il
    n'apparait que "marie" sans plus de precision, ni le nom de l'epoux ; ajouter le
    regime et le nom du conjoint ». La valeur collapsee (« marie ») perdait le regime
    porte par le preset ET le conjoint saisi. On reconstruit, pour un associe MARIE :
    « marie(e) sous le regime de <regime>, epoux/epouse de <Civilite Prenom Nom> ».
    Le regime est ACCENTUE et accorde (pas le libelle brut du preset, qui partait
    double et non accentue — regression O24-11). Hors « marie », on retombe sur le mot
    d'etat civil accorde (situation_display) : pas de regime ni de conjoint a ajouter."""
    feminine = genre == Gender.FEMININ
    base = situation_display(matrimonial_status_value(label), genre)
    if matrimonial_status_value(label) != "marie":
        return base
    regime = _married_regime_display(label)
    phrase = f"{base} sous le régime de {regime}" if regime else base
    conjoint = " ".join(
        part.strip()
        for part in (conjoint_civilite, conjoint_prenom, conjoint_nom)
        if part and str(part).strip()
    ).strip()
    if conjoint:
        lien = "épouse de" if feminine else "époux de"
        phrase = f"{phrase}, {lien} {conjoint}"
    return phrase


def married_regime_display(label: str) -> str:
    """Alias public de `_married_regime_display` (libelle accentue « la communauté légale »… du
    regime matrimonial d'un associe MARIE). Reutilise par les slices dont le MODELE rend le regime
    directement dans la comparution (ex. SAS/SPFPL medecins)."""
    return _married_regime_display(label)


def _married_regime_display(label: str) -> str:
    """Libelle ACCENTUE du regime matrimonial d'un associe MARIE, derive du preset.

    `regime_matrimonial_from_status(.., False)` ne distingue PAS la communaute legale
    (il retombe sur « separation de biens » par defaut) -> on detecte d'abord la
    communaute legale via `regime_communautaire_from_status`, puis on mappe les trois
    autres regimes maries vers leur libelle accentue."""
    if regime_communautaire_from_status(label):
        return "la communauté légale"
    normalized = _normalize_label(label)
    if "universelle" in normalized:
        return "la communauté universelle"
    if "participation" in normalized:
        return "la participation aux acquêts"
    return "la séparation de biens"


def regime_communautaire_from_status(label: str) -> bool:
    """Le regime legal / communaute est le seul a declencher DOC-005/DOC-006.

    Derive du libelle de situation matrimoniale (plus de case a cocher dediee,
    R10/R11 Rafael 2026-06-23 / LIVE-02).
    """
    normalized = _normalize_label(label)
    return normalized.startswith("marie") and (
        "legal" in normalized or "communaute" in normalized
    ) and "universelle" not in normalized


# _invariable_before_mille et integer_to_french_words ont ete DEPLACES vers
# utils.grammar (containment 2026-07-06) ; integer_to_french_words est re-importe en
# tete de module (utilise ci-dessous par date_to_french_words).


def date_to_french_words(value: date | None) -> str:
    if not isinstance(value, date):
        return ""
    return (
        f"{integer_to_french_words(value.day)} "
        f"{FRENCH_MONTHS[value.month]} "
        f"{integer_to_french_words(value.year)}"
    )


def today() -> date:
    return date.today()


# _two_digit_words, _hundreds_words et _decimal_from_value ont ete DEPLACES vers
# utils.grammar (containment 2026-07-06). _decimal_from_value est re-importe en tete de
# module (utilise par format_grouped_numeric_value, number_words_from_value,
# prix_lettres_from_value, calculate_nominal_value).


def _normalize_label(value: str) -> str:
    # NFKD -> insensible aux accents (« communauté » -> « communaute ») : les libelles ACCENTUES
    # des presets (R8, Rafael 2026-06-24) matchent toujours (startswith « marie », « communaute »…).
    decomposed = unicodedata.normalize("NFKD", value)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.strip().lower().replace(".", "")
