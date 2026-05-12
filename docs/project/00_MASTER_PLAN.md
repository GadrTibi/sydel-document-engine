# Plan maître — SYDEL Document Engine

## Objet
Construire un moteur documentaire juridique déterministe pour DAAT x SYDEL, versionné dans le dépôt et exploitable sans dépendre de la mémoire du chat.

Ce fichier fixe la mémoire opérationnelle globale : il doit permettre à un nouvel intervenant de comprendre ce qui est construit, dans quel ordre, avec quelles sources et avec quels garde-fous.

## Périmètre V1
- Génération DOCX propre.
- Conversion PDF.
- Constitution d'un ZIP dossier.
- Interface Streamlit simple pour piloter une génération dossier.
- Lot 1 uniquement au démarrage.
- Pas d'IA générative dans le moteur de production.
- Pas d'automatisation initiale des documents marqués "à remplir à la main".

## Source de vérité
- Source de vérité métier : `project/source_truth/Documents_a_generer_par_cas.docx`.
- Sources documentaires Lot 1 : `project/source_documents/lot_01/*`.
- Specs de livraison : `docs/delivery/`.
- L'arbre théorique abandonné n'est pas une source valide.
- Il n'existe pas de fichier séparé "Documents avec variables".

## Architecture retenue
- Le moteur est construit par document canonique, pas par cas métier.
- Le référentiel de départ reste par cas métier pour décider quels documents produire.
- L'orchestrateur dossier appelle les générateurs de documents canoniques selon le contexte.
- Chaque document automatisé dispose d'un générateur dédié.
- Les conditions générales et spécifiques sont explicites et testables.
- La génération DOCX cible des fichiers propres, reconstruits de manière déterministe.
- Les sorties cibles V1 sont : DOCX, PDF, ZIP.
- L'interface cible est une Streamlit simple, sans logique métier cachée dans l'UI.

## ADR applicables
- `docs/adr/0001-source-of-truth.md` : la source de vérité documentaire est le document Word métier.
- `docs/adr/0002-engine-per-document.md` : le moteur se construit par document canonique.
- `docs/adr/0003-lot-based-delivery.md` : la livraison se fait par lots documentaires.
- `docs/adr/0004-from-scratch-docx-generation.md` : les DOCX propres sont reconstruits plutôt que nettoyés en production.
- `docs/adr/0005-codex-working-mode.md` : le travail Codex doit rester repo-first, traçable et limité.

## Règles de travail
- ne pas coder un document sans source + analyse + spec
- ne pas réécrire implicitement un texte juridique
- travailler par petits tickets traçables
- documenter ce qui est fait et ce qui vient après
- garder l'Excel comme pilotage humain
- garder le Markdown du repo comme mémoire opérationnelle

## Phases
1. bootstrap technique du repo
2. mémoire projet versionnée dans le repo
3. implémentation Lot 1
4. orchestrateur Lot 1
5. Streamlit V0 Lot 1
6. lots documentaires suivants

## Etat actuel
- repo GitHub créé
- base poussée
- CI verte
- specs Lot 1 disponibles
- mémoire opérationnelle projet en cours d'installation dans `docs/project/`
- code métier Lot 1 non démarré

## Lot 1
- DOC-001 : Déclaration sur l'honneur de non-condamnation
- DOC-002 : Autorisation de domiciliation
- DOC-003 : Procuration

## Entrées nécessaires avant codage d'un document
- Le document doit être inventorié dans la source de vérité.
- La source documentaire correspondante doit être reçue.
- Une analyse et une spec doivent exister dans `docs/delivery/`.
- Les variables obligatoires doivent être listées.
- Les règles de génération et critères de recette doivent être écrits.
- Les décisions sensibles doivent être explicites avant implémentation.

## Sorties attendues par document codé
- Un générateur déterministe dédié au document canonique.
- Des validations d'entrée claires pour les champs obligatoires.
- Un DOCX propre, sans artefact de transformation.
- Des tests couvrant les règles documentaires spécifiées.
- Une mise à jour du tableau d'exécution.
- Aucune modification implicite du wording juridique.

## Décision temporaire V1
Pour DOC-002, l'adresse de domiciliation est gérée en champ libre :
- adresse_domiciliation_libre

## Ordre d'exécution immédiat
1. finaliser et versionner la mémoire projet dans le repo
2. implémenter DOC-001 : déclaration de non-condamnation
3. implémenter DOC-003
4. implémenter DOC-002
5. brancher l'orchestrateur Lot 1
6. brancher Streamlit Lot 1

## Documents que Codex doit lire avant toute implémentation
- AGENTS.md
- docs/project/00_MASTER_PLAN.md
- docs/project/01_EXECUTION_BOARD.md
- docs/project/02_CODEX_WORKFLOW.md
- docs/delivery/lot_01_analysis_and_specs_v1.md

## Garde-fous permanents
- Ne pas introduire d'IA générative dans le moteur de production.
- Ne pas automatiser un document marqué "à remplir à la main" sans décision explicite.
- Ne pas faire dériver le texte juridique ; en cas d'ambiguïté, bloquer et documenter la décision requise.
- Ne pas toucher plusieurs documents métier dans une même PR sauf ticket explicite.
- Toujours documenter ce qui est fait et ce qui vient après.
