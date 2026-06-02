# SELAS human review pack 001

Date : 2026-06-02

Ticket : `SELAS-HUMAN-REVIEW-PACK-001`

Statut : `DONE_WAITING_HUMAN_REVIEW`

Decision sprint : `PACK PRET POUR REVUE HUMAINE ; NO-GO cloture SELAS V1`

## Objet

Preparer le pack SELAS V1 a envoyer a Gad / associe / juriste pour relecture
humaine.

Ce ticket ne modifie pas le code, ne regenere pas les DOCX, ne change aucun
wording juridique, ne modifie aucune source DOCX et ne valide pas le pack final.

## Artefacts produits

```text
artifacts/selas_human_review_pack_001/20260602_135708/
artifacts/selas_human_review_pack_001/selas_human_review_pack_001_20260602_135708.zip
```

Fichiers de pilotage :

```text
README_REVIEW.md
QUESTIONS_REVUE.md
CHECKLIST_REVUE.md
INVENTAIRE_PACK.md
NOTEBOOKLM_PRECHECK.md
manifest.json
```

## Documents inclus

### Pack happy path

Chemin :

```text
artifacts/selas_human_review_pack_001/20260602_135708/happy_path/
```

Documents :

| Code | Fichier |
| --- | --- |
| `DOC-001` | `declaration_non_condamnation.docx` |
| `DOC-002` | `autorisation_domiciliation.docx` |
| `DOC-003` | `procuration.docx` |
| `DOC-034` | `demande_inscription_ordre.docx` |
| `DOC-018` | `statuts_selas_medecin.docx` |

### Pack regime communautaire

Chemin :

```text
artifacts/selas_human_review_pack_001/20260602_135708/regime_communautaire/
```

Documents :

| Code | Fichier |
| --- | --- |
| `DOC-001` | `declaration_non_condamnation.docx` |
| `DOC-002` | `autorisation_domiciliation.docx` |
| `DOC-003` | `procuration.docx` |
| `DOC-034` | `demande_inscription_ordre.docx` |
| `DOC-005` | `lettre_renonciation_associe.docx` |
| `DOC-006` | `lettre_avertissement_conjoint.docx` |
| `DOC-018` | `statuts_selas_medecin.docx` |

## Questions jointes a la revue

Les questions bloquantes sont documentees dans :

```text
artifacts/selas_human_review_pack_001/20260602_135708/QUESTIONS_REVUE.md
```

Elles portent sur :

- nomination President dans les statuts ou acte separe ;
- occurrences `associe` / `actionnaire` ;
- titre/fichier de la renonciation conjoint ;
- filiation DNC President ;
- plans/devis Ordre comme blocage ou pieces attendues ;
- attestation capital / liste souscripteurs SELAS ;
- confirmation du perimetre V1 limite ;
- feminisation `President` / `Presidente`.

## Pre-check NotebookLM recu

Naomie a interroge NotebookLM sur les questions de revue.

Synthese utile :

| Sujet | Reponse NotebookLM | Certitude | Statut Codex |
| --- | --- | --- | --- |
| Nomination President dans les statuts ou acte separe | Possible dans les statuts, mais un document distinct est prevu dans l'outil | Moyen | A confirmer humainement |
| `associe` vs `actionnaire` | Adapter le vocabulaire SELAS ; actions obligatoires ; `associe` parfois present | Moyen | A confirmer humainement |
| Titre renonciation conjoint | Source parle de renonciation a etre `associe`, sans trancher SELAS | Faible | A confirmer humainement |
| Filiation DNC | Non trouve | N/A | A confirmer humainement |
| Plans/devis Ordre | Bloquants selon NotebookLM | Fort | A faire trancher produit/juridique pour V1 |
| Attestation capital / liste souscripteurs | Attestation capital listee comme obligatoire | Fort | A arbitrer : ajouter ou reserver |
| Perimetre V1 medecin unipersonnel cash | Tres coherent | Fort | A valider officiellement |
| Feminisation President/Presidente | Point sensible signale | Moyen | Ajoute a la grille de revue |

Le fichier suivant a ete ajoute au pack :

```text
artifacts/selas_human_review_pack_001/20260602_135708/NOTEBOOKLM_PRECHECK.md
```

## Decision de sortie

Le pack est pret pour revue humaine.

Il reste en `NO-GO cloture SELAS V1` tant qu'un retour humain n'est pas revenu
et classe.

## Prochaine action recommandee

Action humaine :

```text
Transmettre le ZIP, le pre-check NotebookLM et les questions a Gad / associe / juriste.
```

Action Codex apres retour :

```text
SELAS-HUMAN-FIXES-001
```

Seulement si des corrections sont demandees. Si le retour humain valide le pack
sans correction, passer a `SELAS-FINAL-SMOKE-ZIP-PDF-001`.
