from __future__ import annotations

import random

import pytest


@pytest.fixture(autouse=True)
def _deterministic_test_env(tmp_path, monkeypatch):
    """Rend l'environnement de test DETERMINISTE par test (re-Akainu tours 7-9, flakiness).

    Deux sources de fragilite cross-test, neutralisees par CONSTRUCTION (pas par incantation) :
    1. `shell.ARTIFACTS_DIR` est un chemin RELATIF REEL (« artifacts/track_b_selarl_v1 ») ou de
       nombreux AppTest ecrivent leurs DOCX SANS isolation. CAUSE CERTAINE de collision cross-test
       (chemin partage, ecritures reelles) : on le redirige vers `tmp_path` (unique par test). Lu
       comme global au call-time (shell.py) -> le monkeypatch mord.
    2. `_prefill_random_selarl_data` (shell.py) tire des donnees via le module `random` GLOBAL
       NON seede. CAUSE PLAUSIBLE (non formellement isolee : la flakiness ~1/16 observee n'a PAS
       ete reproduite en controle negatif sans seed) d'une dependance a l'ORDRE / au nombre
       d'appels amont. On RESEED `random` a 0 AVANT chaque test : neutralisation robuste par
       construction, quel que soit l'ordre de collecte.

    PREUVE d'ordre-independance (T9) : la suite est verte sur 4 ORDRES de collecte DISTINCTS
    (pytest-randomly, seeds 1/2/3 + ordre par defaut, 593 verts chacun) -- ce qui prouve
    l'independance a l'ordre, contrairement aux runs « N fois a ordre constant » (qui ne
    prouvaient que la stabilite, pas l'ordre-independance). pytest-randomly est en dep dev :
    l'ordre est desormais randomise par defaut a chaque run.

    (Le monkeypatch de `ui_runtime.DEFAULT_ARTIFACTS_DIR` a ete retire : inerte -- la constante
    est liee en valeur par defaut d'argument de `build_output_dir`, sans appelant dans src/.)"""
    random.seed(0)

    import sydel_doc_engine.front_app.shell as shell

    base = tmp_path / "artifacts"
    base.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", base / "track_b_selarl_v1", raising=False)
