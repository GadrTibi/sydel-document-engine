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
from sydel_doc_engine.utils.dates import format_date_longue_fr
from sydel_doc_engine.domain.models import (
    Address,
    Apport,
    Associe,
    CapitalContext,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    Company,
    DecisionContext,
    DepotFonds,
    DirigeantNomine,
    DocumentContext,
    DocumentGenerationContext,
    DocumentSignataire,
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
    SocieteSpfpl,
    StatutsCivilsAssocie,
    StatutsSelasMultiContext,
    StatutsSelasMultiPresident,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app._field_inputs import text_input_field
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
)
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
    MATRIMONIAL_STATUS_PRESETS,
    accentuate_french_months,
    calculate_nominal_value,
    date_to_french_words,
    derive_gender_from_civilite,
    format_numeric_value,
    is_capital_divisible,
    matrimonial_status_value,
    number_words_from_value,
    pad_birthdate_day,
    parse_associe_birthdate,
    regime_communautaire_from_status,
    situation_maritale_complete,
)
from sydel_doc_engine.front_app.front_widgets import (
    copyable_text_input,
    date_input_with_today,
    date_input_freeform,
    seed_closing_date,
    seed_signature_lieu,
)
from sydel_doc_engine.generators.lot_01.declaration_non_condamnation import (
    DeclarationNonCondamnationGenerator,
)
from sydel_doc_engine.generators.lot_02.lettre_avertissement_conjoint import (
    LettreAvertissementConjointGenerator,
)
from sydel_doc_engine.generators.lot_02.lettre_renonciation_associe import (
    LettreRenonciationAssocieGenerator,
)
from sydel_doc_engine.orchestrator.service import (
    BAIL_AVENANT_DOCUMENT_ID,
    CESSION_CABINET_DOCUMENT_IDS,
)

STRUCTURE = "SELAS"
DOC_CODE = "DOC-044"
# ANO-045 : attestation sur le capital / liste des souscripteurs SELAS (DOC-045).
# Requise au canon pour tout dossier SELAS (case_catalog SELAS ->
# attestation_capital_souscripteurs_selas), mais uniquement CONSTRUCTIBLE quand tous
# les souscripteurs sont des personnes PHYSIQUES et que leur somme d'actions == total
# (le modele d'Albane ne represente QUE des souscripteurs physiques : « au Dr X »).
DOC_ATTESTATION_SELAS = "DOC-045"
PREFIX = "selas"

# Nombre de pages (en lettres) par defaut de l'acte de cession de cabinet, requis
# par le generateur cession_cabinets_common (_required_document). Valeur IDENTIQUE
# au gold SELARL (selarl_slice.CESSION_DOCUMENT_PAGES_LETTRES_DEFAUT = "vingt") :
# la SELAS reutilise les memes generateurs de cession -> meme defaut. Locale (pas
# d'import inter-slice) pour garder la slice SELAS autonome.
CESSION_DOCUMENT_PAGES_LETTRES_DEFAUT = "vingt"

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

# Profession pre-reglee par cle de type enregistre. Retours Rafael 2026-06-23 :
# le cas unique « SELAS pluripersonnelle » choisit la profession DANS le cas ->
# AUCUN pre-reglage (defaut = 1re option du menu ; le moteur bascule sur le corpus
# dentiste/medecin selon le choix). Le dict reste pour une eventuelle extension.
_PROFESSION_DEFAULTS_BY_TYPE: dict[str, str] = {}


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
    # ANO-045 : l'attestation sur le capital / liste des souscripteurs (DOC-045) fait
    # partie du livrable SELAS canon, mais UNIQUEMENT quand le dossier est attestable
    # (tous les souscripteurs physiques, somme des actions == total). Un dossier avec
    # un associe PERSONNE MORALE (ou une somme d'actions incoherente) ne l'inclut pas :
    # le modele d'Albane ne represente que des souscripteurs physiques (« au Dr X ») et
    # le generateur leverait sinon (contrainte somme actions). Pas de plan menteur.
    if _selas_attestable(payload):
        codes.append(DOC_ATTESTATION_SELAS)
    if _regime_communautaire_actif(payload):
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    codes.extend(_cession_codes(payload))
    return tuple(codes)


def _selas_attestable(payload: dict[str, object]) -> bool:
    """ANO-045 : le dossier SELAS peut-il produire l'attestation souscripteurs (DOC-045) ?

    Vrai UNIQUEMENT si TOUS les associes sont des personnes PHYSIQUES et que la somme
    de leurs actions == le nombre total d'actions (apports en numeraire, capital SELAS).
    Le modele d'Albane ne represente QUE des souscripteurs physiques (« ... actions
    attribuees au Dr X ») ; aucun wording n'existe pour un souscripteur personne
    morale. Un associe morale ou une somme d'actions incoherente rend le dossier
    NON-ATTESTABLE (l'attestation est alors omise du plan et du bundle).
    """
    associes = [
        a
        for a in (payload.get("associes") or [])
        if isinstance(a, StatutsCivilsAssocie)
    ]
    if not associes:
        return False
    if any(a.type_personne != "personne_physique" for a in associes):
        return False
    nb_actions_total = int(payload.get("nb_actions_total") or 0)
    if nb_actions_total < 1:
        return False
    total = sum(int(a.nb_actions or 0) for a in associes)
    return total == nb_actions_total


def _cession_codes(payload: dict[str, object]) -> tuple[str, ...]:
    """Codes des documents de cession (cabinet medical/dentaire, bail, appel de
    fonds, cession SCM) selon les contextes saisis. Meme logique que la SELARL :
    on derive les codes des contextes cession/bail/scm_cession presents dans le
    payload (sous-formulaires SELARL reutilises en prefix='selas')."""
    codes: list[str] = []
    cession_ctx = payload.get("cession_context")
    bail_ctx = payload.get("bail_context")
    scm_ctx = payload.get("scm_cession_context")
    if cession_ctx is not None:
        type_cabinet = (getattr(cession_ctx, "type_cabinet", "") or "").strip().lower()
        # #14 (onglet 24) : en SELAS, l'ACTE ET le COMPROMIS sont produits ENSEMBLE
        # pour le type de cabinet -> on ne filtre plus sur l'etape saisie (devenue
        # indicative ; l'orchestrateur genere les deux, cf. _cession_cabinet_enabled).
        for doc_id, (_exp_etape, exp_type) in CESSION_CABINET_DOCUMENT_IDS.items():
            if type_cabinet == exp_type:
                codes.append(doc_id)
        # ANO-008 : l'appel de fonds (DOC-008) est restreint a la SELARL cote moteur
        # (_appel_fonds_enabled) et n'est PAS clairement requis pour la SELAS au canon.
        # On ne l'inscrit donc PLUS au plan SELAS (sinon il serait annonce mais jamais
        # genere -> plan menteur). Question metier flaggee : la SELAS cession doit-elle
        # generer un appel de fonds comme la SELARL ? -> a confirmer Albane avant d'ouvrir
        # la porte cote moteur (et de verifier le rendu sur contexte SELAS).
    if bail_ctx is not None:
        codes.append(BAIL_AVENANT_DOCUMENT_ID)
    if scm_ctx is not None:
        codes.extend(("DOC-031", "DOC-032", "DOC-033"))
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
    # ANO-045 : l'attestation souscripteurs (DOC-045, nom de fichier fixe) passe par
    # l'orchestrateur generique quand le dossier est attestable (tous physiques + somme
    # d'actions == total). Sinon elle est omise (cf. _selas_attestable / plan).
    if _selas_attestable(payload):
        codes.append(DOC_ATTESTATION_SELAS)
    if bool(payload.get("regime_communautaire")):
        # Toggle global : chemin historique inchange (un couple, nom fixe).
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    # Sinon (chemin per-associe), DOC-005/006 sont emis hors orchestrateur.
    codes.extend(_cession_codes(payload))
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
    # Retours Rafael 2026-06-23 : cas unique « SELAS pluripersonnelle » a profession
    # LIBRE (choisie au menu) -> plus aucun pre-reglage par cle (le moteur bascule sur
    # le corpus dentiste/medecin selon le choix). L'appel reste pour extension future.
    _apply_type_profession_default(type_key)
    # RAF-006 (parite gold, couche partagee) : cloture du 1er exercice pre-remplie
    # « 31 décembre N+1 », modifiable. Libelle TEXTUEL (comme le gold), pas un picker.
    seed_closing_date(PREFIX)
    st.subheader("Donnees a saisir")
    st.markdown("**Societe (SELAS d'exercice, vocabulaire actions)**")
    # O24-03 : plus de champ « Siege (adresse affichee) » libre — le siege est saisi sur
    # UNE ligne plus bas et son affichage en est derive (anti double-saisie / une adresse
    # = un champ).
    denomination = _t(st, "denomination", "Denomination")
    col_c, _ = st.columns(2)
    # R1 (retours Rafael 2026-06-18) : profession en menu deroulant ferme ; le
    # pluriel n'est plus saisi mais derive automatiquement du choix.
    profession, profession_pluriel = _render_profession_selectbox(col_c)
    col_e, col_f, col_g = st.columns(3)
    # Capital en number_input (parite gold shell.py:1430-1437) : interdit « 1000 »
    # brut et le « € » superflu. Pattern _i (seed session_state, pas de value= pour
    # eviter le warning value+key) ; stocke en chaine formatee pour l'aval.
    cap_key = f"{PREFIX}_capital_social"
    if cap_key not in st.session_state:
        st.session_state[cap_key] = 0
    capital = format_numeric_value(
        col_e.number_input(
            "Capital social (€)",
            min_value=0,
            step=100,
            key=cap_key,
            help="Montant numerique uniquement (ex : 330 000).",
        )
    )
    nb_actions = _i(col_f, "nb_actions_total", "Nombre total d'actions")
    # Valeur nominale d'une action : TOUJOURS calculee (capital / nb actions),
    # jamais saisie (retours Albane 2026-06-17, SCREEN-2). Champ d'affichage seul.
    # R13 (Rafael 2026-06-23) : PAS de `key` ici -> sinon Streamlit fige la valeur
    # initiale (« value= » + « key= » = la 1re valeur, vide tant que capital=0) et
    # ne la rafraichit jamais. Sans key, le champ affiche la valeur courante recalculee.
    valeur_action = calculate_nominal_value(capital, nb_actions)
    col_g.text_input(
        "Valeur nominale d'une action (calculee)",
        value=valeur_action,
        disabled=True,
    )
    col_h, col_i = st.columns(2)
    ville_rcs = _t(col_h, "ville_rcs", "RCS (ville)")
    adresse_exercice = _t(col_i, "adresse_lieu_exercice", "Adresse lieu d'exercice")

    st.markdown("Depot des fonds")
    col_j, col_k = st.columns(2)
    banque_nom = _t(col_j, "banque_nom", "Banque", hint="ex : CIC CHAPEAU ROUGE BORDEAUX")
    banque_adresse = _t(
        col_k, "banque_adresse", "Adresse banque", hint="ex : 5 place Bellecour, 69002 Lyon"
    )
    # Retour Rafael 2026-07-01 : cloture pre-remplie (seed_closing_date) et recurrente -> volet replie.
    with st.expander("Clôture du 1er exercice (pré-rempli — modifier si besoin)", expanded=False):
        date_cloture = date_input_freeform(
            "Date de clôture du 1er exercice (ex : 31 décembre 2028)",
            key=f"{PREFIX}_date_cloture",
        )

    # O24-03 (onglet 24) : siege sur UNE ligne (parse interne -> num_voie/voie/cp/ville
    # exiges par la domiciliation [num_voie_siege] et la procuration). La case « siege =
    # lieu d'exercice » est RETIREE ici : O24-12 la replace sur l'adresse du CABINET en
    # cession (verbatim : « adresse du cabinet -> case meme adresse que le lieu d'exercice »).
    siege_ligne = _t(st, "siege_adresse", "Adresse du siège (N° et voie, CP Ville)")
    _siege_struct = _parse_address_full(siege_ligne)
    siege_num = _siege_struct.num_voie if _siege_struct else ""
    siege_voie = _siege_struct.voie if _siege_struct else ""
    siege_cp = _siege_struct.cp if _siege_struct else ""
    siege_ville = _siege_struct.ville if _siege_struct else ""
    siege = _siege_struct.adresse_affichee if _siege_struct else ""  # O24-03 : affichage derive

    # Parite gold (anti double-saisie, RAF-003, couche partagee) : lieu de signature
    # pre-rempli = ville du siege, modifiable.
    seed_signature_lieu(PREFIX, siege_ville)

    st.markdown("**Signature**")
    col_l, col_m = st.columns(2)
    signature_lieu = _t(col_l, "signature_lieu", "Lieu de signature")
    with col_m:
        signature_date = _date("signature_date", "Date de signature")

    associes, president_index, dirigeant_sig, dirigeants_nomines = _render_selas_associes()
    # RAF-003a : memoriser l'adresse structuree du president sous des cles stables
    # pour que la case « siege = adresse president » puisse la recopier au run suivant
    # (le bloc president est rendu APRES le siege -> recopie differee d'un run).
    for _f in ("num", "voie", "cp", "ville"):
        st.session_state[f"{PREFIX}_president_adresse_{_f}"] = str(
            dirigeant_sig.get(f"signataire_adresse_{_f}") or ""
        )
    common = _render_common_docs_form()
    cession_context, bail_context, scm_cession_context = _render_selas_cession(
        associes,
        president_index,
        dirigeant_sig,
        denomination=denomination,
        capital=capital,
        ville_rcs=ville_rcs,
        siege_num=siege_num,
        siege_voie=siege_voie,
        siege_cp=siege_cp,
        siege_ville=siege_ville,
        profession=profession,
        adresse_exercice=adresse_exercice,
        ordre_departement=str(common.get("ordre_departement") or ""),
        signature_date=signature_date,
    )

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
        "cession_context": cession_context,
        "bail_context": bail_context,
        "scm_cession_context": scm_cession_context,
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
    st.markdown("**Documents communs (ordre professionnel)**")
    # SU4/SCS2 (Albane) : la date du PV de decision = la date de signature dans TOUS les
    # cas ; le champ « Date de decision » dedie etait mort (jamais lu — DecisionContext
    # plus bas derive la date de signature_date). Supprime (#8 onglet 24 — champ trompeur).
    st.markdown("Ordre professionnel (demande d'inscription)")
    # R5 (retours Rafael 2026-06-18) : « Conseil departemental » supprime du
    # formulaire (inutile) ; le libelle est derive automatiquement cote moteur.
    # R6 : connecteur grammatical (« de » / « du ») a cote du departement, pour
    # gerer l'accord (« ... de Gironde » / « ... du Jura »).
    col_i, col_j = st.columns(2)
    ordre_dep = _t(col_i, "ordre_departement", "Departement ordre")
    ordre_connecteur = _render_connecteur_selectbox(col_j)
    # O24-03 (onglet 24) : adresse de l'ordre sur UNE ligne (comme perso/siège, « ...
    # la voie, etc.. »), parse interne -> ligne_1/cp/ville (OrdreAddress). Plus de champs séparés.
    _ordre_struct = _parse_address_full(
        _t(st, "ordre_adresse", "Adresse de l'ordre (N° et voie, CP Ville)")
    )
    ordre_ligne = f"{_ordre_struct.num_voie} {_ordre_struct.voie}".strip() if _ordre_struct else ""
    ordre_cp = _ordre_struct.cp if _ordre_struct else ""
    ordre_ville = _ordre_struct.ville if _ordre_struct else ""
    ordre_numero = _t(st, "ordre_numero", "Numero d'inscription")
    # Parite gold (retour Albane 2026-06-10, shell.py:1537-1542) : president(e) de
    # l'ordre = femme -> « Madame la Presidente » dans la demande d'inscription (DOC-034).
    feminin_key = f"{PREFIX}_ordre_president_feminin"
    if feminin_key not in st.session_state:
        st.session_state[feminin_key] = False
    ordre_president_feminin = st.checkbox(
        "La présidente de l'ordre est une femme",
        key=feminin_key,
        help="Coche : « Madame la Présidente » au lieu de « Monsieur le Président ».",
    )
    # Parite gold (Albane 2026-06-10, shell.py:1543-1565) : conseiller/mandataire
    # SYDEL editable (defaut « Jordan ELBAZ »), au lieu d'etre code en dur.
    mand_prenom_key = f"{PREFIX}_mandataire_prenom"
    mand_nom_key = f"{PREFIX}_mandataire_nom"
    if not st.session_state.get(mand_prenom_key):
        st.session_state[mand_prenom_key] = DEFAULT_MANDATAIRE_PRENOM
    if not st.session_state.get(mand_nom_key):
        st.session_state[mand_nom_key] = DEFAULT_MANDATAIRE_NOM
    col_man_a, col_man_b = st.columns(2)
    # O24-04 : icône « copier » sur les champs Conseiller (re-Akainu O24-04, MAJEUR M2).
    mandataire_prenom = copyable_text_input(col_man_a, "Conseiller (prénom)", key=mand_prenom_key)
    mandataire_nom = copyable_text_input(col_man_b, "Conseiller (nom)", key=mand_nom_key)
    # R11 (Rafael 2026-06-23) : plus de case « Régime communautaire » GLOBALE — la
    # situation matrimoniale PAR associé (menu) pilote désormais le régime + les docs
    # DOC-005/006. (Le chemin global reste géré côté payload pour les tests directs.)
    return {
        "ordre_departement": ordre_dep,
        "ordre_connecteur": ordre_connecteur,
        "ordre_adresse_ligne_1": ordre_ligne,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
        "ordre_numero": ordre_numero,
        "ordre_president_feminin": ordre_president_feminin,
        "mandataire_prenom": mandataire_prenom or DEFAULT_MANDATAIRE_PRENOM,
        "mandataire_nom": mandataire_nom or DEFAULT_MANDATAIRE_NOM,
    }


def _render_connecteur_selectbox(container) -> str:
    """Menu « de » / « du » (R6) : connecteur grammatical place avant le
    departement de l'ordre dans le libelle derive (gestion de l'accord)."""
    return str(
        container.selectbox(
            "Connecteur (de / du / des)",
            ("de", "du", "des"),
            key=f"{PREFIX}_ordre_connecteur",
            help="S'affiche avant le departement : « ... de Gironde » / « ... du Jura » "
            "/ « ... des Hauts de Seine ».",
        )
    )


def _render_selas_associes() -> tuple[
    list[StatutsCivilsAssocie], int, dict[str, object], list[dict[str, object]]
]:
    if _count_key() not in st.session_state:
        st.session_state[_count_key()] = SELAS_NB_MIN
    nombre = _associe_count()
    cols = st.columns([1, 1, 3])
    if cols[0].button("Ajouter un associe", key=f"{PREFIX}_add"):
        st.session_state[_count_key()] = min(SELAS_NB_MAX, nombre + 1)
    if cols[1].button("Retirer un associe", key=f"{PREFIX}_remove"):
        st.session_state[_count_key()] = max(SELAS_NB_MIN, nombre - 1)
    # N5 (Albane 2026-06-24) : re-lire le nombre APRES +/- au lieu de st.rerun(). Le st.rerun()
    # se declenchait AVANT le rendu de la boucle associes -> Streamlit garbage-collectait l'etat
    # des widgets associes (non instancies sur ce run) -> les champs des associes PRECEDENTS
    # etaient EFFACES. Sans rerun, la boucle rend directement le nouveau nombre, etat preserve.
    nombre = _associe_count()
    st.markdown(
        f"**Associes ({nombre})** — {SELAS_NB_MIN} a {SELAS_NB_MAX}, exercants / non exercants"
    )
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
        # #8 / B4 : identite, adresse structuree et date reprises de l'ASSOCIE
        # (saisies une seule fois) ; plus aucune lecture des cles `_sig_*`.
        adresse = associe.adresse_personnelle
        payload.append(
            {
                "ref_associe_index": index,
                "fonction_affichage": role,
                "civilite_affichage": associe.civilite_affichage or "Monsieur",
                "prenom": associe.prenom or associe.prenoms or "",
                "nom": associe.nom or "",
                "genre": associe.genre or Gender.MASCULIN,
                # Date de naissance ISO derivee du champ texte de l'associe pour la
                # phrase d'identite du PV ; fallback sur la date « en lettres ».
                "date_naissance_iso": parse_associe_birthdate(associe.date_naissance),
                "date_naissance_affichee": associe.date_naissance,
                "ville_naissance": associe.ville_naissance,
                "departement_naissance": associe.departement_naissance,
                "nationalite": associe.nationalite,
                # A26-PV5 : profession + situation maritale de l'associe pour la phrase
                # d'identite complete du PV (modele PV nominations dirigeants SELAS :
                # « ..., <profession>, de nationalite ..., ne le ..., <situation maritale>, ... »).
                "profession": associe.profession,
                "situation_maritale": associe.situation_maritale,
                # Adresse personnelle structuree de l'associe.
                "adresse_num": str((adresse.num_voie if adresse else "") or ""),
                "adresse_voie": str((adresse.voie if adresse else "") or ""),
                "adresse_cp": str((adresse.cp if adresse else "") or ""),
                "adresse_ville": str((adresse.ville if adresse else "") or ""),
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

    Retours Rafael 2026-06-23 : chaque associe choisit UN role parmi President,
    Directeur General et Directeur General Associe (ce dernier MANQUAIT). Cardinalite
    (onglet 24) : 1 President, 1 Directeur General, plusieurs DG Associes. Le President
    reste le signataire du tronc commun (DNC / procuration / statuts) ; le DG et les
    DG Associes ajoutent chacun une decision de nomination au PV (le PV rend le role
    de facon generique).

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
        ("Président", "Directeur Général", "Directeur Général Associé"),
        key=role_key,
        help=(
            "Le Président signe le tronc commun ; le Directeur Général et le Directeur "
            "Général Associé ajoutent chacun une décision de nomination au PV."
        ),
    )
    # #8 / B4 (onglet 24) : la filiation (parents) est la SEULE info propre au
    # dirigeant pour la DNC. L'adresse personnelle ET la date de naissance sont
    # reprises de l'associe (saisies une seule fois plus haut) -> plus de re-saisie.
    st.caption("Declaration de non-condamnation du dirigeant (filiation des parents)")
    col_a, col_b = st.columns(2)
    _ts(col_a, f"{prefix}_sig_nom_pere", "Nom du pere")
    _ts(col_b, f"{prefix}_sig_nom_mere", "Nom de la mere")


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

    Le dirigeant pilote (president_index) vient en PREMIERE decision ; les autres
    dirigeants physiques coches suivent dans l'ordre des associes. Ignore les
    personnes morales (un dirigeant SELAS est une personne physique).

    Racine O24-07 (re-Akainu 2026-06-23, MAJEUR) : on ne FORCE plus le role
    « President » sur le dirigeant pilote — on lit son role REELLEMENT choisi. Un
    associe explicitement « Directeur General » n'est donc plus requalifie
    silencieusement « President ». Si le pilote n'a pas de role explicite (chemin
    par defaut / bare-payload), _dirigeant_role retombe sur « President » (un SELAS
    a structurellement un president). Le cas « dirigeants designes mais AUCUN
    president » est un etat invalide bloque en amont par _validate_roles_dirigeants.
    """
    dirigeants: list[tuple[int, str]] = []
    if 0 <= president_index < len(associes):
        dirigeants.append((president_index, _dirigeant_role(president_index)))
    for i, associe in enumerate(associes):
        if i == president_index:
            continue
        if associe.type_personne != "personne_physique":
            continue
        if not bool(st.session_state.get(f"{PREFIX}_associe_{i}_is_dirigeant")):
            continue
        dirigeants.append((i, _dirigeant_role(i)))
    return dirigeants


def _validate_roles_dirigeants(associes: list[StatutsCivilsAssocie]) -> list[str]:
    """#7 (onglet 24) : cardinalite des roles de direction.

    Un seul President et un seul Directeur General sont admis ; les Directeurs
    Generaux Associes peuvent etre PLUSIEURS (retours Rafael 2026-06-23). On bloque
    donc seulement si plus d'un associe coche « President » ou « Directeur General »."""
    roles = [
        _dirigeant_role(i)
        for i, associe in enumerate(associes)
        if associe.type_personne == "personne_physique"
        and bool(st.session_state.get(f"{PREFIX}_associe_{i}_is_dirigeant"))
    ]
    blockers: list[str] = []
    # O24-07 : un Président est OBLIGATOIRE (« soit président (un seul) » = cardinalité 1,
    # bornée par le bas aussi). Sans ce blocage, un associé désigné DG/DGA serait
    # requalifié « Président » par le fallback de _derive_president_index, écrasant le rôle
    # choisi — incohérence relevée par l'audit.
    # Ne bloque QUE si des dirigeants sont désignés sans aucun Président (cas UI réel ;
    # le chemin bare-payload sans état de dirigeants a un president_index déjà résolu).
    if roles and roles.count("Président") == 0:
        blockers.append(
            "Un Président est obligatoire : désignez un associé dirigeant « Président »."
        )
    if roles.count("Président") > 1:
        blockers.append(
            "Un seul Président est admis : les fonctions de direction ne sont pas cumulatives."
        )
    if roles.count("Directeur Général") > 1:
        blockers.append(
            "Un seul Directeur Général est admis : les fonctions de direction "
            "ne sont pas cumulatives."
        )
    return blockers


def _validate_dirigeants_filiation(
    payload: dict[str, object], associes: list[StatutsCivilsAssocie]
) -> list[str]:
    """R7 (Rafael 2026-06-23) : une DNC par dirigeant -> la filiation (nom du père et
    de la mère) est requise pour CHAQUE dirigeant autre que le président (celle du
    président est déjà validée via le tronc commun)."""
    president_index = _resolve_president_index(payload, associes)
    blockers: list[str] = []
    for index, _role in _collect_dirigeants_nomines_indices(associes, president_index):
        if index == president_index:
            continue
        prefix = f"{PREFIX}_associe_{index}"
        pere = str(st.session_state.get(f"{prefix}_sig_nom_pere") or "").strip()
        mere = str(st.session_state.get(f"{prefix}_sig_nom_mere") or "").strip()
        if not pere or not mere:
            nom = associes[index].nom or associes[index].prenom or f"associé {index + 1}"
            blockers.append(
                f"Dirigeant {nom} : filiation (nom du père et de la mère) requise "
                "pour sa déclaration de non-condamnation."
            )
    return blockers


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
    # #8 / B4 : adresse + date reprises de l'ASSOCIE (saisies une seule fois) ; seule
    # la filiation reste propre a la case « Dirigeant ».
    adresse = dirigeant.adresse_personnelle
    return {
        "signataire_nom_pere": str(st.session_state.get(f"{prefix}_sig_nom_pere") or ""),
        "signataire_nom_mere": str(st.session_state.get(f"{prefix}_sig_nom_mere") or ""),
        "signataire_adresse_num": str((adresse.num_voie if adresse else "") or ""),
        "signataire_adresse_voie": str((adresse.voie if adresse else "") or ""),
        "signataire_adresse_cp": str((adresse.cp if adresse else "") or ""),
        "signataire_adresse_ville": str((adresse.ville if adresse else "") or ""),
        "signataire_nationalite": str(dirigeant.nationalite or ""),
        "signataire_titre": str(dirigeant.profession or "Docteur"),
        "signataire_date_naissance": parse_associe_birthdate(dirigeant.date_naissance),
    }


def _physique(prefix: str, nb_actions: int, montant: str) -> StatutsCivilsAssocie:
    col_a, col_b, col_c = st.columns(3)
    civilite = col_a.selectbox(
        "Civilite",
        ("Madame", "Monsieur"),
        key=f"{prefix}_civilite",
    )
    genre = derive_gender_from_civilite(civilite)
    prenoms = _ts(col_b, f"{prefix}_prenoms", "Prenom(s)")
    nom = _ts(col_c, f"{prefix}_nom", "Nom")
    col_d, col_e, col_f = st.columns(3)
    # R29-06 (Rafael) : selecteur de date (calendrier) + « Aujourd'hui » sur la date de
    # naissance des associes SELAS multi. Champ texte JJ/MM/AAAA conserve comme source
    # editable (saisie verbatim « 1er aout 1985 » possible), cle `{prefix}_date_naissance`
    # inchangee -> pad_birthdate_day + accentuation aval preserves. seed=False (pas de
    # date du jour sur une naissance). On relit la chaine texte (pas l'objet date).
    date_input_with_today(
        "Date naissance (ex: 1 janvier 1980)",
        key=f"{prefix}_date_naissance",
        value=date.today(),
        container=col_d,
        seed=False,
    )
    date_naissance = str(st.session_state.get(f"{prefix}_date_naissance") or "").strip()
    ville_naissance = _ts(col_e, f"{prefix}_ville_naissance", "Ville naissance")
    departement = _ts(col_f, f"{prefix}_departement", "Departement naissance")
    nationalite = render_nationalite_selectbox(prefix, container=st)
    # #9 (onglet 24) : le champ « profession » est RETIRE du formulaire (redondant
    # avec la qualification). Le titre « Docteur » est derive (defaut) pour NE PAS
    # changer le texte de l'acte (comparution « Docteur [qualification] »).
    # [QUESTION RAFAEL accumulee (docs/review/QUESTIONS_RAFAEL.md #9) : garder
    # « Docteur » ou n'afficher que la qualification ? -> defaut le plus sur ici.]
    profession = "Docteur"
    # #8 / B4 (onglet 24) : adresse personnelle STRUCTUREE saisie UNE SEULE FOIS ici
    # (comme le gold). Elle alimente la comparution (affichage derive), la DNC /
    # procuration du dirigeant ET l'avertissement au conjoint -> plus de re-saisie
    # sous la case « Dirigeant » ni de champ de foyer separe.
    # O24-03 (onglet 24) : adresse personnelle sur UNE ligne, pas de champ separe.
    # Parse interne (num_voie/voie/cp/ville) car DOC-001 (DNC), DOC-006 (avertissement
    # conjoint) et le regime communautaire exigent l'adresse structuree complete.
    adresse_ligne = _ts(st, f"{prefix}_adresse", "Adresse personnelle (N° et voie, CP Ville)")
    adresse_struct = _parse_address_full(adresse_ligne)
    adresse = adresse_struct.adresse_affichee if adresse_struct else ""
    col_i, col_j = st.columns(2)
    # R10/R11 (Rafael 2026-06-23) : situation matrimoniale = MENU (comme la SELARL),
    # plus de texte libre ni de case « marié sous régime communautaire ». Quand le
    # régime de la COMMUNAUTÉ est choisi -> champs conjoint + DOC-005/006 générés.
    situation_label = col_i.selectbox(
        "Situation matrimoniale", MATRIMONIAL_STATUS_PRESETS, key=f"{prefix}_situation"
    )
    qualification = _ts(col_j, f"{prefix}_qualification", "Qualification principale (profession)")
    col_k, col_l, col_m = st.columns(3)
    ordre_dep = _ts(col_k, f"{prefix}_ordre_dep", "Departement ordre")
    numero_ordre = _ts(col_l, f"{prefix}_numero_ordre", "Numero ordre")
    numero_rpps = _ts(col_m, f"{prefix}_numero_rpps", "Numero RPPS")
    qualite = _ts(st, f"{prefix}_qualite", "Qualite au capital (ex: associee exercante)")
    regime_associe = _render_conjoint_si_communaute(prefix, situation_label)
    # ST4 (Albane 2026-06-26) : la comparution d'un associe MARIE doit porter le REGIME
    # (« marie(e) sous le regime de ... ») ET le nom du conjoint, pas un « marie » nu.
    # Le conjoint est saisi pour TOUT associe marie (cles de session ci-dessous, posees
    # par _render_conjoint_si_communaute juste au-dessus).
    situation_maritale = situation_maritale_complete(
        situation_label,
        genre,
        conjoint_civilite=str(st.session_state.get(f"{prefix}_conjoint_civilite") or ""),
        conjoint_prenom=str(st.session_state.get(f"{prefix}_conjoint_prenom") or ""),
        conjoint_nom=str(st.session_state.get(f"{prefix}_conjoint_nom") or ""),
    )

    return StatutsCivilsAssocie(
        type_personne="personne_physique",
        genre=genre,
        civilite_affichage=civilite,
        prenom=prenoms,
        prenoms=prenoms,
        nom=nom,
        # LIVE-03 : date de naissance a saisie LIBRE (text_input « 1 janvier 1980 »)
        # -> re-accentue les mois avant injection ; le generateur reste un echo fidele.
        # ST3 (Albane 2026-06-26) : jour de 1 a 9 zero-pade (« 01 janvier 1980 »).
        date_naissance=(
            pad_birthdate_day(accentuate_french_months(date_naissance))
            if date_naissance
            else None
        ),
        ville_naissance=ville_naissance or None,
        departement_naissance=departement or None,
        nationalite=nationalite or None,
        profession=profession or None,
        situation_maritale=situation_maritale,
        # #8 / B4 : adresse personnelle STRUCTUREE (saisie une seule fois). Sert la
        # comparution (affichage derive), la DNC du dirigeant et l'avertissement au
        # conjoint (foyer = domicile). Repli president supprime : toujours renseignee.
        adresse_personnelle=adresse_struct,
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


def _render_conjoint_si_communaute(
    prefix: str, situation_label: str
) -> RegimeCommunautaireAssocie | None:
    """Conjoint d'UN associe physique.

    Affiche le sous-formulaire conjoint (civilite/prenom/nom) pour tout associe
    MARIE (re-Akainu 2026-06-23, MAJEUR O24-11 : le conjoint du vendeur doit figurer
    a l'acte de cession pour TOUS les regimes maries — separation, communaute
    universelle, participation aux acquets —, pas seulement la communaute legale,
    comme le fait deja la SELARL). Les coordonnees vivent dans les cles de session
    `{prefix}_conjoint_*` et sont lues telles quelles par le sous-formulaire de cession.

    PERIMETRE PACS (re-Akainu tour 2, MAJEUR O24-11) : le PACS est VOLONTAIREMENT EXCLU.
    Le verbatim O24-11 vise le vendeur MARIE, et l'acte de cession ne porte pas de
    segment « pacse avec [conjoint] » -> capter le partenaire pacse ferait disparaitre
    une donnee saisie (jamais retranscrite). On s'aligne donc sur « marie » uniquement ;
    le perimetre PACS est un arbitrage Albane en attente (docs/review/QUESTIONS_RAFAEL.md).

    En revanche, l'objet RegimeCommunautaireAssocie — qui DECLENCHE DOC-005
    (renonciation) + DOC-006 (avertissement) — n'est retourne QUE pour la
    communaute LEGALE (R10/R11, Rafael 2026-06-23) : les autres regimes maries
    n'entrainent aucun document complementaire."""
    if matrimonial_status_value(situation_label) != "marie":
        return None
    st.caption("Conjoint de cet associé (figure à l'acte ; lettres si communauté légale)")
    col_a, col_b, col_c = st.columns(3)
    conjoint_civilite = col_a.selectbox(
        "Civilité conjoint",
        ("Madame", "Monsieur"),
        key=f"{prefix}_conjoint_civilite",
    )
    conjoint_prenom = _ts(col_b, f"{prefix}_conjoint_prenom", "Prénom conjoint")
    conjoint_nom = _ts(col_c, f"{prefix}_conjoint_nom", "Nom conjoint")
    # DOC-005/DOC-006 : communaute legale uniquement. Hors communaute legale, le
    # conjoint est capte (cles de session ci-dessus, pour l'acte) mais aucun document
    # de regime n'est genere -> on ne retourne pas d'objet RegimeCommunautaireAssocie.
    if not regime_communautaire_from_status(situation_label):
        return None
    return RegimeCommunautaireAssocie(
        actif=True,
        regime_matrimonial="la communauté légale",
        conjoint_civilite=conjoint_civilite,
        conjoint_genre=derive_gender_from_civilite(conjoint_civilite),
        conjoint_prenom=conjoint_prenom or None,
        conjoint_nom=conjoint_nom or None,
    )


# O24-03 (propagation Q4) — le parser d'adresse une-ligne est extrait dans le golden
# bloc partage `address_oneline` (appele par TOUS les types). Importe en tete sous l'alias
# `_parse_address_full` ; les sites d'appel locaux (siege / ordre / adresse perso) restent
# inchanges. Toute evolution du parsing se fait desormais dans address_oneline, une fois.


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


def _validate(payload: dict[str, object]) -> tuple[str, ...]:  # noqa: C901
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
    # O24-05 (re-Akainu T4) : capital non divisible par le nb d'actions -> valeur nominale
    # fractionnaire (« 3333.333... € ») dans le DOCX / lettres cassees. Garde partagee, meme
    # wording que civil/SAS/SELARL.
    if not is_capital_divisible(payload.get("capital_social"), payload.get("nb_actions_total")):
        blockers.append(
            "Le capital social doit etre divisible par le nombre d'actions "
            "(la valeur nominale d'une action doit etre un nombre entier)."
        )
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
        # #7 (onglet 24) : roles de direction non cumulatifs (1 President, 1 DG max).
        blockers.extend(_validate_roles_dirigeants(associes))
        # R7 : DNC par dirigeant -> filiation requise pour chaque dirigeant non-president.
        blockers.extend(_validate_dirigeants_filiation(payload, associes))
    blockers.extend(_validate_common_docs(payload))
    blockers.extend(_validate_regime_communautaire(payload))
    blockers.extend(_validate_cession_exercices(payload))
    blockers.extend(_validate_scm_cedee_divisibility(payload))
    return tuple(dict.fromkeys(blockers))


def _validate_scm_cedee_divisibility(payload: dict[str, object]) -> list[str]:
    """O24-05 (re-Akainu T4) : en cession SCM, le capital de la SCM cedee doit etre
    divisible par le nb de parts (valeur nominale entiere). Blocker de PLAN (UX) cote
    SELAS, symetrique de selarl_slice.validate_selarl_input ; le generateur
    required_scm_cedee leve de toute facon en aval (plancher universel)."""
    scm_ctx = payload.get("scm_cession_context")
    scm_cedee = getattr(scm_ctx, "scm_cedee", None) if scm_ctx is not None else None
    if scm_cedee is None:
        return []
    if not is_capital_divisible(scm_cedee.capital_social, scm_cedee.nb_parts_total):
        return [
            "Le capital de la SCM cedee doit etre divisible par le nombre de parts "
            "(la valeur nominale d'une part doit etre un nombre entier)."
        ]
    return []


def _validate_cession_exercices(payload: dict[str, object]) -> list[str]:
    """#13 (onglet 24) : en cession, le chiffre d'affaires et le resultat des
    exercices ne sont plus facultatifs. On bloque tant qu'un exercice saisi presente
    un CA ou un resultat vide (n'agit que si une cession de cabinet est active)."""
    cession = payload.get("cession_context")
    if cession is None:
        return []
    blockers: list[str] = []
    for i, exercice in enumerate(getattr(cession, "exercices", None) or [], start=1):
        if not str(getattr(exercice, "chiffre_affaires", "") or "").strip():
            blockers.append(f"Cession : chiffre d'affaires de l'exercice {i} requis.")
        if not str(getattr(exercice, "resultat", "") or "").strip():
            blockers.append(f"Cession : resultat de l'exercice {i} requis.")
    return blockers


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
        # O24-03 : adresse de l'ordre sur une ligne -> un seul blocker (cp/ville derives du parse).
        ("ordre_adresse_ligne_1", "Adresse de l'ordre requise (demande inscription)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    if payload.get("signataire_date_naissance") is None:
        blockers.append("Date de naissance du president requise (declaration).")
    # SU4/SCS2 (Albane) : plus de blocker « Date de decision » — champ supprime (la date du
    # PV = la date de signature dans tous les cas, derivee par DecisionContext).
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


def _render_selas_cession(
    associes: list[StatutsCivilsAssocie],
    president_index: int,
    dirigeant_sig: dict[str, object],
    *,
    denomination: str,
    capital: str,
    ville_rcs: str,
    siege_num: str,
    siege_voie: str,
    siege_cp: str,
    siege_ville: str,
    profession: str,
    adresse_exercice: str = "",
    ordre_departement: str,
    signature_date: object,
):
    """Cession (cabinet medical/dentaire + bail) + cession de parts SCM pour la
    SELAS, en REUTILISANT les sous-formulaires SELARL valides (prefix='selas').

    Vendeur par defaut = le president (modifiable dans le sous-formulaire) ;
    acquereur = la SELAS. Import differe de shell (anti-cycle)."""
    from sydel_doc_engine.front_app import shell

    societe: dict[str, object] = {
        "denomination": denomination,
        "capital_social": capital,
        "ville_rcs": ville_rcs,
        "siege_num_voie": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "lieu_exercice": adresse_exercice,
    }
    ordre = {"departement_ordre": ordre_departement}
    generation = {"signature_date": signature_date}
    physiques = [i for i, a in enumerate(associes) if a.type_personne == "personne_physique"]

    st.markdown("**Cession (optionnel)**")
    cession_on = st.checkbox(
        "Cession de cabinet liberal (medical / dentaire)",
        key="selas_cession_on",
    )
    # #11 (Rafael 2026-06-24) : le SELECTEUR de l'associe vendeur est rendu DANS la section
    # Vendeur du sous-formulaire (shell._render_cession_form), pas en haut du bloc cession.
    # Ici on LIT l'index choisi (pose par ce selectbox au rerun precedent ; defaut = president)
    # pour deriver ses infos -> passees au sous-formulaire qui rend le selecteur au bon endroit.
    _default_vendeur_i = (
        president_index
        if president_index in physiques
        else (physiques[0] if physiques else president_index)
    )
    vendeur_index = _default_vendeur_i
    if cession_on and physiques:
        _picked = st.session_state.get("selas_cession_vendeur_index")
        if isinstance(_picked, int) and _picked in physiques:
            vendeur_index = _picked
    vendeur = associes[vendeur_index] if 0 <= vendeur_index < len(associes) else None
    # Adresse du vendeur : pour le president, on garde la source historique (cles
    # signataire_*, byte-identique) ; pour un autre associe, son adresse structuree.
    if vendeur_index == president_index:
        v_num = str(dirigeant_sig.get("signataire_adresse_num") or "")
        v_voie = str(dirigeant_sig.get("signataire_adresse_voie") or "")
        v_cp = str(dirigeant_sig.get("signataire_adresse_cp") or "")
        v_ville = str(dirigeant_sig.get("signataire_adresse_ville") or "")
    else:
        v_adr = vendeur.adresse_personnelle if vendeur else None
        v_num = str((v_adr.num_voie if v_adr else "") or "")
        v_voie = str((v_adr.voie if v_adr else "") or "")
        v_cp = str((v_adr.cp if v_adr else "") or "")
        v_ville = str((v_adr.ville if v_adr else "") or "")
    # O24-11 : le LIBELLE BRUT du menu situation matrimoniale (preset MATRIMONIAL_STATUS_PRESETS)
    # sert UNIQUEMENT a deriver le regime (separation/universelle/participation) cote cession ;
    # il NE doit PAS partir dans `situation_maritale` (sinon l'acte rend « Marie(e) sous le
    # regime ... » brut, non accentue et double — regression MAJEUR relevee par re-Akainu
    # 2026-06-23). On dissocie comme la SELARL : valeur COLLAPSEE (« marie ») pour l'affichage,
    # libelle BRUT pour le regime (cle de session lue par _vendeur_regime_label).
    # Libelle BRUT du preset (porte le detail du regime) ; '' si la cle de session est absente.
    v_situation_raw = str(
        st.session_state.get(f"{PREFIX}_associe_{vendeur_index}_situation") or ""
    )
    # Affichage : matrimonial_status_value(v_situation_raw) -> 'marie'/'pacse'/... pour
    # _situation_display cote sous-formulaire. PAS de repli vers vendeur.situation_maritale
    # (re-Akainu tour 3, NITPICK O24-11) : cette valeur est DEJA accentuee (« marié ») et
    # matrimonial_status_value la mal-deriverait en 'celibataire' (pas de NFKD). En UI reelle
    # v_situation_raw est toujours renseigne (le selectbox situation a un defaut « Célibataire »).
    # Conjoint du vendeur : lu directement depuis les cles de session de l'associe choisi
    # (captees pour tout associe MARIE, cf. _render_conjoint_si_communaute), donc present
    # meme hors communaute legale ou regime_communautaire_associe est None (MAJEUR O24-11).
    v_conj_prefix = f"{PREFIX}_associe_{vendeur_index}"
    praticien: dict[str, object] = {
        "prenom": (vendeur.prenom or vendeur.prenoms) if vendeur else "",
        "nom": vendeur.nom if vendeur else "",
        "genre": vendeur.genre if vendeur else None,
        "date_naissance": vendeur.date_naissance if vendeur else None,
        "ville_naissance": vendeur.ville_naissance if vendeur else None,
        "departement_naissance": vendeur.departement_naissance if vendeur else None,
        "nationalite": vendeur.nationalite if vendeur else None,
        "numero_ordre": vendeur.numero_ordre if vendeur else None,
        "numero_rpps": vendeur.numero_rpps if vendeur else None,
        "situation_maritale": matrimonial_status_value(v_situation_raw),
        "conjoint_civilite": str(
            st.session_state.get(f"{v_conj_prefix}_conjoint_civilite") or ""
        ),
        "conjoint_prenom": str(st.session_state.get(f"{v_conj_prefix}_conjoint_prenom") or ""),
        "conjoint_nom": str(st.session_state.get(f"{v_conj_prefix}_conjoint_nom") or ""),
        "adresse_num_voie": v_num,
        "adresse_voie": v_voie,
        "adresse_cp": v_cp,
        "adresse_ville": v_ville,
    }
    # Le sous-formulaire de cession derive le regime via cette cle : il lui faut le LIBELLE
    # BRUT du preset (« Marié(e) sous le régime de la communauté universelle »), pas la valeur
    # collapsee — _vendeur_regime_label y lit « universelle »/« participation »/« separation ».
    # On n'y met QUE le libelle brut (jamais le fallback collapse) : a defaut, chaine vide ->
    # aucun regime faussement derive (re-Akainu tour 2, MINEUR O24-11).
    st.session_state["selas_situation_maritale"] = v_situation_raw
    # Matiere du selecteur de vendeur, rendu DANS la section Vendeur du sous-formulaire (#11).
    vendeur_selector = (
        {
            "options": physiques,
            "default": _default_vendeur_i,
            "label": lambda i: _associe_label(associes[i], i),
        }
        if (cession_on and physiques)
        else None
    )
    scm_on = st.checkbox("Cession de parts de SCM", key="selas_scm_cession_on")
    cession_ctx, bail_ctx = shell._render_cession_form(
        cession_on,
        profession,
        praticien=praticien,
        societe=societe,
        ordre=ordre,
        generation=generation,
        prefix="selas",
        vendeur_selector=vendeur_selector,
    )
    scm_ctx = shell._render_scm_cession_form(
        scm_on,
        praticien=praticien,
        societe=societe,
        profession_label=profession,
        ordre=ordre,
        prefix="selas",
    )
    return cession_ctx, bail_ctx, scm_ctx


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
    # B1 (fidelite gold) : le sous-formulaire de cession PARTAGE code l'acquereur en
    # « SELARL » (shell._render_cession_form, cle acquereur_payload["forme_sociale"],
    # hardcode unipersonnel). En SELAS, l'acquereur EST la SELAS creee : on post-corrige
    # sa forme sociale pour que les actes/compromis de cession affichent « SELAS » (meme
    # principe que selas_uni_medecin_slice pour la societe). SELAS-only : le gold SELARL
    # reste intact. (re-Akainu 2026-06-23 : ancre stable, plus de numero de ligne.)
    _cession_ctx = payload.get("cession_context")
    if _cession_ctx is not None and getattr(_cession_ctx, "acquereur", None) is not None:
        _cession_ctx.acquereur.forme_sociale = "SELAS"
    # CABLAGE cession SCM (TACHE A) : le sous-formulaire SCM est REUTILISE de la
    # SELARL (scm_cession_fixture porte variante_structure='selarl'). Or
    # l'orchestrateur n'emet DOC-031/032/033 que si
    # scm_cession.variante_structure == structure du dossier
    # (service._scm_cession_enabled), et le generateur SCM LEVE si la variante ne
    # correspond pas (scm_cession_common.validate_scm_cession_enabled). Sur un
    # dossier SELAS, la variante DOIT donc valoir 'selas', sinon build_selas_plan
    # ANNONCE la cession SCM mais generate_dossier ne l'emet jamais (plan menteur).
    # On aligne la variante sur la structure du dossier — comme la post-correction
    # acquereur=SELAS ci-dessus. Normalise ici (pas dans le rendu du formulaire)
    # pour couvrir TOUTE source de payload (UI, fixtures, appels directs).
    _scm_ctx = payload.get("scm_cession_context")
    if _scm_ctx is not None and getattr(_scm_ctx, "variante_structure", None) is not None:
        _scm_ctx.variante_structure = "selas"
    return DocumentGenerationContext(
        structure="SELAS",
        dossier_options=DossierOptions(
            associe_unique=False,
            regime_communautaire=regime_communautaire_actif,
            cession=payload.get("cession_context") is not None,
            scm_cession=payload.get("scm_cession_context") is not None,
        ),
        cession=payload.get("cession_context"),
        bail=payload.get("bail_context"),
        scm_cession=payload.get("scm_cession_context"),
        # CABLAGE cession (TACHE A) : les generateurs de cession de cabinet
        # (cession_cabinets_common._required_document) ET d'avenant de bail
        # (avenant_contrat_bail._required_document_context) exigent un `document`
        # non nul. Sans lui, le dossier SELAS levait « document est obligatoire
        # pour CODE-CESSION-CAB-001 » et ne generait AUCUN doc de cession. On
        # alimente le contexte comme le gold SELARL (selarl_slice:685) : nombre de
        # pages en lettres SEULEMENT si une cession cabinet est demandee (sinon
        # None, comme la SELARL), exemplaires « quatre » (parite signature SELAS),
        # signataire = le president. Aucun contenu juridique nouveau (echo fidele).
        document=DocumentContext(
            nombre_exemplaires_lettres="quatre",
            nombre_pages_lettres=(
                CESSION_DOCUMENT_PAGES_LETTRES_DEFAUT
                if payload.get("cession_context") is not None
                else None
            ),
            signataire=DocumentSignataire(prenom=prenom, nom=nom),
        ),
        personne_signataire=signataire,
        conjoint=(
            _conjoint_person(regime_payload, conjoint_foyer)
            if regime_communautaire_actif
            else None
        ),
        signature=Signature(
            # SU3 (Albane 2026-06-25) : ville de signature = ville du siege, FORCE au moteur.
            lieu=str(payload.get("siege_ville") or payload.get("signature_lieu") or ""),
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
        mandataire=cc.default_mandataire(
            prenom=str(payload.get("mandataire_prenom") or ""),
            nom=str(payload.get("mandataire_nom") or ""),
        ),
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
        associes=_selas_pv_associes(
            associes,
            profession_reglementee=str(payload.get("profession_reglementee") or ""),
        ),
        # SCS2/SU4 (Albane 2026-06-25, propag. Q4) : date de decision (PV) = date de signature.
        decision=DecisionContext(date=_display_date(payload.get("signature_date"))),
        reunion=ReunionContext(
            # B1/SCS2 (Albane 2026-06-25) : date de reunion (PV) = date de signature.
            date_lettres=date_to_french_words(payload.get("signature_date")),
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
            # LIVE-03 : re-accentue le mois saisi librement EN AMONT du generateur.
            date_cloture_premier_exercice=accentuate_french_months(
                str(payload.get("date_cloture") or "")
            ),
            associes=associes,
            president=StatutsSelasMultiPresident(ref_associe_index=president_index),
        ),
        # ANO-045 : donnees de l'attestation souscripteurs (DOC-045). Construites
        # uniquement pour un dossier ATTESTABLE (tous physiques + somme actions ==
        # total) ; None sinon -> le generateur n'est de toute facon pas au bundle.
        societe_spfpl=_build_societe_spfpl_selas(
            payload, siege_struct, capital, nb_actions_total, valeur_action
        ),
        depot_fonds=_build_depot_fonds_selas(payload),
        capital_souscription=_build_capital_souscription_selas(
            payload, associes, president_index, nb_actions_total, valeur_action, capital
        ),
        metadata={"front_slice": "track_b_selas_multi_v1"},
    )


def _profession_pluriel_capitalise(payload: dict[str, object]) -> str:
    """Profession (pluriel) capitalisee pour l'entete de l'attestation (DOC-045).

    Le modele d'Albane affiche « Societe d'exercice liberale par Actions simplifiees
    de Medecins » : la profession y est au PLURIEL et capitalisee (« Médecins »,
    « Chirurgiens-dentistes »). Le payload porte le pluriel en minuscule
    (`profession_reglementee_pluriel`), on capitalise la 1re lettre. Repli sur la
    profession au singulier si le pluriel est absent (jamais invente)."""
    pluriel = str(
        payload.get("profession_reglementee_pluriel")
        or payload.get("profession_reglementee")
        or ""
    ).strip()
    if not pluriel:
        return ""
    return pluriel[0].upper() + pluriel[1:]


def _build_societe_spfpl_selas(
    payload: dict[str, object],
    siege_struct: Address,
    capital: str,
    nb_actions_total: int,
    valeur_action: str,
) -> SocieteSpfpl | None:
    """SocieteSpfpl requise par le generateur d'attestation souscripteurs (ANO-045).

    None si le dossier n'est pas attestable. `forme_sociale` = libelle long SELAS ;
    `profession` = profession reglementee au pluriel capitalise (parite modele
    d'Albane « ... de Médecins »)."""
    if not _selas_attestable(payload):
        return None
    return SocieteSpfpl(
        denomination=str(payload.get("denomination") or ""),
        forme_sociale="Société d'exercice libéral par actions simplifiée",
        capital_social=capital,
        nb_actions_total=nb_actions_total,
        valeur_nominale_action=valeur_action,
        profession=_profession_pluriel_capitalise(payload),
        siege=siege_struct,
    )


def _build_depot_fonds_selas(payload: dict[str, object]) -> DepotFonds | None:
    """DepotFonds (banque) requis par l'attestation souscripteurs (ANO-045).

    None si le dossier n'est pas attestable. Reutilise la banque deja saisie
    (`banque_nom`)."""
    if not _selas_attestable(payload):
        return None
    return DepotFonds(
        banque=CessionBanque(nom=str(payload.get("banque_nom") or "")),
    )


def _build_capital_souscription_selas(
    payload: dict[str, object],
    associes: list[StatutsCivilsAssocie],
    president_index: int,
    nb_actions_total: int,
    valeur_action: str,
    capital: str,
) -> CapitalSouscription | None:
    """CapitalSouscription (souscripteurs physiques) pour l'attestation (ANO-045).

    None si le dossier n'est pas attestable. Un souscripteur par associe physique
    (civilite / prenom / nom / nb_actions) ; president = l'associe physique a
    `president_index`. La somme des actions == nb_actions_total est garantie par
    `_selas_attestable` (le generateur revalide de toute facon)."""
    if not _selas_attestable(payload):
        return None
    souscripteurs = [
        CapitalSouscripteur(
            civilite_affichage=associe.civilite_affichage or "",
            prenom=associe.prenom or associe.prenoms or "",
            nom=associe.nom or "",
            nb_actions=associe.nb_actions or 0,
        )
        for associe in associes
    ]
    if not (0 <= president_index < len(associes)):
        president_index = 0
    president_associe = associes[president_index]
    # Le generateur rend « certifie ... par le President, {civilite} {prenom} {nom} ».
    # Le modele d'Albane porte le TITRE professionnel a cet emplacement (parite avec
    # « au Dr X » / « Le Docteur X » du corps) : on utilise le titre de l'associe
    # (« Docteur » par defaut en SELAS multi), pas la civilite civile (Monsieur/Madame).
    president = CapitalSouscripteur(
        civilite_affichage=(president_associe.profession or "Docteur"),
        prenom=president_associe.prenom or president_associe.prenoms or "",
        nom=president_associe.nom or "",
    )
    return CapitalSouscription(
        nb_actions_total=nb_actions_total,
        valeur_nominale_action=valeur_action,
        apports_numeraire_montant=capital,
        president=president,
        souscripteurs=souscripteurs,
    )


def _selas_dirigeant_identite_phrase(entry: dict[str, object], adresse: Address | None) -> str | None:
    """A26-PV5 : phrase d'identite COMPLETE du dirigeant pour le PV nomination dirigeant SELAS.

    Format du modele Albane (MODELE_PV_nominations_dirigeants) :
    « <civ> <prenom> <NOM>, <profession>, de nationalite <nat>, <ne/nee> le <date longue>
    a <ville> (<dept>), <situation maritale>, demeurant <adresse> ».
    Renvoie None si la profession n'est PAS fournie -> le PV retombe sur la reconstruction par
    champs (byte-identique ; SELARL/SPFPL et les cas sans profession restent inchanges)."""
    profession = str(entry.get("profession") or "").strip()
    if not profession:
        return None
    civilite = str(entry.get("civilite_affichage") or "Monsieur").strip()
    prenom = str(entry.get("prenom") or "").strip()
    nom = str(entry.get("nom") or "").strip()
    nationalite = str(entry.get("nationalite") or "").strip()
    ville = str(entry.get("ville_naissance") or "").strip()
    dept = str(entry.get("departement_naissance") or "").strip()
    ne = "née" if (entry.get("genre") or Gender.MASCULIN) == Gender.FEMININ else "né"
    iso = entry.get("date_naissance_iso")
    date_txt = (
        format_date_longue_fr(iso)
        if isinstance(iso, date)
        else str(entry.get("date_naissance_affichee") or "").strip()
    )
    adresse_inline = (adresse.adresse_affichee or "").strip() if adresse else ""
    if not adresse_inline and adresse is not None:
        num = (adresse.num_voie or "").strip()
        adresse_inline = (
            f"{num} {(adresse.voie or '').strip()}, "
            f"{(adresse.cp or '').strip()} {(adresse.ville or '').strip()}"
        ).strip()
    situation = str(entry.get("situation_maritale") or "").strip()
    parts = [
        f"{civilite} {prenom} {nom}",
        profession,
        f"de nationalité {nationalite}",
        f"{ne} le {date_txt} à {ville} ({dept})",
    ]
    if situation:
        parts.append(situation)
    return ", ".join(parts) + f", demeurant {adresse_inline}"


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
                # A26-PV5 : phrase d'identite complete (profession + regime + conjoint) du
                # modele SELAS ; None si profession absente -> reconstruction par champs.
                identite_phrase=_selas_dirigeant_identite_phrase(entry, adresse),
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
        destinataire_appel=(
            "Madame la Présidente"
            if bool(payload.get("ordre_president_feminin"))
            else "Monsieur le Président"
        ),
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


def _selas_pv_associes(
    associes: list[StatutsCivilsAssocie],
    *,
    profession_reglementee: str = "",
) -> list[Associe]:
    mapped: list[Associe] = []
    profession_dossier = (profession_reglementee or "").strip()
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
        # A1 (Albane 2026-06-26) : l'entete societe (PV + lettres regime communautaire)
        # doit afficher la PROFESSION REGLEMENTEE du dossier (« médecin » /
        # « chirurgien-dentiste »), pas le titre « Docteur ». En SELAS multi,
        # `associe.profession` porte le titre derive (« Docteur ») ; la profession
        # reglementee canonique du dossier (`payload["profession_reglementee"]`) est la
        # source correcte. Repli : qualification puis profession brute. `profession`
        # (titre) reste intacte pour la comparution de l'acte.
        vraie_profession = (
            profession_dossier
            or (associe.qualification_principale or "").strip()
            or (associe.profession or "").strip()
        )
        mapped.append(
            Associe(
                genre=associe.genre or Gender.MASCULIN,
                civilite_affichage=associe.civilite_affichage or "Monsieur",
                prenom=associe.prenom or associe.prenoms or "",
                nom=associe.nom or "",
                nb_parts=nb,
                nb_parts_lettres=number_words_from_value(nb),
                profession=associe.profession or "",
                profession_reglementee=vraie_profession,
                qualification_principale=vraie_profession or None,
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


def _dnc_context_for_dirigeant(
    base_ctx: DocumentGenerationContext,
    associe: StatutsCivilsAssocie,
    index: int,
) -> DocumentGenerationContext:
    """Contexte DNC d'UN dirigeant (R7, Rafael 2026-06-23) : signataire = ce dirigeant.

    Identite + adresse + date reprises de l'associe (saisie unique, #8) ; filiation
    depuis sa case « Dirigeant » (cles `_sig_nom_pere/mere`)."""
    from sydel_doc_engine.domain.models import Address, Person

    prefix = f"{PREFIX}_associe_{index}"
    adresse = associe.adresse_personnelle or Address()
    person = Person(
        genre=associe.genre or Gender.MASCULIN,
        civilite=associe.civilite_affichage or "Monsieur",
        prenom=associe.prenom or associe.prenoms or "",
        nom=associe.nom or "",
        date_naissance=parse_associe_birthdate(associe.date_naissance),
        ville_naissance=associe.ville_naissance or "",
        departement_naissance=associe.departement_naissance or None,
        nationalite=associe.nationalite or "",
        nom_pere=str(st.session_state.get(f"{prefix}_sig_nom_pere") or ""),
        nom_mere=str(st.session_state.get(f"{prefix}_sig_nom_mere") or ""),
        adresse_perso=adresse,
        adresse_personnelle_affichee=adresse.adresse_affichee,
        qualification_principale=associe.qualification_principale or "",
    )
    return base_ctx.model_copy(update={"personne_signataire": person})


def _generate_dnc_par_dirigeant(
    payload: dict[str, object],
    base_ctx: DocumentGenerationContext,
    docx_paths: list[Path],
    output_dir: Path,
) -> list[Path]:
    """#2 + R7 (Rafael 2026-06-23) : la DNC porte le nom du dirigeant ET il y en a UNE
    PAR dirigeant (President + chaque Directeur General / DG Associe).

    La DNC du president est produite par l'orchestrateur (etape 1) : on la renomme.
    Pour chaque AUTRE dirigeant, on derive un contexte (signataire = ce dirigeant) et
    on genere sa propre DNC, nommee par son nom."""
    associes = list(payload.get("associes") or [])
    president_index = _resolve_president_index(payload, associes)
    if not (0 <= president_index < len(associes)):
        return docx_paths
    pres_slug = _associe_filename_slug(associes[president_index])
    renamed: list[Path] = []
    for path in docx_paths:
        if path.name == "declaration_non_condamnation.docx":
            renamed.append(_rename_with_slug(path, pres_slug))
        else:
            renamed.append(path)
    generator = DeclarationNonCondamnationGenerator()
    for index, _role in _collect_dirigeants_nomines_indices(associes, president_index):
        if index == president_index:
            continue
        ctx = _dnc_context_for_dirigeant(base_ctx, associes[index], index)
        produced = generator.generate(ctx, output_dir)
        renamed.append(_rename_with_slug(produced, _associe_filename_slug(associes[index])))
    return renamed


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
    # 1bis) #2 + R7 (Rafael 2026-06-23) : la DNC porte le nom du dirigeant ET il y en a
    #    UNE PAR dirigeant (President renomme + une generee par DG / DG Associe).
    docx_paths = _generate_dnc_par_dirigeant(payload, ctx, docx_paths, output_dir)
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
    # A5 (Albane 2026-06-26) : le montant de la phrase « en apportant X euros » /
    # « somme en numeraire de X » doit etre l'apport INDIVIDUEL du renoncant, pas le
    # capital social total porte par `base_ctx.apport`. On reconstruit l'apport du
    # contexte par-associe depuis l'apport saisi pour CET associe ; apport individuel
    # absent -> marqueur visible « (À COMPLÉTER) », jamais le capital (M1, Akainu).
    apport_ctx = _apporteur_apport(associe)
    dossier_options = base_ctx.dossier_options or DossierOptions(associe_unique=False)
    return base_ctx.model_copy(
        update={
            "apport": apport_ctx,
            "dossier_options": dossier_options.model_copy(
                update={"regime_communautaire": True}
            ),
            "personne_signataire": apporteur,
            "conjoint": conjoint,
            "regime_communautaire": regime_ctx,
        }
    )


def _apporteur_apport(associe: StatutsCivilsAssocie) -> Apport | None:
    """Apport INDIVIDUEL du renoncant pour les lettres de regime communautaire (A5).

    Prend le montant saisi pour CET associe (`associe.apport`). M1 (Akainu 2026-06-26) :
    si l'apport individuel n'est pas renseigne, on ecrit un marqueur VISIBLE R10
    « (À COMPLÉTER : apport individuel) » — JAMAIS un repli sur le capital, qui
    reintroduirait le bug A26-40 (capital affiche au lieu de l'apport reel). Un montant
    faux silencieux est pire qu'un trou visible. Recompose la version en lettres si seul
    le chiffre est fourni."""
    indiv = associe.apport
    montant = (indiv.montant if indiv else None) or ""
    if not montant.strip():
        marqueur = "(À COMPLÉTER : apport individuel)"
        return Apport(montant=marqueur, montant_lettres=marqueur)
    montant_lettres = (
        (indiv.montant_lettres if indiv else None) or number_words_from_value(montant)
    )
    return Apport(montant=montant, montant_lettres=montant_lettres)


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


def _associe_label(associe: StatutsCivilsAssocie, index: int) -> str:
    """Libelle court d'un associe pour les menus (« Prenom Nom » ; defaut « Associe N »)."""
    prenom = (associe.prenom or associe.prenoms or "").strip()
    nom = f"{prenom} {(associe.nom or '').strip()}".strip()
    return nom or f"Associé {index + 1}"


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
    # Idempotence (re-Akainu tour 6, MINEUR O24-05) : si la source a deja ete consommee
    # (renommee par un run anterieur / etat FS perime / race Windows), ne JAMAIS lever de
    # FileNotFoundError -> retenir la cible deja produite, sinon le chemin tel quel. (Meme
    # robustesse que ui_runtime.rename_dnc_with_signataire ; cause de la flakiness ~20 %.)
    base_target = path.with_name(f"{path.stem}_{slug}{path.suffix}")
    if not path.exists():
        return base_target if base_target.exists() else path
    target = base_target
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


def _t(container, field: str, label: str, hint: str | None = None) -> str:
    return _ts(container, f"{PREFIX}_{field}", label, hint)


def _ts(container, key: str, label: str, hint: str | None = None) -> str:
    # C2 : helper canonique partage (front_app/_field_inputs). Comportement inchange.
    return text_input_field(container, key, label, hint)


def _i(container, field: str, label: str) -> int:
    return _is(container, f"{PREFIX}_{field}", label)


def _is(container, key: str, label: str) -> int:
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(field: str, label: str) -> date | None:
    # Consomme la couche de rendu PARTAGEE (front_widgets) au lieu de reimplementer
    # le helper localement (cause racine des ecarts de parite). Nesting-safe : peut
    # etre appele a l'interieur d'une colonne (ex. signature_date sous `with col_m`).
    from sydel_doc_engine.front_app.front_widgets import date_input_with_today

    return date_input_with_today(label, key=f"{PREFIX}_{field}", value=date.today())
