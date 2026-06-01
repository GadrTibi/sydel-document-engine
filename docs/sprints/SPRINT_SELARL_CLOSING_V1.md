# Sprint SELARL closing V1

Date : 2026-06-01

## Objet

Ce fichier suit la fin de sprint SELARL.

Il cloture le perimetre simple et regime communautaire sur une base technique
verifiee. Il ne declare pas encore toute la SELARL juridiquement terminee a
100 %, car les variantes complexes restent hors scope et la validation finale de
l'associe sur le pack corrige reste attendue.

Point de reprise canonique :

- `docs/project/SELARL_CANONICAL_STATUS_V1.md`

## Statut executif

Statut SELARL : `PARTIAL - perimetre simple + regime communautaire pret pour validation finale`.

Correction majeure du 2026-06-01 :

- retour associe : les questions posees etaient trop prudentes et inutiles ;
- decision produit : ne plus questionner ce qui est deja connu ou logique dans
  les sources ;
- correction reelle : `DOC-006` doit etre genere quand le regime communautaire
  est actif ;
- cause racine : anciennes docs et front avaient conserve une reserve source
  historique alors que la source DOCX et le batch Lot 2 existent ;
- action : generation regime communautaire = `DOC-005` + `DOC-006`.

Derniere execution :

- `SELARL-DOC006-REGIME-FIX-001` est `DONE` ;
- `SELARL-CLOSING-PACK-002` est `DONE` ;
- `SELARL-HUMAN-RETURNS-DEEP-AUDIT-002` est `DONE` ;
- `SELARL-CLOSING-PACK-003` est `DONE` ;
- `SELARL-THREE-SOURCE-AUDIT-004` est `DONE` ;
- `SELARL-CLOSING-PACK-004` est `DONE` ;
- `SELARL-CLOSING-SMOKE-001` est `DONE` ;
- `SELARL-HUMAN-RETURNS-DEEP-AUDIT-005` est `DONE` ;
- pack corrige actif dans `artifacts/selarl_closing_pack_004/` ;
- rapport pack : `docs/review/selarl_closing_pack_004_report_v1.md` ;
- rapport audit trois sources : `docs/review/selarl_three_source_alignment_004_report_v1.md` ;
- rapport audit retours humains actif : `docs/review/selarl_human_returns_deep_audit_005_report_v1.md` ;
- rapport source/fidelite : `docs/review/selarl_source_fidelity_audit_001_report_v1.md` ;
- action en cours : `SELARL-FINAL-ASSOCIE-VALIDATION-001`.

Estimation PM apres correction :

| Perimetre | Avancement | Lecture |
| --- | ---: | --- |
| SELARL simple + regime communautaire, technique | 98 % | Code, pack, smoke et tests OK ; reste validation humaine finale. |
| SELARL simple + regime communautaire, produit | 90 % | L'associe doit valider le pack corrige ou annoter les derniers ecarts. |
| SELARL globale tous cas confondus | 75 % | Les variantes cession, SCM, site distinct, derogation et statuts multi-associes complets restent separees. |

## Pack corrige

Racine :

- `artifacts/selarl_closing_pack_004/`

Manifest :

- `artifacts/selarl_closing_pack_004/manifest_selarl_closing_pack_004.json`

Scenarios generes :

| Scenario | Documents DOCX | Regle critique |
| --- | ---: | --- |
| `medecin_simple` | 6 | Pas de `DOC-005` / `DOC-006` hors regime |
| `dentiste_simple` | 6 | Pas de `DOC-005` / `DOC-006` hors regime |
| `medecin_regime_communautaire` | 8 | `DOC-005` + `DOC-006` presents |
| `dentiste_regime_communautaire` | 8 | `DOC-005` + `DOC-006` presents |

## Ce qui est deja generable

### Creation simple medecin

- `DOC-001` declaration de non-condamnation ;
- `DOC-002` autorisation de domiciliation ;
- `DOC-003` procuration ;
- `DOC-004` PV nomination gerant ;
- `DOC-034` demande d'inscription a l'ordre ;
- `DOC-017` statuts SELARL medecin.

### Creation simple chirurgien-dentiste

- `DOC-001` declaration de non-condamnation ;
- `DOC-002` autorisation de domiciliation ;
- `DOC-003` procuration ;
- `DOC-004` PV nomination gerant ;
- `DOC-034` demande d'inscription a l'ordre ;
- `DOC-016` statuts SELARL chirurgien-dentiste.

### Regime communautaire

Effet :

- `DOC-005` est ajoute si regime communautaire actif ;
- `DOC-006` est ajoute si regime communautaire actif ;
- l'adresse du conjoint est requise pour `DOC-006`.

Statut : couvert dans le pack corrige.

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

## Ce qui reste avant cloture produit

| Sujet | Statut | Decision |
| --- | --- | --- |
| Validation finale associe du pack corrige | IN_PROGRESS | Transmettre pack 004 et brief final |
| Corrections eventuelles issues du pack 004 | BLOCKED | Attend retour concret associe |
| `DOC-034` lock humain | A VALIDER | Demander seulement ecarts concrets, pas questions abstraites |
| `DOC-016` wrapper post-article | A VALIDER | Articles 1 a 34 deja couverts |
| `DOC-017` retour humain medecin | A VALIDER | Source-level lock deja OK |
| Cession cabinet medicale / dentaire | BLOQUE | Nouveau sous-cas obligatoire |
| Cession SCM | BLOQUE | Nouveau sous-cas obligatoire |
| Statuts multi-associes complets | BLOQUE | Source humaine/spec requise |
| Plusieurs gerants | BLOQUE | Source humaine/spec requise |
| President externe | BLOQUE | Source humaine/spec requise |
| Derogations / site distinct | MANUEL ou BLOQUE | Arbitrage requis |

## Tickets de fin de sprint

| Ordre | Ticket | Statut | Objet | Critere de sortie |
| --- | --- | --- | --- | --- |
| 1 | `SELARL-CLOSING-PACK-001` | DONE | Pack historique avant correction `DOC-006` | Remplace par packs 002, 003 puis 004 |
| 2 | `SELARL-ASSOCIE-REVIEW-001` | DONE | Reception du retour associe | Retour classe : questions inutiles, `DOC-006` evident, fidelite source stricte |
| 3 | `SELARL-REVIEW-TRIAGE-001` | DONE | Classer le retour humain | Correction reelle identifiee : lever reserve `DOC-006` |
| 4 | `SELARL-DOC006-REGIME-FIX-001` | DONE | Generer `DOC-006` quand regime communautaire actif | Front, contexte, tests et docs alignes |
| 5 | `SELARL-CLOSING-PACK-002` | DONE | Regenerer le pack corrige | 6/6/8/8 DOCX, `DOC-006` present uniquement en regime |
| 6 | `SELARL-HUMAN-RETURNS-DEEP-AUDIT-002` | DONE | Relire les retours humains et verifier le pack 002 | Trois ecarts PV detectes et corriges |
| 7 | `SELARL-CLOSING-PACK-003` | DONE | Regenerer le pack apres audit retours humains | Remplace par pack 004 |
| 8 | `SELARL-THREE-SOURCE-AUDIT-004` | DONE | Verifier document de reference + retours modele + retour humain | Ecart `DOC-003` trouve dans pack 003 |
| 9 | `SELARL-CLOSING-PACK-004` | DONE | Corriger la procuration et regenerer le pack | Pack 004 vert sur controles trois sources |
| 10 | `SELARL-CLOSING-SMOKE-001` | DONE | Relancer tests et smoke final technique | Ruff OK, tests cibles OK, `pytest -q` 416 passes, manifest pack 004 sans echec |
| 11 | `SELARL-HUMAN-RETURNS-DEEP-AUDIT-005` | DONE | Reverifier les retours humains sur pack 004 | 116 controles cibles OK ; nuance article 8 statuts dentiste documentee |
| 12 | `SELARL-FINAL-ASSOCIE-VALIDATION-001` | IN_PROGRESS | Faire valider le pack corrige par l'associe | Validation finale ou liste courte d'ecarts reels |
| 13 | `SELARL-CANONICAL-CLOSE-001` | BLOCKED | Clore le statut canonique SELARL simple/regime | Debloque apres validation finale associe |
| 14 | `SELARL-NEXT-SUBCASE-SELECTION-001` | READY | Choisir un seul sous-cas complexe suivant | Decision Gad : cession, SCM, multi-associes complet, plusieurs gerants, derogation, site distinct, ou report |

## Gate de cloture

La SELARL simple + regime communautaire peut etre declaree
`DONE - perimetre simple/regime` seulement si :

1. le pack 004 est transmis ;
2. l'associe valide le pack ou donne des ecarts concrets ;
3. chaque ecart concret est corrige ou reporte explicitement ;
4. `SELARL_CANONICAL_STATUS_V1.md`, `01_EXECUTION_BOARD.md` et
   `04_LAST_STATE.md` sont mis a jour.

## Reponse courte a "ou en est la SELARL ?"

Techniquement, le perimetre SELARL simple medecin/dentiste + regime
communautaire est quasiment ferme. La correction importante est faite :
`DOC-006` est genere avec `DOC-005` quand il y a regime communautaire.

Il reste une validation finale humaine du pack corrige. Les variantes complexes
ne sont pas fermees par ce sprint et doivent etre traitees une par une.

## Prochaine action recommandee

Poursuivre `SELARL-FINAL-ASSOCIE-VALIDATION-001` :

- transmettre `artifacts/selarl_closing_pack_004/` ;
- transmettre `docs/review/selarl_final_validation_001_brief_v1.md` ;
- demander uniquement une validation finale ou des ecarts concrets par document.
