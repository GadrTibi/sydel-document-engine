# Sprint SELARL closing V1

Date : 2026-06-02

## Objet

Ce fichier suit la fin de sprint SELARL.

Il cloture le perimetre simple et regime communautaire sur une base technique
verifiee. Il ne declare pas encore toute la SELARL juridiquement terminee a
100 %, car les variantes complexes restent hors scope et la validation finale de
l'associe sur le pack corrige reste attendue.

Point de reprise canonique :

- `docs/project/SELARL_CANONICAL_STATUS_V1.md`

## Statut executif

Statut SELARL : `PARTIAL - perimetre simple + regime communautaire pret pour validation finale associe`.

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
- `SELARL-HUMAN-RETURNS-006-TRIAGE-001` est `DONE` ;
- `SELARL-RETURNS-006-STATUTS-001` est `DONE` ;
- `SELARL-RETURNS-006-DNC-001` est `DONE` ;
- `SELARL-RETURNS-006-PV-001` est `DONE` ;
- `SELARL-RETURNS-006-PROCURATION-001` est `DONE` ;
- `SELARL-RETURNS-006-CONJOINT-LETTERS-001` est `DONE` ;
- `SELARL-RETURNS-006-ORDRE-001` est `DONE` ;
- `SELARL-RETURNS-006-FRONT-VARIABLES-001` est `DONE` ;
- `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001` est `DONE` ;
- `SELARL-CLOSING-PACK-005` est `DONE` ;
- `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006` est `DONE` ;
- `SELARL-RETURNS-006-CONJOINT-ADDRESS-FRONT-LOCK-001` est `DONE` ;
- `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` est `DONE` ;
- pack actif : `artifacts/selarl_closing_pack_005/` ;
- rapport pack : `docs/review/selarl_closing_pack_005_report_v1.md` ;
- rapport audit trois sources : `docs/review/selarl_three_source_alignment_004_report_v1.md` ;
- rapport audit retours humains actif : `docs/review/selarl_human_returns_deep_audit_006_report_v1.md` ;
- rapport audit incident generalise :
  `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md` ;
- retour humain brut 006 : `docs/review/selarl_human_returns_006_raw_v1.md` ;
- triage retour humain 006 : `docs/review/selarl_human_returns_triage_006_report_v1.md` ;
- rapports corrections 006 finales :
  `docs/review/selarl_returns_006_ordre_001_report_v1.md`,
  `docs/review/selarl_returns_006_front_variables_001_report_v1.md`,
  `docs/review/selarl_returns_006_address_signature_001_report_v1.md` ;
- rapport source/fidelite : `docs/review/selarl_source_fidelity_audit_001_report_v1.md` ;
- brief validation associe : `docs/review/selarl_final_validation_001_brief_v1.md` ;
- action en cours : `SELARL-FINAL-ASSOCIE-VALIDATION-001`.

Estimation PM apres correction :

| Perimetre | Avancement | Lecture |
| --- | ---: | --- |
| SELARL simple + regime communautaire, technique | 99 % | Pack 005 regenere, incident front adresse conjoint corrige, `DOC-002` corrige en `pour 99 ans`, regression SELARL ciblee 187 tests OK. |
| SELARL simple + regime communautaire, produit | 96 % | Retours humains 006 traites et reverifies ; validation finale associe requise avant 100 %. |
| SELARL globale tous cas confondus | 75 % | Les variantes cession, SCM, site distinct, derogation et statuts multi-associes complets restent separees. |

## Pack corrige

Racine :

- `artifacts/selarl_closing_pack_005/`

Manifest :

- `artifacts/selarl_closing_pack_005/manifest_selarl_closing_pack_005.json`

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
- l'adresse du conjoint est derivee depuis l'adresse personnelle de l'associe /
  signataire pour `DOC-006`.

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
| Validation finale associe du pack corrige | READY | Pack 005 amende apres audit incident ; demander seulement des ecarts concrets ou validation |
| Retours humains 006 | DONE code/test/pack/audit | Retours recus, triage fait, corrections traitees, pack 005 regenere puis amende apres incident `DOC-002` |
| Corrections eventuelles issues du pack 004 | DONE code/test/pack | Tickets `SELARL-RETURNS-006-*` traites ; pack 004 remplace par pack 005 |
| `DOC-034` lock humain | A VALIDER | Demander seulement ecarts concrets sur pack 005, pas questions abstraites |
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
| 12 | `SELARL-FINAL-ASSOCIE-VALIDATION-001` | READY | Faire valider le pack final par l'associe | Pack 005 controle puis amende ; attendre verdict associe par ecarts concrets |
| 13 | `SELARL-HUMAN-RETURNS-006-TRIAGE-001` | DONE | Enregistrer et classer les retours humains 006 | Brut + triage + tickets de correction |
| 14 | `SELARL-RETURNS-006-STATUTS-001` | DONE | Corriger les retours 006 statuts | Rapport `docs/review/selarl_returns_006_statuts_001_report_v1.md` ; tests statuts SEL OK |
| 15 | `SELARL-RETURNS-006-DNC-001` | DONE | Corriger declaration non condamnation | Rapport `docs/review/selarl_returns_006_dnc_001_report_v1.md` ; tests DNC/front OK |
| 16 | `SELARL-RETURNS-006-PV-001` | DONE | Corriger PV nomination gerant | Rapport `docs/review/selarl_returns_006_pv_001_report_v1.md` ; tests PV/front OK |
| 17 | `SELARL-RETURNS-006-PROCURATION-001` | DONE | Corriger procuration | Rapport `docs/review/selarl_returns_006_procuration_001_report_v1.md` ; phrase `demeurant..., agissant...` conforme ; tests procuration OK |
| 18 | `SELARL-RETURNS-006-CONJOINT-LETTERS-001` | DONE | Corriger lettres regime communautaire | Rapport `docs/review/selarl_returns_006_conjoint_letters_001_report_v1.md` ; adresse conjoint derivee, forme juridique redigee, date renonciation retiree ; tests regime/front OK |
| 19 | `SELARL-RETURNS-006-ORDRE-001` | DONE | Corriger demande inscription ordre | Rapport `docs/review/selarl_returns_006_ordre_001_report_v1.md` ; conseil compose depuis profession + departement ; tests ordre/front OK |
| 20 | `SELARL-RETURNS-006-FRONT-VARIABLES-001` | DONE | Simplifier variables/front SELARL | Rapport `docs/review/selarl_returns_006_front_variables_001_report_v1.md` ; constantes + nationalite portugaise + reuse siege=adresse personnelle ; tests front OK |
| 21 | `SELARL-RETURNS-006-ADDRESS-SIGNATURE-001` | DONE | Corriger regles transversales adresses/signatures | Rapport `docs/review/selarl_returns_006_address_signature_001_report_v1.md` ; CP avant ville + suppression encadres signature ; tests cibles OK |
| 22 | `SELARL-CLOSING-PACK-005` | DONE | Regenerer le pack apres retours 006 | Pack 005 6/6/8/8 DOCX, manifest 0 echec, rapport pack 005 |
| 23 | `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006` | DONE historique | Verifier retours 006 sur pack 005 | Ancien audit trop confiant ; amende par `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` |
| 24 | `SELARL-RETURNS-006-CONJOINT-ADDRESS-FRONT-LOCK-001` | DONE | Verrouiller adresse conjoint cote front/schema | Incident Gad/associe confirme ; aucune saisie adresse conjoint, derivee depuis adresse personnelle ; tests anti-regression OK |
| 25 | `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001` | DONE | Rejouer les incidents associe sur toutes les surfaces | Ecart `DOC-002` trouve et corrige ; pack 005 regenere localement ; regression 187 tests OK |
| 26 | `SELARL-RETURNS-007-SIGNATURE-DNC-001` | DONE | Traiter nouveaux retours associe signatures/DNC | Signatures DOC-001/002/003 sans table ; DNC ville naissance verifiee ; pack 005 regenere ; regression 187 tests OK |
| 27 | `SELARL-CANONICAL-CLOSE-001` | BLOCKED | Clore le statut canonique SELARL simple/regime | Debloque apres validation finale associe ou corrections d'ecarts concrets |
| 28 | `SELARL-NEXT-SUBCASE-SELECTION-001` | READY | Choisir un seul sous-cas complexe suivant | Decision Gad : cession, SCM, multi-associes complet, plusieurs gerants, derogation, site distinct, ou report |

## Gate de cloture

La SELARL simple + regime communautaire peut etre declaree
`DONE - perimetre simple/regime` seulement si :

1. les retours humains 006 sont corriges ou reportes explicitement ;
2. le pack 005 est regenere ;
3. l'audit retours 006 sur pack 005 est vert ;
4. l'associe valide le pack 005 ou donne uniquement des ecarts residuels ;
5. chaque ecart concret residuel est corrige ou reporte explicitement ;
6. `SELARL_CANONICAL_STATUS_V1.md`, `01_EXECUTION_BOARD.md` et
   `04_LAST_STATE.md` sont mis a jour.

## Reponse courte a "ou en est la SELARL ?"

Techniquement, le perimetre SELARL simple medecin/dentiste + regime
communautaire est quasiment ferme. Les corrections retours humains 006 sont
faites, testees, integrees dans le pack 005 et auditees cote Codex. Le dernier
audit incident a trouve puis corrige `DOC-002` : l'autorisation de domiciliation
rend maintenant `pour 99 ans`.

Il reste une validation finale humaine du pack corrige. Les variantes complexes
ne sont pas fermees par ce sprint et doivent etre traitees une par une.

## Prochaine action recommandee

Faire valider le pack corrige apres retours humains 006 :

- transmettre `artifacts/selarl_closing_pack_005/` ;
- transmettre `docs/review/selarl_final_validation_001_brief_v1.md` ;
- demander a l'associe uniquement une validation ou des ecarts concrets.
