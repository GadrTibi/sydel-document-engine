"""Tests adversariaux micro holding (DOC-047, demande Albane 2026-06-26).

Micro holding = societe civile A CAPITAL VARIABLE, clone du socle SCI dont le seul bloc
objet (article 2) est pilote par variante A (generique civil) / B (holding). Ces tests
verifient le COMPORTEMENT (le bon objet selon le flag, le capital variable, le max = 10x le
minimum, l'absence de token residuel, le bundle de creation civil), pas seulement la presence.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from docx import Document

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Company,
    DocumentGenerationContext,
    Person,
    Signature,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsCapitalDepot,
    StatutsCivilsContext,
    StatutsCivilsParts,
)
from sydel_doc_engine.front_app import civil_statuts_slice as cs
from sydel_doc_engine.front_app.type_registry import registered_type_by_key
from sydel_doc_engine.generators.lot_04.statuts_micro_holding import (
    OBJET_VARIANTE_A,
    OBJET_VARIANTE_B,
    StatutsMicroHoldingGenerator,
    objet_social_for_variante,
)
from sydel_doc_engine.registry.catalog import ALL_STRUCTURES


def _docx_text(path: Path) -> str:
    document = Document(path)
    texts = [p.text for p in document.paragraphs if p.text]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                texts.extend(p.text for p in cell.paragraphs if p.text)
    return "\n".join(texts)


def _associe(
    prenom: str, nom: str, nb: int, debut: int, fin: int, *, montant: int | None = None
) -> StatutsCivilsAssocie:
    amount = str(montant if montant is not None else nb * 10)
    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=Gender.MASCULIN,
        civilite_affichage="Monsieur",
        prenom=prenom,
        prenoms=prenom,
        nom=nom,
        date_naissance="1 janvier 1980",
        ville_naissance="Paris",
        departement_naissance="75",
        nationalite="francaise",
        situation_maritale="celibataire",
        adresse_personnelle=Address(num_voie="1", voie="rue Exemple", cp="75000", ville="Paris"),
        adresse_personnelle_affichee="1 rue Exemple, 75000 Paris",
        apport=StatutsCivilsApport(montant=amount, montant_lettres=amount),
        parts=StatutsCivilsParts(
            nb=nb, nb_lettres=str(nb), plage_affichee=f"{debut} a {fin}", debut=debut, fin=fin
        ),
    )


def _ctx(variante: str, *, capital_min: int = 1000) -> DocumentGenerationContext:
    cap = str(capital_min)
    cap_max = str(capital_min * 10)
    return DocumentGenerationContext(
        structure="MICRO_HOLDING",
        personne_signataire=Person(
            genre=Gender.MASCULIN, civilite="Monsieur", prenom="Jean", nom="Durand"
        ),
        signature=Signature(lieu="Paris", date=date(2026, 5, 15)),
        societe=Company(
            denomination="MA MICRO HOLDING",
            forme_sociale="societe civile",
            siege=Address(
                num_voie="10",
                voie="rue de la Paix",
                cp="75002",
                ville="Paris",
                adresse_affichee="10 rue de la Paix, 75002 Paris",
            ),
            ville_rcs="Paris",
        ),
        statuts_civils=StatutsCivilsContext(
            type="micro_holding",
            forme_sociale="societe civile",
            objet_social=objet_social_for_variante(variante),
            mention_capital_variable="a capital variable",
            capital_social=cap,
            capital_social_lettres="mille",
            capital_autorise=cap_max,
            capital_autorise_lettres="dix mille",
            capital_maximal=cap_max,
            capital_maximal_lettres="dix mille",
            nb_parts_total=100,
            nb_parts_total_lettres="cent",
            valeur_nominale_part="10",
            valeur_nominale_part_lettres="dix",
            plage_parts_totale="1 a 100",
            duree_societe="99",
            capital_depot=StatutsCivilsCapitalDepot(
                banque_nom="BANQUE EXEMPLE", banque_adresse="1 rue Banque, 75009 Paris"
            ),
            associes=[
                # Apports coherents avec le capital saisi (somme apports == capital_social) :
                # 40 / 60 parts -> 40% / 60% du capital. Le generateur valide cette egalite.
                _associe("Jean", "Durand", 40, 1, 40, montant=capital_min * 40 // 100),
                _associe("Alice", "Martin", 60, 41, 100, montant=capital_min * 60 // 100),
            ],
            date_cloture_premier_exercice="31 decembre 2026",
            nombre_exemplaires_lettres="trois",
            denomination_cabinet_mandataire="DAAT",
        ),
    )


def _payload(variante: str, capital_min: int = 1000) -> dict:
    cap = str(capital_min)
    return {
        "structure": "MICRO_HOLDING",
        "statuts_type": "micro_holding",
        "denomination": "MA MICRO HOLDING",
        "capital_social": cap,
        "nb_parts_total": 100,
        "valeur_nominale_part": str(capital_min // 100),
        "siege_num": "10",
        "siege_voie": "rue de la Paix",
        "siege_cp": "75002",
        "siege_ville": "Paris",
        "ville_rcs": "Paris",
        "banque_nom": "BANQUE",
        "banque_adresse": "1 rue Banque, 75009 Paris",
        "date_cloture_premier_exercice": "31 decembre 2026",
        "signature_lieu": "Paris",
        "signature_date": date(2026, 5, 15),
        "decision_date": date(2026, 5, 10),
        "associes": [
            _associe("Jean", "Durand", 40, 1, 40),
            _associe("Alice", "Martin", 60, 41, 100),
        ],
        "gerant_index": 0,
        "objet_variante": variante,
    }


# --- enregistrement du type --------------------------------------------------


def test_micro_holding_structure_registered() -> None:
    assert "MICRO_HOLDING" in ALL_STRUCTURES
    assert "MICRO_HOLDING" in cs.CIVIL_TYPE_BY_STRUCTURE
    statuts_type, doc_code = cs.CIVIL_TYPE_BY_STRUCTURE["MICRO_HOLDING"]
    assert statuts_type == "micro_holding"
    assert doc_code == "DOC-047"


def test_micro_holding_registered_in_type_registry() -> None:
    rt = registered_type_by_key("micro_holding_v1")
    assert rt.structure == "MICRO_HOLDING"
    assert rt.slice_module == "sydel_doc_engine.front_app.micro_holding_slice"
    assert rt.generation_enabled is True


# --- objet social selon le flag (A vs B) -------------------------------------


def test_objet_a_renders_generic_object(tmp_path: Path) -> None:
    out = StatutsMicroHoldingGenerator().generate(_ctx("A"), tmp_path)
    text = _docx_text(out)
    # Variante A = objet societe civile generique (modele SCI).
    assert "biens et droits immobiliers" in text
    # Le marqueur exclusif de la variante B NE DOIT PAS apparaitre.
    assert "à toutes entreprises ou sociétés" not in text


def test_objet_b_renders_holding_object(tmp_path: Path) -> None:
    out = StatutsMicroHoldingGenerator().generate(_ctx("B"), tmp_path)
    text = _docx_text(out)
    # Variante B = objet holding (participation a toutes entreprises ou societes).
    assert "à toutes entreprises ou sociétés" in text
    assert "La participation de la société" in text
    # Le marqueur exclusif de la variante A NE DOIT PAS apparaitre.
    assert "biens et droits immobiliers" not in text


def test_objet_variante_default_is_a() -> None:
    assert objet_social_for_variante(None) == OBJET_VARIANTE_A
    assert objet_social_for_variante("") == OBJET_VARIANTE_A
    assert objet_social_for_variante("A") == OBJET_VARIANTE_A
    assert objet_social_for_variante("B") == OBJET_VARIANTE_B
    # Casse tolerante.
    assert objet_social_for_variante("b") == OBJET_VARIANTE_B


# --- capital variable, max = 10x min, pas de token residuel -------------------


@pytest.mark.parametrize(
    ("variante", "capital_min"),
    [("A", 1000), ("B", 1000), ("A", 2500), ("B", 33000)],
)
def test_capital_variable_and_no_residual_token(
    tmp_path: Path, variante: str, capital_min: int
) -> None:
    out = StatutsMicroHoldingGenerator().generate(
        _ctx(variante, capital_min=capital_min), tmp_path
    )
    text = _docx_text(out)
    # Pas de placeholder source residuel.
    assert "[" not in text
    assert "]" not in text
    # Mention de capital variable presente.
    assert "capital" in text.lower()
    assert "variable" in text.lower()


@pytest.mark.parametrize("capital_min", [1000, 1500, 2500, 33000, 100_000_000])
def test_capital_max_is_ten_times_min_via_slice(capital_min: int) -> None:
    # Le maximum (capital_autorise) est calcule par le slice = 10x le minimum saisi.
    # Inclut un cas NON-ROND (1500 -> 15000) et un cas franchissant le MILLIARD
    # (100 000 000 -> 1 000 000 000) : Akainu 2026-06-26.
    ctx = cs.build_generation_context(_payload("A", capital_min=capital_min))
    sc = ctx.statuts_civils
    assert sc.capital_social == str(capital_min)
    assert sc.capital_autorise == str(capital_min * 10)
    assert sc.capital_maximal == str(capital_min * 10)
    assert sc.mention_capital_variable == "a capital variable"


def test_capital_autorise_lettres_correct_y_compris_milliard() -> None:
    # Akainu 2026-06-26 : le MAXIMUM en LETTRES doit etre correct, y compris au-dela du
    # milliard (bug « mille millions » au lieu de « un milliard » corrige dans
    # integer_to_french_words). Cas non-rond + cas milliard.
    ctx_nr = cs.build_generation_context(_payload("A", capital_min=1500))
    assert ctx_nr.statuts_civils.capital_autorise == "15000"
    assert ctx_nr.statuts_civils.capital_autorise_lettres == "quinze mille"

    ctx_g = cs.build_generation_context(_payload("A", capital_min=100_000_000))
    assert ctx_g.statuts_civils.capital_autorise == "1000000000"
    assert ctx_g.statuts_civils.capital_autorise_lettres == "un milliard"
    assert "mille millions" not in ctx_g.statuts_civils.capital_autorise_lettres


@pytest.mark.parametrize(
    ("capital_min", "max_lettres"),
    [
        (8000, "quatre-vingt mille"),  # « vingt » invariable devant « mille »
        (30000, "trois cent mille"),  # « cent » invariable devant « mille »
        (80000, "huit cent mille"),
        (28000, "deux cent quatre-vingt mille"),
    ],
)
def test_capital_autorise_lettres_accord_vingt_cent(capital_min: int, max_lettres: str) -> None:
    # Akainu 2026-06-26 : « quatre-vingts » et « cents » INVARIABLES devant « mille ».
    ctx = cs.build_generation_context(_payload("A", capital_min=capital_min))
    assert ctx.statuts_civils.capital_autorise == str(capital_min * 10)
    assert ctx.statuts_civils.capital_autorise_lettres == max_lettres


def test_capital_max_ligne_dans_docx_reel(tmp_path: Path) -> None:
    # Akainu 2026-06-26 : regenerer le DOCX et controler que la ligne du maximum (capital
    # autorise) porte la BONNE valeur en lettres et en chiffres (min 1000 -> max 10000).
    out = StatutsMicroHoldingGenerator().generate(_ctx("A", capital_min=1000), tmp_path)
    text = _docx_text(out)
    assert "Le capital social est variable" in text
    assert "dix mille" in text  # capital autorise = 10x 1000, en lettres
    assert "10000" in text  # capital autorise en chiffres


def test_slice_resolves_objet_from_variante() -> None:
    ctx_a = cs.build_generation_context(_payload("A"))
    ctx_b = cs.build_generation_context(_payload("B"))
    assert ctx_a.statuts_civils.objet_social == OBJET_VARIANTE_A
    assert ctx_b.statuts_civils.objet_social == OBJET_VARIANTE_B


# --- objet social obligatoire (garde) ----------------------------------------


def test_micro_holding_requires_objet_social(tmp_path: Path) -> None:
    ctx = _ctx("A")
    ctx.statuts_civils.objet_social = None
    with pytest.raises(ValueError, match="objet_social"):
        StatutsMicroHoldingGenerator().generate(ctx, tmp_path)


# --- bundle de creation = statuts + tronc commun civil -----------------------


def test_bundle_is_statuts_plus_civil_tronc_commun() -> None:
    plan = cs.build_civil_plan(_payload("A"))
    codes = set(plan.document_codes)
    # Statuts micro holding + tronc commun civil (DNC, domiciliation, procuration) + PV gerant.
    assert "DOC-047" in codes  # statuts micro holding
    assert "DOC-001" in codes  # declaration non-condamnation
    assert "DOC-002" in codes  # autorisation de domiciliation
    assert "DOC-003" in codes  # procuration
    assert "DOC-004" in codes  # PV nomination gerant (partie du bundle annonce, Akainu)
    # Pas de satellites SCM ni d'option IS sur la micro holding.
    assert "DOC-025" not in codes
    assert "DOC-026" not in codes
    assert "DOC-022" not in codes
