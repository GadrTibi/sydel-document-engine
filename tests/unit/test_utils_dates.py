"""Tests du helper canonique de dates (utils/dates) — B1 Albane + accents Rafael 2026-07-09."""

from __future__ import annotations

from datetime import date

from sydel_doc_engine.utils.dates import (
    accentuate_months,
    coerce_date,
    format_birthdate_fr,
)


def test_format_birthdate_fr_numerique_vers_lettre_accentue() -> None:
    # B1 (Albane 2026-07-09) : une date numerique (objet, ISO, JJ/MM/AAAA) -> « JJ mois AAAA »
    # avec mois accentue + jour sur 2 chiffres.
    assert format_birthdate_fr(date(1975, 3, 10)) == "10 mars 1975"
    assert format_birthdate_fr("1975-03-10") == "10 mars 1975"
    assert format_birthdate_fr("10/03/1975") == "10 mars 1975"
    assert format_birthdate_fr(date(1978, 12, 1)) == "01 décembre 1978"


def test_format_birthdate_fr_lettre_saisie_reaccentuee() -> None:
    # Rafael 2026-07-09 (accents) : une date DEJA saisie en toutes lettres SANS accent
    # (« 1er aout 1980 ») ne doit pas garder le mois non accentue -> re-accentuation.
    assert format_birthdate_fr("1er aout 1980") == "1er août 1980"
    assert format_birthdate_fr("1er decembre 1978") == "1er décembre 1978"
    assert format_birthdate_fr("15 fevrier 1990") == "15 février 1990"
    # Deja accentuee -> inchangee (fidelite).
    assert format_birthdate_fr("1er janvier 1980") == "1er janvier 1980"


def test_accentuate_months_casse_et_bornes() -> None:
    assert accentuate_months("DU 15 AOUT 2026") == "DU 15 AOÛT 2026"
    assert accentuate_months("le 3 fevrier et le 8 decembre") == "le 3 février et le 8 décembre"
    # Un mot qui contient un nom de mois sans etre le mois (borne \b) reste intact.
    assert accentuate_months("aoutage") == "aoutage"


def test_coerce_date_none_sur_lettre_ou_vide() -> None:
    assert coerce_date(None) is None
    assert coerce_date("") is None
    assert coerce_date("1er decembre 1978") is None  # non parsable -> None (fidelite chaine)
    assert coerce_date("2026-05-22") == date(2026, 5, 22)
