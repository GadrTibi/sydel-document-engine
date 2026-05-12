# Mode opératoire Codex

## Lecture obligatoire avant tout ticket
1. AGENTS.md
2. docs/project/00_MASTER_PLAN.md
3. docs/project/01_EXECUTION_BOARD.md
4. docs/project/02_CODEX_WORKFLOW.md
5. docs/project/03_HANDOFF_FOR_NEW_AGENT.md
6. docs/project/04_LAST_STATE.md
7. le document de spec concerné

Pour un ticket documentaire, vérifier aussi l'ADR applicable dans `docs/adr/` avant d'écrire du code.

## Choix du périmètre
- Identifier le ticket exact dans `docs/project/01_EXECUTION_BOARD.md`.
- Vérifier le statut du ticket avant de commencer.
- Ne travailler que sur le document ou le composant explicitement demandé.
- Ne pas embarquer de refactor opportuniste.
- Si le ticket implique un document canonique, ne pas toucher un autre document métier dans la même tâche.

## Pipeline documentaire à respecter
Un document ne peut être codé que si le cycle suivant est satisfait :

`Inventorié -> Validé -> Source reçue -> Analysé -> Spécifié -> Codé -> Testé -> Validé`

Avant le passage en code, vérifier au minimum :
- source reçue ;
- spec écrite ;
- variables listées ;
- règles de génération décrites ;
- critères de recette présents ;
- décisions métier sensibles explicites.

## Règles d'exécution
- faire un changement petit et ciblé
- ne pas modifier implicitement le texte juridique
- s'appuyer sur les documents source et les specs
- conserver les conventions du repo
- ajouter ou mettre à jour les tests utiles
- exécuter les validations locales avant clôture

## Validations minimales
- .\.venv\Scripts\python.exe -m ruff check .
- .\.venv\Scripts\python.exe -m pytest

Pour une tâche de documentation pure, les validations de code peuvent être remplacées par :
- relecture du diff
- vérification que le scope ne touche pas au code métier Python
- vérification que le tableau d'exécution indique la prochaine étape

Pour un ticket documentaire codé, ajouter des validations ciblées :
- tests du générateur concerné ;
- tests des helpers transverses modifiés ;
- vérification que les sorties ne contiennent pas de placeholder résiduel ;
- vérification que les accords et conditions décrits dans la spec sont couverts.

## Mise à jour documentaire obligatoire en fin de ticket
Mettre à jour :
- docs/project/01_EXECUTION_BOARD.md
- docs/project/04_LAST_STATE.md
- docs/delivery/work_status.md si nécessaire

La mise à jour doit documenter :
- ce qui vient d'être fait
- le prochain ticket recommandé
- les hypothèses ou décisions métier ouvertes
- toute dérive volontaire de wording juridique, si elle a été explicitement demandée

`docs/project/04_LAST_STATE.md` doit toujours refléter l'état immédiatement reprenable du projet : dernier ticket terminé, état du repo, prochain ticket, points ouverts, validations connues et recommandation immédiate.

## Format attendu du compte-rendu Codex
- Fait
- Fichiers modifiés
- Tests exécutés
- Résultat des tests
- Prochaine étape recommandée
- Questions ouvertes éventuelles

Le compte-rendu doit aussi signaler explicitement :
- tout fichier non touché volontairement alors qu'il semblait proche du sujet ;
- toute hypothèse métier ;
- toute impossibilité de lancer une validation ;
- toute modification de wording juridique, uniquement si elle a été demandée par la spec ou le ticket.

## Règles de clôture
- Le diff doit rester lisible et limité.
- Le tableau d'exécution doit indiquer le prochain ticket.
- Les fichiers temporaires ou artefacts accidentels doivent être supprimés s'ils ne servent pas le projet.
- Aucun commit, push ou PR ne doit être fait sauf demande explicite.
- En cas de doute métier, documenter le point ouvert au lieu d'inventer une règle.

## Prompt standard à utiliser avec Codex
Lis d'abord :
- AGENTS.md
- docs/project/00_MASTER_PLAN.md
- docs/project/01_EXECUTION_BOARD.md
- docs/project/02_CODEX_WORKFLOW.md
- docs/project/03_HANDOFF_FOR_NEW_AGENT.md
- docs/project/04_LAST_STATE.md
- le fichier de spec visé

Ensuite :
- implémente le ticket demandé avec un scope minimal et propre
- ne modifie pas le texte juridique hors besoins explicitement spécifiés
- ajoute ou mets à jour les tests nécessaires
- exécute ruff et pytest
- mets à jour docs/project/01_EXECUTION_BOARD.md et docs/project/04_LAST_STATE.md avec le statut, ce qui a été fait et la prochaine étape
