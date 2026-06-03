# Rapport SELARL-COMPLETE-CONTEXT-ADAPTER-001

Date : 2026-05-25

## Verdict

Le nouveau front global a ete mis a jour : il n'est plus limite au test
`DOC-001` a `DOC-004` pour la SELARL.

Le parcours visible reste volontairement minimal :

- `Type de dossier` ;
- `Donnees a saisir` ;
- `Generation`.

Aucun generateur, moteur DOCX/PDF/ZIP, source de verite ou wording juridique
n'a ete modifie.

## Etat reel visible

La surface principale conserve une seule entree utilisateur : le dossier
SELARL. Les sous-zones visibles dans `Donnees a saisir` couvrent maintenant :

- qualification du dossier : profession medecin ou chirurgien-dentiste,
  regime communautaire, cession de cabinet, cession SCM, site distinct,
  derogation ;
- praticien / associe / gerant / signataire ;
- societe, siege, domiciliation et capital ;
- ordre professionnel et mandataire ;
- statuts SEL, depot des fonds, exercice social et seuils de gerance ;
- conjoint et donnees de regime communautaire quand l'option est cochee.

La vue normale ne remet pas en surface les anciens diagnostics, tableaux ou
outils internes. Les documents manuels ou reserves restent traites dans la
readiness, pas comme des boutons de generation.

## Etat reel des generations

### Cas simple medecin

Un dossier SELARL medecin complet peut generer depuis le nouveau front :

- `DOC-001` declaration de non-condamnation ;
- `DOC-002` autorisation de domiciliation ;
- `DOC-003` procuration ;
- `DOC-004` PV nomination gerant ;
- `DOC-034` demande d'inscription a l'ordre ;
- `DOC-017` statuts SELARL medecin.

Le ZIP est branche apres generation DOCX. Le PDF reste le backend optionnel
existant : ce ticket ne le modifie pas.

### Cas simple chirurgien-dentiste

Le choix de profession bascule la cible statuts de `DOC-017` vers `DOC-016`.
La readiness et le contexte moteur utilisent l'overlay `selarl_dentiste`.

### Regime communautaire

Quand le regime communautaire est coche :

- `DOC-005` entre dans les documents cibles generables ;
- `DOC-006` reste visible avec reserve, mais exclu de la generation
  automatique.

### Derogations et documents manuels

Les documents suivants restent hors generation automatique SELARL :

- `DOC-013` ;
- `DOC-014` ;
- derogation SEL BNC sans code moteur.

Ils sont visibles comme manuels/exclus, pas comme documents prets a generer.

### Cession et SCM

La selection documentaire conditionnelle est branchee pour :

- cession medicale : `DOC-007`, `DOC-008`, `DOC-009`, `DOC-010` ;
- cession dentaire : `DOC-007`, `DOC-008`, `DOC-011`, `DOC-012` ;
- cession SCM : `DOC-031`, `DOC-032`, `DOC-033`.

Ces sous-scenarios restent volontairement en `context_incomplete` tant que les
sous-formulaires metier detailles ne sont pas branches. Le front ne pretend
donc pas encore generer un pack cession/SCM final.

## Garde-fous ajoutes

- selection documentaire par le catalogue metier SELARL ;
- requirements/readiness SELARL centralises dans
  `src/sydel_doc_engine/app/front_selarl_complete.py` ;
- documents reserves et manuels exclus de `generate_front_docx(...)` ;
- contexte moteur enrichi pour ordre, mandataire, statuts SEL, depot des fonds,
  regime communautaire et valeurs de signature ;
- tests unitaires pour medecin, dentiste, regime communautaire, derogation
  manuelle, cession medicale, cession dentaire et cession SCM.

## Validation

- `python -m ruff check .` : OK.
- `python -m pytest tests\unit\test_front_generation_actions.py tests\unit\test_front_dossier_data_entry.py -q` :
  OK, 23 tests passes.
- Smoke technique DOCX : generation dentiste OK avec
  `statuts_selarl_chirurgien_dentiste.docx` ; generation regime communautaire
  OK avec `lettre_renonciation_associe.docx`.

Observation locale : Python/pytest emet encore des warnings de cache/temp
Windows `PermissionError` apres la fin des tests Streamlit, mais le run cible
retourne bien un code 0.

`python -m pytest -q` a aussi ete tente. Le run complet reste non conclusif
sur cette machine : pytest echoue en setup/cleanup `tmp_path` avec des
`PermissionError` Windows sur les dossiers temporaires, avant de pouvoir donner
un verdict fonctionnel utile sur l'ensemble de la suite.

## Prochain ticket unique recommande

`SELARL-COMPLETE-COMPLEX-SUBFORMS-001`

Objectif : brancher les sous-formulaires et l'adaptateur contexte pour les
scenarios cession medicale/dentaire, bail/appel de fonds et cession SCM, sans
modifier les generateurs ni le moteur DOCX/PDF/ZIP.

Ce ticket doit convertir les documents actuellement `context_incomplete` en
documents generables uniquement quand les donnees metier completes sont saisies.
