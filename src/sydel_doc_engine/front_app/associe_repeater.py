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
from typing import Final

import streamlit as st

from sydel_doc_engine.domain.models import (
    Address,
    StatutsCivilsApport,
    StatutsCivilsAssocie,
    StatutsCivilsParts,
    StatutsCivilsRepresentant,
)
from sydel_doc_engine.front_app.field_derivations import (
    derive_gender_from_civilite,
    number_words_from_value,
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
    # Pour les SEL d'exercice (SELAS), on collecte des champs ordinaux + qualite capital.
    collect_exercice_fields: bool = False


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

    st.markdown(f"**Associes ({nombre})**")
    cols = st.columns([1, 1, 3])
    if cols[0].button("Ajouter un associe", key=f"{config.key_prefix}_add"):
        st.session_state[_count_key(config)] = min(config.nb_max, nombre + 1)
        st.rerun()
    if cols[1].button("Retirer un associe", key=f"{config.key_prefix}_remove"):
        st.session_state[_count_key(config)] = max(config.nb_min, nombre - 1)
        st.rerun()
    cols[2].caption(
        f"Entre {config.nb_min} et {config.nb_max} associes. Vocabulaire : {config.titre_unite}."
    )

    associes: list[StatutsCivilsAssocie] = []
    for index in range(nombre):
        associes.append(_render_one_associe(config, index))
    return associes


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
    return str(container.text_input(label, key=key)).strip()


def _int(prefix: str, field: str, label: str, *, container=st) -> int:
    key = f"{prefix}_{field}"
    _seed(key, 0)
    return int(container.number_input(label, min_value=0, step=1, key=key))


def _parts_block(
    config: RepeaterConfig,
    prefix: str,
    role_statutaire: str | None,
) -> tuple[StatutsCivilsApport, StatutsCivilsParts, int]:
    unite = config.titre_unite
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

    col_c, col_d = st.columns(2)
    debut = _int(prefix, "parts_debut", f"{unite.capitalize()} debut", container=col_c)
    fin = _int(prefix, "parts_fin", f"{unite.capitalize()} fin", container=col_d)
    plage = f"{debut} a {fin}" if debut and fin else None
    parts = StatutsCivilsParts(
        nb=nb_titres,
        nb_lettres=number_words_from_value(nb_titres),
        plage_affichee=plage,
        debut=debut or None,
        fin=fin or None,
        qualite_associe=role_statutaire,
    )
    return apport, parts, nb_titres


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

    col_d, col_e, col_f = st.columns(3)
    date_naissance = _text(prefix, "date_naissance", "Date de naissance", container=col_d)
    ville_naissance = _text(prefix, "ville_naissance", "Ville de naissance", container=col_e)
    departement_naissance = _text(
        prefix, "departement_naissance", "Departement naissance", container=col_f
    )

    col_g, col_h = st.columns(2)
    nationalite = _text(prefix, "nationalite", "Nationalite", container=col_g)
    situation = _text(prefix, "situation_maritale", "Situation matrimoniale", container=col_h)
    profession = _text(prefix, "profession", "Profession")
    adresse = _text(prefix, "adresse", "Adresse personnelle (affichee)")

    apport, parts, _nb = _parts_block(config, prefix, role_statutaire)

    associe = StatutsCivilsAssocie(
        type_personne="personne_physique",
        role_statutaire=role_statutaire,
        genre=derive_gender_from_civilite(civilite),
        civilite_affichage=civilite,
        prenom=prenom,
        prenoms=prenom,
        nom=nom,
        date_naissance=date_naissance or None,
        ville_naissance=ville_naissance or None,
        departement_naissance=departement_naissance or None,
        nationalite=nationalite or None,
        profession=profession or None,
        situation_maritale=situation or None,
        adresse_personnelle_affichee=adresse or None,
        apport=apport,
        parts=parts,
    )

    if config.collect_exercice_fields:
        _enrich_exercice_fields(associe, prefix, parts.nb or 0)
    return associe


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
    profession = _text(prefix, "profession", "Profession (personne morale)")

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
