# DAAT x SYDEL - SPEC TEXTE V1
## Famille `cession de cabinets medical / dentaire` - SPEC-TEXTE-CESSION-CAB-001

## 1. Objet

Stabiliser la specification texte V1 de la famille documentaire `cession de cabinets`, avant tout codage.

Cette spec complete la spec canonique :
- `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`

Elle couvre quatre documents sources :
- acte de cession d'un cabinet medical ;
- compromis de cession d'un cabinet medical ;
- acte de cession d'un cabinet dentaire ;
- compromis de cession d'un cabinet dentaire.

Objectif V1 :
- distinguer le tronc commun ;
- distinguer les overlays medical / dentaire ;
- distinguer les ecarts acte / compromis ;
- lister les variables texte ;
- identifier les points manuels ;
- documenter les points ouverts qui bloquent tout futur codage automatique.

Aucun code Python ne doit etre modifie par cette spec.

## 2. Sources lues

Memoire projet et referentiels :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`
- `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0004 : generation DOCX propre from-scratch pour un futur ticket code ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Observation source de verite :
- la famille est declenchee dans les branches `Si cession de cabinet medical` et `Si cession de cabinet dentaire` ;
- chaque branche liste un acte et un compromis ;
- la source de verite ne precise pas si acte et compromis doivent toujours etre produits ensemble ou selon une etape dossier.

Sources DOCX :
- `project/source_documents/lot_03/` ne contient pas les quatre sources attendues, seulement un README ;
- les quatre sources ont donc ete lues dans le fallback `project/source_import/raw_drive_dump/`.

Sources fallback lues :
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Acte de cession d_un cabinet medical.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Compromis de cession/Compromis de cession d_un cabinet medical.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Acte de cession d_un cabinet dentaire.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Cession/Compromis de cession/Compromis de cession d_un cabinet dentaire.docx`

Note fichier :
- la source de verite nomme l'acte dentaire avec apostrophe (`d'un`) ;
- le fichier retrouve dans le raw dump porte un underscore (`d_un`) ;
- ce point est une divergence de nommage source, pas une decision metier.

## 3. Decisions texte V1

### 3.1 Documents canoniques

La V1 conserve quatre documents canoniques distincts :
- `LOT03-CESSION-ACTE-MEDICAL`
- `LOT03-CESSION-COMPROMIS-MEDICAL`
- `LOT03-CESSION-ACTE-DENTAIRE`
- `LOT03-CESSION-COMPROMIS-DENTAIRE`

Raison :
- les textes medical / dentaire sont proches mais pas identiques ;
- les actes et compromis n'ont pas le meme role juridique ;
- plusieurs anomalies source empechent une mutualisation sure.

### 3.2 Wording

Regle V1 :
- le futur code ne doit pas harmoniser les formulations medicales et dentaires sans arbitrage ;
- le futur code ne doit pas corriger les anomalies source sans note de validation ;
- chaque document doit conserver son wording source tant qu'une decision metier ne valide pas une formulation canonique commune.

Les blocs communs peuvent etre mutualises techniquement seulement si le texte source est identique ou si la difference est representee explicitement comme overlay.

### 3.3 Sources SELARL / SELAS

Les quatre sources lues sont les sources SELARL du raw dump.

Des variantes SELAS existent dans le raw dump, mais elles ne sont pas dans la liste de lecture de ce ticket et ne sont pas integrees a cette spec texte.

Decision V1 :
- ne pas generaliser le texte SELARL aux SELAS sans ticket dedie ;
- garder `dossier.structure in {SELARL, SELAS}` comme cadrage canonique deja pose, mais bloquer le wording SELAS si aucune source/validation n'est fournie au moment du code.

## 4. Tronc commun texte

Les quatre documents suivent une architecture commune.

### 4.1 En-tete et parties

Tronc commun :
- titre en deux lignes : nature du document puis type de cabinet ;
- bloc `Entre les soussignes` ;
- identification du vendeur ;
- identification de la societe acquereur ;
- qualification des parties de premiere et seconde part ;
- formule d'ouverture `Il a ete declare fait et convenu ce qui suit`.

Variabilite :
- acte medical : vendeur avec SIREN, ordre, conjoint et regime matrimonial ;
- compromis medical : vendeur avec SIREN, ordre, conjoint, regime matrimonial et mention `sans contrat de mariage` ;
- acte dentaire : vendeur avec Conseil des chirurgiens-dentistes et RPPS ;
- compromis dentaire : vendeur avec SIREN, ordre et situation maritale, sans conjoint detaille dans la source lue.

Point sensible :
- les sources dentaires reutilisent parfois les placeholders vendeur dans le bloc representant acquereur ;
- ne pas transformer automatiquement ces placeholders en representant acquereur sans arbitrage.

### 4.2 Objet du contrat

Tronc commun :
- le document presente la cession ou la promesse de cession du fonds liberal ;
- le texte fixe les conditions de la cession, le transfert de propriete et la jouissance.

Acte :
- wording de cession definitive : le vendeur `cede et transporte` au cessionnaire ;
- le document determine les conditions de la cession et les modalites de transfert.

Compromis :
- wording de promesse synallagmatique : le promettant promet de vendre et le beneficiaire accepte et s'engage a acquerir ;
- la cession reste soumise aux conditions suspensives.

Overlay medical :
- acte medical : fonds liberal de medecin ;
- compromis medical : fonds liberal de `[nature_fonds_liberal]`.

Overlay dentaire :
- acte dentaire : fonds liberal de `[profession_vendeur]` ;
- compromis dentaire : fonds liberal de `[profession_vendeur]`.

### 4.3 Declarations des parties

Tronc commun :
- declaration sur etat civil / existence juridique ;
- absence de poursuites ou mesures pouvant entrainer confiscation ;
- pleine capacite juridique ;
- absence de restriction legale, judiciaire ou contractuelle faisant obstacle a la cession.

Decision V1 :
- conserver les variations grammaticales source (`soumise` / `soumis`) par document ;
- ne pas corriger la formulation sans validation juridique.

### 4.4 Declaration du vendeur et consistance du fonds liberal

Tronc commun :
- propriete du cabinet ;
- patientele et fichiers ;
- dossiers, archives ou informations patients ;
- droit au bail ou droit d'exercer dans les lieux ;
- ligne telephonique ;
- instruments, materiel professionnel, meubles et objets mobiliers ;
- autorisations transmissibles ;
- contrats, marches, traites et conventions ;
- exclusion des elements d'actif hors fonds liberal.

Overlay medical :
- `cabinet medical` ;
- mention de dossiers medicaux ;
- maintien du cabinet medical dans son etat actuel dans l'acte.

Overlay dentaire :
- `cabinet dentaire` ;
- acte dentaire : `droit d'exercer dans les lieux` au lieu de `droit au bail` dans la liste de consistance ;
- acte dentaire : `contrats, encours, marches, traites et conventions passees dans le cadre de l'activite liberale`.

### 4.5 Origine de propriete

Tronc commun :
- section `Sur l'origine de propriete`.

Medical :
- acte medical : acquisition de la patientele en `[annees_acquisition_patientele]` + description manuelle ;
- compromis medical : origine de propriete sur `[date_origine_propriete]`, mais la source attribue la propriete au representant acquereur, ce qui est probablement une anomalie.

Dentaire :
- acte dentaire : acquisition aupres d'un precedent proprietaire, avec prix d'origine ;
- compromis dentaire : creation reguliere a `[date_origine_propriete]`.

Point sensible :
- le compromis medical doit etre relu avant code, car la personne designee comme proprietaire ne correspond pas naturellement au vendeur.

### 4.6 Droit au bail

Tronc commun :
- date du bail ;
- duree ;
- date de debut et date de fin quand presentes ;
- reconductions quand presentes ;
- loyer mensuel quand present ;
- absence d'arriere de loyer ;
- absence de sous-location ou droit d'occupation consenti ;
- absence de sommation, conge ou differend bailleur ;
- absence de remise du cabinet a un tiers en infraction au bail.

Medical :
- acte medical : bail a usage exclusivement professionnel, loyer non soumis a TVA, activite medicale et paramedicale ;
- compromis medical : contient pourtant une formulation d'activite de chirurgien-dentiste / stomatologue / docteur en medecine.

Dentaire :
- acte dentaire : bloc plus court, sans dates de debut/fin/reconduction ni loyer mensuel dans la source lue ;
- compromis dentaire : activite de `[profession_vendeur], stomatologue, docteur en medecine`.

Point ouvert majeur :
- les mentions dentaires dans des sources medicales ne doivent pas etre corrigees automatiquement ;
- il faut une validation metier pour savoir si elles sont des erreurs source ou des clauses voulues.

### 4.7 Chiffres d'affaires et resultats

Tronc commun :
- tableau de trois exercices ;
- colonnes : exercice, chiffre d'affaires, resultat.

Decision V1 :
- le futur modele doit utiliser `cession.exercices[]` avec trois lignes structurees ;
- le rendu doit bloquer si les trois lignes ne sont pas completes.

Anomalies source :
- les compromis medical et dentaire reutilisent `[chiffre_affaires_1]` / `[resultat_1]` pour le deuxieme exercice ;
- l'acte dentaire contient des periodes fixes 2023/2024/2025 collees ou melangees avec les placeholders ;
- ces anomalies ne doivent pas etre reproduites sans arbitrage.

### 4.8 Situation generale et libre disposition

Tronc commun :
- libre disposition et pleine propriete du materiel ;
- absence de saisie / confiscation ;
- absence de pret, location, reserve de propriete ou depot par tiers ;
- bon fonctionnement ;
- normes de salubrite, hygiene et securite ;
- absence d'autre promesse ou engagement ;
- absence d'interdiction administrative, judiciaire ou autre ;
- absence d'instance avec un patient ;
- declarations de l'acquereur sur absence d'obstacle et aptitude a exercer.

Overlay medical :
- exercice de l'activite de medecin.

Overlay dentaire :
- exercice de l'activite de `[profession_vendeur]`.

### 4.9 Prix et repartition

Tronc commun :
- prix principal en lettres et en chiffres ;
- ventilation elements corporels / incorporels ;
- reference a l'article L. 141-5 du Code de commerce ;
- caractere intangible du prix total.

Decision V1 :
- conserver la ventilation en trois montants : total, corporels, incorporels ;
- bloquer si la somme ou la repartition ne peut pas etre rendue proprement, sauf decision explicite de ne pas controler l'arithmetique en V1.

### 4.10 Prorata d'exploitation

Tronc commun :
- paiement comptant par l'acquereur des prorata d'exploitation dus au titre des charges d'exploitation ;
- deduction des prorata inverses.

Decision V1 :
- bloc commun mutualisable sous reserve de conserver exactement les variantes grammaticales source par document.

### 4.11 Conditions a la charge des parties

Tronc commun vendeur :
- garantie des enonciations sur origine de propriete et consistance ;
- effort de conservation de la patientele ;
- remise des dossiers / fichiers / justificatifs ;
- reglement des charges jusqu'a l'entree en jouissance ;
- remboursement des charges anterieures payees par l'acquereur ;
- prise en charge des contrats et engagements ;
- transmission des correspondances, appels, informations et dossiers patients.

Tronc commun acquereur :
- prise du fichier et des dossiers patients ;
- acceptation du risque de diminution du chiffre d'affaires lie a la patientele ;
- paiement des frais, droits et honoraires.

Overlays :
- acte medical : clause de cession de parts SCM ;
- acte medical : ligne incomplete `De reprendre les contrats de travail de` ;
- acte dentaire : reprise de deux salaries nommes par placeholders.

Decision V1 :
- la clause SCM et les salaries restent des blocs conditionnels/manuels ;
- aucune reprise salarie ne doit etre imposee globalement au tronc commun.

### 4.12 Droits, frais, communication ordinale et domicile

Tronc commun :
- droits d'enregistrement ;
- frais, droits et honoraires a la charge de l'acquereur ;
- communication du contrat au Conseil departemental de l'Ordre ;
- election de domicile.

Acte :
- affirmation de sincerite ;
- transfert de propriete.

Compromis :
- faculte de substitution ;
- conditions suspensives ;
- propriete/jouissance differee a la signature de l'acte.

Overlay medical :
- Ordre des Medecins.

Overlay dentaire :
- Ordre des Chirurgiens-Dentistes ;
- clause de conciliation ordinale presente dans l'acte et le compromis dentaires.

## 5. Overlays medical / dentaire

### 5.1 Medical

L'overlay medical porte au minimum sur :
- titre `cabinet medical` ;
- fonds liberal de medecin ou nature de fonds liberal ;
- Ordre des Medecins ;
- declarations d'aptitude a exercer la profession de medecin ;
- acte medical : pret bancaire + credit-vendeur conditionnel ;
- acte medical : clause SCM conditionnelle ;
- acte medical : immatriculation RCS et inscription a l'Ordre dans le transfert de propriete.

Points de prudence medical :
- les blocs bail contiennent des formulations dentaires dans certaines sources ;
- la ligne de reprise des contrats de travail de l'acte medical est incomplete ;
- le bloc credit-vendeur commence par une instruction source et doit etre transforme en conditionnel avant code.

### 5.2 Dentaire

L'overlay dentaire porte au minimum sur :
- titre `cabinet dentaire` ;
- Conseil de l'Ordre des Chirurgiens-Dentistes ;
- numero RPPS dans l'acte dentaire ;
- profession affichee via `[profession_vendeur]` dans plusieurs clauses ;
- acte dentaire : accessibilite des cabinets dentaires aux personnes handicapees ;
- acte dentaire : reprise de deux salaries ;
- acte et compromis dentaires : clause de conciliation devant le President du Conseil departemental ;
- compromis dentaire : taux de pret fixe a `5 %` dans la source ;
- acte dentaire : mentions finales `Lu et approuve`.

Points de prudence dentaire :
- les sources dentaires reutilisent parfois les placeholders du vendeur pour representer le representant de l'acquereur ;
- l'acte dentaire ne contient pas les placeholders de signature image `[signature_vendeur]` / `[signature_acquereur]` ;
- le nombre d'exemplaires de l'acte dentaire est fixe a `quatre exemplaires` dans la source.

## 6. Difference acte / compromis

### 6.1 Acte de cession

Role texte :
- formaliser la vente definitive ;
- rendre le paiement du prix ;
- rendre le transfert de propriete ;
- rendre l'affirmation de sincerite ;
- rendre la convention de preuve / signature electronique quand presente ;
- lister les annexes.

Blocs acte communs :
- `Conditions de la vente`
- `PRIX`
- `PAIEMENT DU PRIX`
- `DISPENSE DE GARANTIE D'ACTIF ET DE PASSIF`
- `PRORATA D'EXPLOITATION`
- `CONDITIONS`
- `DROIT ENREGISTREMENT`
- `TRANSFERT DE PROPRIETE`
- `FRAIS, DROITS ET HONORAIRES`
- `COMMUNICATION DU PRESENT CONTRAT AU CONSEIL DE L'ORDRE ...`
- `AFFIRMATION DE SINCERITE`
- `ELECTION DE DOMICILE - ATTRIBUTION DE JURIDICTION`
- `CONVENTION SUR LA PREUVE - SIGNATURE ELECTRONIQUE`

Variantes acte :
- acte medical : paiement par pret bancaire et bloc credit-vendeur conditionnel ;
- acte dentaire : paiement comptant ;
- acte dentaire : bloc accessibilite ;
- acte dentaire : clause de conciliation ;
- acte dentaire : signature textuelle avec mentions manuscrites ;
- acte medical : signature par placeholders image, mais date de signature absente apres `Le` dans la source lue.

### 6.2 Compromis de cession

Role texte :
- formaliser la promesse synallagmatique ;
- fixer une date limite de realisation ;
- prevoir les conditions suspensives ;
- preparer l'acte de cession.

Blocs compromis communs :
- `Promesse de vente et d'achat du cabinet ...`
- `PROMESSE SYNALLAGMATIQUE DE VENTE`
- `PRIX`
- `PRORATA D'EXPLOITATION`
- `[date_origine_propriete] PREVUE DE REALISATION`
- `CONDITIONS`
- `PROPRIETE - JOUISSANCE`
- `CONDITIONS SUSPENSIVES`
- `DROIT ENREGISTREMENT`
- `FACULTE DE SUBSTITUTION`
- `FRAIS, DROITS ET HONORAIRES`
- `COMMUNICATION DU PRESENT CONTRAT AU CONSEIL DE L'ORDRE ...`
- `ELECTION DE DOMICILE - ATTRIBUTION DE JURIDICTION`

Variantes compromis :
- compromis medical : pret avec montant, taux et duree ;
- compromis dentaire : pret avec montant et taux source fixe `5 %`, sans duree variable ;
- compromis dentaire : convention de preuve / signature electronique detaillee ;
- compromis medical : pas de convention de preuve / signature electronique observee dans la source lue.

Point ouvert :
- le titre `[date_origine_propriete] PREVUE DE REALISATION` semble anormal ; il doit etre arbitre avant code.

## 7. Variables

### 7.1 Variables de selection

- `dossier.structure`
- `dossier.options.cession`
- `dossier.cession.type_cabinet`
- `dossier.cession.etape`

Valeurs attendues :
- `dossier.options.cession == true`
- `dossier.cession.type_cabinet in {medical, dentaire}`
- `dossier.cession.etape in {acte, compromis}`

### 7.2 Variables parties

Vendeur :
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

Conjoint vendeur :
- `cession.vendeur.conjoint.civilite_affichage`
- `cession.vendeur.conjoint.prenom`
- `cession.vendeur.conjoint.nom`

Acquereur :
- `cession.acquereur.denomination_societe`
- `cession.acquereur.forme_sociale`
- `cession.acquereur.capital_social`
- `cession.acquereur.siege.adresse_affichee`
- `cession.acquereur.rcs_ville`
- `cession.acquereur.numero_rcs`
- `cession.acquereur.numero_siret`
- `cession.acquereur.date_immatriculation`
- `cession.acquereur.date_inscription_ordre`

Representant acquereur :
- `cession.acquereur.representant.civilite_affichage`
- `cession.acquereur.representant.genre`
- `cession.acquereur.representant.prenom`
- `cession.acquereur.representant.nom`
- `cession.acquereur.representant.fonction`

### 7.3 Variables cabinet / bail

Cabinet :
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

Bail :
- `cession.bail.date_bail`
- `cession.bail.duree`
- `cession.bail.date_debut`
- `cession.bail.date_fin`
- `cession.bail.date_reconduction_1`
- `cession.bail.date_reconduction_2`
- `cession.bail.loyer_mensuel`
- `cession.bail.activite_autorisee_affichee`

Exercices :
- `cession.exercices[]`
  - `periode`
  - `chiffre_affaires`
  - `resultat`

### 7.4 Variables prix / financement

Prix :
- `cession.prix.total`
- `cession.prix.total_lettres`
- `cession.prix.elements_corporels`
- `cession.prix.elements_corporels_lettres`
- `cession.prix.elements_incorporels`
- `cession.prix.elements_incorporels_lettres`

Pret :
- `cession.financement.pret.montant`
- `cession.financement.pret.taux`
- `cession.financement.pret.duree`

Credit-vendeur :
- `cession.financement.credit_vendeur.actif`
- `cession.financement.credit_vendeur.montant`
- `cession.financement.credit_vendeur.duree`
- `cession.financement.credit_vendeur.taux`
- `cession.financement.credit_vendeur.majoration_interet_retard`

### 7.5 Variables specifiques / signature

Clauses specifiques :
- `cession.scm.nb_parts_a_ceder`
- `cession.salaries[]`
  - `civilite_affichage`
  - `prenom`
  - `nom`
- `cession.accessibilite_cabinet_dentaire.information_requise`
- `cession.date_entree_jouissance`

Document :
- `document.nombre_pages_lettres`
- `document.nombre_exemplaires_lettres`
- `document.annexes[]`

Signature :
- `signature.lieu`
- `signature.date`
- `signature.vendeur.image_optionnelle`
- `signature.acquereur.image_optionnelle`
- `signature.mentions_manuscrites_requises`

## 8. Points manuels

Doivent rester saisis, fournis par contexte ou valides humainement :
- origine de propriete et description d'origine ;
- date ou annees d'acquisition / creation ;
- precedent proprietaire ;
- details du bail professionnel ;
- activite autorisee par le bail ;
- chiffres d'affaires et resultats des trois exercices ;
- repartition du prix ;
- conditions de pret ;
- activation et contenu du credit-vendeur ;
- activation et contenu de la clause SCM ;
- salaries repris ;
- accessibilite des cabinets dentaires ;
- date limite de realisation du compromis ;
- date d'entree en jouissance ;
- nombre de pages ;
- nombre d'exemplaires ;
- signatures ;
- mentions manuscrites ;
- annexes.

Les annexes ne sont pas generees automatiquement en V1 faute de source annexe detaillee.

## 9. Points ouverts

1. La source de verite liste acte et compromis dans chaque branche, mais ne precise pas si les deux documents doivent etre produits ensemble.
2. Les sources lues sont SELARL ; les variantes SELAS ne sont pas stabilisees par ce ticket.
3. Les sources medicales contiennent des mentions dentaires dans le bloc bail.
4. Les sources dentaires reutilisent parfois les placeholders vendeur pour le representant de l'acquereur.
5. Le compromis medical designe le representant acquereur comme proprietaire dans le bloc origine de propriete.
6. Les compromis contiennent un titre anormal `[date_origine_propriete] PREVUE DE REALISATION`.
7. Les compromis reutilisent les placeholders du premier exercice pour le deuxieme exercice.
8. L'acte dentaire contient des periodes fixes 2023/2024/2025 collees ou melangees avec les placeholders.
9. Le taux de pret du compromis dentaire est fixe a `5 %`, contrairement au compromis medical.
10. L'acte medical contient une instruction source `Ajouter en cas de CV` a transformer en bloc conditionnel.
11. L'acte medical contient une clause SCM a arbitrer avec la famille SCM separee.
12. L'acte medical contient une ligne incomplete de reprise des contrats de travail.
13. L'acte dentaire impose deux salaries dans la source, mais le modele canonique doit rester repetable.
14. L'acte medical a une ligne finale `Le` sans `[date_signature]` dans la source extraite.
15. L'acte dentaire fixe `quatre exemplaires` au lieu d'utiliser `document.nombre_exemplaires_lettres`.
16. Les signatures divergent fortement : images de signature, mentions manuscrites, signature electronique courte ou detaillee.
17. Les clauses dentaires d'accessibilite et de conciliation ne doivent pas etre transferees aux documents medicaux.
18. Les annexes sont titrees seulement ; aucun contenu annexe exploitable n'est source.

## 10. Regles de blocage avant futur code

Un futur ticket de code doit bloquer si :
- le type de cabinet est absent ou hors `medical` / `dentaire` ;
- l'etape `acte` / `compromis` n'est pas explicite ;
- le document est demande pour une structure dont le wording n'a pas ete stabilise ;
- les donnees vendeur / acquereur / cabinet / prix / signature sont incompletes ;
- les trois exercices ne peuvent pas etre rendus proprement ;
- une clause conditionnelle est activee sans donnees suffisantes ;
- une anomalie source listee comme point ouvert n'a pas ete arbitree ;
- un wording medical est sur le point d'etre applique a un document dentaire, ou inversement.

## 11. Critere de completion

`SPEC-TEXTE-CESSION-CAB-001` est complet pour une stabilisation texte V1 sans codage.

Avant tout code, il reste necessaire de :
- arbitrer les points ouverts ;
- decider le mode de selection acte / compromis ;
- valider les corrections eventuelles de wording source ;
- attribuer les identifiants catalogue definitifs ;
- definir les tests attendus par type de cabinet et type de document.
