# Backlog rebuild front global V1

Tickets sources :

- `GLOBAL-FRONT-ARCHITECTURE-001`
- `FRONT-REVIEW-001`

Statut : socle data termine ; backlog maintenant oriente vers le rebuild UI visible.

## Socle termine

Ces tickets fondent le nouveau front et ne doivent pas etre recodes dans les tickets UI :

1. `FRONT-DATA-LAYER-001` - objets front globaux, valeurs canoniques, reuse rules, diagnostics.
2. `FRONT-ROLE-MODEL-001` - roles fins, portees, ordre, representation, garde-fous.
3. `FRONT-ADDRESS-MODEL-001` - adresses typees, reutilisations explicites, overrides.
4. `FRONT-DOSSIER-FLOW-001` - etapes, blocs, dependances et validations dossier.
5. `FRONT-DOCUMENT-STATUS-LAYER-001` - statuts documents/lots, raisons, reserves, blocages.
6. `FRONT-UNIT-DOCUMENT-MODE-001` - mode document unique data-layer.
7. `FRONT-TEST-PREFILL-001` - scenarios fictifs alignes sur `front_data`.
8. `FRONT-REVIEW-001` - carte de migration, decision prototype, backlog UI visible.
9. `FRONT-UI-SHELL-001` - shell UI visible, nouveau front distinct du prototype.
10. `FRONT-DOSSIER-EDITOR-001` - editeur dossier V1 branche sur `front_data`.
11. `FRONT-DOSSIER-DATA-ENTRY-001` - premiere saisie reelle SELARL simple vers `DossierRecord`.
12. `FRONT-GENERATION-ACTIONS-001` - actions DOCX/ZIP/PDF optionnel sur `DOC-001` a `DOC-004` depuis le nouveau front.
13. `FRONT-UX-CLEANUP-001` - simplification du parcours visible pour test utilisateur reel.
14. `FRONT-UX-HARD-CUT-001` - retrait complet du bruit non-user de la surface principale.
15. `FRONT-STATE-AUDIT-001` - audit de l'etat projet/front apres retour utilisateur.
16. `FRONT-REALITY-CHECK-001` - audit de l'ecart entre debriefs front et code reel visible/branche.
17. `FRONT-MINIMAL-SURFACE-CLEANUP-001` - surface normale minimale type dossier / saisie / generation, debug cache.
18. `SELARL-COMPLETE-CASE-PLAYBOOK-001` - cadrage SELARL complete, matrice documents et recette reproductible.
19. `SELARL-COMPLETE-CONTEXT-ADAPTER-001` - selection/readiness/contexte SELARL complet cote front, sans modification des generateurs.

## Ordre recommande maintenant

1. `SELARL-COMPLETE-COMPLEX-SUBFORMS-001` : completer les sous-formulaires et l'adaptateur contexte pour cession medicale/dentaire, bail/appel de fonds et cession SCM.
2. `SELARL-COMPLETE-SMOKE-001` : generer les packs DOCX/ZIP des scenarios SELARL complets.
3. `SELARL-COMPLETE-JURIST-REVIEW-001` : revue humaine avant toute promesse de final juridique.
4. `REPLICATION-NEXT-CASE-001` : appliquer la recette SELARL au cas suivant.
5. `FRONT-UNIT-DOCUMENT-UI-001`
6. `FRONT-TEST-TOOLS-CONSOLIDATION-001`
7. `FRONT-PROTOTYPE-DEPRECATION-001`

`SELARL-JURIST-REVIEW-001` reste conserve comme jalon historique du pilote, mais la demande utilisateur courante de SELARL complete remplace la prochaine action par `SELARL-COMPLETE-COMPLEX-SUBFORMS-001`.

## Garde-fous communs

Pour tous les tickets UI visibles :

- ne pas modifier les generateurs ;
- ne pas modifier le moteur DOCX/PDF/ZIP ;
- ne pas modifier le wording juridique ;
- ne pas supprimer le prototype tant que `FRONT-PROTOTYPE-DEPRECATION-001` n'est pas execute ;
- ne pas utiliser le prototype comme source de verite metier ;
- consommer `front_data` comme source produit/data cible ;
- conserver les documents manuels visibles mais hors generation automatique ;
- distinguer dossier complet, document unitaire et diagnostic technique.

## FRONT-UI-SHELL-001

Statut : DONE.

Objectif : creer la premiere tranche visible du nouveau front global en isolant clairement le prototype actuel.

Fichiers concernes :

- `src/sydel_doc_engine/app/streamlit_app.py` ou nouveau module shell app dedie ;
- eventuels composants UI sous `src/sydel_doc_engine/app/` ;
- tests UI/AppTest si structure modifiee ;
- documentation de revue si necessaire.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- logique de generation des documents ;
- wording juridique ;
- suppression du prototype.

Dependances :

- `FRONT-REVIEW-001` DONE ;
- `front_data/dossier_flow.py` ;
- `front_data/document_status.py`.

CritÃ¨res d'acceptation :

- le nouveau front global est visible comme entree distincte ;
- le prototype actuel reste accessible et explicitement marque comme prototype / diagnostic ;
- `Technique / diagnostic` reste accessible ;
- `Document unitaire` reste separe du parcours dossier complet ;
- un squelette read-only du flow dossier global peut etre affiche sans coder l'editeur complet ;
- aucun document n'est genere automatiquement par le nouveau shell seul ;
- tests ou smoke UI adaptes au changement.

## FRONT-DOSSIER-EDITOR-001

Statut : DONE.

Objectif : implementer un premier editeur dossier data-first, sans chercher la couverture exhaustive.

Fichiers concernes :

- composants UI du nouveau front ;
- `src/sydel_doc_engine/front_data/models.py` en lecture ;
- `role_model.py`, `address_model.py`, `dossier_flow.py`, `canonical_mapping.py`, `validation.py` en lecture ;
- tests d'assemblage `DossierRecord` depuis l'UI.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- `business_wizard.py` sauf adaptateur explicitement justifie ;
- prototype historique hors branchement shell.

Dependances :

- `FRONT-UI-SHELL-001`.

CritÃ¨res d'acceptation :

- l'UI sait construire un `DossierRecord` minimal ;
- les etapes, blocs actifs, exigences et statuts documentaires sont visibles ;
- aucune fusion silencieuse de roles ou d'adresses n'est introduite ;
- les documents attendus affichent roles, adresses, champs canoniques et blocages ;
- les statuts de lot `ready`, `partial` et `blocked` sont prepares ;
- les validations `front_data` peuvent etre affichees sans logique metier dans Streamlit.

## FRONT-DOSSIER-DATA-ENTRY-001

Statut : DONE.

Objectif : ajouter une premiere tranche de saisie reelle dans le nouvel editeur dossier sans reconstruire le wizard historique.

Fichiers concernes :

- `src/sydel_doc_engine/app/front_dossier_entry.py` ;
- `src/sydel_doc_engine/app/front_dossier_editor.py` en lecture ;
- `src/sydel_doc_engine/app/streamlit_app.py` pour le rendu des champs ;
- `src/sydel_doc_engine/front_data/*` en consommation ;
- tests AppTest et unitaires.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- wording juridique ;
- modes prototype hors isolement existant ;
- logique historique `business_wizard.py`.

Dependances :

- `FRONT-DOSSIER-EDITOR-001`.

Criteres d'acceptation :

- le profil `SELARL creation simple` alimente un vrai `DossierRecord` ;
- la personne principale, la societe principale, les adresses typees, les roles et les valeurs canoniques sont crees depuis la saisie ;
- `Dossier unipersonnel` cree des `RoleAssignment` explicites sans fusion silencieuse ;
- `domiciliation = siege_social` passe par une `ReuseRuleState` explicite ;
- les statuts DOC-001 a DOC-004 se recalculent depuis les donnees saisies ;
- les cas ordre, cession, SCM, SPFPL restent read-only/orange pour les tickets suivants.

## FRONT-DOCUMENTS-PANEL-001

Statut : BLOCKED.

Objectif : construire le panneau Documents attendus du nouveau front a partir de la couche de statuts.

Fichiers concernes :

- composants UI du nouveau front ;
- `src/sydel_doc_engine/front_data/document_status.py` ;
- `src/sydel_doc_engine/front_data/dossier_flow.py` ;
- `src/sydel_doc_engine/front_data/validation.py` ;
- tests de rendu / table de statuts.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- selection documentaire moteur hors lecture ;
- wording juridique.

Dependances :

- `FRONT-MINIMAL-SURFACE-CLEANUP-001` DONE.
- Decision post-test utilisateur confirmant qu'un panneau visible ne pollue pas la surface principale.

CritÃ¨res d'acceptation :

- afficher documents attendus, generables, manuels, non implementes, contexte incomplet, reserves et blocages ;
- afficher les raisons : roles manquants, adresses manquantes, valeurs canoniques absentes, ambiguities, reserves ;
- distinguer statut document et statut lot ;
- ne jamais presenter un document manuel comme pret a generer ;
- conserver `DOC-006`, `DOC-013` et `DOC-014` dans leur statut produit attendu.

## FRONT-MINIMAL-SURFACE-CLEANUP-001

Statut : DONE.

Objectif : appliquer la surface utilisateur minimale definie dans
`docs/project/FRONT_MINIMAL_USER_SURFACE_V1.md`, avant tout push, redeploiement
ou test utilisateur.

Fichiers concernes :

- `src/sydel_doc_engine/app/streamlit_app.py` ;
- `src/sydel_doc_engine/app/front_generation_actions.py` en lecture ou extension limitee ;
- tests AppTest du nouveau front ;
- docs de pilotage si necessaire.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- wording juridique ;
- source de verite ;
- extension du perimetre documentaire.

Dependances :

- `FRONT-REALITY-CHECK-001`.

Criteres d'acceptation :

- la vue normale affiche seulement `Type de dossier`, `Donnees a saisir` et `Generation` ;
- aucun outil interne n'est visible en session utilisateur normale ;
- aucune table, aucun radio, aucun panneau documents et aucun diagnostic visible ;
- les aides de format restent pres des champs concernes ;
- les blocages runtime utiles sont visibles dans `Generation` ;
- le PDF est cache si le backend local est indisponible ;
- le perimetre `DOC-001` a `DOC-004` reste explicite sans liste/table detaillee ;
- AppTest couvre la surface normale minimale.

Livraison :

- suppression des expanders ouverts de la surface normale ;
- masquage des outils internes derriere `SYDEL_ENABLE_INTERNAL_TOOLS=1` ou flag de session interne ;
- masquage du bouton PDF quand le backend local est indisponible ;
- affichage de blocages courts dans `Generation` ;
- validation `ruff check .` et `pytest` OK, 382 tests passes ;
- rapport : `docs/review/front_minimal_surface_cleanup_001_report_v1.md`.

## FRONT-GENERATION-READINESS-UX-001

Statut : BLOCKED.

Objectif : expliquer les blocages de generation dans la surface normale du
nouveau front avant d'etendre le perimetre documentaire.

Fichiers concernes :

- `src/sydel_doc_engine/app/streamlit_app.py` ;
- `src/sydel_doc_engine/app/front_generation_actions.py` en lecture ou extension limitee ;
- `src/sydel_doc_engine/front_data/document_status.py` en lecture ;
- tests AppTest du nouveau front.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- wording juridique ;
- source de verite ;
- prototype historique hors affichage d'outils internes.

Dependances :

- `FRONT-MINIMAL-SURFACE-CLEANUP-001`.
- Reassessment post-test utilisateur.

Criteres d'acceptation :

- ne lancer ce ticket separement que si le cleanup minimal ne suffit pas ;
- privilegier l'absorption des raisons de blocage dans `FRONT-MINIMAL-SURFACE-CLEANUP-001`.

## FRONT-GENERATION-ACTIONS-001

Statut : DONE.

Objectif : brancher les actions de generation du nouveau front uniquement sur les documents prets, sans modifier le moteur.

Fichiers concernes :

- composants UI de generation ;
- `src/sydel_doc_engine/app/ui_runtime.py` ou adaptateur equivalent ;
- adaptateur futur `DossierRecord` -> contexte moteur si cree dans un ticket dedie ;
- tests de generation ciblee si code modifie.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- wording juridique ;
- documents non generables ou manuels.

Dependances :

- `FRONT-DOSSIER-DATA-ENTRY-001`.
- Depuis `FRONT-REALITY-CHECK-001`, ne pas ajouter `FRONT-DOCUMENTS-PANEL-001` en surface visible avant `FRONT-MINIMAL-SURFACE-CLEANUP-001`.

CritÃ¨res d'acceptation :

- seuls les documents `generable` dans le perimetre V1 peuvent etre proposes ;
- les documents manuels restent exclus ;
- `DOC-006` est inclus quand le regime communautaire SELARL est actif ;
  `DOC-013` et `DOC-014` restent exclus de la generation V1 ;
- DOCX reste prioritaire, PDF local optionnel, ZIP dossier avec manifeste ;
- les erreurs moteur sont affichees sans masquer les raisons data-layer ;
- aucune logique de mapping documentaire n'est dupliquee dans l'UI.

## FRONT-UX-CLEANUP-001

Statut : DONE.

Objectif : simplifier la vue visible du nouveau front pour permettre un vrai test
local sans bruit d'architecture.

Fichiers concernes :

- `src/sydel_doc_engine/app/streamlit_app.py` ;
- tests AppTest du shell, de l'editeur dossier, de la saisie et de la generation ;
- rapport de revue UX.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- fondations `front_data` ;
- wording juridique ;
- suppression des outils de test.

Dependances :

- `FRONT-GENERATION-ACTIONS-001`.

Criteres d'acceptation :

- la vue principale expose type de dossier, saisie, resume documents et actions de generation ;
- les tableaux complets de flow, blocs, exigences, statuts et lots sont replies en diagnostic ;
- les outils de test restent accessibles mais secondaires ;
- le parcours `SELARL creation simple` et `DOC-001` a `DOC-004` reste fonctionnel ;
- ruff et pytest restent verts.

## FRONT-UX-HARD-CUT-001

Statut : DONE.

Objectif : retirer tout le bruit non-user de la vue principale normale.

Fichiers concernes :

- `src/sydel_doc_engine/app/streamlit_app.py` ;
- tests AppTest du shell, de la saisie, de la generation, du prototype interne et du document unitaire ;
- rapport de revue UX hard cut.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- fondations `front_data` ;
- wording juridique ;
- suppression des outils de test.

Dependances :

- `FRONT-UX-CLEANUP-001`.

Criteres d'acceptation :

- la vue principale normale n'affiche aucun radio de navigation ;
- aucun tableau de diagnostic n'est rendu par defaut ;
- la surface principale contient seulement type de dossier, champs de saisie et generation ;
- les outils historiques sont accessibles via `Outils internes` en sidebar ;
- le debug est disponible uniquement via `Debug interne` ;
- le parcours `SELARL creation simple` et `DOC-001` a `DOC-004` reste fonctionnel.

## FRONT-UNIT-DOCUMENT-UI-001

Objectif : consolider le mode Document unitaire visible autour de `front_data/unit_document_mode.py`.

Fichiers concernes :

- `src/sydel_doc_engine/app/single_document_mode.py` ;
- composants UI du mode document unitaire ;
- `src/sydel_doc_engine/front_data/unit_document_mode.py` en lecture ou extension limitee ;
- tests du mode document unique.

Ne pas toucher :

- parcours dossier complet ;
- generateurs ;
- moteur DOCX/PDF/ZIP ;
- prefills Assistant metier sauf reuse de test explicite.

Dependances :

- `FRONT-UI-SHELL-001`;
- `FRONT-GENERATION-ACTIONS-001` si les actions sont mutualisees.

CritÃ¨res d'acceptation :

- selection par `DOC-XXX` ou libelle ;
- exigences data-layer visibles ;
- documents hors perimetre V1 signales proprement ;
- `DOC-006` est genere uniquement si le regime communautaire SELARL est actif ;
- `DOC-013` et `DOC-014` restent manuels ;
- aucune confusion avec le parcours dossier complet.

## FRONT-TEST-TOOLS-CONSOLIDATION-001

Objectif : regrouper proprement les outils de test, prefill et diagnostic pour eviter qu'ils ressemblent au parcours produit.

Fichiers concernes :

- shell UI ;
- `app/test_prefill_presets.py` ;
- `front_data/test_prefill_presets.py` ;
- tests AppTest / unitaires lies aux scenarios.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- donnees reelles ;
- wording juridique.

Dependances :

- `FRONT-UI-SHELL-001`;
- `FRONT-DOSSIER-EDITOR-001` si les prefills alimentent le nouvel editeur.

CritÃ¨res d'acceptation :

- les donnees fictives sont marquees comme telles ;
- les scenarios SELARL simple, SELARL regime/site, SELARL cession/bail/financement et SCI restent disponibles ;
- reset propre des etats de test ;
- le mode `Technique / diagnostic` reste separe ;
- les prefills peuvent alimenter un `DossierRecord` sans passer par les widgets historiques.

## FRONT-PROTOTYPE-DEPRECATION-001

Objectif : deprecier progressivement le prototype historique quand les parcours cibles couvrent les memes usages.

Fichiers concernes :

- shell UI ;
- docs de migration ;
- tests de non-regression sur modes conserves ;
- eventuellement suppression differee de composants obsoletes, seulement apres decision explicite.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- wording juridique ;
- outils de diagnostic encore utiles sans remplacement.

Dependances :

- `FRONT-DOSSIER-EDITOR-001`;
- `FRONT-DOCUMENTS-PANEL-001`;
- `FRONT-GENERATION-ACTIONS-001`;
- `FRONT-TEST-TOOLS-CONSOLIDATION-001`.

CritÃ¨res d'acceptation :

- le prototype est marque comme obsolete ou archive dans l'UI ;
- aucun usage de diagnostic encore utile n'est perdu ;
- les tests prouvent que les parcours cibles remplacent les usages principaux ;
- la suppression de code, si elle est proposee, est explicite et reversible par ticket separe.

## Tickets futurs possibles

Ces sujets restent hors rebuild UI V1 sauf decision explicite :

- mode Projet / filigrane ;
- SELAS medecin avec micro-holding ;
- calculs avances droits financiers / droits de vote ;
- API Pappers ;
- portail client ;
- pieces justificatives bloquantes pour l'ordre ;
- parametrage cabinet pour banque, fiscalite et signature electronique ;
- remplacement complet de Streamlit par un autre framework.
