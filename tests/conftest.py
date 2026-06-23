from __future__ import annotations

import random

import pytest


@pytest.fixture(autouse=True)
def _deterministic_test_env(tmp_path, monkeypatch):
    """Rend l'environnement de test DETERMINISTE par test (re-Akainu tours 7-8, flakiness).

    Deux sources de non-determinisme cross-test prouvees par l'audit independant :
    1. `shell.ARTIFACTS_DIR` est un chemin RELATIF REEL (« artifacts/track_b_selarl_v1 ») ou de
       nombreux AppTest ecrivent leurs DOCX SANS isolation -> collisions cross-test
       (ZipBundleError « fichier introuvable », bundle incomplet). On le redirige vers `tmp_path`
       (unique par test). Lu comme global au call-time (shell.py) -> le monkeypatch mord.
    2. `_prefill_random_selarl_data` (shell.py) tire des donnees via le module `random` GLOBAL
       NON seede ; plusieurs tests cliquent le bouton « donnees de test » -> le flux random
       depend de l'ORDRE / du nombre d'appels amont, rendant certains tests ORDER-DEPENDENT
       (ex. O24-11 regime accentue dans l'acte SCM, flaky ~1/16 en suite complete). On RESEED
       `random` a 0 AVANT chaque test pour fixer le flux quel que soit l'ordre de collecte.

    (Le monkeypatch de `ui_runtime.DEFAULT_ARTIFACTS_DIR` a ete retire : inerte -- la constante
    est liee en valeur par defaut d'argument de `build_output_dir`, sans appelant dans src/.)"""
    random.seed(0)

    import sydel_doc_engine.front_app.shell as shell

    base = tmp_path / "artifacts"
    base.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", base / "track_b_selarl_v1", raising=False)
