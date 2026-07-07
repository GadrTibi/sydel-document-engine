"""Civilité d'adresse CIVILE — R3 (Albane 2026-07-07).

Verbatim Albane : « "Docteur" n'est pas une civilité ! La retirer partout où
elle existe » (comme civilité). Le TITRE professionnel « le Docteur X » dans le
corps des actes reste légitime (retours A26-45/49) : seuls les SLOTS de civilité
(« Je soussigné __ », « par le Président, __ », bloc signature, tête de
désignation de personne) passent par ce helper, qui substitue Monsieur/Madame
(accordé au genre) à un titre professionnel (« Docteur »/« Dr ») posé en
civilité. Une civilité déjà civile (Monsieur/Madame…) est renvoyée inchangée.
"""

from __future__ import annotations

from sydel_doc_engine.domain.enums import Gender

# Titres d'adresse professionnels jamais admis en civilité — même ensemble que le
# discriminant PV2 `_is_title_only` (pv_nomination_gerant, retour Albane 2026-06-26).
_TITRES_PROFESSIONNELS = frozenset({"docteur", "dr", "dr."})


def est_titre_professionnel(value: str) -> bool:
    """Vrai si `value` est un TITRE d'adresse (« Docteur »/« Dr ») et non une civilité."""
    return value.strip().casefold() in _TITRES_PROFESSIONNELS


def civilite_civile(civilite: str, genre: Gender | None) -> str:
    """Civilité CIVILE pour un slot de civilité : « Docteur »/« Dr » -> Monsieur/Madame.

    `genre` absent (modèles sans champ genre) -> masculin par défaut, comme
    `derive_gender_from_civilite` côté front (le flux réel pose le genre du
    signataire). Toute autre civilité est renvoyée telle quelle (aucune réécriture
    d'une donnée déjà civile).
    """
    if est_titre_professionnel(civilite):
        return "Madame" if genre == Gender.FEMININ else "Monsieur"
    return civilite.strip()
