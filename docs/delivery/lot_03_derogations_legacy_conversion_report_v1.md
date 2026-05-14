# DAAT x SYDEL - RAPPORT DE CONVERSION LEGACY V1
## Famille `derogations`

## 1. Objet

Ce rapport documente le traitement du fichier legacy :

- `Demande_derogation_cumul_SELARL_salariee.doc`

Conclusion V1 :
- aucune conversion locale fiable en DOCX propre n'a ete produite ;
- aucun fichier `project/source_documents/lot_03/Demande_derogation_cumul_SELARL_salariee.docx` n'est livre par ce ticket ;
- le futur code de la sous-famille `cumul_salariee` reste bloque tant qu'une source DOCX propre n'est pas fournie ou qu'une conversion fiable n'est pas validee.

## 2. Source legacy identifiee

Source raw dump :

- `project/source_import/raw_drive_dump/Creation SELAS/Derogation/Demande_derogation_cumul_SELARL_salariee.doc`

Controle source :

| Fichier | Taille | SHA256 |
|---|---:|---|
| `Demande_derogation_cumul_SELARL_salariee.doc` | 21504 | `F5CA40CAA9116C52C7AC10FAAEDB08272D8747D30D53DA2CA51300F5F63594CF` |

## 3. Conversion locale testee

Outils locaux verifies :

- `Word.Application` COM : disponible ;
- `LibreOffice` / `OpenOffice` / `soffice` : non trouve localement ;
- `pandoc` : non trouve localement ;
- `antiword` / `catdoc` : non trouves localement.

Tentative effectuee :

- ouverture du `.doc` via `Word.Application` COM ;
- conversion par `SaveAs2(..., wdFormatXMLDocument)` vers `.docx` ;
- Word lance en mode invisible, lecture seule, alertes desactivees.

Resultat :

- la commande a expire apres 120 secondes ;
- aucun DOCX cible n'a ete produit ;
- le processus Word residue a ete arrete ;
- aucun fichier temporaire utile n'a ete conserve dans `project/source_documents/lot_03/`.

## 4. Motif de blocage

La conversion n'est pas consideree fiable, car :

- le flux Word COM ne s'est pas termine ;
- l'absence d'outil de conversion headless fiable empeche une conversion reproductible ;
- aucun DOCX obtenu ne peut etre relu, compare ou valide contre le wording source ;
- le ticket interdit de bricoler une conversion approximative.

## 5. Impact documentaire

Sous-famille impactee :

- `cumul_salariee`

Statut :

- source legacy lue et localisee ;
- source executable non disponible ;
- code interdit tant qu'un DOCX propre n'est pas livre et valide.

Action recommandee :

- fournir une version DOCX propre du fichier legacy depuis Word en session humaine controlee, ou installer un convertisseur headless fiable puis relancer une conversion avec comparaison des placeholders et du texte source.
