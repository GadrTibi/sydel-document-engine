# SELAS smoke regime communautaire 001

Date : 2026-06-02

Ticket : `SELAS-SMOKE-REGIME-COMMUNAUTAIRE-001`

Statut : `DONE_PARTIAL_QA`

Decision sprint : `GO test interne ; NO-GO pack final SELAS`

## Objet

Generer et verifier le pack SELAS V1 avec regime communautaire active.

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
regime_communautaire = true
conjoint renseigne
qualite renoncee = actionnaire
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
DOC-005
DOC-006
```

Documents non selectionnes comme attendu :

```text
DOC-004
cession
SCM
bail
derogations
attestation capital SELAS reservee
```

## Artefacts generes

Repertoire smoke :

```text
artifacts/selas_smoke_regime_communautaire_001/20260602_133412/
```

Fichiers generes :

```text
declaration_non_condamnation.docx
autorisation_domiciliation.docx
procuration.docx
demande_inscription_ordre.docx
lettre_renonciation_associe.docx
lettre_avertissement_conjoint.docx
statuts_selas_medecin.docx
manifest.json
```

## Controles realises

Tous les controles ci-dessous sont passes :

| Controle | Resultat |
| --- | --- |
| Selection exacte `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018`, `DOC-005`, `DOC-006` | OK |
| Nombre de DOCX generes = 7 | OK |
| Presence de `DOC-005` et `DOC-006` si regime communautaire | OK |
| Absence de `DOC-004` PV nomination gerant | OK |
| Absence de documents cession / SCM / bail / derogation / attestation capital reservee | OK |
| Absence de placeholders `[` / `]` dans les textes extraits | OK |
| Absence de `SELARL` dans le pack | OK |
| Absence de `Gerant` / `gérant` / `Gérant` dans le pack | OK |
| Absence de `parts sociales` dans le pack | OK |
| Renonciation : presence `personnellement actionnaire de cette société` | OK |
| Renonciation : absence `personnellement associé de cette société` | OK |
| Avertissement : presence `à la SELAS RC SANTE` | OK |
| Documents regime communautaire : absence de `Directeur General` / `Directeur Général` | OK |
| Procuration : presence `Agissant en qualité de President` | OK |
| Statuts : presence `actions` | OK |
| Statuts : presence `President` | OK |

## Limites

- Ce smoke ne vaut pas validation juridique.
- Ce smoke ne remplace pas le checkpoint trois sources.
- Ce smoke ne remplace pas la revue humaine Gad / associe / juriste.
- Aucun PDF ni ZIP final n'a ete produit dans ce ticket ; ils restent prevus
  dans les tickets de cloture technique.
- Les documents generes restent des artefacts internes de test.
- `pytest` et `ruff` restent a relancer dans un environnement equipe si les
  dependances dev ne sont pas disponibles localement.

## Decision de sortie

Le parcours SELAS avec regime communautaire produit un pack DOCX coherent et
borne.

Prochaine action recommandee : `SELAS-ANTI-REGRESSION-WORDING-001`.
