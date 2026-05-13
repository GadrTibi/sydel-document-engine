# DAAT x SYDEL — SPEC CANONIQUE V1  
## Famille `PV nomination gérant`

## 1. Objet
Formaliser la **spec canonique** de la famille documentaire **PV nomination gérant** avant codage.

Cette spec ne code rien.  
Elle sert à :
- sortir d’un modèle source trop spécifique ;
- raccorder le document au **dictionnaire canonique des variables** ;
- préparer un générateur **from-scratch** ;
- expliciter les blocs fixes, blocs conditionnels, règles de pluralisation et points ouverts.

---

## 2. Périmètre documentaire visé

Le référentiel par cas rattache `PV nomination gérant.docx` aux familles suivantes :

- SELARL
- SELAS
- SPFPL cession
- SPFPL apport
- SCS
- SCI
- SCM

SAS est hors périmètre de cette famille documentaire, avec un document distinct de type président.

> Important : le fait que **SELAS** pointe aussi vers `PV nomination gérant.docx` est conservé comme **source de vérité projet** à ce stade, même si la dénomination mérite validation métier ultérieure.

---

## 3. Principe de canonisation

Le modèle source lu pour le Lot 2 est trop spécifique :
- il est rédigé comme un exemple très marqué SCI ;
- il contient un bloc d’emprunt immobilier ;
- il limite visiblement la liste des associés à `personne_1` et `personne_2` ;
- il fixe implicitement le dirigeant nommé sur `personne_2` ;
- il mélange des accords (`gérant` / `née`) non généralisés.

La canonisation retenue est donc :

1. **on ne recopie pas le modèle source tel quel** ;
2. **on extrait un noyau commun** de la famille PV nomination gérant ;
3. **on rend dynamiques** :
   - la liste des associés ;
   - l’identité du dirigeant nommé ;
   - les accords de genre ;
   - certains blocs conditionnels ;
4. **on garde un document from-scratch** ;
5. **on ne lance pas encore le code** sur cette base tant que la spec n’est pas validée.

---

## 4. Rôles canoniques utilisés

### 4.1 Rôles principaux
- `societe`
- `associes[]`
- `dirigeant_nomine`
- `signature`

### 4.2 Rôles conditionnels
- `bien_immobilier`
- `emprunt`

### 4.3 Rôle legacy à ne pas conserver comme vérité
- `personne_1`
- `personne_2`

Ces noms peuvent exister dans le document source, mais **ne doivent pas devenir la structure canonique du moteur**.

---

## 5. Variables canoniques minimales

## 5.1 Société
- `societe.denomination`
- `societe.forme_sociale_affichage`
- `societe.capital_social`
- `societe.capital_variable` (booléen ou variante de texte)
- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.cp`
- `societe.siege.ville`
- `societe.ville_rcs`

## 5.2 Réunion / décision
- `decision.date`
- `reunion.date_lettres`
- `reunion.heure`

## 5.3 Parts / capital
- `capital.nb_parts_total`
- `capital.valeur_nominale_part`

## 5.4 Associés (répétable)
Chaque item de `associes[]` contient a minima :
- `civilite_affichage`
- `genre`
- `prenom`
- `nom`
- `nb_parts`
- `est_present_ou_represente`

## 5.5 Dirigeant nommé
- `dirigeant_nomine.civilite_affichage`
- `dirigeant_nomine.genre`
- `dirigeant_nomine.prenom`
- `dirigeant_nomine.nom`
- `dirigeant_nomine.date_naissance`
- `dirigeant_nomine.ville_naissance`
- `dirigeant_nomine.departement_naissance`
- `dirigeant_nomine.nationalite`
- `dirigeant_nomine.adresse_personnelle.num_voie`
- `dirigeant_nomine.adresse_personnelle.voie`
- `dirigeant_nomine.adresse_personnelle.cp`
- `dirigeant_nomine.adresse_personnelle.ville`
- `dirigeant_nomine.fonction_affichage`

## 5.6 Signature
- `signature.lieu`
- `signature.nombre_exemplaires`

## 5.7 Bloc conditionnel emprunt / bien
- `emprunt.actif` (booléen)
- `emprunt.montant_max`
- `bien_immobilier.num_voie`
- `bien_immobilier.voie`
- `bien_immobilier.cp`
- `bien_immobilier.ville`

---

## 6. Blocs documentaires canoniques

## Bloc A — Tête du document
Contenu attendu :
- titre sur 3 lignes ;
- date de décision ;
- identité société ;
- capital ;
- siège ;
- RCS ;
- date et heure de réunion.

### Canonisation
- le texte fixe de tête doit être séparé du contenu variable ;
- la mention exacte de forme sociale ne doit pas être figée sur `société civile immobilière` pour toute la famille ;
- la formulation peut varier selon la structure, mais la **place fonctionnelle** du bloc reste la même.

---

## Bloc B — Introduction de l’assemblée
Contenu attendu :
- rappel des associés réunis ;
- rappel du capital divisé en parts ;
- réunion au siège ;
- préambule des décisions à prendre.

### Canonisation
- le bloc reste commun à la famille ;
- la liste des associés devient dynamique ;
- les formulations singulier/pluriel devront dépendre du nombre d’associés.

---

## Bloc C — Liste des associés présents ou représentés
Contenu attendu :
- liste des associés ;
- nombre de parts représentées ;
- total des parts présentes ;
- totalité du capital si applicable.

### Canonisation
- **bloc répétable** basé sur `associes[]` ;
- le moteur ne doit pas être limité à 2 associés ;
- la phrase de synthèse doit pouvoir se recalculer.

### Règles
- si 1 associé : forme singulière ;
- si 2+ associés : forme plurielle ;
- le référentiel projet dit explicitement que ce document fait partie de ceux où le nombre d’associés doit être géré dynamiquement.

---

## Bloc D — Ordre du jour / décisions prévues
Contenu attendu :
- nomination du gérant ;
- éventuellement autres décisions ;
- pouvoir.

### Canonisation
- `nomination du gérant` = noyau commun ;
- `pouvoir` = noyau commun ;
- `autorisation de contracter un emprunt...` = **bloc conditionnel**, pas noyau universel.

---

## Bloc E — Première décision : nomination du dirigeant
Contenu attendu :
- désignation du dirigeant ;
- identité complète du dirigeant nommé ;
- durée ;
- formule de vote / unanimité.

### Canonisation
- le dirigeant nommé est porté par `dirigeant_nomine`, pas par `personne_2` ;
- les accords `né / née` doivent dépendre de `dirigeant_nomine.genre` ;
- la fonction affichée du dirigeant nommé doit être pilotée proprement.

### Décision de spec
- pour la famille `PV nomination gérant`, la **fonction canonique par défaut** est `gérant` ;
- si une variante structurelle impose une autre fonction, cela devra être traité explicitement comme variante métier, pas implicitement.

---

## Bloc F — Deuxième décision : emprunt / bien immobilier
Contenu attendu dans le modèle lu :
- montant maximum ;
- acquisition d’un bien immobilier ;
- adresse du bien.

### Canonisation
- ce bloc est **conditionnel** ;
- il ne doit pas être rendu obligatoire pour toute la famille ;
- il doit être activé par une condition explicite.

### Décision de spec
- booléen canonique : `emprunt.actif`
- si `false`, le bloc n’est pas généré
- si `true`, il est généré avec les données `emprunt` + `bien_immobilier`

---

## Bloc G — Troisième décision : pouvoirs
Contenu attendu :
- pouvoirs au porteur d’un original ;
- formalités au greffe / tribunal de commerce.

### Canonisation
- bloc fixe quasi universel de la famille ;
- wording exact à stabiliser lors de la spec de texte.

---

## Bloc H — Signature / acceptation
Contenu attendu :
- `Fait à ... en ... exemplaires`
- mention d’acceptation des fonctions

### Canonisation
- `signature.lieu`
- `signature.nombre_exemplaires`
- mention d’acceptation :
  - wording à stabiliser ;
  - fonction affichée portée par `dirigeant_nomine.fonction_affichage`

---

## 7. Règles grammaticales minimales

Le référentiel projet limite les variantes connues à :
- singulier / pluriel
- masculin / féminin

Application à cette famille :

### 7.1 Singulier / pluriel
À prévoir au minimum pour :
- `associé présent / associés présents`
- `représente / représentent`
- formulation de synthèse des parts

### 7.2 Masculin / féminin
À prévoir au minimum pour :
- `né / née`
- éventuellement la fonction si la variante doit être affichée au féminin

### Décision
La variable de genre est distincte de la civilité d’affichage.

---

## 8. Ce qui est canonique vs ce qui reste ouvert

## 8.1 Canonique déjà fixé
- rôles `associes[]`, `dirigeant_nomine`, `societe`, `signature`
- liste d’associés dynamique
- bloc emprunt conditionnel
- sortie de la logique `personne_1 / personne_2`
- séparation `civilite_affichage` / `genre`

## 8.2 Ouvert / à arbitrer avant code
- périmètre exact de la famille pour **SELAS**
- wording canonique de la tête selon les structures
- maintien ou non de `à capital variable` selon structures
- wording canonique du bloc pouvoirs
- féminisation éventuelle de la fonction du dirigeant dans l’affichage
- formule d’acceptation finale exacte
- présence / absence d’un bloc d’emprunt selon sous-familles

---

## 9. Décision de mise en œuvre

## Ce qu’on fait maintenant
- on **valide cette spec canonique**
- on **n’écrit pas encore le générateur**
- on prépare ensuite un ticket de **spec détaillée de texte** document par document pour cette famille

## Ce qu’on ne fait pas encore
- pas de refactor UI
- pas d’intégration Streamlit
- pas de code du générateur sur la base du modèle source brut

---

## 10. Prochaine étape recommandée
À partir de cette spec canonique V1 :
1. formaliser la **spec textuelle détaillée** du document `PV nomination gérant` ;
2. fixer les variantes structurelles nécessaires ;
3. puis seulement ouvrir le ticket de code.
