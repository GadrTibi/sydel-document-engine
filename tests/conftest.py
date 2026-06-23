from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _isolate_artifacts_dir(tmp_path, monkeypatch):
    """Isole le repertoire d'artefacts de generation PAR test (re-Akainu tour 7, MAJEUR flakiness).

    `shell.ARTIFACTS_DIR` et `ui_runtime.DEFAULT_ARTIFACTS_DIR` sont des chemins RELATIFS REELS
    (« artifacts/... » au cwd). Beaucoup d'AppTest cliquent un bouton de generation et y ecrivent
    SANS isoler le dossier -> deux runs/tests qui le partagent provoquent des echecs NON
    deterministes (ZipBundleError « fichier introuvable », bundle incomplet) quand un fichier est
    ecrase/supprime entre la generation et la mise en ZIP. On redirige ces dossiers vers `tmp_path`
    (unique par test) pour rendre la suite DETERMINISTE. Les tests qui monkeypatchent deja
    ARTIFACTS_DIR restent prioritaires (leur setattr ulterieur l'emporte ; restauration OK)."""
    import sydel_doc_engine.app.ui_runtime as ui_runtime
    import sydel_doc_engine.front_app.shell as shell

    base = tmp_path / "artifacts"
    base.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(shell, "ARTIFACTS_DIR", base / "track_b_selarl_v1", raising=False)
    monkeypatch.setattr(
        ui_runtime, "DEFAULT_ARTIFACTS_DIR", base / "ui_pdf_zip_integration_001", raising=False
    )
