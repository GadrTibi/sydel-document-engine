"""Bibliothèque de scénarios SELARL figés (cas type, données fictives réalistes).

Chaque scénario produit un `SelarlSliceInput` déterministe, passé tel quel au
pipeline validé `front_app.selarl_slice.generate_selarl_dossier`. C'est la
"boussole reproductible" du pack : même scénario + même commit → même documents.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from sydel_doc_engine.front_app.data_entry import build_clean_data_entry
from sydel_doc_engine.front_app.dossier_selection import dossier_type_by_label
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_DENTISTE,
    PROFESSION_MEDECIN,
    SelarlSliceInput,
)

SELARL_DOSSIER_LABEL = "SELARL creation V1"


def _base_kwargs(
    profession: str,
    *,
    regime_communautaire: bool = False,
    married_separation: bool = False,
) -> dict[str, Any]:
    """Données type d'un dossier SELARL unipersonnel (fictives mais réalistes)."""
    is_married = regime_communautaire or married_separation
    kwargs: dict[str, Any] = {
        "dossier_reference": "SCENARIO-SELARL-001",
        "profession": profession,
        "dossier_unipersonnel": True,
        "regime_communautaire": regime_communautaire,
        "civilite": "Monsieur",
        "prenom": "Jean",
        "nom": "Martin",
        "date_naissance": date(1984, 4, 12),
        "ville_naissance": "Paris",
        "departement_naissance": "75",
        "nationalite": "française",
        "nom_pere": "Pierre Martin",
        "nom_mere": "Anne Martin",
        "adresse_num_voie": "10",
        "adresse_voie": "rue Test",
        "adresse_cp": "75001",
        "adresse_ville": "Paris",
        "situation_maritale": "marie" if is_married else "celibataire",
        "regime_matrimonial": (
            "regime de communaute"
            if regime_communautaire
            else "separation de biens"
            if married_separation
            else ""
        ),
        "numero_ordre": "ORD-123",
        "numero_rpps": "10000000001",
        "departement_ordre": "75",
        "denomination": "SELARL MARTIN",
        "capital_social": "1000",
        "nb_parts_total": 100,
        "valeur_nominale_part": "10",
        "siege_num_voie": "20",
        "siege_voie": "avenue du Siege",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "ville_rcs": "Paris",
        "ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "ordre_cp": "75008",
        "ordre_ville": "Paris",
        "signature_lieu": "Paris",
        "signature_date": date(2026, 5, 26),
        "decision_date": date(2026, 5, 26),
        "depot_banque_nom": "Banque Test",
        "depot_banque_adresse": "30 boulevard Banque, 75009 Paris",
        "exercice_debut": "1er janvier",
        "exercice_fin": "31 decembre",
        "exercice_cloture_premier": "31 decembre 2026",
    }
    if profession == PROFESSION_DENTISTE or regime_communautaire or married_separation:
        kwargs.update(
            {
                "conjoint_civilite": "Madame",
                "conjoint_prenom": "Claire",
                "conjoint_nom": "Martin",
            }
        )
    return kwargs


# clé de scénario -> paramètres du cas
SELARL_SCENARIOS: dict[str, dict[str, Any]] = {
    "selarl_medecin_simple": {"profession": PROFESSION_MEDECIN},
    "selarl_dentiste_simple": {"profession": PROFESSION_DENTISTE},
    "selarl_medecin_regime_communautaire": {
        "profession": PROFESSION_MEDECIN,
        "regime_communautaire": True,
    },
}


def build_selarl_scenario(key: str) -> SelarlSliceInput:
    if key not in SELARL_SCENARIOS:
        raise KeyError(
            f"Scénario inconnu : {key}. Disponibles : {', '.join(SELARL_SCENARIOS)}"
        )
    dossier_type = dossier_type_by_label(SELARL_DOSSIER_LABEL)
    return build_clean_data_entry(dossier_type, **_base_kwargs(**SELARL_SCENARIOS[key]))
