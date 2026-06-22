from __future__ import annotations

import random
import re
from datetime import date
from pathlib import Path

import streamlit as st

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    BailContext,
    CessionContext,
    ScmCessionAssocie,
    ScmCessionContext,
    ScmCessionPartsAttribution,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
)
from sydel_doc_engine.front_app.data_entry import (
    CleanDataEntry,
    build_clean_data_entry,
)
from sydel_doc_engine.front_app.dossier_selection import (
    DossierTypeOption,
    dossier_type_by_label,
    dossier_type_labels,
)
from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
    DEFAULT_TITRE_AFFICHAGE,
    MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE,
    MATRIMONIAL_STATUS_PRESETS,
    NATIONALITY_PRESETS,
    calculate_nominal_value,
    derive_gender_from_civilite,
    format_french_date,
    format_grouped_numeric_value,
    format_numeric_value,
    matrimonial_status_value,
    number_words_from_value,
    parse_french_date,
    regime_communautaire_from_status,
    regime_matrimonial_from_status,
)
from sydel_doc_engine.front_app.generation import (
    CleanGenerationPlan,
    build_clean_generation_plan,
)
from sydel_doc_engine.front_app.selarl_slice import (
    PROFESSION_DENTISTE,
    PROFESSION_MEDECIN,
    generate_selarl_dossier,
)
from sydel_doc_engine.scenarios.selarl import scm_cession_fixture
from sydel_doc_engine.utils.grammar import euro_word

ARTIFACTS_DIR = Path("artifacts") / "track_b_selarl_v1"
GENERATED_DOSSIER_STATE_KEY = "clean_generated_dossier"
DOCX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def render_clean_front() -> None:
    st.title("SYDEL Track B")
    st.caption(
        "Front clean Track B : creation multi-types (SELARL, SCM, SCI, SCI IRIS, SCS, SAS, "
        "SPFPL, SELAS), sans ecrans legacy ni outils internes."
    )
    dossier_type = _render_dossier_type_selection()
    # SELARL = chemin historique EXACT (front valide client) : on ne touche a rien.
    if dossier_type.structure == "SELARL":
        data_entry = _render_data_entry_zone(dossier_type)
        generation_plan = build_clean_generation_plan(dossier_type, data_entry)
        _render_generation_zone(data_entry, generation_plan)
        return
    # Tous les autres types : routage vers leur slice dedie.
    _render_typed_dossier(dossier_type)


def _render_dossier_type_selection() -> DossierTypeOption:
    st.subheader("Type de dossier")
    selected_label = st.selectbox(
        "Type de dossier",
        dossier_type_labels(),
        key="clean_dossier_type",
    )
    selected = dossier_type_by_label(selected_label)
    if selected.structure == "SELARL":
        if st.button("Generer des donnees de test", key="clean_generate_test_data"):
            _prefill_random_selarl_data()
            st.success("Donnees de test coherentes pre-remplies.")
        st.caption("Perimetre actif : SELARL unipersonnelle de production.")
    else:
        # Une cle de type peut surcharger le prefill par defaut de sa structure
        # (ex. SELAS dentiste pluripersonnelle -> prefill SELAS en dentiste).
        prefill = _TYPED_TEST_DATA_PREFILL_BY_KEY.get(
            selected.key
        ) or _TYPED_TEST_DATA_PREFILL.get(selected.structure)
        if prefill is not None and st.button(
            "Generer des donnees de test",
            key=f"clean_test_data_{selected.structure}".replace(" ", "_"),
        ):
            prefill()
            st.success("Donnees de test coherentes pre-remplies.")
        st.caption(f"Perimetre actif : {selected.label} ({selected.structure}).")
    return selected


def _prefill_random_selarl_data() -> None:
    person = random.choice(_test_people())
    company = random.choice(_test_companies())
    capital, parts = random.choice(((1000, 100), (2000, 200), (5000, 500), (10000, 1000)))
    # Respecte la profession deja choisie dans le wizard pour que la cession
    # preremplie soit coherente (medical vs dentaire) ; defaut Medecin.
    profession_label = st.session_state.get("selarl_profession") or "Medecin"
    if profession_label not in ("Medecin", "Chirurgien-dentiste"):
        profession_label = "Medecin"
    regime_communautaire = profession_label == "Chirurgien-dentiste" or random.choice(
        (False, True)
    )
    today_text = format_french_date(date.today())
    dossier_suffix = random.randint(1000, 9999)
    status = (
        MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE
        if regime_communautaire
        else random.choice(
            tuple(
                item
                for item in MATRIMONIAL_STATUS_PRESETS
                if item != MATRIMONIAL_STATUS_MARRIED_COMMUNAUTE
            )
        )
    )

    profession_key = (
        PROFESSION_DENTISTE if profession_label == "Chirurgien-dentiste" else PROFESSION_MEDECIN
    )

    values = {
        "selarl_profession": profession_label,
        "selarl_dossier_unipersonnel": True,
        "selarl_cession": True,
        "selarl_scm": True,
        "selarl_dossier_reference": f"TEST-SELARL-{dossier_suffix}",
        "selarl_civilite": person["civilite"],
        "selarl_prenom": person["prenom"],
        "selarl_nom": person["nom"],
        "selarl_date_naissance": person["date_naissance"],
        "selarl_ville_naissance": person["ville_naissance"],
        "selarl_ville_naissance_article_au": False,
        "selarl_departement_naissance": person["departement_naissance"],
        "selarl_nationalite_choice": random.choice(NATIONALITY_PRESETS[:-1]),
        "selarl_nationalite_other": "",
        "selarl_situation_maritale": status,
        "selarl_numero_ordre": f"ORD-{random.randint(100000, 999999)}",
        "selarl_numero_rpps": str(random.randint(10000000000, 19999999999)),
        "selarl_nom_pere": person["nom_pere"],
        "selarl_nom_mere": person["nom_mere"],
        # Numero et voie fusionnes (ticket 1.5).
        "selarl_adresse_voie": f"{person['adresse_num_voie']} {person['adresse_voie']}",
        "selarl_adresse_cp": person["adresse_cp"],
        "selarl_adresse_ville": person["adresse_ville"],
        "selarl_denomination": f"SELARL {person['nom']}",
        "selarl_capital_social": capital,
        "selarl_nb_parts_total": parts,
        "selarl_ville_rcs": company["ville"],
        "selarl_siege_voie": f"{company['numero']} {company['voie']}",
        "selarl_siege_cp": company["cp"],
        "selarl_siege_ville": company["ville"],
        "selarl_departement_ordre": company["departement_ordre"],
        "selarl_ordre_adresse_ligne_1": company["ordre_adresse"],
        "selarl_ordre_cp": company["ordre_cp"],
        "selarl_ordre_ville": company["ville"],
        "selarl_signature_lieu": company["ville"],
        "selarl_signature_date": today_text,
        "selarl_decision_date": today_text,
        "selarl_depot_banque_nom": random.choice(("BNP Paribas", "CIC", "Credit Agricole")),
        "selarl_depot_banque_adresse": company["banque_adresse"],
        "selarl_exercice_debut": "1er janvier",
        "selarl_exercice_fin": "31 decembre",
        "selarl_exercice_cloture_premier": f"31 decembre {date.today().year + 1}",
        "selarl_autre_lieu_exercice": False,
        "selarl_lieu_exercice_adresse": "",
        "selarl_second_lieu_exercice_nom": "",
        "selarl_second_lieu_exercice_adresse": "",
        "selarl_conjoint_civilite": "Madame",
        "selarl_conjoint_prenom": random.choice(("Claire", "Sophie", "Nadia")),
        "selarl_conjoint_nom": person["nom"],
    }
    values.update(_cession_prefill_values(profession_key))
    values.update(_scm_cession_prefill_values(person))
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


def _scm_associe_prefill_values(
    index: int,
    *,
    civilite: str,
    prenom: str,
    nom: str,
    ville: str,
    departement: str,
    naissance: str,
    adresse: str,
    apport: str,
    nb: int,
    debut: int,
    fin: int,
) -> dict[str, object]:
    """Cles session_state d'un associe SCM (personne physique) pour le prefill."""
    p = f"scm_associe_{index}"
    # Adresse structuree (§18.5) + nationalite deroulant (cle _choice) + plus de
    # parts debut/fin (derivation cumulative). Profession conservee (SCM, §18.6).
    num, voie, cp, ville_adr = _split_demo_address(adresse)
    return {
        f"{p}_type": "personne_physique",
        f"{p}_civilite": civilite,
        f"{p}_prenom": prenom,
        f"{p}_nom": nom,
        f"{p}_date_naissance": naissance,
        f"{p}_ville_naissance": ville,
        f"{p}_departement_naissance": departement,
        f"{p}_nationalite_choice": "Française",
        f"{p}_situation_maritale": "celibataire",
        f"{p}_profession": "Medecin",
        f"{p}_adresse_num": num,
        f"{p}_adresse_voie": voie,
        f"{p}_adresse_cp": cp,
        f"{p}_adresse_ville": ville_adr,
        f"{p}_apport_montant": apport,
        f"{p}_nb_titres": nb,
    }


def _prefill_scm_test_data() -> None:
    """Pre-remplit un dossier SCM de creation FICTIF et coherent (2 associes medecins).

    Donnees d'exemple uniquement (aucune donnee reelle). Somme des parts = total.
    """
    values: dict[str, object] = {
        "scm_denomination": "SCM DES DOCTEURS EXEMPLE",
        "scm_capital_social": 1000,
        "scm_nb_parts_total": 100,
        "scm_siege_num": "10",
        "scm_siege_voie": "rue de la Paix",
        "scm_siege_cp": "75002",
        "scm_siege_ville": "Paris",
        "scm_ville_rcs": "Paris",
        "scm_banque_nom": "BANQUE EXEMPLE",
        "scm_banque_adresse": "1 rue Banque, 75009 Paris",
        "scm_date_cloture_premier_exercice": "31 decembre 2026",
        "scm_signature_date": "15/05/2026",
        "scm_signataire_fonction": "gerant",
        "scm_signataire_titre": "Docteur",
        "scm_decision_date": "15/05/2026",
        "scm_ordre_conseil": "Conseil departemental de l'Ordre des medecins",
        "scm_ordre_departement": "75",
        "scm_ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "scm_ordre_cp": "75008",
        "scm_ordre_ville": "Paris",
        "scm_ordre_numero": "ORD-12345",
        "scm_nb_associes": 2,
        # Satellites SCM (pacte + liste depenses, generes a 2 associes).
        "scm_pacte_ville_tribunal": "Paris",
        "scm_societe_numero_rcs": "en cours de constitution",
        # Documents inter-SEL (R22-03/04) : contrat de frais communs + reglement interieur.
        # Actifs par defaut ; donnees FICTIVES de la SEL de chaque praticien + parametres.
        "scm_inter_sel_active": True,
        "scm_inter_sel_forme": "SELARL",
        "scm_inter_sel_titre": "Docteur",
        "scm_inter_sel_1_denomination": "SELARL DOCTEUR DURAND",
        "scm_inter_sel_1_capital": "1 000 euros",
        "scm_inter_sel_1_siege": "1 rue Exemple, 75000 Paris",
        "scm_inter_sel_1_ville_rcs": "Paris",
        "scm_inter_sel_1_numero_rcs": "900 000 011",
        "scm_inter_sel_1_telephone": "01 00 00 00 01",
        "scm_inter_sel_2_denomination": "SELARL DOCTEUR MARTIN",
        "scm_inter_sel_2_capital": "1 000 euros",
        "scm_inter_sel_2_siege": "2 rue Exemple, 69000 Lyon",
        "scm_inter_sel_2_ville_rcs": "Lyon",
        "scm_inter_sel_2_numero_rcs": "900 000 012",
        "scm_inter_sel_2_telephone": "04 00 00 00 02",
        "scm_inter_sel_locaux": "10 rue de la Paix, 75002 Paris",
        "scm_inter_sel_date_effet": "1er janvier 2027",
        "scm_inter_sel_seuil": "1 500 euros",
        "scm_inter_sel_annee_ref": "2027",
        "scm_inter_sel_date_fin_gestion": "31 decembre 2027",
        "scm_inter_sel_date_attribution": "1er janvier",
    }
    values.update(
        _scm_associe_prefill_values(
            0,
            civilite="Monsieur",
            prenom="Jean",
            nom="Durand",
            ville="Paris",
            departement="75",
            naissance="1 janvier 1980",
            adresse="1 rue Exemple, 75000 Paris",
            apport="700",
            nb=70,
            debut=1,
            fin=70,
        )
    )
    values.update(
        _scm_associe_prefill_values(
            1,
            civilite="Madame",
            prenom="Alice",
            nom="Martin",
            ville="Lyon",
            departement="69",
            naissance="2 fevrier 1982",
            adresse="2 rue Exemple, 69000 Lyon",
            apport="300",
            nb=30,
            debut=71,
            fin=100,
        )
    )
    values.update(_civil_gerant_dnc_prefill("scm", 0))
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


def _civil_gerant_dnc_prefill(prefix: str, index: int) -> dict[str, object]:
    """Coche l'associe `index` comme gerant + sa DNC (filiation/adresse), saisies
    sous lui (reunion 2026-06-09). Donnees fictives. Le gerant designe alimente
    les cles signataire_* via _collect_gerant_sig."""
    # Adresse du gerant : plus saisie ici (§18.5), reprise de l'adresse personnelle
    # de l'associe. On ne pose que la filiation + la case dirigeant.
    p = f"{prefix}_associe_{index}"
    return {
        f"{p}_is_dirigeant": True,
        f"{p}_sig_nom_pere": "Pierre Durand",
        f"{p}_sig_nom_mere": "Anne Durand",
    }


def _civil_society_prefill(
    prefix: str,
    *,
    denomination: str,
    forme_sociale: str,
) -> dict[str, object]:
    """Cles societe + documents communs (hors identite du gerant) pour un dossier
    civil de test (fictif). La filiation/adresse du gerant est saisie sous lui."""
    # forme_sociale derivee (§18.1), valeur nominale calculee (§18.2), duree figee
    # (§18.3), lieu de signature = ville siege (§18.4) : ces champs ne sont plus des
    # widgets saisis -> plus de cle de prefill pour eux.
    del forme_sociale
    return {
        f"{prefix}_denomination": denomination,
        f"{prefix}_capital_social": 1000,
        f"{prefix}_nb_parts_total": 100,
        f"{prefix}_siege_num": "10",
        f"{prefix}_siege_voie": "rue de la Paix",
        f"{prefix}_siege_cp": "75002",
        f"{prefix}_siege_ville": "Paris",
        f"{prefix}_ville_rcs": "Paris",
        f"{prefix}_banque_nom": "BANQUE EXEMPLE",
        f"{prefix}_banque_adresse": "1 rue Banque, 75009 Paris",
        f"{prefix}_date_cloture_premier_exercice": "31 decembre 2026",
        f"{prefix}_signature_date": "15/05/2026",
        f"{prefix}_signataire_fonction": "gerant",
        f"{prefix}_signataire_titre": "Docteur",
        f"{prefix}_decision_date": "15/05/2026",
    }


def _civil_pp_associe_prefill(
    prefix: str,
    index: int,
    *,
    civilite: str,
    prenom: str,
    nom: str,
    ville: str,
    departement: str,
    naissance: str,
    adresse: str,
    apport: str,
    nb: int,
    debut: int,
    fin: int,
    role: str | None = None,
) -> dict[str, object]:
    p = f"{prefix}_associe_{index}"
    # Adresse personnelle STRUCTUREE (§18.5) : on derive num/voie/cp/ville depuis
    # l'adresse fictive « 1 rue Exemple, 75000 Paris ». parts debut/fin ne sont plus
    # saisis (derivation cumulative). Nationalite = deroulant (cle _choice).
    num, voie, cp, ville_adr = _split_demo_address(adresse)
    values: dict[str, object] = {
        f"{p}_type": "personne_physique",
        f"{p}_civilite": civilite,
        f"{p}_prenom": prenom,
        f"{p}_nom": nom,
        f"{p}_date_naissance": naissance,
        f"{p}_ville_naissance": ville,
        f"{p}_departement_naissance": departement,
        f"{p}_nationalite_choice": "Française",
        f"{p}_situation_maritale": "celibataire",
        f"{p}_profession": "Medecin",
        f"{p}_adresse_num": num,
        f"{p}_adresse_voie": voie,
        f"{p}_adresse_cp": cp,
        f"{p}_adresse_ville": ville_adr,
        f"{p}_apport_montant": apport,
        f"{p}_nb_titres": nb,
    }
    if role is not None:
        values[f"{p}_role"] = role
    return values


def _split_demo_address(adresse: str) -> tuple[str, str, str, str]:
    """Eclate « 1 rue Exemple, 75000 Paris » en (num, voie, cp, ville) pour le prefill.

    Donnees fictives uniquement (bouton « donnees de test »). Best-effort : ce qui
    ne se parse pas tombe en voie/ville pour rester non bloquant.
    """
    rue_part, _, loc_part = adresse.partition(",")
    rue_part = rue_part.strip()
    loc_part = loc_part.strip()
    num, _, voie = rue_part.partition(" ")
    cp, _, ville = loc_part.partition(" ")
    return num.strip(), voie.strip(), cp.strip(), ville.strip()


def _civil_pm_associe_prefill(
    prefix: str,
    index: int,
    *,
    denomination: str,
    forme_juridique: str,
    capital: str,
    siege: str,
    numero_rcs: str,
    ville_rcs: str,
    rep_prenom: str,
    rep_nom: str,
    apport: str,
    nb: int,
    debut: int,
    fin: int,
) -> dict[str, object]:
    # Profession PM : widget SCM uniquement (§18.6) ; parts debut/fin derivees (§18.5).
    p = f"{prefix}_associe_{index}"
    values: dict[str, object] = {
        f"{p}_type": "personne_morale",
        f"{p}_denomination": denomination,
        f"{p}_forme_juridique": forme_juridique,
        f"{p}_capital_social": capital,
        f"{p}_siege": siege,
        f"{p}_numero_rcs": numero_rcs,
        f"{p}_ville_rcs": ville_rcs,
        f"{p}_rep_civilite": "Monsieur",
        f"{p}_rep_prenom": rep_prenom,
        f"{p}_rep_nom": rep_nom,
        f"{p}_rep_fonction": "gerant",
        f"{p}_apport_montant": apport,
        f"{p}_nb_titres": nb,
    }
    if prefix == "scm":
        values[f"{p}_profession"] = "Medecin"
    return values


def _commit_civil_prefill(values: dict[str, object]) -> None:
    st.session_state.update(values)
    st.session_state.pop(GENERATED_DOSSIER_STATE_KEY, None)


def _option_is_prefill(prefix: str) -> dict[str, object]:
    """Active l'option IS + le centre des impots (lettre DOC-022) dans les donnees de test.

    R22-05 (Rafael 2026-06-22) : la lettre d'option IS existe deja pour SCI / SCI IRIS mais
    n'etait pas demontree au bouton de test -> Rafael ne la voyait pas. On l'active ici. Le
    « Centre » n'est plus saisi (R22-07 : fige a « Centre des Finances Publiques »).
    """
    return {
        f"{prefix}_option_is": True,
        f"{prefix}_siren": "900 000 001",
        f"{prefix}_impots_service": "Service des impots des entreprises de Paris 8e",
        f"{prefix}_impots_adresse_ligne_1": "6 rue Paul Baudry",
        f"{prefix}_impots_adresse_ligne_2": "TSA 00001",
        f"{prefix}_impots_cp": "75008",
        f"{prefix}_impots_ville": "Paris",
    }


def _prefill_sci_test_data() -> None:
    """SCI de creation fictive (2 associes physiques) + option IS (lettre DOC-022)."""
    values = _civil_society_prefill(
        "sci", denomination="SCI EXEMPLE", forme_sociale="societe civile immobiliere"
    )
    values["sci_nb_associes"] = 2
    values.update(_option_is_prefill("sci"))
    values.update(
        _civil_pp_associe_prefill(
            "sci", 0, civilite="Monsieur", prenom="Jean", nom="Durand", ville="Paris",
            departement="75", naissance="1 janvier 1980",
            adresse="1 rue Exemple, 75000 Paris", apport="400", nb=40, debut=1, fin=40,
        )
    )
    values.update(
        _civil_pp_associe_prefill(
            "sci", 1, civilite="Madame", prenom="Alice", nom="Martin", ville="Lyon",
            departement="69", naissance="2 fevrier 1982",
            adresse="2 rue Exemple, 69000 Lyon", apport="600", nb=60, debut=41, fin=100,
        )
    )
    values.update(_civil_gerant_dnc_prefill("sci", 0))
    _commit_civil_prefill(values)


def _prefill_sci_iris_test_data() -> None:
    """SCI IRIS de creation fictive (1 societe associee + 1 associe physique)."""
    values = _civil_society_prefill(
        "sci_iris", denomination="SCI IRIS EXEMPLE",
        forme_sociale="societe civile immobiliere",
    )
    values["sci_iris_nb_associes"] = 2
    values.update(_option_is_prefill("sci_iris"))
    values.update(
        _civil_pm_associe_prefill(
            "sci_iris", 0, denomination="SEL EXEMPLE", forme_juridique="SELARL",
            capital="1 000 euros", siege="2 rue Pro, 75000 Paris",
            numero_rcs="900 000 001", ville_rcs="Paris", rep_prenom="Jean", rep_nom="Durand",
            apport="400", nb=40, debut=1, fin=40,
        )
    )
    values.update(
        _civil_pp_associe_prefill(
            "sci_iris", 1, civilite="Madame", prenom="Alice", nom="Martin", ville="Lyon",
            departement="69", naissance="2 fevrier 1982",
            adresse="2 rue Exemple, 69000 Lyon", apport="600", nb=60, debut=41, fin=100,
        )
    )
    # Gerant SCI IRIS = associe physique (index 1 ; l'associe 0 est la personne morale).
    values.update(_civil_gerant_dnc_prefill("sci_iris", 1))
    _commit_civil_prefill(values)


def _prefill_scs_test_data() -> None:
    """SCS de creation fictive (1 commandite + 1 commanditaire)."""
    values = _civil_society_prefill(
        "scs", denomination="SCS EXEMPLE", forme_sociale="societe en commandite simple"
    )
    values["scs_nb_associes"] = 2
    values.update(
        _civil_pp_associe_prefill(
            "scs", 0, civilite="Monsieur", prenom="Jean", nom="Durand", ville="Paris",
            departement="75", naissance="1 janvier 1980",
            adresse="1 rue Exemple, 75000 Paris", apport="600", nb=60, debut=1, fin=60,
            role="commandite",
        )
    )
    values.update(
        _civil_pp_associe_prefill(
            "scs", 1, civilite="Madame", prenom="Alice", nom="Martin", ville="Lyon",
            departement="69", naissance="2 fevrier 1982",
            adresse="2 rue Exemple, 69000 Lyon", apport="400", nb=40, debut=61, fin=100,
            role="commanditaire",
        )
    )
    # Gerant SCS = le commandite (associe 0).
    values.update(_civil_gerant_dnc_prefill("scs", 0))
    _commit_civil_prefill(values)


def _prefill_sas_test_data() -> None:
    """SAS (SPFPL medecins) de creation fictive — actionnaire unique masculin (V1)."""
    values: dict[str, object] = {
        "sas_denomination": "SPFPL MARTIN",
        "sas_siege": "10 rue de la Paix, 75002 Paris",
        "sas_siege_num": "10",
        "sas_siege_voie": "rue de la Paix",
        "sas_siege_cp": "75002",
        "sas_siege_ville": "Paris",
        "sas_capital_social": 12000,
        "sas_nb_actions_total": 120,
        "sas_valeur_nominale_action": "100",
        "sas_apports_nature_montant": "10000",
        "sas_apports_numeraire_montant": "2000",
        "sas_civilite": "Docteur",
        "sas_prenom": "Camille",
        "sas_nom": "Martin",
        "sas_genre_label": "Monsieur",
        "sas_qualification_principale": "Medecin cardiologue",
        "sas_date_naissance": "2 janvier 1980",
        "sas_date_naissance_iso": "02/01/1980",
        "sas_ville_naissance": "Paris",
        "sas_departement_naissance": "75",
        "sas_nationalite_choice": "Française",
        "sas_regime_matrimonial": "la communaute legale",
        "sas_adresse": "5 rue Royale, 75008 Paris",
        "sas_adresse_num": "5",
        "sas_adresse_voie": "rue Royale",
        "sas_adresse_cp": "75008",
        "sas_adresse_ville": "Paris",
        "sas_nom_pere": "Pierre Martin",
        "sas_nom_mere": "Anne Martin",
        "sas_conjoint_civilite": "Madame",
        "sas_conjoint_prenom": "Alice",
        "sas_conjoint_nom": "Martin",
        "sas_ordre_departement": "Paris",
        "sas_numero_ordre": "12345",
        "sas_numero_rpps": "10000000001",
        "sas_cible_denomination": "SELARL CABINET MARTIN",
        "sas_cible_forme": "SELARL",
        "sas_cible_siege": "12 avenue des Ternes, 75017 Paris",
        "sas_cible_ville_rcs": "Paris",
        "sas_cible_numero_rcs": "900 000 001",
        "sas_apport_nb_parts": 50,
        "sas_banque_nom": "BANQUE EXEMPLE",
        "sas_signature_lieu": "Paris",
        "sas_exercice_debut": "1er janvier",
        "sas_exercice_fin": "31 decembre",
        "sas_date_cloture": "31 decembre 2026",
        "sas_signature_date": "14/05/2026",
    }
    _commit_civil_prefill(values)


def _spfpl_prefill_values(prefix: str) -> dict[str, object]:
    """Dossier SPFPL de creation fictif (associe unique medecin), prefixe par parcours."""
    return {
        f"{prefix}_denomination": "SPFPL MARTIN",
        f"{prefix}_siege": "10 rue de la Paix, 75002 Paris",
        f"{prefix}_siege_num": "10",
        f"{prefix}_siege_voie": "rue de la Paix",
        f"{prefix}_siege_cp": "75002",
        f"{prefix}_siege_ville": "Paris",
        f"{prefix}_capital_social": 60000,
        # Nombre d'actions VARIABLE (defaut 600) ; la valeur nominale est calculee
        # (60000 / 600 = 100) et affichee en lecture seule, plus de saisie libre.
        f"{prefix}_nb_actions_total": 600,
        f"{prefix}_ville_rcs": "Paris",
        # §14.2 : la civilite SPFPL est desormais la civilite CIVILE (M./Mme) ; le
        # titre « Docteur » est applique automatiquement (plus de selecteur
        # « Docteur » ni de selecteur « Genre civil » redondant).
        f"{prefix}_civilite": "Monsieur",
        f"{prefix}_prenom": "Camille",
        f"{prefix}_prenoms": "Camille Andre",
        f"{prefix}_nom": "Martin",
        f"{prefix}_date_naissance": "02/01/1980",
        f"{prefix}_ville_naissance": "Paris",
        f"{prefix}_departement_naissance": "75",
        f"{prefix}_nationalite_choice": "Française",
        f"{prefix}_regime_matrimonial": "la communaute legale",
        f"{prefix}_adresse": "5 rue Royale, 75008 Paris",
        f"{prefix}_adresse_num": "5",
        f"{prefix}_adresse_voie": "rue Royale",
        f"{prefix}_adresse_cp": "75008",
        f"{prefix}_adresse_ville": "Paris",
        f"{prefix}_nom_pere": "Pierre Martin",
        f"{prefix}_nom_mere": "Anne Martin",
        f"{prefix}_conjoint_civilite": "Madame",
        f"{prefix}_conjoint_prenom": "Alice",
        f"{prefix}_conjoint_nom": "Martin",
        f"{prefix}_ordre_departement": "Paris",
        f"{prefix}_numero_ordre": "12345",
        f"{prefix}_numero_rpps": "10000000001",
        f"{prefix}_ordre_conseil": "Conseil departemental",
        f"{prefix}_ordre_adresse_ligne_1": "1 rue de l'Ordre",
        f"{prefix}_ordre_cp": "75008",
        f"{prefix}_ordre_ville": "Paris",
        f"{prefix}_banque_nom": "BANQUE EXEMPLE",
        f"{prefix}_banque_adresse": "1 boulevard Haussmann, 75009 Paris",
        f"{prefix}_apport_montant": "60000",
        f"{prefix}_apport_nb_parts": 60,
        f"{prefix}_apport_plage": "41 a 100",
        f"{prefix}_apport_valeur_globale": "60000",
        f"{prefix}_cible_denomination": "SELARL CABINET MARTIN",
        f"{prefix}_cible_siege": "12 avenue des Ternes, 75017 Paris",
        f"{prefix}_cible_ville_rcs": "Paris",
        f"{prefix}_cible_numero_rcs": "900 000 001",
        # Operation cession (DOC-037 note + DOC-038/039 PV + DOC-040 acte) :
        # repartition de la cible + prix + siege structure. 1 associe cible -> PV unique.
        f"{prefix}_cession_nb_parts_cedees": 60,
        f"{prefix}_cession_prix_unitaire": "1000",
        f"{prefix}_cession_plage_cedee": "41 a 100",
        f"{prefix}_cible_forme_complete": "societe d'exercice liberal a responsabilite limitee",
        f"{prefix}_cible_siege_num": "12",
        f"{prefix}_cible_siege_voie": "avenue des Ternes",
        f"{prefix}_cible_siege_cp": "75017",
        f"{prefix}_cible_siege_ville": "Paris",
        f"{prefix}_cession_nb_associes": 1,
        f"{prefix}_cession_assoc_0_civ": "Docteur",
        f"{prefix}_cession_assoc_0_prenom": "Camille",
        f"{prefix}_cession_assoc_0_nom": "Martin",
        f"{prefix}_cession_assoc_0_avant": 100,
        f"{prefix}_cession_assoc_0_apres": 40,
        f"{prefix}_cession_assoc_0_plage": "1 a 40",
        f"{prefix}_cible_forme": "SELARL",
        f"{prefix}_cible_profession": "chirurgien-dentiste",
        f"{prefix}_cible_capital": "10000",
        f"{prefix}_cible_nb_parts": 100,
        f"{prefix}_cible_valeur_part": "100",
        # Operation apport (DOC-041 contrat + DOC-042/043 attestations) : detail
        # des titres apportes + organes de controle (commissaire + evaluateur).
        f"{prefix}_apport_nature_titres": "parts sociales",
        f"{prefix}_apport_valeur_par_titre": "1000",
        f"{prefix}_commissaire_denomination": "CAA EXPERTISE",
        f"{prefix}_commissaire_forme": "SAS",
        f"{prefix}_commissaire_capital": "1 000 euros",
        f"{prefix}_commissaire_siege": "1 rue Scheffer, 75016 Paris",
        f"{prefix}_commissaire_ville_rcs": "Paris",
        f"{prefix}_commissaire_numero_rcs": "948 483 730",
        f"{prefix}_commissaire_rep_civilite": "Monsieur",
        f"{prefix}_commissaire_rep_prenom": "Nabil",
        f"{prefix}_commissaire_rep_nom": "Saidi",
        f"{prefix}_evaluateur_denomination": "EVAL CONSEIL",
        f"{prefix}_evaluateur_forme": "SAS",
        f"{prefix}_evaluateur_capital": "1 000 euros",
        f"{prefix}_evaluateur_siege": "1 rue Scheffer, 75016 Paris",
        f"{prefix}_evaluateur_ville_rcs": "Paris",
        f"{prefix}_evaluateur_numero_rcs": "948 483 730",
        f"{prefix}_evaluateur_rep_civilite": "Madame",
        f"{prefix}_evaluateur_rep_prenom": "Eva",
        f"{prefix}_evaluateur_rep_nom": "Lemoine",
        f"{prefix}_exercice_debut": "1er janvier",
        f"{prefix}_exercice_fin": "31 decembre",
        f"{prefix}_date_cloture": "31 decembre 2026",
        f"{prefix}_signature_lieu": "Paris",
        f"{prefix}_signature_date": "14/05/2026",
        f"{prefix}_decision_date": "14/05/2026",
    }


def _prefill_spfpl_cession_test_data() -> None:
    _commit_civil_prefill(_spfpl_prefill_values("spfpl_cession"))


def _prefill_spfpl_apport_test_data() -> None:
    _commit_civil_prefill(_spfpl_prefill_values("spfpl_apport"))


def _selas_associe_prefill(
    index: int,
    *,
    civilite: str,
    prenoms: str,
    nom: str,
    ville: str,
    departement: str,
    nationalite_ordre: str,
    numero_ordre: str,
    numero_rpps: str,
    qualite: str,
    nb_actions: int,
    apport: str,
) -> dict[str, object]:
    p = f"selas_associe_{index}"
    return {
        f"{p}_type": "personne_physique",
        f"{p}_nb_actions": nb_actions,
        f"{p}_montant": apport,
        f"{p}_civilite": civilite,
        f"{p}_prenoms": prenoms,
        f"{p}_nom": nom,
        f"{p}_date_naissance": "1 janvier 1980",
        f"{p}_ville_naissance": ville,
        f"{p}_departement": departement,
        f"{p}_nationalite": "francaise",
        f"{p}_profession": "Docteur",
        f"{p}_adresse_num": "10",
        f"{p}_adresse_voie": "rue Exemple",
        f"{p}_adresse_cp": f"{departement}000",
        f"{p}_adresse_ville": ville,
        f"{p}_situation": "celibataire",
        f"{p}_qualification": "Medecin generaliste",
        f"{p}_ordre_dep": nationalite_ordre,
        f"{p}_numero_ordre": numero_ordre,
        f"{p}_numero_rpps": numero_rpps,
        f"{p}_qualite": qualite,
    }


def _prefill_selas_test_data(
    profession: str = "médecin", profession_pluriel: str = "médecins"
) -> None:
    """SELAS multi de creation fictive (2 associes exercants, somme = total).

    La profession est parametrable : « médecin » par defaut (SELAS multi), ou
    « chirurgien-dentiste » pour le cas nomme SELAS dentiste pluripersonnelle —
    de sorte que les donnees de test basculent le moteur sur le bon corpus.
    R1 (2026-06-18) : la profession est desormais un menu deroulant ferme cote
    formulaire (cle `selas_profession_choice`) ; on seed cette cle pour rester
    coherent (la valeur DOIT etre une option exacte du menu)."""
    values: dict[str, object] = {
        "selas_denomination": "SELAS EXEMPLE",
        "selas_siege": "5 place du Centre, 69000 Lyon",
        "selas_siege_num": "5",
        "selas_siege_voie": "place du Centre",
        "selas_siege_cp": "69000",
        "selas_siege_ville": "Lyon",
        "selas_profession_choice": profession,
        # Capital = number_input cote SELAS (parite gold) -> seed un ENTIER, pas une
        # chaine (sinon le widget number_input leve).
        "selas_capital_social": 1000,
        "selas_nb_actions_total": 100,
        "selas_valeur_nominale_action": "10",
        "selas_ville_rcs": "Lyon",
        "selas_adresse_lieu_exercice": "5 place du Centre, 69000 Lyon",
        "selas_banque_nom": "BANQUE EXEMPLE",
        "selas_banque_adresse": "1 rue Banque, 69009 Lyon",
        "selas_date_cloture": "31 decembre 2026",
        "selas_signature_lieu": "Lyon",
        "selas_signature_date": "15/05/2026",
        # DNC + identite du dirigeant : saisies SOUS l'associe coche dirigeant
        # (associe 0). La nationalite / le titre derivent de l'associe lui-meme.
        # DNC + identite du dirigeant : adresse et date sont reprises de l'associe
        # (saisies une seule fois, #8 / B4) ; seule la filiation reste propre ici.
        "selas_associe_0_is_dirigeant": True,
        "selas_associe_0_sig_nom_pere": "Pierre Durand",
        "selas_associe_0_sig_nom_mere": "Anne Durand",
        "selas_decision_date": "15/05/2026",
        # R5/R6 (2026-06-18) : « Conseil departemental » retire du formulaire ;
        # le connecteur grammatical (« de » / « du ») le remplace pour l'accord.
        "selas_ordre_departement": "Rhone",
        "selas_ordre_connecteur": "du",
        "selas_ordre_adresse_ligne_1": "1 rue de l'Ordre",
        "selas_ordre_cp": "69002",
        "selas_ordre_ville": "Lyon",
        "selas_ordre_numero": "69-12345",
        "selas_nb_associes": 2,
    }
    values.update(
        _selas_associe_prefill(
            0, civilite="Monsieur", prenoms="Jean", nom="Durand", ville="Lyon",
            departement="69", nationalite_ordre="Rhone", numero_ordre="69-12345",
            numero_rpps="10100000001", qualite="associe exercant", nb_actions=60, apport="600",
        )
    )
    values.update(
        _selas_associe_prefill(
            1, civilite="Madame", prenoms="Alice", nom="Martin", ville="Paris",
            departement="75", nationalite_ordre="Paris", numero_ordre="75-67890",
            numero_rpps="10100000002", qualite="associee exercante", nb_actions=40, apport="400",
        )
    )
    _commit_civil_prefill(values)


# Boutons "donnees de test" par type (calques sur le bouton SELARL). Etendu type
# par type au fur et a mesure de la validation.
_TYPED_TEST_DATA_PREFILL = {
    "SCM": _prefill_scm_test_data,
    "SCI": _prefill_sci_test_data,
    "SCI IRIS": _prefill_sci_iris_test_data,
    "SCS": _prefill_scs_test_data,
    "SAS": _prefill_sas_test_data,
    "SPFPL cession": _prefill_spfpl_cession_test_data,
    "SPFPL apport": _prefill_spfpl_apport_test_data,
    "SELAS": _prefill_selas_test_data,
}

# Prefill surchargeant le defaut par structure pour une cle de type precise.
# La SELAS dentiste pluripersonnelle reutilise le prefill SELAS avec la
# profession chirurgien-dentiste -> donnees de test coherentes avec le corpus
# dentiste (sinon le prefill par structure remplirait « medecin »).
_TYPED_TEST_DATA_PREFILL_BY_KEY = {
    "selas_dentiste_pluri_v1": lambda: _prefill_selas_test_data(
        "chirurgien-dentiste", "chirurgiens-dentistes"
    ),
}


def _cession_prefill_values(profession: str) -> dict[str, object]:
    """Cles du sous-formulaire cession (donnees de test FICTIVES, nouvelles cles).

    Le vendeur et l'acquereur sont repris automatiquement du dossier : seuls les
    champs specifiques a la cession sont preremplis ici. Un clic = cession
    testable et generable.
    """
    dentaire = profession == PROFESSION_DENTISTE
    year = date.today().year
    values: dict[str, object] = {
        "selarl_cession_meta_type_cabinet": "dentaire" if dentaire else "medical",
        "selarl_cession_meta_etape": "acte",
        "selarl_cession_vendeur_auto": True,
        "selarl_cession_vendeur_siren": "123 456 789",
        "selarl_cession_acquereur_numero_rcs": "900 000 001",
        "selarl_cession_acquereur_numero_siret": "900 000 001 00012",
        # Adresse cabinet : laissee vide -> reprise du siege social au rendu.
        "selarl_cession_cabinet_adresse": "",
        "selarl_cession_cabinet_telephone": "01 44 00 00 00",
        "selarl_cession_cabinet_origine_date": "01/01/2020",
        "selarl_cession_bail_date_bail": "01/09/2021",
        "selarl_cession_bail_date_effet": "01/09/2021",
        "selarl_cession_bail_duree": "six années",
        "selarl_cession_bail_loyer": "2 000",
        "selarl_cession_bail_descriptif": (
            "Les locaux sont composés d'une pièce principale de 80 m² avec "
            "jouissance de la salle d'attente et des toilettes."
        ),
        "selarl_cession_prix_total": "300 000",
        "selarl_cession_prix_total_lettres": "",
        "selarl_cession_prix_corporels": "50 000",
        "selarl_cession_prix_incorporels": "250 000",
        # §12.1 : champ « Banque » retire du questionnaire d'appel de fonds (nom
        # inconnu au remplissage) -> plus de seed de test pour cette cle.
        "selarl_cession_financement_destinataire_civilite": "Monsieur",
        "selarl_cession_financement_destinataire_prenom": "Louis",
        "selarl_cession_financement_destinataire_nom": "Bernard",
        "selarl_cession_financement_deblocage": "240 000",
        "selarl_cession_bailleur_civilite": "Monsieur",
        "selarl_cession_bailleur_prenom": "Paul",
        "selarl_cession_bailleur_nom": "Leroy",
        "selarl_cession_bailleur_adresse": "8 rue Victor Hugo, 69002 Lyon",
    }
    for index in range(3):
        values[f"selarl_cession_exercice_{index}_periode"] = str(year - 3 + index)
        values[f"selarl_cession_exercice_{index}_ca"] = f"2{index}0 000"
        values[f"selarl_cession_exercice_{index}_resultat"] = f"8{index} 000"
    if dentaire:
        values.update(
            {
                "selarl_cession_cabinet_precedent_civilite": "Docteur",
                "selarl_cession_cabinet_precedent_prenom": "Henri",
                "selarl_cession_cabinet_precedent_nom": "Petit",
                "selarl_cession_cabinet_origine_prix": "150 000",
                "selarl_cession_salaries_aucun": False,
                "selarl_cession_salaries_nb": 2,
                "selarl_cession_salarie_0_civilite": "Madame",
                "selarl_cession_salarie_0_prenom": "Lea",
                "selarl_cession_salarie_0_nom": "Petit",
                "selarl_cession_salarie_0_poste": "assistante dentaire",
                "selarl_cession_salarie_1_civilite": "Monsieur",
                "selarl_cession_salarie_1_prenom": "Noe",
                "selarl_cession_salarie_1_nom": "Robert",
                "selarl_cession_salarie_1_poste": "",
            }
        )
    else:
        values.update(
            {
                "selarl_cession_cabinet_origine_mode": "Cabinet cree par le vendeur",
                "selarl_cession_financement_credit_actif": True,
                "selarl_cession_financement_credit_montant": "60 000",
                "selarl_cession_financement_credit_duree": "trois",
                "selarl_cession_financement_credit_taux": "5",
                "selarl_cession_financement_credit_majoration": "2",
                "selarl_cession_scm_clause_actif": True,
                "selarl_cession_financement_scm_parts": "10",
                "selarl_cession_acquereur_date_immatriculation": "15/01/2026",
                "selarl_cession_acquereur_date_inscription_ordre": "01/02/2026",
            }
        )
    return values


def _scm_cession_prefill_values(person: dict[str, str]) -> dict[str, object]:
    """Cles `selarl_cession_scm_*` : fixture SCM + cedant = la personne de test.

    §4.1 : prefill aussi le repeater des associes PRESENTS (3 par defaut, total
    cohérent avec le capital de la SCM) dont le cedant = la personne de test, plus
    le nombre de parts cedees. L'apres-cession est derive deterministe a la
    generation (cedant reduit + SEL acquereur entrante)."""
    payload = scm_cession_fixture().model_dump(by_alias=True)
    scm_cedee = payload.get("scm_cedee") or {}
    parts_cedees = payload.get("parts_cedees") or {}
    prix = payload.get("prix") or {}
    # SCM de demo : 300 parts (100 + 100 + 100) ; cession de 50 parts.
    nb_total = int(scm_cedee.get("nb_parts_total") or 300)
    nb_cedees = int(parts_cedees.get("nb") or 50)
    # Trois presents : le cedant (la personne de test) + deux co-associes de demo,
    # chacun 1/3 du capital, pour un total egal a nb_total.
    part = nb_total // 3
    reste = nb_total - 2 * part  # absorbe l'eventuel reste de division sur le 3e
    presents = [
        {
            "morale": False,
            "civilite": person["civilite"],
            "prenom": person["prenom"],
            "nom": person["nom"],
            "nb_parts": str(part),
            "plage": f"1 a {part}",
        },
        {
            "morale": False,
            "civilite": "Monsieur",
            "prenom": "Paul",
            "nom": "Bernard",
            "nb_parts": str(part),
            "plage": f"{part + 1} a {2 * part}",
        },
        {
            "morale": False,
            "civilite": "Madame",
            "prenom": "Anne",
            "nom": "Martin",
            "nb_parts": str(reste),
            "plage": f"{2 * part + 1} a {nb_total}",
        },
    ]
    values: dict[str, object] = {
        "selarl_cession_scm_cedee_denomination": scm_cedee.get("denomination") or "",
        "selarl_cession_scm_cedee_rcs_ville": scm_cedee.get("ville_rcs") or "",
        "selarl_cession_scm_cedee_numero_rcs": scm_cedee.get("numero_rcs") or "",
        "selarl_cession_scm_cedee_capital_social": scm_cedee.get("capital_social") or "",
        "selarl_cession_scm_cedee_nb_parts_total": str(nb_total),
        "selarl_cession_scm_cedee_valeur_nominale_part": (
            scm_cedee.get("valeur_nominale_part") or ""
        ),
        "selarl_cession_scm_cedee_plage_parts_total": (
            scm_cedee.get("plage_parts_total") or ""
        ),
        # Cedant = l'associe unique (ticket 2.13).
        "selarl_cession_scm_cedant_civilite": person["civilite"],
        "selarl_cession_scm_cedant_prenom": person["prenom"],
        "selarl_cession_scm_cedant_nom": person["nom"],
        # Parts cedees : le cedant cede les `nb_cedees` dernieres de sa tranche.
        "selarl_cession_scm_parts_nb": str(nb_cedees),
        "selarl_cession_scm_parts_plage": f"{part - nb_cedees + 1} a {part}",
        "selarl_cession_scm_prix_global": prix.get("global") or "",
        "selarl_cession_scm_prix_global_lettres": prix.get("global_lettres") or "",
        # Repeater des presents.
        "selarl_cession_scm_presents_count": len(presents),
    }
    for index, present in enumerate(presents):
        values[f"selarl_cession_scm_present_{index}_morale"] = present["morale"]
        values[f"selarl_cession_scm_present_{index}_civilite"] = present["civilite"]
        values[f"selarl_cession_scm_present_{index}_prenom"] = present["prenom"]
        values[f"selarl_cession_scm_present_{index}_nom"] = present["nom"]
        values[f"selarl_cession_scm_present_{index}_nb_parts"] = present["nb_parts"]
        values[f"selarl_cession_scm_present_{index}_plage"] = present["plage"]
    return values


def _test_people() -> tuple[dict[str, str], ...]:
    return (
        {
            "civilite": "Monsieur",
            "prenom": "Jean",
            "nom": "Martin",
            "date_naissance": "12/04/1984",
            "ville_naissance": "Paris",
            "departement_naissance": "75",
            "nom_pere": "Pierre Martin",
            "nom_mere": "Anne Martin",
            "adresse_num_voie": "10",
            "adresse_voie": "rue des Tilleuls",
            "adresse_cp": "75011",
            "adresse_ville": "Paris",
        },
        {
            "civilite": "Madame",
            "prenom": "Camille",
            "nom": "Bernard",
            "date_naissance": "21/09/1978",
            "ville_naissance": "Lyon",
            "departement_naissance": "69",
            "nom_pere": "Laurent Bernard",
            "nom_mere": "Marie Bernard",
            "adresse_num_voie": "8",
            "adresse_voie": "avenue Victor Hugo",
            "adresse_cp": "69002",
            "adresse_ville": "Lyon",
        },
        {
            "civilite": "Monsieur",
            "prenom": "Thomas",
            "nom": "Durand",
            "date_naissance": "03/02/1981",
            "ville_naissance": "Nantes",
            "departement_naissance": "44",
            "nom_pere": "Alain Durand",
            "nom_mere": "Helene Durand",
            "adresse_num_voie": "14",
            "adresse_voie": "boulevard Saint-Felix",
            "adresse_cp": "44000",
            "adresse_ville": "Nantes",
        },
    )


def _test_companies() -> tuple[dict[str, str], ...]:
    return (
        {
            "numero": "20",
            "voie": "avenue du Siege",
            "cp": "75002",
            "ville": "Paris",
            "departement_ordre": "75, Paris",
            "ordre_adresse": "1 rue de l'Ordre",
            "ordre_cp": "75008",
            "banque_adresse": "30 boulevard Haussmann, 75009 Paris",
        },
        {
            "numero": "5",
            "voie": "place Bellecour",
            "cp": "69002",
            "ville": "Lyon",
            "departement_ordre": "69, Rhone",
            "ordre_adresse": "12 quai Jules Courmont",
            "ordre_cp": "69002",
            "banque_adresse": "7 cours de la Liberte, 69003 Lyon",
        },
        {
            "numero": "3",
            "voie": "rue Crebillon",
            "cp": "44000",
            "ville": "Nantes",
            "departement_ordre": "44, Loire-Atlantique",
            "ordre_adresse": "9 allee Baco",
            "ordre_cp": "44000",
            "banque_adresse": "2 rue de Strasbourg, 44000 Nantes",
        },
    )


def _ordre_label(profession_label: str, ville: str) -> str:
    profession = (
        "chirurgiens-dentistes" if profession_label == "Chirurgien-dentiste" else "médecins"
    )
    return f"Conseil departemental de l'Ordre des {profession} de {ville}"


def _render_data_entry_zone(dossier_type: DossierTypeOption) -> CleanDataEntry:
    st.subheader("Donnees a saisir")
    qualification = _render_qualification()
    praticien = _render_praticien(profession=str(qualification["profession"]))
    societe = _render_societe(praticien=praticien)
    membres = _render_selarl_membres(
        unipersonnel=bool(qualification["dossier_unipersonnel"]),
        nb_parts_total=societe.get("nb_parts_total"),
    )
    ordre_mandataire = _render_ordre_mandataire()
    generation_context = _render_generation_context(societe)
    cession_context, bail_context = _render_cession_form(
        bool(qualification["cession"]),
        str(qualification["profession"]),
        praticien=praticien,
        societe=societe,
        ordre=ordre_mandataire,
        generation=generation_context,
    )
    scm_cession_context = _render_scm_cession_form(
        bool(qualification["scm"]),
        praticien=praticien,
        societe=societe,
        profession_label=str(qualification["profession"]),
        ordre=ordre_mandataire,
    )
    return build_clean_data_entry(
        dossier_type,
        **qualification,
        **praticien,
        **societe,
        **membres,
        **ordre_mandataire,
        **generation_context,
        cession_context=cession_context,
        bail_context=bail_context,
        scm_cession_context=scm_cession_context,
    )


def _render_selarl_membres(
    *,
    unipersonnel: bool,
    nb_parts_total: object,
) -> dict[str, object]:
    """Saisie multi-associes SELARL (retours V3 2026-06-17) — ADDITIF.

    N'apparait QUE si « Dossier unipersonnel » est decoche. Collecte la part du
    praticien (membre #1, signataire) + N membres additionnels (personne physique
    OU morale). Le nombre d'associes = praticien + membres (tous signataires). En
    unipersonnel -> dict vide, parcours historique inchange.
    """
    if unipersonnel:
        return {}

    st.markdown("**Associes (multi)**")
    st.caption(
        "Le praticien est le 1er associe (signataire). Ajoutez les autres associes "
        "(personne physique ou morale). La somme des parts doit egaler le nombre "
        "total de parts du capital."
    )
    col_a, col_b = st.columns(2)
    praticien_nb_parts = int(
        col_a.number_input(
            "Parts du praticien",
            min_value=0,
            step=1,
            key="selarl_praticien_nb_parts",
        )
    )
    praticien_apport = col_b.text_input(
        "Apport du praticien (euros)",
        key="selarl_praticien_apport",
    )

    count_key = "selarl_membres_count"
    if count_key not in st.session_state:
        st.session_state[count_key] = 1
    nombre = max(1, min(5, int(st.session_state[count_key])))
    add_col, remove_col = st.columns(2)
    if add_col.button("Ajouter un associe", key="selarl_membres_add"):
        st.session_state[count_key] = min(5, nombre + 1)
        st.rerun()
    if remove_col.button("Retirer un associe", key="selarl_membres_remove"):
        st.session_state[count_key] = max(1, nombre - 1)
        st.rerun()

    membres: list[StatutsCivilsAssocie] = []
    for index in range(nombre):
        membre = _render_one_selarl_membre(index)
        if membre is not None:
            membres.append(membre)

    return {
        "praticien_nb_parts": praticien_nb_parts,
        "praticien_apport": praticien_apport,
        "membres_additionnels": tuple(membres),
    }


def _render_one_selarl_membre(index: int) -> StatutsCivilsAssocie | None:
    prefix = f"selarl_membre_{index}"
    with st.expander(f"Associe additionnel {index + 2}", expanded=index == 0):
        type_personne = st.selectbox(
            "Type d'associe",
            ("personne_physique", "personne_morale"),
            key=f"{prefix}_type",
        )
        col_p, col_a = st.columns(2)
        nb_parts = int(
            col_p.number_input(
                "Nombre de parts",
                min_value=0,
                step=1,
                key=f"{prefix}_nb_parts",
            )
        )
        apport = col_a.text_input("Apport (euros)", key=f"{prefix}_apport")
        parts = StatutsCivilsParts(nb=nb_parts, nb_lettres=number_words_from_value(nb_parts))
        apport_obj = StatutsCivilsApport(
            montant=apport, montant_lettres=number_words_from_value(apport)
        )
        if type_personne == "personne_morale":
            denomination = st.text_input("Denomination", key=f"{prefix}_denomination")
            col_b, col_c = st.columns(2)
            forme = col_b.text_input("Forme juridique", key=f"{prefix}_forme")
            capital = col_c.text_input("Capital social (euros)", key=f"{prefix}_capital")
            siege = st.text_input("Siege (adresse affichee)", key=f"{prefix}_siege")
            col_d, col_e = st.columns(2)
            numero_rcs = col_d.text_input("Numero RCS", key=f"{prefix}_rcs")
            ville_rcs = col_e.text_input("Ville RCS", key=f"{prefix}_ville_rcs")
            st.caption("Representant legal")
            col_f, col_g, col_h = st.columns(3)
            rep_civilite = col_f.selectbox(
                "Civilite rep.", ("Monsieur", "Madame"), key=f"{prefix}_rep_civilite"
            )
            rep_prenom = col_g.text_input("Prenom rep.", key=f"{prefix}_rep_prenom")
            rep_nom = col_h.text_input("Nom rep.", key=f"{prefix}_rep_nom")
            if not denomination.strip():
                return None
            return StatutsCivilsAssocie(
                type_personne="personne_morale",
                denomination=denomination,
                forme_juridique=forme or None,
                capital_social=capital or None,
                siege=Address(adresse_affichee=siege) if siege.strip() else None,
                numero_rcs=numero_rcs or None,
                ville_rcs=ville_rcs or None,
                representant=StatutsCivilsRepresentant(
                    civilite_affichage=rep_civilite,
                    prenom=rep_prenom or None,
                    nom=rep_nom or None,
                ),
                apport=apport_obj,
                parts=parts,
            )
        col_b, col_c, col_d = st.columns(3)
        civilite = col_b.selectbox(
            "Civilite", ("Monsieur", "Madame"), key=f"{prefix}_civilite"
        )
        prenom = col_c.text_input("Prenom", key=f"{prefix}_prenom")
        nom = col_d.text_input("Nom", key=f"{prefix}_nom")
        col_e, col_f, col_g = st.columns(3)
        date_naissance = col_e.text_input("Date de naissance", key=f"{prefix}_date_naissance")
        ville_naissance = col_f.text_input("Ville de naissance", key=f"{prefix}_ville_naissance")
        dep_naissance = col_g.text_input("Departement naissance", key=f"{prefix}_dep_naissance")
        col_h, col_i = st.columns(2)
        nationalite = col_h.text_input("Nationalite", key=f"{prefix}_nationalite")
        situation = col_i.text_input("Situation matrimoniale", key=f"{prefix}_situation")
        profession = st.text_input("Profession", key=f"{prefix}_profession")
        adresse = st.text_input("Adresse personnelle (affichee)", key=f"{prefix}_adresse")
        col_j, col_k, col_l = st.columns(3)
        ordre_dep = col_j.text_input("Departement ordre", key=f"{prefix}_ordre_dep")
        numero_ordre = col_k.text_input("Numero ordre", key=f"{prefix}_numero_ordre")
        numero_rpps = col_l.text_input("Numero RPPS", key=f"{prefix}_numero_rpps")
        if not (prenom.strip() and nom.strip()):
            return None
        return StatutsCivilsAssocie(
            type_personne="personne_physique",
            genre=derive_gender_from_civilite(civilite),
            civilite_affichage=civilite,
            prenom=prenom,
            nom=nom,
            profession=profession or None,
            date_naissance=date_naissance or None,
            ville_naissance=ville_naissance or None,
            departement_naissance=dep_naissance or None,
            nationalite=nationalite or None,
            situation_maritale=situation or None,
            adresse_personnelle_affichee=adresse or None,
            ordre_departemental=ordre_dep or None,
            numero_ordre=numero_ordre or None,
            numero_rpps=numero_rpps or None,
            apport=apport_obj,
            parts=parts,
        )


def _render_qualification() -> dict[str, object]:
    st.markdown("**Qualification**")
    profession_label = st.selectbox(
        "Profession",
        ("Medecin", "Chirurgien-dentiste"),
        key="selarl_profession",
    )
    col_a, col_b = st.columns(2)
    dossier_unipersonnel = col_a.checkbox(
        "Dossier unipersonnel",
        value=True,
        key="selarl_dossier_unipersonnel",
    )
    # Les documents du regime de la communaute (DOC-005/DOC-006) sont derives de
    # la situation matrimoniale choisie dans la fiche praticien (retours client
    # 2026-06-11, ticket 1.2) : plus de case a cocher dediee.
    col_b.caption(
        "Documents du regime de la communaute : actives automatiquement quand le "
        "praticien est marie sous le regime legal / communaute."
    )

    st.markdown("**Operations complementaires**")
    out_a, out_b = st.columns(2)
    cession = out_a.checkbox("Cession de fonds liberal", value=False, key="selarl_cession")
    scm = out_b.checkbox("SCM", value=False, key="selarl_scm")

    return {
        "dossier_reference": st.text_input(
            "Reference dossier",
            key="selarl_dossier_reference",
        ),
        "profession": (
            PROFESSION_DENTISTE if profession_label == "Chirurgien-dentiste" else PROFESSION_MEDECIN
        ),
        "dossier_unipersonnel": dossier_unipersonnel,
        "cession": cession,
        "scm": scm,
    }


def _render_praticien(*, profession: str) -> dict[str, object]:
    st.markdown("**Fiche Client / Praticien**")
    civilite = st.selectbox("Civilite", ("Monsieur", "Madame"), key="selarl_civilite")
    col_d, col_e = st.columns(2)
    prenom = col_d.text_input("Prenom", key="selarl_prenom")
    nom = col_e.text_input("Nom", key="selarl_nom")
    col_f, col_g, col_h = st.columns(3)
    with col_f:
        date_naissance = _date_input_with_today(
            "Date de naissance",
            key="selarl_date_naissance",
            value=date(1990, 1, 1),
        )
    ville_naissance = col_g.text_input("Ville de naissance", key="selarl_ville_naissance")
    ville_naissance_article_au = col_g.checkbox(
        "au",
        key="selarl_ville_naissance_article_au",
        help="Affiche 'ne au ...' au lieu de 'ne a ...' dans la DNC.",
    )
    departement_naissance = col_h.text_input(
        "Departement naissance",
        key="selarl_departement_naissance",
    )
    col_i, col_j = st.columns(2)
    nationalite_choice = col_i.selectbox(
        "Nationalite",
        NATIONALITY_PRESETS,
        key="selarl_nationalite_choice",
    )
    nationalite = (
        col_i.text_input("Nationalite autre", key="selarl_nationalite_other")
        if nationalite_choice == "Autre"
        else nationalite_choice.lower()
    )
    situation_maritale_label = col_j.selectbox(
        "Situation matrimoniale",
        MATRIMONIAL_STATUS_PRESETS,
        key="selarl_situation_maritale",
    )
    # Le regime legal / communaute est le seul a declencher DOC-005/DOC-006
    # (retours client 2026-06-11, ticket 1.2). Les autres regimes maries sont
    # proposes mais sans logique documentaire particuliere.
    regime_communautaire = regime_communautaire_from_status(situation_maritale_label)
    if regime_communautaire:
        col_j.caption("Regime de la communaute : DOC-005 et DOC-006 seront generes.")

    # Epoux / partenaire : a cote de la situation matrimoniale (ticket 1.3).
    situation_value = matrimonial_status_value(situation_maritale_label)
    is_married_or_pacse = situation_value in ("marie", "pacse")
    conjoint: dict[str, object] = {
        "conjoint_civilite": "",
        "conjoint_genre": derive_gender_from_civilite("Madame"),
        "conjoint_prenom": "",
        "conjoint_nom": "",
    }
    if profession == PROFESSION_DENTISTE or is_married_or_pacse:
        conj_a, conj_b, conj_c = st.columns(3)
        conjoint_civilite = conj_a.selectbox(
            "Civilite epoux / partenaire",
            ("Madame", "Monsieur"),
            key="selarl_conjoint_civilite",
        )
        conjoint = {
            "conjoint_civilite": conjoint_civilite,
            "conjoint_genre": derive_gender_from_civilite(conjoint_civilite),
            "conjoint_prenom": conj_b.text_input(
                "Prenom de l'epoux / partenaire",
                key="selarl_conjoint_prenom",
            ),
            "conjoint_nom": conj_c.text_input(
                "Nom de l'epoux / partenaire",
                key="selarl_conjoint_nom",
            ),
        }

    # Numero d'Ordre et RPPS sur une meme ligne (ticket 1.4).
    col_k, col_m = st.columns(2)
    numero_ordre = col_k.text_input("Numero d'Ordre", key="selarl_numero_ordre")
    numero_rpps = col_m.text_input("Numero RPPS", key="selarl_numero_rpps")
    # Parents sur la ligne suivante, avec les libelles demandes (ticket 1.4).
    col_n, col_o = st.columns(2)
    nom_pere = col_n.text_input("Nom et prenom du pere", key="selarl_nom_pere")
    nom_mere = col_o.text_input(
        "Nom de jeune fille et prenom de la mere",
        key="selarl_nom_mere",
    )

    st.markdown("Adresse personnelle")
    # Numero et voie fusionnes en un seul champ (ticket 1.5) : la valeur vit
    # dans adresse_voie, adresse_num_voie reste vide.
    adr_a, adr_b, adr_c = st.columns((2, 1, 1))
    return {
        "civilite": civilite,
        "genre": derive_gender_from_civilite(civilite),
        "prenom": prenom,
        "nom": nom,
        "date_naissance": date_naissance,
        "ville_naissance": ville_naissance,
        "ville_naissance_article_au": ville_naissance_article_au,
        "departement_naissance": departement_naissance,
        "nationalite": nationalite,
        "nom_pere": nom_pere,
        "nom_mere": nom_mere,
        "situation_maritale": situation_value,
        "regime_communautaire": regime_communautaire,
        "regime_matrimonial": regime_matrimonial_from_status(
            situation_maritale_label,
            regime_communautaire,
        ),
        "numero_ordre": numero_ordre,
        "numero_rpps": numero_rpps,
        **conjoint,
        "adresse_num_voie": "",
        "adresse_voie": adr_a.text_input("Numero et voie", key="selarl_adresse_voie"),
        "adresse_cp": adr_b.text_input("CP", key="selarl_adresse_cp"),
        "adresse_ville": adr_c.text_input("Ville", key="selarl_adresse_ville"),
    }


def _render_societe(
    *,
    praticien: dict[str, object],
) -> dict[str, object]:
    st.markdown("**Fiche Societe**")
    col_a, col_b = st.columns(2)
    denomination = col_a.text_input("Denomination sociale", key="selarl_denomination")
    capital_social = col_b.number_input(
        "Capital social (€)",
        min_value=0,
        step=100,
        value=0,
        key="selarl_capital_social",
        help="Montant numerique uniquement (ex : 330 000).",
    )
    nb_parts_total = st.number_input(
        "Nombre total de parts",
        min_value=0,
        step=1,
        value=0,
        key="selarl_nb_parts_total",
    )
    valeur_nominale_part = calculate_nominal_value(capital_social, nb_parts_total)
    if valeur_nominale_part:
        st.caption(f"Valeur nominale calculee : {valeur_nominale_part} EUR")
    else:
        st.caption("Valeur nominale calculee automatiquement apres capital et parts.")
    ville_rcs = st.text_input("RCS (ville)", key="selarl_ville_rcs")

    st.markdown("Siege social")
    siege_same_as_personal = st.checkbox(
        "identique a l'adresse personnelle",
        value=False,
        key="selarl_siege_same_as_personal",
    )
    if siege_same_as_personal:
        societe = {
            "denomination": denomination,
            "capital_social": format_numeric_value(capital_social),
            "duree": "99 ans",
            "nb_parts_total": int(nb_parts_total),
            "valeur_nominale_part": valeur_nominale_part,
            "ville_rcs": ville_rcs,
            "siege_num_voie": str(praticien.get("adresse_num_voie") or ""),
            "siege_voie": str(praticien.get("adresse_voie") or ""),
            "siege_cp": str(praticien.get("adresse_cp") or ""),
            "siege_ville": str(praticien.get("adresse_ville") or ""),
        }
    else:
        # Numero et voie fusionnes en un seul champ (ticket 1.5).
        adr_a, adr_b, adr_c = st.columns((2, 1, 1))
        societe = {
            "denomination": denomination,
            "capital_social": format_numeric_value(capital_social),
            "duree": "99 ans",
            "nb_parts_total": int(nb_parts_total),
            "valeur_nominale_part": valeur_nominale_part,
            "ville_rcs": ville_rcs,
            "siege_num_voie": "",
            "siege_voie": adr_a.text_input("Numero et voie", key="selarl_siege_voie"),
            "siege_cp": adr_b.text_input("Code postal", key="selarl_siege_cp"),
            "siege_ville": adr_c.text_input("Ville", key="selarl_siege_ville"),
        }

    # « Autre lieu d'exercice » juste apres l'adresse du siege (ticket 1.8 + 2.2).
    # Le siege reste TOUJOURS le lieu d'exercice #1. La case ajoute un VRAI 2e lieu
    # (nom + adresse), JAMAIS un remplacement du siege : les champs ne sont plus
    # pre-remplis avec le siege (sinon doublon). L'article 5 des statuts ne rend
    # le 2e lieu que si nom ET adresse sont fournis ensemble (contrat SELAS).
    autre_lieu_exercice = st.checkbox(
        "Autre lieu d'exercice ?",
        value=False,
        key="selarl_autre_lieu_exercice",
        help=(
            "Le siege reste le lieu d'exercice principal. Cochez pour ajouter un "
            "2e lieu d'exercice (en plus du siege)."
        ),
    )
    second_lieu_nom = ""
    second_lieu_adresse = ""
    if autre_lieu_exercice:
        second_lieu_nom = st.text_input(
            "Nom du 2e lieu d'exercice",
            key="selarl_second_lieu_exercice_nom",
        )
        second_lieu_adresse = st.text_input(
            "Adresse du 2e lieu d'exercice",
            key="selarl_second_lieu_exercice_adresse",
        )
    # Champ legacy conserve pour retro-compat (jamais pre-rempli ici) : le 1er lieu
    # est desormais toujours derive du siege cote contexte.
    societe["lieu_exercice_adresse"] = ""
    societe["second_lieu_exercice_nom"] = second_lieu_nom
    societe["second_lieu_exercice_adresse"] = second_lieu_adresse
    return societe


def _render_ordre_mandataire() -> dict[str, object]:
    st.markdown("**Ordre professionnel**")
    col_a, _ = st.columns(2)
    departement_ordre = col_a.text_input(
        "Departement d'inscription a l'ordre",
        key="selarl_departement_ordre",
        help="Exemple : Paris, Loire-Atlantique ou le departement ordinal attendu par le dossier.",
    )
    col_c, col_d, col_e = st.columns(3)
    ordre_adresse_ligne_1 = col_c.text_input(
        "Adresse ordre",
        key="selarl_ordre_adresse_ligne_1",
    )
    ordre_cp = col_d.text_input("CP ordre", key="selarl_ordre_cp")
    ordre_ville = col_e.text_input("Ville ordre", key="selarl_ordre_ville")
    # Retour Albane 2026-06-10 : president(e) de l'ordre = femme -> « Madame la
    # Presidente » dans la demande d'inscription (verifie a chaque fois).
    ordre_president_feminin = st.checkbox(
        "La présidente de l'ordre est une femme",
        value=False,
        key="selarl_ordre_president_feminin",
        help="Coche : « Madame la Présidente » au lieu de « Monsieur le Président ».",
    )
    # Retour Albane 2026-06-10 : nom du conseiller (mandataire SYDEL) adaptable,
    # au lieu de « Jordan ELBAZ » en dur.
    if not st.session_state.get("selarl_mandataire_prenom"):
        st.session_state["selarl_mandataire_prenom"] = DEFAULT_MANDATAIRE_PRENOM
    if not st.session_state.get("selarl_mandataire_nom"):
        st.session_state["selarl_mandataire_nom"] = DEFAULT_MANDATAIRE_NOM
    col_f, col_g = st.columns(2)
    mandataire_prenom = col_f.text_input(
        "Conseiller (prénom)",
        key="selarl_mandataire_prenom",
    )
    mandataire_nom = col_g.text_input(
        "Conseiller (nom)",
        key="selarl_mandataire_nom",
    )
    return {
        "departement_ordre": departement_ordre,
        "ordre_adresse_ligne_1": ordre_adresse_ligne_1,
        "ordre_cp": ordre_cp,
        "ordre_ville": ordre_ville,
        "ordre_president_feminin": ordre_president_feminin,
        "mandataire_prenom": mandataire_prenom or DEFAULT_MANDATAIRE_PRENOM,
        "mandataire_nom": mandataire_nom or DEFAULT_MANDATAIRE_NOM,
    }


def _render_generation_context(societe: dict[str, object]) -> dict[str, object]:
    st.markdown("**Generation**")
    # Lieu de signature preremplie avec la ville du siege social, modifiable
    # (retours client 2026-06-11, ticket 1.6).
    siege_ville = str(societe.get("siege_ville") or "").strip()
    if not st.session_state.get("selarl_signature_lieu") and siege_ville:
        st.session_state["selarl_signature_lieu"] = siege_ville
    # Dates d'exercice preremplies, cloture du premier exercice au 31 decembre
    # de l'annee N+1, dynamique selon l'annee du dossier (ticket 1.7).
    if not st.session_state.get("selarl_exercice_debut"):
        st.session_state["selarl_exercice_debut"] = "1er janvier"
    if not st.session_state.get("selarl_exercice_fin"):
        st.session_state["selarl_exercice_fin"] = "31 decembre"
    if not st.session_state.get("selarl_exercice_cloture_premier"):
        st.session_state["selarl_exercice_cloture_premier"] = (
            f"31 decembre {date.today().year + 1}"
        )
    col_a, col_b = st.columns(2)
    signature_lieu = col_a.text_input("Lieu de signature", key="selarl_signature_lieu")
    with col_b:
        signature_date = _date_input_with_today(
            "Date de signature",
            key="selarl_signature_date",
            value=date.today(),
        )
    decision_date = _date_input_with_today(
        "Date de decision",
        key="selarl_decision_date",
        value=date.today(),
    )
    col_g, col_h = st.columns(2)
    depot_banque_nom = col_g.text_input("Banque depot", key="selarl_depot_banque_nom")
    depot_banque_adresse = col_h.text_input(
        "Adresse banque (facultatif)",
        key="selarl_depot_banque_adresse",
        help="Vide : les statuts laissent une zone a completer a la main.",
    )
    col_j, col_k, col_l = st.columns(3)
    exercice_debut = col_j.text_input("Debut exercice", key="selarl_exercice_debut")
    exercice_fin = col_k.text_input("Fin exercice", key="selarl_exercice_fin")
    exercice_cloture_premier = col_l.text_input(
        "Cloture premier exercice",
        key="selarl_exercice_cloture_premier",
    )
    return {
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "signature_nombre_exemplaires": "quatre",
        "decision_date": decision_date,
        "depot_banque_nom": depot_banque_nom,
        "depot_banque_adresse": depot_banque_adresse,
        "exercice_debut": exercice_debut,
        "exercice_fin": exercice_fin,
        "exercice_cloture_premier": exercice_cloture_premier,
    }


def _date_input_with_today(label: str, *, key: str, value: date) -> date | None:
    # Implementation extraite dans la couche de rendu partagee (front_widgets) pour
    # que TOUS les types l'heritent au lieu de la dupliquer (cause racine des ecarts
    # de parite — voir docs/review/METHODE_PARITE_GOLD.md). Le SELARL (3 appels)
    # reste byte-identique : meme fonction, nom local conserve.
    from sydel_doc_engine.front_app.front_widgets import date_input_with_today

    return date_input_with_today(label, key=key, value=value)


def _siege_display(societe: dict[str, object]) -> str:
    return (
        f"{societe.get('siege_num_voie', '')} "
        f"{societe.get('siege_voie', '')}, "
        f"{societe.get('siege_cp', '')} "
        f"{societe.get('siege_ville', '')}"
    ).strip(" ,")


CESSION_TYPE_LABELS: dict[str, str] = {"medical": "medical", "dentaire": "dentaire"}
CESSION_ETAPE_LABELS: dict[str, str] = {"acte": "acte", "compromis": "compromis"}

# Petits nombres d'annees en toutes lettres pour deriver la fin de bail depuis
# « six années » (duree par defaut conservee, ticket 2.6).
_YEARS_WORDS: dict[str, int] = {
    "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
    "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10, "onze": 11, "douze": 12,
}


def _cession_default_type(profession: str) -> str:
    return "dentaire" if profession == PROFESSION_DENTISTE else "medical"


def _profession_label(profession: str) -> str:
    return "chirurgien-dentiste" if profession == PROFESSION_DENTISTE else "médecin"


def _personal_address_display(praticien: dict[str, object]) -> str:
    parts_voie = " ".join(
        str(praticien.get(key) or "").strip()
        for key in ("adresse_num_voie", "adresse_voie")
    ).strip()
    suffix = " ".join(
        str(praticien.get(key) or "").strip() for key in ("adresse_cp", "adresse_ville")
    ).strip()
    return ", ".join(part for part in (parts_voie, suffix) if part)


def _scm_profession_pair(profession_label: str) -> tuple[str, str]:
    """(singulier, pluriel) de la profession reglementee pour la cession SCM."""
    if "dentiste" in str(profession_label).casefold():
        return "chirurgien-dentiste", "chirurgiens-dentistes"
    return "médecin", "médecins"


def _scm_cedant_overrides(
    praticien: dict[str, object],
    *,
    profession_label: str,
    departement_ordre: str,
) -> dict[str, object]:
    """Etat civil du cedant (= associe unique) derive de la fiche praticien.

    Retour Albane lot 2 §13.2 : le sous-formulaire de cession SCM partait d'une
    fixture de demo, si bien que nationalite / adresse / naissance / situation du
    cedant restaient des valeurs fictives (cedant suisse affiche francais...). On
    derive ces champs de la saisie reelle. UNIQUEMENT les valeurs non vides sont
    renvoyees : un champ absent laisse la valeur de base inchangee (les champs
    requis du generateur ne sont jamais vides par ce biais). La cle ``ordre`` est
    un dict PARTIEL a fusionner sur l'ordre de base par l'appelant (sinon une
    cle manquante ecraserait l'autre)."""
    singulier, pluriel = _scm_profession_pair(profession_label)
    candidates: dict[str, object] = {
        "nationalite": str(praticien.get("nationalite") or ""),
        "adresse_affichee": _personal_address_display(praticien),
        "date_naissance": praticien.get("date_naissance"),
        "ville_naissance": str(praticien.get("ville_naissance") or ""),
        "departement_naissance": str(praticien.get("departement_naissance") or ""),
        "situation_maritale": str(praticien.get("situation_maritale") or ""),
        "numero_rpps": str(praticien.get("numero_rpps") or ""),
        "profession": singulier,
        "profession_reglementee_pluriel": pluriel,
    }
    overrides: dict[str, object] = {key: value for key, value in candidates.items() if value}
    ordre = {
        key: value
        for key, value in (
            ("numero", str(praticien.get("numero_ordre") or "")),
            ("departemental", str(departement_ordre or "")),
        )
        if value
    }
    if ordre:
        overrides["ordre"] = ordre
    conjoint = {
        key: value
        for key, value in (
            ("civilite_affichage", str(praticien.get("conjoint_civilite") or "")),
            ("prenom", str(praticien.get("conjoint_prenom") or "")),
            ("nom", str(praticien.get("conjoint_nom") or "")),
        )
        if value
    }
    if conjoint:
        overrides["conjoint"] = conjoint
    return overrides


def _scm_cessionnaire_overrides(societe: dict[str, object]) -> dict[str, object]:
    """Description de la SEL cessionnaire (= societe creee) derivee de la fiche societe.

    Retour Albane lot 2 §13.3 : le capital / siege / denomination du cessionnaire
    restaient ceux de la fixture (capital 10 000 affiche alors que 1 000 saisi).
    Valeurs non vides uniquement (preserve le representant deja calcule)."""
    overrides: dict[str, object] = {}
    denomination = str(societe.get("denomination") or "")
    capital = str(societe.get("capital_social") or "")
    ville_rcs = str(societe.get("ville_rcs") or "")
    siege = _siege_display(societe)
    if denomination:
        overrides["denomination"] = denomination
    if capital:
        overrides["capital_social"] = capital
    if ville_rcs:
        overrides["ville_rcs"] = ville_rcs
    if siege:
        overrides["siege"] = {"adresse_affichee": siege}
    return overrides


def _situation_display(value: str, genre: object) -> str:
    feminine = genre == Gender.FEMININ
    return {
        "marie": "mariée" if feminine else "marié",
        "pacse": "pacsée" if feminine else "pacsé",
        "divorce": "divorcée" if feminine else "divorcé",
        "veuf": "veuve" if feminine else "veuf",
        "celibataire": "célibataire",
    }.get(value, value)


def _vendeur_regime_label(situation_label: str) -> str:
    """Libelle du regime matrimonial injecte dans les actes de cession.

    Style des modeles : « sous le régime de <libelle> » sans article (releve de
    la fixture validee « communauté réduite aux acquêts »).
    """
    normalized = situation_label.casefold()
    if not normalized.startswith("mari"):
        return ""
    if "universelle" in normalized:
        return "communauté universelle"
    if "participation" in normalized:
        return "participation aux acquêts"
    if "separation" in normalized or "séparation" in normalized:
        return "séparation de biens"
    return "communauté réduite aux acquêts"


def _format_montant(value: str) -> str:
    """Formate un montant saisi en groupes lisibles (« 200 000 », ticket 2.9).

    Valeur non numerique ou vide : renvoyee telle quelle (aucun blocage).
    """
    cleaned = (value or "").strip()
    if not cleaned:
        return ""
    formatted = format_grouped_numeric_value(cleaned)
    return formatted or cleaned


def _euro_amount_letters(value: str) -> str:
    """Montant en toutes lettres derive du montant saisi (ticket 2.10).

    Montants non entiers ou vides : chaine vide (saisie manuelle possible).
    """
    words = number_words_from_value(value)
    if not words:
        return ""
    return f"{words} {euro_word(value)}"


def _years_from_text(text: str) -> int:
    cleaned = (text or "").strip().casefold()
    digits = re.search(r"\d+", cleaned)
    if digits:
        return int(digits.group())
    for word, years in _YEARS_WORDS.items():
        if re.search(rf"\b{word}\b", cleaned):
            return years
    return 0


def _add_years(value: date, years: int) -> date:
    try:
        return value.replace(year=value.year + years)
    except ValueError:
        # 29 fevrier -> 28 fevrier de l'annee cible.
        return value.replace(year=value.year + years, day=28)


def _seed_default(key: str, default: object) -> None:
    if key not in st.session_state:
        st.session_state[key] = default


# Prefixe des cles de session du sous-formulaire cession, parametrable pour
# reutiliser le sous-formulaire SELARL valide sur d'autres types (SELAS...).
# Defaut « selarl » => SELARL byte-identique ; « selas » => clefs propres SELAS.
# Pose par _render_cession_form / _render_scm_cession_form au debut de chaque
# rendu (Streamlit = mono-thread par session, sans course).
_CESSION_PREFIX = "selarl"


def _cession_text(
    container: object,
    label: str,
    *,
    section: str,
    field: str,
    default: str,
) -> str:
    key = f"{_CESSION_PREFIX}_cession_{section}_{field}"
    _seed_default(key, default)
    value = container.text_input(label, key=key)
    return str(value).strip()


def _render_cession_form(
    cession: bool,
    profession: str,
    *,
    praticien: dict[str, object],
    societe: dict[str, object],
    ordre: dict[str, object],
    generation: dict[str, object],
    prefix: str = "selarl",
) -> tuple[CessionContext | None, BailContext | None]:
    """Sous-formulaire CESSION DE FONDS LIBERAL, pilote par les donnees du dossier.

    Refonte retours client 2026-06-11 : le payload est construit a partir des
    donnees REELLES du dossier (vendeur = associe unique, acquereur = fiche
    societe) plus les champs specifiques a la cession. Plus aucune donnee de
    fixture de test n'entre dans les documents generes. Les champs facultatifs
    vides laissent une zone a completer a la main et ne bloquent jamais.
    """
    if not cession:
        return None, None

    global _CESSION_PREFIX
    _CESSION_PREFIX = prefix

    st.markdown("**Cession de fonds liberal**")

    with st.expander("Type & etape", expanded=True):
        col_a, col_b = st.columns(2)
        type_key = f"{_CESSION_PREFIX}_cession_meta_type_cabinet"
        _seed_default(type_key, _cession_default_type(profession))
        type_cabinet = col_a.selectbox(
            "Type de cabinet",
            tuple(CESSION_TYPE_LABELS),
            key=type_key,
        )
        etape_key = f"{_CESSION_PREFIX}_cession_meta_etape"
        _seed_default(etape_key, "acte")
        etape = col_b.selectbox(
            "Etape",
            tuple(CESSION_ETAPE_LABELS),
            key=etape_key,
        )

    profession_label = _profession_label(profession)
    siege_display = _siege_display(societe)
    praticien_prenom = str(praticien.get("prenom") or "").strip()
    praticien_nom = str(praticien.get("nom") or "").strip()
    praticien_genre = praticien.get("genre")
    praticien_adresse = _personal_address_display(praticien)
    situation_label = str(st.session_state.get(f"{_CESSION_PREFIX}_situation_maritale") or "")
    conjoint_payload = {
        "civilite_affichage": str(praticien.get("conjoint_civilite") or ""),
        "prenom": str(praticien.get("conjoint_prenom") or ""),
        "nom": str(praticien.get("conjoint_nom") or ""),
    }

    # --- Vendeur (ticket 2.1 : associe unique par defaut, modifiable) ---
    with st.expander("Vendeur"):
        # #11 (onglet 24) : en SELAS le vendeur est l'associe choisi au menu ci-dessus
        # (plus « l'associe unique », faux en multi-associes). Hors SELAS : inchange.
        vendeur_auto = st.checkbox(
            "Le vendeur est l'associé sélectionné ci-dessus"
            if prefix == "selas"
            else "Le vendeur est l'associe unique",
            value=True,
            key=f"{_CESSION_PREFIX}_cession_vendeur_auto",
            help="Decocher uniquement si un autre vendeur doit etre renseigne.",
        )
        siren = _cession_text(
            st, "Numero SIREN du vendeur (facultatif)",
            section="vendeur", field="siren", default="",
        )
        if vendeur_auto:
            identite = " ".join(
                part
                for part in (DEFAULT_TITRE_AFFICHAGE, praticien_prenom, praticien_nom)
                if part
            )
            st.caption(f"Repris de la fiche praticien : {identite or 'a completer plus haut'}.")
            vendeur_payload: dict[str, object] = {
                "civilite_affichage": DEFAULT_TITRE_AFFICHAGE,
                "genre": praticien_genre,
                "prenom": praticien_prenom,
                "nom": praticien_nom,
                "profession": profession_label,
                "date_naissance": praticien.get("date_naissance"),
                "ville_naissance": str(praticien.get("ville_naissance") or ""),
                "departement_naissance": str(praticien.get("departement_naissance") or ""),
                "nationalite": str(praticien.get("nationalite") or ""),
                "numero_ordre": str(praticien.get("numero_ordre") or ""),
                "numero_rpps": str(praticien.get("numero_rpps") or ""),
                "adresse_affichee": praticien_adresse,
                "situation_maritale": _situation_display(
                    str(praticien.get("situation_maritale") or ""), praticien_genre
                ),
                "regime_matrimonial": _vendeur_regime_label(situation_label),
                "conjoint": conjoint_payload,
            }
        else:
            col_a, col_b, col_c = st.columns(3)
            civilite = _cession_text(
                col_a, "Civilite", section="vendeur", field="civilite",
                default=DEFAULT_TITRE_AFFICHAGE,
            )
            prenom = _cession_text(col_b, "Prenom", section="vendeur", field="prenom", default="")
            nom = _cession_text(col_c, "Nom", section="vendeur", field="nom", default="")
            col_d, col_e, col_f = st.columns(3)
            date_naissance = _cession_text(
                col_d, "Date de naissance (JJ/MM/AAAA)",
                section="vendeur", field="date_naissance", default="",
            )
            ville_naissance = _cession_text(
                col_e, "Ville de naissance", section="vendeur", field="ville_naissance",
                default="",
            )
            departement_naissance = _cession_text(
                col_f, "Departement de naissance",
                section="vendeur", field="departement_naissance", default="",
            )
            col_g, col_h = st.columns(2)
            nationalite = _cession_text(
                col_g, "Nationalite", section="vendeur", field="nationalite",
                default="française",
            )
            situation_vendeur = _cession_text(
                col_h, "Situation matrimoniale (telle qu'affichee dans l'acte)",
                section="vendeur", field="situation", default="célibataire",
            )
            adresse = _cession_text(
                st, "Adresse personnelle", section="vendeur", field="adresse", default="",
            )
            col_i, col_j = st.columns(2)
            numero_ordre = _cession_text(
                col_i, "Numero d'Ordre", section="vendeur", field="numero_ordre", default="",
            )
            numero_rpps = _cession_text(
                col_j, "Numero RPPS", section="vendeur", field="numero_rpps", default="",
            )
            col_k, col_m, col_n = st.columns(3)
            conjoint_civilite = _cession_text(
                col_k, "Civilite conjoint (si marie)",
                section="vendeur", field="conjoint_civilite", default="",
            )
            conjoint_prenom = _cession_text(
                col_m, "Prenom conjoint", section="vendeur", field="conjoint_prenom",
                default="",
            )
            conjoint_nom = _cession_text(
                col_n, "Nom conjoint", section="vendeur", field="conjoint_nom", default="",
            )
            vendeur_payload = {
                "civilite_affichage": civilite,
                "genre": None,
                "prenom": prenom,
                "nom": nom,
                "profession": profession_label,
                "date_naissance": date_naissance,
                "ville_naissance": ville_naissance,
                "departement_naissance": departement_naissance,
                "nationalite": nationalite,
                "numero_ordre": numero_ordre,
                "numero_rpps": numero_rpps,
                "adresse_affichee": adresse,
                "situation_maritale": situation_vendeur,
                "regime_matrimonial": _vendeur_regime_label(situation_vendeur),
                "conjoint": {
                    "civilite_affichage": conjoint_civilite,
                    "prenom": conjoint_prenom,
                    "nom": conjoint_nom,
                },
            }
        vendeur_payload.update(
            {
                "cp_naissance": "",
                "pays_naissance": "France",
                "numero_siren": siren,
                "ordre_departemental": str(ordre.get("departement_ordre") or ""),
            }
        )

    # --- Acquereur (ticket 2.2 : repris automatiquement de la fiche societe) ---
    denomination = str(societe.get("denomination") or "")
    ville_rcs = str(societe.get("ville_rcs") or "")
    numero_rcs = ""
    numero_siret = ""
    date_immatriculation = ""
    date_inscription_ordre = ""
    # #15 (onglet 24) : en SELAS, l'acquereur EST la societe en cours de creation ->
    # aucun champ a saisir (denomination / siege / RCS deja derives de la fiche
    # societe ; RCS/SIRET/dates n'existent pas encore). Le bloc de SAISIE n'est rendu
    # qu'en dehors de la SELAS (parite gold SELARL preservee).
    if prefix != "selas":
        with st.expander("Acquereur (societe en cours de creation)"):
            st.caption(
                "Repris de la fiche societe : "
                f"{denomination or 'denomination a completer'} — "
                f"{siege_display or 'siege a completer'} — RCS {ville_rcs or 'a completer'}."
            )
            col_a, col_b = st.columns(2)
            numero_rcs = _cession_text(
                col_a, "Numero RCS (des immatriculation, facultatif)",
                section="acquereur", field="numero_rcs", default="",
            )
            numero_siret = _cession_text(
                col_b, "Numero SIRET (facultatif)",
                section="acquereur", field="numero_siret", default="",
            )
            if type_cabinet == "medical" and etape == "acte":
                col_c, col_d = st.columns(2)
                date_immatriculation = _cession_text(
                    col_c, "Date d'immatriculation (JJ/MM/AAAA, facultatif)",
                    section="acquereur", field="date_immatriculation", default="",
                )
                date_inscription_ordre = _cession_text(
                    col_d, "Date d'inscription a l'ordre (JJ/MM/AAAA, facultatif)",
                    section="acquereur", field="date_inscription_ordre", default="",
                )
    acquereur_payload = {
        "denomination_societe": denomination,
        "forme_sociale": "SELARL",
        "capital_social": format_grouped_numeric_value(societe.get("capital_social")),
        "siege": {"adresse_affichee": siege_display},
        "rcs_ville": ville_rcs,
        "numero_rcs": numero_rcs,
        "numero_siret": numero_siret,
        "date_immatriculation": date_immatriculation,
        "date_inscription_ordre": date_inscription_ordre,
        "representant": {
            "civilite_affichage": DEFAULT_TITRE_AFFICHAGE,
            "genre": praticien_genre,
            "prenom": praticien_prenom,
            "nom": praticien_nom,
            "fonction": "gérante" if praticien_genre == Gender.FEMININ else "gérant",
        },
    }

    # --- Cabinet (ticket 2.3 : cadre reduit aux seules infos specifiques) ---
    with st.expander("Cabinet"):
        st.caption(f"Nature du fonds liberal : {profession_label} (derivee de la profession).")
        if not st.session_state.get(f"{_CESSION_PREFIX}_cession_cabinet_adresse") and siege_display:
            st.session_state[f"{_CESSION_PREFIX}_cession_cabinet_adresse"] = siege_display
        adresse_cabinet = _cession_text(
            st, "Adresse du cabinet", section="cabinet", field="adresse",
            default=siege_display,
        )
        telephone_cabinet = _cession_text(
            st, "Telephone du cabinet (facultatif)", section="cabinet", field="telephone",
            default="",
        )
        st.markdown("Origine de propriete du vendeur")
        if type_cabinet == "medical":
            mode_key = f"{_CESSION_PREFIX}_cession_cabinet_origine_mode"
            _seed_default(mode_key, "Cabinet cree par le vendeur")
            mode_label = st.selectbox(
                "Le vendeur a...",
                ("Cabinet cree par le vendeur", "Cabinet achete par le vendeur"),
                key=mode_key,
            )
            origine_mode = "achete" if "achete" in mode_label else "cree"
        else:
            # La clause du modele dentaire decrit une acquisition : les champs
            # ci-dessous alimentent ses tokens (vides -> zones a completer).
            origine_mode = "achete"
        date_origine = _cession_text(
            st, "Date d'origine de propriete (JJ/MM/AAAA, facultatif)",
            section="cabinet", field="origine_date", default="",
        )
        precedent_payload: dict[str, str] | None = None
        prix_origine = ""
        if origine_mode == "achete":
            col_a, col_b, col_c = st.columns(3)
            precedent_payload = {
                "civilite_affichage": _cession_text(
                    col_a, "Civilite du precedent proprietaire",
                    section="cabinet", field="precedent_civilite", default="",
                ),
                "prenom": _cession_text(
                    col_b, "Prenom du precedent proprietaire",
                    section="cabinet", field="precedent_prenom", default="",
                ),
                "nom": _cession_text(
                    col_c, "Nom du precedent proprietaire",
                    section="cabinet", field="precedent_nom", default="",
                ),
            }
            prix_origine = _format_montant(
                _cession_text(
                    st, "Prix d'origine de propriete (facultatif)",
                    section="cabinet", field="origine_prix", default="",
                )
            )
        cabinet_payload = {
            "nature_fonds_liberal": profession_label,
            "denomination_ou_adresse_affichee": adresse_cabinet or siege_display,
            "adresse_affichee": adresse_cabinet or siege_display,
            "adresse_locaux_affichee": adresse_cabinet or siege_display,
            "telephone": telephone_cabinet,
            "superficie_local": "",
            "origine_propriete_mode": origine_mode,
            "date_origine_propriete": date_origine,
            "annees_acquisition_patientele": "",
            "prix_origine_propriete": prix_origine,
            "precedent_proprietaire": precedent_payload,
        }
        vendeur_payload["adresse_exercice_affichee"] = adresse_cabinet or siege_display

    # --- Bail professionnel (tickets 2.4 / 2.5 / 2.6) ---
    with st.expander("Bail professionnel"):
        col_a, col_b = st.columns(2)
        date_bail = _cession_text(
            col_a, "Date du bail (JJ/MM/AAAA, facultatif)",
            section="bail", field="date_bail", default="",
        )
        date_effet = _cession_text(
            col_b, "Date d'effet du bail (JJ/MM/AAAA, facultatif)",
            section="bail", field="date_effet", default="",
        )
        col_c, col_d = st.columns(2)
        duree_bail = _cession_text(
            col_c, "Duree du bail", section="bail", field="duree", default="six années",
        )
        loyer = _format_montant(
            _cession_text(
                col_d, "Loyer mensuel (facultatif)", section="bail", field="loyer",
                default="",
            )
        )
        descriptif_key = f"{_CESSION_PREFIX}_cession_bail_descriptif"
        _seed_default(descriptif_key, "")
        descriptif_local = str(
            st.text_area(
                "Descriptif libre du local (facultatif)",
                key=descriptif_key,
                help=(
                    "Rempli : le texte est insere tel quel dans l'acte a la place de la "
                    "phrase type. Vide : aucune phrase n'est inseree et la generation "
                    "n'est pas bloquee."
                ),
            )
        ).strip()
        date_effet_parsed = parse_french_date(date_effet)
        duree_annees = _years_from_text(duree_bail)
        date_fin = (
            _add_years(date_effet_parsed, duree_annees)
            if date_effet_parsed and duree_annees
            else ""
        )
        date_reconduction_2 = (
            _add_years(date_fin, duree_annees) if date_fin and duree_annees else ""
        )
        bail_payload = {
            "date_bail": date_bail,
            "duree": duree_bail,
            "date_debut": date_effet,
            "date_fin": date_fin,
            "date_reconduction_1": date_fin,
            "date_reconduction_2": date_reconduction_2,
            "loyer_mensuel": loyer,
            "activite_autorisee_affichee": (
                "activité dentaire et paramédicale"
                if type_cabinet == "dentaire"
                else "activité médicale et paramédicale"
            ),
            "descriptif_local": descriptif_local,
        }

    # --- Exercices (tickets 2.7 / 2.8) ---
    exercices_payload: list[dict[str, str]] = []
    with st.expander("Exercices (3 derniers)"):
        current_year = date.today().year
        year_options = [str(year) for year in range(current_year, current_year - 11, -1)]
        for index in range(3):
            col_a, col_b, col_c = st.columns(3)
            periode_key = f"{_CESSION_PREFIX}_cession_exercice_{index}_periode"
            _seed_default(periode_key, str(current_year - 3 + index))
            if str(st.session_state.get(periode_key)) not in year_options:
                st.session_state[periode_key] = str(current_year - 3 + index)
            periode = col_a.selectbox(f"Annee {index + 1}", year_options, key=periode_key)
            # #13 (onglet 24) : en SELAS, le CA et le resultat des exercices ne sont
            # plus facultatifs (la validation SELAS les exige) -> on retire la mention.
            opt = "" if prefix == "selas" else " (facultatif)"
            ca = _cession_text(
                col_b, f"CA {index + 1}{opt}",
                section="exercice", field=f"{index}_ca", default="",
            )
            resultat = _cession_text(
                col_c, f"Resultat {index + 1}{opt}",
                section="exercice", field=f"{index}_resultat", default="",
            )
            exercices_payload.append(
                {
                    "periode": str(periode),
                    "chiffre_affaires": _format_montant(ca),
                    "resultat": _format_montant(resultat),
                }
            )

    # --- Prix (tickets 2.9 / 2.10) ---
    with st.expander("Prix"):
        col_a, col_b = st.columns(2)
        prix_total = _format_montant(
            _cession_text(col_a, "Prix total", section="prix", field="total", default="")
        )
        lettres_auto = _euro_amount_letters(prix_total)
        prix_total_lettres = _cession_text(
            col_b, "Prix total en lettres (vide = automatique)",
            section="prix", field="total_lettres", default="",
        ) or lettres_auto
        if lettres_auto:
            col_b.caption(f"Automatique : {lettres_auto}")
        col_c, col_d = st.columns(2)
        prix_corporels = _format_montant(
            _cession_text(
                col_c, "Elements corporels (facultatif)",
                section="prix", field="corporels", default="",
            )
        )
        prix_incorporels = _format_montant(
            _cession_text(
                col_d, "Elements incorporels (facultatif)",
                section="prix", field="incorporels", default="",
            )
        )
        prix_payload = {
            "total": prix_total,
            "total_lettres": prix_total_lettres,
            "elements_corporels": prix_corporels,
            "elements_corporels_lettres": _euro_amount_letters(prix_corporels),
            "elements_incorporels": prix_incorporels,
            "elements_incorporels_lettres": _euro_amount_letters(prix_incorporels),
        }

    # --- Financement (ticket 2.11) ---
    with st.expander("Financement"):
        # §12.1 (retours Albane lot 2) : le nom de la banque n'est PAS connu au
        # moment du remplissage (l'appel de fonds part avant le choix definitif de
        # la banque). On retire donc la SAISIE « Banque » du questionnaire. La
        # mention banque reste possible dans le courrier genere, a completer
        # manuellement ; cote moteur, banque vide => aucune ligne banque parasite.
        st.caption(
            "Le nom de la banque n'est plus demande ici (inconnu au remplissage) ; "
            "il se complete a la main sur l'appel de fonds genere si besoin."
        )
        col_a, col_b, col_c = st.columns(3)
        destinataire_civilite = _cession_text(
            col_a, "Civilite destinataire (facultatif)",
            section="financement", field="destinataire_civilite", default="",
        )
        destinataire_prenom = _cession_text(
            col_b, "Prenom destinataire", section="financement",
            field="destinataire_prenom", default="",
        )
        destinataire_nom = _cession_text(
            col_c, "Nom destinataire", section="financement",
            field="destinataire_nom", default="",
        )
        montant_deblocage = _format_montant(
            _cession_text(
                st, "Montant deblocage minimum (facultatif)",
                section="financement", field="deblocage", default="",
            )
        )
        pret_payload: dict[str, str] = {"montant": "", "taux": "", "duree": ""}
        if etape == "compromis":
            col_d, col_e, col_f = st.columns(3)
            pret_payload = {
                "montant": _format_montant(
                    _cession_text(
                        col_d, "Montant du pret (compromis)",
                        section="financement", field="pret_montant", default="",
                    )
                ),
                "taux": _cession_text(
                    col_e, "Taux du pret (facultatif)",
                    section="financement", field="pret_taux", default="",
                ),
                "duree": _cession_text(
                    col_f, "Duree du pret (facultatif)",
                    section="financement", field="pret_duree", default="",
                ),
            }
        credit_payload: dict[str, object] | None = None
        scm_payload: dict[str, object] | None = None
        if etape == "acte" and type_cabinet == "medical":
            credit_key = f"{_CESSION_PREFIX}_cession_financement_credit_actif"
            _seed_default(credit_key, True)
            credit_actif = st.checkbox(
                "Credit-vendeur (clause de l'acte medical)",
                key=credit_key,
                help=(
                    "La clause credit-vendeur du modele medical est figee : "
                    "la decocher bloque la generation."
                ),
            )
            if credit_actif:
                col_g, col_h, col_i, col_j = st.columns(4)
                credit_payload = {
                    "actif": True,
                    "montant": _format_montant(
                        _cession_text(
                            col_g, "Montant credit-vendeur", section="financement",
                            field="credit_montant", default="",
                        )
                    ),
                    "duree": _cession_text(
                        col_h, "Duree (annees)", section="financement",
                        field="credit_duree", default="",
                    ),
                    "taux": _cession_text(
                        col_i, "Taux", section="financement",
                        field="credit_taux", default="",
                    ),
                    "majoration_interet_retard": _cession_text(
                        col_j, "Majoration interet de retard", section="financement",
                        field="credit_majoration", default="",
                    ),
                }
            scm_actif_key = f"{_CESSION_PREFIX}_cession_scm_clause_actif"
            _seed_default(scm_actif_key, False)
            scm_actif = st.checkbox(
                "Cession de parts de SCM associee (clause de l'acte medical)",
                key=scm_actif_key,
            )
            if scm_actif:
                scm_payload = {
                    "actif": True,
                    "nb_parts_a_ceder": _cession_text(
                        st, "Nombre de parts SCM a ceder",
                        section="financement", field="scm_parts", default="",
                    ),
                }
        financement_payload = {
            # §12.1 : banque non saisie -> vide. Le generateur d'appel de fonds
            # omet la ligne banque quand le nom est vide (pas de placeholder
            # parasite) ; la mention se complete a la main sur le document.
            "banque": {"nom": "", "adresse_affichee": ""},
            "destinataire": {
                "civilite_affichage": destinataire_civilite,
                "prenom": destinataire_prenom,
                "nom": destinataire_nom,
            },
            "montant_deblocage": montant_deblocage,
            "pret": pret_payload,
            "credit_vendeur": credit_payload,
        }

    # --- Salaries (tickets 2.12 / 3.3 / 3.4) : acte dentaire uniquement ---
    salaries_payload: list[dict[str, object]] = []
    if type_cabinet == "dentaire" and etape == "acte":
        with st.expander("Salaries repris"):
            aucun_key = f"{_CESSION_PREFIX}_cession_salaries_aucun"
            _seed_default(aucun_key, True)
            aucun_salarie = st.checkbox("Aucun salarie", key=aucun_key)
            if aucun_salarie:
                st.caption(
                    "La phrase relative aux salaries sera supprimee de l'acte ; "
                    "la generation n'est pas bloquee."
                )
            else:
                nb_key = f"{_CESSION_PREFIX}_cession_salaries_nb"
                _seed_default(nb_key, 1)
                nb_salaries = st.number_input(
                    "Nombre de salaries repris",
                    min_value=1,
                    max_value=20,
                    step=1,
                    key=nb_key,
                )
                for index in range(int(nb_salaries)):
                    col_a, col_b, col_c, col_d = st.columns(4)
                    salaries_payload.append(
                        {
                            "civilite_affichage": _cession_text(
                                col_a, f"Civilite salarie {index + 1}",
                                section="salarie", field=f"{index}_civilite", default="",
                            ),
                            "prenom": _cession_text(
                                col_b, f"Prenom salarie {index + 1}",
                                section="salarie", field=f"{index}_prenom", default="",
                            ),
                            "nom": _cession_text(
                                col_c, f"Nom salarie {index + 1}",
                                section="salarie", field=f"{index}_nom", default="",
                            ),
                            "poste": _cession_text(
                                col_d, f"Poste salarie {index + 1} (facultatif)",
                                section="salarie", field=f"{index}_poste", default="",
                            )
                            or None,
                        }
                    )

    date_limite_realisation = ""
    if etape == "compromis":
        date_limite_realisation = _cession_text(
            st, "Date limite de realisation (JJ/MM/AAAA, facultatif)",
            section="meta", field="date_limite", default="",
        )

    # --- Avenant de bail (DOC-007) : bailleur a renseigner, locataire derive ---
    with st.expander("Avenant de bail — bailleur"):
        st.caption(
            "Le locataire actuel est l'associe unique ; le nouveau locataire est la "
            "societe en cours de creation. Champs vides : omis de l'avenant."
        )
        col_a, col_b, col_c = st.columns(3)
        bailleur_civilite = _cession_text(
            col_a, "Civilite du bailleur", section="bailleur", field="civilite",
            default="",
        )
        bailleur_prenom = _cession_text(
            col_b, "Prenom du bailleur", section="bailleur", field="prenom", default="",
        )
        bailleur_nom = _cession_text(
            col_c, "Nom du bailleur", section="bailleur", field="nom", default="",
        )
        bailleur_adresse = _cession_text(
            st, "Adresse du bailleur (facultatif)", section="bailleur", field="adresse",
            default="",
        )

    payload: dict[str, object] = {
        "type_cabinet": type_cabinet,
        "etape": etape,
        "vendeur": vendeur_payload,
        "acquereur": acquereur_payload,
        "cabinet": cabinet_payload,
        "bail_professionnel": bail_payload,
        "exercices": exercices_payload,
        "prix": prix_payload,
        "financement": financement_payload,
        "scm": scm_payload,
        "salaries": salaries_payload,
        "date_limite_realisation": date_limite_realisation,
        # Wordings figes des modeles valides en amont (memes drapeaux que les
        # scenarios ratifies) ; le cas complexe d'origine reste manuel.
        "validations": {
            "mentions_bail_medical_validees": True,
            "origine_compromis_medical_validee": True,
            "date_realisation_compromis_validee": True,
            "ligne_contrats_travail_medical_supprimee": True,
            "salaries_dentaire_deux_valides": True,
        },
    }
    cession_context = CessionContext.model_validate(payload)

    bail_context = BailContext.model_validate(
        {
            "date_avenant": generation.get("signature_date"),
            "date_signature_origine": date_bail,
            "societe_en_cours_immatriculation": True,
            "bailleur_accepte_changement_locataire": True,
            "bailleur": {
                "civilite_affichage": bailleur_civilite,
                "prenom": bailleur_prenom,
                "nom": bailleur_nom,
                "profession": "",
                "adresse_affichee": bailleur_adresse,
            },
            "locataire": {
                "civilite_affichage": DEFAULT_TITRE_AFFICHAGE,
                "civilite_courte": DEFAULT_TITRE_AFFICHAGE,
                "prenom": praticien_prenom,
                "nom": praticien_nom,
                "profession": profession_label,
                "date_naissance": praticien.get("date_naissance"),
                "ville_naissance": str(praticien.get("ville_naissance") or ""),
                "nationalite": str(praticien.get("nationalite") or ""),
                "adresse_affichee": praticien_adresse,
            },
        }
    )
    return cession_context, bail_context


def _render_scm_cession_form(
    scm: bool,
    *,
    praticien: dict[str, object],
    societe: dict[str, object],
    profession_label: str,
    ordre: dict[str, object],
    prefix: str = "selarl",
) -> ScmCessionContext | None:
    """Sous-formulaire de cession de parts de SCM standalone (DOC-031/032/033).

    Plus court que la cession de cabinet : reutilise la fixture SCM comme base
    complete et expose les champs cles. Le cedant est preremplie avec l'associe
    unique (retours client 2026-06-11, ticket 2.13) et reste modifiable.
    Retourne None si non demande.
    """
    if not scm:
        return None

    global _CESSION_PREFIX
    _CESSION_PREFIX = prefix

    st.markdown("**Cession de parts de SCM**")
    base = scm_cession_fixture()
    payload = base.model_dump(by_alias=True)

    scm_cedee = payload.setdefault("scm_cedee", {}) or {}
    with st.expander("SCM cedee", expanded=True):
        scm_cedee["denomination"] = _cession_text(
            st, "Denomination SCM", section="scm_cedee", field="denomination",
            default=str(scm_cedee.get("denomination") or ""),
        )
        col_a, col_b = st.columns(2)
        scm_cedee["ville_rcs"] = _cession_text(
            col_a, "RCS (ville)", section="scm_cedee", field="rcs_ville",
            default=str(scm_cedee.get("ville_rcs") or ""),
        )
        scm_cedee["numero_rcs"] = _cession_text(
            col_b, "Numero RCS", section="scm_cedee", field="numero_rcs",
            default=str(scm_cedee.get("numero_rcs") or ""),
        )
        # §4.1 — capital / parts / nominal / plage pilotables (la fixture ne les
        # exposait pas : capital 3 000, 300 parts, nominal 10, plage 1 a 300
        # s'imprimaient en dur). On les rend editables, preremplis avec la base.
        col_c, col_d = st.columns(2)
        scm_cedee["capital_social"] = _cession_text(
            col_c, "Capital social SCM", section="scm_cedee", field="capital_social",
            default=str(scm_cedee.get("capital_social") or ""),
        )
        nb_parts_saisi = _cession_text(
            col_d, "Nombre total de parts", section="scm_cedee", field="nb_parts_total",
            default=str(scm_cedee.get("nb_parts_total") or ""),
        )
        # nb_parts_total est un entier cote modele : on ne remplace la base que
        # si la saisie est un entier valide, sinon on conserve la valeur de base
        # (jamais de cle requise videe / cassee).
        if nb_parts_saisi.isdigit():
            scm_cedee["nb_parts_total"] = int(nb_parts_saisi)
        col_e, col_f = st.columns(2)
        scm_cedee["valeur_nominale_part"] = _cession_text(
            col_e, "Valeur nominale d'une part", section="scm_cedee",
            field="valeur_nominale_part",
            default=str(scm_cedee.get("valeur_nominale_part") or ""),
        )
        scm_cedee["plage_parts_total"] = _cession_text(
            col_f, "Plage totale des parts (ex. 1 a 300)", section="scm_cedee",
            field="plage_parts_total",
            default=str(scm_cedee.get("plage_parts_total") or ""),
        )
    payload["scm_cedee"] = scm_cedee

    cedant = payload.setdefault("cedant", {}) or {}
    with st.expander("Cedant"):
        st.caption("Preremplie avec l'associe unique ; modifiable si besoin.")
        # Preremplissage vivant : tant que le champ est vide, il suit la fiche
        # praticien ; une saisie manuelle prend le dessus.
        for field, value in (
            ("civilite", str(praticien.get("civilite") or "")),
            ("prenom", str(praticien.get("prenom") or "")),
            ("nom", str(praticien.get("nom") or "")),
        ):
            key = f"{_CESSION_PREFIX}_cession_scm_cedant_{field}"
            if not st.session_state.get(key) and value:
                st.session_state[key] = value
        col_a, col_b, col_c = st.columns(3)
        cedant["civilite_affichage"] = _cession_text(
            col_a, "Civilite", section="scm_cedant", field="civilite",
            default="",
        )
        cedant["prenom"] = _cession_text(
            col_b, "Prenom", section="scm_cedant", field="prenom",
            default="",
        )
        cedant["nom"] = _cession_text(
            col_c, "Nom", section="scm_cedant", field="nom",
            default="",
        )
    # §13.2 : completer le cedant avec l'etat civil REEL (la fixture ne pilote que
    # civilite/prenom/nom). L'ordre est FUSIONNE (pas remplace) pour ne jamais
    # vider une cle requise par le generateur.
    cedant_overrides = _scm_cedant_overrides(
        praticien,
        profession_label=profession_label,
        departement_ordre=str((ordre or {}).get("departement_ordre") or ""),
    )
    ordre_override = cedant_overrides.pop("ordre", None)
    cedant.update(cedant_overrides)
    if ordre_override:
        cedant["ordre"] = {**(cedant.get("ordre") or {}), **ordre_override}
    payload["cedant"] = cedant
    # Coherence V1 du wording source : le representant de la SEL cessionnaire
    # EST le cedant (l'associe unique cede ses parts a sa propre SEL).
    cessionnaire = payload.setdefault("cessionnaire", {}) or {}
    representant = cessionnaire.setdefault("representant", {}) or {}
    representant["civilite_affichage"] = cedant["civilite_affichage"]
    representant["civilite_courte"] = (
        "Mme" if "adame" in str(cedant["civilite_affichage"]) else "M."
    )
    representant["prenom"] = cedant["prenom"]
    representant["nom"] = cedant["nom"]
    cessionnaire["representant"] = representant
    # §13.3 : la description de la SEL cessionnaire = la societe creee
    # (denomination / capital / siege / RCS), pas les valeurs de la fixture.
    cessionnaire.update(_scm_cessionnaire_overrides(societe))
    payload["cessionnaire"] = cessionnaire

    parts_cedees = payload.setdefault("parts_cedees", {}) or {}
    prix = payload.setdefault("prix", {}) or {}
    with st.expander("Parts cedees & prix"):
        col_a, col_b, col_c = st.columns(3)
        nb_cedees_saisi = _cession_text(
            col_a, "Nombre de parts cedees", section="scm_parts", field="nb",
            default=str(parts_cedees.get("nb") or ""),
        )
        if nb_cedees_saisi.isdigit():
            parts_cedees["nb"] = int(nb_cedees_saisi)
        plage = _cession_text(
            col_b, "Plage parts cedees (ex. 151 a 200)", section="scm_parts", field="plage",
            default=str(parts_cedees.get("plage") or ""),
        )
        parts_cedees["plage"] = plage
        prix["global"] = _cession_text(
            col_c, "Prix global", section="scm_prix", field="global",
            default=str(prix.get("global") or ""),
        )
        prix["global_lettres"] = _cession_text(
            st, "Prix global (lettres)", section="scm_prix", field="global_lettres",
            default=str(prix.get("global_lettres") or ""),
        )
    payload["parts_cedees"] = parts_cedees
    payload["prix"] = prix

    # §4.1 — repeater des associes PRESENTS (plus de fixture 3 presents / 4 apres).
    # L'apres-cession est DERIVE deterministe (cedant reduit + SEL cessionnaire
    # entrante), jamais saisi. signataires_pv en derive aussi.
    presents = _render_scm_cession_associes_presents(scm_cedee)
    payload["associes_presents"] = [a.model_dump() for a in presents]
    payload["associes_avant_cession"] = [a.model_dump() for a in presents]
    apres = _derive_scm_apres_cession(presents, cedant, cessionnaire, parts_cedees)
    payload["associes_apres_cession"] = [a.model_dump() for a in apres]
    payload["signataires_pv"] = _derive_scm_signataires_pv(presents)

    return ScmCessionContext.model_validate(payload)


def _render_scm_cession_associes_presents(
    scm_cedee: dict[str, object],
) -> list[ScmCessionAssocie]:
    """Repeater des associes PRESENTS a l'AGE de cession SCM (§4.1).

    N associes (identite + nb de parts + plage). Le total des parts doit egaler
    le capital de la SCM (nb_parts_total) ; un avertissement non bloquant le
    signale sinon. Le dernier associe preside la seance (regle moteur a10ff29)."""
    with st.expander("Associes presents a l'assemblee", expanded=True):
        st.caption(
            "Le total des parts des presents doit egaler le nombre total de parts "
            "de la SCM. Le dernier associe saisi preside la seance (gerant associe)."
        )
        count_key = f"{_CESSION_PREFIX}_cession_scm_presents_count"
        _seed_default(count_key, 3)
        nb_associes = int(
            st.number_input(
                "Nombre d'associes presents",
                min_value=1,
                step=1,
                key=count_key,
            )
        )
        presents: list[ScmCessionAssocie] = []
        for index in range(nb_associes):
            st.markdown(f"Associe present {index + 1}")
            morale = st.checkbox(
                "Personne morale",
                key=f"{_CESSION_PREFIX}_cession_scm_present_{index}_morale",
            )
            if morale:
                col_a, col_b = st.columns(2)
                denomination = _cession_text(
                    col_a, "Denomination", section="scm_present", field=f"{index}_denomination",
                    default="",
                )
                forme = _cession_text(
                    col_b, "Forme juridique", section="scm_present", field=f"{index}_forme",
                    default="",
                )
                identity = {
                    "type_personne": "personne_morale",
                    "denomination": denomination or None,
                    "forme_juridique": forme or None,
                }
            else:
                col_a, col_b, col_c = st.columns(3)
                civilite = col_a.selectbox(
                    "Civilite",
                    ("Monsieur", "Madame"),
                    key=f"{_CESSION_PREFIX}_cession_scm_present_{index}_civilite",
                )
                prenom = _cession_text(
                    col_b, "Prenom", section="scm_present", field=f"{index}_prenom",
                    default="",
                )
                nom = _cession_text(
                    col_c, "Nom", section="scm_present", field=f"{index}_nom",
                    default="",
                )
                identity = {
                    "type_personne": "personne_physique",
                    "civilite_affichage": civilite,
                    "prenom": prenom or None,
                    "nom": nom or None,
                }
            col_d, col_e = st.columns(2)
            nb_parts_saisi = _cession_text(
                col_d, "Nombre de parts", section="scm_present", field=f"{index}_nb_parts",
                default="",
            )
            plage = _cession_text(
                col_e, "Plage de parts (ex. 1 a 100)", section="scm_present",
                field=f"{index}_plage", default="",
            )
            presents.append(
                ScmCessionAssocie(
                    **identity,
                    parts=ScmCessionPartsAttribution(
                        nb=int(nb_parts_saisi) if nb_parts_saisi.isdigit() else None,
                        plage=plage or None,
                    ),
                )
            )
        total_parts = sum((a.parts.nb or 0) for a in presents if a.parts)
        nb_total_scm = int(scm_cedee.get("nb_parts_total") or 0)
        if nb_total_scm and total_parts != nb_total_scm:
            st.warning(
                f"Total des parts des presents ({total_parts}) different du nombre "
                f"total de parts de la SCM ({nb_total_scm}). La generation du PV "
                "sera bloquee tant que les deux ne coincident pas."
            )
    return presents


def _scm_same_person(associe: ScmCessionAssocie, cedant: dict[str, object]) -> bool:
    """Vrai si l'associe present EST le cedant (match prenom + nom, insensible casse)."""
    if associe.type_personne != "personne_physique":
        return False
    prenom = (associe.prenom or "").strip().casefold()
    nom = (associe.nom or "").strip().casefold()
    cedant_prenom = str(cedant.get("prenom") or "").strip().casefold()
    cedant_nom = str(cedant.get("nom") or "").strip().casefold()
    if not (cedant_prenom or cedant_nom):
        return False
    return prenom == cedant_prenom and nom == cedant_nom


def _derive_scm_apres_cession(
    presents: list[ScmCessionAssocie],
    cedant: dict[str, object],
    cessionnaire: dict[str, object],
    parts_cedees: dict[str, object],
) -> list[ScmCessionAssocie]:
    """Derive la repartition APRES cession, deterministe (§4.1).

    Regle : le cedant cede `parts_cedees.nb` parts (plage `parts_cedees.plage`) a
    la SEL cessionnaire (personne morale entrante). Les autres associes sont
    inchanges. Cas geres :
      - cedant cede TOUTES ses parts -> retire de l'apres-cession ;
      - cedant cede une PARTIE -> reduit (nb diminue, plage = complement) ;
      - la SEL acquereur entre avec les parts cedees (plage = plage cedee).
    La plage residuelle du cedant est le COMPLEMENT de sa plage initiale moins la
    plage cedee quand celles-ci sont des intervalles contigus ; sinon on retombe
    proprement sur un libelle explicite (jamais de placeholder)."""
    nb_cedees = int(parts_cedees.get("nb") or 0)
    plage_cedee = str(parts_cedees.get("plage") or "")
    apres: list[ScmCessionAssocie] = []
    cessionnaire_present = False
    for associe in presents:
        if not _scm_same_person(associe, cedant):
            apres.append(associe.model_copy(deep=True))
            continue
        nb_initial = (associe.parts.nb if associe.parts else None) or 0
        plage_initiale = (associe.parts.plage if associe.parts else None) or ""
        reste = nb_initial - nb_cedees
        if reste > 0:
            apres.append(
                associe.model_copy(
                    deep=True,
                    update={
                        "parts": ScmCessionPartsAttribution(
                            nb=reste,
                            plage=_complement_plage(plage_initiale, plage_cedee),
                        )
                    },
                )
            )
        # reste <= 0 : le cedant a tout cede -> il sort de l'apres-cession.
    # SEL cessionnaire entrante (personne morale) avec les parts cedees.
    apres.append(
        ScmCessionAssocie(
            type_personne="personne_morale",
            denomination=str(cessionnaire.get("denomination") or "") or None,
            forme_juridique=str(cessionnaire.get("forme_juridique") or "") or None,
            parts=ScmCessionPartsAttribution(
                nb=nb_cedees or None,
                plage=plage_cedee or None,
            ),
        )
    )
    cessionnaire_present = True
    _ = cessionnaire_present
    return apres


def _parse_plage(plage: str) -> tuple[int, int] | None:
    """Parse « A a B » / « A à B » / « A-B » en (A, B) ; None si non parsable."""
    match = re.search(r"(\d+)\s*(?:a|à|-)\s*(\d+)", plage.strip(), flags=re.IGNORECASE)
    if match is None:
        return None
    debut, fin = int(match.group(1)), int(match.group(2))
    if fin < debut:
        return None
    return debut, fin


def _complement_plage(plage_initiale: str, plage_cedee: str) -> str:
    """Plage residuelle du cedant = plage initiale moins la plage cedee (§4.1).

    Cas deterministe simple : la plage cedee est a une EXTREMITE de la plage
    initiale (debut ou fin) -> le complement est l'autre tranche contigue. Sinon
    (cas non contigu / non parsable), on retombe sur un libelle explicite base sur
    la plage initiale, jamais de placeholder ni de plage fausse."""
    init = _parse_plage(plage_initiale)
    cedee = _parse_plage(plage_cedee)
    if init is None or cedee is None:
        return plage_initiale
    i_debut, i_fin = init
    c_debut, c_fin = cedee
    # Plage cedee a la FIN de la plage initiale : reste = [i_debut, c_debut - 1].
    if c_fin == i_fin and c_debut > i_debut:
        return f"{i_debut} a {c_debut - 1}"
    # Plage cedee au DEBUT de la plage initiale : reste = [c_fin + 1, i_fin].
    if c_debut == i_debut and c_fin < i_fin:
        return f"{c_fin + 1} a {i_fin}"
    # Cas non contigu : on conserve la plage initiale (le nb reste fait foi).
    return plage_initiale


def _derive_scm_signataires_pv(presents: list[ScmCessionAssocie]) -> list[str]:
    """Signataires du PV = les associes presents (libelle court civilite + nom)."""
    signataires: list[str] = []
    for associe in presents:
        if associe.type_personne == "personne_morale":
            label = str(associe.denomination or "").strip()
        else:
            civ = str(associe.civilite_affichage or "")
            court = "Mme" if "adame" in civ else "M."
            prenom = str(associe.prenom or "").strip()
            nom = str(associe.nom or "").strip()
            label = " ".join(part for part in (court, prenom, nom) if part)
        if label:
            signataires.append(label)
    return signataires


def _render_generation_zone(data_entry: CleanDataEntry, plan: CleanGenerationPlan) -> None:
    st.subheader("Generation")
    for warning in plan.warnings:
        st.info(warning)
    if plan.can_generate:
        st.success(plan.reason)
    else:
        st.warning(plan.reason)
    if plan.blockers:
        for blocker in plan.blockers[:8]:
            st.caption(f"Blocage : {blocker}")
        if len(plan.blockers) > 8:
            st.caption(f"{len(plan.blockers) - 8} autres champs requis.")

    st.markdown("Documents")
    for row in plan.document_rows:
        st.caption(f"{row.doc_code} - {row.label} - {row.status} : {row.message}")

    if plan.front_data_scope:
        st.caption("Fondations front_data utilisees : " + " | ".join(plan.front_data_scope))

    if st.button(
        "Generer le dossier",
        key="clean_generate_dossier",
        disabled=not plan.can_generate,
        type="primary",
    ):
        try:
            result = generate_selarl_dossier(
                data_entry,
                _output_dir(data_entry.dossier_reference),
            )
        except Exception as exc:
            st.error(f"Generation bloquee par le moteur : {exc}")
            return
        st.session_state[GENERATED_DOSSIER_STATE_KEY] = {
            "output_dir": str(result.output_dir),
            "zip_path": str(result.zip_path),
            "docx_paths": [str(path) for path in result.docx_paths],
        }

    generated_dossier = st.session_state.get(GENERATED_DOSSIER_STATE_KEY)
    if isinstance(generated_dossier, dict):
        _render_generated_dossier_downloads(generated_dossier)


def _output_dir(dossier_reference: str) -> Path:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", dossier_reference).strip("._")
    return ARTIFACTS_DIR / (slug or "selarl_v1")


# --- Routage des types non-SELARL --------------------------------------------

TYPED_GENERATED_STATE_KEY = "clean_typed_generated_dossier"


def _render_typed_dossier(dossier_type: DossierTypeOption) -> None:
    """Rendu generique pour tout type non-SELARL : form -> plan -> generation.

    Route par structure vers le slice dedie (registre `type_registry`). Chaque
    slice expose `render_*_form`, `build_*_plan`, `generate_dossier`.
    """
    from sydel_doc_engine.front_app import (
        civil_statuts_slice,
        sas_slice,
        selas_multi_slice,
        selas_uni_medecin_slice,
        spfpl_slice,
    )

    structure = dossier_type.structure
    if structure in civil_statuts_slice.CIVIL_TYPE_BY_STRUCTURE:
        payload = civil_statuts_slice.render_civil_form(structure)
        plan = civil_statuts_slice.build_civil_plan(payload)
        generate = civil_statuts_slice.generate_dossier
    elif structure == "SAS":
        payload = sas_slice.render_sas_form()
        plan = sas_slice.build_sas_plan(payload)
        generate = sas_slice.generate_dossier
    elif structure in spfpl_slice.OPERATION_BY_STRUCTURE:
        payload = spfpl_slice.render_spfpl_form(structure)
        plan = spfpl_slice.build_spfpl_plan(payload)
        generate = spfpl_slice.generate_dossier
    elif structure == "SELAS uni medecin":
        # SELAS UNIPERSONNELLE medecin (DOC-018) : parcours uni dedie, distinct de
        # la SELAS multi (DOC-044, >=2 associes). Rebranche le generateur orphelin.
        payload = selas_uni_medecin_slice.render_selas_uni_medecin_form()
        plan = selas_uni_medecin_slice.build_selas_uni_medecin_plan(payload)
        generate = selas_uni_medecin_slice.generate_dossier
    elif structure == "SELAS":
        # On passe la cle du type pour que la SELAS « dentiste pluripersonnelle »
        # pre-regle la profession sur chirurgien-dentiste (corpus dentiste).
        payload = selas_multi_slice.render_selas_form(dossier_type.key)
        plan = selas_multi_slice.build_selas_plan(payload)
        generate = selas_multi_slice.generate_dossier
    else:
        st.warning("Type de dossier non branche dans le front clean.")
        return

    _render_typed_generation_zone(dossier_type, payload, plan, generate)


def _render_typed_generation_zone(
    dossier_type: DossierTypeOption,
    payload: dict,
    plan,
    generate,
) -> None:
    st.subheader("Generation")
    for warning in getattr(plan, "warnings", ()):  # type: ignore[arg-type]
        st.info(warning)
    if plan.can_generate:
        st.success(plan.reason)
    else:
        st.warning(plan.reason)
    for blocker in list(plan.blockers)[:8]:
        st.caption(f"Blocage : {blocker}")
    if len(plan.blockers) > 8:
        st.caption(f"{len(plan.blockers) - 8} autres champs requis.")

    st.markdown("Documents")
    for code in plan.document_codes:
        st.caption(f"{code} - inclus dans {dossier_type.label}.")

    generation_disabled = not (plan.can_generate and dossier_type.generation_enabled)
    if not dossier_type.generation_enabled:
        st.warning("Generation desactivee pour ce type (en attente de validation metier).")

    if st.button(
        "Generer le dossier",
        key="clean_typed_generate_dossier",
        disabled=generation_disabled,
        type="primary",
    ):
        try:
            result = generate(payload, _typed_output_dir(dossier_type))
        except Exception as exc:  # noqa: BLE001 — on remonte l'erreur moteur a l'UI
            st.error(f"Generation bloquee par le moteur : {exc}")
            return
        st.session_state[TYPED_GENERATED_STATE_KEY] = {
            "output_dir": str(result.output_dir),
            "zip_path": str(result.zip_path),
            "docx_paths": [str(path) for path in result.docx_paths],
        }

    generated_dossier = st.session_state.get(TYPED_GENERATED_STATE_KEY)
    if isinstance(generated_dossier, dict):
        _render_generated_dossier_downloads(generated_dossier)


def _typed_output_dir(dossier_type: DossierTypeOption) -> Path:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", dossier_type.key).strip("._")
    return ARTIFACTS_DIR / (slug or "typed")


def _render_generated_dossier_downloads(generated_dossier: dict[str, object]) -> None:
    output_dir = generated_dossier.get("output_dir", "")
    zip_path = Path(str(generated_dossier.get("zip_path", "")))
    docx_paths = [
        Path(str(path))
        for path in generated_dossier.get("docx_paths", [])
        if isinstance(path, str)
    ]

    st.success(f"Dossier genere : {output_dir}")
    st.caption(f"ZIP : {zip_path}")
    if zip_path.is_file():
        st.download_button(
            "Telecharger le dossier ZIP",
            data=zip_path.read_bytes(),
            file_name=zip_path.name,
            mime="application/zip",
            key="clean_download_zip",
            type="primary",
            on_click="ignore",
        )
    else:
        st.error("ZIP genere introuvable sur le serveur.")

    for index, path in enumerate(docx_paths):
        st.caption(f"DOCX : {path}")
        if not path.is_file():
            st.error(f"DOCX genere introuvable : {path.name}")
            continue
        st.download_button(
            f"Telecharger {path.name}",
            data=path.read_bytes(),
            file_name=path.name,
            mime=DOCX_MIME_TYPE,
            key=f"clean_download_docx_{index}",
            on_click="ignore",
        )
