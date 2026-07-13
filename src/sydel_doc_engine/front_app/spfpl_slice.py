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
    rename_dnc_with_signataire,
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
from sydel_doc_engine.front_app._field_inputs import text_input_prefixed
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
)
from sydel_doc_engine.front_app.associe_repeater import render_nationalite_selectbox
from sydel_doc_engine.front_app.field_derivations import (
    MATRIMONIAL_STATUS_PRESETS,
    accentuate_french_months,
    calculate_nominal_value,
    date_to_french_words,
    derive_cumulative_plages,
    derive_gender_from_civilite,
    format_grouped_numeric_value,
    format_numeric_value,
    group_montant,
    is_capital_divisible,
    matrimonial_status_value,
    number_words_from_value,
    prix_lettres_from_value,
    regime_communautaire_from_status,
    regime_matrimonial_from_status,
    shift_repeater_rows_down,
    situation_display,
)
from sydel_doc_engine.front_app.front_widgets import (
    copyable_text_input,
    date_input_freeform,
    date_input_with_today,
    mandataire_inputs,
    seed_closing_date,
    seed_exercice_dates,
    seed_if_empty,
    seed_siege_from_perso,
    seed_signature_lieu,
    siege_same_as_perso_checkbox,
)

OPERATION_BY_STRUCTURE: dict[str, tuple[str, str]] = {
    "SPFPL cession": ("cession", "DOC-035"),
    "SPFPL apport": ("apport", "DOC-036"),
}

# Documents d'OPERATION apport (canon « Si apport ») — gates moteur sur
# dossier_options.apport : note d'information (DOC-037 — Rafael 2026-07-09 : le
# document porte cession ET apport, il manquait au bundle apport alors que le
# generateur et le gate orchestrateur supportaient deja l'apport) + contrat
# d'apport (DOC-041) + attestation capital / liste des souscripteurs (DOC-042)
# + attestation du commissaire aux apports (DOC-043). Ils s'ajoutent au bundle
# de creation des que l'operation = apport.
SPFPL_APPORT_OPERATION_CODES: tuple[str, ...] = ("DOC-037", "DOC-041", "DOC-042", "DOC-043")

# Documents d'OPERATION cession (canon « Si cession ») : note d'information (DOC-037),
# PV d'agrement (DOC-038 si la cible a UN associe reel / DOC-039 si PLUSIEURS), acte de
# cession de parts (DOC-040). Le PV depend du nombre d'associes REELS de la cible
# (hors holding acquereur, ajoute automatiquement comme personne morale).
SPFPL_CESSION_NOTE_CODE = "DOC-037"
SPFPL_CESSION_ACTE_PARTS_CODE = "DOC-040"
SPFPL_CESSION_PV_UNIQUE_CODE = "DOC-038"
SPFPL_CESSION_PV_PLUSIEURS_CODE = "DOC-039"
# Attestation capital / liste des souscripteurs, VARIANTE CESSION (retour Albane 11) : le
# bundle cession n'en produisait aucune ; on cable le modele source cession existant. Le
# capital de la holding acquereuse est en NUMERAIRE (vs apport en nature cote DOC-042).
SPFPL_CESSION_ATTESTATION_CAPITAL_CODE = "DOC-051"

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
    # Parite gold (couche partagee) : pre-remplir exercice (1er janvier / 31 décembre)
    # + cloture « 31 décembre N+1 », modifiables.
    seed_exercice_dates(prefix)
    seed_closing_date(prefix)
    # Parite gold (RAF-003a) : recopie siege <- adresse perso si la case est cochee.
    seed_siege_from_perso(prefix)
    # §6.5 / §6.6 (retours Albane) : la profession de l'associe unique ET la profession
    # reglementee de la societe cible sont pre-remplies « chirurgien-dentiste » (SPFPL
    # dentiste), MODIFIABLES. Seede AVANT les widgets (Streamlit interdit la modif post-widget).
    seed_if_empty(f"{prefix}_profession_associe_unique", "chirurgien-dentiste")
    seed_if_empty(f"{prefix}_cible_profession", "chirurgien-dentiste")
    # C4 (retour Rafael 2026-07-09 soir) : n° de l'article du capital social de la SEL
    # cible dans la 2e resolution du PV d'agrement (DOC-038/039) — code en dur « 7 bis »
    # cote generateur, rendu SAISISSABLE. Seede AVANT le widget (Streamlit interdit la
    # modif post-widget) ; « 7 bis » = defaut historique conserve si non renseigne.
    seed_if_empty(f"{prefix}_pv_article_capital_numero", "7 bis")
    st.subheader("Donnees a saisir")
    st.markdown(f"**Societe SPFPL ({operation})**")
    denomination = _t(st, prefix, "denomination", "Denomination SPFPL")
    # §14.1 (retours Albane lot 2) : suppression du champ texte libre « Siege
    # (adresse affichee) » qui doublonnait la grille structuree ci-dessous.
    # L'adresse affichee est desormais DERIVEE de la grille (cf. _siege_display),
    # comme le formulaire SELARL de reference.
    # O24-03 : siege sur UNE ligne (parse interne -> num/voie/cp/ville exiges par la
    # domiciliation [num_voie_siege] et la procuration).
    siege_same_as_perso_checkbox(prefix)
    siege_ligne = _t(st, prefix, "siege", "Adresse du siège (N° et voie, CP Ville)")
    _siege_struct = _parse_address_full(siege_ligne)
    siege_num = _siege_struct.num_voie if _siege_struct else ""
    siege_voie = _siege_struct.voie if _siege_struct else ""
    siege_cp = _siege_struct.cp if _siege_struct else ""
    siege_ville = _siege_struct.ville if _siege_struct else ""
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
            help="Montant numerique uniquement (ex : 330 000).",
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
    # §6.6 (retour Albane) : profession de l'associe unique pre-remplie « chirurgien-dentiste »,
    # MODIFIABLE (le titre « Docteur » des mentions ordinales reste separe — titre_affichage).
    # Ne bloque PAS la validation (repli sur « chirurgien-dentiste » cote moteur).
    profession_associe_unique = _t(st, prefix, "profession_associe_unique", "Profession")
    col_j, col_k, col_l = st.columns(3)
    # R29-06 (Rafael) : selecteur de date (calendrier) + « Aujourd'hui » sur la date de
    # naissance SPFPL. Champ texte JJ/MM/AAAA conserve, cle `{prefix}_date_naissance`
    # inchangee. seed=False (pas de date du jour sur une naissance).
    date_input_with_today(
        "Date de naissance (JJ/MM/AAAA)",
        key=f"{prefix}_date_naissance",
        value=date.today(),
        container=col_j,
        seed=False,
    )
    date_naissance = str(st.session_state.get(f"{prefix}_date_naissance") or "").strip()
    ville_naissance = _t(col_k, prefix, "ville_naissance", "Ville de naissance")
    departement_naissance = _t(
        col_l, prefix, "departement_naissance", "Departement naissance (ou pays si étranger)"
    )
    col_m, col_n = st.columns(2)
    # Parite gold : nationalite en deroulant (NATIONALITY_PRESETS + « Autre »).
    nationalite = render_nationalite_selectbox(prefix, container=col_m)
    # Retour Rafael 2026-07-02 : la SPFPL utilise DESORMAIS le MEME menu complet
    # « Situation matrimoniale » que tous les autres types (SELARL, SELAS uni/multi,
    # SCS, micro holding) — plus de menu « Regime matrimonial » restreint aux regimes
    # MARIES. On reutilise le patron ratifie (SELAS uni medecin) : le libelle collapse
    # + accorde est DERIVE (situation_display), le regime matrimonial ET le declencheur
    # DOC-005/006 (communaute legale uniquement) sont derives via les memes helpers.
    situation_label = col_n.selectbox(
        "Situation matrimoniale",
        MATRIMONIAL_STATUS_PRESETS,
        key=f"{prefix}_situation",
    )
    situation_maritale = situation_display(
        matrimonial_status_value(situation_label),
        derive_gender_from_civilite(civilite),
    )
    regime_communautaire = regime_communautaire_from_status(situation_label)
    # Le regime matrimonial n'a de sens que pour un associe MARIE ; pour tout autre
    # statut (celibataire, pacse, divorce, veuf) il reste vide (pas de « sous le regime
    # de ... » dans la comparution).
    is_marie = matrimonial_status_value(situation_label) == "marie"
    # Albane 6.3/7.3 (RATIFIE 2026-07-06) : le PARTENAIRE PACSE figure a la comparution
    # (« pacsé avec {partenaire} ») -> on affiche aussi les champs conjoint pour un pacse.
    # Le REGIME matrimonial reste MARIE-only (le PACS n'a pas de « sous le régime de … »).
    is_pacse = matrimonial_status_value(situation_label) == "pacse"
    is_marie_ou_pacse = is_marie or is_pacse
    regime = (
        regime_matrimonial_from_status(situation_label, regime_communautaire)
        if is_marie
        else ""
    )
    if regime_communautaire:
        st.caption(
            "Régime de la communauté : la lettre de renonciation et la "
            "lettre d'avertissement au conjoint seront générées."
        )
    # O24-03 : adresse personnelle sur UNE ligne (parse interne -> num/voie/cp/ville
    # exiges par la DNC du president).
    st.caption("Adresse personnelle + filiation (déclaration de non-condamnation)")
    adresse_ligne = _t(st, prefix, "adresse", "Adresse personnelle (N° et voie, CP Ville)")
    _adresse_struct = _parse_address_full(adresse_ligne)
    adresse_num = _adresse_struct.num_voie if _adresse_struct else ""
    adresse_voie = _adresse_struct.voie if _adresse_struct else ""
    adresse_cp = _adresse_struct.cp if _adresse_struct else ""
    adresse_ville = _adresse_struct.ville if _adresse_struct else ""
    # SU4/SCS2 (Albane) : la date du PV de decision = la date de signature dans TOUS les cas
    # (DecisionContext la derive de signature_date). Le champ « Date de decision (PV gerant) »
    # dedie etait mort (jamais lu) + requis + trompeur. Supprime ; la filiation ne porte plus que
    # le nom du pere et de la mere (2 colonnes au lieu de 3) (#8 onglet 24).
    col_ae, col_af = st.columns(2)
    nom_pere = _t(col_ae, prefix, "nom_pere", "Nom du pere")
    nom_mere = _t(col_af, prefix, "nom_mere", "Nom de la mere")

    # Retour Rafael 2026-07-02 + Albane 6.3/7.3 (RATIFIE 2026-07-06) : les champs conjoint
    # s'affichent pour un associe MARIE ou PACSE (la comparution porte le conjoint/partenaire
    # dans ces deux cas ; un celibataire/divorce/veuf rend juste son statut). Le libelle couvre
    # les deux (« conjoint / partenaire »). Pour un pacse le partenaire est OPTIONNEL (« si
    # renseigne ») : laisse vide -> aucune mention (« pas de mention sans nom »).
    if is_marie_ou_pacse:
        st.markdown("Conjoint / partenaire")
        col_o, col_p, col_q = st.columns(3)
        conjoint_civilite = col_o.selectbox(
            "Civilite conjoint / partenaire",
            ("Madame", "Monsieur"),
            key=f"{prefix}_conjoint_civilite",
        )
        conjoint_prenom = _t(col_p, prefix, "conjoint_prenom", "Prenom conjoint / partenaire")
        conjoint_nom = _t(col_q, prefix, "conjoint_nom", "Nom conjoint / partenaire")
    else:
        conjoint_civilite = conjoint_prenom = conjoint_nom = ""

    st.markdown("Ordre")
    col_r, col_s, col_t = st.columns(3)
    ordre_departement = _t(col_r, prefix, "ordre_departement", "Departement ordre")
    numero_ordre = _t(col_s, prefix, "numero_ordre", "Numero ordre")
    numero_rpps = _t(col_t, prefix, "numero_rpps", "Numero RPPS")
    # KAN-1 (Rafael 2026-07-13) : selecteur du connecteur grammatical avant le departement
    # (« de Paris » / « du Calvados » / « des Hauts-de-Seine »), comme la SELARL. Sans lui, le
    # destinataire de la demande d'inscription restait bloque sur « de ».
    connecteur_departement = str(
        st.selectbox(
            "Connecteur avant le département (de / du / des)",
            ("de", "du", "des"),
            key=f"{prefix}_ordre_connecteur",
            help="« Conseil départemental de l'Ordre <connecteur> <département> » : "
            "« de Paris » / « du Calvados » / « des Hauts-de-Seine ».",
        )
    )
    # Retour Albane 9.4 (2026-07-06) : le champ « Conseil departemental » est RETIRE.
    # Le destinataire de la demande d'inscription (DOC-034) est DERIVE de « Departement
    # ordre » (+ connecteur) via `_conseil_departemental_lines` ; ce champ libre
    # `ordre_conseil` ne pilotait plus rien (vestigial) -> retire. Meme cleanup que la
    # SELAS uni medecin (Rafael 2026-06-25 #3).
    # O24-03 : adresse de l'ordre sur UNE ligne (parse interne -> ligne_1/cp/ville),
    # comme siege/perso/SELAS. Remplace les 3 champs separes ; alimente les MEMES cles
    # -> generateur DOC-034 et gold byte-identique inchanges.
    _ordre_struct = _parse_address_full(
        _t(st, prefix, "ordre_adresse", "Adresse de l'ordre (N° et voie, CP Ville)")
    )
    ordre_adresse_ligne_1 = (
        f"{_ordre_struct.num_voie} {_ordre_struct.voie}".strip() if _ordre_struct else ""
    )
    ordre_cp = _ordre_struct.cp if _ordre_struct else ""
    ordre_ville = _ordre_struct.ville if _ordre_struct else ""
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
    banque_nom = _t(
        col_u, prefix, "banque_nom", "Banque", hint="ex : CIC CHAPEAU ROUGE BORDEAUX"
    )
    banque_adresse = _t(
        col_v, prefix, "banque_adresse", "Adresse banque", hint="ex : 5 place Bellecour, 69002 Lyon"
    )
    col_w, col_x, col_y = st.columns(3) if is_apport else (*st.columns(2), None)
    apport_montant = _t(col_w, prefix, "apport_montant", "Montant de l'apport")
    apport_nb_parts = _i(col_x, prefix, "apport_nb_parts", "Nombre de parts apportees")
    # Retour Albane 2026-07-07 (« je ne vois pas la possibilite de retirer la plage de
    # parts ??? ») : en CESSION, aucun document du bundle ne consomme `apport_plage`
    # (le PV/acte rendent la plage CEDEE, derivee — cf. _derive_cession_repartition) ->
    # champ ni affiche ni exige. Il reste saisi en APPORT : le contrat DOC-041 et les
    # statuts d'apport le rendent verbatim ([plage_parts_apportees]/[plage_parts_cedees]).
    apport_plage = (
        _t(col_y, prefix, "apport_plage", "Plage de parts (ex: 41 à 100)") if is_apport else ""
    )
    # Retour Rafael 2026-07-07 (fusion doublon) : « Valeur globale apportee » portait
    # TOUJOURS la meme valeur que « Montant de l'apport » (la valeur des parts
    # apportees) -> UNE seule saisie ; `apport_valeur_globale` est DERIVE (payload
    # inchange pour les generateurs : ApportTitres.valeur_globale, DOC-041/042/043).
    apport_valeur_globale = apport_montant

    st.markdown("**Societe cible**")
    cible_denomination = _t(st, prefix, "cible_denomination", "Dénomination cible (SEL)")
    # Retour Rafael 2026-07-07 : suppression du champ libre « Siege cible (affiche) »
    # (redondant). En CESSION, l'adresse de la cible est saisie au sous-formulaire
    # cession (ligne unique + case « Meme adresse que le siege de la SPFPL », cf.
    # _spfpl_cible_siege_input) -> plus de double-saisie. En APPORT (seul flux qui
    # consommait encore `cible_siege` : adresse_affichee de la societe cible,
    # DOC-036/041/042/043), on REUTILISE le meme patron ligne-unique + case ; la
    # cle payload `cible_siege` reste alimentee (derivee) -> generateurs inchanges.
    if is_apport:
        _cible_apport_struct = _parse_address_full(_spfpl_cible_siege_input(prefix))
        cible_siege = _cible_apport_struct.adresse_affichee if _cible_apport_struct else ""
    else:
        cible_siege = ""
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
    # N1 (retour Rafael 2026-07-09 soir) : selon que la societe cible emet des ACTIONS
    # (SELAS) ou des PARTS SOCIALES (SELARL), la note d'information (DOC-037) et les
    # PV/actes doivent employer le bon terme. La forme de la cible est un champ TEXTE
    # LIBRE (`cible_forme` / `cible_forme_complete`) -> le type de titre n'est PAS
    # deterministe depuis une donnee structuree ; on ajoute donc une saisie explicite
    # (suggestion Rafael « une case en plus »). Defaut « parts sociales » = comportement
    # actuel (flux SELARL cible valide, sortie byte-identique). En APPORT la nature est
    # deja saisie plus bas (« Nature des titres apportes ») -> on la REUTILISE au moment
    # d'assembler le payload (pas de double-saisie).
    cible_nature_titres = "parts sociales"
    if not is_apport:
        cible_nature_titres = st.selectbox(
            "Titres émis par la société cible",
            ("parts sociales", "actions"),
            key=f"{prefix}_cible_nature_titres",
            help=(
                "Pilote le vocabulaire (parts sociales / actions) dans la note "
                "d'information et les actes de cession. SELARL = parts sociales, "
                "SELAS = actions."
            ),
        )

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

    # --- Operation cession (DOC-037 note + DOC-038/039 PV agrement + DOC-040 acte) :
    # repartition des associes de la cible (avant/apres), parts cedees au holding, prix.
    cession_data: dict[str, object] = {"associes": []}
    if not is_apport:
        # Retour Albane 2026-07-07 : le CEDANT de la repartition = l'actionnaire
        # fondateur (le flux DOC-035/040 est mono-cedant) -> son identite pilote la
        # derivation « parts apres » (avant - cedees).
        cession_data = _render_spfpl_cession_cible(
            prefix, founder_prenom=prenom, founder_nom=nom
        )

    # Retour Rafael 2026-07-01 : exercice/cloture pre-remplis et recurrents -> volet replie.
    with st.expander(
        "Exercice comptable et clôture (pré-rempli — modifier si besoin)", expanded=False
    ):
        if is_apport:
            # SPFPL APPORT : l'exercice social est FIGE dans le modele d'apport (« commence le
            # 1er janvier et finit le 31 decembre », statuts_spfpl_templates.py:660). Aucun
            # generateur du bundle apport ne lit exercice.debut/fin (verifie) -> ces 2 selecteurs
            # etaient INUTILES en apport. On ne les DEMANDE plus ; valeurs figees au modele
            # (validation satisfaite, sortie byte-inchangee car jamais rendues). Seule la cloture
            # du 1er exercice reste saisie (elle, EST rendue en apport via date_cloture_premier).
            exercice_debut = "1er janvier"
            exercice_fin = "31 décembre"
            date_cloture = date_input_freeform(
                "Date de clôture du 1er exercice (ex : 31 décembre 2028)",
                key=f"{prefix}_date_cloture",
            )
        else:
            col_ad, col_ae, col_af = st.columns(3)
            exercice_debut = date_input_freeform(
                "Début de l'exercice comptable (ex : 1er janvier)",
                key=f"{prefix}_exercice_debut", container=col_ad,
            )
            exercice_fin = date_input_freeform(
                "Fin de l'exercice comptable (ex : 31 décembre)",
                key=f"{prefix}_exercice_fin", container=col_ae,
            )
            date_cloture = date_input_freeform(
                "Date de clôture du 1er exercice (ex : 31 décembre 2028)",
                key=f"{prefix}_date_cloture", container=col_af,
            )
    st.markdown("**Signature**")
    signature_lieu = _t(st, prefix, "signature_lieu", "Lieu de signature")
    signature_date = _date(prefix, "signature_date", "Date de signature")

    return {
        "structure": structure,
        "operation": operation,
        "is_apport": is_apport,
        "cession_data": cession_data,
        "denomination": denomination,
        # O24-03 : « siege » (affichage) derive du parse de la ligne unique.
        "siege": _siege_struct.adresse_affichee if _siege_struct else "",
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
        # §6.6 : profession saisie de l'associe unique (defaut « chirurgien-dentiste »,
        # modifiable). Propagee a founder.profession dans build_generation_context.
        "profession_associe_unique": profession_associe_unique,
        # §14.2 : genre derive de la civilite CIVILE (M./Mme), plus de selecteur
        # « Genre civil » redondant.
        "genre": derive_gender_from_civilite(civilite),
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        # Retour Rafael 2026-07-02 : le statut matrimonial CHOISI (collapse + accorde)
        # est porte dans le payload — plus de « marie » hardcode cote moteur. La
        # comparification (statuts / acte / PV) rend ce libelle verbatim.
        "situation_maritale": situation_maritale,
        "regime_matrimonial": regime,
        # O24-03 : « adresse » (affichage) derivee du parse de la ligne unique.
        "adresse": _adresse_struct.adresse_affichee if _adresse_struct else "",
        "adresse_num": adresse_num,
        "adresse_voie": adresse_voie,
        "adresse_cp": adresse_cp,
        "adresse_ville": adresse_ville,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "conjoint_civilite": conjoint_civilite,
        "conjoint_genre": derive_gender_from_civilite(conjoint_civilite),
        "conjoint_prenom": conjoint_prenom,
        "conjoint_nom": conjoint_nom,
        "regime_communautaire": regime_communautaire,
        "ordre_departement": ordre_departement,
        "connecteur_departement": connecteur_departement,
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        "ordre_president_feminin": ordre_president_feminin,
        "mandataire_prenom": mandataire_prenom,
        "mandataire_nom": mandataire_nom,
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
        # N1 : nature des titres de la cible (parts sociales / actions). En cession =
        # la saisie explicite ci-dessus ; en apport = la « Nature des titres apportes »
        # deja saisie (les titres apportes SONT ceux de la cible) -> source unique.
        "cible_nature_titres": (apport_nature_titres if is_apport else cible_nature_titres),
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
    elif operation == "cession":
        # PV agrement : associe unique de la cible (<=1 associe reel) -> DOC-038,
        # sinon plusieurs associes -> DOC-039.
        cession_data = payload.get("cession_data") or {}
        nb_real = len(cession_data.get("associes") or [])  # type: ignore[arg-type]
        pv_code = (
            SPFPL_CESSION_PV_UNIQUE_CODE if nb_real <= 1 else SPFPL_CESSION_PV_PLUSIEURS_CODE
        )
        document_codes = document_codes + (
            SPFPL_CESSION_NOTE_CODE,
            pv_code,
            SPFPL_CESSION_ACTE_PARTS_CODE,
            SPFPL_CESSION_ATTESTATION_CAPITAL_CODE,
        )
    all_blockers = _validate(payload)
    # KAN-2 (Rafael 2026-07-13) : un champ manquant ne BLOQUE plus la génération. Les zones
    # non renseignées sortent en « (À COMPLÉTER : … ) » (required_text, universel) et sont à
    # compléter à la main sur le DOCX. SEULE exception : les manques STRUCTURELS / NUMÉRIQUES
    # (nb d'actions/parts, capital non divisible, prix, dates, répartition cible) qui cassent
    # le calcul ou la structure du document — eux restent bloquants (`_HARD_BLOCKER_MESSAGES`).
    hard_blockers = tuple(b for b in all_blockers if b in _HARD_BLOCKER_MESSAGES)
    soft_gaps = tuple(b for b in all_blockers if b not in _HARD_BLOCKER_MESSAGES)
    warnings_list = [
        f"Dossier de création {structure} : associé unique.",
    ]
    if regime_communautaire:
        warnings_list.append(
            "Régime communautaire actif : la lettre de renonciation et la "
            "lettre d'avertissement au conjoint seront générées."
        )
    if soft_gaps:
        warnings_list.append(
            f"{len(soft_gaps)} champ(s) non renseigné(s) : les zones concernées sortiront "
            "en « (À COMPLÉTER : …) » et sont à compléter à la main dans le document."
        )
        warnings_list.extend(soft_gaps)
    warnings = tuple(warnings_list)
    if hard_blockers:
        return SpfplSlicePlan(
            can_generate=False,
            status="blocked",
            reason=hard_blockers[0],
            document_codes=document_codes,
            blockers=hard_blockers,
            warnings=warnings,
        )
    return SpfplSlicePlan(
        can_generate=True,
        status="ready" if not soft_gaps else "ready_with_gaps",
        reason=(
            f"Prêt pour la génération du dossier {structure}."
            if not soft_gaps
            else f"Génération possible — {len(soft_gaps)} zone(s) à compléter à la main."
        ),
        document_codes=document_codes,
        blockers=(),
        warnings=warnings,
    )


# KAN-2 (Rafael 2026-07-13) : manques STRUCTURELS / NUMÉRIQUES qui restent BLOQUANTS (ils
# cassent un calcul — valeur nominale = capital / nb actions, prix = prix_unitaire × nb — ou
# une itération de répartition, ou un formatage de date). Tout autre manque = champ TEXTE ->
# sort en « (À COMPLÉTER : …) » (required_text universel) sans bloquer. Doit rester STRICTEMENT
# synchronisé avec les messages de `_validate` ci-dessous.
_HARD_BLOCKER_MESSAGES: frozenset[str] = frozenset(
    {
        "Nombre d'actions requis et superieur a zero.",
        "Le capital social doit etre divisible par le nombre d'actions "
        "(la valeur nominale d'une action doit etre un nombre entier).",
        "Nombre de parts apportees requis et superieur a zero.",
        "Date de signature requise.",
        "Parts totales de la cible requises (note d'information).",
        "Parts apportees superieures aux parts totales de la societe cible (apport).",
        "Au moins un associe de la cible requis (cession).",
        "Nombre de parts cedees au holding requis (cession).",
        "Prix par part cedee requis (cession).",
        "Parts cedees au holding superieures aux parts detenues avant "
        "cession par le cedant (l'actionnaire fondateur) (cession).",
    }
)


def _validate(payload: dict[str, object]) -> tuple[str, ...]:  # noqa: C901
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
        ("adresse", "Adresse personnelle requise."),
        ("ordre_departement", "Departement ordre requis."),
        ("numero_ordre", "Numero ordre requis."),
        ("numero_rpps", "Numero RPPS requis."),
        ("banque_nom", "Banque requise."),
        ("banque_adresse", "Adresse banque requise."),
        ("apport_montant", "Montant de l'apport requis."),
        # Fusion Rafael 2026-07-07 : `apport_valeur_globale` est DERIVE de
        # `apport_montant` (plus de saisie propre) -> plus de blocker dedie.
        ("cible_denomination", "Denomination de la societe cible requise."),
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
        ("ordre_adresse_ligne_1", "Adresse de l'ordre requise (demande inscription)."),
        ("ordre_cp", "Code postal de l'ordre requis (demande inscription)."),
        ("ordre_ville", "Ville de l'ordre requise (demande inscription)."),
    )
    for field, message in required:
        if not str(payload.get(field) or "").strip():
            blockers.append(message)
    # Retour Rafael 2026-07-02 : le regime matrimonial ET le conjoint ne sont EXIGES
    # que pour un actionnaire MARIE (menu complet « Situation matrimoniale »). Un
    # celibataire / pacse / divorce / veuf rend juste son statut, sans conjoint : ne
    # plus bloquer « Regime matrimonial requis » / « conjoint requis » dans ce cas.
    if _spfpl_is_marie(payload):
        marie_required = (
            ("regime_matrimonial", "Regime matrimonial requis."),
            ("conjoint_prenom", "Prenom du conjoint requis."),
            ("conjoint_nom", "Nom du conjoint requis."),
        )
        for field, message in marie_required:
            if not str(payload.get(field) or "").strip():
                blockers.append(message)
    # Nombre d'actions VARIABLE (defaut 600) : doit etre >= 1 pour deriver une
    # valeur nominale coherente (capital / nb actions). Remplace l'ancien champ
    # « valeur nominale » en saisie libre (desormais calculee, non saisissable).
    # Dogfood 2026-06-22 : le « or 600 » NEUTRALISAIT cette garde (un 0 saisi devenait
    # 600 avant le test) -> 600 actions fantomes. On teste la valeur BRUTE.
    if int(payload.get("nb_actions_total") or 0) < 1:
        blockers.append("Nombre d'actions requis et superieur a zero.")
    # O24-05 (re-Akainu T4) : capital non divisible par le nb d'actions -> valeur nominale
    # fractionnaire (« 16.666... € ») dans le DOCX / lettres cassees. Garde partagee, meme
    # wording que civil/SAS/SELARL/SELAS.
    if not is_capital_divisible(payload.get("capital_social"), payload.get("nb_actions_total")):
        blockers.append(
            "Le capital social doit etre divisible par le nombre d'actions "
            "(la valeur nominale d'une action doit etre un nombre entier)."
        )
    if int(payload.get("apport_nb_parts") or 0) < 1:
        blockers.append("Nombre de parts apportees requis et superieur a zero.")
    if payload.get("signature_date") is None:
        blockers.append("Date de signature requise.")
    # SU4/SCS2 (Albane) : plus de blocker « Date de decision » — champ supprime (la date du PV =
    # la date de signature dans tous les cas, derivee par DecisionContext payload signature_date).
    # Operation apport : les documents DOC-041/042/043 exigent le detail des
    # titres + les organes de controle (commissaire aux apports + evaluateur) +
    # la forme/capital de la cible (sinon le generateur leve `required_*`).
    if bool(payload.get("is_apport")):
        apport_required = (
            # Retour Albane 2026-07-07 : la plage apportee n'est exigee qu'en APPORT
            # (seuls DOC-041 + statuts d'apport la rendent) ; en cession le champ
            # n'existe plus (la plage cedee est derivee).
            ("apport_plage", "Plage de parts apportees requise."),
            ("apport_valeur_par_titre", "Valeur d'un titre apporte requise (contrat d'apport)."),
            # Retour Rafael 2026-07-07 : le siege de la cible n'est plus un champ
            # commun (« Siege cible (affiche) » supprime) ; en APPORT il est saisi
            # via la ligne unique + case meme-adresse et DERIVE dans `cible_siege`.
            # En cession, le sous-formulaire porte ses propres gardes structurees.
            ("cible_siege", "Siege de la societe cible requis."),
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
        # Rafael 2026-07-09 : la note d'information (DOC-037, desormais dans le bundle
        # apport) rend la repartition APRES apport -> parts totales de la cible requises
        # et parts apportees <= parts totales (sinon repartition negative/incoherente).
        nb_total_cible = int(payload.get("cible_nb_parts") or 0)
        nb_apportees_cible = int(payload.get("apport_nb_parts") or 0)
        if nb_total_cible < 1:
            blockers.append("Parts totales de la cible requises (note d'information).")
        elif nb_apportees_cible > nb_total_cible:
            blockers.append(
                "Parts apportees superieures aux parts totales de la societe cible (apport)."
            )
    if str(payload.get("operation") or "") == "cession":
        # Operation cession : repartition de la cible + prix + siege cible exiges par
        # la note d'info (DOC-037), le PV d'agrement (DOC-038/039) et l'acte (DOC-040).
        cd = payload.get("cession_data") or {}
        if not (cd.get("associes") or []):  # type: ignore[union-attr]
            blockers.append("Au moins un associe de la cible requis (cession).")
        if int(cd.get("nb_cedees") or 0) < 1:  # type: ignore[union-attr]
            blockers.append("Nombre de parts cedees au holding requis (cession).")
        if not str(cd.get("prix_unitaire") or "").strip():  # type: ignore[union-attr]
            blockers.append("Prix par part cedee requis (cession).")
        if not str(cd.get("cible_siege_num") or "").strip():  # type: ignore[union-attr]
            blockers.append("Siege structure de la cible requis (cession).")
        # Dogfood 2026-06-22 : la note d'info / le PV / l'acte exigent aussi la FORME
        # complete de la cible, son siege complet et l'identite de chaque associe cible
        # (sinon `required_*` leve a la generation alors que le plan disait « pret »).
        if not str(cd.get("cible_forme_complete") or "").strip():  # type: ignore[union-attr]
            blockers.append("Forme sociale complete de la cible requise (cession).")
        if not all(
            str(cd.get(field) or "").strip()  # type: ignore[union-attr]
            for field in ("cible_siege_voie", "cible_siege_cp", "cible_siege_ville")
        ):
            blockers.append("Adresse complete du siege de la cible requise (voie, CP, ville).")
        for index, associe in enumerate(cd.get("associes") or [], start=1):  # type: ignore[union-attr]
            data = associe or {}
            if not all(str(data.get(key) or "").strip() for key in ("civilite", "prenom", "nom")):
                blockers.append(
                    f"Associe cible {index} : civilite, prenom et nom requis (cession)."
                )
        # Retour Albane 2026-07-07 : « parts apres » du cedant = avant - cedees (derive).
        # Un nb cede superieur aux parts AVANT du cedant rendrait une repartition fausse
        # (la derivation plafonne a 0) -> blocage explicite plutot qu'un crash aval.
        associes_cd = list(cd.get("associes") or [])  # type: ignore[union-attr]
        nb_cedees_cd = int(cd.get("nb_cedees") or 0)  # type: ignore[union-attr]
        if associes_cd and nb_cedees_cd >= 1:
            cedant_data = (
                associes_cd[
                    _cession_cedant_index(
                        associes_cd,
                        str(payload.get("prenom") or ""),
                        str(payload.get("nom") or ""),
                    )
                ]
                or {}
            )
            if nb_cedees_cd > int(cedant_data.get("avant") or 0):
                blockers.append(
                    "Parts cedees au holding superieures aux parts detenues avant "
                    "cession par le cedant (l'actionnaire fondateur) (cession)."
                )
    return tuple(dict.fromkeys(blockers))


def _spfpl_is_marie(payload: dict[str, object]) -> bool:
    """L'actionnaire fondateur est-il MARIE ? (regime + conjoint requis, comparution
    avec « sous le régime de ... avec <conjoint> »).

    Retour Rafael 2026-07-02 : le slice pose `situation_maritale` (collapse + accorde).
    On la teste en priorite (« marié »/« mariée » -> marie) ; a defaut (tests legacy
    fournissant seulement `regime_matrimonial`), un regime non vide vaut marie."""
    explicit = str(payload.get("situation_maritale") or "").strip().lower()
    explicit = explicit.replace("é", "e")
    if explicit:
        return explicit.startswith("marie")
    return bool(str(payload.get("regime_matrimonial") or "").strip())


def _spfpl_situation_maritale(payload: dict[str, object], genre: object) -> str:
    """Statut matrimonial (collapse + accorde au genre) de l'actionnaire fondateur.

    Retour Rafael 2026-07-02 : la SPFPL utilise desormais le menu complet
    « Situation matrimoniale » (comme les autres types) au lieu d'un « marie »
    hardcode. Le slice pose deja le libelle accorde dans `situation_maritale` ; on
    l'utilise en priorite. A defaut (appelants directs / tests legacy qui ne
    fournissent que `regime_matrimonial` + conjoint), on retombe sur « marié(e) »
    si un regime matrimonial non vide est present, sinon « célibataire »."""
    explicit = str(payload.get("situation_maritale") or "").strip()
    if explicit:
        return explicit
    has_regime = bool(str(payload.get("regime_matrimonial") or "").strip())
    return situation_display("marie" if has_regime else "celibataire", genre)


def build_generation_context(payload: dict[str, object]) -> DocumentGenerationContext:
    structure = str(payload["structure"])
    operation = str(payload["operation"])
    is_apport = bool(payload["is_apport"])
    # R5 (Albane 2026-07-07) : tous les champs MONTANT sont groupes par 3 (« 60 000 »)
    # A LA SOURCE (construction du contexte) — le capital partait brut (« 60000 ») dans
    # les statuts, attestations, PV, note d'information et actes. Idempotent, et les
    # derivations aval (lettres, valeur nominale) parsent les espaces.
    capital = group_montant(str(payload.get("capital_social") or ""))
    nb_parts = int(payload.get("apport_nb_parts") or 0)
    # Nombre d'actions du capital : VARIABLE (defaut 600 = ancien codage en dur,
    # preserve la sortie byte-identique des dossiers existants). La valeur nominale
    # derive de capital / nb_actions ; on respecte une valeur deja calculee fournie
    # par le slice, sinon on la (re)calcule pour les appelants directs.
    nb_actions_total = int(payload.get("nb_actions_total") or 600)
    valeur_action = group_montant(
        str(
            payload.get("valeur_nominale_action")
            or calculate_nominal_value(capital, nb_actions_total)
            or ""
        )
    )
    # Detail des titres apportes (operation apport). La valeur globale est saisie ;
    # la valeur par titre est saisie (valeur d'un titre de la cible apporte). Les
    # versions « en lettres » sont DERIVEES, comme partout dans le slice. Le nombre
    # d'actions SPFPL attribuees en contrepartie = le nombre total d'actions du
    # holding (l'apporteur, associe unique, recoit toutes les actions).
    nature_titres = str(payload.get("apport_nature_titres") or "parts sociales")
    # R5 : valeurs d'apport groupees par 3 (contrat d'apport DOC-041, attestations
    # DOC-042/043, article 6/8 des statuts d'apport).
    valeur_par_titre = group_montant(str(payload.get("apport_valeur_par_titre") or ""))
    valeur_globale = group_montant(str(payload.get("apport_valeur_globale") or ""))

    founder_genre = payload.get("genre") or Gender.MASCULIN
    founder = SpfplPerson(
        # SP2 (Rafael 2026-06-25) : civilite civile M./Mme, jamais « Docteur » (titre a part).
        civilite_affichage=str(payload.get("civilite") or "Monsieur"),
        prenom=str(payload.get("prenom") or ""),
        prenoms=str(payload.get("prenoms") or payload.get("prenom") or ""),
        nom=str(payload.get("nom") or ""),
        genre=founder_genre,
        # §6.6 (retour Albane) : profession de l'associe unique SAISIE (defaut
        # « chirurgien-dentiste », modifiable). Repli sur le defaut pour les appelants
        # directs / tests legacy qui ne fournissent pas le champ.
        profession=str(payload.get("profession_associe_unique") or "chirurgien-dentiste"),
        profession_reglementee="chirurgiens-dentistes",
        profession_reglementee_pluriel="chirurgiens-dentistes",
        # LIVE-03 : date de naissance a saisie LIBRE -> re-accentue les mois avant
        # injection dans les statuts SPFPL (echo fidele du modele). Saisie ISO
        # (12/04/1984) intacte ; saisie textuelle (« 12 avril 1984 ») accentuee.
        date_naissance=accentuate_french_months(str(payload.get("date_naissance") or "")),
        ville_naissance=str(payload.get("ville_naissance") or ""),
        departement_naissance=str(payload.get("departement_naissance") or ""),
        nationalite=str(payload.get("nationalite") or ""),
        # Retour Rafael 2026-07-02 : statut matrimonial du CHOIX (menu complet), plus
        # de « marie » hardcode. Le libelle est le collapse + accorde pose par le slice
        # (situation_maritale) ; a defaut (appelants directs qui ne fournissent que
        # regime + conjoint, ex. tests legacy) on retombe sur « marié(e) » si un regime
        # est present, sinon « célibataire ». L'acte de cession / la comparution rendent
        # cedant.situation_maritale verbatim (ACCENTUE et accorde au genre).
        situation_maritale=_spfpl_situation_maritale(payload, founder_genre),
        regime_matrimonial=str(payload.get("regime_matrimonial") or ""),
        conjoint=SpfplConjoint(
            civilite_affichage=str(payload.get("conjoint_civilite") or ""),
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
    # R5 : capital de la cible groupe par 3 (acte de cession, note d'information,
    # PV d'agrement : « au capital de 10 000 euros »).
    cible_capital = group_montant(str(payload.get("cible_capital") or ""))
    nb_apportees = nb_parts
    regime_communautaire_actif = bool(payload.get("regime_communautaire"))
    # --- Operation cession : repartition de la cible + pricing (DOC-037/038/039/040).
    cession_data = payload.get("cession_data") or {}
    cession_associes_raw = cession_data.get("associes") or []  # type: ignore[union-attr]
    nb_cedees = int(cession_data.get("nb_cedees") or 0)  # type: ignore[union-attr]
    prix_unitaire_num = _parse_amount(cession_data.get("prix_unitaire"))  # type: ignore[union-attr]
    prix_total_num = prix_unitaire_num * nb_cedees
    associe_unique_cible = len(cession_associes_raw) <= 1
    if is_apport:
        cession_parts_obj = CessionParts(
            nb_parts=nb_apportees,
            nb_parts_lettres=number_words_from_value(nb_apportees),
            plage_parts=_normalize_plage(payload.get("apport_plage")),
        )
    else:
        cession_parts_obj = CessionParts(
            nb_parts=nb_cedees,
            nb_parts_lettres=number_words_from_value(nb_cedees),
            plage_parts=str(cession_data.get("plage_cedee") or ""),  # type: ignore[union-attr]
            prix_unitaire=format_grouped_numeric_value(prix_unitaire_num),
            # B1 (Akainu 2026-07-06) : lettres SANS unite figee (« un », « mille »), comme la
            # valeur nominale art.8. L'acte accorde « euro(s) » au MONTANT via `euro_word`
            # (« un euro » pour 1, « mille euros » pour 1000) -> plus de « un euros » fige.
            prix_unitaire_lettres=prix_lettres_from_value(prix_unitaire_num),
            prix_total=format_grouped_numeric_value(prix_total_num),
            prix_total_lettres=prix_lettres_from_value(prix_total_num),
            nombre_exemplaires_lettres="trois",
        )
    ctx = DocumentGenerationContext(
        structure=structure,
        dossier_options=DossierOptions(
            apport=is_apport,
            cession=not is_apport,
            # PV d'agrement : en cession, le « associe unique » reflete la CIBLE
            # (1 associe reel -> DOC-038 ; sinon DOC-039). En apport, sans effet.
            associe_unique=(True if is_apport else associe_unique_cible),
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
            # SU3 (Albane 2026-06-25) : ville de signature = ville du siege, FORCE au moteur.
            lieu=str(payload.get("siege_ville") or payload.get("signature_lieu") or ""),
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
        # SCS2/SU4 (Albane 2026-06-25, propag. Q4) : date de decision (PV) = date de signature.
        decision=DecisionContext(date=_display_date(payload.get("signature_date"))),
        reunion=ReunionContext(
            # B1/SCS2 (Albane 2026-06-25) : date de reunion (PV) = date de signature.
            date_lettres=date_to_french_words(payload.get("signature_date")),
            # Annee en lettres + heure : exigees par le PV d'agrement de cession.
            # B1/SCS2 (Akainu re-gate) : l'annee aussi = date de signature (token voisin).
            annee_lettres=_annee_lettres(payload.get("signature_date")),
            heure="10 heures",
            president=ReunionPresident(
                civilite_affichage=str(payload.get("civilite") or "Monsieur"),
                prenom=str(payload.get("prenom") or ""),
                nom=str(payload.get("nom") or ""),
                # M1 (Akainu doc-entier 2026-07-09) : la qualite du president de seance reflete la
                # CIBLE. Cible a UN associe reel (DOC-038) -> « associé unique » ; cible MULTI
                # (DOC-039) -> « associé » GENERIQUE (le PV plusieurs contredisait « associé
                # unique »). La fonction EXACTE du president multi (gérant / associé) n'est pas
                # derivable du front (pas de champ dedie) -> defaut generique « associé », a
                # CONFIRMER cote metier. DOC-038 n'utilise pas ce champ (il rend le cedant).
                qualite="associé unique" if associe_unique_cible else "associé",
                civilite_president_seance=str(payload.get("civilite") or "Monsieur"),
                prenom_president_seance=str(payload.get("prenom") or ""),
                nom_personne_seance=str(payload.get("nom") or ""),
            ),
        ),
        cedant=founder if not is_apport else None,
        apporteur=founder if is_apport else None,
        operation_titres=OperationTitres(nb_titres=nb_apportees),
        # N1 (Rafael 2026-07-09 soir) : nature des titres de la cible (parts sociales /
        # actions) portee sur le champ CANON `operation_spfpl.nature_titres` (deja
        # reference par la selection de documents, cf. orchestrator `_acte_cession_*`).
        # Defaut « parts sociales » = comportement historique : « != actions » reste vrai
        # -> selection de documents inchangee, et les generateurs qui echoent encore
        # « parts » sortent a l'identique. Le generateur de la note d'information
        # (DOC-037) + PV agrement (DOC-038/039) doit lire ce champ pour basculer le
        # vocabulaire parts<->actions (travail d'un autre agent, cf. rapport).
        operation_spfpl=OperationSpfpl(
            type=operation,
            nature_titres=str(payload.get("cible_nature_titres") or "parts sociales"),
        ),
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
                # Civilite courte (M./Mme) : exigee par l'acte de cession (DOC-040).
                civilite_courte=(
                    "Mme"
                    if str(payload.get("civilite") or "").strip().lower() == "madame"
                    else "M."
                ),
                prenom=str(payload.get("prenom") or ""),
                nom=str(payload.get("nom") or ""),
                fonction="Président",
            ),
        ),
        actionnaire_unique=founder,
        apport=Apport(
            # R5 : montant d'apport groupe par 3 ; les lettres derivent de la valeur
            # brute (parse insensible aux espaces, sortie identique).
            # Rafael 2026-07-09 (double unite lettres DOC-005/006) : lettres NUES
            # (« soixante mille »), contrat IDENTIQUE aux slices SELARL/SELAS. Les
            # lettres portaient « euros » -> la lettre d'avertissement au conjoint
            # rendait « soixante mille euros (60 000) euros » et la renonciation
            # « (soixante mille euros) euros ». L'unite est composee au POINT DE
            # RENDU (statuts cession art. 6 : montant_lettres_avec_unite).
            montant=group_montant(str(payload.get("apport_montant") or "")),
            montant_lettres=number_words_from_value(payload.get("apport_montant")),
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
            plage_parts=_normalize_plage(payload.get("apport_plage")),
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
            # Forme complete : exigee par l'acte de cession (DOC-040). Saisie au
            # sous-formulaire cession ; repli sur la forme courte sinon.
            forme_sociale_complete=str(
                cession_data.get("cible_forme_complete")  # type: ignore[union-attr]
                or payload.get("cible_forme")
                or ""
            ),
            profession_reglementee=str(payload.get("cible_profession") or ""),
            capital_social=cible_capital,
            capital_social_lettres=number_words_from_value(cible_capital),
            nb_parts_total=int(payload.get("cible_nb_parts") or 0),
            # R5 : valeur nominale d'une part de la cible groupee par 3 (acte de cession).
            valeur_nominale_part=group_montant(str(payload.get("cible_valeur_part") or "")),
            valeur_nominale_part_lettres=number_words_from_value(
                payload.get("cible_valeur_part")
            ),
            siege=Address(
                num_voie=str(cession_data.get("cible_siege_num") or ""),  # type: ignore[union-attr]
                voie=str(cession_data.get("cible_siege_voie") or ""),  # type: ignore[union-attr]
                cp=str(cession_data.get("cible_siege_cp") or ""),  # type: ignore[union-attr]
                ville=str(cession_data.get("cible_siege_ville") or ""),  # type: ignore[union-attr]
                # O24-03 : affichage derive du parse de la ligne unique (cession),
                # repli sur `cible_siege` (APPORT : derive de la ligne unique du
                # bloc « Societe cible » depuis Rafael 2026-07-07 ; legacy : brut).
                adresse_affichee=str(
                    cession_data.get("cible_siege_affiche")  # type: ignore[union-attr]
                    or payload.get("cible_siege")
                    or ""
                ),
            ),
            ville_rcs=str(payload.get("cible_ville_rcs") or ""),
            numero_rcs=str(payload.get("cible_numero_rcs") or ""),
        ),
        cession_parts=cession_parts_obj,
        # Rafael 2026-07-09 : la note d'information (DOC-037) sort AUSSI en apport ->
        # elle exige la repartition APRES operation. En apport elle est DERIVEE (pas de
        # roster saisi, flux mono-detenteur V1) : le fondateur garde (total - apportees),
        # le holding recoit les parts apportees (plage saisie).
        associes_cible=(
            _build_associes_cible(payload)
            if not is_apport
            else _build_associes_cible_apport(payload)
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
                    civilite_affichage=str(payload.get("civilite") or "Monsieur"),  # SP2
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
            # LIVE-03 : re-accentue les mois saisis librement (« 1er aout » -> « 1er août »)
            # EN AMONT du generateur, qui reste un echo fidele du modele. debut accentue
            # comme fin/cloture (oubli releve par re-Akainu T4).
            debut=accentuate_french_months(str(payload.get("exercice_debut") or "")),
            fin=accentuate_french_months(str(payload.get("exercice_fin") or "")),
            date_cloture_premier_exercice=accentuate_french_months(
                str(payload.get("date_cloture") or "")
            ),
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
        metadata={
            "front_slice": f"track_b_spfpl_{operation}_v1",
            # C4 (Rafael 2026-07-09 soir) : n° de l'article du capital social de la SEL
            # cible dans le PV d'agrement (DOC-038/039), aujourd'hui code en dur « 7 bis »
            # cote generateur (pv_agrement_common.add_article_7_bis, DEUX occurrences).
            # Le front le rend saisissable et le passe via metadata (canal front->generation
            # deja utilise, cf. slices SELAS) ; le generateur (autre agent) doit lire
            # ctx.metadata.get("pv_article_capital_numero", "7 bis"). Defaut « 7 bis »
            # -> sortie inchangee tant que non modifie.
            "pv_article_capital_numero": str(
                cession_data.get("article_capital_numero") or "7 bis"
            ),
        },
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


def _professional_entity(payload: dict[str, object], role: str) -> ProfessionalEntity:
    """Construit une entite professionnelle (commissaire / evaluateur) du payload.

    KAN-2 (Rafael 2026-07-13) : l'entite est TOUJOURS construite, meme denomination vide ->
    les champs non renseignes sortent en « (À COMPLÉTER : …) » via les generateurs (required_*),
    a completer a la main, au lieu de renvoyer None et de faire echouer la generation apport
    (attestations DOC-042/043, statuts). Le manque de commissaire/evaluateur ne BLOQUE plus.
    """
    denomination = str(payload.get(f"{role}_denomination") or "")
    return ProfessionalEntity(
        denomination=denomination,
        forme_sociale=str(payload.get(f"{role}_forme") or ""),
        # R5 : capital du commissaire / evaluateur groupe par 3 (presentation DOC-041/043).
        capital_social=group_montant(str(payload.get(f"{role}_capital") or "")),
        siege=Address(adresse_affichee=str(payload.get(f"{role}_siege") or "")),
        ville_rcs=str(payload.get(f"{role}_ville_rcs") or ""),
        numero_rcs=str(payload.get(f"{role}_numero_rcs") or ""),
        representant=SpfplRepresentant(
            civilite_affichage=str(payload.get(f"{role}_rep_civilite") or ""),
            prenom=str(payload.get(f"{role}_rep_prenom") or ""),
            nom=str(payload.get(f"{role}_rep_nom") or ""),
        ),
    )


def _spfpl_cible_siege_input(prefix: str) -> str:
    """Adresse du siege de la cible + case « Meme adresse que le siege de la SPFPL ».

    Partage CESSION (sous-formulaire) / APPORT (bloc « Societe cible » — retour
    Rafael 2026-07-07 : remplace le champ libre « Siege cible (affiche) » supprime).
    La cle de widget `*_cible_siege_cession` est historique (nee cote cession) et
    conservee telle quelle pour les deux flux (un seul des deux rend le widget).

    §6.1 (retour Albane) : reutilise le patron O24-12 SELAS (shell.py:1414-1439). La
    SAISIE MANUELLE vit dans `manual_key` (jamais ecrasee par le report) ; le champ
    visible (`field_key`) est pilote par l'etat de la case :
      - cochee + siege SPFPL renseigne -> MIROIR du siege SPFPL, champ DESACTIVE ;
      - sinon (decochee, ou cochee mais siege vide) -> EDITABLE, valeur = saisie manuelle.
    A la transition coche->decoche on RESTAURE `manual_key`. En mode editable on
    resynchronise `manual_key` APRES le widget -> la saisie survit a tout cycle coche/decoche.
    """
    field_key = f"{prefix}_cible_siege_cession"
    prev_key = f"{prefix}_cible_siege_meme_spfpl_prev"
    manual_key = f"{prefix}_cible_siege_manuelle"
    if field_key not in st.session_state:
        st.session_state[field_key] = ""
    # Adresse du siege de la SPFPL saisie plus haut dans le meme run (champ une-ligne).
    siege_spfpl = str(st.session_state.get(f"{prefix}_siege") or "").strip()
    was_checked = bool(st.session_state.get(prev_key))
    checked = st.checkbox(
        "Même adresse que le siège de la SPFPL",
        key=f"{prefix}_cible_siege_meme_spfpl",
        help="Coché : recopie l'adresse du siège de la SPFPL dans l'adresse de la cible.",
    )
    locked = False
    if checked and siege_spfpl:
        st.session_state[field_key] = siege_spfpl  # miroir non editable
        locked = True
    elif was_checked and not checked:
        # Coche -> decoche : restaurer la derniere saisie manuelle.
        st.session_state[field_key] = str(st.session_state.get(manual_key) or "")
    st.session_state[prev_key] = checked
    value = str(
        copyable_text_input(
            st,
            "Adresse du siège de la cible (N° et voie, CP Ville)",
            key=field_key,
            disabled=locked,
        )
    ).strip()
    if not locked:
        # En mode editable, la valeur courante EST la saisie manuelle -> memorisee
        # pour survivre a un futur report (coche).
        st.session_state[manual_key] = value
    return value


def _cession_cedant_index(
    associes: list[dict[str, object]], founder_prenom: str, founder_nom: str
) -> int:
    """Ligne du CEDANT dans la repartition de la cible (Albane 2026-07-07).

    Le flux SPFPL cession est MONO-cedant : le cedant de l'acte (DOC-040) est TOUJOURS
    l'actionnaire fondateur du holding (`cedant=founder` au contexte). On le retrouve
    par prenom + nom (insensible a la casse/espaces) ; a defaut de correspondance, la
    1re ligne (le fondateur se liste en premier — convention des fixtures et des
    dossiers valides).
    """
    target = (founder_prenom.strip().casefold(), founder_nom.strip().casefold())
    if target[1]:
        for index, associe in enumerate(associes):
            pair = (
                str(associe.get("prenom") or "").strip().casefold(),
                str(associe.get("nom") or "").strip().casefold(),
            )
            if pair == target:
                return index
    return 0


def _derive_cession_repartition(
    associes: list[dict[str, object]],
    nb_cedees: int,
    founder_prenom: str,
    founder_nom: str,
) -> tuple[str, int]:
    """Derive IN PLACE la repartition APRES cession + les plages (Albane 2026-07-07).

    « Le systeme parts avant / parts apres / plage n'est pas intuitif ni pertinent
    puisqu'il peut etre DEDUIT. Calcul automatique. » :
      - parts APRES = parts avant, sauf le CEDANT (l'actionnaire fondateur) qui perd
        les parts cedees au holding (plancher 0 ; l'exces est bloque par _validate) ;
      - plages = attribution contigue sequentielle sur la repartition APRES, dans
        l'ordre des lignes, holding acquereur en DERNIER (patron ratifie du repeater
        civil §18.5 et de la SCM N4) — reproduit exactement les plages des dossiers
        valides (« 1 à 10 » / « 11 à 40 » / « 41 à 100 »).
    Complete chaque associe (cles `apres` + `plage`, memes cles payload qu'avant) et
    renvoie (plage_cedee, index_cedant). Un nb <= 0 rend une plage vide (la mention
    « numérotées de ... » est alors omise par les generateurs, comportement historique).
    """
    cedant_index = _cession_cedant_index(associes, founder_prenom, founder_nom)
    for index, associe in enumerate(associes):
        avant = int(associe.get("avant") or 0)
        associe["apres"] = max(avant - nb_cedees, 0) if index == cedant_index else avant
    plages = derive_cumulative_plages(
        [int(a.get("apres") or 0) for a in associes] + [max(nb_cedees, 0)]
    )
    for associe, plage in zip(associes, plages[:-1], strict=True):
        associe["plage"] = plage
    return plages[-1], cedant_index


def _remove_cession_associe(prefix: str, index: int) -> None:
    """Retire l'associe cible `index` (bouton par ligne — retour Albane 2026-07-07).

    Callback `on_click` (pre-rerun) : recopie les lignes suivantes d'un cran et
    decremente le number_input compteur AVANT son instanciation (seule fenetre ou
    Streamlit autorise ces mutations de session_state).
    """
    count_key = f"{prefix}_cession_nb_associes"
    count = int(st.session_state.get(count_key) or 0)
    if count <= 1:
        return
    shift_repeater_rows_down(st.session_state, f"{prefix}_cession_assoc_", index, count)
    st.session_state[count_key] = count - 1


def _display_cession_repartition(
    associes: list[dict[str, object]],
    nb_cedees: int,
    plage_cedee: str,
    cedant_index: int,
) -> None:
    """Affichage LECTURE SEULE de la repartition apres cession (Albane 2026-07-07 :
    plus de saisie manuelle « parts apres » / « plage » — valeurs deduites)."""
    st.caption("Répartition après cession — calculée automatiquement :")
    for index, associe in enumerate(associes):
        nb = int(associe.get("apres") or 0)
        who = " ".join(
            str(associe.get(champ) or "").strip()
            for champ in ("civilite", "prenom", "nom")
        ).strip()
        marque = " (cédant)" if index == cedant_index else ""
        plage = str(associe.get("plage") or "")
        mention = f", numérotées de {plage}" if plage else ""
        st.caption(f"– {who or f'Associé cible {index + 1}'}{marque} : {nb} part(s){mention}")
    mention = f", numérotées de {plage_cedee}" if plage_cedee else ""
    st.caption(f"– Holding acquéreur : {nb_cedees} part(s) cédée(s){mention}")


def _render_spfpl_cession_cible(
    prefix: str, founder_prenom: str = "", founder_nom: str = ""
) -> dict[str, object]:
    """Sous-formulaire cession SPFPL : repartition des associes de la cible,
    parts cedees au holding, prix par part, forme complete de la cible.
    Alimente la note d'info (DOC-037), le PV d'agrement (DOC-038/039) et l'acte (DOC-040).

    Retour Albane 2026-07-07 : « parts apres » et « plage » ne se SAISISSENT plus —
    ils sont DEDUITS (cf. _derive_cession_repartition) et affiches en lecture seule ;
    chaque ligne d'associe porte son bouton « Retirer » (plus seulement le dernier).
    """
    st.markdown("**Cession — repartition de la cible & prix**")
    col_a, col_b = st.columns(2)
    nb_cedees = _i(col_a, prefix, "cession_nb_parts_cedees", "Parts cédées à la holding")
    prix_unitaire = _t(
        col_b, prefix, "cession_prix_unitaire", "Prix par part", hint="ex : 1 000"
    )
    # Retour Albane 2026-07-07 (« je ne vois pas la possibilite de retirer la plage de
    # parts ») : le champ « Plage parts cedees » est RETIRE — la plage cedee est DERIVEE
    # (dernieres parts de la numerotation apres cession, cf. _derive_cession_repartition).
    cible_forme_complete = _t(
        st,
        prefix,
        "cible_forme_complete",
        "Forme complete de la cible",
        hint="ex : societe d'exercice liberal a responsabilite limitee",
    )
    # C4 (retour Rafael 2026-07-09 soir) : n° de l'article du capital social de la SEL
    # cible dans la 2e resolution du PV d'agrement (DOC-038/039). Etait code en dur
    # « 7 bis » cote generateur -> SAISISSABLE (defaut « 7 bis » seede dans render_spfpl_form).
    article_capital_numero = _t(
        st,
        prefix,
        "pv_article_capital_numero",
        "N° de l'article du capital social de la SEL cible",
        hint="défaut : 7 bis",
    )
    # O24-03 : siege de la cible sur UNE ligne (parse interne -> num/voie/cp/ville
    # exiges par l'acte/PV de cession). Remplace l'ancienne grille No/Voie/CP/Ville
    # ET le champ « Siege cible (affiche) » du bloc principal (double-saisie).
    # §6.1 (retour Albane) : case « Meme adresse que le siege de la SPFPL » -> recopie
    # l'adresse du siege SPFPL dans l'adresse cible ; champ desactive (miroir) mais la
    # saisie manuelle survit a la decoche (patron O24-12 SELAS, shell.py:1414-1439).
    cible_siege_ligne = _spfpl_cible_siege_input(prefix)
    _cible_struct = _parse_address_full(cible_siege_ligne)
    cible_siege_num = _cible_struct.num_voie if _cible_struct else ""
    cible_siege_voie = _cible_struct.voie if _cible_struct else ""
    cible_siege_cp = _cible_struct.cp if _cible_struct else ""
    cible_siege_ville = _cible_struct.ville if _cible_struct else ""
    cible_siege_affiche = _cible_struct.adresse_affichee if _cible_struct else ""
    nb_associes = int(
        st.number_input(
            "Nombre d'associes de la cible (hors holding acquereur)",
            min_value=1,
            max_value=6,
            step=1,
            key=f"{prefix}_cession_nb_associes",
        )
    )
    associes: list[dict[str, object]] = []
    for i in range(nb_associes):
        st.caption(f"Associe cible {i + 1}")
        c1, c2, c3 = st.columns(3)
        # Akainu M1 (2026-07-09) : « Docteur » n'est PAS une civilite (racine du retour
        # recurrent Rafael) -> selectbox M./Mme seulement. Le genre en derive -> la
        # repartition rend « Madame Louise Bernard » (plus de defaut masculin sur « Docteur »).
        civ = c1.selectbox(
            "Civilite",
            ("Monsieur", "Madame"),
            key=f"{prefix}_cession_assoc_{i}_civ",
        )
        pre = _t(c2, prefix, f"cession_assoc_{i}_prenom", "Prenom")
        nom = _t(c3, prefix, f"cession_assoc_{i}_nom", "Nom")
        # Retour Albane 2026-07-07 : seules les parts AVANT se saisissent ; « parts
        # apres » et « plage » sont DEDUITS (affiches en lecture seule sous le bloc).
        c4, c5 = st.columns([1, 2])
        avant = _i(c4, prefix, f"cession_assoc_{i}_avant", "Parts avant")
        # Retour Albane 2026-07-07 : bouton « Retirer » PAR associe (aujourd'hui on ne
        # peut que supprimer le dernier ajoute). on_click : recopie pre-rerun des cles.
        c5.button(
            "Retirer cet associé",
            key=f"{prefix}_cession_remove_assoc_{i}",
            on_click=_remove_cession_associe,
            args=(prefix, i),
            disabled=nb_associes <= 1,
        )
        associes.append({"civilite": civ, "prenom": pre, "nom": nom, "avant": avant})
    plage_cedee, cedant_index = _derive_cession_repartition(
        associes, nb_cedees, founder_prenom, founder_nom
    )
    _display_cession_repartition(associes, nb_cedees, plage_cedee, cedant_index)
    return {
        "nb_cedees": nb_cedees,
        "prix_unitaire": prix_unitaire,
        "plage_cedee": plage_cedee,
        "cible_forme_complete": cible_forme_complete,
        # C4 : n° d'article capital de la SEL cible (defaut « 7 bis »), consomme par le
        # generateur PV d'agrement via ctx.metadata["pv_article_capital_numero"].
        "article_capital_numero": article_capital_numero or "7 bis",
        "cible_siege_num": cible_siege_num,
        "cible_siege_voie": cible_siege_voie,
        "cible_siege_cp": cible_siege_cp,
        "cible_siege_ville": cible_siege_ville,
        "cible_siege_affiche": cible_siege_affiche,
        "associes": associes,
    }


def _parse_amount(value: object) -> int:
    """Parse un montant saisi (« 1 000 », « 1000 ») en entier (espaces/insecables retires)."""
    raw = str(value or "").replace(" ", "").replace(" ", "").replace("\xa0", "")
    digits = "".join(c for c in raw if c.isdigit())
    return int(digits) if digits else 0


def _normalize_plage(value: object) -> str:
    """Normalise l'accent d'une plage saisie en texte libre (« 41 a 100 » -> « 41 à 100 »).

    M3 (Akainu doc-entier 2026-07-07) : la plage APPORT reste saisie a la main et partait
    verbatim dans les statuts/contrat (« numérotées de 41 a 100 ») — un « a » nu induit par
    l'ancien exemple du libelle. La plage CESSION est, elle, auto-derivee accentuee (N4)."""
    return str(value or "").replace(" a ", " à ")


def _annee_lettres(value: object) -> str:
    """Annee en lettres a partir d'une date (ex. 2026 -> « deux mille vingt-six »)."""
    if isinstance(value, date):
        return number_words_from_value(value.year)
    return ""


def _build_associes_cible(payload: dict[str, object]) -> list[object]:
    """Construit la liste AssocieCible (vendeurs/restants de la cible + holding
    acquereur en personne morale qui recoit les parts cedees)."""
    from sydel_doc_engine.domain.models import AssocieCible

    cession_data = payload.get("cession_data") or {}
    raw = cession_data.get("associes") or []  # type: ignore[union-attr]
    nb_cedees = int(cession_data.get("nb_cedees") or 0)  # type: ignore[union-attr]
    associes: list[object] = [
        AssocieCible(
            civilite_affichage=str(a.get("civilite") or "Monsieur"),  # SP2
            prenom=str(a.get("prenom") or ""),
            nom=str(a.get("nom") or ""),
            nb_parts_avant=int(a.get("avant") or 0),
            nb_parts_apres=int(a.get("apres") or 0),
            plage_parts=str(a.get("plage") or ""),
        )
        for a in raw
    ]
    # Le holding acquereur (personne morale) recoit les parts cedees.
    associes.append(
        AssocieCible(
            type="personne_morale",
            denomination=str(payload.get("denomination") or ""),
            nb_parts_avant=0,
            nb_parts_apres=nb_cedees,
            plage_parts=str(cession_data.get("plage_cedee") or ""),  # type: ignore[union-attr]
            est_present_ou_represente=False,
        )
    )
    return associes


def _build_associes_cible_apport(payload: dict[str, object]) -> list[object]:
    """Repartition APRES apport de la cible, DERIVEE (Rafael 2026-07-09, DOC-037 apport).

    Le flux apport V1 est mono-detenteur : l'actionnaire fondateur detient les parts de
    la cible et en apporte une partie au holding. Apres l'operation :
      - le fondateur garde `cible_nb_parts - apport_nb_parts` (plage restante NON saisie
        -> omise, la note n'ecrit jamais une numerotation inventee) ;
      - le holding (personne morale) recoit `apport_nb_parts`, plage = la plage
        apportee SAISIE (normalisee « 41 à 100 »).
    La somme vaut `cible_nb_parts` par construction (garde `_validate` : apportees
    <= parts totales de la cible).
    """
    from sydel_doc_engine.domain.models import AssocieCible

    nb_total = int(payload.get("cible_nb_parts") or 0)
    nb_apportees = int(payload.get("apport_nb_parts") or 0)
    return [
        AssocieCible(
            civilite_affichage=str(payload.get("civilite") or "Monsieur"),
            prenom=str(payload.get("prenom") or ""),
            nom=str(payload.get("nom") or ""),
            nb_parts_avant=nb_total,
            nb_parts_apres=max(nb_total - nb_apportees, 0),
        ),
        AssocieCible(
            type="personne_morale",
            denomination=str(payload.get("denomination") or ""),
            nb_parts_avant=0,
            nb_parts_apres=nb_apportees,
            plage_parts=_normalize_plage(payload.get("apport_plage")),
            est_present_ou_represente=False,
        ),
    ]


def _spfpl_ordre_professionnel(payload: dict[str, object]) -> OrdreProfessionnel:
    ligne_1 = str(payload.get("ordre_adresse_ligne_1") or "")
    cp = str(payload.get("ordre_cp") or "")
    ville = str(payload.get("ordre_ville") or "")
    bloc = f"{ligne_1}\n{cp} {ville}"
    return OrdreProfessionnel(
        # conseil_departemental_libelle : champ vestigial retire du front (retour Albane
        # 9.4). Le libelle destinataire est DERIVE de departement_inscription (+ connecteur)
        # par le generateur DOC-034 -> on n'alimente plus ce champ (vide, jamais rendu).
        departement_inscription=str(payload.get("ordre_departement") or ""),
        # KAN-1 : connecteur grammatical choisi au formulaire (de/du/des), passe au generateur
        # de la demande d'inscription (DOC-034) qui rend « <connecteur> <departement> ».
        connecteur_departement=str(payload.get("connecteur_departement") or "de"),
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
    docx_paths = rename_dnc_with_signataire(docx_paths, ctx)  # O24-02 : DNC nommee par le dirigeant
    # Procuration SEL (Albane 2026-07-10, IMG_7852) : en CESSION, DEUX procurations sont
    # requises — une au nom de la SPFPL (deja dans docx_paths) + une au nom de la SOCIETE
    # CIBLE (SEL). Meme modele DOC-003, regenere avec la societe = cible, sous un nom de
    # fichier distinct « procuration_SEL.docx ». L'attestation de depot des parts n'est PAS
    # requise (rien a faire de ce cote).
    sel_procuration = _generate_procuration_sel(ctx, output_dir)
    if sel_procuration is not None:
        docx_paths = [*docx_paths, sel_procuration]
    zip_path = generate_zip_file(output_dir, docx_paths)
    return GeneratedDossier(
        output_dir=output_dir,
        docx_paths=docx_paths,
        pdf_results=[],
        zip_path=zip_path,
    )


def _generate_procuration_sel(
    ctx: DocumentGenerationContext, output_dir: Path
) -> Path | None:
    """2e procuration (DOC-003) au nom de la SOCIETE CIBLE (SEL) — cession SPFPL uniquement.

    Meme modele que la procuration SPFPL, regenere avec `ctx.societe` = la cible SEL
    (denomination / forme / siege / capital / RCS). Ecrit « procuration_SEL.docx » (distinct
    de « procuration.docx »). No-op si l'operation n'est pas une cession ou si les donnees
    minimales de la cible (forme + denomination + siege) manquent -> jamais bloquant.

    NB metier a confirmer avec Albane : le REPRESENTANT de la SEL dans cette procuration
    reste le signataire du dossier (le fondateur / associe unique de la SPFPL). Si la SEL
    cible a un dirigeant distinct, ce champ devra etre saisi separement.
    """
    options = ctx.dossier_options
    if options is None or not options.cession:
        return None
    cible = ctx.societe_cible
    if cible is None:
        return None
    siege = cible.siege
    siege_ok = siege is not None and bool(
        (siege.adresse_affichee or "").strip()
        or ((siege.voie or "").strip() and (siege.ville or "").strip())
    )
    if not (
        (cible.forme_sociale or "").strip()
        and (cible.denomination or "").strip()
        and siege_ok
    ):
        return None
    cible_company = Company(
        forme_sociale=cible.forme_sociale or "",
        forme_sociale_affichage=cible.forme_sociale or "",
        forme_sociale_abregee=cible.forme_sociale or "",
        forme_sociale_complete=cible.forme_sociale_complete or cible.forme_sociale or "",
        denomination=cible.denomination or "",
        denomination_courte=cible.denomination or "",
        capital=cible.capital_social or "",
        capital_social=cible.capital_social or "",
        siege=siege,
        ville_rcs=cible.ville_rcs or "",
    )
    cible_ctx = ctx.model_copy(update={"societe": cible_company})
    tmp_dir = output_dir / "_procuration_sel"
    generated = generate_docx_files_for_document_codes(
        cible_ctx, tmp_dir, (cc.DOC_PROCURATION,)
    )
    if not generated:
        return None
    target = output_dir / "procuration_SEL.docx"
    if target.exists():
        target.unlink()
    generated[0].replace(target)
    try:
        tmp_dir.rmdir()
    except OSError:
        pass
    return target


def _t(container, prefix: str, field: str, label: str, hint: str | None = None) -> str:
    # C2 : helper canonique partage (front_app/_field_inputs). Comportement inchange.
    return text_input_prefixed(container, prefix, field, label, hint)


def _i(container, prefix: str, field: str, label: str) -> int:
    key = f"{prefix}_{field}"
    if key not in st.session_state:
        st.session_state[key] = 0
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _date(prefix: str, field: str, label: str) -> date | None:
    # Consomme la couche de rendu partagee (front_widgets) au lieu de reimplementer
    # le helper localement (cause racine des ecarts de parite).
    return date_input_with_today(label, key=f"{prefix}_{field}", value=date.today())
