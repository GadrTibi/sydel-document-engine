"""Retours Albane 2026-07-07 — UX front SPFPL cession (répartition des parts).

1. « Le système parts avant / parts après / plage n'est pas intuitif ni pertinent
   puisqu'il peut être DÉDUIT. Calcul automatique. Exemple : 20 parts -> automatiquement
   de 1 à 20. » -> plages + parts après DÉRIVÉES (plus de saisie manuelle).
2. « Ajouter la possibilité de retirer un associé EN PARTICULIER. » -> bouton « Retirer »
   par ligne (répartition SPFPL + composant partagé associe_repeater).
3. « Je ne vois pas la possibilité de retirer la plage de parts ??? » -> champs plage
   retirés de la saisie (dérivés, affichés en lecture seule).

Les tests prouvent : les helpers purs, le CABLAGE render -> cession_data (stub Streamlit,
patron test_fb_lot_formulaire), l'équivalence BYTE des bundles générés (saisie dérivée ==
saisie manuelle équivalente), et le retrait au milieu en session réelle (AppTest).

PROPAGATION (règle 68 Q4) — le retour 2 (« retirer un associé EN PARTICULIER ») s'applique
à TOUS les repeaters d'associés : SELAS multi (`selas_multi_slice`), SELARL membres
additionnels (`shell._render_selarl_membres`), en plus du composant partagé et du SPFPL.
Le retour 3 (« retirer la plage ») se propage au champ « Plage de parts » de la section
Dépôt/titres SPFPL : SAISI + REQUIS en cession alors qu'aucun document du bundle cession
ne le consomme -> retiré (il reste APPORT-only).
"""

from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.front_app import spfpl_slice
from sydel_doc_engine.front_app.field_derivations import (
    derive_cumulative_plages,
    shift_repeater_rows_down,
)

# Réutilise le stub Streamlit minimal + le payload SPFPL canon déjà éprouvés.
from tests.unit.test_multi_type_front import _docx_text, _spfpl_payload, _StScmStub

PREFIX = "spfpl_cession"


# ------------------------------------------------------------------ helpers purs


def test_derive_cumulative_plages_verbatim_20_80() -> None:
    # Verbatim Albane : « 20 parts -> automatiquement de 1 à 20 » ; attribution contiguë
    # séquentielle (associé 2 : 21 à 100). « à » accentué (convention N4 ratifiée).
    assert derive_cumulative_plages([20, 80]) == ["1 à 20", "21 à 100"]


def test_derive_cumulative_plages_zero_et_start() -> None:
    # nb <= 0 -> plage VIDE (aucune mention), le curseur n'avance pas.
    assert derive_cumulative_plages([0, 40, 0, 60]) == ["", "1 à 40", "", "41 à 100"]
    assert derive_cumulative_plages([10], start=41) == ["41 à 50"]
    assert derive_cumulative_plages([1]) == ["1 à 1"]
    assert derive_cumulative_plages([]) == []


def test_shift_repeater_rows_down_retire_le_milieu() -> None:
    state: dict[str, object] = {
        "p_assoc_0_prenom": "A",
        "p_assoc_0_avant": 20,
        "p_assoc_1_prenom": "B",
        "p_assoc_1_avant": 30,
        "p_assoc_2_prenom": "C",
        "p_assoc_2_avant": 50,
        # Clé étrangère au patron (compteur / autre widget) : jamais touchée.
        "p_nb_associes": 3,
        "p_assoc_remove_1": True,
    }
    shift_repeater_rows_down(state, "p_assoc_", 1, 3)
    assert state["p_assoc_0_prenom"] == "A"  # ligne avant l'index retiré : intacte
    assert state["p_assoc_1_prenom"] == "C"  # la ligne 2 remonte en 1
    assert state["p_assoc_1_avant"] == 50
    # Les clés de la dernière ligne sont supprimées (une ligne re-ajoutée repart vierge).
    assert "p_assoc_2_prenom" not in state
    assert "p_assoc_2_avant" not in state
    assert state["p_nb_associes"] == 3  # compteur à la charge de l'appelant


def test_shift_repeater_rows_down_ligne_disparue_champs_heterogenes() -> None:
    # Lignes hétérogènes (personne physique vs morale) : la ligne cible est ENTIÈREMENT
    # remplacée par la suivante — aucun champ orphelin de l'ancienne ligne ne survit.
    state: dict[str, object] = {
        "p_assoc_0_denomination": "SELARL X",  # ligne 0 : personne morale
        "p_assoc_1_prenom": "B",  # ligne 1 : personne physique
    }
    shift_repeater_rows_down(state, "p_assoc_", 0, 2)
    assert state == {"p_assoc_0_prenom": "B"}


def test_shift_repeater_rows_down_ignore_cles_non_assignables() -> None:
    # Une clé refusée à l'écriture (bouton Streamlit, ex. suffixe `_today`) est ignorée
    # sans faire échouer la recopie des autres champs.
    class _EtatBoutonVerrouille(dict):
        def __setitem__(self, key: str, value: object) -> None:
            if key.endswith("_today"):
                raise RuntimeError("bouton non assignable")
            super().__setitem__(key, value)

    state = _EtatBoutonVerrouille(
        {
            "p_assoc_0_prenom": "A",
            "p_assoc_1_prenom": "B",
            "p_assoc_1_date_naissance_today": False,
        }
    )
    shift_repeater_rows_down(state, "p_assoc_", 0, 2)
    assert state["p_assoc_0_prenom"] == "B"
    assert "p_assoc_0_date_naissance_today" not in state
    assert "p_assoc_1_prenom" not in state


# ------------------------------------------------- dérivation répartition SPFPL


def test_cedant_index_match_nom_puis_fallback_premiere_ligne() -> None:
    associes: list[dict[str, object]] = [
        {"prenom": "Louise", "nom": "Bernard"},
        {"prenom": "Camille", "nom": " MARTIN "},
    ]
    # Match prénom+nom insensible à la casse/espaces : le cédant n'est pas forcément 1er.
    assert spfpl_slice._cession_cedant_index(associes, "Camille", "Martin") == 1
    # Aucune correspondance -> 1re ligne (convention : le fondateur se liste en premier).
    assert spfpl_slice._cession_cedant_index(associes, "Jean", "Dupont") == 0
    # Nom fondateur vide (payload incomplet) -> jamais de match sur du vide, 1re ligne.
    assert spfpl_slice._cession_cedant_index(associes, "", "") == 0


def test_derive_cession_repartition_reproduit_le_dossier_canon() -> None:
    # Scénario canon (payload _spfpl_payload) : Camille 70 / Louise 30, 60 cédées par le
    # fondateur Camille -> après 10/30, plages « 1 à 10 » / « 11 à 40 », holding
    # « 41 à 100 ». Reproduit EXACTEMENT la saisie manuelle des dossiers validés.
    associes: list[dict[str, object]] = [
        {"civilite": "Docteur", "prenom": "Camille", "nom": "Martin", "avant": 70},
        {"civilite": "Docteur", "prenom": "Louise", "nom": "Bernard", "avant": 30},
    ]
    plage_cedee, cedant_index = spfpl_slice._derive_cession_repartition(
        associes, 60, "Camille", "Martin"
    )
    assert cedant_index == 0
    assert [a["apres"] for a in associes] == [10, 30]
    assert [a["plage"] for a in associes] == ["1 à 10", "11 à 40"]
    assert plage_cedee == "41 à 100"


def test_derive_cession_repartition_cedant_cede_tout() -> None:
    # Le cédant cède TOUTES ses parts -> après 0, plage vide (mention omise), les autres
    # remontent en tête de numérotation, le holding prend la fin.
    associes: list[dict[str, object]] = [
        {"prenom": "Camille", "nom": "Martin", "avant": 60},
        {"prenom": "Louise", "nom": "Bernard", "avant": 40},
    ]
    plage_cedee, cedant_index = spfpl_slice._derive_cession_repartition(
        associes, 60, "Camille", "Martin"
    )
    assert cedant_index == 0
    assert [a["apres"] for a in associes] == [0, 40]
    assert [a["plage"] for a in associes] == ["", "1 à 40"]
    assert plage_cedee == "41 à 100"


def test_cedees_superieures_aux_parts_du_cedant_ne_bloque_plus() -> None:
    # KAN-2 (Rafael 2026-07-14) : plus AUCUN blocage — « tous les documents doivent pouvoir être
    # générés, même si je ne remplis aucun champ ». Parts cédées > parts AVANT du cédant est
    # surfacé en AVERTISSEMENT (la répartition dérivée plafonne à 0, le document sort et se
    # corrige à la main) au lieu d'interdire la génération.
    payload = _spfpl_payload("SPFPL cession")
    cession = dict(payload["cession_data"])
    cession["associes"] = [
        {**cession["associes"][0], "avant": 50},  # Camille (cédant) : 50 < 60 cédées
        cession["associes"][1],
    ]
    payload["cession_data"] = cession
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert plan.blockers == ()
    assert any("cedant" in w.lower() and "superieures" in w.lower() for w in plan.warnings)


# ------------------------------------------------- câblage render -> cession_data


class _StubEnregistreur(_StScmStub):
    """Stub Streamlit qui journalise les clés de widgets rendus (preuve de retrait)."""

    def __init__(self, session_state: dict[str, object]) -> None:
        super().__init__(session_state)
        self.widget_keys: list[str] = []
        self.captions: list[str] = []

    def text_input(self, _label, *, key=None, disabled=False, value=None, **_k):
        if key is not None:
            self.widget_keys.append(str(key))
        return super().text_input(_label, key=key, disabled=disabled, value=value, **_k)

    def number_input(self, _label, *, key=None, min_value=None, step=None, **_k):
        if key is not None:
            self.widget_keys.append(str(key))
        return super().number_input(_label, key=key, min_value=min_value, step=step, **_k)

    def caption(self, message, *_a, **_k):
        self.captions.append(str(message))
        return None


def _stub_render_cession(
    session_state: dict[str, object], monkeypatch
) -> tuple[dict[str, object], _StubEnregistreur]:
    from sydel_doc_engine.front_app import _field_inputs

    stub = _StubEnregistreur(session_state)
    monkeypatch.setattr(spfpl_slice, "st", stub)
    # `_t` (helper canonique partagé) seede via le st de _field_inputs -> même stub.
    monkeypatch.setattr(_field_inputs, "st", stub)
    data = spfpl_slice._render_spfpl_cession_cible(
        PREFIX, founder_prenom="Camille", founder_nom="Martin"
    )
    return data, stub


def _session_cession_deux_associes() -> dict[str, object]:
    return {
        f"{PREFIX}_cession_nb_parts_cedees": 60,
        f"{PREFIX}_cession_prix_unitaire": "1000",
        f"{PREFIX}_cible_forme_complete": "societe d'exercice liberal a responsabilite limitee",
        f"{PREFIX}_cible_siege_cession": "12 avenue des Ternes, 75017 Paris",
        f"{PREFIX}_cession_nb_associes": 2,
        f"{PREFIX}_cession_assoc_0_civ": "Docteur",
        f"{PREFIX}_cession_assoc_0_prenom": "Camille",
        f"{PREFIX}_cession_assoc_0_nom": "Martin",
        f"{PREFIX}_cession_assoc_0_avant": 70,
        f"{PREFIX}_cession_assoc_1_civ": "Docteur",
        f"{PREFIX}_cession_assoc_1_prenom": "Louise",
        f"{PREFIX}_cession_assoc_1_nom": "Bernard",
        f"{PREFIX}_cession_assoc_1_avant": 30,
    }


def test_render_cession_cible_derive_sans_saisie_manuelle(monkeypatch) -> None:
    # Le sous-formulaire ne rend PLUS les champs « plage cédée », « parts après » ni
    # « plage » par associé ; les valeurs sont DÉRIVÉES dans le cession_data retourné
    # (mêmes clés payload qu'avant -> générateurs inchangés).
    data, stub = _stub_render_cession(_session_cession_deux_associes(), monkeypatch)

    assert f"{PREFIX}_cession_plage_cedee" not in stub.widget_keys
    assert f"{PREFIX}_cession_assoc_0_apres" not in stub.widget_keys
    assert f"{PREFIX}_cession_assoc_0_plage" not in stub.widget_keys
    assert f"{PREFIX}_cession_assoc_0_avant" in stub.widget_keys  # la saisie qui reste

    assert data["nb_cedees"] == 60
    assert data["plage_cedee"] == "41 à 100"
    associes = data["associes"]
    assert [a["apres"] for a in associes] == [10, 30]
    assert [a["plage"] for a in associes] == ["1 à 10", "11 à 40"]
    # Affichage lecture seule : la répartition dérivée est montrée à l'utilisatrice.
    texte = "\n".join(stub.captions)
    assert "Répartition après cession" in texte
    assert "Docteur Camille Martin (cédant) : 10 part(s), numérotées de 1 à 10" in texte
    assert "Holding acquéreur : 60 part(s) cédée(s), numérotées de 41 à 100" in texte


def test_remove_cession_associe_du_milieu_recale_les_lignes(monkeypatch) -> None:
    # Retrait de l'associé du MILIEU (index 1 sur 3) : la liste se recale et les plages
    # se recalculent au rendu suivant.
    session = _session_cession_deux_associes()
    session[f"{PREFIX}_cession_nb_associes"] = 3
    session[f"{PREFIX}_cession_assoc_2_civ"] = "Docteur"
    session[f"{PREFIX}_cession_assoc_2_prenom"] = "Paul"
    session[f"{PREFIX}_cession_assoc_2_nom"] = "Durand"
    session[f"{PREFIX}_cession_assoc_2_avant"] = 50

    stub = _StScmStub(session)
    monkeypatch.setattr(spfpl_slice, "st", stub)
    spfpl_slice._remove_cession_associe(PREFIX, 1)  # retire Louise (milieu)

    assert session[f"{PREFIX}_cession_nb_associes"] == 2
    assert session[f"{PREFIX}_cession_assoc_1_prenom"] == "Paul"
    assert session[f"{PREFIX}_cession_assoc_1_avant"] == 50
    assert f"{PREFIX}_cession_assoc_2_prenom" not in session

    data, _stub = _stub_render_cession(session, monkeypatch)
    associes = data["associes"]
    assert [(a["prenom"], a["avant"]) for a in associes] == [("Camille", 70), ("Paul", 50)]
    # Plages recalculées : Camille (cédant) 70-60=10 -> 1 à 10 ; Paul 50 -> 11 à 60 ;
    # holding 60 -> 61 à 120.
    assert [a["plage"] for a in associes] == ["1 à 10", "11 à 60"]
    assert data["plage_cedee"] == "61 à 120"


def test_remove_cession_associe_plancher_un(monkeypatch) -> None:
    session = _session_cession_deux_associes()
    session[f"{PREFIX}_cession_nb_associes"] = 1
    stub = _StScmStub(session)
    monkeypatch.setattr(spfpl_slice, "st", stub)
    spfpl_slice._remove_cession_associe(PREFIX, 0)  # plancher : no-op
    assert session[f"{PREFIX}_cession_nb_associes"] == 1
    assert session[f"{PREFIX}_cession_assoc_0_prenom"] == "Camille"


# ------------------------------------ équivalence BYTE : dérivé == saisie manuelle


def test_bundle_cession_identique_saisie_derivee_vs_manuelle(
    tmp_path: Path, monkeypatch
) -> None:
    # Le bundle SPFPL cession généré depuis la saisie DÉRIVÉE (render stub, parts avant
    # uniquement) est identique, document par document, au bundle d'une saisie MANUELLE
    # équivalente (mêmes plages posées à la main dans cession_data).
    data, _stub = _stub_render_cession(_session_cession_deux_associes(), monkeypatch)

    payload_derive = _spfpl_payload("SPFPL cession")
    payload_derive["cession_data"] = data

    payload_manuel = _spfpl_payload("SPFPL cession")
    payload_manuel["cession_data"] = {
        **payload_manuel["cession_data"],
        "plage_cedee": "41 à 100",
        "associes": [
            {
                "civilite": "Docteur", "prenom": "Camille", "nom": "Martin",
                "avant": 70, "apres": 10, "plage": "1 à 10",
            },
            {
                "civilite": "Docteur", "prenom": "Louise", "nom": "Bernard",
                "avant": 30, "apres": 30, "plage": "11 à 40",
            },
        ],
    }

    genere_derive = spfpl_slice.generate_dossier(payload_derive, tmp_path / "derive")
    genere_manuel = spfpl_slice.generate_dossier(payload_manuel, tmp_path / "manuel")

    textes_derive = {p.name: _docx_text(p) for p in genere_derive.docx_paths}
    textes_manuel = {p.name: _docx_text(p) for p in genere_manuel.docx_paths}
    assert set(textes_derive) == set(textes_manuel)
    for name, texte in textes_manuel.items():
        assert textes_derive[name] == texte, f"divergence saisie dérivée vs manuelle : {name}"
    # Preuve que les plages dérivées figurent bien dans les documents de cession.
    pv = next(t for n, t in textes_derive.items() if "agrement" in n)
    assert "numérotées de 41 à 100 inclus" in pv


# ----------------------------------------------- composant partagé (repeater civil)


def test_remove_associe_at_repeater_milieu(monkeypatch) -> None:
    # Composant PARTAGÉ (SCI / SCI IRIS / SCS / SCM / SELAS via civil) : retrait au
    # choix, les lignes suivantes remontent, le compteur décrémente, la dernière ligne
    # est purgée.
    from sydel_doc_engine.front_app import associe_repeater as repeater

    session: dict[str, object] = {
        "sci_nb_associes": 3,
        "sci_associe_0_prenom": "Jean",
        "sci_associe_0_nb_titres": 40,
        "sci_associe_1_prenom": "Alice",
        "sci_associe_1_nb_titres": 35,
        "sci_associe_2_prenom": "Paul",
        "sci_associe_2_nb_titres": 25,
    }
    monkeypatch.setattr(repeater, "st", _StScmStub(session))
    config = repeater.RepeaterConfig(key_prefix="sci")
    repeater._remove_associe_at(config, 1)  # retire Alice (milieu)

    assert session["sci_nb_associes"] == 2
    assert session["sci_associe_0_prenom"] == "Jean"
    assert session["sci_associe_1_prenom"] == "Paul"
    assert session["sci_associe_1_nb_titres"] == 25
    assert "sci_associe_2_prenom" not in session

    # Plancher nb_min : plus de retrait sous le minimum.
    repeater._remove_associe_at(
        repeater.RepeaterConfig(key_prefix="sci", nb_min=2), 0
    )
    assert session["sci_nb_associes"] == 2


# ------------------------------- propagation : SELAS multi / SELARL membres (par ligne)


def test_remove_selas_associe_du_milieu_recale_les_lignes(monkeypatch) -> None:
    # Propagation du retour 2 au repeater SELAS multi (bouton par ligne, plancher
    # SELAS_NB_MIN=2) : la ligne du milieu disparaît, les suivantes remontent d'un cran.
    from sydel_doc_engine.front_app import selas_multi_slice

    session: dict[str, object] = {
        "selas_nb_associes": 3,
        "selas_associe_0_nom": "Martin",
        "selas_associe_0_nb_actions": 60,
        "selas_associe_1_nom": "Bernard",
        "selas_associe_1_nb_actions": 25,
        "selas_associe_1_is_dirigeant": True,
        "selas_associe_2_nom": "Durand",
        "selas_associe_2_nb_actions": 15,
    }
    monkeypatch.setattr(selas_multi_slice, "st", _StScmStub(session))
    selas_multi_slice._remove_selas_associe_at(1)  # retire Bernard (milieu)

    assert session["selas_nb_associes"] == 2
    assert session["selas_associe_0_nom"] == "Martin"
    assert session["selas_associe_1_nom"] == "Durand"
    assert session["selas_associe_1_nb_actions"] == 15
    # La ligne remplacée est ENTIÈREMENT remplacée : pas de flag dirigeant orphelin.
    assert "selas_associe_1_is_dirigeant" not in session
    assert "selas_associe_2_nom" not in session

    # Plancher SELAS_NB_MIN (2 associés, minimum de la pluripersonnelle) : no-op.
    selas_multi_slice._remove_selas_associe_at(0)
    assert session["selas_nb_associes"] == 2
    assert session["selas_associe_0_nom"] == "Martin"


def test_remove_selarl_membre_du_milieu_recale_les_lignes(monkeypatch) -> None:
    # Propagation du retour 2 aux membres additionnels SELARL (bouton par ligne,
    # plancher 1 membre) — lignes hétérogènes physique/morale recopiées en bloc.
    from sydel_doc_engine.front_app import shell

    session: dict[str, object] = {
        "selarl_membres_count": 3,
        "selarl_membre_0_nb_parts": 30,
        "selarl_membre_0_prenom": "Alice",
        "selarl_membre_1_nb_parts": 20,
        "selarl_membre_1_prenom": "Bruno",
        "selarl_membre_2_nb_parts": 10,
        "selarl_membre_2_denomination": "SELARL X",  # personne morale
    }
    monkeypatch.setattr(shell, "st", _StScmStub(session))
    shell._remove_selarl_membre_at(1)  # retire Bruno (milieu)

    assert session["selarl_membres_count"] == 2
    assert session["selarl_membre_0_nb_parts"] == 30
    assert session["selarl_membre_1_nb_parts"] == 10
    assert session["selarl_membre_1_denomination"] == "SELARL X"
    assert "selarl_membre_1_prenom" not in session  # aucun champ orphelin de Bruno
    assert "selarl_membre_2_nb_parts" not in session

    shell._remove_selarl_membre_at(0)  # 2 -> 1 : la morale remonte en tête
    assert session["selarl_membres_count"] == 1
    assert session["selarl_membre_0_denomination"] == "SELARL X"

    shell._remove_selarl_membre_at(0)  # plancher 1 membre additionnel : no-op
    assert session["selarl_membres_count"] == 1
    assert session["selarl_membre_0_denomination"] == "SELARL X"


# --------------------------- propagation : plage apportée SPFPL (apport-only, retour 3)


def test_plan_cession_pret_sans_plage_apportee() -> None:
    # Verbatim Albane : « je ne vois pas la possibilité de retirer la plage ??? » —
    # en CESSION aucun document du bundle ne consomme `apport_plage` (le PV/acte
    # rendent la plage CÉDÉE dérivée) -> le plan est prêt SANS cette saisie.
    payload = _spfpl_payload("SPFPL cession")
    payload.pop("apport_plage")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert plan.blockers == ()


def test_plan_apport_plage_manquante_ne_bloque_plus() -> None:
    # KAN-2 (Rafael 2026-07-13) : la plage apportee est un champ TEXTE rendu verbatim
    # ([plage_parts_apportees] / [plage_parts_cedees]) -> son absence ne BLOQUE plus la
    # generation (elle sort en « (À COMPLÉTER : …) », a completer a la main) ; elle passe en
    # AVERTISSEMENT. Seuls les manques STRUCTURELS / NUMERIQUES restent bloquants.
    payload = _spfpl_payload("SPFPL apport")
    payload.pop("apport_plage")
    plan = spfpl_slice.build_spfpl_plan(payload)
    assert plan.can_generate is True
    assert "Plage de parts apportees requise." not in plan.blockers


# --------------------------------------------------- session réelle (AppTest)


def test_apptest_spfpl_retrait_associe_du_milieu(tmp_path: Path, monkeypatch) -> None:
    """Preuve en session Streamlit RÉELLE : le bouton « Retirer cet associé » d'une
    ligne du MILIEU recale les lignes suivantes (recopie des clés de widgets + compteur
    number_input décrémenté depuis un callback on_click) et les anciens champs manuels
    (plage cédée / parts après / plage) ne sont plus rendus."""
    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app import shell

    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui-spfpl-remove")
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SPFPL dentistes — cession")
    app = app.run(timeout=180)
    next(b for b in app.button if "test_data" in str(b.key)).click()
    app = app.run(timeout=180)

    # Les champs manuels retirés (retour Albane 2026-07-07) ne sont plus rendus.
    text_keys = {str(w.key) for w in app.text_input}
    assert "spfpl_cession_cession_plage_cedee" not in text_keys
    assert "spfpl_cession_cession_assoc_0_plage" not in text_keys
    number_keys = {str(w.key) for w in app.number_input}
    assert "spfpl_cession_cession_assoc_0_apres" not in number_keys
    assert "spfpl_cession_cession_assoc_0_avant" in number_keys

    # Passer la répartition à 3 associés et remplir les lignes 1 et 2.
    next(
        w for w in app.number_input if str(w.key) == "spfpl_cession_cession_nb_associes"
    ).set_value(3)
    app = app.run(timeout=180)

    def set_text(key: str, value: str) -> None:
        next(w for w in app.text_input if str(w.key) == key).set_value(value)

    def set_number(key: str, value: int) -> None:
        next(w for w in app.number_input if str(w.key) == key).set_value(value)

    set_text("spfpl_cession_cession_assoc_1_prenom", "Louise")
    set_text("spfpl_cession_cession_assoc_1_nom", "Bernard")
    set_number("spfpl_cession_cession_assoc_1_avant", 30)
    set_text("spfpl_cession_cession_assoc_2_prenom", "Paul")
    set_text("spfpl_cession_cession_assoc_2_nom", "Durand")
    set_number("spfpl_cession_cession_assoc_2_avant", 50)
    app = app.run(timeout=180)

    # Retirer la ligne du MILIEU (index 1 : Louise).
    next(
        b for b in app.button if str(b.key) == "spfpl_cession_cession_remove_assoc_1"
    ).click()
    app = app.run(timeout=180)

    assert app.session_state["spfpl_cession_cession_nb_associes"] == 2
    assert app.session_state["spfpl_cession_cession_assoc_0_prenom"] == "Camille"
    assert app.session_state["spfpl_cession_cession_assoc_1_prenom"] == "Paul"
    assert app.session_state["spfpl_cession_cession_assoc_1_nom"] == "Durand"
    assert app.session_state["spfpl_cession_cession_assoc_1_avant"] == 50
    assert "spfpl_cession_cession_assoc_2_prenom" not in [
        str(w.key) for w in app.text_input
    ]


def test_apptest_selas_retrait_associe_du_milieu() -> None:
    """Propagation SELAS multi en session RÉELLE : 3 associés, retrait du MILIEU via le
    bouton par ligne -> les lignes suivantes remontent, l'ancien bouton global a disparu."""
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SELAS pluripersonnelle")
    app = app.run(timeout=180)

    # L'ancien bouton global « Retirer un associe » (dernier seulement) a disparu.
    button_keys = {str(b.key) for b in app.button}
    assert "selas_remove" not in button_keys
    assert "selas_remove_associe_0" in button_keys

    def set_number(key: str, value: int) -> None:
        next(w for w in app.number_input if str(w.key) == key).set_value(value)

    def set_text(key: str, value: str) -> None:
        next(w for w in app.text_input if str(w.key) == key).set_value(value)

    set_text("selas_associe_0_nom", "Martin")
    set_number("selas_associe_0_nb_actions", 60)
    set_text("selas_associe_1_nom", "Bernard")
    set_number("selas_associe_1_nb_actions", 25)
    app = app.run(timeout=180)
    next(b for b in app.button if str(b.key) == "selas_add").click()
    app = app.run(timeout=180)
    set_text("selas_associe_2_nom", "Durand")
    set_number("selas_associe_2_nb_actions", 15)
    app = app.run(timeout=180)

    # Retirer la ligne du MILIEU (index 1 : Bernard).
    next(b for b in app.button if str(b.key) == "selas_remove_associe_1").click()
    app = app.run(timeout=180)

    assert app.session_state["selas_nb_associes"] == 2
    assert app.session_state["selas_associe_0_nom"] == "Martin"
    assert app.session_state["selas_associe_0_nb_actions"] == 60
    assert app.session_state["selas_associe_1_nom"] == "Durand"
    assert app.session_state["selas_associe_1_nb_actions"] == 15
    assert "selas_associe_2_nom" not in [str(w.key) for w in app.text_input]
    # Plancher SELAS_NB_MIN (2) : les boutons de retrait restants sont désactivés.
    assert all(
        b.disabled for b in app.button if str(b.key).startswith("selas_remove_associe_")
    )


def test_apptest_selarl_membres_retrait_du_milieu() -> None:
    """Propagation SELARL membres additionnels en session RÉELLE : 3 membres, retrait du
    MILIEU via le bouton par ligne -> lignes recalées, bouton global disparu."""
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SELARL")
    app = app.run(timeout=180)
    # Passer en mode multi-associes : decocher « Dossier unipersonnel » (defaut coche).
    next(w for w in app.checkbox if str(w.key) == "selarl_dossier_unipersonnel").set_value(False)
    app = app.run(timeout=180)

    button_keys = {str(b.key) for b in app.button}
    assert "selarl_membres_remove" not in button_keys  # ancien bouton global disparu
    assert "selarl_membres_remove_0" in button_keys

    # Passer à 3 membres additionnels (2 clics « Ajouter »).
    next(b for b in app.button if str(b.key) == "selarl_membres_add").click()
    app = app.run(timeout=180)
    next(b for b in app.button if str(b.key) == "selarl_membres_add").click()
    app = app.run(timeout=180)

    def set_number(key: str, value: int) -> None:
        next(w for w in app.number_input if str(w.key) == key).set_value(value)

    set_number("selarl_membre_0_nb_parts", 30)
    set_number("selarl_membre_1_nb_parts", 20)
    set_number("selarl_membre_2_nb_parts", 10)
    app = app.run(timeout=180)

    # Retirer la ligne du MILIEU (index 1).
    next(b for b in app.button if str(b.key) == "selarl_membres_remove_1").click()
    app = app.run(timeout=180)

    assert app.session_state["selarl_membres_count"] == 2
    assert app.session_state["selarl_membre_0_nb_parts"] == 30
    assert app.session_state["selarl_membre_1_nb_parts"] == 10
    assert "selarl_membre_2_nb_parts" not in [str(w.key) for w in app.number_input]


def test_apptest_spfpl_plage_apportee_cession_absente_apport_presente() -> None:
    """Retour 3 propagé (section Dépôt/titres) : en CESSION le champ « Plage de parts »
    n'est plus rendu et le plan prérempli reste prêt sans lui ; en APPORT il reste rendu
    (DOC-041 + statuts d'apport le consomment)."""
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SPFPL dentistes — cession")
    app = app.run(timeout=180)
    next(b for b in app.button if "test_data" in str(b.key)).click()
    app = app.run(timeout=180)

    # CESSION : champ absent, et le dossier prérempli (sans plage apportée) est prêt.
    assert "spfpl_cession_apport_plage" not in {str(w.key) for w in app.text_input}
    generate_button = next(
        b for b in app.button if str(b.key) == "clean_typed_generate_dossier"
    )
    assert generate_button.disabled is False
    assert not any("Blocage" in item.value for item in app.caption)

    # APPORT : le champ reste saisi (consommé par le contrat d'apport + statuts).
    app.selectbox(key="clean_dossier_type").set_value("SPFPL dentistes — apport")
    app = app.run(timeout=180)
    assert "spfpl_apport_apport_plage" in {str(w.key) for w in app.text_input}
