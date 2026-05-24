# Regles structurelles du front global V1

Ticket : `GLOBAL-FRONT-ARCHITECTURE-001`

Statut : regles produit et donnees, sans implementation UI.

## Regle 1 - Pas de fusion silencieuse de roles

Deux roles proches ne sont jamais fusionnes par libelle, proximite metier ou frequence d'usage.

Exemples :

- praticien != associe ;
- associe != gerant ;
- signataire != mandataire ;
- mandataire != representant de personne morale ;
- vendeur != bailleur ;
- cedant != cessionnaire ;
- SEL principale != SCM cedee ;
- associe personne morale != representant de cette personne morale.

Quand deux roles pointent vers la meme fiche, le front doit afficher ou tracer cette relation via `RoleAssignment` et `ReuseRule`.

## Regle 2 - Adresses typees par usage

Une adresse n'est jamais seulement "adresse". Elle doit porter un usage.

Usages minimaux :

- domicile du praticien ;
- lieu d'exercice / cabinet ;
- siege social de la societe principale ;
- domiciliation ;
- adresse de la SCM ;
- adresse de la SCM cedee ;
- adresse du cessionnaire SCM ;
- adresse des locaux loues ;
- adresse du conseil de l'ordre ;
- adresse de banque ;
- adresse fiscale ou administrative.

Regles V2.1 :

- domiciliation = siege social ;
- siege social = lieu d'exercice seulement via option explicite ;
- adresse SCM standard = lieu d'exercice selon l'arbitrage Albane ;
- SCM cedee et cessionnaire SCM restent distincts par defaut.

## Regle 3 - Reutilisation uniquement via regle explicite

Le front peut reduire la double saisie par trois mecanismes :

- reference vers la meme fiche ;
- prefill initial depuis une fiche source ;
- derivation controlee, par exemple composants d'adresse vers adresse affichee.

Ces mecanismes doivent etre portes par une `ReuseRule` visible ou auditable.

Une reutilisation inactive doit laisser les champs distincts. Une reutilisation active doit conserver les roles distincts.

## Regle 4 - Typologie de la matrice d'identite

La matrice globale distingue cinq familles de decision.

| Type | Sens front | Exemple | Comportement |
|---|---|---|---|
| `SAME_FIELD` | meme champ canonique | `signature.lieu` et alias locaux | un seul champ source |
| `SAME_DATA_DIFFERENT_SHAPE` | meme donnee, forme differente | adresse composee / adresse affichee ; montant chiffres / lettres | source unique + formes derivees avec override |
| `EXPLICIT_REUSE_ONLY` | reutilisation possible mais non automatique | praticien vers signataire ; SEL vers acquereur | regle explicite, reversible |
| `DISTINCT_FIELDS` | champs differents | signataire / mandataire ; siege / lieu d'exercice | saisie et validation separees |
| `UNCERTAIN_REQUIRES_HUMAN_DECISION` | decision non tranchee | variables spec-only, calculs complexes | pas de fusion ni de derivation automatique |

Le front ne doit pas transformer `UNCERTAIN_REQUIRES_HUMAN_DECISION` en comportement produit.

## Regle 5 - Dossier, document et lot documentaire sont distincts

Le dossier est le contexte metier. Il contient les personnes, societes, adresses, options et documents attendus.

Le document est une occurrence attendue ou generable. Il consomme des champs et roles selon son code `DOC-XXX`.

Le lot documentaire est une organisation de livraison et de source. Il ne doit pas devenir une logique de saisie front.

Consequence :

- un champ utile a un document peut rester local au document ;
- une donnee commune au dossier peut etre proposee a plusieurs documents ;
- une option de lot ne doit pas etre prise pour une option metier ;
- le mode document unitaire doit rester separe du parcours dossier complet.

## Regle 6 - Gestion des overrides

Un override est une valeur locale qui remplace une valeur derivee ou partagee dans un scope donne.

Scopes possibles :

- dossier ;
- role ;
- document ;
- champ ;
- forme affichee ;
- piece ou validation.

Regles :

- l'override ne modifie pas silencieusement la fiche source ;
- l'override doit garder sa raison et son scope ;
- une mise a jour de la source doit signaler que l'override diverge ;
- un override documentaire sensible doit produire une `ValidationIssue` de revue.

Exemples :

- date de signature differente pour un document ;
- adresse affichee corrigee manuellement ;
- locataire du bail saisi en champ libre ;
- montant en lettres force apres controle.

## Regle 7 - Champs composites et decomposes

Les champs composites doivent etre modelises avec leur source et leurs formes.

Exemples :

- adresse : composants + adresse affichee ;
- personne : prenom + nom + civilite + affichage complet ;
- montant : valeur numerique + affichage + lettres ;
- capital : nombre de titres + valeur nominale + montant total ;
- cession : prix total + prix unitaire + plage de parts ;
- RCS : numero + ville ;
- ordre : numero RPPS + numero d'ordre + departement ou ville ordinale.

Regles :

- les composants sont privilegies pour la saisie et la validation ;
- la forme affichee est calculee quand la source est fiable ;
- la forme affichee peut rester libre si la source documentaire l'exige ;
- une forme en lettres doit etre derivee ou forcee, jamais inventee.

## Regle 8 - Documents manuels et reserves

Un document manuel doit rester visible comme attendu, mais non generable.

Un document reserve ou non implemente doit indiquer :

- pourquoi il n'est pas generable ;
- quelles informations sont connues ;
- quel ticket ou arbitrage est requis ;
- s'il peut etre teste en document unitaire.

Le front ne doit pas masquer un document attendu seulement parce qu'il n'est pas automatise.

## Regle 9 - Revue et validation

Le front doit distinguer :

- validation de saisie : champs manquants, formats, contradictions ;
- validation documentaire : document manuel, contexte incomplet, source non recue ;
- validation juridique : wording, arbitrage, decision humaine ;
- validation de generation : DOCX/PDF/ZIP produits.

Une generation technique reussie ne vaut pas validation juridique.

## Regle 10 - Sources et hierarchie

Le registre V2.1 est suffisant pour concevoir l'architecture front. Il ne remplace pas les specs documentaires pour coder un document.

Hierarchie d'usage pour ce ticket :

1. source de verite documentaire et V3 ;
2. registre canonique global V2.1 ;
3. audit d'identite et questions V2 ;
4. dictionnaire et mapping V1 ;
5. catalogue moteur ;
6. prototype Streamlit en reference secondaire seulement.

Le prototype ne peut jamais trancher une contradiction avec le registre V2.1.
