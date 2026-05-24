# Backlog rebuild front global V1

Ticket source : `GLOBAL-FRONT-ARCHITECTURE-001`

Statut : backlog de reconstruction, sans implementation dans ce ticket.

## Ordre recommande

1. `FRONT-DATA-LAYER-001`
2. `FRONT-ROLE-MODEL-001`
3. `FRONT-ADDRESS-MODEL-001`
4. `FRONT-DOSSIER-FLOW-001`
5. `FRONT-DOCUMENT-STATUS-LAYER-001`
6. `FRONT-UNIT-DOCUMENT-MODE-001`
7. `FRONT-TEST-PREFILL-001`
8. `FRONT-REVIEW-001`

Les tickets doivent rester separes. Aucun ticket ne doit modifier les generateurs ou le moteur DOCX/PDF/ZIP sans decision explicite.

## FRONT-DATA-LAYER-001

Objectif : creer la couche de donnees front globale a partir du registre V2.1.

Fichiers concernes :

- a creer : module de schema front global, a definir lors du ticket ;
- a lire : `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md` ;
- a lire : `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md` ;
- a lire : `docs/project/GLOBAL_FRONT_RULES_V1.md`.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- wording juridique ;
- Streamlit existant sauf si le ticket le prevoit explicitement.

Dependances :

- `GLOBAL-FRONT-ARCHITECTURE-001` DONE.

Critères d'acceptation :

- objets front representes sans reference au prototype comme source ;
- `Person`, `Organization`, `Address`, `RoleAssignment`, `Dossier`, `DocumentRequirement`, `FieldDefinition`, `ReuseRule`, `ValidationIssue`, `SupportingEvidence` couverts ;
- regles `SAME_FIELD`, `SAME_DATA_DIFFERENT_SHAPE`, `EXPLICIT_REUSE_ONLY`, `DISTINCT_FIELDS` et `UNCERTAIN_REQUIRES_HUMAN_DECISION` preservées ;
- tests ou validations adaptes au type de modification ;
- aucune modification des generateurs.

## FRONT-ROLE-MODEL-001

Objectif : modeliser les roles explicites et leurs assignments sans fusion silencieuse.

Fichiers concernes :

- couche de donnees front issue de `FRONT-DATA-LAYER-001` ;
- documentation des roles ;
- tests de non-regression role/reutilisation si code ajoute.

Ne pas toucher :

- generateurs ;
- catalogue moteur sauf besoin de lecture ;
- Streamlit prototype.

Dependances :

- `FRONT-DATA-LAYER-001`.

Critères d'acceptation :

- praticien, associe, gerant, president, signataire, mandataire, vendeur, cedant, acquereur, cessionnaire, bailleur, locataire et representant sont distincts ;
- `Dossier unipersonnel` cree des liens, pas des fusions ;
- un role peut etre scope dossier, operation, document ou lot ;
- cas personne morale + representant prevu.

## FRONT-ADDRESS-MODEL-001

Objectif : modeliser les adresses typees par usage et leurs formes composees/affichees.

Fichiers concernes :

- couche de donnees front ;
- mapping des adresses pivots ;
- tests de derivation si code ajoute.

Ne pas toucher :

- moteur DOCX ;
- generateurs ;
- wording de documents.

Dependances :

- `FRONT-DATA-LAYER-001`;
- `FRONT-ROLE-MODEL-001` si les adresses sont rattachees aux roles.

Critères d'acceptation :

- domicile praticien, lieu d'exercice, siege social et domiciliation distingues ;
- domiciliation = siege social modele comme regle ;
- siege = lieu d'exercice uniquement via option ;
- SCM cedee et cessionnaire SCM distincts par defaut ;
- adresse affichee derivee depuis composants avec override possible.

## FRONT-DOSSIER-FLOW-001

Objectif : definir le flow dossier complet global, data-first, sans maquettes detaillees.

Fichiers concernes :

- future couche front ;
- documentation de flow ;
- eventuels tests de selection de blocs si code ajoute.

Ne pas toucher :

- prototype Streamlit actuel ;
- generateurs ;
- moteur PDF/ZIP.

Dependances :

- `FRONT-DATA-LAYER-001`;
- `FRONT-ROLE-MODEL-001`;
- `FRONT-ADDRESS-MODEL-001`.

Critères d'acceptation :

- entree par operation/famille documentaire ;
- fiches personne et societe separees ;
- blocs parties, adresses, ordre, financement, bail, cession, SCM et SPFPL couverts ;
- distinction dossier complet vs document unitaire documentee ;
- documents attendus visibles avant generation.

## FRONT-DOCUMENT-STATUS-LAYER-001

Objectif : creer la couche de statut des documents attendus pour le futur front.

Fichiers concernes :

- future couche front ;
- `src/sydel_doc_engine/registry/catalog.py` en lecture ;
- eventuellement `src/sydel_doc_engine/domain/case_catalog.py` si le ticket l'autorise ;
- tests de statuts si code ajoute.

Ne pas toucher :

- generateurs ;
- contenu juridique ;
- sortie DOCX/PDF/ZIP.

Dependances :

- `FRONT-DATA-LAYER-001`;
- `FRONT-DOSSIER-FLOW-001`.

Critères d'acceptation :

- statuts generable, manuel, non implemente, reserve, contexte incomplet couverts ;
- document attendu et document pret a generer distingues ;
- champs manquants et pieces manquantes visibles ;
- documents manuels visibles mais exclus de la generation automatique ;
- mode dossier complet compatible avec le catalogue.

## FRONT-UNIT-DOCUMENT-MODE-001

Objectif : definir ou reconstruire le mode document unitaire comme outil separe de test et diagnostic.

Fichiers concernes :

- future couche front ;
- mode document unitaire futur ;
- tests de contexte minimal si code ajoute.

Ne pas toucher :

- parcours dossier complet ;
- generateurs ;
- Streamlit prototype tant que le ticket ne l'autorise pas.

Dependances :

- `FRONT-DOCUMENT-STATUS-LAYER-001`.

Critères d'acceptation :

- selection par `DOC-XXX` ;
- contexte minimal clairement separe du dossier complet ;
- champs requis du document affiches ;
- documents manuels/non supportes signales ;
- aucun comportement de reutilisation globale deduit depuis ce mode.

## FRONT-TEST-PREFILL-001

Objectif : concevoir des scenarios fictifs deterministes pour tester le nouveau front sans melanger prefill et donnees reelles.

Fichiers concernes :

- future couche de presets ;
- tests front/data ;
- documentation de scenarios.

Ne pas toucher :

- sources juridiques ;
- generateurs ;
- wording ;
- donnees reelles client.

Dependances :

- `FRONT-DOSSIER-FLOW-001`;
- `FRONT-DOCUMENT-STATUS-LAYER-001`;
- `FRONT-UNIT-DOCUMENT-MODE-001` si les presets couvrent le test unitaire.

Critères d'acceptation :

- presets marques comme fictifs ;
- scenarios couvrant SELARL standard, SELARL avec regime communautaire, cession cabinet, SCM, SPFPL et SCI si pertinent ;
- prefill reversible ;
- aucune valeur fictive masquee comme source metier ;
- tests reproductibles.

## FRONT-REVIEW-001

Objectif : organiser la revue produit/juriste du nouveau modele front avant implementation UI visible.

Fichiers concernes :

- rapports de revue ;
- docs d'architecture front ;
- backlog mis a jour.

Ne pas toucher :

- generateurs ;
- moteur DOCX/PDF/ZIP ;
- wording ;
- Streamlit production ou prototype.

Dependances :

- `FRONT-DATA-LAYER-001`;
- `FRONT-ROLE-MODEL-001`;
- `FRONT-ADDRESS-MODEL-001`;
- `FRONT-DOSSIER-FLOW-001`;
- `FRONT-DOCUMENT-STATUS-LAYER-001`.

Critères d'acceptation :

- revue des roles et adresses par un humain metier ;
- points ouverts qualifies en arbitrage interne, backlog documentaire ou futur produit ;
- decision explicite sur le demarrage de l'implementation UI ;
- confirmation que le registre V2.1 reste la base du rebuild.

## Tickets futurs possibles

Ces sujets ne doivent pas entrer dans les huit tickets ci-dessus sans decision explicite :

- mode Projet / filigrane ;
- SELAS medecin avec micro-holding ;
- calculs avances droits financiers / droits de vote ;
- API Pappers ;
- portail client ;
- pieces justificatives bloquantes pour l'ordre ;
- parametrage cabinet pour banque, fiscalite et signature electronique.
