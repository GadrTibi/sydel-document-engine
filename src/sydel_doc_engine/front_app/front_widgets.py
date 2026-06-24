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

import html as _html
from datetime import date

import streamlit as st
import streamlit.components.v1 as components

from sydel_doc_engine.front_app.field_derivations import (
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
    format_french_date,
    parse_french_date,
)


def _copy_button_html(text: str) -> str:
    """Bouton « copier » autonome (O24-04). Le presse-papier est écrit AU CLIC (le bouton
    EST le geste utilisateur) -> `navigator.clipboard.writeText` fiable en contexte sécurisé
    (Streamlit Cloud = https). La valeur transite par un attribut `data-copy` HTML-échappé
    pour éviter tout problème de quotes/caractères spéciaux dans le handler."""
    esc = _html.escape(text, quote=True)
    return (
        f'<button title="Copier le contenu" data-copy="{esc}" '
        'onclick="var b=this;navigator.clipboard.writeText(b.dataset.copy).then('
        "function(){var o=b.textContent;b.textContent='\\u2713 copié';"
        'setTimeout(function(){b.textContent=o;},1200);});" '
        'style="cursor:pointer;border:1px solid #d0d0d0;border-radius:6px;background:#fafafa;'
        'padding:2px 8px;font-size:12px;color:#444;white-space:nowrap;">\U0001F4CB</button>'
    )


def copyable_text_input(
    container, label: str, *, key: str | None = None, help: str | None = None, **text_input_kwargs
) -> str:
    """`text_input` + icône « copier » à côté (O24-04, retour Rafael « icône copier par champ »).

    DROP-IN sûr pour tout `text_input` existant : `**text_input_kwargs` (ex. `disabled`) est
    transmis tel quel. L'icône est un enrichissement PROGRESSIF -> on retombe proprement sur un
    `text_input` simple (sans icône) dans 3 cas, sans jamais casser le formulaire :
      - pas de `key` (impossible de relire la valeur à copier) ;
      - `container.columns` indisponible / nesting trop profond (Streamlit interdit > 1 niveau) ;
      - conteneur mocké en test (stub sans protocole de context manager).
    En contexte réel (Streamlit Cloud, https), l'icône `components.html` écrit le presse-papier
    AU CLIC (le bouton EST le geste utilisateur) ; la valeur est relue dans `st.session_state[key]`.
    """
    if key is None:
        return container.text_input(label, key=key, help=help, **text_input_kwargs)
    try:
        col_field, col_copy = container.columns([0.90, 0.10])
    except Exception:
        # Nesting trop profond ou conteneur sans `columns` -> champ simple, pas d'icône.
        return container.text_input(label, key=key, help=help, **text_input_kwargs)
    value = col_field.text_input(label, key=key, help=help, **text_input_kwargs)
    text = str(st.session_state.get(key, "") or "")
    try:
        with col_copy:
            # Spacer : descend l'icône sous le label pour l'aligner sur le champ.
            st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
            components.html(_copy_button_html(text), height=40)
    except Exception:
        # Conteneur mocké (test) ou contexte hors-Streamlit : on garde juste le champ.
        pass
    return value


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

    # R3 (Rafael 2026-06-24) : calendrier en OPTION (pour aller plus vite) + bouton
    # « Aujourd'hui ». Le calendrier ecrit la date formatee dans la cle TEXTE au changement
    # (on_change) ; le champ texte JJ/MM/AAAA reste la source editable. NESTING-SAFE (aucun
    # st.columns interne). value=None -> calendrier vide tant qu'on n'a pas choisi.
    cal_key = f"{key}_cal"

    def _sync_from_calendar() -> None:
        picked = st.session_state.get(cal_key)
        if isinstance(picked, date):
            st.session_state[key] = format_french_date(picked)

    target.date_input(
        f"{label} (calendrier)",
        value=None,
        key=cal_key,
        format="DD/MM/YYYY",
        on_change=_sync_from_calendar,
    )
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
    """Pre-remplit la cloture du 1er exercice a « 31 décembre N+1 » (convention gold
    SELARL-UI-1, shell.py:1582-1585), modifiable. Libelle TEXTUEL, pas un date-picker."""
    seed_if_empty(f"{prefix}_{field}", f"31 décembre {date.today().year + 1}")


def seed_exercice_dates(
    prefix: str,
    *,
    debut_field: str = "exercice_debut",
    fin_field: str = "exercice_fin",
) -> None:
    """Pre-remplit debut='1er janvier' / fin='31 décembre' (gold shell.py:1578-1581)."""
    seed_if_empty(f"{prefix}_{debut_field}", "1er janvier")
    seed_if_empty(f"{prefix}_{fin_field}", "31 décembre")


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


def seed_siege_from_perso(
    prefix: str,
    *,
    perso_fields: tuple[str, ...] = ("adresse_num", "adresse_voie", "adresse_cp", "adresse_ville"),
    siege_fields: tuple[str, ...] = ("siege_num", "siege_voie", "siege_cp", "siege_ville"),
    perso_oneline: str = "adresse",
    siege_oneline: str = "siege",
) -> None:
    """Si la case « siege = adresse perso » (cle {prefix}_siege_same_as_perso) est
    cochee, recopie l'adresse personnelle dans le siege. Parite gold (shell.py:1453-1470)
    pour les types MONO-associe (source fixe). A appeler EN HAUT du render, avant les
    widgets siege (cross-rerun : l'adresse perso peut etre saisie apres le siege).

    O24-03 : siege et adresse perso sont desormais des champs UNE LIGNE -> on recopie le
    champ une-ligne `{prefix}_{perso_oneline}` -> `{prefix}_{siege_oneline}`. La recopie
    legacy des composants ({prefix}_{*_num/voie/cp/ville}) est conservee en best-effort
    pour les formulaires qui exposent encore des composants."""
    if not st.session_state.get(f"{prefix}_siege_same_as_perso"):
        return
    src_line = st.session_state.get(f"{prefix}_{perso_oneline}")
    if src_line:
        st.session_state[f"{prefix}_{siege_oneline}"] = src_line
    for pf, sf in zip(perso_fields, siege_fields, strict=True):
        src = st.session_state.get(f"{prefix}_{pf}")
        if src:
            st.session_state[f"{prefix}_{sf}"] = src


def siege_same_as_perso_checkbox(prefix: str) -> bool:
    """Case « Siege social = adresse personnelle » (anti double-saisie). A rendre a
    l'emplacement du siege ; la recopie effective est faite par seed_siege_from_perso
    en haut du render (au run suivant)."""
    key = f"{prefix}_siege_same_as_perso"
    if key not in st.session_state:
        st.session_state[key] = False
    return st.checkbox(
        "Siège social = adresse personnelle",
        key=key,
        help="Coché : recopie l'adresse personnelle dans le siège (évite la double saisie).",
    )


def mandataire_inputs(prefix: str) -> tuple[str, str]:
    """Saisie du conseiller/mandataire SYDEL, editable (defaut « Jordan ELBAZ »,
    ratifie Albane 2026-06-10 ; parite gold shell.py:1543-1565). Seede les valeurs
    par defaut, rend 2 champs (prenom / nom), retourne (prenom, nom) avec repli sur
    le defaut. Cle a passer ensuite a cc.default_mandataire(prenom, nom)."""
    prenom_key = f"{prefix}_mandataire_prenom"
    nom_key = f"{prefix}_mandataire_nom"
    if not st.session_state.get(prenom_key):
        st.session_state[prenom_key] = DEFAULT_MANDATAIRE_PRENOM
    if not st.session_state.get(nom_key):
        st.session_state[nom_key] = DEFAULT_MANDATAIRE_NOM
    col_a, col_b = st.columns(2)
    # O24-04 : icône « copier » sur les champs Conseiller (re-Akainu O24-04, MAJEUR M1).
    prenom = copyable_text_input(col_a, "Conseiller (prénom)", key=prenom_key)
    nom = copyable_text_input(col_b, "Conseiller (nom)", key=nom_key)
    return (prenom or DEFAULT_MANDATAIRE_PRENOM, nom or DEFAULT_MANDATAIRE_NOM)
