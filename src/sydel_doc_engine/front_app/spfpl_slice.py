"""Socle des slices SPFPL (cession DOC-035 / apport DOC-036), patron SELARL.

SPFPL V1 = associe unique (le moteur bloque le multi-associes). Contexte moteur
mirroir du builder de test `test_lot_04_statuts_spfpl`. Le slice collecte les
champs cles, superpose un contexte de defaut valide, route vers le bon
generateur selon l'operation (cession / apport).
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
    ApportTitres,
    CapitalContext,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    CessionParts,
    Company,
    DecisionContext,
    DepotFonds,
    DirigeantNomine,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    ExerciceSocial,
    OperationSpfpl,
    OperationTitres,
    OrdreAddress,
    OrdreProfessionnel,
    Person,
    ProfessionalEntity,
    RegimeCommunautaire,
    RegimeCommunautaireAvertissement,
    RegimeCommunautaireRenonciation,
    ReunionContext,
    ReunionPresident,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplDirigeant,
    SpfplOrdre,
    SpfplPerson,
    SpfplRepresentant,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    calculate_nominal_value,
    date_to_french_words,
    derive_gender_from_civilite,
    format_numeric_value,
    number_words_from_value,
)
from sydel_doc_engine.front_app.front_widgets import (
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    seed_exercice_dates,
    seed_signature_lieu,
)

OPERATION_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SPFPL cession": ("cession", "DOC-035"),
    "SPFPL apport": ("apport", "DOC-036"),
}

# Documents d'OPERATION apport (canon « Si apport ») — gates moteur sur
# dossier_options.apport : contrat d'apport (DOC-041) + attestation capital /
# liste des souscripteurs (DOC-042) + attestation du commissaire aux apports
# (DOC-043). Ils s'ajoutent au bundle de creation des que l'operation = apport.
SPFPL_APPORT_OPERATION_CODES: tuple[str, ...] = ("DOC-041", "DOC-042", "DOC-043")

# Activite standard d'une SPFPL (societe de participations financieres de
# profession liberale) — boilerplate du type, pas une donnee de dossier.
_SPFPL_ACTIVITE = "participations financières de profession libérale"

# Champs d'une entite professionnelle (commissaire aux apports / evaluateur)
# collectee dans le sous-formulaire apport.
_ENTITY_FIELDS: tuple[str, ...] = (
    "denomination",
    "forme",
    "capital",
    "siege",
    "ville_rcs",
    "numero_rcs",
    "rep_civilite",
    "rep_prenom",
    "rep_nom",
)

# Bundle de creation SPFPL (canon, perimetre CREATION cablable) : statuts du type
# + tronc commun (DNC / domiciliation / procuration) + PV nomination gerant +
# demande d'inscription a l'ordre.
#
# Hors bundle automatique (exigent des donnees d'OPERATION non collectees a la
# creation du holding -> voir manques[]) :
#   - note d'information (DOC-037) : exige `associes_cible` = la repartition du
#     capital de la societe cible AVANT/APRES l'operation (roster d'associes de la
#     societe operationnelle), non saisie a la creation du holding.
#   - cession : PV agrement (DOC-038/039), acte cession parts/actions (DOC-040/029)
#     -> exigent associes_cible, prix en lettres, PV reunion d'agrement.
#   - apport : contrat apport (DOC-041), attestations capital / commissaire
#     (DOC-042/043) -> exigent l'identite du commissaire aux apports / evaluateur
#     et le detail des titres apportes en lettres.


def _creation_bundle_codes(
    statuts_code: str,
    *,
    regime_communautaire: bool = False,
) -> tuple[str, ...]:
    codes = [
        statuts_code,
        *cc.TRONC_COMMUN_CODES,
        cc.DOC_PV_NOMINATION_GERANT,
        cc.DOC_DEMANDE_INSCRIPTION_ORDRE,
    ]
    # Conditionnel canon « Si regime communautaire » (DOC-005 + DOC-006).
    if regime_communautaire:
        codes.extend(cc.REGIME_COMMUNAUTAIRE_CODES)
    return tuple(codes)


@dataclass(frozen=True)
class SpfplSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.spfpl_slice"


def _prefix(structure: str) -> str:
    return "spfpl_" + OPERATION_BY_STRUCTURE[structure][0]


def render_spfpl_form(structure: str) -> dict[str, object]:
    operation, _doc = OPERATION_BY_STRUCTURE[structure]
    prefix = _prefix(structure)
    is_apport = operation == "apport"
    # Parite gold (couche partagee) : pre-remplir exercice (1er janvier / 31 decembre)
    # + cloture « 31 decembre N+1 », modifiables.
    seed_exercice_dates(prefix)
    seed_closing_date(prefix)
    st.subheader("Donnees a saisir")
    st.markdown(f"**Societe SPFPL ({operation})**")
    denomination = _t(st, prefix, "denomination", "Denomination SPFPL")
    # §14.1 (retours Albane lot 2) : suppression du champ texte libre « Siege
    # (adresse affichee) » qui doublonnait la grille structuree ci-dessous.
    # L'adresse affichee est desormais DERIVEE de la grille (cf. _siege_display),
    # comme le formulaire SELARL de reference.
    st.caption("Siege social (adresse structuree, pour la domiciliation / procuration)")
    col_sa, col_sb, col_sc, col_sd = st.columns(4)
    siege_num = _t(col_sa, prefix, "siege_num", "No")
    siege_voie = _t(col_sb, prefix, "siege_voie", "Voie")
    siege_cp = _t(col_sc, prefix, "siege_cp", "CP")
    siege_ville = _t(col_sd, prefix, "siege_ville", "Ville")
    # Parite gold : lieu de signature pre-rempli = ville du siege (anti double-saisie).
    seed_signature_lieu(prefix, siege_ville)
    col_c, col_d, col_dd = st.columns(3)
    # Capital en number_input (parite gold shell.py:1430) : interdit « 1000 » brut et
    # le « € » superflu. Stocke en chaine formatee pour l'aval.
    cap_key = f"{prefix}_capital_social"
    if cap_key not in st.session_state:
        st.session_state[cap_key] = 0
    capital = format_numeric_value(
        col_c.number_input(
            "Capital social (€)",
            min_value=0,
            step=100,
            key=cap_key,
            help="Montant numerique uniquement.",
        )
    )
    # Decision Gad 2026-06-18 : nombre d'actions VARIABLE (defaut 600), aligne sur
    # le patron SAS/SELAS. La valeur nominale n'est plus saisie librement : elle
    # est CALCULEE (capital / nb actions) et affichee en lecture seule.
    nb_actions = _i(col_d, prefix, "nb_actions_total", "Nombre d'actions")
    valeur_action = calculate_nominal_value(capital, nb_actions)
    col_dd.text_input(
        "Valeur nominale d'une action (calculee)",
        value=valeur_action,
        disabled=True,
        key=f"{prefix}_valeur_nominale_action_display",
    )
    ville_rcs = _t(st, prefix, "ville_rcs", "RCS SPFPL (ville)")

    st.markdown("**Actionnaire unique (chirurgien-dentiste, marie(e))**")
    st.caption(
        "Le titre « Docteur » est applique automatiquement (l'associe d'une SPFPL "
        "dentiste est necessairement docteur) ; la civilite ci-dessous est la "
        "civilite CIVILE (M. / Mme)."
    )
    # §14.2 (retours Albane lot 2) : « Docteur » n'est plus une valeur a choisir
    # (il etait melange avec la civilite civile et se propageait en titre dans les
    # satellites). On ne garde QUE la civilite civile M./Mme ; le genre en derive
    # (plus de double selecteur « Genre civil » redondant). Le titre pro « Docteur »
    # est injecte automatiquement cote moteur (build_generation_context).
    col_e, col_f, col_g = st.columns(3)
    civilite = col_e.selectbox(
        "Civilite (civile)",
        ("Monsieur", "Madame"),
        key=f"{prefix}_civilite",
    )
    prenom = _t(col_f, prefix, "prenom", "Prenom")
    prenoms = _t(col_g, prefix, "prenoms", "Prenoms complets (etat civil)")
    nom = _t(st, prefix, "nom", "Nom")
    col_j, col_k, col_l = st.columns(3)
    date_naissance = _t(col_j, prefix, "date_naissance", "Date de naissance (JJ/MM/AAAA)")
    ville_naissance = _t(col_k, prefix, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(col_l, prefix, "departement_naissance", "Departement naissance")
    col_m, col_n = st.columns(2)
    # Parite gold : nationalite en deroulant (NATIONALITY_PRESETS + « Autre »).
    nationalite = render_nationalite_selectbox(prefix, container=col_m)
    regime = _t(col_n, prefix, "regime_matrimonial", "Regime matrimonial")
    # §14.1 : suppression du champ texte libre « Adresse personnelle (affichee) »
    # redondant ; l'adresse affichee est DERIVEE de la grille structuree.
    st.caption("Adresse personnelle structuree + filiation (declaration de non-condamnation)")
    col_aa, col_ab, col_ac, col_ad = st.columns(4)
    adresse_num = _t(col_aa, prefix, "adresse_num", "No")
    adresse_voie = _t(col_ab, prefix, "adresse_voie", "Voie")
    adresse_cp = _t(col_ac, prefix, "adresse_cp", "CP")
    adresse_ville = _t(col_ad, prefix, "adresse_ville", "Ville")
    col_ae, col_af, col_ag = st.columns(3)
    nom_pere = _t(col_ae, prefix, "nom_pere", "Nom du pere")
    nom_mere = _t(col_af, prefix, "nom_mere", "Nom de la mere")
    with col_ag:
        decision_date = _date(prefix, "decision_date", "Date de decision (PV gerant)")

    st.markdown("Conjoint")
    col_o, col_p, col_q = st.columns(3)
    conjoint_civilite = col_o.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key=f"{prefix}_conjoint_civilite",
    )
    conjoint_prenom = _t(col_p, prefix, "conjoint_prenom", "Prenom conjoint")
    conjoint_nom = _t(col_q, prefix, "conjoint_nom", "Nom conjoint")
    regime_key = f"{prefix}_regime_communautaire"
    if regime_key not in st.session_state:
        st.session_state[regime_key] = False
    regime_communautaire = st.checkbox(
        "Regime communautaire (ajoute lettre de renonciation + avertissement au conjoint)",
        key=regime_key,
    )

    st.markdown("Ordre")
    col_r, col_s, col_t = st.columns(3)
    ordre_departement = _t(col_r, prefix, "ordre_departement", "Departement ordre")
    numero_ordre = _t(col_s, prefix, "numero_ordre", "Numero ordre")
    numero_rpps = _t(col_t, prefix, "numero_rpps", "Numero RPPS")
    col_ra, col_rb, col_rc = st.columns(3)
    ordre_conseil = _t(col_ra, prefix, "ordre_conseil", "Conseil departemental")
    ordre_adresse_ligne_1 = _t(col_rb, prefix, "ordre_adresse_ligne_1", "Adresse ordre")
    ordre_cp = _t(col_rc, prefix, "ordre_cp", "CP ordre")
    ordre_ville = _t(st, prefix, "ordre_ville", "Ville ordre")
    # Parite gold (Albane 2026-06-10) : « Madame la Presidente » si la presidente de
    # l'ordre est une femme (demande d'inscription a l'ordre).
    feminin_key = f"{prefix}_ordre_president_feminin"
    if feminin_key not in st.session_state:
        st.session_state[feminin_key] = False
    ordre_president_feminin = st.checkbox(
        "La présidente de l'ordre est une femme",
        key=feminin_key,
        help="Coché : « Madame la Présidente » au lieu de « Monsieur le Président ».",
    )
    # Parite gold (couche partagee) : conseiller/mandataire SYDEL editable.
    mandataire_prenom, mandataire_nom = mandataire_inputs(prefix)

    st.markdown("**Depot / titres apportes**")
    col_u, col_v = st.columns(2)
    banque_nom = _t(col_u, prefix, "banque_nom", "Banque")
    banque_adresse = _t(col_v, prefix, "banque_adresse", "Adresse banque")
    col_w, col_x, col_y = st.columns(3)
    apport_montant = _t(col_w, prefix, "apport_montant", "Montant de l'apport")
    apport_nb_parts = _i(col_x, prefix, "apport_nb_parts", "Nombre de parts apportees")
    apport_plage = _t(col_y, prefix, "apport_plage", "Plage de parts (ex: 41 a 100)")
    apport_valeur_globale = _t(st, prefix, "apport_valeur_globale", "Valeur globale apportee")

    st.markdown("**Societe cible**")
    col_z, col_aa2 = st.columns(2)
    cible_denomination = _t(col_z, prefix, "cible_denomination", "Denomination cible")
    cible_siege = _t(col_aa2, prefix, "cible_siege", "Siege cible (affiche)")
    col_ab, col_ac = st.columns(2)
    cible_ville_rcs = _t(col_ab, prefix, "cible_ville_rcs", "RCS cible (ville)")
    cible_numero_rcs = _t(col_ac, prefix, "cible_numero_rcs", "Numero RCS cible")
    col_ad2, col_ae2, col_af2 = st.columns(3)
    cible_forme = _t(col_ad2, prefix, "cible_forme", "Forme sociale cible")
    cible_profession = _t(col_ae2, prefix, "cible_profession", "Profession reglementee cible")
    cible_capital = _t(col_af2, prefix, "cible_capital", "Capital social cible")
    col_ag2, col_ah2 = st.columns(2)
    cible_nb_parts = _i(col_ag2, prefix, "cible_nb_parts", "Parts totales cible")
    cible_valeur_part = _t(col_ah2, prefix, "cible_valeur_part", "Valeur nominale part cible")

    # --- Operation apport (DOC-041 contrat + DOC-042/043 attestations) :
    # detail des titres apportes + organes de controle (commissaire aux apports
    # + evaluateur). Rendu UNIQUEMENT pour l'apport ; en cession ces champs
    # restent vides et ne sont pas lus.
    apport_nature_titres = "parts sociales"
    apport_valeur_par_titre = ""
    commissaire_fields = dict.fromkeys(_ENTITY_FIELDS, "")
    evaluateur_fields = dict.fromkeys(_ENTITY_FIELDS, "")
    if is_apport:
        st.markdown("**Apport en nature — detail & organes de controle**")
        col_at1, col_at2 = st.columns(2)
        apport_nature_titres = col_at1.selectbox(
            "Nature des titres apportes",
            ("parts sociales", "actions"),
            key=f"{prefix}_apport_nature_titres",
        )
        apport_valeur_par_titre = _t(
            col_at2, prefix, "apport_valeur_par_titre", "Valeur d'un titre apporte"
        )
        st.caption("Commissaire aux apports")
        commissaire_fields = _render_entity_inputs(prefix, "commissaire")
        st.caption("Evaluateur de l'apport")
        evaluateur_fields = _render_entity_inputs(prefix, "evaluateur")

    st.markdown("**Exercice / signature**")
    col_ad, col_ae, col_af = st.columns(3)
    exercice_debut = _t(col_ad, prefix, "exercice_debut", "Debut exercice")
    exercice_fin = _t(col_ae, prefix, "exercice_fin", "Fin exercice")
    date_cloture = _t(col_af, prefix, "date_cloture", "Cloture premier exercice")
    signature_lieu = _t(st, prefix, "signature_lieu", "Lieu de signature")
    signature_date = _date(prefix, "signature_date", "Date de signature")

    return {
        "structure": structure,
        "operation": operation,
        "is_apport": is_apport,
        "denomination": denomination,
        # §14.1 : « siege » (affichage) derive de la grille structuree, plus de
        # champ texte libre.
        "siege": _siege_display(
            {
                "siege_num": siege_num,
                "siege_voie": siege_voie,
                "siege_cp": siege_cp,
                "siege_ville": siege_ville,
            }
        ),
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "ville_rcs": ville_rcs,
        "capital_social": capital,
        "nb_actions_total": nb_actions,
        # Valeur nominale CALCULEE (capital / nb actions), plus de saisie libre.
        "valeur_nominale_action": valeur_action,
        "civilite": civilite,
        # §14.2 : titre pro automatique (associe SPFPL dentiste = docteur). Plus de
        # « Docteur » dans la deroulante civilite ; le titre est pose ici.
        "titre_affichage": "Docteur",
        "prenom": prenom,
        "prenoms": prenoms or prenom,
        "nom": nom,
        # §14.2 : genre derive de la civilite CIVILE (M./Mme), plus de selecteur
        # « Genre civil » redondant.
        "genre": derive_gender_from_civilite(civilite),
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "regime_matrimonial": regime,
        # §14.1 : « adresse » (affichage) derivee de la grille structuree.
        "adresse": _adresse_perso_display(
            {
                "adresse_num": adresse_num,
                "adresse_voie": adresse_voie,
                "adresse_cp": adresse_cp,
                "adresse_ville": adresse_ville,
            }
        ),
        "adresse_num": adresse_num,
        "adresse_voie": adresse_voie,
        "adresse_cp": adresse_cp,
        "adresse_ville": adresse_ville,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "decision_date": decision_date,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_genre": derive_gender_from_civilite(conjoint_civilite),
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "regime_communautaire": regime_communautaire,
        "ordre_departement": ordre_departement,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "ordre_president_feminin": ordre_president_feminin,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
        "ordre_conseil": ordre_conseil,
        "ordre_adresse_ligne_1": ordre_adresse_ligne_1,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
        "banque_nom": banque_nom,
        "banque_adresse": banque_adresse,
        "apport_montant": apport_montant,
        "apport_nb_parts": apport_nb_parts,
        "apport_plage": apport_plage,
        "apport_valeur_globale": apport_valeur_globale,
        "cible_denomination": cible_denomination,
        "cible_siege": cible_siege,
        "cible_ville_rcs": cible_ville_rcs,
        "cible_numero_rcs": cible_numero_rcs,
        "cible_forme": cible_forme,
        "cible_profession": cible_profession,
        "cible_capital": cible_capital,
        "cible_nb_parts": cible_nb_parts,
        "cible_valeur_part": cible_valeur_part,
        "apport_nature_titres": apport_nature_titres,
        "apport_valeur_par_titre": apport_valeur_par_titre,
        **{f"commissaire_{k}": v for k, v in commissaire_fields.items()},
        **{f"evaluateur_{k}": v for k, v in evaluateur_fields.items()},
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "date_cloture": date_cloture,
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
    }


def build_spfpl_plan(payload: dict[str, object]) -> SpfplSlicePlan:
    structure = str(payload["structure"])
    operation, doc_code = OPERATION_BY_STRUCTURE[structure]
    regime_communautaire = bool(payload.get("regime_communautaire"))
    document_codes = _creation_bundle_codes(
        doc_code,
        regime_communautaire=regime_communautaire,
    )
    # Operation apport : le bundle de creation est complete par les documents
    # d'apport (contrat + 2 attestations), comme le canon « Si apport ».
    if operation == "apport":
        document_codes = document_codes + SPFPL_APPORT_OPERATION_CODES
    blockers = _validate(payload)
    warnings = [
        f"{structure} V1 = associe unique (multi-associes bloque par le moteur). Bundle de "
        "creation : statuts + tronc commun + PV gerant + demande ordre + note d'information.",
    ]
    if regime_communautaire:
        warnings.append("Regime communautaire actif : DOC-005 et DOC-006 seront generes.")
    warnings = tuple(warnings)
    if blockers:
        return SpfplSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=document_codes,
            blockers=blockers,
            warnings=warnings,
        )
    return SpfplSlicePlan(
        can_generate=True,
        status="ready",
        reason=f"Pret pour generation {structure} V1 (bundle de creation).",
        document_codes=document_codes,
        blockers=(),
        warnings=warnings,
    )


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination SPFPL requise."),
        ("siege", "Siege SPFPL requis."),
        ("capital_social", "Capital social requis."),
        ("prenom", "Prenom de l'actionnaire requis."),
        ("nom", "Nom de l'actionnaire requis."),
        ("date_naissance", "Date de naissance requise."),
        ("ville_naissance", "Ville de naissance requise."),
        ("departement_naissance", "Departement de naissance requis."),
        ("nationalite", "Nationalite requise."),
        ("regime_matrimonial", "Regime matrimonial requis."),
        ("adresse", "Adresse personnelle requise."),
        ("conjoint_prenom", "Prenom du conjoint requis."),
        ("conjoint_nom", "Nom du conjoint requis."),
        ("ordre_departement", "Departement ordre requis."),
        ("numero_ordre", "Numero ordre requis."),
        ("numero_rpps", "Numero RPPS requis."),
        ("banque_nom", "Banque requise."),
        ("banque_adresse", "Adresse banque requise."),
        ("apport_montant", "Montant de l'apport requis."),
        ("apport_plage", "Plage de parts apportees requise."),
        ("apport_valeur_globale", "Valeur globale apportee requise."),
        ("cible_denomination", "Denomination de la societe cible requise."),
        ("cible_siege", "Siege de la societe cible requis."),
        ("cible_ville_rcs", "RCS (ville) cible requis."),
        ("cible_numero_rcs", "Numero RCS cible requis."),
        ("exercice_debut", "Debut d'exercice requis."),
        ("exercice_fin", "Fin d'exercice requise."),
        ("date_cloture", "Cloture du premier exercice requise."),
        ("signature_lieu", "Lieu de signature requis."),
    )
    required += (
        ("siege_num", "No de voie du siege requis (domiciliation)."),
        ("siege_voie", "Voie du siege requise (domiciliation)."),
        ("siege_cp", "Code postal du siege requis (domiciliation)."),
        ("siege_ville", "Ville du siege requise (domiciliation)."),
        ("adresse_num", "No de voie personnel requis (declaration)."),
        ("adresse_voie", "Voie personnelle requise (declaration)."),
        ("adresse_cp", "Code postal personnel requis (declaration)."),
        ("adresse_ville", "Ville personnelle requise (declaration)."),
        ("nom_pere", "Nom du pere requis (declaration)."),
        ("nom_mere", "Nom de la mere requis (declaration)."),
        ("ordre_conseil", "Conseil departemental de l'ordre requis (demande inscription)."),
        ("ordre_adresse_ligne_1", "Adresse de l'ordre requise (demande inscription)."),
        ("ordre_cp", "Code postal de l'ordre requis (demande inscription)."),
        ("ordre_ville", "Ville de l'ordre requise (demande inscription)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    # Nombre d'actions VARIABLE (defaut 600) : doit etre >= 1 pour deriver une
    # valeur nominale coherente (capital / nb actions). Remplace l'ancien champ
    # « valeur nominale » en saisie libre (desormais calculee, non saisissable).
    if int(payload.get("nb_actions_total") or 600) < 1:
        blockers.append("Nombre d'actions requis et superieur a zero.")
    if int(payload.get("apport_nb_parts") or 0) < 1:
        blockers.append("Nombre de parts apportees requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    if payload.get("decision_date") is None:
        blockers.append("Date de decision requise (PV nomination gerant).")
    # Operation apport : les documents DOC-041/042/043 exigent le detail des
    # titres + les organes de controle (commissaire aux apports + evaluateur) +
    # la forme/capital de la cible (sinon le generateur leve `required_*`).
    if bool(payload.get("is_apport")):
        apport_required = (
            ("apport_valeur_par_titre", "Valeur d'un titre apporte requise (contrat d'apport)."),
            ("cible_forme", "Forme sociale de la cible requise (contrat d'apport)."),
            ("cible_capital", "Capital social de la cible requis (contrat d'apport)."),
            (
                "commissaire_denomination",
                "Denomination du commissaire aux apports requise (attestations).",
            ),
            ("commissaire_rep_nom", "Nom du representant du commissaire requis."),
            ("evaluateur_denomination", "Denomination de l'evaluateur de l'apport requise."),
            ("evaluateur_rep_nom", "Nom du representant de l'evaluateur requis."),
        )
        for field, message in apport_required:
            if not str(payload.get(field) or "").strip():
                blockers.append(message)
    return tuple(dict.fromkeys(blockers))


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    structure = str(payload["structure"])
    operation = str(payload["operation"])
    is_apport = bool(payload["is_apport"])
    capital = str(payload.get("capital_social") or "")
    nb_parts = int(payload.get("apport_nb_parts") or 0)
    # Nombre d'actions du capital : VARIABLE (defaut 600 = ancien codage en dur,
    # preserve la sortie byte-identique des dossiers existants). La valeur nominale
    # derive de capital / nb_actions ; on respecte une valeur deja calculee fournie
    # par le slice, sinon on la (re)calcule pour les appelants directs.
    nb_actions_total = int(payload.get("nb_actions_total") or 600)
    valeur_action = str(
        payload.get("valeur_nominale_action")
        or calculate_nominal_value(capital, nb_actions_total)
        or ""
    )
    # Detail des titres apportes (operation apport). La valeur globale est saisie ;
    # la valeur par titre est saisie (valeur d'un titre de la cible apporte). Les
    # versions « en lettres » sont DERIVEES, comme partout dans le slice. Le nombre
    # d'actions SPFPL attribuees en contrepartie = le nombre total d'actions du
    # holding (l'apporteur, associe unique, recoit toutes les actions).
    nature_titres = str(payload.get("apport_nature_titres") or "parts sociales")
    valeur_par_titre = str(payload.get("apport_valeur_par_titre") or "")
    valeur_globale = str(payload.get("apport_valeur_globale") or "")

    founder = SpfplPerson(
        civilite_affichage=str(payload.get("civilite") or "Docteur"),
        prenom=str(payload.get("prenom") or ""),
        prenoms=str(payload.get("prenoms") or payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        genre=payload.get("genre") or Gender.MASCULIN,
        profession="chirurgien-dentiste",
        profession_reglementee="chirurgiens-dentistes",
        date_naissance=str(payload.get("date_naissance") or ""),
        ville_naissance=str(payload.get("ville_naissance") or ""),
        departement_naissance=str(payload.get("departement_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        situation_maritale="marie",
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        conjoint=SpfplConjoint(
            civilite_affichage=str(payload.get("conjoint_civilite") or "Madame"),
            prenom=str(payload.get("conjoint_prenom") or ""),
            nom=str(payload.get("conjoint_nom") or ""),
        ),
        adresse_personnelle=Address(adresse_affichee=str(payload.get("adresse") or "")),
        adresse_personnelle_affichee=str(payload.get("adresse") or ""),
        ordre=SpfplOrdre(
            professionnel="Ordre des chirurgiens-dentistes",
            departement=str(payload.get("ordre_departement") or ""),
            ville=str(payload.get("ordre_departement") or ""),
            numero=str(payload.get("numero_ordre") or ""),
            numero_rpps=str(payload.get("numero_rpps") or ""),
        ),
    )
    siege_struct = Address(
        num_voie=str(payload.get("siege_num") or ""),
        voie=str(payload.get("siege_voie") or ""),
        cp=str(payload.get("siege_cp") or ""),
        ville=str(payload.get("siege_ville") or ""),
        adresse_affichee=str(payload.get("siege") or "") or _siege_display(payload),
    )
    adresse_perso = Address(
        num_voie=str(payload.get("adresse_num") or ""),
        voie=str(payload.get("adresse_voie") or ""),
        cp=str(payload.get("adresse_cp") or ""),
        ville=str(payload.get("adresse_ville") or ""),
        adresse_affichee=str(payload.get("adresse") or ""),
    )
    cible_capital = str(payload.get("cible_capital") or "")
    nb_apportees = nb_parts
    regime_communautaire_actif = bool(payload.get("regime_communautaire"))
    ctx = DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(
            apport=is_apport,
            cession=not is_apport,
            associe_unique=True,
            regime_communautaire=regime_communautaire_actif,
        ),
        conjoint=(
            _conjoint_person(payload, adresse_perso) if regime_communautaire_actif else None
        ),
        regime_communautaire=(
            _regime_communautaire(payload) if regime_communautaire_actif else None
        ),
        personne_signataire=Person(
            genre=payload.get("genre") or Gender.MASCULIN,
            civilite=str(payload.get("civilite") or "Monsieur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            # §14.2 : titre PRO = « Docteur » automatique (et non la civilite civile
            # M./Mme), utilise par la demande d'inscription a l'ordre. L'associe
            # d'une SPFPL dentiste est necessairement docteur.
            titre_affichage=str(payload.get("titre_affichage") or "Docteur"),
            adresse_perso=adresse_perso,
            adresse_personnelle_affichee=adresse_perso.adresse_affichee,
            date_naissance=cc.parse_birth_date(payload.get("date_naissance")),
            ville_naissance=str(payload.get("ville_naissance") or ""),
            nationalite=str(payload.get("nationalite") or ""),
            nom_pere=str(payload.get("nom_pere") or ""),
            nom_mere=str(payload.get("nom_mere") or ""),
            fonction_dirigeant="président",
            qualification_principale="chirurgien-dentiste",
        ),
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
            nombre_exemplaires="trois",
        ),
        societe=Company(
            forme_sociale="SPFPL",
            forme_sociale_affichage="SPFPL",
            forme_sociale_abregee="SPFPL",
            forme_sociale_complete=(
                "société de participations financières de professions libérales"
            ),
            forme_sociale_libelle_long=(
                "Société de participations financières de professions libérales"
            ),
            denomination=str(payload.get("denomination") or ""),
            denomination_courte=str(payload.get("denomination") or ""),
            capital=capital,
            capital_social=capital,
            capital_variable=True,
            siege=siege_struct,
            ville_rcs=str(payload.get("ville_rcs") or payload.get("siege_ville") or ""),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=siege_struct.adresse_affichee,
        ),
        mandataire=cc.default_mandataire(
            prenom=str(payload.get("mandataire_prenom") or ""),
            nom=str(payload.get("mandataire_nom") or ""),
        ),
        ordre=_spfpl_ordre_professionnel(payload),
        capital=CapitalContext(
            nb_parts_total=nb_apportees,
            valeur_nominale_part=valeur_action,
            nb_parts_representees=nb_apportees,
            montant=capital,
            type_titre="actions",
        ),
        dirigeant_nomine=DirigeantNomine(
            genre=payload.get("genre") or Gender.MASCULIN,
            civilite_affichage=str(payload.get("civilite") or "Monsieur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            date_naissance=cc.parse_birth_date(payload.get("date_naissance")),
            ville_naissance=str(payload.get("ville_naissance") or ""),
            departement_naissance=str(payload.get("departement_naissance") or ""),
            nationalite=str(payload.get("nationalite") or ""),
            adresse_personnelle=adresse_perso,
            fonction_affichage="président",
            ref_associe_index=0,
        ),
        associes=[_spfpl_pv_associe(payload, nb_apportees)],
        decision=DecisionContext(date=_display_date(payload.get("decision_date"))),
        reunion=ReunionContext(
            date_lettres=date_to_french_words(payload.get("decision_date")),
            president=ReunionPresident(
                civilite_affichage=str(payload.get("civilite") or "Monsieur"),
                prenom=str(payload.get("prenom") or ""),
                nom=str(payload.get("nom") or ""),
                qualite="associé unique",
                civilite_president_seance=str(payload.get("civilite") or "Monsieur"),
                prenom_president_seance=str(payload.get("prenom") or ""),
                nom_personne_seance=str(payload.get("nom") or ""),
            ),
        ),
        cedant=founder if not is_apport else None,
        apporteur=founder if is_apport else None,
        operation_titres=OperationTitres(nb_titres=nb_apportees),
        operation_spfpl=OperationSpfpl(type=operation),
        societe_spfpl=SocieteSpfpl(
            denomination=str(payload.get("denomination") or ""),
            forme_sociale="par actions simplifiee",
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            # Activite + profession : exiges par le contrat d'apport (DOC-041) et
            # l'attestation du commissaire (DOC-043). Boilerplate du type SPFPL
            # dentiste, pas une saisie de dossier.
            activite=_SPFPL_ACTIVITE,
            profession="chirurgien-dentiste",
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
            siege=siege_struct,
            ville_rcs=str(payload.get("ville_rcs") or payload.get("siege_ville") or ""),
            numero_rcs="en cours",
            dirigeant=SpfplDirigeant(fonction="Président"),
            representant=SpfplRepresentant(
                civilite_affichage=str(payload.get("civilite") or "Monsieur"),
                prenom=str(payload.get("prenom") or ""),
                nom=str(payload.get("nom") or ""),
                fonction="Président",
            ),
        ),
        actionnaire_unique=founder,
        apport=Apport(
            montant=str(payload.get("apport_montant") or ""),
            montant_lettres=(number_words_from_value(payload.get("apport_montant")) + " euros")
            if number_words_from_value(payload.get("apport_montant"))
            else str(payload.get("apport_montant") or ""),
        ),
        depot_fonds=DepotFonds(
            banque=CessionBanque(
                nom=str(payload.get("banque_nom") or ""),
                adresse_affichee=str(payload.get("banque_adresse") or ""),
            )
        ),
        apport_titres=ApportTitres(
            nb_parts=nb_parts,
            nb_parts_lettres=number_words_from_value(nb_parts),
            nature_titres=nature_titres,
            plage_parts=str(payload.get("apport_plage") or ""),
            valeur_par_titre=valeur_par_titre,
            valeur_par_titre_lettres=number_words_from_value(valeur_par_titre),
            valeur_globale=valeur_globale,
            valeur_globale_lettres=number_words_from_value(valeur_globale),
            nb_actions_attribuees=nb_actions_total,
            nb_actions_attribuees_lettres=number_words_from_value(nb_actions_total),
            valeur_nominale_action=valeur_action,
            valeur_nominale_action_lettres=number_words_from_value(valeur_action),
        ),
        societe_cible=SocieteCible(
            denomination=str(payload.get("cible_denomination") or ""),
            forme_sociale=str(payload.get("cible_forme") or ""),
            profession_reglementee=str(payload.get("cible_profession") or ""),
            capital_social=cible_capital,
            capital_social_lettres=number_words_from_value(cible_capital),
            nb_parts_total=int(payload.get("cible_nb_parts") or 0),
            valeur_nominale_part=str(payload.get("cible_valeur_part") or ""),
            valeur_nominale_part_lettres=number_words_from_value(
                payload.get("cible_valeur_part")
            ),
            siege=Address(adresse_affichee=str(payload.get("cible_siege") or "")),
            ville_rcs=str(payload.get("cible_ville_rcs") or ""),
            numero_rcs=str(payload.get("cible_numero_rcs") or ""),
        ),
        cession_parts=CessionParts(
            nb_parts=nb_apportees,
            nb_parts_lettres=number_words_from_value(nb_apportees),
            plage_parts=str(payload.get("apport_plage") or ""),
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=nb_actions_total,
            valeur_nominale_action=valeur_action,
            # Apport SPFPL : le capital est constitue par l'apport EN NATURE des
            # titres de la cible (numeraire = 0). L'apporteur est l'unique
            # souscripteur et recoit toutes les actions.
            apports_nature_montant=valeur_globale,
            apports_numeraire_montant="0 euro",
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage="Docteur",
                    prenom=str(payload.get("prenom") or ""),
                    nom=str(payload.get("nom") or ""),
                    profession="chirurgien-dentiste",
                    adresse_personnelle_affichee=adresse_perso.adresse_affichee,
                    nb_actions=nb_actions_total,
                    qualite="actionnaire unique",
                )
            ],
        ),
        exercice_social=ExerciceSocial(
            debut=str(payload.get("exercice_debut") or ""),
            fin=str(payload.get("exercice_fin") or ""),
            date_cloture_premier_exercice=str(payload.get("date_cloture") or ""),
        ),
        # Organes de controle de l'apport : SAISIS dans le sous-formulaire apport
        # (plus de valeurs en dur). Chaque dossier a son propre commissaire aux
        # apports et son evaluateur. None en cession (non lus).
        commissaire_aux_apports=(
            _professional_entity(payload, "commissaire") if is_apport else None
        ),
        evaluateur_apport=(
            _professional_entity(payload, "evaluateur") if is_apport else None
        ),
        metadata={"front_slice": f"track_b_spfpl_{operation}_v1"},
    )
    return ctx


def _conjoint_person(payload: dict[str, object], signataire_address: Address) -> Person:
    """Conjoint (renonciation DOC-005 + avertissement DOC-006).

    L'avertissement adresse le conjoint au domicile du foyer ; on reutilise
    l'adresse personnelle structuree de l'actionnaire, deja saisie.
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


def _render_entity_inputs(prefix: str, role: str) -> dict[str, str]:
    """Saisie d'une entite professionnelle (commissaire aux apports / evaluateur).

    Collecte les champs exiges par `professional_entity_presentation` (denomination,
    forme, capital, siege, RCS) + son representant (civilite / prenom / nom).
    """
    col_a, col_b, col_c = st.columns(3)
    denomination = _t(col_a, prefix, f"{role}_denomination", "Denomination")
    forme = _t(col_b, prefix, f"{role}_forme", "Forme sociale")
    capital = _t(col_c, prefix, f"{role}_capital", "Capital social")
    siege = _t(st, prefix, f"{role}_siege", "Siege (adresse affichee)")
    col_d, col_e = st.columns(2)
    ville_rcs = _t(col_d, prefix, f"{role}_ville_rcs", "RCS (ville)")
    numero_rcs = _t(col_e, prefix, f"{role}_numero_rcs", "Numero RCS")
    col_f, col_g, col_h = st.columns(3)
    rep_civilite = col_f.selectbox(
        "Civilite representant",
        ("Monsieur", "Madame"),
        key=f"{prefix}_{role}_rep_civilite",
    )
    rep_prenom = _t(col_g, prefix, f"{role}_rep_prenom", "Prenom representant")
    rep_nom = _t(col_h, prefix, f"{role}_rep_nom", "Nom representant")
    return {
        "denomination": denomination,
        "forme": forme,
        "capital": capital,
        "siege": siege,
        "ville_rcs": ville_rcs,
        "numero_rcs": numero_rcs,
        "rep_civilite": rep_civilite,
        "rep_prenom": rep_prenom,
        "rep_nom": rep_nom,
    }


def _professional_entity(payload: dict[str, object], role: str) -> ProfessionalEntity | None:
    """Construit une entite professionnelle (commissaire / evaluateur) du payload.

    Renvoie None si la denomination n'est pas saisie (le validateur apport bloque
    alors la generation avec un message explicite).
    """
    denomination = str(payload.get(f"{role}_denomination") or "")
    if not denomination:
        return None
    return ProfessionalEntity(
        denomination=denomination,
        forme_sociale=str(payload.get(f"{role}_forme") or ""),
        capital_social=str(payload.get(f"{role}_capital") or ""),
        siege=Address(adresse_affichee=str(payload.get(f"{role}_siege") or "")),
        ville_rcs=str(payload.get(f"{role}_ville_rcs") or ""),
        numero_rcs=str(payload.get(f"{role}_numero_rcs") or ""),
        representant=SpfplRepresentant(
            civilite_affichage=str(payload.get(f"{role}_rep_civilite") or ""),
            prenom=str(payload.get(f"{role}_rep_prenom") or ""),
            nom=str(payload.get(f"{role}_rep_nom") or ""),
        ),
    )


def _spfpl_ordre_professionnel(payload: dict[str, object]) -> OrdreProfessionnel:
    ligne_1 = str(payload.get("ordre_adresse_ligne_1") or "")
    cp = str(payload.get("ordre_cp") or "")
    ville = str(payload.get("ordre_ville") or "")
    bloc = f"{ligne_1}\n{cp} {ville}"
    return OrdreProfessionnel(
        conseil_departemental_libelle=str(payload.get("ordre_conseil") or ""),
        departement_inscription=str(payload.get("ordre_departement") or ""),
        destinataire_appel=(
            "Madame la Présidente"
            if bool(payload.get("ordre_president_feminin"))
            else "Monsieur le Président"
        ),
        profession_signataire_affichee="chirurgien-dentiste",
        profession_ligne_destinataire="chirurgiens-dentistes",
        profession_reglementee_pluriel="chirurgiens-dentistes",
        adresse_affichee=bloc,
        adresse_bloc_affiche=bloc,
        adresse=OrdreAddress(
            ligne_1=str(payload.get("ordre_adresse_ligne_1") or ""),
            cp=str(payload.get("ordre_cp") or ""),
            ville=str(payload.get("ordre_ville") or ""),
        ),
    )


def _spfpl_pv_associe(payload: dict[str, object], nb_parts: int) -> object:
    from sydel_doc_engine.domain.models import Associe

    return Associe(
        genre=payload.get("genre") or Gender.MASCULIN,
        civilite_affichage=str(payload.get("civilite") or "Monsieur"),
        prenom=str(payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        nb_parts=nb_parts,
        nb_parts_lettres=number_words_from_value(nb_parts),
        profession="chirurgien-dentiste",
        profession_reglementee="chirurgien-dentiste",
        qualite="associé unique",
    )


def _siege_display(payload: dict[str, object]) -> str:
    return (
        f"{payload.get('siege_num', '')} {payload.get('siege_voie', '')}, "
        f"{payload.get('siege_cp', '')} {payload.get('siege_ville', '')}"
    ).strip(" ,")


def _adresse_perso_display(payload: dict[str, object]) -> str:
    # §14.1 (retours Albane lot 2) : l'adresse personnelle est DERIVEE de la
    # grille structuree (No/Voie/CP/Ville), comme la SELARL — plus de champ
    # texte libre « adresse affichee » redondant.
    return (
        f"{payload.get('adresse_num', '')} {payload.get('adresse_voie', '')}, "
        f"{payload.get('adresse_cp', '')} {payload.get('adresse_ville', '')}"
    ).strip(" ,")


def _display_date(value) -> str | None:
    if value is None:
        return None
    return value.strftime("%d/%m/%Y")


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_spfpl_plan(payload)
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


def _t(container, prefix: str, field: str, label: str) -> str:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key)).strip()


def _i(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(prefix: str, field: str, label: str) -> date | None:
    # Consomme la couche de rendu partagee (front_widgets) au lieu de reimplementer
    # le helper localement (cause racine des ecarts de parite).
    return date_input_with_today(label, key=f"{prefix}_{field}", value=date.today())
