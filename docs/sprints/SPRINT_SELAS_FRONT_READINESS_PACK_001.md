# SELAS front readiness pack 001

Date : 2026-06-02

Ticket : `SELAS-FRONT-READINESS-PACK-001`

Statut : `DONE_PARTIAL_QA`

Decision sprint : `NO-GO pack SELAS`

## Objet

Aligner la couche front/data pour que le parcours SELAS V1 distingue clairement :

- les documents prets du pack simple ;
- les documents conditionnels ;
- les documents reserves ;
- les cas hors V1 a bloquer ;
- le prochain ticket d'orchestration.

Ce ticket ne branche pas l'orchestrateur de lot, ne genere pas de pack DOCX/PDF/ZIP
SELAS et ne modifie aucun wording juridique.

## Perimetre V1 expose au front

Parcours simple :

```text
SELAS medecin
actionnaire unique
President unique
creation simple
capital en numeraire
actions ordinaires
sans Directeur General
sans multi-actionnaires
sans actions complexes
```

Documents prets pour le pack simple :

| Code | Document | Statut front |
| --- | --- | --- |
| `DOC-001` | DNC President | Pret |
| `DOC-002` | Attestation de domiciliation | Pret |
| `DOC-003` | Procuration President | Pret |
| `DOC-034` | Demande d'inscription a l'Ordre | Pret |
| `DOC-018` | Statuts SELAS medecin actionnaire unique | Pret |

Documents conditionnels :

| Code | Document | Declencheur |
| --- | --- | --- |
| `DOC-005` | Lettre de renonciation conjoint | Regime communautaire |
| `DOC-006` | Lettre d'avertissement conjoint | Regime communautaire |

Documents reserves :

| Code | Decision |
| --- | --- |
| `SELAS-DECISION-PRESIDENT` | Reserve : nomination President absorbee par les statuts V1 |
| `SELAS-STATUTS-DENTISTE` | Reserve : source/spec dentiste SELAS non traitee dans cette V1 |
| `SELAS-ATTESTATION-CAPITAL` | Reserve : source canonique exacte a identifier avant promesse produit |

## Changements techniques

- Ajout d'un objet `SelasPackReadiness` dans
  `src/sydel_doc_engine/front_data/selas_schema.py`.
- Ajout des listes explicites :
  `SELAS_READY_DOCUMENT_CODES`, `SELAS_CONDITIONAL_DOCUMENT_CODES` et
  `SELAS_RESERVED_DOCUMENT_CODES`.
- Exposition de `pack_readiness` dans `SelasFrontSchema`.
- Maintien de `generation_enabled=False`.
- Ajout du prochain ticket technique : `SELAS-ORCHESTRATOR-PACK-001`.
- Sortie de `SELAS-DECISION-PRESIDENT` des candidats generables et maintien en
  reserve.
- Nettoyage des anciennes ambiguittes front deja levees par les specs/devs :
  `DOC-003` et `DOC-018` ne restent plus bloques par les anciens verrous de
  readiness.
- Expansion des champs canoniques attendus pour `DOC-018` afin que le front voie
  les donnees capital/actions, President, actionnaire, Ordre, banque et
  signature necessaires.
- Export des nouveaux objets depuis `src/sydel_doc_engine/front_data/__init__.py`.
- Tests cibles ajoutes dans `tests/unit/test_selas_front_schema.py`.

## Validations realisees

```text
compileall ciblé : OK
tests SELAS front directs : 13 tests executes OK
smoke schema simple : OK
smoke schema regime communautaire : OK
git diff --check : OK
```

Limite locale :

```text
pytest : indisponible localement
ruff : indisponible localement
```

Ces commandes doivent etre relancees dans un environnement avec dependances dev.

## Decision de sortie

Le front/data sait maintenant presenter le pack SELAS V1 comme un pack en attente
d'orchestration :

- pack simple actif cote readiness : `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`,
  `DOC-018` ;
- pack regime communautaire actif cote readiness : les cinq documents simples
  plus `DOC-005` et `DOC-006` ;
- generation de pack toujours inactive ;
- prochain ticket : `SELAS-ORCHESTRATOR-PACK-001`.

Prochaine action recommandee : `SELAS-ORCHESTRATOR-PACK-001`.
