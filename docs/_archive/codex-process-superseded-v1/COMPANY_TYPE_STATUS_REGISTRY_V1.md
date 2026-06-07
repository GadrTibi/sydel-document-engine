# Company type status registry V1

Date : 2026-06-02

## Objet

Ce registre fixe le statut produit reel des types d'entreprise du projet SYDEL.

Il corrige une confusion importante :

```text
Present dans le catalogue ou le moteur != traite comme type d'entreprise.
```

Un type d'entreprise est considere `traite` uniquement s'il dispose d'un sprint
metier identifiable, d'une triangulation des sources, d'une matrice
documentaire, d'un audit de reutilisation, de tickets bornes, de controles, et
d'un statut canonique `DONE`, `PARTIAL` ou `BLOCKED`.

Le code existant, les generateurs historiques, les tests unitaires et le
catalogue documentaire sont des preuves techniques. Ils ne valent pas validation
metier du type.

## Niveaux de statut

| Niveau | Signification | Peut etre presente comme traite ? |
| --- | --- | --- |
| `SPRINT_ACTIF` | Sprint metier ouvert et suivi dans `docs/sprints/` | Oui, en precisant la phase |
| `PARTIAL` | Sous-perimetre valide ou avance, variantes ouvertes | Oui, en precisant les limites |
| `DONE` | Perimetre annonce valide techniquement et humainement | Oui |
| `BLOCKED` | Sprint ouvert mais bloque par source, sync, retour ou decision | Oui, comme bloque |
| `INVENTAIRE_TECHNIQUE` | Present dans catalogue/code/tests sans sprint metier complet | Non |
| `NON_TRAITE` | Aucun sprint produit ouvert | Non |

## Registre courant

| Type | Statut produit reel | Preuves | Lecture autorisee |
| --- | --- | --- | --- |
| `SELARL` | `SPRINT_ACTIF` / `PARTIAL` | `docs/project/SELARL_CANONICAL_STATUS_V1.md`, `docs/sprints/SPRINT_SELARL_CLOSING_V1.md`, rapports SELARL, packs 001-004, retours humains 006 | Type en traitement avance. Perimetre simple/regime communautaire en corrections 006 ; non clos a 100 %. |
| `SELAS` | `SPRINT_ACTIF` / `BLOCKED sync` / `NO-GO dev` | `docs/sprints/SPRINT_SELAS_V1.md`, worklog Naomi, rapport rattrapage, branche `codex/naomie-selas-sprint` | Type en traitement Naomi. Avancee annoncee, mais requalification impossible sans commit pousse ou Sync packet. |
| `SPFPL cession` | `INVENTAIRE_TECHNIQUE` | `src/sydel_doc_engine/domain/case_catalog.py`, `docs/delivery/lot_05_spfpl_*`, tests lot 05 | Non traite comme sprint produit. Ne pas presenter comme type traite. |
| `SPFPL apport` | `INVENTAIRE_TECHNIQUE` | `src/sydel_doc_engine/domain/case_catalog.py`, `docs/delivery/lot_05_spfpl_*`, tests lot 05 | Non traite comme sprint produit. Ne pas presenter comme type traite. |
| `SCS` | `INVENTAIRE_TECHNIQUE` | `src/sydel_doc_engine/domain/case_catalog.py`, specs statuts civils, tests statuts civils | Non traite comme sprint produit. |
| `SCI` | `INVENTAIRE_TECHNIQUE` | `src/sydel_doc_engine/domain/case_catalog.py`, mode assistant historique, tests SCI/statuts civils | Non traite comme sprint produit. Les scenarios SCI sont des preuves techniques ou de non-regression, pas un sprint complet. |
| `SCM` | `INVENTAIRE_TECHNIQUE` | `src/sydel_doc_engine/domain/case_catalog.py`, specs SCM, tests statuts/cession/satellites SCM | Non traite comme sprint produit. |
| `SAS` | `INVENTAIRE_TECHNIQUE` | `src/sydel_doc_engine/domain/case_catalog.py`, specs statuts SAS, tests SAS/satellites | Non traite comme sprint produit. |

## Audit catalogue au 2026-06-02

Le catalogue moteur connait huit types :

| Type | Occurrences catalogue | Documents uniques | Lecture |
| --- | ---: | ---: | --- |
| `SELARL` | 24 | 21 | Sprint produit actif et partiel |
| `SELAS` | 20 | 18 | Sprint produit actif, sync manquante |
| `SPFPL cession` | 15 | 13 | Inventaire technique seulement |
| `SPFPL apport` | 14 | 12 | Inventaire technique seulement |
| `SCS` | 5 | 5 | Inventaire technique seulement |
| `SCI` | 7 | 7 | Inventaire technique seulement |
| `SCM` | 12 | 10 | Inventaire technique seulement |
| `SAS` | 7 | 6 | Inventaire technique seulement |

## Regle de langage

Reponses autorisees :

- `SELARL est en traitement avance, partiel, en corrections retour humain 006.`
- `SELAS est en traitement, mais sa requalification depend de la synchronisation Naomi.`
- `SCI/SCM/SPFPL/SAS/SCS existent dans le catalogue et le moteur, mais n'ont pas ete traitees comme sprints produit.`

Reponses interdites :

- `SCI est deja traitee` si la preuve est seulement un test ou un generateur.
- `SCM est terminee` si aucun sprint complet n'a applique NotebookLM, reuse, matrice, pack et retour humain.
- `Le moteur sait generer donc le type est valide.`

## Nettoyage recommande

1. Mettre ce registre comme source de statut des types d'entreprise.
2. Mettre a jour la tour de controle et le dernier etat pour y pointer.
3. Creer un ticket de durcissement front/code si l'UI continue d'exposer tous
   les types comme `generable_in_v1=True`.
4. Pour chaque type non traite, ouvrir un sprint dedie seulement quand Gad le
   demande, en commencant par `NO-GO dev`, sources, NotebookLM, reuse audit,
   matrice, puis validation Gad.

## Decision

Au 2026-06-02, seuls deux types peuvent etre presentes comme en traitement :

```text
SELARL
SELAS
```

Tous les autres types sont :

```text
inventories / cables historiquement / non traites en sprint produit
```
