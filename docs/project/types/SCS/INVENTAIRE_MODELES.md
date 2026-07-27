# SCS — Inventaire des modèles

Date : 2026-06-07
Branche : `sprint/engine-completion`
Périmètre : sourcing + cartographie + prompts NotebookLM uniquement. **Aucun code, aucun commit.**

## Origine

Modèles copiés depuis le Drive :
`C:/Users/Gad/Downloads/Documents avec variables-20260604T122837Z-3-001/Documents avec variables/Création SCS/`
vers `project/source_documents/scs/`.

4 modèles trouvés (tous `.docx`, lisibles par `python-docx`, **aucun `.doc` legacy** à signaler).
Dédoublonnés : les 4 fichiers ont des noms et contenus distincts (pas de doublon).

> Note importante : `project/source_documents/scs/Statuts_SCS_modele.docx` est **strictement identique**
> (même MD5 `43abe567778697758390275848d7acdc`) à `project/source_documents/lot_04/Statuts_SCS_modele.docx`
> déjà utilisé par le moteur (générateur `DOC-019 / generate_statuts_scs`). Le moteur s'appuie donc
> déjà sur l'un des 4 modèles du Drive. Les 3 autres modèles n'ont **pas** encore de source dans le repo.

## Tableau des modèles

| Modèle (fichier) | Variables `[...]` (nombre) | Ce que le doc paraît être |
| --- | --- | --- |
| `Statuts_SCS_modele.docx` | 60 | **Statuts SCS à capital variable**, 2 personnes physiques : associé commandité (personne_1) + associé commanditaire (personne_2, ici une épouse). Capital variable (minimal + maximal). 2 tables (répartition des parts). **C'est le modèle déjà câblé dans le moteur (DOC-019).** |
| `Statuts_SCSS_SYDEL_modele.docx` | 39 | **Statuts SCS « SYDEL »**, capital fixe. Associé **commanditaire = une société** (holding, `*_societe_associe_1`) + associé **commandité = personne physique** (personne_1). Préambule explicite sur la logique commandité/commanditaire (investisseur vs gestion). « SCSS » = vraisemblablement SCS avec **société** commanditaire. |
| `SCS_modele_chenal_modele.docx` | 52 | **Statuts SCS « Chenal »**, capital fixe. Mixte : associé **commanditaire = société** (`*_societe_associe_1`) **+ une 2e personne physique commanditaire** (personne_1) et associé **commandité = personne physique** (personne_2). Préambule confidentialité des comptes. Variante du modèle SYDEL à 3 associés. |
| `RM_Sydel_SCS_modele.docx` | 19 | **Rapport de mission** (document de conseil / lettre de mission patrimoniale), pas un acte statutaire. Décrit la SCS (art. L.222-1 à L.222-11 C. com.), minimum 2 associés (1 commandité + 1 commanditaire), régime fiscal, seuils CAC. **Contient un artefact de copier-coller : une phrase mentionne « Société Civile Immobilière » au lieu de SCS** (résidu d'un RM SCI — à signaler, wording à corriger côté métier). |

## Lecture transverse des variables

Familles de variables communes aux 3 modèles de statuts :
- Société : `[denomination_societe]`, `[forme_sociale]`, `[capital_social]`, `[capital_lettres]`,
  `[adresse_siege]`, `[ville_rcs]`, `[duree_societe]`, `[valeur_nominale_part]` (+ `_lettres`),
  `[nb_parts_total]` / `[nb_parts_total_lettres]`, `[date_cloture_exercice_1]`,
  `[nom_banque]`, `[adresse_banque]`, `[lieu_signature]`, `[date_signature]`.
- Personne physique : `[civilite_personne_N]`, `[prenom_personne_N]`, `[nom_personne_N]`,
  `[date_naissance_personne_N]`, `[ville_naissance_personne_N]`, `[nationalite_personne_N]`,
  `[adresse_personne_N]`, `[situation_maritale_personne_N]`, `[qualite_associe_personne_N]`,
  `[apport_personne_N]` (+ `_lettres`), `[nb_parts_lettres_personne_N]`, `[plage_parts_personne_N]`.
- Société associée (commanditaire holding, modèles SYDEL & Chenal) :
  `[denomination_societe_associe_1]`, `[forme_sociale_societe_associe_1]`,
  `[capital_social_societe_associe_1]`, `[adresse_siege_societe_associe_1]`,
  `[numero_rcs_societe_associe_1]`, `[ville_rcs_societe_associe_1]`,
  `[fonction_representant_societe_associe_1]`, `[apport_societe_associe_1]` (+ `_lettres`),
  `[nb_parts_lettres_societe_associe_1]`, `[plage_parts_societe_associe_1]`,
  `[qualite_associe_societe_1]`.

Variables propres au modèle **capital variable** (`Statuts_SCS_modele`) :
`[capital_social_maximal]` (+ `_lettres`), `[total_apports_commandites]`,
`[apport_commanditaire_personne_2]` (+ `_lettres`), `[plage_parts_total]`,
`[nb_parts_lettres_societe_associe_1]`, `[parts_societe_associe_1]`.

Variables propres au **rapport de mission** (`RM_Sydel_SCS_modele`) :
`[civilite_client]`, `[prenom_client]`, `[nom_client]`, `[date_naissance]`,
`[regime_matrimonial]`, `[residence_fiscale]`, `[enfants_a_charge]`,
`[revenus_annuels_nets]`, `[charges_annuelles]`, `[patrimoine_global]`,
`[montant_ir]`, `[montant_ifi]`, `[objectifs_client]`, `[rappel_situation_client]`,
`[adresse_cabinet]`, `[cp_ville_cabinet]`, `[denomination_cabinet_mandataire]`.

## Constat structurant pour la cartographie

Les 3 modèles de statuts ne décrivent **pas le même montage d'associés** :

| Modèle | Commandité(s) | Commanditaire(s) | Capital |
| --- | --- | --- | --- |
| `Statuts_SCS_modele` | 1 personne physique | 1 personne physique | **variable** |
| `Statuts_SCSS_SYDEL_modele` | 1 personne physique | 1 société (holding) | fixe |
| `SCS_modele_chenal_modele` | 1 personne physique | 1 société + 1 personne physique | fixe |

C'est un point d'arbitrage métier (quel(s) montage(s) la V1 doit-elle générer) — voir
`NOTEBOOKLM_PROMPTS_V2.md` et `STATUT.md`.
