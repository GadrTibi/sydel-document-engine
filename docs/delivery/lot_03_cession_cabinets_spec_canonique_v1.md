# DAAT x SYDEL - SPEC CANONIQUE V1
## Bloc `cession cabinets medical / dentaire` - SPEC-CESSION-BAIL-001

## 1. Objet

Formaliser le bloc documentaire `cession de cabinet` avant tout codage.

Cette spec couvre quatre documents sources :
- `Acte de cession d_un cabinet medical.docx` ;
- `Compromis de cession d_un cabinet medical.docx` ;
- `Acte de cession d'un cabinet dentaire.docx` ;
- `Compromis de cession d_un cabinet dentaire.docx`.

Elle distingue :
- actes / compromis ;
- medical / dentaire ;
- textes communs ;
- differences metier et wording ;
- variables canoniques ;
- points manuels et points ouverts.

Aucun code Python n'est modifie par cette spec.

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
- aucune des quatre sources n'a ete trouvee dans `project/source_documents/lot_03/` ;
- les sources ont donc ete lues dans `project/source_import/raw_drive_dump/Creation SELARL/Cession/`.

Sources raw lues :
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Acte de cession d_un cabinet medical.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Compromis de cession/Compromis de cession d_un cabinet medical.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Acte de cession d_un cabinet dentaire.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Compromis de cession/Compromis de cession d_un cabinet dentaire.docx`

## 3. Perimetre documentaire V1

La source de verite rattache ces documents aux branches :
- SELARL, si cession de cabinet medical ;
- SELARL, si cession de cabinet dentaire ;
- SELAS, si cabinet medical ;
- SELAS, si cabinet dentaire.

Condition documentaire :
- `dossier.options.cession == true`.

Condition de variante :
- `dossier.cession.type_cabinet == medical` : acte medical + compromis medical ;
- `dossier.cession.type_cabinet == dentaire` : acte dentaire + compromis dentaire.

Decision V1 :
- conserver quatre documents canoniques distincts ;
- ne pas chercher a fusionner medical et dentaire dans un seul generateur tant que les ecarts source ne sont pas arbitres ;
- mutualiser uniquement les packs de variables, validations, sections communes et helpers de rendu.

Identifiants de travail :
- `LOT03-CESSION-ACTE-MEDICAL`
- `LOT03-CESSION-COMPROMIS-MEDICAL`
- `LOT03-CESSION-ACTE-DENTAIRE`
- `LOT03-CESSION-COMPROMIS-DENTAIRE`

Les identifiants catalogue definitifs devront etre attribues dans un futur ticket de code.

## 4. Role de chaque famille documentaire

### 4.1 Acte de cession

Role metier :
- formaliser la cession definitive du cabinet ;
- decrire les parties ;
- decrire le fonds liberal cede ;
- fixer le prix, le paiement, les conditions, le transfert de propriete et les formalites ordinales ;
- prevoir les annexes.

Documents concernes :
- acte medical ;
- acte dentaire.

### 4.2 Compromis de cession

Role metier :
- formaliser la promesse synallagmatique de vente avant l'acte definitif ;
- decrire les parties et le fonds liberal ;
- fixer le prix et la date limite de realisation ;
- prevoir les conditions suspensives ;
- preparer l'acte de cession ulterieur.

Documents concernes :
- compromis medical ;
- compromis dentaire.

## 5. Structure commune observee

Les quatre documents partagent une architecture proche :

1. titre du document ;
2. identification des parties ;
3. declaration des parties sur etat civil, existence, capacite et droits ;
4. objet du contrat ;
5. declaration du vendeur ;
6. consistance du fonds liberal cede ;
7. origine de propriete ;
8. droit au bail ;
9. chiffre d'affaires et resultats sur trois exercices ;
10. situation generale et libre disposition du fonds liberal ;
11. prix et repartition elements corporels / incorporels ;
12. prorata d'exploitation ;
13. conditions a la charge du vendeur et de l'acquereur ;
14. droits d'enregistrement ;
15. frais, droits et honoraires ;
16. communication a l'ordre professionnel ;
17. election de domicile / juridiction ;
18. signature ;
19. annexes.

### Textes communs a stabiliser avant code

Les zones suivantes semblent mutualisables, sous reserve d'une spec texte ulterieure :
- declarations generales de capacite des parties ;
- consistance standard du fonds liberal ;
- libre disposition du fonds liberal ;
- prix et repartition du prix ;
- prorata d'exploitation ;
- frais et droits ;
- affirmation ou information sur droits d'enregistrement ;
- election de domicile ;
- annexes `ETAT DES ELEMENTS CORPORELS CEDES` et `COPIE 2035 AMORTISSEMENTS` quand presentes.

Regle de prudence :
- ces textes ne doivent pas etre "ameliores" ni harmonises automatiquement ;
- les ecarts de wording entre sources doivent etre soit preserves document par document, soit valides explicitement dans une spec texte.

## 6. Differences medical / dentaire

### 6.1 Parties et identification professionnelle

| Zone | Medical | Dentaire |
|---|---|---|
| Titre | `cabinet medical` | `cabinet dentaire` |
| Ordre | Conseil de l'Ordre des Medecins | Conseil de l'Ordre des Chirurgiens-Dentistes |
| Vendeur acte | SIREN + numero ordre + situation matrimoniale | RPPS + Conseil des chirurgiens-dentistes |
| Vendeur compromis | SIREN + numero ordre + conjoint/regime | SIREN + numero ordre, sans conjoint/regime detaille dans la source lue |
| Acquereur | representant specifique dans medical | dans plusieurs zones dentaires, le representant reprend les placeholders vendeur |

Point ouvert :
- les sources dentaires paraissent parfois reutiliser les placeholders vendeur pour representer l'acquereur ou son representant ; ne pas coder sans arbitrage.

### 6.2 Fonds liberal et consistance

Medical :
- acte medical : fonds liberal de medecin ;
- compromis medical : `[nature_fonds_liberal]` ;
- declarations acquereur sur exercice de la profession de medecin.

Dentaire :
- fonds liberal de `[profession_vendeur]` ou cabinet dentaire ;
- declaration d'exercice de la profession de `[profession_vendeur]` ;
- mention specifique de l'accessibilite des cabinets dentaires dans l'acte dentaire.

### 6.3 Bail

Medical :
- les sources medicales contiennent des formulations de locaux mentionnant parfois `cabinet dentaire`, probablement par copie source ;
- l'acte medical indique que le bail autorise l'activite medicale et paramedicale.

Dentaire :
- compromis dentaire : bail autorisant `[profession_vendeur], stomatologue, docteur en medecine` ;
- acte dentaire : bloc droit au bail plus court, sans reconductions detaillees observees dans le compromis.

Point ouvert :
- les mentions de `cabinet dentaire` dans des sources medicales doivent etre arbitrees avant tout code.

### 6.4 Paiement, pret et credit-vendeur

Acte medical :
- prix paye par pret bancaire ;
- bloc source `Ajouter en cas de CV` pour credit-vendeur ;
- variables de credit-vendeur : montant, duree, taux, majoration d'interet de retard.

Acte dentaire :
- paiement comptant ;
- aucun bloc credit-vendeur equivalent observe.

Compromis medical :
- condition suspensive de pret avec montant, taux et duree.

Compromis dentaire :
- condition suspensive de pret avec montant ;
- taux maximum hard-code a `5 %` dans la source ;
- pas de variable `duree_pret` observee.

### 6.5 Conditions specifiques

Acte medical :
- ligne source sur la cession de parts SCM au profit du cessionnaire ;
- ligne source inachevee `De reprendre les contrats de travail de`.

Acte dentaire :
- reprise de deux salaries avec placeholders nominaux ;
- section accessibilite des cabinets dentaires ;
- clause de conciliation devant le President du Conseil departemental ;
- signature finale avec mentions `Lu et approuve`.

Compromis dentaire :
- clause de conciliation ordinale ;
- convention de preuve / signature electronique beaucoup plus detaillee que dans le compromis medical.

## 7. Variables canoniques attendues

### 7.1 Dossier / selection

- `dossier.structure`
- `dossier.options.cession`
- `dossier.cession.type_cabinet`
- `dossier.cession.etape` : `compromis` ou `acte`

Valeurs V1 :
- `dossier.structure in {SELARL, SELAS}`
- `dossier.cession.type_cabinet in {medical, dentaire}`

### 7.2 Vendeur

- `cession.vendeur.civilite_affichage`
- `cession.vendeur.genre`
- `cession.vendeur.prenom`
- `cession.vendeur.nom`
- `cession.vendeur.profession`
- `cession.vendeur.date_naissance`
- `cession.vendeur.ville_naissance`
- `cession.vendeur.departement_naissance`
- `cession.vendeur.cp_naissance`
- `cession.vendeur.pays_naissance`
- `cession.vendeur.nationalite`
- `cession.vendeur.adresse_affichee`
- `cession.vendeur.adresse_exercice_affichee`
- `cession.vendeur.numero_siren`
- `cession.vendeur.numero_ordre`
- `cession.vendeur.numero_rpps`
- `cession.vendeur.ordre_departemental`
- `cession.vendeur.situation_maritale`
- `cession.vendeur.regime_matrimonial`

### 7.3 Conjoint du vendeur

- `cession.vendeur.conjoint.civilite_affichage`
- `cession.vendeur.conjoint.prenom`
- `cession.vendeur.conjoint.nom`

Regle :
- requis uniquement pour les sources qui mentionnent explicitement le conjoint ;
- ne pas inventer de bloc conjoint dans les variantes qui ne l'ont pas.

### 7.4 Acquereur / societe acquereur

- `cession.acquereur.denomination_societe`
- `cession.acquereur.forme_sociale`
- `cession.acquereur.capital_social`
- `cession.acquereur.siege.adresse_affichee`
- `cession.acquereur.rcs_ville`
- `cession.acquereur.numero_rcs`
- `cession.acquereur.numero_siret`
- `cession.acquereur.date_immatriculation`
- `cession.acquereur.date_inscription_ordre`

Representant :
- `cession.acquereur.representant.civilite_affichage`
- `cession.acquereur.representant.genre`
- `cession.acquereur.representant.prenom`
- `cession.acquereur.representant.nom`
- `cession.acquereur.representant.fonction`

### 7.5 Cabinet / fonds liberal

- `cession.cabinet.type`
- `cession.cabinet.nature_fonds_liberal`
- `cession.cabinet.adresse_affichee`
- `cession.cabinet.adresse_locaux_affichee`
- `cession.cabinet.telephone`
- `cession.cabinet.superficie_local`
- `cession.cabinet.description_origine_propriete`
- `cession.cabinet.date_origine_propriete`
- `cession.cabinet.annees_acquisition_patientele`
- `cession.cabinet.prix_origine_propriete`

Precedent proprietaire :
- `cession.cabinet.precedent_proprietaire.civilite_affichage`
- `cession.cabinet.precedent_proprietaire.prenom`
- `cession.cabinet.precedent_proprietaire.nom`

### 7.6 Bail professionnel

- `cession.bail.date_bail`
- `cession.bail.duree`
- `cession.bail.date_debut`
- `cession.bail.date_fin`
- `cession.bail.date_reconduction_1`
- `cession.bail.date_reconduction_2`
- `cession.bail.loyer_mensuel`
- `cession.bail.activite_autorisee_affichee`

### 7.7 Chiffres d'affaires et resultats

- `cession.exercices[]`
  - `periode`
  - `chiffre_affaires`
  - `resultat`

Regle :
- la source vise trois exercices ;
- les placeholders source divergent et contiennent des anomalies ;
- le futur modele doit utiliser une liste structuree de trois lignes, pas des champs eparpilles dans le code.

### 7.8 Prix et paiement

- `cession.prix.total`
- `cession.prix.total_lettres`
- `cession.prix.elements_corporels`
- `cession.prix.elements_corporels_lettres`
- `cession.prix.elements_incorporels`
- `cession.prix.elements_incorporels_lettres`

Pret / financement :
- `cession.financement.pret.montant`
- `cession.financement.pret.taux`
- `cession.financement.pret.duree`

Credit-vendeur :
- `cession.financement.credit_vendeur.actif`
- `cession.financement.credit_vendeur.montant`
- `cession.financement.credit_vendeur.duree`
- `cession.financement.credit_vendeur.taux`
- `cession.financement.credit_vendeur.majoration_interet_retard`

### 7.9 Clauses specifiques et annexes

- `cession.scm.nb_parts_a_ceder`
- `cession.salaries[]`
  - `civilite_affichage`
  - `prenom`
  - `nom`
- `cession.accessibilite_cabinet_dentaire.information_requise`
- `document.nombre_pages_lettres`
- `document.nombre_exemplaires_lettres`
- `document.annexes[]`

### 7.10 Signature

- `signature.lieu`
- `signature.date`
- `signature.vendeur.image_optionnelle`
- `signature.acquereur.image_optionnelle`
- `signature.mentions_manuscrites_requises`

## 8. Mapping source vers canonique

### 8.1 Mapping commun principal

| Placeholder source | Variable canonique cible |
|---|---|
| `[civilite_vendeur]` | `cession.vendeur.civilite_affichage` |
| `[prenom_vendeur]` | `cession.vendeur.prenom` |
| `[nom_vendeur]` | `cession.vendeur.nom` |
| `[profession_vendeur]` | `cession.vendeur.profession` |
| `[date_naissance_vendeur]` | `cession.vendeur.date_naissance` |
| `[ville_naissance_vendeur]` | `cession.vendeur.ville_naissance` |
| `[departement_naissance_vendeur]` | `cession.vendeur.departement_naissance` |
| `[cp_naissance_vendeur]` | `cession.vendeur.cp_naissance` |
| `[pays_naissance_vendeur]` | `cession.vendeur.pays_naissance` |
| `[nationalite_vendeur]` | `cession.vendeur.nationalite` |
| `[adresse_vendeur]` | `cession.vendeur.adresse_affichee` |
| `[adresse_exercice_vendeur]` | `cession.vendeur.adresse_exercice_affichee` |
| `[numero_siren_vendeur]` | `cession.vendeur.numero_siren` |
| `[numero_ordre_vendeur]` | `cession.vendeur.numero_ordre` |
| `[numero_rpps_vendeur]` | `cession.vendeur.numero_rpps` |
| `[ordre_departemental_vendeur]` | `cession.vendeur.ordre_departemental` |
| `[situation_maritale_vendeur]` | `cession.vendeur.situation_maritale` |
| `[regime_matrimonial_vendeur]` | `cession.vendeur.regime_matrimonial` |
| `[denomination_societe_acquereur]` | `cession.acquereur.denomination_societe` |
| `[forme_sociale_acquereur]` | `cession.acquereur.forme_sociale` |
| `[capital_social_acquereur]` | `cession.acquereur.capital_social` |
| `[adresse_siege_acquereur]` | `cession.acquereur.siege.adresse_affichee` |
| `[ville_rcs_acquereur]` | `cession.acquereur.rcs_ville` |
| `[numero_rcs_acquereur]` | `cession.acquereur.numero_rcs` |
| `[numero_siret_acquereur]` | `cession.acquereur.numero_siret` |
| `[fonction_acquereur_representant]` | `cession.acquereur.representant.fonction` |
| `[civilite_acquereur_representant]` | `cession.acquereur.representant.civilite_affichage` |
| `[prenom_acquereur_representant]` | `cession.acquereur.representant.prenom` |
| `[nom_acquereur_representant]` | `cession.acquereur.representant.nom` |
| `[adresse_cabinet]` | `cession.cabinet.adresse_affichee` |
| `[adresse_locaux]` | `cession.cabinet.adresse_locaux_affichee` |
| `[telephone_cabinet]` | `cession.cabinet.telephone` |
| `[superficie_local]` | `cession.cabinet.superficie_local` |
| `[date_bail]` | `cession.bail.date_bail` |
| `[duree_bail]` | `cession.bail.duree` |
| `[date_debut_bail]` | `cession.bail.date_debut` |
| `[date_fin_bail]` | `cession.bail.date_fin` |
| `[date_reconduction_bail_1]` | `cession.bail.date_reconduction_1` |
| `[date_reconduction_bail_2]` | `cession.bail.date_reconduction_2` |
| `[loyer_mensuel]` | `cession.bail.loyer_mensuel` |
| `[prix_cession]` | `cession.prix.total` |
| `[prix_cession_lettres]` | `cession.prix.total_lettres` |
| `[prix_elements_corporels]` | `cession.prix.elements_corporels` |
| `[prix_elements_corporels_lettres]` | `cession.prix.elements_corporels_lettres` |
| `[prix_elements_incorporels]` | `cession.prix.elements_incorporels` |
| `[prix_elements_incorporels_lettres]` | `cession.prix.elements_incorporels_lettres` |
| `[lieu_signature]` | `signature.lieu` |
| `[date_signature]` | `signature.date` |
| `[nombre_pages_lettres]` | `document.nombre_pages_lettres` |
| `[nombre_exemplaires_lettres]` | `document.nombre_exemplaires_lettres` |
| `[signature_vendeur]` | `signature.vendeur.image_optionnelle` |
| `[signature_acquereur]` | `signature.acquereur.image_optionnelle` |

### 8.2 Mapping local medical

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[annees_acquisition_patientele]` | `cession.cabinet.annees_acquisition_patientele` | acte medical |
| `[description_origine_propriete]` | `cession.cabinet.description_origine_propriete` | acte medical |
| `[date_inscription_ordre_acquereur]` | `cession.acquereur.date_inscription_ordre` | acte medical |
| `[date_immatriculation_acquereur]` | `cession.acquereur.date_immatriculation` | acte medical |
| `[montant_credit_vendeur]` | `cession.financement.credit_vendeur.montant` | acte medical, bloc conditionnel |
| `[duree_credit_vendeur]` | `cession.financement.credit_vendeur.duree` | acte medical, bloc conditionnel |
| `[taux_credit_vendeur]` | `cession.financement.credit_vendeur.taux` | acte medical, bloc conditionnel |
| `[majoration_interet_retard]` | `cession.financement.credit_vendeur.majoration_interet_retard` | acte medical, bloc conditionnel |
| `[montant_pret]` | `cession.financement.pret.montant` | compromis medical |
| `[taux_pret]` | `cession.financement.pret.taux` | compromis medical |
| `[duree_pret]` | `cession.financement.pret.duree` | compromis medical |
| `[nb_parts_scm_a_ceder]` | `cession.scm.nb_parts_a_ceder` | acte medical, point ouvert |

### 8.3 Mapping local dentaire

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[numero_rpps_vendeur]` | `cession.vendeur.numero_rpps` | acte dentaire |
| `[civilite_precedent_proprietaire]` | `cession.cabinet.precedent_proprietaire.civilite_affichage` | acte dentaire |
| `[prenom_precedent_proprietaire]` | `cession.cabinet.precedent_proprietaire.prenom` | acte dentaire |
| `[nom_precedent_proprietaire]` | `cession.cabinet.precedent_proprietaire.nom` | acte dentaire |
| `[prix_origine_propriete]` | `cession.cabinet.prix_origine_propriete` | acte dentaire |
| `[date_origine_propriete]` | `cession.cabinet.date_origine_propriete` | acte / compromis |
| `[civilite_salarie_1]` | `cession.salaries[0].civilite_affichage` | acte dentaire |
| `[prenom_salarie_1]` | `cession.salaries[0].prenom` | acte dentaire |
| `[nom_salarie_1]` | `cession.salaries[0].nom` | acte dentaire |
| `[civilite_salarie_2]` | `cession.salaries[1].civilite_affichage` | acte dentaire |
| `[prenom_salarie_2]` | `cession.salaries[1].prenom` | acte dentaire |
| `[nom_salarie_2]` | `cession.salaries[1].nom` | acte dentaire |
| `[date_entree_jouissance]` | `cession.date_entree_jouissance` | acte dentaire |
| `[montant_pret]` | `cession.financement.pret.montant` | compromis dentaire |
| taux hard-code `5 %` | `cession.financement.pret.taux` ou valeur source fixe | point ouvert |

### 8.4 Chiffres d'affaires

Mapping cible :
- `[exercice_1]`, `[chiffre_affaires_1]`, `[resultat_1]` -> `cession.exercices[0]`
- `[exercice_2]`, `[chiffre_affaires_2]`, `[resultat_2]` -> `cession.exercices[1]`
- `[exercice_3]`, `[chiffre_affaires_3]`, `[resultat_3]` -> `cession.exercices[2]`

Point ouvert :
- les compromis lus repetent parfois `[chiffre_affaires_1]` / `[resultat_1]` pour le deuxieme exercice au lieu de placeholders `_2`.
- le futur code ne doit pas reproduire aveuglement cette anomalie sans validation.

## 9. Blocs conditionnels et variantes

### 9.1 Type de document

Si `dossier.cession.etape == compromis` :
- produire le compromis correspondant au type de cabinet ;
- inclure conditions suspensives ;
- inclure date limite de realisation.

Si `dossier.cession.etape == acte` :
- produire l'acte correspondant au type de cabinet ;
- inclure paiement / transfert de propriete ;
- inclure annexes selon source.

Point ouvert :
- la source de verite liste acte et compromis dans chaque branche ; elle ne dit pas si les deux doivent toujours etre generes ensemble ou selon une etape dossier.

### 9.2 Type de cabinet

Si `dossier.cession.type_cabinet == medical` :
- utiliser uniquement les sources medicales ;
- communication a l'Ordre des Medecins ;
- profession et declarations medicales sans adaptation dentaire.

Si `dossier.cession.type_cabinet == dentaire` :
- utiliser uniquement les sources dentaires ;
- communication a l'Ordre des Chirurgiens-Dentistes ;
- conserver les clauses dentaires d'accessibilite et de conciliation si le document source les contient.

### 9.3 Credit-vendeur

Le bloc source `Ajouter en cas de CV` de l'acte medical doit devenir un bloc conditionnel :
- rendu seulement si `cession.financement.credit_vendeur.actif == true` ;
- ne jamais rendre la mention d'instruction `Ajouter en cas de CV`.

### 9.4 Salaries

Source dentaire :
- deux salaries nommes par placeholders.

Source medicale :
- ligne inachevee sur la reprise des contrats de travail.

Decision V1 :
- conserver `cession.salaries[]` comme pack repetable ;
- bloquer le rendu si le document demande un bloc salaries non arbitre ;
- ne pas imposer deux salaries fixes dans le modele canonique.

### 9.5 Parts SCM

L'acte medical contient une clause de cession de parts SCM.

Decision V1 :
- traiter cette clause comme conditionnelle et manuelle ;
- ne pas l'activer automatiquement depuis le seul type de cabinet ;
- exiger une decision explicite entre le bloc cession cabinet et le bloc SCM deja present dans l'arbre moteur.

## 10. Points manuels

Doivent rester fournis par contexte dossier, saisie humaine ou validation :
- description de l'origine de propriete ;
- annees ou date d'acquisition / creation du cabinet ;
- details du bail professionnel ;
- chiffres d'affaires et resultats des trois exercices ;
- repartition du prix entre elements corporels et incorporels ;
- pret bancaire et conditions suspensives ;
- credit-vendeur ;
- salaries repris ;
- parts SCM eventuelles ;
- nombre de pages et d'exemplaires ;
- signatures et mentions manuscrites ;
- annexes : etat des elements corporels cedes, copie 2035 amortissements.

Les annexes ne sont pas specifiees dans les sources au-dela de leurs titres ; elles restent hors generation automatique initiale sauf source annexe dediee.

## 11. Regles de blocage avant future generation

Un futur generateur doit bloquer si :
- `dossier.options.cession != true` ;
- `dossier.structure` est hors `SELARL` / `SELAS` sans arbitrage ;
- `dossier.cession.type_cabinet` est absent ou hors `medical` / `dentaire` ;
- l'etape `acte` / `compromis` n'est pas explicite si le moteur ne produit pas les deux documents ensemble ;
- les donnees vendeur, acquereur, cabinet, prix ou signature obligatoires manquent ;
- les donnees de bail obligatoires manquent ;
- les trois exercices ne peuvent pas etre rendus proprement ;
- une clause conditionnelle source est activee sans donnees suffisantes ;
- une anomalie de wording source identifiee dans cette spec n'a pas ete arbitree.

## 12. Points ouverts

1. La source de verite liste acte et compromis pour chaque branche ; elle ne precise pas si les deux documents sont toujours produits ensemble.
2. Les sources sont dans le raw dump SELARL ; aucune variante SELAS distincte n'a ete lue pour ce bloc.
3. Plusieurs sources medicales contiennent des mentions de `cabinet dentaire` dans le bloc bail ; validation metier requise avant code.
4. Les sources dentaires reutilisent parfois les placeholders vendeur pour representer l'acquereur ou son representant ; mapping a valider.
5. L'acte medical contient un bloc credit-vendeur sous forme d'instruction ; il doit etre transforme en bloc conditionnel valide.
6. L'acte medical contient une clause SCM ; il faut decider si elle releve du bloc cession cabinet ou du bloc SCM separe.
7. Les compromis contiennent des anomalies sur le deuxieme exercice de chiffre d'affaires et resultats.
8. Le taux de pret du compromis dentaire est hard-code a `5 %`, contrairement au compromis medical qui utilise `[taux_pret]`.
9. La ligne `De reprendre les contrats de travail de` de l'acte medical est incomplete.
10. Les signatures different fortement : placeholders de signature, mentions `Lu et approuve`, et clauses de signature electronique divergent.
11. Les clauses d'accessibilite et de conciliation dentaires ne doivent pas etre transferees aux documents medicaux.
12. Les annexes sont seulement titrees ; aucune generation detaillee d'annexe n'est sourcee.

## 13. Critere de completion

`SPEC-CESSION-BAIL-001` est complet cote `cession cabinets` pour un cadrage canonique V1.

Avant tout code, il faudra :
- valider les points ouverts ;
- produire une spec texte si le projet veut figer le wording ligne a ligne ;
- decider si acte et compromis sont generes ensemble ou selon une etape dossier ;
- attribuer les identifiants catalogue definitifs ;
- prevoir des tests par type de cabinet et type de document.
