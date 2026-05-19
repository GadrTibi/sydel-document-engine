# Backlog de reconstruction controlee SELARL V2

Tickets source : `SELARL-NOTEBOOKLM-RECONCILIATION-001`, corrige par `SELARL-PLAN-CORRECTION-001`.

## Principes

- Les arbitrages explicites de l'associe priment sur NotebookLM.
- Ne pas toucher aux generateurs avant realignement produit.
- Ne pas modifier le moteur DOCX/PDF/ZIP.
- Ne pas generaliser aux autres cas.
- Ne pas changer de wording juridique dans les actes.
- Corriger d'abord le schema et les tests, puis l'UI.
- Garder le mode `Technique / diagnostic` et le parcours SCI existants.
- Ne pas pousser ni redeployer l'UI SELARL actuelle tant que le realignement produit n'est pas termine.

## Ordre recommande

1. `SELARL-WORDING-REALIGN-001`
2. `SELARL-FLOW-REALIGN-001`
3. `SELARL-REUSE-RULES-REALIGN-001`
4. `SELARL-UI-REALIGN-001`
5. `SELARL-SMOKE-REALISTIC-001`
6. `SELARL-JURIST-REVIEW-001`

## SELARL-WORDING-REALIGN-001

Objectif : realigner les libelles SELARL visibles sur les arbitrages associe et NotebookLM.

Fichiers concernes :

- `docs/project/SELARL_FORM_SCHEMA_V1.md` ou nouvelle version V2 ;
- `docs/project/SELARL_UI_WIZARD_SPEC_V1.md` ou nouvelle version V2 ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `tests/unit/test_selarl_form_schema.py` ;
- `tests/unit/test_business_wizard.py`.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- `streamlit_app.py` sauf si le ticket est explicitement elargi ;
- autres cas que SELARL.

Tests attendus :

- test absence du libelle banni dans les labels SELARL visibles ;
- test presence de `Praticien`, `Fiche Client`, `Gerant`, `Associe`, `Signataire`, `Mandataire` selon contexte ;
- test absence de la transcription erronée de SELARL hors source NotebookLM.

Criteres d'acceptation :

- l'ecran personne cible est `Fiche Client` ;
- le terme pivot visible est `Praticien` ;
- les roles juridiques exacts sont utilises quand ils existent ;
- les labels techniques internes peuvent rester stables si non visibles ;
- aucune modification juridique documentaire.

## SELARL-FLOW-REALIGN-001

Objectif : realigner l'ordre conceptuel du formulaire SELARL.

Fichiers concernes :

- `docs/project/SELARL_UI_WIZARD_SPEC_V2.md` ;
- `docs/project/SELARL_FORM_SCHEMA_V2.md` ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- tests unitaires du schema et du wizard.

Ne pas toucher :

- rendu Streamlit visible si non necessaire ;
- generateurs ;
- moteur DOCX/PDF/ZIP ;
- cas SCI, SELAS, SPFPL, SCM, SAS.

Tests attendus :

- ordre des blocs : qualification, Fiche Client / Praticien, Fiche Societe, Capital & Associes, scenarios, documents ;
- presence du type d'operation si utile au parcours SELARL ;
- conservation des documents attendus.

Criteres d'acceptation :

- le schema machine-readable exprime l'ordre cible ;
- les blocs inactifs restent non bloquants ;
- la societe ne precede plus la Fiche Client dans le cadrage SELARL.

## SELARL-REUSE-RULES-REALIGN-001

Objectif : corriger les regles de reutilisation SELARL autour de `Dossier unipersonnel`.

Fichiers concernes :

- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- `tests/unit/test_selarl_form_schema.py` ;
- `tests/unit/test_business_wizard.py` ;
- specs SELARL V2.

Ne pas toucher :

- generateurs ;
- templates ;
- moteur ;
- code des autres cas.

Tests attendus :

- dossier unipersonnel : Praticien = associe unique = gerant = signataire si option active ;
- mandataire distinct du signataire par defaut ;
- SELARL reutilisable comme acquereur / cessionnaire seulement via option ;
- vendeur = locataire actuel seulement via option ;
- siege = lieu d'exercice / cabinet seulement via option.

Criteres d'acceptation :

- la case ou logique `Dossier unipersonnel` est lisible et testee ;
- aucune derivation sensible n'est automatique sans confirmation ;
- les champs derives sont identifiables et verrouillables ;
- le mandataire reste hors priorite UX s'il n'est pas requis par les variables ou documents.

## SELARL-UI-REALIGN-001

Objectif : realigner le parcours Streamlit SELARL apres realignement du schema.

Fichiers concernes :

- `src/sydel_doc_engine/app/streamlit_app.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` si projections UI necessaires ;
- `tests/unit/test_business_wizard.py` ;
- rapport de revue UI.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- mode `Technique / diagnostic` ;
- parcours SCI ;
- autres cas metier.

Tests attendus :

- tests unitaires de parcours SELARL ;
- tests source-level anti-regression sur libelles ;
- controle que les documents manuels ne partent pas en generation ;
- controle que l'UI SELARL existante n'est pas presentee comme validee produit avant realignement.

Criteres d'acceptation :

- parcours visible : qualification, Fiche Client, Fiche Societe, Capital & Associes, scenarios, documents/generation ;
- labels alignes sur `Praticien` et les roles juridiques exacts ;
- logique `Dossier unipersonnel` exposee si elle est portee par le schema ;
- aucun mode Projet ni filigrane ajoute ;
- aucun nouveau statut produit lourd ajoute.

## SELARL-SMOKE-REALISTIC-001

Objectif : smoke tester le parcours SELARL avec des donnees realistes apres realignement.

Fichiers concernes :

- exemples de contexte si besoin ;
- rapport `docs/review/selarl_smoke_realistic_001_report_v1.md` ;
- tests unitaires si un bug de projection est trouve.

Ne pas toucher :

- generateurs sauf bug explicitement ouvert ;
- moteur DOCX/PDF/ZIP sauf bug explicitement ouvert ;
- wording juridique.

Tests attendus :

- smoke dossier SELARL unipersonnel medecin ;
- smoke dossier chirurgien-dentiste avec regime communautaire ;
- scenario avec cession activee et documents manuels/reserves controles selon le catalogue existant ;
- verification que `DOC-013` / `DOC-014` restent exclus.

Criteres d'acceptation :

- les documents produits correspondent aux seuls documents prets ;
- les documents manuels restent visibles mais exclus de generation ;
- les champs manquants sont lisibles par bloc metier ;
- aucun document manuel n'est genere.

## SELARL-JURIST-REVIEW-001

Objectif : faire valider le parcours realigne par un juriste Sydel avant extension.

Fichiers concernes :

- rapport de revue `docs/review/selarl_jurist_review_001_report_v1.md` ;
- specs SELARL V2 si arbitrages ;
- backlog si nouveaux tickets.

Ne pas toucher :

- code sans ticket d'implementation ;
- generateurs ;
- templates ;
- wording juridique hors decision explicite.

Tests attendus :

- aucun test code obligatoire si revue documentaire pure ;
- controle du diff si specs mises a jour.

Criteres d'acceptation :

- validation ou reserves explicites sur `Fiche Client` ;
- validation ou reserves explicites sur `Praticien` ;
- validation ou reserves explicites sur l'ordre ;
- validation ou reserves explicites sur `Dossier unipersonnel` ;
- decisions listees avant tout nouveau code documentaire.

## Ticket retire ou absorbe

`SELARL-DOCUMENT-STATUS-REALIGN-001` est retire du backlog cible V2.

La clarification documentaire reste absorbee dans `SELARL-FLOW-REALIGN-001`, `SELARL-UI-REALIGN-001` et `SELARL-SMOKE-REALISTIC-001` sous une forme simple :

- respecter les statuts techniques et reserves existants ;
- ne pas generer les documents manuels ;
- ne pas inventer de mode Projet ou filigrane ;
- ne pas ajouter de couche produit lourde sans validation explicite.
