# SELAS smoke happy path 001

Date : 2026-06-02

Ticket : `SELAS-SMOKE-HAPPY-PATH-001`

Statut : `DONE_PARTIAL_QA`

Decision sprint : `GO test interne ; NO-GO pack final SELAS`

## Objet

Generer et verifier le pack SELAS V1 simple, sans regime communautaire et sans
cas complexe.

Ce ticket ne modifie pas le code, ne modifie aucune source DOCX, ne change aucun
wording juridique et ne cloture pas la SELAS V1.

## Scenario smoke

Perimetre teste :

```text
SELAS medecin
actionnaire unique
President unique
creation simple
capital en numeraire
actions ordinaires
statuts_sel.overlay = selas_medecin
regime_communautaire = false
aucune cession
aucune SCM
aucun site distinct
aucune derogation
aucun Directeur General nomme
```

## Resultat selection orchestrateur

Documents selectionnes :

```text
DOC-001
DOC-002
DOC-003
DOC-034
DOC-018
```

Documents non selectionnes comme attendu :

```text
DOC-004
DOC-005
DOC-006
cession
SCM
derogations
```

## Artefacts generes

Repertoire smoke :

```text
artifacts/selas_smoke_happy_path_001/20260602_130911/
```

Fichiers generes :

```text
declaration_non_condamnation.docx
autorisation_domiciliation.docx
procuration.docx
demande_inscription_ordre.docx
statuts_selas_medecin.docx
manifest.json
```

## Controles realises

Tous les controles ci-dessous sont passes :

| Controle | Resultat |
| --- | --- |
| Selection exacte `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018` | OK |
| Nombre de DOCX generes = 5 | OK |
| Absence de `DOC-005` / `DOC-006` sans regime communautaire | OK |
| Absence de `DOC-004` PV nomination gerant | OK |
| Absence de placeholders `[` / `]` dans les textes extraits | OK |
| Absence de `SELARL` dans le pack | OK |
| Absence de `Gerant` / `gérant` / `Gérant` dans le pack | OK |
| Absence de `parts sociales` dans le pack | OK |
| Procuration : presence `Agissant en qualité de President` | OK |
| Statuts : presence `actions` | OK |
| Statuts : presence `President` | OK |

## Limites

- Ce smoke ne vaut pas validation juridique.
- Ce smoke ne remplace pas le checkpoint trois sources.
- Ce smoke ne remplace pas la revue humaine Gad / associe / juriste.
- Aucun PDF ni ZIP final n'a ete produit dans ce ticket ; ils restent prevus
  dans les tickets de cloture technique.
- `pytest` et `ruff` restent a relancer dans un environnement equipe si les
  dependances dev ne sont pas disponibles localement.

## Decision de sortie

Le parcours SELAS simple sans regime communautaire produit un pack DOCX
coherent et borne.

Prochaine action recommandee : `SELAS-SMOKE-REGIME-COMMUNAUTAIRE-001`.
