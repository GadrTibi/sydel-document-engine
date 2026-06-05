# SAS — Inventaire des modèles tokenisés (V1)

> **Date :** 2026-06-05 · **Portée :** fondation du type **SAS** uniquement.
> **Source Drive (lecture seule) :** `Documents avec variables/Création SAS/`.
> **Copie de travail (déduplication, noms propres) :** `project/source_documents/sas/`.
> Variables = chaînes entre crochets `[...]` réellement présentes dans le DOCX (lues sur le **contenu**, pas le nom).
> Le recoupement avec le CSV fourni par la source (`Création SAS/variables_extraites.csv`, **non copié** — métadonnée, pas un modèle) confirme les 5 documents « de base ».

## Modèles copiés (7)

| Modèle (nom propre dans `source_documents/sas/`) | Nom source Drive | Variables tokenisées | Ce que le document paraît être |
|---|---|---|---|
| `statuts_sas_spfpl_medecins_modele.docx` | `Statuts/STATUTS_SAS_SPFPL_medecins_modele.docx` | `[adresse_personnelle]` `[adresse_siege]` `[capital_lettres]` `[capital_social]` `[civilite]` `[civilite_conjoint]` `[date_cloture_exercice_1]` `[date_naissance]` `[debut_exercice]` `[denomination_societe]` `[departement_naissance]` `[fin_exercice]` `[lieu_signature]` `[nationalite]` `[nb_actions]` `[nb_actions_lettres]` `[nom]` `[nom_banque]` `[nom_conjoint]` `[numero_ordre]` `[numero_rpps]` `[ordre_departemental]` `[prenom]` `[prenom_conjoint]` `[qualification_principale]` `[regime_matrimonial]` `[situation_maritale]` `[valeur_nominale_action]` `[valeur_nominale_action_lettres]` `[ville_naissance]` (30) | Statuts d'une **SAS / SPFPL de médecins par actions simplifiée** ; structure capitalistique en **actions** (pas en parts), bloc conjoint/régime matrimonial présent. C'est le seul vrai « statuts SAS » du corpus. |
| `autorisation_domiciliation_transforme.docx` | `Document de base/Autorisation de domiciliation - transforme.docx` | `[capital_social]` `[civilite]` `[cp_siege]` `[date_signature]` `[denomination_societe]` `[lieu_signature]` `[nom]` `[prenom]` `[ville_siege]` (9) | Autorisation de domiciliation du siège, durée **indéterminée** (cf. piège durée). Document « dans tous les cas ». |
| `declaration_non_condamnation_transforme.docx` | `Document de base/Declaration sur l_honneur de non condamnation - transforme.docx` | `[civilite]` `[cp_perso]` `[date_naissance]` `[date_signature]` `[lieu_signature]` `[nationalite]` `[nom]` `[nom_mere]` `[nom_pere]` `[num_voie_perso]` `[prenom]` `[signature]` `[ville_perso]` `[voie_perso]` (14) | Déclaration sur l'honneur de non-condamnation du dirigeant. Document « dans tous les cas ». |
| `procuration_transforme.docx` | `Document de base/Procuration - transforme.docx` | `[civilite]` `[cp_perso]` `[cp_siege]` `[date_signature]` `[denomination_societe]` `[fonction_dirigeant]` `[forme_sociale]` `[lieu_signature]` `[nom]` `[num_voie_perso]` `[num_voie_siege]` `[prenom]` `[ville_perso]` `[ville_siege]` `[voie_perso]` `[voie_siege]` (16) | Procuration donnée par le dirigeant pour les formalités. Document « dans tous les cas ». |
| `liste_souscripteurs_transforme.docx` | `Document de base/Liste des souscripteurs - transforme.docx` | `[date_signature]` `[denomination_societe]` `[lieu_signature]` `[montant_sous]` `[nb_actions]` `[nom]` `[prenom]` (7) | État des souscriptions (souscripteurs / nombre d'actions / montant souscrit). Variante **courte**. |
| `liste_souscripteurs_variante_copie_transforme.docx` | `Copie de - Liste des souscripteurs - transforme.docx` | `[adresse_personnelle]` `[adresse_siege]` `[capital_social]` `[civilite]` `[date_signature]` `[denomination_societe]` `[forme_sociale]` `[lieu_signature]` `[montant_sous]` `[nb_actions]` `[nom]` `[prenom]` `[profession_reglementee]` `[signature]` (14) | **Variante enrichie** de la liste des souscripteurs (mentions SPFPL « Société de Participations Financières de Profession Libérale de [profession_reglementee] », capital, adresses). **Différente** de la version courte (≠ octets, ≠ tokens) → conservée à part. **Laquelle fait foi ?** = point NotebookLM/Rafael. |
| `pv_remuneration_president_transforme.docx` | `PV remuneration president - transforme.docx` | `[civilite]` `[cp_perso]` `[date_cloture_exercice_1]` `[date_signature]` `[denomination_societe]` `[fonction_dirigeant]` `[lieu_signature]` `[nom]` `[num_voie_perso]` `[prenom]` `[qualite_associe]` `[ville_perso]` `[voie_perso]` (13) | PV / décision relatif à la **rémunération du président** (absence de rémunération jusqu'à clôture du 1er exercice, dans la version Codex). Document spécifique SAS. |

## Modèles SAS-nommés présents sur le Drive mais HORS corpus « Création SAS » (NON copiés — à arbitrer)

Le glob `*SAS*` du Drive remonte aussi ces fichiers, qui **n'appartiennent pas** au dossier `Création SAS` :

| Fichier Drive | Emplacement | Tokens | Statut |
|---|---|---|---|
| `statuts SASU Holding - transforme.docx` | racine `Documents avec variables/` | 27 (`[forme_sociale]`, `[qualite_associe]`, `[nb_actions]`, capital en actions, bloc président…) | **Candidat SAS** plausible (SASU = SAS unipersonnelle / holding). N'est pas dans `Création SAS`. **À confirmer : fait-il partie du type SAS ?** |
| `STATUTS SAS SPFPL médecins - transforme.docx` | `Création SPFPL/Statuts/` | 26 | Range sous le type **SPFPL** par la source (≈ doublon du statuts SAS médecins copié). Hors scope SAS sauf décision contraire. |
| `Statuts SAS SPFPL pharmaciens - transforme.docx` | `Création SPFPL/Statuts/` | 24 | Type **SPFPL** (pharmaciens). Hors scope SAS. |

> **Décision retenue (à valider) :** le corpus du **type SAS** = le dossier `Création SAS` (7 fichiers ci-dessus).
> Les fichiers « SPFPL » à forme SAS relèvent du type **SPFPL** (autre chantier). Le `SASU Holding`
> est mis en attente d'arbitrage. **Aucun fichier hors `Création SAS` n'a été copié.**

## Notes de lecture (à reverser dans le canon une fois confirmées)

- Le corpus SAS est **capitalisé en ACTIONS** (`[nb_actions]`, `[valeur_nominale_action]`), pas en parts
  → divergence structurelle nette avec la SELARL (parts) ; impacte les modèles de données et l'UI.
- Le seul « statuts » du corpus est **SAS / SPFPL médecins** : pas de statuts SAS « pharmaciens » ni
  « dentistes » dans `Création SAS` (ils sont sous `Création SPFPL`). **Le périmètre profession du
  type SAS est donc, en l'état, médecin uniquement** → à confirmer.
- Deux variantes de « Liste des souscripteurs » coexistent (courte vs enrichie SPFPL) → trancher la
  version de référence avant tout générateur fidèle.
