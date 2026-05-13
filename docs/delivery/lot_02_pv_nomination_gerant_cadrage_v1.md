# Cadrage métier — Famille « PV nomination gérant » V1

## Position dans le projet
Ce n'est **pas** encore un ticket de code.
La bonne étape suivante, après :
- l'arbre documentaire V1,
- le dictionnaire canonique des variables V1,
- la table de mapping document -> variables canoniques V1,

est le **cadrage / la spec métier** de la famille documentaire « PV nomination gérant ».

## Pourquoi on ne part pas sur UI-001 maintenant
Le document de référence indique explicitement que la gestion du nombre variable d’associés concerne notamment :
- les statuts ;
- le PV de nomination de gérant ;
- la liste des souscripteurs.

Donc, avant de brancher une UI plus large, il faut figer la logique canonique de ce document et sa relation avec `associes[]`.

## Source de vérité
Le document `Documents à générer par cas` rattache **PV nomination gérant** à plusieurs familles :
- SELARL
- SELAS
- SPFPL cession
- SPFPL apport
- SCS
- SCI
- SCM

## Décisions métier prises à ce stade
1. « PV nomination gérant » doit être traité comme une **famille documentaire mutualisable**, pas comme un simple exemple figé.
2. Les placeholders locaux de type `personne_1`, `personne_2` ne sont **pas** canoniques.
3. Les rôles canoniques retenus sont :
   - `societe`
   - `associes[]`
   - `dirigeant_nomine`
   - `signature`
   - éventuellement `bien_immobilier`
   - éventuellement `emprunt`
4. `civilite_affichage` et `genre` restent séparés.
5. La gestion dynamique du nombre d’associés est **obligatoire** dans le cadrage de cette famille.
6. Les blocs qui n'apparaissent pas dans tous les cas doivent devenir des **blocs conditionnels**, pas du texte fixe universel.

## Ce que la lecture actuelle du modèle implique
La lecture du modèle transmis montre qu'il ressemble à un exemple très contextualisé.
Il ne faut donc **pas** coder directement un générateur universel à partir de ce seul rendu sans re-spécification.

En pratique, cela veut dire :
- extraire le **tronc canonique** de nomination du dirigeant ;
- identifier les **blocs conditionnels** ;
- détacher les exemples locaux du rôle canonique.

## Tronc canonique attendu de la famille
Le tronc canonique V1 devra au minimum couvrir :
- en-tête société ;
- réunion / assemblée ;
- liste des associés présents ou représentés ;
- constat de représentation du capital ;
- décision de nomination du dirigeant ;
- acceptation des fonctions ;
- pouvoirs pour formalités ;
- signature / lieu / date / exemplaires.

## Blocs possiblement conditionnels
À confirmer dans la spec détaillée :
- bloc d’autorisation d’emprunt ;
- bloc relatif à un bien immobilier ;
- formulations dépendant d’une forme sociale très spécifique ;
- accord de genre du dirigeant nommé ;
- variantes singulier/pluriel selon le nombre d’associés.

## Règles canoniques à appliquer
- `associes[]` = bloc répétable
- `dirigeant_nomine` = rôle distinct, ne pas le confondre avec `associes[1]`
- ne pas figer `personne_2` comme dirigeant
- ne pas figer un genre dans le texte canonique
- ne pas figer un type de société dans le tronc canonique sans justification métier
- toute donnée ponctuelle utilisée une seule fois peut rester un champ manuel si besoin

## Livrable attendu au prochain ticket
Le prochain vrai ticket doit produire une **spec canonique document par document** pour cette famille, avec :
- structure du document ;
- blocs fixes ;
- blocs conditionnels ;
- mapping des variables canoniques ;
- règles de répétition pour `associes[]` ;
- règles de grammaire minimales ;
- points ouverts restants.

## Ce qu'on ne fait pas encore
- pas de code du générateur
- pas d'UI
- pas de refactor du Lot 1
- pas de PDF / ZIP
