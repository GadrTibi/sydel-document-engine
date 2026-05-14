# DAAT x SYDEL - SPEC TEXTE V1
## Famille `Statuts SEL d'exercice`

## 1. Objet

Formaliser la spec texte V1 de la famille `Statuts SEL d'exercice`, sans coder et sans modifier le wording juridique des sources.

Cette spec complete :

- `docs/delivery/lot_04_statuts_sel_exercice_spec_canonique_v1.md`

Elle prepare une future implementation deterministe en separant :

- le tronc commun SEL d'exercice ;
- les overlays `selarl_dentiste`, `selarl_medecin`, `selas_medecin` ;
- les blocs dynamiques d'associes ;
- les variantes grammaticales ;
- les elements manuels ;
- les points ouverts.

## 2. Sources texte analysees

Sources DOCX :

- `project/source_documents/lot_04/Modele statuts SELARL chirurgien dentiste sans communaute.docx`
- `project/source_documents/lot_04/Modèle statuts SELARL médecins.docx`
- `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`

Source de verite :

- `project/source_truth/Documents_a_generer_par_cas.docx`

Documents projet lus :

- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_preparation_v1.md`

## 3. Principe de spec texte

La famille n'est pas reduite a un modele unique.

Le texte futur devra etre construit comme suit :

1. selection d'un overlay obligatoire ;
2. generation du tronc fonctionnel commun ;
3. injection des clauses propres a l'overlay ;
4. repetition des blocs `associes[]` ;
5. controle des totaux capital / parts / actions ;
6. application des seules variantes grammaticales identifiees ;
7. blocage en cas de wording non valide.

Aucune correction de coquille, harmonisation de style ou modernisation juridique ne doit etre faite par le generateur sans validation explicite.

## 4. Structure texte commune attendue

### Bloc A - Couverture / en-tete

Fonction :

- afficher la denomination ;
- afficher la forme sociale ;
- afficher le capital ;
- afficher le siege ;
- afficher `STATUTS`.

Champs :

- `{societe.denomination}`
- `{societe.forme_sociale_complete}`
- `{societe.forme_sociale_abregee}`
- `{profession.libelle}`
- `{profession.libelle_pluriel}`
- `{capital.montant}`
- `{societe.siege.adresse_affichee}`

Regles :

- `selarl_dentiste` conserve le principe source `{forme_sociale_complete} de {profession_reglementee}` ;
- `selarl_medecin` conserve le libelle source `Societe d'exercice liberal a responsabilite limitee de medecin` tant qu'aucune variante n'est validee ;
- `selas_medecin` conserve le couple `{forme_sociale_complete}` / `{forme_sociale_abregee}`.

### Bloc B - Comparution des soussignes

Fonction :

- presenter les associes fondateurs ;
- rattacher chaque personne a sa profession, son etat civil, son adresse et son inscription ordinale si applicable.

Bloc source associe unique :

```text
{associe.civilite_affichage} {associe.prenom} {associe.nom}, ...
```

Regles de repetition :

- parcourir `associes[]` dans l'ordre fourni ;
- utiliser un bloc par associe ;
- ne pas coder en dur `[prenom] [nom]`, `[prenom_personne_2] [nom_personne_2]` ou `[PRENOM] [NOM]` ;
- si un wording pluriel d'introduction est necessaire, il doit etre valide avant code.

Variantes minimales :

| Condition | Effet texte |
|---|---|
| `len(associes[]) == 1` | utiliser la logique source `LE SOUSSIGNE` / associe unique |
| `len(associes[]) >= 2` | wording pluriel a valider avant code |
| `associe.genre == masculin` | `ne` |
| `associe.genre == feminin` | `nee` |

Point ouvert : les trois sources sont majoritairement associe unique ; le texte exact pour 2 a 6 associes doit etre valide.

### Bloc C - Forme et objet

Fonction :

- poser la forme juridique ;
- definir l'objet social ;
- rappeler les textes applicables ;
- encadrer l'exercice par des membres qualifies.

Regles :

- conserver les clauses propres a chaque overlay ;
- ne pas fusionner les references dentistes et medecins ;
- ne pas remplacer les references legales ou deontologiques sans validation.

Overlay :

- `selarl_dentiste` : profession parametree, ordonnance 2023-77, SELARL de professionnels de sante ;
- `selarl_medecin` : code de deontologie medicale et profession de medecin ;
- `selas_medecin` : SELAS, articles du code de la sante publique, ordonnance 2023-77, code de deontologie medicale.

### Bloc D - Denomination, siege, lieu d'exercice, duree

Fonction :

- afficher la denomination sociale ;
- fixer le siege ;
- fixer le ou les lieux d'exercice ;
- fixer la duree ;
- rappeler l'inscription ordinale comme condition de demarrage si la source le prevoit.

Regles par overlay :

| Overlay | Lieu d'exercice | Duree |
|---|---|---|
| `selarl_dentiste` | `{exercice.lieux[0].adresse_affichee}` | `{societe.duree}` |
| `selarl_medecin` | source adossee a `{societe.siege.adresse_affichee}` | `99 ans` source |
| `selas_medecin` | `{exercice.lieux[0]}` plus second lieu optionnel | `{societe.duree}` |

Condition second lieu SELAS :

- generer le second lieu seulement si `exercice.lieux[1]` est renseigne et valide ;
- si la source exige une ligne vide ou placeholder, bloquer en attendant validation plutot que produire un blanc.

### Bloc E - Apports

Fonction :

- decrire les apports en numeraire ;
- indiquer le depot des fonds ;
- rattacher les apports aux associes.

Regles :

- generer une ligne d'apport par associe si `len(associes[]) >= 2` et si le wording pluriel est valide ;
- pour V1, les sources associe unique ne suffisent pas a produire un wording multi-associes sans arbitrage ;
- le depot bancaire utilise `banque_depot.nom` et, selon overlay, `banque_depot.adresse_affichee`.

Champs :

- `{associe.apport_numeraire}`
- `{associe.apport_numeraire_lettres}`
- `{capital.montant}`
- `{capital.montant_lettres}`
- `{banque_depot.nom}`
- `{banque_depot.adresse_affichee}`

### Bloc F - Capital social

Fonction :

- fixer le capital ;
- afficher le nombre de parts ou actions ;
- afficher la valeur nominale ;
- attribuer les titres aux associes ;
- afficher le total.

Regles communes :

- `capital.type_titre == parts_sociales` pour les SELARL ;
- `capital.type_titre == actions` pour la SELAS ;
- generer une ligne d'attribution par associe ;
- controler que la somme des titres attribues egale `capital.nombre_titres_total` ;
- bloquer si le total est incoherent.

Bloc repetable conceptuel :

```text
{associe.civilite_affichage} {associe.prenom} {associe.nom} ... {associe.nombre_titres} {titre_label}
```

Variantes :

| Condition | Label |
|---|---|
| `capital.type_titre == parts_sociales` et `nombre == 1` | `part sociale` |
| `capital.type_titre == parts_sociales` et `nombre > 1` | `parts sociales` |
| `capital.type_titre == actions` et `nombre == 1` | `action` |
| `capital.type_titre == actions` et `nombre > 1` | `actions` |

Point ouvert : le wording exact des lignes multi-associes doit etre valide, notamment pour `selarl_medecin` ou la source contient une ligne `personne_2` incomplete.

### Bloc G - Qualite d'associe

Fonction :

- definir les associes professionnels ;
- definir les professionnels exterieurs ;
- definir anciens associes et ayants droit ;
- poser les restrictions de detention.

Regles :

- conserver un texte par overlay ;
- `selarl_dentiste` et `selarl_medecin` ne doivent pas etre deduits l'un de l'autre ;
- `selas_medecin` doit conserver la logique actions et droits de vote ;
- les professions interdites ou exclusions propres au texte medical ne sont pas mutualisables sans validation.

### Bloc H - Transmission des titres

Fonction :

- encadrer demembrement, cession, deces, communaute, nantissement ou mouvements d'actions.

Regles par forme :

- SELARL : utiliser `parts sociales`, `cession de parts`, `nantissement de parts sociales` ;
- SELAS : utiliser `actions`, `transmission des actions`, `virement des actions`, `registre des mouvements`.

Variante :

- le type de titre est pilote par `capital.type_titre` ;
- le wording juridique reste overlay, pas une simple substitution automatique de `parts` par `actions`.

### Bloc I - Clauses professionnelles specifiques

Fonction :

- porter les clauses d'exercice propres a la profession et a la forme sociale.

Clauses observees :

| Overlay | Clauses specifiques |
|---|---|
| `selarl_dentiste` | exclusion chirurgien-dentiste, sanctions disciplinaires, cessation d'activite, conciliation devant le president du Conseil departemental |
| `selarl_medecin` | non-concurrence, exclusion, cessation d'activite, placement hors convention, respect de la deontologie medicale, communication au Conseil departemental |
| `selas_medecin` | exclusion d'un associe, presidence, directeurs generaux, cessation d'activite, placement hors convention, respect de la deontologie medicale, sanctions disciplinaires |

Regle :

- ces clauses ne sont pas des blocs optionnels libres ;
- elles appartiennent a l'overlay source tant qu'une validation metier n'en decide pas autrement.

### Bloc J - Gouvernance

Fonction :

- definir l'organe de direction ;
- definir pouvoirs, responsabilite et remuneration ;
- definir decisions sociales et conventions.

Regles :

- `selarl_dentiste` : gerance ;
- `selarl_medecin` : gerance, pouvoirs du gerant, seuils d'autorisation ;
- `selas_medecin` : president, directeurs generaux, duree de mandat.

Champs SELAS :

- `{dirigeant.fonction}`
- `{dirigeant.duree_mandat}`
- `{dirigeant.civilite_affichage}`
- `{dirigeant.prenom}`
- `{dirigeant.nom}`
- `{dirigeant.adresse_personnelle.adresse_affichee}`

Point ouvert :

- la feminisation de `{dirigeant.fonction}` doit etre fournie par la donnee validee, pas calculee silencieusement.

### Bloc K - Exercice social, comptes, dissolution

Fonction :

- dates d'exercice ;
- premier exercice ;
- comptes sociaux ;
- affectation des resultats ;
- commissaire aux comptes ;
- dissolution / liquidation.

Regles :

- `date_cloture_exercice_1` est obligatoire si l'overlay contient une clause de premier exercice ;
- `debut_exercice` et `fin_exercice` sont obligatoires uniquement pour les sources qui les utilisent ;
- aucune harmonisation de numerotation d'articles entre overlays.

### Bloc L - Condition suspensive, pouvoirs, signature electronique

Fonction :

- conditionner le debut d'exercice a l'inscription ordinale ;
- donner pouvoirs pour formalites ;
- inclure ou non la convention de preuve / signature electronique ;
- cloturer par lieu et date de signature.

Regles :

- `selarl_dentiste` contient un bloc signature electronique ;
- `selarl_medecin` ne contient pas ce bloc dans la source analysee ;
- `selas_medecin` contient un bloc signature electronique ;
- ne pas ajouter ce bloc a `selarl_medecin` sans validation.

Champs :

- `{signature.lieu}`
- `{signature.date}`
- `{signature.nombre_exemplaires_lettres}`
- `{signature.prestataire_signature_electronique}`

### Bloc M - Signatures et annexes

Fonction :

- generer les signatures ;
- rappeler la mention manuscrite si la source l'exige ;
- lister les actes accomplis pour le compte de la societe en formation.

Regles :

- une ligne de signature par associe ;
- SELAS : la source contient une mention d'acceptation des fonctions de `{dirigeant.fonction}` ;
- SELARL dentiste et SELARL medecin : mention `Lu et approuve` observee ;
- annexe source minimale : ouverture d'un compte bancaire.

Point ouvert :

- si le dirigeant n'est pas associe, une signature dirigeant separee doit etre validee avant generation.

## 5. Overlays texte retenus

### 5.1 `selarl_dentiste`

Base texte :

- SELARL de chirurgien-dentiste ou profession reglementee parametree ;
- ordre departemental des chirurgiens-dentistes ;
- lieu d'exercice distinct ;
- clauses de parts sociales ;
- gerance ;
- sanctions disciplinaires ;
- signature electronique.

Variables obligatoires propres :

- `profession.libelle`
- `profession.libelle_pluriel`
- `ordre.departement_ou_ville`
- `associes[].numero_rpps`
- `exercice.lieux[0].adresse_affichee`
- `societe.duree`
- `signature.prestataire_signature_electronique`

Elements a ne pas deduire :

- ne pas remplacer automatiquement `chirurgien-dentiste` par `medecin` ;
- ne pas reprendre les clauses medicales de `selarl_medecin`.

### 5.2 `selarl_medecin`

Base texte :

- SELARL de medecin ;
- Conseil departemental de l'ordre ;
- numero national et RPPS ;
- lieu d'exercice au siege selon source ;
- clauses medicales detaillees ;
- gerance avec seuils d'autorisation ;
- communication au Conseil departemental.

Variables obligatoires propres :

- `ordre.departement_ou_ville`
- `associes[].numero_ordre`
- `associes[].numero_rpps`
- `banque_depot.adresse_affichee`
- `gerance.seuil_achat_materiel`
- `gerance.seuil_emprunt`
- `signature.nombre_exemplaires_lettres`

Elements a ne pas deduire :

- ne pas ajouter le bloc signature electronique d'un autre overlay ;
- ne pas figer `personne_2` comme role metier.

### 5.3 `selas_medecin`

Base texte :

- SELAS medecin ;
- actions ;
- president ;
- directeurs generaux ;
- lieux d'exercice potentiellement multiples ;
- signature electronique ;
- acceptation des fonctions.

Variables obligatoires propres :

- `societe.forme`
- `societe.forme_sociale_complete`
- `societe.forme_sociale_abregee`
- `capital.nombre_titres_total`
- `capital.nombre_titres_total_lettres`
- `capital.valeur_nominale_titre`
- `capital.valeur_nominale_titre_lettres`
- `dirigeant.fonction`
- `dirigeant.duree_mandat`
- `signature.prestataire_signature_electronique`

Elements a ne pas deduire :

- ne pas transformer la SELAS en SELARL par substitution de termes ;
- ne pas inclure la liste des souscripteurs dans les statuts sans spec distincte.

## 6. Variables texte par famille

### 6.1 Tronc commun

- `societe.denomination`
- `societe.forme`
- `societe.forme_sociale_complete`
- `societe.forme_sociale_abregee`
- `societe.siege.adresse_affichee`
- `capital.montant`
- `capital.montant_lettres`
- `capital.nombre_titres_total`
- `capital.valeur_nominale_titre`
- `capital.type_titre`
- `associes[]`
- `banque_depot.nom`
- `exercice.date_cloture_premier_exercice`
- `signature.lieu`
- `signature.date`

### 6.2 `associes[]`

Chaque associe doit pouvoir porter :

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
- `conjoint.civilite_affichage`
- `conjoint.prenom`
- `conjoint.nom`
- `numero_rpps`
- `numero_ordre`
- `apport_numeraire`
- `apport_numeraire_lettres`
- `nombre_titres`

## 7. Variantes grammaticales

### 7.1 Singulier / pluriel

| Zone | Singulier | Pluriel |
|---|---|---|
| comparution | source `LE SOUSSIGNE` | wording a valider |
| qualite | `associe unique` | `associes` |
| titres SELARL | `part sociale` | `parts sociales` |
| titres SELAS | `action` | `actions` |
| attribution capital | une ligne associe | repetition `associes[]` |
| signature | une signature | repetition `associes[]` |

Regle de blocage :

- si `len(associes[]) >= 2` et que le wording pluriel de l'overlay n'est pas valide, ne pas generer.

### 7.2 Masculin / feminin

| Zone | Variable pilote | Formes |
|---|---|---|
| naissance | `personne.genre` | `ne` / `nee` |
| qualite associe | `associe.genre` | `associe` / `associee`, si valide |
| dirigeant SELARL | `dirigeant.fonction` | texte fourni et valide |
| dirigeant SELAS | `dirigeant.fonction` | texte fourni et valide |

Regle :

- le generateur ne doit pas inventer une feminisation ;
- la forme affichee doit venir d'une variable ou d'une table validee dans une spec de code.

## 8. Elements manuels et hors texte genere

Restent hors automatisation initiale dans cette famille :

- formulaires `A REMPLIR A LA MAIN` cites par la source de verite ;
- derogation SEL BNC manuelle ;
- arbitrages de wording pluriel non presents dans les sources ;
- corrections typographiques ;
- decisions de suppression ou ajout de clauses ordinales ;
- liste des souscripteurs SELAS ;
- annexes autres que celles explicitement stabilisees ;
- second lieu d'exercice SELAS si condition non fournie ;
- signature d'un dirigeant non associe.

## 9. Criteres de recette documentaire avant code

Un ticket de code ne devra demarrer que si les points suivants sont valides :

- chaque overlay a une source texte unique ;
- `associes[]` est confirme comme structure d'entree ;
- les cas associe unique et pluralite d'associes ont un wording valide ;
- les tests couvriront au moins 1, 2 et 3 associes ;
- les tests couvriront masculin et feminin sur les personnes physiques ;
- les tests controleront les sommes d'apports et de titres ;
- la SELARL utilise des parts sociales ;
- la SELAS utilise des actions ;
- les clauses professionnelles restent celles de l'overlay choisi ;
- aucun placeholder source ne reste dans la sortie ;
- aucun fichier `A REMPLIR A LA MAIN` n'est genere comme statuts.

## 10. Points ouverts

1. Wording pluriel exact des blocs `LE SOUSSIGNE`, apports, capital et signatures pour 2 a 6 associes.
2. Traitement de la ligne `personne_2` dans le capital `selarl_medecin`.
3. Condition d'activation du second lieu d'exercice dans `selas_medecin`.
4. Statut de la liste des souscripteurs SELAS, hors statuts mais citee par la source de verite.
5. Feminisation des fonctions de dirigeant.
6. Signature du dirigeant si distinct des associes.
7. Correction ou conservation des coquilles et espacements sources.

## 11. Statut de la spec texte

`SPEC-STATUTS-SEL-001` est stabilise en specification texte V1.

Cette spec ne suffit pas a coder sans arbitrage des points ouverts ci-dessus, principalement sur la pluralite d'associes et le wording exact des lignes dynamiques.
