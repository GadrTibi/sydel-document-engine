"""Retours Albane (Direction Juridique SYDEL) — email 2026-07-09, création MICRO-HOLDING.

Volet FRONT/UX uniquement (les items DOCUMENTS/PV sont traités ailleurs). Chaque test
verrouille un retour A1..A7 par un AppTest Streamlit RÉEL sur le parcours micro-holding
(société civile à capital variable, socle civil partagé) + quelques helpers purs.

Carnet : docs/returns/CARNET_ALBANE_MAIL_2026-07-09.md
A8 (assouplir des blocages) : NON traité ici — bloqué par des dépendances dures des
générateurs (`_required_text` sur banque_adresse / situation_maritale) + le conflit métier
DNC en attente (B7). Voir le rapport de livraison.
"""

from __future__ import annotations

from streamlit.testing.v1 import AppTest

from sydel_doc_engine.front_app.civil_statuts_slice import _split_cp_ville
from sydel_doc_engine.front_app.field_derivations import derive_parts_from_apport

ADDR = "10 rue de la Paix, 75002 Paris"


# --- helpers AppTest ---------------------------------------------------------


def _load_micro() -> AppTest:
    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=240)
    app.selectbox(key="clean_dossier_type").set_value("Micro holding")
    return app.run(timeout=240)


def _ti(app: AppTest) -> dict:
    return {str(w.key): w for w in app.text_input}


def _ni(app: AppTest) -> dict:
    return {str(w.key): w for w in app.number_input}


def _cb(app: AppTest) -> dict:
    return {str(w.key): w for w in app.checkbox}


# --- A1 : date de clôture — retirer le hint « Format attendu : JJ/MM/AAAA » ----


def test_a1_no_jjmmaaaa_hint_on_free_form_closing_date() -> None:
    # Le champ de clôture est pré-rempli « 31 décembre N+1 » (mois TEXTUEL, non parsable en
    # JJ/MM/AAAA). L'ancien widget affichait alors « Format attendu : JJ/MM/AAAA » (incohérent).
    app = _load_micro()
    captions = [str(c.value) for c in app.caption]
    assert not any("Format attendu" in c for c in captions), captions


# --- A2 (BUG) : « siège = adresse perso » remplit le siège, quel que soit l'ordre -


def test_a2_box_checked_before_address_still_fills_siege() -> None:
    # Bug A2 : cocher la case AVANT de saisir l'adresse (flux naturel — la case est en haut,
    # l'adresse de l'associé plus bas) ne remplissait JAMAIS le siège. Doit désormais le remplir.
    app = _load_micro()
    _cb(app)["micro_holding_siege_same_as_perso"].set_value(True)
    app = app.run(timeout=240)
    _ti(app)["micro_holding_associe_0_adresse"].set_value(ADDR)
    app = app.run(timeout=240)
    assert _ti(app)["micro_holding_siege_adresse"].value == ADDR


def test_a2_address_before_box_still_fills_siege() -> None:
    # Non-régression de l'ordre historique (adresse saisie, puis case cochée).
    app = _load_micro()
    _ti(app)["micro_holding_associe_0_adresse"].set_value(ADDR)
    app = app.run(timeout=240)
    _cb(app)["micro_holding_siege_same_as_perso"].set_value(True)
    app = app.run(timeout=240)
    assert _ti(app)["micro_holding_siege_adresse"].value == ADDR


# --- A3 : nb de parts dérivé de l'apport (apport / valeur nominale) ------------


def test_a3_derive_parts_from_apport_pure_helper() -> None:
    assert derive_parts_from_apport("400", "10") == 40
    assert derive_parts_from_apport("1000", "1") == 1000
    assert derive_parts_from_apport("1000", "1,25") == 800  # valeur nominale décimale
    # Non dérivable -> None (on laisse la saisie manuelle).
    assert derive_parts_from_apport("400", "") is None
    assert derive_parts_from_apport("", "10") is None
    assert derive_parts_from_apport("400", "0") is None


def test_a3_nb_parts_readonly_when_derivable() -> None:
    # capital 1000 + nb parts total 100 -> valeur nominale = 10 ; apport 400 -> 40 parts (RO).
    app = _load_micro()
    _ni(app)["micro_holding_capital_social"].set_value(1000)
    app = app.run(timeout=240)
    _ni(app)["micro_holding_nb_parts_total"].set_value(100)
    app = app.run(timeout=240)
    _ti(app)["micro_holding_associe_0_apport_montant"].set_value("400")
    app = app.run(timeout=240)
    nb = _ni(app)["micro_holding_associe_0_nb_titres"]
    assert nb.value == 40
    assert nb.disabled is True


def test_a3_nb_parts_manual_when_valeur_nominale_unknown() -> None:
    # Sans capital/nb parts total (valeur nominale inconnue), le champ reste éditable.
    app = _load_micro()
    nb = _ni(app)["micro_holding_associe_0_nb_titres"]
    assert nb.disabled is False


# --- A4 : « Département de naissance (ou pays si étranger) » -------------------


def test_a4_departement_label_mentions_pays_etranger() -> None:
    app = _load_micro()
    labels = [str(w.label) for w in app.text_input]
    assert any("ou pays si étranger" in label for label in labels), labels


# --- A5 : fonction pré-remplie « gérant » + libellé titre clarifié ------------


def test_kan39_fonction_and_titre_fields_removed_from_micro() -> None:
    # KAN-39 (Rafael 2026-07-27) SUPERSEDE A5 : les champs « Fonction (ex : gérant) » et « Titre
    # professionnel affiché (ex : Docteur) » sont RETIRES du formulaire micro-holding (inutiles :
    # la fonction est definie par la case « Dirigeant », le titre affiche n'a pas d'interet ici).
    # La fonction reste « gérant » (avec accent) par defaut cote generation, sans champ de saisie.
    app = _load_micro()
    keys = [str(w.key) for w in app.text_input]
    assert "micro_holding_signataire_fonction" not in keys, keys
    labels = [str(w.label) for w in app.text_input]
    assert not any("Titre professionnel affiché" in label for label in labels), labels
    assert not any(label.startswith("Fonction") for label in labels), labels


# --- A6 : lettre d'option IS toujours présente (case retirée) pour la micro ----


def test_a6_micro_option_is_always_on_no_checkbox() -> None:
    app = _load_micro()
    cb_keys = [str(w.key) for w in app.checkbox]
    # La case « option IS » n'existe plus pour la micro (générée systématiquement).
    assert "micro_holding_option_is" not in cb_keys
    # Les champs du destinataire (lettre DOC-022) sont bien affichés d'emblée.
    ti_keys = [str(w.key) for w in app.text_input]
    assert "micro_holding_impots_service" in ti_keys


# --- A7 : CP + Ville regroupés sur une seule ligne ----------------------------


def test_a7_split_cp_ville_pure_helper() -> None:
    assert _split_cp_ville("75002 Paris") == ("75002", "Paris")
    assert _split_cp_ville("54000 NANCY") == ("54000", "NANCY")
    assert _split_cp_ville("Paris") == ("", "Paris")  # sans CP -> tout en ville
    assert _split_cp_ville("") == ("", "")


def test_a7_single_cp_ville_field_in_impots_block() -> None:
    app = _load_micro()
    ti_keys = [str(w.key) for w in app.text_input]
    assert "micro_holding_impots_cp_ville" in ti_keys  # champ unique regroupé
    assert "micro_holding_impots_cp" not in ti_keys  # anciens champs séparés retirés
    assert "micro_holding_impots_ville" not in ti_keys
