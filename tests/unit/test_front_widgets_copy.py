"""Contrat du helper « copier » O24-04 (re-Akainu O24-04, NITPICK n3).

Verrouille les 2 propriétés de sûreté que l'audit a vérifiées à la main :
1. l'échappement HTML de la valeur (anti-injection / attribut non cassé) ;
2. le fallback propre vers un `text_input` simple (jamais de crash de formulaire).
"""

from __future__ import annotations

import pytest

from sydel_doc_engine.front_app.front_widgets import (
    _copy_button_html,
    copyable_text_input,
)


def test_copy_button_html_escapes_dangerous_value() -> None:
    # Valeur hostile : guillemets (cassent l'attribut), chevrons (<script>), esperluette.
    html = _copy_button_html('a" onmouseover="alert(1)" x="<script>&')
    # La valeur vit dans data-copy, entièrement échappée.
    assert 'data-copy="' in html
    # Aucun handler injecté ni balise brute ne survit.
    assert "onmouseover=\"alert" not in html
    assert "<script>" not in html
    # Les guillemets de la valeur sont échappés (&quot;), pas bruts.
    assert "&quot;" in html


def test_date_input_calendrier_label_collapsed_n2(monkeypatch: pytest.MonkeyPatch) -> None:
    # N2 (Rafael 2026-06-24, Akainu m1) : le date_input « calendrier » du helper partage doit etre
    # rendu avec label_visibility="collapsed" pour ne PAS afficher le libelle du champ deux fois.
    # Verrou : sans ce kwarg, le double libelle (« X (calendrier) » + « X ») reviendrait.
    from datetime import date

    from sydel_doc_engine.front_app import front_widgets

    captured: dict[str, object] = {}

    class _FakeTarget:
        def date_input(self, label: str, **kwargs: object) -> None:
            captured["label"] = label
            captured["label_visibility"] = kwargs.get("label_visibility")

        def button(self, *_a: object, **_k: object) -> bool:
            return False

        def text_input(self, _label: str, **_kwargs: object) -> str:
            return ""

    class _FakeSt:
        session_state: dict[str, object] = {}

    monkeypatch.setattr(front_widgets, "st", _FakeSt())
    front_widgets.date_input_with_today(
        "Date de decision", key="d_n2", value=date(2026, 1, 1), container=_FakeTarget()
    )

    # libelle du calendrier replie -> un seul libelle visible (sur le champ texte)
    assert captured["label_visibility"] == "collapsed"
    assert captured["label"] == "Date de decision (calendrier)"


class _StubNoColumns:
    """Conteneur minimal : `text_input` seulement (pas de `columns`)."""

    def __init__(self) -> None:
        self.text_input_called = False

    def text_input(self, _label: str, **_kwargs: object) -> str:
        self.text_input_called = True
        return "VALEUR"

    def columns(self, _spec: object):  # pragma: no cover - ne doit PAS être appelé sans key
        raise AssertionError("columns() ne doit pas être appelé quand key est None")


def test_copyable_text_input_without_key_falls_back_to_plain() -> None:
    stub = _StubNoColumns()
    # Sans key, on ne peut pas relire la valeur à copier -> text_input simple, pas de columns().
    assert copyable_text_input(stub, "Label") == "VALEUR"
    assert stub.text_input_called


class _StubColumnsRaise:
    """Conteneur dont `columns` lève (simule un nesting Streamlit trop profond)."""

    def text_input(self, _label: str, **_kwargs: object) -> str:
        return "REPLI"

    def columns(self, _spec: object):
        raise RuntimeError("Columns can only be nested one level deep")


def test_copyable_text_input_columns_failure_falls_back_to_plain() -> None:
    # Si columns() lève (nesting), on retombe sur text_input simple sans casser le formulaire.
    assert copyable_text_input(_StubColumnsRaise(), "Label", key="k") == "REPLI"
