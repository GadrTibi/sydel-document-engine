# Audit du périmètre restant V1

Ticket : `AUDIT-REMAINING-SCOPE-001`

Date : 2026-05-15

## Objet

Ce document dresse un état de périmètre à partir de la source de vérité, des specs et préparations disponibles, et des générateurs présents dans `src/sydel_doc_engine/generators/`.

Il ne modifie pas le wording juridique et ne vaut pas validation métier. Il sert à séparer :

- ce qui est déjà codé ;
- ce qui est spécifié mais non codé ;
- ce qui est préparé mais non spécifié ;
- ce qui reste totalement à traiter.

## Sources lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`
- `docs/delivery/*`
- `src/sydel_doc_engine/generators/**/*`

## Définitions utilisées

- **Codé** : un générateur déterministe existe dans `src/sydel_doc_engine/generators/`, avec tests ciblés visibles quand ils existent.
- **Branché** : le document apparaît dans `src/sydel_doc_engine/registry/catalog.py` et dans le registre de générateurs de `src/sydel_doc_engine/orchestrator/service.py`.
- **Spécifié** : une spec canonique et/ou texte exploitable existe dans `docs/delivery/`.
- **Préparé** : une source a été placée, convertie, auditée ou cadrée, mais le cycle `Analysé -> Spécifié` n'est pas complet.
- **Hors automatisation initiale** : document marqué à remplir à la main ou nécessitant une décision explicite avant code.

## Synthèse courte

Le moteur dispose d'un socle codé large : documents universels, plusieurs blocs mutualisables, statuts principaux, option IS et satellites SAS. Le reste se concentre surtout sur SCM, quelques sources legacy ou récemment préparées, et sur l'alignement de documents déjà codés mais pas toujours branchés dans le catalogue/orchestrateur observé.

Points d'attention :

- La demande d'inscription à l'ordre dispose d'un générateur et de tests, mais son branchement catalogue/orchestrateur n'a pas été constaté dans les fichiers lus.
- Les générateurs SPFPL spécifiques existent pour note d'information, agrément, acte de cession de parts, contrat d'apport et attestations, mais leur branchement catalogue/orchestrateur n'a pas été constaté dans les fichiers lus.
- Le catalogue/orchestrateur lu expose clairement `DOC-001` à `DOC-024`, hors demande d'inscription à l'ordre et hors coeur SPFPL spécifique.
- Plusieurs sources SCM sont préparées, mais restent à spécifier et coder.

## 1. Déjà codé

### 1.1 Documents universels

| Document | État code | État branchement | Sources/specs |
|---|---|---|---|
| `DOC-001` - Déclaration sur l'honneur de non-condamnation | Codé | Branché | Lot 1 spécifié dans `docs/delivery/lot_01_analysis_and_specs_v1.md` |
| `DOC-002` - Autorisation de domiciliation | Codé | Branché | Lot 1 spécifié ; alias legacy d'adresse encore visible côté code |
| `DOC-003` - Procuration | Codé | Branché | Lot 1 spécifié |

### 1.2 Documents mutualisables

| Document ou famille | État code | État branchement | Remarque |
|---|---|---|---|
| `DOC-004` - PV nomination gérant | Codé | Branché | Mutualisé hors SAS ; pas branché SCI IRIS dans le catalogue lu |
| Demande d'inscription à l'ordre | Codé | Non constaté | Générateur `lot_02/demande_inscription_ordre.py` et tests présents ; absent du catalogue/orchestrateur lus |
| `DOC-005` - Lettre de renonciation à revendiquer la qualité d'associé | Codé | Branché | Batch régime communautaire |
| `DOC-006` - Lettre d'avertissement au conjoint | Codé | Branché | Batch régime communautaire |
| `DOC-007` - Avenant contrat de bail | Codé | Branché | SELARL/SELAS, condition cession |
| `DOC-008` - Appel de fonds SEL | Codé | Branché | SELARL uniquement dans le catalogue lu |
| `DOC-009` - Acte de cession cabinet médical | Codé | Branché | Famille cession cabinets |
| `DOC-010` - Compromis de cession cabinet médical | Codé | Branché | Famille cession cabinets |
| `DOC-011` - Acte de cession cabinet dentaire | Codé | Branché | Famille cession cabinets |
| `DOC-012` - Compromis de cession cabinet dentaire | Codé | Branché | Famille cession cabinets |
| `DOC-013` - Formulaire de dérogation multi-sites SEL | Codé | Branché | Produit un formulaire à compléter |
| `DOC-014` - Demande de dérogation cumul SELARL-BNC | Codé | Branché | Produit un formulaire à compléter |

### 1.3 Statuts

| Document | État code | État branchement | Remarque |
|---|---|---|---|
| `DOC-015` - Statuts SAS / SPFPL médecins | Codé | Branché | Source SAS/SPFPL médecins ; revue humaine recommandée |
| `DOC-016` - Statuts SELARL chirurgien-dentiste | Codé | Branché | Famille statuts SEL |
| `DOC-017` - Statuts SELARL médecin | Codé | Branché | Famille statuts SEL |
| `DOC-018` - Statuts SELAS médecin | Codé | Branché | Famille statuts SEL |
| `DOC-019` - Statuts SCS | Codé | Branché | Coeur statuts civils |
| `DOC-020` - Statuts SCI | Codé | Branché | Coeur statuts civils |
| `DOC-021` - Statuts SCI IRIS | Codé | Branché | Coeur statuts civils |
| Statuts SPFPL cession | Codé | Non constaté | Générateur `lot_04/statuts_spfpl_cession.py` présent ; branchement non constaté dans le catalogue lu |
| Statuts SPFPL apport | Codé | Non constaté | Générateur `lot_04/statuts_spfpl_apport.py` présent ; branchement non constaté dans le catalogue lu |

### 1.4 Spécifiques

| Document ou famille | État code | État branchement | Remarque |
|---|---|---|---|
| `DOC-022` - Lettre option IS | Codé | Branché | SCI / SCI IRIS |
| `DOC-023` - PV rémunération président SAS | Codé | Branché | Satellite SAS V1 |
| `DOC-024` - Attestation capital / liste des souscripteurs SAS | Codé | Branché | Satellite SAS V1 |
| Note d'information SPFPL | Codé | Non constaté | Générateur `lot_05/note_information.py` présent |
| PV agrément cession SPFPL - associé unique | Codé | Non constaté | Générateur présent |
| PV agrément cession SPFPL - plusieurs associés | Codé | Non constaté | Générateur présent |
| Acte de cession de parts SPFPL | Codé | Non constaté | Générateur présent |
| Contrat d'apport SEL/SPFPL | Codé | Non constaté | Générateur présent |
| Attestation sur le capital - apport - liste des souscripteurs SPFPL | Codé | Non constaté | Générateur présent, distinct du générateur SAS |
| Attestation nomination commissaire aux apports | Codé | Non constaté | Générateur présent |

## 2. Spécifié mais non codé

### 2.1 Statuts

| Document | Catégorie | État | Prochaine action |
|---|---|---|---|
| Statuts SCM | Statuts / spécifique SCM | Source préparée, specs statuts civils et arbitrages SCM disponibles, mais aucun générateur SCM constaté | `CODE-STATUTS-SCM-001` |

### 2.2 Spécifiques et mutualisables

Aucun autre document n'est clairement dans l'état "spec complète disponible, aucun générateur présent" sans nuance. Les cas suivants ont soit déjà un générateur, soit seulement une préparation/audit :

- demande d'inscription à l'ordre : générateur présent, mais branchement non constaté ;
- coeur SPFPL spécifique : générateurs présents, mais branchement non constaté ;
- satellites SCM : préparés mais pas spécifiés ;
- cession SCM : préparée mais pas spécifiée ;
- acte de cession d'actions : source/audit/préparation visibles, mais spec complète non constatée.

## 3. Préparé mais non spécifié

### 3.1 SCM

| Document | Catégorie | État préparatoire | Prochaine action |
|---|---|---|---|
| Pacte d'associés SCM | Spécifique SCM | Source placée dans `project/source_documents/lot_05/` via préparation satellites SCM | `SPEC-SCM-SATELLITES-001` |
| Liste dépenses communes SCM | Spécifique SCM | Source legacy convertie en DOCX exploitable | `SPEC-SCM-SATELLITES-001` |
| Contrat frais communs | Spécifique SCM | Source placée via préparation satellites SCM | `SPEC-SCM-SATELLITES-001` |
| Règlement intérieur SCM | Spécifique SCM | Source placée avec écart de nom documenté | `SPEC-SCM-SATELLITES-001` |
| PV AGE cession parts SCM - SELARL | Spécifique SCM cession | Source préparée | Spec cession SCM dédiée |
| Courrier SDE - SELARL | Spécifique SCM cession | Source préparée | Spec cession SCM dédiée |
| Acte cession parts SCM vers SELARL | Spécifique SCM cession | Source préparée | Spec cession SCM dédiée |
| PV AGE cession parts SCM - SELAS | Spécifique SCM cession | Source préparée | Spec cession SCM dédiée |
| Courrier SDE - SELAS | Spécifique SCM cession | Source préparée | Spec cession SCM dédiée |
| Acte cession parts SCM vers SEL | Spécifique SCM cession | Source préparée | Spec cession SCM dédiée |

### 3.2 Actes et sources legacy

| Document | Catégorie | État préparatoire | Prochaine action |
|---|---|---|---|
| Acte de cession d'actions SPFPL | Spécifique SPFPL cession | Audit V1 et préparation/conversion visibles ; source DOCX exploitable récemment préparée | Spec canonique + spec texte avant code |
| Demande de dérogation cumul SELARL salariée | Mutualisable / dérogation SELAS | Source legacy `.doc` identifiée ; conversion/remplacement encore ticketé | Conversion ou remplacement avant spec/code |

## 4. Reste totalement à traiter

### 4.1 Documents ou variantes hors automatisation initiale

| Document ou variante | Catégorie | Pourquoi ce n'est pas prêt |
|---|---|---|
| Formulaire de déclaration préalable de site distinct CD94 avec la SEL | Mutualisable / ordre-dérogation | Marqué à remplir à la main dans la source de vérité ; pas d'automatisation initiale sans décision explicite |
| Dérogation SEL BNC complet | Mutualisable / dérogation | Marqué à remplir à la main dans la source de vérité ; le moteur code seulement le formulaire ciblé `DOC-014` |
| Documents avec zones narratives sensibles non structurées | Plusieurs familles | Doivent rester manuels ou bloquants tant qu'aucune spec n'encadre le wording |

### 4.2 Fonctions transverses hors génération documentaire

| Bloc | État |
|---|---|
| PDF | Non intégré comme flux final V1 dans l'état audité |
| ZIP dossier | Non intégré comme flux final V1 dans l'état audité |
| Streamlit V0 | Explicitement en attente ; ne pas lancer sans ticket dédié |
| Validation juridique fine des rendus DOCX | Recommandée sur les familles codées ; les tests ne valent pas validation juridique |

## 5. Écarts et points de vigilance

### 5.1 Écart code présent / branchement non constaté

Les générateurs suivants existent et disposent de tests ou contextes visibles, mais ne sont pas branchés dans le catalogue/orchestrateur observé :

- `lot_02/demande_inscription_ordre.py`
- `lot_04/statuts_spfpl_cession.py`
- `lot_04/statuts_spfpl_apport.py`
- `lot_05/note_information.py`
- `lot_05/pv_agrement_cession_spfpl_associe_unique.py`
- `lot_05/pv_agrement_cession_spfpl_plusieurs_associes.py`
- `lot_05/acte_cession_parts_spfpl.py`
- `lot_05/contrat_apport_spfpl.py`
- `lot_05/attestation_capital_liste_souscripteurs.py`
- `lot_05/attestation_commissaire_apports.py`

Avant de coder de nouveaux documents dans ces familles, il faut décider si le prochain ticket doit d'abord aligner catalogue, orchestrateur et tests de sélection.

### 5.2 Écart documentation / état code

La documentation projet lue mentionne des lots déjà absorbés et des statuts avancés. Le code lu confirme une grande partie des générateurs, mais le registre moteur observé ne reflète pas tous les générateurs présents. L'audit retient donc la distinction `codé` / `branché` au lieu de réduire l'état à un seul statut.

### 5.3 Sources non suivies dans le worktree

Le worktree contenait des fichiers non suivis au moment de l'audit. Ils ont été lus quand ils existaient dans les chemins demandés, mais ce ticket ne les intègre pas et ne les modifie pas.

## 6. Estimation des blocs restants

Estimation en blocs fonctionnels, hors corrections mineures :

1. Alignement catalogue/orchestrateur des générateurs déjà présents mais non branchés.
2. Statuts SCM.
3. Satellites SCM : pacte, liste dépenses, contrat frais communs, règlement intérieur.
4. Cession SCM SELARL/SELAS : PV, courrier SDE, acte.
5. Acte de cession d'actions SPFPL.
6. Dérogation cumul SELARL salariée legacy.
7. Flux de sortie V1 : PDF, ZIP dossier.
8. Streamlit V0, seulement après ticket dédié.

## 7. Prochaine étape recommandée

Lancer d'abord un ticket d'alignement du registre moteur pour les générateurs déjà présents mais non branchés, ou confirmer explicitement que le prochain ticket prioritaire reste `SPEC-SCM-SATELLITES-001`.
