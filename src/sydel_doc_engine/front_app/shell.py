from __future__ import annotations

import re
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

import streamlit as st

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
from sydel_doc_engine.front_app._dev_fixtures import (
    _TYPED_TEST_DATA_PREFILL,
    _TYPED_TEST_DATA_PREFILL_BY_KEY,
    _prefill_random_selarl_data,
)
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
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
    MATRIMONIAL_STATUS_PRESETS,
    NATIONALITY_PRESETS,
    _decimal_from_value,
    accentuate_french_months,
    calculate_nominal_value,
    derive_gender_from_civilite,
    format_french_date,
    format_grouped_numeric_value,
    format_numeric_value,
    matrimonial_display_gendered,
    matrimonial_status_value,
    number_words_from_value,
    parse_french_date,
    prix_lettres_from_value,
    regime_communautaire_from_status,
    regime_matrimonial_from_status,
    shift_repeater_rows_down,
    situation_display,
)
from sydel_doc_engine.front_app.front_widgets import (
    copyable_text_input,
    date_input_with_today,
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
    st.title("SYDEL")
    st.caption(
        "Génération de dossiers juridiques : SELARL, SCM, SCI, SCI IRIS, SCS, SAS, "
        "SPFPL, SELAS."
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
        st.caption("Type sélectionné : SELARL unipersonnelle.")
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
        st.caption(f"Type sélectionné : {selected.label}.")
    return selected


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
    praticien_apport = copyable_text_input(col_b,
        "Apport du praticien (euros)",
        key="selarl_praticien_apport",
    )

    count_key = "selarl_membres_count"
    if count_key not in st.session_state:
        st.session_state[count_key] = 1
    nombre = max(1, min(5, int(st.session_state[count_key])))
    add_col = st.columns([1, 3])[0]
    if add_col.button("Ajouter un associe", key="selarl_membres_add"):
        st.session_state[count_key] = min(5, nombre + 1)
    # Retour Albane 2026-07-07 (propagation) : le bouton global « Retirer un associe »
    # (qui ne supprimait que le DERNIER) est remplace par un bouton « Retirer cet
    # associe » PAR LIGNE (cf. _remove_selarl_membre_at), comme le repeater civil.
    # N5 (Albane 2026-06-24) : re-lire le nombre APRES les boutons +/- au lieu de st.rerun().
    # Le st.rerun() premature s'executait avant la boucle membres -> Streamlit garbage-collectait
    # l'etat des widgets membres non instancies -> les champs des associes PRECEDENTS etaient
    # effaces a l'ajout. Meme fix que selas_multi_slice / associe_repeater (propagation N5).
    nombre = max(1, min(5, int(st.session_state[count_key])))

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


def _remove_selarl_membre_at(index: int) -> None:
    """Retire le membre additionnel `index` (bouton par ligne — Albane 2026-07-07).

    Callback `on_click` : il s'execute AVANT l'instanciation des widgets du rerun, seule
    fenetre ou Streamlit autorise la recopie des cles `selarl_membre_{i}_*` (les lignes
    suivantes remontent d'un cran) et la decrementation du compteur. Pas de st.rerun()
    manuel (lecon N5 : un rerun avant le rendu des lignes efface l'etat des widgets non
    instancies). Plancher 1 membre additionnel (le mode multi = praticien + au moins 1).
    """
    count_key = "selarl_membres_count"
    count = max(1, min(5, int(st.session_state.get(count_key) or 1)))
    if count <= 1:
        return
    shift_repeater_rows_down(st.session_state, "selarl_membre_", index, count)
    st.session_state[count_key] = count - 1


def _render_one_selarl_membre(index: int) -> StatutsCivilsAssocie | None:
    prefix = f"selarl_membre_{index}"
    with st.expander(f"Associe additionnel {index + 2}", expanded=index == 0):
        # Retour Albane 2026-07-07 (propagation) : chaque ligne porte son bouton
        # « Retirer » (on ne pouvait supprimer que le dernier ajoute). Desactive au
        # plancher 1 membre. on_click OBLIGATOIRE : recopie des cles pre-rerun.
        st.button(
            "Retirer cet associe",
            key=f"selarl_membres_remove_{index}",
            on_click=_remove_selarl_membre_at,
            args=(index,),
            disabled=int(st.session_state.get("selarl_membres_count") or 1) <= 1,
        )
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
        apport = copyable_text_input(col_a, "Apport (euros)", key=f"{prefix}_apport")
        parts = StatutsCivilsParts(nb=nb_parts, nb_lettres=number_words_from_value(nb_parts))
        apport_obj = StatutsCivilsApport(
            montant=apport, montant_lettres=number_words_from_value(apport)
        )
        if type_personne == "personne_morale":
            denomination = copyable_text_input(st, "Denomination", key=f"{prefix}_denomination")
            col_b, col_c = st.columns(2)
            forme = copyable_text_input(col_b, "Forme juridique", key=f"{prefix}_forme")
            capital = copyable_text_input(col_c, "Capital social (euros)", key=f"{prefix}_capital")
            siege = copyable_text_input(st, "Siege (adresse affichee)", key=f"{prefix}_siege")
            col_d, col_e = st.columns(2)
            numero_rcs = copyable_text_input(col_d, "Numero RCS", key=f"{prefix}_rcs")
            ville_rcs = copyable_text_input(col_e, "Ville RCS", key=f"{prefix}_ville_rcs")
            st.caption("Representant legal")
            col_f, col_g, col_h = st.columns(3)
            rep_civilite = col_f.selectbox(
                "Civilite rep.", ("Monsieur", "Madame"), key=f"{prefix}_rep_civilite"
            )
            rep_prenom = copyable_text_input(col_g, "Prenom rep.", key=f"{prefix}_rep_prenom")
            rep_nom = copyable_text_input(col_h, "Nom rep.", key=f"{prefix}_rep_nom")
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
        prenom = copyable_text_input(col_c, "Prenom", key=f"{prefix}_prenom")
        nom = copyable_text_input(col_d, "Nom", key=f"{prefix}_nom")
        col_e, col_f, col_g = st.columns(3)
        # R29-06 (Rafael) : selecteur de date (calendrier) + « Aujourd'hui » sur la date
        # de naissance (associe personne physique d'une personne morale / SELARL multi).
        # Champ texte JJ/MM/AAAA conserve (saisie verbatim possible), cle inchangee ->
        # _accentuate_date_value aval preserve. seed=False (pas de date du jour).
        date_input_with_today(
            "Date de naissance",
            key=f"{prefix}_date_naissance",
            value=date.today(),
            container=col_e,
            seed=False,
        )
        date_naissance = str(st.session_state.get(f"{prefix}_date_naissance") or "").strip()
        ville_naissance = copyable_text_input(
            col_f, "Ville de naissance", key=f"{prefix}_ville_naissance"
        )
        dep_naissance = copyable_text_input(
            col_g, "Departement naissance (ou pays si étranger)", key=f"{prefix}_dep_naissance"
        )
        col_h, col_i = st.columns(2)
        nationalite = copyable_text_input(col_h, "Nationalite", key=f"{prefix}_nationalite")
        # KAN-37 (Rafael 2026-07-27) : la situation matrimoniale est un MENU DÉROULANT PARTOUT.
        # Le membre SELARL multi echoant sa situation dans les statuts, on NORMALISE le preset via
        # `situation_display` (genre resolu -> mot d'etat civil accorde et accentue, « marié »/
        # « mariée »), donc plus de « (e) » injecte : c'est la conversion differee de [R3-membre].
        situation_label = col_i.selectbox(
            "Situation matrimoniale", MATRIMONIAL_STATUS_PRESETS, key=f"{prefix}_situation"
        )
        situation = matrimonial_display_gendered(
            situation_label, derive_gender_from_civilite(civilite)
        )
        profession = copyable_text_input(st, "Profession", key=f"{prefix}_profession")
        adresse = copyable_text_input(st, "Adresse personnelle (affichee)", key=f"{prefix}_adresse")
        # DNC par associe (Rafael 2026-07-09) : chaque associe personne physique a sa
        # propre declaration de non-condamnation -> filiation saisie PAR membre.
        st.caption("Declaration de non-condamnation (noms des parents)")
        col_pere, col_mere = st.columns(2)
        nom_pere = copyable_text_input(col_pere, "Nom du pere", key=f"{prefix}_sig_nom_pere")
        nom_mere = copyable_text_input(col_mere, "Nom de la mere", key=f"{prefix}_sig_nom_mere")
        col_j, col_k, col_l = st.columns(3)
        ordre_dep = copyable_text_input(col_j, "Departement ordre", key=f"{prefix}_ordre_dep")
        numero_ordre = copyable_text_input(col_k, "Numero ordre", key=f"{prefix}_numero_ordre")
        numero_rpps = copyable_text_input(col_l, "Numero RPPS", key=f"{prefix}_numero_rpps")
        if not (prenom.strip() and nom.strip()):
            return None
        return StatutsCivilsAssocie(
            type_personne="personne_physique",
            genre=derive_gender_from_civilite(civilite),
            civilite_affichage=civilite,
            prenom=prenom,
            nom=nom,
            profession=profession or None,
            # LIVE-03 : date de naissance a saisie LIBRE -> re-accentue les mois
            # (« 1er aout 1980 » -> « 1er août 1980 ») AVANT injection ; le generateur
            # des statuts reste un echo fidele et n'accentue rien en sortie.
            date_naissance=_accentuate_date_value(date_naissance) or None,
            ville_naissance=ville_naissance or None,
            departement_naissance=dep_naissance or None,
            nationalite=nationalite or None,
            situation_maritale=situation or None,
            # DNC par associe : adresse STRUCTUREE derivee de la saisie affichee (meme
            # parseur O24-03 que les autres slices) — requise par DOC-001 du membre.
            adresse_personnelle=_parse_address_full(adresse),
            adresse_personnelle_affichee=adresse or None,
            nom_pere=nom_pere or None,
            nom_mere=nom_mere or None,
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
        "dossier_reference": copyable_text_input(st,
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
    prenom = copyable_text_input(col_d, "Prenom", key="selarl_prenom")
    nom = copyable_text_input(col_e, "Nom", key="selarl_nom")
    col_f, col_g, col_h = st.columns(3)
    with col_f:
        date_naissance = _date_input_with_today(
            "Date de naissance",
            key="selarl_date_naissance",
            value=date(1990, 1, 1),
        )
    ville_naissance = copyable_text_input(col_g, "Ville de naissance", key="selarl_ville_naissance")
    ville_naissance_article_au = col_g.checkbox(
        "au",
        key="selarl_ville_naissance_article_au",
        help="Affiche 'ne au ...' au lieu de 'ne a ...' dans la DNC.",
    )
    departement_naissance = copyable_text_input(col_h,
        "Departement naissance (ou pays si étranger)",
        key="selarl_departement_naissance",
    )
    col_i, col_j = st.columns(2)
    nationalite_choice = col_i.selectbox(
        "Nationalite",
        NATIONALITY_PRESETS,
        key="selarl_nationalite_choice",
    )
    nationalite = (
        copyable_text_input(col_i, "Nationalite autre", key="selarl_nationalite_other")
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
        col_j.caption(
            "Régime de la communauté : la lettre de renonciation et la "
            "lettre d'avertissement au conjoint seront générées."
        )

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
            "conjoint_prenom": copyable_text_input(conj_b,
                "Prenom de l'epoux / partenaire",
                key="selarl_conjoint_prenom",
            ),
            "conjoint_nom": copyable_text_input(conj_c,
                "Nom de l'epoux / partenaire",
                key="selarl_conjoint_nom",
            ),
        }

    # Numero d'Ordre et RPPS sur une meme ligne (ticket 1.4).
    col_k, col_m = st.columns(2)
    numero_ordre = copyable_text_input(col_k, "Numero d'Ordre", key="selarl_numero_ordre")
    numero_rpps = copyable_text_input(col_m, "Numero RPPS", key="selarl_numero_rpps")
    # Parents sur la ligne suivante, avec les libelles demandes (ticket 1.4).
    col_n, col_o = st.columns(2)
    nom_pere = copyable_text_input(col_n, "Nom et prenom du pere", key="selarl_nom_pere")
    nom_mere = copyable_text_input(col_o,
        "Nom de jeune fille et prenom de la mere",
        key="selarl_nom_mere",
    )

    st.markdown("Adresse personnelle")
    # O24-03 : adresse personnelle sur UNE ligne (parse interne -> num/voie/cp/ville).
    # Remplace les 3 champs (Numero et voie / CP / Ville). Le parse alimente les MEMES
    # cles que l'ancienne grille -> generateur SELARL et gold byte-identique inchanges.
    _perso_ligne = copyable_text_input(st,
        "Adresse personnelle (N° et voie, CP Ville)", key="selarl_adresse_ligne"
    )
    _perso_struct = _parse_address_full(_perso_ligne)
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
        "adresse_num_voie": _perso_struct.num_voie if _perso_struct else "",
        "adresse_voie": _perso_struct.voie if _perso_struct else "",
        "adresse_cp": _perso_struct.cp if _perso_struct else "",
        "adresse_ville": _perso_struct.ville if _perso_struct else "",
    }


def _render_societe(
    *,
    praticien: dict[str, object],
) -> dict[str, object]:
    st.markdown("**Fiche Societe**")
    col_a, col_b = st.columns(2)
    denomination = copyable_text_input(col_a, "Denomination sociale", key="selarl_denomination")
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
    # O24-05 (onglet 24) : valeur nominale calculée automatiquement ET affichée DANS LE
    # CHAMP concerné (text_input désactivé), comme les 5 autres types — plus de simple
    # caption gris. Pas de `key` (sinon « value= » + « key= » fige la valeur initiale).
    copyable_text_input(st,
        "Valeur nominale d'une part (calculee)",
        value=valeur_nominale_part,
        disabled=True,
    )
    ville_rcs = copyable_text_input(st, "RCS (ville)", key="selarl_ville_rcs")

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
        # O24-03 : siege sur UNE ligne (parse interne -> num/voie/cp/ville). Remplace les
        # 3 champs (Numero et voie / CP / Ville) ; memes cles que l'ancienne grille ->
        # generateur SELARL et gold byte-identique inchanges.
        _siege_ligne = copyable_text_input(st,
            "Adresse du siège (N° et voie, CP Ville)", key="selarl_siege_ligne"
        )
        _siege_struct = _parse_address_full(_siege_ligne)
        societe = {
            "denomination": denomination,
            "capital_social": format_numeric_value(capital_social),
            "duree": "99 ans",
            "nb_parts_total": int(nb_parts_total),
            "valeur_nominale_part": valeur_nominale_part,
            "ville_rcs": ville_rcs,
            "siege_num_voie": _siege_struct.num_voie if _siege_struct else "",
            "siege_voie": _siege_struct.voie if _siege_struct else "",
            "siege_cp": _siege_struct.cp if _siege_struct else "",
            "siege_ville": _siege_struct.ville if _siege_struct else "",
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
        second_lieu_nom = copyable_text_input(st,
            "Nom du 2e lieu d'exercice",
            key="selarl_second_lieu_exercice_nom",
        )
        second_lieu_adresse = copyable_text_input(st,
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
    departement_ordre = copyable_text_input(col_a,
        "Departement d'inscription a l'ordre",
        key="selarl_departement_ordre",
        help="Exemple : Paris, Loire-Atlantique ou le departement ordinal attendu par le dossier.",
    )
    # M2 (Akainu, 2026-06-30, parite SELAS) : connecteur grammatical place avant le
    # departement dans le destinataire de la demande d'inscription a l'Ordre (R5) :
    # « de Paris » / « du Calvados » / « des Hauts de Seine ». Sans ce selecteur, le SELARL
    # restait bloque sur « de » et ne pouvait pas produire « du Calvados ».
    connecteur_departement = str(
        st.selectbox(
            "Connecteur avant le departement (de / du / des)",
            ("de", "du", "des"),
            key="selarl_ordre_connecteur",
            help="S'affiche dans « ... de l'Ordre <connecteur> <departement> des ... » : "
            "« de Paris » / « du Calvados » / « des Hauts de Seine ».",
        )
    )
    # O24-03 : adresse de l'ordre sur UNE ligne (parse interne -> ligne_1/cp/ville),
    # comme perso/siege/SELAS. Remplace les 3 champs separes (Adresse / CP / Ville ordre) ;
    # alimente les MEMES cles -> generateur DOC-034 et gold byte-identique inchanges.
    _ordre_struct = _parse_address_full(
        copyable_text_input(st,
            "Adresse de l'ordre (N° et voie, CP Ville)",
            key="selarl_ordre_adresse_ligne",
        )
    )
    ordre_adresse_ligne_1 = (
        f"{_ordre_struct.num_voie} {_ordre_struct.voie}".strip() if _ordre_struct else ""
    )
    ordre_cp = _ordre_struct.cp if _ordre_struct else ""
    ordre_ville = _ordre_struct.ville if _ordre_struct else ""
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
    mandataire_prenom = copyable_text_input(col_f,
        "Conseiller (prénom)",
        key="selarl_mandataire_prenom",
    )
    mandataire_nom = copyable_text_input(col_g,
        "Conseiller (nom)",
        key="selarl_mandataire_nom",
    )
    return {
        "departement_ordre": departement_ordre,
        "connecteur_departement": connecteur_departement,
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
    # Dates d'exercice preremplies, cloture du premier exercice au 31 décembre
    # de l'annee N+1, dynamique selon l'annee du dossier (ticket 1.7).
    if not st.session_state.get("selarl_exercice_debut"):
        st.session_state["selarl_exercice_debut"] = "1er janvier"
    if not st.session_state.get("selarl_exercice_fin"):
        st.session_state["selarl_exercice_fin"] = "31 décembre"
    if not st.session_state.get("selarl_exercice_cloture_premier"):
        st.session_state["selarl_exercice_cloture_premier"] = (
            f"31 décembre {date.today().year + 1}"
        )
    col_a, col_b = st.columns(2)
    signature_lieu = copyable_text_input(col_a, "Lieu de signature", key="selarl_signature_lieu")
    with col_b:
        signature_date = _date_input_with_today(
            "Date de signature",
            key="selarl_signature_date",
            value=date.today(),
        )
    # SU4/SCS2 (Albane) : la date du PV de decision = la date de signature dans TOUS les
    # cas (DecisionContext la derive de signature_date). Le champ « Date de decision »
    # dedie etait mort (jamais lu) + requis + trompeur. Supprime (#8 onglet 24).
    col_g, col_h = st.columns(2)
    depot_banque_nom = copyable_text_input(col_g, "Banque depot", key="selarl_depot_banque_nom")
    depot_banque_adresse = copyable_text_input(col_h,
        "Adresse banque",
        key="selarl_depot_banque_adresse",
        help="Vide : les statuts laissent une zone a completer a la main.",
    )
    col_j, col_k, col_l = st.columns(3)
    exercice_debut = copyable_text_input(col_j, "Debut exercice", key="selarl_exercice_debut")
    exercice_fin = copyable_text_input(col_k, "Fin exercice", key="selarl_exercice_fin")
    exercice_cloture_premier = copyable_text_input(col_l,
        "Cloture premier exercice",
        key="selarl_exercice_cloture_premier",
    )
    return {
        "signature_lieu": signature_lieu,
        "signature_date": signature_date,
        "signature_nombre_exemplaires": "quatre",
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
    # O24-10 : tolerant a la forme de la profession (« chirurgien-dentiste » tiret du
    # menu SELAS vs PROFESSION_DENTISTE « chirurgien_dentiste » underscore) -> on teste
    # « dentiste » dans la chaine, comme _scm_profession_pair.
    return "dentaire" if "dentiste" in (profession or "").casefold() else "medical"


def _profession_label(profession: str) -> str:
    # O24-10 : même tolérance que _cession_default_type (tiret vs underscore).
    return "chirurgien-dentiste" if "dentiste" in (profession or "").casefold() else "médecin"


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
        # LIVE-03 : date de naissance saisie libre -> mois re-accentues en amont.
        # Une vraie `date` (saisie via date_input) est preservee telle quelle.
        "date_naissance": _accentuate_date_value(praticien.get("date_naissance")),
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


def _scm_cessionnaire_overrides(
    societe: dict[str, object], *, prefix: str = "selarl"
) -> dict[str, object]:
    """Description de la SEL cessionnaire (= societe creee) derivee de la fiche societe.

    Retour Albane lot 2 §13.3 : le capital / siege / denomination du cessionnaire
    restaient ceux de la fixture (capital 10 000 affiche alors que 1 000 saisi).
    Valeurs non vides uniquement (preserve le representant deja calcule).

    Retour Albane 2026-06-26 §S1 : en SELAS, la FORME du cessionnaire restait « SELARL »
    (valeur fixture jamais ecrasee) -> l'acte imprimait « SELARL au capital de … » et
    « representee par son gerant ». Le generateur lit `cessionnaire.forme_juridique` quand
    `ctx.structure == 'SELAS'` ; on la peuple ici a partir du `prefix` du sous-formulaire
    (selas => « SELAS », selarl => inchange, le generateur force « SELARL »). La fonction
    du representant (« president » en SELAS) est posee dans le bloc representant du form."""
    overrides: dict[str, object] = {}
    denomination = str(societe.get("denomination") or "")
    capital = str(societe.get("capital_social") or "")
    ville_rcs = str(societe.get("ville_rcs") or "")
    siege = _siege_display(societe)
    if denomination:
        overrides["denomination"] = denomination
    if capital:
        # R5 (Albane 2026-07-07) : capital du cessionnaire groupe par 3 (« 60 000 »),
        # comme l'acquereur de l'acte cabinet (format_grouped_numeric_value, L1377).
        overrides["capital_social"] = _format_montant(capital)
    if ville_rcs:
        overrides["ville_rcs"] = ville_rcs
    if siege:
        overrides["siege"] = {"adresse_affichee": siege}
    if prefix == "selas":
        # La SEL cessionnaire EST la SELAS creee : forme reelle « SELAS » (le generateur
        # n'imprime cette valeur que pour ctx.structure == 'SELAS' ; en SELARL il force
        # « SELARL » et ignore ce champ, donc le gold SELARL reste byte-identique).
        overrides["forme_juridique"] = "SELAS"
    return overrides


def _situation_display(value: str, genre: object) -> str:
    # Delegue au helper partage field_derivations.situation_display (source unique,
    # O24-11 / MINEUR 2b) pour ne jamais diverger des slices.
    return situation_display(value, genre)


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


def _scm_cedant_situation_maritale_display(
    praticien: dict[str, object], *, prefix: str
) -> str:
    """Libelle complet accentue de la situation matrimoniale du cedant SCM (O24-11).

    Le modele SCM n'a qu'UN placeholder `[situation_maritale_cedant]` (pas de placeholder
    regime separe). La valeur collapsee posee par le slice (« marie ») PERD le regime
    (separation / universelle / communaute) et n'est pas accentuee. On reconstruit ici le
    libelle complet — statut accentue/genre (_situation_display) + « sous le régime de » +
    regime accentue (_vendeur_regime_label) — sur le libelle BRUT du preset
    (st.session_state[f"{prefix}_situation_maritale"]), exactement comme l'acte cabinet.
    Sortie mariee : « marié sous le régime de séparation de biens » ; le « avec <conjoint> »
    est ajoute par le generateur (mentions_conjoint). Non marie : juste le statut accentue.
    """
    collapse = str(praticien.get("situation_maritale") or "")
    genre = praticien.get("genre")
    statut = _situation_display(collapse, genre)
    libelle_brut = str(st.session_state.get(f"{prefix}_situation_maritale") or "")
    regime = _vendeur_regime_label(libelle_brut)
    if regime:
        return f"{statut} sous le régime de {regime}"
    return statut


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

    Le wording monetaire d'un PRIX n'est PAS ratifie (contrairement a la valeur nominale) ->
    montant ENTIER = mots-nus + « euro(s) » accorde ; montant DECIMAL = FIGURE (« 2,5 ») +
    « euro », JAMAIS la phrase monetaire (double « euro » sinon). Vide -> chaine vide (saisie
    manuelle possible). Akainu M1 2026-07-06 : 3e surface prix, meme famille que SPFPL/SCM ;
    `number_words_from_value` (decimal-aware pour la valeur nominale) doublait l'unite ici.
    """
    words = prix_lettres_from_value(value)
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


def _add_months(value: date, months: int) -> date:
    """Ajoute `months` mois a une date en clampant le jour de fin de mois.

    Sert au prefill « date limite de realisation = date des actes + 6 mois »
    (FA5, Albane lot Formulaire). Le 31 mars + 1 mois -> 30 avril (jour clampe au
    dernier jour du mois cible), jamais de date invalide / de crash.
    """
    total = value.month - 1 + months
    year = value.year + total // 12
    month = total % 12 + 1
    # Dernier jour du mois cible (mois suivant - 1 jour).
    if month == 12:
        last_day = 31
    else:
        last_day = (date(year, month + 1, 1) - timedelta(days=1)).day
    return value.replace(year=year, month=month, day=min(value.day, last_day))


def _seed_default(key: str, default: object) -> None:
    if key not in st.session_state:
        st.session_state[key] = default


# Prefixe des cles de session du sous-formulaire cession, parametrable pour
# reutiliser le sous-formulaire SELARL valide sur d'autres types (SELAS...).
# Defaut « selarl » => SELARL byte-identique ; « selas » => clefs propres SELAS.
# Pose par _render_cession_form / _render_scm_cession_form au debut de chaque
# rendu (Streamlit = mono-thread par session, sans course).
_CESSION_PREFIX = "selarl"

# FA4 (Albane, Lot Formulaire) : la majoration des intérêts de retard du crédit-vendeur
# est FIXE (« il n'y a pas de variable à mettre, reprendre ce qu'il y avait dans le
# modèle »). Le modèle source médical rend « majoré de [majoration_interet_retard]
# points » avec la valeur 2 (cf. scénario SELARL `majoration_interet_retard="2"` et le
# modèle SELARL « majoré de 2 points »). Plus aucun champ de saisie.
CREDIT_VENDEUR_MAJORATION_FIXE = "2"


def _cession_text(
    container: object,
    label: str,
    *,
    section: str,
    field: str,
    default: str,
    disabled: bool = False,
) -> str:
    key = f"{_CESSION_PREFIX}_cession_{section}_{field}"
    _seed_default(key, default)
    value = copyable_text_input(container, label, key=key, disabled=disabled)
    return str(value).strip()


def _cession_civilite(
    container: object,
    label: str,
    *,
    section: str,
    field: str,
) -> str:
    """R4 (Rafael 2026-06-24) : une civilite CIVILE se choisit dans un menu deroulant
    Monsieur / Madame, jamais en texte libre. Une option vide est conservee pour les
    champs FACULTATIFS (ex. conjoint si non marie) afin de ne pas forcer une civilite
    parasite. Les champs de TITRE professionnel (« Docteur » : vendeur / cedant
    praticien) ne passent PAS par ici (fidelite gold de l'acte ; doctrine §14.2).
    Meme clef de session que `_cession_text` => compatible prefill et payloads."""
    options = ("", "Monsieur", "Madame")
    key = f"{_CESSION_PREFIX}_cession_{section}_{field}"
    _seed_default(key, "")
    if str(st.session_state.get(key) or "") not in options:
        st.session_state[key] = ""
    return str(container.selectbox(label, options, key=key)).strip()


def _cession_situation(
    container: object,
    label: str,
    *,
    section: str,
    field: str,
) -> str:
    """R3 (Rafael 2026-07-13) : la situation matrimoniale se choisit dans le MEME menu
    deroulant que le praticien principal (MATRIMONIAL_STATUS_PRESETS), jamais en texte libre.
    Meme clef de session que `_cession_text` => compatible prefill et payloads. Une valeur
    de session hors presets (ancien texte libre / prefill obsolete) retombe sur le 1er preset."""
    key = f"{_CESSION_PREFIX}_cession_{section}_{field}"
    _seed_default(key, MATRIMONIAL_STATUS_PRESETS[0])
    if str(st.session_state.get(key) or "") not in MATRIMONIAL_STATUS_PRESETS:
        st.session_state[key] = MATRIMONIAL_STATUS_PRESETS[0]
    return str(container.selectbox(label, MATRIMONIAL_STATUS_PRESETS, key=key)).strip()


def _accentuate_date_value(value: object) -> object:
    """Re-accentue les mois d'une date saisie en TEXTE libre (LIVE-03).

    Une vraie `date` (saisie via un date_input) est renvoyee TELLE QUELLE : le
    generateur la formate deja avec les mois accentues (FRENCH_MONTHS). Seules les
    saisies str (« 1er aout 2021 ») sont re-accentuees en amont. None / vide :
    renvoye intact (l'anti-trou du generateur s'en charge)."""
    if isinstance(value, str):
        return accentuate_french_months(value)
    return value


def _cession_date(
    container: object,
    label: str,
    *,
    section: str,
    field: str,
    default: str = "",
) -> str:
    """Champ date du sous-formulaire cession/bail.

    R29-06 (Rafael) : repose desormais sur le helper partage
    `date_input_with_today` -> selecteur de date (calendrier) + bouton « Aujourd'hui »
    PARTOUT, en plus du champ texte editable. On CONSERVE :
    - la cle de session `{_CESSION_PREFIX}_cession_{section}_{field}` (prefill / payloads
      intacts) ;
    - le pre-remplissage `default` (seede ici, AVANT le helper, donc non ecrase par la
      date du jour ; seed=False cote helper) ;
    - la re-accentuation des mois (« 1er aout 2021 » -> « 1er août 2021 ») AVANT injection,
      le generateur restant un echo fidele du modele.
    La saisie verbatim francaise reste possible (champ texte) ; une saisie JJ/MM/AAAA
    (calendrier / Aujourd'hui) est intacte (aucun nom de mois a accentuer). Le contrat
    de retour (chaine re-accentuee) est inchange pour tous les appelants.
    """
    key = f"{_CESSION_PREFIX}_cession_{section}_{field}"
    _seed_default(key, default)
    date_input_with_today(
        label,
        key=key,
        value=date.today(),
        container=container if container is not None else st,
        seed=False,
    )
    return accentuate_french_months(str(st.session_state.get(key) or "").strip())


def _render_cession_form(  # noqa: C901
    cession: bool,
    profession: str,
    *,
    praticien: dict[str, object],
    societe: dict[str, object],
    ordre: dict[str, object],
    generation: dict[str, object],
    prefix: str = "selarl",
    vendeur_selector: dict[str, object] | None = None,
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

    type_key = f"{_CESSION_PREFIX}_cession_meta_type_cabinet"
    _seed_default(type_key, _cession_default_type(profession))
    etape_key = f"{_CESSION_PREFIX}_cession_meta_etape"
    _seed_default(etape_key, "acte")
    # R2 (Rafael 2026-06-24) : en SELAS l'expander « Type & etape » n'offrait AUCUN choix
    # (type DERIVE de la profession #10 ; acte + compromis generes ENSEMBLE #14) -> retire.
    # Type et etape calcules silencieusement. Hors SELAS : menu conserve.
    if prefix == "selas":
        type_cabinet = _cession_default_type(profession)
        st.session_state[type_key] = type_cabinet
        etape = "acte"
        st.session_state[etape_key] = "acte"
    else:
        # MD1 (Albane 2026-07-10) : la SELARL produit DESORMAIS l'acte ET le compromis
        # ENSEMBLE (comme la SELAS depuis #14) -> l'ETAPE n'est plus un choix (elle etait
        # filtrante et faisait manquer le compromis). On force « acte » : les champs
        # specifiques a l'acte (credit-vendeur, salaries) restent conditionnes sur
        # etape=='acte', et les champs du compromis (pret, date limite) sont montres pour
        # toute cession SEL (cf. conditions ci-dessous). Le TYPE de cabinet reste choisi.
        etape = "acte"
        st.session_state[etape_key] = "acte"
        with st.expander("Type de cabinet", expanded=True):
            type_cabinet = st.selectbox(
                "Type de cabinet",
                tuple(CESSION_TYPE_LABELS),
                key=type_key,
            )

    profession_label = _profession_label(profession)
    siege_display = _siege_display(societe)

    # --- Vendeur (ticket 2.1 : associe unique par defaut, modifiable) ---
    with st.expander("Vendeur", expanded=True):
        # #11 (Rafael 2026-06-24) : le CHOIX de l'associe vendeur vit DESORMAIS DANS la
        # section Vendeur (avant : en haut du bloc cession). En SELAS multi, on selectionne
        # ICI l'associe qui cede -> ses infos sont reprises automatiquement (le derive est
        # fourni par le slice appelant). Hors SELAS : pas de selecteur (associe unique).
        if vendeur_selector is not None:
            # Le selecteur de l'associe vendeur vit ICI (section Vendeur). Il met a jour la cle
            # de session ; le slice appelant la relit au rerun pour deriver les infos du vendeur
            # (deja refletees dans `praticien` passe ci-dessus). Selectbox = geste utilisateur.
            _vsel_options = vendeur_selector["options"]
            st.selectbox(
                "Associé vendeur du cabinet",
                _vsel_options,
                index=_vsel_options.index(vendeur_selector["default"]),
                format_func=vendeur_selector["label"],
                key=f"{_CESSION_PREFIX}_cession_vendeur_index",
                help="L'associé qui cède son cabinet ; ses infos sont reprises automatiquement.",
            )
        # Locaux derives du vendeur (recalcules ICI, APRES le selecteur, pour refleter
        # l'associe choisi). LIVE-03 : la date de naissance (text_input libre) est
        # re-accentuee en amont ; reutilisee aussi pour le locataire du bail plus bas.
        praticien_prenom = str(praticien.get("prenom") or "").strip()
        praticien_nom = str(praticien.get("nom") or "").strip()
        praticien_genre = praticien.get("genre")
        praticien_adresse = _personal_address_display(praticien)
        praticien_date_naissance = _accentuate_date_value(praticien.get("date_naissance"))
        situation_label = str(st.session_state.get(f"{_CESSION_PREFIX}_situation_maritale") or "")
        conjoint_payload = {
            "civilite_affichage": str(praticien.get("conjoint_civilite") or ""),
            "prenom": str(praticien.get("conjoint_prenom") or ""),
            "nom": str(praticien.get("conjoint_nom") or ""),
        }
        if prefix == "selas":
            # R7 (Rafael 2026-06-24) : case « Le vendeur est l'associe selectionne ci-dessus »
            # retiree (le vendeur EST deja l'associe choisi au selecteur ci-dessus).
            vendeur_auto = True
        else:
            vendeur_auto = st.checkbox(
                "Le vendeur est l'associe unique",
                value=True,
                key=f"{_CESSION_PREFIX}_cession_vendeur_auto",
                help="Decocher uniquement si un autre vendeur doit etre renseigne.",
            )
        siren = _cession_text(
            st, "Numero SIREN du vendeur",
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
                "date_naissance": praticien_date_naissance,
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
            # R2 (Rafael 2026-07-13) : civilite du vendeur en MENU Madame/Monsieur (plus de texte
            # libre « Docteur » — SUPERSEDE la doctrine §14.2). Le genre est DERIVE de la civilite
            # choisie -> accord genre de l'acte (« né/née », « inscrit(e) », etc.) pour un vendeur
            # distinct du fondateur (comble aussi l'ancien trou « genre None »).
            civilite = _cession_civilite(
                col_a, "Civilité", section="vendeur", field="civilite",
            )
            genre_vendeur = derive_gender_from_civilite(civilite)
            prenom = _cession_text(col_b, "Prenom", section="vendeur", field="prenom", default="")
            nom = _cession_text(col_c, "Nom", section="vendeur", field="nom", default="")
            col_d, col_e, col_f = st.columns(3)
            date_naissance = _cession_date(
                col_d, "Date de naissance (JJ/MM/AAAA)",
                section="vendeur", field="date_naissance",
            )
            ville_naissance = _cession_text(
                col_e, "Ville de naissance", section="vendeur", field="ville_naissance",
                default="",
            )
            departement_naissance = _cession_text(
                col_f, "Departement de naissance (ou pays si étranger)",
                section="vendeur", field="departement_naissance", default="",
            )
            col_g, col_h = st.columns(2)
            nationalite = _cession_text(
                col_g, "Nationalite", section="vendeur", field="nationalite",
                default="française",
            )
            # R3 (Rafael 2026-07-13) : situation matrimoniale au MEME menu deroulant que le
            # praticien principal (MATRIMONIAL_STATUS_PRESETS) ; la valeur affichee dans l'acte
            # est le statut accorde au genre (« marié »/« célibataire »).
            situation_label = _cession_situation(
                col_h, "Situation matrimoniale", section="vendeur", field="situation",
            )
            situation_value = matrimonial_status_value(situation_label)
            situation_vendeur = _situation_display(situation_value, genre_vendeur)
            is_married_or_pacse = situation_value in ("marie", "pacse")
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
            # R3 : l'identite du conjoint n'est demandee QUE quand la situation s'y prete
            # (marie ou pacse) — sinon les champs conjoint ne s'affichent pas.
            conjoint_civilite = ""
            conjoint_prenom = ""
            conjoint_nom = ""
            if is_married_or_pacse:
                col_k, col_m, col_n = st.columns(3)
                conjoint_civilite = _cession_civilite(
                    col_k, "Civilité du conjoint",
                    section="vendeur", field="conjoint_civilite",
                )
                conjoint_prenom = _cession_text(
                    col_m, "Prénom du conjoint", section="vendeur", field="conjoint_prenom",
                    default="",
                )
                conjoint_nom = _cession_text(
                    col_n, "Nom du conjoint", section="vendeur", field="conjoint_nom", default="",
                )
            vendeur_payload = {
                "civilite_affichage": civilite,
                "genre": genre_vendeur,
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
                "regime_matrimonial": _vendeur_regime_label(situation_label),
                "conjoint": {
                    "civilite_affichage": conjoint_civilite,
                    "prenom": conjoint_prenom,
                    "nom": conjoint_nom,
                },
            }
        # FB1 (Albane, Lot Formulaire) : « né le ... à Lyon (France) » — la mention entre
        # parenthèses après la ville de naissance doit être le DÉPARTEMENT (« 75 »), pas
        # « France ». L'ACTE médical/dentaire utilise le token [departement_naissance_vendeur]
        # (déjà correct, « 69 »), mais le COMPROMIS médical rend
        # « [ville_naissance_vendeur] ([pays_naissance_vendeur]) » : c'est le token PAYS qui
        # s'affiche dans la parenthèse, d'où le « (France) ». On câble donc le DÉPARTEMENT
        # saisi dans `pays_naissance` (fallback « France » si aucun département connu) ->
        # le compromis affiche le département comme l'acte. Le token pays ne sert qu'à cette
        # parenthèse de lieu de naissance (la nationalité a son propre token), donc aucun
        # autre rendu n'est touché. S'applique SELARL et SELAS (même intention partout).
        _departement_naissance = str(
            vendeur_payload.get("departement_naissance") or ""
        ).strip()
        vendeur_payload.update(
            {
                "cp_naissance": "",
                "pays_naissance": _departement_naissance or "France",
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
                col_a, "Numero RCS (des immatriculation)",
                section="acquereur", field="numero_rcs", default="",
            )
            numero_siret = _cession_text(
                col_b, "Numero SIRET",
                section="acquereur", field="numero_siret", default="",
            )
            if type_cabinet == "medical" and etape == "acte":
                col_c, col_d = st.columns(2)
                date_immatriculation = _cession_date(
                    col_c, "Date d'immatriculation (JJ/MM/AAAA)",
                    section="acquereur", field="date_immatriculation",
                )
                date_inscription_ordre = _cession_date(
                    col_d, "Date d'inscription a l'ordre (JJ/MM/AAAA)",
                    section="acquereur", field="date_inscription_ordre",
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
            # KAN-23 (Rafael 2026-07-15) : « gérant » n'est JAMAIS féminisé, même pour une
            # femme -> forme masculine invariable (cf. `_FONCTION_INVARIANTES_MF`).
            "fonction": "gérant",
        },
    }

    # --- Cabinet (ticket 2.3 : cadre reduit aux seules infos specifiques) ---
    with st.expander("Cabinet"):
        st.caption(f"Nature du fonds libéral : {profession_label} (dérivée de la profession).")
        cab_key = f"{_CESSION_PREFIX}_cession_cabinet_adresse"
        # O24-12 (onglet 24) : « adresse du cabinet -> ajouter une case "meme adresse que
        # le lieu d'exercice" et reporter les donnees si cochee ». En SELAS, le lieu
        # d'exercice (saisi en UNE ligne, O24-03) est reporte dans l'adresse du cabinet
        # quand la case est cochee. Hors SELAS : pre-remplissage siege inchange.
        lieu_exercice = str(societe.get("lieu_exercice") or "")
        # O24-12 : la case existe dès que le bloc Cabinet est rendu en SELAS (verbatim
        # « ajouter une case », inconditionnel) ; elle ne reporte que si le lieu d'exercice
        # est renseigné (sinon rien à recopier). Le report est RÉVERSIBLE (re-Akainu
        # 2026-06-23, MAJEUR O24-12 : décocher doit défaire le report, sinon l'adresse
        # reste polluée par le lieu d'exercice). On mémorise l'état précédent de la case ET
        # la valeur du cabinet AVANT report : à la transition décoché→coché on sauvegarde la
        # saisie courante, à coché→décoché on la RESTAURE (re-Akainu tour 2, MINEUR O24-12 :
        # une adresse saisie manuellement ne doit pas être écrasée par le siège à la décoche).
        # O24-12 (re-Akainu tour 4, RE-SCOPE règle 12 — 3e perte de saisie sur l'ancien design).
        # Design propre : la SAISIE MANUELLE vit dans `manual_key` (jamais écrasée par le report)
        # et le champ visible (cab_key) est piloté par l'état de la case :
        #  - cochée + lieu d'exercice renseigné -> MIROIR du lieu, champ DÉSACTIVÉ ;
        #  - sinon (décochée, OU cochée mais lieu vide) -> ÉDITABLE, valeur = saisie manuelle.
        # À la transition coché→décoché on restaure `manual_key` (siège à défaut). En mode
        # éditable on resynchronise `manual_key` APRÈS le widget -> la saisie survit à tout
        # cycle coche/décoche.
        cabinet_locked = False
        if prefix == "selas":
            prev_key = f"{_CESSION_PREFIX}_cabinet_meme_lieu_exercice_prev"
            manual_key = f"{_CESSION_PREFIX}_cabinet_adresse_manuelle"
            was_checked = bool(st.session_state.get(prev_key))
            checked = st.checkbox(
                "Adresse du cabinet = même adresse que le lieu d'exercice",
                key=f"{_CESSION_PREFIX}_cabinet_meme_lieu_exercice",
                help="Coché : reporte l'adresse du lieu d'exercice dans l'adresse du cabinet.",
            )
            if checked and lieu_exercice:
                st.session_state[cab_key] = lieu_exercice  # miroir non éditable
                cabinet_locked = True
            elif was_checked and not checked:
                # Coché → décoché : restaurer la dernière saisie manuelle (siège à défaut).
                st.session_state[cab_key] = st.session_state.get(manual_key) or siege_display
            st.session_state[prev_key] = checked
        elif not st.session_state.get(cab_key) and siege_display:
            st.session_state[cab_key] = siege_display
        adresse_cabinet = _cession_text(
            st, "Adresse du cabinet", section="cabinet", field="adresse",
            default=siege_display, disabled=cabinet_locked,
        )
        if prefix == "selas" and not cabinet_locked:
            # En mode éditable, la valeur courante du champ EST la saisie manuelle ->
            # on la mémorise pour qu'elle survive à un futur report (coche).
            st.session_state[manual_key] = adresse_cabinet
        telephone_cabinet = _cession_text(
            st, "Telephone du cabinet", section="cabinet", field="telephone",
            default="",
        )
        st.markdown("Origine de propriete du vendeur")
        # O1 (Albane 2026-07-10) : le cabinet peut avoir ete CREE (pas seulement acquis).
        # Choix « cree / acquis » pour TOUS les types (medical ET dentaire) — le generateur
        # d'acte (medical comme dentaire) rend la clause adaptee via `origine_propriete_mode` :
        #   - "cree"   -> « ... proprietaire ... pour les avoir regulierement crees le <date> »
        #                 (seule la date de creation se saisit) ;
        #   - "achete" -> « ... acquis aupres de <precedent>, le <date> au prix de <prix> »
        #                 (date + precedent proprietaire + prix).
        # Auparavant le dentaire etait FORCE en "achete" ; le modele dentaire supporte la
        # variante "cree" (verifie : clause « crees le <date> » rendue), donc le choix est
        # ouvert aux deux professions. Cle de contexte consommee par l'acte :
        # `cession.cabinet.origine_propriete_mode`.
        mode_key = f"{_CESSION_PREFIX}_cession_cabinet_origine_mode"
        _seed_default(mode_key, "Cabinet créé par le vendeur")
        mode_label = st.selectbox(
            "Le vendeur a...",
            ("Cabinet créé par le vendeur", "Cabinet acheté par le vendeur"),
            key=mode_key,
        )
        # R4 (Rafael 2026-07-13) : options accentuees (« créé »/« acheté ») -> le mapping teste
        # « acheté » (l'ancien « achete » sans accent ne matchait plus la nouvelle option).
        origine_mode = "achete" if "acheté" in mode_label else "cree"
        # Le libelle de la date suit le mode : « creation » (cree) vs « acquisition » (achete).
        date_origine_label = (
            "Date d'acquisition du cabinet par le vendeur (JJ/MM/AAAA)"
            if origine_mode == "achete"
            else "Date de creation du cabinet par le vendeur (JJ/MM/AAAA)"
        )
        date_origine = _cession_date(
            st, date_origine_label,
            section="cabinet", field="origine_date",
        )
        precedent_payload: dict[str, str] | None = None
        prix_origine = ""
        if origine_mode == "achete":
            col_a, col_b, col_c = st.columns(3)
            precedent_payload = {
                # R2 (Rafael 2026-07-13) : civilite du precedent proprietaire en menu.
                "civilite_affichage": _cession_civilite(
                    col_a, "Civilité du précédent propriétaire",
                    section="cabinet", field="precedent_civilite",
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
                    st, "Prix d'origine de propriete",
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
        date_bail = _cession_date(
            col_a, "Date du bail (JJ/MM/AAAA)",
            section="bail", field="date_bail",
        )
        date_effet = _cession_date(
            col_b, "Date d'effet du bail / d'entrée dans les locaux (JJ/MM/AAAA)",
            section="bail", field="date_effet",
        )
        col_c, col_d = st.columns(2)
        duree_bail = _cession_text(
            col_c, "Duree du bail", section="bail", field="duree", default="six années",
        )
        loyer = _format_montant(
            _cession_text(
                col_d, "Loyer mensuel", section="bail", field="loyer",
                default="",
            )
        )
        descriptif_key = f"{_CESSION_PREFIX}_cession_bail_descriptif"
        _seed_default(descriptif_key, "")
        descriptif_local = str(
            st.text_area(
                "Descriptif libre du local",
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
            # #13 (onglet 24) + R9 (Rafael 2026-06-24) : plus aucune mention « (facultatif) »
            # nulle part -> pas de suffixe sur les labels CA / resultat.
            opt = ""
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
        # O2 (Albane 2026-07-10) : si le PRIX TOTAL et les ELEMENTS INCORPORELS sont saisis,
        # les ELEMENTS CORPORELS sont derives par defaut = total - incorporels (modifiable).
        # On rend d'abord l'incorporel (col_d), puis on preseed le corporel (col_c) tant qu'il
        # est vide -> la saisie manuelle du corporel prime toujours (seed uniquement si vide).
        prix_incorporels = _format_montant(
            _cession_text(
                col_d, "Elements incorporels",
                section="prix", field="incorporels", default="",
            )
        )
        _total_dec = _decimal_from_value(prix_total)
        _incorp_dec = _decimal_from_value(prix_incorporels)
        corporels_key = f"{_CESSION_PREFIX}_cession_prix_corporels"
        if (
            _total_dec is not None
            and _incorp_dec is not None
            and not str(st.session_state.get(corporels_key) or "").strip()
        ):
            st.session_state[corporels_key] = format_grouped_numeric_value(
                _total_dec - _incorp_dec
            )
        if _total_dec is not None and _incorp_dec is not None:
            col_c.caption(
                f"Automatique : {format_grouped_numeric_value(_total_dec - _incorp_dec)} "
                "(= total - incorporels)"
            )
        prix_corporels = _format_montant(
            _cession_text(
                col_c, "Elements corporels",
                section="prix", field="corporels", default="",
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
        # FB-2 (Albane 2026-06-26) : « en cas de cession sur la partie financement le
        # destinataire n'est pas utile (appel de fonds = doc qu'on complète nous), il faut
        # que seul le nom de la société et les éléments comme le nom du client soient
        # préremplis ». -> on RETIRE la saisie du destinataire de l'appel de fonds. Le
        # générateur appel_fond_sel traite déjà `financement.destinataire` comme OPTIONNEL
        # (destinataire absent -> ligne « À l'attention de » omise), donc ne plus alimenter
        # ce champ ne casse pas la génération. Société (acquéreur) + client (vendeur) restent
        # préremplis par ailleurs.
        montant_deblocage = _format_montant(
            _cession_text(
                st, "Montant deblocage minimum",
                section="financement", field="deblocage", default="",
            )
        )
        pret_payload: dict[str, str] = {"montant": "", "taux": "", "duree": ""}
        # O24-14 : en SELAS le compromis est produit en plus de l'acte -> on expose ses
        # champs propres (prêt) même si l'étape affichée est 'acte'. MD1 (Albane 2026-07-10) :
        # la SELARL produit aussi l'acte + le compromis -> mêmes champs prêt exposés (prefix
        # 'selarl'). Toute cession SEL affiche donc le prêt du compromis.
        if etape == "compromis" or prefix in ("selas", "selarl"):
            # Lot Formulaire (Albane) — préremplissages déterministes du prêt :
            #  FA1 « montant du prêt (compromis) = prix de cession » -> défaut = prix total
            #       saisi plus haut (auto, modifiable). On (re)seede tant que l'utilisateur
            #       n'a pas saisi de montant propre : le champ SUIT le prix de cession.
            #  FA2 « taux du prêt : toujours mettre 5,5 % » -> défaut 5,5 %.
            #  FA3 « durée du prêt : toujours mettre 10 ans » -> défaut 10 ans.
            # Tous restent éditables (_cession_text). Le prix vient du bloc Prix rendu
            # juste au-dessus (prix_total), donc disponible ici.
            montant_key = f"{_CESSION_PREFIX}_cession_financement_pret_montant"
            if not str(st.session_state.get(montant_key) or "").strip() and prix_total:
                st.session_state[montant_key] = prix_total
            col_d, col_e, col_f = st.columns(3)
            pret_payload = {
                "montant": _format_montant(
                    _cession_text(
                        col_d, "Montant du pret (compromis)",
                        section="financement", field="pret_montant",
                        default=prix_total,
                    )
                ),
                "taux": _cession_text(
                    col_e, "Taux du pret",
                    section="financement", field="pret_taux", default="5,5 %",
                ),
                "duree": _cession_text(
                    col_f, "Duree du pret",
                    section="financement", field="pret_duree", default="10 ans",
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
                col_g, col_h, col_i = st.columns(3)
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
                    # FA4 (Albane, Lot Formulaire) : « majoration intérêts de retard :
                    # c'est fixe, il n'y a pas de variable à mettre, reprendre ce qu'il y
                    # avait dans le modèle ». On RETIRE la saisie : la valeur du MODÈLE
                    # SOURCE médical (« majoré de 2 points », cf. scénario SELARL
                    # majoration_interet_retard="2") est figée ici. Aligne SELARL/SELAS
                    # (même modèle, même valeur).
                    "majoration_interet_retard": CREDIT_VENDEUR_MAJORATION_FIXE,
                }
            scm_actif_key = f"{_CESSION_PREFIX}_cession_scm_clause_actif"
            _seed_default(scm_actif_key, False)
            scm_actif = st.checkbox(
                "Cession de parts de SCM associee (clause de l'acte medical)",
                key=scm_actif_key,
            )
            if scm_actif:
                col_scm_a, col_scm_b = st.columns(2)
                scm_payload = {
                    "actif": True,
                    "nb_parts_a_ceder": _cession_text(
                        col_scm_a, "Nombre de parts SCM a ceder",
                        section="financement", field="scm_parts", default="",
                    ),
                    # FB-1 (CE8, Albane 2026-06-26) : le point 8 de l'acte médical cède
                    # « l'intégralité des parts qu'il détient de la SCM <dénomination> ». Le
                    # champ `CessionScm.denomination` existait déjà côté moteur mais n'était
                    # PAS saisi -> l'acte affichait un marqueur à compléter. On expose la
                    # saisie ici (vide -> le générateur retombe sur sa zone à compléter,
                    # jamais bloquant).
                    "denomination": (
                        _cession_text(
                            col_scm_b, "Denomination de la SCM",
                            section="financement", field="scm_denomination", default="",
                        )
                        or None
                    ),
                }
        financement_payload = {
            # §12.1 : banque non saisie -> vide. Le generateur d'appel de fonds
            # omet la ligne banque quand le nom est vide (pas de placeholder
            # parasite) ; la mention se complete a la main sur le document.
            "banque": {"nom": "", "adresse_affichee": ""},
            # FB-2 : plus de destinataire saisi (clé omise -> generateur omet la ligne).
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
                            "civilite_affichage": _cession_civilite(
                                col_a, f"Civilite salarie {index + 1}",
                                section="salarie", field=f"{index}_civilite",
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
                                col_d, f"Poste salarie {index + 1}",
                                section="salarie", field=f"{index}_poste", default="",
                            )
                            or None,
                        }
                    )

    date_limite_realisation = ""
    # O24-14 : compromis produit aussi en SELAS ; MD1 (Albane 2026-07-10) : idem SELARL
    # (acte + compromis) -> la date limite de realisation du compromis est exposee pour
    # toute cession SEL.
    if etape == "compromis" or prefix in ("selas", "selarl"):
        # FA5 (Albane, Lot Formulaire) : « date limite de la réalisation : par défaut à
        # +6 mois de la date des actes ». On préremplit la date limite = date de
        # signature (date des actes, `generation["signature_date"]`) + 6 mois, tant que
        # l'utilisateur n'a pas saisi sa propre valeur. Modifiable.
        # FB3 (même retour) : le bug « 01/01//2027 » (double barre) venait d'un format
        # douteux ; on formate ici la date dérivée via `format_french_date` (« %d/%m/%Y »
        # propre, jamais de double slash). La saisie reste libre (JJ/MM/AAAA).
        date_limite_key = f"{_CESSION_PREFIX}_cession_meta_date_limite"
        if not str(st.session_state.get(date_limite_key) or "").strip():
            _date_actes = generation.get("signature_date")
            if isinstance(_date_actes, date):
                st.session_state[date_limite_key] = format_french_date(
                    _add_months(_date_actes, 6)
                )
        date_limite_realisation = _cession_date(
            st, "Date limite de signature de l'acte définitif (JJ/MM/AAAA)",
            section="meta", field="date_limite",
        )

    # --- Avenant de bail (DOC-007) : bailleur a renseigner, locataire derive ---
    with st.expander("Avenant de bail — bailleur"):
        st.caption(
            # O24-11 : en SELAS multi-associes, « l'associe unique » est faux -> locataire =
            # l'associe selectionne (vendeur). Hors SELAS : wording historique inchange.
            "Le locataire actuel est l'associé sélectionné ci-dessus ; le nouveau locataire "
            "est la société en cours de création. Champs vides : omis de l'avenant."
            if prefix == "selas"
            else "Le locataire actuel est l'associe unique ; le nouveau locataire est la "
            "societe en cours de creation. Champs vides : omis de l'avenant."
        )
        col_a, col_b, col_c = st.columns(3)
        bailleur_civilite = _cession_civilite(
            col_a, "Civilite du bailleur", section="bailleur", field="civilite",
        )
        bailleur_prenom = _cession_text(
            col_b, "Prenom du bailleur", section="bailleur", field="prenom", default="",
        )
        bailleur_nom = _cession_text(
            col_c, "Nom du bailleur", section="bailleur", field="nom", default="",
        )
        bailleur_adresse = _cession_text(
            st, "Adresse du bailleur", section="bailleur", field="adresse",
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
                # R3 (Rafael 2026-07-09) : genre pour accorder la civilite civile si un titre
                # professionnel etait saisi (« Docteur » -> Monsieur/Madame).
                "genre": derive_gender_from_civilite(bailleur_civilite),
                "prenom": bailleur_prenom,
                "nom": bailleur_nom,
                "profession": "",
                "adresse_affichee": bailleur_adresse,
            },
            "locataire": {
                "civilite_affichage": DEFAULT_TITRE_AFFICHAGE,
                "civilite_courte": DEFAULT_TITRE_AFFICHAGE,
                # R3 (Rafael 2026-07-09) : le titre par defaut « Docteur » est rendu en civilite
                # civile (Monsieur/Madame) accordee au genre du praticien locataire.
                "genre": praticien_genre,
                "prenom": praticien_prenom,
                "nom": praticien_nom,
                "profession": profession_label,
                "date_naissance": praticien_date_naissance,
                "ville_naissance": str(praticien.get("ville_naissance") or ""),
                "nationalite": str(praticien.get("nationalite") or ""),
                "adresse_affichee": praticien_adresse,
            },
        }
    )
    return cession_context, bail_context


def _render_scm_cession_form(  # noqa: C901
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
    # F1 (Albane 2026-07-10) : le flux SCM ne PRE-REMPLIT plus les champs SAISIS avec les
    # donnees d'EXEMPLE de la fixture (« SCM CABINET CENTRAL », « 3 000 », « 300 », siege /
    # RCS / prix / parts cedees inventes) -> ils demarrent VIDES. On conserve seulement les
    # seeds qui ont du sens : forme juridique (constante SCM), et les champs back-office NON
    # exposes requis par les generateurs (agrement, enregistrement, signataire SDE) — ces
    # derniers portent encore des valeurs d'exemple (cf. SIGNAL : a exposer / rendre optionnels
    # cote generateur). Les champs saisis vides sont bloques par validate_selarl_input (message
    # clair au lieu d'un crash generateur).

    scm_cedee = payload.setdefault("scm_cedee", {}) or {}
    with st.expander("SCM cedee", expanded=True):
        scm_cedee["denomination"] = _cession_text(
            st, "Denomination SCM", section="scm_cedee", field="denomination",
            default="",
        )
        # FB-6 (Albane 2026-06-26) : « l'adresse du siege dans le PV doit provenir d'un
        # champ saisi (ou par defaut le siege de la SEL), pas d'une valeur fixe ». FB-8a :
        # « l'adresse [de l'expose de l'acte] souvent c'est la meme que le siege de la SEL
        # -> proposee par defaut ou en cochant une case ». -> on saisit le siege de la SCM,
        # avec une case « = siege de la SEL » qui le prerempli depuis le siege de la societe.
        # Ce champ alimente scm_cedee.siege (lu par le PV pour tous, et par l'expose de
        # l'acte en SELAS ; en SELARL l'expose lit deja cessionnaire.siege = siege SEL).
        siege_sel = (
            str(st.session_state.get(f"{prefix}_siege") or "").strip()
            or _siege_display(societe)
        )
        # F1 : plus de pre-remplissage du siege SCM avec la valeur d'exemple de la fixture
        # (« 12 rue des Soins, 75008 Paris ») -> champ vide (ou report du siege SEL si la
        # case ci-dessous est cochee).
        siege_scm_existant = ""
        siege_same_key = f"{_CESSION_PREFIX}_cession_scm_cedee_siege_same_as_sel"
        _seed_default(siege_same_key, False)
        siege_same = st.checkbox(
            "Siege de la SCM = siege de la SEL",
            key=siege_same_key,
            help="Coche : prerempli l'adresse du siege de la SCM avec celle de la SEL.",
        )
        siege_text_key = f"{_CESSION_PREFIX}_cession_scm_cedee_siege"
        if siege_same and siege_sel:
            st.session_state[siege_text_key] = siege_sel
        scm_cedee_siege_saisi = _cession_text(
            st, "Siege de la SCM (adresse affichee)",
            section="scm_cedee", field="siege",
            default=siege_scm_existant,
        )
        # F1 : siege VIDE -> on efface la valeur d'exemple de la fixture (sinon elle survivait
        # dans le payload et fuyait dans le PV / l'acte).
        if scm_cedee_siege_saisi:
            scm_cedee["siege"] = {"adresse_affichee": scm_cedee_siege_saisi}
        else:
            scm_cedee["siege"] = None
        col_a, col_b = st.columns(2)
        scm_cedee["ville_rcs"] = _cession_text(
            col_a, "RCS (ville)", section="scm_cedee", field="rcs_ville",
            default="",
        )
        scm_cedee["numero_rcs"] = _cession_text(
            col_b, "Numero RCS", section="scm_cedee", field="numero_rcs",
            default="",
        )
        # §4.1 — capital / parts / nominal / plage pilotables. F1 : plus de pre-remplissage
        # avec les valeurs d'exemple (capital 3 000, 300 parts) -> champs vides.
        col_c, col_d = st.columns(2)
        # R5 (Albane 2026-07-07) : capital de la SCM cedee groupe par 3 (« 3 000 »).
        scm_cedee["capital_social"] = _format_montant(_cession_text(
            col_c, "Capital social SCM", section="scm_cedee", field="capital_social",
            default="",
        ))
        nb_parts_saisi = _cession_text(
            col_d, "Nombre total de parts", section="scm_cedee", field="nb_parts_total",
            default="",
        )
        # nb_parts_total est un entier cote modele. F1 : saisie vide -> 0 (on n'herite plus
        # de la valeur d'exemple de la fixture ; le blocage validate_selarl_input demande la
        # saisie avant generation).
        scm_cedee["nb_parts_total"] = int(nb_parts_saisi) if nb_parts_saisi.isdigit() else 0
        col_e, col_f = st.columns(2)
        # O24-05 (re-Akainu 2026-06-23) : valeur nominale « calculee automatiquement ET
        # affichee » s'applique a TOUS les types — y compris la SCM cedee, qui porte son
        # propre capital + nb de parts. Champ desactive (auto-calc capital / nb parts),
        # plus de saisie libre, comme les 6 types principaux.
        scm_cedee["valeur_nominale_part"] = calculate_nominal_value(
            scm_cedee.get("capital_social"), scm_cedee.get("nb_parts_total")
        )
        # Label DISTINCT de la valeur nominale de la societe (sinon DuplicateWidgetID :
        # deux text_input desactifs sans cle au meme libelle -> meme ID auto).
        copyable_text_input(col_e,
            "Valeur nominale d'une part de SCM (calculee)",
            value=scm_cedee["valeur_nominale_part"],
            disabled=True,
        )
        # N4 (Rafael 2026-06-24) : la plage TOTALE des parts est auto-calculee (« 1 a N »),
        # plus de saisie manuelle (champ desactive, comme la valeur nominale calculee).
        _nb_scm = scm_cedee.get("nb_parts_total")
        scm_cedee["plage_parts_total"] = f"1 à {_nb_scm}" if _nb_scm else ""  # N4 : « à »
        copyable_text_input(
            col_f, "Plage totale des parts (calculee)",
            value=scm_cedee["plage_parts_total"],
            disabled=True,
        )
    payload["scm_cedee"] = scm_cedee

    cedant = payload.setdefault("cedant", {}) or {}
    with st.expander("Cedant"):
        # O24-11 (re-Akainu tour 3, MINEUR) : en SELAS multi-associes le cedant est le vendeur
        # SELECTIONNE parmi plusieurs associes — « l'associe unique » y est FAUX (comme la
        # legende bail, deja conditionnee sur le prefixe). + accents corriges.
        if prefix == "selas":
            st.caption("Préremplie avec l'associé sélectionné ci-dessus ; modifiable si besoin.")
        else:
            st.caption("Préremplie avec l'associé unique ; modifiable si besoin.")
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
        # R2 (Rafael 2026-07-13) : civilite du cedant SCM en MENU Madame/Monsieur (comme le
        # vendeur de cession et le precedent proprietaire). Le seed vivant depuis la fiche
        # praticien pose deja « Monsieur »/« Madame » (option valide). Le genre du cedant est
        # derive de cette civilite dans l'acte SCM (_cedant_genre).
        cedant["civilite_affichage"] = _cession_civilite(
            col_a, "Civilité", section="scm_cedant", field="civilite",
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
    # O24-11 : injecter le LIBELLE COMPLET ACCENTUE de la situation matrimoniale
    # (statut accentue/genre + « sous le régime de » + regime) — le modele SCM n'a
    # qu'un placeholder unique et la valeur collapsee posee plus haut perdait le
    # regime + l'accent. Ecrase la valeur collapsee de _scm_cedant_overrides ; pour
    # un non-marie, rend juste le statut accentue (donc jamais de cle videe).
    situation_complete = _scm_cedant_situation_maritale_display(praticien, prefix=prefix)
    if situation_complete:
        cedant["situation_maritale"] = situation_complete
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
    # Albane 2026-06-26 §S1 : en SELAS, le dirigeant de la SEL cessionnaire est un
    # « president » (pas un « gerant »). Le generateur lit representant.fonction quand
    # ctx.structure == 'SELAS' ; en SELARL il force « gerant » et ignore ce champ, donc
    # le gold SELARL reste byte-identique. Pose ici, a la source du contexte.
    if prefix == "selas":
        representant["fonction"] = "président"
    cessionnaire["representant"] = representant
    # §13.3 : la description de la SEL cessionnaire = la societe creee
    # (denomination / capital / siege / RCS), pas les valeurs de la fixture.
    # Albane §S1 : `prefix` propage la forme reelle (SELAS) pour ecraser la forme
    # fixture (SELARL) du cessionnaire dans le rendu SELAS.
    cessionnaire.update(_scm_cessionnaire_overrides(societe, prefix=prefix))
    payload["cessionnaire"] = cessionnaire

    parts_cedees = payload.setdefault("parts_cedees", {}) or {}
    prix = payload.setdefault("prix", {}) or {}
    with st.expander("Parts cedees & prix"):
        col_a, col_b, col_c = st.columns(3)
        # F1 : plus de pre-remplissage du nb de parts cedees avec la valeur d'exemple.
        nb_cedees_saisi = _cession_text(
            col_a, "Nombre de parts cedees", section="scm_parts", field="nb",
            default="",
        )
        parts_cedees["nb"] = int(nb_cedees_saisi) if nb_cedees_saisi.isdigit() else 0
        # FB-4 (Albane 2026-06-26) : « pour les plages cédées est-ce qu'on peut prendre la
        # main ? en pratique le mec détient 10 parts numérotées de 1 à 5 et 21 à 25 ». -> on
        # rouvre une SAISIE MANUELLE OPTIONNELLE de la plage cédée. Renseignée -> elle OVERRIDE
        # la dérivation automatique (les parts détenues peuvent être NON contiguës, ex.
        # « 1 a 5 et 21 a 25 ») ; laissée VIDE -> la dérivation déterministe actuelle (dernières
        # parts du cedant, _derive_scm_apres_cession) reste en place. On efface d'abord la plage
        # héritée de la fixture (Albane §S4 : sinon « 151 a 200 » restait collée et incohérente
        # avec un nb saisi différent), puis on ne repose que la saisie manuelle si fournie.
        parts_cedees.pop("plage", None)
        plage_cedee_manuelle = _cession_text(
            col_b, "Plage des parts cedees (laisser vide = calcul auto)",
            section="scm_parts", field="plage", default="",
        )
        if plage_cedee_manuelle:
            parts_cedees["plage"] = plage_cedee_manuelle
        else:
            col_b.caption(
                "Plage des parts cedees : calculee automatiquement (dernieres parts du cedant)."
            )
        # R5 (Albane 2026-07-07) : prix global groupe par 3 (« 20 000 »), comme les
        # autres montants de cession (_format_montant partout).
        # F1 : plus de pre-remplissage du prix global avec la valeur d'exemple (« 5 000 »).
        prix["global"] = _format_montant(_cession_text(
            col_c, "Prix global", section="scm_prix", field="global",
            default="",
        ))
        # FA7 (Albane, Lot Formulaire) : « SCM / prix : en mettant le prix global est-ce
        # qu'il peut se mettre d'office en lettre ? » -> le prix global en lettres est
        # DÉRIVÉ AUTOMATIQUEMENT du prix global saisi (même helper number_words_from_value
        # que la valeur nominale calculée), affiché en champ désactivé. Repli sur la valeur
        # de base si le prix n'est pas un montant exploitable (jamais de clé requise vidée).
        # F1 : lettres DERIVEES du prix global saisi ; vide si le prix est vide (plus de
        # repli sur la valeur d'exemple de la fixture « cinq mille »).
        prix["global_lettres"] = prix_lettres_from_value(prix.get("global"))
        copyable_text_input(
            st, "Prix global en lettres (automatique)",
            value=prix["global_lettres"],
            disabled=True,
        )
    # Albane 2026-06-26 §S2 : le prix UNITAIRE par part doit etre RECALCULE = prix global /
    # nombre de parts cedees (chiffre + lettres), au lieu de rester fige a la valeur fixture
    # (« cent (100) »). Ex. 20 EUR pour 20 parts -> « un (1) euro » par part. Derivation
    # deterministe in-place ; non divisible -> figure decimale francaise (jamais de crash).
    _derive_scm_prix_unitaire(prix, parts_cedees.get("nb"))
    payload["parts_cedees"] = parts_cedees
    payload["prix"] = prix

    # §4.1 — repeater des associes PRESENTS (plus de fixture 3 presents / 4 apres).
    # L'apres-cession est DERIVE deterministe (cedant reduit + SEL cessionnaire
    # entrante), jamais saisi. signataires_pv en derive aussi.
    presents = _render_scm_cession_associes_presents(scm_cedee, cedant=cedant)
    payload["associes_presents"] = [a.model_dump() for a in presents]
    payload["associes_avant_cession"] = [a.model_dump() for a in presents]
    apres = _derive_scm_apres_cession(presents, cedant, cessionnaire, parts_cedees)
    payload["associes_apres_cession"] = [a.model_dump() for a in apres]
    payload["signataires_pv"] = _derive_scm_signataires_pv(presents)

    # Albane 2026-06-26 §S3 : le nombre d'exemplaires de l'acte de cession de parts SCM est
    # « quatre » (la fixture portait « trois »). Valeur fixe de l'acte, posee a la source du
    # contexte (le courrier SDE porte deja « 4 exemplaires » par ailleurs).
    payload["nombre_exemplaires_lettres"] = "quatre"

    return ScmCessionContext.model_validate(payload)


def _scm_present_label(associe: ScmCessionAssocie) -> str:
    """Libelle d'affichage TOLERANT d'un associe present (FB-7/FB-8b).

    Contrairement a `associe_display` du generateur (strict, leve si un champ manque),
    ce helper front ne crashe jamais sur une saisie partielle : il assemble ce qui est
    disponible et renvoie chaine vide si rien n'est saisi (le selecteur retombe alors sur
    un libelle « Associe N » ; la case gerant vide n'ajoute pas de cogerant fantome)."""
    if associe.type_personne == "personne_morale":
        return (associe.denomination or "").strip()
    parts = [associe.civilite_affichage, associe.prenom, associe.nom]
    return " ".join(p.strip() for p in parts if p and p.strip())


def _render_scm_cession_associes_presents(  # noqa: C901
    scm_cedee: dict[str, object],
    *,
    cedant: dict[str, object] | None = None,
) -> list[ScmCessionAssocie]:
    """Repeater des associes PRESENTS a l'AGE de cession SCM (§4.1).

    N associes (identite + nb de parts). Le total des parts doit egaler le capital
    de la SCM (nb_parts_total) ; un avertissement non bloquant le signale sinon.

    FB-5 (Albane 2026-06-26) : « les plages de parts pour les associes presents je
    pense qu'il n'est pas necessaire de le mettre car ce n'est reporte nulle part
    et cela risque de creer des erreurs ; et dans les associes par defaut le
    premier peut etre le cedant ». -> on RETIRE la saisie/affichage de la plage des
    presents ; on garde le nb. La plage des presents n'est consommee par AUCUN
    generateur (le PV ne lit que parts.nb ; l'apres-cession DERIVE sa propre plage),
    on la calcule donc cumulativement EN INTERNE (pour la seule derivation
    apres-cession du cedant) sans jamais l'afficher. Le 1er present est preremplie
    avec le cedant.

    FB-7 (Albane 2026-06-26) : « le cedant preside par defaut ». Le generateur PV
    prend `associes_presents[-1]` comme president de seance. Pour faire presider le
    cedant, on REORDONNE la liste afin que le president selectionne (defaut = cedant)
    figure en DERNIERE position (l'ordre interne des autres est preserve).

    FB-8b (Albane 2026-06-26) : « le nom des cogerants est mis au hasard -> dans la
    liste des associes on puisse cocher si la personne est gerante ». -> une case
    « Gerant(e) de la SCM » par associe ; la liste `scm_cedee['cogerants']` est
    DERIVEE des cases cochees (au lieu du fallback hardcode du generateur)."""
    with st.expander("Associes presents a l'assemblee", expanded=True):
        st.caption(
            "Le total des parts des presents doit egaler le nombre total de parts "
            "de la SCM. Cochez « Gerant(e) » pour les cogerants ; choisissez plus bas "
            "qui preside la seance (par defaut le cedant)."
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
        # FB-5 : 1er present preremplie avec le cedant (identite), modifiable.
        if cedant:
            for field, value in (
                ("civilite", str(cedant.get("civilite_affichage") or "")),
                ("prenom", str(cedant.get("prenom") or "")),
                ("nom", str(cedant.get("nom") or "")),
            ):
                key = f"{_CESSION_PREFIX}_cession_scm_present_0_{field}"
                if not st.session_state.get(key) and value:
                    st.session_state[key] = value
        presents: list[ScmCessionAssocie] = []
        cogerants: list[str] = []  # FB-8b : cogerants derives des cases cochees
        cursor = 1  # plage cumulative INTERNE (jamais affichee) -> derivation apres-cession
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
            # FB-5 : plus de saisie de plage -> une seule colonne pour le nb de parts.
            nb_parts_saisi = _cession_text(
                st, "Nombre de parts", section="scm_present", field=f"{index}_nb_parts",
                default="",
            )
            nb_present = int(nb_parts_saisi) if nb_parts_saisi.isdigit() else None
            # Plage INTERNE cumulative (ordre des presents + nb) : present k = [cursor,
            # cursor + nb - 1]. Sert UNIQUEMENT a la derivation deterministe de
            # l'apres-cession (plage residuelle du cedant / plage cedee), jamais affichee.
            plage = ""
            if nb_present and nb_present > 0:
                plage = f"{cursor} à {cursor + nb_present - 1}"  # N4 : « à » accentue
                cursor += nb_present
            # FB-8b : case « Gerant(e) de la SCM » -> alimente la liste des cogerants.
            est_gerant = st.checkbox(
                "Gerant(e) de la SCM",
                key=f"{_CESSION_PREFIX}_cession_scm_present_{index}_gerant",
            )
            associe = ScmCessionAssocie(
                **identity,
                parts=ScmCessionPartsAttribution(
                    nb=nb_present,
                    plage=plage or None,
                ),
            )
            if est_gerant:
                cogerant_label = _scm_present_label(associe)
                if cogerant_label:
                    cogerants.append(cogerant_label)
            presents.append(associe)
        total_parts = sum((a.parts.nb or 0) for a in presents if a.parts)
        nb_total_scm = int(scm_cedee.get("nb_parts_total") or 0)
        if nb_total_scm and total_parts != nb_total_scm:
            st.warning(
                f"Total des parts des presents ({total_parts}) different du nombre "
                f"total de parts de la SCM ({nb_total_scm}). La generation du PV "
                "sera bloquee tant que les deux ne coincident pas."
            )
        # FB-8b : la liste des cogerants derive des cases cochees. F1 (Albane 2026-07-10) :
        # on ecrase TOUJOURS la liste d'exemple de la fixture (« Paul Bernard / Jean Dupont /
        # Anne Martin ») — vide si aucune case cochee, pour ne plus faire fuiter des cogerants
        # inventes (cf. SC2 cote generateur : « laisser vierge si non rempli »).
        scm_cedee["cogerants"] = cogerants
        # FB-7 : le president de seance (par defaut le cedant) doit figurer en DERNIERE
        # position (le generateur PV prend associes_presents[-1]). On expose le choix.
        presents = _scm_reorder_president_last(presents, cedant)
    return presents


def _scm_reorder_president_last(
    presents: list[ScmCessionAssocie],
    cedant: dict[str, object] | None,
) -> list[ScmCessionAssocie]:
    """FB-7 : reordonne les presents pour que le PRESIDENT de seance soit en derniere
    position (le generateur PV AGE SCM lit associes_presents[-1] comme president).

    Par DEFAUT le president = le cedant (celui qui vend les parts) ; un selecteur
    permet de choisir un autre present si besoin. L'ordre relatif des autres associes
    est preserve. Liste vide / un seul present -> renvoyee telle quelle."""
    if len(presents) <= 1:
        return presents
    # Index par defaut = le cedant s'il est present, sinon le dernier (comportement
    # historique : le dernier associe saisi presidait).
    default_index = len(presents) - 1
    if cedant:
        for idx, associe in enumerate(presents):
            if _scm_same_person(associe, cedant):
                default_index = idx
                break
    labels = [
        _scm_present_label(a) or f"Associe {i + 1}"
        for i, a in enumerate(presents)
    ]
    choix = st.selectbox(
        "Qui preside la seance ? (par defaut le cedant)",
        options=list(range(len(presents))),
        index=default_index,
        format_func=lambda i: labels[i],
        key=f"{_CESSION_PREFIX}_cession_scm_president_index",
    )
    president = presents[int(choix)]
    autres = [a for i, a in enumerate(presents) if i != int(choix)]
    return [*autres, president]


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
        # N4 (Rafael 2026-06-24) : plage cedee auto-derivee de la plage du cedant + nb cede,
        # convention « le cedant cede ses dernieres parts » (cf. _plage_dernieres_parts).
        # A confirmer Rafael (QUESTIONS_RAFAEL O24-06). Une plage cedee deja fournie est respectee.
        if not plage_cedee:
            derivee = _plage_dernieres_parts(plage_initiale, nb_cedees)
            if derivee:
                plage_cedee = derivee
                parts_cedees["plage"] = derivee
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
        return f"{i_debut} à {c_debut - 1}"  # N4 : « à » accentue
    # Plage cedee au DEBUT de la plage initiale : reste = [c_fin + 1, i_fin].
    if c_debut == i_debut and c_fin < i_fin:
        return f"{c_fin + 1} à {i_fin}"  # N4 : « à » accentue
    # Cas non contigu : on conserve la plage initiale (le nb reste fait foi).
    return plage_initiale


def _plage_dernieres_parts(plage_initiale: str, nb: int) -> str:
    """Plage des `nb` DERNIERES parts d'une plage « A a B » (convention de cession §4.1).

    N4 (Rafael 2026-06-24) : le cedant cede ses dernieres parts -> [B - nb + 1, B], residu
    contigu au debut (cas principal de _complement_plage). Vide si la plage est non parsable,
    si nb <= 0, ou si nb depasse la taille de la plage (cession partielle invalide)."""
    init = _parse_plage(plage_initiale)
    if init is None or nb <= 0:
        return ""
    debut, fin = init
    if nb > (fin - debut + 1):
        return ""
    return f"{fin - nb + 1} à {fin}"  # N4 : « à » accentue


def _derive_scm_prix_unitaire(prix: dict[str, object], nb_parts: object) -> None:
    """Recalcule le prix UNITAIRE par part = prix global / nb de parts cedees (§S2 Albane).

    Le prix global est saisi ; le prix par part doit en DECOULER (ex. 20 EUR pour 20 parts
    -> « un (1) euro »). On derive in-place `prix['unitaire']` (chiffre) et
    `prix['unitaire_lettres']` (toutes lettres) via les helpers publics
    `format_numeric_value` / `number_words_from_value` (memes que la valeur nominale).
    Divisible -> entier (« 1 » / « un ») ; non divisible -> figure decimale francaise
    (« 1,5 », lettres = figure, la mise en lettres monetaire decimale n'etant pas ratifiee).
    Donnees absentes / nb == 0 : on NE touche a rien (jamais de crash, jamais de cle videe)."""
    global_raw = str(prix.get("global") or "").strip()
    if not global_raw:
        return
    try:
        nb = int(nb_parts) if nb_parts is not None else 0
    except (TypeError, ValueError):
        nb = 0
    if nb <= 0:
        return
    cleaned = re.sub(r"[^0-9,.\-]", "", global_raw.replace(" ", "").replace(",", "."))
    if not cleaned:
        return
    try:
        global_amount = Decimal(cleaned)
    except InvalidOperation:
        return
    unitaire = global_amount / Decimal(nb)
    # M2 (Akainu 2026-06-26) : arrondir au centime — sinon un global non divisible (ex
    # 100/3) imprimerait 28 decimales brutes sur l'acte. Un divisible exact redevient un
    # entier propre (« 1 », pas « 1,00 ») pour la mise en lettres.
    unitaire = unitaire.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if unitaire == unitaire.to_integral_value():
        unitaire = unitaire.to_integral_value()
    figure = format_numeric_value(unitaire).replace(".", ",")
    prix["unitaire"] = figure
    # PRIX SCM (hors scope Albane 7.5) : le slot lettres doit rester SANS unite car l'acte SCM
    # compose « <unitaire_lettres> (<unitaire>) <euro accorde> par part cédée » (l'unite « euro »
    # est ajoutee A PART par `_accord_euro`). ENTIER -> mots nus (« un », « cent »). DECIMAL ->
    # on garde la FIGURE en lettres (« 2,5 ») : la mise en lettres MONETAIRE (« deux euros et
    # cinquante centimes ») n'est ratifiee que pour la VALEUR NOMINALE (7.5), pas pour le prix,
    # et injecterait ici un DOUBLE « euro » (« ...centimes (2,5) euros »). Verrou explicite.
    if unitaire == unitaire.to_integral_value():
        prix["unitaire_lettres"] = number_words_from_value(figure) or figure
    else:
        prix["unitaire_lettres"] = figure


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


def _row_is_included(status: str | None) -> bool:
    # Produit fini : un document est LISTE s'il fait partie du dossier genere. Les statuts
    # internes hors perimetre (« hors_v1 », « blocked »/« bloque ») sont exclus de l'affichage.
    normalized = (status or "").strip().lower()
    return "hors" not in normalized and normalized not in {"blocked", "bloque", "bloqué"}


def _render_generation_zone(data_entry: CleanDataEntry, plan: CleanGenerationPlan) -> None:  # noqa: C901
    st.subheader("Génération")
    for warning in plan.warnings:
        st.info(warning)
    if plan.can_generate:
        st.success(plan.reason)
    else:
        st.warning(plan.reason)
    if plan.blockers:
        for blocker in plan.blockers[:8]:
            st.caption(f"À compléter : {blocker}")
        if len(plan.blockers) > 8:
            st.caption(f"{len(plan.blockers) - 8} autres champs requis.")

    # Produit fini : on liste les documents GENERES par leur nom, sans le code technique interne
    # (doc_code), le statut brut ni le message de perimetre. L'entete n'apparait que s'il y a au
    # moins un document (evite une section « Documents » vide sur un formulaire non rempli).
    documents_inclus = [
        row.label for row in plan.document_rows if _row_is_included(row.status)
    ]
    if documents_inclus:
        st.markdown("**Documents du dossier**")
        for label in documents_inclus:
            st.caption(f"• {label}")

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
        sasu_holding_slice,
        selas_multi_slice,
        selas_uni_dentiste_slice,
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
    elif structure == "SASU_HOLDING":
        # SASU Holding generaliste (DOC-048) : SAS unipersonnelle, holding patrimoniale,
        # DISTINCTE de la « SAS / SPFPL medecins » ci-dessus.
        payload = sasu_holding_slice.render_sasu_holding_form()
        plan = sasu_holding_slice.build_sasu_holding_plan(payload)
        generate = sasu_holding_slice.generate_dossier
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
    elif structure == "SELAS uni dentiste":
        # SELAS UNIPERSONNELLE dentiste (DOC-046) : parcours uni dedie, clone du medecin
        # uni avec corpus dentiste (retour Rafael #5).
        payload = selas_uni_dentiste_slice.render_selas_uni_dentiste_form()
        plan = selas_uni_dentiste_slice.build_selas_uni_dentiste_plan(payload)
        generate = selas_uni_dentiste_slice.generate_dossier
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
    st.subheader("Génération")
    for warning in getattr(plan, "warnings", ()):  # type: ignore[arg-type]
        st.info(warning)
    if plan.can_generate:
        st.success(plan.reason)
    else:
        st.warning(plan.reason)
    for blocker in list(plan.blockers)[:8]:
        st.caption(f"À compléter : {blocker}")
    if len(plan.blockers) > 8:
        st.caption(f"{len(plan.blockers) - 8} autres champs requis.")

    # Produit fini : resume du nombre de documents, sans les codes techniques internes (DOC-XXX).
    nb_documents = len(list(plan.document_codes))
    if nb_documents:
        pluriel = "s" if nb_documents > 1 else ""
        st.markdown(f"**{nb_documents} document{pluriel}** seront générés pour ce dossier.")

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
