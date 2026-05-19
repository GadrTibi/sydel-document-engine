# Rapport SELARL-NOTEBOOKLM-RECONCILIATION-001

## Perimetre

Objectif initial : reprendre le cadrage SELARL a partir de la hierarchie de sources NotebookLM -> V3 -> templates / registre -> code, sans modifier l'UI, les generateurs, le moteur DOCX/PDF/ZIP ni la structure existante.

Correction `SELARL-PLAN-CORRECTION-001` : integrer les arbitrages explicites de l'associe comme source prioritaire. Les corrections ci-dessous ne changent ni le code applicatif, ni l'UI, ni les generateurs.

Sources lues :

- `project/source_truth/notebooklm_selarl_10_prompts_v1.md` ;
- `project/source_truth/Documents_a_generer_par_cas_V3.docx` ;
- `project/source_truth/Documents_a_generer_par_cas_V2.docx` ;
- `src/sydel_doc_engine/domain/case_catalog.py` ;
- `src/sydel_doc_engine/app/selarl_form_schema.py` ;
- `src/sydel_doc_engine/app/business_wizard.py` ;
- `src/sydel_doc_engine/app/streamlit_app.py` ;
- `docs/project/SELARL_PROCESS_SPEC_V1.md` ;
- `docs/project/SELARL_FORM_SCHEMA_V1.md` ;
- `docs/project/SELARL_UI_WIZARD_SPEC_V1.md` ;
- `docs/review/selarl_ui_wizard_impl_001_report_v1.md` ;
- `tests/unit/test_selarl_form_schema.py` ;
- `tests/unit/test_business_wizard.py`.

## Etat Git au demarrage repris

Apres validation utilisateur des deux fichiers sources et normalisation des noms, un commit source separe a ete cree :

- `f1da08b docs: add selarl notebooklm and v3 sources`.

Etat demande lors de la reconciliation :

- branche : `main` ;
- commit UI SELARL present : `9993a81 feat: add selarl business wizard ui v1` ;
- le ticket UI SELARL est donc committe, pas seulement en working tree ;
- fichier non suivi hors perimetre : `docs/docssource_truth/`.

Recommandation de sauvegarde :

- ne pas pousser automatiquement ;
- conserver `f1da08b` comme commit source atomique ;
- ne pas inclure `docs/docssource_truth/` sans audit dedie, car il ressemble a un doublon hors ticket ;
- ne pas pousser ni redeployer l'UI SELARL tant que le realignement wording / flow / reutilisation / UI n'est pas termine et valide produit.

## Arbitrages explicites de l'associe

Ces arbitrages corrigent la lecture NotebookLM et priment dans la planification :

- ecran personne : `Fiche Client` ;
- terme pivot : `Praticien` ;
- abandon de l'ancien libelle personne dans les labels visibles et les tickets futurs ;
- ajout d'une logique `Dossier unipersonnel` ;
- mandataire sorti des priorites UX si aucune variable ou document ne le rend central ;
- pas de mode Projet ni filigrane dans la V1 ;
- pas de nouvelle couche produit lourde de statut documentaire sans validation explicite ;
- perimetre SELARL inchange.

## Diagnostic principal corrige

Le cadrage SELARL V1 est solide cote inventaire documentaire V2/V3, mais il reste trop oriente variables et generateurs. NotebookLM apporte un correctif metier utile : vocabulaire juriste, ordre de saisie, roles et reutilisations.

La correction produit prioritaire n'est pas une nouvelle couche documentaire lourde. Elle consiste a realigner le vocabulaire, l'ordre du parcours, la logique `Dossier unipersonnel` et les points UX vraiment necessaires avant un smoke realiste.

L'UI actuelle peut etre reparee, mais elle n'est pas encore validee produit. Le commit `9993a81` ne doit pas etre pousse/redeploie comme version SELARL validee tant que le realignement n'est pas fait.

## Points conserves

- La selection documentaire SELARL par conditions est globalement coherente avec V2/V3.
- Les documents communs `DOC-001`, `DOC-002`, `DOC-003` restent attendus.
- Le PV nomination gerant `DOC-004`, la demande d'inscription a l'ordre `DOC-034` et les statuts `DOC-016` / `DOC-017` restent au coeur du flux.
- `DOC-013` et `DOC-014` sont correctement exclus de la generation pilote et visibles comme manuels.
- `DOC-006` porte correctement une reserve source.
- Les blocs conditionnels cession, SCM, bail, banque, regime communautaire et signature existent dans le schema.
- Les statuts techniques existants du catalogue restent suffisants pour la V1 tant qu'aucun arbitrage produit contraire n'est donne.
- Les tests protegent deja certains garde-fous utiles : pas de label exact `adresse`, documents manuels exclus, mode technique conserve.

## Points a modifier

### A. Vocabulaire

NotebookLM et l'associe convergent sur un point : le terme global recommande est `Praticien`, et l'ecran personne doit etre `Fiche Client`.

Constats actuels :

- `selarl_form_schema.py` utilise encore des formulations centrees sur une personne principale et le gerant ;
- `streamlit_app.py` affiche un ecran personne/gérant qui doit etre renomme ;
- `tests/unit/test_business_wizard.py` valide encore un wording obsolete.

Correction conceptuelle :

- utiliser `Fiche Client` comme titre d'ecran personne ;
- utiliser `Praticien` pour l'identite globale ;
- utiliser `Gerant` seulement pour le mandat social ;
- utiliser `Associe` pour le capital ;
- utiliser `Signataire` pour la signature ;
- utiliser `Mandataire` seulement quand les formalites ou variables le justifient ;
- bannir la transcription erronée de SELARL de toute UI et documentation projet hors citation source.

### B. Ordre des ecrans

Ordre cible confirme :

1. Qualification & type d'operation ;
2. Fiche Client / Praticien ;
3. Fiche Societe ;
4. Capital & Associes ;
5. Contexte & scenarios metier ;
6. Documents & generation.

Ordre actuel SELARL :

1. conditions metier de selection documentaire ;
2. Societe ;
3. personne/gérant ;
4. Associes ;
5. Conditions specifiques ;
6. Documents attendus ;
7. Generation.

Ecart principal : la societe est saisie avant la `Fiche Client`, alors que NotebookLM et l'arbitrage associe font de la personne cliente la source de verite initiale du parcours.

### C. Regles de reutilisation

Regle pivot a integrer :

- `Dossier unipersonnel` : Praticien = associe unique = gerant = signataire lorsque l'option est active.

Regles a garder explicites :

- mandataire distinct du signataire par defaut ;
- SELARL = acquereur / cessionnaire selon cession ou SCM uniquement via option utile ;
- siege social = lieu d'exercice / cabinet seulement si confirme ;
- vendeur = locataire actuel seulement si confirme.

Correction par rapport a la premiere reconciliation :

- le mandataire ne doit plus etre un axe UX majeur ;
- aucun critere central `mandataire Sydel par defaut` ne doit piloter le backlog ;
- le mandataire reste un champ de formalite si V3 ou un template consomme ses variables.

### D. Documents et statuts

V3 classe les documents et variables. NotebookLM signale des risques de presentation trop definitive pour certains actes complexes, mais l'associe a arbitre contre une nouvelle couche produit lourde en V1.

Statut cible V1 :

- conserver les statuts techniques existants : generable, manuel, non implemente, reserve, contexte incomplet si deja present ;
- ne pas presenter un document manuel comme generable ;
- ne pas creer de mode Projet ni filigrane ;
- ne pas ajouter une couche `brouillon/projet` sans validation produit explicite ;
- documenter les reserves si un document depend de pieces ou d'une revue humaine.

La correction se limite donc a la clarte du parcours et des messages existants, pas a un nouveau systeme de statuts.

### E. Champs et formulaires

Champs actuels utiles :

- profession, site distinct, SCM cession, regime communautaire, derogation, cession, type de cabinet ;
- societe, capital, parts, RCS, siege, domiciliation ;
- identite, naissance, nationalite, filiation, adresse personnelle ;
- ordre, RPPS, conseil de l'ordre ;
- associes, mandataire, signataire ;
- regime/conjoint, cession, bail, SCM, banque/financement, signature.

Notions a ajouter ou deplacer :

- titre d'ecran `Fiche Client` ;
- terme pivot `Praticien` ;
- type d'operation : creation, cession de parts, transformation si le parcours SELARL le justifie ;
- logique `Dossier unipersonnel` ;
- source Fiche de creation comme donnee client, sans renommer l'ecran ;
- pieces Ordre en checklist ou information si necessaire, sans inventer un mode produit non arbitre.

Champs demandes trop tot ou au mauvais endroit :

- Societe avant Fiche Client ;
- details Ordre visibles sans lien clair avec le document active ;
- mandataire dans le flux personne si aucune variable ou formalite active ne l'exige.

## Points a abandonner

- Utiliser le libelle banni dans l'UI ou les tickets futurs.
- Traiter `Mandataire = signataire` comme defaut.
- Faire du mandataire Sydel par defaut une exigence centrale du backlog.
- Lancer `SELARL-DOCS-GENERATION-SMOKE-001` comme prochaine etape immediate sans realignement.
- Ajouter un mode Projet ou un filigrane en V1.
- Ajouter une couche produit documentaire lourde non arbitree.
- Presenter tous les documents techniquement generables comme juridiquement finalises.
- Assimiler automatiquement siege, lieu d'exercice, cabinet et domiciliation.
- Assimiler automatiquement vendeur, praticien et locataire.
- Construire le flux SELARL depuis le code existant plutot que depuis la hierarchie corrigee.

## Contradictions NotebookLM vs V3 et arbitrages

| Sujet | NotebookLM | V3 | Arbitrage retenu |
|---|---|---|---|
| Vocabulaire praticien | `Praticien`, `Fiche Client`, roles precis | questions parfois formulees autour du praticien ou dirigeant | Associe + NotebookLM pour les labels visibles ; V3 pour variables. |
| Documents cession / bail / SCM | complexes, souvent a relire ou dependants de pieces | variables listees, documents presents | garder la logique documentaire V3 ; pas de nouveau statut produit V1 sans validation. |
| Derogations | justification metier, pieces, manuel | `DOC-013`/`DOC-014` non fournis ou a remplir a la main | manuel / hors generation pilote. |
| Appel de fonds | peut designer acompte back-office declenche par fiche de creation | `appel de fond sel.docx` en bloc cession | ne pas fusionner sans arbitrage metier. |
| Ordre de saisie | Fiche Client avant societe | V3 est organise par documents et variables | Associe + NotebookLM pilotent l'ordre UI. |
| Mode Projet / filigrane | piste NotebookLM pour banque et Ordre | absent comme variable documentaire generale | non retenu en V1 par arbitrage associe. |
| Mandataire | role distinct a ne pas confondre | variables presentes sur certains documents | traiter si necessaire par variables, sans en faire un sujet UX majeur. |

## Impact par fichier

### `case_catalog.py`

- Ne pas changer les generateurs dans ce ticket.
- Ne pas ajouter de couche statut produit lourde.
- Conserver les statuts techniques existants et les reserves deja presentes.
- Verifier plus tard l'effet de V3 sur `DOC-006`, `DOC-007`, `DOC-009` a `DOC-012`, `DOC-031` a `DOC-033` seulement dans un ticket dedie.

### `selarl_form_schema.py`

- Renommer les labels visibles vers `Praticien` et `Fiche Client`.
- Reordonner les blocs : qualification, Fiche Client / Praticien, societe, capital/associes, scenarios, documents.
- Ajouter ou clarifier la logique `Dossier unipersonnel`.
- Garder le mandataire hors priorite UX s'il n'est pas requis par le document actif.
- Ne pas ajouter de mode Projet ni filigrane.

### `business_wizard.py`

- Modifier les projections de parcours pour que le bloc societe ne precede plus la Fiche Client.
- Supprimer les defaults trompeurs entre mandataire et signataire.
- Porter la logique `Dossier unipersonnel` si elle releve des projections de formulaire.
- Ne pas creer de nouveau statut produit global.

### `streamlit_app.py`

- Reparer le parcours SELARL actuel par realignement controle : titres d'ecrans, ordre, defaults et labels.
- Ne pas modifier dans ce ticket.
- Le mode `Technique / diagnostic` et le parcours SCI doivent rester intacts.
- Le commit UI SELARL existant n'est pas une validation produit ; ne pas pousser ni redeployer avant realignement.

### Tests

- Ajouter des tests anti-regression sur l'absence du libelle banni dans les labels visibles SELARL.
- Mettre a jour le test qui valide l'ancien titre de bloc personne.
- Tester l'ordre logique des blocs SELARL.
- Tester la logique `Dossier unipersonnel`.
- Tester que `mandataire_is_signataire` n'est pas la valeur par defaut.
- Tester que la transcription erronée de SELARL est absente hors source NotebookLM.
- Ne pas ajouter de tests exigeant mode Projet, filigrane ou couche statut produit lourde.

## Risques si on continue sans corriger

- Les juristes verront un langage non metier et risquent de rejeter l'Assistant.
- Les roles signataire / mandataire / gerant / associe peuvent etre inverses.
- Le smoke SELARL produira un resultat techniquement vert mais produit faux.
- Les adresses peuvent etre reutilisees au mauvais endroit.
- L'UI SELARL actuelle pourrait etre poussee ou redeployee comme validee alors qu'elle ne l'est pas.
- La future correction coutera plus cher si elle est faite apres ajout de mappings complexes.

## Conclusion

L'UI actuelle est reparable, mais elle doit etre partiellement realignee avant tout smoke realiste. La bonne sequence corrigee est : wording, flow, regles de reutilisation centrees sur `Dossier unipersonnel`, realignement UI, smoke realiste, revue juriste.

Le commit UI SELARL existant n'est pas encore valide produit. Il ne faut pas le pousser ni le redeployer comme parcours SELARL cible tant que ce realignement n'est pas termine.
