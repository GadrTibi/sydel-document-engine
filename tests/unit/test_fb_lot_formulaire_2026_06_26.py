"""Lot Formulaire — nouveautes de SAISIE (retours Albane 2026-06-26).

Verrouille, item par item, que la SAISIE alimente bien le CONTEXTE produit aux
generateurs (cession cabinet + cession SCM standalone), via le sous-formulaire reel
piloté par un stub Streamlit minimal. Aucun generateur n'est modifie : ces tests
prouvent uniquement le CABLAGE front -> contexte.

FB-1  dénomination SCM saisie -> clause point 8 de l'acte médical (cession.scm.denomination).
FB-2  destinataire de l'appel de fonds RETIRE (cession.financement.destinataire is None).
FB-3  widget « copier » retiré (cf. test_front_widgets_copy.py).
FB-4  plage des parts cédées : saisie manuelle OVERRIDE la dérivation auto.
FB-5  plages des associés présents retirées (saisie) ; 1er présent = cédant par défaut.
FB-7  cédant préside par défaut (figure en dernière position des présents).
FB-8b case « gérant » par associé -> liste cogerants dérivée des cases cochées.
"""

from __future__ import annotations

from sydel_doc_engine.domain.models import Gender
from sydel_doc_engine.front_app import shell

# Réutilise le stub Streamlit minimal déjà éprouvé pour le sous-formulaire SCM.
from tests.unit.test_multi_type_front import _StScmStub


def _praticien() -> dict[str, object]:
    return {
        "civilite": "Monsieur",
        "prenom": "Jean",
        "nom": "Dupont",
        "situation_maritale": "marie",
        "genre": Gender.MASCULIN,
        "nationalite": "française",
    }


def _societe() -> dict[str, object]:
    return {
        "denomination": "SELARL CABINET DUPONT",
        "capital_social": "10 000",
        "ville_rcs": "Paris",
        "siege_num_voie": "20",
        "siege_voie": "avenue des Praticiens",
        "siege_cp": "75008",
        "siege_ville": "Paris",
    }


def _render(session_state: dict[str, object], monkeypatch, *, prefix: str = "selarl"):
    monkeypatch.setattr(shell, "st", _StScmStub(session_state))
    return shell._render_scm_cession_form(
        True,
        praticien=_praticien(),
        societe=_societe(),
        profession_label="chirurgien-dentiste",
        ordre={"departement_ordre": "Paris"},
        prefix=prefix,
    )


# --------------------------------------------------------------------------- FB-1


def test_fb1_denomination_scm_saisie_alimente_clause_point8(monkeypatch) -> None:
    # FB-1 (CE8) : le champ dénomination de la SCM associée (clause point 8 de l'acte
    # médical) doit alimenter cession.scm.denomination quand la clause est active. La
    # clause SCM n'existe que pour un cabinet MÉDICAL à l'étape « acte » (profession sans
    # « dentiste » -> type_cabinet medical via _cession_default_type).
    from sydel_doc_engine.front_app import shell as shell_mod

    session_state = {
        "selarl_cession_scm_clause_actif": True,
        "selarl_cession_financement_scm_parts": "10",
        "selarl_cession_financement_scm_denomination": "SCM DU PARC",
    }
    monkeypatch.setattr(shell_mod, "st", _StScmStub(session_state))
    cession, _bail = shell_mod._render_cession_form(
        True,
        "médecin",
        praticien={**_praticien(), "date_naissance": "1er janvier 1980"},
        societe=_societe(),
        ordre={"departement_ordre": "Paris"},
        generation={},
        prefix="selarl",
    )
    assert cession is not None
    assert cession.scm is not None
    assert cession.scm.actif is True
    assert cession.scm.denomination == "SCM DU PARC"


# --------------------------------------------------------------------------- FB-2


def test_fb2_destinataire_appel_de_fonds_retire(monkeypatch) -> None:
    # FB-2 : la saisie du destinataire de l'appel de fonds est retirée -> le contexte
    # financement ne porte plus de destinataire (clé absente). Société + client restent
    # alimentés par ailleurs (vendeur / acquéreur), donc l'appel de fonds reste générable.
    from sydel_doc_engine.front_app import shell as shell_mod

    session_state = {
        "selarl_cession_scm_clause_actif": False,
        # Même si d'anciennes clés destinataire traînaient, elles ne doivent plus être lues.
        "selarl_cession_financement_destinataire_nom": "FANTOME",
    }
    monkeypatch.setattr(shell_mod, "st", _StScmStub(session_state))
    cession, _bail = shell_mod._render_cession_form(
        True,
        "médecin",
        praticien={**_praticien(), "date_naissance": "1er janvier 1980"},
        societe=_societe(),
        ordre={"departement_ordre": "Paris"},
        generation={},
        prefix="selarl",
    )
    assert cession is not None
    assert cession.financement is not None
    assert cession.financement.destinataire is None


# --------------------------------------------------------------------------- FB-4


def test_fb4_plage_cedee_manuelle_override_la_derivation(monkeypatch) -> None:
    # FB-4 : une plage cédée saisie manuellement (parts non contiguës) OVERRIDE la
    # dérivation automatique. La SEL entrante (après-cession) porte la plage saisie.
    session_state = {
        "selarl_cession_scm_cedee_nb_parts_total": "25",
        "selarl_cession_scm_presents_count": 1,
        "selarl_cession_scm_present_0_civilite": "Monsieur",
        "selarl_cession_scm_present_0_prenom": "Jean",
        "selarl_cession_scm_present_0_nom": "Dupont",
        "selarl_cession_scm_present_0_nb_parts": "25",
        "selarl_cession_scm_cedant_civilite": "Monsieur",
        "selarl_cession_scm_cedant_prenom": "Jean",
        "selarl_cession_scm_cedant_nom": "Dupont",
        "selarl_cession_scm_parts_nb": "10",
        "selarl_cession_scm_parts_plage": "1 a 5 et 21 a 25",
    }
    scm = _render(session_state, monkeypatch)
    assert scm is not None
    assert scm.parts_cedees.plage == "1 a 5 et 21 a 25"
    # La personne morale entrante (SEL cessionnaire) porte la plage cédée saisie.
    entrants = [a for a in scm.associes_apres_cession if a.type_personne == "personne_morale"]
    assert entrants, "la SEL cessionnaire doit figurer dans l'apres-cession"
    assert entrants[-1].parts is not None
    assert entrants[-1].parts.plage == "1 a 5 et 21 a 25"


def test_fb4_plage_vide_garde_la_derivation_auto(monkeypatch) -> None:
    # FB-4 (revers) : plage laissée vide -> la dérivation déterministe (dernières parts
    # du cedant) reste en place, jamais figée à la valeur fixture.
    session_state = {
        "selarl_cession_scm_cedee_nb_parts_total": "100",
        "selarl_cession_scm_presents_count": 1,
        "selarl_cession_scm_present_0_civilite": "Monsieur",
        "selarl_cession_scm_present_0_prenom": "Jean",
        "selarl_cession_scm_present_0_nom": "Dupont",
        "selarl_cession_scm_present_0_nb_parts": "100",
        "selarl_cession_scm_cedant_prenom": "Jean",
        "selarl_cession_scm_cedant_nom": "Dupont",
        "selarl_cession_scm_parts_nb": "40",
        # pas de plage manuelle
    }
    scm = _render(session_state, monkeypatch)
    assert scm is not None
    # 100 parts (1 à 100), 40 cédées -> dernières parts = 61 à 100.
    # N4 (2026-07-01) : plage avec « à » accentue (derivation front).
    assert scm.parts_cedees.plage == "61 à 100"


# --------------------------------------------------------------------------- FB-5 / FB-7


def test_fb5_premier_present_prerempli_avec_cedant(monkeypatch) -> None:
    # FB-5 : le 1er présent est préremplie avec l'identité du cédant (modifiable).
    session_state = {
        "selarl_cession_scm_cedee_nb_parts_total": "100",
        "selarl_cession_scm_presents_count": 1,
        "selarl_cession_scm_cedant_civilite": "Monsieur",
        "selarl_cession_scm_cedant_prenom": "Jean",
        "selarl_cession_scm_cedant_nom": "Dupont",
        "selarl_cession_scm_present_0_nb_parts": "100",
        "selarl_cession_scm_parts_nb": "50",
    }
    scm = _render(session_state, monkeypatch)
    assert scm is not None
    present0 = scm.associes_presents[0]
    assert present0.prenom == "Jean"
    assert present0.nom == "Dupont"


def test_fb7_cedant_preside_par_defaut_figure_en_dernier(monkeypatch) -> None:
    # FB-7 : par défaut le cédant préside -> il figure en DERNIÈRE position des présents
    # (le générateur PV lit associes_presents[-1] comme président). Ici le cédant est
    # saisi en 1re position ; après réordonnancement il doit être en dernier.
    session_state = {
        "selarl_cession_scm_cedee_nb_parts_total": "300",
        "selarl_cession_scm_presents_count": 3,
        # présent 0 = le cédant
        "selarl_cession_scm_present_0_civilite": "Monsieur",
        "selarl_cession_scm_present_0_prenom": "Jean",
        "selarl_cession_scm_present_0_nom": "Dupont",
        "selarl_cession_scm_present_0_nb_parts": "100",
        # présent 1
        "selarl_cession_scm_present_1_civilite": "Monsieur",
        "selarl_cession_scm_present_1_prenom": "Paul",
        "selarl_cession_scm_present_1_nom": "Bernard",
        "selarl_cession_scm_present_1_nb_parts": "100",
        # présent 2
        "selarl_cession_scm_present_2_civilite": "Madame",
        "selarl_cession_scm_present_2_prenom": "Anne",
        "selarl_cession_scm_present_2_nom": "Martin",
        "selarl_cession_scm_present_2_nb_parts": "100",
        "selarl_cession_scm_cedant_civilite": "Monsieur",
        "selarl_cession_scm_cedant_prenom": "Jean",
        "selarl_cession_scm_cedant_nom": "Dupont",
        "selarl_cession_scm_parts_nb": "50",
    }
    scm = _render(session_state, monkeypatch)
    assert scm is not None
    president = scm.associes_presents[-1]
    assert (president.prenom, president.nom) == ("Jean", "Dupont"), (
        "le cédant doit présider par défaut (dernière position des présents)"
    )


# --------------------------------------------------------------------------- FB-8b


def test_fb8b_cases_gerant_derivent_les_cogerants(monkeypatch) -> None:
    # FB-8b : cocher « Gérant(e) » sur des présents -> la liste cogerants en est dérivée
    # (au lieu du fallback hardcodé du générateur).
    session_state = {
        "selarl_cession_scm_cedee_nb_parts_total": "200",
        "selarl_cession_scm_presents_count": 2,
        "selarl_cession_scm_present_0_civilite": "Monsieur",
        "selarl_cession_scm_present_0_prenom": "Jean",
        "selarl_cession_scm_present_0_nom": "Dupont",
        "selarl_cession_scm_present_0_nb_parts": "100",
        "selarl_cession_scm_present_0_gerant": True,
        "selarl_cession_scm_present_1_civilite": "Madame",
        "selarl_cession_scm_present_1_prenom": "Anne",
        "selarl_cession_scm_present_1_nom": "Martin",
        "selarl_cession_scm_present_1_nb_parts": "100",
        "selarl_cession_scm_present_1_gerant": True,
        "selarl_cession_scm_cedant_prenom": "Jean",
        "selarl_cession_scm_cedant_nom": "Dupont",
        "selarl_cession_scm_parts_nb": "50",
    }
    scm = _render(session_state, monkeypatch)
    assert scm is not None
    cogerants = scm.scm_cedee.cogerants
    assert "Monsieur Jean Dupont" in cogerants
    assert "Madame Anne Martin" in cogerants


def test_fb8b_aucune_case_cochee_ne_remplace_pas_le_fallback(monkeypatch) -> None:
    # FB-8b (revers) : si aucune case gérant n'est cochée, on n'écrase pas la liste de
    # base (le générateur garde son repli) -> les cogerants de la fixture subsistent.
    session_state = {
        "selarl_cession_scm_presents_count": 1,
        "selarl_cession_scm_present_0_civilite": "Monsieur",
        "selarl_cession_scm_present_0_prenom": "Jean",
        "selarl_cession_scm_present_0_nom": "Dupont",
        "selarl_cession_scm_present_0_nb_parts": "300",
        "selarl_cession_scm_cedant_prenom": "Jean",
        "selarl_cession_scm_cedant_nom": "Dupont",
        "selarl_cession_scm_parts_nb": "50",
    }
    scm = _render(session_state, monkeypatch)
    assert scm is not None
    # La fixture porte 3 cogerants ; aucune case cochée -> liste de base conservée
    # À L'IDENTIQUE (m1 Akainu 2026-06-26 : verrouiller le contenu exact du fallback,
    # pas juste « non vide » -> une régression du repli serait sinon invisible).
    assert scm.scm_cedee.cogerants == [
        "Monsieur Paul Bernard",
        "Monsieur Jean Dupont",
        "Madame Anne Martin",
    ]


# --------------------------------------------------------------------------- FB-6 / FB-8a


def test_fb6_siege_scm_egal_siege_sel_prerempli(monkeypatch) -> None:
    # FB-6 / FB-8a : case « Siège de la SCM = siège de la SEL » -> scm_cedee.siege est
    # préremplie avec le siège de la société (alimente le PV + l'exposé en SELAS).
    session_state = {
        "selarl_cession_scm_cedee_siege_same_as_sel": True,
        "selarl_cession_scm_presents_count": 1,
        "selarl_cession_scm_present_0_civilite": "Monsieur",
        "selarl_cession_scm_present_0_prenom": "Jean",
        "selarl_cession_scm_present_0_nom": "Dupont",
        "selarl_cession_scm_present_0_nb_parts": "300",
        "selarl_cession_scm_cedant_prenom": "Jean",
        "selarl_cession_scm_cedant_nom": "Dupont",
        "selarl_cession_scm_parts_nb": "50",
    }
    scm = _render(session_state, monkeypatch)
    assert scm is not None
    assert scm.scm_cedee.siege is not None
    assert scm.scm_cedee.siege.adresse_affichee == "20 avenue des Praticiens, 75008 Paris"
