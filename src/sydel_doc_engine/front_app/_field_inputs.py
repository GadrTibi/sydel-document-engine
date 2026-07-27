"""Helpers de saisie texte partages pour les slices front (C2).

Le helper de saisie texte (`_t` / `_text`) etait duplique a l'identique dans plusieurs
slices (`sas`, `selas_multi`, `selas_uni_medecin`, `selas_uni_dentiste`, `civil_statuts`,
`spfpl`). On extrait UNE implementation canonique ici ; les slices la consomment via
des wrappers fins qui preservent leur signature locale (avec ou sans `prefix` explicite).

Comportement strictement identique a l'historique :
- la cle de session = `f"{prefix}_{field}"` (ou la cle complete passee directement) ;
- defaut a "" si absente de `st.session_state` ;
- rendu via `copyable_text_input` (icone « copier » O24-04), valeur `.strip()`.

Couche UI uniquement : ce module n'influence pas le document genere.
"""

from __future__ import annotations

import streamlit as st

from sydel_doc_engine.front_app.front_widgets import copyable_text_input


def text_input_field(
    container,
    key: str,
    label: str,
    hint: str | None = None,
) -> str:
    """Champ texte canonique keye par la cle de session COMPLETE."""
    if key not in st.session_state:
        st.session_state[key] = ""
    return str(copyable_text_input(container, label, key=key, help=hint)).strip()


def text_input_prefixed(
    container,
    prefix: str,
    field: str,
    label: str,
    hint: str | None = None,
) -> str:
    """Champ texte canonique keye par `f"{prefix}_{field}"`."""
    return text_input_field(container, f"{prefix}_{field}", label, hint)
