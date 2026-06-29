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
    DEFAULT_MANDATAIRE_NOM,
    DEFAULT_MANDATAIRE_PRENOM,
    format_french_date,
    parse_french_date,
)


def copyable_text_input(
    container, label: str, *, key: str | None = None, help: str | None = None, **text_input_kwargs
) -> str:
    """`text_input` SIMPLE (l'icône « copier » latérale a été RETIRÉE — FB-3 Albane 2026-06-26).

    Albane : « j'ai vu qu'il y avait des champs sur le côté pour copier le texte, est-ce possible
    de les retirer ? … avec le copier le tab passe dessus, ça rend la saisie moins fluide ». La
    colonne icône captait le focus de tabulation et cassait la fluidité de saisie. On revient donc
    à un `text_input` nu PARTOUT (le nom de la fonction et sa signature sont CONSERVÉS pour rester
    un drop-in : tous les appelants existants — y compris ceux sans `key`, avec `value=`/`disabled=`
    via `**text_input_kwargs` — continuent de fonctionner à l'identique, sans la colonne copier).
    """
    return container.text_input(label, key=key, help=help, **text_input_kwargs)


def date_input_with_today(
    label: str,
    *,
    key: str,
    value: date,
    container=None,
    seed: bool = True,
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

    `seed` (defaut True) : pre-remplit la cle texte avec `value` si elle est vide.
    Le mettre a False pour un champ qui NE doit PAS afficher de valeur par defaut
    (ex. date de NAISSANCE : « aujourd'hui » serait une fausse date) — le champ reste
    vide tant que l'utilisateur n'a pas tape, choisi au calendrier ou clique
    « Aujourd'hui ». La saisie texte JJ/MM/AAAA reste la source editable dans tous les
    cas, donc la saisie verbatim francaise (« 1er aout 1985 ») reste possible (R29-06)."""
    target = container if container is not None else st

    current_value = st.session_state.get(key)
    if isinstance(current_value, date):
        st.session_state[key] = format_french_date(current_value)
    elif current_value is None and seed:
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

    # N2 (Rafael 2026-06-24) : le libelle du calendrier est REPLIE (label_visibility="collapsed")
    # pour ne PAS afficher le nom du champ DEUX fois (« X (calendrier) » au-dessus de « X »). Un
    # seul libelle visible (sur le champ texte editable) ; le calendrier reste un selecteur discret
    # juste au-dessus. Propage a TOUS les champs date (helper partage).
    target.date_input(
        f"{label} (calendrier)",
        value=None,
        key=cal_key,
        format="DD/MM/YYYY",
        on_change=_sync_from_calendar,
        label_visibility="collapsed",
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
    """SU3 (Albane 2026-06-25) : la ville de signature EST la ville du siege DANS TOUS LES CAS,
    partout dans le moteur. On la FORCE (= siege, on ecrase toute valeur divergente) des que la
    ville du siege est connue : plus une simple pre-saisie modifiable, c'est un invariant.
    Le champ signature_lieu doit donc etre rendu en lecture seule (derive)."""
    if ville_siege:
        st.session_state[f"{prefix}_{field}"] = ville_siege


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
