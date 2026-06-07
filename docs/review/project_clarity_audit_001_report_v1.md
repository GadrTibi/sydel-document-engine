# Project clarity audit 001 report V1

Date : 2026-06-02

Ticket : `PROJECT-CLARITY-AUDIT-001`

Demande Gad : clarifier tout le projet apres constat d'une confusion entre le
premier traitement fonde trop vite sur `Documents_a_generer_par_cas.docx`, la
matiere NotebookLM, les retours humains et le statut reel des types
d'entreprise.

## Verdict court

Le projet doit etre remis a niveau sur une distinction centrale :

```text
Catalogue / moteur historique != sprint produit traite.
```

La seule lecture propre au 2026-06-02 est :

| Type | Statut reel |
| --- | --- |
| `SELARL` | En traitement avance, `PARTIAL`, corrections retours humains 006 en cours |
| `SELAS` | En traitement, pilote Naomi, sync manquante, `NO-GO dev` tant que preuve absente |
| `SPFPL cession` | Non traite en sprint produit ; inventaire technique seulement |
| `SPFPL apport` | Non traite en sprint produit ; inventaire technique seulement |
| `SCS` | Non traite en sprint produit ; inventaire technique seulement |
| `SCI` | Non traite en sprint produit ; inventaire technique seulement |
| `SCM` | Non traite en sprint produit ; inventaire technique seulement |
| `SAS` | Non traite en sprint produit ; inventaire technique seulement |

## Cause racine

Le projet a accumule deux couches differentes :

1. une couche moteur/catalogue historique, construite depuis le document
   `Documents_a_generer_par_cas.docx` et des lots documentaires ;
2. une couche sprint produit plus recente, imposee apres les retours de l'associe :
   source de reference, NotebookLM/modele, retours humains, audit de
   reutilisation, matrice, pack actif et validation.

La premiere couche donne une capacite technique. La seconde seule donne un
statut metier fiable.

Le flou vient du fait que les rapports et le code utilisent parfois des mots
comme `generable`, `catalogue metier`, `moteur DOCX V1`, `documents attendus`
ou `type catalogue` sans rappeler que cela ne vaut pas sprint produit.

## Points d'audit

### 1. Sprints reels

Les fichiers de sprint presents sont :

- `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`
- `docs/sprints/SPRINT_SELAS_V1.md`

Conclusion : seuls `SELARL` et `SELAS` ont un sprint produit actif ou suivi.

### 2. Registre de tour de controle

`docs/project/PROJECT_CONTROL_TOWER_V1.md` liste seulement deux sprints
courants :

- `SELARL`
- `SELAS`

Conclusion : la tour de controle ne valide pas les autres types comme traites.

### 3. Catalogue moteur

`src/sydel_doc_engine/domain/case_catalog.py` connait huit types :

- `SELARL`
- `SELAS`
- `SPFPL cession`
- `SPFPL apport`
- `SCS`
- `SCI`
- `SCM`
- `SAS`

Conclusion : le catalogue est large, mais il ne prouve pas une validation
produit par type.

### 4. Rapports et specs historiques

Les dossiers `docs/delivery/` et `docs/review/` contiennent de nombreuses specs
et revues de lots (`lot_04`, `lot_05`, `SCM`, `SPFPL`, `SAS`, `SCI`, etc.).

Conclusion : ces documents prouvent une analyse/generation documentaire par
lot ou par document canonique, pas un sprint produit complet par type
d'entreprise selon la methode actuelle.

### 5. Front et exposition produit

Le code front et le wizard savent lister plusieurs types. Cela cree un risque :
un utilisateur ou un agent peut croire que tous les types sont generables en V1.

Point sensible repere :

- `business_dossier_types()` construit des types depuis `CaseType` avec
  `generable_in_v1=True` pour tous les types.

Conclusion : il faut ouvrir un ticket de durcissement front/statut pour eviter
que l'UI ou les rapports presentent les types non sprintes comme prets.

## Statut corrige par type

| Type | Source de preuve principale | Statut corrige | Action |
| --- | --- | --- | --- |
| `SELARL` | `SELARL_CANONICAL_STATUS_V1.md` + sprint closing + retours humains | En traitement avance, `PARTIAL` | Continuer retours 006, pack 005, audit 006 |
| `SELAS` | `SPRINT_SELAS_V1.md` + worklog + sync protocol | En traitement, sync manquante | Obtenir commit pousse ou Sync packet |
| `SPFPL cession` | Catalogue/specs/tests lot 05 | Non traite en sprint produit | Rester `NO-GO dev` jusqu'a sprint dedie |
| `SPFPL apport` | Catalogue/specs/tests lot 05 | Non traite en sprint produit | Rester `NO-GO dev` jusqu'a sprint dedie |
| `SCS` | Catalogue/specs/tests statuts civils | Non traite en sprint produit | Rester `NO-GO dev` jusqu'a sprint dedie |
| `SCI` | Catalogue/tests/front historique | Non traite en sprint produit | Rester `NO-GO dev` jusqu'a sprint dedie |
| `SCM` | Catalogue/specs/tests SCM | Non traite en sprint produit | Rester `NO-GO dev` jusqu'a sprint dedie |
| `SAS` | Catalogue/specs/tests SAS | Non traite en sprint produit | Rester `NO-GO dev` jusqu'a sprint dedie |

## Nettoyage effectue dans ce ticket

Creation du registre :

- `docs/project/COMPANY_TYPE_STATUS_REGISTRY_V1.md`

Ce registre devient la source de statut des types d'entreprise. Il separe :

- types en sprint ;
- types partiels ;
- types seulement inventories/cables techniquement ;
- types non traites produit.

## Nettoyage encore recommande

### Priorite 1 - Verrouiller le langage projet

Mettre a jour les docs de reprise pour toujours dire :

```text
Types en traitement : SELARL, SELAS.
Autres types : inventaire technique / non traites en sprint produit.
```

### Priorite 2 - Durcir le front

Ouvrir un ticket :

```text
PROJECT-COMPANY-TYPE-UI-STATUS-001
```

Objectif : l'UI ne doit pas presenter `SCI`, `SCM`, `SPFPL`, `SAS`, `SCS` comme
generables produit V1 si le type n'a pas de sprint valide.

### Priorite 3 - Nettoyer les anciens rapports

Ne pas supprimer les anciens rapports. Les reclasser mentalement ainsi :

- rapports de lots = preuves moteur/document ;
- rapports SELARL = preuves sprint produit ;
- rapports globaux/front = preuves architecture ;
- aucun rapport lot 04/05 ne cloture un type d'entreprise complet.

### Priorite 4 - Un registre par prochain type

Pour tout prochain type choisi par Gad, creer d'abord :

```text
docs/sprints/SPRINT_[TYPE]_V1.md
```

avec `NO-GO dev`, puis NotebookLM, reuse audit, matrice, contrat front, tickets,
GO Gad.

## Decision d'audit

Le projet n'est pas faux techniquement, mais son statut produit etait devenu
ambigu.

Decision :

```text
SELARL et SELAS seulement sont en traitement metier.
Les autres types ne sont pas traites ; ils sont seulement presents dans le
catalogue/moteur historique.
```

Cette decision doit guider toutes les prochaines reponses a Gad et tous les
nouveaux tickets.
