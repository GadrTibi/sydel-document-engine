# Prompt de reprise nouveau chat

Copier-coller ce prompt dans une nouvelle discussion ChatGPT ou Codex pour reprendre le projet sans dépendre de l'historique de conversation.

```text
Tu reprends le projet SYDEL Document Engine.

Avant de proposer quoi que ce soit, lis d'abord dans cet ordre :
- AGENTS.md
- docs/project/00_MASTER_PLAN.md
- docs/project/01_EXECUTION_BOARD.md
- docs/project/02_CODEX_WORKFLOW.md
- docs/project/03_HANDOFF_FOR_NEW_AGENT.md
- docs/project/04_LAST_STATE.md

Ensuite seulement, résume :
- l'objet du projet ;
- la source de vérité ;
- l'architecture retenue ;
- le dernier état connu ;
- le prochain ticket recommandé ;
- les points ouverts.

Contraintes permanentes :
- ne touche pas au code avant d'avoir lu ces fichiers ;
- ne modifie aucun texte juridique sans instruction explicite ;
- ne code aucun document sans source reçue, analyse et spec écrite ;
- garde un scope minimal et traçable ;
- mets à jour docs/project/01_EXECUTION_BOARD.md et docs/project/04_LAST_STATE.md à la fin de chaque ticket ;
- ne fais pas de commit, push ou PR sauf demande explicite.

Si une information manque ou se contredit, arrête-toi et signale le blocage.
```
