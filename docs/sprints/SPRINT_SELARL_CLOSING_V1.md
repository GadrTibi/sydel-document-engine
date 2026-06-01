# Sprint SELARL closing V1

Date : 2026-06-01

## Objet

Ce fichier decrit la fin de sprint SELARL.

Il ne declare pas la SELARL terminee juridiquement a 100 %. Il organise la
cloture propre du perimetre deja construit et la suite des tickets necessaires
pour obtenir une validation humaine, puis pour ouvrir les variantes complexes
une par une.

Point de reprise canonique :

- `docs/project/SELARL_CANONICAL_STATUS_V1.md`

## Statut executif

Statut SELARL : `PARTIAL - production simple avancee`.

Derniere execution :

- `SELARL-CLOSING-PACK-001` est `DONE` au 2026-06-01 ;
- pack regenere dans `artifacts/selarl_closing_pack_001/` ;
- rapport de recette : `docs/review/selarl_closing_pack_001_report_v1.md` ;
- action en cours : `SELARL-ASSOCIE-REVIEW-001`.

Estimation PM apres pack :

- SELARL globale, tous cas confondus : environ 70 % ;
- SELARL simple cloturable : environ 90 % ;
- fin de sprint SELARL simple : environ 35 %.

Decision actuelle :

- `GO revue humaine` sur le pack simple deja generable ;
- `SELARL-ASSOCIE-REVIEW-001` demarre avec le brief
  `docs/review/selarl_associe_review_001_brief_v1.md` ;
- `NO-GO dev` pour toute extension complexe tant qu'un sous-cas unique n'est pas
  choisi, cadre et valide par Gad ;
- `NO-GO cloture 100 %` tant que l'associe / juriste n'a pas teste et retourne
  ses corrections ou sa validation.

## Ce qui est deja generable

### Creation simple medecin

Documents generes :

- `DOC-001` declaration de non-condamnation ;
- `DOC-002` autorisation de domiciliation ;
- `DOC-003` procuration ;
- `DOC-004` PV nomination gerant ;
- `DOC-034` demande d'inscription a l'ordre ;
- `DOC-017` statuts SELARL medecin.

Statut : candidat technique avance.

Limites :

- `DOC-034` reste PARTIAL faute de lock humain specifique ;
- `DOC-017` est LOCKED source-level, sans retour humain medecin recent
  equivalent au dentiste.

### Creation simple chirurgien-dentiste

Documents generes :

- `DOC-001` declaration de non-condamnation ;
- `DOC-002` autorisation de domiciliation ;
- `DOC-003` procuration ;
- `DOC-004` PV nomination gerant ;
- `DOC-034` demande d'inscription a l'ordre ;
- `DOC-016` statuts SELARL chirurgien-dentiste.

Statut : candidat technique avance.

Limites :

- `DOC-016` est LOCKED sur articles 1 a 34 ;
- le wrapper post-article reste OPEN GAP.

### Regime communautaire

Effet :

- `DOC-005` est ajoute si regime communautaire actif ;
- `DOC-006` reste reserve et exclu de la generation automatique.

Statut : couvert en V1 bornee.

### Multi-associes limite

Deux sous-cas existent :

- `DOC-004` multi-associes simple limite ;
- `DOC-004` + `DOC-016` dentiste multi-associes simple en PARTIAL.

Limites :

- pas de statuts multi-associes complets ;
- pas de medecin multi-associes ;
- pas de plusieurs gerants ;
- pas de president externe ;
- pas de vote non unanime ;
- pas de cession / SCM / derogation dans ce perimetre.

## Ce qui n'est pas termine

Les sujets suivants ne doivent pas etre traites comme des petites corrections de
fin de sprint. Ils demandent des tickets ou sprints separes.

| Sujet | Statut | Decision |
| --- | --- | --- |
| Revue associe / juriste du pack simple | EN COURS | Brief pret, attente retour humain |
| Corrections issues de la revue | BLOQUE | Attend retour humain |
| `DOC-034` lock humain | A FAIRE | A traiter dans la revue |
| `DOC-016` wrapper post-article | A FAIRE | A verifier humainement |
| `DOC-017` retour humain medecin | A FAIRE | A verifier humainement |
| `DOC-006` avertissement conjoint | RESERVE | Pas de generation sans decision |
| Cession cabinet medicale / dentaire | BLOQUE | Nouveau sous-cas obligatoire |
| Cession SCM | BLOQUE | Nouveau sous-cas obligatoire |
| Statuts multi-associes complets | BLOQUE | Source humaine/spec requise |
| Plusieurs gerants | BLOQUE | Source humaine/spec requise |
| President externe | BLOQUE | Source humaine/spec requise |
| Derogations / site distinct | MANUEL ou BLOQUE | Arbitrage requis |

## Gates de cloture

La SELARL peut etre declaree `DONE - perimetre simple` seulement si :

1. le pack simple medecin est regenere et transmis en revue ;
2. le pack simple dentiste est regenere et transmis en revue ;
3. le pack regime communautaire est regenere et transmis en revue ;
4. l'associe / juriste retourne une validation ou des corrections ;
5. chaque correction est classee : bug, wording, source, UX, hors scope ;
6. les corrections retenues sont implementees avec tests ;
7. les corrections reportees sont documentees ;
8. `SELARL_CANONICAL_STATUS_V1.md` est mis a jour ;
9. `01_EXECUTION_BOARD.md` et `04_LAST_STATE.md` indiquent le statut final.

## Tickets de fin de sprint

| Ordre | Ticket | Statut | Objet | Critere de sortie |
| --- | --- | --- | --- | --- |
| 1 | `SELARL-CLOSING-PACK-001` | DONE | Regenerer le pack de revue SELARL simple | Pack medecin, dentiste et regime communautaire produit, liste documents incluse |
| 2 | `SELARL-ASSOCIE-REVIEW-001` | IN_PROGRESS | Faire tester / relire le pack par l'associe ou juriste | Retour humain recu ou validation explicite |
| 3 | `SELARL-REVIEW-TRIAGE-001` | BLOCKED | Classer les retours humains | Debloque apres retour associe |
| 4 | `SELARL-REVIEW-FIXES-001` | BLOCKED | Corriger uniquement les retours valides | Debloque apres triage + `GO dev` |
| 5 | `SELARL-CLOSING-SMOKE-001` | BLOCKED | Relancer tests et smoke final | Debloque apres corrections |
| 6 | `SELARL-CANONICAL-CLOSE-001` | BLOCKED | Mettre a jour statut final SELARL simple | Debloque apres smoke final |
| 7 | `SELARL-NEXT-SUBCASE-SELECTION-001` | READY | Choisir un seul sous-cas complexe suivant | Decision Gad : cession, SCM, multi-associes, plusieurs gerants, derogation, site distinct, ou report |

## Ticket 1 - SELARL-CLOSING-PACK-001

Objectif : preparer un pack de revue humain sans modifier le code.

Entrees :

- `SELARL_CANONICAL_STATUS_V1.md` ;
- rapports Track B SELARL ;
- clean front Track B ;
- contexts / prefills existants.

Sorties :

- pack medecin simple ;
- pack dentiste simple ;
- pack medecin regime communautaire ;
- liste des documents produits ;
- liste des documents reserves/manuels/exclus ;
- note de revue pour l'associe.

Critere :

- aucun document reserve comme `DOC-006` ne doit etre dans le ZIP ;
- les documents manuels doivent etre visibles comme manuels ;
- les limites doivent etre annoncees.

Resultat 2026-06-01 :

- pack produit dans `artifacts/selarl_closing_pack_001/` ;
- manifest produit dans `artifacts/selarl_closing_pack_001/manifest_selarl_closing_pack_001.json` ;
- rapport produit dans `docs/review/selarl_closing_pack_001_report_v1.md` ;
- 6 DOCX medecin simple, 6 DOCX dentiste simple, 7 DOCX medecin regime communautaire ;
- `DOC-006` absent des ZIP ;
- tests cibles SELARL : 5 passes.

## Ticket 2 - SELARL-ASSOCIE-REVIEW-001

Objectif : obtenir le retour humain.

Entrees :

- pack de revue ;
- note de revue ;
- liste des points a verifier.

Sorties :

- validation explicite ou retour annote ;
- decisions sur `DOC-034`, `DOC-016` wrapper, `DOC-017` medecin ;
- corrections demandees.

Critere :

- on ne corrige rien avant d'avoir classe les retours.

Demarrage 2026-06-01 :

- brief de revue cree dans `docs/review/selarl_associe_review_001_brief_v1.md` ;
- brief corrige apres verification de `C:\Users\Gad\Downloads\Retours humains .docx` :
  le retour humain existant couvre deja plusieurs corrections `DOC-001` a
  `DOC-005` et le lock articles 1 a 34 de `DOC-016` ;
- pack a transmettre depuis `artifacts/selarl_closing_pack_001/` ;
- statut : attente retour humain brut, annote ou validation explicite ;
- prochain ticket bloque tant que ce retour n'est pas recu :
  `SELARL-REVIEW-TRIAGE-001`.

## Ticket 3 - SELARL-REVIEW-TRIAGE-001

Objectif : transformer le retour humain en tickets propres.

Classes :

- bug ;
- wording valide ;
- wording a arbitrer ;
- UX ;
- source manquante ;
- hors scope ;
- nouveau sous-cas.

Sorties :

- tableau des retours ;
- decision `corriger maintenant / reporter / bloquer` ;
- premier ticket de correction borne.

## Ticket 4 - SELARL-REVIEW-FIXES-001

Objectif : appliquer uniquement les corrections validees.

Regles :

- pas de wording invente ;
- pas de melange avec cession / SCM / multi-associes complet ;
- tests cibles obligatoires ;
- smoke DOCX/ZIP obligatoire si generation touchee.

## Ticket 5 - SELARL-CLOSING-SMOKE-001

Objectif : prouver que le perimetre simple reste stable.

Tests attendus :

- tests unitaires cibles ;
- `ruff check .` ;
- smoke medecin simple ;
- smoke dentiste simple ;
- smoke regime communautaire ;
- verification placeholders ;
- verification absence `DOC-006` dans les ZIP ;
- front local HTTP 200 si l'environnement le permet.

## Ticket 6 - SELARL-CANONICAL-CLOSE-001

Objectif : clore le sprint simple.

Sorties :

- `SELARL_CANONICAL_STATUS_V1.md` mis a jour ;
- board mis a jour ;
- dernier etat mis a jour ;
- statut final :
  - `DONE - perimetre simple` si la revue valide ;
  - `PARTIAL - corrections ouvertes` si des corrections restent ;
  - `BLOCKED - arbitrage humain` si un point sensible bloque.

## Ticket 7 - SELARL-NEXT-SUBCASE-SELECTION-001

Objectif : choisir la suite sans rouvrir tout a la fois.

Candidats :

- cession cabinet medicale / dentaire ;
- cession SCM ;
- statuts multi-associes complets ;
- plusieurs gerants ;
- president externe ;
- derogation / site distinct ;
- `DOC-006`.

Regle :

```text
1 sous-cas = 1 ticket ou sprint dedie = 1 GO dev explicite.
```

## Reponse courte a "ou en est la SELARL ?"

La SELARL est techniquement avancee sur le perimetre simple medecin / dentiste
et regime communautaire. Elle n'est pas terminee a 100 %. La prochaine action
propre est de regenerer un pack de revue et de le faire valider par l'associe ou
juriste. Les variantes complexes restent bloquees jusqu'a choix d'un sous-cas
unique et `GO dev` explicite.

## Prochaine action recommandee

Poursuivre `SELARL-ASSOCIE-REVIEW-001`.

Ce ticket est une revue humaine : transmettre le brief
`docs/review/selarl_associe_review_001_brief_v1.md` et le pack
`artifacts/selarl_closing_pack_001/` a l'associe / juriste, puis revenir avec
une validation explicite ou des retours annotees. Aucun nouveau developpement
complexe SELARL ne doit etre ouvert avant cette boucle de revue.
