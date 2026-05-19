# Backlog de reconstruction contrôlée SELARL V2

Ticket source : `SELARL-NOTEBOOKLM-RECONCILIATION-001`

## Principes

- Ne pas toucher aux générateurs avant réalignement produit.
- Ne pas modifier le moteur DOCX/PDF/ZIP.
- Ne pas généraliser aux autres cas.
- Ne pas changer de wording juridique dans les actes.
- Corriger d'abord le schéma et les tests, puis l'UI.
- Garder le mode `Technique / diagnostic` et le parcours SCI existants.

## Ordre recommandé

1. `SELARL-WORDING-REALIGN-001`
2. `SELARL-FORM-FLOW-REALIGN-001`
3. `SELARL-REUSE-RULES-REALIGN-001`
4. `SELARL-DOCUMENT-STATUS-REALIGN-001`
5. `SELARL-UI-REPAIR-001`
6. `SELARL-SMOKE-REALISTIC-001`
7. `SELARL-JURIST-REVIEW-001`

## SELARL-WORDING-REALIGN-001

Objectif : réaligner les libellés SELARL visibles sur NotebookLM.

Fichiers concernés :

- `docs/project/SELARL_FORM_SCHEMA_V1.md` ou nouvelle version V2 ;
- `docs/project/SELARL_UI_WIZARD_SPEC_V1.md` ou nouvelle version V2 ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `tests/unit/test_selarl_form_schema.py` ;
- `tests/unit/test_business_wizard.py`.

Ne pas toucher :

- générateurs ;
- moteur DOCX/PDF/ZIP ;
- `streamlit_app.py` sauf si le ticket est explicitement élargi ;
- autres cas que SELARL.

Tests attendus :

- test absence de `professionnel principal` dans les labels SELARL visibles ;
- test présence de `Praticien`, `Fiche Client`, `Gérant`, `Associé`, `Signataire`, `Mandataire` selon contexte ;
- test absence de `CELAR` hors source NotebookLM.

Critères d'acceptation :

- le vocabulaire visible est aligné sur NotebookLM ;
- les labels techniques internes peuvent rester stables si non visibles ;
- aucune modification juridique documentaire.

## SELARL-FORM-FLOW-REALIGN-001

Objectif : réaligner l'ordre conceptuel du formulaire SELARL.

Fichiers concernés :

- `docs/project/SELARL_UI_WIZARD_SPEC_V2.md` ;
- `docs/project/SELARL_FORM_SCHEMA_V2.md` ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- tests unitaires du schéma et du wizard.

Ne pas toucher :

- rendu Streamlit visible si non nécessaire ;
- générateurs ;
- moteur DOCX/PDF/ZIP ;
- cas SCI, SELAS, SPFPL, SCM, SAS.

Tests attendus :

- ordre des blocs : qualification, Fiche Client / Praticien, Fiche Société, Capital & Associés, scénarios, documents ;
- présence du type d'opération ;
- conservation des documents attendus.

Critères d'acceptation :

- le schéma machine-readable exprime l'ordre NotebookLM ;
- les blocs inactifs restent non bloquants ;
- la société ne précède plus le praticien dans le cadrage SELARL.

## SELARL-REUSE-RULES-REALIGN-001

Objectif : corriger les règles de réutilisation SELARL.

Fichiers concernés :

- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- `tests/unit/test_selarl_form_schema.py` ;
- `tests/unit/test_business_wizard.py` ;
- specs SELARL V2.

Ne pas toucher :

- générateurs ;
- templates ;
- moteur ;
- code des autres cas.

Tests attendus :

- dossier unipersonnel : praticien = associé unique = gérant = signataire si option active ;
- mandataire distinct du signataire par défaut ;
- mandataire Sydel proposé par défaut ;
- SELARL réutilisable comme acquéreur / cessionnaire seulement via option ;
- vendeur = locataire actuel seulement via option ;
- siège = lieu d'exercice / cabinet seulement via option.

Critères d'acceptation :

- aucune dérivation sensible n'est automatique sans confirmation ;
- les champs dérivés sont identifiables et verrouillables ;
- les anciennes règles trompeuses sont supprimées ou renommées.

## SELARL-DOCUMENT-STATUS-REALIGN-001

Objectif : distinguer statut technique et statut produit des documents SELARL.

Fichiers concernés :

- `docs/project/SELARL_PROCESS_SPEC_V2.md` ;
- `docs/project/SELARL_UI_WIZARD_SPEC_V2.md` ;
- `src/sydel_doc_engine/domain/case_catalog.py` ou couche d'overlay statut SELARL ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- tests unitaires associés.

Ne pas toucher :

- générateurs ;
- moteur DOCX/PDF/ZIP ;
- templates ;
- wording juridique.

Tests attendus :

- `DOC-001` à `DOC-003` restent générables simples ;
- statuts / PV / ordre peuvent être `Projet` ou `brouillon à relire` ;
- cession / bail / SCM ne sont pas présentés comme définitifs ;
- `DOC-013` / `DOC-014` restent manuels ;
- `DOC-006` garde sa réserve ;
- pièces Ordre visibles comme bloquantes ou alertantes selon décision.

Critères d'acceptation :

- l'utilisateur ne peut pas confondre générable technique et définitif juridique ;
- le mode Projet est représenté dans le schéma ;
- les documents manuels restent exclus de génération.

## SELARL-UI-REPAIR-001

Objectif : réparer le parcours Streamlit SELARL après réalignement du schéma.

Fichiers concernés :

- `src/sydel_doc_engine/app/streamlit_app.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` si projections UI nécessaires ;
- `tests/unit/test_business_wizard.py` ;
- rapport de revue UI.

Ne pas toucher :

- générateurs ;
- moteur DOCX/PDF/ZIP ;
- mode `Technique / diagnostic` ;
- parcours SCI ;
- autres cas métier.

Tests attendus :

- tests unitaires de parcours SELARL ;
- tests source-level anti-regression sur libellés ;
- contrôle que les documents manuels ne partent pas en génération ;
- contrôle que le mode Projet est visible ou explicitement réservé.

Critères d'acceptation :

- parcours visible : qualification, Fiche Client, Fiche Société, Capital & Associés, scénarios, documents/génération ;
- labels alignés NotebookLM ;
- mandataire par défaut Sydel ;
- documents complexes affichés comme brouillons/projets à relire.

## SELARL-SMOKE-REALISTIC-001

Objectif : smoke tester le parcours SELARL avec des données réalistes après réparation.

Fichiers concernés :

- exemples de contexte si besoin ;
- rapport `docs/review/selarl_smoke_realistic_001_report_v1.md` ;
- tests unitaires si un bug de projection est trouvé.

Ne pas toucher :

- générateurs sauf bug explicitement ouvert ;
- moteur DOCX/PDF/ZIP sauf bug explicitement ouvert ;
- wording juridique.

Tests attendus :

- smoke dossier SELARL unipersonnel médecin ;
- smoke dossier chirurgien-dentiste avec régime communautaire ;
- scénario avec cession activée mais documents complexes marqués brouillon / contexte incomplet si non branchés ;
- vérification que `DOC-013` / `DOC-014` restent exclus.

Critères d'acceptation :

- les documents produits correspondent aux seuls documents prêts ;
- les documents complexes sont visibles avec leur bon statut ;
- les champs manquants sont lisibles par bloc métier ;
- aucun document manuel n'est généré.

## SELARL-JURIST-REVIEW-001

Objectif : faire valider le parcours réaligné par un juriste Sydel avant extension.

Fichiers concernés :

- rapport de revue `docs/review/selarl_jurist_review_001_report_v1.md` ;
- specs SELARL V2 si arbitrages ;
- backlog si nouveaux tickets.

Ne pas toucher :

- code sans ticket d'implémentation ;
- générateurs ;
- templates ;
- wording juridique hors décision explicite.

Tests attendus :

- aucun test code obligatoire si revue documentaire pure ;
- contrôle du diff si specs mises à jour.

Critères d'acceptation :

- validation ou réserves explicites sur vocabulaire ;
- validation ou réserves explicites sur ordre ;
- validation ou réserves explicites sur documents brouillons / manuels ;
- décisions listées avant tout nouveau code documentaire.
