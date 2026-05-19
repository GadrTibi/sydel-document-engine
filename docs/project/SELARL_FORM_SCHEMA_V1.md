# Schéma de formulaire SELARL V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Ce document transforme les variables SELARL en blocs de saisie compréhensibles pour un juriste. Il ne modifie pas l'UI actuelle : il définit la cible de saisie du pilote.

Source : `project/source_truth/Documents_a_generer_par_cas_V2.docx` et référentiels existants `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`, `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`, specs delivery des familles SELARL.

## Principes

- Le formulaire part du processus SELARL, pas des générateurs.
- Chaque champ doit avoir un libellé qualifié.
- Une donnée saisie une fois doit alimenter tous les documents qui en dépendent.
- Les documents manuels restent visibles, mais ne déclenchent pas de génération.
- Les champs conditionnels ne sont obligatoires que si leur bloc est actif.

## Blocs et champs

| Champ UI cible | Variable(s) moteur alimentée(s) | Bloc UI | Obligatoire | Condition d'affichage | Aide contextuelle | Exemple |
|---|---|---|---|---|---|---|
| Profession exercée | `conditions.profession`, `statuts_sel.profession`, `ordre.profession` | Qualification du dossier | oui | Toujours | Choisir le métier qui pilote les statuts et les mentions ordinales. | Chirurgien-dentiste |
| Site distinct à déclarer | `conditions.site_distinct`, `dossier_options.site_distinct` | Qualification du dossier | oui | Toujours | Affiche une pièce manuelle si un site distinct est concerné. | Non |
| Cession de parts de SCM vers la SELARL | `conditions.scm_cession`, `dossier_options.scm_cession` | Qualification du dossier | oui | Toujours | Active les documents SCM cession, distincts de la cession de cabinet. | Oui |
| Régime matrimonial communautaire | `conditions.regime_communautaire`, `dossier_options.regime_communautaire` | Qualification du dossier | oui | Toujours | Active les lettres conjoint et renonciation. | Oui |
| Dérogation ordinale | `conditions.derogation`, `dossier_options.derogation` | Qualification du dossier | oui | Toujours | Active les documents de dérogation ; certaines zones restent manuelles. | Non |
| Cession de cabinet | `conditions.cession`, `dossier_options.cession` | Qualification du dossier | oui | Toujours | Active les blocs cession, bail et financement. | Oui |
| Type de cabinet cédé | `conditions.cabinet_type`, `cession.cabinet.type` | Qualification du dossier | conditionnel | Si cession de cabinet = oui | Choisir `aucun` si la cession ne porte pas sur un cabinet médical ou dentaire. | Cabinet dentaire |
| Dénomination de la SELARL | `societe.denomination` | Société | oui | Toujours | Nom de la société en création ou acquéreur dans le dossier. | SELARL DU CENTRE |
| Forme sociale | `societe.forme_sociale`, `societe.forme_sociale_affichage`, `societe.forme_sociale_libelle_long` | Société | oui | Toujours | Valeur pilote : SELARL. Le libellé long alimente certains documents. | SELARL |
| Capital social | `societe.capital`, `societe.capital_social` | Société | oui | Documents communs, PV, statuts, cession | Montant du capital de la SELARL. | 5 000 euros |
| Nombre total de parts | `capital.nb_parts_total`, `statuts_sel.capital.nb_parts_total` | Société | conditionnel | Si PV/statuts actifs | Doit correspondre à la somme des parts des associés. | 500 |
| Valeur nominale d'une part | `capital.valeur_nominale_part`, `statuts_sel.capital.valeur_nominale_part` | Société | conditionnel | Si PV/statuts actifs | Utilisé pour la répartition du capital. | 10 euros |
| Ville du RCS | `societe.ville_rcs` | Société | oui | Statuts, PV, cession SCM | Greffe d'immatriculation de la SELARL. | Paris |
| Adresse du siège social - numéro | `societe.siege.num_voie` | Siège social | oui | Toujours | Adresse juridique du siège, distincte de l'adresse personnelle et du cabinet cédé. | 12 |
| Adresse du siège social - voie | `societe.siege.voie` | Siège social | oui | Toujours | Ne pas utiliser pour le cabinet cédé sauf si cela est explicitement le même lieu. | rue de la Paix |
| Adresse du siège social - code postal | `societe.siege.cp` | Siège social | oui | Toujours | Code postal du siège. | 75002 |
| Adresse du siège social - ville | `societe.siege.ville` | Siège social | oui | Toujours | Ville du siège. | Paris |
| Adresse de domiciliation affichée | `domiciliation.adresse_affichee`, alias runtime `domiciliation.adresse_domiciliation_affichee` | Siège social | oui | Si `DOC-002` actif | Champ libre décidé V1 ; ne pas déduire automatiquement sans confirmation. | 12 rue de la Paix, 75002 Paris |
| Civilité du professionnel principal | `signataire.civilite_affichage`, `dirigeant_nomine.civilite_affichage` si réutilisé | Professionnel / gérant | oui | Toujours | Civilité affichée, distincte du genre grammatical. | Docteur |
| Genre grammatical du professionnel principal | `signataire.genre`, `dirigeant_nomine.genre` si réutilisé | Professionnel / gérant | oui | Toujours | Pilote les accords comme soussigné/soussignée. | masculin |
| Prénom du professionnel principal | `signataire.prenom`, `dirigeant_nomine.prenom` si réutilisé | Professionnel / gérant | oui | Toujours | Personne principale du dossier. | Camille |
| Nom du professionnel principal | `signataire.nom`, `dirigeant_nomine.nom` si réutilisé | Professionnel / gérant | oui | Toujours | Nom de naissance ou nom usuel selon source validée. | Martin |
| Date de naissance du professionnel principal | `signataire.date_naissance`, `dirigeant_nomine.date_naissance` si réutilisé | Professionnel / gérant | oui | Documents communs, PV | Date au format JJ/MM/AAAA côté UI, export ISO possible côté moteur. | 03/04/1985 |
| Ville de naissance du professionnel principal | `dirigeant_nomine.ville_naissance` | Professionnel / gérant | conditionnel | PV/statuts actifs | Requise pour le PV nomination gérant. | Lyon |
| Département de naissance du professionnel principal | `dirigeant_nomine.departement_naissance` | Professionnel / gérant | conditionnel | PV/statuts actifs | Requis pour le PV nomination gérant. | Rhône |
| Nationalité du professionnel principal | `signataire.nationalite`, `dirigeant_nomine.nationalite` si réutilisé | Professionnel / gérant | oui | Documents communs, PV | Ne pas déduire depuis le lieu de naissance. | française |
| Adresse personnelle du professionnel - numéro | `signataire.adresse_personnelle.num_voie`, `dirigeant_nomine.adresse_personnelle.num_voie` si réutilisé | Professionnel / gérant | oui | Documents communs, PV | Adresse personnelle, pas siège ni cabinet. | 8 |
| Adresse personnelle du professionnel - voie | `signataire.adresse_personnelle.voie`, `dirigeant_nomine.adresse_personnelle.voie` si réutilisé | Professionnel / gérant | oui | Documents communs, PV | Adresse personnelle complète. | avenue Victor Hugo |
| Adresse personnelle du professionnel - code postal | `signataire.adresse_personnelle.cp`, `dirigeant_nomine.adresse_personnelle.cp` si réutilisé | Professionnel / gérant | oui | Documents communs, PV | Code postal personnel. | 69002 |
| Adresse personnelle du professionnel - ville | `signataire.adresse_personnelle.ville`, `dirigeant_nomine.adresse_personnelle.ville` si réutilisé | Professionnel / gérant | oui | Documents communs, PV | Ville personnelle. | Lyon |
| Fonction du professionnel principal | `signataire.fonction_dirigeant`, `dirigeant_nomine.fonction_affichage` | Professionnel / gérant | oui | Toujours | Pour SELARL pilote : utiliser `Gérant / professionnel principal`. | Gérant |
| Numéro RPPS | `ordre.numero_rpps` | Ordre professionnel | conditionnel | Demande d'inscription / dérogation | Numéro professionnel si disponible. | 10101234567 |
| Numéro ordinal | `ordre.numero_ordre` | Ordre professionnel | conditionnel | Demande d'inscription / dérogation | Numéro d'inscription à l'ordre. | 75-12345 |
| Conseil de l'ordre compétent | `ordre.conseil`, `ordre.ville_ordre` | Ordre professionnel | oui | Si `DOC-034`, `DOC-013` ou `DOC-014` actif | Conseil départemental ou autorité compétente. | Conseil départemental de Paris |
| Signataire est le premier associé | `ui.reuse.signataire_associe_1`, mapping vers `associes[0]` | Associés | optionnel | Si au moins un associé | Evite de ressaisir l'identité du professionnel. | Oui |
| Nombre d'associés | `associes[]` cardinalité | Associés | oui | PV/statuts actifs | V1 doit couvrir le cas simple et bloquer les cardinalités non arbitrées. | 1 |
| Associé 1 - identité | `associes[0].civilite_affichage`, `associes[0].prenom`, `associes[0].nom`, `associes[0].genre` | Associés | oui | PV/statuts actifs | Peut être copié depuis le professionnel principal. | Dr Camille Martin |
| Associé 1 - parts | `associes[0].nb_parts` | Associés | oui | PV/statuts actifs | Doit s'additionner au total de parts. | 500 |
| Associé 2 - identité | `associes[1].*` | Associés | conditionnel | Si nombre d'associés >= 2 | Cas simple V1 seulement si la spec du document l'autorise. | Dr Alex Bernard |
| Gérant choisi parmi les associés | `dirigeant_nomine.ref_associe_index` | Associés | optionnel | Si PV/statuts actifs | Masque les champs d'identité du gérant s'ils sont déjà portés par l'associé. | Associé 1 |
| Mandataire est le signataire | `mandataire.*` depuis `signataire.*` | Mandataire / signataire | optionnel | Si demande d'inscription à l'ordre active | Evite une double saisie du mandataire. | Oui |
| Identité du mandataire | `mandataire.civilite`, `mandataire.prenom`, `mandataire.nom`, `mandataire.fonction` | Mandataire / signataire | conditionnel | Si mandataire distinct | Personne ou cabinet qui signe ou dépose la demande. | Me Dupont |
| Identité du conjoint | `conjoint.civilite`, `conjoint.prenom`, `conjoint.nom`, `conjoint.genre` | Régime matrimonial / conjoint | conditionnel | Si régime communautaire = oui | Alimente les lettres conjoint. | Mme Sophie Martin |
| Régime matrimonial | `apport.regime_matrimonial`, `regime_communautaire.*` | Régime matrimonial / conjoint | conditionnel | Si régime communautaire = oui | Ne pas déduire sans preuve dossier. | communauté légale |
| Apport concerné par le régime communautaire | `apport`, `regime_communautaire.renonciation`, `regime_communautaire.avertissement` | Régime matrimonial / conjoint | conditionnel | Si régime communautaire = oui | Décrire la somme ou le bien commun concerné selon la spec. | apport en numéraire |
| Cabinet cédé - adresse | `cession.cabinet.adresse.*`, `cession.cabinet.adresse_affichee` | Cession de cabinet | conditionnel | Si cession = oui | Adresse du cabinet vendu, distincte du siège social. | 4 rue du Cabinet, 75015 Paris |
| Vendeur du cabinet | `cession.vendeur.*` | Cession de cabinet | conditionnel | Si cession = oui | Personne ou société cédante. | Dr Jean Durand |
| Acquéreur du cabinet | `cession.acquereur.*`, souvent `societe` | Cession de cabinet | conditionnel | Si cession = oui | Peut être la SELARL en création. | SELARL DU CENTRE |
| Prix de cession | `cession.prix.*` | Cession de cabinet | conditionnel | Si cession = oui | Montant et modalités selon acte ou compromis. | 120 000 euros |
| Banque financeuse | `cession.financement.banque.*` | Banque / financement | conditionnel | Si financement bancaire actif | Banque concernée par l'appel de fonds ou la condition suspensive. | Banque X |
| Adresse de la banque | `cession.financement.banque.adresse.*` | Banque / financement | conditionnel | Si banque active | Adresse de la banque, pas adresse du siège. | 1 boulevard Haussmann, 75009 Paris |
| Montant maximum de l'emprunt PV | `emprunt.montant_max` | Banque / financement | conditionnel | Si `emprunt.actif = true` dans le PV | Branche du `DOC-004`, pas document autonome. | 250 000 euros |
| Adresse du bien financé par l'emprunt | `bien_immobilier.adresse.*` | Banque / financement | conditionnel | Si `emprunt.actif = true` | Adresse du bien immobilier visé par le PV. | 10 rue du Bien, 75010 Paris |
| Bailleur | `bail.bailleur.*` | Bail | conditionnel | Si cession = oui et avenant bail actif | Identité du bailleur du local. | SCI DES LOCAUX |
| Adresse du bailleur | `bail.bailleur.adresse.*` | Bail | conditionnel | Si bailleur actif | Adresse du bailleur. | 2 rue du Bailleur, 75008 Paris |
| Locaux loués | `bail.locaux.adresse.*`, `cession.cabinet.adresse.*` si identique | Bail | conditionnel | Si avenant bail actif | Adresse des locaux du bail. | 4 rue du Cabinet |
| SCM cédée | `scm_cession.scm_cedee.*` | SCM | conditionnel | Si SCM cession = oui | Société civile de moyens dont les parts sont cédées. | SCM DES DOCTEURS |
| Cédant des parts SCM | `scm_cession.cedant.*` | SCM | conditionnel | Si SCM cession = oui | Personne ou société cédante. | Dr Jean Durand |
| Cessionnaire des parts SCM | `scm_cession.cessionnaire.*`, souvent `societe` | SCM | conditionnel | Si SCM cession = oui | Peut être la SELARL en création. | SELARL DU CENTRE |
| Prix de cession des parts SCM | `scm_cession.prix.*` | SCM | conditionnel | Si SCM cession = oui | Prix des parts SCM, distinct du prix de cabinet. | 1 000 euros |
| Lieu de signature | `signature.lieu` | Signature | oui | Si un document signé est généré | Lieu affiché dans les documents. | Paris |
| Date de signature | `signature.date` | Signature | oui | Si un document signé est généré | Date de signature du dossier. | 19/05/2026 |
| Nombre d'exemplaires | `signature.nombre_exemplaires`, `document.nombre_exemplaires` | Signature | conditionnel | PV, documents qui l'exigent | Ne pas demander si aucun document actif ne l'utilise. | 3 |

## Règles de réutilisation des données

- Le signataire peut être le premier associé : proposer `Le signataire est le premier associé`.
- Le gérant peut être le professionnel principal : proposer `Le gérant est le professionnel principal`.
- Le gérant peut être choisi parmi les associés : afficher un sélecteur `Choisir parmi les associés`.
- L'adresse du siège social peut alimenter l'autorisation de domiciliation seulement si l'utilisateur coche `L'adresse de domiciliation est le siège social`.
- L'adresse personnelle du professionnel alimente `signataire.adresse_personnelle.*` et peut alimenter `dirigeant_nomine.adresse_personnelle.*` si le gérant est ce professionnel.
- La société acquéreur peut être la SELARL en création dans les cas de cession : proposer `La SELARL en création est l'acquéreur`.
- La société cessionnaire peut être la SELARL en création dans les cas de SCM cession : proposer `La SELARL en création est la cessionnaire des parts SCM`.
- Le mandataire peut être le signataire ou une personne distincte : proposer un choix explicite.
- Les champs dérivés doivent devenir en lecture seule lorsque la source est cochée, avec un lien de retour vers la donnée source.

Mécanismes UI recommandés :

- case à cocher : `Le signataire est le premier associé` ;
- case à cocher : `Le gérant est le professionnel principal` ;
- bouton : `Copier depuis associé 1` ;
- bouton : `Utiliser la SELARL comme acquéreur` ;
- champ source unique avec aperçu des variables alimentées ;
- champs dérivés verrouillés tant que la réutilisation est active.

## Retours associés intégrés

### A. Signataire / associé 1

Problème : l'UI actuelle peut demander deux fois la même identité.

Proposition : ajouter une case `Le signataire est le premier associé` et un bouton `Copier depuis associé 1` pour les cas où le lien n'est pas permanent.

Impact UX : réduction de la double saisie, cohérence plus forte entre documents communs, statuts et PV.

### B. Libellé `Dirigeant / pharmacien`

Problème : le wording est incohérent pour le pilote SELARL et a été repéré dans `src/sydel_doc_engine/app/streamlit_app.py`.

Règle cible :

- SELARL / SCI / SCM / SPFPL : `Gérant` ;
- SELAS / SAS : `Président` ;
- générique : `Représentant légal`.

Pour le pilote SELARL, utiliser `Gérant / professionnel principal`. Cette formulation rappelle le rôle juridique et le rôle métier sans imposer que le gérant soit toujours une personne distincte.

### C. Champ `adresse` ambigu

Problème : un champ nommé seulement `adresse` ne permet pas de savoir quoi saisir.

Règle : aucun champ ne doit s'appeler seulement `adresse`.

Adresses qualifiées dans le pilote :

- adresse personnelle du professionnel ;
- adresse du siège social ;
- adresse de domiciliation ;
- adresse du cabinet cédé ;
- adresse du bailleur ;
- adresse des locaux loués ;
- adresse de la banque ;
- adresse du bien financé ;
- adresse de la SCM cédée ;
- adresse du service d'enregistrement.

### D. PV d'autorisation d'emprunt

Vérification :

- source V2 SELARL : aucun document autonome `PV d'autorisation d'emprunt` n'est listé ;
- catalogue `case_catalog.py` : aucun document autonome de ce nom ;
- UI actuelle : checkbox `PV avec autorisation d'emprunt` ;
- specs PV : l'emprunt est une branche conditionnelle du `DOC-004` PV nomination gérant.

Décision produit V1 : ne pas afficher `PV d'autorisation d'emprunt` comme document distinct du flux SELARL pilote. Afficher seulement une option conditionnelle dans le bloc `Banque / financement` du PV nomination gérant.
