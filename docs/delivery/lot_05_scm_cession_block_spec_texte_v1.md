# DAAT x SYDEL - SPEC TEXTE V1
## Bloc cession de parts SCM vers SEL

## 1. Objet

Cette spec texte complete :
- `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md`.

Elle stabilise la structure textuelle du bloc cession SCM pour les variantes SELARL et SELAS, sans reecrire le wording juridique source.

Regle V1 :
- le texte source est conserve comme reference ;
- les squelettes ci-dessous decrivent l'ordre des blocs, les variables et les overlays ;
- toute correction d'anomalie apparente reste un point ouvert, pas une modification automatique.

## 2. Sources lues

Memoire projet, referentiels et specs :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md` en lecture seule
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md` en lecture seule
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`
- `docs/delivery/lot_05_scm_satellites_spec_canonique_v1.md`
- `docs/delivery/lot_05_scm_satellites_spec_texte_v1.md`
- `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md`

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`.

Sources documentaires lues :
- `project/source_import/raw_drive_dump/Creation SELARL/scm cession/PV AGE cession part SCM.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/scm cession/Courrier SDE.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/scm cession/Acte de cession des parts de la SCM a la SELARL - transforme.docx`
- `project/source_import/raw_drive_dump/Creation SELAS/SCM/PV AGE cession part SCM - SELAS.docx`
- `project/source_import/raw_drive_dump/Creation SELAS/SCM/Courrier SDE - SELAS.docx`
- `project/source_import/raw_drive_dump/Creation SELAS/SCM/Acte_cession_parts_SCM_SEL_modele.docx`

## 3. Synthese texte commune et overlays

| Document | Tronc commun | Overlay SELARL | Overlay SELAS |
|---|---|---|---|
| PV AGE cession SCM | En-tete SCM, assemblee, ordre du jour, trois resolutions, nouvelle repartition du capital, pouvoirs, signatures | date locale `[date_du_jour]`, agrement a compter de ce jour | date locale `[date_pv]`, agrement dans un delai avec date limite |
| Courrier SDE | lieu/date, objet, demande d'enregistrement, cheque de droits, retour des originaux, formule de politesse, signataire | pas de destinataire, 4 exemplaires fixes | destinataire fiscal, nombre d'exemplaires variable |
| Acte de cession | comparution cedant/cessionnaire, expose, origine de propriete, declarations, cession, prix, paiement, formalites, signature electronique, signatures | SELARL et gerant fixes, chirurgiens-dentistes fixe, Yousign fixe, majoration 3 points fixe | forme/fonction/profession/prestataire/majoration variables |

## 4. PV AGE cession part SCM

### 4.1 Structure texte commune

Le PV comporte les blocs suivants :
- en-tete de la SCM ;
- titre de proces-verbal d'assemblee generale extraordinaire ;
- date en lettres ;
- rappel des associes presents ou representes ;
- mention de l'habilitation de l'assemblee ;
- president de seance ;
- depot des documents ;
- ordre du jour ;
- premiere resolution : agrement du nouvel associe ;
- deuxieme resolution : modification de l'article 7 des statuts ;
- troisieme resolution : pouvoirs pour formalites ;
- cloture et signatures.

### 4.2 Squelette texte V1

Le squelette est descriptif et ne remplace pas le texte source complet.

```text
{scm_cedee.denomination}
Societe civile de moyens
Au capital de {scm_cedee.capital_social}
Siege social : {scm_cedee.siege.adresse_affichee}
RCS de {scm_cedee.ville_rcs} sous le numero {scm_cedee.numero_rcs}

PROCES-VERBAL DES DECISIONS DE L'ASSEMBLEE GENERALE EXTRAORDINAIRE DU {scm_cession.agrement.date_pv}

L'an {scm_cession.agrement.date_pv_lettres}

Les associes de la {scm_cedee.denomination}, au capital de {scm_cedee.capital_social} euros, compose de {scm_cedee.nb_parts_total} parts de {scm_cedee.valeur_nominale_part} euros chacune, se sont reunis [...]

Sont presents ou representes :
1. {scm_cession.associes_presents[0]}
2. {scm_cession.associes_presents[1]}
3. {scm_cession.associes_presents[2]}

PREMIERE RESOLUTION
{overlay_agrement}

DEUXIEME RESOLUTION
Modification de l'article 7 des statuts pour afficher la nouvelle repartition :
{scm_cession.associes_apres_cession[]}
Total : {scm_cedee.nb_parts_total} parts.

TROISIEME RESOLUTION
Pouvoirs pour formalites.

Signatures :
{scm_cession.signataires_pv[]}
```

### 4.3 Overlay SELARL

Source :
- titre avec `[date_du_jour]` ;
- premiere resolution : agrement de la nouvelle societe a compter de ce jour.

Regle texte :
- ne pas ajouter de delai d'agrement ni de date limite dans la variante SELARL sans validation ;
- mapper `[date_du_jour]` vers `scm_cession.agrement.date_pv`.

### 4.4 Overlay SELAS

Source :
- titre avec `[date_pv]` ;
- premiere resolution : agrement dans un delai de `[delai_agrement]` mois a compter de ce jour, jusqu'au `[date_limite_agrement]`.

Regle texte :
- `scm_cession.agrement.delai_mois` et `scm_cession.agrement.date_limite` sont obligatoires pour la variante SELAS ;
- ne pas harmoniser automatiquement avec SELARL.

### 4.5 Limites texte

Blocages avant code :
- roles `personne_1` a `personne_4` non confirmes ;
- president de seance non mappe explicitement ;
- presence de `personne_4` dans la repartition apres cession alors qu'elle n'apparait pas parmi les presents ;
- signatures finales extraites sur une meme ligne dans les deux sources, a reconstruire avec validation de rendu ;
- somme des parts apres cession non controlable.

## 5. Courrier SDE

### 5.1 Structure texte commune

Le courrier comporte les blocs suivants :
- eventuel destinataire fiscal ;
- lieu et date ;
- objet : enregistrement des actes de cession des parts de la societe SCM ;
- demande d'enregistrement des exemplaires de l'acte ;
- mention du cheque de droits d'enregistrement ;
- demande de retour des originaux chez Sydel ;
- formule de politesse ;
- signataire.

### 5.2 Squelette texte V1

```text
{overlay_destinataire}

{signature.lieu}, le {signature.date}

Objet : Enregistrement actes de cession des parts de la societe SCM

Madame, Monsieur,

Je vous prie de bien vouloir trouver sous ce pli {enregistrement.nombre_exemplaires} exemplaires de l'acte de cession pour les enregistrer.

Vous trouverez egalement un cheque de {enregistrement.montant_droits} euros correspondants aux droits d'enregistrements.

Merci de bien vouloir me retourner les originaux chez Sydel. A cet effet, vous trouverez une enveloppe de retour timbree.

Je vous prie d'agreer, Madame, Monsieur, mes salutations distinguees.

{signature.signataire_sde.prenom} {signature.signataire_sde.nom}
```

### 5.3 Overlay SELARL

Source :
- pas de destinataire fiscal ;
- nombre d'exemplaires fixe a `4 exemplaires`.

Regle texte :
- rendre `4` comme constante source SELARL tant qu'aucun arbitrage ne generalise `enregistrement.nombre_exemplaires` ;
- ne pas ajouter de bloc destinataire a la variante SELARL sans validation.

### 5.4 Overlay SELAS

Source :
- destinataire fiscal avec `[service_enregistrement]`, `[centre_finances_publiques]`, `[adresse_service_enregistrement]`, `[cp_ville_service_enregistrement]` ;
- nombre d'exemplaires variable via `[nombre_exemplaires]`.

Regle texte :
- les quatre champs de destinataire sont obligatoires si le bloc destinataire SELAS est rendu ;
- `enregistrement.nombre_exemplaires` est obligatoire pour SELAS.

### 5.5 Limites texte

Blocages avant code :
- confirmer si le destinataire fiscal doit etre commun aux deux structures ;
- confirmer si le nombre d'exemplaires SELARL reste fixe a `4` ;
- confirmer le montant des droits d'enregistrement, qui doit rester une saisie controlee ou un calcul valide hors spec.

## 6. Acte de cession des parts de SCM

### 6.1 Structure texte commune

Les deux actes suivent le meme plan :
- titre de cession des parts de la societe civile de moyens ;
- cadre reserve a l'administration ;
- comparution du cedant ;
- comparution de la societe cessionnaire ;
- expose prealable ;
- origine de propriete ;
- declarations du cedant ;
- clause de cession ;
- propriete et jouissance ;
- prix ;
- paiement du prix ;
- dispense de garantie d'actif et de passif ;
- declarations generales ;
- declaration pour l'enregistrement ;
- formalites et publicite ;
- affirmation de sincerite ;
- communication au conseil de l'ordre ;
- frais ;
- convention sur la preuve et signature electronique ;
- lieu, exemplaires et signatures.

### 6.2 Squelette texte V1

Le squelette est volontairement reduit aux blocs et variables. Le texte juridique complet doit rester celui de la source selectionnee.

```text
CESSION DES PARTS DE LA SOCIETE CIVILE DE MOYENS

Entre les soussignes :

{cedant.identite_complete}, {cedant.profession}, ne le {cedant.date_naissance} a {cedant.ville_naissance} ({cedant.departement_naissance}), de nationalite {cedant.nationalite}, demeurant {cedant.adresse_affichee}, {cedant.situation_maritale} avec {cedant.conjoint.identite_complete}. Inscrit au Tableau de l'ordre departemental des {overlay_profession_ordre} du {cedant.ordre.departemental} sous le numero {cedant.ordre.numero} et sous le numero RPPS {cedant.numero_rpps}.

ET :

{cessionnaire.denomination}
{cessionnaire.forme_juridique} au capital de {cessionnaire.capital_social}
Ayant son siege au {cessionnaire.siege.adresse_affichee}
En cours d'immatriculation au RCS de {cessionnaire.ville_rcs}
Representee par son {cessionnaire.representant.fonction}, {cessionnaire.representant.identite_complete}

Expose :
{cedant.identite_complete} cede a {cessionnaire.denomination} {scm_cession.parts_cedees.nb} parts de {scm_cedee.denomination}.

Description de la societe cedee :
{scm_cedee.denomination}, {scm_cedee.forme_juridique}, capital {scm_cedee.capital_social}, siege {scm_cedee.siege.adresse_affichee}, RCS {scm_cedee.ville_rcs} numero {scm_cedee.numero_rcs}, cogerants {scm_cedee.cogerants[]}.

Origine de propriete :
{scm_cession.associes_avant_cession[]}

CESSION
Le cedant cede {scm_cession.parts_cedees.nb} parts numerotees de {scm_cession.parts_cedees.plage}.

PRIX
Prix unitaire : {scm_cession.prix.unitaire_lettres} ({scm_cession.prix.unitaire}) euros.
Prix global : {scm_cession.prix.global_lettres} ({scm_cession.prix.global}) euros.

PAIEMENT DU PRIX
Paiement par pret bancaire.
{bloc_credit_vendeur_conditionnel}

SIGNATURE ELECTRONIQUE
Prestataire : {signature.prestataire_electronique}

Fait a {signature.lieu}
En {signature.nombre_exemplaires_lettres} exemplaires originaux
Le {signature.date_ou_zone_manuelle}

Signatures :
{cedant.identite_complete}
{cessionnaire.representant.identite_complete}
```

### 6.3 Overlay SELARL

Source :
- ordre professionnel fixe : chirurgiens-dentistes ;
- cessionnaire affichee comme `SELARL` ;
- capital avec suffixe `EUR` ;
- representant affiche comme `gerant` ;
- phrase de representation utilise les placeholders du cedant ;
- societe cedee affichee comme `Societe Civile de Moyens` ;
- siege de la societe cedee affiche via `[adresse_siege_cessionnaire]` ;
- origine de propriete repete `[nb_parts_cedees]` pour les trois associes ;
- credit-vendeur avec `euros`, `ans`, `%` et retard majore de `3 points` ;
- signature electronique via `Yousign`.

Regle texte :
- conserver ces choix comme overlay SELARL tant qu'aucun arbitrage ne les generalise ;
- ne pas corriger l'adresse de la societe cedee ni les placeholders de parts sans validation ;
- si le representant cessionnaire n'est pas le cedant, le texte SELARL doit etre arbitre avant code.

### 6.4 Overlay SELAS

Source :
- profession ordinale variable : `[profession_reglementee_pluriel]` ;
- cessionnaire variable : `[forme_sociale_cessionnaire]` ;
- representant variable : `[fonction_representant_cessionnaire]` ;
- societe cedee variable : `[forme_sociale_societe_cedee]`, `[adresse_siege_societe_cedee]` ;
- origine de propriete repete `[parts_associe_societe_cedee_1]` pour les trois associes ;
- credit-vendeur sans certaines unites fixes et avec `[majoration_interet_retard]` ;
- signature electronique via `[prestataire_signature_electronique]`.

Regle texte :
- les variables SELAS sont preferables comme generalisation future, mais les formulations source restent a valider ;
- ne pas reparer automatiquement les formulations anormales ;
- `signature.prestataire_electronique` est obligatoire si la clause de signature electronique est rendue.

### 6.5 Bloc credit-vendeur

La source contient une instruction de redaction : `Ajouter en cas de CV`.

Decision texte V1 :
- ce bloc n'est pas un paragraphe fixe ;
- il doit devenir un bloc conditionnel explicitement active par `scm_cession.credit_vendeur.actif` ou rester manuel ;
- si actif, les variables montant, duree, taux et majoration doivent etre completes ;
- si inactif, le texte final ne doit pas conserver l'instruction `Ajouter en cas de CV`.

### 6.6 Limites texte

Blocages avant code :
- origine de propriete non fiable tant qu'une repartition par associe n'est pas fournie ;
- siege de la SCM cedee divergent entre SELARL et SELAS ;
- phrase de representation du cessionnaire a confirmer ;
- date de signature de l'acte non placeholderisee dans la source ;
- clauses de paiement supposees sur pret bancaire ;
- credit-vendeur a transformer en bloc conditionnel ou a exclure ;
- corrections d'orthographe ou de grammaire SELAS interdites sans validation juridique.

## 7. Variables texte obligatoires

### 7.1 Communes au bloc

- `dossier.structure`
- `dossier.options.scm_cession`
- `scm_cedee.denomination`
- `scm_cedee.capital_social`
- `scm_cedee.siege.adresse_affichee`
- `scm_cedee.ville_rcs`
- `scm_cedee.numero_rcs`
- `cessionnaire.denomination`
- `cedant.civilite_affichage`
- `cedant.prenom`
- `cedant.nom`
- `signature.lieu`

### 7.2 PV AGE

- `scm_cession.agrement.date_pv`
- `scm_cession.agrement.date_pv_lettres`
- `scm_cedee.nb_parts_total`
- `scm_cedee.valeur_nominale_part`
- `scm_cedee.plage_parts_total`
- `scm_cession.associes_presents[]`
- `scm_cession.associes_apres_cession[]`
- `cessionnaire.parts.plage`
- `scm_cession.signataires_pv[]`

SELAS uniquement :
- `scm_cession.agrement.delai_mois`
- `scm_cession.agrement.date_limite`

### 7.3 Courrier SDE

- `signature.date`
- `enregistrement.montant_droits`
- `signature.signataire_sde.prenom`
- `signature.signataire_sde.nom`

SELAS uniquement ou generalisation a arbitrer :
- `enregistrement.service`
- `enregistrement.centre_finances_publiques`
- `enregistrement.adresse_service`
- `enregistrement.cp_ville_service`
- `enregistrement.nombre_exemplaires`

### 7.4 Acte de cession

- `cedant.*`
- `cedant.conjoint.*`
- `cessionnaire.*`
- `cessionnaire.representant.*`
- `scm_cedee.*`
- `scm_cession.associes_avant_cession[]`
- `scm_cession.parts_cedees.nb`
- `scm_cession.parts_cedees.plage`
- `scm_cession.prix.unitaire`
- `scm_cession.prix.unitaire_lettres`
- `scm_cession.prix.global`
- `scm_cession.prix.global_lettres`
- `signature.nombre_exemplaires_lettres`

Conditionnels :
- `scm_cession.credit_vendeur.*`
- `signature.prestataire_electronique`
- `signature.date`

## 8. Elements manuels

Elements manuels ou a fournir explicitement :
- les roles exacts des personnes 1 a 4 dans le PV ;
- la nouvelle repartition de capital apres cession ;
- la repartition avant cession dans l'acte ;
- les donnees ordinales du cedant ;
- les donnees conjoint et situation matrimoniale ;
- la validation que le cedant represente ou non la SEL cessionnaire ;
- le montant des droits d'enregistrement ;
- le service d'enregistrement ;
- la date de l'acte ;
- le prestataire de signature electronique si non fixe ;
- le traitement du credit-vendeur ;
- toute correction de wording source.

## 9. Regles de blocage texte

Un futur generateur doit bloquer si :
- le dossier n'est pas SELARL ou SELAS avec option cession SCM ;
- les trois documents du bloc ne sont pas explicitement demandes ou arbitres ;
- les sources ne sont pas stabilisees dans un emplacement documentaire decide ;
- le texte final conserverait un placeholder `[` ou `]` ;
- les roles des associes SCM ne permettent pas de produire le PV et l'acte sans ambiguite ;
- les parts par associe ne totalisent pas le nombre total de parts ;
- le credit-vendeur est actif avec donnees incompletes ;
- le credit-vendeur est inactif mais l'instruction source reste visible ;
- une correction de wording SELAS ou SELARL est appliquee sans note de validation ;
- la variante SELARL non transformee doit etre prise en compte sans comparaison dediee.

## 10. Points ouverts

1. Confirmer le placement ou la reference stable des six sources avant code.
2. Decider le sort de l'acte SELARL non transforme mentionne dans la source de verite.
3. Arbitrer les roles `personne_1`, `personne_2`, `personne_3`, `personne_4`.
4. Valider la repartition des parts par associe dans PV et acte.
5. Confirmer l'adresse de siege de la SCM cedee dans l'acte SELARL.
6. Confirmer le representant de la SEL cessionnaire dans l'acte SELARL.
7. Arbitrer le bloc credit-vendeur.
8. Confirmer si le delai d'agrement SELAS reste specifique.
9. Confirmer si le courrier SDE SELARL doit recevoir le destinataire fiscal et un nombre d'exemplaires variable.
10. Valider ou conserver telles quelles les anomalies de formulation SELAS.
11. Confirmer si la date de l'acte reste manuelle.

## 11. Criteres avant implementation

Un ticket de code pourra demarrer seulement si :
- il cible explicitement un des trois documents ou le bloc complet ;
- les sources de travail sont stabilisees ;
- les points ouverts de roles et repartition sont arbitres ;
- le traitement du credit-vendeur est decide ;
- les overlays SELARL / SELAS sont confirmes ;
- les tests futurs couvrent les blocages principaux ;
- aucun wording juridique n'est modifie silencieusement.

## 12. Statut

`SPEC-SCM-CESSION-BLOCK-001` stabilise la spec texte V1 du bloc cession SCM, sans code Python et sans modification des fichiers de pilotage.

La prochaine etape recommandee est un arbitrage metier avant tout ticket de code.
