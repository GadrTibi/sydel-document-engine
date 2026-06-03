from __future__ import annotations

import streamlit as st

from sydel_doc_engine.front_app.shell import render_clean_front

st.set_page_config(page_title="SYDEL Track B", layout="wide")
render_clean_front()
