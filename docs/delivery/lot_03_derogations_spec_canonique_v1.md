# DAAT x SYDEL - SPEC CANONIQUE V1
## Famille `derogations`

## 1. Objet

Formaliser la famille documentaire `derogations` avant tout codage.

Cette spec couvre les sous-familles demandees dans `SPEC-DEROG-001` :
- site distinct ;
- derogation / declaration pour exercer sur plusieurs sites avec la SEL ;
- cumul SELARL / BNC ;
- cumul salariee ou activite externe ;
- formulaires explicitement a remplir a la main.

Elle ne code rien, ne modifie aucun wording juridique source et ne modifie aucun fichier de pilotage partage.

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
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Sources Lot 03 :
- `project/source_documents/lot_03/README.md`

Constat :
- `project/source_documents/lot_03/` ne contient pas encore les sources DOCX/DOC demandees ;
- les sources utiles ont donc ete lues dans `project/source_import/raw_drive_dump/`, conformement au fallback du ticket.

Sources raw dump lues :
- `project/source_import/raw_drive_dump/Creation SELARL/Derogation/Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Derogation/Demande de derogation cumul SELARL - BNC.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Derogation/Derogation SEL BNC complet.docx`
- `project/source_import/raw_drive_dump/Creation SELARL/Site distinct/Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx`
- `project/source_import/raw_drive_dump/Creation SELAS/Derogation/Demande_derogation_cumul_SELARL_salariee.doc`
- `project/source_import/raw_drive_dump/Creation SELAS/Derogation/Formulaire_derogation_exercer_plusieurs_sites_modele.docx`

Note technique :
- les chemins ci-dessus sont normalises sans accents dans cette spec pour limiter les problemes d'encodage ;
- les fichiers source reels conservent leurs accents et variantes Unicode dans le depot.

## 3. Perimetre documentaire V1

La source de verite rattache les derogations principalement aux structures suivantes :
- SELARL ;
- SELAS.

Rattachements observes :
- SELARL : site distinct, formulaire plusieurs sites SEL, derogation SEL BNC manuelle, cumul SELARL / BNC ;
- SELAS : formulaire plusieurs sites SEL, cumul salariee ou activite externe.

Structures hors perimetre V1 de cette spec :
- SPFPL cession ;
- SPFPL apport ;
- SCS ;
- SCI / SCI IRIS ;
- SCM ;
- SAS.

Conditions metier a conserver separees :
- `dossier.options.site_distinct` : active la famille site distinct ;
- `dossier.options.derogation` : active une sous-famille de derogation ;
- `derogation.type` : doit distinguer le motif documentaire exact avant tout futur code.

Valeurs recommandees pour `derogation.type` :
- `site_distinct_manual`
- `multi_sites_sel`
- `cumul_sel_bnc`
- `cumul_salariee`
- `sel_bnc_manual`

## 4. Sous-familles canoniques

### 4.1 Site distinct - formulaire CD94 a remplir a la main

Source :
- `Creation SELARL/Site distinct/Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx`

Statut source de verite :
- rattache a `Si site distinct` ;
- marque `A REMPLIR A LA MAIN`.

Nature :
- formulaire ordinal de declaration prealable d'ouverture d'un lieu d'exercice distinct ;
- document tres formulaire, avec nombreuses zones libres et cases a cocher ;
- aucune zone placeholder moteur exploitable observee dans la source.

Decision V1 :
- hors automatisation initiale ;
- ne pas creer de generateur sans decision explicite ;
- le moteur peut au mieux lister ce document comme piece manuelle attendue dans un futur dossier ZIP.

### 4.2 Formulaire multi-sites SEL pre-remplissable

Sources :
- `Creation SELARL/Derogation/Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx`
- `Creation SELAS/Derogation/Formulaire_derogation_exercer_plusieurs_sites_modele.docx`

Nature :
- formulaire de declaration prealable d'ouverture d'un site distinct de la residence professionnelle d'une SEL ;
- les variantes SELARL et SELAS ont le meme role documentaire ;
- les deux sources contiennent des zones pre-remplissables et de nombreuses zones narratives a completer.

Variables source observees :
- SELARL : `[denomination_societe]`, `[departement_inscription_societe]`, `[numero_inscription_societe]`, `[adresse_siege]`, `[nom_personne_1]`, `[prenom_personne_1]`, `[fonction_dirigeant]`, `[email_personne_1]`, `[qualification_principale]`, `[choix_oui]`, `[date_debut_activite_site_1]`.
- SELAS : `[denomination_societe]`, `[departement_inscription_societe]`, `[adresse_siege]`, `[cp_siege]`, `[ville_siege]`, `[nom]`, `[prenom]`, `[fonction_dirigeant]`, `[numero_inscription_ordre]`, `[telephone]`, `[telephone_mobile]`, `[email]`, `[qualification_principale]`, `[adresse_lieu_exercice]`, `[date_debut_activite_site_1]`.

Decision V1 :
- partiellement automatisable, uniquement pour les blocs d'identification, societe, representant legal, associe exercant et signature si la source le permet ;
- les zones de description d'activite, moyens, materiels, continuite des soins, environnement professionnel et temps hebdomadaire restent manuelles ;
- le futur generateur, s'il est autorise, devra bloquer si les champs manuels obligatoires ne sont pas fournis ou devra produire explicitement un document marque comme formulaire a completer.

### 4.3 Cumul SELARL / BNC

Source principale :
- `Creation SELARL/Derogation/Demande de derogation cumul SELARL - BNC.docx`

Source proche mais manuelle :
- `Creation SELARL/Derogation/Derogation SEL BNC complet.docx`

Nature de la source principale :
- demande de cumul d'exercices en SEL et a titre individuel ;
- vise les articles R.4113-3 et R.4127-85 du Code de la sante publique ;
- contient des zones pre-remplissables et plusieurs zones explicatives libres.

Variables source observees dans la source principale :
- `[nom]`
- `[prenom]`
- `[ville_ordre]`
- `[numero_inscription_ordre]`
- `[qualification_principale]`
- `[adresse_siege]`
- `[cp_siege]`
- `[ville_siege]`
- `[telephone]`
- `[email]`
- `[denomination_societe]`
- `[ville_ordre_sel]`
- `[numero_inscription_societe]`
- `[date_signature]`
- `[lieu_signature]`

Zones manuelles observees :
- type d'activite individuelle ;
- adresse et temps hebdomadaire de l'activite individuelle ;
- temps hebdomadaire dans la SEL ;
- autres sites d'exercice deja declares ;
- continuite des soins sur les lieux d'exercice ;
- criteres fondant la demande de cumul et explications associees ;
- pieces jointes ;
- eventuel planning d'activites si la variante complete est retenue.

Decision V1 :
- la source principale est partiellement automatisable ;
- `Derogation SEL BNC complet.docx` est classee comme formulaire / aide complete manuelle, sans placeholders, et ne doit pas etre codee en V1 ;
- le futur code ne doit pas fusionner automatiquement ces deux sources sans arbitrage texte.

### 4.4 Cumul salariee ou activite externe

Source :
- `Creation SELAS/Derogation/Demande_derogation_cumul_SELARL_salariee.doc`

Nature :
- ancien format Word `.doc` ;
- fichier place dans l'arborescence SELAS, mais son nom contient `SELARL_salariee` ;
- le texte extrait parle plus largement d'une activite externe.

Variables source observees :
- `[ville_ordre]`
- `[prenom]`
- `[nom]`
- `[numero_inscription_ordre]`
- `[qualification_principale]`
- `[adresse_siege]`
- `[adresse_lieu_exercice]`
- `[date_signature]`

Zones manuelles observees :
- justification du critere R.4113-3 ;
- explications associees aux cases cochees ;
- dispositions prises pour la continuite des soins ;
- reponse aux urgences et organisation pratique ;
- signature manuscrite.

Decision V1 :
- partiellement automatisable apres conversion / stabilisation de la source en DOCX propre ;
- ne pas coder depuis le `.doc` legacy tel quel ;
- qualifier le document en `cumul_salariee` seulement apres validation metier, car le texte source mentionne aussi une activite externe.

### 4.5 Formulaires a remplir a la main

Documents classes manuels en V1 :
- `Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx` ;
- `Derogation SEL BNC complet.docx` ;
- toutes les zones libres narratives des formulaires multi-sites, cumul SELARL/BNC et cumul salariee.

Regle :
- un document marque manuel par la source de verite ou sans placeholders exploitables reste hors automatisation initiale ;
- les champs narratifs ne deviennent pas du texte fixe ;
- ils doivent etre soit saisis manuellement, soit fournis explicitement par le contexte dossier, soit bloquer la generation.

## 5. Variables canoniques

### 5.1 Dossier et selection

- `dossier.structure`
- `dossier.options.site_distinct`
- `dossier.options.derogation`
- `derogation.type`

Valeurs acceptees pour `dossier.structure` en V1 :
- `SELARL`
- `SELAS`

### 5.2 Societe / SEL

- `societe.denomination`
- `societe.forme_sociale`
- `societe.siege.adresse_affichee`
- `societe.siege.cp`
- `societe.siege.ville`
- `societe.inscription_ordre.departement`
- `societe.inscription_ordre.ville`
- `societe.inscription_ordre.numero`

Mappings principaux :
- `[denomination_societe]` -> `societe.denomination`
- `[adresse_siege]` -> `societe.siege.adresse_affichee`
- `[cp_siege]` -> `societe.siege.cp`
- `[ville_siege]` -> `societe.siege.ville`
- `[departement_inscription_societe]` -> `societe.inscription_ordre.departement`
- `[ville_ordre_sel]` -> `societe.inscription_ordre.ville`
- `[numero_inscription_societe]` -> `societe.inscription_ordre.numero`

### 5.3 Signataire / declarant / representant legal

Par defaut, le role canonique est `signataire`.

Si une future spec texte doit distinguer le representant legal de l'associe exercant, ajouter un role local `representant_legal` mappe depuis `signataire` ou depuis `associes[]`.

- `signataire.civilite_affichage`
- `signataire.genre`
- `signataire.prenom`
- `signataire.nom`
- `signataire.fonction`
- `signataire.numero_inscription_ordre`
- `signataire.qualification_principale`
- `signataire.contact.telephone`
- `signataire.contact.telephone_mobile`
- `signataire.contact.email`

Mappings principaux :
- `[prenom]`, `[prenom_personne_1]` -> `signataire.prenom`
- `[nom]`, `[nom_personne_1]` -> `signataire.nom`
- `[fonction_dirigeant]` -> `signataire.fonction`
- `[numero_inscription_ordre]` -> `signataire.numero_inscription_ordre`
- `[qualification_principale]` -> `signataire.qualification_principale`
- `[telephone]` -> `signataire.contact.telephone`
- `[telephone_mobile]` -> `signataire.contact.telephone_mobile`
- `[email]`, `[email_personne_1]` -> `signataire.contact.email`

### 5.4 Ordre professionnel

- `ordre.ville`
- `ordre.conseil_departemental`
- `ordre.departement`

Mappings principaux :
- `[ville_ordre]` -> `ordre.ville`
- `[departement_inscription_societe]` -> `ordre.departement` lorsque la source vise l'inscription de la SEL.

### 5.5 Site declare / lieu d'exercice

- `site_declare.adresse_affichee`
- `site_declare.date_debut_activite`
- `site_declare.activite.type`
- `site_declare.activite.description_consultations`
- `site_declare.activite.description_actes_medico_techniques`
- `site_declare.activite.description_actes_chirurgicaux`
- `site_declare.activite.description_autres`
- `site_declare.temps_hebdomadaire`

Mappings principaux :
- `[adresse_lieu_exercice]` -> `site_declare.adresse_affichee`
- `[date_debut_activite_site_1]` -> `site_declare.date_debut_activite`

Les descriptions d'activite et le temps hebdomadaire sont manuels si absents du contexte.

### 5.6 Sites existants

- `sites_existants[]`
  - `adresse_affichee`
  - `date_debut_activite`
  - `temps_hebdomadaire`
  - `nature_activite`

Regle V1 :
- les formulaires sources prevoient plusieurs sites, souvent jusqu'a 4 ;
- le modele canonique doit etre repetable ;
- si aucune saisie structuree n'est disponible, cette zone reste manuelle.

### 5.7 Cumul SEL / BNC / salariee

- `derogation.cumul.activite_individuelle.type`
- `derogation.cumul.activite_individuelle.adresse_affichee`
- `derogation.cumul.activite_individuelle.temps_hebdomadaire`
- `derogation.cumul.activite_sel.adresse_residence_professionnelle`
- `derogation.cumul.activite_sel.temps_hebdomadaire`
- `derogation.cumul.activite_externe.libelle`
- `derogation.cumul.motifs.regroupement_equipe`
- `derogation.cumul.motifs.equipement_soumis_autorisation`
- `derogation.cumul.motifs.equipement_usages_multiples`
- `derogation.cumul.motifs.explication`

Regle V1 :
- les motifs et leurs explications sont des champs manuels a fournir ;
- aucune case ne doit etre cochee automatiquement sans donnee explicite.

### 5.8 Conditions d'exercice et continuite des soins

- `derogation.conditions.qualite_securite.consultations.moyens_personnel`
- `derogation.conditions.qualite_securite.consultations.materiels`
- `derogation.conditions.qualite_securite.autres_actes.moyens_personnel`
- `derogation.conditions.qualite_securite.autres_actes.materiels`
- `derogation.conditions.continuite_soins`
- `derogation.conditions.environnement_travail`
- `derogation.conditions.reponse_urgences`

Regle V1 :
- ces champs sont manuels et juridiquement sensibles ;
- ne pas inventer de contenu ;
- bloquer ou produire un formulaire explicitement incomplet si ces champs sont requis.

### 5.9 Signature

- `signature.lieu`
- `signature.date`

Mappings principaux :
- `[lieu_signature]` -> `signature.lieu`
- `[date_signature]` -> `signature.date`

## 6. Automatisable vs manuel

### Automatisable apres spec texte et arbitrage

Peuvent etre pre-remplis de maniere deterministe :
- blocs d'identification du declarant / signataire ;
- blocs societe SEL ;
- blocs ordre professionnel ;
- adresse du siege ;
- date previsionnelle de debut d'activite si fournie ;
- adresse du site declare si fournie ;
- date et lieu de signature ;
- rendu des cases uniquement si le contexte contient une valeur explicite.

Documents candidats a un futur generateur partiel :
- `Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx`
- `Formulaire_derogation_exercer_plusieurs_sites_modele.docx`
- `Demande de derogation cumul SELARL - BNC.docx`
- `Demande_derogation_cumul_SELARL_salariee.doc`, apres conversion source.

### Manuel en V1

Restent manuels :
- `Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx` ;
- `Derogation SEL BNC complet.docx` ;
- descriptions de consultations, actes, materiels et moyens ;
- continuite des soins ;
- environnement professionnel ;
- motifs argumentes de derogation ;
- planning d'activites ;
- pieces jointes ;
- signatures manuscrites.

### Regle de blocage

Un futur generateur doit bloquer si :
- la sous-famille n'est pas identifiee ;
- le document est marque manuel ;
- une source DOCX propre n'est pas placee ou arbitree ;
- une zone narrative obligatoire n'est pas fournie alors que le rendu cible ne doit pas rester vierge ;
- un wording juridique devrait etre complete sans source ou validation.

## 7. Comparaison et decisions de canonisation

### 7.1 Site distinct vs multi-sites SEL

Constat :
- le fichier CD94 `site distinct` et les formulaires `plusieurs sites avec la SEL` traitent un objet proche ;
- la source de verite les separe : `Si site distinct` d'un cote, `Si derogation` de l'autre ;
- le CD94 est marque manuel, tandis que les formulaires multi-sites contiennent des placeholders.

Decision V1 :
- ne pas fusionner ces deux sous-familles ;
- `site_distinct_manual` reste une piece manuelle ;
- `multi_sites_sel` peut devenir un document pre-remplissable apres spec texte.

### 7.2 Cumul SELARL/BNC vs SEL BNC complet

Constat :
- `Demande de derogation cumul SELARL - BNC.docx` contient des placeholders ;
- `Derogation SEL BNC complet.docx` ne contient pas de placeholders et ressemble a un formulaire ou dossier complet a remplir.

Decision V1 :
- `cumul_sel_bnc` se fonde sur la source avec placeholders ;
- `sel_bnc_manual` reste manuel et ne sert pas de modele executable ;
- le contenu du fichier complet peut servir de reference de revue, mais pas de source de generation sans arbitrage.

### 7.3 Cumul salariee

Constat :
- la source est un `.doc` legacy ;
- le fichier est dans `Creation SELAS/Derogation`, mais son nom mentionne `SELARL_salariee` ;
- le wording extrait mentionne une activite externe, pas seulement salariee.

Decision V1 :
- classer la sous-famille sous `cumul_salariee` par alignement avec la source de verite ;
- documenter l'ambiguite `salariee` / `activite externe` comme point ouvert ;
- exiger une source DOCX propre avant tout code.

## 8. Criteres avant implementation

Aucun ticket de code ne doit demarrer avant :
- placement ou arbitrage explicite des sources Lot 03 dans `project/source_documents/lot_03/` ;
- spec texte dediee pour chaque sous-famille a coder ;
- decision sur le statut des documents partiellement remplis ;
- validation des champs manuels obligatoires ;
- attribution d'identifiants catalogue definitifs ;
- tests prevus pour chaque sous-famille selectionnable ;
- verification qu'aucun document marque `A REMPLIR A LA MAIN` n'est automatise.

Le futur code devra rester limite a une sous-famille a la fois, sauf ticket explicite de batch.

## 9. Points ouverts

1. Les sources DOCX/DOC Lot 03 ne sont pas encore placees dans `project/source_documents/lot_03/`.
2. Faut-il produire des formulaires pre-remplis avec zones vierges visibles, ou bloquer tant que tous les champs narratifs ne sont pas saisis ?
3. Le formulaire CD94 site distinct et le formulaire multi-sites SEL doivent-ils rester deux documents canoniques distincts ?
4. Le fichier `Derogation SEL BNC complet.docx` est-il une piece manuelle, une aide de remplissage, ou une source texte a specifier ulterieurement ?
5. Le `.doc` `Demande_derogation_cumul_SELARL_salariee.doc` doit etre converti en DOCX propre avant tout codage.
6. La sous-famille `cumul_salariee` doit-elle etre renommee `cumul_activite_externe` cote moteur ?
7. Les roles `signataire`, `representant_legal` et `associe_exercant` doivent etre arbitres quand ils ne designent pas la meme personne.
8. Le formulaire SELARL multi-sites contient `Monsieur [prenom_personne_1] [nom_personne_1]` en signature ; aucune feminisation ne doit etre ajoutee sans validation.
9. La gestion des cases a cocher et plannings d'activites doit etre specifiee avant code.
10. Les pieces jointes obligatoires doivent rester listees, mais leur production automatique n'est pas couverte par cette spec.

## 10. Statut de SPEC-DEROG-001

`SPEC-DEROG-001` est complet cote spec canonique V1, sans code Python et sans modification des fichiers de pilotage.

Prochaine etape recommandee :
- lancer une spec texte ciblee sur une seule sous-famille automatisable, de preference `cumul_sel_bnc` ou `multi_sites_sel`, apres placement/arbitrage des sources Lot 03.
