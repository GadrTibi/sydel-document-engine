# SCP — Inventaire des modèles tokenisés (V1)

> **Statut : FONDATION (sources).** Ce document recense les modèles `.docx`/`.doc` réellement
> présents pour le type **SCP** (le dossier Drive est nommé « Création SCP »). Il décrit **ce que le
> fichier EST** d'après ses variables et son contenu — **PAS** dans quel cas il s'assemble (la carte
> officielle cas → documents est **MANQUANTE**, cf. `CARTOGRAPHIE_TENTATIVE.md`).
> Aucun wording inventé. `dérivé` ≠ `confirmé`. Date : 2026-06-05.

## Provenance

- **Source Drive (lecture seule) :**
  `C:\Users\Gad\Downloads\Documents avec variables-20260604T122837Z-3-001\Documents avec variables\Création SCP\`
- **Copiés (NFC, dédupliqués par md5) dans :** `project/source_documents/scp/`
- **5 modèles `.docx`** copiés + `variables_source_scp.csv` (réf. des variables fournie avec le lot Drive,
  d'origine `variables_utilisees_par_document.csv`).
- **Aucun doublon octet-pour-octet** (hash MD5 distinct sur chaque fichier) ; **aucun doublon NFC/NFD** de nom.
- **2 fichiers Drive NON copiés** (cf. § « Non récupérés ») : 1 `.doc` legacy + 1 `.pdf`.
- Tokens extraits par **scan XML complet** (les `[token]` fragmentés sur plusieurs runs sont récupérés ;
  l'extraction paragraphe-par-paragraphe sous-compte — piège connu Sydel).

## Tableau modèle → variables tokenisées → nature présumée

| Modèle (nom dans `source_documents/scp/`) | Nb tokens | Variables tokenisées | Ce que le document paraît être (1 phrase) |
|---|---|---|---|
| `Modèle Statuts SCP - transforme.docx` | 48 | `[adresse_banque]`, `[adresse_personne_1]`, `[adresse_personne_2]`, `[apport_lettres_personne_1]`, `[apport_lettres_personne_2]`, `[apport_personne_1]`, `[apport_personne_2]`, `[capital_social]`, `[civilite_personne_1]`, `[civilite_personne_2]`, `[cp_siege]`, `[date_naissance_personne_1]`, `[date_naissance_personne_2]`, `[date_signature]`, `[debut_exercice]`, `[denomination_societe]`, `[duree_societe]`, `[fin_exercice]`, `[forme_sociale]`, `[lieu_signature]`, `[nationalite_personne_1]`, `[nationalite_personne_2]`, `[nb_parts_lettres_personne_1]`, `[nb_parts_lettres_personne_2]`, `[nb_parts_personne_1]`, `[nb_parts_personne_2]`, `[nb_parts_total]`, `[nom_banque]`, `[nom_naissance_personne_1]`, `[nom_personne_1]`, `[nom_personne_2]`, `[nom_signataire_1]`, `[num_voie_siege]`, `[numero_part_debut_personne_1]`, `[numero_part_debut_personne_2]`, `[numero_part_fin_personne_1]`, `[numero_part_fin_personne_2]`, `[pays_naissance_personne_1]`, `[prenom_personne_1]`, `[prenom_personne_2]`, `[prenom_signataire_1]`, `[situation_maritale_personne_1]`, `[situation_maritale_personne_2]`, `[valeur_nominale_part]`, `[ville_naissance_personne_1]`, `[ville_naissance_personne_2]`, `[ville_siege]`, `[voie_siege]` | Statuts constitutifs d'une société civile à **2 associés personnes physiques** (capital, apports, répartition des parts, durée, exercice social). **⚠️ L'objet social décrit une société de PORTEFEUILLE / participations (« prise de participation… détention, gestion d'un portefeuille de titres… à l'exclusion de toute opération commerciale »), PAS l'exercice en commun d'une profession** — ce n'est pas la trame classique d'une « Société Civile **Professionnelle** » d'exercice. Ambiguïté majeure : cf. `CARTOGRAPHIE_TENTATIVE.md` et Bloc 1 des prompts. |
| `Fiche de création de Société Civile - transforme.docx` | 77 | `[adresse_banque]`, `[adresse_personne_1..5]`, `[capital_social]`, `[cp_siege]`, `[date_cloture_exercice]`, `[date_cloture_exercice_1]`, `[date_naissance_personne_1..5]`, `[denomination_societe]`, `[email_personne_1..5]`, `[forme_sociale]`, `[nationalite_personne_1..5]`, `[nom_banque]`, `[nom_gerant_1]`, `[nom_gerant_2]`, `[nom_mere_personne_1..5]`, `[nom_pere_personne_1..5]`, `[nom_personne_1..5]`, `[num_voie_siege]`, `[parts_personne_1..5]`, `[prenom_gerant_1]`, `[prenom_gerant_2]`, `[prenom_personne_1..5]`, `[repartition_capital]`, `[situation_maritale_personne_1..5]`, `[statut_residence_personne_1]`, `[telephone_personne_1..5]`, `[ville_naissance_personne_1..5]`, `[ville_siege]`, `[voie_siege]` | Fiche récapitulative de création d'une **société civile** (formulaire de collecte). **Supporte jusqu'à 5 associés** (`_personne_1..5`) et **2 gérants** (`_gerant_1/_gerant_2`) — la borne haute du type est ici, pas dans les statuts (qui n'exposent que 2 personnes). À confirmer : livrable client ou outil interne ? |
| `Autorisation de domiciliation - transforme.docx` | 11 | `[capital_social]`, `[civilite]`, `[cp_siege]`, `[date_signature]`, `[denomination_societe]`, `[lieu_signature]`, `[nom]`, `[num_voie_siege]`, `[prenom]`, `[ville_siege]`, `[voie_siege]` | Autorisation de domiciliation du siège (trame **commune**, identique à celle des SEL/SCM). |
| `Déclaration sur l_honneur de non condamnation - transforme.docx` | 13 | `[civilite]`, `[cp_perso]`, `[date_naissance]`, `[date_signature]`, `[lieu_signature]`, `[nationalite]`, `[nom]`, `[nom_mere]`, `[nom_pere]`, `[num_voie_perso]`, `[prenom]`, `[ville_perso]`, `[voie_perso]` | Déclaration sur l'honneur de non-condamnation (trame **commune**). |
| `procuration - transforme.docx` | 15 | `[civilite_personne_2]`, `[cp_perso]`, `[cp_siege]`, `[date_signature]`, `[denomination_societe]`, `[fonction_dirigeant]`, `[lieu_signature]`, `[nom_personne_2]`, `[num_voie_perso]`, `[num_voie_siege]`, `[prenom_personne_2]`, `[ville_perso]`, `[ville_siege]`, `[voie_perso]`, `[voie_siege]` | Procuration (probable mandat aux formalités SYDEL). Utilise `_personne_2` (et non `[nom]/[prenom]` génériques) — variante par rapport à la procuration SCM. |

## Modèles Drive NON récupérés (à re-fournir / convertir)

| Fichier Drive | Pourquoi non copié | Action |
|---|---|---|
| `PV nomination gérant - transforme.doc` | **`.doc` legacy** (OLE/Word97, magic `D0CF11E0`), non tokenisable par `python-docx` → tokens non extraits. | Reconvertir en `.docx` tokenisé. **C'est le PV de nomination du/des gérant(s) de la société civile** (variables connues via le CSV Drive : `[date_pv]`, `[heure_reunion]`, `[date_reunion_lettres]`, `[montant_emprunt]`, `[cp_bien]`/`[ville_bien]`/`[voie_bien]`/`[num_voie_bien]`, `[departement_naissance_personne_2]`, `[ville_rcs]`, + identité personnes 1/2). La présence de `[montant_emprunt]` et d'une adresse de **bien** suggère un PV mixant nomination **et** acquisition/emprunt — **à vérifier** (Bloc 4). |
| `SCP IR Note assistance à la déclaration - transforme.pdf` | **PDF**, pas un modèle DOCX tokenisable ; « IR » = vraisemblablement impôt sur le revenu (note d'assistance à la déclaration fiscale). | Hors périmètre génération DOCX a priori ; **confirmer** si c'est un livrable à produire ou une simple note d'aide. |

## Notes de fidélité / pièges relevés

1. **⚠️ « SCP » ≠ Société Civile Professionnelle d'exercice (le piège n°1 du wording).** Le dossier
   Drive s'appelle « Création SCP », mais l'objet social des statuts est celui d'une **société civile de
   portefeuille / détention de participations** (`forme_sociale` tokenisé, objet = participations/titres,
   « à l'exclusion de toute opération commerciale »). Avant tout code : faire **trancher la nature réelle
   du type** (SCP professionnelle ? société civile de moyens patrimoniale ? holding civile ?) — Bloc 1.
2. **Borne du nombre d'associés incohérente entre modèles** : la **Fiche de création** prévoit **5
   associés** et **2 gérants** ; les **Statuts** n'exposent que **2 associés** tokenisés. La modélisation
   devra gérer N associés ; le nombre canonique est à confirmer (Bloc 1).
3. **`forme_sociale` est une variable** (pas figée) dans Statuts/Fiche/PV → le type couvre peut-être
   plusieurs formes de société civile sous une même trame. À clarifier (Bloc 1 / Bloc 4).
4. **`duree_societe` est une variable** (pas figée) dans les statuts — contraste avec la SELARL où la
   durée société est figée (99 ans). À confirmer : variable libre ou valeur canonique (Bloc 4).
5. **Modèles « communs »** (`Autorisation de domiciliation`, `Déclaration… non condamnation`) :
   trames partagées déjà présentes pour SELARL/SCM. **Ne pas dupliquer la couche partagée** au moment du
   moteur — réutiliser le générateur commun + mapping SCP si nécessaire.
6. **`médecin` apparaît dans les statuts** mais **sans coquille inter-profession** : c'est une clause
   neutre (« constat par un médecin d'une incapacité du gérant à exprimer sa volonté »). Pas à purger.
7. **`variables_source_scp.csv`** liste **123 variables** par document (colonne `source_documents`). C'est
   un **dictionnaire de référence du lot**, à recouper avec les tokens réellement extraits ci-dessus ; ne
   pas le traiter comme un contrat de génération.
