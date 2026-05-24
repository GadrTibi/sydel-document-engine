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

## Ordre recommande maintenant

1. `FRONT-DOSSIER-EDITOR-001`
2. `FRONT-DOCUMENTS-PANEL-001`
3. `FRONT-GENERATION-ACTIONS-001`
4. `FRONT-UNIT-DOCUMENT-UI-001`
5. `FRONT-TEST-TOOLS-CONSOLIDATION-001`
6. `FRONT-PROTOTYPE-DEPRECATION-001`

`SELARL-JURIST-REVIEW-001` reste recommande en parallele comme revue metier/juridique, mais le shell UI peut demarrer sans attendre cette revue tant qu'il ne modifie pas les generateurs ni le wording juridique.

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

Statut : READY.

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
- qualification, personnes, societes, roles et adresses typees sont representes ;
- aucune fusion silencieuse de roles ou d'adresses ;
- les reuse rules sont visibles et explicites ;
- les champs derives restent tracables ;
- les validations `front_data` peuvent etre affichees.

## FRONT-DOCUMENTS-PANEL-001

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

- `FRONT-DOSSIER-EDITOR-001`.

CritÃ¨res d'acceptation :

- afficher documents attendus, generables, manuels, non implementes, contexte incomplet, reserves et blocages ;
- afficher les raisons : roles manquants, adresses manquantes, valeurs canoniques absentes, ambiguities, reserves ;
- distinguer statut document et statut lot ;
- ne jamais presenter un document manuel comme pret a generer ;
- conserver `DOC-006`, `DOC-013` et `DOC-014` dans leur statut produit attendu.

## FRONT-GENERATION-ACTIONS-001

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

- `FRONT-DOCUMENTS-PANEL-001`.

CritÃ¨res d'acceptation :

- seuls les documents `generable` ou explicitement `generable_with_reserve` selon decision UI peuvent etre proposes ;
- les documents manuels restent exclus ;
- DOCX reste prioritaire, PDF local optionnel, ZIP dossier avec manifeste ;
- les erreurs moteur sont affichees sans masquer les raisons data-layer ;
- aucune logique de mapping documentaire n'est dupliquee dans l'UI.

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
- `DOC-006` reste avec reserve ;
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
