# Lot 04 - preparation statuts V1

## Objet

Ce document prepare la vague `statuts` avant toute specification et tout codage.

Ticket : `PREP-STATUTS-001`.
Date : 2026-05-14.

Contraintes appliquees :
- aucun code Python modifie ;
- aucune UI modifiee ;
- aucun wording juridique modifie ;
- `docs/project/01_EXECUTION_BOARD.md` et `docs/project/04_LAST_STATE.md` non modifies, conformement au ticket ;
- copie limitee aux statuts rattaches explicitement au referentiel et identifies en matching HIGH dans `project/source_import/raw_drive_dump/`.

## Sources consultees

- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/project/10_SOURCE_IMPORT_MANIFEST_V1.md`
- `docs/project/11_SOURCE_DUPLICATES_REPORT_V1.md`
- `docs/project/12_SOURCE_PLACEMENT_PLAN_V1.md`
- `docs/project/13_SOURCE_ARBITRATION_DECISIONS_V1.md`
- `project/source_truth/Documents_a_generer_par_cas.docx`
- `project/source_import/raw_drive_dump/`

ADR reperes : `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0005`.

## Methode

Les statuts ont ete retenus uniquement lorsque les trois conditions suivantes etaient reunies :
1. la famille est citee dans la source de verite ou dans le ticket ;
2. le fichier existe dans le dump brut avec un libelle compatible avec le referentiel ;
3. le contexte de dossier permet un rattachement direct sans fusion inter-familles.

Le niveau `HIGH` employe ici qualifie seulement l'appariement `source de verite -> raw dump` pour `PREP-STATUTS-001`. Il ne modifie pas l'arbitrage anterieur selon lequel les statuts ne doivent pas etre dedupliques automatiquement entre familles.

Les variantes proches, hors perimetre ou concurrentes restent dans le dump brut. Elles ne sont pas dedupliquees et ne doivent pas etre utilisees comme base de codage sans ticket d'arbitrage.

## Statuts trouves et copies

| Famille | Source brute | Cible Lot 04 | SHA-256 |
|---|---|---|---|
| SELARL chirurgien-dentiste | `project/source_import/raw_drive_dump/Creation SELARL/Documents de base/Statuts/Modele statuts SELARL chirurgien dentiste sans communaute.docx` | `project/source_documents/lot_04/Modele statuts SELARL chirurgien dentiste sans communaute.docx` | `642FBE69F9BD2876DF4A8EFF6F18528B5E774E5BEB653123C2D7EC2DB7DA6EB8` |
| SELARL medecin | `project/source_import/raw_drive_dump/Creation SELARL/Documents de base/Statuts/Modele statuts SELARL medecins.docx` | `project/source_documents/lot_04/Modele statuts SELARL medecins.docx` | `1020BAE5B9C3BCDB601AFFBE6E20266C79161C800B76DB214933ACA7FD2DCCAD` |
| SELAS medecin | `project/source_import/raw_drive_dump/Creation SELAS/Documents de base/Statuts/Statuts_SELAS_medecin.docx` | `project/source_documents/lot_04/Statuts_SELAS_medecin.docx` | `0EAE6A0B6319679C33D1B782E9B7967B76C2D58BFE3E70347AB9D5F2EA3BD64F` |
| SPFPL cession | `project/source_import/raw_drive_dump/Creation SPFPL/Statuts/Statuts_SPFPLAS_dentistes_cession.docx` | `project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx` | `84BAFD01D195EC6DFE119CFF958B647488836DABB9831D699D9678114928586B` |
| SPFPL apport | `project/source_import/raw_drive_dump/Creation SPFPL/apport/statuts/Statuts SPFPLAS dentistes - apport.docx` | `project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx` | `7758ADE5A59C926490FBE9914E71DDE953435BDF032F56E894561F5C9620D549` |
| SCS | `project/source_import/raw_drive_dump/Creation SCS/Statuts_SCS_modele.docx` | `project/source_documents/lot_04/Statuts_SCS_modele.docx` | `CE9101153E9D41CA8884C4D1035AEE0C7E1AB8130BA58F087491714DC896E5EB` |
| SCI | `project/source_import/raw_drive_dump/Creation SCI/Statuts/Modele statuts SCI.docx` | `project/source_documents/lot_04/Modele statuts SCI.docx` | `194E697B21559D926AF48DE2E70FE98DC4042B13CE53CC1FD7F25F4C3B2916A3` |
| SCI IRIS | `project/source_import/raw_drive_dump/Creation SCI/Statuts/Modele statuts SCI IRIS.docx` | `project/source_documents/lot_04/Modele statuts SCI IRIS.docx` | `2007638667394238387E2C8A92E8ABA497BF2C02539AF30F78BEB8746679E19A` |
| SCM | `project/source_import/raw_drive_dump/creation scm/Statuts SCM.docx` | `project/source_documents/lot_04/Statuts SCM.docx` | `4A4DE4383A4D1E7E1E890F64D69D2D1086C742C7EF80D867E46ED2A35CF76991` |
| SAS | `project/source_import/raw_drive_dump/Creation SAS/Statuts/STATUTS_SAS_SPFPL_medecins_modele.docx` | `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx` | `40F8D64E7053289F95A78DD87B967527605BB13E49254516D1FAE311C2E4BE84` |

Note : les chemins ci-dessus sont normalises sans accents pour la lisibilite. Les fichiers physiques conservent leurs noms exacts sur disque.

## Statuts manquants

Aucun statut n'est manquant pour le perimetre cite explicitement par le ticket :
- SELARL chirurgien-dentiste ;
- SELARL medecin ;
- SELAS medecin ;
- SPFPL cession ;
- SPFPL apport ;
- SCS ;
- SCI ;
- SCI IRIS ;
- SCM ;
- SAS.

## Variantes trouvees mais non copiees

Ces fichiers existent dans le dump brut mais ne sont pas retenus dans cette preparation HIGH :

| Fichier | Raison de non-copie |
|---|---|
| `project/source_import/raw_drive_dump/Creation SELARL/Documents de base/Statuts/Modele statuts SELARL Kine (1) - transforme.docx` | profession hors perimetre courant |
| `project/source_import/raw_drive_dump/Creation SPFPL/Statuts/STATUTS SAS SPFPL medecins - transforme.docx` | variante SPFPL/SAS non referencee comme source cible du ticket |
| `project/source_import/raw_drive_dump/Creation SPFPL/Statuts/Statuts SAS SPFPL pharmaciens - transforme.docx` | profession hors perimetre courant |
| `project/source_import/raw_drive_dump/Creation SPFPL/Statuts/Statuts_SPFPLAS_dentistes_apport_modele.docx` | variante proche de SPFPL apport, hash distinct de la source retenue |
| `project/source_import/raw_drive_dump/Creation SCS/Statuts_SCSS_SYDEL_modele.docx` | variante SCS non citee par la source de verite |
| `project/source_import/raw_drive_dump/Creation SCS/SCS_modele_chenal_modele.docx` | variante SCS a qualifier avant tout usage |
| `project/source_import/raw_drive_dump/Creation SCP/Modele Statuts SCP - transforme.docx` | SCP hors perimetre courant |
| `project/source_import/raw_drive_dump/statuts SASU Holding - transforme.docx` | SASU Holding hors perimetre courant |

## Familles clairement separables

1. Statuts SEL d'exercice :
   - SELARL chirurgien-dentiste ;
   - SELARL medecin ;
   - SELAS medecin.

2. Statuts SPFPL :
   - SPFPL cession ;
   - SPFPL apport.

3. Statuts civiles :
   - SCS ;
   - SCI ;
   - SCI IRIS ;
   - SCM.

4. Statuts SAS :
   - SAS.

## Risques de non-fusion

- Les statuts changent de sens selon la forme juridique : SELARL, SELAS, SPFPL, SCS, SCI, SCM et SAS ne doivent pas etre fusionnes par similarite de nom.
- Les variantes SELARL chirurgien-dentiste et SELARL medecin peuvent contenir des clauses ordinales et professionnelles distinctes.
- SELARL et SELAS appartiennent a une meme grande famille SEL, mais leur gouvernance et leurs formulations statutaires ne sont pas interchangeables.
- SPFPL cession et SPFPL apport doivent rester separees : l'operation initiale modifie potentiellement la logique capitalistique, les apports et les documents satellites.
- SCI et SCI IRIS ne doivent pas etre dedupliquees automatiquement : `SCI IRIS` peut etre une variante nominative ou metier qui necessite une analyse dediee.
- SCS a plusieurs variantes dans le dump ; seule `Statuts_SCS_modele.docx` est retenue ici car elle correspond au referentiel.
- SCM porte une logique de moyens et de depenses communes qui ne doit pas etre rapprochee des SCI/SCS.
- SAS est exposee par un fichier dont le nom contient aussi `SPFPL_medecins`; ce point doit etre verifie en spec avant tout codage.
- Les fichiers `modele`, `transforme` et copies proches peuvent diverger juridiquement meme lorsque les noms semblent proches.

## Ordre recommande de traitement

1. `SPEC-STATUTS-SEL-001` - Statuts SEL d'exercice : commencer par SELARL chirurgien-dentiste, SELARL medecin, puis SELAS medecin. Cette sous-famille est la plus connectee aux blocs deja presents : ordre, regime communautaire, cession et derogations.
2. `SPEC-STATUTS-SPFPL-001` - Statuts SPFPL : traiter cession et apport ensemble en comparaison, mais conserver deux sorties documentaires tant que la fusion n'est pas prouvee.
3. `SPEC-STATUTS-CIVILES-001` - Statuts civiles : traiter SCI et SCI IRIS en premier, puis SCM, puis SCS. Cette famille doit surtout verifier les variables capital, associes, siege, objet et options type IS.
4. `SPEC-STATUTS-SAS-001` - Statuts SAS : traiter apres les familles ci-dessus, avec attention particuliere a la liste des souscripteurs et a l'attestation sur le capital, qui restent une famille distincte non stabilisee.

## Prochaine etape recommandee

Ouvrir un ticket de specification, pas de code, pour `SPEC-STATUTS-SEL-001`.

Ce prochain ticket doit :
- lire les trois sources SEL copiees dans `project/source_documents/lot_04/` ;
- extraire les placeholders et zones variables ;
- comparer les clauses SELARL chirurgien-dentiste, SELARL medecin et SELAS medecin ;
- produire une spec canonique et une spec texte avant toute implementation.
