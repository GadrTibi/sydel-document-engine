# Front information dedup agent protocol V1

Date : 2026-06-02

## Objet

Ce document definit le sous-agent specialise `Front Information Dedup Agent`.

Sa mission est de proteger le front contre la redondance de saisie :

```text
Une information metier identique doit etre demandee une seule fois.
```

Elle peut ensuite etre reutilisee, derivee ou affichee dans plusieurs
documents, mais elle ne doit pas etre redemandee comme champ editable sauf si une
source, une regle metier ou un arbitrage humain prouve que les deux informations
sont distinctes.

## Decision produit

Avant tout `GO dev` qui touche un formulaire, un parcours utilisateur ou un
contrat metier-front, Codex doit activer ce controle.

Le sprint ne peut pas etre considere pret cote front si les champs visibles ne
sont pas classes en :

- saisie source unique ;
- valeur derivee ;
- reutilisation explicite ;
- affichage lecture seule ;
- champ distinct justifie ;
- blocage / arbitrage requis.

## Role du sous-agent

Nom recommande :

```text
Front Information Dedup Agent
```

Mission :

1. inventorier tous les champs editables visibles du front ;
2. rattacher chaque champ a un objet metier canonique ;
3. detecter les doublons de saisie ;
4. verifier que les reutilisations sont explicites, reversibles et tracees ;
5. verifier que les constantes metier ne sont pas demandees a l'utilisateur ;
6. signaler les champs qui doivent devenir caches, derives ou lecture seule ;
7. produire un rapport `PASS`, `PARTIAL` ou `BLOCKED`.

## Sources obligatoires

Le sous-agent lit au minimum :

- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md` ;
- `docs/project/GLOBAL_FRONT_RULES_V1.md` ;
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md` ;
- `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv` ;
- `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` ;
- le contrat metier-front du sprint ;
- le fichier de sprint actif ;
- le code front concerne dans `src/sydel_doc_engine/app/` ou
  `src/sydel_doc_engine/front_app/` ;
- les tests front concernes.

## Classification obligatoire

| Cas | Decision | Exemple |
| --- | --- | --- |
| Meme donnee, meme role, meme usage | `DEDUP_REQUIRED` | adresse personnelle redemandee pour conjoint alors que la regle dit identique |
| Meme donnee, autre role possible | `EXPLICIT_REUSE_ONLY` | praticien peut etre gerant, mais pas toujours |
| Donnee calculee | `DERIVED` | valeur nominale = capital / parts |
| Donnee constante | `HIDE_CONSTANT` | duree sociale SELARL = 99 ans |
| Donnee affichee pour controle | `READ_ONLY_OK` | resume d'adresse avant generation |
| Meme libelle, role metier different | `KEEP_DISTINCT` | siege social vs lieu d'exercice si source les distingue |
| Source insuffisante | `BLOCKED` | relation de role non prouvee |

## Methode de controle

Pour chaque parcours front :

1. lister les champs editables ;
2. lister les champs caches/derives/lecture seule ;
3. mapper chaque champ vers un objet canonique ;
4. grouper les champs par information metier ;
5. identifier les groupes qui ont plusieurs champs editables ;
6. classer chaque groupe selon la table ci-dessus ;
7. ouvrir un ticket si une redondance editable n'est pas justifiee.

## Regles non negociables

- Une valeur reutilisee ne doit pas etre redemandee sous un autre libelle.
- Une valeur derivee peut etre affichee, mais pas saisie une deuxieme fois.
- Une constante metier ne doit pas etre un champ utilisateur.
- Une relation sensible de role doit etre opt-in ou sourcee, jamais implicite.
- Une adresse identique par regle doit etre copiee/derivee, pas redemandee.
- Un champ peut rester distinct seulement si le role metier est distinct.

## Sortie attendue

Le rapport du sous-agent doit contenir :

- parcours audite ;
- nombre de champs editables ;
- doublons detectes ;
- decisions `DEDUP_REQUIRED`, `EXPLICIT_REUSE_ONLY`, `DERIVED`,
  `HIDE_CONSTANT`, `READ_ONLY_OK`, `KEEP_DISTINCT`, `BLOCKED` ;
- tickets ouverts ou decision sourcee ;
- tests front concernes ;
- verdict `PASS`, `PARTIAL` ou `BLOCKED`.

## Application SELARL courante

La SELARL a deja eu un audit de deduplication front :

- `TRACK-B-SELARL-FIELD-DEDUP-AUDIT-001` ;
- rapport : `docs/review/track_b_selarl_field_dedup_audit_001_report_v1.md`.

Les retours humains 006 ont ajoute des cas concrets traites :

- adresse conjoint supprimee comme saisie autonome quand elle est identique a
  celle de l'associe ;
- duree sociale supprimee comme variable utilisateur, toujours 99 ans ;
- nombre d'exemplaires supprime comme variable utilisateur, toujours 4 ;
- qualite renoncee supprimee comme variable utilisateur, toujours associe ;
- date courrier derivee du jour ;
- siege social peut etre repris depuis l'adresse personnelle via option
  explicite.

Verdict courant SELARL simple/regime : pas de blocage dedup connu avant la
validation associe du pack 005.
