from __future__ import annotations

from typing import Final

# Mois francais ACCENTUES, indexes par numero de mois (1 = janvier ... 12 = decembre).
# L'index 0 est une chaine vide : `FRENCH_MONTHS[value.month]` fonctionne directement.
# Convention CRITIQUE (Rafael 2026-06-23) : les sorties portent les accents
# (fevrier/aout/decembre). Ne PAS retirer les accents de cette table.
FRENCH_MONTHS: Final = (
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
