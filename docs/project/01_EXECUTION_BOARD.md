# Tableau d'exécution

## Statuts
- READY
- IN_PROGRESS
- BLOCKED
- DONE

## Tickets actifs

| ID | Statut | Objet | Entrées obligatoires | Sorties obligatoires |
|---|---|---|---|---|
| PM-001 | DONE | Installer la mémoire projet dans le repo | source de vérité + specs Lot 1 | docs/project/* |
| PM-002 | DONE | Vérifier et compléter la mémoire projet opérationnelle | AGENTS.md + docs/project/* | docs/project complétés + artefact parasite traité |
| PM-003 | DONE | Installer le kit de reprise nouveau ChatGPT / Codex | mémoire projet existante | handoff + last state + prompt nouveau chat |
| DOC-001 | DONE | Implémenter la déclaration de non-condamnation | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-003 | DONE | Implémenter la procuration | source doc + spec Lot 1 | générateur + tests + MAJ doc |
| DOC-002 | DONE | Implémenter l'autorisation de domiciliation | source doc + spec Lot 1 + décision V1 adresse libre | générateur + tests + MAJ doc |
| ORCH-001 | DONE | Brancher l'orchestrateur Lot 1 | générateurs DOC-001/002/003 | service orchestrateur + tests |
| PM-004 | DONE | Intégrer l'arbre moteur document-centré V1 dans la mémoire projet | arbre moteur document-centré V1 | board + dernier état mis à jour |
| PM-005 | DONE | Intégrer le dictionnaire canonique des variables V1 dans la mémoire projet | dictionnaire canonique des variables V1 | board + dernier état mis à jour |
| SMOKE-001 | DONE | Smoke test réel Lot 1 via orchestrateur | contexte exemple Lot 1 + orchestrateur | 3 DOCX générés + docs projet mises à jour |
| VAR-001 | DONE | Ajouter une table de mapping document -> variables canoniques | arbre documentaire V1 + dictionnaire canonique V1 + specs | table de mapping document -> variables canoniques |
| PM-006 | DONE | Intégrer le cadrage métier PV nomination gérant V1 dans la mémoire projet | cadrage Lot 2 PV nomination gérant | board + dernier état mis à jour |
| SPEC-PV-001 | DONE | Formaliser la spec canonique du PV nomination gérant à partir du cadrage V1 | cadrage Lot 2 + arbre documentaire V1 + dictionnaire canonique V1 + table de mapping V1 | spec canonique écrite, blocs conditionnels, mapping variables, règles `associes[]`, points ouverts |
| SPEC-TEXTE-PV-001 | DONE | Stabiliser le texte canonique et les variantes du PV nomination gérant | spec canonique PV nomination gérant V1 + source Lot 2 | spec textuelle détaillée, variantes structurelles, wording à valider, critères avant code |
| CODE-PV-001 | DONE | Implémenter le générateur canonique PV nomination gérant | spec canonique V1 + spec texte V1 + source Lot 2 | générateur PV from-scratch + tests associes[]/genre/emprunt + MAJ doc |
| REVIEW-PV-001 | DONE | Préparer la revue humaine du PV nomination gérant généré | contexte exemple Lot 2 + générateur PV existant | DOCX régénéré + aperçu texte + checklist de revue humaine |
| SPEC-RENDER-001 | DONE | Spécifier une couche de rendu DOCX commune | générateurs DOC-001/002/003 + PV nomination gérant + specs existantes | spec technique render style system V1 |
| RENDER-STYLE-001 | DONE | Implémenter la couche de rendu DOCX commune | spec render style system V1 + générateurs existants | helpers communs + générateurs migrés + tests + smoke DOCX |
| ORCH-L2-PV-001 | DONE | Brancher le PV nomination gérant dans l'orchestrateur | générateur PV + specs Lot 2 + décisions de sélection | catalogue + registre orchestrateur + tests ciblés |
| UI-001 | BLOCKED | Brancher Streamlit V0 Lot 1 | orchestrateur Lot 1 + spec canonique PV nomination gérant validée | écran simple + test manuel |

## Référentiels moteur disponibles
- Le moteur dispose désormais d'un arbre documentaire document-centré V1 : `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`.
- Le moteur dispose désormais d'un dictionnaire canonique des variables V1 : `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`.
- Le moteur dispose désormais d'une table de mapping document -> variables canoniques V1 : `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.
- Le cadrage métier de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- La spec canonique V1 de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- La spec texte V1 de la famille `PV nomination gérant` est disponible : `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- La spec technique V1 de couche de rendu DOCX commune est disponible : `docs/delivery/render_style_system_v1.md`.
- Le pack de revue humaine du PV nomination gérant est disponible : `docs/review/lot_02_pv_nomination_gerant_review_v1.md`.
- L'aperçu texte extrait du DOCX généré est disponible : `docs/review/lot_02_pv_nomination_gerant_preview_v1.txt`.
- Ces référentiels cadrent les prochains tickets ; ils ne doivent pas être réinventés pendant l'implémentation.

## Ecart temporaire connu
- Nom canonique retenu pour la domiciliation : `domiciliation.adresse_affichee`.
- Alias legacy temporaire présent dans le code Lot 1 : `adresse_domiciliation_affichee`.
- Le présent ticket ne refactore pas le code Python ; les prochains tickets doivent converger vers le nom canonique sans recréer de variante locale.

## Détail des prochains tickets

### DOC-001
- Objectif : générer la déclaration sur l'honneur de non-condamnation.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- ADR à relire : ADR-0001, ADR-0002, ADR-0004, ADR-0005.
- Contraintes : source reçue, spec écrite, accords de genre, DOCX propre, tests obligatoires.
- Sortie attendue : générateur DOC-001, tests, mise à jour documentaire.

### DOC-003
- Objectif : générer la procuration après DOC-001.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contraintes : bloc mandataire SYDEL externalisé en configuration, wording source conservé.
- Sortie attendue : générateur DOC-003, tests, mise à jour documentaire.

### DOC-002
- Objectif : générer l'autorisation de domiciliation après arbitrage V1 déjà posé.
- Spec à lire : `docs/delivery/lot_01_analysis_and_specs_v1.md`.
- Contrainte sensible : le nom canonique documentaire est désormais `domiciliation.adresse_affichee`; le code Lot 1 existant conserve temporairement l'alias legacy `adresse_domiciliation_affichee`.
- Sortie : générateur DOC-002 terminé, tests unitaires ciblés ajoutés, validations locales vertes.

### ORCH-001
- Objectif : brancher les trois générateurs Lot 1 dans l'orchestrateur dossier.
- Prérequis : DOC-001, DOC-002 et DOC-003 terminés.
- Sortie : registre minimal DOC-001/DOC-002/DOC-003 branché, génération DOCX dossier selon `ctx.structure`, tests d'orchestration ajoutés.

### VAR-001
- Objectif : ajouter une table de mapping document -> variables canoniques sans refaire le dictionnaire.
- Prérequis : arbre documentaire V1 et dictionnaire canonique des variables V1 intégrés.
- Sortie : table de mapping V1 intégrée à la mémoire projet, sans réécriture ; écart temporaire documenté entre `domiciliation.adresse_affichee` et l'alias legacy `adresse_domiciliation_affichee`.

### SPEC-PV-001
- Objectif : formaliser la spec canonique du PV nomination gérant à partir du cadrage V1, sans refaire le cadrage.
- Spec/cadrage à lire : `docs/delivery/lot_02_pv_nomination_gerant_cadrage_v1.md`.
- Prérequis : arbre documentaire V1, dictionnaire canonique V1 et table de mapping document -> variables canoniques V1.
- Contraintes : traiter `PV nomination gérant` comme une famille documentaire mutualisable, gérer `associes[]` dynamiquement, distinguer `dirigeant_nomine` de `associes[]`, identifier les blocs conditionnels, ne coder aucun générateur.
- Sortie attendue : spec canonique écrite dans `docs/delivery/`, avec structure, blocs fixes, blocs conditionnels, mapping variables, règles de répétition, règles de grammaire minimales et points ouverts.
- Statut : terminé ; spec canonique V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.

### SPEC-TEXTE-PV-001
- Objectif : stabiliser le texte canonique et les variantes du PV nomination gérant avant tout codage.
- Spec à lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md`.
- Source à consulter : `project/source_documents/lot_02/PV nomination gérant - transforme.docx`.
- Contraintes : ne pas refaire la spec canonique, ne pas coder de générateur, ne pas modifier implicitement le wording juridique ; signaler les formulations à validation.
- Sortie attendue : spec textuelle détaillée du PV nomination gérant, variantes structurelles explicites, wording à valider, critères d'entrée avant code.
- Statut : terminé ; spec texte V1 disponible dans `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.

### CODE-PV-001
- Objectif : implémenter le générateur canonique `PV nomination gérant` à partir des specs V1, sans reprendre `personne_1` / `personne_2` comme vérité métier.
- Specs à lire : `docs/delivery/lot_02_pv_nomination_gerant_spec_canonique_v1.md` et `docs/delivery/lot_02_pv_nomination_gerant_spec_texte_v1.md`.
- Source à consulter : `project/source_documents/lot_02/PV nomination gérant - transforme.docx`.
- Contraintes : générateur DOCX from-scratch, `associes[]` dynamique, `dirigeant_nomine` distinct, variantes `né/née`, branche `emprunt.actif`, renumérotation des décisions, aucun changement de wording juridique hors spec texte.
- Sortie attendue : générateur dédié, tests unitaires ciblés, validation locale, mise à jour documentaire.
- Statut : terminé ; générateur disponible dans `src/sydel_doc_engine/generators/lot_02/pv_nomination_gerant.py`, non branché à l'orchestrateur.
- Smoke test réel : contexte exemple disponible dans `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/`.

### REVIEW-PV-001
- Objectif : préparer la revue humaine du rendu DOCX et du wording du PV nomination gérant déjà codé, sans modifier le code métier.
- Entrées : générateur PV existant, contexte exemple `examples/contexts/lot_02_pv_nomination_gerant_example.yaml`, specs Lot 2.
- Sortie : DOCX régénéré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/pv_nomination_gerant.docx`, aperçu texte et checklist de revue dans `docs/review/`.
- Statut : terminé ; le PV reste non branché à l'orchestrateur Lot 2 tant qu'une validation humaine explicite n'a pas été donnée.

### SPEC-RENDER-001
- Objectif : formaliser une couche de rendu DOCX commune avant refactor du code métier.
- Spec à lire : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ne modifier aucun générateur, ne changer aucun wording juridique, documenter les styles communs, le titre encadré, les signatures simples/encadrées, le rappel légal et les surcharges documentaires.
- Sortie : spec technique V1 créée ; documents impactés listés : DOC-001, DOC-002, DOC-003 et PV nomination gérant.
- Statut : terminé ; le point d'écart explicite est que les encadrés de signature manquent aujourd'hui dans le rendu généré.

### RENDER-STYLE-001
- Objectif : implémenter la couche commune de rendu DOCX dans `src/sydel_doc_engine/rendering/docx_builder.py`.
- Prérequis : `docs/delivery/render_style_system_v1.md`.
- Contraintes : ticket technique uniquement, aucun changement de wording juridique, migration progressive, tests existants à conserver verts.
- Sortie attendue : profil global de style, helpers de paragraphes/blocs, titre encadré, signature simple, signature encadrée disponible, rappel légal commun.
- Statut : terminé ; couche commune implémentée et appliquée à DOC-001, DOC-002, DOC-003 et PV nomination gérant.

### ORCH-L2-PV-001
- Objectif : brancher le générateur PV nomination gérant dans le catalogue et l'orchestrateur, sans UI, PDF ni ZIP.
- Prérequis : générateur PV existant, specs Lot 2, décisions de sélection SELARL/SELAS/SPFPL cession/SPFPL apport/SCS/SCI/SCM et exclusion SAS.
- Sortie : `DOC-004` ajouté au catalogue, générateur enregistré, sélection testée pour SELARL/SCI/SAS, génération orchestrée testée avec production du DOCX PV.
- Statut : terminé ; aucune modification de wording juridique.

### UI-001
- Objectif : exposer une Streamlit simple pour générer le Lot 1.
- Statut : en attente explicite ; ne pas lancer sans ticket explicite dédié.
- Prérequis : orchestrateur Lot 1 fonctionnel et spec canonique `PV nomination gérant` validée.
- Sortie attendue : écran simple, génération testable manuellement, aucun métier caché dans l'UI.

## Règle de mise à jour
Chaque ticket terminé doit mettre à jour ce fichier :
- passer son statut à DONE
- déplacer le ticket actif en IN_PROGRESS pendant l'exécution si la tâche dure plus qu'une modification courte
- indiquer le prochain ticket à lancer
- indiquer les éventuels points ouverts
- mettre à jour `docs/project/04_LAST_STATE.md`

## Prochaine étape prévue
- prochaine action recommandée : lancer un ticket dédié de smoke dossier Lot 2 via orchestrateur sur contexte réel, sans PDF/ZIP/UI.
- action suivante côté métier : relire humainement `docs/review/lot_02_pv_nomination_gerant_review_v1.md`, l'aperçu texte et le DOCX généré.
- UI-001 reste explicitement en attente.

## Points ouverts
- Aucun point bloquant identifié après le smoke test réel Lot 1.
- Les trois DOCX sont bien produits par l'orchestrateur dans `artifacts/lot_01_smoke_test/`, mais le rendu visuel et le wording juridique restent à relire humainement dans les fichiers générés.
- PDF et ZIP restent hors ORCH-001 et devront être traités dans un ticket dédié.
- Ecart temporaire non bloquant pour l'UI : la table V1 retient `domiciliation.adresse_affichee` comme nom canonique, tandis que le code Lot 1 existant conserve l'alias legacy `adresse_domiciliation_affichee` jusqu'à refactor dédié.
- ORCH-L2-PV-001 est terminé ; le PV nomination gérant est branché dans l'orchestrateur pour les structures concernées et exclu pour SAS.
- REVIEW-PV-001 est terminé, mais la validation humaine du rendu DOCX et du wording reste à obtenir pour la revue juridique fine.
- RENDER-STYLE-001 est terminé ; les signatures encadrées sont disponibles dans la couche commune et appliquées aux signatures Lot 1.
- Le PV nomination gérant conserve des signatures répétables simples ; toute signature encadrée dirigeant/associés séparée reste soumise à validation métier.
- UI-001 reste en attente explicite : ne pas lancer le branchement Streamlit sans nouveau ticket.
- Points ouverts PV documentés dans la spec texte : périmètre SELAS, capital non variable, société déjà immatriculée, dirigeant non associé, ponctuation finale des associés, féminisation éventuelle de la fonction, règle `euro/euros`.

## Journal court
- 2026-05-12 : mémoire projet installée dans `docs/project/`.
- 2026-05-12 : mémoire projet complétée pour servir de contexte opérationnel autonome ; artefact `tall -U pip` identifié comme fichier parasite à supprimer.
- 2026-05-12 : kit de reprise ajouté pour nouveau ChatGPT / Codex avec handoff, dernier état et prompt de reprise.
- 2026-05-12 : DOC-001 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-001 corrigé pour rendre l'adresse personnelle dans l'ordre source `num voie + voie, ville cp`.
- 2026-05-12 : DOC-003 implémenté en génération DOCX from-scratch avec tests unitaires ; validations locales vertes.
- 2026-05-12 : DOC-002 implémenté en génération DOCX from-scratch avec champ libre `adresse_domiciliation_affichee` ; validations locales vertes.
- 2026-05-12 : ORCH-001 branche les générateurs DOC-001, DOC-002 et DOC-003 dans l'orchestrateur dossier ; génération DOCX uniquement.
- 2026-05-13 : logique documentaire du moteur formalisée par l'arbre document-centré V1 ; mémoire projet alignée sans réécriture de l'arbre.
- 2026-05-13 : SMOKE-001 génère réellement les trois DOCX du Lot 1 via l'orchestrateur avec `examples/contexts/lot_01_example.yaml` corrigé au strict minimum.
- 2026-05-13 : dictionnaire canonique des variables V1 intégré dans la mémoire projet ; le moteur dispose désormais d'un arbre documentaire et d'un dictionnaire canonique de variables.
- 2026-05-13 : table de mapping document -> variables canoniques V1 intégrée dans la mémoire projet sans réécriture ; écart temporaire `domiciliation.adresse_affichee` / `adresse_domiciliation_affichee` documenté.
- 2026-05-13 : cadrage métier V1 de la famille `PV nomination gérant` intégré dans la mémoire projet ; SPEC-PV-001 ajouté en READY et UI-001 placé en attente tant que cette famille n'est pas spécifiée.
- 2026-05-13 : spec canonique V1 de la famille `PV nomination gérant` intégrée dans la mémoire projet ; SPEC-PV-001 passé DONE, SPEC-TEXTE-PV-001 ajouté READY, UI-001 maintenu en attente explicite.
- 2026-05-13 : spec texte V1 de la famille `PV nomination gérant` créée ; SPEC-TEXTE-PV-001 passé DONE, CODE-PV-001 ajouté READY, aucun code Python modifié.
- 2026-05-13 : CODE-PV-001 implémente le générateur DOCX from-scratch du PV nomination gérant avec `associes[]`, `dirigeant_nomine`, branche `emprunt.actif`, variantes de genre/singulier-pluriel et tests ciblés ; ruff et pytest verts.
- 2026-05-13 : smoke test réel CODE-PV-001 ajouté via `examples/contexts/lot_02_pv_nomination_gerant_example.yaml` ; DOCX généré dans `artifacts/lot_02_pv_nomination_gerant_smoke_test/` hors versionnement.
- 2026-05-13 : REVIEW-PV-001 régénère le DOCX PV depuis le contexte exemple, extrait un aperçu texte et crée une checklist de revue humaine dans `docs/review/`, sans modification du code Python.
- 2026-05-13 : SPEC-RENDER-001 crée la spec technique `docs/delivery/render_style_system_v1.md` pour une couche de rendu DOCX commune, sans modification de code Python.
- 2026-05-13 : RENDER-STYLE-001 implémente la couche commune de rendu DOCX, migre DOC-001/DOC-002/DOC-003/PV nomination gérant, ajoute les tests de rendu et génère les smoke DOCX dans `artifacts/render_style_001_*`.
- 2026-05-13 : ORCH-L2-PV-001 branche le PV nomination gérant dans le catalogue et l'orchestrateur pour SELARL, SELAS, SPFPL cession, SPFPL apport, SCS, SCI et SCM ; SAS reste exclue ; ruff et pytest verts.
