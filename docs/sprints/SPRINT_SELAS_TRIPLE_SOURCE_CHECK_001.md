# SELAS triple source check 001

Date : 2026-06-02

Ticket : `SELAS-TRIPLE-SOURCE-CHECK-001`

Statut : `DONE_PARTIAL_QA`

Decision sprint : `GO revue humaine ; NO-GO cloture SELAS V1`

## Objet

Comparer la premiere version totale SELAS V1 contre les trois reperes demandes :

1. source metier `project/source_truth/Documents_a_generer_par_cas.docx` ;
2. journal NotebookLM SELAS `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md` ;
3. retours humains disponibles sur la SELAS.

Ce ticket ne modifie pas le code, ne modifie aucune source DOCX, ne change aucun
wording juridique et ne valide pas le pack SELAS final.

## Artefacts de controle

```text
artifacts/selas_triple_source_check_001/20260602_135234/
```

Fichiers :

```text
manifest.json
source_truth_text.txt
source_truth_hits.json
source_truth_hits.md
notebooklm_hits.json
notebooklm_hits.md
human_returns_scan.json
```

## Packs compares

| Pack | Artefact | Documents generes |
| --- | --- | --- |
| Happy path SELAS V1 | `artifacts/selas_smoke_happy_path_001/20260602_130911/` | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018` |
| Regime communautaire SELAS V1 | `artifacts/selas_smoke_regime_communautaire_001/20260602_133412/` | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-034`, `DOC-018`, `DOC-005`, `DOC-006` |

## Source 1 - document a generer par cas

Lecture de `project/source_truth/Documents_a_generer_par_cas.docx`.

Points confirmes pour le perimetre V1 :

| Point | Constat source | Impact pack actuel |
| --- | --- | --- |
| Documents communs | DNC, domiciliation et procuration sont listes dans les docs a generer dans tous les cas | Presents dans les deux packs |
| SELAS | Une section SELAS existe dans la source | Le sprint reste bien sur le cas SELAS, pas une extrapolation SELARL seule |
| Demande d'inscription a l'Ordre | Listee dans le bloc SELAS | `DOC-034` present dans les deux packs |
| Statuts SELAS medecin | Source rattachee a `Statuts_SELAS_medecin.docx` | `DOC-018` present dans les deux packs |
| Regime communautaire | Lettres de renonciation et d'avertissement listees comme conditionnelles | `DOC-005` et `DOC-006` presents uniquement dans le pack regime communautaire |
| SCM / cession / derogation | Documents listes comme conditionnels | Non presents dans les packs V1 simples, ce qui est conforme au scope V1 |

Ecart a surveiller :

| Point | Source | Decision V1 |
| --- | --- | --- |
| `PV nomination gerant` apparait dans la zone SELAS | La source metier conserve le nom de modele historique | En V1, `DOC-004` reste reserve car la nomination President est absorbee par les statuts SELAS medecin AU ; a faire relire humainement |
| Attestation capital / liste souscripteurs | La source rattache ce sujet surtout a SPFPL/SELAS/SCS selon les lignes extraites | Reserve V1 : source canonique exacte a identifier avant promesse produit |

## Source 2 - NotebookLM SELAS

Lecture de `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`.

Points alignes avec le pack actuel :

| Point NotebookLM | Decision pack |
| --- | --- |
| President SELAS au lieu de Gerant | Controle anti-regression strict OK, aucun `Gerant` dans les packs |
| Actions au lieu de parts sociales | Controle anti-regression strict OK, aucun `parts sociales` dans les packs |
| DNC, procuration, Ordre et statuts attendus dans le lot simple | Presents dans le pack happy path |
| Regime communautaire conditionnel | Active seulement dans le pack regime communautaire |
| Directeur General non trouve | Bloque hors V1 |
| Multi-actionnaires, actions de preference, cession, SCM, site distinct | Restent reserves / hors V1 |
| Revue humaine avant cloture | Prochaine etape obligatoire |

Points NotebookLM non fermes :

| Point | Statut |
| --- | --- |
| Filiation DNC President | NotebookLM indique non trouve ; le moteur la garde obligatoire par prudence source/spec |
| Plans/devis Ordre | Pieces attendues, pas documents generes ; caractere bloquant a arbitrer humainement |
| Numerotation detaillee des actions | V1 limitee a numerotation simple `1 a N` |
| Liste complete des 62 documents SELAS | Non reproduite comme source exploitable ; le sprint V1 ne pretend pas couvrir toute la SELAS |

## Source 3 - retours humains disponibles

Retour humain SELAS trouve :

| Fichier | Nature | Impact |
| --- | --- | --- |
| `docs/sprints/SPRINT_SELAS_GAD_FEEDBACK_001.md` | Retour Gad sur la strategie cas par cas / reutilisation SELARL | Confirme la ligne produit : reutiliser le socle, mais ne pas generer tous les cas d'un coup |

Retours humains non encore trouves :

| Retour attendu | Statut |
| --- | --- |
| Relecture Gad / associe / juriste du pack SELAS V1 genere | Non presente dans le depot |
| Corrections humaines sur les DOCX SELAS V1 | Non presentes |
| Validation finale du wording `associe` / `actionnaire` dans les statuts, Ordre et renonciation | Non presente |

Conclusion : la troisieme source existe seulement sous forme de retour produit
pre-dev. Elle ne remplace pas la revue humaine de la premiere version totale.

## Occurrences `associe` / `actionnaire`

Le ticket precedent a classe 173 paragraphes contenant `associe` / `associé`.

Decision du checkpoint :

| Zone | Decision |
| --- | --- |
| Statuts SELAS medecin | Occurrences coherentes avec la source statuts SELAS, mais a faire relire humainement avant cloture |
| Demande d'inscription a l'Ordre | Occurrence a revalider humainement car l'overlay Ordre peut utiliser des termes transverses |
| Lettre de renonciation | Le corps contient bien `actionnaire`; l'occurrence restante vient du titre/source du document, a confirmer humainement |

Aucune correction automatique n'est autorisee sur ces occurrences.

## Decision de sortie

Verdict :

```text
PASS source metier + NotebookLM sur le perimetre SELAS V1
NO-GO cloture finale faute de retour humain pack
GO preparation revue humaine
```

Le pack SELAS V1 est coherent avec le perimetre developpe :

- SELAS medecin ;
- actionnaire unique ;
- President unique ;
- creation simple ;
- capital en numeraire ;
- actions ordinaires ;
- sans DG ;
- sans multi-actionnaires ;
- sans cession ;
- sans SCM ;
- sans site distinct ;
- sans micro-holding ;
- sans actions de preference.

Il ne couvre pas encore toute la SELAS. Les reserves restent :

- SELAS dentiste ;
- Decision/PV President separe ;
- attestation capital / liste souscripteurs SELAS ;
- multi-actionnaires ;
- Directeur General ;
- actions de preference ;
- micro-holding ;
- cession de fonds / cabinet ;
- SCM ;
- site distinct / derogation ;
- plans/devis Ordre comme blocage produit eventuel.

## Prochaine action recommandee

Lancer :

```text
SELAS-HUMAN-REVIEW-PACK-001
```

Objectif : preparer le pack a envoyer a Gad / associe / juriste, avec les
questions de revue ciblees sur les points non fermes :

- faut-il un acte separe de nomination President ou la nomination dans les
  statuts V1 suffit-elle ?
- les occurrences `associe` restantes sont-elles acceptees dans les statuts,
  Ordre et renonciation SELAS ?
- les plans/devis Ordre doivent-ils bloquer le parcours ?
- faut-il promettre ou reserver l'attestation capital / liste souscripteurs
  SELAS ?
- la DNC President doit-elle conserver la filiation obligatoire ?
