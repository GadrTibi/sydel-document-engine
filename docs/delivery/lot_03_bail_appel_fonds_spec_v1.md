# DAAT x SYDEL - SPEC CANONIQUE V1
## Bloc `bail / appel de fonds` - SPEC-CESSION-BAIL-001

## 1. Objet

Formaliser le bloc documentaire `bail / appel de fonds` rattache aux dossiers avec cession, sans coder.

Cette spec couvre deux documents distincts :
- `Avenant Contrat de bail.docx` ;
- `appel de fond sel.docx`.

Elle ne modifie aucun wording juridique source. Elle prepare uniquement un futur travail de specification texte ou de code, qui devra rester strictement derive des sources lues.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/07_ARBRE_MOTEUR_DOCUMENT_CENTRE_V1.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour un futur ticket code ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources DOCX demandees :
- aucune des deux sources n'a ete trouvee dans `project/source_documents/lot_03/` ;
- les sources ont donc ete lues dans `project/source_import/raw_drive_dump/Creation SELARL/Cession/`.

Sources raw lues :
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Avenant Contrat de bail.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/appel de fond sel.docx`

## 3. Perimetre documentaire V1

### 3.1 Avenant contrat de bail

Source de verite :
- rattache au bloc `Si cession` de SELARL ;
- rattache au bloc `Si Cession` de SELAS.

Decision de specification :
- document canonique distinct ;
- activable quand `dossier.options.cession == true` pour SELARL ou SELAS ;
- reusable entre cession de cabinet medical et cession de cabinet dentaire, sauf arbitrage contraire.

Identifiant de travail :
- `LOT03-BAIL-AVENANT`.

### 3.2 Appel de fonds SEL

Source de verite :
- rattache au bloc `Si cession` de SELARL ;
- non liste dans le bloc cession SELAS.

Decision de specification :
- document canonique distinct ;
- activable en V1 uniquement pour SELARL avec `dossier.options.cession == true`, sauf decision metier ulterieure pour SELAS ;
- le document source contient un wording specialise `cabinet dentaire`, ce qui bloque son usage medical sans validation.

Identifiant de travail :
- `LOT03-APPEL-FONDS-SEL`.

## 4. Role metier des documents

### 4.1 Avenant contrat de bail

Role metier :
- constater le changement de locataire du bail professionnel ;
- substituer la societe en cours d'immatriculation au locataire personne physique ;
- maintenir les clauses du bail en cours ;
- rappeler la responsabilite de l'ancien locataire pour les actes passes au nom de la societe avant immatriculation.

Parties source :
- `bailleur` ;
- `locataire` personne physique, aussi ancien locataire ;
- `societe` nouvelle locataire.

Structure source observee :
1. titre avec date du jour ;
2. identification du bailleur ;
3. identification du locataire personne physique ;
4. article 1 : changement de locataire ;
5. article 2 : responsabilite pour une societe en cours de formation ;
6. article 3 : clauses du bail ;
7. formule de signature et trois emplacements : Bailleur, ancien locataire, nouveau locataire.

### 4.2 Appel de fonds SEL

Role metier :
- demander a la banque le deblocage de fonds ;
- rattacher le deblocage a la cession d'un cabinet ;
- identifier le vendeur et la societe acquereur.

Structure source observee :
1. banque ;
2. lieu et date ;
3. destinataire ;
4. objet ;
5. formule d'appel ;
6. demande de deblocage ;
7. montant ;
8. phrase de rattachement a la cession ;
9. formule de politesse ;
10. signature.

## 5. Textes communs et differences internes

Il n'existe pas de tronc textuel commun substantiel entre l'avenant de bail et l'appel de fonds. La mutualisation doit rester limitee a :
- les donnees de dossier cession ;
- la societe acquereur ;
- le vendeur / locataire personne physique lorsque ce role est le meme ;
- les lieux, dates et signatures ;
- les helpers de rendu DOCX generiques.

Differences structurantes :

| Zone | Avenant bail | Appel de fonds |
|---|---|---|
| Finalite | modification du bail | instruction bancaire de deblocage |
| Parties | bailleur, locataire, societe | banque, destinataire, vendeur, acquereur |
| Structures source | SELARL et SELAS selon source de verite | SELARL seulement selon source de verite |
| Cabinet | neutre medical/dentaire dans le titre et le corps | source hard-code `cabinet dentaire` |
| Montant | aucun montant de cession | montant de fonds present sans placeholder exploitable |
| Signatures | trois emplacements | un signataire |

## 6. Variables canoniques attendues

### 6.1 Dossier / selection

- `dossier.structure`
- `dossier.options.cession`
- `dossier.cession.type_cabinet`

Valeurs attendues :
- `dossier.structure in {SELARL, SELAS}` pour l'avenant bail ;
- `dossier.structure == SELARL` pour l'appel de fonds en V1 ;
- `dossier.cession.type_cabinet in {medical, dentaire}` pour l'avenant ;
- `dossier.cession.type_cabinet == dentaire` pour l'appel de fonds tant que le wording source n'est pas arbitre.

### 6.2 Bailleur

- `bail.bailleur.civilite_affichage`
- `bail.bailleur.prenom`
- `bail.bailleur.nom`
- `bail.bailleur.profession`
- `bail.bailleur.date_naissance`
- `bail.bailleur.ville_naissance`
- `bail.bailleur.nationalite`
- `bail.bailleur.adresse_affichee`

### 6.3 Locataire personne physique / vendeur

Pour l'avenant :
- `bail.locataire.civilite_affichage`
- `bail.locataire.civilite_courte`
- `bail.locataire.prenom`
- `bail.locataire.nom`
- `bail.locataire.profession`
- `bail.locataire.date_naissance`
- `bail.locataire.ville_naissance`
- `bail.locataire.nationalite`
- `bail.locataire.adresse_affichee`

Pour l'appel de fonds, si le vendeur est la meme personne :
- `cession.vendeur.civilite_affichage`
- `cession.vendeur.prenom`
- `cession.vendeur.nom`

Regle :
- ne pas supposer automatiquement que `bail.locataire` et `cession.vendeur` sont identiques sans mapping dossier explicite.

### 6.4 Societe acquereur / nouvelle locataire

- `societe.denomination`
- `societe.siege.adresse_affichee`
- `societe.rcs_ville`

Pour l'appel de fonds :
- `cession.acquereur.denomination_societe`

Regle :
- si `cession.acquereur.denomination_societe` est absent, le futur generateur pourra utiliser `societe.denomination` uniquement si l'acquereur est explicitement la societe du dossier.

### 6.5 Bail

- `bail.date_signature_origine`
- `bail.date_avenant`

Mapping :
- `[date_bail]` -> `bail.date_signature_origine`
- `[date_du_jour]` -> `bail.date_avenant`

### 6.6 Banque / appel de fonds

- `cession.financement.banque.nom`
- `cession.financement.destinataire.civilite_affichage`
- `cession.financement.destinataire.prenom`
- `cession.financement.destinataire.nom`
- `cession.financement.montant_deblocage`
- `cession.financement.montant_deblocage_lettres` optionnel

Point sensible :
- le montant apparait dans la source sous forme de texte non placeholderise `Montant du fond` suivi de `EUR`.
- il doit devenir un champ manuel obligatoire si le document est automatise.

### 6.7 Signature

- `signature.lieu`
- `signature.date`
- `document.nombre_exemplaires_lettres`
- `document.signataire.prenom`
- `document.signataire.nom`

## 7. Mapping source vers canonique

### 7.1 Avenant contrat de bail

| Placeholder source | Variable canonique cible |
|---|---|
| `[date_du_jour]` | `bail.date_avenant` |
| `[civilite_bailleur]` | `bail.bailleur.civilite_affichage` |
| `[prenom_bailleur]` | `bail.bailleur.prenom` |
| `[nom_bailleur]` | `bail.bailleur.nom` |
| `[profession_bailleur]` | `bail.bailleur.profession` |
| `[date_naissance_bailleur]` | `bail.bailleur.date_naissance` |
| `[ville_naissance_bailleur]` | `bail.bailleur.ville_naissance` |
| `[nationalite_bailleur]` | `bail.bailleur.nationalite` |
| `[adresse_bailleur]` | `bail.bailleur.adresse_affichee` |
| `[civilite_locataire]` | `bail.locataire.civilite_affichage` |
| `[civilite_courte_locataire]` | `bail.locataire.civilite_courte` |
| `[prenom_locataire]` | `bail.locataire.prenom` |
| `[nom_locataire]` | `bail.locataire.nom` |
| `[profession_locataire]` | `bail.locataire.profession` |
| `[date_naissance_locataire]` | `bail.locataire.date_naissance` |
| `[ville_naissance_locataire]` | `bail.locataire.ville_naissance` |
| `[nationalite_locataire]` | `bail.locataire.nationalite` |
| `[adresse_locataire]` | `bail.locataire.adresse_affichee` |
| `[date_bail]` | `bail.date_signature_origine` |
| `[denomination_societe]` | `societe.denomination` |
| `[ville_rcs]` | `societe.rcs_ville` |
| `[adresse_siege]` | `societe.siege.adresse_affichee` |
| `[lieu_signature]` | `signature.lieu` |
| `[nombre_exemplaires_lettres]` | `document.nombre_exemplaires_lettres` |
| `[date_signature]` | `signature.date` |

### 7.2 Appel de fonds SEL

| Placeholder / zone source | Variable canonique cible |
|---|---|
| `[nom_banque]` | `cession.financement.banque.nom` |
| `[lieu_signature]` | `signature.lieu` |
| `[date_signature]` | `signature.date` |
| `[civilite_destinataire]` | `cession.financement.destinataire.civilite_affichage` |
| `[prenom_destinataire]` | `cession.financement.destinataire.prenom` |
| `[nom_destinataire]` | `cession.financement.destinataire.nom` |
| `Montant du fond` | `cession.financement.montant_deblocage` |
| `[denomination_societe]` | `cession.cabinet.denomination_ou_adresse_affichee` |
| `[civilite_vendeur]` | `cession.vendeur.civilite_affichage` |
| `[prenom_vendeur]` | `cession.vendeur.prenom` |
| `[nom_vendeur]` | `cession.vendeur.nom` |
| `[denomination_societe_acquereur]` | `cession.acquereur.denomination_societe` |
| `[prenom_signataire]` | `document.signataire.prenom` |
| `[nom_signataire]` | `document.signataire.nom` |

## 8. Points manuels

### 8.1 Avenant bail

Doivent rester fournis par saisie dossier ou controle humain :
- identite complete du bailleur ;
- identite complete de l'ancien locataire ;
- date du bail initial ;
- adresse affichee du siege ;
- ville RCS lorsque la societe est en cours d'immatriculation ;
- nombre d'exemplaires ;
- confirmation que le bailleur accepte le changement de locataire.

### 8.2 Appel de fonds

Doivent rester fournis par saisie dossier ou controle humain :
- banque ;
- destinataire bancaire ;
- montant du deblocage ;
- signataire effectif de la lettre ;
- confirmation que le wording `cabinet dentaire` correspond au dossier.

## 9. Regles de blocage avant future generation

Un futur generateur doit bloquer si :
- `dossier.options.cession != true` ;
- l'avenant bail est demande hors `SELARL` / `SELAS` sans decision metier ;
- l'appel de fonds est demande hors `SELARL` sans decision metier ;
- l'appel de fonds est demande pour un cabinet medical sans wording valide ;
- le montant de deblocage est absent ;
- le lien entre `bail.locataire`, `cession.vendeur` et `societe` n'est pas explicite ;
- une variable obligatoire du bailleur, locataire, acquereur ou destinataire bancaire manque ;
- le nombre d'exemplaires ou la date de signature manque dans l'avenant bail.

## 10. Points ouverts

1. L'appel de fonds est liste dans la source de verite pour SELARL, mais pas pour SELAS ; ne pas l'activer en SELAS sans arbitrage.
2. L'appel de fonds contient `cabinet dentaire` en dur ; une variante medicale n'est pas sourcee.
3. La zone `Montant du fond` n'est pas un placeholder ; elle doit etre transformee en champ manuel obligatoire avant code.
4. Le placeholder `[denomination_societe]` de l'appel de fonds designe le cabinet exploite, pas clairement la societe du dossier ; mapping a valider.
5. L'avenant bail vise une societe en cours d'immatriculation ; aucune variante source pour societe deja immatriculee n'a ete lue.
6. `civilite_courte_locataire` pilote une formulation grammaticale locale ; sa liste de valeurs doit etre fournie explicitement avant code.

## 11. Statut de la spec

`SPEC-CESSION-BAIL-001` est complet cote `bail / appel de fonds` pour un cadrage V1.

Avant code, il faudra :
- valider les points ouverts ci-dessus ;
- produire une spec texte si le projet veut figer ligne a ligne le wording cible ;
- attribuer les identifiants catalogue definitifs.
