# DEPLOY-STREAMLIT-CLOUD-FIX-001 - Rapport v1

## Erreur cloud observee

Streamlit Cloud echoue pendant l'installation Poetry du projet avec l'erreur :

```text
The current project could not be installed: No file/folder found for package sydel-document-engine
```

## Cause racine

Le nom du projet Python est `sydel-document-engine`, mais le package source reel est
`src/sydel_doc_engine`.

Poetry tente d'installer le projet comme package et deduit un nom de package depuis le nom
projet. Sans declaration explicite, il ne trouve pas de dossier correspondant a
`sydel-document-engine`.

## Changement effectue

Le fichier `pyproject.toml` declare maintenant explicitement le package Poetry :

```toml
[tool.poetry]
packages = [
  { include = "sydel_doc_engine", from = "src" },
]
```

Aucun changement de logique metier, d'UI, de moteur DOCX/PDF/ZIP ou de dependance LibreOffice
n'a ete effectue.

## Tests lances

- `.\.venv\Scripts\python.exe -m pip install -e .`
- `.\.venv\Scripts\python.exe -m ruff check .`
- `.\.venv\Scripts\python.exe -m pytest`
- Verification disponibilite Poetry :
  - `Get-Command poetry -ErrorAction SilentlyContinue`
  - `.\.venv\Scripts\python.exe -m poetry --version`

## Resultat des tests

- Installation editable locale : OK.
- Ruff : OK, `All checks passed!`.
- Pytest : OK, 196 tests passes.
- Poetry local : non disponible en commande globale et non installe dans la venv ; `poetry check`
  et `poetry install` n'ont donc pas pu etre executes localement.

## Prochaine etape

Pousser le commit, puis redemarrer / reboot l'application Streamlit Cloud pour relancer
l'installation Poetry avec le package explicitement declare.
