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
