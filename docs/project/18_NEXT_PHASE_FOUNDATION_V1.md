# Plan de fondation post-moteur V1

Ticket : `NEXT-PHASE-FOUNDATION-001`

Reconciliation : `RECONCILE-MOTOR-CLOSE-001`

Date : 2026-05-15

## Objet

Ce document prepare le plan d'execution concret de la phase post-moteur, apres cloture du moteur documentaire DOCX V1.

Il couvre quatre sous-chantiers :

- UI ;
- PDF ;
- ZIP ;
- recette finale.

Il ne modifie pas le pilotage projet, ne vaut pas validation metier ou juridique, et ne demande aucune modification de code Python dans ce ticket.

## Point de depart retenu

Le point de depart est la conclusion consolidee de
`docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md` et
`docs/project/17_FINAL_ENGINE_QUALITY_AUDIT_V1.md` : le moteur documentaire
DOCX V1 est feature complete et clos pour la generation DOCX deterministe du
perimetre valide.

Cette conclusion couvre :

- le moteur Python ;
- le catalogue ;
- l'orchestrateur ;
- les generateurs DOCX `DOC-001` a `DOC-043` ;
- les tests unitaires associes.

Elle ne couvre pas encore :

- UI Streamlit ;
- generation PDF ;
- constitution ZIP dossier ;
- recette finale metier ;
- revue humaine juridique et visuelle des rendus.

La phase suivante ne doit pas rouvrir le codage documentaire sans ticket dedie.

## References de cadrage

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/project/15_REMAINING_SCOPE_AUDIT_V1.md`
- `docs/project/16_MOTOR_COMPLETION_AUDIT_V1.md`
- `docs/delivery/render_style_system_v1.md`
- `docs/delivery/render_style_blueprint_batch_v1.md`
- `docs/delivery/render_style_blueprint_lot03_batch_v1.md`
- `docs/review/lot_02_pv_nomination_gerant_review_v1.md`
- `docs/review/lot_02_orchestrator_smoke_review_v1.md`

## Principes transverses

- La phase post-moteur consomme le moteur existant ; elle ne doit pas reouvrir le codage documentaire sans ticket dedie.
- L'UI ne doit pas contenir de logique metier cachee : elle collecte un contexte dossier et appelle l'orchestrateur.
- La conversion PDF doit partir des DOCX generes, sans modifier le contenu juridique.
- Le ZIP dossier doit emballer des sorties deja produites et tracer ce qui a ete inclus.
- La recette finale doit separer validation technique, validation visuelle et validation juridique.

## 1. Sous-chantier UI

### Objectif

Livrer une interface Streamlit V0 permettant de piloter une generation dossier depuis un contexte saisi ou charge, en s'appuyant sur le catalogue et l'orchestrateur existants.

La V0 doit rester utilitaire :

- choix du type de dossier / structure ;
- saisie ou chargement du contexte canonique ;
- affichage des documents selectionnes ;
- generation DOCX ;
- affichage des erreurs de validation ;
- acces aux fichiers produits.

### Dependances

- Moteur DOCX V1 considere complet.
- Catalogue moteur couvrant `DOC-001` a `DOC-043`.
- Orchestrateur `select_documents_for_context` et `generate_documents`.
- Dictionnaire canonique des variables.
- Table de mapping documents -> variables.
- Contextes exemples deja disponibles dans `examples/contexts/`.
- Arbitrage de niveau UI sur les champs obligatoires, champs conditionnels et champs manuels.

### Tickets probables

- `UI-SPEC-001` : spec ecran V0, parcours utilisateur, donnees minimales et erreurs attendues.
- `UI-CONTEXT-LOAD-001` : chargement / edition d'un contexte YAML ou JSON existant.
- `UI-FORM-V0-001` : formulaire Streamlit minimal branche sur les variables canoniques prioritaires.
- `UI-SELECTION-PREVIEW-001` : previsualisation de la liste des documents selectionnes avant generation.
- `UI-GENERATE-DOCX-001` : bouton de generation DOCX et affichage des chemins de sortie.
- `UI-ERRORS-001` : rendu lisible des erreurs bloquantes de validation.
- `UI-SMOKE-001` : smoke manuel documente sur au moins un dossier complet.

### Ordre conseille

1. Spec UI V0, sans code, pour figer ce que l'interface doit faire et ne pas faire.
2. Ecran de chargement d'un contexte exemple existant.
3. Generation DOCX depuis l'UI en lecture du contexte charge.
4. Previsualisation de la selection documentaire.
5. Formulaire minimal pour les variables prioritaires.
6. Gestion propre des erreurs et messages de blocage.
7. Smoke UI sur dossier complet, puis preparation de la connexion PDF / ZIP.

### Risques

- Reintroduire de la logique metier dans l'UI au lieu d'appeler l'orchestrateur.
- Surcharger la V0 avec un formulaire exhaustif avant stabilisation des parcours.
- Confondre champ manuel, champ obligatoire et champ conditionnel.
- Masquer des erreurs de validation moteur sous des messages UI trop generiques.
- Laisser croire que la revue UI vaut validation juridique.

## 2. Sous-chantier PDF

### Objectif

Ajouter une conversion PDF deterministe a partir des DOCX generes, sans modifier le wording ni les regles documentaires.

La cible V1 doit permettre :

- produire un PDF pour chaque DOCX final ;
- signaler clairement les echecs de conversion ;
- conserver une correspondance DOCX -> PDF tracable ;
- permettre une revue visuelle humaine sur les PDF.

### Dependances

- DOCX generes sans placeholder residuel.
- Rendu DOCX suffisamment stable pour les documents inclus dans la recette.
- Choix technique explicite du moteur de conversion : LibreOffice headless, Microsoft Word local, ou autre outil autorise.
- Conventions de nommage des fichiers de sortie.
- Dossier de sortie stable par generation.

### Tickets probables

- `PDF-SPIKE-001` : etude courte du convertisseur disponible et de ses contraintes Windows / CI.
- `PDF-CONVERTER-001` : wrapper technique de conversion DOCX -> PDF.
- `PDF-CONTRACT-001` : contrat d'erreur et resultat de conversion.
- `PDF-BATCH-001` : conversion de tous les DOCX d'un dossier de generation.
- `PDF-SMOKE-001` : smoke reel sur un dossier exemple complet.
- `PDF-VISUAL-REVIEW-001` : checklist de revue visuelle PDF.

### Ordre conseille

1. Spike technique de conversion sur un DOCX simple.
2. Decision de l'outil de conversion et documentation des pre-requis locaux.
3. Wrapper unitaire DOCX -> PDF.
4. Conversion batch d'un repertoire de sortie DOCX.
5. Tests ciblant les echecs previsibles : fichier absent, sortie deja presente, convertisseur indisponible.
6. Smoke PDF sur un dossier representatif.
7. Revue humaine des PDF produits.

### Risques

- Dependances systeme non disponibles sur toutes les machines.
- Differences de rendu PDF selon outil de conversion ou polices installees.
- Fichiers DOCX verrouilles par Word pendant la conversion.
- Confusion entre succes technique de conversion et validation visuelle / juridique.
- Tentation de corriger le rendu en modifiant le contenu juridique au lieu de corriger la couche de style.

## 3. Sous-chantier ZIP

### Objectif

Produire une archive ZIP dossier contenant les sorties finales attendues, avec une structure stable et lisible.

La cible V1 doit permettre :

- inclure les DOCX generes ;
- inclure les PDF lorsque le sous-chantier PDF est pret ;
- optionnellement inclure un manifeste technique ;
- exclure les fichiers temporaires et artefacts hors dossier ;
- garantir un nommage reproductible.

### Dependances

- Generation DOCX stable.
- Conversion PDF stable si les PDF sont inclus.
- Regles de nommage des documents et du dossier.
- Decision sur le contenu du manifeste ZIP.
- Dossier de sortie unique par generation.

### Tickets probables

- `ZIP-SPEC-001` : spec de contenu, arborescence et nommage ZIP.
- `ZIP-MANIFEST-001` : format du manifeste technique de generation.
- `ZIP-BUILDER-001` : creation de l'archive depuis un dossier de sortie.
- `ZIP-DOCX-ONLY-001` : premier ZIP avec DOCX uniquement si PDF non pret.
- `ZIP-PDF-001` : inclusion des PDF apres stabilisation du convertisseur.
- `ZIP-SMOKE-001` : smoke ZIP complet et controle du contenu.

### Ordre conseille

1. Spec de l'arborescence ZIP et des fichiers inclus.
2. Definition du manifeste minimal : date, structure, documents produits, formats presents, erreurs eventuelles.
3. Builder ZIP sur dossier DOCX existant.
4. Controle automatique du contenu de l'archive.
5. Inclusion PDF quand la conversion est stable.
6. Smoke ZIP complet sur un dossier representatif.
7. Validation de l'archive par ouverture manuelle et controle des fichiers attendus.

### Risques

- Archiver des artefacts temporaires ou des fichiers de travail.
- Produire un ZIP non reproductible a cause d'un nommage instable.
- Inclure des PDF manquants sans signaler l'echec de conversion.
- Masquer les documents a completer manuellement dans un paquet qui semble final.
- Oublier la tracabilite entre contexte d'entree, documents selectionnes et fichiers produits.

## 4. Sous-chantier recette finale

### Objectif

Organiser une recette finale permettant de qualifier le flux complet dossier :

`contexte dossier -> selection documentaire -> DOCX -> PDF -> ZIP -> revue humaine`

La recette doit confirmer le fonctionnement technique et preparer la validation humaine, sans se substituer a la validation juridique.

### Dependances

- UI V0 utilisable ou, au minimum, commande de generation dossier stabilisee.
- DOCX V1 produits par l'orchestrateur.
- PDF disponible pour les documents inclus dans la recette.
- ZIP dossier disponible.
- Jeux de contextes representatifs.
- Checklists de revue humaine pour les documents sensibles.
- Liste explicite des exclusions V1 et documents manuels.

### Tickets probables

- `RECETTE-MATRIX-001` : matrice des cas de recette par structure et options.
- `RECETTE-CONTEXTS-001` : constitution des contextes exemples de recette finale.
- `RECETTE-DOCX-001` : generation et controle des DOCX.
- `RECETTE-PDF-001` : generation et controle des PDF.
- `RECETTE-ZIP-001` : generation et controle du ZIP dossier.
- `RECETTE-HUMAN-REVIEW-001` : checklist de revue humaine visuelle et juridique.
- `RECETTE-REPORT-001` : rapport final listant validations, exclusions, risques et suites.

### Ordre conseille

1. Definir la matrice de cas minimale : au moins un dossier simple et des dossiers couvrant les options majeures.
2. Figer les contextes de recette, sans inventer de wording juridique.
3. Executer la generation DOCX et verifier l'absence de placeholders residuels.
4. Convertir en PDF et controler les echecs techniques.
5. Construire le ZIP et verifier son contenu.
6. Faire la revue humaine visuelle et juridique sur les rendus.
7. Produire un rapport de recette avec decision : valide, valide avec reserves, ou bloque.

### Risques

- Confondre tests automatises et validation juridique.
- Choisir une matrice de recette trop pauvre pour les options majeures.
- Ne pas tracer les exclusions V1 et les documents a remplir a la main.
- Decouvrir tardivement des ecarts de rendu deja identifies dans les blueprints de style.
- Laisser des exemples de contexte non realistes piloter une validation finale.

## Ordre global recommande

1. `UI-SPEC-001`
2. `PDF-SPIKE-001`
3. `ZIP-SPEC-001`
4. `UI-GENERATE-DOCX-001`
5. `PDF-CONVERTER-001`
6. `ZIP-BUILDER-001`
7. `RECETTE-MATRIX-001`
8. `RECETTE-CONTEXTS-001`
9. `RECETTE-DOCX-001`
10. `RECETTE-PDF-001`
11. `RECETTE-ZIP-001`
12. `RECETTE-HUMAN-REVIEW-001`
13. `RECETTE-REPORT-001`

## Prochaine etape recommandee

Lancer `UI-SPEC-001` en premier, tout en ouvrant `PDF-SPIKE-001` comme ticket technique parallele si le convertisseur PDF disponible doit etre arbitre rapidement.
