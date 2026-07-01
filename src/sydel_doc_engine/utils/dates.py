from __future__ import annotations

from datetime import date

from sydel_doc_engine.utils.months import FRENCH_MONTHS


def format_date_fr(value: date) -> str:
    """Formate une date au format numerique francais « JJ/MM/AAAA »."""
    return value.strftime("%d/%m/%Y")


def format_date_longue_fr(value: date) -> str:
    """Formate une date en francais long « JJ mois AAAA » (mois accentue, « 1er » pour le 1er).

    Convention partagee des types generalistes recents d'Albane (SASU/micro holding) :
    jour SANS zero initial, « 1er » pour le premier du mois, mois accentue (cf. FRENCH_MONTHS).
    Ex. date(2026, 5, 22) -> « 22 mai 2026 » ; date(2026, 5, 1) -> « 1er mai 2026 »."""
    jour = "1er" if value.day == 1 else str(value.day)
    return f"{jour} {FRENCH_MONTHS[value.month]} {value.year}"
