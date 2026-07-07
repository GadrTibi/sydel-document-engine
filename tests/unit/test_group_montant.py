"""Tests du groupement des montants R5 (Albane 2026-07-07) — `group_montant`.

Convention : tout MONTANT >= 4 chiffres sort groupe par 3 (« 60 000 »), applique a la
CONSTRUCTION du contexte cote front. Contrat STRICT anti-degat : seule une valeur
purement numerique est regroupee ; tout le reste (unite accolee, plage, texte,
identifiant) est renvoye INTACT. Assertions adversariales (doublons, decimales,
conventions concurrentes, mutation) des le 1er jet.
"""

from __future__ import annotations

from sydel_doc_engine.domain.models import StatutsCivilsApport, StatutsCivilsAssocie
from sydel_doc_engine.front_app.field_derivations import (
    group_montant,
    groupe_montants_associe,
)


def test_group_montant_groupe_des_4_chiffres() -> None:
    assert group_montant("1000") == "1 000"
    assert group_montant("60000") == "60 000"
    assert group_montant("10000") == "10 000"
    assert group_montant("2000") == "2 000"
    assert group_montant(60000) == "60 000"  # entier calcule (ex. capital max = 10x)


def test_group_montant_idempotent_et_normalise_les_insecables() -> None:
    assert group_montant("60 000") == "60 000"
    assert group_montant("60 000") == "60 000"  # NBSP -> espace normal
    assert group_montant("60 000") == "60 000"  # NNBSP -> espace normal
    assert group_montant(group_montant("1234567")) == group_montant("1234567")


def test_group_montant_sous_4_chiffres_inchange() -> None:
    assert group_montant("600") == "600"
    assert group_montant("0") == "0"
    assert group_montant("") == ""
    assert group_montant(None) == ""


def test_group_montant_preserve_la_partie_decimale_verbatim() -> None:
    # Difference voulue avec format_grouped_numeric_value : pas de perte du zero final.
    assert group_montant("1500,50") == "1 500,50"
    assert group_montant("1234.5") == "1 234.5"
    assert group_montant("100,00") == "100,00"  # < 4 chiffres entiers : intact


def test_group_montant_ne_touche_jamais_une_valeur_non_purement_numerique() -> None:
    # Unite accolee (champ libre « Seuil de depense commune », hint « 1 500 euros »).
    assert group_montant("1500 euros") == "1500 euros"
    assert group_montant("0 euro") == "0 euro"
    assert group_montant("100 €") == "100 €"
    # Plage de parts, texte, marqueur R10.
    assert group_montant("41 a 100") == "41 a 100"
    assert group_montant("(À COMPLÉTER : apport individuel)") == (
        "(À COMPLÉTER : apport individuel)"
    )
    # Convention POINT du modele micro holding (Albane 2026-06-29) : intacte.
    assert group_montant("1.020") == "1.020"
    assert group_montant("10.200") == "10.200"


def test_groupe_montants_associe_copie_sans_muter_l_original() -> None:
    original = StatutsCivilsAssocie(
        type_personne="personne_physique",
        apport=StatutsCivilsApport(montant="10000", montant_lettres="dix mille"),
    )
    copie = groupe_montants_associe(original)
    assert copie.apport is not None
    assert copie.apport.montant == "10 000"
    assert copie.apport.montant_lettres == "dix mille"  # lettres inchangees
    assert original.apport is not None
    assert original.apport.montant == "10000"  # payload appelant JAMAIS mute


def test_groupe_montants_associe_capital_personne_morale() -> None:
    pm = StatutsCivilsAssocie(type_personne="personne_morale", capital_social="60000")
    assert groupe_montants_associe(pm).capital_social == "60 000"
    assert pm.capital_social == "60000"


def test_groupe_montants_associe_sans_changement_rend_le_meme_objet() -> None:
    deja_groupe = StatutsCivilsAssocie(
        type_personne="personne_physique",
        apport=StatutsCivilsApport(montant="1 000", montant_lettres="mille"),
    )
    assert groupe_montants_associe(deja_groupe) is deja_groupe
