# Decisions d'arbitrage sources V1

## Objet
Ce fichier consigne les arbitrages metier applicables a `ARBITRAGE-SOURCES-001`.

Il complete :
- `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`
- `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`
- `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`

Aucun deplacement physique de fichier n'est effectue dans ce ticket.

## Decisions validees

1. Les statuts ne doivent jamais etre deduppliques automatiquement entre familles, professions ou variantes metier.
2. Les familles ou fichiers suivants restent hors moteur courant :
   - SCP ;
   - SASU Holding ;
   - kine ;
   - pharmaciens ;
   - fiches de creation ;
   - RM Sydel ;
   - PDF 2672.
3. Pour `PV nomination gerant`, la source deja retenue dans `project/source_documents/lot_02/` reste la base canonique de famille.
4. Les autres versions de `PV nomination gerant` restent des references ; elles ne remplacent pas la source canonique sans ticket explicite.
5. Pour `Demande d'inscription a l'ordre`, aucune source unique ne doit etre choisie automatiquement tant que les variantes SELARL / SELAS / SPFPL n'ont pas ete comparees.
6. Pour `Regime communautaire`, les copies exactes peuvent etre rapprochees, mais les variantes SELARL non identiques restent a arbitrer.
7. Pour `Liste des souscripteurs` / `Attestation sur le capital`, la famille reste ambigue ; aucun placement automatique n'est autorise.
8. Aucun fichier source ne doit etre deplace, supprime ou renomme dans `ARBITRAGE-SOURCES-001`.

## Familles non fusionnables automatiquement

| Famille | Raison |
|---|---|
| Statuts | structure, profession et variante metier changent le sens juridique |
| PV nomination gerant | une source canonique existe ; les autres versions sont references et non remplacements |
| Demande d'inscription a l'ordre | variantes SELARL / SELAS / SPFPL a comparer |
| Regime communautaire | copies exactes et variantes SELARL coexistent |
| Liste des souscripteurs / Attestation sur le capital | perimetre et famille documentaire non stabilises |
| Compromis / actes de cession | profession et contexte de cession restent discriminants |

## Familles a comparer avant choix

| Famille | Variantes a comparer | Statut |
|---|---|---|
| Demande d'inscription a l'ordre | SELARL, SELAS, SPFPL | MEDIUM - bloque |
| Lettre de renonciation regime communautaire | SELARL vs SELAS/SPFPL exacts | MEDIUM - bloque |
| Lettre d'avertissement regime communautaire | SELARL vs SELAS/SPFPL exacts | MEDIUM - bloque |
| Liste des souscripteurs / Attestation sur le capital | SAS, SCS, SPFPL cession, SPFPL apport | LOW - bloque |
| Statuts | toutes structures et professions | LOW - traiter document par document |

## Hors perimetre courant

Les documents hors perimetre ne doivent pas etre places ni automatises dans le moteur courant :

| Categorie | Decision |
|---|---|
| SCP | hors moteur courant |
| SASU Holding | hors moteur courant |
| Kine | hors moteur courant |
| Pharmaciens | hors moteur courant |
| Fiches de creation | hors moteur courant |
| RM Sydel | hors moteur courant |
| PDF 2672 | hors moteur courant |

Nombre de documents hors perimetre identifies dans le dump : **16**.

## Consequence pour le placement

Le futur ticket `PLACEMENT-HIGH-001` doit se limiter aux cas `HIGH` listes dans `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`.

Toute famille `MEDIUM` ou `LOW` doit rester bloquee jusqu'a comparaison documentaire ou arbitrage metier explicite.

