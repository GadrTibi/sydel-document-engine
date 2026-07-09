from __future__ import annotations

from datetime import date, datetime

from sydel_doc_engine.utils.months import FRENCH_MONTHS

# Formats numeriques acceptes en ENTREE d'une date de naissance saisie librement
# (l'UI civile passe une chaine texte : « 10/03/1975 », un ISO ou un objet date).
_BIRTHDATE_INPUT_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")


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
    return "" if value is None else str(value).strip()


def format_date_longue_fr(value: date) -> str:
    """Formate une date en francais long « JJ mois AAAA » (mois accentue, « 1er » pour le 1er).

    Convention partagee des types generalistes recents d'Albane (SASU/micro holding) :
    jour SANS zero initial, « 1er » pour le premier du mois, mois accentue (cf. FRENCH_MONTHS).
    Ex. date(2026, 5, 22) -> « 22 mai 2026 » ; date(2026, 5, 1) -> « 1er mai 2026 »."""
    jour = "1er" if value.day == 1 else str(value.day)
    return f"{jour} {FRENCH_MONTHS[value.month]} {value.year}"
