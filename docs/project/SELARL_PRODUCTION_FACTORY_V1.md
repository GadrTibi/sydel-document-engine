# SELARL production factory V1

## Objet

Ce document fixe la recette standard pour transformer une famille de cas en pack de production serieux, document par document, sans casser le moteur deterministe.

Le modele de depart est la famille SELARL. La methode est ensuite reutilisable pour les autres familles.

## 1. Source humaine / source de verite

Ordre de priorite obligatoire :

1. retours humains les plus recents fournis par l'utilisateur ;
2. arbitrages humains deja actes ;
3. source de verite projet et specs existantes ;
4. code existant seulement comme implementation a verifier, jamais comme source juridique.

Tout texte humain exact fourni doit etre repris le plus fidelement possible. Si une formulation complete n'est pas disponible dans le depot, le point reste ouvert et ne doit pas etre invente.

## 2. Contrat metier-front

Avant d'ecrire du code, verifier le contrat entre le front et le moteur :

- famille, cas et variantes couvertes ;
- documents generables, reserves, manuels et hors scope ;
- champs saisis par l'utilisateur ;
- champs derives depuis une source unique ;
- roles rattaches automatiquement ;
- variables moteur attendues.

Pour SELARL V1 Track B, le contrat cible reste le clean front `front_app`, pas le legacy front.

## 3. Delta front

Le front ne change que si une variable documentaire de production n'est pas alimentee proprement.

Regles :

- preferer une derivation ou un rattachement explicite a une nouvelle saisie ;
- ne pas dupliquer une donnee deja sourcee ;
- ne pas rouvrir un chantier UX large pendant un ticket documentaire ;
- garder les cas hors scope visibles comme blocages ou reserves honnetes.

Exemple SELARL : le president de seance du PV est derive de l'associe unique, sans champ visible supplementaire.

## 4. Delta generateur

Chaque generateur est modifie uniquement sur les retours humains explicites du ticket.

Cycle obligatoire par document :

`Inventorie -> Valide -> Source recue -> Analyse -> Specifie -> Code -> Teste -> Valide`

Si un retour humain modifie un wording deja code, le test doit verifier la correction exacte et, si possible, l'absence de l'ancien texte.

## 5. Smoke docs

La recette minimale d'un pack de production comprend :

- tests unitaires cibles des generateurs corriges ;
- generation DOCX reelle des documents touches ;
- generation ZIP dossier depuis le parcours famille ;
- verification qu'aucun placeholder source ne reste dans les DOCX ;
- verification que les textes retires ne reapparaissent pas.

Pour le front Track B :

- lancement local du clean front ;
- preuve HTTP 200 ;
- pas de contournement si browser-use refuse localhost.

## 6. Relecture humaine

La sortie du ticket n'est pas une validation juridique finale.

La relecture humaine doit porter sur :

- fidelite au texte humain fourni ;
- absence de wording invente ;
- orthographe, typographie et suppression des parasites ;
- coherence des variables mappees ;
- variantes non couvertes ou bloquees.

## 7. Verrouillage

Quand le pack est juge acceptable :

- inscrire les corrections dans le backlog famille ;
- figer les variables ajoutees ;
- conserver les tests qui prouvent les non-regressions ;
- lister les OPEN POINTS restants ;
- ne pas fusionner plusieurs familles dans le meme changement.

## 8. Passage au cas suivant

Le passage a une autre famille se fait seulement apres :

- smoke DOCX/ZIP vert du pack courant ;
- front local accessible ;
- backlog famille a jour ;
- points ouverts documentes ;
- decision humaine sur les textes incomplets ou ambigus.
