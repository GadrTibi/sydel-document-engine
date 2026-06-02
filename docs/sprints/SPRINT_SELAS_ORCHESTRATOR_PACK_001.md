# SELAS orchestrator pack 001

Date : 2026-06-02

Ticket : `SELAS-ORCHESTRATOR-PACK-001`

Statut : `DONE_PARTIAL_QA`

Decision sprint : `NO-GO pack final SELAS`

## Objet

Brancher la selection du pack SELAS V1 dans l'orchestrateur, sans ouvrir les cas
hors V1 et sans modifier le wording juridique.

Ce ticket ne cloture pas la SELAS, ne vaut pas revue humaine, ne realise pas le
checkpoint trois sources et ne produit pas encore de pack final valide.

## Perimetre inclus

Pack SELAS V1 simple :

```text
SELAS medecin
actionnaire unique
President unique
creation simple
capital en numeraire
actions ordinaires
statuts_sel.overlay = selas_medecin
```

Documents selectionnes par l'orchestrateur pour le pack simple :

```text
DOC-001
DOC-002
DOC-003
DOC-034
DOC-018
```

Documents conditionnels ajoutes si `dossier_options.regime_communautaire = true` :

```text
DOC-005
DOC-006
```

## Cas bloques

La selection explicite du pack SELAS V1 bloque :

- structure autre que `SELAS` ;
- overlay statuts autre que `selas_medecin` ;
- cession ;
- SCM / cession SCM ;
- site distinct ;
- derogation ;
- multi-actionnaires ;
- nomination effective d'un Directeur General ;
- capital non divise en actions si le champ est renseigne.

La selection generique `select_documents_for_context(...)` filtre aussi les
documents SELAS hors readiness V1 afin de ne pas activer par accident `DOC-004`,
cession, SCM ou autres satellites reserves.

## Changements techniques

- Ajout de `UnsupportedSelasPackContextError`.
- Ajout de `DocumentOrchestrator.select_selas_v1_pack_documents(ctx)`.
- Raccordement a `selas_pack_readiness(...)` pour respecter l'ordre et les
  documents actifs cote front/data.
- Ajout d'un filtre SELAS V1 dans `_document_enabled_for_context(...)`.
- Tests cibles ajoutes dans `tests/unit/test_orchestrator_service.py`.

## Validations realisees

```text
compileall service/test orchestrateur : OK
smoke selection pack simple : OK
smoke selection pack regime communautaire : OK
smoke blocages hors V1 : OK
tests directs orchestrateur SELAS : 4 tests OK
test direct regime communautaire selection orchestrateur : OK
```

Limite locale :

```text
pytest : indisponible localement
ruff : indisponible localement
```

Ces commandes doivent etre relancees dans un environnement avec dependances dev.

## Decision de sortie

L'orchestrateur sait maintenant selectionner le pack SELAS V1 sans ouvrir les
cas complexes.

Prochaine action recommandee : `SELAS-SMOKE-HAPPY-PATH-001`.
