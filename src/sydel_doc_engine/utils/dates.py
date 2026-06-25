from __future__ import annotations

from datetime import date


def format_date_fr(value: date) -> str:
    """Formate une date au format numerique francais « JJ/MM/AAAA »."""
    return value.strftime("%d/%m/%Y")
