"""Slice front SELAS multi-associes (DOC-044), patron SELARL.

SELAS multi = SEL d'exercice par actions, 2 a 5 associes exercants/non exercants
(personne physique + personne morale), vocabulaire ACTIONS. Contexte moteur
mirroir du builder de test `test_lot_04_statuts_selas_multi`. Reutilise le
repeater generique en mode "exercice" (actions + qualite capital + ordre).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from unicodedata import combining, normalize

import streamlit as st

from sydel_doc_engine.app.ui_runtime import (
    GeneratedDossier,
    generate_docx_files_for_document_codes,
    generate_zip_file,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    Associe,
    CapitalContext,
    Company,
    DecisionContext,
    DirigeantNomine,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    Person,
    RegimeCommunautaire,
    RegimeCommunautaireAssocie,
    RegimeCommunautaireAvertissement,
    RegimeCommunautaireRenonciation,
    ReunionContext,
    ReunionPresident,
    Signature,
    StatutsCivilsAssocie,
    StatutsSelasMultiContext,
    StatutsSelasMultiPresident,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    calculate_nominal_value,
    date_to_french_words,
    derive_gender_from_civilite,
    format_french_date,
    number_words_from_value,
    parse_french_date,
)
from sydel_doc_engine.generators.lot_02.lettre_avertissement_conjoint import (
    LettreAvertissementConjointGenerator,
)
from sydel_doc_engine.generators.lot_02.lettre_renonciation_associe import (
    LettreRenonciationAssocieGenerator,
)

STRUCTURE = "SELAS"
DOC_CODE = "DOC-044"
PREFIX = "selas"

# Bornes du repeater SELAS (A1 : nommees, AUCUN changement de valeur). Alignees
# sur le generateur statuts_selas_multi (2 a 5 associes exercants / non exercants).
SELAS_NB_MIN = 2
SELAS_NB_MAX = 6

# Professions reglementees proposees au menu (retours Rafael 2026-06-18, R1) :
# l'operateur ne tape plus la profession ni son pluriel ; il choisit dans une
# liste fermee et le pluriel est derive automatiquement. Le moteur bascule sur
# le corpus dentiste des que la profession contient « dentiste » (cf.
# statuts_selas_multi._select_profile), donc « chirurgien-dentiste » -> corpus
# dentiste, « médecin » -> corpus medecin.
_PROFESSION_PLURIELS: dict[str, str] = {
    "chirurgien-dentiste": "chirurgiens-dentistes",
    "médecin": "médecins",
}
_PROFESSION_OPTIONS: tuple[str, ...] = tuple(_PROFESSION_PLURIELS)

# Profession pre-reglee par cle de type enregistre. La SELAS « multi » generique
# n'a pas de pre-reglage (defaut = 1re option, medecin). La SELAS « dentiste
# pluripersonnelle » pre-selectionne « chirurgien-dentiste ». Cle absente =
# aucun pre-reglage.
_PROFESSION_DEFAULTS_BY_TYPE: dict[str, str] = {
    "selas_dentiste_pluri_v1": "chirurgien-dentiste",
}


def _profession_choice_key() -> str:
    return f"{PREFIX}_profession_choice"


def _apply_type_profession_default(type_key: str) -> None:
    """Pre-selectionne la profession au menu selon la cle de type.

    N'ecrase JAMAIS un choix existant : ne pose le defaut que si le selectbox
    n'a pas encore de valeur en session, pour que l'operateur reste libre de
    corriger. Sans entree pour la cle, ne fait rien (SELAS multi generique :
    defaut = 1re option du menu)."""
    default = _PROFESSION_DEFAULTS_BY_TYPE.get(type_key)
    if not default:
        return
    choice_key = _profession_choice_key()
    if choice_key not in st.session_state:
        st.session_state[choice_key] = default


def _render_profession_selectbox(container) -> tuple[str, str]:
    """Menu deroulant « Profession » (R1). Retourne (singulier, pluriel derive).

    Le pluriel n'est plus saisi : il est derive du choix via _PROFESSION_PLURIELS.
    Le defaut pre-regle par _apply_type_profession_default (cas dentiste) est
    respecte car il a deja ecrit la cle de session avant le rendu."""
    choice_key = _profession_choice_key()
    profession = container.selectbox(
        "Profession",
        _PROFESSION_OPTIONS,
        key=choice_key,
    )
    pluriel = _PROFESSION_PLURIELS.get(profession, "")
    return profession, pluriel

# Bundle de creation SELAS multi (canon) : statuts multi-associes + tronc commun
# (DNC / domiciliation / procuration) + PV nomination gerant + demande
# d'inscription a l'ordre. Le signataire / gerant des documents communs = le
# premier associe physique (designe president par defaut).
SELAS_BUNDLE_CODES: tuple[str, ...] = (
    DOC_CODE,
    *cc.TRONC_COMMUN_CODES,
    cc.DOC_PV_NOMINATION_GERANT,
    cc.DOC_DEMANDE_INSCRIPTION_ORDRE,
)


def _associes_maries_communaute(
    payload: dict[str, object],
) -> list[StatutsCivilsAssocie]:
    """Associes personne physique maries sous regime communautaire (R7).

    Lit le bloc per-associe `regime_communautaire_associe.actif`. Ordre du
    formulaire preserve (le 1er married pilote le DOC-005/006 unique tant que le
    moteur n'emet pas par personne)."""
    result: list[StatutsCivilsAssocie] = []
    for associe in payload.get("associes") or []:
        if not isinstance(associe, StatutsCivilsAssocie):
            continue
        if associe.type_personne != "personne_physique":
            continue
        regime = associe.regime_communautaire_associe
        if regime is not None and regime.actif:
            result.append(associe)
    return result


def _regime_communautaire_actif(payload: dict[str, object]) -> bool:
    """Regime communautaire actif au sens generation : toggle global historique
    OU au moins un associe physique marie sous communaute (R7). Conserve le
    comportement existant (toggle global) tout en activant le nouveau chemin
    per-associe."""
    return bool(payload.get("regime_communautaire")) or bool(
        _associes_maries_communaute(payload)
    )


def _selas_document_codes(payload: dict[str, object]) -> tuple[str, ...]:
    """Bundle SELAS de creation, augmente du conditionnel canon « Si regime
    communautaire » (DOC-005 renonciation + DOC-006 avertissement) quand le
    regime est actif (toggle global OU au moins un associe physique marie sous
    communaute, R7). Inactif -> bundle de base inchange.

    Codes de PLAN (ce qui SERA produit, pour l'affichage / les assertions). La
    repartition de fait entre l'orchestrateur generique et la boucle par-associe
    (R7) est portee par `_orchestrator_codes` / `generate_dossier` : ici on
    declare simplement que DOC-005/006 font partie du livrable des que le regime
    est actif, quelle que soit la voie d'emission."""
    codes = list(SELAS_BUNDLE_CODES)
    if _regime_communautaire_actif(payload):
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    return tuple(codes)


def _orchestrator_codes(payload: dict[str, object]) -> tuple[str, ...]:
    """Codes confies a l'orchestrateur generique (1 doc_id -> 1 fichier de nom
    fixe).

    Le tronc de creation y passe toujours. DOC-005/006 n'y passent QUE par la
    voie historique du « toggle global » (un seul couple, nom de fichier fixe,
    byte-identique). Des qu'au moins un associe physique est marie sous
    communaute via le bloc PAR associe (R7) et que le toggle global est inactif,
    DOC-005/006 sont RETIRES de l'orchestrateur : ils sont generes par
    `generate_dossier` une fois PAR associe marie, avec des noms de fichiers
    distincts (l'orchestrateur ne sait emettre qu'un fichier de nom fixe par
    code, ce qui ecraserait les couples successifs)."""
    codes = list(SELAS_BUNDLE_CODES)
    if bool(payload.get("regime_communautaire")):
        # Toggle global : chemin historique inchange (un couple, nom fixe).
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    # Sinon (chemin per-associe), DOC-005/006 sont emis hors orchestrateur.
    return tuple(codes)


@dataclass(frozen=True)
class SelasSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.selas_multi_slice"


def _count_key() -> str:
    return f"{PREFIX}_nb_associes"


def _associe_count() -> int:
    raw = st.session_state.get(_count_key(), SELAS_NB_MIN)
    try:
        return max(SELAS_NB_MIN, min(SELAS_NB_MAX, int(raw)))
    except (TypeError, ValueError):
        return SELAS_NB_MIN


def render_selas_form(type_key: str = "selas_multi_v1") -> dict[str, object]:
    # Cas nomme « SELAS dentiste pluripersonnelle » : pre-regle la profession sur
    # « chirurgien-dentiste » (le moteur basculera sur le corpus dentiste). Pour
    # la SELAS multi generique, aucun pre-reglage (profession libre).
    _apply_type_profession_default(type_key)
    st.subheader("Donnees a saisir")
    st.markdown("**Societe (SELAS d'exercice, vocabulaire actions)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    siege = _t(col_b, "siege", "Siege (adresse affichee)")
    col_c, _ = st.columns(2)
    # R1 (retours Rafael 2026-06-18) : profession en menu deroulant ferme ; le
    # pluriel n'est plus saisi mais derive automatiquement du choix.
    profession, profession_pluriel = _render_profession_selectbox(col_c)
    col_e, col_f, col_g = st.columns(3)
    capital = _t(col_e, "capital_social", "Capital social")
    nb_actions = _i(col_f, "nb_actions_total", "Nombre total d'actions")
    # Valeur nominale d'une action : TOUJOURS calculee (capital / nb actions),
    # jamais saisie (retours Albane 2026-06-17, SCREEN-2). Champ d'affichage seul.
    valeur_action = calculate_nominal_value(capital, nb_actions)
    col_g.text_input(
        "Valeur nominale d'une action (calculee)",
        value=valeur_action,
        disabled=True,
        key=f"{PREFIX}_valeur_nominale_action_display",
    )
    col_h, col_i = st.columns(2)
    ville_rcs = _t(col_h, "ville_rcs", "RCS (ville)")
    adresse_exercice = _t(col_i, "adresse_lieu_exercice", "Adresse lieu d'exercice")

    st.markdown("Depot des fonds")
    col_j, col_k = st.columns(2)
    banque_nom = _t(col_j, "banque_nom", "Banque")
    banque_adresse = _t(col_k, "banque_adresse", "Adresse banque")
    date_cloture = _t(st, "date_cloture", "Cloture du premier exercice")

    st.caption("Siege social (adresse structuree, pour la domiciliation / procuration)")
    col_sa, col_sb, col_sc, col_sd = st.columns(4)
    siege_num = _t(col_sa, "siege_num", "No")
    siege_voie = _t(col_sb, "siege_voie", "Voie")
    siege_cp = _t(col_sc, "siege_cp", "CP")
    siege_ville = _t(col_sd, "siege_ville", "Ville")

    st.markdown("**Signature**")
    col_l, col_m = st.columns(2)
    signature_lieu = _t(col_l, "signature_lieu", "Lieu de signature")
    with col_m:
        signature_date = _date("signature_date", "Date de signature")

    associes, president_index, dirigeant_sig, dirigeants_nomines = _render_selas_associes()
    common = _render_common_docs_form()

    payload: dict[str, object] = {
        "denomination": denomination,
        "siege": siege,
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "profession_reglementee": profession,
        "profession_reglementee_pluriel": profession_pluriel,
        "capital_social": capital,
        "nb_actions_total": nb_actions,
        "valeur_nominale_action": valeur_action,
        "ville_rcs": ville_rcs,
        "adresse_lieu_exercice": adresse_exercice,
        "banque_nom": banque_nom,
        "banque_adresse": banque_adresse,
        "date_cloture": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "associes": associes,
        "president_index": president_index,
        "dirigeants_nomines": dirigeants_nomines,
    }
    payload.update(common)
    # La DNC / l'identite du dirigeant (saisies sous l'associe coche) alimentent
    # les cles signataire_* lues par build_generation_context.
    payload.update(dirigeant_sig)
    return payload


def _render_common_docs_form() -> dict[str, object]:
    """Documents communs NON lies a l'identite du dirigeant.

    La filiation + l'adresse personnelle + la date de naissance du dirigeant
    (declaration de non-condamnation, procuration) sont desormais saisies SOUS
    l'associe coche « Dirigeant » (reunion 2026-06-09 : champs conditionnels au
    dirigeant). Ce bloc ne garde que ce qui n'appartient pas a un associe : date
    de decision (PV), ordre professionnel, regime communautaire.
    """
    st.markdown("**Documents communs (decision, ordre professionnel)**")
    decision_date = _date("decision_date", "Date de decision (PV gerant)")
    st.markdown("Ordre professionnel (demande d'inscription)")
    # R5 (retours Rafael 2026-06-18) : « Conseil departemental » supprime du
    # formulaire (inutile) ; le libelle est derive automatiquement cote moteur.
    # R6 : connecteur grammatical (« de » / « du ») a cote du departement, pour
    # gerer l'accord (« ... de Gironde » / « ... du Jura »).
    col_i, col_j = st.columns(2)
    ordre_dep = _t(col_i, "ordre_departement", "Departement ordre")
    ordre_connecteur = _render_connecteur_selectbox(col_j)
    col_k, col_l, col_m = st.columns(3)
    ordre_ligne = _t(col_k, "ordre_adresse_ligne_1", "Adresse ordre")
    ordre_cp = _t(col_l, "ordre_cp", "CP ordre")
    ordre_ville = _t(col_m, "ordre_ville", "Ville ordre")
    ordre_numero = _t(st, "ordre_numero", "Numero d'inscription")
    regime = _render_regime_communautaire_form()
    common = {
        "decision_date": decision_date,
        "ordre_departement": ordre_dep,
        "ordre_connecteur": ordre_connecteur,
        "ordre_adresse_ligne_1": ordre_ligne,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
        "ordre_numero": ordre_numero,
    }
    common.update(regime)
    return common


def _render_connecteur_selectbox(container) -> str:
    """Menu « de » / « du » (R6) : connecteur grammatical place avant le
    departement de l'ordre dans le libelle derive (gestion de l'accord)."""
    return str(
        container.selectbox(
            "Connecteur (de / du)",
            ("de", "du"),
            key=f"{PREFIX}_ordre_connecteur",
            help="S'affiche avant le departement : « ... de Gironde » / « ... du Jura ».",
        )
    )


def _render_regime_communautaire_form() -> dict[str, object]:
    """Conditionnel canon « Si regime communautaire » (DOC-005 + DOC-006).

    Toggle + saisies conjoint requises par les generateurs de renonciation et
    d'avertissement. Inactif -> aucun document ajoute, bundle de base inchange.
    """
    regime_key = f"{PREFIX}_regime_communautaire"
    if regime_key not in st.session_state:
        st.session_state[regime_key] = False
    actif = st.checkbox(
        "Regime communautaire (ajoute lettre de renonciation + avertissement au conjoint)",
        key=regime_key,
    )
    if not actif:
        return {"regime_communautaire": False}
    st.caption("Conjoint (lettres de renonciation / avertissement)")
    col_a, col_b, col_c = st.columns(3)
    conjoint_civilite = col_a.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key=f"{PREFIX}_conjoint_civilite",
    )
    conjoint_prenom = _t(col_b, "conjoint_prenom", "Prenom conjoint")
    conjoint_nom = _t(col_c, "conjoint_nom", "Nom conjoint")
    regime_matrimonial = _t(st, "regime_matrimonial", "Regime matrimonial")
    return {
        "regime_communautaire": True,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_genre": derive_gender_from_civilite(conjoint_civilite),
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "regime_matrimonial": regime_matrimonial,
    }


def _render_selas_associes() -> tuple[
    list[StatutsCivilsAssocie], int, dict[str, object], list[dict[str, object]]
]:
    if _count_key() not in st.session_state:
        st.session_state[_count_key()] = SELAS_NB_MIN
    nombre = _associe_count()
    st.markdown(
        f"**Associes ({nombre})** — {SELAS_NB_MIN} a {SELAS_NB_MAX}, exercants / non exercants"
    )
    cols = st.columns([1, 1, 3])
    if cols[0].button("Ajouter un associe", key=f"{PREFIX}_add"):
        st.session_state[_count_key()] = min(SELAS_NB_MAX, nombre + 1)
        st.rerun()
    if cols[1].button("Retirer un associe", key=f"{PREFIX}_remove"):
        st.session_state[_count_key()] = max(SELAS_NB_MIN, nombre - 1)
        st.rerun()
    cols[2].caption(
        "Cochez le(s) dirigeant(s) sur un associe (President et/ou Directeur General) ; "
        "a defaut, le premier associe physique est president."
    )

    associes: list[StatutsCivilsAssocie] = []
    for index in range(nombre):
        associes.append(_render_one_associe(index))
    president_index = _derive_president_index(associes)
    dirigeant_sig = _collect_dirigeant_sig(associes, president_index)
    dirigeants_nomines = _build_dirigeants_nomines_payload(associes, president_index)
    return associes, president_index, dirigeant_sig, dirigeants_nomines


def _build_dirigeants_nomines_payload(
    associes: list[StatutsCivilsAssocie], president_index: int
) -> list[dict[str, object]]:
    """Charge utile serialisable des dirigeants nommes pour le PV (President + DG).

    Une entree par dirigeant physique coche, dans l'ordre PV (President d'abord).
    Chaque entree porte de quoi reconstruire un `DirigeantNomine` cote
    `build_generation_context`, sans dependre du session_state Streamlit.
    """
    payload: list[dict[str, object]] = []
    for index, role in _collect_dirigeants_nomines_indices(associes, president_index):
        associe = associes[index]
        prefix = f"{PREFIX}_associe_{index}"
        raw_date = st.session_state.get(f"{prefix}_sig_date_naissance")
        payload.append(
            {
                "ref_associe_index": index,
                "fonction_affichage": role,
                "civilite_affichage": associe.civilite_affichage or "Monsieur",
                "prenom": associe.prenom or associe.prenoms or "",
                "nom": associe.nom or "",
                "genre": associe.genre or Gender.MASCULIN,
                # Date de naissance ISO (saisie sous la case Dirigeant) pour la
                # phrase d'identite du PV ; fallback sur la date « en lettres ».
                "date_naissance_iso": parse_french_date(raw_date),
                "date_naissance_affichee": associe.date_naissance,
                "ville_naissance": associe.ville_naissance,
                "departement_naissance": associe.departement_naissance,
                "nationalite": associe.nationalite,
                # Adresse personnelle structuree (saisie sous la case Dirigeant).
                "adresse_num": str(st.session_state.get(f"{prefix}_sig_adresse_num") or ""),
                "adresse_voie": str(st.session_state.get(f"{prefix}_sig_adresse_voie") or ""),
                "adresse_cp": str(st.session_state.get(f"{prefix}_sig_adresse_cp") or ""),
                "adresse_ville": str(st.session_state.get(f"{prefix}_sig_adresse_ville") or ""),
                "adresse_personnelle_affichee": associe.adresse_personnelle_affichee,
            }
        )
    return payload


def _render_one_associe(index: int) -> StatutsCivilsAssocie:
    prefix = f"{PREFIX}_associe_{index}"
    with st.expander(f"Associe {index + 1}", expanded=index == 0):
        type_key = f"{prefix}_type"
        if type_key not in st.session_state:
            st.session_state[type_key] = "personne_physique"
        type_personne = st.selectbox(
            "Type d'associe",
            ("personne_physique", "personne_morale"),
            key=type_key,
        )
        col_a, col_b = st.columns(2)
        nb_actions = _is(col_a, f"{prefix}_nb_actions", "Nombre d'actions")
        montant = _ts(col_b, f"{prefix}_montant", "Apport (montant)")
        if type_personne == "personne_morale":
            # Une personne morale ne peut pas etre president (contrainte moteur) :
            # aucune case dirigeant. Un flag residuel est ignore a la derivation.
            return _morale(prefix, nb_actions, montant)
        _render_dirigeant_choice(prefix, index)
        return _physique(prefix, nb_actions, montant)


def _render_dirigeant_choice(prefix: str, index: int) -> None:
    """Case « Dirigeant » + role + champs complementaires pour un associe physique.

    Le wording « Directeur General » est desormais FOURNI par le modele PV
    nominations dirigeants (Albane 2026-06-17) : le verrou est leve, on propose
    « President » ET « Directeur General » (le « DG delegue » reste hors V1, son
    wording dedie n'etant pas fourni). Le President reste le signataire du tronc
    commun (DNC / procuration / statuts) ; le Directeur General ajoute une
    deuxieme decision de nomination au PV.

    Reunion 2026-06-09 : les champs complementaires (filiation pour la declaration
    de non-condamnation, adresse structuree pour la procuration) ne sont demandes
    QUE pour l'associe coche dirigeant — pas pour les autres associes.
    """
    dirigeant_key = f"{prefix}_is_dirigeant"
    if dirigeant_key not in st.session_state:
        # Defaut historique : le 1er associe (index 0) est dirigeant.
        st.session_state[dirigeant_key] = index == 0
    is_dirigeant = st.checkbox("Dirigeant", key=dirigeant_key)
    if not is_dirigeant:
        return
    role_key = f"{prefix}_role_dirigeant"
    if role_key not in st.session_state:
        st.session_state[role_key] = "Président"
    st.selectbox(
        "Role du dirigeant",
        ("Président", "Directeur Général"),
        key=role_key,
        help="Le Président signe le tronc commun ; le Directeur Général ajoute une décision au PV.",
    )
    st.caption("Declaration de non-condamnation du dirigeant (filiation + adresse personnelle)")
    col_a, col_b = st.columns(2)
    _ts(col_a, f"{prefix}_sig_nom_pere", "Nom du pere")
    _ts(col_b, f"{prefix}_sig_nom_mere", "Nom de la mere")
    # R4 (retours Rafael 2026-06-18) : titre explicite au-dessus des 4 champs
    # structures d'adresse perso (No / Voie / CP / Ville), sinon ambigus.
    st.markdown("**Adresse personnelle**")
    col_c, col_d, col_e, col_f = st.columns(4)
    _ts(col_c, f"{prefix}_sig_adresse_num", "No")
    _ts(col_d, f"{prefix}_sig_adresse_voie", "Voie")
    _ts(col_e, f"{prefix}_sig_adresse_cp", "CP")
    _ts(col_f, f"{prefix}_sig_adresse_ville", "Ville")
    _date(f"associe_{index}_sig_date_naissance", "Date de naissance (JJ/MM/AAAA)")


def _derive_president_index(associes: list[StatutsCivilsAssocie]) -> int:
    """Index du president = associe PHYSIQUE coche « dirigeant » avec role President.

    A defaut (aucun President explicite), retombe sur le premier associe physique
    coche dirigeant, puis sur le premier associe physique — comportement
    historique. Ne renvoie jamais l'index d'une personne morale (le generateur
    leverait : President = physique).
    """
    # 1) Dirigeant physique explicitement « President ».
    for i, associe in enumerate(associes):
        if associe.type_personne != "personne_physique":
            continue
        if not bool(st.session_state.get(f"{PREFIX}_associe_{i}_is_dirigeant")):
            continue
        if _dirigeant_role(i) == "Président":
            return i
    # 2) Premier dirigeant physique coche (role non President -> fallback).
    for i, associe in enumerate(associes):
        if associe.type_personne != "personne_physique":
            continue
        if bool(st.session_state.get(f"{PREFIX}_associe_{i}_is_dirigeant")):
            return i
    # 3) Premier associe physique (historique).
    return next(
        (i for i, a in enumerate(associes) if a.type_personne == "personne_physique"),
        0,
    )


def _dirigeant_role(index: int) -> str:
    return str(st.session_state.get(f"{PREFIX}_associe_{index}_role_dirigeant") or "Président")


def _collect_dirigeants_nomines_indices(
    associes: list[StatutsCivilsAssocie], president_index: int
) -> list[tuple[int, str]]:
    """Liste ordonnee (index associe, role) des dirigeants nommes au PV.

    Le President vient toujours en PREMIERE decision ; les autres dirigeants
    physiques coches (Directeur General) suivent dans l'ordre des associes.
    Ignore les personnes morales (un dirigeant SELAS est une personne physique).
    """
    dirigeants: list[tuple[int, str]] = []
    if 0 <= president_index < len(associes):
        dirigeants.append((president_index, "Président"))
    for i, associe in enumerate(associes):
        if i == president_index:
            continue
        if associe.type_personne != "personne_physique":
            continue
        if not bool(st.session_state.get(f"{PREFIX}_associe_{i}_is_dirigeant")):
            continue
        dirigeants.append((i, _dirigeant_role(i)))
    return dirigeants


def _collect_dirigeant_sig(
    associes: list[StatutsCivilsAssocie], president_index: int
) -> dict[str, object]:
    """Champs « signataire » (DNC / procuration) du dirigeant -> cles signataire_*.

    L'identite (nom, prenom, ville naissance, nationalite) vient de l'associe
    lui-meme (zero sursaisie) ; la filiation + l'adresse structuree + la date ISO
    sont saisies sous la case « Dirigeant ». Mappe vers les cles `signataire_*`
    deja lues par build_generation_context (qui reste donc inchange).
    """
    if not (0 <= president_index < len(associes)):
        return {}
    prefix = f"{PREFIX}_associe_{president_index}"
    dirigeant = associes[president_index]
    raw_date = st.session_state.get(f"{prefix}_sig_date_naissance")
    return {
        "signataire_nom_pere": str(st.session_state.get(f"{prefix}_sig_nom_pere") or ""),
        "signataire_nom_mere": str(st.session_state.get(f"{prefix}_sig_nom_mere") or ""),
        "signataire_adresse_num": str(st.session_state.get(f"{prefix}_sig_adresse_num") or ""),
        "signataire_adresse_voie": str(st.session_state.get(f"{prefix}_sig_adresse_voie") or ""),
        "signataire_adresse_cp": str(st.session_state.get(f"{prefix}_sig_adresse_cp") or ""),
        "signataire_adresse_ville": str(
            st.session_state.get(f"{prefix}_sig_adresse_ville") or ""
        ),
        "signataire_nationalite": str(dirigeant.nationalite or ""),
        "signataire_titre": str(dirigeant.profession or "Docteur"),
        "signataire_date_naissance": parse_french_date(raw_date),
    }


def _physique(prefix: str, nb_actions: int, montant: str) -> StatutsCivilsAssocie:
    col_a, col_b, col_c = st.columns(3)
    civilite = col_a.selectbox(
        "Civilite",
        ("Madame", "Monsieur"),
        key=f"{prefix}_civilite",
    )
    prenoms = _ts(col_b, f"{prefix}_prenoms", "Prenom(s)")
    nom = _ts(col_c, f"{prefix}_nom", "Nom")
    col_d, col_e, col_f = st.columns(3)
    date_naissance = _ts(col_d, f"{prefix}_date_naissance", "Date naissance (ex: 1 janvier 1980)")
    ville_naissance = _ts(col_e, f"{prefix}_ville_naissance", "Ville naissance")
    departement = _ts(col_f, f"{prefix}_departement", "Departement naissance")
    col_g, col_h = st.columns(2)
    nationalite = render_nationalite_selectbox(prefix, container=col_g)
    profession = _ts(col_h, f"{prefix}_profession", "Profession (ex: Docteur)")
    adresse = _ts(st, f"{prefix}_adresse", "Adresse personnelle (affichee)")
    col_i, col_j = st.columns(2)
    situation = _ts(col_i, f"{prefix}_situation", "Situation matrimoniale")
    qualification = _ts(col_j, f"{prefix}_qualification", "Qualification principale")
    col_k, col_l, col_m = st.columns(3)
    ordre_dep = _ts(col_k, f"{prefix}_ordre_dep", "Departement ordre")
    numero_ordre = _ts(col_l, f"{prefix}_numero_ordre", "Numero ordre")
    numero_rpps = _ts(col_m, f"{prefix}_numero_rpps", "Numero RPPS")
    qualite = _ts(st, f"{prefix}_qualite", "Qualite au capital (ex: associee exercante)")
    regime_associe, foyer_address = _render_regime_associe_form(prefix)

    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=derive_gender_from_civilite(civilite),
        civilite_affichage=civilite,
        prenom=prenoms,
        prenoms=prenoms,
        nom=nom,
        date_naissance=date_naissance or None,
        ville_naissance=ville_naissance or None,
        departement_naissance=departement or None,
        nationalite=nationalite or None,
        profession=profession or None,
        situation_maritale=situation or None,
        # R7 : adresse de foyer STRUCTUREE de l'associe marie (avertissement
        # DOC-006). Lue par _associe_signataire_address ; si None (incomplete ou
        # associe non marie), repli historique vers l'adresse du president.
        adresse_personnelle=foyer_address,
        adresse_personnelle_affichee=adresse or None,
        qualification_principale=qualification or None,
        ordre_departemental=ordre_dep or None,
        numero_ordre=numero_ordre or None,
        numero_rpps=numero_rpps or None,
        qualite_capital=qualite or None,
        nb_actions=nb_actions or None,
        nb_actions_lettres=number_words_from_value(nb_actions) if nb_actions else None,
        apport=_apport(montant),
        regime_communautaire_associe=regime_associe,
    )


def _render_regime_associe_form(
    prefix: str,
) -> tuple[RegimeCommunautaireAssocie | None, Address | None]:
    """Regime matrimonial communautaire PAR associe physique (R7).

    Reprend la STRUCTURE SELARL (toggle + regime matrimonial + conjoint), mais
    portee au niveau de l'associe au lieu du toggle global unique. Inactif ->
    (None, None) (associe non concerne).

    Collecte aussi l'adresse de foyer STRUCTUREE (No/Voie/CP/Ville) de CET
    associe : l'avertissement au conjoint (DOC-006) est adresse au domicile du
    foyer. Sans cette saisie structuree, le moteur retombait sur l'adresse du
    president (residu d63393c) ; avec elle, chaque associe marie porte SON foyer.
    Retourne l'`Address` structuree (ou None si incomplete -> repli president)."""
    regime_key = f"{prefix}_regime_communautaire"
    if regime_key not in st.session_state:
        st.session_state[regime_key] = False
    actif = st.checkbox(
        "Marie(e) sous un regime communautaire "
        "(ajoute renonciation + avertissement au conjoint pour cet associe)",
        key=regime_key,
    )
    if not actif:
        return None, None
    st.caption("Conjoint de cet associe (lettres de renonciation / avertissement)")
    col_a, col_b, col_c = st.columns(3)
    conjoint_civilite = col_a.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key=f"{prefix}_conjoint_civilite",
    )
    conjoint_prenom = _ts(col_b, f"{prefix}_conjoint_prenom", "Prenom conjoint")
    conjoint_nom = _ts(col_c, f"{prefix}_conjoint_nom", "Nom conjoint")
    regime_matrimonial = _ts(st, f"{prefix}_regime_matrimonial", "Regime matrimonial")
    st.caption(
        "Adresse du foyer de cet associe (avertissement au conjoint DOC-006). "
        "Si laissee vide, l'adresse du president est utilisee."
    )
    col_d, col_e, col_f, col_g = st.columns(4)
    foyer_num = _ts(col_d, f"{prefix}_foyer_adresse_num", "No")
    foyer_voie = _ts(col_e, f"{prefix}_foyer_adresse_voie", "Voie")
    foyer_cp = _ts(col_f, f"{prefix}_foyer_adresse_cp", "CP")
    foyer_ville = _ts(col_g, f"{prefix}_foyer_adresse_ville", "Ville")
    foyer_address = _foyer_address(foyer_num, foyer_voie, foyer_cp, foyer_ville)
    regime = RegimeCommunautaireAssocie(
        actif=True,
        regime_matrimonial=regime_matrimonial or None,
        conjoint_civilite=conjoint_civilite,
        conjoint_genre=derive_gender_from_civilite(conjoint_civilite),
        conjoint_prenom=conjoint_prenom or None,
        conjoint_nom=conjoint_nom or None,
    )
    return regime, foyer_address


def _foyer_address(num: str, voie: str, cp: str, ville: str) -> Address | None:
    """Adresse de foyer STRUCTUREE par associe (R7) ; None si incomplete.

    L'avertissement DOC-006 exige une adresse complete (num/voie/cp/ville). Si
    l'un des champs manque, on renvoie None pour laisser le repli vers le
    president jouer (jamais de generation bloquee ni d'adresse partielle)."""
    parts = (num.strip(), voie.strip(), cp.strip(), ville.strip())
    if not all(parts):
        return None
    return Address(
        num_voie=num.strip(),
        voie=voie.strip(),
        cp=cp.strip(),
        ville=ville.strip(),
        adresse_affichee=f"{num.strip()} {voie.strip()}, {cp.strip()} {ville.strip()}",
    )


def _morale(prefix: str, nb_actions: int, montant: str) -> StatutsCivilsAssocie:
    from sydel_doc_engine.domain.models import Address, StatutsCivilsRepresentant

    denomination = _ts(st, f"{prefix}_denomination", "Denomination (personne morale)")
    col_a, col_b = st.columns(2)
    forme = _ts(col_a, f"{prefix}_forme", "Forme juridique")
    capital = _ts(col_b, f"{prefix}_capital", "Capital social (affiche)")
    siege = _ts(st, f"{prefix}_siege", "Siege (affiche)")
    col_c, col_d = st.columns(2)
    numero_rcs = _ts(col_c, f"{prefix}_numero_rcs", "Numero RCS")
    ville_rcs = _ts(col_d, f"{prefix}_ville_rcs", "RCS (ville)")
    qualite = _ts(st, f"{prefix}_qualite", "Qualite au capital (ex: associee non exercante)")
    st.markdown("Representant legal")
    col_e, col_f, col_g = st.columns(3)
    rep_civilite = col_e.selectbox(
        "Civilite rep.",
        ("Monsieur", "Madame"),
        key=f"{prefix}_rep_civilite",
    )
    rep_prenom = _ts(col_f, f"{prefix}_rep_prenom", "Prenom rep.")
    rep_nom = _ts(col_g, f"{prefix}_rep_nom", "Nom rep.")

    return StatutsCivilsAssocie(
        type_personne="personne_morale",
        denomination=denomination or None,
        forme_juridique=forme or None,
        capital_social=capital or None,
        siege=Address(adresse_affichee=siege) if siege else None,
        numero_rcs=numero_rcs or None,
        ville_rcs=ville_rcs or None,
        representant=StatutsCivilsRepresentant(
            civilite_affichage=rep_civilite,
            prenom=rep_prenom or None,
            nom=rep_nom or None,
            fonction="gerant",
        ),
        qualite_capital=qualite or None,
        nb_actions=nb_actions or None,
        nb_actions_lettres=number_words_from_value(nb_actions) if nb_actions else None,
        apport=_apport(montant),
    )


def _apport(montant: str):
    from sydel_doc_engine.domain.models import StatutsCivilsApport

    return StatutsCivilsApport(
        montant=montant or None,
        montant_lettres=number_words_from_value(montant) if montant else None,
    )


def build_selas_plan(payload: dict[str, object]) -> SelasSlicePlan:
    blockers = _validate(payload)
    document_codes = _selas_document_codes(payload)
    warnings = [
        "SELAS multi V1 : 2 a 5 associes, vocabulaire actions. Bundle de creation : statuts "
        "+ tronc commun + PV gerant + demande ordre. Le moteur exige la coherence des actions.",
    ]
    if _regime_communautaire_actif(payload):
        warnings.append("Regime communautaire actif : DOC-005 et DOC-006 seront generes.")
    # R7 : generation PAR associe marie. Le formulaire collecte le regime par
    # associe physique ; `generate_dossier` emet desormais un couple DOC-005/006
    # PAR associe marie sous communaute, avec des fichiers de noms distincts. On
    # informe simplement l'operateur du nombre de couples produits.
    maries = _associes_maries_communaute(payload)
    if len(maries) > 1:
        noms = ", ".join(f"{a.prenoms or a.prenom or ''} {a.nom or ''}".strip() for a in maries)
        warnings.append(
            f"{len(maries)} associes maries sous communaute detectes ({noms}) : un couple "
            "renonciation + avertissement sera genere POUR CHACUN (fichiers nommes par associe)."
        )
    if blockers:
        return SelasSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=document_codes,
            blockers=blockers,
            warnings=tuple(warnings),
        )
    return SelasSlicePlan(
        can_generate=True,
        status="ready",
        reason="Pret pour generation SELAS multi V1 (bundle de creation).",
        document_codes=document_codes,
        blockers=(),
        warnings=tuple(warnings),
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination requise."),
        ("siege", "Siege requis."),
        ("profession_reglementee", "Profession requise."),
        ("profession_reglementee_pluriel", "Profession (pluriel) requise."),
        ("capital_social", "Capital social requis."),
        # Valeur nominale : calculee (capital / nb actions), plus saisie (SCREEN-2)
        # -> on bloque sur capital + nb actions (deja valides), pas sur la valeur.
        ("ville_rcs", "RCS (ville) requis."),
        ("adresse_lieu_exercice", "Adresse du lieu d'exercice requise."),
        ("banque_nom", "Banque requise."),
        ("banque_adresse", "Adresse banque requise."),
        ("date_cloture", "Cloture du premier exercice requise."),
        ("signature_lieu", "Lieu de signature requis."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    nb_actions_total = int(payload.get("nb_actions_total") or 0)
    if nb_actions_total < 1:
        blockers.append("Nombre total d'actions requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    associes = payload.get("associes") or []
    if not isinstance(associes, list) or len(associes) < SELAS_NB_MIN:
        blockers.append(f"SELAS multi requiert au moins {SELAS_NB_MIN} associes.")
    else:
        if not any(a.type_personne == "personne_physique" for a in associes):
            blockers.append("Au moins une personne physique (futur president) requise.")
        for idx, associe in enumerate(associes, start=1):
            if not _named(associe):
                blockers.append(f"Identite de l'associe {idx} requise.")
            if not associe.nb_actions:
                blockers.append(f"Nombre d'actions de l'associe {idx} requis.")
            if not str(associe.qualite_capital or "").strip():
                blockers.append(f"Qualite au capital de l'associe {idx} requise.")
            if associe.type_personne == "personne_physique":
                for field, name in (
                    ("date_naissance", "date de naissance"),
                    ("ville_naissance", "ville de naissance"),
                    ("nationalite", "nationalite"),
                    ("adresse_personnelle_affichee", "adresse"),
                    ("qualification_principale", "qualification"),
                    ("ordre_departemental", "departement ordre"),
                    ("numero_ordre", "numero ordre"),
                    ("numero_rpps", "numero RPPS"),
                ):
                    if not str(getattr(associe, field) or "").strip():
                        blockers.append(f"Associe {idx} : {name} requise.")
        if nb_actions_total:
            total = sum((a.nb_actions or 0) for a in associes)
            if total != nb_actions_total:
                # R3 (retours Rafael 2026-06-18) : message explicite, sans jargon.
                blockers.append(
                    "Problème de calcul : la somme des actions réparties entre les "
                    f"associés ({total}) ne correspond pas au nombre total d'actions "
                    f"({nb_actions_total})."
                )
    blockers.extend(_validate_common_docs(payload))
    blockers.extend(_validate_regime_communautaire(payload))
    return tuple(dict.fromkeys(blockers))


def _validate_regime_communautaire(payload: dict[str, object]) -> list[str]:
    """Saisies conjoint requises par DOC-005 / DOC-006 quand le regime est actif.

    Deux sources possibles (R7) : le toggle GLOBAL historique (cles plates) OU
    le regime PAR associe physique. Chaque source active impose la saisie du
    conjoint + du regime matrimonial."""
    blockers: list[str] = []
    if bool(payload.get("regime_communautaire")):
        required = (
            ("conjoint_prenom", "Prenom du conjoint requis (regime communautaire)."),
            ("conjoint_nom", "Nom du conjoint requis (regime communautaire)."),
            ("regime_matrimonial", "Regime matrimonial requis (regime communautaire)."),
        )
        for field, message in required:
            if not str(payload.get(field) or "").strip():
                blockers.append(message)
    # R7 : validation par associe physique marie sous communaute.
    associes = payload.get("associes") or []
    for index, associe in enumerate(associes):
        if not isinstance(associe, StatutsCivilsAssocie):
            continue
        regime = associe.regime_communautaire_associe
        if regime is None or not regime.actif:
            continue
        label = f"Associe {index + 1}"
        if not str(regime.conjoint_prenom or "").strip():
            blockers.append(f"{label} : prenom du conjoint requis (regime communautaire).")
        if not str(regime.conjoint_nom or "").strip():
            blockers.append(f"{label} : nom du conjoint requis (regime communautaire).")
        if not str(regime.regime_matrimonial or "").strip():
            blockers.append(f"{label} : regime matrimonial requis (regime communautaire).")
    return blockers


def _validate_common_docs(payload: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    required = (
        ("siege_num", "No de voie du siege requis (domiciliation)."),
        ("siege_voie", "Voie du siege requise (domiciliation)."),
        ("siege_cp", "Code postal du siege requis (domiciliation)."),
        ("siege_ville", "Ville du siege requise (domiciliation)."),
        ("signataire_nom_pere", "Nom du pere du president requis (declaration)."),
        ("signataire_nom_mere", "Nom de la mere du president requis (declaration)."),
        ("signataire_adresse_num", "No de voie du president requis (declaration)."),
        ("signataire_adresse_voie", "Voie du president requise (declaration)."),
        ("signataire_adresse_cp", "Code postal du president requis (declaration)."),
        ("signataire_adresse_ville", "Ville du president requise (declaration)."),
        ("signataire_nationalite", "Nationalite du president requise (declaration)."),
        # R5 (2026-06-18) : « Conseil departemental » supprime du formulaire ; le
        # libelle est derive du departement + connecteur, plus de saisie a valider.
        ("ordre_departement", "Departement d'inscription a l'ordre requis (demande inscription)."),
        ("ordre_adresse_ligne_1", "Adresse de l'ordre requise (demande inscription)."),
        ("ordre_cp", "Code postal de l'ordre requis (demande inscription)."),
        ("ordre_ville", "Ville de l'ordre requise (demande inscription)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    if payload.get("signataire_date_naissance") is None:
        blockers.append("Date de naissance du president requise (declaration).")
    if payload.get("decision_date") is None:
        blockers.append("Date de decision requise (PV nomination gerant).")
    return blockers


def _named(associe: StatutsCivilsAssocie) -> bool:
    if associe.type_personne == "personne_morale":
        return bool((associe.denomination or "").strip())
    return bool((associe.prenoms or associe.prenom or "").strip()) and bool(
        (associe.nom or "").strip()
    )


def _resolve_president_index(
    payload: dict[str, object], associes: list[StatutsCivilsAssocie]
) -> int:
    """Index du president retenu pour la generation.

    Lit le choix UI `payload["president_index"]` ; tombe sur le premier associe
    physique si absent / invalide (fixtures historiques, ou index pointant une
    personne morale). Garantit qu'aucun index moral n'atteint le generateur
    (qui exige un President personne physique).
    """
    default_index = next(
        (i for i, a in enumerate(associes) if a.type_personne == "personne_physique"),
        0,
    )
    raw = payload.get("president_index")
    if raw is None:
        return default_index
    try:
        idx = int(raw)
    except (TypeError, ValueError):
        return default_index
    if 0 <= idx < len(associes) and associes[idx].type_personne == "personne_physique":
        return idx
    return default_index


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    associes: list[StatutsCivilsAssocie] = list(payload.get("associes") or [])
    president_index = _resolve_president_index(payload, associes)
    signataire_associe = associes[president_index] if associes else None
    genre = (signataire_associe.genre if signataire_associe else None) or Gender.FEMININ
    civilite = signataire_associe.civilite_affichage if signataire_associe else "Madame"
    prenom = signataire_associe.prenom if signataire_associe else ""
    nom = signataire_associe.nom if signataire_associe else ""
    profession = (
        (signataire_associe.qualification_principale or signataire_associe.profession)
        if signataire_associe
        else ""
    ) or ""
    adresse_perso = Address(
        num_voie=str(payload.get("signataire_adresse_num") or ""),
        voie=str(payload.get("signataire_adresse_voie") or ""),
        cp=str(payload.get("signataire_adresse_cp") or ""),
        ville=str(payload.get("signataire_adresse_ville") or ""),
        adresse_affichee=_struct_display(payload, "signataire_adresse"),
    )
    siege_struct = Address(
        num_voie=str(payload.get("siege_num") or ""),
        voie=str(payload.get("siege_voie") or ""),
        cp=str(payload.get("siege_cp") or ""),
        ville=str(payload.get("siege_ville") or ""),
        adresse_affichee=str(payload.get("siege") or "") or _struct_display(payload, "siege"),
    )
    capital = str(payload.get("capital_social") or "")
    nb_actions_total = int(payload.get("nb_actions_total") or 0)
    # Valeur nominale d'une action : calculee (capital / nb actions) si non fournie
    # explicitement (SCREEN-2). Le chemin de test direct peut fournir une valeur.
    valeur_action = str(
        payload.get("valeur_nominale_action") or ""
    ) or calculate_nominal_value(capital, nb_actions_total)
    titre = str(payload.get("signataire_titre") or "Docteur")

    signataire = Person(
        genre=genre,
        civilite=civilite,
        prenom=prenom,
        nom=nom,
        titre_affichage=titre,
        adresse_perso=adresse_perso,
        adresse_personnelle_affichee=adresse_perso.adresse_affichee,
        date_naissance=payload.get("signataire_date_naissance"),
        ville_naissance=(signataire_associe.ville_naissance if signataire_associe else "") or "",
        nationalite=str(payload.get("signataire_nationalite") or ""),
        nom_pere=str(payload.get("signataire_nom_pere") or ""),
        nom_mere=str(payload.get("signataire_nom_mere") or ""),
        fonction_dirigeant="président",
        qualification_principale=profession,
    )

    regime_communautaire_actif = _regime_communautaire_actif(payload)
    # R7 : si le toggle global est inactif mais qu'un associe physique est marie
    # sous communaute, on derive le contexte regime du PREMIER associe marie
    # (ordre du formulaire). Le moteur n'emet encore qu'UN couple DOC-005/006 ;
    # build_selas_plan flague la multiplication a faire cote moteur.
    regime_payload = _effective_regime_payload(payload)
    # Adresse du foyer pour le conjoint : adresse de l'associe marie pilote si le
    # chemin per-associe gouverne, sinon adresse du president (toggle global).
    conjoint_foyer = _conjoint_foyer_address(payload, adresse_perso)
    return DocumentGenerationContext(
        structure="SELAS",
        dossier_options=DossierOptions(
            associe_unique=False,
            regime_communautaire=regime_communautaire_actif,
        ),
        personne_signataire=signataire,
        conjoint=(
            _conjoint_person(regime_payload, conjoint_foyer)
            if regime_communautaire_actif
            else None
        ),
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
            nombre_exemplaires="quatre",
        ),
        societe=Company(
            forme_sociale="SELAS",
            forme_sociale_affichage="SELAS",
            forme_sociale_abregee="SELAS",
            forme_sociale_complete="société d'exercice libéral par actions simplifiée",
            forme_sociale_libelle_long="Société d'exercice libéral par actions simplifiée",
            denomination=str(payload.get("denomination") or ""),
            denomination_courte=str(payload.get("denomination") or ""),
            capital=capital,
            capital_social=capital,
            capital_variable=True,
            siege=siege_struct,
            ville_rcs=str(payload.get("ville_rcs") or ""),
            nb_parts_total=nb_actions_total,
        ),
        apport=Apport(
            montant=capital,
            montant_lettres=number_words_from_value(capital),
        ),
        regime_communautaire=(
            _regime_communautaire(regime_payload) if regime_communautaire_actif else None
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=siege_struct.adresse_affichee,
        ),
        mandataire=cc.default_mandataire(),
        ordre=_selas_ordre(payload),
        capital=CapitalContext(
            nb_parts_total=nb_actions_total,
            valeur_nominale_part=valeur_action,
            nb_parts_representees=nb_actions_total,
            montant=capital,
            type_titre="actions",
        ),
        dirigeant_nomine=DirigeantNomine(
            genre=genre,
            civilite_affichage=civilite,
            prenom=prenom,
            nom=nom,
            date_naissance=payload.get("signataire_date_naissance"),
            ville_naissance=(signataire_associe.ville_naissance if signataire_associe else "")
            or "",
            departement_naissance=(
                signataire_associe.departement_naissance if signataire_associe else ""
            )
            or "",
            nationalite=str(payload.get("signataire_nationalite") or ""),
            adresse_personnelle=adresse_perso,
            fonction_affichage="président",
            ref_associe_index=president_index,
        ),
        dirigeants_nomines=_build_dirigeants_nomines(payload, president_index, adresse_perso),
        associes=_selas_pv_associes(associes),
        decision=DecisionContext(date=_display_date(payload.get("decision_date"))),
        reunion=ReunionContext(
            date_lettres=date_to_french_words(payload.get("decision_date")),
            president=ReunionPresident(
                civilite_affichage=civilite,
                prenom=prenom,
                nom=nom,
                qualite="président",
                civilite_president_seance=civilite,
                prenom_president_seance=prenom,
                nom_personne_seance=nom,
            ),
        ),
        statuts_selas_multi=StatutsSelasMultiContext(
            profession_reglementee=str(payload.get("profession_reglementee") or ""),
            profession_reglementee_pluriel=str(
                payload.get("profession_reglementee_pluriel") or ""
            ),
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            nb_actions_total=nb_actions_total,
            nb_actions_total_lettres=number_words_from_value(nb_actions_total),
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
            adresse_lieu_exercice=str(payload.get("adresse_lieu_exercice") or ""),
            banque_nom=str(payload.get("banque_nom") or ""),
            banque_adresse=str(payload.get("banque_adresse") or ""),
            date_cloture_premier_exercice=str(payload.get("date_cloture") or ""),
            associes=associes,
            president=StatutsSelasMultiPresident(ref_associe_index=president_index),
        ),
        metadata={"front_slice": "track_b_selas_multi_v1"},
    )


def _build_dirigeants_nomines(
    payload: dict[str, object],
    president_index: int,
    president_adresse: Address,
) -> list[DirigeantNomine]:
    """Liste des dirigeants nommes au PV (President d'abord, puis DG).

    Reconstruit un `DirigeantNomine` par dirigeant coche, dans l'ordre PV. Le
    President reutilise l'adresse personnelle structuree deja calculee
    (signataire) ; les autres dirigeants (Directeur General) utilisent l'adresse
    structuree saisie sous leur propre case « Dirigeant ». Renvoie [] si l'UI n'a
    pas alimente la charge utile (fixtures / appels directs) -> le PV retombe sur
    le mode mono via `dirigeant_nomine`.
    """
    raw = payload.get("dirigeants_nomines")
    if not isinstance(raw, list) or not raw:
        return []
    dirigeants: list[DirigeantNomine] = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        index = entry.get("ref_associe_index")
        if index == president_index:
            adresse = president_adresse
        else:
            adresse = Address(
                num_voie=str(entry.get("adresse_num") or ""),
                voie=str(entry.get("adresse_voie") or ""),
                cp=str(entry.get("adresse_cp") or ""),
                ville=str(entry.get("adresse_ville") or ""),
                adresse_affichee=str(entry.get("adresse_personnelle_affichee") or ""),
            )
        date_naissance = entry.get("date_naissance_iso") or entry.get("date_naissance_affichee")
        dirigeants.append(
            DirigeantNomine(
                genre=entry.get("genre") or Gender.MASCULIN,
                civilite_affichage=str(entry.get("civilite_affichage") or "Monsieur"),
                prenom=str(entry.get("prenom") or ""),
                nom=str(entry.get("nom") or ""),
                date_naissance=date_naissance,
                ville_naissance=str(entry.get("ville_naissance") or "") or None,
                departement_naissance=str(entry.get("departement_naissance") or "") or None,
                nationalite=str(entry.get("nationalite") or "") or None,
                adresse_personnelle=adresse,
                fonction_affichage=str(entry.get("fonction_affichage") or "Président"),
                ref_associe_index=index if isinstance(index, int) else None,
            )
        )
    return dirigeants


def _selas_ordre(payload: dict[str, object]):
    from sydel_doc_engine.domain.models import OrdreAddress, OrdreProfessionnel

    ligne_1 = str(payload.get("ordre_adresse_ligne_1") or "")
    cp = str(payload.get("ordre_cp") or "")
    ville = str(payload.get("ordre_ville") or "")
    bloc = f"{ligne_1}\n{cp} {ville}"
    pluriel = str(payload.get("profession_reglementee_pluriel") or "")
    departement = str(payload.get("ordre_departement") or "")
    # R6 : connecteur grammatical (« de » / « du ») choisi au formulaire ;
    # defaut « de » si absent.
    connecteur = str(payload.get("ordre_connecteur") or "de").strip() or "de"
    # R5 : le « Conseil departemental » n'est plus saisi -> on derive le libelle
    # (utilise uniquement par le fallback non-SEL ; pour la SELAS le moteur
    # reconstruit la ligne a partir du departement + connecteur).
    conseil_libelle = (
        f"Conseil Départemental de l'Ordre des {pluriel} {connecteur} {departement}".strip()
        if pluriel and departement
        else ""
    )
    return OrdreProfessionnel(
        conseil_departemental_libelle=conseil_libelle,
        departement_inscription=departement,
        connecteur_departement=connecteur,
        destinataire_appel="Monsieur le Président",
        profession_signataire_affichee=str(payload.get("profession_reglementee") or ""),
        profession_ligne_destinataire=pluriel,
        profession_reglementee_pluriel=pluriel,
        adresse_affichee=bloc,
        adresse_bloc_affiche=bloc,
        adresse=OrdreAddress(
            ligne_1=str(payload.get("ordre_adresse_ligne_1") or ""),
            cp=str(payload.get("ordre_cp") or ""),
            ville=str(payload.get("ordre_ville") or ""),
        ),
    )


def _conjoint_foyer_address(payload: dict[str, object], president_address: Address) -> Address:
    """Adresse du foyer pour le conjoint (R7).

    Toggle global -> adresse du president (historique). Chemin per-associe ->
    adresse de l'associe marie pilote (1er) si elle est renseignee, sinon repli
    sur l'adresse du president."""
    if bool(payload.get("regime_communautaire")):
        return president_address
    maries = _associes_maries_communaute(payload)
    if maries and (maries[0].adresse_personnelle_affichee or "").strip():
        return Address(adresse_affichee=str(maries[0].adresse_personnelle_affichee or ""))
    return president_address


def _effective_regime_payload(payload: dict[str, object]) -> dict[str, object]:
    """Payload effectif pour le contexte regime communautaire (R7).

    - Toggle global actif -> payload inchange (comportement historique : conjoint
      + regime des cles plates `conjoint_*` / `regime_matrimonial`).
    - Toggle global inactif mais >= 1 associe physique marie sous communaute ->
      overlay du PREMIER associe marie (ses cles conjoint/regime) sur le payload.
      Le moteur n'emet qu'UN couple DOC-005/006 ; la generation par-personne
      reste a faire cote moteur (flag dans build_selas_plan)."""
    if bool(payload.get("regime_communautaire")):
        return payload
    maries = _associes_maries_communaute(payload)
    if not maries:
        return payload
    regime = maries[0].regime_communautaire_associe
    if regime is None:
        return payload
    overlay = dict(payload)
    overlay["conjoint_civilite"] = regime.conjoint_civilite or "Madame"
    overlay["conjoint_genre"] = regime.conjoint_genre or Gender.FEMININ
    overlay["conjoint_prenom"] = regime.conjoint_prenom or ""
    overlay["conjoint_nom"] = regime.conjoint_nom or ""
    overlay["regime_matrimonial"] = regime.regime_matrimonial or ""
    return overlay


def _conjoint_person(payload: dict[str, object], signataire_address: Address) -> Person:
    """Conjoint (renonciation DOC-005 + avertissement DOC-006).

    L'avertissement adresse le conjoint au domicile du foyer ; on reutilise
    l'adresse personnelle structuree du signataire, deja saisie.
    """
    return Person(
        genre=payload.get("conjoint_genre") or Gender.FEMININ,
        civilite=str(payload.get("conjoint_civilite") or "Madame"),
        prenom=str(payload.get("conjoint_prenom") or ""),
        nom=str(payload.get("conjoint_nom") or ""),
        adresse_perso=signataire_address,
        adresse_personnelle_affichee=signataire_address.adresse_affichee,
    )


def _regime_communautaire(payload: dict[str, object]) -> RegimeCommunautaire:
    """Mappe les saisies vers le contexte du conditionnel regime communautaire."""
    signature_date = payload.get("signature_date")
    return RegimeCommunautaire(
        avertissement=RegimeCommunautaireAvertissement(date_signature=signature_date),
        renonciation=RegimeCommunautaireRenonciation(
            lieu_signature=str(payload.get("signature_lieu") or ""),
            date_signature=signature_date,
            nombre_exemplaires_lettres="quatre",
        ),
        date_courrier_avertissement=signature_date,
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        qualite_renoncee="associé",
    )


def _selas_pv_associes(associes: list[StatutsCivilsAssocie]) -> list[Associe]:
    mapped: list[Associe] = []
    for associe in associes:
        nb = associe.nb_actions or 0
        if associe.type_personne == "personne_morale":
            mapped.append(
                Associe(
                    genre=Gender.MASCULIN,
                    civilite_affichage="",
                    prenom="",
                    nom=associe.denomination or "",
                    nb_parts=nb,
                    nb_parts_lettres=number_words_from_value(nb),
                )
            )
            continue
        mapped.append(
            Associe(
                genre=associe.genre or Gender.MASCULIN,
                civilite_affichage=associe.civilite_affichage or "Monsieur",
                prenom=associe.prenom or associe.prenoms or "",
                nom=associe.nom or "",
                nb_parts=nb,
                nb_parts_lettres=number_words_from_value(nb),
                profession=associe.profession or "",
                profession_reglementee=associe.profession or "",
            )
        )
    return mapped


def _struct_display(payload: dict[str, object], prefix: str) -> str:
    return (
        f"{payload.get(prefix + '_num', '')} {payload.get(prefix + '_voie', '')}, "
        f"{payload.get(prefix + '_cp', '')} {payload.get(prefix + '_ville', '')}"
    ).strip(" ,")


def _display_date(value) -> str | None:
    if value is None:
        return None
    return value.strftime("%d/%m/%Y")


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_selas_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    # 1) Tronc commun + statuts (+ DOC-005/006 SI toggle global) via l'orchestrateur
    #    generique (1 doc_id -> 1 fichier de nom fixe). Contrat orchestrateur intact.
    docx_paths = generate_docx_files_for_document_codes(
        ctx, output_dir, _orchestrator_codes(payload)
    )
    # 2) R7 : un couple renonciation (DOC-005) + avertissement (DOC-006) PAR associe
    #    physique marie sous communaute, hors orchestrateur, avec des fichiers de
    #    noms distincts. Ne s'active QUE par le chemin per-associe (toggle global
    #    inactif) ; le chemin toggle global reste gere a l'etape 1.
    docx_paths.extend(_generate_regime_par_associe(payload, ctx, output_dir))
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def _generate_regime_par_associe(
    payload: dict[str, object],
    base_ctx: DocumentGenerationContext,
    output_dir: Path,
) -> list[Path]:
    """Emet renonciation + avertissement UNE FOIS PAR associe marie (R7).

    Inactif si le toggle global porte le regime (l'orchestrateur a deja emis le
    couple unique de nom fixe a l'etape 1) ou si aucun associe physique n'est
    marie sous communaute. Sinon, pour chaque associe marie, derive un contexte
    par-associe (renoncant = l'associe, son conjoint, son regime) puis ecrit les
    deux lettres sous des noms distincts (incluant le nom de l'associe).

    Mecanisme de nommage : les generateurs ont un OUTPUT_FILENAME fixe ; on les
    laisse ecrire ce nom puis on RENOMME le Path retourne. Avec un seul associe
    marie, on conserve le nom fixe historique (byte-identique) ; avec plusieurs,
    on suffixe par le nom de l'associe pour eviter tout ecrasement."""
    if bool(payload.get("regime_communautaire")):
        return []
    maries = _associes_maries_communaute(payload)
    if not maries:
        return []
    suffix_par_associe = len(maries) > 1
    renonciation_gen = LettreRenonciationAssocieGenerator()
    avertissement_gen = LettreAvertissementConjointGenerator()
    produced: list[Path] = []
    for associe in maries:
        ctx = _regime_context_for_associe(base_ctx, payload, associe)
        rendu_renonciation = renonciation_gen.generate(ctx, output_dir)
        rendu_avertissement = avertissement_gen.generate(ctx, output_dir)
        if suffix_par_associe:
            slug = _associe_filename_slug(associe)
            rendu_renonciation = _rename_with_slug(rendu_renonciation, slug)
            rendu_avertissement = _rename_with_slug(rendu_avertissement, slug)
        produced.append(rendu_renonciation)
        produced.append(rendu_avertissement)
    return produced


def _regime_context_for_associe(
    base_ctx: DocumentGenerationContext,
    payload: dict[str, object],
    associe: StatutsCivilsAssocie,
) -> DocumentGenerationContext:
    """Contexte par-associe pour les lettres de regime communautaire (R7).

    Copie le contexte de base (societe / apport / signature partages) en
    remplacant : le renoncant (`personne_signataire`), son conjoint et le
    contexte `regime_communautaire` (dates de signature partagees + regime
    matrimonial de CET associe). Force `dossier_options.regime_communautaire`
    a vrai pour passer la garde des generateurs."""
    regime = associe.regime_communautaire_associe
    apporteur_adresse = _associe_signataire_address(associe, base_ctx.personne_signataire)
    apporteur = Person(
        genre=associe.genre or Gender.FEMININ,
        civilite=associe.civilite_affichage or "Madame",
        prenom=associe.prenom or associe.prenoms or "",
        nom=associe.nom or "",
        titre_affichage=associe.profession or "Docteur",
        adresse_perso=apporteur_adresse,
        adresse_personnelle_affichee=apporteur_adresse.adresse_affichee,
        nationalite=associe.nationalite or None,
        ville_naissance=associe.ville_naissance or "",
        fonction_dirigeant="associé",
        qualification_principale=(
            associe.qualification_principale or associe.profession or ""
        ),
    )
    conjoint = Person(
        genre=(regime.conjoint_genre if regime else None) or Gender.FEMININ,
        civilite=(regime.conjoint_civilite if regime else None) or "Madame",
        prenom=(regime.conjoint_prenom if regime else None) or "",
        nom=(regime.conjoint_nom if regime else None) or "",
        adresse_perso=apporteur_adresse,
        adresse_personnelle_affichee=apporteur_adresse.adresse_affichee,
    )
    signature_date = payload.get("signature_date")
    regime_ctx = RegimeCommunautaire(
        avertissement=RegimeCommunautaireAvertissement(date_signature=signature_date),
        renonciation=RegimeCommunautaireRenonciation(
            lieu_signature=str(payload.get("signature_lieu") or ""),
            date_signature=signature_date,
            nombre_exemplaires_lettres="quatre",
        ),
        date_courrier_avertissement=signature_date,
        regime_matrimonial=(regime.regime_matrimonial if regime else None) or "",
        qualite_renoncee="associé",
    )
    dossier_options = base_ctx.dossier_options or DossierOptions(associe_unique=False)
    return base_ctx.model_copy(
        update={
            "dossier_options": dossier_options.model_copy(
                update={"regime_communautaire": True}
            ),
            "personne_signataire": apporteur,
            "conjoint": conjoint,
            "regime_communautaire": regime_ctx,
        }
    )


def _associe_signataire_address(
    associe: StatutsCivilsAssocie,
    president: Person,
) -> Address:
    """Adresse structuree du renoncant (apporteur) et donc du foyer du conjoint.

    L'avertissement (DOC-006) exige une adresse STRUCTUREE complete
    (num_voie / voie / cp / ville). On utilise l'adresse structuree de l'associe
    si elle est renseignee ; sinon on retombe sur celle du president (le tronc
    commun garantit qu'elle est complete), pour ne jamais bloquer la generation.
    """
    structuree = associe.adresse_personnelle
    if structuree is not None and all(
        (getattr(structuree, field) or "").strip()
        for field in ("num_voie", "voie", "cp", "ville")
    ):
        return structuree
    return president.adresse_perso or Address()


def _associe_filename_slug(associe: StatutsCivilsAssocie) -> str:
    """Slug de nom de fichier base sur le nom de l'associe (R7).

    Inclut le nom de l'associe pour distinguer les couples DOC-005/006 quand
    plusieurs associes sont maries. Repli sur le prenom puis sur l'index si le
    nom est vide. Sans accents ni caracteres exotiques (compatibilite OS)."""
    base = (associe.nom or associe.prenom or associe.prenoms or "associe").strip()
    normalized = "".join(
        c for c in normalize("NFKD", base) if not combining(c)
    )
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", normalized).strip("_")
    return cleaned or "associe"


def _rename_with_slug(path: Path, slug: str) -> Path:
    """Renomme un fichier genere en y insérant le slug de l'associe.

    « lettre_renonciation_associe.docx » -> « lettre_renonciation_associe_Dupont.docx ».
    En cas de collision improbable (deux associes au meme slug), suffixe un index.
    """
    target = path.with_name(f"{path.stem}_{slug}{path.suffix}")
    if target.exists() and target != path:
        index = 2
        while True:
            candidate = path.with_name(f"{path.stem}_{slug}_{index}{path.suffix}")
            if not candidate.exists():
                target = candidate
                break
            index += 1
    path.replace(target)
    return target


def _address(adresse_affichee: str):
    from sydel_doc_engine.domain.models import Address

    return Address(adresse_affichee=adresse_affichee)


def _t(container, field: str, label: str) -> str:
    return _ts(container, f"{PREFIX}_{field}", label)


def _ts(container, key: str, label: str) -> str:
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key)).strip()


def _i(container, field: str, label: str) -> int:
    return _is(container, f"{PREFIX}_{field}", label)


def _is(container, key: str, label: str) -> int:
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(field: str, label: str) -> date | None:
    key = f"{PREFIX}_{field}"
    current = st.session_state.get(key)
    if isinstance(current, date):
        st.session_state[key] = format_french_date(current)
    elif current is None:
        st.session_state[key] = format_french_date(date.today())
    # Bouton « Aujourd'hui » (comme SELARL) : ecrit la date du jour AVANT que le
    # text_input soit instancie (sinon Streamlit interdit la modif post-widget).
    if st.button("Aujourd'hui", key=f"{key}_today"):
        st.session_state[key] = format_french_date(date.today())
    raw = st.text_input(label, key=key, placeholder="JJ/MM/AAAA")
    return parse_french_date(raw)
