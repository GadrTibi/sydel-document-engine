"""Mapping cession SCM <- saisie reelle (retour Albane lot 2, §13.2 / §13.3).

Le sous-formulaire de cession SCM partait d'une fixture de demo : le cedant et la
description de la SEL cessionnaire restaient des valeurs fictives (cedant suisse
affiche francais, capital 10 000 alors que 1 000 saisi). Ces tests verrouillent
la derivation pure (praticien -> cedant, societe -> cessionnaire) et prouvent que
le contexte revalide porte bien les donnees reelles, format de date inclus.
"""

from __future__ import annotations

from datetime import date

from sydel_doc_engine.domain.models import ScmCessionContext
from sydel_doc_engine.front_app.shell import (
    _scm_cedant_overrides,
    _scm_cessionnaire_overrides,
)
from sydel_doc_engine.scenarios.selarl import scm_cession_fixture


def _praticien_suisse() -> dict[str, object]:
    return {
        "civilite": "Monsieur",
        "prenom": "Hans",
        "nom": "Muller",
        "nationalite": "suisse",
        "adresse_num_voie": "",
        "adresse_voie": "10 rue du Lac",
        "adresse_cp": "74000",
        "adresse_ville": "Annecy",
        "date_naissance": date(1979, 3, 4),
        "ville_naissance": "Genève",
        "departement_naissance": "99",
        "situation_maritale": "marie",
        "numero_rpps": "10999000111",
        "numero_ordre": "ORD-555",
        "conjoint_civilite": "Madame",
        "conjoint_prenom": "Eva",
        "conjoint_nom": "Roux",
    }


def _societe_1000() -> dict[str, object]:
    return {
        "denomination": "SELARL MULLER",
        "capital_social": "1 000",
        "ville_rcs": "Annecy",
        "siege_num_voie": "",
        "siege_voie": "5 rue de la Sante",
        "siege_cp": "74000",
        "siege_ville": "Annecy",
    }


def test_cedant_overrides_derive_du_praticien() -> None:
    overrides = _scm_cedant_overrides(
        _praticien_suisse(), profession_label="Medecin", departement_ordre="Haute-Savoie"
    )
    assert overrides["nationalite"] == "suisse"
    assert overrides["adresse_affichee"] == "10 rue du Lac, 74000 Annecy"
    assert overrides["date_naissance"] == date(1979, 3, 4)
    assert overrides["ville_naissance"] == "Genève"
    assert overrides["situation_maritale"] == "marie"
    assert overrides["numero_rpps"] == "10999000111"
    # Profession derivee du parcours (medecin ici), pas la valeur dentiste de la fixture.
    assert overrides["profession"] == "médecin"
    assert overrides["profession_reglementee_pluriel"] == "médecins"
    # Ordre : numero depuis la fiche praticien, departement depuis le bloc ordre.
    assert overrides["ordre"] == {"numero": "ORD-555", "departemental": "Haute-Savoie"}
    assert overrides["conjoint"] == {
        "civilite_affichage": "Madame",
        "prenom": "Eva",
        "nom": "Roux",
    }


def test_cedant_overrides_dentiste_label() -> None:
    overrides = _scm_cedant_overrides(
        _praticien_suisse(), profession_label="Chirurgien-dentiste", departement_ordre="Paris"
    )
    assert overrides["profession"] == "chirurgien-dentiste"
    assert overrides["profession_reglementee_pluriel"] == "chirurgiens-dentistes"


def test_cedant_overrides_ignore_les_champs_vides() -> None:
    # Champs vides -> non renvoyes (la valeur de base / fixture reste inchangee,
    # aucune cle requise n'est ecrasee par du vide).
    overrides = _scm_cedant_overrides(
        {"prenom": "Hans"}, profession_label="Medecin", departement_ordre=""
    )
    assert "nationalite" not in overrides
    assert "ordre" not in overrides
    assert "conjoint" not in overrides


def test_cessionnaire_overrides_derive_de_la_societe() -> None:
    overrides = _scm_cessionnaire_overrides(_societe_1000())
    assert overrides["denomination"] == "SELARL MULLER"
    assert overrides["capital_social"] == "1 000"
    assert overrides["ville_rcs"] == "Annecy"
    assert overrides["siege"] == {"adresse_affichee": "5 rue de la Sante, 74000 Annecy"}


def test_payload_revalide_porte_les_donnees_reelles() -> None:
    # Reproduit l'enchainement du front : fixture -> dump -> overrides -> revalidation.
    payload = scm_cession_fixture().model_dump(by_alias=True)

    cedant = payload["cedant"]
    overrides = _scm_cedant_overrides(
        _praticien_suisse(), profession_label="Medecin", departement_ordre="Haute-Savoie"
    )
    ordre_override = overrides.pop("ordre", None)
    cedant.update(overrides)
    if ordre_override:
        cedant["ordre"] = {**(cedant.get("ordre") or {}), **ordre_override}
    payload["cedant"] = cedant

    cessionnaire = payload["cessionnaire"]
    cessionnaire.update(_scm_cessionnaire_overrides(_societe_1000()))
    payload["cessionnaire"] = cessionnaire

    ctx = ScmCessionContext.model_validate(payload)
    # §13.2 : le cedant n'est plus francais ni a l'adresse de la fixture.
    assert ctx.cedant.nationalite == "suisse"
    assert ctx.cedant.adresse_affichee == "10 rue du Lac, 74000 Annecy"
    assert ctx.cedant.date_naissance == date(1979, 3, 4)
    # §13.3 : la SEL cessionnaire affiche le capital reellement saisi (1 000), pas 10 000.
    assert ctx.cessionnaire.capital_social == "1 000"
    assert ctx.cessionnaire.denomination == "SELARL MULLER"
    assert ctx.cessionnaire.siege is not None
    assert ctx.cessionnaire.siege.adresse_affichee == "5 rue de la Sante, 74000 Annecy"
