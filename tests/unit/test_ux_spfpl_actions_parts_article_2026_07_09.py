"""Retours Rafael 2026-07-09 (soir) — 2 cases front SPFPL cession.

N1 (note d'information — actions vs parts) : selon que la societe cible emet des
ACTIONS (SELAS) ou des PARTS SOCIALES (SELARL), les docs doivent employer le bon
terme. La forme de la cible etant un champ TEXTE LIBRE (non deterministe), on ajoute
une saisie explicite (selectbox « Titres emis par la societe cible », defaut « parts
sociales »). Elle alimente le champ canon `operation_spfpl.nature_titres`.

C4 (PV agrement — n° article capital SEL) : le n° d'article « 7 bis » sortait en dur
dans la 2e resolution du PV. On ajoute un champ front saisissable (defaut « 7 bis »),
passe au generateur via `ctx.metadata["pv_article_capital_numero"]`.

PERIMETRE = FRONT uniquement (spfpl_slice) : le front pose la saisie + le payload +
le champ de contexte ; le basculement de vocabulaire parts<->actions dans la note /
le PV et la lecture de metadata sont a la charge du generateur (autre agent). Ces
tests prouvent le CABLAGE front->payload->contexte, le defaut byte-neutre, et la
presence des widgets en session Streamlit reelle (AppTest).
"""

from __future__ import annotations

from pathlib import Path

from sydel_doc_engine.front_app import spfpl_slice

# Reutilise le payload SPFPL canon + le lecteur de texte docx deja eprouves.
from tests.unit.test_multi_type_front import _docx_text, _spfpl_payload

PREFIX = "spfpl_cession"


# --------------------------------------------------------------- N1 : nature titres


def test_nature_titres_defaut_parts_sociales_byte_neutre() -> None:
    # Payload canon (sans `cible_nature_titres`) -> defaut « parts sociales » : le champ
    # canon est renseigne mais « != actions » reste vrai -> selection de documents et
    # sortie inchangees (le generateur echoue encore « parts »).
    ctx = spfpl_slice.build_generation_context(_spfpl_payload("SPFPL cession"))
    assert ctx.operation_spfpl is not None
    assert ctx.operation_spfpl.nature_titres == "parts sociales"


def test_nature_titres_actions_portee_sur_operation_spfpl() -> None:
    # La saisie « actions » (cible SELAS) est portee sur `operation_spfpl.nature_titres`
    # = le champ que la selection de documents (orchestrateur) et les generateurs lisent.
    payload = _spfpl_payload("SPFPL cession")
    payload["cible_nature_titres"] = "actions"
    ctx = spfpl_slice.build_generation_context(payload)
    assert ctx.operation_spfpl.nature_titres == "actions"


def test_nature_titres_apport_reutilise_la_nature_apportee() -> None:
    # En apport, les titres apportes SONT ceux de la cible : la nature est portee par
    # `apport_nature_titres` (deja saisi) -> reutilisee sur operation_spfpl.nature_titres.
    payload = _spfpl_payload("SPFPL apport")
    payload["cible_nature_titres"] = "actions"  # ce que poserait render_spfpl_form
    ctx = spfpl_slice.build_generation_context(payload)
    assert ctx.operation_spfpl.nature_titres == "actions"


# ------------------------------------------------------------- C4 : n° article capital


def test_article_capital_defaut_7_bis_dans_metadata() -> None:
    # Sans saisie -> defaut « 7 bis » (comportement historique) passe en metadata.
    ctx = spfpl_slice.build_generation_context(_spfpl_payload("SPFPL cession"))
    assert ctx.metadata.get("pv_article_capital_numero") == "7 bis"


def test_article_capital_saisi_passe_en_metadata() -> None:
    # Un n° d'article saisi (cession_data) est transmis au generateur via metadata.
    payload = _spfpl_payload("SPFPL cession")
    payload["cession_data"] = {**payload["cession_data"], "article_capital_numero": "8 ter"}
    ctx = spfpl_slice.build_generation_context(payload)
    assert ctx.metadata.get("pv_article_capital_numero") == "8 ter"


# --------------------------------------------- M1 : qualite du president = realite de la cible


def test_president_qualite_reflects_cible_associate_count() -> None:
    """M1 (Akainu doc-entier 2026-07-09) : la qualite du president de seance (PV agrement)
    reflete la CIBLE. Le payload canon (2 associes reels -> DOC-039 plusieurs) rend « associé »
    generique (« associé unique » y serait CONTRADICTOIRE) ; une cible a 1 associe reel
    (DOC-038) rend « associé unique »."""
    ctx_multi = spfpl_slice.build_generation_context(_spfpl_payload("SPFPL cession"))
    assert ctx_multi.reunion.president.qualite == "associé"

    payload_unique = _spfpl_payload("SPFPL cession")
    payload_unique["cession_data"] = {
        **payload_unique["cession_data"],
        "associes": [
            {
                "civilite": "Monsieur", "prenom": "Camille", "nom": "Martin",
                "avant": 100, "apres": 40, "plage": "1 a 40",
            },
        ],
    }
    ctx_unique = spfpl_slice.build_generation_context(payload_unique)
    assert ctx_unique.reunion.president.qualite == "associé unique"


def test_bundle_cession_defaut_inchange(tmp_path: Path) -> None:
    # Preuve byte-neutre du cote FRONT : avec les defauts (parts sociales / 7 bis), le PV
    # d'agrement genere contient toujours « 7 bis » et « parts sociales » (le generateur
    # echoue encore ces valeurs en dur — non touche par ce ticket).
    genere = spfpl_slice.generate_dossier(_spfpl_payload("SPFPL cession"), tmp_path / "def")
    pv = next(_docx_text(p) for p in genere.docx_paths if "agrement" in p.name)
    assert "7 bis" in pv
    assert "parts sociales" in pv


# ----------------------------------------------- cablage render sous-formulaire cession


def test_render_cession_cible_retourne_article_capital(monkeypatch) -> None:
    # Le sous-formulaire cession expose le n° d'article dans cession_data (defaut « 7 bis »
    # applique meme si le seed amont — render_spfpl_form — n'a pas tourne dans ce stub).
    from tests.unit.test_ux_repartition_spfpl_2026_07_07 import (
        _session_cession_deux_associes,
        _stub_render_cession,
    )

    data, stub = _stub_render_cession(_session_cession_deux_associes(), monkeypatch)
    assert data["article_capital_numero"] == "7 bis"
    assert f"{PREFIX}_pv_article_capital_numero" in stub.widget_keys


# --------------------------------------------------------------- session reelle (AppTest)


def test_apptest_spfpl_cession_widgets_nature_et_article(tmp_path: Path, monkeypatch) -> None:
    """Session Streamlit REELLE : le flux SPFPL cession expose la selectbox actions/parts
    (defaut « parts sociales ») et le champ n° d'article (defaut « 7 bis »)."""
    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app import shell

    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui-spfpl-actions-parts")
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SPFPL dentistes - cession creation V1")
    app = app.run(timeout=180)
    next(b for b in app.button if "test_data" in str(b.key)).click()
    app = app.run(timeout=180)

    # N1 : la selectbox actions/parts existe, defaut « parts sociales ».
    assert app.session_state["spfpl_cession_cible_nature_titres"] == "parts sociales"
    # C4 : le champ n° d'article existe, defaut « 7 bis ».
    assert "spfpl_cession_pv_article_capital_numero" in {str(w.key) for w in app.text_input}
    assert app.session_state["spfpl_cession_pv_article_capital_numero"] == "7 bis"

    # Basculer la nature en « actions » + renseigner un autre n° d'article.
    next(
        w for w in app.selectbox if str(w.key) == "spfpl_cession_cible_nature_titres"
    ).set_value("actions")
    next(
        w for w in app.text_input if str(w.key) == "spfpl_cession_pv_article_capital_numero"
    ).set_value("9 bis")
    app = app.run(timeout=180)

    assert app.session_state["spfpl_cession_cible_nature_titres"] == "actions"
    assert app.session_state["spfpl_cession_pv_article_capital_numero"] == "9 bis"


def test_apptest_spfpl_apport_pas_de_double_selecteur_nature(tmp_path: Path, monkeypatch) -> None:
    """En APPORT, la nature des titres est deja saisie (« Nature des titres apportes ») :
    on ne rend PAS un second selecteur `cible_nature_titres` (source unique)."""
    from streamlit.testing.v1 import AppTest

    from sydel_doc_engine.front_app import shell

    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui-spfpl-apport-nature")
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=180)
    app.selectbox(key="clean_dossier_type").set_value("SPFPL dentistes - apport creation V1")
    app = app.run(timeout=180)

    selectbox_keys = {str(w.key) for w in app.selectbox}
    assert "spfpl_apport_cible_nature_titres" not in selectbox_keys
    assert "spfpl_apport_apport_nature_titres" in selectbox_keys
