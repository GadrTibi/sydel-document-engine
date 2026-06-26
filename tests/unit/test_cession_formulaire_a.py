"""Lot « Formulaire-A » (Albane) — préremplissages déterministes + bugs front cession.

Couvre, contre le verbatim Albane, les items FA1-FA7 (préremplissages déterministes du
sous-formulaire cession partagé SELARL/SELAS : financement, prêt, crédit-vendeur, SCM,
date limite) et FB1-FB3 (bugs front du compromis médical : département de naissance,
origine de propriété, double slash de date).

Les tests de défauts pilotent le VRAI front (streamlit AppTest) sur le parcours SELAS
pluripersonnel — exactement le parcours qu'Albane testait — pour PROUVER les valeurs
par défaut réellement câblées (pas une paraphrase). Les tests de bout en bout régénèrent
les DOCX et vérifient le texte produit.
"""

from __future__ import annotations

import re
import zipfile
from datetime import date
from pathlib import Path

from sydel_doc_engine.front_app import shell

# ---------------------------------------------------------------------------
# Helper pur : _add_months (support du préremplissage FA5 « +6 mois »).
# ---------------------------------------------------------------------------


def test_add_months_six_mois_simple() -> None:
    # FA5 : « +6 mois de la date des actes ». 15/05/2026 -> 15/11/2026.
    assert shell._add_months(date(2026, 5, 15), 6) == date(2026, 11, 15)


def test_add_months_traverse_annee() -> None:
    # +6 mois qui franchit l'année (octobre -> avril N+1).
    assert shell._add_months(date(2026, 10, 31), 6) == date(2027, 4, 30)


def test_add_months_clamp_fin_de_mois() -> None:
    # 31 août + 6 mois -> 28 février (clamp dernier jour du mois cible, pas de crash).
    assert shell._add_months(date(2025, 8, 31), 6) == date(2026, 2, 28)


# ---------------------------------------------------------------------------
# Défauts du sous-formulaire cession via le VRAI front (AppTest, parcours SELAS).
# ---------------------------------------------------------------------------


def _docx_text(path: Path) -> str:
    raw = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8", "ignore")
    return re.sub(r"<[^>]+>", "", raw)


def _selas_cession_app():
    """Parcours SELAS pluripersonnel avec sous-formulaire cession ouvert."""
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/sydel_doc_engine/front_app/app.py").run(timeout=200)
    app.selectbox(key="clean_dossier_type").set_value(
        "SELAS pluripersonnelle creation V1"
    )
    app = app.run(timeout=200)
    next(b for b in app.button if "test_data" in str(b.key)).click()
    app = app.run(timeout=200)
    app.checkbox(key="selas_cession_on").set_value(True)
    return app.run(timeout=200)


def _ss(app, key: str):
    try:
        return app.session_state[key]
    except Exception:  # noqa: BLE001 — clé absente du state = valeur non câblée.
        return None


def test_pret_taux_defaut_5_5(monkeypatch, tmp_path) -> None:
    # FA2 : « taux du prêt : toujours mettre 5,5 % ».
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui")
    app = _selas_cession_app()
    assert _ss(app, "selas_cession_financement_pret_taux") == "5,5 %"


def test_pret_duree_defaut_10_ans(monkeypatch, tmp_path) -> None:
    # FA3 : « durée du prêt : toujours mettre 10 ans ».
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui")
    app = _selas_cession_app()
    assert _ss(app, "selas_cession_financement_pret_duree") == "10 ans"


def test_pret_montant_egal_prix_de_cession(monkeypatch, tmp_path) -> None:
    # FA1 : « montant du prêt (compromis) = prix de cession ». Le montant suit le prix
    # total saisi (auto, modifiable).
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui")
    app = _selas_cession_app()
    app.text_input(key="selas_cession_prix_total").set_value("300000")
    app = app.run(timeout=200)
    montant = _ss(app, "selas_cession_financement_pret_montant")
    # Formaté en groupes (« 300 000 ») comme le prix.
    assert montant.replace(" ", " ").replace("\xa0", " ") == "300 000"


def test_date_limite_realisation_plus_6_mois_sans_double_slash(
    monkeypatch, tmp_path
) -> None:
    # FA5 : date limite de réalisation = date des actes + 6 mois (préremplie, modifiable).
    # FB3 : aucune « barre en plus » (« 01/01//2027 ») — format propre JJ/MM/AAAA.
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui")
    app = _selas_cession_app()
    signature = _ss(app, "selas_signature_date")  # « JJ/MM/AAAA »
    date_limite = _ss(app, "selas_cession_meta_date_limite")
    assert "//" not in date_limite, f"double slash résiduel : {date_limite!r}"
    # Vérifie le +6 mois exact à partir de la date des actes affichée.
    d, m, y = (int(p) for p in signature.split("/"))
    attendu = shell.format_french_date(shell._add_months(date(y, m, d), 6))
    assert date_limite == attendu


def test_montant_deblocage_minimum_vide_par_defaut(monkeypatch, tmp_path) -> None:
    # FA6 : « montant de déblocage mini : si c'est pour l'appel de fonds il faut aussi
    # que cela reste vierge ».
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui")
    app = _selas_cession_app()
    assert (_ss(app, "selas_cession_financement_deblocage") or "") == ""


def test_majoration_interet_retard_credit_vendeur_sans_champ(
    monkeypatch, tmp_path
) -> None:
    # FA4 : « il n'y a pas de variable à mettre » — plus AUCUN champ de saisie pour la
    # majoration d'intérêts de retard du crédit-vendeur.
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", tmp_path / "ui")
    app = _selas_cession_app()
    keys = {str(w.key) for w in app.text_input}
    assert not any("credit_majoration" in k for k in keys), (
        "FA4 : la majoration d'intérêts de retard ne doit plus être saisie."
    )


# ---------------------------------------------------------------------------
# Bouts en bout : régénération réelle des DOCX cession médicale (FB1/FB2/FA4).
# ---------------------------------------------------------------------------


def _generate_cession_medicale(app, tmp_path):
    """Remplit les champs requis de la cession médicale et génère le dossier."""

    def setv(key: str, value: str) -> None:
        app.text_input(key=key).set_value(value)

    setv("selas_cession_cabinet_origine_date", "01/01/2020")
    setv("selas_cession_prix_total", "300000")
    setv("selas_cession_prix_corporels", "50000")
    setv("selas_cession_prix_incorporels", "250000")
    for i in range(3):
        setv(f"selas_cession_exercice_{i}_ca", "200000")
        setv(f"selas_cession_exercice_{i}_resultat", "50000")
    setv("selas_cession_financement_credit_montant", "60000")
    setv("selas_cession_financement_credit_duree", "trois")
    setv("selas_cession_financement_credit_taux", "5")
    app = app.run(timeout=200)
    next(b for b in app.button if b.key == "clean_typed_generate_dossier").click()
    return app.run(timeout=200)


def _docx(tmp_path: Path, glob_pat: str) -> Path | None:
    matches = list(tmp_path.glob(f"**/{glob_pat}"))
    return matches[0] if matches else None


def test_compromis_departement_naissance_pas_france(monkeypatch, tmp_path) -> None:
    # FB1 : « né le ... à Lyon (France) » — la parenthèse doit être le DÉPARTEMENT (« 69 »),
    # pas « France ». Le compromis médical rend [pays_naissance_vendeur] dans la parenthèse :
    # on y câble le département. Le test_data SELAS pose le département « 69 ».
    artefacts = tmp_path / "ui"
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", artefacts)
    app = _selas_cession_app()
    app = _generate_cession_medicale(app, artefacts)
    for e in app.error:
        assert "obligatoire" not in str(e.value), str(e.value)
    compromis = _docx(artefacts, "*compromis*cabinet*medical*.docx")
    assert compromis is not None, "compromis médical non généré"
    texte = _docx_text(compromis)
    # Le département est saisi (« 69 ») -> il ne doit JAMAIS y avoir « (France) » dans la
    # ligne de naissance.
    assert "Lyon (69)" in texte, "FB1 : la parenthèse doit porter le département (69)."
    assert "Lyon (France)" not in texte, (
        "FB1 : « (France) » au lieu du département dans la ligne de naissance."
    )


def test_origine_propriete_transmise_date_et_mode(monkeypatch, tmp_path) -> None:
    # FB2 : « sur l'origine de propriété tout a disparu, le paragraphe est totalement
    # vide, j'avais noté créé et mis une date » -> la date + le mode (créé) doivent être
    # transmis et la phrase d'origine apparaître.
    artefacts = tmp_path / "ui"
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", artefacts)
    app = _selas_cession_app()
    app = _generate_cession_medicale(app, artefacts)
    acte = _docx(artefacts, "*acte*cabinet*medical*.docx")
    assert acte is not None, "acte médical non généré"
    texte = _docx_text(acte)
    # Phrase d'origine non vide : « ... propriétaire des éléments constitutifs du cabinet
    # pour l'avoir régulièrement créé le <date>. »
    assert "régulièrement créé le" in texte, (
        "FB2 : la clause d'origine de propriété (mode créé + date) doit être transmise."
    )
    # Le paragraphe « Sur l'origine de propriété : » ne doit plus être suivi du vide.
    m = re.search(r"origine de propri[ée]t[ée]\s*:?\s*(.{0,40})", texte)
    assert m is not None and m.group(1).strip(), "FB2 : origine de propriété vide."


def test_acte_majoration_interet_retard_fixe_du_modele(monkeypatch, tmp_path) -> None:
    # FA4 : la valeur fixe du modèle (« majoré de 2 points ») sort sans saisie utilisateur.
    artefacts = tmp_path / "ui"
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", artefacts)
    app = _selas_cession_app()
    app = _generate_cession_medicale(app, artefacts)
    acte = _docx(artefacts, "*acte*cabinet*medical*.docx")
    assert acte is not None, "acte médical non généré"
    texte = _docx_text(acte)
    assert "majoré de 2 points" in texte, (
        "FA4 : la majoration fixe du modèle (« majoré de 2 points ») doit ressortir."
    )


# ---------------------------------------------------------------------------
# FA7 : prix global SCM mis « d'office en lettre » (comme la valeur nominale).
# ---------------------------------------------------------------------------


def test_scm_prix_global_en_lettres_auto() -> None:
    # FA7 : « SCM / prix : en mettant le prix global est-ce qu'il peut se mettre d'office
    # en lettre ? » -> le prix global en lettres = number_words_from_value(prix global),
    # le même helper que la valeur nominale calculée. On vérifie la dérivation déterministe
    # qui alimente prix['global_lettres'] dans _render_scm_cession_form.
    from sydel_doc_engine.front_app.field_derivations import number_words_from_value

    assert number_words_from_value("5000") == "cinq mille"
    assert number_words_from_value("5 000") == "cinq mille"
    # Cohérence avec ce que le formulaire injecte : global '12 000' -> 'douze mille'.
    assert number_words_from_value("12 000") == "douze mille"
