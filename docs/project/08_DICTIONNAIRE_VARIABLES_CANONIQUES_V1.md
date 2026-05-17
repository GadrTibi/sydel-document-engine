# Dictionnaire canonique des variables — V1

## Décisions structurantes

1. **Normalisation par rôle métier**
   - La vérité canonique ne doit pas reprendre des noms locaux de modèles comme `personne_1` ou `personne_2`.
   - On normalise par **rôle métier** : `signataire`, `associes[]`, `dirigeant_nomine`, `societe`, `siege_social`, `domiciliation`, `bien_immobilier`, etc.

2. **Séparation civilité / genre**
   - `civilite_affichage` sert à l'affichage (ex. `M.`, `Mme`, `Docteur`).
   - `genre` sert aux accords grammaticaux (`soussigné/soussignée`, `né/née`, `fils/fille`).
   - On ne suppose pas qu'une civilité suffit toujours à déduire le genre.

3. **Séparation variable canonique / placeholder source**
   - Les crochets présents dans les modèles source sont des **aliases documentaires**.
   - Ils doivent être mappés vers une variable canonique unique.

4. **Règle de globalisation minimale**
   - Une donnée répétée dans plusieurs documents devient une **variable canonique globale**.
   - Une donnée ponctuelle, utilisée une seule fois, peut rester un **champ manuel/documentaire**.

## Convention de nommage

- **Documentation / specs** : notation pointée
  - `signataire.prenom`
  - `societe.denomination`
  - `associes[].nb_parts`

- **Code Python** : modèles structurés ou snake_case, selon le besoin technique
  - l'important est de préserver la correspondance avec la forme canonique documentaire.

## Packs canoniques de variables

### 1. Dossier
- `dossier.structure`
- `dossier.famille`
- `dossier.options.regime_communautaire`
- `dossier.options.site_distinct`
- `dossier.options.derogation`
- `dossier.options.scm`
- `dossier.options.cession`
- `dossier.options.apport`
- `dossier.options.associe_unique`

### 2. Signature / clôture
- `signature.lieu`
- `signature.date`
- `signature.image_optionnelle`
- `signature.nombre_exemplaires`

### 3. Signataire
- `signataire.genre`
- `signataire.civilite_affichage`
- `signataire.prenom`
- `signataire.nom`
- `signataire.date_naissance`
- `signataire.ville_naissance`
- `signataire.departement_naissance`
- `signataire.nationalite`
- `signataire.nom_pere`
- `signataire.nom_mere`
- `signataire.fonction`

### 4. Adresse personnelle du signataire
- `signataire.adresse.num_voie`
- `signataire.adresse.voie`
- `signataire.adresse.ville`
- `signataire.adresse.cp`

### 5. Société
- `societe.forme_juridique`
- `societe.denomination`
- `societe.capital_social`
- `societe.ville_rcs`
- `societe.nb_parts_total`
- `societe.valeur_nominale_part`

### 6. Siège social
- `societe.siege.num_voie`
- `societe.siege.voie`
- `societe.siege.ville`
- `societe.siege.cp`

### 7. Domiciliation
- `domiciliation.adresse_affichee`

### 8. Dirigeant nommé
- `dirigeant_nomine.genre`
- `dirigeant_nomine.civilite_affichage`
- `dirigeant_nomine.prenom`
- `dirigeant_nomine.nom`
- `dirigeant_nomine.date_naissance`
- `dirigeant_nomine.ville_naissance`
- `dirigeant_nomine.departement_naissance`
- `dirigeant_nomine.nationalite`
- `dirigeant_nomine.fonction`
- `dirigeant_nomine.adresse.num_voie`
- `dirigeant_nomine.adresse.voie`
- `dirigeant_nomine.adresse.ville`
- `dirigeant_nomine.adresse.cp`
- `dirigeant_nomine.ref_associe_index` (optionnel si le gérant est choisi parmi les associés)

### 9. Associés (répétable)
- `associes[]`
  - `genre`
  - `civilite_affichage`
  - `prenom`
  - `nom`
  - `nb_parts`
  - `date_naissance` (si nécessaire)
  - `ville_naissance` (si nécessaire)
  - `departement_naissance` (si nécessaire)
  - `nationalite` (si nécessaire)
  - `adresse.num_voie` (si nécessaire)
  - `adresse.voie` (si nécessaire)
  - `adresse.ville` (si nécessaire)
  - `adresse.cp` (si nécessaire)

### 10. Bien immobilier / cession / emprunt
- `bien_immobilier.adresse.num_voie`
- `bien_immobilier.adresse.voie`
- `bien_immobilier.adresse.ville`
- `bien_immobilier.adresse.cp`
- `emprunt.montant_max`

## Mappings canoniques — Lot 1

### DOC-001 — Déclaration de non-condamnation
- `[civilite]` -> `signataire.civilite_affichage`
- `[prenom]` -> `signataire.prenom`
- `[nom]` -> `signataire.nom`
- `[date_naissance]` -> `signataire.date_naissance`
- `[num_voie_perso]` -> `signataire.adresse.num_voie`
- `[voie_perso]` -> `signataire.adresse.voie`
- `[ville_perso]` -> `signataire.adresse.ville`
- `[cp_perso]` -> `signataire.adresse.cp`
- `[nationalite]` -> `signataire.nationalite`
- `[nom_pere]` -> `signataire.nom_pere`
- `[nom_mere]` -> `signataire.nom_mere`
- `[lieu_signature]` -> `signature.lieu`
- `[date_signature]` -> `signature.date`
- `[signature]` -> `signature.image_optionnelle`

### DOC-002 — Autorisation de domiciliation
- `[civilite]` -> `signataire.civilite_affichage`
- `[prenom]` -> `signataire.prenom`
- `[nom]` -> `signataire.nom`
- `[denomination_societe]` -> `societe.denomination`
- `[capital_social]` -> `societe.capital_social`
- **adresse source non canonique** -> `domiciliation.adresse_affichee`
- `[lieu_signature]` -> `signature.lieu`
- `[date_signature]` -> `signature.date`

### DOC-003 — Procuration
- `[civilite]` -> `signataire.civilite_affichage`
- `[prenom]` -> `signataire.prenom`
- `[nom]` -> `signataire.nom`
- `[num_voie_perso]` -> `signataire.adresse.num_voie`
- `[voie_perso]` -> `signataire.adresse.voie`
- `[ville_perso]` -> `signataire.adresse.ville`
- `[cp_perso]` -> `signataire.adresse.cp`
- `[fonction_dirigeant]` -> `signataire.fonction`
- `[forme_sociale]` -> `societe.forme_juridique`
- `[denomination_societe]` -> `societe.denomination`
- `[num_voie_siege]` -> `societe.siege.num_voie`
- `[voie_siege]` -> `societe.siege.voie`
- `[ville_siege]` -> `societe.siege.ville`
- `[cp_siege]` -> `societe.siege.cp`
- `[lieu_signature]` -> `signature.lieu`
- `[date_signature]` -> `signature.date`

## Préparation canonique — PV nomination gérant

Le modèle source lu pour le PV de nomination gérant ne doit **pas** devenir la vérité canonique tel quel.

### Aliases locaux observés
- `personne_1` -> probablement `associes[0]`
- `personne_2` -> probablement `associes[1]`
- gérant nommé fixé sur `personne_2` dans le modèle exemple

### Traduction canonique cible
- `[civilite_personne_1]` -> `associes[0].civilite_affichage`
- `[prenom_personne_1]` -> `associes[0].prenom`
- `[nom_personne_1]` -> `associes[0].nom`
- `[nb_parts_personne_1]` -> `associes[0].nb_parts`

- `[civilite_personne_2]` -> `associes[1].civilite_affichage`
- `[prenom_personne_2]` -> `associes[1].prenom`
- `[nom_personne_2]` -> `associes[1].nom`
- `[nb_parts_personne_2]` -> `associes[1].nb_parts`

- `[date_naissance_personne_2]` -> `dirigeant_nomine.date_naissance`
- `[ville_naissance_personne_2]` -> `dirigeant_nomine.ville_naissance`
- `[departement_naissance_personne_2]` -> `dirigeant_nomine.departement_naissance`
- `[nationalite_personne_2]` -> `dirigeant_nomine.nationalite`
- `[num_voie_perso_personne_2]` -> `dirigeant_nomine.adresse.num_voie`
- `[voie_perso_personne_2]` -> `dirigeant_nomine.adresse.voie`
- `[cp_perso_personne_2]` -> `dirigeant_nomine.adresse.cp`
- `[ville_perso_personne_2]` -> `dirigeant_nomine.adresse.ville`
- `[fonction_dirigeant]` -> `dirigeant_nomine.fonction`

### Décision structurante pour les documents à venir
- Le modèle canonique doit permettre **N associés** via `associes[]`.
- Le document peut ensuite désigner un `dirigeant_nomine`, qui peut être l'un des associés.
- On ne fige pas la vérité canonique sur `personne_2`.

## Ce qui doit rester local / manuel si besoin

Exemples typiques :
- `emprunt.montant_max`
- `signature.nombre_exemplaires`
- données ponctuelles d'un bien immobilier

Ces données peuvent exister dans le dictionnaire, mais elles n'ont pas besoin d'être promues en “tronc commun UI” si elles n'apparaissent que dans peu de documents.

## Ce que ce dictionnaire permet ensuite

1. Construire l'**arbre de variables/UI** sans doublons.
2. Mapper chaque document source vers des variables canoniques.
3. Réutiliser les mêmes packs de questions dans Streamlit.
4. Gérer proprement les documents à associés dynamiques.

## Consolidation finale moteur DOCX V1

Ticket : `RECONCILE-MOTOR-CLOSE-001`

Cette section consolide les packs apparus apres le socle Lot 1 / PV. Le detail
champ par champ reste porte par `src/sydel_doc_engine/domain/models.py` et par
les specs `docs/delivery/`; le role de ce dictionnaire est de figer les noms de
packs canoniques qui alimentent le moteur expose par le catalogue.

### Packs transverses ajoutes

- `ordre` : donnees ordinales de la demande d'inscription a l'ordre.
- `mandataire` : mandataire configurable, jamais constante juridique cachee.
- `regime_communautaire` : avertissement, renonciation et donnees de courrier.
- `bail` : bailleur, locataire, dates et acceptation de changement.
- `cession` : cabinet, vendeur, acquereur, financement, prix, salaries et validations.
- `derogation` : type, mode de rendu, roles, sites, cumul, motifs et conditions.
- `document` : nombre d'exemplaires/pages, annexes et signataire documentaire.

### Packs societes / statuts

- `statuts_sas`
- `statuts_sel`
- `statuts_civils`
- `capital_souscription`
- `depot_fonds`
- `exercice_social`
- `president`
- `remuneration_president`

### Packs SPFPL

- `operation_spfpl`
- `societe_spfpl`
- `societe_cible`
- `associes_cible[]`
- `cedant`
- `apporteur`
- `cession_parts`
- `cession_actions`
- `operation_titres`
- `apport_titres`
- `evaluateur_apport`
- `commissaire_aux_apports`

### Packs SCM

- `scm_satellites`
- `pacte_associes`
- `frais_communs`
- `reglement_interieur`
- `parties_frais_communs[]`
- `praticiens[]`
- `locaux`
- `scm_cession`

### Decision de cloture variables

Les variables tardives sont considerees consolidees pour le moteur DOCX V1 si
elles appartiennent a l'un des packs ci-dessus et si leur usage document par
document est trace dans `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`.

L'arbre UI exhaustif reste hors V1 moteur et passe dans la phase suivante.

## Ordre de travail recommandé après ce V1

1. Intégrer ce dictionnaire dans le repo.
2. Mettre à jour le registre / board / last state.
3. Ajouter une table de mapping document -> variables canoniques.
4. Reprendre `PV nomination gérant` à partir de ce dictionnaire, puis le spécifier avant codage.
