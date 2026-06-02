# SELAS roadmap to completion 001

Date : 2026-06-02

Ticket : `SELAS-ROADMAP-TO-COMPLETION-001`

Statut : `DONE - plan valide pour execution`

Decision sprint : `GO dev borne par ticket selon ordre de roadmap ; NO-GO pack`

## Objet

Fixer l'ordre de travail complet pour aller jusqu'au bout de la SELAS V1 de
maniere methodique.

Ce livrable ne code rien, ne modifie aucun generateur, ne genere aucun
DOCX/PDF/ZIP et ne valide aucun wording juridique. Il donne l'ordre recommande
des tickets et le message a renvoyer a Gad pour validation.

## Definition de fin SELAS V1

La SELAS V1 est consideree terminee quand le parcours suivant est generable,
teste et relu :

```text
SELAS medecin
actionnaire unique
President unique
creation simple
capital en numeraire
actions ordinaires
sans Directeur General
sans multi-actionnaires
sans cession
sans SCM
sans site distinct
sans micro-holding
sans actions de preference
```

Documents du pack V1 :

| Document | Code | Statut cible V1 |
| --- | --- | --- |
| Declaration de non-condamnation President | `DOC-001` | Deja code SELAS-safe, a revalider outille |
| Autorisation de domiciliation | `DOC-002` | Deja code SELAS-safe, a revalider outille |
| Procuration President | `DOC-003` | Deja code SELAS-safe, a revalider outille |
| Statuts SELAS medecin actionnaire unique | `DOC-018` | A coder |
| Demande d'inscription a l'Ordre | `DOC-034` | A coder / brancher SELAS |
| Lettre de renonciation conjoint, si communaute | `DOC-005` | A coder / brancher SELAS conditionnel |
| Lettre d'avertissement conjoint, si communaute | `DOC-006` | A sortir de reserve et coder conditionnel |

Document reserve en V1 :

| Document | Decision |
| --- | --- |
| Decision/PV nomination President separe | Reserve, car la nomination President est absorbee par les statuts V1 selon `SELAS-SPEC-STATUTS-MEDECIN-AU-001`. A rouvrir seulement si Gad exige un acte separe. |

## Ordre A-Z recommande

| Ordre | Ticket | Type | Statut | Objectif | Pourquoi cet ordre |
| --- | --- | --- | --- | --- | --- |
| A | `SELAS-ROADMAP-TO-COMPLETION-001` | Cadrage | DONE | Ecrire cette roadmap et l'envoyer a Gad | Evite de choisir au hasard entre Ordre et regime communautaire |
| B | `SELAS-GAD-VALIDATE-ROADMAP-001` | Validation | DONE | Obtenir validation Gad sur l'ordre A-Z | Validation transmise par Naomie : avancer en suivant la methode SELARL et ajouter le gate trois sources |
| C | `SELAS-VALIDATIONS-EXISTING-DOCS-001` | QA | A FAIRE | Relancer `pytest` / `ruff` sur les tickets deja codes `DOC-001`, `DOC-002`, `DOC-003` | Nettoie les bases avant d'ajouter de nouveaux documents |
| D | `SELAS-DOC034-ORDRE-001` | Dev | DONE_PARTIAL_QA | Brancher `DOC-034` pour SELAS | Document du parcours simple, plus frequent que le regime communautaire |
| E | `SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001` | Dev | DONE_PARTIAL_QA | Brancher les deux lettres conjoint conditionnelles | Important mais conditionnel ; a faire apres le socle toujours attendu |
| F | `SELAS-DOC018-STATUTS-MEDECIN-AU-001` | Dev | DONE_PARTIAL_QA | Implementer les statuts SELAS medecin actionnaire unique | Document central et plus risque ; a faire apres les documents courts |
| G | `SELAS-FRONT-READINESS-PACK-001` | Dev front/data | DONE_PARTIAL_QA | Mettre a jour les statuts front du pack SELAS V1 | Le front sait quels documents sont prets, conditionnels ou reserves ; pack toujours bloque |
| H | `SELAS-ORCHESTRATOR-PACK-001` | Dev orchestration | DONE_PARTIAL_QA | Selectionner le pack SELAS V1 via le contexte dossier | L'orchestrateur selectionne le lot V1 sans activer les cas bloques |
| I | `SELAS-SMOKE-HAPPY-PATH-001` | QA | DONE_PARTIAL_QA | Generer le pack SELAS simple sans regime communautaire | Pack simple genere : `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018`; controles parasites/wording OK |
| J | `SELAS-SMOKE-REGIME-COMMUNAUTAIRE-001` | QA | DONE_PARTIAL_QA | Generer le pack SELAS avec `DOC-005` et `DOC-006` | Pack conditionnel genere avec 7 DOCX ; controle le cas conditionnel conjoint |
| K | `SELAS-ANTI-REGRESSION-WORDING-001` | QA | DONE_PARTIAL_QA | Verifier absence de `SELARL`, `Gerant`, `parts sociales`, `associe` mal place | Controle strict OK ; occurrences `associe` classees pour checkpoint trois sources |
| L | `SELAS-TRIPLE-SOURCE-CHECK-001` | Verification source | DONE_PARTIAL_QA | Comparer le pack V1 aux trois sources de verite projet | Source metier + NotebookLM alignes sur perimetre V1 ; retour Gad strategie present ; retour humain pack encore absent |
| M | `SELAS-HUMAN-REVIEW-PACK-001` | Revue | DONE_WAITING_HUMAN_REVIEW | Preparer le pack SELAS V1 a transmettre a Gad / associe / juriste | ZIP, questions et checklist produits ; attente retour humain |
| N | `SELAS-HUMAN-FIXES-001` | Corrections | A FAIRE SI RETOURS | Traiter les corrections humaines une par une | Corriger sans modifier tout le pack d'un coup |
| O | `SELAS-FINAL-SMOKE-ZIP-PDF-001` | QA | A FAIRE | Verifier DOCX, ZIP et PDF si backend disponible | Cloture technique du pack |
| P | `SELAS-CLOSE-V1-001` | Cloture | A FAIRE | Documenter le statut final SELAS V1 et les reserves | Rend le sprint reprenable et auditable |

## Ordre de dev recommande

Pour les prochains `GO dev`, l'ordre recommande est :

1. `SELAS-DOC034-ORDRE-001`
2. `SELAS-DOC005-DOC006-REGIME-COMMUNAUTAIRE-001`
3. `SELAS-DOC018-STATUTS-MEDECIN-AU-001`
4. `SELAS-FRONT-READINESS-PACK-001`
5. `SELAS-ORCHESTRATOR-PACK-001`
6. `SELAS-SMOKE-HAPPY-PATH-001`
7. `SELAS-SMOKE-REGIME-COMMUNAUTAIRE-001`
8. `SELAS-ANTI-REGRESSION-WORDING-001`
9. `SELAS-TRIPLE-SOURCE-CHECK-001`
10. `SELAS-HUMAN-REVIEW-PACK-001`

## Gate trois sources avant cloture

Avant de cloturer la SELAS V1, executer obligatoirement :

```text
SELAS-TRIPLE-SOURCE-CHECK-001
```

Ce checkpoint compare la premiere version totale developpee avec :

1. `project/source_truth/Documents_a_generer_par_cas.docx` ;
2. le journal NotebookLM SELAS `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
3. les retours humains Gad / associe / juriste sur la premiere version complete.

Decision apres execution :

- la source metier dit quels documents doivent exister par cas ;
- NotebookLM aide a verifier les variantes, conditions et trous ;
- le retour Gad disponible confirme la strategie de reutilisation prudente ;
- les retours humains du pack V1 complet restent absents ;
- le sprint SELAS ne peut pas passer en `CLOSE V1` sans revue humaine pack et
  iteration sur les retours humains.

Raison :

- `DOC-034` est dans le parcours simple et son risque est encadre par la spec.
- `DOC-005` / `DOC-006` sont conditionnels, mais maintenant specifies ensemble.
- `DOC-018` est le document central et le plus sensible ; il vaut mieux le coder
  quand les documents courts et les controles terminologiques sont deja stables.
- Le pack complet ne doit etre branche qu'apres les documents unitaires.

## Cas a ne pas melanger dans cette V1

Ces sujets restent hors sprint SELAS V1 finalisable :

| Sujet | Decision |
| --- | --- |
| SELAS dentiste | Reserve tant que source statuts dentiste SELAS non qualifiee |
| Multi-actionnaires | Sprint separe |
| Directeur General | Bloque faute de source NotebookLM V1 |
| Actions de preference | Sprint separe |
| Micro-holding | Sprint separe |
| Cession de fonds / cabinet | Manuel ou sprint separe |
| SCM | Sprint separe |
| Site distinct / derogation | Sprint separe ou pieces attendues selon Ordre |
| Attestation capital / liste souscripteurs SELAS | Source canonique exacte a identifier avant promesse produit |

## Message a envoyer a Gad

```text
J'ai demande a Codex de nous ecrire une roadmap SELAS complete, dans l'ordre,
pour aller jusqu'au bout de la SELAS V1 sans repartir au hasard document par
document.

Proposition de perimetre V1 :
- SELAS medecin
- actionnaire unique
- President unique
- creation simple
- capital en numeraire / actions ordinaires
- pas de DG, pas de multi-actionnaires, pas de cession, pas de SCM, pas de
  site distinct, pas de micro-holding, pas d'actions de preference

Ordre propose :
1. revalider les docs deja codes DOC-001 / DOC-002 / DOC-003
2. coder DOC-034 Ordre
3. coder DOC-005 + DOC-006 regime communautaire conditionnel
4. coder DOC-018 Statuts SELAS medecin actionnaire unique
5. brancher readiness front + orchestrateur pack SELAS
6. smoke pack simple
7. smoke pack avec regime communautaire
8. verification trois sources : Documents a generer par cas + NotebookLM + retours humains
9. revue humaine Gad / associe / juriste
10. corrections
11. cloture SELAS V1

Tu valides cette roadmap comme ordre officiel du sprint SELAS ?
Si oui, on lance le prochain GO dev borne sur SELAS-DOC034-ORDRE-001.
```

## Decision de sortie

Cette roadmap est validee pour execution par tickets bornes.

Decision permanente :

- pas de pack SELAS complet avant readiness front, orchestrateur, smoke,
  checkpoint trois sources et revue humaine ;
- pas de DOCX/PDF/ZIP SELAS complet avant specs documentaires, tests et
  validation humaine ;
- chaque dev reste borne au ticket courant.

Prochaine action recommandee : transmettre le pack de revue humaine, puis lancer
`SELAS-HUMAN-FIXES-001` si des corrections sont demandees.
