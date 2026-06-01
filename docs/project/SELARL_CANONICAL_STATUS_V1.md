# SELARL canonical status V1

Ticket source : `SELARL-CANONICAL-STATUS-001`

Date : 2026-06-01

## Role de ce document

Ce fichier est le point d'entree unique pour savoir ou en est la SELARL.

Il ne remplace pas la source de verite juridique. La source metier reste
`project/source_truth/Documents_a_generer_par_cas.docx` et les specs restent
dans `docs/delivery/`.

En revanche, pour l'etat projet, ce fichier prime sur les anciens rapports et
sur les anciennes formulations du type "le front est limite a quatre
documents". Ces formulations sont historiques quand elles contredisent les
tickets Track B plus recents.

La fin de sprint operationnelle est detaillee dans :

- `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`

## Decision produit actuelle

Decision : `NO-GO dev` pour une nouvelle extension SELARL complexe tant que le
prochain sous-cas n'est pas choisi et cadre sous gate produit.

Decision : `GO documentation / reprise projet` pour consolider l'etat, preparer
une revue humaine et garder la methode reutilisable pour les autres formes
sociales.

La SELARL actuelle est un candidat technique avance pour les cas simples. Elle
n'est pas declaree juridiquement finale sur toutes ses variantes.

## Entree technique actuelle

Front Track B propre :

- `src/sydel_doc_engine/front_app/app.py`
- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/front_app/shell.py`
- tests principaux : `tests/unit/test_clean_front_app.py`

Front historique / prototype :

- `src/sydel_doc_engine/app/streamlit_app.py`

Regle : les nouveaux travaux Track B SELARL doivent partir du front propre
`front_app`, sauf ticket explicite contraire.

## Synthese executive

Ce qui est vraiment disponible :

- SELARL unipersonnelle medecin : pack DOCX/ZIP genere depuis le clean front.
- SELARL unipersonnelle chirurgien-dentiste : pack DOCX/ZIP genere depuis le
  clean front.
- Regime communautaire : `DOC-005` ajoute quand l'option est active ;
  `DOC-006` reste reserve et exclu.
- Multi-associes : uniquement deux sous-cas limites existent :
  `DOC-004` seul, ou dentiste `DOC-004` + `DOC-016` en PARTIAL.

Ce qui n'est pas encore proprement disponible :

- statuts multi-associes complets ;
- medecin multi-associes ;
- plusieurs gerants ;
- president de seance externe ;
- cession cabinet medicale ou dentaire dans le front Track B ;
- cession SCM dans le front Track B ;
- derogations et site distinct en generation automatique ;
- validation juridique finale globale.

## Matrice des documents SELARL

| Code | Document | Etat actuel SELARL | Decision |
| --- | --- | --- | --- |
| `DOC-001` | Declaration de non-condamnation | LOCKED sur les corrections humaines du pack simple | Generable dans les packs simples |
| `DOC-002` | Autorisation de domiciliation | LOCKED sur domiciliation siege/cabinet | Generable dans les packs simples |
| `DOC-003` | Procuration | LOCKED sur suppression parasites et clause finale | Generable dans les packs simples |
| `DOC-004` | PV nomination gerant | LOCKED en unipersonnel et en multi-associes simple limite | Generable selon les sous-cas couverts |
| `DOC-005` | Renonciation conjoint commun en biens | LOCKED sur corrections humaines | Generable si regime communautaire actif |
| `DOC-006` | Avertissement conjoint | Reserve source | Ne pas generer automatiquement |
| `DOC-007` | Avenant bail | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-008` | Appel de fonds | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-009` | Acte cession cabinet medical | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-010` | Compromis cession cabinet medical | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-011` | Acte cession cabinet dentaire | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-012` | Compromis cession cabinet dentaire | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-013` | Formulaire multi-sites SEL | Moteur existant mais manuel dans le flux SELARL verifie | Hors generation SELARL automatique |
| `DOC-014` | Demande derogation cumul SELARL BNC | Moteur existant mais manuel dans le flux SELARL verifie | Hors generation SELARL automatique |
| `DOC-016` | Statuts SELARL chirurgien-dentiste | LOCKED articles 1 a 34 en unipersonnel ; PARTIAL en dentiste multi simple | Generable selon scope, PARTIAL en multi |
| `DOC-017` | Statuts SELARL medecin | LOCKED source-level en unipersonnel | Generable medecin simple, pas multi |
| `DOC-031` | PV AGE cession parts SCM | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-032` | Courrier SDE cession SCM | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-033` | Acte cession parts SCM vers SELARL | Generateur moteur existant, sous-formulaire SELARL absent | Bloque front Track B |
| `DOC-034` | Demande inscription a l'ordre | Generable, smoke OK, lock humain specifique absent | PARTIAL a relire humainement |
| sans code | Site distinct CD94 | Manuel | Afficher comme manuel |
| sans code | Derogation SEL BNC | Manuel | Afficher comme manuel |

## Scenarios couverts

### SELARL medecin unipersonnelle simple

Statut : candidat technique avance.

Documents generes :

- `DOC-001`
- `DOC-002`
- `DOC-003`
- `DOC-004`
- `DOC-034`
- `DOC-017`

Limites :

- `DOC-034` reste PARTIAL faute de lock humain specifique ;
- `DOC-017` est LOCKED source-level, pas encore relu par retour humain medecin
  recent equivalent au dentiste.

### SELARL chirurgien-dentiste unipersonnelle simple

Statut : candidat technique avance.

Documents generes :

- `DOC-001`
- `DOC-002`
- `DOC-003`
- `DOC-004`
- `DOC-034`
- `DOC-016`

Limites :

- `DOC-016` est LOCKED sur les articles 1 a 34 ;
- le wrapper post-article reste OPEN GAP de perimetre.

### Regime communautaire

Statut : couvert en V1 bornee.

Effet :

- ajoute `DOC-005` ;
- garde `DOC-006` en reserve, hors generation automatique.

### Multi-associes simple limite a `DOC-004`

Statut : couvert mais limite.

Documents generes :

- `DOC-004` uniquement.

Regles :

- president de seance choisi parmi les associes existants ;
- gerant unique ;
- totalite des parts representee ;
- unanimite totale ;
- blocage si la repartition des parts est incoherente.

### Dentiste multi-associes simple PARTIAL

Statut : partiellement couvert.

Documents generes :

- `DOC-004`
- `DOC-016` en PARTIAL

Limites :

- comparution plurielle non verrouillee ligne par ligne ;
- signature plurielle stricte non verrouillee ;
- plusieurs gerants, president externe, cession, SCM et vote non unanime hors
  scope.

## Scenarios non couverts

Ces scenarios ne doivent pas etre codes sans nouveau gate produit et nouvelle
spec de sous-cas :

- medecin multi-associes ;
- statuts multi-associes complets `DOC-016` / `DOC-017` ;
- plusieurs gerants ;
- president de seance externe aux associes ;
- associe absent non represente, quorum partiel, vote non unanime ;
- cession cabinet medicale ou dentaire ;
- bail / appel de fonds lie au parcours SELARL ;
- cession SCM ;
- derogations ;
- site distinct ;
- `DOC-006` en generation automatique.

## Sources de reprise

A lire pour comprendre la SELARL courante :

1. `docs/project/SELARL_CANONICAL_STATUS_V1.md`
2. `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md`
3. `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md`
4. `docs/project/SELARL_PRODUCTION_FACTORY_V1.md`
5. `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`
6. `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md`
7. `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md`

Rapports de preuve principaux :

- `docs/review/track_b_selarl_dentist_line_by_line_lock_003_report_v1.md`
- `docs/review/track_b_selarl_medecin_line_by_line_lock_004_report_v1.md`
- `docs/review/track_b_selarl_medecin_regime_communautaire_005_report_v1.md`
- `docs/review/track_b_selarl_multi_associes_doc004_limited_007_report_v1.md`
- `docs/review/track_b_selarl_dentist_multi_associes_statuts_partial_008_report_v1.md`

Documents utiles mais historiques :

- `docs/project/SELARL_COMPLETE_CASE_PLAYBOOK_V1.md` reste utile pour la
  methode et la matrice initiale, mais certaines limites de front y sont
  depassees par les tickets Track B posterieurs.
- Les anciennes specs du prototype `src/sydel_doc_engine/app/` restent des
  references de migration, pas le point de depart du clean front Track B.

## Methode reutilisable pour les autres formes

La SELARL sert de methode standard pour les prochains types d'entreprises.
Le protocole transversal a appliquer est :

- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md`

Resume de la methode :

1. etablir la hierarchie des sources ;
2. creer une matrice documents : generable, reserve, manuel, bloque ;
3. figer un contrat metier-front avant code ;
4. definir la saisie par processus metier, pas par generateur ;
5. rendre toutes les reutilisations explicites ;
6. brancher un adaptateur contexte limite ;
7. tester par scenarios et produire DOCX/ZIP ;
8. faire relire humainement avant d'appeler le cas "final" ;
9. ecrire un canonical status equivalent avant de passer au cas suivant.

## Mode d'emploi boucle depuis la SELARL

La SELARL a permis de fixer le mode d'emploi global :

- un sprint couvre un type d'entreprise ;
- le sprint commence toujours en `NO-GO dev` ;
- le sprint doit interroger NotebookLM largement avant code ;
- Naomie doit s'identifier avant de demarrer un sprint et etre guidee etape par
  etape ;
- les documents manuels, reserves, partials et bloques doivent etre visibles
  avant implementation ;
- le test de l'associe est obligatoire avant validation 100 % ;
- les retours humains sont boucles en corrections ou en arbitrages traces ;
- la cloture produit un statut canonique comme le present fichier.

Ce point cloture la SELARL comme modele de methode. Il ne cloture pas encore la
SELARL juridiquement a 100 %, car le pack simple doit encore passer par la revue
associe / juriste.

## Plan de sprint recommande

### Sprint 0 - Clarification projet

Statut : DONE par ce ticket.

Livrable : ce fichier canonique et les pointeurs de reprise.

### Sprint 1 - Revue humaine du pack simple

Objectif : faire relire le pack simple medecin/dentiste et le pack regime
communautaire.

Sorties attendues :

- decision sur `DOC-034` ;
- decision sur le wrapper post-article `DOC-016` ;
- decision sur le niveau de confiance `DOC-017` medecin ;
- liste courte de corrections humaines, sans dev non cadre.

### Sprint 2 - Choix du prochain sous-cas

Objectif : choisir un seul sous-cas a ouvrir.

Candidats :

- cession cabinet medicale/dentaire ;
- cession SCM ;
- statuts multi-associes complets ;
- plusieurs gerants ;
- derogation / site distinct ;
- `DOC-006`.

Sortie attendue : un ticket avec `GO dev` ou `NO-GO dev`.

### Sprint 3 - Implementation bornee

Objectif : coder uniquement le sous-cas choisi, avec tests et smoke.

Regle : ne pas melanger cession, SCM, multi-gerants et derogations dans le meme
ticket.

### Sprint 4 - Generalisation methode

Objectif : appliquer `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` a la
prochaine forme sociale ou famille documentaire.

## Prochaine action recommandee

Lancer `SELARL-CLOSING-PACK-001` selon
`docs/sprints/SPRINT_SELARL_CLOSING_V1.md` : regenerer le pack simple medecin,
dentiste et regime communautaire pour revue associe / juriste avant d'ouvrir un
nouveau developpement complexe.

Si l'utilisateur prefere accelerer le produit plutot que la revue, la prochaine
discussion doit choisir un seul sous-cas et produire un `GO dev` explicite.
