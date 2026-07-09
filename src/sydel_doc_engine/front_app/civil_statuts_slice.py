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
    rename_dnc_with_signataire,
)
from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
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
from sydel_doc_engine.front_app._field_inputs import text_input_prefixed
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
)
from sydel_doc_engine.front_app.associe_repeater import RepeaterConfig, render_associe_repeater
from sydel_doc_engine.front_app.dnc_par_associe import generate_dnc_autres_associes
from sydel_doc_engine.front_app.field_derivations import (
    accentuate_french_months,
    calculate_nominal_value,
    format_numeric_value,
    group_montant,
    groupe_montants_associe,
    is_capital_divisible,
    number_words_from_value,
    parse_french_date,
)
from sydel_doc_engine.front_app.front_widgets import (
    date_input_freeform,
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    siege_same_as_perso_checkbox,
)
from sydel_doc_engine.front_app.selas_multi_slice import (
    _associe_filename_slug,
    _associes_maries_communaute,
    _regime_context_for_associe,
    _rename_with_slug,
)
from sydel_doc_engine.generators.lot_02.lettre_avertissement_conjoint import (
    LettreAvertissementConjointGenerator,
)
from sydel_doc_engine.generators.lot_02.lettre_renonciation_associe import (
    LettreRenonciationAssocieGenerator,
)
from sydel_doc_engine.generators.lot_05.liste_souscripteurs_scs import (
    DOCUMENT_CODE as _DOC_LISTE_SOUSCRIPTEURS_SCS,
)
from sydel_doc_engine.generators.lot_05.liste_souscripteurs_scs import (
    ListeSouscripteursScsGenerator,
)

# Mapping structure -> (type statuts civils, doc_code statuts).
CIVIL_TYPE_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SCI": ("sci", "DOC-020"),
    "SCI IRIS": ("sci_iris", "DOC-021"),
    "SCS": ("scs", "DOC-019"),
    "SCM": ("scm", "DOC-025"),
    # Micro holding (Albane 2026-06-26) : societe civile a capital variable, socle civil reutilise.
    "MICRO_HOLDING": ("micro_holding", "DOC-047"),
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
    # Micro holding = societe civile a capital variable.
    "MICRO_HOLDING": "société civile",
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
    # Micro holding : 1 associe minimum (societe civile a capital variable, 1..6).
    "MICRO_HOLDING": 1,
    "SCI IRIS": 2,
    "SCS": 2,
}
CIVIL_NB_MIN_DEFAUT = 2
CIVIL_NB_MAX_ASSOCIES = 6

# Lettre d'option IS (canon « Si IS ») : conditionnel CREATION pour SCI / SCI IRIS.
DOC_OPTION_IS = "DOC-022"
OPTION_IS_STRUCTURES: tuple[str, ...] = ("SCI", "SCI IRIS", "MICRO_HOLDING")

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
    regime_communautaire: bool = False,
) -> tuple[str, ...]:
    codes: list[str] = [statuts_code, *cc.TRONC_COMMUN_CODES, cc.DOC_PV_NOMINATION_GERANT]
    # SCS4 (Albane 2026-06-25) : un associe SCS marie sous communaute legale genere
    # le couple regime (DOC-005 renonciation + DOC-006 avertissement), comme la SELAS
    # pluri. Codes de PLAN (ce qui SERA livre) ; l'emission de fait est per-associe dans
    # generate_dossier (hors orchestrateur, noms de fichiers distincts), pas via l'orchestrateur.
    if regime_communautaire:
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    # SCS5 (Albane 2026-06-25 ; arbitrage Rafael « parts/president ») : liste des souscripteurs
    # SCS = generateur DEDIE (token-replacement du modele SCS, « actions »->« parts », President
    # conserve), emis directement dans generate_dossier (pas via l'orchestrateur de catalog).
    if structure == "SCS":
        codes.append(_DOC_LISTE_SOUSCRIPTEURS_SCS)
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
    # Parite gold (couche partagee) : cloture du 1er exercice pre-remplie « 31 décembre
    # N+1 », modifiable. Le modele civil ne consomme QUE la cloture (pas debut/fin) ->
    # on ne seede pas exercice_debut/fin (difference justifiee).
    seed_closing_date(prefix, field="date_cloture_premier_exercice")
    # RAF-003a : si « siege = adresse perso » coche, recopier l'adresse du gerant
    # (memorisee au run precedent sous des cles stables) dans le siege AVANT son
    # widget (cross-rerun : le gerant est designe dans le repeater, apres le siege).
    # O24-03 : le siege est desormais UN champ une-ligne (`{prefix}_siege_adresse`)
    # -> on recompose la ligne « N° voie, CP Ville » a partir des composants memorises.
    if st.session_state.get(f"{prefix}_siege_same_as_perso"):
        _g = {
            _f: str(st.session_state.get(f"{prefix}_gerant_adresse_{_f}") or "")
            for _f in ("num", "voie", "cp", "ville")
        }
        if any(_g.values()):
            _ligne = f"{_g['num']} {_g['voie']}, {_g['cp']} {_g['ville']}".strip(" ,")
            st.session_state[f"{prefix}_siege_adresse"] = _ligne

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
    )
    duree = "99"

    st.markdown("Siege social")
    siege_same_as_perso_checkbox(prefix)
    # O24-03 (onglet 24) : siege sur UNE ligne (parse interne -> num/voie/cp/ville
    # exiges par la domiciliation [num_voie_siege], la DNC et les statuts civils).
    siege_ligne = _text(st, prefix, "siege_adresse", "Adresse du siège (N° et voie, CP Ville)")
    _siege_struct = _parse_address_full(siege_ligne)
    siege_num = _siege_struct.num_voie if _siege_struct else ""
    siege_voie = _siege_struct.voie if _siege_struct else ""
    siege_cp = _siege_struct.cp if _siege_struct else ""
    siege_ville = _siege_struct.ville if _siege_struct else ""
    ville_rcs = _text(st, prefix, "ville_rcs", "RCS (ville)")

    st.markdown("Depot des fonds")
    col_k, col_l = st.columns(2)
    banque_nom = _text(
        col_k, prefix, "banque_nom", "Banque", hint="ex : CIC CHAPEAU ROUGE BORDEAUX"
    )
    banque_adresse = _text(
        col_l, prefix, "banque_adresse", "Adresse banque", hint="ex : 5 place Bellecour, 69002 Lyon"
    )
    # Retour Rafael 2026-07-01 : cloture pre-remplie (seed_closing_date), recurrente, volet replie.
    with st.expander("Clôture du 1er exercice (pré-rempli — modifier si besoin)", expanded=False):
        date_cloture = date_input_freeform(
            "Date de clôture du 1er exercice (ex : 31 décembre 2028)",
            key=f"{prefix}_date_cloture_premier_exercice",
        )

    st.markdown("**Signature**")
    # Lieu de signature : supprime du questionnaire ; on reprend automatiquement la
    # ville du siege social (retours Albane 2026-06-17, §18.4).
    signature_lieu = siege_ville
    signature_date = _date_input(prefix, "signature_date", "Date de signature")

    # Micro holding (VRAI modele Albane 2026-06-29) : l'objet social (art. 2 « societe civile de
    # portefeuille ») est desormais VERBATIM dans le modele source -> plus de selecteur A/B.

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
            # SCS4 (Albane 2026-06-25) : bloc matrimonial riche (selectbox + conjoint + regime),
            # comme la SELAS pluri, pour la SCS uniquement.
            rich_matrimonial=structure == "SCS",
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
    if structure == "SCS":
        # SCS3 (Albane 2026-06-25) : pour la SCS, champ « Fonction » retire -> toujours « gérant ».
        fonction = "gérant"
        titre = _text(st, prefix, "signataire_titre", "Titre d'affichage") or "Docteur"
    else:
        col_g, col_h = st.columns(2)
        fonction = _text(col_g, prefix, "signataire_fonction", "Fonction (ex: gerant)") or "gérant"
        titre = _text(col_h, prefix, "signataire_titre", "Titre d'affichage") or "Docteur"
    # SU4/SCS2 (Albane) : la date du PV de decision = la date de signature dans TOUS les cas
    # (decision_context la derive de signature_date). Le champ « Date de decision (PV gerant) »
    # dedie etait mort (jamais lu) + requis + trompeur. Supprime du formulaire (#8 onglet 24).
    # SCS1 (Albane 2026-06-25) : pour la SCS, champ conseiller/mandataire retire (pas d'interet a le
    # saisir) -> vide, common_creation le defaulte sur le mandataire SYDEL standard (Jordan ELBAZ).
    # Les autres civils (SCI/SCM) gardent la saisie editable.
    if structure == "SCS":
        mandataire_prenom, mandataire_nom = "", ""
    else:
        mandataire_prenom, mandataire_nom = mandataire_inputs(prefix)

    common: dict[str, object] = {
        "signataire_fonction": fonction,
        "signataire_titre": titre,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
    }

    if structure == "SCM":
        st.markdown("Ordre professionnel (demande d'inscription)")
        col_i, col_j = st.columns(2)
        ordre_conseil = _text(col_i, prefix, "ordre_conseil", "Conseil departemental")
        ordre_dep = _text(col_j, prefix, "ordre_departement", "Departement ordre")
        # O24-03 : adresse de l'ordre sur UNE ligne (parse interne -> ligne_1/cp/ville),
        # comme siege/perso/SELAS multi. Remplace les 3 champs separes ; alimente les
        # MEMES cles -> generateur DOC-034 et gold byte-identique inchanges.
        _ordre_struct = _parse_address_full(
            _text(st, prefix, "ordre_adresse", "Adresse de l'ordre (N° et voie, CP Ville)")
        )
        ordre_ligne = (
            f"{_ordre_struct.num_voie} {_ordre_struct.voie}".strip() if _ordre_struct else ""
        )
        ordre_cp = _ordre_struct.cp if _ordre_struct else ""
        ordre_ville = _ordre_struct.ville if _ordre_struct else ""
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
    # R22-07 : le « Centre » est toujours « Centre des Finances Publiques » (figé dans le
    # generateur) -> plus saisi ici. Seuls le service + l'adresse identifient le destinataire.
    siren = _text(st, prefix, "siren", "SIREN de la societe")
    impots_service = _text(st, prefix, "impots_service", "Service des impots des entreprises (SIE)")
    impots_ligne_1 = _text(st, prefix, "impots_adresse_ligne_1", "Adresse (ligne 1)")
    impots_ligne_2 = _text(st, prefix, "impots_adresse_ligne_2", "Adresse (ligne 2)")
    col_c, col_d = st.columns(2)
    impots_cp = _text(col_c, prefix, "impots_cp", "CP")
    impots_ville = _text(col_d, prefix, "impots_ville", "Ville")
    return {
        "option_is": True,
        "siren": siren,
        "impots_service": impots_service,
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
        # Rafael 2026-07-09 (transverse devise) : l'utilisateur ne tape QUE le montant ;
        # l'unite « euros » est derivee par le moteur (satellites SCM).
        capital = _text(
            col_b,
            prefix,
            f"inter_sel_{idx}_capital",
            "Capital social (affiche)",
            hint="ex : 1 000 (« euros » ajoute automatiquement)",
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
    # R29-06 (Rafael) : vraie date complete (jour+mois+annee) -> selecteur de date
    # (calendrier) + « Aujourd'hui », champ texte JJ/MM/AAAA conserve (saisie verbatim
    # « 1er janvier 2027 » possible), cle session inchangee. seed=False (pas de defaut).
    date_input_with_today(
        "Date d'effet du contrat de frais communs",
        key=f"{prefix}_inter_sel_date_effet",
        value=date.today(),
        seed=False,
    )
    date_effet = str(st.session_state.get(f"{prefix}_inter_sel_date_effet") or "").strip()
    col_r1, col_r2 = st.columns(2)
    # Rafael 2026-07-09 (transverse devise) : montant nu, unite derivee par le moteur.
    seuil = _text(
        col_r1,
        prefix,
        "inter_sel_seuil",
        "Seuil de depense commune",
        hint="ex : 1 500 (« euros » ajoute automatiquement)",
    )
    annee = _text(
        col_r2, prefix, "inter_sel_annee_ref", "Annee de reference des charges", hint="ex : 2027"
    )
    col_r3, col_r4 = st.columns(2)
    # R29-06 (Rafael) : vraie date complete -> selecteur de date + « Aujourd'hui »,
    # champ texte conserve, cle session inchangee. seed=False.
    date_input_with_today(
        "Fin de la cogestion administrative (jusqu'à cette date, gestion conjointe des cogérants)",
        key=f"{prefix}_inter_sel_date_fin_gestion",
        value=date.today(),
        container=col_r3,
        seed=False,
    )
    date_fin = str(st.session_state.get(f"{prefix}_inter_sel_date_fin_gestion") or "").strip()
    # MAJ coherence (Rafael 2026-07-01) : l'ancienne exception R29-06 (garder « Attribution des
    # responsabilites » en text_input car « 1er janvier » recurrent) est LEVEE — on utilise
    # desormais `date_input_freeform` (meme selecteur que toutes les dates) qui EXPOSE un champ
    # texte editable : « 1er janvier » reste saisissable, tout en donnant la parite visuelle
    # (calendrier optionnel) demandee. Idem exercice/cloture partout.
    # Cohérence Rafael 2026-07-01 : meme selecteur que les autres dates du bloc (calendrier +
    # texte). La saisie verbatim « 1er janvier » (recurrent, sans annee) reste possible via le
    # champ texte du widget.
    date_attrib = date_input_freeform(
        "Date d'attribution des responsabilités aux cogérants (ex : 1er janvier)",
        key=f"{prefix}_inter_sel_date_attribution",
        container=col_r4,
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
                    # R5 : capital de la SEL groupe par 3 SI purement numerique ; une
                    # saisie avec unite (« 1 000 euros », hint du champ) reste intacte.
                    capital_social=group_montant(str(sel.get("capital") or "")) or None,
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
    # LIVE-03 : ces 3 dates sont des text_input LIBRES (« 1er aout 2026 ») ; sans
    # re-accentuation EN AMONT, « aout »/« fevrier »/« decembre » partent verbatim dans
    # contrat_frais_communs.docx et reglement_interieur_scm.docx. On accentue ici comme
    # les autres dates de sortie a saisie libre (convention Rafael 2026-06-23).
    frais = FraisCommunsContext(
        date_effet_contrat=(
            accentuate_french_months(str(payload.get("inter_sel_date_effet") or "")) or None
        )
    )
    reglement = ReglementInterieurScmContext(
        # R5 : seuil groupe par 3 SI purement numerique (saisie avec unite intacte).
        seuil_depense_commune=group_montant(str(payload.get("inter_sel_seuil") or "")) or None,
        annee_reference_charges=str(payload.get("inter_sel_annee_ref") or "") or None,
        date_fin_gestion_administrative=(
            accentuate_french_months(str(payload.get("inter_sel_date_fin_gestion") or "")) or None
        ),
        date_attribution_responsabilites=(
            accentuate_french_months(str(payload.get("inter_sel_date_attribution") or "")) or None
        ),
    )
    return parties, praticiens, locaux, frais, reglement


def build_civil_plan(payload: dict[str, object]) -> CivilSlicePlan:
    structure = str(payload["structure"])
    _statuts_type, doc_code = CIVIL_TYPE_BY_STRUCTURE[structure]
    option_is = bool(payload.get("option_is")) and structure in OPTION_IS_STRUCTURES
    scm_pair = _scm_satellites_pair_active(payload)
    regime_actif = bool(_associes_maries_communaute(payload))
    document_codes = _creation_bundle_codes(
        structure,
        doc_code,
        option_is=option_is,
        scm_satellites_pair=scm_pair,
        scm_inter_sel=_scm_inter_sel_active(payload),
        regime_communautaire=regime_actif,
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


def _validate_one_associe(  # noqa: C901
    idx: int,
    associe: StatutsCivilsAssocie,
    structure: str,
) -> list[str]:
    # Extraction C7 de la validation d'UN associe (corps de boucle). Ordre d'append et
    # messages strictement identiques a l'historique.
    blockers: list[str] = []
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
    elif associe.type_personne == "personne_morale":
        # Dogfood 2026-06-22 : le generateur exige l'identite complete de la
        # personne morale + son representant ; sans eux, crash a la generation.
        for field, name in (
            ("forme_juridique", "forme juridique"),
            ("capital_social", "capital social"),
            ("numero_rcs", "numero RCS"),
            ("ville_rcs", "ville du RCS"),
        ):
            if not str(getattr(associe, field, "") or "").strip():
                blockers.append(
                    f"Associe {idx} (personne morale) : {name} requise."
                )
        siege = getattr(associe, "siege", None)
        if siege is None or not str(getattr(siege, "adresse_affichee", "") or "").strip():
            blockers.append(f"Associe {idx} (personne morale) : siege requis.")
        rep = getattr(associe, "representant", None)
        if (
            rep is None
            or not str(getattr(rep, "prenom", "") or "").strip()
            or not str(getattr(rep, "nom", "") or "").strip()
        ):
            blockers.append(
                f"Associe {idx} (personne morale) : representant (prenom + nom) requis."
            )
    return blockers


def _validate_associes(
    associes: list[StatutsCivilsAssocie],
    structure: str,
    nb_parts_total: int,
    payload: dict[str, object],
) -> list[str]:
    # Extraction C7 du corps `else` de la validation des associes. Ordre d'append et
    # messages strictement identiques a l'historique.
    blockers: list[str] = []
    # SCI standard + associe personne morale = AUTORISE (ratifie Rafael 2026-06-08).
    if structure == "SCI IRIS" and not any(
        a.type_personne == "personne_morale" for a in associes
    ):
        blockers.append("SCI IRIS : au moins une personne morale associee requise.")
    for idx, associe in enumerate(associes, start=1):
        blockers.extend(_validate_one_associe(idx, associe, structure))
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
    return blockers


def _validate_scs(
    associes: list[StatutsCivilsAssocie],
    payload: dict[str, object],
) -> list[str]:
    # Extraction C7 du bloc SCS. Logique et messages strictement identiques.
    blockers: list[str] = []
    roles = {a.role_statutaire for a in associes if isinstance(associes, list)}
    if "commandite" not in roles or "commanditaire" not in roles:
        blockers.append("SCS : au moins un commandite ET un commanditaire requis.")
    # Source NotebookLM (validee) : « legalement seul le commandite gere, le
    # commanditaire n'est qu'apporteur de capitaux » et « ne s'immisce pas dans la
    # gestion » -> le gerant designe doit etre un commandite.
    gerant = _signataire_associe(payload)
    if gerant is not None and gerant.role_statutaire == "commanditaire":
        blockers.append(
            "SCS : le gerant doit etre un associe commandite ; le commanditaire est un "
            "simple apporteur de capitaux et ne gere pas la societe."
        )
    return blockers


def _validate_scm_satellites_pair(payload: dict[str, object]) -> list[str]:
    # Extraction C7 du bloc satellites SCM. Logique et messages strictement identiques.
    blockers: list[str] = []
    # Satellites SCM (pacte + liste depenses) generes -> champs requis.
    if not str(payload.get("pacte_ville_tribunal") or "").strip():
        blockers.append("Ville du tribunal requise (pacte d'associes SCM).")
    if not str(payload.get("societe_numero_rcs") or "").strip():
        blockers.append(
            "N° RCS de la SCM requis pour le pacte (ou « en cours de constitution »)."
        )
    return blockers


def _validate(payload: dict[str, object]) -> tuple[str, ...]:  # noqa: C901
    blockers: list[str] = []
    structure = str(payload["structure"])
    if not str(payload.get("denomination") or "").strip():
        blockers.append("Denomination sociale requise.")
    if not str(payload.get("capital_social") or "").strip():
        blockers.append("Capital social requis.")
    elif _safe_int(payload.get("capital_social")) <= 0:
        # Dogfood 2026-06-22 : « 0 » passe la garde de presence -> societe « au capital de
        # 0 euros ». Le capital doit etre strictement positif.
        blockers.append("Capital social doit etre superieur a zero.")
    nb_parts_total = int(payload.get("nb_parts_total") or 0)
    if nb_parts_total < 1:
        blockers.append("Nombre total de parts requis et superieur a zero.")
    # Valeur nominale : calculee (capital / nb parts), plus saisie (§18.2). On bloque
    # donc sur capital + nb parts (deja valides), jamais sur la valeur elle-meme.
    # Dogfood 2026-06-22 : capital non divisible par le nb de parts -> valeur nominale a
    # 28 chiffres dans l'acte + lettres cassees. Garde de divisibilite (couche partagee).
    if not is_capital_divisible(payload.get("capital_social"), payload.get("nb_parts_total")):
        blockers.append(
            "Le capital social doit etre divisible par le nombre de parts "
            "(la valeur nominale d'une part doit etre un nombre entier)."
        )
    if not str(payload.get("siege_ville") or "").strip():
        # Le lieu de signature reprend la ville du siege (§18.4) : bloquer sur siege.
        blockers.append("Ville du siege requise.")
    if not str(payload.get("ville_rcs") or "").strip():
        blockers.append("Ville RCS requise.")
    if not str(payload.get("banque_nom") or "").strip():
        blockers.append("Banque de depot des fonds requise.")
    if not str(payload.get("banque_adresse") or "").strip():
        # Dogfood 2026-06-22 : le generateur exige l'adresse de la banque
        # (capital_depot.banque_adresse) ; sans elle, crash a la generation.
        blockers.append("Adresse de la banque de depot requise.")
    if not str(payload.get("date_cloture_premier_exercice") or "").strip():
        blockers.append("Date de cloture du premier exercice requise.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    associes = payload.get("associes") or []
    if not isinstance(associes, list) or not associes:
        blockers.append("Au moins un associe requis.")
    else:
        # C7 : la validation par associe + coherence parts/apports est extraite telle
        # quelle (meme ordre d'append, memes messages). Comportement inchange.
        blockers.extend(_validate_associes(associes, structure, nb_parts_total, payload))
    if structure == "SCS":
        blockers.extend(_validate_scs(associes, payload))
    if _scm_satellites_pair_active(payload):
        blockers.extend(_validate_scm_satellites_pair(payload))
    blockers.extend(_validate_inter_sel(payload))
    blockers.extend(_validate_common_docs(payload, structure))
    blockers.extend(_validate_associes_dnc(payload))
    blockers.extend(_validate_option_is(payload, structure))
    return tuple(dict.fromkeys(blockers))


def _validate_associes_dnc(payload: dict[str, object]) -> list[str]:
    """DNC par associe (Rafael 2026-07-09) : filiation (noms des parents) requise
    pour CHAQUE associe personne physique autre que le gerant — sa DNC est generee
    d'office. Celle du gerant est deja validee via les cles ``signataire_*``
    (tronc commun, ``_validate_common_docs``)."""
    associes = payload.get("associes") or []
    if not isinstance(associes, list) or not associes:
        return []
    gerant_index = _resolve_gerant_index(payload, associes)
    blockers: list[str] = []
    for idx, associe in enumerate(associes):
        if idx == gerant_index or associe.type_personne != "personne_physique":
            continue
        pere = str(associe.nom_pere or "").strip()
        mere = str(associe.nom_mere or "").strip()
        if not pere or not mere:
            nom = associe.nom or associe.prenom or f"associe {idx + 1}"
            blockers.append(
                f"Associe {nom} : filiation (nom du pere et de la mere) requise "
                "pour sa declaration de non-condamnation."
            )
    return blockers


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
    # SU4/SCS2 (Albane) : plus de blocker « Date de decision » — le champ dedie est supprime du
    # formulaire (la date du PV = la date de signature dans tous les cas, derivee par
    # decision_context). Le champ dataclass CommonDocsInput.decision_date est CONSERVE (il sert de
    # garde de non-regression : un decision_date divergent injecte ne doit JAMAIS sortir).
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
    # R5 (Albane 2026-07-07) : montants des associes (apport individuel, capital d'une
    # personne morale) groupes par 3 a la construction du contexte (copies pydantic,
    # payload jamais mute). MICRO_HOLDING exclu : son modele Albane 2026-06-29 porte sa
    # propre convention (separateur de milliers a POINT, `_fmt_dot_thousands`) — dans le
    # doute entre les deux conventions, on ne touche pas au micro (fidelite au modele).
    associes: list[StatutsCivilsAssocie] = [
        (a if structure == "MICRO_HOLDING" else groupe_montants_associe(a))
        for a in (payload.get("associes") or [])
    ]

    siege = Address(
        num_voie=str(payload.get("siege_num") or ""),
        voie=str(payload.get("siege_voie") or ""),
        cp=str(payload.get("siege_cp") or ""),
        ville=str(payload.get("siege_ville") or ""),
        adresse_affichee=_siege_display(payload),
    )
    # R5 : capital social groupe par 3 (« 60 000 ») a la construction du contexte.
    # MICRO_HOLDING exclu (convention POINT du modele Albane, cf. ci-dessus).
    capital = str(payload.get("capital_social") or "")
    if structure != "MICRO_HOLDING":
        capital = group_montant(capital)
    nb_parts = int(payload.get("nb_parts_total") or 0)
    # Valeurs DERIVEES (retours Albane 2026-06-17) : valeur nominale auto-calculee
    # (§18.2), forme sociale derivee de la structure (§18.1), duree figee a 99 ans
    # (§18.3), lieu de signature = ville du siege (§18.4). On honore une valeur
    # explicite deja presente dans le payload (chemin de test direct), sinon on
    # derive. R5 : groupee par 3 des 4 chiffres.
    valeur_nominale_part = group_montant(
        str(payload.get("valeur_nominale_part") or "")
        or calculate_nominal_value(capital, nb_parts)
    )
    forme_sociale = str(payload.get("forme_sociale") or "") or civil_forme_sociale(structure)
    # SU3 (Albane 2026-06-25) : la ville de signature EST la ville du siege DANS TOUS LES CAS.
    # On FORCE = siege (avant toute valeur de payload divergente). Couvre signature ET renonciation.
    signature_lieu = str(payload.get("siege_ville") or "") or str(
        payload.get("signature_lieu") or ""
    )

    # Micro holding (VRAI modele Albane 2026-06-29) : capital affiche avec separateur de milliers
    # a POINT (« 1.020 » / « 10.200 » comme le modele) ; lettres calculees depuis l'ENTIER
    # (number_words_from_value ne sait pas lire « 1.020 »). Maximum = 10x le minimum saisi.
    # Objet social desormais VERBATIM dans le modele source (plus de variante / token).
    cap_int = _safe_int(capital)
    if structure == "MICRO_HOLDING" and cap_int:
        capital_value = _fmt_dot_thousands(cap_int)
        capital_lettres = number_words_from_value(cap_int)
        capital_maximal_value = _fmt_dot_thousands(cap_int * 10)
        capital_maximal_lettres = number_words_from_value(cap_int * 10)
    else:
        capital_value = capital
        capital_lettres = number_words_from_value(capital)
        # R5 : capital maximal (capital variable, 10x le capital) groupe par 3 —
        # « dix mille euros (10 000 €) » et non « (10000 €) » (statuts SCI / SCI IRIS).
        capital_maximal_value = group_montant(cap_int * 10) if cap_int else None
        capital_maximal_lettres = number_words_from_value(cap_int * 10) if cap_int else None

    statuts_civils = StatutsCivilsContext(
        type=statuts_type,
        forme_sociale=forme_sociale,
        mention_capital_variable="a capital variable",
        capital_social=capital_value,
        capital_social_lettres=capital_lettres,
        capital_autorise=capital_maximal_value,
        capital_autorise_lettres=capital_maximal_lettres,
        capital_maximal=capital_maximal_value,
        capital_maximal_lettres=capital_maximal_lettres,
        nb_parts_total=nb_parts,
        nb_parts_total_lettres=number_words_from_value(nb_parts),
        valeur_nominale_part=valeur_nominale_part,
        valeur_nominale_part_lettres=number_words_from_value(valeur_nominale_part)
        or valeur_nominale_part,
        plage_parts_totale=f"1 à {nb_parts}" if nb_parts else None,  # N4 : « à » accentue
        duree_societe="99",
        capital_depot=StatutsCivilsCapitalDepot(
            banque_nom=str(payload.get("banque_nom") or ""),
            banque_adresse=str(payload.get("banque_adresse") or ""),
        ),
        associes=associes,
        # LIVE-03 : re-accentue le mois saisi librement EN AMONT du generateur.
        date_cloture_premier_exercice=accentuate_french_months(
            str(payload.get("date_cloture_premier_exercice") or "")
        ),
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
        _apply_option_is_qualite_associe(
            associes, structure=structure, gerant_index=_resolve_gerant_index(payload, associes)
        )

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
        # Coherence 2026-06-22 : l'en-tete du PV affichait « SCI IRIS » (cle interne, pas une
        # forme sociale) alors que les statuts disent « societe civile ». « IRIS » est un
        # variant interne -> la forme reelle affichee est « SCI ».
        forme_sociale_affichage=("SCI" if structure == "SCI IRIS" else structure),
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
        dossier_options=_dossier_options(
            structure,
            option_is=option_is,
            regime_communautaire=bool(_associes_maries_communaute(payload)),
        ),
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


def _dossier_options(
    structure: str, *, option_is: bool = False, regime_communautaire: bool = False
) -> DossierOptions:
    return DossierOptions(
        associe_unique=False,
        scm_satellites=structure == "SCM",
        option_is=option_is,
        # SCS4 : active la garde regime des generateurs DOC-005/006 (per-associe).
        regime_communautaire=regime_communautaire,
    )


def _centre_impots(payload: dict[str, object]) -> CentreImpots:
    """Centre des impots destinataire de la lettre d'option IS (DOC-022).

    Mapping direct des saisies utilisateur ; aucune valeur inventee. R22-07 : le centre
    est fige (« Centre des Finances Publiques ») cote generateur, plus saisi -> on le
    renseigne ici pour la coherence du modele.
    """
    return CentreImpots(
        service=str(payload.get("impots_service") or ""),
        centre="Centre des Finances Publiques",
        adresse_ligne_1=str(payload.get("impots_adresse_ligne_1") or ""),
        adresse_ligne_2=str(payload.get("impots_adresse_ligne_2") or ""),
        cp=str(payload.get("impots_cp") or ""),
        ville=str(payload.get("impots_ville") or ""),
    )


def _apply_option_is_qualite_associe(
    associes: list[StatutsCivilsAssocie],
    *,
    structure: str = "",
    gerant_index: int = -1,
) -> None:
    """Renseigne la qualite d'associe attendue par DOC-022 pour les personnes
    physiques sans qualite explicite.

    La lettre d'option IS decrit chaque associe « ... qualite, detenant N parts ».
    Pour une SCI / SCI IRIS l'associe physique est un simple associe (associe / associee).
    Micro holding (Albane 2026-06-29) : l'associe physique GERANT est decrit « gerante »
    (modele Albane « ... gerante, detenant 10 parts ») ; les autres restent « associe(e) ».
    On derive uniquement la variante grammaticale de genre, sans inventer de regle metier.
    Une qualite deja saisie n'est jamais ecrasee.
    """
    for index, associe in enumerate(associes):
        if associe.type_personne != "personne_physique" or associe.parts is None:
            continue
        if str(associe.parts.qualite_associe or "").strip():
            continue
        feminin = associe.genre == Gender.FEMININ
        if structure == "MICRO_HOLDING" and index == gerant_index:
            associe.parts.qualite_associe = "gérante" if feminin else "gérant"
        else:
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
        # R5 : capital groupe par 3 (PV nomination gerant via cc.capital_context).
        # MICRO_HOLDING exclu (convention POINT du modele Albane micro).
        capital_social=(
            str(payload.get("capital_social") or "")
            if structure == "MICRO_HOLDING"
            else group_montant(str(payload.get("capital_social") or ""))
        ),
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
    # SCS4 : DOC-005/006 ne passent PAS par l'orchestrateur (1 doc_id -> 1 fichier de
    # nom fixe ecraserait les couples si plusieurs associes maries). Ils sont retires
    # des codes confies a l'orchestrateur et emis UNE FOIS PAR associe marie ci-dessous
    # (noms de fichiers distincts), exactement comme la SELAS pluri (_generate_regime_par_associe).
    # SCS4 : DOC-005/006 hors orchestrateur (per-associe). SCS5 : DOC-LSS-SCS (liste des
    # souscripteurs SCS) emis directement aussi (token-replacement in-place du modele source,
    # pas un code d'orchestrateur de catalog).
    structure = str(payload["structure"])
    _direct_codes = {*cc.REGIME_COMMUNAUTAIRE_CODES, _DOC_LISTE_SOUSCRIPTEURS_SCS}
    orchestrator_codes = tuple(
        code for code in plan.document_codes if code not in _direct_codes
    )
    docx_paths = generate_docx_files_for_document_codes(
        ctx,
        output_dir,
        orchestrator_codes,
    )
    # O24-02 : la DNC porte le nom du dirigeant (gerant) dans tous les cas.
    docx_paths = rename_dnc_with_signataire(docx_paths, ctx)
    # DNC par associe (Rafael 2026-07-09) : une declaration de non-condamnation PAR
    # associe personne physique. Celle du gerant vient de l'orchestrateur (renommee
    # juste au-dessus) ; on genere celle de chaque AUTRE associe physique, nommee
    # par son nom (helper partage, tous types civils : SCI / SCI IRIS / SCM / SCS /
    # micro holding).
    docx_paths = [*docx_paths, *_generate_dnc_autres_associes_civil(payload, ctx, output_dir)]
    # SCS4 : couple regime (DOC-005/006) per-associe marie sous communaute.
    docx_paths = [*docx_paths, *_generate_regime_civil_par_associe(payload, ctx, output_dir)]
    # SCS5 (Albane 2026-06-25) : liste des souscripteurs (parts/President), SCS uniquement.
    if structure == "SCS":
        docx_paths.append(ListeSouscripteursScsGenerator().generate(ctx, output_dir))
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


# --- helpers internes ---------------------------------------------------------


def _generate_dnc_autres_associes_civil(
    payload: dict[str, object],
    base_ctx: DocumentGenerationContext,
    output_dir: Path,
) -> list[Path]:
    """DNC par associe (Rafael 2026-07-09) : la DNC de chaque associe personne
    physique AUTRE que le gerant (la sienne est produite par l'orchestrateur puis
    renommee O24-02). Helper partage ``generate_dnc_autres_associes`` — les
    personnes morales n'ont pas de DNC."""
    associes = payload.get("associes") or []
    if not isinstance(associes, list) or not associes:
        return []
    gerant_index = _resolve_gerant_index(payload, associes)
    autres = [a for i, a in enumerate(associes) if i != gerant_index]
    return generate_dnc_autres_associes(base_ctx, autres, output_dir)


def _generate_regime_civil_par_associe(
    payload: dict[str, object],
    base_ctx: DocumentGenerationContext,
    output_dir: Path,
) -> list[Path]:
    """SCS4 : emet le couple regime (DOC-005 renonciation + DOC-006 avertissement)
    UNE FOIS PAR associe civil marie sous communaute legale.

    Reprend le mecanisme SELAS pluri (_regime_context_for_associe + renommage par
    associe quand plusieurs maries) mais INJECTE l'apport DE CET associe : le ctx
    civil n'a pas d'apport unique au niveau dossier (chaque associe porte le sien,
    contrairement a la SELAS uni dont le contexte expose un apport unique)."""
    maries = _associes_maries_communaute(payload)
    if not maries:
        return []
    suffix_par_associe = len(maries) > 1
    renonciation_gen = LettreRenonciationAssocieGenerator()
    avertissement_gen = LettreAvertissementConjointGenerator()
    produced: list[Path] = []
    for associe in maries:
        ctx = _regime_context_for_associe(base_ctx, payload, associe)
        # SCS4 (Akainu M1) : DOC-005 (renonciation) lit societe.forme_sociale_complete et
        # DOC-006 (avertissement) lit societe.forme_sociale_abregee. Le Company civil ne pose
        # PAS ces champs (sinon il changerait l'en-tete du PV, qui lit complete en priorite).
        # On les renseigne donc UNIQUEMENT dans le contexte des lettres de regime, derives de
        # la forme civile -> plus de marqueur « (À COMPLÉTER : …) », PV des autres docs intact.
        if ctx.societe is not None:
            societe = ctx.societe
            forme = societe.forme_sociale or ""
            ctx = ctx.model_copy(
                update={
                    "societe": societe.model_copy(
                        update={
                            "forme_sociale_abregee": societe.forme_sociale_abregee
                            or ctx.structure,
                            "forme_sociale_complete": societe.forme_sociale_complete or forme,
                            "forme_sociale_libelle_long": societe.forme_sociale_libelle_long
                            or forme,
                        }
                    )
                }
            )
        if associe.apport is not None:
            ctx = ctx.model_copy(
                update={
                    "apport": Apport(
                        # R5 : apport individuel groupe par 3 (lettres de regime :
                        # « informé de l'apport de 10 000 euros »).
                        montant=(
                            group_montant(associe.apport.montant)
                            if associe.apport.montant
                            else associe.apport.montant
                        ),
                        montant_lettres=(
                            associe.apport.montant_lettres
                            or number_words_from_value(associe.apport.montant)
                        ),
                    )
                }
            )
        rendu_renonciation = renonciation_gen.generate(ctx, output_dir)
        rendu_avertissement = avertissement_gen.generate(ctx, output_dir)
        if suffix_par_associe:
            slug = _associe_filename_slug(associe)
            rendu_renonciation = _rename_with_slug(rendu_renonciation, slug)
            rendu_avertissement = _rename_with_slug(rendu_avertissement, slug)
        produced.append(rendu_renonciation)
        produced.append(rendu_avertissement)
    return produced


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


def _fmt_dot_thousands(value: int) -> str:
    """Separateur de milliers a POINT (« 1.020 », « 10.200 ») — convention du modele Albane
    micro holding (capital minimal / effectif / maximal)."""
    return f"{value:,}".replace(",", ".")


def _sum_apports(associes: list[StatutsCivilsAssocie], *, role: str) -> str:
    total = 0
    for associe in associes:
        if associe.role_statutaire == role and associe.apport and associe.apport.montant:
            total += _safe_int(associe.apport.montant)
    # R5 : total des apports groupe par 3 des 4 chiffres (statuts SCS).
    return group_montant(total) if total else ""


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
    # C2 : helper canonique partage (front_app/_field_inputs). Comportement inchange.
    return text_input_prefixed(container, prefix, field, label, hint)


def _int(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date_input(prefix: str, field: str, label: str) -> date | None:
    # Consomme la couche de rendu partagee (front_widgets) au lieu de reimplementer
    # le helper localement (cause racine des ecarts de parite).
    return date_input_with_today(label, key=f"{prefix}_{field}", value=date.today())
