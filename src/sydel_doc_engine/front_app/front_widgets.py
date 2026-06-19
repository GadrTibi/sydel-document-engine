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
