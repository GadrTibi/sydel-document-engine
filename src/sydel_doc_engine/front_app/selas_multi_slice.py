"""Slice front SELAS multi-associes (DOC-044), patron SELARL.

SELAS multi = SEL d'exercice par actions, 2 a 5 associes exercants/non exercants
(personne physique + personne morale), vocabulaire ACTIONS. Contexte moteur
mirroir du builder de test `test_lot_04_statuts_selas_multi`. Reutilise le
repeater generique en mode "exercice" (actions + qualite capital + ordre).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

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
from sydel_doc_engine.front_app.field_derivations import (
    date_to_french_words,
    derive_gender_from_civilite,
    format_french_date,
    number_words_from_value,
    parse_french_date,
)

STRUCTURE = "SELAS"
DOC_CODE = "DOC-044"
PREFIX = "selas"

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


def _selas_document_codes(payload: dict[str, object]) -> tuple[str, ...]:
    """Bundle SELAS de creation, augmente du conditionnel canon « Si regime
    communautaire » (DOC-005 renonciation + DOC-006 avertissement) quand le
    toggle est actif. Toggle inactif -> bundle de base inchange."""
    codes = list(SELAS_BUNDLE_CODES)
    if bool(payload.get("regime_communautaire")):
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
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
    raw = st.session_state.get(_count_key(), 2)
    try:
        return max(2, min(5, int(raw)))
    except (TypeError, ValueError):
        return 2


def render_selas_form() -> dict[str, object]:
    st.subheader("Donnees a saisir")
    st.markdown("**Societe (SELAS d'exercice, vocabulaire actions)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    siege = _t(col_b, "siege", "Siege (adresse affichee)")
    col_c, col_d = st.columns(2)
    profession = _t(col_c, "profession_reglementee", "Profession (ex: medecin)")
    profession_pluriel = _t(col_d, "profession_reglementee_pluriel", "Profession (pluriel)")
    col_e, col_f, col_g = st.columns(3)
    capital = _t(col_e, "capital_social", "Capital social")
    nb_actions = _i(col_f, "nb_actions_total", "Nombre total d'actions")
    valeur_action = _t(col_g, "valeur_nominale_action", "Valeur nominale d'une action")
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

    associes = _render_selas_associes()
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
    }
    payload.update(common)
    return payload


def _render_common_docs_form() -> dict[str, object]:
    """Signataire / president (documents communs : DNC, procuration, PV, ordre)."""
    st.markdown("**President / signataire (documents communs)**")
    col_a, col_b = st.columns(2)
    nom_pere = _t(col_a, "signataire_nom_pere", "Nom du pere (declaration)")
    nom_mere = _t(col_b, "signataire_nom_mere", "Nom de la mere (declaration)")
    st.caption("Adresse personnelle du president (declaration / procuration)")
    col_c, col_d, col_e, col_f = st.columns(4)
    adr_num = _t(col_c, "signataire_adresse_num", "No")
    adr_voie = _t(col_d, "signataire_adresse_voie", "Voie")
    adr_cp = _t(col_e, "signataire_adresse_cp", "CP")
    adr_ville = _t(col_f, "signataire_adresse_ville", "Ville")
    col_g, col_h = st.columns(2)
    nationalite = _t(col_g, "signataire_nationalite", "Nationalite")
    titre = _t(col_h, "signataire_titre", "Titre d'affichage") or "Docteur"
    with st.container():
        date_naissance_iso = _date("signataire_date_naissance", "Date naissance (JJ/MM/AAAA)")
    decision_date = _date("decision_date", "Date de decision (PV gerant)")
    st.markdown("Ordre professionnel (demande d'inscription)")
    col_i, col_j = st.columns(2)
    ordre_conseil = _t(col_i, "ordre_conseil", "Conseil departemental")
    ordre_dep = _t(col_j, "ordre_departement", "Departement ordre")
    col_k, col_l, col_m = st.columns(3)
    ordre_ligne = _t(col_k, "ordre_adresse_ligne_1", "Adresse ordre")
    ordre_cp = _t(col_l, "ordre_cp", "CP ordre")
    ordre_ville = _t(col_m, "ordre_ville", "Ville ordre")
    ordre_numero = _t(st, "ordre_numero", "Numero d'inscription")
    regime = _render_regime_communautaire_form()
    common = {
        "signataire_nom_pere": nom_pere,
        "signataire_nom_mere": nom_mere,
        "signataire_adresse_num": adr_num,
        "signataire_adresse_voie": adr_voie,
        "signataire_adresse_cp": adr_cp,
        "signataire_adresse_ville": adr_ville,
        "signataire_nationalite": nationalite,
        "signataire_titre": titre,
        "signataire_date_naissance": date_naissance_iso,
        "decision_date": decision_date,
        "ordre_conseil": ordre_conseil,
        "ordre_departement": ordre_dep,
        "ordre_adresse_ligne_1": ordre_ligne,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
        "ordre_numero": ordre_numero,
    }
    common.update(regime)
    return common


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


def _render_selas_associes() -> list[StatutsCivilsAssocie]:
    if _count_key() not in st.session_state:
        st.session_state[_count_key()] = 2
    nombre = _associe_count()
    st.markdown(f"**Associes ({nombre})** — 2 a 5, exercants / non exercants")
    cols = st.columns([1, 1, 3])
    if cols[0].button("Ajouter un associe", key=f"{PREFIX}_add"):
        st.session_state[_count_key()] = min(5, nombre + 1)
        st.rerun()
    if cols[1].button("Retirer un associe", key=f"{PREFIX}_remove"):
        st.session_state[_count_key()] = max(2, nombre - 1)
        st.rerun()
    cols[2].caption("Le premier associe physique est designe president par defaut.")

    associes: list[StatutsCivilsAssocie] = []
    for index in range(nombre):
        associes.append(_render_one_associe(index))
    return associes


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
            return _morale(prefix, nb_actions, montant)
        return _physique(prefix, nb_actions, montant)


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
    nationalite = _ts(col_g, f"{prefix}_nationalite", "Nationalite")
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
        adresse_personnelle_affichee=adresse or None,
        qualification_principale=qualification or None,
        ordre_departemental=ordre_dep or None,
        numero_ordre=numero_ordre or None,
        numero_rpps=numero_rpps or None,
        qualite_capital=qualite or None,
        nb_actions=nb_actions or None,
        nb_actions_lettres=number_words_from_value(nb_actions) if nb_actions else None,
        apport=_apport(montant),
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
    if bool(payload.get("regime_communautaire")):
        warnings.append("Regime communautaire actif : DOC-005 et DOC-006 seront generes.")
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
        ("valeur_nominale_action", "Valeur nominale d'une action requise."),
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
    if not isinstance(associes, list) or len(associes) < 2:
        blockers.append("SELAS multi requiert au moins 2 associes.")
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
                blockers.append(
                    f"Somme des actions ({total}) != total declare ({nb_actions_total})."
                )
    blockers.extend(_validate_common_docs(payload))
    blockers.extend(_validate_regime_communautaire(payload))
    return tuple(dict.fromkeys(blockers))


def _validate_regime_communautaire(payload: dict[str, object]) -> list[str]:
    """Saisies conjoint requises par DOC-005 / DOC-006 quand le regime est actif."""
    if not bool(payload.get("regime_communautaire")):
        return []
    blockers: list[str] = []
    required = (
        ("conjoint_prenom", "Prenom du conjoint requis (regime communautaire)."),
        ("conjoint_nom", "Nom du conjoint requis (regime communautaire)."),
        ("regime_matrimonial", "Regime matrimonial requis (regime communautaire)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
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
        ("ordre_conseil", "Conseil departemental de l'ordre requis (demande inscription)."),
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


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    associes: list[StatutsCivilsAssocie] = list(payload.get("associes") or [])
    president_index = next(
        (i for i, a in enumerate(associes) if a.type_personne == "personne_physique"),
        0,
    )
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
    valeur_action = str(payload.get("valeur_nominale_action") or "")
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

    regime_communautaire_actif = bool(payload.get("regime_communautaire"))
    return DocumentGenerationContext(
        structure="SELAS",
        dossier_options=DossierOptions(
            associe_unique=False,
            regime_communautaire=regime_communautaire_actif,
        ),
        personne_signataire=signataire,
        conjoint=_conjoint_person(payload, adresse_perso) if regime_communautaire_actif else None,
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
        regime_communautaire=_regime_communautaire(payload) if regime_communautaire_actif else None,
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


def _selas_ordre(payload: dict[str, object]):
    from sydel_doc_engine.domain.models import OrdreAddress, OrdreProfessionnel

    ligne_1 = str(payload.get("ordre_adresse_ligne_1") or "")
    cp = str(payload.get("ordre_cp") or "")
    ville = str(payload.get("ordre_ville") or "")
    bloc = f"{ligne_1}\n{cp} {ville}"
    pluriel = str(payload.get("profession_reglementee_pluriel") or "")
    return OrdreProfessionnel(
        conseil_departemental_libelle=str(payload.get("ordre_conseil") or ""),
        departement_inscription=str(payload.get("ordre_departement") or ""),
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
    docx_paths = generate_docx_files_for_document_codes(ctx, output_dir, plan.document_codes)
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


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
    raw = st.text_input(label, key=key, placeholder="JJ/MM/AAAA")
    return parse_french_date(raw)
