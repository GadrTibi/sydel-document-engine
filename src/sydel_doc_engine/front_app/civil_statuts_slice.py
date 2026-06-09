"""Slices des statuts civils (SCI, SCI IRIS, SCS, SCM) sur patron SELARL.

Ces quatre types partagent le meme contexte moteur (`StatutsCivilsContext`) et le
meme generateur de famille (statuts_civils). Le slice :
  1. expose une saisie societe + un repeater d'associes generique ;
  2. mappe ces saisies dans un `DocumentGenerationContext` valide ;
  3. appelle le generateur via `generate_docx_files_for_document_codes`.

Patron repris de `selarl_slice` : un contexte de DEFAUT valide (mirroir des
payloads de test/exemple, generation sans token residuel) sur lequel on
superpose les saisies utilisateur. Aucune regle metier nouvelle : on ne fait que
collecter et router vers le moteur existant.
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
    CentreImpots,
    Company,
    DocumentGenerationContext,
    DossierOptions,
    PacteAssociesScmContext,
    Person,
    ScmSatellitesOptions,
    Signature,
    StatutsCivilsAssocie,
    StatutsCivilsCapitalDepot,
    StatutsCivilsContext,
    StatutsCivilsGroupeParts,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app.associe_repeater import RepeaterConfig, render_associe_repeater
from sydel_doc_engine.front_app.field_derivations import (
    format_french_date,
    number_words_from_value,
    parse_french_date,
)

# Mapping structure -> (type statuts civils, doc_code statuts).
CIVIL_TYPE_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SCI": ("sci", "DOC-020"),
    "SCI IRIS": ("sci_iris", "DOC-021"),
    "SCS": ("scs", "DOC-019"),
    "SCM": ("scm", "DOC-025"),
}

# Bornes du repeater d'associes par type (A1 : nommees, AUCUN changement de valeur).
# SCI / SCM : 1 associe minimum ; SCI IRIS / SCS : 2 (structures a deux roles ou
# exigeant une personne morale). Maximum commun = 6.
CIVIL_NB_MIN_BY_STRUCTURE: dict[str, int] = {
    "SCI": 1,
    "SCM": 1,
    "SCI IRIS": 2,
    "SCS": 2,
}
CIVIL_NB_MIN_DEFAUT = 2
CIVIL_NB_MAX_ASSOCIES = 6

# Lettre d'option IS (canon « Si IS ») : conditionnel CREATION pour SCI / SCI IRIS.
DOC_OPTION_IS = "DOC-022"
OPTION_IS_STRUCTURES: tuple[str, ...] = ("SCI", "SCI IRIS")

# Bundle de CREATION par type (canon : statuts du type + tronc commun
# DNC/domiciliation/procuration + PV nomination gerant ; la SCM ajoute la demande
# d'inscription a l'ordre). Les cas non-creation (cession SCM, etc.) sont hors V1.
#
# Satellites SCM (decision RAFAEL 2026-06-08 : ils FONT PARTIE du dossier SCM).
# Cables pour une SCM A EXACTEMENT 2 ASSOCIES (contrainte dure des generateurs) :
#   - DOC-030 liste des depenses communes (societe + 2 associes) ;
#   - DOC-026 pacte d'associes (+ ville du tribunal + mention RCS de la SCM).
# DOC-027 (contrat a frais communs) + DOC-028 (reglement interieur) restent HORS bundle :
# ils exigent l'identite des 2 societes d'exercice partenaires (SEL) + locaux + praticiens,
# donnee/structure a confirmer Rafael avant cablage. Voir _RAFAEL_PACKET_V1.md.
DOC_PACTE_ASSOCIES_SCM = "DOC-026"
DOC_LISTE_DEPENSES_SCM = "DOC-030"


def _creation_bundle_codes(
    structure: str,
    statuts_code: str,
    *,
    option_is: bool = False,
    scm_satellites_pair: bool = False,
) -> tuple[str, ...]:
    codes: list[str] = [statuts_code, *cc.TRONC_COMMUN_CODES, cc.DOC_PV_NOMINATION_GERANT]
    if structure == "SCM":
        codes.append(cc.DOC_DEMANDE_INSCRIPTION_ORDRE)
        # Satellites SCM (Rafael) : pacte + liste depenses, si exactement 2 associes.
        if scm_satellites_pair:
            codes.append(DOC_LISTE_DEPENSES_SCM)
            codes.append(DOC_PACTE_ASSOCIES_SCM)
    # Conditionnel canon « Si IS » (SCI / SCI IRIS) : lettre d'option IS (DOC-022).
    if option_is and structure in OPTION_IS_STRUCTURES:
        codes.append(DOC_OPTION_IS)
    return tuple(dict.fromkeys(codes))


def _scm_satellites_pair_active(payload: dict[str, object]) -> bool:
    """Les satellites pacte + liste depenses se generent pour une SCM a 2 associes."""
    if str(payload.get("structure")) != "SCM":
        return False
    associes = payload.get("associes") or []
    return isinstance(associes, list) and len(associes) == 2


@dataclass(frozen=True)
class CivilSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str


def _signature_date(structure: str) -> date | None:
    key = f"{_prefix(structure)}_signature_date"
    raw = st.session_state.get(key)
    parsed = parse_french_date(raw)
    return parsed


def _prefix(structure: str) -> str:
    return CIVIL_TYPE_BY_STRUCTURE[structure][0]


def render_civil_form(structure: str) -> dict[str, object]:
    """Rend la saisie societe + associes pour un type civil et retourne un payload."""

    statuts_type, _doc = CIVIL_TYPE_BY_STRUCTURE[structure]
    prefix = statuts_type
    st.subheader("Donnees a saisir")
    st.markdown(f"**Societe ({structure})**")

    col_a, col_b = st.columns(2)
    denomination = _text(col_a, prefix, "denomination", "Denomination sociale")
    forme_sociale = _text(col_b, prefix, "forme_sociale", "Forme sociale (libelle)")
    col_c, col_d = st.columns(2)
    capital_social = _text(col_c, prefix, "capital_social", "Capital social")
    nb_parts_total = _int(col_d, prefix, "nb_parts_total", "Nombre total de parts")
    col_e, col_f = st.columns(2)
    valeur_nominale = _text(col_e, prefix, "valeur_nominale_part", "Valeur nominale d'une part")
    duree = _text(col_f, prefix, "duree_societe", "Duree (annees)")

    st.markdown("Siege social")
    col_g, col_h, col_i, col_j = st.columns(4)
    siege_num = _text(col_g, prefix, "siege_num", "No")
    siege_voie = _text(col_h, prefix, "siege_voie", "Voie")
    siege_cp = _text(col_i, prefix, "siege_cp", "CP")
    siege_ville = _text(col_j, prefix, "siege_ville", "Ville")
    ville_rcs = _text(st, prefix, "ville_rcs", "RCS (ville)")

    st.markdown("Depot des fonds")
    col_k, col_l = st.columns(2)
    banque_nom = _text(col_k, prefix, "banque_nom", "Banque")
    banque_adresse = _text(col_l, prefix, "banque_adresse", "Adresse banque")
    date_cloture = _text(
        st, prefix, "date_cloture_premier_exercice", "Cloture du premier exercice"
    )

    st.markdown("**Signature**")
    col_m, col_n = st.columns(2)
    signature_lieu = _text(col_m, prefix, "signature_lieu", "Lieu de signature")
    with col_n:
        signature_date = _date_input(prefix, "signature_date", "Date de signature")

    role_options: tuple[str, ...] = ()
    if structure == "SCS":
        role_options = ("commandite", "commanditaire")

    associes = render_associe_repeater(
        RepeaterConfig(
            key_prefix=prefix,
            titre_unite="parts",
            nb_min=CIVIL_NB_MIN_BY_STRUCTURE.get(structure, CIVIL_NB_MIN_DEFAUT),
            nb_max=CIVIL_NB_MAX_ASSOCIES,
            nb_defaut=CIVIL_NB_MIN_DEFAUT,
            allow_personne_morale=True,
            role_statutaire_options=role_options,
        )
    )

    common = _render_common_docs_form(structure, prefix)

    payload: dict[str, object] = {
        "structure": structure,
        "statuts_type": statuts_type,
        "denomination": denomination,
        "forme_sociale": forme_sociale,
        "capital_social": capital_social,
        "nb_parts_total": nb_parts_total,
        "valeur_nominale_part": valeur_nominale,
        "duree_societe": duree,
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "ville_rcs": ville_rcs,
        "banque_nom": banque_nom,
        "banque_adresse": banque_adresse,
        "date_cloture_premier_exercice": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "associes": associes,
    }
    payload.update(common)
    return payload


def _render_common_docs_form(structure: str, prefix: str) -> dict[str, object]:
    """Saisie du signataire / gerant pour les documents communs du bundle.

    Les statuts collectent deja l'identite de chaque associe ; ces champs
    additionnels sont ceux que les generateurs communs exigent UNIQUEMENT pour le
    signataire (DNC : filiation + adresse structuree ; demande d'inscription a
    l'ordre pour la SCM). Le signataire = premier associe physique.
    """

    st.markdown("**Signataire / gerant (documents communs)**")
    col_a, col_b = st.columns(2)
    nom_pere = _text(col_a, prefix, "signataire_nom_pere", "Nom du pere (declaration)")
    nom_mere = _text(col_b, prefix, "signataire_nom_mere", "Nom de la mere (declaration)")
    st.caption("Adresse personnelle du signataire (declaration / procuration)")
    col_c, col_d, col_e, col_f = st.columns(4)
    adr_num = _text(col_c, prefix, "signataire_adresse_num", "No")
    adr_voie = _text(col_d, prefix, "signataire_adresse_voie", "Voie")
    adr_cp = _text(col_e, prefix, "signataire_adresse_cp", "CP")
    adr_ville = _text(col_f, prefix, "signataire_adresse_ville", "Ville")
    col_g, col_h = st.columns(2)
    fonction = _text(col_g, prefix, "signataire_fonction", "Fonction (ex: gerant)") or "gérant"
    titre = _text(col_h, prefix, "signataire_titre", "Titre d'affichage") or "Docteur"
    decision_date = _date_input(prefix, "decision_date", "Date de decision (PV gerant)")

    common: dict[str, object] = {
        "signataire_nom_pere": nom_pere,
        "signataire_nom_mere": nom_mere,
        "signataire_adresse_num": adr_num,
        "signataire_adresse_voie": adr_voie,
        "signataire_adresse_cp": adr_cp,
        "signataire_adresse_ville": adr_ville,
        "signataire_fonction": fonction,
        "signataire_titre": titre,
        "decision_date": decision_date,
    }

    if structure == "SCM":
        st.markdown("Ordre professionnel (demande d'inscription)")
        col_i, col_j = st.columns(2)
        ordre_conseil = _text(col_i, prefix, "ordre_conseil", "Conseil departemental")
        ordre_dep = _text(col_j, prefix, "ordre_departement", "Departement ordre")
        col_k, col_l, col_m = st.columns(3)
        ordre_ligne = _text(col_k, prefix, "ordre_adresse_ligne_1", "Adresse ordre")
        ordre_cp = _text(col_l, prefix, "ordre_cp", "CP ordre")
        ordre_ville = _text(col_m, prefix, "ordre_ville", "Ville ordre")
        ordre_numero = _text(st, prefix, "ordre_numero", "Numero d'inscription")
        common.update(
            {
                "ordre_conseil": ordre_conseil,
                "ordre_departement": ordre_dep,
                "ordre_adresse_ligne_1": ordre_ligne,
                "ordre_cp": ordre_cp,
                "ordre_ville": ordre_ville,
                "ordre_numero": ordre_numero,
            }
        )
        # Satellites SCM (pacte + liste depenses, generes si 2 associes) : ville du
        # tribunal de commerce competent + mention RCS de la SCM (qui n'est pas encore
        # immatriculee a la constitution -> saisie libre, ex. « en cours de constitution »).
        st.markdown("Satellites SCM (pacte d'associes / liste des depenses communes)")
        col_p, col_q = st.columns(2)
        pacte_ville_tribunal = _text(col_p, prefix, "pacte_ville_tribunal", "Ville du tribunal")
        societe_numero_rcs = _text(
            col_q, prefix, "societe_numero_rcs", "N° RCS SCM (ou 'en cours de constitution')"
        )
        common.update(
            {
                "pacte_ville_tribunal": pacte_ville_tribunal,
                "societe_numero_rcs": societe_numero_rcs,
            }
        )
    if structure in OPTION_IS_STRUCTURES:
        common.update(_render_option_is_form(prefix))
    return common


def _render_option_is_form(prefix: str) -> dict[str, object]:
    """Conditionnel canon « Si IS » (SCI / SCI IRIS) : lettre d'option IS (DOC-022).

    Toggle + centre des impots requis par le generateur de la lettre + SIREN de
    la societe. Inactif -> aucun document ajoute, bundle de base inchange.
    """
    option_key = f"{prefix}_option_is"
    if option_key not in st.session_state:
        st.session_state[option_key] = False
    actif = st.checkbox(
        "Option IS (ajoute la lettre d'option pour l'impot sur les societes)",
        key=option_key,
    )
    if not actif:
        return {"option_is": False}
    st.caption("Centre des impots destinataire (lettre d'option IS)")
    siren = _text(st, prefix, "siren", "SIREN de la societe")
    col_a, col_b = st.columns(2)
    impots_service = _text(col_a, prefix, "impots_service", "Service")
    impots_centre = _text(col_b, prefix, "impots_centre", "Centre")
    impots_ligne_1 = _text(st, prefix, "impots_adresse_ligne_1", "Adresse (ligne 1)")
    impots_ligne_2 = _text(st, prefix, "impots_adresse_ligne_2", "Adresse (ligne 2)")
    col_c, col_d = st.columns(2)
    impots_cp = _text(col_c, prefix, "impots_cp", "CP")
    impots_ville = _text(col_d, prefix, "impots_ville", "Ville")
    return {
        "option_is": True,
        "siren": siren,
        "impots_service": impots_service,
        "impots_centre": impots_centre,
        "impots_adresse_ligne_1": impots_ligne_1,
        "impots_adresse_ligne_2": impots_ligne_2,
        "impots_cp": impots_cp,
        "impots_ville": impots_ville,
    }


def build_civil_plan(payload: dict[str, object]) -> CivilSlicePlan:
    structure = str(payload["structure"])
    _statuts_type, doc_code = CIVIL_TYPE_BY_STRUCTURE[structure]
    option_is = bool(payload.get("option_is")) and structure in OPTION_IS_STRUCTURES
    scm_pair = _scm_satellites_pair_active(payload)
    document_codes = _creation_bundle_codes(
        structure, doc_code, option_is=option_is, scm_satellites_pair=scm_pair
    )
    blockers = _validate(payload)
    warnings_list = [
        f"{structure} : bundle de creation (statuts + tronc commun + PV gerant"
        + (" + demande ordre + satellites SCM" if structure == "SCM" else "")
        + "). Le moteur valide la coherence des parts / du capital.",
    ]
    if option_is:
        warnings_list.append("Option IS active : la lettre d'option IS (DOC-022) sera generee.")
    warnings = tuple(warnings_list)
    if blockers:
        return CivilSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=document_codes,
            blockers=blockers,
            warnings=warnings,
            target_engine_adapter="front_app.civil_statuts_slice",
        )
    return CivilSlicePlan(
        can_generate=True,
        status="ready",
        reason=f"Pret pour generation {structure} V1 (bundle de creation).",
        document_codes=document_codes,
        blockers=(),
        warnings=warnings,
        target_engine_adapter="front_app.civil_statuts_slice",
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    structure = str(payload["structure"])
    if not str(payload.get("denomination") or "").strip():
        blockers.append("Denomination sociale requise.")
    if not str(payload.get("capital_social") or "").strip():
        blockers.append("Capital social requis.")
    nb_parts_total = int(payload.get("nb_parts_total") or 0)
    if nb_parts_total < 1:
        blockers.append("Nombre total de parts requis et superieur a zero.")
    if not str(payload.get("valeur_nominale_part") or "").strip():
        blockers.append("Valeur nominale d'une part requise.")
    if not str(payload.get("siege_ville") or "").strip():
        blockers.append("Ville du siege requise.")
    if not str(payload.get("ville_rcs") or "").strip():
        blockers.append("Ville RCS requise.")
    if not str(payload.get("banque_nom") or "").strip():
        blockers.append("Banque de depot des fonds requise.")
    if not str(payload.get("date_cloture_premier_exercice") or "").strip():
        blockers.append("Date de cloture du premier exercice requise.")
    if not str(payload.get("signature_lieu") or "").strip():
        blockers.append("Lieu de signature requis.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    associes = payload.get("associes") or []
    if not isinstance(associes, list) or not associes:
        blockers.append("Au moins un associe requis.")
    else:
        # SCI standard + associe personne morale = AUTORISE (ratifie Rafael 2026-06-08).
        if structure == "SCI IRIS" and not any(
            a.type_personne == "personne_morale" for a in associes
        ):
            blockers.append("SCI IRIS : au moins une personne morale associee requise.")
        for idx, associe in enumerate(associes, start=1):
            if not _associe_named(associe):
                blockers.append(f"Identite de l'associe {idx} requise.")
            if associe.parts is None or not associe.parts.nb:
                blockers.append(f"Nombre de parts de l'associe {idx} requis.")
            if associe.apport is None or not str(associe.apport.montant or "").strip():
                blockers.append(f"Apport de l'associe {idx} requis.")
            if structure == "SCM" and not str(associe.profession or "").strip():
                blockers.append(f"Profession de l'associe {idx} requise (SCM).")
            if associe.type_personne == "personne_physique":
                for field, name in (
                    ("date_naissance", "date de naissance"),
                    ("ville_naissance", "ville de naissance"),
                    ("departement_naissance", "departement de naissance"),
                    ("nationalite", "nationalite"),
                    ("situation_maritale", "situation matrimoniale"),
                    ("adresse_personnelle_affichee", "adresse"),
                ):
                    if not str(getattr(associe, field) or "").strip():
                        blockers.append(f"Associe {idx} : {name} requise.")
        # Coherence dure exigee par le moteur : somme parts = nb_parts_total,
        # somme apports = capital_social. On la SURFACE en blocage front au lieu
        # de la decouvrir a la generation.
        if nb_parts_total:
            total_parts = sum((a.parts.nb or 0) for a in associes if a.parts)
            if total_parts != nb_parts_total:
                blockers.append(
                    f"Somme des parts ({total_parts}) != total declare ({nb_parts_total})."
                )
        capital = _safe_int(payload.get("capital_social"))
        if capital:
            total_apports = sum(
                _safe_int(a.apport.montant) for a in associes if a.apport
            )
            if total_apports != capital:
                blockers.append(
                    f"Somme des apports ({total_apports}) != capital social ({capital})."
                )
    if structure == "SCS":
        roles = {a.role_statutaire for a in associes if isinstance(associes, list)}
        if "commandite" not in roles or "commanditaire" not in roles:
            blockers.append("SCS : au moins un commandite ET un commanditaire requis.")
    if _scm_satellites_pair_active(payload):
        # Satellites SCM (pacte + liste depenses) generes -> champs requis.
        if not str(payload.get("pacte_ville_tribunal") or "").strip():
            blockers.append("Ville du tribunal requise (pacte d'associes SCM).")
        if not str(payload.get("societe_numero_rcs") or "").strip():
            blockers.append(
                "N° RCS de la SCM requis pour le pacte (ou « en cours de constitution »)."
            )
    blockers.extend(_validate_common_docs(payload, structure))
    blockers.extend(_validate_option_is(payload, structure))
    return tuple(dict.fromkeys(blockers))


def _validate_option_is(payload: dict[str, object], structure: str) -> list[str]:
    """Champs requis par la lettre d'option IS (DOC-022) quand l'option est active."""
    if not bool(payload.get("option_is")) or structure not in OPTION_IS_STRUCTURES:
        return []
    blockers: list[str] = []
    required = (
        ("siren", "SIREN de la societe requis (option IS)."),
        ("impots_service", "Service du centre des impots requis (option IS)."),
        ("impots_centre", "Centre des impots requis (option IS)."),
        ("impots_adresse_ligne_1", "Adresse (ligne 1) du centre des impots requise (option IS)."),
        ("impots_adresse_ligne_2", "Adresse (ligne 2) du centre des impots requise (option IS)."),
        ("impots_cp", "Code postal du centre des impots requis (option IS)."),
        ("impots_ville", "Ville du centre des impots requise (option IS)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    return blockers


def _validate_common_docs(payload: dict[str, object], structure: str) -> list[str]:
    """Champs requis par les documents communs du bundle (DNC, procuration, PV)."""
    blockers: list[str] = []
    required = (
        ("signataire_nom_pere", "Nom du pere du signataire requis (declaration)."),
        ("signataire_nom_mere", "Nom de la mere du signataire requis (declaration)."),
        ("signataire_adresse_num", "No de voie du signataire requis (declaration)."),
        ("signataire_adresse_voie", "Voie du signataire requise (declaration)."),
        ("signataire_adresse_cp", "Code postal du signataire requis (declaration)."),
        ("signataire_adresse_ville", "Ville du signataire requise (declaration)."),
    )
    for field_name, message in required:
        if not str(payload.get(field_name) or "").strip():
            blockers.append(message)
    if payload.get("decision_date") is None:
        blockers.append("Date de decision requise (PV nomination gerant).")
    signataire = _signataire_associe(payload)
    if signataire is not None:
        for field_name, name in (
            ("date_naissance", "date de naissance"),
            ("ville_naissance", "ville de naissance"),
            ("departement_naissance", "departement de naissance"),
            ("nationalite", "nationalite"),
        ):
            if not str(getattr(signataire, field_name) or "").strip():
                blockers.append(f"Signataire : {name} requise (documents communs).")
    if structure == "SCM":
        ordre_required = (
            ("ordre_conseil", "Conseil departemental de l'ordre requis (SCM)."),
            ("ordre_departement", "Departement d'inscription a l'ordre requis (SCM)."),
            ("ordre_adresse_ligne_1", "Adresse de l'ordre requise (SCM)."),
            ("ordre_cp", "Code postal de l'ordre requis (SCM)."),
            ("ordre_ville", "Ville de l'ordre requise (SCM)."),
        )
        for field_name, message in ordre_required:
            if not str(payload.get(field_name) or "").strip():
                blockers.append(message)
    return blockers


def _signataire_associe(payload: dict[str, object]) -> StatutsCivilsAssocie | None:
    associes = payload.get("associes") or []
    if not isinstance(associes, list):
        return None
    for associe in associes:
        if associe.type_personne == "personne_physique":
            return associe
    return associes[0] if associes else None


def _associe_named(associe: StatutsCivilsAssocie) -> bool:
    if associe.type_personne == "personne_morale":
        return bool((associe.denomination or "").strip())
    return bool((associe.prenom or "").strip()) and bool((associe.nom or "").strip())


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    structure = str(payload["structure"])
    statuts_type = str(payload["statuts_type"])
    associes: list[StatutsCivilsAssocie] = list(payload.get("associes") or [])

    siege = Address(
        num_voie=str(payload.get("siege_num") or ""),
        voie=str(payload.get("siege_voie") or ""),
        cp=str(payload.get("siege_cp") or ""),
        ville=str(payload.get("siege_ville") or ""),
        adresse_affichee=_siege_display(payload),
    )
    capital = str(payload.get("capital_social") or "")
    nb_parts = int(payload.get("nb_parts_total") or 0)

    statuts_civils = StatutsCivilsContext(
        type=statuts_type,
        forme_sociale=str(payload.get("forme_sociale") or structure),
        mention_capital_variable="a capital variable",
        capital_social=capital,
        capital_social_lettres=number_words_from_value(capital),
        capital_autorise=str(int(_safe_int(capital) * 10)) if _safe_int(capital) else None,
        capital_autorise_lettres=number_words_from_value(_safe_int(capital) * 10)
        if _safe_int(capital)
        else None,
        capital_maximal=str(int(_safe_int(capital) * 10)) if _safe_int(capital) else None,
        capital_maximal_lettres=number_words_from_value(_safe_int(capital) * 10)
        if _safe_int(capital)
        else None,
        nb_parts_total=nb_parts,
        nb_parts_total_lettres=number_words_from_value(nb_parts),
        valeur_nominale_part=str(payload.get("valeur_nominale_part") or ""),
        valeur_nominale_part_lettres=number_words_from_value(
            payload.get("valeur_nominale_part")
        )
        or str(payload.get("valeur_nominale_part") or ""),
        plage_parts_totale=f"1 a {nb_parts}" if nb_parts else None,
        duree_societe=str(payload.get("duree_societe") or "99"),
        capital_depot=StatutsCivilsCapitalDepot(
            banque_nom=str(payload.get("banque_nom") or ""),
            banque_adresse=str(payload.get("banque_adresse") or ""),
        ),
        associes=associes,
        date_cloture_premier_exercice=str(payload.get("date_cloture_premier_exercice") or ""),
        nombre_exemplaires_lettres="trois",
        denomination_cabinet_mandataire="DAAT",
    )

    if structure == "SCS":
        statuts_civils.total_apports_commandites = _sum_apports(
            associes, role="commandite"
        )
    if structure == "SCI IRIS":
        _apply_iris_result_groups(statuts_civils, associes)

    option_is = bool(payload.get("option_is")) and structure in OPTION_IS_STRUCTURES
    if option_is:
        _apply_option_is_qualite_associe(associes)

    common = _common_docs_input(payload, structure)
    company = Company(
        denomination=str(payload.get("denomination") or ""),
        denomination_courte=str(payload.get("denomination") or ""),
        forme_sociale=str(payload.get("forme_sociale") or structure),
        forme_sociale_affichage=structure,
        forme_juridique=str(payload.get("forme_sociale") or structure),
        capital=capital,
        capital_social=capital,
        capital_variable=True,
        siege=siege,
        ville_rcs=str(payload.get("ville_rcs") or ""),
        numero_rcs=str(payload.get("societe_numero_rcs") or "") or None,
        nb_parts_total=nb_parts,
        siren=str(payload.get("siren") or "") if option_is else None,
    )

    pv_associes = _pv_associes(associes)
    ctx = DocumentGenerationContext(
        structure=structure,
        dossier_options=_dossier_options(structure, option_is=option_is),
        impots=_centre_impots(payload) if option_is else None,
        personne_signataire=cc.founder_person(common),
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
            nombre_exemplaires=common.signature_nombre_exemplaires,
        ),
        societe=company,
        domiciliation=cc.domiciliation(siege),
        statuts_civils=statuts_civils,
        mandataire=cc.default_mandataire(),
        decision=cc.decision_context(common),
        reunion=cc.reunion_context(common),
        capital=cc.capital_context(common),
        dirigeant_nomine=cc.dirigeant_nomine(common),
        associes=pv_associes,
        metadata={"front_slice": f"track_b_{statuts_type}_v1"},
    )
    if structure == "SCM":
        ctx.ordre = cc.ordre_professionnel(common)
        # Satellites SCM (Rafael 2026-06-08) : pacte + liste depenses, si 2 associes.
        if _scm_satellites_pair_active(payload):
            ctx.scm_satellites = ScmSatellitesOptions(
                pacte_associes=True,
                liste_depenses_communes=True,
            )
            ctx.pacte_associes = PacteAssociesScmContext(
                ville_tribunal=str(payload.get("pacte_ville_tribunal") or "") or None,
            )
    return ctx


def _pv_associes(associes: list[StatutsCivilsAssocie]) -> list:
    """Associes du PV nomination gerant (TOUS presents, parts = totalite).

    Le PV liste tous les associes presents/representes et exige que la somme de
    leurs parts egale le capital. On mappe les associes des statuts (sans inventer
    de donnee) ; une personne morale est rendue par sa denomination.
    """
    from sydel_doc_engine.domain.models import Associe

    mapped: list[Associe] = []
    for associe in associes:
        nb_parts = (associe.parts.nb if associe.parts else 0) or 0
        if associe.type_personne == "personne_morale":
            label = associe.denomination or ""
            mapped.append(
                Associe(
                    genre=Gender.MASCULIN,
                    civilite_affichage="",
                    prenom="",
                    nom=label,
                    nb_parts=nb_parts,
                    nb_parts_lettres=number_words_from_value(nb_parts),
                )
            )
            continue
        mapped.append(
            Associe(
                genre=associe.genre or Gender.MASCULIN,
                civilite_affichage=associe.civilite_affichage or "Monsieur",
                prenom=associe.prenom or associe.prenoms or "",
                nom=associe.nom or "",
                nb_parts=nb_parts,
                nb_parts_lettres=number_words_from_value(nb_parts),
                profession=associe.profession or "",
                profession_reglementee=associe.profession or "",
            )
        )
    return mapped


def _dossier_options(structure: str, *, option_is: bool = False) -> DossierOptions:
    return DossierOptions(
        associe_unique=False,
        scm_satellites=structure == "SCM",
        option_is=option_is,
    )


def _centre_impots(payload: dict[str, object]) -> CentreImpots:
    """Centre des impots destinataire de la lettre d'option IS (DOC-022).

    Mapping direct des saisies utilisateur ; aucune valeur inventee.
    """
    return CentreImpots(
        service=str(payload.get("impots_service") or ""),
        centre=str(payload.get("impots_centre") or ""),
        adresse_ligne_1=str(payload.get("impots_adresse_ligne_1") or ""),
        adresse_ligne_2=str(payload.get("impots_adresse_ligne_2") or ""),
        cp=str(payload.get("impots_cp") or ""),
        ville=str(payload.get("impots_ville") or ""),
    )


def _apply_option_is_qualite_associe(associes: list[StatutsCivilsAssocie]) -> None:
    """Renseigne la qualite d'associe attendue par DOC-022 pour les personnes
    physiques sans qualite explicite.

    La lettre d'option IS decrit chaque associe « ... qualite, detenant N parts ».
    Pour une SCI / SCI IRIS l'associe physique est un simple associe ; on derive la
    seule variante grammaticale genre (associe / associee) documentee au canon,
    sans inventer de regle metier. Une qualite deja saisie n'est jamais ecrasee.
    """
    for associe in associes:
        if associe.type_personne != "personne_physique" or associe.parts is None:
            continue
        if str(associe.parts.qualite_associe or "").strip():
            continue
        feminin = associe.genre == Gender.FEMININ
        associe.parts.qualite_associe = "associée" if feminin else "associé"


def _common_docs_input(payload: dict[str, object], structure: str) -> cc.CommonDocsInput:
    signataire = _signataire_associe(payload)
    profession = ""
    profession_pluriel = ""
    genre = Gender.MASCULIN
    civilite = "Monsieur"
    prenom = ""
    nom = ""
    date_naissance = None
    ville_naissance = ""
    departement_naissance = ""
    nationalite = ""
    if signataire is not None:
        genre = signataire.genre or Gender.MASCULIN
        civilite = signataire.civilite_affichage or "Monsieur"
        prenom = signataire.prenom or signataire.prenoms or ""
        nom = signataire.nom or ""
        profession = signataire.profession or signataire.qualification_principale or ""
        date_naissance = cc.parse_birth_date(signataire.date_naissance)
        ville_naissance = signataire.ville_naissance or ""
        departement_naissance = signataire.departement_naissance or ""
        nationalite = signataire.nationalite or ""
    founder = cc.FounderIdentity(
        genre=genre,
        civilite=civilite,
        prenom=prenom,
        nom=nom,
        titre_affichage=str(payload.get("signataire_titre") or "Docteur"),
        fonction_dirigeant=str(payload.get("signataire_fonction") or "gérant"),
        date_naissance=date_naissance,
        ville_naissance=ville_naissance,
        departement_naissance=departement_naissance,
        nationalite=nationalite,
        nom_pere=str(payload.get("signataire_nom_pere") or ""),
        nom_mere=str(payload.get("signataire_nom_mere") or ""),
        adresse_num_voie=str(payload.get("signataire_adresse_num") or ""),
        adresse_voie=str(payload.get("signataire_adresse_voie") or ""),
        adresse_cp=str(payload.get("signataire_adresse_cp") or ""),
        adresse_ville=str(payload.get("signataire_adresse_ville") or ""),
        qualification_principale=profession,
        profession_pluriel=profession_pluriel,
    )
    return cc.CommonDocsInput(
        founder=founder,
        capital_social=str(payload.get("capital_social") or ""),
        nb_parts_total=int(payload.get("nb_parts_total") or 0),
        valeur_nominale_part=str(payload.get("valeur_nominale_part") or ""),
        siege=cc.CompanyAddress(
            num_voie=str(payload.get("siege_num") or ""),
            voie=str(payload.get("siege_voie") or ""),
            cp=str(payload.get("siege_cp") or ""),
            ville=str(payload.get("siege_ville") or ""),
        ),
        signature_lieu=str(payload.get("signature_lieu") or ""),
        signature_date=payload.get("signature_date"),
        decision_date=payload.get("decision_date"),
        signature_nombre_exemplaires="quatre",
        ordre=cc.OrdreInput(
            conseil_departemental_libelle=str(payload.get("ordre_conseil") or ""),
            departement_inscription=str(payload.get("ordre_departement") or ""),
            adresse_ligne_1=str(payload.get("ordre_adresse_ligne_1") or ""),
            cp=str(payload.get("ordre_cp") or ""),
            ville=str(payload.get("ordre_ville") or ""),
            numero=str(payload.get("ordre_numero") or ""),
        ),
        type_titre="parts sociales",
    )




def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_civil_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    docx_paths = generate_docx_files_for_document_codes(
        ctx,
        output_dir,
        plan.document_codes,
    )
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


# --- helpers internes ---------------------------------------------------------


def _siege_display(payload: dict[str, object]) -> str:
    return (
        f"{payload.get('siege_num', '')} {payload.get('siege_voie', '')}, "
        f"{payload.get('siege_cp', '')} {payload.get('siege_ville', '')}"
    ).strip(" ,")


def _first_physique_or_default(associes: list[StatutsCivilsAssocie]) -> Person:
    for associe in associes:
        if associe.type_personne == "personne_physique" and (associe.nom or "").strip():
            return Person(
                genre=associe.genre or Gender.MASCULIN,
                civilite=associe.civilite_affichage or "Monsieur",
                prenom=associe.prenom or "",
                nom=associe.nom or "",
            )
    # Personne morale uniquement : on derive le signataire de son representant.
    for associe in associes:
        if associe.representant is not None:
            rep = associe.representant
            return Person(
                genre=Gender.MASCULIN,
                civilite=rep.civilite_affichage or "Monsieur",
                prenom=rep.prenom or "",
                nom=rep.nom or "",
            )
    return Person(genre=Gender.MASCULIN, civilite="Monsieur", prenom="", nom="")


def _safe_int(value: object) -> int:
    try:
        cleaned = str(value).replace(" ", "").replace(" ", "").replace(",", ".")
        return int(float(cleaned))
    except (TypeError, ValueError):
        return 0


def _sum_apports(associes: list[StatutsCivilsAssocie], *, role: str) -> str:
    total = 0
    for associe in associes:
        if associe.role_statutaire == role and associe.apport and associe.apport.montant:
            total += _safe_int(associe.apport.montant)
    return str(total) if total else ""


def _apply_iris_result_groups(
    statuts_civils: StatutsCivilsContext,
    associes: list[StatutsCivilsAssocie],
) -> None:
    """SCI IRIS exige des groupes de resultat exceptionnel par plage de parts."""

    total_parts = sum((a.parts.nb or 0) for a in associes if a.parts) or 0
    groupes: list[StatutsCivilsGroupeParts] = []
    if total_parts:
        for associe in associes:
            if associe.parts and associe.parts.nb:
                quote = round(100 * (associe.parts.nb or 0) / total_parts)
                groupes.append(
                    StatutsCivilsGroupeParts(
                        parts_debut=associe.parts.debut,
                        parts_fin=associe.parts.fin,
                        quote_part_resultat_exceptionnel=f"{quote} %",
                    )
                )
    statuts_civils.resultat_groupes_parts = groupes
    statuts_civils.resultat_quote_part_exceptionnel_total = "100 %"


def _text(container, prefix: str, field: str, label: str) -> str:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key)).strip()


def _int(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date_input(prefix: str, field: str, label: str) -> date | None:
    key = f"{prefix}_{field}"
    current = st.session_state.get(key)
    if isinstance(current, date):
        st.session_state[key] = format_french_date(current)
    elif current is None:
        st.session_state[key] = format_french_date(date.today())
    raw = st.text_input(label, key=key, placeholder="JJ/MM/AAAA")
    return parse_french_date(raw)
