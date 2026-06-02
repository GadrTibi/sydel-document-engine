# SELAS anti regression wording 001

Date : 2026-06-02

Ticket : `SELAS-ANTI-REGRESSION-WORDING-001`

Statut : `DONE_PARTIAL_QA`

Decision sprint : `PASS strict ; REVIEW humain requis sur associe`

## Objet

Verifier les deux packs SELAS V1 deja generes contre les regressions de wording
les plus sensibles :

- `SELARL` ;
- forme longue SELARL / responsabilite limitee ;
- `Gerant` / `Gérant` / `gérant` ;
- `parts sociales` / `part sociale` ;
- occurrences de `associe` / `associé` a classer pour savoir si elles sont mal
  placees.

Ce ticket ne modifie pas le code, ne modifie aucune source DOCX, ne change aucun
wording juridique et ne cloture pas la SELAS V1.

## Packs controles

```text
artifacts/selas_smoke_happy_path_001/20260602_130911/
artifacts/selas_smoke_regime_communautaire_001/20260602_133412/
```

## Artefacts de controle

```text
artifacts/selas_anti_regression_wording_001/20260602_134239/
```

Fichiers :

```text
manifest.json
wording_occurrences.csv
```

## Resultats stricts

| Controle strict | Resultat |
| --- | --- |
| Absence de `SELARL` | OK |
| Absence de forme longue SELARL / responsabilite limitee | OK |
| Absence de `Gerant` / `Gérant` / `gérant` | OK |
| Absence de `parts sociales` | OK |
| Absence de `part sociale` | OK |

Verdict strict : `PASS`.

## Occurrences a revoir

Le controle a trouve 173 paragraphes contenant `associe` / `associé`.

Ces occurrences ne sont pas classees comme regression stricte, car elles se
repartissent ainsi :

| Document | Pack | Occurrences | Classement |
| --- | --- | ---: | --- |
| `statuts_selas_medecin.docx` | happy path | 85 | Source statuts SELAS ; a confirmer au checkpoint trois sources |
| `statuts_selas_medecin.docx` | regime communautaire | 85 | Source statuts SELAS ; a confirmer au checkpoint trois sources |
| `demande_inscription_ordre.docx` | happy path | 1 | Overlay Ordre ; a revalider humainement |
| `demande_inscription_ordre.docx` | regime communautaire | 1 | Overlay Ordre ; a revalider humainement |
| `lettre_renonciation_associe.docx` | regime communautaire | 1 | Titre/source regime communautaire ; a revalider humainement |

Point important : la renonciation contient bien le wording SELAS controle
`personnellement actionnaire de cette société`. L'occurrence restante de
`associé` concerne le titre source du document.

## Decision de sortie

Le pack SELAS V1 passe le controle anti-regression strict.

Il ne peut pas etre valide final pour autant : les occurrences de `associé`
doivent etre examinees dans `SELAS-TRIPLE-SOURCE-CHECK-001`, avec :

1. `project/source_truth/Documents_a_generer_par_cas.docx` ;
2. le journal NotebookLM SELAS ;
3. les retours humains Gad / associe / juriste.

Prochaine action recommandee : `SELAS-TRIPLE-SOURCE-CHECK-001`.
