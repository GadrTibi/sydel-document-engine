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
    FraisCommunsContext,
    LocauxContext,
    PacteAssociesScmContext,
    PartieFraisCommuns,
    Person,
    PraticienScm,
    ReglementInterieurScmContext,
    ScmRepresentant,
    ScmSatellitesOptions,
    ScmSocietePartie,
    Signature,
    StatutsCivilsAssocie,
    StatutsCivilsCapitalDepot,
    StatutsCivilsContext,
    StatutsCivilsGroupeParts,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app.associe_repeater import RepeaterConfig, render_associe_repeater
from sydel_doc_engine.front_app.field_derivations import (
    calculate_nominal_value,
    format_numeric_value,
    number_words_from_value,
    parse_french_date,
)
from sydel_doc_engine.front_app.front_widgets import (
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    siege_same_as_perso_checkbox,
)

# Mapping structure -> (type statuts civils, doc_code statuts).
CIVIL_TYPE_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SCI": ("sci", "DOC-020"),
    "SCI IRIS": ("sci_iris", "DOC-021"),
    "SCS": ("scs", "DOC-019"),
    "SCM": ("scm", "DOC-025"),
}

# Libelle de forme sociale DERIVE automatiquement de la structure (§18.1, retours
# Albane 2026-06-17) : le redacteur ne le saisit plus. La SCM est une societe
# civile de moyens ; les autres civiles (SCI, SCI IRIS, SCS) sont des societes
# civiles classiques.
CIVIL_FORME_SOCIALE_BY_STRUCTURE: dict[str, str] = {
    "SCM": "société civile de moyens",
    "SCI": "société civile",
    "SCI IRIS": "société civile",
    "SCS": "société civile",
}


def civil_forme_sociale(structure: str) -> str:
    """Libelle de forme sociale derive de la structure (§18.1).

    SCM -> « societe civile de moyens » ; toute autre civile -> « societe civile ».
    """
    return CIVIL_FORME_SOCIALE_BY_STRUCTURE.get(structure, "société civile")

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
# DOC-027 (contrat a frais communs) + DOC-028 (reglement interieur) sont des satellites
# INTER-SEL : ils se signent ENTRE les societes d'exercice (SEL) de chaque praticien, pas
# par la SCM. Ils exigent donc une couche de donnees en plus (identite de la SEL de chaque
# associe + telephone + parametres du reglement), inexistante dans la creation SCM simple
# (spec lot_05 SCM-SATELLITES, section 10). Cables en OPT-IN (case decochee par defaut) :
# tranche le point ouvert n2 de la spec par le defaut conservateur. Personnes (representant
# de chaque SEL, praticien) DERIVEES des associes SCM deja saisis -- aucune ressaisie.
DOC_PACTE_ASSOCIES_SCM = "DOC-026"
DOC_LISTE_DEPENSES_SCM = "DOC-030"
DOC_CONTRAT_FRAIS_COMMUNS = "DOC-027"
DOC_REGLEMENT_INTERIEUR_SCM = "DOC-028"


def _creation_bundle_codes(
    structure: str,
    statuts_code: str,
    *,
    option_is: bool = False,
    scm_satellites_pair: bool = False,
    scm_inter_sel: bool = False,
) -> tuple[str, ...]:
    codes: list[str] = [statuts_code, *cc.TRONC_COMMUN_CODES, cc.DOC_PV_NOMINATION_GERANT]
    if structure == "SCM":
        codes.append(cc.DOC_DEMANDE_INSCRIPTION_ORDRE)
        # Satellites SCM (Rafael) : pacte + liste depenses, si exactement 2 associes.
        if scm_satellites_pair:
            codes.append(DOC_LISTE_DEPENSES_SCM)
            codes.append(DOC_PACTE_ASSOCIES_SCM)
        # Satellites inter-SEL (opt-in) : contrat de frais communs + reglement interieur.
        if scm_inter_sel:
            codes.append(DOC_CONTRAT_FRAIS_COMMUNS)
            codes.append(DOC_REGLEMENT_INTERIEUR_SCM)
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


def _scm_inter_sel_active(payload: dict[str, object]) -> bool:
    """Documents inter-SEL (DOC-027/028) : opt-in, sur une SCM a 2 associes physiques."""
    if not _scm_satellites_pair_active(payload):
        return False
    return bool(payload.get("inter_sel_active"))


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
    # Parite gold (couche partagee) : cloture du 1er exercice pre-remplie « 31 decembre
    # N+1 », modifiable. Le modele civil ne consomme QUE la cloture (pas debut/fin) ->
    # on ne seede pas exercice_debut/fin (difference justifiee).
    seed_closing_date(prefix, field="date_cloture_premier_exercice")
    # RAF-003a : si « siege = adresse perso » coche, recopier l'adresse du gerant
    # (memorisee au run precedent sous des cles stables) dans le siege AVANT ses
    # widgets (cross-rerun : le gerant est designe dans le repeater, apres le siege).
    if st.session_state.get(f"{prefix}_siege_same_as_perso"):
        for _f in ("num", "voie", "cp", "ville"):
            _src = st.session_state.get(f"{prefix}_gerant_adresse_{_f}")
            if _src:
                st.session_state[f"{prefix}_siege_{_f}"] = _src

    # Forme sociale (libelle) : DERIVEE de la structure, plus saisie (§18.1).
    forme_sociale = civil_forme_sociale(structure)
    denomination = _text(st, prefix, "denomination", "Denomination sociale")
    col_c, col_d = st.columns(2)
    # Capital en number_input (parite gold shell.py:1430) : interdit « 1000 » brut et
    # le « € » superflu. Stocke en chaine formatee pour l'aval.
    cap_key = f"{prefix}_capital_social"
    if cap_key not in st.session_state:
        st.session_state[cap_key] = 0
    capital_social = format_numeric_value(
        col_c.number_input(
            "Capital social (€)",
            min_value=0,
            step=100,
            key=cap_key,
            help="Montant numerique uniquement (ex : 330 000).",
        )
    )
    nb_parts_total = _int(col_d, prefix, "nb_parts_total", "Nombre total de parts")
    # Valeur nominale d'une part : TOUJOURS calculee (capital / nb parts), jamais
    # saisie (retours Albane 2026-06-17, SCREEN-2 / §18.2). Champ d'affichage seul.
    # Duree de la societe : supprimee du questionnaire, toujours 99 ans (§18.3).
    valeur_nominale = calculate_nominal_value(capital_social, nb_parts_total)
    st.text_input(
        "Valeur nominale d'une part (calculee)",
        value=valeur_nominale,
        disabled=True,
        key=f"{prefix}_valeur_nominale_part_display",
    )
    duree = "99"

    st.markdown("Siege social")
    siege_same_as_perso_checkbox(prefix)
    col_g, col_h, col_i, col_j = st.columns(4)
    siege_num = _text(col_g, prefix, "siege_num", "No")
    siege_voie = _text(col_h, prefix, "siege_voie", "Voie")
    siege_cp = _text(col_i, prefix, "siege_cp", "CP")
    siege_ville = _text(col_j, prefix, "siege_ville", "Ville")
    ville_rcs = _text(st, prefix, "ville_rcs", "RCS (ville)")

    st.markdown("Depot des fonds")
    col_k, col_l = st.columns(2)
    banque_nom = _text(
        col_k, prefix, "banque_nom", "Banque", hint="ex : CIC CHAPEAU ROUGE BORDEAUX"
    )
    banque_adresse = _text(
        col_l, prefix, "banque_adresse", "Adresse banque", hint="ex : 5 place Bellecour, 69002 Lyon"
    )
    date_cloture = _text(
        st, prefix, "date_cloture_premier_exercice", "Cloture du premier exercice"
    )

    st.markdown("**Signature**")
    # Lieu de signature : supprime du questionnaire ; on reprend automatiquement la
    # ville du siege social (retours Albane 2026-06-17, §18.4).
    signature_lieu = siege_ville
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
            collect_dirigeant=True,
            # Profession demandee UNIQUEMENT pour la SCM (§18.6).
            collect_profession=structure == "SCM",
        )
    )
    gerant_index = _derive_gerant_index(associes, prefix)

    common = _render_common_docs_form(structure, prefix)
    # Satellites inter-SEL (opt-in) : DERIVE les personnes des associes deja saisis ;
    # locaux pre-rempli sur le siege de la SCM (souvent identiques). Rendu ici car les
    # associes ne sont disponibles qu'apres le repeater.
    siege_affiche = f"{siege_num} {siege_voie}, {siege_cp} {siege_ville}".strip(" ,")
    inter_sel = _render_scm_inter_sel(prefix, structure, associes, siege_affiche)

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
        "gerant_index": gerant_index,
    }
    payload.update(common)
    payload.update(inter_sel)
    # La DNC / filiation du gerant (saisie sous l'associe coche) alimente les cles
    # signataire_* lues par les documents communs.
    payload.update(_collect_gerant_sig(associes, gerant_index, prefix))
    # RAF-003a : memoriser l'adresse du gerant sous des cles stables pour que la case
    # « siege = adresse perso » puisse la recopier au run suivant (cas multi-associe).
    for _gf in ("num", "voie", "cp", "ville"):
        st.session_state[f"{prefix}_gerant_adresse_{_gf}"] = str(
            payload.get(f"signataire_adresse_{_gf}") or ""
        )
    return payload


def _render_common_docs_form(structure: str, prefix: str) -> dict[str, object]:
    """Documents communs NON lies a l'identite du gerant.

    Les statuts collectent deja l'identite de chaque associe. La filiation +
    l'adresse personnelle du gerant (declaration de non-condamnation, procuration)
    sont desormais saisies SOUS l'associe coche « Dirigeant (gerant) »
    (reunion 2026-06-09 : champs conditionnels au dirigeant). Ce bloc garde la
    fonction / le titre d'affichage, la date de decision (PV), l'ordre (SCM) et
    l'option IS.
    """

    st.markdown("**Documents communs (decision, gerant)**")
    col_g, col_h = st.columns(2)
    fonction = _text(col_g, prefix, "signataire_fonction", "Fonction (ex: gerant)") or "gérant"
    titre = _text(col_h, prefix, "signataire_titre", "Titre d'affichage") or "Docteur"
    decision_date = _date_input(prefix, "decision_date", "Date de decision (PV gerant)")
    # Parite gold (couche partagee) : conseiller/mandataire SYDEL editable (procuration).
    mandataire_prenom, mandataire_nom = mandataire_inputs(prefix)

    common: dict[str, object] = {
        "signataire_fonction": fonction,
        "signataire_titre": titre,
        "decision_date": decision_date,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
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
        # Parite gold (Albane 2026-06-10) : « Madame la Presidente » si la presidente
        # de l'ordre est une femme (demande d'inscription SCM, DOC-034).
        fem_key = f"{prefix}_ordre_president_feminin"
        if fem_key not in st.session_state:
            st.session_state[fem_key] = False
        ordre_president_feminin = st.checkbox(
            "La présidente de l'ordre est une femme",
            key=fem_key,
            help="Coché : « Madame la Présidente » au lieu de « Monsieur le Président ».",
        )
        common.update(
            {
                "ordre_conseil": ordre_conseil,
                "ordre_departement": ordre_dep,
                "ordre_adresse_ligne_1": ordre_ligne,
                "ordre_cp": ordre_cp,
                "ordre_ville": ordre_ville,
                "ordre_numero": ordre_numero,
                "ordre_president_feminin": ordre_president_feminin,
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


def _render_scm_inter_sel(
    prefix: str,
    structure: str,
    associes: list,
    siege_affiche: str,
) -> dict[str, object]:
    """Opt-in : documents inter-SEL (contrat frais communs DOC-027 + reglement DOC-028).

    Ces deux satellites se signent ENTRE les societes d'exercice (SEL) de chaque
    praticien (pas par la SCM). Off par defaut : tranche le point ouvert n2 de la spec
    par le defaut conservateur. Les personnes (representant de chaque SEL, praticien)
    sont DERIVEES des associes SCM deja saisis -- on ne collecte que l'identite de la
    SEL + le telephone + les parametres du contrat / reglement, jamais inventes.
    """
    if structure != "SCM" or not isinstance(associes, list) or len(associes) != 2:
        return {"inter_sel_active": False}
    # Retour Rafael R22-03/04 (2026-06-22) : le contrat de frais communs + le reglement
    # interieur FONT PARTIE du dossier SCM (canon). Champs VISIBLES et generation ACTIVE
    # par defaut (plus d'opt-in cache : Rafael « je ne vois pas les champs »). La bascule
    # reste pour le cas rare d'une SCM a 2 praticiens SANS SEL distincte.
    active_key = f"{prefix}_inter_sel_active"
    if active_key not in st.session_state:
        st.session_state[active_key] = True
    st.markdown("**Documents inter-SEL — contrat de frais communs + reglement interieur**")
    active = st.checkbox(
        "Generer le contrat de frais communs + le reglement interieur "
        "(decocher si SCM sans SEL distincte)",
        key=active_key,
        help="Coche par defaut : ces deux documents font partie du dossier SCM a frais "
        "communs. Decocher seulement si les praticiens n'exercent pas via des SEL distinctes.",
    )
    if not active:
        return {"inter_sel_active": False}
    # Le reglement interieur exige la MEME forme sociale pour les 2 SEL (placeholder
    # source unique). On collecte une forme commune.
    forme_commune = _text(
        st,
        prefix,
        "inter_sel_forme",
        "Forme des SEL (identique pour les 2 parties)",
        hint="ex : SELARL — doit etre identique pour les deux parties",
    )
    parties: list[dict[str, str]] = []
    for idx, associe in enumerate(associes, start=1):
        nom_assoc = (
            f"{getattr(associe, 'prenom', '') or ''} {getattr(associe, 'nom', '') or ''}".strip()
        )
        st.markdown(f"SEL de l'associe {idx} — {nom_assoc or f'associe {idx}'}")
        col_a, col_b = st.columns(2)
        denom = _text(col_a, prefix, f"inter_sel_{idx}_denomination", "Denomination de la SEL")
        capital = _text(
            col_b,
            prefix,
            f"inter_sel_{idx}_capital",
            "Capital social (affiche)",
            hint="ex : 1 000 euros",
        )
        siege = _text(st, prefix, f"inter_sel_{idx}_siege", "Adresse du siege de la SEL")
        col_c, col_d, col_e = st.columns(3)
        ville_rcs = _text(col_c, prefix, f"inter_sel_{idx}_ville_rcs", "RCS (ville)")
        numero_rcs = _text(col_d, prefix, f"inter_sel_{idx}_numero_rcs", "N° RCS")
        tel = _text(
            col_e,
            prefix,
            f"inter_sel_{idx}_telephone",
            "Telephone praticien",
            hint="ex : 01 23 45 67 89",
        )
        parties.append(
            {
                "denomination": denom,
                "capital": capital,
                "siege": siege,
                "ville_rcs": ville_rcs,
                "numero_rcs": numero_rcs,
                "telephone": tel,
            }
        )
    st.markdown("Parametres communs (contrat de frais communs + reglement interieur)")
    titre = (
        _text(st, prefix, "inter_sel_titre", "Titre des representants", hint="ex : Docteur")
        or "Docteur"
    )
    locaux_saisi = _text(
        st,
        prefix,
        "inter_sel_locaux",
        "Adresse des locaux communs",
        hint="souvent le siege de la SCM",
    )
    date_effet = _text(
        st,
        prefix,
        "inter_sel_date_effet",
        "Date d'effet du contrat de frais communs",
        hint="ex : 1er janvier 2027",
    )
    col_r1, col_r2 = st.columns(2)
    seuil = _text(
        col_r1, prefix, "inter_sel_seuil", "Seuil de depense commune", hint="ex : 1 500 euros"
    )
    annee = _text(
        col_r2, prefix, "inter_sel_annee_ref", "Annee de reference des charges", hint="ex : 2027"
    )
    col_r3, col_r4 = st.columns(2)
    date_fin = _text(
        col_r3,
        prefix,
        "inter_sel_date_fin_gestion",
        "Fin de gestion administrative",
        hint="ex : 31 decembre 2027",
    )
    date_attrib = _text(
        col_r4,
        prefix,
        "inter_sel_date_attribution",
        "Attribution des responsabilites",
        hint="ex : 1er janvier",
    )
    return {
        "inter_sel_active": True,
        "inter_sel_forme": forme_commune,
        "inter_sel_titre": titre,
        "inter_sel_parties": parties,
        "inter_sel_locaux": locaux_saisi or siege_affiche,
        "inter_sel_date_effet": date_effet,
        "inter_sel_seuil": seuil,
        "inter_sel_annee_ref": annee,
        "inter_sel_date_fin_gestion": date_fin,
        "inter_sel_date_attribution": date_attrib,
    }


def _build_inter_sel_context(
    payload: dict[str, object],
) -> tuple[
    list[PartieFraisCommuns],
    list[PraticienScm],
    LocauxContext,
    FraisCommunsContext,
    ReglementInterieurScmContext,
]:
    """Construit les pieces de contexte des docs inter-SEL depuis le payload.

    Les personnes (representant de chaque SEL, praticien) sont DERIVEES des associes
    SCM (meme personne : le praticien est le gerant de sa SEL et l'associe de la SCM).
    """
    parties_data = payload.get("inter_sel_parties") or []
    associes = payload.get("associes") or []
    forme = str(payload.get("inter_sel_forme") or "") or None
    titre = str(payload.get("inter_sel_titre") or "Docteur") or None
    parties: list[PartieFraisCommuns] = []
    praticiens: list[PraticienScm] = []
    for idx, sel in enumerate(parties_data):
        associe = associes[idx] if idx < len(associes) else None
        prenom = str(getattr(associe, "prenom", "") or "")
        nom = str(getattr(associe, "nom", "") or "")
        civ = str(getattr(associe, "civilite_affichage", "") or "")
        identite = f"{prenom} {nom}".strip()
        parties.append(
            PartieFraisCommuns(
                societe=ScmSocietePartie(
                    denomination=str(sel.get("denomination") or "") or None,
                    forme_juridique=forme,
                    capital_social=str(sel.get("capital") or "") or None,
                    siege=Address(adresse_affichee=str(sel.get("siege") or "") or None),
                    ville_rcs=str(sel.get("ville_rcs") or "") or None,
                    numero_rcs=str(sel.get("numero_rcs") or "") or None,
                ),
                representant=ScmRepresentant(
                    civilite_affichage=civ or None,
                    prenom=prenom or None,
                    nom=nom or None,
                    identite_affichee=identite or None,
                    titre_affichage=titre,
                    fonction="gérant",
                ),
            )
        )
        praticiens.append(
            PraticienScm(
                identite_affichee=identite or None,
                telephone=str(sel.get("telephone") or "") or None,
            )
        )
    locaux = LocauxContext(adresse_affichee=str(payload.get("inter_sel_locaux") or "") or None)
    frais = FraisCommunsContext(
        date_effet_contrat=str(payload.get("inter_sel_date_effet") or "") or None
    )
    reglement = ReglementInterieurScmContext(
        seuil_depense_commune=str(payload.get("inter_sel_seuil") or "") or None,
        annee_reference_charges=str(payload.get("inter_sel_annee_ref") or "") or None,
        date_fin_gestion_administrative=(
            str(payload.get("inter_sel_date_fin_gestion") or "") or None
        ),
        date_attribution_responsabilites=str(payload.get("inter_sel_date_attribution") or "")
        or None,
    )
    return parties, praticiens, locaux, frais, reglement


def build_civil_plan(payload: dict[str, object]) -> CivilSlicePlan:
    structure = str(payload["structure"])
    _statuts_type, doc_code = CIVIL_TYPE_BY_STRUCTURE[structure]
    option_is = bool(payload.get("option_is")) and structure in OPTION_IS_STRUCTURES
    scm_pair = _scm_satellites_pair_active(payload)
    document_codes = _creation_bundle_codes(
        structure,
        doc_code,
        option_is=option_is,
        scm_satellites_pair=scm_pair,
        scm_inter_sel=_scm_inter_sel_active(payload),
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
    # Valeur nominale : calculee (capital / nb parts), plus saisie (§18.2). On bloque
    # donc sur capital + nb parts (deja valides), jamais sur la valeur elle-meme.
    if not str(payload.get("siege_ville") or "").strip():
        # Le lieu de signature reprend la ville du siege (§18.4) : bloquer sur siege.
        blockers.append("Ville du siege requise.")
    if not str(payload.get("ville_rcs") or "").strip():
        blockers.append("Ville RCS requise.")
    if not str(payload.get("banque_nom") or "").strip():
        blockers.append("Banque de depot des fonds requise.")
    if not str(payload.get("date_cloture_premier_exercice") or "").strip():
        blockers.append("Date de cloture du premier exercice requise.")
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
    blockers.extend(_validate_inter_sel(payload))
    blockers.extend(_validate_common_docs(payload, structure))
    blockers.extend(_validate_option_is(payload, structure))
    return tuple(dict.fromkeys(blockers))


def _validate_inter_sel(payload: dict[str, object]) -> list[str]:
    """Champs requis par les documents inter-SEL (DOC-027/028) quand l'opt-in est actif."""
    if not _scm_inter_sel_active(payload):
        return []
    blockers: list[str] = []
    associes = payload.get("associes") or []
    if isinstance(associes, list) and any(
        getattr(a, "type_personne", "") == "personne_morale" for a in associes
    ):
        blockers.append(
            "Documents inter-SEL : les 2 associes doivent etre des personnes physiques "
            "(la SEL de chacun est la partie)."
        )
    if not str(payload.get("inter_sel_forme") or "").strip():
        blockers.append("Forme des SEL requise (documents inter-SEL).")
    parties = payload.get("inter_sel_parties") or []
    for i, sel in enumerate(parties if isinstance(parties, list) else [], start=1):
        for field_name, label in (
            ("denomination", "denomination"),
            ("capital", "capital social"),
            ("siege", "adresse du siege"),
            ("ville_rcs", "RCS (ville)"),
            ("numero_rcs", "N° RCS"),
            ("telephone", "telephone du praticien"),
        ):
            if not str(sel.get(field_name) or "").strip():
                blockers.append(f"SEL {i} : {label} requis (documents inter-SEL).")
    for field_name, label in (
        ("inter_sel_locaux", "Adresse des locaux communs"),
        ("inter_sel_date_effet", "Date d'effet du contrat de frais communs"),
        ("inter_sel_seuil", "Seuil de depense commune"),
        ("inter_sel_annee_ref", "Annee de reference des charges"),
        ("inter_sel_date_fin_gestion", "Date de fin de gestion administrative"),
        ("inter_sel_date_attribution", "Date d'attribution des responsabilites"),
    ):
        if not str(payload.get(field_name) or "").strip():
            blockers.append(f"{label} requise (documents inter-SEL).")
    return blockers


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
    if not isinstance(associes, list) or not associes:
        return None
    return associes[_resolve_gerant_index(payload, associes)]


def _resolve_gerant_index(
    payload: dict[str, object], associes: list[StatutsCivilsAssocie]
) -> int:
    """Index du gerant (signataire des documents communs).

    Lit `payload["gerant_index"]` (choix UI) ; tombe sur le 1er associe physique
    si absent / invalide / pointant une personne morale. Garantit un signataire
    personne physique (les documents communs decrivent une personne physique).
    """
    default_index = next(
        (i for i, a in enumerate(associes) if a.type_personne == "personne_physique"),
        0,
    )
    raw = payload.get("gerant_index")
    if raw is None:
        return default_index
    try:
        idx = int(raw)
    except (TypeError, ValueError):
        return default_index
    if 0 <= idx < len(associes) and associes[idx].type_personne == "personne_physique":
        return idx
    return default_index


def _derive_gerant_index(associes: list[StatutsCivilsAssocie], prefix: str) -> int:
    """Index du gerant = 1er associe PHYSIQUE coche « Dirigeant (gerant) » ; a
    defaut, le 1er associe physique (historique). Jamais une personne morale."""
    for i, associe in enumerate(associes):
        if associe.type_personne != "personne_physique":
            continue
        if bool(st.session_state.get(f"{prefix}_associe_{i}_is_dirigeant")):
            return i
    return next(
        (i for i, a in enumerate(associes) if a.type_personne == "personne_physique"),
        0,
    )


def _collect_gerant_sig(
    associes: list[StatutsCivilsAssocie], gerant_index: int, prefix: str
) -> dict[str, object]:
    """Filiation du gerant (saisie sous l'associe coche) + adresse REPRISE de
    l'adresse personnelle du meme associe -> cles signataire_*. L'adresse du gerant
    n'est plus saisie a part (§18.5) : on reutilise les champs num/voie/cp/ville de
    son adresse personnelle. L'identite (nom, naissance, nationalite) vient deja de
    l'associe via _common_docs_input ; on ne mappe ici que la DNC propre au gerant."""
    if not (0 <= gerant_index < len(associes)):
        return {}
    p = f"{prefix}_associe_{gerant_index}"
    return {
        "signataire_nom_pere": str(st.session_state.get(f"{p}_sig_nom_pere") or ""),
        "signataire_nom_mere": str(st.session_state.get(f"{p}_sig_nom_mere") or ""),
        "signataire_adresse_num": str(st.session_state.get(f"{p}_adresse_num") or ""),
        "signataire_adresse_voie": str(st.session_state.get(f"{p}_adresse_voie") or ""),
        "signataire_adresse_cp": str(st.session_state.get(f"{p}_adresse_cp") or ""),
        "signataire_adresse_ville": str(st.session_state.get(f"{p}_adresse_ville") or ""),
    }


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
    # Valeurs DERIVEES (retours Albane 2026-06-17) : valeur nominale auto-calculee
    # (§18.2), forme sociale derivee de la structure (§18.1), duree figee a 99 ans
    # (§18.3), lieu de signature = ville du siege (§18.4). On honore une valeur
    # explicite deja presente dans le payload (chemin de test direct), sinon on
    # derive.
    valeur_nominale_part = str(
        payload.get("valeur_nominale_part") or ""
    ) or calculate_nominal_value(capital, nb_parts)
    forme_sociale = str(payload.get("forme_sociale") or "") or civil_forme_sociale(structure)
    signature_lieu = str(payload.get("signature_lieu") or "") or str(
        payload.get("siege_ville") or ""
    )

    statuts_civils = StatutsCivilsContext(
        type=statuts_type,
        forme_sociale=forme_sociale,
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
        valeur_nominale_part=valeur_nominale_part,
        valeur_nominale_part_lettres=number_words_from_value(valeur_nominale_part)
        or valeur_nominale_part,
        plage_parts_totale=f"1 a {nb_parts}" if nb_parts else None,
        duree_societe="99",
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

    common = _common_docs_input(
        payload,
        structure,
        signature_lieu=signature_lieu,
        valeur_nominale_part=valeur_nominale_part,
    )
    company = Company(
        denomination=str(payload.get("denomination") or ""),
        denomination_courte=str(payload.get("denomination") or ""),
        forme_sociale=forme_sociale,
        forme_sociale_affichage=structure,
        forme_juridique=forme_sociale,
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
            lieu=signature_lieu,
            date=payload.get("signature_date"),
            nombre_exemplaires=common.signature_nombre_exemplaires,
        ),
        societe=company,
        domiciliation=cc.domiciliation(siege),
        statuts_civils=statuts_civils,
        mandataire=cc.default_mandataire(
            prenom=str(payload.get("mandataire_prenom") or ""),
            nom=str(payload.get("mandataire_nom") or ""),
        ),
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
            inter_sel = _scm_inter_sel_active(payload)
            ctx.scm_satellites = ScmSatellitesOptions(
                pacte_associes=True,
                liste_depenses_communes=True,
                contrat_frais_communs=inter_sel,
                reglement_interieur=inter_sel,
            )
            ctx.pacte_associes = PacteAssociesScmContext(
                ville_tribunal=str(payload.get("pacte_ville_tribunal") or "") or None,
            )
            if inter_sel:
                (
                    ctx.parties_frais_communs,
                    ctx.praticiens,
                    ctx.locaux,
                    ctx.frais_communs,
                    ctx.reglement_interieur,
                ) = _build_inter_sel_context(payload)
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


def _common_docs_input(
    payload: dict[str, object],
    structure: str,
    *,
    signature_lieu: str = "",
    valeur_nominale_part: str = "",
) -> cc.CommonDocsInput:
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
        valeur_nominale_part=valeur_nominale_part
        or str(payload.get("valeur_nominale_part") or ""),
        siege=cc.CompanyAddress(
            num_voie=str(payload.get("siege_num") or ""),
            voie=str(payload.get("siege_voie") or ""),
            cp=str(payload.get("siege_cp") or ""),
            ville=str(payload.get("siege_ville") or ""),
        ),
        signature_lieu=signature_lieu or str(payload.get("signature_lieu") or ""),
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
            ordre_president_feminin=bool(payload.get("ordre_president_feminin")),
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


def _text(container, prefix: str, field: str, label: str, hint: str | None = None) -> str:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key, help=hint)).strip()


def _int(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date_input(prefix: str, field: str, label: str) -> date | None:
    # Consomme la couche de rendu partagee (front_widgets) au lieu de reimplementer
    # le helper localement (cause racine des ecarts de parite).
    return date_input_with_today(label, key=f"{prefix}_{field}", value=date.today())
