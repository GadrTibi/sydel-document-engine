# Rapport doublons sources V1

## Objet
Ce rapport repare le prerequis documentaire manquant pour `ARBITRAGE-SOURCES-001`.

Il documente les doublons exacts et les collisions probables entre :
- `project/source_import/raw_drive_dump/`
- `project/source_documents/`

Aucune deduplication physique n'a ete effectuee.

## Regles appliquees
- Un doublon exact est un groupe de fichiers avec le meme hash SHA-256.
- Un doublon probable est une collision de nom apres neutralisation du bruit de nommage autorise :
  - `copie`, `copie de`, suffixes `(1)`, `(2)`, underscores, accents, casse, doubles espaces.
- Les mots metier sensibles restent discriminants :
  - structure juridique ;
  - profession ;
  - cession / apport ;
  - associe unique / plusieurs associes ;
  - transforme / modele.
- Le contexte de dossier prime sur le seul nom de fichier.

## Synthese

| Indicateur | Nombre |
|---|---:|
| Groupes de doublons exacts | 15 |
| Fichiers inclus dans des doublons exacts | 42 |
| Groupes de doublons probables par nom/contexte | 18 |
| Fichiers inclus dans ces collisions probables | 66 |

Le nombre retenu pour le suivi "doublons probables" est **18 groupes**.

## Doublons exacts principaux

| Groupe | Fichiers | Decision |
|---|---|---|
| Autorisation de domiciliation Lot 1 | `Création SAS/Document de base/Autorisation de domiciliation - transforme.docx` ; `source_documents/lot_01/autorisation_domiciliation_transforme.docx` | deja couvert par Lot 1 |
| Autorisation de domiciliation SELAS/SPFPL | `Création SELAS/Documents de base/Autorisation de domiciliation.docx` ; `Création SPFPL/apport/Documents de base/Copie de Autorisation de domiciliation.docx` ; `Création SPFPL/cession spfpl/Documents de base/Autorisation de domiciliation.docx` | rapprochement exact possible, mais pas de fusion inter-familles sans spec |
| Declaration de non-condamnation Lot 1 | `Création SAS/Document de base/Declaration sur l_honneur de non condamnation - transforme.docx` ; `source_documents/lot_01/declaration_non_condamnation_transforme.docx` | deja couvert par Lot 1 |
| Declaration SCP/SCS | `Création SCP/Déclaration sur l_honneur de non condamnation - transforme.docx` ; `Création SCS/Déclaration sur l_honneur de non condamnation - transforme.docx` | SCP hors perimetre ; SCS a ne pas fusionner automatiquement |
| Declaration SPFPL | trois copies SPFPL apport / cession / racine | copies exactes, mais contexte dossier a conserver |
| Procuration Lot 1 | `Création SAS/Document de base/Procuration - transforme.docx` ; `source_documents/lot_01/procuration_transforme.docx` | deja couvert par Lot 1 |
| Procuration SCS/SPFPL | quatre copies SCS/SPFPL | copies exactes, contexte dossier a conserver |
| PV nomination gerant | `Création SCI/PV nomination gérant - transforme.docx` ; `source_documents/lot_02/PV nomination gérant - transforme.docx` | source canonique deja retenue en Lot 2 |
| Demande d'inscription a l'ordre SPFPL | trois copies SPFPL + `source_documents/lot_02/Demande d_inscription à l_ordre - transforme.docx` | exact, mais famille globale bloquee avant comparaison SELARL/SELAS/SPFPL |
| Regime communautaire - avertissement | SELAS + SPFPL apport + SPFPL cession + SPFPL cession/apport + `source_documents/lot_02` | copies exactes rapprochables ; variantes SELARL non identiques a arbitrer |
| Regime communautaire - renonciation | SELAS + SPFPL apport + SPFPL cession + SPFPL cession/apport + `source_documents/lot_02` | copies exactes rapprochables ; variantes SELARL non identiques a arbitrer |
| Compromis cabinet medical | SELAS + SPFPL cession copie | exact, mais profession/cession a conserver |
| Compromis cabinet dentaire | SELAS + SPFPL cession copie `(1)` | exact, mais profession/cession a conserver |
| PDF 2672 | SELARL + SELAS | hors moteur courant |
| Variables SELARL | `Création SELARL/variables.csv` ; `Création SELARL/scm cession/variables.csv` | donnees support, pas un document moteur |

## Collisions probables a ne pas fusionner automatiquement

| Famille / collision | Risque |
|---|---|
| Statuts | variantes structure, profession, `SCI IRIS`, `SPFPL cession`, `SPFPL apport`, SAS/SCS/SCM ; aucune dedup automatique |
| Autorisation de domiciliation | documents proches mais contextes SELARL/SELAS/SAS/SCI/SCM/SCS/SPFPL/SCP ; ne pas fusionner par nom seul |
| Declaration de non-condamnation | documents proches mais contextes et sources deja retenues a respecter |
| Procuration | plusieurs copies exactes ou proches ; garder le contexte dossier |
| PV nomination gerant | la source Lot 2 retenue reste canonique ; SELARL/SELAS/SCS/SCM/SCP restent references ou hors perimetre selon le cas |
| Demande d'inscription a l'ordre | variantes SELARL / SELAS / SPFPL non comparees ; choix canonique bloque |
| Regime communautaire renonciation | copies exactes SELAS/SPFPL rapprochables ; variante SELARL distincte |
| Regime communautaire avertissement | copies exactes SELAS/SPFPL rapprochables ; variante SELARL distincte |
| Liste des souscripteurs / Attestation sur le capital | famille ambigue ; ne pas placer automatiquement |
| Compromis cabinet medical/dentaire | copies exactes entre SELAS/SPFPL mais profession et contexte cession restent discriminants |
| Kine / pharmaciens / SCP / SASU Holding / RM Sydel / PDF 2672 | hors moteur courant |

## Conclusion
Les doublons exacts peuvent servir a confirmer qu'un fichier est deja represente dans `source_documents`, mais ils ne suffisent pas a creer une famille canonique.

Les familles bloquees doivent etre arbitrees par spec documentaire avant tout placement ou codage.

