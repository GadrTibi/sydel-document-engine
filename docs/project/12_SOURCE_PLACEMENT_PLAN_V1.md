# Plan de placement sources V1

## Objet
Ce plan prepare et suit le placement physique limite aux cas `HIGH`.

`PLACEMENT-HIGH-001` a ete execute le 2026-05-14. Aucun fichier source brut n'a ete deplace, supprime ou renomme.

## Niveaux de confiance

| Niveau | Signification | Placement automatique |
|---|---|---|
| HIGH | Source deja retenue ou match exact avec source deja retenue, sans ambiguite metier ouverte | Oui, uniquement dans le ticket `PLACEMENT-HIGH-001` |
| MEDIUM | Source presente mais variante metier a comparer avant choix canonique | Non |
| LOW | Famille ambigue, source sans rattachement clair, ou collision non resolue | Non |

## Synthese des cas

| Niveau | Nombre de cas | Situation |
|---|---:|---|
| HIGH | 4 | cas deja couverts ou prets pour placement strictement limite |
| MEDIUM | 3 | familles a comparer avant choix |
| LOW | 3 | familles ou lots non stabilises |

Nombre de documents sans source claire pour placement automatique : **6**.

Nombre de documents hors perimetre moteur courant : **16**.

## Cas HIGH prets pour placement physique

Ces cas sont les seuls eligibles au futur ticket `PLACEMENT-HIGH-001`.

| Cas | Source retenue / cible | Statut placement |
|---|---|---|
| DOC-001 - Declaration de non-condamnation | `project/source_documents/lot_01/declaration_non_condamnation_transforme.docx` | PLACE - no-op confirme le 2026-05-14 ; fichier deja present |
| DOC-002 - Autorisation de domiciliation | `project/source_documents/lot_01/autorisation_domiciliation_transforme.docx` | PLACE - no-op confirme le 2026-05-14 ; fichier deja present |
| DOC-003 - Procuration | `project/source_documents/lot_01/procuration_transforme.docx` | PLACE - no-op confirme le 2026-05-14 ; fichier deja present |
| PV nomination gerant | `project/source_documents/lot_02/PV nomination gérant - transforme.docx` | PLACE - no-op confirme le 2026-05-14 ; source canonique deja presente |

Note : le ticket a constate que ces fichiers etaient deja au bon emplacement. Le placement est donc un no-op documente, sans nouvelle copie. Le cas `PV nomination gerant` est egalement PLACE par confirmation de presence de la source canonique en Lot 2.

## Journal d'execution

Le journal d'execution du ticket est disponible dans `docs/project/14_SOURCE_PLACEMENT_EXECUTION_V1.md`.

## Cas MEDIUM bloques

| Famille | Blocage | Action avant placement |
|---|---|---|
| Demande d'inscription a l'ordre | variantes SELARL / SELAS / SPFPL non comparees ; ne pas auto-choisir la source SPFPL presente | comparer les variantes et produire une spec de choix canonique |
| Regime communautaire - renonciation | copies exactes SELAS/SPFPL rapprochables, mais variante SELARL non identique | comparer SELARL vs SELAS/SPFPL avant choix |
| Regime communautaire - avertissement | copies exactes SELAS/SPFPL rapprochables, mais variante SELARL non identique | comparer SELARL vs SELAS/SPFPL avant choix |

## Cas LOW bloques

| Famille | Blocage | Action avant placement |
|---|---|---|
| Statuts | nombreuses variantes par structure, profession, cession/apport, `transforme`/`modele`; aucune dedup inter-familles | traiter document par document |
| Liste des souscripteurs / Attestation sur le capital | famille encore ambigue ; fichiers SAS, SCS, SPFPL cession/apport melanges | arbitrage metier dedie |
| Documents sans source claire | 6 documents ne sont pas rattaches a une famille canonique stabilisee | qualifier ou exclure explicitement |

## Hors perimetre

Les fichiers relevant des categories suivantes ne doivent pas etre places dans le moteur courant :
- SCP ;
- SASU Holding ;
- kine ;
- pharmaciens ;
- fiches de creation ;
- RM Sydel ;
- PDF 2672.

## Ticket execute

`PLACEMENT-HIGH-001 | Deplacer physiquement dans source_documents uniquement les cas HIGH valides`

Resultat :
- les 4 cas HIGH ci-dessus sont marques comme places ;
- aucune nouvelle copie n'a ete necessaire car les fichiers cibles etaient deja presents ;
- aucune famille MEDIUM ou LOW n'a ete modifiee ;
- `project/source_import/raw_drive_dump/` reste une source brute non versionnee ;
- `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` ont ete mis a jour.
