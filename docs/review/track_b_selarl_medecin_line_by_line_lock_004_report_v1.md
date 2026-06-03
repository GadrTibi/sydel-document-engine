# TRACK-B-SELARL-MEDECIN-LINE-BY-LINE-LOCK-004 - Rapport V1

## Contexte prouve

- `pwd` : `C:\Users\Gad\Desktop\Sydel\sydel-track-b`
- `git rev-parse --show-toplevel` : `C:/Users/Gad/Desktop/Sydel/sydel-track-b`
- `git branch --show-current` : `track-b/clean-rebuild`
- `git rev-parse HEAD` : `cc54110df73fe5b3df2268710c38b2d6d6d0d05f`
- `git status --short --branch` : worktree deja modifiee par les tickets Track B SELARL precedents, aucun reset effectue.

## References lues

- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`
- `docs/project/SELARL_PRODUCTION_FACTORY_V1.md`
- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md`
- `docs/review/track_b_selarl_rollout_next_case_001_report_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `project/source_documents/lot_04/Modèle statuts SELARL médecins.docx`
- `C:\Users\Gad\Downloads\Retours humains .docx`

## Mini-matrice des sources medecin

| Source | Niveau de confiance | Portee couverte | Suffisante pour lock ligne par ligne |
|---|---|---|---|
| `C:\Users\Gad\Downloads\Retours humains .docx` | Eleve comme dernier retour humain, faible pour `DOC-017` | Corrections documents courts et bloc humain dentiste ; pas de bloc medecin complet identifie. | Non pour `DOC-017`. |
| `project/source_documents/lot_04/Modèle statuts SELARL médecins.docx` | Eleve comme source documentaire repo du `DOC-017`, semi-humain/source de travail | Couverture complete des statuts medecin : couverture, articles 1 a 36, signature, annexe. | Oui pour un lock source-level, avec une exclusion documentee. |
| `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md` | Moyen | Selection overlay, mapping et regles de blocage. | Non seul ; utile pour qualifier le scope. |
| `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md` | Moyen | Description texte des overlays, points ouverts multi-associes et particularites medecin. | Non seul ; utile pour qualifier le scope. |
| `project/source_truth/Documents_a_generer_par_cas.docx` et docs SELARL de pilotage | Eleve pour le choix documentaire | Confirme `DOC-017` pour SELARL medecin, pas le texte ligne par ligne. | Non seul. |
| Code/templates existants | Faible comme source juridique | Implementation a verifier. | Non comme source, seulement comme rendu compare. |

## Decision GO / NO-GO

Decision : GO limite.

Le verrouillage ligne par ligne est possible contre la source repo `Modèle statuts SELARL médecins.docx`, qui est la source documentaire exploitable du `DOC-017`.

Ce lock n'est pas strictement de meme nature que le lock dentiste :

- le dentiste a ete compare a un bloc humain complet issu du retour utilisateur ;
- le medecin est compare a la source DOCX projet existante ;
- aucun retour humain medecin plus recent ou plus strict n'a ete trouve.

## Methode de comparaison

- Generation smoke SELARL medecin unipersonnelle standard depuis le clean front Track B.
- Extraction des paragraphes du `DOC-017` source et du `DOC-017` genere.
- Substitution des placeholders source par les valeurs du contexte smoke.
- Comparaison a partir de `ARTICLE 1`.
- Conservation dans le controle du bloc signature et annexe, car ils sont dans la source medecin apres l'article 36.
- Exclusion explicite d'une ligne source invalide :
  `[civilite_personne_2] [prenom_personne_2] [nom_personne_2] ... [nb_parts_total] parts`

Cette ligne n'est pas generable en dossier unipersonnel standard et etait deja neutralisee par le generateur via `skip_personne_2_line=True`.

## Resultat ligne par ligne

- Source brute a partir de `ARTICLE 1` : 312 paragraphes.
- Source exploitable apres exclusion de la ligne `personne_2` : 311 paragraphes.
- Rendu genere a partir de `ARTICLE 1` : 311 paragraphes.
- Ecarts ligne par ligne : 0.
- Articles couverts : `ARTICLE 1` a `ARTICLE 36`.
- Signature et annexe source medecin : couvertes.

## Statut DOC-017

Statut : LOCKED source-level pour la SELARL medecin unipersonnelle standard.

Perimetre LOCKED :

- couverture et corps des statuts medecin generes depuis `DOC-017` ;
- articles 1 a 36 ;
- signature ;
- annexe ;
- selection clean front `profession=medecin -> DOC-017` ;
- absence de `DOC-016` dans le pack medecin.

OPEN GAPS rattaches :

- pas de retour humain medecin recent equivalent au bloc dentiste du ticket `003` ;
- ligne source `personne_2` incomplete non retenue en unipersonnel ;
- multi-associes medecin hors lock ;
- regime communautaire medecin avec `DOC-005` non relu comme pack medecin specifique dans ce ticket.

## Documents du pack medecin

| Document | Statut | Decision |
|---|---|---|
| DOC-001 DNC | LOCKED | Herite du lock documents courts. |
| DOC-002 Autorisation domiciliation | LOCKED | Herite du lock documents courts. |
| DOC-003 Procuration | LOCKED | Herite du lock documents courts. |
| DOC-004 PV nomination gerant | LOCKED | Herite du lock documents courts. |
| DOC-034 Demande inscription ordre | PARTIAL | Smoke OK, mais pas de lock humain specifique dans cette serie de tickets. |
| DOC-017 Statuts SELARL medecin | LOCKED source-level | 311/311 paragraphes source exploitables alignes, 0 ecart. |
| DOC-016 Statuts SELARL chirurgien-dentiste | LOCKED | Non rouvert ; golden standard conserve. |

## Artefacts generes

- `artifacts/track_b_selarl_medecin_line_by_line_lock_004`
- `artifacts/track_b_selarl_medecin_line_by_line_lock_004/dossier_generation.zip`

Documents generes :

- `declaration_non_condamnation.docx`
- `autorisation_domiciliation.docx`
- `procuration.docx`
- `pv_nomination_gerant.docx`
- `demande_inscription_ordre.docx`
- `statuts_selarl_medecin.docx`

## Controle texte smoke

- 6 DOCX produits.
- ZIP produit.
- Aucun placeholder residuel `[` / `]`.
- Aucun segment parasite `RCS PARIS 788 531 432`.
- Aucun segment parasite `0153814303`.
- `statuts_selarl_medecin.docx` present.
- `statuts_selarl_chirurgien_dentiste.docx` absent.

## Delta exact vs ticket precedent

- Ajout d'un test ligne par ligne `DOC-017` contre la source DOCX medecin.
- Ajout du rapport de lock `004`.
- Mise a jour du backlog et de la memoire projet.
- Aucun changement de wording juridique.
- Aucun changement front.
- Aucun changement du lock dentiste.

## Validations

- Tests cibles `tests/unit/test_lot_04_statuts_sel_exercice.py` : OK, 11 passes.
- Tests cibles complets SELARL/documents : OK, 62 passes.
- `ruff check .` : OK.
- Smoke DOCX/ZIP medecin : OK.
- Clean front Track B : HTTP 200 sur `http://localhost:8526`.
- Process front : nettoyage manuel apres sonde Streamlit ; verification finale `remaining=0`.
