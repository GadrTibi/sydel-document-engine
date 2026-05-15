# DAAT x SYDEL - SPEC CANONIQUE V1
## Batch satellites SAS

## 1. Objet

Specifier le batch documentaire satellite du chemin `SAS` avant tout codage.

Ticket : `SPEC-SAS-SATELLITES-001`.
Date : 2026-05-15.

Cette spec couvre uniquement les deux documents satellites SAS inventoriés dans la source de vérité :
- `PV remuneration president - transforme.docx` ;
- `Attestation sur le capital - apport - liste des souscripteurs.docx`.

Elle ne code rien, ne modifie aucun wording juridique source et ne modifie aucun fichier de pilotage partagé.

Documents explicitement hors périmètre :
- statuts SAS, déjà spécifiés séparément ;
- documents universels déjà traités séparément ;
- demande d'inscription à l'ordre ;
- PV nomination gérant ;
- tout document marqué à remplir à la main ;
- toute variante SAS générique ou multi-actionnaires non sourcée.

## 2. Sources lues

Mémoire projet et référentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_sas_spec_canonique_v1.md`
- `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`

ADR applicables :
- ADR-0001 : source de vérité documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : génération DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

Source de vérité métier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources documentaires lues :
- `project/source_import/raw_drive_dump/Creation SAS/PV remuneration president - transforme.docx`
- `project/source_documents/lot_05/Attestation sur le capital - apport - liste des souscripteurs.docx`

Constat de placement :
- le PV rémunération président n'est pas présent dans `project/source_documents/lot_05/` et a donc été lu dans `project/source_import/raw_drive_dump/` ;
- l'attestation sur le capital / liste des souscripteurs est présente dans `project/source_documents/lot_05/` ;
- la source de vérité liste deux fois l'attestation dans le chemin `SAS`, comme `Attestation sur le capital` puis comme `liste des souscripteurs Attestation sur le capital`.

## 3. Périmètre documentaire V1

Dans la source de vérité, le chemin `SAS` comprend :
- statuts : `STATUTS_SAS_SPFPL_medecins_modele.docx` ;
- documents universels ;
- attestation sur le capital / liste des souscripteurs ;
- PV rémunération président.

La présente spec isole les satellites des statuts SAS.

Identifiants de travail proposés, sans attribution catalogue définitive :

| Identifiant de travail | Document canonique | Source |
|---|---|---|
| `SAS-PV-REMUNERATION-PRESIDENT` | PV de décision de l'associé unique fixant l'absence de rémunération du président | `PV remuneration president - transforme.docx` |
| `SAS-ATTESTATION-CAPITAL-SOUSCRIPTEURS` | Attestation sur le capital / liste des souscripteurs | `Attestation sur le capital - apport - liste des souscripteurs.docx` |

Décision V1 :
- les deux documents sont distincts et ne doivent pas être fusionnés avec les statuts ;
- le batch reste centré sur la source SAS disponible, qui est cohérente avec une constitution unipersonnelle ;
- les listes dynamiques d'associés ou de souscripteurs restent hors automatisation V1 sans arbitrage.

## 4. Cycle documentaire

| Document | Inventorié | Source reçue | Analysé | Spécifié | Prêt à coder |
|---|---:|---:|---:|---:|---:|
| PV rémunération président | oui | oui, depuis raw dump | oui | oui | non, points ouverts à arbitrer |
| Attestation capital / liste des souscripteurs | oui | oui, dans `lot_05` | oui | oui | non, points ouverts à arbitrer |

## 5. Conditions de sélection futures

Condition commune minimale :
- `dossier.structure == SAS`

Condition de sécurité recommandée, alignée avec les specs statuts SAS :
- le périmètre SAS doit être confirmé comme `SAS / SPFPL medecins` ou équivalent métier validé ;
- la constitution doit être unipersonnelle ;
- le président doit être l'actionnaire unique en V1.

### 5.1 PV rémunération président

Sélection future :
- `dossier.structure == SAS`
- `dossier.options.associe_unique == true`
- `president.ref_associe_index == 0`
- `remuneration_president.type == absence_remuneration`

Règles de blocage :
- bloquer si plusieurs associés ou actionnaires sont fournis ;
- bloquer si le président n'est pas l'actionnaire unique ;
- bloquer si une rémunération positive, variable ou différée doit être rédigée ;
- bloquer si la société n'est pas en cours d'immatriculation ;
- bloquer si la fonction dirigeante ou le genre impose une variation non sourcée du wording.

### 5.2 Attestation sur le capital / liste des souscripteurs

Sélection future :
- `dossier.structure == SAS`
- `capital_souscription.mode == apport` ou décision métier équivalente ;
- `capital_souscription.souscripteurs[]` contient une seule entrée en V1.

Règles de blocage :
- bloquer si plusieurs souscripteurs sont demandés ;
- bloquer si aucun apport en nature n'est fourni alors que la source rend le bloc `Apports en nature` ;
- bloquer si le capital, le nombre d'actions ou la valeur nominale divergent des statuts SAS ;
- bloquer si le wording doit devenir numéraire-only sans validation explicite.

## 6. Variables canoniques communes

Les placeholders sources ne deviennent pas la vérité du moteur. Les variables ci-dessous prolongent les rôles déjà utilisés dans les specs statuts SAS et SPFPL.

### 6.1 Dossier

- `dossier.structure`
- `dossier.options.associe_unique`
- `dossier.options.apport`

### 6.2 Société en constitution

Rôle canonique :
- `societe`

Variables :
- `societe.denomination`
- `societe.forme_juridique`
- `societe.capital_social`
- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.cp`
- `societe.siege.ville`
- `societe.siege.adresse_affichee`
- `societe.ville_rcs`
- `societe.profession`

### 6.3 Actionnaire unique / président

Rôles canoniques :
- `actionnaire_unique`
- `president`

Décision V1 :
- `actionnaire_unique` et `president` désignent la même personne ;
- `president.ref_associe_index == 0`.

Variables :
- `actionnaire_unique.civilite_affichage`
- `actionnaire_unique.prenom`
- `actionnaire_unique.nom`
- `actionnaire_unique.profession`
- `actionnaire_unique.qualite_associe`
- `actionnaire_unique.adresse_personnelle.num_voie`
- `actionnaire_unique.adresse_personnelle.voie`
- `actionnaire_unique.adresse_personnelle.ville`
- `actionnaire_unique.adresse_personnelle.cp`
- `actionnaire_unique.adresse_personnelle_affichee`
- `president.civilite_affichage`
- `president.prenom`
- `president.nom`
- `president.fonction`
- `president.adresse_personnelle_affichee`

### 6.4 Exercice social et rémunération

Rôles canoniques :
- `exercice_social`
- `remuneration_president`

Variables :
- `exercice_social.date_cloture_premier_exercice`
- `remuneration_president.type`
- `remuneration_president.date_fin_non_remuneree`

Décision V1 :
- la source couvre uniquement une absence de rémunération jusqu'à la clôture du premier exercice ;
- `remuneration_president.date_fin_non_remuneree` doit rester cohérente avec `exercice_social.date_cloture_premier_exercice`.

### 6.5 Capital / souscription

Rôle canonique :
- `capital_souscription`

Variables :
- `capital_souscription.nb_actions_total`
- `capital_souscription.valeur_nominale_action`
- `capital_souscription.apports_nature_montant`
- `capital_souscription.apports_numeraire_montant`
- `capital_souscription.souscripteurs[]`
- `capital_souscription.repartition_actions`

Variables par souscripteur :
- `civilite_affichage`
- `prenom`
- `nom`
- `profession`
- `adresse_personnelle_affichee`
- `nb_actions`
- `qualite`

Décision V1 :
- une seule entrée souscripteur est stabilisée par la source ;
- cette entrée correspond à l'actionnaire unique / président.

### 6.6 Apport de titres et société cible

Rôles canoniques :
- `apport_titres`
- `societe_cible`

Variables :
- `apport_titres.nb_parts`
- `societe_cible.forme_sociale`
- `societe_cible.denomination`
- `societe_cible.siege.adresse_affichee`
- `societe_cible.ville_rcs`
- `societe_cible.numero_rcs`

### 6.7 Signature

Rôle canonique :
- `signature`

Variables :
- `signature.lieu`
- `signature.date`
- `signature.nombre_exemplaires`

Décision V1 :
- le PV source fixe `en trois exemplaires` ;
- l'attestation source utilise `[ville_siege]` comme lieu de signature, mais la variable canonique cible reste `signature.lieu`.

## 7. Mapping placeholders source

### 7.1 PV rémunération président

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | en-tête |
| `[forme_sociale]` | `societe.forme_juridique` | source à confirmer sur périmètre SAS / SPFPL |
| `[capital_social]` | `societe.capital_social` | en-tête |
| `[num_voie_siege]` | `societe.siege.num_voie` | siège |
| `[voie_siege]` | `societe.siege.voie` | siège |
| `[cp_siege]` | `societe.siege.cp` | siège |
| `[ville_siege]` | `societe.siege.ville` | siège |
| `[ville_rcs]` | `societe.ville_rcs` | société en cours d'immatriculation |
| `[date_signature]` | `signature.date` | date du PV |
| `[civilite]` | `actionnaire_unique.civilite_affichage` et `president.civilite_affichage` | même personne en V1 |
| `[prenom]` | `actionnaire_unique.prenom` et `president.prenom` | même personne en V1 |
| `[nom]` | `actionnaire_unique.nom` et `president.nom` | même personne en V1 |
| `[num_voie_perso]` | `actionnaire_unique.adresse_personnelle.num_voie` | adresse personnelle |
| `[voie_perso]` | `actionnaire_unique.adresse_personnelle.voie` | adresse personnelle |
| `[ville_perso]` | `actionnaire_unique.adresse_personnelle.ville` | adresse personnelle |
| `[cp_perso]` | `actionnaire_unique.adresse_personnelle.cp` | adresse personnelle |
| `[qualite_associe]` | `actionnaire_unique.qualite_associe` | ex. associé unique / actionnaire unique |
| `[fonction_dirigeant]` | `president.fonction` | fonction dirigeante |
| `[date_cloture_exercice_1]` | `exercice_social.date_cloture_premier_exercice` et `remuneration_president.date_fin_non_remuneree` | fin de non-rémunération |
| `[lieu_signature]` | `signature.lieu` | clôture |

### 7.2 Attestation sur le capital / liste des souscripteurs

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | société en constitution |
| `[capital_social]` | `societe.capital_social` | capital |
| `[profession]` | `societe.profession` ou `actionnaire_unique.profession` selon occurrence | à distinguer au rendu |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | adresse complète |
| `[civilite]` | `president.civilite_affichage` et `actionnaire_unique.civilite_affichage` | même personne en V1 |
| `[prenom]` | `president.prenom` et `actionnaire_unique.prenom` | même personne en V1 |
| `[nom]` | `president.nom` et `actionnaire_unique.nom` | même personne en V1 |
| `[adresse_personnelle]` | `actionnaire_unique.adresse_personnelle_affichee` | souscripteur |
| `[nb_actions]` | `capital_souscription.nb_actions_total` et `capital_souscription.souscripteurs[0].nb_actions` | cohérents en V1 |
| `[valeur_nominale_part]` | `capital_souscription.valeur_nominale_action` | alias source hétérogène, texte parle d'actions |
| `[nb_parts_apportees]` | `apport_titres.nb_parts` | apport en nature |
| `[forme_sociale]` | `societe_cible.forme_sociale` | société dont les titres sont apportés |
| `[denomination_societe_cedee]` | `societe_cible.denomination` | société cible |
| `[adresse_siege_societe_cedee]` | `societe_cible.siege.adresse_affichee` | société cible |
| `[ville_rcs_societe_cedee]` | `societe_cible.ville_rcs` | société cible |
| `[numero_rcs_societe_cedee]` | `societe_cible.numero_rcs` | société cible |
| `[montant_apports_nature]` | `capital_souscription.apports_nature_montant` | apports en nature |
| `[montant_apports_numeraire]` | `capital_souscription.apports_numeraire_montant` | apports en numéraire |
| `[ville_siege]` | `signature.lieu` | source à confirmer, peut correspondre à la ville du siège |
| `[date_signature]` | `signature.date` | signature |

## 8. Structure canonique des documents

### 8.1 PV rémunération président

Blocs source :
- en-tête société ;
- titre `PROCES-VERBAL DES DECISIONS DE L'ASSOCIE UNIQUE` ;
- date de décision ;
- identification de l'associé unique / président ;
- ordre du jour limité à la rémunération du président ;
- décision unique d'absence de rémunération ;
- remboursement possible des frais sur justificatif ;
- clôture et signature.

Décision V1 :
- le document est un PV d'associé unique ;
- il ne couvre pas une assemblée pluripersonnelle ;
- il ne couvre pas une rémunération positive.

### 8.2 Attestation sur le capital / liste des souscripteurs

Blocs source :
- en-tête société ;
- titre `ATTESTATION` ;
- sous-titre `Liste des souscripteurs` ;
- attestation du président ;
- capital social ;
- nombre d'actions et valeur nominale ;
- répartition des actions à l'actionnaire unique ;
- apports en nature ;
- total des apports en nature ;
- apports en numéraire ;
- certification par le président ;
- signature.

Décision V1 :
- le document source stabilise une liste d'un seul souscripteur ;
- le bloc apports en nature est structurel dans la source ;
- la duplication source `attestation` / `liste des souscripteurs` désigne un seul document canonique.

## 9. Blocs conditionnels et blocages

### 9.1 Blocs conditionnels PV

- bloc identité : une seule personne, actionnaire unique et président ;
- bloc décision : uniquement absence de rémunération ;
- date de fin : alignée sur la clôture du premier exercice ;
- signature : nombre d'exemplaires fixé à trois par la source.

Blocages :
- multi-actionnaires ;
- président distinct de l'actionnaire unique ;
- rémunération autre que zéro ;
- société déjà immatriculée ;
- féminisation ou variation grammaticale non validée du pronom `il` ou de la fonction.

### 9.2 Blocs conditionnels attestation

- bloc souscripteur unique ;
- bloc apports en nature ;
- bloc apports en numéraire ;
- certification par le président.

Blocages :
- plusieurs souscripteurs ;
- apports en nature absents ou non structurés ;
- incohérence entre `capital_social`, `nb_actions_total`, `valeur_nominale_action` et montants d'apports ;
- divergence avec les statuts SAS ;
- variante numéraire-only non validée ;
- correction automatique de l'alias source `valeur_nominale_part`.

## 10. Éléments manuels

Éléments à fournir par contexte dossier, saisie contrôlée ou arbitrage :
- confirmation du périmètre `SAS / SPFPL medecins` ;
- qualité affichée de l'associé unique ;
- fonction dirigeante exacte ;
- date de signature du PV ;
- lieu de signature ;
- clôture du premier exercice social ;
- profession affichée dans l'attestation ;
- adresse personnelle affichée du souscripteur ;
- apport en nature détaillé ;
- montant des apports en nature ;
- montant des apports en numéraire ;
- choix de rendu si le lieu de signature de l'attestation doit être différent de la ville du siège ;
- toute variante de genre, nombre ou rémunération.

Ces éléments ne doivent pas être inventés par le moteur.

## 11. Cohérence inter-documents

Les satellites SAS doivent rester cohérents avec les statuts SAS sur :
- `societe.denomination` ;
- `societe.forme_juridique` ;
- `societe.capital_social` ;
- `societe.siege.*` ;
- `societe.ville_rcs` ;
- `actionnaire_unique.*` ;
- `president.*` ;
- `exercice_social.date_cloture_premier_exercice` ;
- `capital_souscription.nb_actions_total` ;
- `capital_souscription.valeur_nominale_action`.

Règle :
- toute divergence entre statuts, PV rémunération et attestation capital doit bloquer un futur rendu automatique.

## 12. Critères avant implémentation

Un ticket de code pourra démarrer seulement si :
- le périmètre SAS source est confirmé comme compatible avec les satellites ;
- la V1 actionnaire unique est acceptée ;
- le président est bien l'actionnaire unique ;
- l'absence de rémunération jusqu'à la clôture du premier exercice est confirmée ;
- l'attestation est confirmée comme document unique malgré la duplication de la source de vérité ;
- le cas apports en nature / apports en numéraire est arbitré ;
- la gestion du genre pour le président est soit validée, soit bloquée explicitement ;
- aucun DOCX source n'est utilisé comme template d'exécution ;
- les tests futurs vérifient l'absence de placeholders `[` / `]` ;
- aucun wording juridique n'est modifié hors arbitrage documenté.

## 13. Points ouverts

1. **Périmètre SAS exact** : les specs statuts SAS signalent un contenu `SPFPL medecins`; confirmer que les satellites suivent le même périmètre.
2. **PV rémunération président** : la source couvre uniquement l'absence de rémunération jusqu'à la clôture du premier exercice.
3. **Genre du président** : la décision source utilise `il`; aucune variante féminine n'est sourceée.
4. **Qualité associé / actionnaire** : `[qualite_associe]` doit être fourni ou arbitré pour éviter une variation locale.
5. **Attestation duplicate** : la source de vérité liste l'attestation et la liste des souscripteurs comme deux libellés proches du même fichier ; confirmer qu'il s'agit d'un seul document à générer.
6. **Liste dynamique** : plusieurs souscripteurs restent hors automatisation V1.
7. **Apports en nature** : le document source impose un bloc d'apport de parts ; une attestation numéraire-only n'est pas sourceée.
8. **Alias `valeur_nominale_part`** : la source emploie ce placeholder alors que le texte parle d'actions ; ne pas corriger le wording sans validation.
9. **Lieu de signature attestation** : `[ville_siege]` doit être confirmé comme `signature.lieu` ou remplacé par une saisie dédiée.

## 14. Statut

`SPEC-SAS-SATELLITES-001` est stabilisé côté canonique pour les satellites SAS V1, sans code Python.

Prochaine étape recommandée :
- arbitrer les points ouverts 1, 2, 3, 5 et 7 avant tout ticket de code.
