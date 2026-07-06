"""Repeater d'associes generique 1->N (personne physique + personne morale).

Extrait du patron SELARL (saisie + derivation genre + nombres en lettres) pour
etre PARTAGE par tous les types multi-associes (SCI, SCI IRIS, SCS, SCM, SELAS).
Il produit des `StatutsCivilsAssocie` valides, vocabulaire parts/actions
parametrable, role statutaire optionnel (commandite/commanditaire pour la SCS).

Le composant est auto-extensible : un bouton "Ajouter un associe" incremente le
nombre via `st.session_state`. Le moteur reste seul juge de la coherence (somme
des parts, totaux) ; le repeater ne fait que collecter une saisie propre.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Final

import streamlit as st

from sydel_doc_engine.domain.enums import Gender
from sydel_doc_engine.domain.models import (
    Address,
    RegimeCommunautaireAssocie,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
)
from sydel_doc_engine.front_app.address_oneline import (
    parse_address_full as _parse_address_full,
)
from sydel_doc_engine.front_app.field_derivations import (
    MATRIMONIAL_STATUS_PRESETS,
    NATIONALITY_PRESETS,
    accentuate_french_months,
    derive_gender_from_civilite,
    format_numeric_value,
    matrimonial_status_value,
    number_words_from_value,
    regime_communautaire_from_status,
)
from sydel_doc_engine.front_app.front_widgets import (
    copyable_text_input,
    date_input_with_today,
)

PERSONNE_PHYSIQUE: Final = "personne_physique"
PERSONNE_MORALE: Final = "personne_morale"


@dataclass(frozen=True)
class RepeaterConfig:
    """Parametrage du repeater par type."""

    key_prefix: str
    titre_unite: str = "parts"  # "parts" ou "actions" (vocabulaire affiche)
    nb_min: int = 1
    nb_max: int = 6
    nb_defaut: int = 2
    allow_personne_morale: bool = True
    role_statutaire_options: tuple[str, ...] = ()  # ex: ("commandite", "commanditaire")
    # Profession des associes : demandee/affichee UNIQUEMENT pour la SCM (§18.6,
    # retours Albane 2026-06-17). Les autres civiles (SCI, SCI IRIS, SCS) ne la
    # collectent plus (le generateur civil generique ne la rend pas).
    collect_profession: bool = True
    # Pour les SEL d'exercice (SELAS), on collecte des champs ordinaux + qualite capital.
    collect_exercice_fields: bool = False
    # Pour les types a gerant (civils) : case « Dirigeant (gerant) » par associe
    # physique + champs DNC (filiation/adresse) saisis SOUS le gerant designe
    # (reunion 2026-06-09 : champs conditionnels au dirigeant).
    collect_dirigeant: bool = False
    # SCS4 (Albane 2026-06-25) : bloc regime matrimonial RICHE par associe (selectbox de statut +
    # sous-formulaire conjoint si marie + RegimeCommunautaireAssocie / DOC-005-006 si communaute
    # legale), comme la SELAS pluri. Active pour la SCS ; les autres civils gardent le champ simple.
    rich_matrimonial: bool = False


def _count_key(config: RepeaterConfig) -> str:
    return f"{config.key_prefix}_nb_associes"


def associe_count(config: RepeaterConfig) -> int:
    raw = st.session_state.get(_count_key(config), config.nb_defaut)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = config.nb_defaut
    return max(config.nb_min, min(config.nb_max, value))


def _seed(key: str, default: object) -> None:
    if key not in st.session_state:
        st.session_state[key] = default


def render_associe_repeater(config: RepeaterConfig) -> list[StatutsCivilsAssocie]:
    """Rend le formulaire N associes et retourne les `StatutsCivilsAssocie` saisis."""

    _seed(_count_key(config), config.nb_defaut)
    nombre = associe_count(config)

    cols = st.columns([1, 1, 3])
    if cols[0].button("Ajouter un associe", key=f"{config.key_prefix}_add"):
        st.session_state[_count_key(config)] = min(config.nb_max, nombre + 1)
    if cols[1].button("Retirer un associe", key=f"{config.key_prefix}_remove"):
        st.session_state[_count_key(config)] = max(config.nb_min, nombre - 1)
    # N5 (Albane 2026-06-24) : re-lire le nombre APRES +/- au lieu de st.rerun() (qui se declenchait
    # AVANT le rendu des associes -> Streamlit garbage-collectait l'etat des widgets non instancies
    # -> champs des associes PRECEDENTS EFFACES). Sans rerun, la boucle rend le nouveau nombre.
    nombre = associe_count(config)
    st.markdown(f"**Associes ({nombre})**")
    cols[2].caption(
        f"Entre {config.nb_min} et {config.nb_max} associes. Vocabulaire : {config.titre_unite}."
    )

    associes: list[StatutsCivilsAssocie] = []
    for index in range(nombre):
        associes.append(_render_one_associe(config, index))
    _assign_cumulative_part_ranges(associes)
    return associes


def _assign_cumulative_part_ranges(associes: list[StatutsCivilsAssocie]) -> None:
    """Attribue des plages de parts cumulatives a partir du nombre par associe.

    Les champs « parts debut / fin » ne sont plus saisis (§18.5, retours Albane
    2026-06-17) : la numerotation se derive de l'ordre des associes et de leur
    nombre de parts. SCI IRIS exige debut/fin (generateur + groupes de resultat) ;
    on les calcule donc ici, plages contigues 1..N sans trou ni chevauchement.
    """
    cursor = 1
    for associe in associes:
        if associe.parts is None:
            continue
        nb = associe.parts.nb or 0
        if nb <= 0:
            associe.parts.debut = None
            associe.parts.fin = None
            associe.parts.plage_affichee = None
            continue
        debut = cursor
        fin = cursor + nb - 1
        associe.parts.debut = debut
        associe.parts.fin = fin
        # N4 (Albane/Rafael 2026-07-01, « comme les modeles ») : plage avec « à » accentue
        # (« 1 à 100 »), comme le modele SCI IRIS et le francais correct.
        associe.parts.plage_affichee = f"{debut} à {fin}"
        cursor = fin + 1


def _render_one_associe(config: RepeaterConfig, index: int) -> StatutsCivilsAssocie:
    prefix = f"{config.key_prefix}_associe_{index}"
    with st.expander(f"Associe {index + 1}", expanded=index == 0):
        type_personne = PERSONNE_PHYSIQUE
        if config.allow_personne_morale:
            type_key = f"{prefix}_type"
            _seed(type_key, PERSONNE_PHYSIQUE)
            type_personne = st.selectbox(
                "Type d'associe",
                (PERSONNE_PHYSIQUE, PERSONNE_MORALE),
                key=type_key,
            )

        role_statutaire = None
        if config.role_statutaire_options:
            role_key = f"{prefix}_role"
            _seed(role_key, config.role_statutaire_options[0])
            role_statutaire = st.selectbox(
                "Role statutaire",
                config.role_statutaire_options,
                key=role_key,
            )

        if type_personne == PERSONNE_MORALE:
            return _render_personne_morale(config, prefix, index, role_statutaire)
        return _render_personne_physique(config, prefix, index, role_statutaire)


def _text(prefix: str, field: str, label: str, *, container=st) -> str:
    key = f"{prefix}_{field}"
    _seed(key, "")
    # O24-04 : icône « copier » sur chaque champ texte (helper partagé).
    return str(copyable_text_input(container, label, key=key)).strip()


def render_nationalite_selectbox(prefix: str, *, container=st) -> str:
    """Nationalite en deroulant (NATIONALITY_PRESETS), patron SELARL (§SCREEN-1).

    Cle `{prefix}_nationalite_choice` (selectbox) + `{prefix}_nationalite_other`
    (saisie libre si « Autre »). Sortie lowercased pour rester compatible avec le
    mapping existant (l'associe stocke `nationalite` en minuscules).
    """
    choice_key = f"{prefix}_nationalite_choice"
    _seed(choice_key, NATIONALITY_PRESETS[0])
    choice = container.selectbox("Nationalite", NATIONALITY_PRESETS, key=choice_key)
    if choice == "Autre":
        return _text(prefix, "nationalite_other", "Nationalite autre", container=container)
    return str(choice).lower()


def _render_nationalite(prefix: str, *, container=st) -> str:
    return render_nationalite_selectbox(prefix, container=container)


def _int(prefix: str, field: str, label: str, *, container=st) -> int:
    key = f"{prefix}_{field}"
    _seed(key, 0)
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _societe_capital_montant(config: RepeaterConfig) -> str:
    """Montant du capital social de la societe, lu depuis l'etat de saisie.

    Retour Albane §1 (2026-06-28) : dans une societe UNIPERSONNELLE, on ne demande
    PAS le montant d'apport de l'associe unique — il vaut FORCEMENT le capital social
    (« si le capital est de 1.000 €, l'apport de l'associe unique est de 1.000 € »).
    Le slice civil (`civil_statuts_slice`) ecrit le capital dans la cle de session
    `{prefix}_capital_social` (number_input) ; on le reformate ici EXACTEMENT comme le
    payload (`format_numeric_value`) pour rester byte-fidele a une saisie manuelle
    (« 1000 »). Vide tant que le capital n'est pas saisi -> apport vide, comme avant.
    """
    return format_numeric_value(
        st.session_state.get(f"{config.key_prefix}_capital_social", "")
    )


def _parts_block(
    config: RepeaterConfig,
    prefix: str,
    role_statutaire: str | None,
) -> tuple[StatutsCivilsApport, StatutsCivilsParts, int]:
    unite = config.titre_unite
    # §1 (Albane) : societe UNIPERSONNELLE (un seul associe) -> le montant d'apport de
    # l'associe unique n'est plus saisi ; on reprend AUTOMATIQUEMENT le capital social.
    # SEL d'exercice (SELAS, `collect_exercice_fields`) exclu : ses apports en actions
    # sont geres par la couche exercice, hors de ce chemin civil. Pluripersonnel (>=2)
    # inchange : chaque associe garde son apport individuel (apports repartis).
    unipersonnel = not config.collect_exercice_fields and associe_count(config) == 1
    if unipersonnel:
        apport_montant = _societe_capital_montant(config)
        nb_titres = _int(prefix, "nb_titres", f"Nombre de {unite}")
    else:
        col_a, col_b = st.columns(2)
        apport_montant = _text(prefix, "apport_montant", "Apport (montant)", container=col_a)
        nb_titres = _int(prefix, "nb_titres", f"Nombre de {unite}", container=col_b)

    apport = StatutsCivilsApport(
        montant=apport_montant,
        montant_lettres=number_words_from_value(apport_montant),
    )

    if config.collect_exercice_fields:
        # SEL d'exercice (SELAS) : titres = actions, qualite capital exercante / non.
        return apport, StatutsCivilsParts(), nb_titres

    # Plages « parts debut / fin » : plus saisies (§18.5) ; derivees ensuite de
    # l'ordre + du nombre via _assign_cumulative_part_ranges. On ne collecte ici
    # que les parts souscrites (nb_titres).
    parts = StatutsCivilsParts(
        nb=nb_titres,
        nb_lettres=number_words_from_value(nb_titres),
        qualite_associe=role_statutaire,
    )
    return apport, parts, nb_titres


def _oneline_address(
    prefix: str, field: str, label: str, *, container=st
) -> Address | None:
    """O24-03 : UN champ texte d'adresse (« 10 rue de la Paix, 75002 Paris »).

    Remplace les 4 colonnes No/Voie/CP/Ville. Le verbatim client O24-03 exige UNE
    ligne. Les consommateurs en aval (DNC du gerant via signataire_adresse_*, seed
    « siege = adresse perso ») lisent encore les cles de session
    `{prefix}_{field}_num/voie/cp/ville` -> on les RE-ECRIT a partir du parse (parite
    avec l'ancien comportement, generateurs inchanges). Renvoie l'Address ou None.
    """
    raw = _text(prefix, field, label, container=container)
    struct = _parse_address_full(raw)
    st.session_state[f"{prefix}_{field}_num"] = struct.num_voie if struct else ""
    st.session_state[f"{prefix}_{field}_voie"] = struct.voie if struct else ""
    st.session_state[f"{prefix}_{field}_cp"] = struct.cp if struct else ""
    st.session_state[f"{prefix}_{field}_ville"] = struct.ville if struct else ""
    return struct


def _render_dirigeant_civil(prefix: str, index: int) -> None:
    """Case « Dirigeant (gerant) » + filiation du gerant designe (civils).

    Le gerant est un associe ; on le designe par une case et on saisit SOUS lui
    les NOMS DES PARENTS de la declaration de non-condamnation. L'ADRESSE du gerant
    est REPRISE de l'adresse personnelle deja saisie pour cet associe (§18.5,
    retours Albane 2026-06-17 : plus d'adresse supplementaire). A defaut, le 1er
    associe physique est gerant (historique).
    """
    dirigeant_key = f"{prefix}_is_dirigeant"
    _seed(dirigeant_key, index == 0)
    if not st.checkbox("Dirigeant (gerant)", key=dirigeant_key):
        return
    st.caption("Declaration de non-condamnation du gerant (noms des parents)")
    col_a, col_b = st.columns(2)
    _text(prefix, "sig_nom_pere", "Nom du pere", container=col_a)
    _text(prefix, "sig_nom_mere", "Nom de la mere", container=col_b)


def _render_personne_physique(
    config: RepeaterConfig,
    prefix: str,
    index: int,
    role_statutaire: str | None,
) -> StatutsCivilsAssocie:
    col_a, col_b, col_c = st.columns(3)
    civilite = col_a.selectbox(
        "Civilite",
        ("Monsieur", "Madame"),
        key=f"{prefix}_civilite",
    )
    prenom = _text(prefix, "prenom", "Prenom", container=col_b)
    nom = _text(prefix, "nom", "Nom", container=col_c)
    # Q4 (nom d'usage marital) : nom de naissance OPTIONNEL. S'il est renseigne ET differe du nom
    # d'usage, la comparution (SCS / micro holding) rend « <prenoms> <nom_naissance> épouse <nom> »
    # (modeles Albane). Laisser vide pour les cas sans nom d'usage -> rendu inchange.
    nom_naissance = _text(
        prefix, "nom_naissance", "Nom de naissance (si différent du nom d'usage)"
    )

    col_d, col_e, col_f = st.columns(3)
    # R29-06 (Rafael) : selecteur de date (calendrier) + bouton « Aujourd'hui » sur la
    # date de naissance, PARTOUT. Le helper conserve le champ texte JJ/MM/AAAA comme
    # source editable (saisie verbatim francaise « 1er aout 1985 » toujours possible) et
    # la cle session_state `{prefix}_date_naissance` est inchangee -> aucun post-traitement
    # casse (accentuation des mois ci-dessous). seed=False : pas de date du jour pre-remplie
    # sur une naissance. On relit la chaine texte (et non l'objet date) pour rester byte-fidele.
    date_input_with_today(
        "Date de naissance",
        key=f"{prefix}_date_naissance",
        value=date.today(),
        container=col_d,
        seed=False,
    )
    date_naissance = str(st.session_state.get(f"{prefix}_date_naissance") or "").strip()
    ville_naissance = _text(prefix, "ville_naissance", "Ville de naissance", container=col_e)
    departement_naissance = _text(
        prefix, "departement_naissance", "Departement naissance", container=col_f
    )

    col_g, col_h = st.columns(2)
    nationalite = _render_nationalite(prefix, container=col_g)
    # SCS4 (Albane 2026-06-25) : pour la SCS, bloc matrimonial RICHE (selectbox de statut +
    # conjoint si marie + RegimeCommunautaireAssocie / DOC-005-006), comme la SELAS pluri. Les
    # autres civils (SCI/SCM) gardent le champ « situation matrimoniale » texte simple.
    regime_associe: RegimeCommunautaireAssocie | None = None
    if config.rich_matrimonial:
        situation_label = col_h.selectbox(
            "Situation matrimoniale", MATRIMONIAL_STATUS_PRESETS, key=f"{prefix}_situation"
        )
        situation = _situation_display_civil(
            situation_label, derive_gender_from_civilite(civilite)
        )
        regime_associe = _render_conjoint_si_communaute_civil(prefix, situation_label)
    else:
        situation = _text(prefix, "situation_maritale", "Situation matrimoniale", container=col_h)
    # Profession : SCM uniquement (§18.6). Hors SCM, aucun champ ni valeur.
    profession = _text(prefix, "profession", "Profession") if config.collect_profession else ""

    # Adresse personnelle STRUCTUREE (§18.5) : une seule adresse par associe, reprise
    # telle quelle pour la DNC du gerant. O24-03 : saisie sur UNE LIGNE (parse interne
    # -> num/voie/cp/ville exiges par la DNC et le seed « siege = adresse perso » qui
    # lisent encore les cles de session adresse_num/voie/cp/ville).
    st.caption("Adresse personnelle (N° et voie, CP Ville)")
    adresse_perso = _oneline_address(
        prefix, "adresse", "Adresse personnelle (N° et voie, CP Ville)"
    )
    adresse_affichee = adresse_perso.adresse_affichee if adresse_perso else ""

    apport, parts, _nb = _parts_block(config, prefix, role_statutaire)

    if config.collect_dirigeant:
        _render_dirigeant_civil(prefix, index)

    associe = StatutsCivilsAssocie(
        type_personne="personne_physique",
        role_statutaire=role_statutaire,
        genre=derive_gender_from_civilite(civilite),
        civilite_affichage=civilite,
        prenom=prenom,
        prenoms=prenom,
        nom=nom,
        # Q4 : nom de naissance (maiden) optionnel -> mention « épouse » en comparution.
        nom_naissance=nom_naissance or None,
        # LIVE-03 : date de naissance a saisie LIBRE (text_input) -> re-accentue les
        # mois avant injection (SCI / SCM / SCS via le repeater) ; generateur = echo fidele.
        date_naissance=accentuate_french_months(date_naissance) if date_naissance else None,
        ville_naissance=ville_naissance or None,
        departement_naissance=departement_naissance or None,
        nationalite=nationalite or None,
        profession=profession or None,
        situation_maritale=situation or None,
        adresse_personnelle=adresse_perso,
        adresse_personnelle_affichee=adresse_affichee or None,
        apport=apport,
        parts=parts,
        regime_communautaire_associe=regime_associe,  # SCS4 : DOC-005/006 si communaute
    )

    if config.collect_exercice_fields:
        _enrich_exercice_fields(associe, prefix, parts.nb or 0)
    return associe


def _situation_display_civil(situation_label: str, genre: Gender) -> str:
    """SCS4 (Albane 2026-06-25) : affichage genre-resolu de la situation matrimoniale, comme la
    SELAS pluri (_situation_display) -> on stocke le mot d'etat civil accorde et accentue."""
    feminin = genre == Gender.FEMININ
    table = {
        "marie": "mariée" if feminin else "marié",
        "pacse": "pacsée" if feminin else "pacsé",
        "divorce": "divorcée" if feminin else "divorcé",
        "veuf": "veuve" if feminin else "veuf",
        "celibataire": "célibataire",
    }
    return table.get(matrimonial_status_value(situation_label), "célibataire")


def _render_conjoint_si_communaute_civil(
    prefix: str, situation_label: str
) -> RegimeCommunautaireAssocie | None:
    """SCS4 : conjoint d'un associe physique MARIE ou partenaire PACSE (figure a l'acte) +
    RegimeCommunautaireAssocie (DOC-005 renonciation + DOC-006 avertissement) si communaute
    LEGALE (mariage) seulement.

    Albane 6.3/7.3 (RATIFIE 2026-07-06) : le partenaire PACSE est desormais capte (figure a
    l'acte de cession, « pacsé avec {partenaire} ») — SUPERSEDE l'exclusion PACS O24-11. Le
    partenaire pacse est OPTIONNEL. L'objet RegimeCommunautaireAssocie (DOC-005/006) reste
    MARIAGE + communaute legale uniquement (un PACS ne genere aucun document de regime)."""
    status_value = matrimonial_status_value(situation_label)
    if status_value not in {"marie", "pacse"}:
        return None
    label = "Conjoint" if status_value == "marie" else "Partenaire (PACS)"
    st.caption(f"{label} de cet associé (figure à l'acte ; lettres si communauté légale)")
    col_a, col_b, col_c = st.columns(3)
    conjoint_civilite = col_a.selectbox(
        f"Civilité {label.lower()}", ("Madame", "Monsieur"), key=f"{prefix}_conjoint_civilite"
    )
    conjoint_prenom = _text(prefix, "conjoint_prenom", f"Prénom {label.lower()}", container=col_b)
    conjoint_nom = _text(prefix, "conjoint_nom", f"Nom {label.lower()}", container=col_c)
    if status_value != "marie" or not regime_communautaire_from_status(situation_label):
        return None
    return RegimeCommunautaireAssocie(
        actif=True,
        regime_matrimonial="la communauté légale",
        conjoint_civilite=conjoint_civilite,
        conjoint_genre=derive_gender_from_civilite(conjoint_civilite),
        conjoint_prenom=conjoint_prenom or None,
        conjoint_nom=conjoint_nom or None,
    )


def _render_personne_morale(
    config: RepeaterConfig,
    prefix: str,
    index: int,
    role_statutaire: str | None,
) -> StatutsCivilsAssocie:
    denomination = _text(prefix, "denomination", "Denomination (personne morale)")
    col_a, col_b = st.columns(2)
    forme = _text(prefix, "forme_juridique", "Forme juridique", container=col_a)
    capital = _text(prefix, "capital_social", "Capital social (affiche)", container=col_b)
    siege = _text(prefix, "siege", "Siege (adresse affichee)")
    col_c, col_d = st.columns(2)
    numero_rcs = _text(prefix, "numero_rcs", "Numero RCS", container=col_c)
    ville_rcs = _text(prefix, "ville_rcs", "RCS (ville)", container=col_d)
    # Profession : SCM uniquement (§18.6).
    profession = (
        _text(prefix, "profession", "Profession (personne morale)")
        if config.collect_profession
        else ""
    )

    st.markdown("Representant legal")
    col_e, col_f, col_g, col_h = st.columns(4)
    rep_civilite = col_e.selectbox(
        "Civilite rep.",
        ("Monsieur", "Madame"),
        key=f"{prefix}_rep_civilite",
    )
    rep_prenom = _text(prefix, "rep_prenom", "Prenom rep.", container=col_f)
    rep_nom = _text(prefix, "rep_nom", "Nom rep.", container=col_g)
    rep_fonction = _text(prefix, "rep_fonction", "Fonction rep.", container=col_h)

    apport, parts, _nb = _parts_block(config, prefix, role_statutaire)

    associe = StatutsCivilsAssocie(
        type_personne="personne_morale",
        role_statutaire=role_statutaire,
        denomination=denomination or None,
        forme_juridique=forme or None,
        capital_social=capital or None,
        siege=Address(adresse_affichee=siege) if siege else None,
        numero_rcs=numero_rcs or None,
        ville_rcs=ville_rcs or None,
        profession=profession or None,
        representant=StatutsCivilsRepresentant(
            civilite_affichage=rep_civilite,
            prenom=rep_prenom or None,
            nom=rep_nom or None,
            fonction=rep_fonction or None,
        ),
        apport=apport,
        parts=parts,
    )

    if config.collect_exercice_fields:
        _enrich_exercice_fields(associe, prefix, parts.nb or 0)
    return associe


def _enrich_exercice_fields(
    associe: StatutsCivilsAssocie,
    prefix: str,
    nb_titres: int,
) -> None:
    """Champs additifs SEL d'exercice (SELAS) : qualite capital + ordre + nb_actions."""

    qualite_key = f"{prefix}_qualite_capital"
    _seed(qualite_key, "")
    qualite = str(st.session_state.get(qualite_key, "")).strip()
    if associe.type_personne == "personne_physique":
        associe.qualification_principale = (
            _readonly(prefix, "qualification_principale") or associe.qualification_principale
        )
        associe.ordre_departemental = _readonly(prefix, "ordre_departemental")
        associe.numero_ordre = _readonly(prefix, "numero_ordre")
        associe.numero_rpps = _readonly(prefix, "numero_rpps")
    associe.qualite_capital = qualite or None
    associe.nb_actions = nb_titres or None
    associe.nb_actions_lettres = number_words_from_value(nb_titres) if nb_titres else None


def _readonly(prefix: str, field: str) -> str | None:
    key = f"{prefix}_{field}"
    value = st.session_state.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
