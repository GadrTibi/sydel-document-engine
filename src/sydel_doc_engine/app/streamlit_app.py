from __future__ import annotations

import streamlit as st

from sydel_doc_engine.registry.catalog import catalog_rows
from sydel_doc_engine.registry.lot_status import count_by_status

st.set_page_config(page_title="SYDEL Document Engine", layout="wide")

st.title("SYDEL Document Engine — V1 bootstrap")
st.caption("Base GitHub + Codex, pas encore l'interface métier finale.")

st.subheader("État du registre seed")
st.table(catalog_rows())

st.subheader("Répartition par statut")
st.json(count_by_status())

st.info(
    "Étape suivante recommandée : arbitrer DOC-002, valider le rendu from-scratch, "
    "puis ouvrir les tickets d'implémentation du Lot 1."
)