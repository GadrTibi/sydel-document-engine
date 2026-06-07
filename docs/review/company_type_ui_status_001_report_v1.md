# PROJECT-COMPANY-TYPE-UI-STATUS-001 report V1

Date : 2026-06-02

## Objet

Durcir l'affichage Assistant metier pour aligner le front/rapport sur le registre
de statut des types d'entreprise :

```text
Present dans le catalogue ou le moteur != traite comme type d'entreprise.
```

## Decision produit appliquee

- `SELARL` reste le seul type marque `generable_in_v1=True`.
- `SELAS` reste visible comme sprint actif, mais `NO-GO dev` et non generable
  produit V1.
- `SCI`, `SCM`, `SAS`, `SCS`, `SPFPL cession` et `SPFPL apport` restent visibles
  en diagnostic catalogue, mais sont marques `INVENTAIRE_TECHNIQUE`.
- Le mode diagnostic historique n'est pas supprime : il sert encore aux tests de
  non-regression catalogue.

## Changements

- `src/sydel_doc_engine/app/business_wizard.py`
  - ajout des ensembles `PRODUCT_TREATED_CASE_TYPES` et
    `PRODUCT_GENERABLE_CASE_TYPES` ;
  - `business_dossier_types()` ne met plus `generable_in_v1=True` sur tous les
    `CaseType` ;
  - labels et statuts distinguent sprint produit, `NO-GO dev` et inventaire
    technique ;
  - warnings de validation ajoutes pour les types hors sprint produit ou non
    generables.

- `tests/unit/test_business_wizard.py`
  - test du contrat de statut produit ;
  - test du warning `INVENTAIRE_TECHNIQUE`.

## Coordination Git

Sous-agent Git/Branch utilise avant edition : Curie.

Constats utiles :

- branche locale : `track-b/clean-rebuild` ;
- remote : `https://github.com/GadrTibi/sydel-document-engine.git` ;
- tracking : `origin/track-b/clean-rebuild`, `ahead 2` ;
- index clean ;
- worktree tres dirty, avec risque de collision sur les fichiers front.

Decision d'execution : travailler en patch minimal, sans formatage large, sans
stash, reset, checkout, commit ou push.

## Fichiers volontairement evites

- generateurs SELARL ;
- tests generateurs SELARL ;
- rapports `docs/review/selarl_*` ;
- clean front SELARL hors lecture de contexte.

## Validations

```text
.\.venv\Scripts\python.exe -m ruff check src/sydel_doc_engine/app/business_wizard.py tests/unit/test_business_wizard.py
```

Resultat : OK.

```text
.\.venv\Scripts\python.exe -m pytest tests/unit/test_business_wizard.py -q
```

Resultat : OK, 42 tests passes.

## Risques residuels

- Le mode Assistant metier conserve la generation diagnostic historique pour les
  types en inventaire technique. C'est volontaire pour ne pas casser les tests de
  non-regression catalogue, mais ce mode ne doit pas etre presente comme produit
  final.
- Le worktree reste sale avec des changements SELARL paralleles. Aucun commit ou
  push n'a ete fait dans ce ticket.

## Prochaine action recommandee

Poursuivre `SELARL-RETURNS-006-PV-001` si Gad continue les corrections SELARL en
parallele, ou attendre un Sync packet/commit pousse de Naomi avant toute
requalification SELAS.
