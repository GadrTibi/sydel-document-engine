# DAAT x SYDEL - RESOLUTION V1
## Bloc cession de parts SCM vers SEL

## 1. Objet

Ticket : `ARBITRAGE-SCM-CESSION-RESOLVE-001`.

Ce document tranche le perimetre V1 du bloc de cession de parts de SCM vers une SEL d'exercice, apres le blocage constate sur `CODE-SCM-CESSION-BLOCK-001`.

Il ne modifie aucun wording juridique source, ne modifie aucun code Python et ne modifie aucun fichier de pilotage partage.

## 2. Sources et specs prises en compte

Sources projet lues :
- `AGENTS.md`
- `docs/project/00_MASTER_PLAN.md`
- `docs/project/01_EXECUTION_BOARD.md` en lecture seule
- `docs/project/02_CODEX_WORKFLOW.md`
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md`
- `docs/project/04_LAST_STATE.md` en lecture seule
- `project/source_truth/Documents_a_generer_par_cas.docx`

Specs et preparation lues :
- `docs/delivery/lot_05_scm_cession_sources_preparation_v1.md`
- `docs/delivery/lot_05_scm_cession_block_spec_canonique_v1.md`
- `docs/delivery/lot_05_scm_cession_block_spec_texte_v1.md`

Sources documentaires lues dans `project/source_documents/lot_05/` :
- `PV AGE cession part SCM.docx`
- `Courrier SDE.docx`
- `Acte de cession des parts de la SCM à la SELARL - transforme.docx`
- `PV AGE cession part SCM - SELAS.docx`
- `Courrier SDE - SELAS.docx`
- `Acte_cession_parts_SCM_SEL_modele.docx`

ADR reperes :
- ADR-0001 : source de verite documentaire
- ADR-0002 : moteur par document canonique
- ADR-0003 : livraison par lots documentaires
- ADR-0004 : generation DOCX propre from-scratch
- ADR-0005 : mode Codex repo-first

## 3. Decision de perimetre V1

La V1 couvre bien les 6 documents nommes par la source de verite et par le ticket.

Il n'y a pas de decoupage fonctionnel en sous-batchs pour la V1. Le futur ticket code doit traiter le bloc comme un mini-batch unique de 3 documents canoniques, chacun decline en overlay SELARL ou SELAS :

| Document canonique V1 | Source SELARL | Source SELAS |
|---|---|---|
| PV AGE cession part SCM | `PV AGE cession part SCM.docx` | `PV AGE cession part SCM - SELAS.docx` |
| Courrier SDE cession SCM | `Courrier SDE.docx` | `Courrier SDE - SELAS.docx` |
| Acte de cession parts SCM vers SEL | `Acte de cession des parts de la SCM à la SELARL - transforme.docx` | `Acte_cession_parts_SCM_SEL_modele.docx` |

La mention historique "BLOCK" dans `CODE-SCM-CESSION-BLOCK-001` ne doit plus etre interpretee comme une consigne de coder uniquement un blocage. Elle designe le bloc documentaire SCM cession. Le code V1 doit produire les 6 sorties prevues lorsque les validations passent, et bloquer seulement les cas non couverts ou insuffisamment renseignes.

## 4. Conclusion executable

Decision : **go code 6 docs**.

Le prochain ticket de code peut implementer :
- les 3 generateurs documentaires canoniques ;
- les overlays SELARL / SELAS de chaque generateur ;
- la selection conditionnelle sur `dossier.structure in {"SELARL", "SELAS"}` et `dossier.options.scm_cession == true` ;
- les validations bloquantes listees dans ce document.

## 5. Parties restant manuelles en V1

Restent manuelles ou fournies explicitement par le contexte dossier :
- activation du bloc cession SCM ;
- choix de structure SELARL ou SELAS ;
- roles exacts des personnes source `personne_1`, `personne_2`, `personne_3`, `personne_4` ;
- president de seance du PV ;
- associes presents ou representes ;
- repartition du capital avant cession ;
- repartition du capital apres cession ;
- nombre total de parts, plages de parts et controles de coherence ;
- identite complete du cedant, du conjoint et de la SEL cessionnaire ;
- confirmation que le cedant represente ou non la SEL cessionnaire ;
- donnees ordinales et RPPS du cedant ;
- nombre, plage, prix unitaire et prix global des parts cedees ;
- mode de paiement ;
- activation ou exclusion du credit-vendeur ;
- donnees completes du credit-vendeur si actif ;
- montant des droits d'enregistrement ;
- service d'enregistrement et nombre d'exemplaires pour l'overlay SELAS ;
- lieu et date de signature des courriers SDE ;
- lieu de signature de l'acte de cession ;
- date de l'acte de cession, qui reste une zone manuelle car la source contient seulement la ligne `Le` ;
- prestataire de signature electronique quand il n'est pas fixe par l'overlay ;
- toute correction de wording source.

Le moteur ne doit pas inventer ces valeurs.

## 6. Overlays SELARL supportes

### 6.1 PV AGE SELARL

Support V1 :
- source `PV AGE cession part SCM.docx` ;
- date de PV mappee depuis l'alias source `[date_du_jour]` ;
- agrement du nouvel associe "a compter de ce jour" ;
- pas de delai d'agrement ni de date limite.

Validation :
- les roles `personne_1` a `personne_4` doivent etre fournis explicitement ;
- la repartition des parts apres cession doit totaliser `scm_cedee.nb_parts_total`.

### 6.2 Courrier SDE SELARL

Support V1 :
- source `Courrier SDE.docx` ;
- pas de bloc destinataire fiscal ;
- nombre d'exemplaires conserve a `4 exemplaires`, comme dans la source ;
- montant des droits et signataire fournis par contexte.

Validation :
- ne pas generaliser le destinataire fiscal SELAS vers SELARL en V1 ;
- ne pas rendre `[nombre_exemplaires]` dans cette variante.

### 6.3 Acte SELARL

Support V1 :
- source `Acte de cession des parts de la SCM à la SELARL - transforme.docx` ;
- forme SELARL fixe ;
- representant affiche comme gerant ;
- profession ordinale source fixe sur les chirurgiens-dentistes ;
- prestataire de signature electronique fixe `Yousign` ;
- majoration d'interet de retard fixe a `3 points` ;
- adresse de siege de la SCM cedee conservee selon la source, meme si l'alias source pointe vers `[adresse_siege_cessionnaire]`.

Validation :
- si le cedant n'est pas le representant de la SEL cessionnaire, le generateur doit bloquer en V1 ;
- la source non transformee `Acte de cession des parts de la SCM à la SELARL.docx` reste hors V1.

## 7. Overlays SELAS supportes

### 7.1 PV AGE SELAS

Support V1 :
- source `PV AGE cession part SCM - SELAS.docx` ;
- date de PV mappee depuis l'alias source `[date_pv]` ;
- delai d'agrement et date limite rendus uniquement pour SELAS.

Validation :
- `scm_cession.agrement.delai_mois` et `scm_cession.agrement.date_limite` sont obligatoires ;
- la repartition des parts apres cession doit totaliser `scm_cedee.nb_parts_total`.

### 7.2 Courrier SDE SELAS

Support V1 :
- source `Courrier SDE - SELAS.docx` ;
- bloc destinataire fiscal rendu ;
- nombre d'exemplaires variable via contexte ;
- montant des droits et signataire fournis par contexte.

Validation :
- les champs service, centre des finances publiques, adresse et CP/ville du service sont obligatoires ;
- `enregistrement.nombre_exemplaires` est obligatoire.

### 7.3 Acte SELAS

Support V1 :
- source `Acte_cession_parts_SCM_SEL_modele.docx` ;
- profession ordinale, forme sociale, fonction du representant, forme de la SCM cedee, adresse de la SCM cedee, prestataire de signature et majoration d'interet variables ;
- wording SELAS conserve tel que source.

Validation :
- aucune correction automatique des formulations source SELAS ;
- les valeurs variables doivent etre fournies explicitement.

## 8. Ambiguites tolerees en V1

Les ambiguites suivantes sont tolerees uniquement parce qu'elles sont encadrees par des validations ou par une conservation stricte de la source :

1. Les aliases `personne_1` a `personne_4` sont toleres comme aliases documentaires, mais jamais comme roles metier implicites.
2. La source SELARL transformee est la seule source acte SELARL retenue ; la source non transformee mentionnee par la source de verite reste ignoree en V1.
3. Les divergences SELARL / SELAS du courrier SDE sont conservees par overlay, sans harmonisation.
4. Les anomalies apparentes de wording SELAS sont conservees telles quelles.
5. L'anomalie d'adresse de siege de la SCM cedee dans l'acte SELARL est conservee telle quelle.
6. La phrase de representation de la SEL cessionnaire dans les actes est supportee uniquement si le contexte confirme le representant attendu ; sinon blocage.
7. La ligne source `Ajouter en cas de CV` est traitee comme instruction documentaire, pas comme texte final.
8. La date de l'acte peut rester une zone manuelle en V1, car la source contient seulement `Le` sans placeholder.

## 9. Ambiguites non tolerees

Le futur code doit bloquer si :
- le dossier n'est ni SELARL ni SELAS ;
- `dossier.options.scm_cession` n'est pas actif ;
- une des 6 sources n'est pas referencee dans le perimetre de test ou de smoke ;
- les roles des associes ne sont pas explicites ;
- les parts avant ou apres cession ne totalisent pas le total de parts attendu ;
- le credit-vendeur est actif avec donnees incompletes ;
- le credit-vendeur est inactif mais le texte final contient encore `Ajouter en cas de CV` ;
- le representant de la SEL cessionnaire est ambigu ;
- le rendu conserve un placeholder source entre crochets ;
- une correction de wording juridique est appliquee sans validation explicite.

## 10. Tests attendus pour le ticket code

Tests minimaux attendus :
- selection du bloc uniquement pour SELARL / SELAS avec option cession SCM active ;
- generation des 3 documents SELARL ;
- generation des 3 documents SELAS ;
- absence de placeholder `[` ou `]` dans les sorties ;
- blocage si repartition de parts incoherente ;
- blocage si roles `personne_1` a `personne_4` non mappes ;
- blocage si credit-vendeur actif incomplet ;
- verification que `Ajouter en cas de CV` ne sort jamais dans un document final ;
- verification des overlays courrier SDE : SELARL sans destinataire et avec 4 exemplaires, SELAS avec destinataire et nombre variable ;
- verification des overlays PV : SELARL sans delai/date limite, SELAS avec delai/date limite ;
- verification des overlays acte : SELARL avec constantes source, SELAS avec variables source.

## 11. Statut

`ARBITRAGE-SCM-CESSION-RESOLVE-001` leve le blocage de perimetre V1.

Conclusion executable : **go code 6 docs**.

Le prochain ticket recommande est un ticket de code limite au bloc cession SCM V1, sans modification de wording juridique et avec validations bloquantes.
