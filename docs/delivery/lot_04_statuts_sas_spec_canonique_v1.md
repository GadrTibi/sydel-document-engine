# DAAT x SYDEL - SPEC CANONIQUE V1
## Statuts SAS

## 1. Objet

Stabiliser la specification canonique des statuts SAS avant tout codage.

Ticket : `SPEC-STATUTS-SAS-001`.
Date : 2026-05-14.

Cette spec couvre uniquement le document source :
- `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx`

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
- `docs/delivery/lot_04_statuts_preparation_v1.md`
- `docs/delivery/lot_05_spfpl_spec_canonique_v1.md`
- `docs/delivery/lot_05_spfpl_spec_texte_v1.md`
- `docs/delivery/lot_05_spfpl_arbitrages_v1.md`

ADR applicables :
- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

Source de verite metier :
- `project/source_truth/Documents_a_generer_par_cas.docx`

Source documentaire Lot 04 :
- `project/source_documents/lot_04/STATUTS_SAS_SPFPL_medecins_modele.docx`

## 3. Perimetre documentaire

Dans la source de verite, le chemin `SAS` comprend :
- statuts : `STATUTS_SAS_SPFPL_medecins_modele.docx` ;
- documents universels deja traites separement ;
- attestation sur le capital / liste des souscripteurs : `Attestation sur le capital - apport - liste des souscripteurs.docx` ;
- PV remuneration president : `PV remuneration president - transforme.docx`.

La presente spec couvre uniquement les statuts.

Documents explicitement hors perimetre de cette spec :
- declaration de non-condamnation ;
- autorisation de domiciliation ;
- procuration ;
- attestation sur le capital / liste des souscripteurs ;
- PV remuneration president ;
- toute variante de statuts SASU holding ou SAS non SPFPL.

## 4. Constat source structurant

Le fichier est inventorie comme source du chemin `SAS`, mais son contenu visible vise une :
- `Societe de Participations Financieres de Profession Liberale de Medecins par actions simplifiee` ;
- formule de constitution unipersonnelle ;
- inscription au Tableau de l'Ordre des Medecins ;
- actionnaire unique egalement nomme president.

Decision de spec V1 :
- traiter ce document comme une source de statuts `SAS / SPFPL medecins` ;
- ne pas en deduire une SAS generique ;
- ne pas reutiliser cette source pour une autre profession ou une SAS non SPFPL sans arbitrage.

Identifiant de travail propose, sans attribution catalogue definitive :
- `STATUTS-SAS-SPFPL-MEDECINS`

## 5. Cycle documentaire

| Etape | Statut V1 | Note |
|---|---:|---|
| Inventorie | oui | source de verite, chemin `SAS` |
| Valide | partiel | valide comme source SAS, mais contenu SPFPL medecins a confirmer |
| Source recue | oui | fichier Lot 04 present |
| Analyse | oui | analyse documentaire realisee dans cette spec |
| Specifie | oui | spec canonique et spec texte V1 |
| Code | non | hors ticket |
| Teste | non | hors ticket |
| Valide | non | revue juridique humaine requise avant code |

## 6. Conditions de selection futures

Selection documentaire minimale :
- `dossier.structure == SAS`

Condition de securite V1 recommandee :
- `statuts_sas.type == spfpl_medecins` ou decision metier equivalente confirmee.

Regle de blocage future :
- bloquer si le dossier demande une SAS generique ;
- bloquer si la profession n'est pas medecin ;
- bloquer si le dossier contient plusieurs actionnaires sans arbitrage multi-actionnaires ;
- bloquer si le document doit servir de statuts SPFPL apport/cession deja traites dans une autre famille.

## 7. Roles canoniques

### 7.1 Dossier

- `dossier.structure`
- `statuts_sas.type`
- `statuts_sas.profession`

Valeurs V1 attendues :
- `dossier.structure == SAS`
- `statuts_sas.type == spfpl_medecins`
- `statuts_sas.profession == medecin`

### 7.2 Societe

Role canonique :
- `societe`

Variables :
- `societe.denomination`
- `societe.forme_juridique`
- `societe.forme_juridique_complete`
- `societe.forme_juridique_abregee`
- `societe.capital_social`
- `societe.capital_social_lettres`
- `societe.nb_actions_total`
- `societe.nb_actions_total_lettres`
- `societe.valeur_nominale_action`
- `societe.valeur_nominale_action_lettres`
- `societe.siege.adresse_affichee`
- `societe.ville_rcs` si requis ulterieurement

Note :
- `societe.forme_juridique_complete` est fixe dans la source sur une SPFPL de medecins par actions simplifiee.

### 7.3 Actionnaire unique / associe unique

Role canonique V1 :
- `actionnaire_unique`

Role de compatibilite moteur :
- `associes[0]`

Variables :
- `actionnaire_unique.civilite_affichage`
- `actionnaire_unique.prenom`
- `actionnaire_unique.nom`
- `actionnaire_unique.qualification_principale`
- `actionnaire_unique.date_naissance`
- `actionnaire_unique.ville_naissance`
- `actionnaire_unique.departement_naissance`
- `actionnaire_unique.adresse_personnelle_affichee`
- `actionnaire_unique.situation_maritale`
- `actionnaire_unique.regime_matrimonial`
- `actionnaire_unique.conjoint.civilite_affichage`
- `actionnaire_unique.conjoint.prenom`
- `actionnaire_unique.conjoint.nom`
- `actionnaire_unique.nationalite`
- `actionnaire_unique.ordre.departemental`
- `actionnaire_unique.ordre.numero`
- `actionnaire_unique.ordre.numero_rpps`
- `actionnaire_unique.nb_actions`

Decision V1 :
- le document source est unipersonnel ;
- `actionnaire_unique` et `associes[0]` representent la meme personne ;
- aucune liste dynamique d'actionnaires n'est stabilisee par cette source.

### 7.4 President

Role canonique :
- `president`

Variables :
- `president.ref_associe_index`
- `president.civilite_affichage`
- `president.prenom`
- `president.nom`
- `president.adresse_personnelle_affichee`
- `president.duree_mandat`

Decision V1 :
- le president est la meme personne que l'actionnaire unique ;
- `president.ref_associe_index == 0` est la valeur cible ;
- aucune variante dirigeant non actionnaire n'est sourcee.

### 7.5 Banque / depot des fonds

Role canonique :
- `depot_fonds`

Variables :
- `depot_fonds.banque.nom`
- `depot_fonds.montant`

Regle :
- `depot_fonds.montant` doit etre coherent avec `societe.capital_social`.

### 7.6 Exercice social

Role canonique :
- `exercice_social`

Variables :
- `exercice_social.debut`
- `exercice_social.fin`
- `exercice_social.date_cloture_premier_exercice`

### 7.7 Signature

Role canonique :
- `signature`

Variables :
- `signature.lieu`
- `signature.date`
- `signature.mention_president`

Note :
- la source contient l'instruction `Faire preceder de la mention "Bon pour acceptation des fonctions de President"`.
- cette instruction doit rester visible comme element manuel ou bloc de signature valide, sans etre transformee implicitement.

## 8. Mapping placeholders source vers variables canoniques

| Placeholder source | Variable canonique cible | Note |
|---|---|---|
| `[denomination_societe]` | `societe.denomination` | aussi footer |
| `[capital_social]` | `societe.capital_social` | aussi apport et depot |
| `[capital_lettres]` | `societe.capital_social_lettres` | article 7 |
| `[adresse_siege]` | `societe.siege.adresse_affichee` | adresse affichee complete |
| `[civilite]` | `actionnaire_unique.civilite_affichage` et `president.civilite_affichage` | meme personne en V1 |
| `[prenom]` | `actionnaire_unique.prenom` et `president.prenom` | meme personne en V1 |
| `[nom]` | `actionnaire_unique.nom` et `president.nom` | meme personne en V1 |
| `[qualification_principale]` | `actionnaire_unique.qualification_principale` | profession/qualification source |
| `[date_naissance]` | `actionnaire_unique.date_naissance` | identite |
| `[ville_naissance]` | `actionnaire_unique.ville_naissance` | identite |
| `[departement_naissance]` | `actionnaire_unique.departement_naissance` | identite |
| `[adresse_personnelle]` | `actionnaire_unique.adresse_personnelle_affichee` | adresse complete |
| `[situation_maritale]` | `actionnaire_unique.situation_maritale` | wording source a arbitrer selon situation |
| `[regime_matrimonial]` | `actionnaire_unique.regime_matrimonial` | obligatoire si la phrase source est conservee |
| `[civilite_conjoint]` | `actionnaire_unique.conjoint.civilite_affichage` | conditionnel ou manuel |
| `[prenom_conjoint]` | `actionnaire_unique.conjoint.prenom` | conditionnel ou manuel |
| `[nom_conjoint]` | `actionnaire_unique.conjoint.nom` | conditionnel ou manuel |
| `[nationalite]` | `actionnaire_unique.nationalite` | identite |
| `[ordre_departemental]` | `actionnaire_unique.ordre.departemental` | Ordre des medecins |
| `[numero_ordre]` | `actionnaire_unique.ordre.numero` | numero national source |
| `[numero_rpps]` | `actionnaire_unique.ordre.numero_rpps` | RPPS |
| `[nom_banque]` | `depot_fonds.banque.nom` | depot des fonds |
| `[nb_actions]` | `societe.nb_actions_total` et `actionnaire_unique.nb_actions` | coherent en V1 actionnaire unique |
| `[nb_actions_lettres]` | `societe.nb_actions_total_lettres` | article 7 |
| `[valeur_nominale_action]` | `societe.valeur_nominale_action` | article 7 |
| `[valeur_nominale_action_lettres]` | `societe.valeur_nominale_action_lettres` | article 7 |
| `[debut_exercice]` | `exercice_social.debut` | article 17 |
| `[fin_exercice]` | `exercice_social.fin` | article 17 |
| `[date_cloture_exercice_1]` | `exercice_social.date_cloture_premier_exercice` | article 17 |
| `[lieu_signature]` | `signature.lieu` | signature finale |

## 9. Structure canonique du document

Blocs fixes principaux :
- cartouche societe ;
- titre `STATUTS` ;
- comparution du soussigne ;
- articles 1 a 27 ;
- signature du president ;
- annexe des engagements pris avant constitution.

Articles sources :
1. Forme
2. Objet
3. Denomination
4. Siege social
5. Duree
6. Apports
7. Capital social
8. Qualite des associes
9. Augmentation et reduction du capital
10. Cession et transmission des actions
11. Comptes courants
12. President
13. Directeurs generaux
14. Conventions entre la societe et ses dirigeants
15. Decisions d'actionnaires
16. Commissaires aux comptes
17. Exercice social - comptes sociaux
18. Affectation et repartition des benefices
19. Capitaux propres inferieurs a la moitie du capital social
20. Exclusion
21. Dissolution - liquidation
22. Transformation de la societe
23. Contestations
24. Condition suspensive
25. Ordre professionnel
26. Frais
27. Jouissance de la personnalite morale - pouvoirs

## 10. Blocs associes / souscripteurs

### 10.1 Source V1

La source V1 est redigee pour un actionnaire unique :
- bloc `Le soussigne` au singulier ;
- `Associe Unique` / `Actionnaire Unique` ;
- apport en numeraire par un seul docteur ;
- attribution de toutes les actions au meme docteur ;
- nomination du meme docteur comme president ;
- signature finale unique.

### 10.2 Multi-actionnaires

La source contient aussi des formules generales sur le fonctionnement avec plusieurs associes, mais elle ne fournit pas de bloc source complet pour :
- plusieurs soussignes ;
- une table dynamique d'apports ;
- une repartition dynamique des actions ;
- des signatures multiples.

Decision V1 :
- la generation automatique future doit rester limitee a un actionnaire unique ;
- les dossiers multi-actionnaires restent bloques ou manuels tant qu'une spec dediee n'est pas fournie.

### 10.3 Lien avec `associes[]`

Pour garder l'alignement avec le dictionnaire canonique :
- `associes[0]` peut representer l'actionnaire unique ;
- `president.ref_associe_index == 0` rattache le president a cette personne ;
- ne pas introduire de placeholders locaux type `personne_1`.

## 11. Elements manuels

Elements a fournir explicitement par contexte dossier ou saisie controlee :
- nom de la banque ;
- situation matrimoniale ;
- regime matrimonial ;
- informations du conjoint si la phrase source reste applicable ;
- departement ordinal ;
- numero ordinal ;
- numero RPPS ;
- debut et fin d'exercice social ;
- date de cloture du premier exercice ;
- lieu de signature ;
- date de signature si le futur rendu ajoute la date absente du placeholder source ;
- mention manuscrite ou instruction de signature `Bon pour acceptation des fonctions de President` ;
- actes accomplis avant constitution si l'annexe doit depasser l'ouverture du compte bancaire.

Regle :
- ces elements ne doivent pas etre inventes par le moteur.

## 12. Lien avec attestation capital / liste des souscripteurs

La source de verite associe au chemin `SAS` le document :
- `Attestation sur le capital - apport - liste des souscripteurs.docx`

Ce document est distinct des statuts et ne doit pas etre fusionne avec eux.

Liens de coherence obligatoires entre statuts et attestation :
- `societe.denomination` ;
- `societe.capital_social` ;
- `societe.nb_actions_total` ;
- `societe.valeur_nominale_action` ;
- `actionnaire_unique.prenom` ;
- `actionnaire_unique.nom` ;
- `actionnaire_unique.adresse_personnelle_affichee` ;
- `actionnaire_unique.nb_actions` ;
- `signature.lieu` ;
- `signature.date`.

Point de vigilance :
- la spec SPFPL existante limite l'attestation capital / liste des souscripteurs V1 a un actionnaire unique ;
- cette limite est compatible avec la source de statuts SAS analysee ;
- toute liste dynamique de souscripteurs reste hors automatisation V1 sans arbitrage.

## 13. Regles de blocage avant generation

Un futur generateur de statuts SAS doit bloquer si :
- la structure n'est pas `SAS` ;
- le type `spfpl_medecins` n'est pas confirme ;
- la profession n'est pas medecin ;
- plusieurs actionnaires sont fournis ;
- `actionnaire_unique` et `president` ne designent pas la meme personne en V1 ;
- la phrase matrimoniale ne peut pas etre rendue sans incoherence ;
- les donnees ordinales obligatoires sont absentes ;
- le capital social, le nombre d'actions ou la valeur nominale sont incoherents ;
- le capital statutaire diverge des donnees attendues pour l'attestation capital / liste des souscripteurs ;
- le rendu final conserverait un placeholder source `[` ou `]` ;
- une correction de wording juridique serait necessaire sans validation explicite.

## 14. Criteres avant implementation

Un ticket de code pourra demarrer seulement si :
- le perimetre est confirme comme `SAS / SPFPL medecins` et non SAS generique ;
- la V1 actionnaire unique est acceptee ;
- le comportement en cas de celibat, mariage, PACS ou absence de conjoint est arbitre ;
- le lien avec l'attestation capital / liste des souscripteurs est confirme ;
- le PV remuneration president est maintenu dans un document separe ;
- aucun DOCX source n'est utilise comme template d'execution ;
- les tests futurs verifient les variables obligatoires, l'absence de placeholders residuels et la coherence capital/actions.

## 15. Points ouverts

1. **Nature exacte du document** : le chemin source est `SAS`, mais le texte vise une SPFPL de medecins par actions simplifiee. Une validation metier doit confirmer que ce document est bien le statut SAS attendu.
2. **SAS generique** : aucune variante SAS generique n'est couverte par cette source.
3. **Actionnaire unique uniquement** : la source V1 ne stabilise pas les blocs multi-actionnaires, malgre des clauses generales pluripersonnelles.
4. **Situation matrimoniale** : la phrase source suppose un regime matrimonial et un conjoint ; les variantes celibataire, divorce, PACS ou sans conjoint ne sont pas sourcees.
5. **Incoherences de vocabulaire** : certains passages utilisent des termes proches des SARL/SEL, notamment `parts sociales`, `gerant` ou `gerance`, dans un document par actions simplifiee. Aucun de ces termes ne doit etre corrige sans validation juridique.
6. **Condition suspensive Ordre** : la condition d'inscription au Tableau de l'Ordre des Medecins doit etre confirmee comme applicable a tous les dossiers SAS cibles.
7. **Attestation capital / liste des souscripteurs** : l'automatisation V1 peut rester coherente en actionnaire unique, mais la variante multi-souscripteurs reste hors perimetre.
8. **PV remuneration president** : document inventorie separement dans le chemin SAS, non analyse dans cette spec.

## 16. Statut

`SPEC-STATUTS-SAS-001` est stabilise cote canonique pour les statuts SAS source Lot 04, sans code Python.

Prochaine etape recommandee :
- revue metier des points ouverts 1, 4, 5 et 7 avant tout ticket de code.
