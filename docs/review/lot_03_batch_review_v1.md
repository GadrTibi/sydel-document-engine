# Revue humaine Lot 03 - batch v1

## Objet

Preparer la revue humaine des DOCX Lot 03 deja generes, sans modifier les sources, le code Python, l'UI, ni les fichiers de pilotage projet.

Cette revue ne vaut pas validation juridique. Elle sert a guider la relecture humaine des rendus DOCX par rapport aux sources Lot 03 et aux specs/arbitrages disponibles.

## Sources de cadrage relues

- `docs/delivery/lot_03_bail_appel_fonds_spec_v1.md`
- `docs/delivery/lot_03_bail_appel_fonds_spec_texte_v1.md`
- `docs/delivery/lot_03_cession_cabinets_spec_canonique_v1.md`
- `docs/delivery/lot_03_cession_cabinets_spec_texte_v1.md`
- `docs/delivery/lot_03_cession_cabinets_arbitrages_v1.md`
- `docs/delivery/lot_03_derogations_spec_canonique_v1.md`
- `docs/delivery/lot_03_derogations_spec_texte_v1.md`
- `docs/delivery/lot_03_derogations_arbitrages_v1.md`
- `docs/delivery/lot_03_derogations_preparation_v1.md`

ADR applicables :
- `docs/adr/0001-source-of-truth.md`
- `docs/adr/0003-lot-based-delivery.md`
- `docs/adr/0005-codex-working-mode.md`

## Sous-batch bail / appel de fonds

### Avenant au contrat de bail

- Chemin source : `project/source_documents/lot_03/Avenant Contrat de bail.docx`
- Chemin DOCX genere : `artifacts/lot_03_bail_appel_fonds_smoke_test/avenant_contrat_bail.docx`

Points visuels a verifier :
- Le titre `Avenant n°1 au bail du ...` doit rester lisible comme titre principal.
- La structure en trois articles doit etre nette : changement de locataire, responsabilite societe en cours de formation, clauses du bail.
- Les espaces entre parties, articles et signature doivent permettre une lecture Word professionnelle.
- La table ou zone de signatures doit restituer correctement les roles attendus : bailleur, ancien locataire, nouveau locataire.
- Le rendu from-scratch contient moins de paragraphes que la source ; verifier qu'aucun bloc visuel utile n'a disparu.

Points juridiques a verifier :
- Le document doit rester limite a une societe en cours d'immatriculation, conformement au wording source.
- L'identite du bailleur et de l'ancien locataire doit etre complete et correctement placee.
- La date du bail initial, le RCS, le siege et la date de signature doivent correspondre au dossier.
- La formulation `demarches seront finies` est un wording source ; toute correction doit etre explicitement arbitree.
- La source contient une anomalie de signatures avec deux cellules `Le nouveau locataire` ; verifier si le rendu retenu est acceptable.

Verdict attendu : OK / corrections

### Appel de fonds SEL

- Chemin source : `project/source_documents/lot_03/appel de fond sel.docx`
- Chemin DOCX genere : `artifacts/lot_03_bail_appel_fonds_smoke_test/appel_fond_sel.docx`

Points visuels a verifier :
- La lettre doit conserver une presentation simple : banque, lieu/date, destinataire, objet, corps, signature.
- Le montant doit etre visible, dans une zone claire, sans libelle source residuel `Montant du fond`.
- Les sauts de ligne autour du montant et de l'euro doivent rester acceptables.
- La signature finale doit etre isolee et lisible.

Points juridiques a verifier :
- Le document doit rester limite a SELARL et cabinet dentaire tant qu'aucun wording medical ou SELAS n'est valide.
- La civilite `Cher Monsieur` reste fixe en V1 ; verifier son adequation au destinataire du dossier.
- Le cabinet cede, le vendeur et la societe acquereur doivent etre les bons roles juridiques.
- Le montant de deblocage doit etre fourni explicitement et ne doit pas etre deduit.
- Verifier que la demande bancaire ne contient aucun placeholder residuel.

Verdict attendu : OK / corrections

## Sous-batch cession cabinets

### Acte de cession d'un cabinet medical

- Chemin source : `project/source_documents/lot_03/Acte de cession d_un cabinet médical.docx`
- Chemin DOCX genere : `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_medical.docx`

Points visuels a verifier :
- Le document genere est sensiblement plus court que la source ; verifier la presence des grandes sections attendues.
- Les titres et intertitres doivent rester reperables malgre le rendu from-scratch.
- Le tableau des chiffres d'affaires/resultats doit contenir trois lignes completes.
- Les zones de prix et de ventilation doivent etre lisibles.
- Les zones de signature, annexes et mentions finales doivent etre visuellement exploitables.

Points juridiques a verifier :
- Le document ne doit pas rendre de clause dentaire dans un acte medical sans validation explicite.
- Le bloc credit-vendeur doit etre absent ou complet selon le contexte ; l'instruction source `Ajouter en cas de CV` ne doit jamais apparaitre.
- La clause SCM et toute reprise de contrats de travail doivent respecter les arbitrages V1.
- Les roles vendeur, acquereur et representant acquereur doivent etre distincts et correctement rendus.
- Les references a l'Ordre des Medecins, au fonds liberal medical, au prix et au transfert de propriete doivent etre relues finement.

Verdict attendu : OK / corrections

### Compromis de cession d'un cabinet medical

- Chemin source : `project/source_documents/lot_03/Compromis de cession d_un cabinet médical.docx`
- Chemin DOCX genere : `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_medical.docx`

Points visuels a verifier :
- Le document genere est sensiblement plus court que la source ; verifier que la promesse, les conditions suspensives et la signature restent visibles.
- Le tableau des trois exercices doit etre complet et lisible.
- La section pret doit presenter montant, taux et duree sans confusion.
- Les zones de date de realisation limite, lieu/date et exemplaires doivent etre clairement restituees.

Points juridiques a verifier :
- Le compromis doit rester une promesse synallagmatique, distincte de l'acte definitif.
- Le bloc origine de propriete medical source contient une anomalie de role ; verifier que le rendu ne change pas le sens juridique.
- Les mentions dentaires presentes dans certaines sources medicales ne doivent pas etre reprises sans validation.
- La date de realisation limite doit correspondre a la variable attendue, pas a la variable source anormale.
- Les conditions suspensives de pret doivent correspondre au contexte dossier.

Verdict attendu : OK / corrections

### Acte de cession d'un cabinet dentaire

- Chemin source : `project/source_documents/lot_03/Acte de cession d'un cabinet dentaire.docx`
- Chemin DOCX genere : `artifacts/lot_03_cession_cabinets_smoke_test/acte_cession_cabinet_dentaire.docx`

Points visuels a verifier :
- Les sections propres au dentaire doivent rester visibles, notamment accessibilite et conciliation ordinale si elles sont attendues.
- Le tableau des chiffres d'affaires/resultats doit contenir trois lignes completes.
- Les salaries repris, s'ils sont rendus, doivent etre presentes de facon lisible.
- Les mentions finales et signatures doivent conserver le mode source du document dentaire.
- Verifier que le nombre de pages/exemplaires et les annexes sont coherents avec le rendu.

Points juridiques a verifier :
- Le document doit rester dentaire : Conseil de l'Ordre des Chirurgiens-Dentistes, RPPS, profession et clauses dentaires.
- L'acte source vise deux salaries ; verifier si le contexte et le wording rendu correspondent exactement a ce cas.
- Les placeholders source parfois ambigus vendeur/acquereur doivent etre remappes selon le role juridique de la clause.
- Le nombre d'exemplaires fixe ou variable doit etre conforme a l'arbitrage applicable.
- Les mentions `Lu et approuve`, conciliation et accessibilite ne doivent pas etre transferees aux documents medicaux.

Verdict attendu : OK / corrections

### Compromis de cession d'un cabinet dentaire

- Chemin source : `project/source_documents/lot_03/Compromis de cession d_un cabinet dentaire.docx`
- Chemin DOCX genere : `artifacts/lot_03_cession_cabinets_smoke_test/compromis_cession_cabinet_dentaire.docx`

Points visuels a verifier :
- La structure de compromis doit rester distincte de l'acte : promesse, conditions suspensives, realisation, signature.
- Le tableau des exercices doit etre complet, malgre les anomalies de placeholders dans la source.
- Les blocs de pret doivent etre lisibles avec le taux source fixe.
- La convention de preuve / signature electronique, si rendue, doit rester identifiable.
- Les zones de signature et mentions finales doivent correspondre au mode source dentaire.

Points juridiques a verifier :
- Le taux de pret fixe `5 %` doit etre conserve comme wording source V1, sauf validation contraire.
- Le document ne doit pas exiger une duree de pret non sourcee pour le compromis dentaire.
- Les roles vendeur, acquereur et representant doivent etre relus a cause des placeholders source ambigus.
- Les clauses de conciliation dentaire doivent etre presentes si elles sont attendues par la source.
- Le document doit rester limite au cabinet dentaire et ne pas reprendre de wording medical.

Verdict attendu : OK / corrections

## Sous-batch derogations coeur

### Formulaire derogation multi-sites SEL

- Chemin source : `project/source_documents/lot_03/Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL.docx`
- Chemin DOCX genere : `artifacts/lot_03_derogations_core_smoke_test/formulaire_derogation_sites_sel_formulaire_a_completer.docx`

Points visuels a verifier :
- Le fichier genere doit etre clairement identifiable comme `formulaire_a_completer`.
- Les zones laissees a completer doivent rester visibles et utilisables dans Word.
- La structure du formulaire doit conserver les grandes rubriques : societe, representant legal, associe exercant, autres sites, conditions d'exercice, pieces.
- Les cases ou choix oui/non ne doivent pas etre cochees par defaut sans donnee explicite.
- Le rendu from-scratch a moins de paragraphes que la source ; verifier que les zones utiles du formulaire n'ont pas ete supprimees.

Points juridiques a verifier :
- Le document ne doit pas etre presente comme finalise si des zones narratives restent vierges.
- Le mapping `personne_1` doit etre valide entre signataire, representant legal et associe exercant.
- Le wording fixe `Monsieur` ne doit pas etre feminise ou corrige sans arbitrage.
- L'adresse du site et l'adresse du siege doivent etre relues, car la source utilise parfois `[adresse_siege]` dans une zone de site.
- Les moyens, materiels, continuite des soins, environnement de travail et pieces jointes doivent rester fournis humainement.

Verdict attendu : OK / corrections

### Demande derogation cumul SELARL / BNC

- Chemin source : `project/source_documents/lot_03/Demande de dérogation cumul SELARL - BNC.docx`
- Chemin DOCX genere : `artifacts/lot_03_derogations_core_smoke_test/demande_derogation_cumul_selarl_bnc_formulaire_a_completer.docx`

Points visuels a verifier :
- Le fichier genere doit etre clairement identifiable comme `formulaire_a_completer`.
- Les blocs d'identification declarant et SEL doivent rester lisibles.
- Les zones de cases, explications, temps hebdomadaires, lieux d'exercice et pieces jointes doivent rester visibles si elles ne sont pas remplies.
- La source contient des tables ; le rendu genere n'en contient pas dans l'extraction technique. Verifier que cette simplification reste acceptable visuellement.
- La date, le lieu et la signature doivent etre presents sans masquer le statut incomplet du formulaire.

Points juridiques a verifier :
- Les references aux articles R.4113-3 et R.4127-85 du Code de la sante publique doivent etre conservees.
- Aucune case de motif ne doit etre cochee sans explication fournie.
- Les zones d'activite individuelle, temps hebdomadaire, continuite des soins et pieces jointes ne doivent pas etre inventees.
- Le wording source `soussigne(e)` et les espaces/ponctuations source ne doivent pas etre corriges sans validation explicite.
- Le document doit rester une demande de cumul SEL / BNC a completer, pas une demande finalisee.

Verdict attendu : OK / corrections

## Hors perimetre de cette revue

- `cumul_salariee` reste bloque tant qu'une source DOCX propre n'est pas disponible.
- `site_distinct_manual` et `sel_bnc_manual` restent hors automatisation initiale.
- PDF, ZIP, UI et tests Python sont hors perimetre de ce pack de revue.

## Conclusion attendue de la revue humaine

Pour chaque document ci-dessus, la revue humaine doit choisir :
- `OK` si le rendu visuel et le contenu juridique sont acceptables pour la V1 ;
- `corrections` si un ticket de correction wording, mapping, structure ou rendu doit etre ouvert avant validation.
