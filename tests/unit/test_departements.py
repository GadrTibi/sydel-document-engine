"""Test unitaire du helper `departement_nom` (convention Albane 7.4/9.2 : le
departement de l'Ordre se rend en NOM, pas en numero).

Protege la logique de conversion contre une regression (Akainu DEPT m1) : sans ce
test, la suite resterait verte meme si `departement_nom` etait retire, car les
fixtures des generateurs passent deja des noms.
"""

from __future__ import annotations

import pytest

from sydel_doc_engine.utils.departements import departement_nom


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        # Numero metropole -> nom officiel INSEE.
        ("77", "Seine-et-Marne"),
        ("75", "Paris"),
        # Padding numero a un chiffre « 7 » -> « 07 » -> nom.
        ("7", "Ardèche"),
        ("07", "Ardèche"),
        # Corse (2A/2B, insensible a la casse).
        ("2A", "Corse-du-Sud"),
        ("2a", "Corse-du-Sud"),
        ("2B", "Haute-Corse"),
        # DROM.
        ("971", "Guadeloupe"),
        ("974", "La Réunion"),
        # Passthrough robuste : un nom deja correct n'est jamais detruit (idempotence).
        ("Paris", "Paris"),
        ("Seine-et-Marne", "Seine-et-Marne"),
        ("Rhône", "Rhône"),
        # Code inconnu -> renvoye tel quel (jamais de perte silencieuse).
        ("99", "99"),
        # Valeur vide / None -> chaine vide (l'appelant reste maitre de la validation).
        ("", ""),
        ("   ", ""),
        (None, ""),
    ],
)
def test_departement_nom(value: str | None, expected: str) -> None:
    assert departement_nom(value) == expected


def test_departement_nom_is_idempotent_on_converted_name() -> None:
    # Convertir deux fois ne re-detruit pas le nom (garde-fou contre une double conversion).
    once = departement_nom("77")
    assert departement_nom(once) == once == "Seine-et-Marne"
