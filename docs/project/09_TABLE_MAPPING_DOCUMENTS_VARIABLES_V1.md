# DAAT x SYDEL — Table de mapping documents -> variables canoniques V1

## Objet

Ce document fixe la couche de correspondance entre :
- les placeholders / zones variables observés dans les documents source ;
- les variables canoniques du moteur.

Il sert à éviter :
- les doublons de saisie UI ;
- les noms divergents pour une même donnée ;
- le codage direct de placeholders locaux (`personne_1`, `personne_2`, etc.) comme vérité du moteur.

## Décisions figées

### 1. Les personnes sont normalisées par rôle métier
On ne garde pas `personne_1`, `personne_2`, etc. comme variables canoniques.

Rôles canoniques principaux :
- `signataire`
- `associes[]`
- `dirigeant_nomine`
- `societe`
- `societe.siege`
- `signature`
- `domiciliation`
- `bien_immobilier`
- `emprunt`

### 2. `civilite_affichage` et `genre` sont distincts
- `civilite_affichage` = donnée d’affichage (`M.`, `Mme`, `Dr`, etc.)
- `genre` = donnée grammaticale (`masculin` / `feminin`)

### 3. Nom canonique retenu pour la domiciliation
Nom canonique retenu :
- `domiciliation.adresse_affichee`

Alias legacy toléré dans le code Lot 1 existant :
- `adresse_domiciliation_affichee`

Règle :
- on ne réutilise plus `adresse_domiciliation_affichee` dans les nouvelles specs ;
- les prochains tickets doivent converger vers `domiciliation.adresse_affichee`.

---

## A. Mapping V1 — Lot 1 déjà codé

### DOC-001 — Déclaration sur l’honneur de non-condamnation

| Source | Variable canonique | Statut |
|---|---|---|
| `[civilite]` | `signataire.civilite_affichage` | canonique |
| accord `Je soussigné / Je soussignée` | `signataire.genre` | canonique |
| `[prenom]` | `signataire.prenom` | canonique |
| `[nom]` | `signataire.nom` | canonique |
| `[date_naissance]` | `signataire.date_naissance` | canonique |
| `[num_voie_perso]` | `signataire.adresse_personnelle.num_voie` | canonique |
| `[voie_perso]` | `signataire.adresse_personnelle.voie` | canonique |
| `[ville_perso]` | `signataire.adresse_personnelle.ville` | canonique |
| `[cp_perso]` | `signataire.adresse_personnelle.cp` | canonique |
| `[nationalite]` | `signataire.nationalite` | canonique |
| `[nom_pere]` | `signataire.filiation.nom_pere` | canonique |
| `[nom_mere]` | `signataire.filiation.nom_mere` | canonique |
| `[lieu_signature]` | `signature.lieu` | canonique |
| `[date_signature]` | `signature.date` | canonique |
| `[signature]` | `signature.image_optionnelle` | canonique |

### DOC-002 — Autorisation de domiciliation

| Source / décision | Variable canonique | Statut |
|---|---|---|
| `[civilite]` | `signataire.civilite_affichage` | canonique |
| accord `Je soussigné / Je soussignée` | `signataire.genre` | canonique |
| `[prenom]` | `signataire.prenom` | canonique |
| `[nom]` | `signataire.nom` | canonique |
| `[denomination_societe]` | `societe.denomination` | canonique |
| `[capital_social]` | `societe.capital_social` | canonique |
| champ libre décidé V1 | `domiciliation.adresse_affichee` | canonique |
| `[lieu_signature]` | `signature.lieu` | canonique |
| `[date_signature]` | `signature.date` | canonique |
| signature finale affichée | `signataire.civilite_affichage`, `signataire.prenom`, `signataire.nom` | canonique |

Note : la source brute étant anormale, le moteur ne mappe pas automatiquement l’adresse depuis `societe.siege` pour DOC-002.

### DOC-003 — Procuration

| Source | Variable canonique | Statut |
|---|---|---|
| `[civilite]` | `signataire.civilite_affichage` | canonique |
| accord `Je soussigné / Je soussignée` | `signataire.genre` | canonique |
| `[prenom]` | `signataire.prenom` | canonique |
| `[nom]` | `signataire.nom` | canonique |
| `[num_voie_perso]` | `signataire.adresse_personnelle.num_voie` | canonique |
| `[voie_perso]` | `signataire.adresse_personnelle.voie` | canonique |
| `[ville_perso]` | `signataire.adresse_personnelle.ville` | canonique |
| `[cp_perso]` | `signataire.adresse_personnelle.cp` | canonique |
| `[fonction_dirigeant]` | `signataire.fonction_dirigeant` | canonique provisoire |
| `[forme_sociale]` | `societe.forme` | canonique |
| `[denomination_societe]` | `societe.denomination` | canonique |
| `[num_voie_siege]` | `societe.siege.num_voie` | canonique |
| `[voie_siege]` | `societe.siege.voie` | canonique |
| `[ville_siege]` | `societe.siege.ville` | canonique |
| `[cp_siege]` | `societe.siege.cp` | canonique |
| `[lieu_signature]` | `signature.lieu` | canonique |
| `[date_signature]` | `signature.date` | canonique |
| signature finale `[prenom] [nom]` | `signataire.prenom`, `signataire.nom` | canonique |

---

## B. Mapping V1 — Préparation du prochain document

### PV nomination gérant — source Lot 2 analysée, non codée

## Décision de méthode
Le document source est lu comme un exemple métier, pas comme un schéma canonique.

Donc :
- `personne_1` et `personne_2` ne sont pas conservés comme vérité du moteur ;
- on remappe vers des rôles canoniques.

### Table de remapping source -> canonique

| Placeholder source | Variable canonique cible | Remarque |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | canonique |
| `[forme_sociale]` | `societe.forme` | à arbitrer avec le texte fixe du document |
| `[capital_social]` | `societe.capital_social` | canonique |
| `[num_voie_siege]` | `societe.siege.num_voie` | canonique |
| `[voie_siege]` | `societe.siege.voie` | canonique |
| `[cp_siege]` | `societe.siege.cp` | canonique |
| `[ville_siege]` | `societe.siege.ville` | canonique |
| `[ville_rcs]` | `societe.rcs_ville` | canonique provisoire |
| `[date_decision]` | `assemblee.date_decision` | canonique provisoire |
| `[date_reunion_lettres]` | `assemblee.date_reunion_lettres` | canonique provisoire |
| `[heure_reunion]` | `assemblee.heure_reunion` | canonique provisoire |
| `[nb_parts]` | `capital.nb_parts_total` | canonique provisoire |
| `[valeur_nominale_part]` | `capital.valeur_nominale_part` | canonique provisoire |
| `[civilite_personne_1]` | `associes[0].civilite_affichage` | document local -> rôle canonique |
| `[prenom_personne_1]` | `associes[0].prenom` | document local -> rôle canonique |
| `[nom_personne_1]` | `associes[0].nom` | document local -> rôle canonique |
| `[nb_parts_personne_1]` | `associes[0].nb_parts` | document local -> rôle canonique |
| `[civilite_personne_2]` | `dirigeant_nomine.civilite_affichage` **ou** `associes[1].civilite_affichage` | dépendra de la spec finale |
| `[prenom_personne_2]` | `dirigeant_nomine.prenom` **ou** `associes[1].prenom` | dépendra de la spec finale |
| `[nom_personne_2]` | `dirigeant_nomine.nom` **ou** `associes[1].nom` | dépendra de la spec finale |
| `[nb_parts_personne_2]` | `associes[1].nb_parts` | canonique si la personne 2 reste aussi associé |
| `[date_naissance_personne_2]` | `dirigeant_nomine.date_naissance` | canonique cible |
| `[ville_naissance_personne_2]` | `dirigeant_nomine.ville_naissance` | canonique cible |
| `[departement_naissance_personne_2]` | `dirigeant_nomine.departement_naissance` | canonique cible |
| `[nationalite_personne_2]` | `dirigeant_nomine.nationalite` | canonique cible |
| `[num_voie_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.num_voie` | canonique cible |
| `[voie_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.voie` | canonique cible |
| `[cp_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.cp` | canonique cible |
| `[ville_perso_personne_2]` | `dirigeant_nomine.adresse_personnelle.ville` | canonique cible |
| `[montant_emprunt]` | `emprunt.montant_max` | canonique provisoire |
| `[num_voie_bien]` | `bien_immobilier.adresse.num_voie` | canonique provisoire |
| `[voie_bien]` | `bien_immobilier.adresse.voie` | canonique provisoire |
| `[cp_bien]` | `bien_immobilier.adresse.cp` | canonique provisoire |
| `[ville_bien]` | `bien_immobilier.adresse.ville` | canonique provisoire |
| `[lieu_signature]` | `signature.lieu` | canonique |
| `[nombre_exemplaires]` | `document.nombre_exemplaires` | champ manuel / canonique local |
| `[fonction_dirigeant]` | `dirigeant_nomine.fonction` | canonique cible |

### Arbitrages encore requis avant codage du PV
- Le document canonique doit-il gérer un nombre dynamique d’associés ?
- Le dirigeant nommé est-il toujours aussi un associé, ou faut-il dissocier les deux rôles ?
- Le texte fixe `société civile immobilière` doit-il rester SCI-only ou être généralisé ?
- Les accords `gérant/gérante` et `né/née` doivent-ils être activés dans cette famille documentaire ?

---

## C. Règles d’utilisation

1. Le dictionnaire canonique est la vérité métier.
2. Les placeholders source ne sont que des repères documentaires.
3. Toute nouvelle spec doit comporter une table de mapping :
   - placeholder source
   - variable canonique
   - règle / note éventuelle
4. Une variable n’est globalisée que si elle est réutilisable ou structurante.
5. Une information ponctuelle peut rester champ manuel, conformément au référentiel.
6. Les prochains tickets doivent converger vers les noms canoniques et non créer de nouvelles variantes locales.

---

## D. Mapping runtime final moteur DOCX V1

Ticket : `RECONCILE-MOTOR-CLOSE-001`

Cette table ferme l'ecart signale par `FINAL-MOTOR-AUDIT-002` : tous les
documents exposes par le catalogue/orchestrateur sont rattaches a des packs de
variables canoniques. Elle ne remplace pas les specs texte/canoniques de
`docs/delivery/`, qui restent la reference champ par champ.

| Document | Packs canoniques principaux |
|---|---|
| `DOC-001` - Declaration non-condamnation | `signataire`, `signataire.adresse`, `signature` |
| `DOC-002` - Autorisation domiciliation | `signataire`, `societe`, `domiciliation`, `signature` |
| `DOC-003` - Procuration | `signataire`, `societe`, `societe.siege`, `signature` |
| `DOC-004` - PV nomination gerant | `societe`, `associes[]`, `dirigeant_nomine`, `decision`, `reunion`, `capital`, `emprunt`, `bien_immobilier`, `signature` |
| `DOC-034` - Demande inscription ordre | `signataire`, `societe`, `ordre`, `mandataire`, `signature`, `dossier.options.derogation` |
| `DOC-005` - Lettre renonciation associe | `signataire`, `conjoint`, `societe`, `apport`, `regime_communautaire.renonciation`, `signature` |
| `DOC-006` - Lettre avertissement conjoint | `signataire`, `conjoint`, `societe`, `apport`, `regime_communautaire.avertissement`, `signature` |
| `DOC-007` - Avenant contrat de bail | `bail`, `societe`, `cession.cabinet`, `signature` |
| `DOC-008` - Appel de fonds SEL | `societe`, `cession.financement`, `cession.vendeur`, `cession.acquereur`, `signature` |
| `DOC-009` - Acte cession cabinet medical | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `signature` |
| `DOC-010` - Compromis cession cabinet medical | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `signature` |
| `DOC-011` - Acte cession cabinet dentaire | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `cession.salaries[]`, `signature` |
| `DOC-012` - Compromis cession cabinet dentaire | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `cession.salaries[]`, `signature` |
| `DOC-013` - Derogation multi-sites SEL | `derogation`, `site_declare`, `sites_existants[]`, `societe`, `signature` |
| `DOC-014` - Derogation cumul SELARL-BNC | `derogation`, `societe`, `signature` |
| `DOC-015` - Statuts SAS | `statuts_sas`, `societe_spfpl`, `actionnaire_unique`, `president`, `capital_souscription`, `apport_titres`, `societe_cible`, `signature` |
| `DOC-035` - Statuts SPFPL cession | `operation_spfpl`, `societe_spfpl`, `actionnaire_unique`, `cedant`, `societe_cible`, `capital_souscription`, `depot_fonds`, `exercice_social`, `signature` |
| `DOC-036` - Statuts SPFPL apport | `operation_spfpl`, `societe_spfpl`, `actionnaire_unique`, `apporteur`, `societe_cible`, `apport`, `apport_titres`, `capital_souscription`, `commissaire_aux_apports`, `signature` |
| `DOC-016` - Statuts SELARL dentiste | `statuts_sel`, `societe`, `associes[]`, `dirigeant_nomine`, `signature` |
| `DOC-017` - Statuts SELARL medecin | `statuts_sel`, `societe`, `associes[]`, `dirigeant_nomine`, `signature` |
| `DOC-018` - Statuts SELAS medecin | `statuts_sel`, `societe`, `associes[]`, `dirigeant_nomine`, `signature` |
| `DOC-019` - Statuts SCS | `statuts_civils`, `statuts_civils.associes[]`, `signature` |
| `DOC-020` - Statuts SCI | `statuts_civils`, `statuts_civils.associes[]`, `signature` |
| `DOC-021` - Statuts SCI IRIS | `statuts_civils`, `statuts_civils.associes[]`, `statuts_civils.resultat_groupes_parts[]`, `signature` |
| `DOC-022` - Lettre option IS | `statuts_civils`, `impots`, `societe`, `signature` |
| `DOC-023` - PV remuneration president SAS | `societe_spfpl`, `actionnaire_unique`, `president`, `remuneration_president`, `exercice_social`, `signature` |
| `DOC-024` - Attestation capital / souscripteurs SAS | `societe_spfpl`, `actionnaire_unique`, `capital_souscription`, `apport_titres`, `societe_cible`, `signature` |
| `DOC-037` - Note information SPFPL | `operation_spfpl`, `societe_spfpl`, `cedant` ou `apporteur`, `societe_cible`, `associes_cible[]`, `cession_parts`, `signature` |
| `DOC-038` - PV agrement SPFPL associe unique | `societe_spfpl`, `societe_cible`, `cedant`, `associes_cible[]`, `cession_parts`, `decision`, `reunion`, `signature` |
| `DOC-039` - PV agrement SPFPL plusieurs associes | `societe_spfpl`, `societe_cible`, `cedant`, `associes_cible[]`, `cession_parts`, `decision`, `reunion`, `signature` |
| `DOC-040` - Acte cession parts SPFPL | `societe_spfpl`, `societe_cible`, `cedant`, `associes_cible[]`, `cession_parts`, `document`, `signature` |
| `DOC-041` - Contrat apport SPFPL | `societe_spfpl`, `societe_cible`, `apporteur`, `apport_titres`, `evaluateur_apport`, `commissaire_aux_apports`, `document`, `signature` |
| `DOC-042` - Attestation capital / souscripteurs SPFPL | `societe_spfpl`, `societe_cible`, `apporteur`, `apport_titres`, `capital_souscription`, `signature` |
| `DOC-043` - Attestation commissaire aux apports | `societe_spfpl`, `societe_cible`, `apporteur`, `apport_titres`, `commissaire_aux_apports`, `signature` |
| `DOC-025` - Statuts SCM | `statuts_civils`, `statuts_civils.associes[]`, `signature` |
| `DOC-026` - Pacte associes SCM | `societe`, `pacte_associes`, `parties_frais_communs[]`, `praticiens[]`, `locaux`, `signature` |
| `DOC-027` - Contrat frais communs SCM | `societe`, `frais_communs`, `parties_frais_communs[]`, `praticiens[]`, `locaux`, `signature` |
| `DOC-028` - Reglement interieur SCM | `societe`, `reglement_interieur`, `parties_frais_communs[]`, `praticiens[]`, `locaux`, `signature` |
| `DOC-029` - Acte cession actions SPFPL | `operation_spfpl`, `societe_spfpl`, `societe_cible`, `cedant`, `associes_cible[]`, `cession_actions`, `document`, `signature` |
| `DOC-030` - Liste depenses communes SCM | `societe`, `parties_frais_communs[]`, `praticiens[]`, `locaux`, `signature` |
| `DOC-031` - PV AGE cession parts SCM | `scm_cession`, `scm_cession.scm_cedee`, `scm_cession.cessionnaire`, `scm_cession.associes_*[]`, `signature` |
| `DOC-032` - Courrier SDE cession SCM | `scm_cession`, `scm_cession.enregistrement`, `scm_cession.signataire_sde`, `signature` |
| `DOC-033` - Acte cession parts SCM | `scm_cession`, `scm_cession.scm_cedee`, `scm_cession.cessionnaire`, `scm_cession.cedant`, `scm_cession.prix`, `signature` |

### Decision de cloture mapping

Le mapping V1 est aligne sur les 43 documents exposes par le moteur DOCX. Les
documents manuels, legacy non convertis, UI, PDF, ZIP et recette finale restent
hors mapping moteur.
