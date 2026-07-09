from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime

from sydel_doc_engine.utils.months import FRENCH_MONTHS

# Formats numeriques acceptes en ENTREE d'une date de naissance saisie librement
# (l'UI civile passe une chaine texte : « 10/03/1975 », un ISO ou un objet date).
_BIRTHDATE_INPUT_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")

# Mois FR sans accent -> forme accentuee (Rafael 2026-07-09 : une date SAISIE en toutes
# lettres « 1er aout 1980 » / « 1er decembre 1978 » ne doit pas garder le mois non accentue).
_MONTHS_ACCENT = {
    unicodedata.normalize("NFKD", m).encode("ascii", "ignore").decode("ascii"): m
    for m in FRENCH_MONTHS
    if m
}


def accentuate_months(text: str) -> str:
    """Re-accentue tout nom de mois FR ecrit sans accent dans une chaine (« aout » -> « août »,
    « decembre » -> « décembre », « fevrier » -> « février »). Insensible a la casse, borne mot."""

    def _repl(match: re.Match[str]) -> str:
        accented = _MONTHS_ACCENT[match.group(0).lower()]
        return accented.upper() if match.group(0).isupper() else accented

    pattern = "|".join(re.escape(k) for k in _MONTHS_ACCENT if k not in FRENCH_MONTHS)
    if not pattern:
        return text
    return re.sub(rf"\b({pattern})\b", _repl, text, flags=re.IGNORECASE)


def format_date_fr(value: date) -> str:
    """Formate une date au format numerique francais « JJ/MM/AAAA »."""
    return value.strftime("%d/%m/%Y")


def coerce_date(value: date | str | None) -> date | None:
    """Parse un objet date OU une chaine numerique en objet date.

    Accepte un objet ``date``/``datetime``, une chaine ISO « AAAA-MM-JJ », « JJ/MM/AAAA »
    ou « JJ-MM-AAAA ». Retourne ``None`` si la valeur est vide OU non parsable (ex. une date
    deja lettree « 1er decembre 1978 ») -> l'appelant conserve alors la chaine telle quelle.
    """
    if value is None:
        return None
    if isinstance(value, date):  # datetime est une sous-classe de date
        return value
    raw = str(value).strip()
    if not raw:
        return None
    for fmt in _BIRTHDATE_INPUT_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def format_birthdate_fr(value: date | str | None) -> str:
    """Date de naissance des STATUTS au format « JJ mois AAAA » (Albane 2026-07-09, B1).

    Jour sur 2 chiffres, mois accentue en toutes lettres (ex. « 10 mars 1975 »,
    « 01 decembre 1978 ») — meme presentation que l'avenant de bail et
    ``cession_cabinets_common``. Une valeur numerique (objet date OU chaine
    ISO / JJ-MM-AAAA / JJ/MM/AAAA) est reformatee ; une date DEJA lettree ou non parsable
    est renvoyee telle quelle (fidelite : « 1er decembre 1978 » reste inchange).
    """
    parsed = coerce_date(value)
    if parsed is not None:
        return f"{parsed.day:02d} {FRENCH_MONTHS[parsed.month]} {parsed.year}"
    # Date DEJA lettree (non parsable) : conservee, mais le mois est RE-ACCENTUE
    # (« 1er aout 1980 » -> « 1er août 1980 ») — retour accents Rafael 2026-07-09.
    return "" if value is None else accentuate_months(str(value).strip())


def format_date_longue_fr(value: date) -> str:
    """Formate une date en francais long « JJ mois AAAA » (mois accentue, « 1er » pour le 1er).

    Convention partagee des types generalistes recents d'Albane (SASU/micro holding) :
    jour SANS zero initial, « 1er » pour le premier du mois, mois accentue (cf. FRENCH_MONTHS).
    Ex. date(2026, 5, 22) -> « 22 mai 2026 » ; date(2026, 5, 1) -> « 1er mai 2026 »."""
    jour = "1er" if value.day == 1 else str(value.day)
    return f"{jour} {FRENCH_MONTHS[value.month]} {value.year}"
