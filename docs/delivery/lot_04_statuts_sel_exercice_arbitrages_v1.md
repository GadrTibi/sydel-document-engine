# DAAT x SYDEL - ARBITRAGES V1
## Famille `Statuts SEL d'exercice`

Ticket : `ARBITRAGE-STATUTS-SEL-001`.
Date : 2026-05-14.

## 1. Objet

Fermer les points ouverts identifies dans :

- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`

Ce document ne code rien, ne modifie aucun wording juridique source et ne remplace pas une validation juridique fine.

## 2. Sources lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `project/source_documents/lot_04/Modele statuts SELARL chirurgien dentiste sans communaute.docx`
- `project/source_documents/lot_04/Modele statuts SELARL medecins.docx`
- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`

ADR reperes :

- ADR-0001 : source de verite documentaire
- ADR-0002 : moteur par document canonique
- ADR-0003 : livraison par lots documentaires
- ADR-0005 : mode Codex repo-first

## 3. Synthese des arbitrages

| Point | Classement | Decision V1 |
|---|---|---|
| Wording pluriel 2 a 6 associes | Manuel V1 | Ne pas automatiser les statuts multi-associes tant que le wording pluriel exact n'est pas valide. |
| Ligne `personne_2` SELARL medecin | Tranche | Ne pas creer de role `personne_2`; la ligne est un alias source incomplet, rattache uniquement au futur traitement `associes[]`. |
| Second lieu SELAS | Tranche | Le second lieu est optionnel ; il est rendu seulement si nom et adresse du second lieu sont fournis ensemble. |
| Liste des souscripteurs SELAS | Tranche | La liste des souscripteurs reste un document ou bloc separe, hors statuts SEL d'exercice V1. |
| Feminisation dirigeant | Tranche | La fonction dirigeante affichee vient d'une donnee validee ; aucune feminisation automatique. |
| Signature dirigeant non associe | Manuel V1 | Si le dirigeant n'est pas deja signe comme associe, la signature dirigeant separee reste manuelle. |
| Conservation/correction des coquilles source | Tranche | Conservation stricte par defaut ; toute correction exige une note de validation explicite. |

## 4. Points tranches

### 4.1 Ligne `personne_2` SELARL medecin

Classement : tranche.

Constat source :

- la source `SELARL medecin` contient une ligne isolee dans l'article capital avec les placeholders `[civilite_personne_2]`, `[prenom_personne_2]`, `[nom_personne_2]` ;
- cette ligne coexiste avec une phrase qui attribue le capital en totalite a l'associe unique ;
- elle ne fournit pas a elle seule un wording complet d'apports, de comparution, de signature ou de gouvernance pour un deuxieme associe.

Decision V1 :

- `personne_2` n'est pas une structure canonique ;
- aucun modele de donnees `personne_2` ne doit etre introduit ;
- si une future version automatise les pluralites, ces champs sources seront remappes vers `associes[1]` uniquement dans le cadre d'un bloc `associes[]` complet et valide ;
- en V1, cette ligne ne suffit pas a autoriser une generation multi-associes.

### 4.2 Second lieu SELAS

Classement : tranche.

Constat source :

- la source `SELAS medecin` contient une ligne principale `[adresse_lieu_exercice]` ;
- elle contient aussi une ligne secondaire `[nom_lieu_exercice_2], [adresse_lieu_exercice_2]`.

Decision V1 :

- `exercice.lieux[0].adresse_affichee` est obligatoire pour l'overlay `selas_medecin` ;
- `exercice.lieux[1]` est optionnel ;
- la ligne du second lieu est rendue uniquement si `exercice.lieux[1].nom` et `exercice.lieux[1].adresse_affichee` sont tous deux fournis ;
- si un seul des deux champs est fourni, la generation doit bloquer plutot que produire une ligne incomplete ;
- si aucun second lieu n'est fourni, la ligne secondaire est omise sans inserer de blanc.

### 4.3 Liste des souscripteurs SELAS

Classement : tranche.

Decision V1 :

- la liste des souscripteurs SELAS n'est pas incluse dans les statuts SEL d'exercice ;
- elle doit rester hors generateur `statuts_sel_exercice` ;
- elle devra faire l'objet d'une specification separee si elle entre dans le perimetre d'automatisation ;
- aucun bloc de liste des souscripteurs ne doit etre invente dans les statuts pour compenser son absence.

### 4.4 Feminisation dirigeant

Classement : tranche.

Decision V1 :

- le generateur ne deduit pas `gerante`, `presidente` ou toute autre forme feminine depuis `genre` ;
- la fonction affichee doit venir d'un champ de donnees deja valide, par exemple `dirigeant.fonction` ;
- les tests de code devront verifier que la valeur fournie est reprise telle quelle, sans correction automatique ;
- toute table de feminisation automatique restera hors V1 tant qu'elle n'est pas validee juridiquement.

### 4.5 Conservation/correction des coquilles source

Classement : tranche.

Decision V1 :

- les coquilles, espacements, ponctuations et graphies apparentes des sources sont conserves par defaut ;
- aucune correction typographique ne doit etre glissee dans le code sous pretexte de normalisation ;
- une correction n'est autorisee que si elle est documentee dans une note de validation explicite ;
- les differences de casse entre placeholders sources, par exemple `[prenom] [nom]` et `[PRENOM] [NOM]`, peuvent etre remappees techniquement vers les variables canoniques sans modifier le wording juridique rendu.

## 5. Points manuels V1

### 5.1 Wording pluriel 2 a 6 associes

Classement : manuel V1.

Constat source :

- les trois sources lues sont principalement redigees pour un associe unique ;
- les blocs sensibles concernes sont la comparution, les apports, le capital, les mentions `associe unique`, les signatures et certaines reprises de pronoms ;
- la source de verite indique un besoin 1 a 6 associes, mais ne fournit pas le wording juridique complet des pluralites.

Decision V1 :

- l'automatisation initiale des statuts SEL d'exercice est limitee a l'associe unique ;
- les dossiers contenant 2 a 6 associes restent en traitement manuel V1 pour les statuts ;
- le code futur doit bloquer explicitement `len(associes[]) >= 2` avec un message de decision requise, sauf si un ticket ulterieur valide le wording pluriel ;
- la structure canonique `associes[]` reste la bonne structure d'entree, meme si la generation multi-associes n'est pas automatisee en V1.

### 5.2 Signature dirigeant non associe

Classement : manuel V1.

Constat source :

- la SELAS contient une mention d'acceptation des fonctions de `[fonction_dirigeant]` ;
- les sources ne stabilisent pas une signature separee lorsque le dirigeant n'est pas deja signataire comme associe ;
- les SELARL restent construites autour de la signature associee aux statuts et a la mention `Lu et approuve`.

Decision V1 :

- si le dirigeant est le meme signataire que l'associe unique, la signature source peut rester dans le flux statuts ;
- si le dirigeant n'est pas associe, la signature dirigeant separee reste manuelle en V1 ;
- le code futur doit bloquer ce cas ou le router explicitement hors automatisation, au lieu d'inventer un bloc de signature.

## 6. Points bloquants restants

Aucun bloquant ne reste pour ouvrir un ticket de code limite aux conditions V1 suivantes :

- un seul associe ;
- pas de signature automatique de dirigeant non associe ;
- second lieu SELAS absent ou completement renseigne ;
- fonction dirigeante fournie sous forme de texte valide ;
- conservation stricte du wording source.

Les cas suivants restent bloquants pour une generation automatique :

- `len(associes[]) >= 2` ;
- `selas_medecin` avec second lieu partiellement renseigne ;
- dirigeant non associe avec signature separee attendue ;
- demande de correction de coquille sans note de validation.

## 7. Prochaine etape recommandee

Ouvrir un ticket de code limite a l'automatisation V1 associe unique des statuts SEL d'exercice, avec blocages explicites pour les cas listes ci-dessus.
