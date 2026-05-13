# Tableau d'exécution

## Statuts
- READY
- IN_PROGRESS
- BLOCKED
- DONE

## Tickets actifs

| ID | Statut | Objet | Entrées obligatoires | Sorties obligatoires |
|---|---|---|---|---|
| PM-001 | DONE | Installer la mémoire projet dans le repo | source de vérité + specs Lot 1 | docs/project/* |
| PM-002 | DONE | Vérifier et compléter la mémoire projet opérationnelle | AGENTS.md + docs/project/* | docs/project complétés + artefact parasite traité |
| PM-003 | DONE | Installer le kit de reprise nouveau ChatGPT / Codex | mémoire projet existante | handoff + last state + prompt nouveau chat |
| DOC-001 | DONE | Implémenter la déclaration de non-condamnation | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-003 | DONE | Implémenter la procuration | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-002 | DONE | Implémenter l'autorisation de domiciliation | source doc + spec Lot 1 + décision V1 adresse libre | générateur + tests + MAJ doc |
| ORCH-001 | DONE | Brancher l'orchestrateur Lot 1 | générateurs DOC-001/002/003 | service orchestrateur + tests |
| PM-004 | DONE | Intégrer l'arbre moteur document-centré V1 dans la mémoire projet | arbre moteur document-centré V1 | board + dernier état mis à jour |
| PM-005 | DONE | Intégrer le dictionnaire canonique des variables V1 dans la mémoire projet | dictionnaire canonique des variables V1 | board + dernier état mis à jour |
| SMOKE-001 | DONE | Smoke test réel Lot 1 via orchestrateur | contexte exemple Lot 1 + orchestrateur | 3 DOCX générés + docs projet mises à jour |
| VAR-001 | DONE | Ajouter une table de mapping document -> variables canoniques | arbre documentaire V1 + dictionnaire canonique V1 + specs | table de mapping document -> variables canoniques |
| UI-001 | READY | Brancher Streamlit V0 Lot 1 | orchestrateur Lot 1 | écran simple + test manuel |

## Référentiels moteur disponibles
- Le moteur dispose désormais d'un arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`.
- Le moteur dispose désormais d'un dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`.
- Le moteur dispose désormais d'une table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Ces référentiels cadrent les prochains tickets ; ils ne doivent pas être réinventés pendant l'implémentation.

## Ecart temporaire connu
- Nom canonique retenu pour la domiciliation : `domiciliation.adresse_affichee`.
- Alias legacy temporaire présent dans le code Lot 1 : `adresse_domiciliation_affichee`.
- Le présent ticket ne refactore pas le code Python ; les prochains tickets doivent converger vers le nom canonique sans recréer de variante locale.

## Détail des prochains tickets

### DOC-001
- Objectif : générer la déclaration sur l'honneur de non-condamnation.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- ADR à relire : ADR-0001, ADR-0002, ADR-0004, ADR-0005.
- Contraintes : source reçue, spec écrite, accords de genre, DOCX propre, tests obligatoires.
- Sortie attendue : générateur DOC-001, tests, mise à jour documentaire.

### DOC-003
- Objectif : générer la procuration après DOC-001.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contraintes : bloc mandataire SYDEL externalisé en configuration, wording source conservé.
- Sortie attendue : générateur DOC-003, tests, mise à jour documentaire.

### DOC-002
- Objectif : générer l'autorisation de domiciliation après arbitrage V1 déjà posé.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contrainte sensible : le nom canonique documentaire est désormais `domiciliation.adresse_affichee`; le code Lot 1 existant conserve temporairement l'alias legacy `adresse_domiciliation_affichee`.
- Sortie : générateur DOC-002 terminé, tests unitaires ciblés ajoutés, validations locales vertes.

### ORCH-001
- Objectif : brancher les trois générateurs Lot 1 dans l'orchestrateur dossier.
- Prérequis : DOC-001, DOC-002 et DOC-003 terminés.
- Sortie : registre minimal DOC-001/DOC-002/DOC-003 branché, génération DOCX dossier selon `ctx.structure`, tests d'orchestration ajoutés.

### VAR-001
- Objectif : ajouter une table de mapping document -> variables canoniques sans refaire le dictionnaire.
- Prérequis : arbre documentaire V1 et dictionnaire canonique des variables V1 intégrés.
- Sortie : table de mapping V1 intégrée à la mémoire projet, sans réécriture ; écart temporaire documenté entre `domiciliation.adresse_affichee` et l'alias legacy `adresse_domiciliation_affichee`.

### UI-001
- Objectif : exposer une Streamlit simple pour générer le Lot 1.
- Prérequis : orchestrateur Lot 1 fonctionnel.
- Sortie attendue : écran simple, génération testable manuellement, aucun métier caché dans l'UI.

## Règle de mise à jour
Chaque ticket terminé doit mettre à jour ce fichier :
- passer son statut à DONE
- déplacer le ticket actif en IN_PROGRESS pendant l'exécution si la tâche dure plus qu'une modification courte
- indiquer le prochain ticket à lancer
- indiquer les éventuels points ouverts
- mettre à jour `docs/project/04_LAST_STATE.md`

## Prochaine étape prévue
- prochain ticket recommandé : UI-001
- action : brancher Streamlit V0 Lot 1 en s'appuyant sur l'arbre documentaire V1, le dictionnaire canonique V1 et la table de mapping document -> variables canoniques V1.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Les trois DOCX sont bien produits par l'orchestrateur dans `artifacts/lot_01_smoke_test/`, mais le rendu visuel et le wording juridique restent à relire humainement dans les fichiers générés.
- PDF et ZIP restent hors ORCH-001 et devront être traités dans un ticket dédié.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.

## Journal court
- 2026-05-12 : mémoire projet installée dans `docs/project/`.
- 2026-05-12 : mémoire projet complétée pour servir de contexte opérationnel autonome ; artefact `tall -U pip` identifié comme fichier parasite à supprimer.
- 2026-05-12 : kit de reprise ajouté pour nouveau ChatGPT / Codex avec handoff, dernier état et prompt de reprise.
- 2026-05-12 : DOC-001 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-001 corrigé pour rendre l'adresse personnelle dans l'ordre source `num voie + voie, ville cp`.
- 2026-05-12 : DOC-003 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-002 implémenté en génération DOCX from-scratch avec champ libre `adresse_domiciliation_affichee` ; validations locales vertes.
- 2026-05-12 : ORCH-001 branche les générateurs DOC-001, DOC-002 et DOC-003 dans l'orchestrateur dossier ; génération DOCX uniquement.
- 2026-05-13 : logique documentaire du moteur formalisée par l'arbre document-centré V1 ; mémoire projet alignée sans réécriture de l'arbre.
- 2026-05-13 : SMOKE-001 génère réellement les trois DOCX du Lot 1 via l'orchestrateur avec `examples/contexts/lot_01_example.yaml` corrigé au strict minimum.
- 2026-05-13 : dictionnaire canonique des variables V1 intégré dans la mémoire projet ; le moteur dispose désormais d'un arbre documentaire et d'un dictionnaire canonique de variables.
- 2026-05-13 : table de mapping document -> variables canoniques V1 intégrée dans la mémoire projet sans réécriture ; écart temporaire `domiciliation.adresse_affichee` / `adresse_domiciliation_affichee` documenté.
