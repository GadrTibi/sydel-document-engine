# DAAT x SYDEL - SPEC CANONIQUE V1
## Batch satellites SCM

## 1. Objet

Specifier le batch documentaire satellite du chemin `SCM` avant tout codage.

Ticket : `SPEC-SCM-SATELLITES-001`.
Date : 2026-05-15.

Cette spec couvre uniquement les quatre satellites SCM inventoriés dans la source de vérité :
- `Pacte d_associes SCM.docx` ;
- `Liste depenses communes SCM.doc` ;
- `CONTRAT FRAIS COMMUNS.docx` ;
- `REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx`.

Elle ne code rien, ne modifie aucun wording juridique source et ne modifie aucun fichier de pilotage partagé.

Documents explicitement hors périmètre :
- `Statuts SCM.docx`, traité dans le lot statuts civils ;
- PV nomination gérant ;
- demande d'inscription à l'ordre ;
- déclaration de non-condamnation, autorisation de domiciliation et procuration ;
- fiche de création SCM ;
- documents de cession de parts SCM ;
- toute variante non sourcée des satellites SCM.

## 2. Sources lues

Mémoire projet et référentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md` en lecture seule
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md` en lecture seule
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_05_scm_satellites_preparation_v1.md`
- `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`

ADR applicables :
- ADR-0001 : source de vérité documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : génération DOCX propre from-scratch pour les futurs tickets code ;
- ADR-0005 : mode Codex repo-first.

Source de vérité métier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources documentaires lues :
- `project/source_documents/lot_05/Pacte d_associes SCM.docx`
- `project/source_documents/lot_05/Liste depenses communes SCM.doc`
- `project/source_documents/lot_05/CONTRAT FRAIS COMMUNS.docx`
- `project/source_documents/lot_05/REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx`

Note de lecture :
- les chemins ci-dessus sont normalisés sans accents pour la lisibilité ;
- les fichiers physiques peuvent contenir des accents décomposés ;
- `Liste depenses communes SCM.doc` a pu être lu en lecture seule via Word COM pour inventaire textuel, mais son format legacy `.doc` reste bloquant avant toute analyse fine de mise en page ou automatisation.

## 3. Périmètre documentaire V1

Dans la source de vérité, le chemin `SCM` comprend notamment :
- statuts SCM ;
- PV nomination gérant ;
- demande d'inscription à l'ordre ;
- documents universels ;
- pacte d'associés SCM ;
- liste des dépenses communes ;
- contrat de frais communs ;
- règlement intérieur de la société civile de moyens.

La présente spec isole uniquement les quatre satellites SCM.

Identifiants de travail proposés, sans attribution catalogue définitive :

| Identifiant de travail | Document canonique | Source |
|---|---|---|
| `SCM-PACTE-ASSOCIES` | Pacte d'associés portant sur les parts sociales de la SCM | `Pacte d_associes SCM.docx` |
| `SCM-LISTE-DEPENSES-COMMUNES` | Liste des dépenses communes SCM | `Liste depenses communes SCM.doc` |
| `SCM-CONTRAT-FRAIS-COMMUNS` | Contrat d'exercice professionnel à frais communs | `CONTRAT FRAIS COMMUNS.docx` |
| `SCM-REGLEMENT-INTERIEUR` | Règlement intérieur de la SCM | `REGLEMENT INTERIEUR DE LA SOCIETE CIVILE DE MOYENS - SCM DES DOCTEURS XX.docx` |

Décisions V1 :
- les quatre documents sont distincts et ne doivent pas être fusionnés avec les statuts SCM ;
- aucun satellite ne doit être injecté comme annexe ou clause complémentaire des statuts SCM ;
- le pacte, le contrat et le règlement intérieur sont sensibles juridiquement et doivent conserver le texte source sauf validation explicite ;
- la liste des dépenses communes reste bloquée pour automatisation tant qu'une conversion DOCX propre ou une source DOCX équivalente n'est pas reçue.

## 4. Cycle documentaire

| Document | Inventorié | Source reçue | Analysé | Spécifié | Prêt à coder |
|---|---:|---:|---:|---:|---:|
| Pacte d'associés SCM | oui | oui, DOCX | oui | oui | non, points ouverts à arbitrer |
| Liste dépenses communes SCM | oui | oui, legacy `.doc` | partiel | oui, avec blocage `.doc` | non, conversion requise |
| Contrat frais communs | oui | oui, DOCX | oui | oui | non, points ouverts à arbitrer |
| Règlement intérieur SCM | oui | oui, DOCX | oui | oui | non, points ouverts à arbitrer |

## 5. Conditions de sélection futures

Condition commune minimale :
- `dossier.structure == SCM`

Condition de sécurité recommandée :
- les statuts SCM ou le dossier SCM doivent être validés comme cohérents avec les satellites ;
- le batch satellites doit être explicitement demandé ou activé par le contexte dossier ;
- les données des parties, associés, représentants, locaux et signatures doivent être complètes ;
- aucun document ne doit être généré depuis une source `.doc` legacy non convertie.

### 5.1 Pacte d'associés SCM

Sélection future :
- `dossier.structure == SCM`
- `dossier.options.scm_satellites == true`
- `scm_satellites.pacte_associes == true`
- deux associés historiques identifiés en V1.

Règles de blocage :
- bloquer si plus de deux associés historiques doivent être rendus ;
- bloquer si les associés sont des personnes morales sans wording source dédié dans les comparutions ;
- bloquer si `societe.nb_parts_total`, `societe.numero_rcs` ou `ville_tribunal` est absent ;
- bloquer si le pacte doit être adapté à une version sans clause de non-concurrence, sans préemption ou avec une gouvernance différente.

### 5.2 Liste dépenses communes SCM

Sélection future :
- `dossier.structure == SCM`
- `dossier.options.scm_satellites == true`
- `scm_satellites.liste_depenses_communes == true`
- source convertie en DOCX propre ou remplacement validé.

Règles de blocage :
- bloquer tant que la source disponible reste uniquement `Liste depenses communes SCM.doc` ;
- bloquer si la table des dépenses doit devenir dynamique sans spec de table validée ;
- bloquer si plus de deux signataires doivent être affichés ;
- bloquer si la clé de répartition doit différer des colonnes source.

### 5.3 Contrat frais communs

Sélection future :
- `dossier.structure == SCM`
- `dossier.options.scm_satellites == true`
- `scm_satellites.contrat_frais_communs == true`
- deux parties contractantes identifiées en V1.

Règles de blocage :
- bloquer si plus de deux parties sont fournies ;
- bloquer si l'adresse de la seconde partie ne correspond pas aux locaux communs alors que la source utilise `[adresse_locaux]` ;
- bloquer si la description fixe des locaux dentaires n'est pas adaptée au dossier ;
- bloquer si la répartition des dépenses doit différer du prorata du temps d'occupation des salles de soin.

### 5.4 Règlement intérieur SCM

Sélection future :
- `dossier.structure == SCM`
- `dossier.options.scm_satellites == true`
- `scm_satellites.reglement_interieur == true`
- deux sociétés ou associés parties et deux praticiens identifiés en V1.

Règles de blocage :
- bloquer si plus de deux parties ou praticiens doivent être rendus ;
- bloquer si les deux parties n'ont pas la même forme sociale alors que la source utilise un placeholder unique `[forme_sociale]` ;
- bloquer si `seuil_depense_commune`, `annee_reference_charges`, `date_fin_gestion_administrative` ou `date_attribution_responsabilites` est absent ;
- bloquer si les clauses de téléphone, départ, temps partiel ou rupture d'association doivent être supprimées ou réécrites.

## 6. Variables canoniques communes

Les placeholders sources ne deviennent pas la vérité du moteur. Les variables ci-dessous prolongent les rôles déjà retenus dans les specs existantes et dans les arbitrages SCM.

### 6.1 Dossier

- `dossier.structure`
- `dossier.options.scm`
- `dossier.options.scm_satellites`
- `scm_satellites.pacte_associes`
- `scm_satellites.liste_depenses_communes`
- `scm_satellites.contrat_frais_communs`
- `scm_satellites.reglement_interieur`

### 6.2 Société SCM

Rôle canonique :
- `societe`

Variables :
- `societe.denomination`
- `societe.forme_juridique`
- `societe.capital_social`
- `societe.siege.adresse_affichee`
- `societe.ville_rcs`
- `societe.numero_rcs`
- `societe.nb_parts_total`

### 6.3 Associés historiques

Rôle canonique :
- `associes[]`

Variables V1 :
- `associes[].civilite_affichage`
- `associes[].prenom`
- `associes[].nom`
- `associes[].signature_libelle`
- `associes[].parts.nb`

Décision V1 :
- les sources pacte et liste stabilisent deux associés affichés avec les placeholders `personne_1` et `personne_2` ;
- `personne_1` et `personne_2` restent des aliases documentaires, non des rôles canoniques.

### 6.4 Parties aux frais communs et au règlement intérieur

Rôle canonique local :
- `parties_frais_communs[]`

Variables par partie :
- `societe.denomination`
- `societe.forme_juridique`
- `societe.capital_social`
- `societe.siege.adresse_affichee`
- `societe.ville_rcs`
- `societe.numero_rcs`
- `representant.civilite_affichage`
- `representant.prenom`
- `representant.nom`
- `representant.identite_affichee`
- `representant.titre_affichage`
- `representant.fonction`

Décision V1 :
- le contrat et le règlement intérieur sont stabilisés sur deux parties ;
- aucune liste dynamique de parties n'est automatisée en V1.

### 6.5 Praticiens et locaux

Rôles canoniques locaux :
- `praticiens[]`
- `locaux`

Variables :
- `praticiens[].identite_affichee`
- `praticiens[].telephone`
- `locaux.adresse_affichee`

### 6.6 Paramètres documentaires locaux

Rôles canoniques locaux :
- `pacte_associes`
- `frais_communs`
- `reglement_interieur`

Variables :
- `pacte_associes.ville_tribunal`
- `frais_communs.date_effet_contrat`
- `reglement_interieur.seuil_depense_commune`
- `reglement_interieur.annee_reference_charges`
- `reglement_interieur.date_fin_gestion_administrative`
- `reglement_interieur.date_attribution_responsabilites`

### 6.7 Signature

Rôle canonique :
- `signature`

Variables :
- `signature.lieu`
- `signature.date`
- `signature.nombre_exemplaires`

## 7. Mapping placeholders source

### 7.1 Pacte d'associés SCM

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | société SCM |
| `[forme_sociale]` | `societe.forme_juridique` | source utilisée aussi dans l'acte d'adhésion |
| `[capital_social]` | `societe.capital_social` | capital |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | siège complet |
| `[ville_rcs]` | `societe.ville_rcs` | RCS |
| `[numero_rcs]` | `societe.numero_rcs` | RCS |
| `[nb_parts_sociales]` | `societe.nb_parts_total` | parts sociales totales |
| `[civilite_personne_1]` | `associes[0].civilite_affichage` | associé historique 1 |
| `[prenom_personne_1]` | `associes[0].prenom` | associé historique 1 |
| `[nom_personne_1]` | `associes[0].nom` | associé historique 1 |
| `[civilite_personne_2]` | `associes[1].civilite_affichage` | associé historique 2 |
| `[prenom_personne_2]` | `associes[1].prenom` | associé historique 2 |
| `[nom_personne_2]` | `associes[1].nom` | associé historique 2 |
| `[ville_tribunal]` | `pacte_associes.ville_tribunal` | clause de juridiction |
| `[lieu_signature]` | `signature.lieu` | clôture |
| `[date_signature]` | `signature.date` | clôture |

### 7.2 Liste dépenses communes SCM

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | en-tête |
| `[forme_sociale]` | `societe.forme_juridique` | en-tête |
| `[capital_social]` | `societe.capital_social` | en-tête |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | en-tête |
| `[ville_rcs]` | `societe.ville_rcs` | société en cours d'immatriculation |
| `[prenom_personne_1]` | `associes[0].prenom` | signature |
| `[nom_personne_1]` | `associes[0].nom` | signature |
| `[prenom_personne_2]` | `associes[1].prenom` | signature |
| `[nom_personne_2]` | `associes[1].nom` | signature |

Blocage spécifique :
- source legacy `.doc`, donc mapping textuel seulement ; la structure Word/table doit être confirmée par conversion avant code.

### 7.3 Contrat frais communs

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe_1]` | `parties_frais_communs[0].societe.denomination` | partie 1 |
| `[forme_sociale_societe_1]` | `parties_frais_communs[0].societe.forme_juridique` | partie 1 |
| `[capital_social_societe_1]` | `parties_frais_communs[0].societe.capital_social` | partie 1 |
| `[adresse_siege_societe_1]` | `parties_frais_communs[0].societe.siege.adresse_affichee` | partie 1 |
| `[ville_rcs_societe_1]` | `parties_frais_communs[0].societe.ville_rcs` | partie 1 |
| `[numero_rcs_societe_1]` | `parties_frais_communs[0].societe.numero_rcs` | partie 1 |
| `[civilite_representant_societe_1]` | `parties_frais_communs[0].representant.civilite_affichage` | partie 1 |
| `[prenom_representant_societe_1]` | `parties_frais_communs[0].representant.prenom` | partie 1 |
| `[nom_representant_societe_1]` | `parties_frais_communs[0].representant.nom` | partie 1 |
| `[fonction_representant_societe_1]` | `parties_frais_communs[0].representant.fonction` | partie 1 |
| `[denomination_societe_2]` | `parties_frais_communs[1].societe.denomination` | partie 2 |
| `[forme_sociale_societe_2]` | `parties_frais_communs[1].societe.forme_juridique` | partie 2 |
| `[capital_social_societe_2]` | `parties_frais_communs[1].societe.capital_social` | partie 2 |
| `[ville_rcs_societe_2]` | `parties_frais_communs[1].societe.ville_rcs` | partie 2 |
| `[numero_rcs_societe_2]` | `parties_frais_communs[1].societe.numero_rcs` | partie 2 |
| `[civilite_representant_societe_2]` | `parties_frais_communs[1].representant.civilite_affichage` | partie 2 |
| `[prenom_representant_societe_2]` | `parties_frais_communs[1].representant.prenom` | partie 2 |
| `[nom_representant_societe_2]` | `parties_frais_communs[1].representant.nom` | partie 2 |
| `[fonction_representant_societe_2]` | `parties_frais_communs[1].representant.fonction` | partie 2 |
| `[adresse_locaux]` | `locaux.adresse_affichee` | locaux communs et siège affiché partie 2 |
| `[date_effet_contrat]` | `frais_communs.date_effet_contrat` | prise d'effet |
| `[lieu_signature]` | `signature.lieu` | clôture |
| `[date_signature]` | `signature.date` | clôture |

### 7.4 Règlement intérieur SCM

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | SCM |
| `[denomination_societe_1]` | `parties_frais_communs[0].societe.denomination` | partie 1 |
| `[denomination_societe_2]` | `parties_frais_communs[1].societe.denomination` | partie 2 |
| `[forme_sociale]` | `parties_frais_communs[].societe.forme_juridique` | placeholder unique, blocage si formes différentes |
| `[capital_social_societe_1]` | `parties_frais_communs[0].societe.capital_social` | partie 1 |
| `[capital_social_societe_2]` | `parties_frais_communs[1].societe.capital_social` | partie 2 |
| `[adresse_siege_societe_1]` | `parties_frais_communs[0].societe.siege.adresse_affichee` | partie 1 |
| `[adresse_siege_societe_2]` | `parties_frais_communs[1].societe.siege.adresse_affichee` | partie 2 |
| `[ville_rcs_societe_1]` | `parties_frais_communs[0].societe.ville_rcs` | partie 1 |
| `[ville_rcs_societe_2]` | `parties_frais_communs[1].societe.ville_rcs` | partie 2 |
| `[numero_rcs_societe_1]` | `parties_frais_communs[0].societe.numero_rcs` | partie 1 |
| `[numero_rcs_societe_2]` | `parties_frais_communs[1].societe.numero_rcs` | partie 2 |
| `[titre_representant_societe_1]` | `parties_frais_communs[0].representant.titre_affichage` | partie 1 |
| `[titre_representant_societe_2]` | `parties_frais_communs[1].representant.titre_affichage` | partie 2 |
| `[identite_representant_societe_1]` | `parties_frais_communs[0].representant.identite_affichee` | partie 1 |
| `[identite_representant_societe_2]` | `parties_frais_communs[1].representant.identite_affichee` | partie 2 |
| `[fonction_representant_societe_1]` | `parties_frais_communs[0].representant.fonction` | partie 1 |
| `[fonction_representant_societe_2]` | `parties_frais_communs[1].representant.fonction` | partie 2 |
| `[adresse_locaux]` | `locaux.adresse_affichee` | locaux communs |
| `[seuil_depense_commune]` | `reglement_interieur.seuil_depense_commune` | seuil de dépense |
| `[annee_reference_charges]` | `reglement_interieur.annee_reference_charges` | annexe tableau de répartition |
| `[date_fin_gestion_administrative]` | `reglement_interieur.date_fin_gestion_administrative` | gestion administrative |
| `[date_attribution_responsabilites]` | `reglement_interieur.date_attribution_responsabilites` | gestion administrative |
| `[identite_praticien_1]` | `praticiens[0].identite_affichee` | clauses téléphone/départ |
| `[identite_praticien_2]` | `praticiens[1].identite_affichee` | clauses téléphone/départ |
| `[telephone_praticien_1]` | `praticiens[0].telephone` | message téléphonique |
| `[telephone_praticien_2]` | `praticiens[1].telephone` | message téléphonique |
| `[lieu_signature]` | `signature.lieu` | clôture |
| `[date_signature]` | `signature.date` | clôture |

## 8. Structure canonique des documents

### 8.1 Pacte d'associés SCM

Blocs source :
- titre du pacte ;
- comparution des deux associés historiques ;
- présence de la société SCM ;
- préambule ;
- Titre I : objet, définitions, déclarations ;
- Titre II : modalités relatives aux cessions de titres ;
- Titre III : gouvernance de la société ;
- Titre IV : départ d'un associé ;
- Titre V : droit d'information ;
- Titre VI : stipulations spécifiques ;
- dispositions générales ;
- règlement des différends ;
- signature ;
- Annexe 1 statuts de la société ;
- Annexe 2 acte d'adhésion.

Décision V1 :
- le document source stabilise deux associés historiques ;
- les annexes sont conservées comme blocs textuels du document source, sans injection des statuts.

### 8.2 Liste dépenses communes SCM

Blocs source :
- en-tête société ;
- table des dépenses communes ;
- deux colonnes de clé de répartition : prorata des parts de SCM et prorata chiffre d'affaires ;
- signatures de deux personnes.

Décision V1 :
- le document reste bloqué pour code tant que la source `.doc` n'est pas convertie ou remplacée ;
- la table est considérée fixe en V1, non pilotée par une liste dynamique.

### 8.3 Contrat frais communs

Blocs source :
- titre contrat d'exercice professionnel à frais communs ;
- comparution de deux parties ;
- articles 1 à 8 ;
- description des locaux ;
- table des dépenses communes au prorata du temps d'occupation des salles de soin ;
- liste des dépenses professionnelles personnelles ;
- prise d'effet ;
- résiliation, remplacement, départ, litiges et contre-lettre ;
- signature.

Décision V1 :
- le document est limité à deux parties ;
- la description des locaux et les catégories de dépenses sont fixes sauf arbitrage.

### 8.4 Règlement intérieur SCM

Blocs source :
- titre règlement intérieur de la SCM ;
- comparution de deux parties ;
- préambule ;
- article 1 : objet et durée ;
- article 2 : déontologie et exercice ;
- article 3 : gestion du cabinet ;
- article 4 : moyens mis en commun ;
- article 5 : absence des associés ;
- article 6 : assurance ;
- article 7 : exclusion ;
- article 8 : litiges ;
- article 9 : communication ;
- article 10 : clauses particulières ;
- autonomie des clauses ;
- signature en quatre exemplaires.

Décision V1 :
- le document source stabilise deux parties et deux praticiens ;
- le tableau de répartition des charges et les clauses de séparation restent fixes.

## 9. Blocs conditionnels et blocages

### 9.1 Blocs communs

Blocs fixes :
- textes juridiques sources ;
- tableaux de dépenses ;
- clauses de litige, contre-lettre, confidentialité ou autonomie ;
- signatures selon la structure source.

Blocs conditionnels non automatisés en V1 :
- associés ou parties multiples au-delà de deux ;
- adaptation à une profession autre que celle implicite des sources ;
- réécriture des clés de répartition ;
- suppression ou ajout de clauses ;
- annexes dynamiques.

### 9.2 Blocages communs

Un futur générateur doit bloquer si :
- le dossier n'est pas `SCM` ;
- un satellite est demandé depuis le générateur de statuts SCM ;
- le rendu final conserverait un placeholder `[` ou `]` ;
- une donnée obligatoire de société, partie, associé, représentant, praticien, local ou signature est absente ;
- le contexte impose une variation de wording non validée ;
- la cohérence entre statuts SCM et satellites n'est pas vérifiable.

## 10. Éléments manuels

Éléments à fournir par contexte dossier, saisie contrôlée ou arbitrage :
- activation exacte des satellites à produire ;
- confirmation des deux associés historiques du pacte ;
- confirmation des deux parties aux frais communs ;
- représentants, titres et fonctions des sociétés parties ;
- identités et téléphones des praticiens ;
- adresse complète des locaux ;
- seuil de dépense commune ;
- année de référence des charges ;
- dates de gestion administrative ;
- date d'effet du contrat de frais communs ;
- ville du tribunal compétent pour le pacte ;
- lieu et date de signature ;
- nombre d'exemplaires si une valeur différente de la source est souhaitée ;
- conversion ou remplacement de la source `.doc`.

Ces éléments ne doivent pas être inventés par le moteur.

## 11. Cohérence inter-documents

Les satellites SCM doivent rester cohérents avec les statuts SCM sur :
- `societe.denomination` ;
- `societe.forme_juridique` ;
- `societe.capital_social` ;
- `societe.siege.adresse_affichee` ;
- `societe.ville_rcs` ;
- `societe.numero_rcs` ;
- `associes[]` ;
- parts sociales et associés historiques lorsque ces données sont affichées.

Règle :
- toute divergence entre statuts SCM, pacte, liste, contrat et règlement intérieur doit bloquer un futur rendu automatique.

## 12. Critères avant implémentation

Un ticket de code pourra démarrer seulement si :
- le document cible est explicitement l'un des quatre satellites ou le batch complet ;
- la source `.doc` de la liste des dépenses communes est convertie ou remplacée ;
- la V1 limitée à deux associés ou deux parties est acceptée ;
- les tables de dépenses sont confirmées comme fixes ou une spec de table dynamique est ajoutée ;
- les données des représentants, praticiens, locaux et dates sont fournies par contexte ;
- la cohérence avec les statuts SCM est contrôlable ;
- aucun DOCX source n'est utilisé comme template d'exécution ;
- les tests futurs vérifient l'absence de placeholders `[` / `]` ;
- aucun wording juridique n'est modifié hors arbitrage documenté.

## 13. Points ouverts

1. **Blocage `.doc`** : `Liste depenses communes SCM.doc` doit être converti en DOCX propre ou remplacé avant code.
2. **Activation du batch** : confirmer si les quatre satellites sont générés par défaut pour tout dossier SCM ou uniquement sur option.
3. **Deux associés / parties uniquement** : les sources stabilisent deux personnes ou parties ; aucune dynamique N n'est sourceée pour ces satellites.
4. **Pacte d'associés** : confirmer la validité des clauses de préemption, non-concurrence, inaliénabilité et sortie conjointe pour tous dossiers SCM.
5. **Annexes du pacte** : confirmer le traitement de l'Annexe 1 statuts et de l'Annexe 2 acte d'adhésion.
6. **Liste dépenses** : confirmer les colonnes de répartition et les lignes sans marque `X`, notamment `Achat validé par la SCM`.
7. **Contrat frais communs** : confirmer que la description fixe des locaux dentaires est applicable.
8. **Adresse de la partie 2 au contrat** : la source utilise `[adresse_locaux]` comme siège affiché de la seconde partie.
9. **Règlement intérieur** : le placeholder unique `[forme_sociale]` est utilisé pour deux parties ; bloquer si les formes sociales diffèrent.
10. **Docteur / praticien** : confirmer les formules affichées dans le règlement intérieur pour les professions non médicales ou non dentaires.
11. **Téléphone et séparation** : confirmer si les clauses de message téléphonique et d'organisation du départ doivent rester systématiques.
12. **Nombre d'exemplaires** : le règlement intérieur fixe quatre exemplaires ; confirmer si cette valeur est constante.

## 14. Statut

`SPEC-SCM-SATELLITES-001` est stabilisé côté canonique pour les satellites SCM V1, sans code Python.

Prochaine étape recommandée :
- arbitrer les points ouverts 1, 2, 3, 4, 5, 7, 9 et 10 avant tout ticket de code.
