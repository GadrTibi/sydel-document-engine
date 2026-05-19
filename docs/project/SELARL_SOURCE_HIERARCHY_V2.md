# Hierarchie des sources SELARL V2

Tickets source : `SELARL-NOTEBOOKLM-RECONCILIATION-001`, corrige par `SELARL-PLAN-CORRECTION-001`.

## Objet

Ce document remplace le cadrage implicite SELARL fonde uniquement sur `Documents a generer par cas` par une hierarchie explicite de sources. Il ne modifie pas l'architecture moteur, les generateurs, l'UI ni les formulations juridiques.

La correction `SELARL-PLAN-CORRECTION-001` ajoute un niveau superieur : les arbitrages explicites de l'associe priment sur NotebookLM lorsque NotebookLM propose une piste produit non encore validee.

## Hierarchie retenue

### 1. Arbitrages explicites de l'associe

Ces arbitrages sont prioritaires pour la planification SELARL :

- l'ecran personne s'appelle `Fiche Client` ;
- le terme pivot est `Praticien` ;
- l'ancien libelle personne est banni des labels visibles et des tickets futurs ;
- une logique `Dossier unipersonnel` doit etre ajoutee ;
- le mandataire ne doit pas devenir un sujet UX majeur s'il n'y a pas de variables ou documents qui l'exigent ;
- aucun mode Projet ni filigrane n'est a implementer en V1 ;
- aucune couche produit lourde de statut documentaire ne doit etre ajoutee si les variables, conditions et statuts existants suffisent ;
- le perimetre SELARL reste inchange.

Ces arbitrages ne modifient pas le wording juridique des actes. Toute evolution du texte documentaire reste soumise au pipeline documentaire habituel.

### 2. NotebookLM / transcriptions client

Fichier lu : `project/source_truth/notebooklm_selarl_10_prompts_v1.md`.

NotebookLM apporte la source metier vivante :

- vocabulaire attendu par les juristes ;
- ordre naturel du processus de saisie ;
- roles metier et juridiques a ne pas confondre ;
- regles de reutilisation des donnees ;
- attentes UX et points de friction du parcours SELARL ;
- points de blocage lies a l'Ordre, aux pieces jointes, a la banque et aux cas complexes.

NotebookLM ne doit pas decider seul :

- du wording juridique dans les actes ;
- de la liste finale des documents a generer ;
- des variables exactes extraites des modeles DOCX ;
- d'une nouvelle couche produit non arbitree, notamment mode Projet, filigrane ou statut documentaire lourd ;
- du statut technique d'un generateur deja implemente.

### 3. Documents a generer par cas V3

Fichier lu : `project/source_truth/Documents_a_generer_par_cas_V3.docx`.

V3 apporte la source documentaire :

- documents attendus par cas SELARL ;
- conditions documentaires ;
- noms de fichiers source ;
- variables par document ;
- questions fonctionnelles nouvelles ajoutees par rapport a V2.

Constat important : V3 conserve le contenu V2 puis ajoute une couche de questions par document. Elle ameliore donc l'exploitation formulaire, mais ne regle pas seule les sujets UX, roles et ordre de saisie.

V3 ne doit pas decider seul :

- du libelle visible cote juriste si NotebookLM et l'associe donnent un vocabulaire plus metier ;
- de la reutilisation automatique entre personnes et roles ;
- d'une qualification produit additionnelle des documents non validee par l'associe ;
- de la necessite d'une revue humaine ou de pieces justificatives au-dela des conditions documentees.

### 4. Templates DOCX et registre moteur

Sources techniques :

- templates DOCX dans `project/source_documents/` ;
- registre moteur et catalogue de documents ;
- generateurs existants `DOC-001` a `DOC-043`.

Ils apportent :

- faisabilite technique de generation ;
- variables reellement consommees par les generateurs ;
- noms de sortie ;
- limitations deja codees ;
- statut technique d'un document : generateur present, absent, manuel, incomplet.

Ils ne doivent pas decider seuls :

- de l'ordre de saisie ;
- du vocabulaire affiche dans l'Assistant metier ;
- de la source metier du dossier ;
- de la qualification juridique d'un document comme definitif.

### 5. Code existant

Fichiers concernes par l'audit :

- `src/sydel_doc_engine/domain/case_catalog.py` ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- `src/sydel_doc_engine/app/streamlit_app.py`.

Le code existant est une implementation a corriger. Il sert a mesurer les ecarts, pas a trancher la verite metier.

Le code ne doit pas decider seul :

- qu'un libelle est acceptable parce qu'il est deja teste ;
- qu'un document est juridiquement definitif parce qu'il est techniquement generable ;
- qu'un role peut etre derive par defaut sans validation metier ;
- qu'un ordre d'ecran est correct parce qu'il est deja branche ;
- qu'une adresse peut etre copiee sans case explicite.

## Regles d'arbitrage

| Situation | Source prioritaire | Regle |
|---|---|---|
| Arbitrage explicite de l'associe | Associe | Appliquer l'arbitrage, meme si NotebookLM propose une option plus large. |
| Vocabulaire visible, ordre des ecrans, roles et UX non arbitres | NotebookLM | Appliquer le vocabulaire client sauf contradiction avec l'associe ou avec le juridique. |
| Liste documentaire, variables, conditions par cas | V3 | Utiliser V3 comme source documentaire principale. |
| Difference V2 vs V3 | V3 | V3 remplace V2 pour le cadrage SELARL, sauf anomalie documentee. |
| Document generable mais signale complexe par NotebookLM | V3 + arbitrage associe | Garder le document dans le catalogue ; ne pas ajouter de couche produit lourde sans validation. |
| Document manuel dans V3 | V3 | Ne pas envoyer a la generation sans arbitrage explicite. |
| Template/generateur existant contredit V3 | V3 + decision metier | Ne pas corriger en silence ; documenter l'ecart et ouvrir un ticket. |
| NotebookLM contredit le wording juridique d'un template | Template + revue juriste | Ne jamais modifier le wording juridique sans validation. |
| Ambiguite de role ou d'adresse | Associe + NotebookLM | Ne pas deriver automatiquement ; demander une case explicite ou bloquer. |

## Consequences immediates

- L'ecran personne cible est `Fiche Client`.
- Le terme global visible est `Praticien`, complete par le role exact quand il existe : `Gerant`, `Associe`, `Signataire`.
- Le libelle banni ne doit plus apparaitre dans les labels visibles ni dans les tickets futurs.
- L'ordre cible devient : qualification, Fiche Client / Praticien, Fiche Societe, Capital & Associes, Contexte & scenarios metier, Documents & generation.
- La logique `Dossier unipersonnel` devient le pivot de reutilisation : Praticien = associe unique = gerant = signataire lorsque l'option est active.
- `Mandataire = signataire` ne doit plus etre une hypothese par defaut ; le mandataire reste traite seulement si les variables ou documents l'exigent.
- Les reutilisations d'adresse restent explicites : siege social, lieu d'exercice, cabinet et domiciliation ne sont pas assimiles automatiquement.
- Aucun mode Projet ni filigrane n'est retenu pour la V1.
- Aucun ticket de statut documentaire lourd ne doit etre ouvert si le catalogue existant, les conditions et les reserves suffisent.
- Le smoke SELARL doit attendre un realignement minimal du wording, de l'ordre, des regles de reutilisation et de l'UI.
