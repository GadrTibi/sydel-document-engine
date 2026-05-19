# Rapport SELARL-NOTEBOOKLM-RECONCILIATION-001

## Périmètre

Objectif : reprendre le cadrage SELARL à partir de la hiérarchie de sources NotebookLM -> V3 -> templates / registre -> code, sans modifier l'UI, les générateurs, le moteur DOCX/PDF/ZIP ni la structure existante.

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

## Etat Git au démarrage repris

Après validation utilisateur des deux fichiers sources et normalisation des noms, un commit source séparé a été créé :

- `f1da08b docs: add selarl notebooklm and v3 sources`.

Etat demandé :

- branche : `main` ;
- `main` est ahead de `origin/main` par 1 commit au moment de l'audit ;
- commit UI SELARL présent : `9993a81 feat: add selarl business wizard ui v1` ;
- le ticket UI SELARL est donc committé, pas seulement en working tree ;
- `git diff --name-status` vide après le commit source ;
- fichier non suivi hors périmètre : `docs/docssource_truth/`.

Recommandation de sauvegarde :

- ne pas pousser automatiquement ;
- conserver `f1da08b` comme commit source atomique ;
- ne pas inclure `docs/docssource_truth/` sans audit dédié, car il ressemble à un doublon hors ticket.

## Diagnostic principal

Le cadrage SELARL V1 est solide côté inventaire documentaire V2/V3, mais il est trop orienté variables et générateurs. NotebookLM impose une correction produit : vocabulaire juriste, ordre de saisie, rôles, réutilisations et statut `Projet` doivent être réalignés avant un smoke réaliste.

L'UI actuelle peut être réparée, mais pas par simples retouches de labels. Elle nécessite une refonte partielle contrôlée du parcours SELARL : ordre des écrans, vocabulaire, règles de réutilisation et statuts documentaires.

## Points conservés

- La sélection documentaire SELARL par conditions est globalement cohérente avec V2/V3.
- Les documents communs `DOC-001`, `DOC-002`, `DOC-003` restent attendus.
- Le PV nomination gérant `DOC-004`, la demande d'inscription à l'ordre `DOC-034` et les statuts `DOC-016` / `DOC-017` restent au coeur du flux.
- `DOC-013` et `DOC-014` sont correctement exclus de la génération pilote et visibles comme manuels.
- `DOC-006` porte correctement une réserve source.
- Les adresses sont déjà mieux qualifiées que dans le premier cadrage.
- Les blocs conditionnels cession, SCM, bail, banque, régime communautaire et signature existent dans le schéma.
- Les tests protègent déjà certains garde-fous utiles : pas de label exact `adresse`, documents manuels exclus, mode technique conservé.

## Points à modifier

### A. Vocabulaire

NotebookLM indique que `professionnel principal` n'est pas un terme source et doit être évité dans les labels visibles. Le terme global recommandé est `Praticien`.

Constats actuels :

- `selarl_form_schema.py` utilise `Professionnel / gérant`, `Identité du professionnel principal`, `Fonction du professionnel principal`.
- `streamlit_app.py` affiche `Ecran 3 - Professionnel principal / gerant` et plusieurs labels `professionnel principal`.
- `tests/unit/test_business_wizard.py` valide explicitement `Gerant / professionnel principal`.

Correction conceptuelle :

- utiliser `Praticien` pour l'identité globale ;
- utiliser `Gérant` seulement pour le mandat social ;
- utiliser `Associé` pour le capital ;
- utiliser `Signataire` pour la signature ;
- utiliser `Mandataire` pour les formalités ;
- bannir `CELAR` de toute UI et documentation projet hors citation de transcription ;
- évaluer `Fiche Client` comme titre d'écran recommandé, `Fiche de création` comme nom métier de la donnée source.

### B. Ordre des écrans

Ordre NotebookLM :

1. Qualification & type d'opération ;
2. Fiche Client / Praticien ;
3. Fiche Société ;
4. Capital & Associés ;
5. Contexte & scénarios métier ;
6. Documents & génération.

Ordre actuel SELARL :

1. conditions métier de sélection documentaire ;
2. Société ;
3. Professionnel principal / gérant ;
4. Associés ;
5. Conditions spécifiques ;
6. Documents attendus ;
7. Génération.

Ecart principal : la société est saisie avant le praticien, alors que NotebookLM fait de la Fiche Client / Fiche de création la source de vérité initiale. La qualification actuelle ne contient pas explicitement `type d'opération` au sens création / cession / transformation.

### C. Règles de réutilisation

Règles NotebookLM à intégrer :

- Praticien = associé unique = gérant = signataire dans les dossiers unipersonnels ;
- Mandataire distinct du signataire par défaut ;
- Mandataire = membre Sydel par défaut ;
- SELARL = acquéreur / cessionnaire selon cession ou SCM ;
- Siège social = lieu d'exercice / cabinet seulement si confirmé ;
- Vendeur = locataire actuel seulement si confirmé.

Constats actuels :

- `mandataire_is_signataire` existe et est coché par défaut dans l'UI : c'est contraire au cadrage NotebookLM.
- `signataire_is_associe_1` copie le signataire vers l'associé 1, alors que la source métier devrait être le praticien.
- `gerant_is_professional` va dans la bonne direction, mais le wording doit devenir `Le gérant est le praticien`.
- `selarl_is_acquirer` et `selarl_is_scm_transferee` sont cohérents, sous réserve d'un choix explicite.
- aucune règle dédiée ne couvre `vendeur = locataire actuel`.
- aucune règle dédiée ne couvre `siège = lieu d'exercice / cabinet` sans automatisme.

### D. Documents et statuts

V3 classe de nombreux documents comme documentés par variables, mais NotebookLM demande de ne pas les présenter comme définitifs.

Statuts à affiner :

- documents 100 % générables simples : `DOC-001`, `DOC-002`, `DOC-003` sous réserve des champs ;
- documents générables en mode projet / brouillon à relire : statuts, PV, demande d'ordre, cession, bail, SCM ;
- documents manuels : site distinct CD94, `DOC-013`, `DOC-014`, pièces de dérogation SEL/BNC ;
- documents nécessitant pièces ou justification : plans/devis pour l'Ordre, dérogation de lieu, origine de propriété du fonds, bail d'origine ;
- documents avec réserve source : `DOC-006`.

Le statut actuel `Générable` est trop binaire. Il doit distinguer `Projet`, `Brouillon à relire`, `Manuel`, `Pièces requises`, `Contexte incomplet`.

### E. Champs et formulaires

Champs actuels utiles :

- profession, site distinct, SCM cession, régime communautaire, dérogation, cession, type de cabinet ;
- société, capital, parts, RCS, siège, domiciliation ;
- identité, naissance, nationalité, filiation, adresse personnelle ;
- ordre, RPPS, conseil de l'ordre ;
- associés, mandataire, signataire ;
- régime/conjoint, cession, bail, SCM, banque/financement, signature.

Champs ou notions manquants depuis NotebookLM :

- titre d'écran `Fiche Client` ;
- type d'opération : création, cession de parts, transformation ;
- numéro de sécurité sociale ;
- téléphone professionnel ;
- statut `mode Projet` / filigrane ;
- distinction banque de dépôt vs banque d'exploitation ;
- membre Sydel mandataire par défaut ;
- checklist pièces Ordre : plans, devis, justificatifs ;
- source Fiche de création comme donnée validée par le client ;
- vendeur = locataire actuel en règle optionnelle ;
- siège = lieu d'exercice / cabinet en règle optionnelle.

Champs demandés trop tôt ou au mauvais endroit :

- Société avant Fiche Client ;
- Ordre professionnel toujours visible dans l'écran praticien alors que certains détails peuvent dépendre du type d'opération et du document activé ;
- Mandataire dans l'écran praticien/gérant avec un défaut signataire, alors qu'il relève des formalités.

## Points à abandonner

- Utiliser `professionnel principal` comme libellé visible.
- Traiter `Mandataire = signataire` comme défaut.
- Lancer `SELARL-DOCS-GENERATION-SMOKE-001` comme prochaine étape immédiate sans réalignement.
- Présenter tous les documents techniquement générables comme prêts juridiquement.
- Assimiler automatiquement siège, lieu d'exercice, cabinet et domiciliation.
- Assimiler automatiquement vendeur, praticien et locataire.
- Construire le flux SELARL depuis le code existant plutôt que depuis la hiérarchie NotebookLM/V3.

## Contradictions NotebookLM vs V3

| Sujet | NotebookLM | V3 | Arbitrage recommandé |
|---|---|---|---|
| Vocabulaire praticien | `Praticien`, `Fiche Client`, rôles précis | questions parfois formulées `praticien ou dirigeant principal` | NotebookLM pour les labels visibles ; V3 pour variables. |
| Documents cession / bail / SCM | complexes, souvent brouillons à relire ou dépendants de pièces | variables listées, documents présents | garder générables techniquement, mais afficher `brouillon à relire` / `Projet`. |
| Dérogations | justification métier, pièces, manuel | `DOC-013`/`DOC-014` non fournis ou à remplir à la main | manuel / hors génération pilote. |
| Appel de fonds | peut désigner acompte back-office déclenché par fiche de création | `appel de fond sel.docx` en bloc cession | ne pas fusionner sans arbitrage métier. |
| Ordre de saisie | Fiche Client avant société | V3 est organisé par documents et variables | NotebookLM pilote l'ordre UI. |
| Mode Projet | indispensable pour banque et Ordre | absent comme variable documentaire générale | créer un ticket transversal UI/statut avant smoke. |

## Impact par fichier

### `case_catalog.py`

- Ajouter une trace de source SELARL V3 / NotebookLM dans la documentation ou les notes de catalogue.
- Ne pas changer les générateurs dans ce ticket.
- Prévoir un statut produit au-dessus de `DocumentAvailability` pour distinguer générable technique et brouillon/projet à relire.
- Vérifier l'effet de la source V3 sur `DOC-006`, `DOC-007`, `DOC-009` à `DOC-012`, `DOC-031` à `DOC-033`.

### `selarl_form_schema.py`

- Renommer les labels visibles `professionnel principal` vers `Praticien`.
- Réordonner les blocs : qualification, Fiche Client / Praticien, société, capital/associés, scénarios, documents.
- Corriger les règles de réutilisation : praticien source, mandataire Sydel par défaut, signataire séparé.
- Ajouter les champs manquants NotebookLM : type d'opération, n° sécurité sociale, téléphone pro, mode Projet, pièces Ordre.

### `business_wizard.py`

- Modifier les règles de visibilité pour que le bloc société ne précède plus la Fiche Client.
- Remplacer le défaut `mandataire_is_signataire` par un mandataire Sydel par défaut.
- Ajouter un statut documentaire produit distinct de `STATUS_GENERABLE`.
- Bloquer ou alerter si une réutilisation implicite n'a pas été confirmée.

### `streamlit_app.py`

- Réparer le parcours SELARL actuel par refonte partielle : titres d'écrans, ordre, defaults et labels.
- Ne pas modifier dans ce ticket.
- Le mode `Technique / diagnostic` et le parcours SCI doivent rester intacts.

### Tests

- Ajouter des tests anti-régression sur l'absence de `professionnel principal` dans les labels visibles SELARL.
- Mettre à jour le test qui exige `Gerant / professionnel principal`.
- Tester l'ordre logique des blocs SELARL.
- Tester que `mandataire_is_signataire` n'est pas la valeur par défaut.
- Tester que le mode `Projet` ou statut brouillon est exposé.
- Tester que `CELAR` est absent hors source NotebookLM.

## Risques si on continue sans corriger

- Les juristes verront un langage non métier et risquent de rejeter l'Assistant.
- Les rôles signataire / mandataire / gérant / associé peuvent être inversés.
- Des documents complexes seront interprétés comme finalisables alors qu'ils doivent être relus.
- Le smoke SELARL produira un résultat techniquement vert mais produit faux.
- Les adresses peuvent être réutilisées au mauvais endroit.
- La future correction coûtera plus cher si elle est faite après avoir ajouté les mappings de génération complexes.

## Conclusion

L'UI actuelle est réparable, mais elle doit être partiellement refondue avant tout smoke réaliste. La bonne séquence est : wording, ordre de formulaire, règles de réutilisation, statuts documentaires, puis seulement réparation UI et smoke.
