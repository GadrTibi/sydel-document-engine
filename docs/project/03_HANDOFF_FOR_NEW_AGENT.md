# Handoff pour nouvel agent

## Objet du projet
Le dépôt construit un moteur documentaire juridique déterministe pour DAAT x SYDEL. Le moteur doit produire des documents de dossier de manière reproductible, traçable et contrôlable, sans dépendre de la mémoire d'une conversation précédente.

## Source de vérité
- Source de vérité métier : `project/source_truth/Documents_a_generer_par_cas.docx`.
- Specs opérationnelles : `docs/delivery/`.
- Mémoire projet : `docs/project/`.
- ADR : `docs/adr/`.

L'arbre théorique abandonné n'est pas une source valide. Il n'existe pas de fichier séparé "Documents avec variables".

## Architecture retenue
- Le moteur est construit par document canonique.
- Le référentiel de départ est par cas métier, pour décider quels documents produire.
- Un orchestrateur dossier appelle les générateurs de documents canoniques.
- Chaque document automatisé a son générateur dédié.
- Les sorties cibles V1 sont DOCX, PDF et ZIP.
- L'interface cible est une Streamlit simple.
- Le moteur de production ne doit pas contenir de logique d'IA générative.

## Décisions déjà figées
- La source de vérité documentaire est `project/source_truth/Documents_a_generer_par_cas.docx`.
- Le moteur n'est pas construit par arbre de cas, mais par document canonique.
- Les documents marqués "à remplir à la main" restent hors automatisation initiale.
- Aucun document ne doit être codé sans source reçue, analyse et spec écrite.
- Les DOCX propres sont reconstruits de manière déterministe plutôt que nettoyés à la volée en production.
- Pour DOC-002 en V1, l'adresse de domiciliation est un champ libre : `domiciliation.adresse_locaux_affichee`.

## Ce qui est déjà fait
- Le dépôt de base existe.
- La mémoire projet initiale est installée dans `docs/project/`.
- Les ADR principales existent dans `docs/adr/`.
- La spec Lot 1 existe dans `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Le Lot 1 est défini : DOC-001, DOC-002, DOC-003.
- Le prochain ticket opérationnel est DOC-001.

## Ce qui n'est pas encore fait
- Le code métier Lot 1 n'est pas démarré.
- Les générateurs DOC-001, DOC-002 et DOC-003 ne sont pas encore implémentés.
- L'orchestrateur Lot 1 n'est pas encore branché.
- L'interface Streamlit Lot 1 n'est pas encore branchée.
- Les sorties PDF et ZIP restent à intégrer dans le flux V1.

## Ordre de lecture des fichiers
Avant toute proposition ou implémentation, lire dans cet ordre :

1. `AGENTS.md`
2. `docs/project/00_MASTER_PLAN.md`
3. `docs/project/01_EXECUTION_BOARD.md`
4. `docs/project/02_CODEX_WORKFLOW.md`
5. `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
6. `docs/project/04_LAST_STATE.md`
7. Le fichier de spec concerné dans `docs/delivery/`
8. Les ADR applicables dans `docs/adr/`

## Travail entre ChatGPT chef de projet et Codex exécutant
- ChatGPT chef de projet cadre les tickets, arbitre les priorités et explicite les décisions métier à documenter.
- Codex exécutant lit la mémoire projet, applique le ticket demandé et garde un scope minimal.
- Codex ne modifie pas le wording juridique sans instruction explicite.
- Codex met à jour `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` à la fin de chaque ticket.
- En cas d'ambiguïté métier, Codex bloque l'implémentation concernée et documente la décision requise.
- Les PR doivent rester petites, traçables et centrées sur un seul document métier sauf demande explicite.
