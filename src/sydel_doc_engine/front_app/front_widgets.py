"""Widgets de rendu front PARTAGES entre tous les types d'entreprise.

Couche de rendu commune (cause racine des ecarts de parite) : chaque slice de
type doit CONSOMMER ces helpers au lieu de reimplementer les siens, pour que les
commodites UX du gold SELARL soient HERITEES et non re-codees type par type.
Voir docs/review/METHODE_PARITE_GOLD.md.

Premier helper extrait : la saisie de date + bouton « Aujourd'hui ». Provenance :
shell.py::_date_input_with_today (le gold). Le SELARL reste byte-identique (il
importe desormais cette fonction sous son ancien nom). Les autres types s'y
branchent au lieu de dupliquer leur propre `_date()`.
"""

from __future__ import annotations

from datetime import date

import streamlit as st

from sydel_doc_engine.front_app.field_derivations import (
    format_french_date,
    parse_french_date,
)


def date_input_with_today(
    label: str,
    *,
    key: str,
    value: date,
    container=None,
) -> date | None:
    """Champ de date « JJ/MM/AAAA » + bouton « Aujourd'hui » (helper gold partage).

    Seede `st.session_state[key]` a `value` si absent (sinon respecte la saisie en
    cours), expose un bouton « Aujourd'hui » qui ecrit la date du jour AVANT que le
    text_input soit instancie (Streamlit interdit la modif post-widget), puis rend
    le text_input + une caption d'erreur de format. Retourne la date parsee ou None.

    NESTING-SAFE : rend le bouton AU-DESSUS du champ (pas de `st.columns` interne)
    pour pouvoir etre appele AUSSI a l'interieur d'une colonne (`with col:` ...),
    cas frequent dans les slices (ex. selas_multi_slice signature_date). Le param
    `container` permet de cibler une colonne precise ; par defaut, le contexte
    Streamlit courant.
    """
    target = container if container is not None else st

    current_value = st.session_state.get(key)
    if isinstance(current_value, date):
        st.session_state[key] = format_french_date(current_value)
    elif current_value is None:
        st.session_state[key] = format_french_date(value)

    if target.button("Aujourd'hui", key=f"{key}_today"):
        st.session_state[key] = format_french_date(date.today())
    raw_value = target.text_input(
        label,
        key=key,
        placeholder="JJ/MM/AAAA",
    )
    parsed = parse_french_date(raw_value)
    if str(raw_value).strip() and parsed is None:
        target.caption("Format attendu : JJ/MM/AAAA")
    return parsed


def seed_if_empty(key: str, value: object) -> None:
    """Seede `st.session_state[key]` avec `value` s'il est absent/vide.

    A appeler AVANT le widget correspondant (Streamlit interdit la modification de
    `st.session_state[key]` une fois le widget instancie). Helper de base des
    pre-remplissages de parite (cloture, dates d'exercice, lieu de signature).
    """
    if not st.session_state.get(key):
        st.session_state[key] = value


def seed_closing_date(prefix: str, *, field: str = "date_cloture") -> None:
    """Pre-remplit la cloture du 1er exercice a « 31 decembre N+1 » (convention gold
    SELARL-UI-1, shell.py:1582-1585), modifiable. Libelle TEXTUEL, pas un date-picker."""
    seed_if_empty(f"{prefix}_{field}", f"31 decembre {date.today().year + 1}")


def seed_exercice_dates(
    prefix: str,
    *,
    debut_field: str = "exercice_debut",
    fin_field: str = "exercice_fin",
) -> None:
    """Pre-remplit debut='1er janvier' / fin='31 decembre' (gold shell.py:1578-1581)."""
    seed_if_empty(f"{prefix}_{debut_field}", "1er janvier")
    seed_if_empty(f"{prefix}_{fin_field}", "31 decembre")


def seed_signature_lieu(
    prefix: str,
    ville_siege: str,
    *,
    field: str = "signature_lieu",
) -> None:
    """Pre-remplit le lieu de signature = ville du siege (gold shell.py:1573-1575),
    modifiable. Anti double-saisie. Ne seede que si la ville du siege est connue."""
    if ville_siege:
        seed_if_empty(f"{prefix}_{field}", ville_siege)
