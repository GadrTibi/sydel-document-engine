# Schéma de formulaire UI V1

## Objet

Ce document formalise le schéma de formulaire UI V1 pour une interface de génération sûre.

Il définit :
- les packs de champs affichables ;
- les champs requis et optionnels ;
- les règles de validation par étape ;
- les blocs répétables, notamment `associes[]` ;
- le comportement des cartes repliables ;
- les conditions de blocage et de déblocage du bouton suivant.

Ce document ne modifie pas la source de vérité juridique. Il s'appuie sur :
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` ;
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.

Les documents `docs/project/19_UI_FLOW_V1.md` et `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md` n'existent pas au moment de cette V1 ; les règles ci-dessous restent donc limitées aux référentiels disponibles.

## Principes UI non négociables

1. L'UI affiche uniquement les champs utiles à la branche active.
2. Un champ masqué n'est jamais bloquant pour l'étape active.
3. Le bouton suivant est bloqué si un champ requis visible de l'étape active est invalide.
4. La validation est progressive : chaque étape valide son propre périmètre, sans exiger la complétion anticipée des étapes suivantes.
5. Les champs répétables sont gérés par carte, avec ajout explicite par bouton.
6. Les valeurs saisies dans une branche inactive peuvent être conservées en brouillon, mais elles ne doivent pas être exportées ni validées tant que la branche n'est pas active.
7. Aucun wording juridique n'est réécrit depuis l'UI.

## Etapes de formulaire V1

| Etape | Objet | Packs principaux | Blocage du bouton suivant |
|---|---|---|---|
| 1 | Orientation dossier | `dossier` | structure/famille/options minimales invalides |
| 2 | Société | `societe`, `societe.siege` | société ou siège requis incomplets |
| 3 | Personnes | `signataire`, `associes[]`, `dirigeant_nomine` | personne requise incomplète, associé invalide, dirigeant requis absent |
| 4 | Branches documentaires | `domiciliation`, `bien_immobilier`, `emprunt`, blocs conditionnels | bloc actif incomplet |
| 5 | Signature et contrôle | `signature` | signature requise incomplète ou incohérence transverse bloquante |

## Pack `dossier`

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `dossier.structure` | requis | sélection dans les structures supportées par le moteur |
| `dossier.famille` | requis | sélection cohérente avec la structure |
| `dossier.options.regime_communautaire` | optionnel | booléen, affiche les blocs régime communautaire si actif |
| `dossier.options.site_distinct` | optionnel | booléen, affiche les blocs site distinct si actif |
| `dossier.options.derogation` | optionnel | booléen, affiche les blocs dérogation si actif |
| `dossier.options.scm` | optionnel | booléen, actif uniquement pour les branches SCM |
| `dossier.options.cession` | optionnel | booléen, affiche les blocs cession si actif |
| `dossier.options.apport` | optionnel | booléen, affiche les blocs apport si actif |
| `dossier.options.associe_unique` | optionnel | booléen, contraint `associes[]` à un seul associé |

### Validation

- `dossier.structure` et `dossier.famille` doivent être renseignés avant passage à l'étape 2.
- Les options incompatibles entre elles doivent être bloquées par la branche active, pas par une règle globale inventée.
- Si `dossier.options.associe_unique = true`, l'UI masque ou désactive le bouton ajouter un associé dès que le premier associé existe.
- Si une option est désactivée, les champs de son bloc conditionnel disparaissent et ne bloquent plus l'étape.

## Pack `societe`

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `societe.forme_juridique` ou `societe.forme` | requis si société requise | utiliser le nom canonique disponible dans la branche ; ne pas créer de variante UI |
| `societe.denomination` | requis si société requise | texte non vide |
| `societe.capital_social` | requis si document actif l'utilise | montant positif |
| `societe.ville_rcs` ou `societe.rcs_ville` | requis si document actif l'utilise | texte non vide |
| `societe.nb_parts_total` ou `capital.nb_parts_total` | requis si répartition du capital active | entier strictement positif |
| `societe.valeur_nominale_part` ou `capital.valeur_nominale_part` | requis si répartition du capital active | montant positif |

### Validation

- Les montants doivent être strictement positifs.
- Les nombres de parts doivent être des entiers strictement positifs.
- Si `nb_parts_total`, `valeur_nominale_part` et `capital_social` sont tous visibles, l'UI doit signaler toute incohérence arithmétique.
- L'incohérence `nb_parts_total x valeur_nominale_part != capital_social` est bloquante uniquement lorsque la branche active exige la répartition du capital.

## Pack `societe.siege`

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `societe.siege.num_voie` | requis si siège requis | texte non vide |
| `societe.siege.voie` | requis si siège requis | texte non vide |
| `societe.siege.ville` | requis si siège requis | texte non vide |
| `societe.siege.cp` | requis si siège requis | code postal français à 5 chiffres |

### Validation

- Le siège est requis dès qu'un document actif consomme une adresse de siège.
- Le code postal doit comporter 5 chiffres.
- L'adresse de siège ne remplace pas `domiciliation.adresse_affichee` pour DOC-002 ; la domiciliation reste un champ dédié.

## Pack `signataire`

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `signataire.genre` | requis si accords requis | valeur contrôlée : `masculin` ou `feminin` |
| `signataire.civilite_affichage` | requis si signataire requis | texte ou choix contrôlé |
| `signataire.prenom` | requis si signataire requis | texte non vide |
| `signataire.nom` | requis si signataire requis | texte non vide |
| `signataire.date_naissance` | requis pour DOC-001 et documents qui l'utilisent | date valide |
| `signataire.ville_naissance` | requis si document actif l'utilise | texte non vide |
| `signataire.departement_naissance` | requis si document actif l'utilise | texte non vide |
| `signataire.nationalite` | requis pour DOC-001 et documents qui l'utilisent | texte non vide |
| `signataire.nom_pere` | requis pour DOC-001 | texte non vide |
| `signataire.nom_mere` | requis pour DOC-001 | texte non vide |
| `signataire.fonction` ou `signataire.fonction_dirigeant` | requis si document actif l'utilise | texte non vide |

### Adresse personnelle du signataire

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `signataire.adresse.num_voie` ou `signataire.adresse_personnelle.num_voie` | requis si adresse personnelle requise | texte non vide |
| `signataire.adresse.voie` ou `signataire.adresse_personnelle.voie` | requis si adresse personnelle requise | texte non vide |
| `signataire.adresse.ville` ou `signataire.adresse_personnelle.ville` | requis si adresse personnelle requise | texte non vide |
| `signataire.adresse.cp` ou `signataire.adresse_personnelle.cp` | requis si adresse personnelle requise | code postal français à 5 chiffres |

### Validation

- `genre` pilote les accords grammaticaux ; il ne doit pas être déduit silencieusement de `civilite_affichage`.
- La date de naissance doit être une date valide et ne doit pas être postérieure à la date du jour.
- Les champs de filiation sont requis uniquement pour les documents actifs qui les consomment.
- L'adresse personnelle est requise uniquement lorsque le document actif la consomme.

## Pack répétable `associes[]`

### Comportement général

- Le bloc `associes[]` s'affiche uniquement si la branche active consomme des associés.
- Le bouton `Ajouter un associé` crée une nouvelle carte associé.
- La nouvelle carte est ouverte automatiquement.
- Chaque associé conserve un identifiant UI stable ; l'index documentaire `associes[0]`, `associes[1]`, etc. n'est produit qu'à l'export.
- La suppression d'une carte est interdite si elle fait passer le bloc sous le minimum requis.
- La suppression d'un associé référencé comme dirigeant nommé est bloquée tant que la référence n'est pas changée.

### Champs par carte associé

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `associes[].genre` | requis si accords ou identité complète requis | valeur contrôlée : `masculin` ou `feminin` |
| `associes[].civilite_affichage` | requis | texte ou choix contrôlé |
| `associes[].prenom` | requis | texte non vide |
| `associes[].nom` | requis | texte non vide |
| `associes[].nb_parts` | requis si répartition du capital active | entier supérieur ou égal à 0, strictement positif si l'associé doit détenir des parts |
| `associes[].date_naissance` | requis seulement si document actif l'utilise | date valide |
| `associes[].ville_naissance` | requis seulement si document actif l'utilise | texte non vide |
| `associes[].departement_naissance` | requis seulement si document actif l'utilise | texte non vide |
| `associes[].nationalite` | requis seulement si document actif l'utilise | texte non vide |
| `associes[].adresse.num_voie` | requis seulement si document actif l'utilise | texte non vide |
| `associes[].adresse.voie` | requis seulement si document actif l'utilise | texte non vide |
| `associes[].adresse.ville` | requis seulement si document actif l'utilise | texte non vide |
| `associes[].adresse.cp` | requis seulement si document actif l'utilise | code postal français à 5 chiffres |

### Validation du bloc

- Si `dossier.options.associe_unique = true`, le bloc doit contenir exactement un associé.
- Si `dossier.options.associe_unique = false` et que la branche active consomme plusieurs associés, le minimum est fixé par la branche active.
- Le bouton `Ajouter un associé` est masqué ou désactivé lorsque `associe_unique = true` et qu'un associé existe déjà.
- Le bouton `Ajouter un associé` est désactivé si une carte associé visible contient déjà des champs requis invalides.
- Si la répartition du capital est active, la somme des `associes[].nb_parts` doit correspondre au total de parts attendu par la branche active.
- Une carte associé invalide bloque le bouton suivant de l'étape Personnes, même si elle est repliée.

## Pack `dirigeant_nomine`

### Modes de saisie

| Mode | Comportement |
|---|---|
| Dirigeant choisi parmi les associés | afficher un sélecteur vers `associes[]`, masquer les champs d'identité déjà portés par l'associé |
| Dirigeant distinct | afficher les champs complets de `dirigeant_nomine` |

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `dirigeant_nomine.ref_associe_index` | optionnel | requis seulement si le mode choisi est associé existant |
| `dirigeant_nomine.genre` | requis si dirigeant distinct ou accords requis | valeur contrôlée : `masculin` ou `feminin` |
| `dirigeant_nomine.civilite_affichage` | requis si dirigeant requis | texte ou choix contrôlé |
| `dirigeant_nomine.prenom` | requis si dirigeant distinct | texte non vide |
| `dirigeant_nomine.nom` | requis si dirigeant distinct | texte non vide |
| `dirigeant_nomine.date_naissance` | requis si document actif l'utilise | date valide |
| `dirigeant_nomine.ville_naissance` | requis si document actif l'utilise | texte non vide |
| `dirigeant_nomine.departement_naissance` | requis si document actif l'utilise | texte non vide |
| `dirigeant_nomine.nationalite` | requis si document actif l'utilise | texte non vide |
| `dirigeant_nomine.fonction` | requis si dirigeant requis | texte non vide |
| `dirigeant_nomine.adresse.*` | requis si document actif l'utilise | adresse complète avec code postal à 5 chiffres |

### Validation

- Si le dirigeant est choisi parmi les associés, la référence doit pointer vers une carte associé existante et valide.
- Les champs d'identité du dirigeant ne doivent pas être dupliqués dans l'UI si le dirigeant est un associé existant.
- Si le dirigeant est distinct, ses champs requis sont validés comme une personne autonome.

## Pack `domiciliation`

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `domiciliation.adresse_affichee` | requis si DOC-002 actif | champ libre non vide |

### Validation

- `domiciliation.adresse_affichee` est affiché uniquement si l'autorisation de domiciliation est dans les documents actifs.
- L'UI ne reconstruit pas automatiquement ce champ depuis `societe.siege`.
- Le champ est bloquant pour l'étape Branches documentaires si DOC-002 est actif.

## Packs `bien_immobilier` et `emprunt`

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `bien_immobilier.adresse.num_voie` | requis si branche bien immobilier active | texte non vide |
| `bien_immobilier.adresse.voie` | requis si branche bien immobilier active | texte non vide |
| `bien_immobilier.adresse.ville` | requis si branche bien immobilier active | texte non vide |
| `bien_immobilier.adresse.cp` | requis si branche bien immobilier active | code postal français à 5 chiffres |
| `emprunt.montant_max` | requis si branche emprunt active | montant positif |

### Validation

- Ces champs n'apparaissent que si un document actif les consomme.
- `emprunt.montant_max` doit être strictement positif lorsque la branche emprunt est active.
- Le bloc entier est ignoré par la validation si la branche active ne l'utilise pas.

## Pack `signature`

### Champs

| Champ canonique | Statut V1 | Règle |
|---|---|---|
| `signature.lieu` | requis si un document actif possède une signature datée | texte non vide |
| `signature.date` | requis si un document actif possède une signature datée | date valide |
| `signature.image_optionnelle` | optionnel | fichier image facultatif, jamais bloquant si absent |
| `signature.nombre_exemplaires` | optionnel par défaut | requis seulement si un document actif le consomme explicitement |

### Validation

- `signature.lieu` et `signature.date` sont bloquants uniquement si au moins un document actif les consomme.
- `signature.image_optionnelle` ne bloque jamais la progression.
- `signature.nombre_exemplaires` doit être un entier strictement positif lorsqu'il est visible et requis.

## Règles de cartes repliables

### Cartes simples

- Chaque pack affiché peut être présenté sous forme de carte ouvrable/refermable.
- Une carte peut être refermée même si elle est invalide, mais son en-tête doit afficher un état d'erreur.
- Une carte invalide repliée continue de bloquer le bouton suivant de son étape.
- Lorsqu'un utilisateur tente de passer à l'étape suivante, la première carte invalide de l'étape s'ouvre automatiquement.
- L'en-tête de carte doit afficher un résumé non juridique : nom de personne, dénomination société ou libellé de bloc.

### Cartes répétables

- Les cartes `associes[]` sont ouvertes une par une ou plusieurs à la fois selon le composant UI retenu.
- Une nouvelle carte associé est ouverte automatiquement après clic sur `Ajouter un associé`.
- La première carte invalide est ouverte automatiquement lors d'une tentative de passage à l'étape suivante.
- Les cartes supprimables doivent proposer une confirmation si elles contiennent déjà des données.

## Règles de blocage du bouton suivant

Le bouton suivant de l'étape active est désactivé ou refuse la transition si au moins une condition est vraie :

1. un champ requis visible de l'étape active est vide ;
2. un champ visible de l'étape active ne respecte pas son format ;
3. une carte répétable visible de l'étape active est invalide ;
4. le nombre de cartes répétables ne respecte pas le minimum ou le maximum de la branche active ;
5. une règle transverse explicitement requise par la branche active échoue, par exemple total des parts ;
6. un champ visible dépend d'une option active mais le bloc conditionnel correspondant est incomplet.

Le bouton suivant ne doit pas être bloqué par :
- un champ masqué ;
- une option inactive ;
- un pack appartenant à une étape future ;
- une image de signature absente ;
- une valeur conservée en brouillon dans une branche non active.

## Règles de visibilité conditionnelle

| Condition | Champs affichés | Champs masqués |
|---|---|---|
| aucune société active | aucun pack société | `societe`, `societe.siege` |
| société active | `societe` | blocs documentaires non consommés |
| document avec siège actif | `societe.siege` | siège si aucun document actif ne l'utilise |
| DOC-002 actif | `domiciliation.adresse_affichee` | domiciliation si DOC-002 absent |
| branche avec associés active | `associes[]` | `associes[]` si aucun document actif ne l'utilise |
| `associe_unique = true` | une seule carte associé | bouton ajouter après le premier associé |
| dirigeant parmi associés | sélecteur associé + champs rôle utiles | identité dirigeant dupliquée |
| dirigeant distinct | champs complets `dirigeant_nomine` | sélecteur comme unique source |
| branche emprunt active | `emprunt.montant_max` | emprunt si branche inactive |
| branche bien immobilier active | `bien_immobilier.adresse.*` | bien immobilier si branche inactive |
| signature datée active | `signature.lieu`, `signature.date` | signature si aucun document actif ne la consomme |

## Règles de formats V1

| Type | Validation |
|---|---|
| texte requis | valeur non vide après trim |
| date | date valide |
| date de naissance | date valide non future |
| code postal | 5 chiffres |
| montant | nombre strictement positif |
| nombre de parts | entier supérieur ou égal à 0, avec contrainte stricte si l'associé détient des parts |
| genre | `masculin` ou `feminin` |
| booléen | `true` ou `false` |

## Hypothèses V1

- Le schéma UI V1 décrit des règles de saisie et de validation, pas une nouvelle source de vérité documentaire.
- Les écarts de nommage déjà visibles entre dictionnaire et mapping, par exemple `societe.forme_juridique` / `societe.forme` ou `signataire.adresse` / `signataire.adresse_personnelle`, doivent être résolus par la couche d'adaptation UI/moteur sans créer de nouveaux noms canoniques.
- Les règles de visibilité finales devront être croisées avec `docs/project/19_UI_FLOW_V1.md` et `docs/project/20_UI_DOCUMENT_OCCURRENCES_V1.md` lorsqu'ils existeront.
- Les validations métier sensibles non écrites dans les référentiels restent bloquantes et doivent faire l'objet d'un arbitrage explicite avant implémentation.

## Critères d'acceptation UI-FORM-SCHEMA-001

- Le bouton `Ajouter un associé` est défini avec ses règles d'affichage, de désactivation et de création de carte.
- Les cartes ouvrables/refermables sont définies, y compris l'état invalide replié.
- La validation par étape est définie.
- Le passage à l'étape suivante est bloqué si les champs requis visibles de l'étape active sont invalides.
- Les champs conditionnels n'apparaissent que s'ils sont utiles à la branche active.
- Aucun code Python n'est requis par ce ticket.
