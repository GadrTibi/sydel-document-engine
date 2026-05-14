# Manifest import sources V1

## Objet
Ce manifest repare le prerequis documentaire manquant pour le ticket `ARBITRAGE-SOURCES-001`.

Il inventorie en lecture seule :
- `project/source_import/raw_drive_dump/`
- `project/source_documents/`

Aucun fichier source n'a ete deplace, supprime ou renomme dans ce ticket.

## Methode de scan
- Scan recursif de tous les fichiers.
- Releve du chemin relatif, extension, taille et hash SHA-256.
- Normalisation de nom uniquement pour l'analyse documentaire :
  - accents ignores ;
  - `_` et espaces rapproches ;
  - casse ignoree ;
  - bruit `copie`, `copie de`, suffixes `(1)`, `(2)` neutralise.
- Les mots metier suivants ne sont pas neutralises automatiquement :
  - `SELARL`, `SELAS`, `SAS`, `SCI`, `SCI IRIS`, `SCM`, `SCS`, `SPFPL`, `SCP`, `SASU` ;
  - `medecin`, `dentiste`, `kine`, `pharmacien` ;
  - `cession`, `apport`, `associe unique`, `plusieurs associes`, `transforme`, `modele`.

## Synthese chiffree

| Zone scannee | Nombre de fichiers |
|---|---:|
| `project/source_import/raw_drive_dump/` | 147 |
| `project/source_documents/` | 11 |

### Extensions observees dans `raw_drive_dump`

| Extension | Nombre |
|---|---:|
| `.docx` | 125 |
| `.doc` | 8 |
| `.csv` | 7 |
| `.pdf` | 3 |
| `.xlsx` | 1 |
| sans extension / systeme | 3 |

### Inventaire par famille documentaire observee dans `raw_drive_dump`

| Famille observee | Nombre | Note |
|---|---:|---|
| Statuts | 17 | variantes de structures, professions et apports/cessions ; pas de dedup automatique |
| Autorisation de domiciliation | 10 | tronc commun, plusieurs contextes dossier |
| Declaration de non-condamnation | 10 | tronc commun, plusieurs contextes dossier |
| Actes de cession | 10 | variantes cabinet / parts / SPFPL |
| Procuration | 9 | tronc commun, plusieurs contextes dossier |
| Variables / donnees | 8 | CSV/XLSX, hors placement documentaire direct |
| Compromis de cession | 8 | medical / dentaire / kine, copies et variantes |
| PV nomination gerant | 7 | source canonique deja retenue en Lot 2 ; autres versions references |
| Documents a qualifier finement | 7 | voir section "documents sans source claire" |
| Derogation / site distinct | 6 | certains documents a remplir a la main |
| Attestation capital / liste souscripteurs | 5 | famille ambigue, pas de placement automatique |
| Demande d'inscription a l'ordre | 5 | variantes SELARL / SELAS / SPFPL a comparer |
| Regime communautaire - renonciation | 5 | copies exactes + variantes SELARL non identiques |
| Regime communautaire - avertissement | 5 | copies exactes + variantes SELARL non identiques |
| Avenant bail | 3 | SELARL / SELAS / SCM |
| Appel de fonds | 3 | SEL / SPFPL, variantes |
| Liste des souscripteurs | 3 | liee a l'ambiguite attestation capital |
| Note d'information | 3 | SPFPL, copies et variantes |
| Fiches de creation | 2 | hors moteur courant |
| RM Sydel | 2 | hors moteur courant |
| PDF 2672 | 2 | hors moteur courant |
| Attestation commissaire aux apports | 2 | SPFPL apport / cession + apport |
| Contrat d'apport | 2 | SPFPL apport / cession + apport |
| Courrier SDE | 2 | SELARL / SELAS |
| PV AGE cession SCM | 2 | SELARL / SELAS |
| Contrat frais communs | 1 | SCM |
| Liste depenses communes | 1 | SCM |
| Option IS | 1 | SCI |
| Pacte associes SCM | 1 | SCM |
| PV remuneration president | 1 | SAS |
| Reglement interieur SCM | 1 | SCM |
| Fichiers systeme `.DS_Store` | 3 | hors documentation |

## Etat observe de `project/source_documents/`

| Chemin | Statut observe |
|---|---|
| `project/source_documents/lot_01/autorisation_domiciliation_transforme.docx` | source Lot 1 deja presente |
| `project/source_documents/lot_01/declaration_non_condamnation_transforme.docx` | source Lot 1 deja presente |
| `project/source_documents/lot_01/procuration_transforme.docx` | source Lot 1 deja presente |
| `project/source_documents/lot_02/PV nomination gérant - transforme.docx` | source canonique PV nomination gerant deja presente |
| `project/source_documents/lot_02/Demande d_inscription à l_ordre - transforme.docx` | present physiquement ; famille a comparer avant choix canonique |
| `project/source_documents/lot_02/Lettre de renonciation a revendiquer la qualite d_associe - SELAS.docx` | present physiquement ; variante regime communautaire a arbitrer |
| `project/source_documents/lot_02/Lettre d_avertissement au conjoint en cas d_apport d_un bien commun - transforme.docx` | present physiquement ; variante regime communautaire a arbitrer |
| `project/source_documents/lot_02/README.md` | README de lot |
| `project/source_documents/lot_03/README.md` | README de lot |
| `project/source_documents/lot_04/README.md` | README de lot |
| `project/source_documents/lot_05/README.md` | README de lot |

## Documents sans source claire ou sans famille canonique stabilisee

Ces fichiers existent dans `raw_drive_dump`, mais ne doivent pas etre places automatiquement faute de famille canonique stabilisee ou de source de verite claire pour le moteur courant :

| Chemin | Blocage |
|---|---|
| `project/source_import/raw_drive_dump/Création SCS/Liste_souscripteurs_modele.docx` | famille liste des souscripteurs / attestation capital ambigue |
| `project/source_import/raw_drive_dump/Création SCS/SCS_modele_chenal_modele.docx` | variante SCS a qualifier avant statuts |
| `project/source_import/raw_drive_dump/Création SELAS/Documents de base/PV associé unique nomination Directeur Général - transforme.doc` | famille PV distincte du PV nomination gerant |
| `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/PV agrément cession/PV SELARL agrément cession SPFPL - SELARL 1 associé.docx` | PV agrement cession SPFPL a specifier separement |
| `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/PV agrément cession/PV SELARL agrément cession SPFPL - SELARL plusieurs associés - transforme.docx` | variante plusieurs associes a comparer |
| `project/source_import/raw_drive_dump/Création SPFPL/cession spfpl/PV SPFPL autorisation empruntt - transforme.doc` | PV autorisation emprunt SPFPL a qualifier |

Nombre de documents sans source claire pour placement automatique : **6**.

## Documents hors perimetre moteur courant

Les decisions metier excluent du moteur courant les familles suivantes :
- SCP ;
- SASU Holding ;
- kine ;
- pharmaciens ;
- fiches de creation ;
- RM Sydel ;
- PDF 2672.

Nombre de documents sources hors perimetre identifies dans `raw_drive_dump` : **16**.

