"""Contrat du helper `copyable_text_input` APRES retrait de l'icone copier (FB-3 Albane
2026-06-26).

Albane : « j'ai vu qu'il y avait des champs sur le cote pour copier le texte, est-ce
possible de les retirer ? … avec le copier le tab passe dessus, ca rend la saisie moins
fluide ». Le widget est desormais un `text_input` SIMPLE (plus de colonne icone qui captait
le focus de tabulation). Ces tests verrouillent le NOUVEAU contrat :
1. plus de bouton/icone copier rendu (aucun appel `columns` ni `components.html`) ;
2. la signature reste un drop-in (avec/sans key, kwargs `value`/`disabled` transmis).
"""

from __future__ import annotations

import pytest

from sydel_doc_engine.front_app import front_widgets
from sydel_doc_engine.front_app.front_widgets import copyable_text_input


def test_copy_button_helper_removed_fb3() -> None:
    # FB-3 : le helper de bouton copier a ete retire du module (plus d'icone latérale).
    assert not hasattr(front_widgets, "_copy_button_html")


class _StubNoCopyWidget:
    """Conteneur qui FAIL si une colonne « copier » est rendue.

    `columns` lève (le helper ne doit plus jamais l'appeler pour une icône) et `text_input`
    renvoie une valeur fixe. Le module `components` ne doit pas non plus être sollicité."""

    def __init__(self) -> None:
        self.text_input_called = False

    def text_input(self, _label: str, **_kwargs: object) -> str:
        self.text_input_called = True
        return "VALEUR"

    def columns(self, _spec: object):  # pragma: no cover - ne doit PLUS être appelé
        raise AssertionError("columns() ne doit plus être appelé : icône copier retirée (FB-3)")


def test_copyable_text_input_no_copy_column_fb3() -> None:
    # FB-3 : avec une key, on rend quand même un text_input SIMPLE (pas de colonne copier).
    stub = _StubNoCopyWidget()
    assert copyable_text_input(stub, "Label", key="k") == "VALEUR"
    assert stub.text_input_called


def test_copyable_text_input_passes_kwargs_through_fb3() -> None:
    # Drop-in : value/disabled (sans key) sont transmis tels quels au text_input simple.
    captured: dict[str, object] = {}

    class _Stub:
        def text_input(self, label: str, **kwargs: object) -> str:
            captured["label"] = label
            captured.update(kwargs)
            return str(kwargs.get("value") or "")

    out = copyable_text_input(_Stub(), "Prix (calcule)", value="42", disabled=True)
    assert out == "42"
    assert captured["disabled"] is True
    assert captured["value"] == "42"
    assert captured["key"] is None


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


def test_seed_signature_lieu_force_la_ville_du_siege_su3(monkeypatch: pytest.MonkeyPatch) -> None:
    # SU3 (Albane 2026-06-25) : la ville de signature EST la ville du siege DANS TOUS LES CAS.
    # Le helper FORCE (ecrase toute valeur divergente) des que la ville du siege est connue.
    from sydel_doc_engine.front_app import front_widgets

    class _FakeSt:
        session_state: dict[str, object] = {"x_signature_lieu": "Lyon"}  # ville divergente saisie

    monkeypatch.setattr(front_widgets, "st", _FakeSt())
    front_widgets.seed_signature_lieu("x", "Paris")  # siege = Paris
    assert front_widgets.st.session_state["x_signature_lieu"] == "Paris"  # forcee = siege
    # Siege inconnu -> on ne touche pas (pas d'ecrasement par du vide).
    front_widgets.st.session_state["y_signature_lieu"] = "Marseille"
    front_widgets.seed_signature_lieu("y", "")
    assert front_widgets.st.session_state["y_signature_lieu"] == "Marseille"
