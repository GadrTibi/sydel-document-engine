# DAAT x SYDEL - SPEC CANONIQUE V1
## Famille `Statuts SEL d'exercice`

## 1. Objet

Formaliser la spec canonique de la famille documentaire `Statuts SEL d'exercice` avant tout codage.

Cette spec couvre uniquement les statuts sources suivants :

- `Modele statuts SELARL chirurgien dentiste sans communaute.docx`
- `Modèle statuts SELARL médecins.docx`
- `Statuts_SELAS_medecin.docx`

Elle ne code rien et ne valide aucun changement de wording juridique.

Objectif du ticket `SPEC-STATUTS-SEL-001` :

- stabiliser le tronc commun SEL d'exercice ;
- distinguer les overlays SELARL dentiste, SELARL medecin et SELAS medecin ;
- identifier les blocs associes dynamiques ;
- identifier les variantes singulier/pluriel et masculin/feminin ;
- isoler les elements manuels et les points ouverts avant toute implementation.

## 2. Sources lues

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`
- `project/source_documents/lot_04/Modele statuts SELARL chirurgien dentiste sans communaute.docx`
- `project/source_documents/lot_04/Modèle statuts SELARL médecins.docx`
- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`

ADR reperes :

- ADR-0001 : source de verite documentaire
- ADR-0002 : moteur par document canonique
- ADR-0003 : livraison par lots documentaires
- ADR-0004 : generation DOCX propre from-scratch
- ADR-0005 : mode Codex repo-first

## 3. Perimetre documentaire

La source de verite rattache les statuts SEL d'exercice aux chemins suivants :

| Chemin source de verite | Source statuts retenue | Overlay |
|---|---|---|
| SELARL / si chirurgien dentiste | `Modele statuts SELARL chirurgien dentiste sans communaute.docx` | `selarl_dentiste` |
| SELARL / si medecin | `Modèle statuts SELARL médecins.docx` | `selarl_medecin` |
| SELAS / statuts medecin | `Statuts_SELAS_medecin.docx` | `selas_medecin` |

Les documents associes au dossier mais hors statuts, comme la demande d'inscription a l'ordre, les lettres regime communautaire, les formulaires de derogation, les actes de cession ou les documents SCM, restent hors de cette spec. Ils sont seulement references comme blocs dossier conditionnels.

## 4. Decision de canonisation

La famille canonique est `statuts_sel_exercice`.

Elle est document-centree et non cas-centree :

- un tronc commun de statuts SEL d'exercice porte les blocs partages ;
- chaque source conserve un overlay explicite ;
- aucune fusion automatique de clauses n'est autorisee entre professions ou formes sociales ;
- les statuts sont generes from-scratch a partir d'une spec validee, pas par nettoyage de DOCX source ;
- les sources DOCX restent la base de comparaison, mais le moteur ne doit pas reprendre leurs placeholders locaux comme modele de donnees.

Les trois sorties documentaires restent distinctes tant qu'une validation metier n'a pas prouve qu'elles peuvent etre fusionnees :

- `statuts_selarl_chirurgien_dentiste`
- `statuts_selarl_medecin`
- `statuts_selas_medecin`

## 5. Tronc commun SEL d'exercice

Le tronc commun est fonctionnel, pas textuel. Il decrit les blocs presents dans la famille sans imposer une formulation unique lorsque les sources divergent.

### 5.1 Bloc A - En-tete societe

Contenu canonique :

- denomination sociale ;
- forme sociale complete ou abregee ;
- profession reglementee ou specialite ;
- capital social ;
- siege social ;
- titre `STATUTS`.

Variables principales :

- `societe.denomination`
- `societe.forme`
- `societe.forme_sociale_complete`
- `societe.forme_sociale_abregee`
- `societe.capital_social`
- `societe.capital_social_lettres`
- `societe.siege.adresse_affichee`
- `profession.libelle`
- `profession.libelle_pluriel`

### 5.2 Bloc B - Soussignes / comparution

Contenu canonique :

- identite du ou des associes fondateurs ;
- profession / titre professionnel ;
- naissance ;
- nationalite ;
- adresse personnelle ;
- situation matrimoniale, si la source l'utilise ;
- inscription ordinale ou RPPS, si la source l'utilise.

Ce bloc est dynamique : la source de verite impose une gestion de 1 a 6 associes dans les statuts, notamment dans l'en-tete apres `LE SOUSSIGNE`.

Role canonique :

- `associes[]`

Chaque associe contient a minima :

- `civilite_affichage`
- `genre`
- `prenom`
- `nom`
- `profession`
- `date_naissance`
- `ville_naissance`
- `departement_naissance`
- `nationalite`
- `adresse_personnelle.adresse_affichee`
- `situation_maritale`
- `regime_matrimonial`
- `conjoint` si applicable
- `numero_rpps` si applicable
- `numero_ordre` si applicable
- `ordre.departement_ou_ville` si applicable

### 5.3 Bloc C - Forme, objet, denomination, siege

Contenu canonique :

- article forme ;
- article objet social ;
- article denomination sociale ;
- article siege social ;
- article lieu d'exercice ;
- article duree.

Ces articles appartiennent au tronc commun mais leur texte depend fortement de l'overlay :

- SELARL dentiste : formulation SELARL de professionnels de sante avec `profession_reglementee` parametree ;
- SELARL medecin : formulation medicale plus specifique, avec references deontologiques medicales ;
- SELAS medecin : formulation actions / president et reference SELAS.

### 5.4 Bloc D - Apports et capital

Contenu canonique :

- apports en numeraire ;
- depot des fonds ;
- capital social ;
- nombre de parts ou actions ;
- valeur nominale ;
- attribution aux associes ;
- total du capital.

Ce bloc est dynamique et ne doit pas rester fige sur l'associe unique observe dans les sources.

Roles canoniques :

- `capital`
- `associes[]`
- `banque_depot`

Variables minimales :

- `capital.montant`
- `capital.montant_lettres`
- `capital.nombre_titres_total`
- `capital.valeur_nominale_titre`
- `capital.valeur_nominale_titre_lettres`
- `capital.type_titre` (`parts_sociales` ou `actions`)
- `banque_depot.nom`
- `banque_depot.adresse_affichee`
- `associes[].apport_numeraire`
- `associes[].apport_numeraire_lettres`
- `associes[].nombre_titres`

### 5.5 Bloc E - Qualite d'associe et repartition professionnelle

Contenu canonique :

- detentions reservees aux professionnels exercant ;
- professionnels exterieurs ;
- anciens associes professionnels ;
- ayants droit ;
- SPFPL ;
- interdictions ou restrictions propres a la profession.

Ce bloc est commun par fonction mais doit rester overlay par texte, car les clauses dentiste et medecin divergent.

### 5.6 Bloc F - Transmission, demembrement, cession, deces

Contenu canonique :

- transmission de parts ou d'actions ;
- demembrement ;
- cession ;
- transmission par deces ;
- liquidation de communaute ;
- nantissement.

Overlay forme sociale :

- SELARL : logique de parts sociales ;
- SELAS : logique d'actions, mouvements de compte, agrement et president.

### 5.7 Bloc G - Gouvernance

Contenu canonique :

- SELARL : gerance, pouvoirs du gerant, responsabilite, remuneration ;
- SELAS : presidence, eventuels directeurs generaux, pouvoirs du president ;
- decisions sociales ;
- conventions reglementees ;
- controle des associes.

Variables minimales :

- `dirigeant.fonction`
- `dirigeant.civilite_affichage`
- `dirigeant.genre`
- `dirigeant.prenom`
- `dirigeant.nom`
- `dirigeant.adresse_personnelle.adresse_affichee`
- `dirigeant.duree_mandat`
- `dirigeant.ref_associe_index` optionnel

### 5.8 Bloc H - Vie sociale, comptes, dissolution, ordre

Contenu canonique :

- exercice social ;
- premier exercice ;
- comptes annuels ;
- affectation des resultats ;
- commissaire aux comptes ;
- dissolution / liquidation ;
- contestations ou conciliation ;
- communication a l'ordre ;
- condition suspensive d'inscription ordinale.

Variables minimales :

- `exercice.debut`
- `exercice.fin`
- `exercice.date_cloture_premier_exercice`
- `ordre.professionnel`
- `ordre.departement_ou_ville`

### 5.9 Bloc I - Signature et annexes

Contenu canonique :

- lieu et date de signature ;
- nombre d'exemplaires si la source le prevoit ;
- signatures dynamiques des associes ;
- mention manuscrite ou acceptation des fonctions si la source le prevoit ;
- annexe des actes accomplis pour le compte de la societe en formation.

Variables minimales :

- `signature.lieu`
- `signature.date`
- `signature.nombre_exemplaires_lettres`
- `associes[]`
- `prestataire_signature_electronique` si la source contient le bloc de signature electronique

## 6. Overlays retenus

### 6.1 Overlay `selarl_dentiste`

Source : `Modele statuts SELARL chirurgien dentiste sans communaute.docx`.

Caracteristiques observees :

- forme SELARL ;
- profession parametree par `profession_reglementee` et `profession_reglementee_pluriel` ;
- ordre departemental des chirurgiens-dentistes ;
- numero RPPS ;
- lieu d'exercice distinct de l'adresse de siege via `adresse_lieu_exercice` ;
- duree de societe parametree ;
- depot bancaire sans adresse de banque dans le placeholder observe ;
- parts sociales ;
- clauses d'apporteurs communs en biens et PACS ;
- gerance ;
- sanctions disciplinaires ;
- convention sur la preuve et signature electronique.

Variables sources notables propres ou sensibles :

- `[ordre_departemental]`
- `[adresse_lieu_exercice]`
- `[duree_societe]`
- `[montant_apport]`
- `[montant_apport_lettres]`
- `[regime_matrimonial]`
- `[civilite_conjoint]`, `[prenom_conjoint]`, `[nom_conjoint]`
- `[prestataire_signature_electronique]`

### 6.2 Overlay `selarl_medecin`

Source : `Modèle statuts SELARL médecins.docx`.

Caracteristiques observees :

- forme SELARL de medecin ;
- objet social medical a titre exclusif ;
- references au code de deontologie medicale ;
- inscription au Conseil departemental de `[ville_ordre]` avec numero national `[numero_ordre]` et RPPS ;
- lieu d'exercice actuellement adosse a `[adresse_siege]` dans la source ;
- duree de 99 ans fixee dans le texte source ;
- depot bancaire avec nom et adresse de banque ;
- parts sociales ;
- clauses medicales specifiques : non concurrence, exclusion, cessation d'activite, placement hors convention ;
- seuils d'autorisation de gerance pour achat materiel et emprunt ;
- communication au Conseil departemental ;
- signature en plusieurs exemplaires.

Variables sources notables propres ou sensibles :

- `[ville_ordre]`
- `[numero_ordre]`
- `[adresse_banque]`
- `[seuil_achat_materiel]`
- `[seuil_emprunt_gerance]`
- `[nombre_exemplaires_lettres]`
- `[prenom_signataire]`, `[nom_signataire]`
- `[civilite_personne_2]`, `[prenom_personne_2]`, `[nom_personne_2]`

Point d'attention : les placeholders `personne_2` apparaissent dans l'article capital, mais ne doivent pas devenir la structure canonique. Ils sont a remapper vers `associes[]`.

### 6.3 Overlay `selas_medecin`

Source : `Statuts_SELAS_medecin.docx`.

Caracteristiques observees :

- forme SELAS ;
- profession medicale parametree ;
- actions, non parts sociales ;
- lieu d'exercice avec deux emplacements possibles dans la source ;
- apport en numeraire par personne 1 ;
- president et eventuels directeurs generaux ;
- duree de mandat dirigeant ;
- clauses actions : forme des actions, transmission, mouvements en compte ;
- signature electronique ;
- acceptation des fonctions de dirigeant.

Variables sources notables propres ou sensibles :

- `[forme_sociale]`
- `[forme_sociale_abregee]`
- `[nb_actions]`
- `[nb_actions_lettres]`
- `[valeur_nominale_action]`
- `[valeur_nominale_action_lettres]`
- `[apport_personne_1]`
- `[apport_lettres_personne_1]`
- `[adresse_lieu_exercice]`
- `[nom_lieu_exercice_2]`, `[adresse_lieu_exercice_2]`
- `[fonction_dirigeant]`
- `[duree_mandat_dirigeant]`
- `[qualite_associe]`
- `[titre_professionnel]`
- `[qualification_principale]`

Point d'attention : la source de verite mentionne aussi une liste des souscripteurs pour SELAS. Cette liste n'est pas incluse dans cette spec de statuts et devra rester un document ou bloc separe.

## 7. Blocs associes dynamiques

La source de verite indique explicitement que les statuts peuvent concerner 1 a 6 associes. Les zones concernees sont :

- l'en-tete apres `LE SOUSSIGNE` ;
- la liste des associes ;
- les articles d'apports et de capital, en moyenne articles 7 et 8 ;
- la partie signature finale.

Decision canonique :

- `associes[]` est obligatoire et repetable ;
- le moteur ne doit pas coder une limite structurelle a 1 ou 2 associes ;
- les placeholders sources `personne_1`, `personne_2`, `[prenom] [nom]` associe unique, ou `[PRENOM] [NOM]` sont seulement des aliases locaux ;
- la repartition des titres doit etre calculee ou controlee contre `capital.nombre_titres_total` ;
- la signature finale genere une ligne par associe, sauf decision metier contraire.

## 8. Variantes grammaticales

La source de verite limite les variantes connues a :

- singulier / pluriel ;
- masculin / feminin.

### 8.1 Singulier / pluriel

A gerer au minimum :

- `LE SOUSSIGNE` / formulation plurielle equivalente ;
- `associe unique` / `associes` ;
- `part` / `parts` ;
- `action` / `actions` ;
- `professionnel exercant` / `professionnels exercant` ;
- lignes de total de capital ;
- signatures finales.

### 8.2 Masculin / feminin

A gerer au minimum :

- `ne` / `nee` pour les personnes physiques ;
- `associe` / `associee` si la source impose une qualification genre ;
- `gerant` / `gerante` ou `president` / `presidente` uniquement si le wording source ou une validation metier l'autorise ;
- civilite d'affichage separee du genre grammatical.

Decision canonique :

- `civilite_affichage` ne suffit pas a deduire le genre ;
- `genre` reste une variable explicite ;
- aucune feminisation ou correction typographique ne doit etre introduite sans validation de wording.

## 9. Elements manuels ou hors automatisation initiale

Restent manuels ou a decision explicite avant automatisation :

- formulaires marques `A REMPLIR A LA MAIN` dans la source de verite, notamment site distinct et derogation SEL BNC ;
- arbitrage du nombre exact d'associes lorsque la source fournie est associe unique mais le dossier contient plusieurs associes ;
- ajustements de clauses ordinales ou deontologiques ;
- correction des coquilles apparentes des sources ;
- choix d'une formulation plurielle exacte pour `LE SOUSSIGNE` ;
- signature du dirigeant lorsqu'il n'est pas associe ;
- presence d'un second lieu d'exercice SELAS ;
- liste des souscripteurs SELAS, qui n'est pas le document statuts lui-meme ;
- annexes detaillees au-dela de la liste source `Ouverture d'un compte bancaire`.

## 10. Mapping canonique minimal

| Source locale | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | tronc commun |
| `[forme_sociale_complete]` | `societe.forme_sociale_complete` | overlay selon forme |
| `[forme_sociale]` | `societe.forme` | surtout SELAS |
| `[forme_sociale_abregee]` | `societe.forme_sociale_abregee` | surtout SELAS |
| `[capital_social]` | `capital.montant` | montant chiffre |
| `[capital_lettres]` | `capital.montant_lettres` | montant lettres |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | champ affiche source |
| `[adresse_lieu_exercice]` | `exercice.lieux[0].adresse_affichee` | si distinct du siege |
| `[nom_lieu_exercice_2]` | `exercice.lieux[1].nom` | SELAS, conditionnel |
| `[adresse_lieu_exercice_2]` | `exercice.lieux[1].adresse_affichee` | SELAS, conditionnel |
| `[civilite]` | `associes[0].civilite_affichage` | alias source associe unique |
| `[prenom]` | `associes[0].prenom` | alias source associe unique |
| `[nom]` | `associes[0].nom` | alias source associe unique |
| `[date_naissance]` | `associes[0].date_naissance` | alias source associe unique |
| `[ville_naissance]` | `associes[0].ville_naissance` | alias source associe unique |
| `[departement_naissance]` | `associes[0].departement_naissance` | alias source associe unique |
| `[nationalite]` | `associes[0].nationalite` | alias source associe unique |
| `[adresse_personnelle]` | `associes[0].adresse_personnelle.adresse_affichee` | alias source associe unique |
| `[profession]` | `associes[0].profession` | affichage source |
| `[profession_reglementee]` | `profession.libelle` | texte metier |
| `[profession_reglementee_pluriel]` | `profession.libelle_pluriel` | texte metier |
| `[numero_rpps]` | `associes[0].numero_rpps` | alias source associe unique |
| `[numero_ordre]` | `associes[0].numero_ordre` | SELARL medecin |
| `[ordre_departemental]` | `ordre.departement_ou_ville` | SELARL dentiste |
| `[ville_ordre]` | `ordre.departement_ou_ville` | SELARL medecin |
| `[nb_parts_total]` | `capital.nombre_titres_total` | SELARL |
| `[valeur_nominale_part]` | `capital.valeur_nominale_titre` | SELARL |
| `[nb_actions]` | `capital.nombre_titres_total` | SELAS |
| `[valeur_nominale_action]` | `capital.valeur_nominale_titre` | SELAS |
| `[nom_banque]` | `banque_depot.nom` | depot des fonds |
| `[adresse_banque]` | `banque_depot.adresse_affichee` | selon source |
| `[date_cloture_exercice_1]` | `exercice.date_cloture_premier_exercice` | tronc commun |
| `[debut_exercice]` | `exercice.debut` | selon source |
| `[fin_exercice]` | `exercice.fin` | selon source |
| `[fonction_dirigeant]` | `dirigeant.fonction` | SELAS surtout |
| `[duree_mandat_dirigeant]` | `dirigeant.duree_mandat` | SELAS |
| `[lieu_signature]` | `signature.lieu` | tronc commun |
| `[date_signature]` | `signature.date` | tronc commun |
| `[prestataire_signature_electronique]` | `signature.prestataire_signature_electronique` | si bloc present |

## 11. Conditions de generation a specifier avant code

Avant implementation, il faudra une validation explicite sur :

- le nombre d'associes supporte en recette ;
- la representation exacte des apports par associe ;
- la representation exacte des parts/actions par associe ;
- le controle `somme associes[].nombre_titres == capital.nombre_titres_total` ;
- la presence ou non d'un conjoint dans le bloc comparution ;
- la presence ou non d'un second lieu d'exercice ;
- la correspondance entre dirigeant et associe ;
- les variantes de signature selon associe unique ou pluralite ;
- le traitement des clauses source divergentes sans reecriture juridique.

## 12. Points ouverts

1. Les trois sources sont principalement redigees en associe unique ; la source de verite impose pourtant 1 a 6 associes pour les statuts. Il faut valider le wording des blocs pluriels avant code.
2. `SELARL medecin` contient des placeholders `personne_2` dans l'article capital sans logique complete d'associes multiples. Le remapping vers `associes[]` doit etre arbitre.
3. `SELAS medecin` contient un second lieu d'exercice optionnel dans le corps du texte ; sa condition d'activation doit etre confirmee.
4. La liste des souscripteurs concernant notamment SELAS est hors statuts et devra faire l'objet d'une spec distincte.
5. Les clauses professionnelles dentiste et medecin ne doivent pas etre fusionnees sans validation juridique.
6. Les corrections typographiques apparentes des sources ne sont pas autorisees dans ce ticket.
7. La feminisation des fonctions dirigeantes doit rester pilotee par une variable de texte validee, pas par une correction automatique.

## 13. Statut

Cette spec canonique V1 stabilise le cadre de la famille `Statuts SEL d'exercice`.

Elle autorise l'ouverture d'une revue metier ou d'une spec de code ulterieure, mais pas encore le codage du generateur.
