# Lot 04 - batch review humaine V1

Ticket : `REVIEW-BATCH-LOT04-001`
Date : 2026-05-15

## Objet

Preparer un pack de revue humaine pour les statuts Lot 04 deja generes ou, a defaut, disponibles cote sources Lot 04.

Ce document ne vaut pas validation juridique. Il ne modifie aucun wording juridique source et ne remplace pas une relecture humaine des DOCX dans Word.

## Sources relues

Memoire projet :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md`
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md`

Specs et arbitrages Lot 04 :
- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `docs/delivery/lot_04_statuts_sas_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_spfpl_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_sel_exercice_arbitrages_v1.md`
- `docs/delivery/lot_04_statuts_civils_spec_texte_v1.md`
- `docs/delivery/lot_04_statuts_civils_arbitrages_v1.md`
- `docs/delivery/lot_04_statuts_scm_arbitrages_v1.md`

ADR reperes :
- `docs/adr/0001-source-of-truth.md`
- `docs/adr/0002-engine-per-document.md`
- `docs/adr/0005-codex-working-mode.md`

## Etat des artefacts disponibles

DOCX generes relus en lecture seule :
- `artifacts/lot_04_statuts_sas_smoke_test/statuts_sas_spfpl_medecins.docx`
- `artifacts/lot_04_statuts_spfpl_smoke_test/statuts_spfpl_cession.docx`
- `artifacts/lot_04_statuts_spfpl_smoke_test/statuts_spfpl_apport.docx`
- `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selarl_chirurgien_dentiste.docx`
- `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selarl_medecin.docx`
- `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selas_medecin.docx`

DOCX non disponibles dans `artifacts/` au moment de l'analyse :
- statuts SCS ;
- statuts SCI ;
- statuts SCI IRIS ;
- statuts SCM.

Un controle OpenXML rapide sur les DOCX Lot 04 disponibles n'a pas trouve de crochet source residuel `[` ou `]`.

## SAS

### Statuts SAS / SPFPL medecins

- Chemin source : `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx`
- Chemin DOCX genere : `artifacts/lot_04_statuts_sas_smoke_test/statuts_sas_spfpl_medecins.docx`
- Points visuels a verifier :
  - page de garde : denomination, forme SPFPL medecins, capital, siege, titre `STATUTS` ;
  - lisibilite du long bloc de comparution de l'actionnaire unique ;
  - numerotation continue des articles 1 a 27 ;
  - rendu de la signature du president et de l'annexe des engagements ;
  - footer attendu avec la denomination et la mention statuts constitutifs, si conserve par le rendu.
- Points juridiques a verifier :
  - confirmer que le modele nomme SAS mais contenant une SPFPL de medecins est bien le bon support SAS cible ;
  - relire la condition suspensive d'inscription au Tableau de l'Ordre des medecins ;
  - verifier la conservation des termes heterogenes `gerant`, `gerance`, `parts sociales` ou `actions` sans correction implicite ;
  - confirmer la limitation V1 a l'actionnaire unique ;
  - relire la phrase matrimoniale et les donnees ordinales.
- Verdict attendu : corrections.

## SPFPL

### Statuts SPFPL cession

- Chemin source : `project/source_documents/lot_04/Statuts_SPFPLAS_dentistes_cession.docx`
- Chemin DOCX genere : `artifacts/lot_04_statuts_spfpl_smoke_test/statuts_spfpl_cession.docx`
- Points visuels a verifier :
  - en-tete : denomination, forme SPFPL de chirurgiens-dentistes par actions simplifiee, capital, siege ;
  - restitution des articles longs, notamment cession/transmission des actions et decisions collectives ;
  - distinction visuelle des titres d'articles et de l'annexe 1 ;
  - rendu de la signature et de la mention d'acceptation des fonctions de president.
- Points juridiques a verifier :
  - s'assurer que l'overlay cession n'a pas recu de clauses propres a l'apport ;
  - verifier le bloc d'apport en numeraire, la banque et l'adresse de banque ;
  - verifier l'attribution de 100 % des actions a l'associe unique ;
  - relire le wording ordinal chirurgiens-dentistes ;
  - verifier que les engagements de l'annexe cession sont conformes.
- Verdict attendu : corrections.

### Statuts SPFPL apport

- Chemin source : `project/source_documents/lot_04/Statuts SPFPLAS dentistes - apport.docx`
- Chemin DOCX genere : `artifacts/lot_04_statuts_spfpl_smoke_test/statuts_spfpl_apport.docx`
- Points visuels a verifier :
  - en-tete apport, notamment le libelle de forme et le capital ;
  - lisibilite du bloc apports en nature ;
  - rendu du rapport du commissaire aux apports et de l'annexe 1 ;
  - coherence des montants en chiffres et en lettres dans l'article capital ;
  - signature avec date sourcee.
- Points juridiques a verifier :
  - s'assurer que l'overlay apport n'a pas recu de clauses propres a la cession ;
  - verifier la description des parts apportees, leur plage et la societe cible ;
  - verifier la reference au commissaire aux apports ;
  - relire les anomalies source conservees, dont les libelles de forme et repetitions de montant ;
  - confirmer que la V1 reste mono-associe.
- Verdict attendu : corrections.

## SEL d'exercice

### Statuts SELARL chirurgien-dentiste

- Chemin source : `project/source_documents/lot_04/Modele statuts SELARL chirurgien dentiste sans communaute.docx`
- Chemin DOCX genere : `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selarl_chirurgien_dentiste.docx`
- Points visuels a verifier :
  - page de garde : denomination, forme complete, profession, capital et siege ;
  - bloc `LE SOUSSIGNE` sur une seule personne ;
  - titres d'articles et lisibilite des clauses professionnelles ;
  - rendu de la signature electronique si presente ;
  - signature et mention `Lu et approuve`.
- Points juridiques a verifier :
  - verifier que les clauses chirurgien-dentiste n'ont pas ete remplacees par des clauses medecin ;
  - relire l'inscription a l'ordre departemental et le numero RPPS ;
  - verifier les clauses de parts sociales, gerance et sanctions disciplinaires ;
  - confirmer que la generation reste bloquee hors associe unique ;
  - verifier la conservation des coquilles ou corrections uniquement si validees.
- Verdict attendu : corrections.

### Statuts SELARL medecin

- Chemin source : `project/source_documents/lot_04/Modele statuts SELARL medecins.docx`
- Chemin DOCX genere : `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selarl_medecin.docx`
- Points visuels a verifier :
  - en-tete SELARL medecin et capital en euros ;
  - bloc de comparution avec Conseil departemental, numero national et RPPS ;
  - articles de gerance et seuils d'autorisation ;
  - absence de ligne `personne_2` residuelle dans le rendu final ;
  - signatures et nombre d'exemplaires.
- Points juridiques a verifier :
  - verifier que le texte medical reste propre a la SELARL medecin ;
  - relire le traitement de la ligne source `personne_2`, qui ne doit pas autoriser une pluralite non arbitree ;
  - verifier les clauses de non-concurrence, exclusion, deontologie medicale et communication au Conseil departemental ;
  - confirmer que la signature d'un dirigeant non associe reste manuelle ;
  - verifier les champs de situation matrimoniale.
- Verdict attendu : corrections.

### Statuts SELAS medecin

- Chemin source : `project/source_documents/lot_04/Statuts_SELAS_medecin.docx`
- Chemin DOCX genere : `artifacts/lot_04_statuts_sel_exercice_smoke_test/statuts_selas_medecin.docx`
- Points visuels a verifier :
  - en-tete SELAS, capital, siege ;
  - lisibilite des listes de references legales en article 1 ;
  - rendu du ou des lieux d'exercice ;
  - blocs president / directeurs generaux ;
  - signature electronique et mention d'acceptation des fonctions.
- Points juridiques a verifier :
  - verifier que la SELAS n'est pas transformee en SELARL par substitution de termes ;
  - verifier le second lieu : absent si non fourni, bloque si partiel ;
  - confirmer que la fonction dirigeante affichee vient d'une donnee validee, sans feminisation automatique ;
  - verifier l'absence de liste des souscripteurs injectee dans les statuts ;
  - relire le wording ordinal et les clauses medicales.
- Verdict attendu : corrections.

## Civils

### Statuts SCS

- Chemin source : `project/source_documents/lot_04/Statuts_SCS_modele.docx`
- Chemin DOCX genere : non disponible dans `artifacts/` au moment de l'analyse.
- Points visuels a verifier :
  - page de garde, capital minimal/effectif et ville RCS ;
  - distinction visible entre associes commandites et commanditaires ;
  - titres et sous-titres, notamment les `TITRE` et articles ;
  - apports, repartition des parts et signatures ;
  - annexe finale.
- Points juridiques a verifier :
  - roles commandite / commanditaire fournis explicitement et jamais deduits du rang ;
  - coherence entre apports, capital minimal/effectif et parts ;
  - clauses de responsabilite des commandites et gerance personne morale ;
  - situations matrimoniales et qualites associes ;
  - respect de la limite 1 a 6 associes.
- Verdict attendu : corrections.

### Statuts SCI

- Chemin source : `project/source_documents/lot_04/Modele statuts SCI.docx`
- Chemin DOCX genere : non disponible dans `artifacts/` au moment de l'analyse.
- Points visuels a verifier :
  - page de garde avec capital variable et siege ;
  - repetition des associes physiques ;
  - articles 1 a 38, dont apports, capital, cession de parts et gerance ;
  - signatures par associe ;
  - annexe des actes accomplis pour le compte de la societe en formation.
- Points juridiques a verifier :
  - SCI non fusionnee avec SCI IRIS ;
  - coherence apports / capital / parts ;
  - traitement des situations matrimoniales ;
  - option IS non injectee dans les statuts ;
  - annexes et pouvoirs conformes a la source.
- Verdict attendu : corrections.

### Statuts SCI IRIS

- Chemin source : `project/source_documents/lot_04/Modele statuts SCI IRIS.docx`
- Chemin DOCX genere : non disponible dans `artifacts/` au moment de l'analyse.
- Points visuels a verifier :
  - page de garde avec mention SCI IRIS ;
  - article 7 structure en repartition du capital et variabilite ;
  - groupes de parts et quotes-parts de resultat exceptionnel ;
  - article de declaration fiscale ;
  - signatures et annexes.
- Points juridiques a verifier :
  - SCI IRIS non fusionnee avec SCI simple ;
  - donnees de resultat exceptionnel et groupes de parts coherentes ;
  - associe personne morale traite explicitement si present ;
  - declaration fiscale relue humainement ;
  - option IS conservee comme lettre separee.
- Verdict attendu : corrections.

## SCM

Statuts SCM : source disponible, mais aucun smoke DOCX genere n'est disponible dans `artifacts/` au moment de l'analyse. La sous-famille n'est donc pas incluse dans la revue des DOCX generes.

- Chemin source : `project/source_documents/lot_04/Statuts SCM.docx`
- Chemin DOCX genere : non disponible dans `artifacts/` au moment de l'analyse.
- Points visuels a verifier si un smoke est produit :
  - page de garde SCM et denomination courte ;
  - comparution personne morale representee / personne physique ;
  - apports, repartition du capital et signatures ;
  - titres I a VII ;
  - mentions `Lu et approuve` par signataire.
- Points juridiques a verifier si un smoke est produit :
  - parts explicites par associe, sans reutiliser le placeholder source duplique ;
  - ligne fixe `510 EUR` traitee depuis les donnees dossier, pas comme constante ;
  - donnees de representant, RCS, profession et fonction fournies explicitement ;
  - satellites SCM non injectes dans les statuts ;
  - coherence apports / capital / parts.
- Verdict attendu : corrections, apres production d'un smoke SCM.

## Synthese de revue

- SAS : DOCX disponible, revue humaine requise, verdict attendu `corrections`.
- SPFPL : deux DOCX disponibles, revue humaine requise, verdict attendu `corrections`.
- SEL d'exercice : trois DOCX disponibles, revue humaine requise, verdict attendu `corrections`.
- Civils core : sources relues, DOCX generes non disponibles dans l'etat actuel de `artifacts/`, revue a reprendre apres generation ou restauration des artefacts.
- SCM : source relue, aucun smoke disponible ; revue DOCX a ouvrir seulement apres production d'un smoke SCM.
