"""Tests adversariaux des helpers FRONT du lot « Statuts SELAS multi » (retours
Albane 2026-06-26). Helpers PURS (pas de Streamlit) : zero-pad du jour de naissance
(ST3) et situation maritale complete régime + conjoint (ST4)."""

from __future__ import annotations

import pytest

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.front_app.field_derivations import (
    pad_birthdate_day,
    situation_maritale_complete,
)

# --- ST3 : jour de naissance zero-pade (1..9 -> 01..09) -------------------------------------


@pytest.mark.parametrize(
    ("saisie", "attendu"),
    [
        ("1 janvier 1980", "01 janvier 1980"),
        ("9 août 2001", "09 août 2001"),
        ("1er mars 1990", "01 mars 1990"),  # le « er » ordinal est retire
        ("5 février 1975", "05 février 1975"),
        ("01 janvier 1980", "01 janvier 1980"),  # idempotent
        ("20 février 1994", "20 février 1994"),  # 2 chiffres inchanges
        ("31 décembre 2026", "31 décembre 2026"),
    ],
)
def test_st3_pad_birthdate_day(saisie: str, attendu: str) -> None:
    assert pad_birthdate_day(saisie) == attendu


def test_st3_pad_birthdate_day_naffecte_pas_le_millesime() -> None:
    # Le 1 du jour est zero-pade, jamais le « 1980 » du millesime.
    assert pad_birthdate_day("1 janvier 1980") == "01 janvier 1980"
    assert "01980" not in pad_birthdate_day("1 janvier 1980")


def test_st3_pad_birthdate_day_chaine_vide() -> None:
    assert pad_birthdate_day("") == ""
    assert pad_birthdate_day(None) is None  # type: ignore[arg-type]


# --- ST4 : situation maritale = regime + nom du conjoint ------------------------------------


def test_st4_marie_separation_avec_conjoint_homme() -> None:
    result = situation_maritale_complete(
        "Marié(e) sous le régime de la séparation de biens",
        Gender.MASCULIN,
        conjoint_civilite="Madame",
        conjoint_prenom="Anne",
        conjoint_nom="DURANT",
    )
    assert result == "marié sous le régime de la séparation de biens, époux de Madame Anne DURANT"
    # Plus de « marié » nu sans precision.
    assert result != "marié"
    assert "séparation de biens" in result
    assert "Anne DURANT" in result


def test_st4_mariee_communaute_legale_avec_conjoint_femme() -> None:
    result = situation_maritale_complete(
        "Marié(e) sous le régime légal / communauté",
        Gender.FEMININ,
        conjoint_civilite="Monsieur",
        conjoint_prenom="Paul",
        conjoint_nom="MARTIN",
    )
    assert result == (
        "mariée sous le régime de la communauté légale, épouse de Monsieur Paul MARTIN"
    )


def test_st4_marie_communaute_universelle_et_participation() -> None:
    universelle = situation_maritale_complete(
        "Marié(e) sous le régime de la communauté universelle", Gender.MASCULIN
    )
    assert universelle == "marié sous le régime de la communauté universelle"
    participation = situation_maritale_complete(
        "Marié(e) sous le régime de la participation aux acquêts", Gender.MASCULIN
    )
    assert participation == "marié sous le régime de la participation aux acquêts"


def test_st4_marie_sans_conjoint_garde_le_regime() -> None:
    # Regime present meme si le conjoint n'est pas (encore) saisi.
    result = situation_maritale_complete(
        "Marié(e) sous le régime de la séparation de biens", Gender.MASCULIN
    )
    assert result == "marié sous le régime de la séparation de biens"
    assert "époux de" not in result


def test_st4_non_marie_inchange() -> None:
    # Celibataire / divorce / veuf : aucun regime ni conjoint ajoute.
    assert situation_maritale_complete("Célibataire", Gender.MASCULIN) == "célibataire"
    assert situation_maritale_complete("Divorcé(e)", Gender.FEMININ) == "divorcée"
    assert situation_maritale_complete("Veuf / veuve", Gender.MASCULIN) == "veuf"
