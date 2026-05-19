# Plan d'implémentation SELARL V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Découper la suite du pilote SELARL en tickets petits, traçables et testables.

Ce plan ne lance aucune implémentation dans le ticket courant.

Correction de reconstruction contrôlée : les tickets de réalignement NotebookLM ont resserré ce plan autour de `Fiche Client`, `Praticien`, du flow en six étapes et de `Dossier unipersonnel`. Les règles de réutilisation SELARL doivent rester explicites : aucune déduction mandataire / vendeur / locataire / siège / cabinet / lieu d'exercice ne doit devenir un défaut. Aucun mode Projet / filigrane et aucune couche produit documentaire lourde ne sont prévus en V1.

## SELARL-FORM-SCHEMA-IMPL-001

Objectif : implémenter le schéma de données UI SELARL côté Assistant métier, sans génération de nouveaux documents.

Fichiers concernés :

- `src/sydel_doc_engine/app/business_wizard.py`
- `src/sydel_doc_engine/app/ui_runtime.py`
- `tests/unit/test_business_wizard.py`
- documentation de pilotage.

Risques :

- introduire des champs qui n'alimentent aucun document ;
- casser le mode SCI déjà existant ;
- mélanger SELARL et SELAS.
- réactiver par erreur `DOC-013` ou `DOC-014` comme générables alors que la vraie V2 les exclut du pilote automatisé.

Tests attendus :

- sélection SELARL médecin ;
- sélection SELARL chirurgien-dentiste ;
- conditions `site_distinct`, `scm_cession`, `regime_communautaire`, `derogation`, `cession` ;
- `Dossier unipersonnel` : Praticien = associé unique = gérant = signataire seulement si l'option est active ;
- options explicites SELARL acquéreur, SELARL cessionnaire SCM et domiciliation = siège.
- vérification que les documents de dérogation SELARL sont affichés comme manuels / hors génération pilote.

Critères d'acceptation :

- aucun générateur modifié ;
- aucun wording juridique modifié ;
- tous les champs SELARL ont un label qualifié ;
- aucune réutilisation sensible n'est activée par défaut ;
- la réserve source V2 sur la lettre d'avertissement conjoint est visible dans les documents attendus ;
- `DOC-013` et `DOC-014` sont exclus des codes générables du pilote SELARL ;
- ruff et pytest OK.

## SELARL-UI-WIZARD-IMPL-001

Objectif : adapter l'écran Streamlit du mode Assistant métier pour afficher le parcours SELARL cible.

Fichiers concernés :

- `src/sydel_doc_engine/app/streamlit_app.py`
- `src/sydel_doc_engine/app/business_wizard.py`
- tests runtime UI existants.

Risques :

- rendre l'UI trop large en un seul écran ;
- introduire de la logique métier directement dans Streamlit ;
- masquer les documents manuels.

Tests attendus :

- rendu des conditions SELARL ;
- absence du libellé `Dirigeant / pharmacien` pour SELARL ;
- absence de champ nommé seulement `adresse` dans les labels SELARL ;
- documents attendus recalculés à partir de `get_expected_documents(...)`.
- affichage manuel de `Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL`, `Dérogation SEL BNC` et `Dérogation cumul SELARL BNC`.

Critères d'acceptation :

- les écrans SELARL suivent la spec UI ;
- le mode Technique / diagnostic reste intact ;
- le mode SCI existant reste intact ;
- ruff et pytest OK.

## SELARL-DOCS-GENERATION-SMOKE-001

Objectif : smoke tester la génération SELARL avec le contexte fourni par le formulaire, document par document.

Fichiers concernés :

- exemples de contexte SELARL ;
- tests de smoke si existants ;
- rapport de revue.

Risques :

- certains documents générables restent `Contexte incomplet` faute de champs ;
- les documents formulaire à compléter peuvent être confondus avec des documents finalisés ;
- le backend PDF local peut être indisponible.

Tests attendus :

- SELARL médecin sans condition ;
- SELARL chirurgien-dentiste sans condition ;
- SELARL avec régime communautaire ;
- SELARL avec cession cabinet médical ;
- SELARL avec cession cabinet dentaire ;
- SELARL avec SCM cession ;
- vérification que les documents manuels ne sont pas générés.
- SELARL avec dérogation : vérifier que les documents de dérogation restent listés mais exclus de la génération.

Critères d'acceptation :

- DOCX produits pour les documents prêts ;
- ZIP dossier produit ;
- PDF optionnel documenté selon disponibilité locale ;
- rapport listant les documents restés incomplets.
- aucun DOCX `DOC-013` ou `DOC-014` produit par le smoke SELARL tant que la V2 reste dans cet état.

## SELARL-JURIST-REVIEW-001

Objectif : organiser la revue humaine du parcours SELARL et des premiers rendus.

Fichiers concernés :

- `docs/review/*selarl*`
- éventuellement captures ou checklists de revue.

Risques :

- validation UX sans validation juridique ;
- confusion entre formulaire à compléter et document finalisé ;
- anomalie source statuts médecin non arbitrée.

Tests attendus :

- revue de la liste des questions ;
- revue des documents attendus ;
- revue des documents manuels ;
- revue d'un dossier smoke.

Critères d'acceptation :

- décisions juridiques tracées ;
- wording validé ou points ouverts listés ;
- prochain lot d'implémentation priorisé.

## REPLICATION-NEXT-CASE-001

Objectif : appliquer le protocole SELARL au prochain processus, sans copier aveuglément les choix SELARL.

Fichiers concernés :

- nouvelle spec processus ;
- nouvelle spec formulaire ;
- plan d'implémentation du processus suivant ;
- rapport de comparaison.

Risques :

- généraliser trop tôt des règles propres à la SELARL ;
- réutiliser des libellés non pertinents ;
- mélanger plusieurs processus dans une même PR.

Tests attendus :

- comparaison source vérité vs catalogue ;
- liste de documents attendus ;
- règles de réutilisation des données ;
- écarts avec l'UI actuelle.

Critères d'acceptation :

- protocole appliqué étape par étape ;
- différences avec SELARL explicitement listées ;
- aucun générateur modifié ;
- prochain ticket d'implémentation proposé.
