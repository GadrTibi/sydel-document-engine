# TRACK-B-SELARL-ROLLOUT-NEXT-CASE-001 - Rapport V1

## Contexte prouve

- `pwd` : `C:\Users\Gad\Desktop\Sydel\sydel-track-b`
- `git rev-parse --show-toplevel` : `C:/Users/Gad/Desktop/Sydel/sydel-track-b`
- `git branch --show-current` : `track-b/clean-rebuild`
- `git rev-parse HEAD` : `cc54110df73fe5b3df2268710c38b2d6d6d0d05f`
- `git status --short --branch` : worktree deja modifiee par les tickets Track B SELARL precedents, aucun reset effectue.

## References lues

- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`
- `docs/project/SELARL_PRODUCTION_FACTORY_V1.md`
- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`
- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`

## Matrice courte des cas SELARL restants utiles

| Cas | Delta vs dentiste verrouille | Sources humaines suffisantes | Risque | Priorite | Decision |
|---|---|---|---|---|---|
| SELARL medecin unipersonnelle standard | Remplacer `DOC-016` par `DOC-017`, conserver les documents courts communs, pas de `DOC-005` par defaut. | Oui pour lancer : source DOCX `Modele statuts SELARL medecins`, specs statuts SEL et clean front existant. Non pour un lock humain ligne par ligne equivalent au dentiste. | Faible. | P1 | GO |
| SELARL medecin avec regime communautaire | Meme base que medecin standard, plus `DOC-005` deja verrouille sur les corrections humaines. | Oui pour smoke technique ; lock humain complet non distinct du cas standard. | Faible a moyen. | P2 | GO plus tard, pas choisi ici pour garder un seul delta. |
| SELARL multi-associes creation | Repetition `associes[]`, attribution du capital par associe, signatures multiples, PV president de seance non unique. | Non : wording humain multi-associes, president de seance et signatures multiples a valider. | Eleve. | P3 | NO-GO |
| SELARL plusieurs gerants / president distinct | Bloc identite complet multi-dirigeants, ordre du jour et signatures a pluraliser. | Non : formulations humaines longues et regles de rattachement manquantes. | Eleve. | P4 | NO-GO |
| SELARL cession cabinet medical ou dentaire | Ajout sous-scenario cession, donnees cedant/cessionnaire/prix/conditions, actes et compromis Lot 03. | Partiel : sources et specs existent, mais clean front Track B ne saisit pas encore le sous-formulaire complet. | Moyen a eleve. | P5 | NO-GO dans ce ticket |
| SELARL cession SCM | Ajout sous-scenario SCM avec associes avant/apres, cessionnaire, prix, SDE et actes Lot 05. | Partiel : moteur/sources existent, clean front Track B ne fournit pas encore les donnees complexes. | Eleve. | P6 | NO-GO dans ce ticket |
| SELARL derogation / site distinct | Documents `DOC-013` / `DOC-014`, formulaires ou traitements manuels/reserves. | Non pour production automatisee Track B. | Eleve. | P7 | NO-GO |
| `DOC-006` conjoint commun en biens | Document reserve distinct de `DOC-005`. | Non : reserve source maintenue. | Moyen. | P8 | NO-GO |

## Cas choisi

Cas recommande : SELARL medecin unipersonnelle standard.

Justification :

- c'est le plus petit delta reel apres le lock dentiste ;
- il utilise le meme clean front Track B et les memes documents courts deja verrouilles ;
- il prouve que la methode dentiste peut etre rejouee sans rouvrir le texte dentiste ;
- le moteur dispose deja de `DOC-017` et de la selection front `medecin -> DOC-017` ;
- les cas plus complexes demandent des sources ou des sous-formulaires que le ticket interdit d'inventer.

## Execution du GO

Delta utile applique :

- aucun changement moteur/front, car le cas medecin standard etait deja cable proprement ;
- lancement de production effectue par smoke DOCX/ZIP et controle texte ;
- aucune reecriture juridique du `DOC-017` sans nouvelle reference humaine.

Documents generes :

- `declaration_non_condamnation.docx`
- `autorisation_domiciliation.docx`
- `procuration.docx`
- `pv_nomination_gerant.docx`
- `demande_inscription_ordre.docx`
- `statuts_selarl_medecin.docx`
- `dossier_generation.zip`

Artefacts :

- `artifacts/track_b_selarl_rollout_next_case_001_medecin`
- `artifacts/track_b_selarl_rollout_next_case_001_medecin/dossier_generation.zip`

Controles smoke :

- 6 DOCX produits ;
- ZIP produit ;
- `statuts_selarl_medecin.docx` present ;
- `statuts_selarl_chirurgien_dentiste.docx` absent ;
- aucun placeholder residuel `[` / `]` ;
- aucun segment parasite `RCS PARIS 788 531 432` ;
- aucun segment parasite `0153814303` ;
- PV conserve l'introduction humaine `Les associes de la SELARL...` apres normalisation ;
- procuration conserve `Fait pour servir et valoir ce que de droit.`

## Statuts documentaires

| Document | Statut | Commentaire |
|---|---|---|
| DOC-001 DNC | LOCKED | Correction humaine du format adresse heritee du pack dentiste. |
| DOC-002 Autorisation domiciliation | LOCKED | Formulation siege/cabinet heritee du pack dentiste. |
| DOC-003 Procuration | LOCKED | RCS/telephone parasites absents, clause finale presente. |
| DOC-004 PV nomination gerant | LOCKED | Corrections humaines ciblees conservees. |
| DOC-034 Demande inscription ordre | PARTIAL | Generateur existant et smoke OK ; pas de lock humain specifique dans le ticket dentiste. |
| DOC-017 Statuts SELARL medecin | PARTIAL | Cas GO et generable ; source/spec existantes, mais pas de reference humaine ligne par ligne equivalente au dentiste. |
| DOC-016 Statuts SELARL chirurgien-dentiste | LOCKED | Non rouvert ; reste le golden standard articles 1 a 34. |

## OPEN GAPS

- `DOC-017` n'a pas encore de lock humain ligne par ligne equivalent au `DOC-016` dentiste.
- Les variantes multi-associes, multi-gerants, president de seance distinct, cessions, SCM, derogations, site distinct et `DOC-006` ne doivent pas etre codees depuis ce ticket sans source ou sous-formulaire complementaire.
- Le wrapper post-article de `DOC-016` reste l'OPEN GAP de perimetre deja documente dans le ticket `003`.

## Backlog restant indicatif

Ces items sont l'ordre de risque restant constate, pas une suggestion de ticket :

1. SELARL medecin avec regime communautaire, en reutilisant `DOC-005` deja verrouille.
2. SELARL multi-associes / president de seance / plusieurs gerants, apres source humaine complete.
3. SELARL cession medicale ou dentaire, apres sous-formulaire clean front complet.

## Validations

- Smoke DOCX/ZIP SELARL medecin : OK.
- Controle texte smoke : OK.
- Tests cibles : OK, 41 tests passes.
- `ruff check .` : OK.
- Clean front Track B : HTTP 200 sur `http://localhost:8525`.
- Process front : arret controle apres sonde HTTP ; verification finale `remaining=0` sur les processus Python/Streamlit.
