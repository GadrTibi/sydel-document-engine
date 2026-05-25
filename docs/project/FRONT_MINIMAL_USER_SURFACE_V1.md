# Surface utilisateur minimale front V1

Date : 2026-05-25

## 1. Cible explicite

La surface utilisateur normale doit contenir uniquement :

1. `Type de dossier`
2. `Donnees a saisir`
3. `Generation`

Rien d'autre en surface principale.

Le debug interne peut exister, mais il doit etre cache par defaut et reserve a
l'equipe projet. Il ne doit pas etre un signal visible pour un utilisateur test.

## 2. Etat actuel a simplifier

La vue normale respecte deja trois titres principaux, mais elle reste trop
chargee :

- checkbox `Outils internes` visible en sidebar ;
- trois expanders ouverts dans la saisie ;
- 22 champs texte visibles pour le pilote `SELARL creation simple` ;
- bouton `Generer les PDF` visible meme quand le backend PDF local est absent ;
- metriques de generation sans explication actionnable des blocages ;
- caption technique sur `artifacts/` ;
- vocabulaire interne visible comme `ReuseRuleState`.

## 3. Regles de surface

### Type de dossier

Afficher seulement :

- un choix de type de dossier ;
- le choix courant `SELARL creation simple` tant que c'est le seul parcours
  testable.

Ne pas afficher :

- profils non saisissables ;
- statuts techniques ;
- libelles de migration ou de prototype ;
- documents attendus.

### Donnees a saisir

Afficher seulement les champs utiles au parcours courant.

Regles :

- pas de sous-onglets ;
- pas de tableaux ;
- pas de diagnostics ;
- pas de texte d'architecture ;
- pas de vocabulaire `front_data`, `DossierRecord`, `ReuseRuleState`, runtime ou
  artefact ;
- les aides de format doivent etre proches du champ concerne ;
- les dates doivent etre saisies avec un composant ou une aide qui evite
  l'ambiguite `AAAA-MM-JJ` ;
- les adresses doivent soit etre structurees, soit afficher clairement le format
  attendu avant la generation.

Les regroupements visuels sont autorises seulement s'ils ne creent pas de faux
niveau de navigation. Exemple acceptable : petits intertitres simples dans un
formulaire unique. Exemple a eviter : expanders ouverts qui ressemblent a des
zones secondaires.

### Generation

Afficher seulement :

- l'etat pret/bloque ;
- l'action de generation principale ;
- les raisons exactes de blocage, courtes et actionnables ;
- les telechargements apres production.

Regles :

- DOCX et ZIP doivent etre comprehensibles comme une generation dossier ;
- le ZIP peut etre produit automatiquement apres DOCX si c'est le comportement
  le plus simple pour le test ;
- le PDF ne doit etre visible que si le backend local est disponible, ou rester
  dans un detail interne ;
- ne pas afficher de liste documentaire complete dans la surface principale ;
- ne pas afficher de tables de statut.

## 4. Debug interne cache

Le debug interne peut contenir :

- synthese `DossierRecord` ;
- roles ;
- adresses ;
- statuts documentaires ;
- garde-fous runtime ;
- chemins d'artefacts ;
- outils prototype, document unitaire et technique.

Mais il doit etre cache derriere un mode equipe, par exemple :

- variable de configuration Streamlit ;
- secret local ;
- flag de developpement ;
- parametre interne non visible dans une session test.

La checkbox `Outils internes` ne doit pas etre visible dans la surface normale de
test utilisateur.

## 5. Hors surface principale

Doivent rester hors surface principale :

- tableaux `flow`, blocs, exigences, statuts, lots ;
- panneau documents detaille ;
- profils non saisissables ;
- assistant metier prototype ;
- document unitaire ;
- diagnostic YAML/JSON ;
- chemins `artifacts/` ;
- erreurs backend longues ;
- details de selection orchestrateur.

## 6. Perimetre generation V1

La surface minimale ne doit pas promettre plus que ce qui est branche :

- `DOC-001` ;
- `DOC-002` ;
- `DOC-003` ;
- `DOC-004`.

Elle doit aussi rester honnete :

- `DOC-006` est exclu du pilote courant ;
- `DOC-013` et `DOC-014` restent manuels / hors generation V1 ;
- les autres documents du moteur ne sont pas ouverts dans ce parcours minimal.

Cette information peut etre formulee sobrement dans la zone `Generation`, sans
creer un tableau ou un panneau supplementaire.

## 7. Prochain ticket unique

`FRONT-MINIMAL-SURFACE-CLEANUP-001`

Objectif : appliquer cette surface minimale avant tout push, redeploiement ou
test utilisateur.

Contraintes :

- ne pas modifier les generateurs ;
- ne pas modifier le moteur DOCX/PDF/ZIP ;
- ne pas modifier le wording juridique ;
- ne pas etendre le perimetre documentaire ;
- ne pas ajouter un panneau documents visible ;
- ne pas lancer de refonte d'architecture.

Criteres d'acceptation :

- vue normale : 3 titres maximum, `Type de dossier`, `Donnees a saisir`,
  `Generation` ;
- aucune table, aucun radio, aucun outil interne visible ;
- pas d'expander de diagnostic dans la surface normale ;
- PDF cache si backend indisponible ;
- blocages runtime visibles dans `Generation` ;
- test AppTest de la surface normale ;
- aucune modification Python hors UI/adaptateur necessaire a cette surface.
