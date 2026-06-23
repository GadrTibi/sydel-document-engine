"""Slice front SAS / SPFPL medecins (DOC-015), sur patron SELARL.

SAS V1 = SPFPL medecins, actionnaire unique, associe unique, marie(e) (le moteur
verrouille le wording non marie). Contexte moteur mirroir du builder de test
`test_statuts_sas`. Le slice collecte les champs cles et superpose un contexte de
defaut valide pour garantir une generation sans token residuel.
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
    ApportTitres,
    CapitalSouscripteur,
    CapitalSouscription,
    CessionBanque,
    Company,
    DepotFonds,
    DocumentGenerationContext,
    Domiciliation,
    DossierOptions,
    ExerciceSocial,
    Person,
    RemunerationPresident,
    Signature,
    SocieteCible,
    SocieteSpfpl,
    SpfplConjoint,
    SpfplOrdre,
    SpfplPerson,
    StatutsPresident,
    StatutsSas,
)
from sydel_doc_engine.front_app import common_creation as cc
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    calculate_nominal_value,
    derive_gender_from_civilite,
    format_numeric_value,
    is_capital_divisible,
    number_words_from_value,
)
from sydel_doc_engine.front_app.front_widgets import (
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    seed_exercice_dates,
    seed_siege_from_perso,
    seed_signature_lieu,
    siege_same_as_perso_checkbox,
)

STRUCTURE = "SAS"
DOC_CODE = "DOC-015"
PREFIX = "sas"

# Bundle de creation SAS / SPFPL medecins (canon) : statuts + tronc commun
# (DNC / domiciliation / procuration) + attestation sur le capital / liste des
# souscripteurs (DOC-024, rendu une seule fois) + PV remuneration president
# (DOC-023). La SAS V1 = actionnaire unique medecin, president non remunere
# jusqu'a la cloture du premier exercice (seul cas couvert par la source).
SAS_DOC_STATUTS = "DOC-015"
SAS_DOC_ATTESTATION_CAPITAL = "DOC-024"
SAS_DOC_PV_REMUNERATION = "DOC-023"
SAS_BUNDLE_CODES: tuple[str, ...] = (
    SAS_DOC_STATUTS,
    *cc.TRONC_COMMUN_CODES,
    SAS_DOC_ATTESTATION_CAPITAL,
    SAS_DOC_PV_REMUNERATION,
)


@dataclass(frozen=True)
class SasSlicePlan:
    can_generate: bool
    status: str
    reason: str
    document_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    target_engine_adapter: str = "front_app.sas_slice"


def render_sas_form() -> dict[str, object]:
    st.subheader("Donnees a saisir")
    # Parite gold (couche partagee) : pre-remplir exercice (1er janvier / 31 decembre)
    # + cloture « 31 decembre N+1 », modifiables. Seede AVANT les widgets concernes.
    seed_exercice_dates(PREFIX)
    seed_closing_date(PREFIX)
    # Parite gold (RAF-003a) : recopie siege <- adresse perso si la case est cochee.
    seed_siege_from_perso(PREFIX)
    st.markdown("**Societe (SPFPL medecins, forme SAS)**")
    col_a, col_b = st.columns(2)
    denomination = _t(col_a, "denomination", "Denomination")
    siege = _t(col_b, "siege", "Siege (adresse affichee)")
    st.caption("Siege social (adresse structuree, pour la domiciliation / procuration)")
    siege_same_as_perso_checkbox(PREFIX)
    col_sa, col_sb, col_sc, col_sd = st.columns(4)
    siege_num = _t(col_sa, "siege_num", "No")
    siege_voie = _t(col_sb, "siege_voie", "Voie")
    siege_cp = _t(col_sc, "siege_cp", "CP")
    siege_ville = _t(col_sd, "siege_ville", "Ville")
    # Parite gold : lieu de signature pre-rempli = ville du siege (anti double-saisie).
    seed_signature_lieu(PREFIX, siege_ville)
    col_c, col_d, col_e = st.columns(3)
    # Capital en number_input (parite gold shell.py:1430) : interdit « 1000 » brut et
    # le « € » superflu. Pattern _i (seed session_state) ; stocke en chaine formatee.
    cap_key = f"{PREFIX}_capital_social"
    if cap_key not in st.session_state:
        st.session_state[cap_key] = 0
    capital = format_numeric_value(
        col_c.number_input(
            "Capital social (€)",
            min_value=0,
            step=100,
            key=cap_key,
            help="Montant numerique uniquement (ex : 330 000).",
        )
    )
    nb_actions = _i(col_d, "nb_actions_total", "Nombre total d'actions")
    # Valeur nominale d'une action : TOUJOURS calculee (capital / nb actions),
    # jamais saisie (retours Rafael 2026-06-18, alignement SELAS). Champ d'affichage seul.
    valeur_action = calculate_nominal_value(capital, nb_actions)
    col_e.text_input(
        "Valeur nominale d'une action (calculee)",
        value=valeur_action,
        disabled=True,
    )
    col_an, col_ai = st.columns(2)
    apports_nature = _t(col_an, "apports_nature_montant", "Apports en nature (montant)")
    apports_numeraire = _t(col_ai, "apports_numeraire_montant", "Apports en numeraire (montant)")

    st.markdown("**Actionnaire unique / president (medecin, marie(e))**")
    col_f, col_g, col_h = st.columns(3)
    civilite = col_f.selectbox(
        "Civilite affichee",
        ("Docteur", "Monsieur", "Madame"),
        key=f"{PREFIX}_civilite",
    )
    prenom = _t(col_g, "prenom", "Prenom")
    nom = _t(col_h, "nom", "Nom")
    col_i, col_j = st.columns(2)
    genre_label = col_i.selectbox(
        "Genre civil",
        ("Monsieur", "Madame"),
        key=f"{PREFIX}_genre_label",
    )
    qualification = _t(col_j, "qualification_principale", "Qualification (ex: Medecin cardiologue)")
    col_k, col_l, col_m = st.columns(3)
    date_naissance = _t(col_k, "date_naissance", "Date de naissance (ex: 2 janvier 1980)")
    ville_naissance = _t(col_l, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(col_m, "departement_naissance", "Departement naissance")
    col_n, col_o = st.columns(2)
    # Parite gold : nationalite en deroulant (NATIONALITY_PRESETS + « Autre »).
    nationalite = render_nationalite_selectbox(PREFIX, container=col_n)
    regime = _t(col_o, "regime_matrimonial", "Regime matrimonial (ex: la communaute legale)")
    adresse_perso = _t(st, "adresse", "Adresse personnelle (affichee)")
    st.caption("Adresse personnelle structuree + filiation (declaration de non-condamnation)")
    col_aa, col_ab, col_ac, col_ad = st.columns(4)
    adresse_num = _t(col_aa, "adresse_num", "No")
    adresse_voie = _t(col_ab, "adresse_voie", "Voie")
    adresse_cp = _t(col_ac, "adresse_cp", "CP")
    adresse_ville = _t(col_ad, "adresse_ville", "Ville")
    col_ae, col_af, col_ag = st.columns(3)
    nom_pere = _t(col_ae, "nom_pere", "Nom du pere")
    nom_mere = _t(col_af, "nom_mere", "Nom de la mere")
    with col_ag:
        date_naissance_iso = _date(PREFIX, "date_naissance_iso", "Date naissance (JJ/MM/AAAA)")

    st.markdown("Conjoint")
    col_p, col_q, col_r = st.columns(3)
    conjoint_civilite = col_p.selectbox(
        "Civilite conjoint",
        ("Madame", "Monsieur"),
        key=f"{PREFIX}_conjoint_civilite",
    )
    conjoint_prenom = _t(col_q, "conjoint_prenom", "Prenom conjoint")
    conjoint_nom = _t(col_r, "conjoint_nom", "Nom conjoint")

    st.markdown("Ordre")
    col_s, col_t, col_u = st.columns(3)
    ordre_departement = _t(col_s, "ordre_departement", "Departement ordre")
    numero_ordre = _t(col_t, "numero_ordre", "Numero ordre")
    numero_rpps = _t(col_u, "numero_rpps", "Numero RPPS")
    # Parite gold (couche partagee) : conseiller/mandataire SYDEL editable.
    mandataire_prenom, mandataire_nom = mandataire_inputs(PREFIX)

    st.markdown("**Societe cible (participations apportees en nature)**")
    col_ca, col_cb = st.columns(2)
    cible_denomination = _t(col_ca, "cible_denomination", "Denomination cible")
    cible_forme = _t(col_cb, "cible_forme", "Forme sociale cible")
    cible_siege = _t(st, "cible_siege", "Siege cible (affiche)")
    col_cc, col_cd, col_ce = st.columns(3)
    cible_ville_rcs = _t(col_cc, "cible_ville_rcs", "RCS cible (ville)")
    cible_numero_rcs = _t(col_cd, "cible_numero_rcs", "Numero RCS cible")
    apport_nb_parts = _i(col_ce, "apport_nb_parts", "Parts cible apportees")

    st.markdown("**Depot / exercice / signature**")
    col_v, col_w = st.columns(2)
    banque_nom = _t(col_v, "banque_nom", "Banque depot", hint="ex : CIC CHAPEAU ROUGE BORDEAUX")
    signature_lieu = _t(col_w, "signature_lieu", "Lieu de signature")
    col_x, col_y, col_z = st.columns(3)
    exercice_debut = _t(col_x, "exercice_debut", "Debut exercice")
    exercice_fin = _t(col_y, "exercice_fin", "Fin exercice")
    date_cloture = _t(col_z, "date_cloture", "Cloture premier exercice")
    signature_date = _date(PREFIX, "signature_date", "Date de signature")

    return {
        "denomination": denomination,
        "siege": siege,
        "siege_num": siege_num,
        "siege_voie": siege_voie,
        "siege_cp": siege_cp,
        "siege_ville": siege_ville,
        "capital_social": capital,
        "nb_actions_total": nb_actions,
        "valeur_nominale_action": valeur_action,
        "apports_nature_montant": apports_nature,
        "apports_numeraire_montant": apports_numeraire,
        "civilite": civilite,
        "prenom": prenom,
        "nom": nom,
        "genre": derive_gender_from_civilite(genre_label),
        "qualification_principale": qualification,
        "date_naissance": date_naissance,
        "date_naissance_iso": date_naissance_iso,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "regime_matrimonial": regime,
        "adresse": adresse_perso,
        "adresse_num": adresse_num,
        "adresse_voie": adresse_voie,
        "adresse_cp": adresse_cp,
        "adresse_ville": adresse_ville,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "ordre_departement": ordre_departement,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
        "cible_denomination": cible_denomination,
        "cible_forme": cible_forme,
        "cible_siege": cible_siege,
        "cible_ville_rcs": cible_ville_rcs,
        "cible_numero_rcs": cible_numero_rcs,
        "apport_nb_parts": apport_nb_parts,
        "banque_nom": banque_nom,
        "signature_lieu": signature_lieu,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "date_cloture": date_cloture,
        "signature_date": signature_date,
    }


def build_sas_plan(payload: dict[str, object]) -> SasSlicePlan:
    blockers = _validate(payload)
    warnings = (
        "SAS V1 = SPFPL medecins, actionnaire unique marie(e). Bundle de creation : statuts "
        "+ tronc commun + attestation capital + PV remuneration president (non remunere V1).",
    )
    if blockers:
        return SasSlicePlan(
            can_generate=False,
            status="blocked",
            reason=blockers[0],
            document_codes=SAS_BUNDLE_CODES,
            blockers=blockers,
            warnings=warnings,
        )
    return SasSlicePlan(
        can_generate=True,
        status="ready",
        reason="Pret pour generation SAS / SPFPL medecins V1 (bundle de creation).",
        document_codes=SAS_BUNDLE_CODES,
        blockers=(),
        warnings=warnings,
    )


def _amount(value: object) -> int:
    """Parse un montant affiche (« 12 000 », « 12000 ») en entier ; 0 si invalide."""
    cleaned = str(value or "").replace(" ", "").replace("\xa0", "").replace(" ", "")
    try:
        return int(cleaned or 0)
    except ValueError:
        return 0


def _validate(payload: dict[str, object]) -> tuple[str, ...]:
    blockers: list[str] = []
    required = (
        ("denomination", "Denomination requise."),
        ("siege", "Siege requis."),
        ("capital_social", "Capital social requis."),
        ("valeur_nominale_action", "Valeur nominale d'une action requise."),
        ("prenom", "Prenom de l'actionnaire requis."),
        ("nom", "Nom de l'actionnaire requis."),
        ("qualification_principale", "Qualification requise."),
        ("date_naissance", "Date de naissance requise."),
        ("ville_naissance", "Ville de naissance requise."),
        ("departement_naissance", "Departement de naissance requis."),
        ("nationalite", "Nationalite requise."),
        ("regime_matrimonial", "Regime matrimonial requis."),
        ("adresse", "Adresse personnelle requise."),
        ("conjoint_prenom", "Prenom du conjoint requis (actionnaire marie(e))."),
        ("conjoint_nom", "Nom du conjoint requis (actionnaire marie(e))."),
        ("ordre_departement", "Departement ordre requis."),
        ("numero_ordre", "Numero ordre requis."),
        ("numero_rpps", "Numero RPPS requis."),
        ("banque_nom", "Banque de depot requise."),
        ("signature_lieu", "Lieu de signature requis."),
        ("exercice_debut", "Debut d'exercice requis."),
        ("exercice_fin", "Fin d'exercice requise."),
        ("date_cloture", "Cloture du premier exercice requise."),
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
        ("apports_nature_montant", "Montant des apports en nature requis (attestation capital)."),
        (
            "apports_numeraire_montant",
            "Montant des apports en numeraire requis (attestation capital).",
        ),
        ("cible_denomination", "Denomination de la societe cible requise (attestation capital)."),
        ("cible_forme", "Forme de la societe cible requise (attestation capital)."),
        ("cible_siege", "Siege de la societe cible requis (attestation capital)."),
        ("cible_ville_rcs", "RCS (ville) de la societe cible requis (attestation capital)."),
        ("cible_numero_rcs", "Numero RCS de la societe cible requis (attestation capital)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    if int(payload.get("nb_actions_total") or 0) < 1:
        blockers.append("Nombre total d'actions requis et superieur a zero.")
    # Dogfood 2026-06-22 : capital non divisible par le nb d'actions -> valeur nominale a
    # 28 chiffres + lettres cassees. Garde de divisibilite (couche partagee).
    if not is_capital_divisible(payload.get("capital_social"), payload.get("nb_actions_total")):
        blockers.append(
            "Le capital social doit etre divisible par le nombre d'actions "
            "(la valeur nominale d'une action doit etre un nombre entier)."
        )
    if int(payload.get("apport_nb_parts") or 0) < 1:
        blockers.append("Nombre de parts cible apportees requis (attestation capital).")
    # Dogfood 2026-06-22 : la somme des apports (nature + numeraire) doit egaler le capital
    # (exige par l'attestation sur le capital) ; sinon dossier incoherent.
    capital_int = _amount(payload.get("capital_social"))
    apports_total = _amount(payload.get("apports_nature_montant")) + _amount(
        payload.get("apports_numeraire_montant")
    )
    if capital_int and apports_total != capital_int:
        blockers.append(
            f"Somme des apports nature + numeraire ({apports_total}) "
            f"!= capital social ({capital_int})."
        )
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    if payload.get("date_naissance_iso") is None:
        blockers.append("Date de naissance (JJ/MM/AAAA) requise (declaration).")
    if (payload.get("genre") or Gender.MASCULIN) != Gender.MASCULIN:
        blockers.append(
            "SAS V1 : le PV de remuneration president est verrouille au president masculin "
            "par la source ; actionnaire feminin hors perimetre."
        )
    # Dogfood 2026-06-22 : la civilite (« Docteur » neutre, ou « Monsieur »/« Madame »
    # genree) et le genre sont 2 saisies ; quand la civilite est GENREE, elle doit etre
    # coherente avec le genre (regle etablie derive_gender_from_civilite) -> sinon doc
    # contradictoire (« Madame ... il »). « Docteur » reste neutre (pas de controle).
    civilite = str(payload.get("civilite") or "")
    if civilite in ("Monsieur", "Madame") and derive_gender_from_civilite(civilite) != (
        payload.get("genre") or Gender.MASCULIN
    ):
        blockers.append(
            "Civilite et genre incoherents (ex: « Madame » avec un genre masculin)."
        )
    return tuple(dict.fromkeys(blockers))


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    nb_actions = int(payload.get("nb_actions_total") or 0)
    capital = str(payload.get("capital_social") or "")
    profession = "medecin"
    actionnaire = SpfplPerson(
        civilite_affichage=str(payload.get("civilite") or "Docteur"),
        prenom=str(payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        genre=payload.get("genre") or Gender.MASCULIN,
        profession=profession,
        qualite_associe="actionnaire unique",
        qualification_principale=str(payload.get("qualification_principale") or ""),
        date_naissance=str(payload.get("date_naissance") or ""),
        ville_naissance=str(payload.get("ville_naissance") or ""),
        departement_naissance=str(payload.get("departement_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        situation_maritale="Marie",
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        conjoint=SpfplConjoint(
            civilite_affichage=str(payload.get("conjoint_civilite") or "Madame"),
            prenom=str(payload.get("conjoint_prenom") or ""),
            nom=str(payload.get("conjoint_nom") or ""),
        ),
        adresse_personnelle_affichee=str(payload.get("adresse") or ""),
        ordre=SpfplOrdre(
            departement=str(payload.get("ordre_departement") or ""),
            numero=str(payload.get("numero_ordre") or ""),
            numero_rpps=str(payload.get("numero_rpps") or ""),
        ),
        nb_actions=nb_actions,
    )
    siege_struct = Address(
        num_voie=str(payload.get("siege_num") or ""),
        voie=str(payload.get("siege_voie") or ""),
        cp=str(payload.get("siege_cp") or ""),
        ville=str(payload.get("siege_ville") or ""),
        adresse_affichee=str(payload.get("siege") or "")
        or _siege_display(payload),
    )
    adresse_perso = Address(
        num_voie=str(payload.get("adresse_num") or ""),
        voie=str(payload.get("adresse_voie") or ""),
        cp=str(payload.get("adresse_cp") or ""),
        ville=str(payload.get("adresse_ville") or ""),
        adresse_affichee=str(payload.get("adresse") or ""),
    )
    apports_nature = str(payload.get("apports_nature_montant") or "")
    apports_numeraire = str(payload.get("apports_numeraire_montant") or "")
    return DocumentGenerationContext(
        structure="SAS",
        dossier_options=DossierOptions(associe_unique=True, apport=True),
        personne_signataire=Person(
            genre=payload.get("genre") or Gender.MASCULIN,
            civilite=str(payload.get("civilite") or "Monsieur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            titre_affichage=str(payload.get("civilite") or "Docteur"),
            adresse_perso=adresse_perso,
            adresse_personnelle_affichee=adresse_perso.adresse_affichee,
            date_naissance=payload.get("date_naissance_iso"),
            ville_naissance=str(payload.get("ville_naissance") or ""),
            nationalite=str(payload.get("nationalite") or ""),
            nom_pere=str(payload.get("nom_pere") or ""),
            nom_mere=str(payload.get("nom_mere") or ""),
            fonction_dirigeant="président",
            qualification_principale=str(payload.get("qualification_principale") or ""),
        ),
        signature=Signature(
            lieu=str(payload.get("signature_lieu") or ""),
            date=payload.get("signature_date"),
            nombre_exemplaires="trois",
        ),
        statuts_sas=StatutsSas(type="spfpl_medecins", profession=profession),
        societe=Company(
            forme_sociale="SAS",
            forme_sociale_affichage="SAS",
            denomination=str(payload.get("denomination") or ""),
            denomination_courte=str(payload.get("denomination") or ""),
            capital=capital,
            capital_social=capital,
            capital_variable=True,
            siege=siege_struct,
            ville_rcs=str(payload.get("siege_ville") or ""),
        ),
        domiciliation=Domiciliation(
            adresse_domiciliation_affichee=siege_struct.adresse_affichee,
        ),
        mandataire=cc.default_mandataire(
            prenom=str(payload.get("mandataire_prenom") or ""),
            nom=str(payload.get("mandataire_nom") or ""),
        ),
        societe_spfpl=SocieteSpfpl(
            denomination=str(payload.get("denomination") or ""),
            forme_sociale="Société par actions simplifiée",
            capital_social=capital,
            capital_social_lettres=number_words_from_value(capital),
            nb_actions_total=nb_actions,
            nb_actions_total_lettres=number_words_from_value(nb_actions),
            valeur_nominale_action=str(payload.get("valeur_nominale_action") or ""),
            valeur_nominale_action_lettres=number_words_from_value(
                payload.get("valeur_nominale_action")
            )
            + " euros"
            if number_words_from_value(payload.get("valeur_nominale_action"))
            else str(payload.get("valeur_nominale_action") or ""),
            profession=profession,
            ville_rcs=str(payload.get("siege_ville") or ""),
            siege=siege_struct,
        ),
        actionnaire_unique=actionnaire,
        president=StatutsPresident(
            ref_associe_index=0,
            civilite_affichage=str(payload.get("civilite") or "Docteur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            fonction="Président",
            adresse_personnelle_affichee=adresse_perso.adresse_affichee,
            duree_mandat="illimitee",
        ),
        remuneration_president=RemunerationPresident(
            type="absence_remuneration",
            date_fin_non_remuneree=str(payload.get("date_cloture") or ""),
        ),
        societe_cible=SocieteCible(
            denomination=str(payload.get("cible_denomination") or ""),
            forme_sociale=str(payload.get("cible_forme") or ""),
            siege=Address(adresse_affichee=str(payload.get("cible_siege") or "")),
            ville_rcs=str(payload.get("cible_ville_rcs") or ""),
            numero_rcs=str(payload.get("cible_numero_rcs") or ""),
        ),
        apport_titres=ApportTitres(nb_parts=int(payload.get("apport_nb_parts") or 0)),
        depot_fonds=DepotFonds(
            banque=CessionBanque(nom=str(payload.get("banque_nom") or "")),
            montant=capital,
        ),
        exercice_social=ExerciceSocial(
            debut=str(payload.get("exercice_debut") or ""),
            fin=str(payload.get("exercice_fin") or ""),
            date_cloture_premier_exercice=str(payload.get("date_cloture") or ""),
        ),
        capital_souscription=CapitalSouscription(
            nb_actions_total=nb_actions,
            valeur_nominale_action=str(payload.get("valeur_nominale_action") or ""),
            apports_nature_montant=apports_nature,
            apports_numeraire_montant=apports_numeraire,
            souscripteurs=[
                CapitalSouscripteur(
                    civilite_affichage=str(payload.get("civilite") or "Docteur"),
                    prenom=str(payload.get("prenom") or ""),
                    nom=str(payload.get("nom") or ""),
                    profession=profession,
                    adresse_personnelle_affichee=adresse_perso.adresse_affichee,
                    nb_actions=nb_actions,
                    qualite="actionnaire unique",
                )
            ],
        ),
        metadata={"front_slice": "track_b_sas_spfpl_medecins_v1"},
    )


def _siege_display(payload: dict[str, object]) -> str:
    return (
        f"{payload.get('siege_num', '')} {payload.get('siege_voie', '')}, "
        f"{payload.get('siege_cp', '')} {payload.get('siege_ville', '')}"
    ).strip(" ,")


def generate_dossier(payload: dict[str, object], output_dir: Path) -> GeneratedDossier:
    plan = build_sas_plan(payload)
    if not plan.can_generate:
        raise ValueError(plan.reason)
    ctx = build_generation_context(payload)
    docx_paths = generate_docx_files_for_document_codes(ctx, output_dir, plan.document_codes)
    docx_paths = rename_dnc_with_signataire(docx_paths, ctx)  # O24-02 : DNC nommee par le dirigeant
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def _t(container, field: str, label: str, hint: str | None = None) -> str:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(container.text_input(label, key=key, help=hint)).strip()


def _i(container, field: str, label: str) -> int:
    key = f"{PREFIX}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(prefix: str, field: str, label: str) -> date | None:
    # Consomme la couche de rendu partagee (front_widgets) au lieu de reimplementer
    # le helper localement (cause racine des ecarts de parite).
    return date_input_with_today(label, key=f"{prefix}_{field}", value=date.today())
