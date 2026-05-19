# Schéma de formulaire SELARL V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Ce document transforme les variables SELARL en blocs de saisie compréhensibles pour un juriste. Il ne modifie pas l'UI actuelle : il définit la cible de saisie du pilote.

Sources : arbitrages explicites de l'associé, `project/source_truth/notebooklm_selarl_10_prompts_v1.md`, `project/source_truth/Documents_a_generer_par_cas_V3.docx`, V2 historique et référentiels existants `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md`, `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md`, specs delivery des familles SELARL.

## Principes

- Le formulaire part du processus SELARL, pas des générateurs.
- Chaque champ doit avoir un libellé qualifié.
- Une donnée saisie une fois doit alimenter tous les documents qui en dépendent.
- Les documents manuels restent visibles, mais ne déclenchent pas de génération.
- Les champs conditionnels ne sont obligatoires que si leur bloc est actif.

## Ordre conceptuel cible

Le schéma SELARL exprime désormais l'ordre validé suivant :

1. Qualification ;
2. Fiche Client / Praticien ;
3. Fiche Société ;
4. Capital & Associés ;
5. Contexte & scénarios métier ;
6. Documents & génération.

Cet ordre ne modifie pas les générateurs ni le moteur DOCX/PDF/ZIP. Les règles de réutilisation sont portées par le schéma et les projections métier, sans dérivation automatique dangereuse.

## Blocs et champs

| Champ UI cible | Variable(s) moteur alimentée(s) | Bloc UI | Obligatoire | Condition d'affichage | Aide contextuelle | Exemple |
|---|---|---|---|---|---|---|
| Profession exercée | `conditions.profession`, `statuts_sel.profession`, `ordre.profession` | Qualification du dossier | oui | Toujours | Choisir le métier qui pilote les statuts et les mentions ordinales. | Chirurgien-dentiste |
| Site distinct à déclarer | `conditions.site_distinct`, `dossier_options.site_distinct` | Qualification du dossier | oui | Toujours | Affiche une pièce manuelle si un site distinct est concerné. | Non |
| Cession de parts de SCM vers la SELARL | `conditions.scm_cession`, `dossier_options.scm_cession` | Qualification du dossier | oui | Toujours | Active les documents SCM cession, distincts de la cession de cabinet. | Oui |
| Régime matrimonial communautaire | `conditions.regime_communautaire`, `dossier_options.regime_communautaire` | Qualification du dossier | oui | Toujours | Active les lettres conjoint et renonciation. | Oui |
| Dérogation ordinale | `conditions.derogation`, `dossier_options.derogation` | Qualification du dossier | oui | Toujours | Affiche les pièces de dérogation attendues ; dans la vraie V2 du pilote elles restent hors génération automatique. | Non |
| Cession de cabinet | `conditions.cession`, `dossier_options.cession` | Qualification du dossier | oui | Toujours | Active les blocs cession, bail et financement. | Oui |
| Type de cabinet cédé | `conditions.cabinet_type`, `cession.cabinet.type` | Qualification du dossier | conditionnel | Si cession de cabinet = oui | Choisir `aucun` si la cession ne porte pas sur un cabinet médical ou dentaire. | Cabinet dentaire |
| Dossier unipersonnel | `conditions.dossier_unipersonnel`, `ui.reuse.dossier_unipersonnel` | Qualification du dossier | optionnel | Toujours | Option explicite : le Praticien est l'associé unique, le gérant et le signataire. | Oui |
| Civilité du Praticien | `signataire.civilite_affichage`, `dirigeant_nomine.civilite_affichage` si réutilisé | Fiche Client | oui | Toujours | Civilité affichée, distincte du genre grammatical. | Docteur |
| Genre grammatical du Praticien | `signataire.genre`, `dirigeant_nomine.genre` si réutilisé | Fiche Client | oui | Toujours | Pilote les accords comme soussigné/soussignée. | masculin |
| Prénom du Praticien | `signataire.prenom`, `dirigeant_nomine.prenom` si réutilisé | Fiche Client | oui | Toujours | Personne principale du dossier. | Camille |
| Nom du Praticien | `signataire.nom`, `dirigeant_nomine.nom` si réutilisé | Fiche Client | oui | Toujours | Nom de naissance ou nom usuel selon source validée. | Martin |
| Date de naissance du Praticien | `signataire.date_naissance`, `dirigeant_nomine.date_naissance` si réutilisé | Fiche Client | oui | Documents communs, PV | Date au format JJ/MM/AAAA côté UI, export ISO possible côté moteur. | 03/04/1985 |
| Ville de naissance du Praticien | `dirigeant_nomine.ville_naissance` | Fiche Client | conditionnel | PV/statuts actifs | Requise pour le PV nomination gérant. | Lyon |
| Département de naissance du Praticien | `dirigeant_nomine.departement_naissance` | Fiche Client | conditionnel | PV/statuts actifs | Requis pour le PV nomination gérant. | Rhône |
| Nationalité du Praticien | `signataire.nationalite`, `dirigeant_nomine.nationalite` si réutilisé | Fiche Client | oui | Documents communs, PV | Ne pas déduire depuis le lieu de naissance. | française |
| Adresse personnelle du Praticien - numéro | `signataire.adresse_personnelle.num_voie`, `dirigeant_nomine.adresse_personnelle.num_voie` si réutilisé | Fiche Client | oui | Documents communs, PV | Adresse personnelle, pas siège ni cabinet. | 8 |
| Adresse personnelle du Praticien - voie | `signataire.adresse_personnelle.voie`, `dirigeant_nomine.adresse_personnelle.voie` si réutilisé | Fiche Client | oui | Documents communs, PV | Adresse personnelle complète. | avenue Victor Hugo |
| Adresse personnelle du Praticien - code postal | `signataire.adresse_personnelle.cp`, `dirigeant_nomine.adresse_personnelle.cp` si réutilisé | Fiche Client | oui | Documents communs, PV | Code postal personnel. | 69002 |
| Adresse personnelle du Praticien - ville | `signataire.adresse_personnelle.ville`, `dirigeant_nomine.adresse_personnelle.ville` si réutilisé | Fiche Client | oui | Documents communs, PV | Ville personnelle. | Lyon |
| Fonction du Praticien | `signataire.fonction_dirigeant`, `dirigeant_nomine.fonction_affichage` | Fiche Client | oui | Toujours | Pour SELARL pilote : utiliser `Gérant` si le Praticien exerce le mandat social. | Gérant |
| Numéro RPPS | `ordre.numero_rpps` | Ordre professionnel | conditionnel | Demande d'inscription / dérogation | Numéro professionnel si disponible. | 10101234567 |
| Numéro ordinal | `ordre.numero_ordre` | Ordre professionnel | conditionnel | Demande d'inscription / dérogation | Numéro d'inscription à l'ordre. | 75-12345 |
| Conseil de l'ordre compétent | `ordre.conseil`, `ordre.ville_ordre`, V2 `[ville_ordre]` | Ordre professionnel | oui | Si `DOC-034` actif | Conseil départemental ou autorité compétente. | Conseil départemental de Paris |
| Adresse du conseil de l'ordre | `ordre.adresse_conseil_ordre`, `ordre.cp_ordre`, `ordre.ville_ordre`, V2 `[adresse_conseil_ordre]`, `[cp_ordre]`, `[ville_ordre]` | Ordre professionnel | conditionnel | Si demande d'inscription à l'ordre active | Adresse du conseil de l'ordre, distincte de l'adresse personnelle, du siège et du cabinet. | 10 rue du Conseil, 75000 Paris |
| Adresse du lieu d'exercice | `ordre.adresse_lieu_exercice`, V2 `[adresse_lieu_exercice]` | Ordre professionnel | conditionnel | Statuts chirurgien-dentiste actifs | Adresse professionnelle d'exercice demandée par la vraie V2. | 4 rue du Cabinet, 75015 Paris |
| Dénomination de la SELARL | `societe.denomination` | Fiche Société | oui | Toujours | Nom de la société en création ou acquéreur dans le dossier. | SELARL DU CENTRE |
| Forme sociale | `societe.forme_sociale`, `societe.forme_sociale_affichage`, `societe.forme_sociale_libelle_long` | Fiche Société | oui | Toujours | Valeur pilote : SELARL. Le libellé long alimente certains documents. | SELARL |
| Capital social | `societe.capital`, `societe.capital_social` | Fiche Société | oui | Documents communs, PV, statuts, cession | Montant du capital de la SELARL. | 5 000 euros |
| Ville du RCS | `societe.ville_rcs` | Fiche Société | oui | Statuts, PV, cession SCM | Greffe d'immatriculation de la SELARL. | Paris |
| Adresse du siège social - numéro | `societe.siege.num_voie` | Siège social | oui | Toujours | Adresse juridique du siège, distincte de l'adresse personnelle et du cabinet cédé. | 12 |
| Adresse du siège social - voie | `societe.siege.voie` | Siège social | oui | Toujours | Ne pas utiliser pour le cabinet cédé sauf si cela est explicitement le même lieu. | rue de la Paix |
| Adresse du siège social - code postal | `societe.siege.cp` | Siège social | oui | Toujours | Code postal du siège. | 75002 |
| Adresse du siège social - ville | `societe.siege.ville` | Siège social | oui | Toujours | Ville du siège. | Paris |
| Adresse de domiciliation affichée | `domiciliation.adresse_affichee`, alias runtime `domiciliation.adresse_domiciliation_affichee` | Siège social | oui | Si `DOC-002` actif | Champ libre décidé V1 ; ne pas déduire automatiquement sans confirmation. | 12 rue de la Paix, 75002 Paris |
| Nombre total de parts | `capital.nb_parts_total`, `statuts_sel.capital.nb_parts_total` | Capital & Associés | conditionnel | Si PV/statuts actifs | Doit correspondre à la somme des parts des associés. | 500 |
| Valeur nominale d'une part | `capital.valeur_nominale_part`, `statuts_sel.capital.valeur_nominale_part` | Capital & Associés | conditionnel | Si PV/statuts actifs | Utilisé pour la répartition du capital. | 10 euros |
| Signataire est le premier associé | `ui.reuse.signataire_associe_1`, mapping vers `associes[0]` | Capital & Associés | optionnel | Si au moins un associé | Evite de ressaisir l'identité du Praticien. | Oui |
| Nombre d'associés | `associes[]` cardinalité | Capital & Associés | oui | PV/statuts actifs | V1 doit couvrir le cas simple et bloquer les cardinalités non arbitrées. | 1 |
| Associé 1 - identité | `associes[0].civilite_affichage`, `associes[0].prenom`, `associes[0].nom`, `associes[0].genre` | Capital & Associés | oui | PV/statuts actifs | Peut être copié depuis le Praticien. | Dr Camille Martin |
| Associé 1 - parts | `associes[0].nb_parts` | Capital & Associés | oui | PV/statuts actifs | Doit s'additionner au total de parts. | 500 |
| Associé 2 - identité | `associes[1].*` | Capital & Associés | conditionnel | Si nombre d'associés >= 2 | Cas simple V1 seulement si la spec du document l'autorise. | Dr Alex Bernard |
| Gérant choisi parmi les associés | `dirigeant_nomine.ref_associe_index` | Capital & Associés | optionnel | Si PV/statuts actifs | Masque les champs d'identité du gérant s'ils sont déjà portés par l'associé. | Associé 1 |
| Copier le signataire vers le mandataire | `mandataire.*` depuis `signataire.*` | Mandataire / signataire | optionnel | Si demande d'inscription à l'ordre active et option cochée | Option de confort DOC-034 ; jamais activée par défaut. | Oui |
| Identité du mandataire | `mandataire.civilite`, `mandataire.prenom`, `mandataire.nom`, `mandataire.fonction` | Mandataire / signataire | conditionnel | Si mandataire distinct | Personne ou cabinet qui signe ou dépose la demande. | Me Dupont |
| Identité du conjoint | `conjoint.civilite`, `conjoint.prenom`, `conjoint.nom`, `conjoint.genre` | Régime matrimonial / conjoint | conditionnel | Si régime communautaire = oui | Alimente les lettres conjoint. | Mme Sophie Martin |
| Régime matrimonial | `apport.regime_matrimonial`, `regime_communautaire.*` | Régime matrimonial / conjoint | conditionnel | Si régime communautaire = oui | Ne pas déduire sans preuve dossier. | communauté légale |
| Apport concerné par le régime communautaire | `apport`, `regime_communautaire.renonciation`, `regime_communautaire.avertissement` | Régime matrimonial / conjoint | conditionnel | Si régime communautaire = oui | Décrire la somme ou le bien commun concerné selon la spec. | apport en numéraire |
| Montant de l'apport soumis au régime communautaire | `apport.montant`, `apport.montant_lettres`, V2 `[apport_personne_1]`, `[apport_lettres_personne_1]` | Régime matrimonial / conjoint | conditionnel | Si régime communautaire = oui | Montant ou apport visé par la renonciation du conjoint. | 5 000 euros |
| Cabinet cédé - adresse | `cession.cabinet.adresse.*`, `cession.cabinet.adresse_affichee` | Cession de cabinet | conditionnel | Si cession = oui | Adresse du cabinet vendu, distincte du siège social. | 4 rue du Cabinet, 75015 Paris |
| Adresse d'exercice du vendeur | `cession.vendeur.adresse_exercice`, V2 `[adresse_exercice_vendeur]` | Cession de cabinet | conditionnel | Si cession cabinet médical acte actif | Adresse d'exercice du vendeur, distincte de son adresse personnelle. | 4 rue du Cabinet, 75015 Paris |
| Adresse des locaux cédés | `cession.cabinet.adresse_locaux`, `bail.locaux.adresse.*`, V2 `[adresse_locaux]` | Cession de cabinet ; Bail | conditionnel | Si compromis médical ou dentaire actif | Adresse des locaux, à ne pas confondre avec l'adresse du vendeur ou du siège acquéreur. | 4 rue des Locaux, 75015 Paris |
| Vendeur du cabinet | `cession.vendeur.*` | Cession de cabinet | conditionnel | Si cession = oui | Personne ou société cédante. | Dr Jean Durand |
| Adresse personnelle du vendeur | `cession.vendeur.adresse.*`, V2 `[adresse_vendeur]` | Cession de cabinet | conditionnel | Si cession = oui | Adresse personnelle ou siège du vendeur selon sa nature, distincte de l'adresse du cabinet. | 8 avenue du Vendeur, 69002 Lyon |
| Situation matrimoniale du vendeur | `cession.vendeur.situation_maritale`, `cession.vendeur.conjoint.*`, `cession.vendeur.regime_matrimonial`, V2 `[situation_maritale_vendeur]`, `[civilite_conjoint_vendeur]`, `[prenom_conjoint_vendeur]`, `[nom_conjoint_vendeur]`, `[regime_matrimonial_vendeur]` | Cession de cabinet | conditionnel | Si cession = oui et document cible le demande | Données propres au vendeur ; ne pas réutiliser automatiquement le bloc conjoint du professionnel. | Marié sous le régime de la communauté |
| Identifiants vendeur | `cession.vendeur.numero_siren`, `cession.vendeur.numero_ordre`, `cession.vendeur.numero_rpps`, V2 `[numero_siren_vendeur]`, `[ordre_departemental_vendeur]`, `[numero_ordre_vendeur]`, `[numero_rpps_vendeur]` | Cession de cabinet | conditionnel | Si cession = oui | Identifiants professionnels du vendeur. | SIREN 123 456 789 |
| Acquéreur du cabinet | `cession.acquereur.*`, souvent `societe` | Cession de cabinet | conditionnel | Si cession = oui | Peut être la SELARL en création. | SELARL DU CENTRE |
| Adresse du siège de l'acquéreur | `cession.acquereur.siege.*`, V2 `[adresse_siege_acquereur]` | Cession de cabinet | conditionnel | Si acquéreur distinct ou document cession actif | Peut être dérivée du siège SELARL si `La SELARL en création est l'acquéreur` est coché. | 12 rue du Siège, 75002 Paris |
| Représentant de l'acquéreur | `cession.acquereur.representant.*`, V2 `[fonction_acquereur_representant]`, `[civilite_acquereur_representant]`, `[prenom_acquereur_representant]`, `[nom_acquereur_representant]` | Cession de cabinet | conditionnel | Si cession = oui | Représentant légal de l'acquéreur ; peut être le gérant/Praticien. | Dr Camille Martin, gérant |
| Prix de cession | `cession.prix.*` | Cession de cabinet | conditionnel | Si cession = oui | Montant et modalités selon acte ou compromis. | 120 000 euros |
| Décomposition du prix | `cession.prix.elements_corporels`, `cession.prix.elements_incorporels`, V2 `[prix_elements_corporels]`, `[prix_elements_corporels_lettres]`, `[prix_elements_incorporels]`, `[prix_elements_incorporels_lettres]` | Cession de cabinet | conditionnel | Si cession = oui | Détail du prix par catégories prévues dans les actes. | 20 000 euros corporels, 100 000 euros incorporels |
| Historique et activité du cabinet | `cession.cabinet.historique`, `cession.cabinet.exercices[]`, V2 `[date_origine_propriete]`, `[annees_acquisition_patientele]`, `[description_origine_propriete]`, `[exercice_1]`, `[chiffre_affaires_1]`, `[resultat_1]`, `[exercice_2]`, `[chiffre_affaires_2]`, `[resultat_2]`, `[exercice_3]`, `[chiffre_affaires_3]`, `[resultat_3]` | Cession de cabinet | conditionnel | Si cession = oui | Données économiques du cabinet sur les exercices demandés par la vraie V2. | CA 2025 : 250 000 euros |
| Personnel repris | `cession.salaries[]`, V2 `[civilite_salarie_1]`, `[prenom_salarie_1]`, `[nom_salarie_1]`, `[civilite_salarie_2]`, `[prenom_salarie_2]`, `[nom_salarie_2]` | Cession de cabinet | conditionnel | Si acte cabinet dentaire actif | La reprise salariés reste à borner en V1 ; ne pas créer plus de salariés que la source ne le prévoit. | Mme Alice Bernard |
| Banque financeuse | `cession.financement.banque.*` | Banque / financement | conditionnel | Si financement bancaire actif | Banque concernée par l'appel de fonds ou la condition suspensive. | Banque X |
| Adresse de la banque | `cession.financement.banque.adresse.*` | Banque / financement | conditionnel | Si banque active | Adresse de la banque, pas adresse du siège. | 1 boulevard Haussmann, 75009 Paris |
| Prêt de cession | `cession.financement.pret.*`, V2 `[montant_pret]`, `[taux_pret]`, `[duree_pret]` | Banque / financement | conditionnel | Si compromis avec condition de prêt actif | Données du prêt de cession, distinctes de l'emprunt du PV nomination gérant. | 100 000 euros sur 84 mois |
| Crédit vendeur | `cession.financement.credit_vendeur.*`, V2 `[montant_credit_vendeur]`, `[duree_credit_vendeur]`, `[taux_credit_vendeur]`, `[majoration_interet_retard]` | Banque / financement | conditionnel | Si acte ou cession SCM prévoit un crédit vendeur | Modalités du crédit vendeur. | 20 000 euros sur 24 mois |
| Montant maximum de l'emprunt PV | `emprunt.montant_max` | Banque / financement | conditionnel | Si `emprunt.actif = true` dans le PV | Branche du `DOC-004`, pas document autonome. | 250 000 euros |
| Adresse du bien financé par l'emprunt | `bien_immobilier.adresse.*` | Banque / financement | conditionnel | Si `emprunt.actif = true` | Adresse du bien immobilier visé par le PV. | 10 rue du Bien, 75010 Paris |
| Bailleur | `bail.bailleur.*` | Bail | conditionnel | Si cession = oui et avenant bail actif | Identité du bailleur du local. | SCI DES LOCAUX |
| Adresse du bailleur | `bail.bailleur.adresse.*` | Bail | conditionnel | Si bailleur actif | Adresse du bailleur. | 2 rue du Bailleur, 75008 Paris |
| Locataire du bail | `bail.locataire.*`, V2 `[civilite_locataire]`, `[prenom_locataire]`, `[nom_locataire]`, `[profession_locataire]`, `[adresse_locataire]` | Bail | conditionnel | Si avenant bail actif | Locataire au bail, distinct du vendeur et de l'acquéreur si le dossier le prévoit. | Dr Jean Durand |
| Adresse du locataire | `bail.locataire.adresse.*`, V2 `[adresse_locataire]` | Bail | conditionnel | Si locataire actif | Adresse du locataire, pas adresse du bailleur ni des locaux. | 8 rue du Locataire, 75014 Paris |
| Locaux loués | `bail.locaux.adresse.*`, `cession.cabinet.adresse.*` si identique | Bail | conditionnel | Si avenant bail actif | Adresse des locaux du bail. | 4 rue du Cabinet |
| Dates et conditions du bail | `bail.date_bail`, `bail.duree`, `bail.date_debut`, `bail.date_fin`, `bail.reconductions[]`, `bail.superficie`, `bail.loyer_mensuel`, V2 `[date_bail]`, `[duree_bail]`, `[date_debut_bail]`, `[date_fin_bail]`, `[date_reconduction_bail_1]`, `[date_reconduction_bail_2]`, `[superficie_local]`, `[loyer_mensuel]` | Bail | conditionnel | Si bail actif | Paramètres du bail repris dans les actes et compromis. | Bail du 01/01/2025, loyer 2 000 euros |
| SCM cédée | `scm_cession.scm_cedee.*` | SCM | conditionnel | Si SCM cession = oui | Société civile de moyens dont les parts sont cédées. | SCM DES DOCTEURS |
| Adresse du cédant SCM | `scm_cession.cedant.adresse.*`, V2 `[adresse_cedant]` | SCM | conditionnel | Si SCM cession = oui | Adresse du cédant des parts SCM. | 6 rue du Cédant, 75011 Paris |
| Cédant des parts SCM | `scm_cession.cedant.*` | SCM | conditionnel | Si SCM cession = oui | Personne ou société cédante. | Dr Jean Durand |
| Cessionnaire des parts SCM | `scm_cession.cessionnaire.*`, souvent `societe` | SCM | conditionnel | Si SCM cession = oui | Peut être la SELARL en création. | SELARL DU CENTRE |
| Adresse du cessionnaire SCM | `scm_cession.cessionnaire.siege.*`, V2 `[adresse_siege_cessionnaire]` | SCM | conditionnel | Si SCM cession = oui | Peut être dérivée du siège SELARL si la SELARL est la cessionnaire. | 12 rue du Siège, 75002 Paris |
| Société SCM cédée - immatriculation | `scm_cession.scm_cedee.ville_rcs`, `scm_cession.scm_cedee.numero_rcs`, V2 `[ville_rcs_societe_cedee]`, `[numero_rcs_societe_cedee]` | SCM | conditionnel | Si SCM cession = oui | Identifiants RCS de la SCM dont les parts sont cédées. | RCS Paris 123 456 789 |
| Associés de la SCM cédée | `scm_cession.associes_societe_cedee[]`, V2 `[civilite_associe_societe_cedee_1]`, `[prenom_associe_societe_cedee_1]`, `[nom_associe_societe_cedee_1]`, `[civilite_associe_societe_cedee_3]`, `[prenom_associe_societe_cedee_3]`, `[nom_associe_societe_cedee_3]` | SCM | conditionnel | Si SCM cession = oui | Associés mentionnés dans l'acte SCM, distincts des associés de la SELARL. | Dr A, Dr B |
| Prix de cession des parts SCM | `scm_cession.prix.*` | SCM | conditionnel | Si SCM cession = oui | Prix des parts SCM, distinct du prix de cabinet. | 1 000 euros |
| Droits d'enregistrement SCM | `scm_cession.enregistrement.montant_droits`, V2 `[montant_droits_enregistrement]` | SCM | conditionnel | Si courrier SDE actif | Montant à porter dans le courrier SDE. | 25 euros |
| Lieu de signature | `signature.lieu` | Signature | oui | Si un document signé est généré | Lieu affiché dans les documents. | Paris |
| Date de signature | `signature.date` | Signature | oui | Si un document signé est généré | Date de signature du dossier. | 19/05/2026 |
| Nombre d'exemplaires | `signature.nombre_exemplaires`, `document.nombre_exemplaires` | Signature | conditionnel | PV, documents qui l'exigent | Ne pas demander si aucun document actif ne l'utilise. | 3 |

## Règles de réutilisation des données

La règle pivot du pilote est `Dossier unipersonnel`.

Quand `Dossier unipersonnel` est actif :

- le Praticien alimente l'associé unique ;
- le Praticien alimente le gérant ;
- le Praticien alimente le signataire ;
- les champs dérivés doivent être préremplis et verrouillés avec indication de leur source.

Quand `Dossier unipersonnel` est inactif :

- aucune dérivation Praticien / associé / gérant / signataire n'est imposée ;
- les champs associés, gérant et signataire restent saisissables ou confirmables séparément.

Réutilisations conservées seulement comme options explicites :

- la SELARL en création peut alimenter l'acquéreur si `La SELARL en création est l'acquéreur` est cochée ;
- la SELARL en création peut alimenter le cessionnaire des parts SCM si `La SELARL en création est la cessionnaire des parts SCM` est cochée ;
- l'adresse de domiciliation peut alimenter le siège social si `L'adresse de domiciliation est le siège social` est cochée.

Réutilisations de confort conservées hors défaut :

- `Le signataire est le premier associé`, `Le gérant est le Praticien` et `Le signataire est le Praticien` peuvent rester disponibles comme options de compatibilité si le dossier n'est pas unipersonnel ;
- `Copier le signataire vers le mandataire` peut rester disponible pour `DOC-034`, mais le mandataire ne doit pas devenir un sujet UX central et ne doit jamais être déduit par défaut.

Relations à ne pas automatiser sans confirmation explicite :

- vendeur = locataire actuel ;
- siège social = lieu d'exercice ;
- siège social = cabinet cédé ;
- cabinet cédé = lieu d'exercice ;
- vendeur = Praticien ;
- cédant SCM = Praticien.

Mécanismes UI recommandés :

- case à cocher pivot : `Dossier unipersonnel` ;
- options de copie explicites pour les liens hors dossier unipersonnel ;
- bouton : `Utiliser la SELARL comme acquéreur` ;
- bouton : `Utiliser la SELARL comme cessionnaire SCM` ;
- case à cocher : `L'adresse de domiciliation est le siège social` ;
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

Pour le pilote SELARL, utiliser `Fiche Client` pour l'écran personne et `Gérant` lorsque le rôle juridique est affiché.

### C. Champ `adresse` ambigu

Problème : un champ nommé seulement `adresse` ne permet pas de savoir quoi saisir.

Règle : aucun champ ne doit s'appeler seulement `adresse`.

Adresses qualifiées dans le pilote :

- adresse personnelle du Praticien ;
- adresse du siège social ;
- adresse de domiciliation ;
- adresse du conseil de l'ordre ;
- adresse du lieu d'exercice ;
- adresse du cabinet cédé ;
- adresse du bailleur ;
- adresse du locataire ;
- adresse des locaux loués ;
- adresse de la banque ;
- adresse du bien financé ;
- adresse personnelle du vendeur ;
- adresse d'exercice du vendeur ;
- adresse du cédant ;
- adresse du cessionnaire ;
- adresse de la SCM cédée ;
- adresse du service d'enregistrement.

### D. PV d'autorisation d'emprunt

Vérification :

- source V2 SELARL : aucun document autonome `PV d'autorisation d'emprunt` n'est listé ;
- catalogue `case_catalog.py` : aucun document autonome de ce nom ;
- UI actuelle : checkbox `PV avec autorisation d'emprunt` ;
- specs PV : l'emprunt est une branche conditionnelle du `DOC-004` PV nomination gérant.

Décision produit V1 : ne pas afficher `PV d'autorisation d'emprunt` comme document distinct du flux SELARL pilote. Afficher seulement une option conditionnelle dans le bloc `Banque / financement` du PV nomination gérant.

## Couverture des variables V2 réelles

Vérification `SELARL-PILOT-SOURCE-VERIFY-001` : la vraie V2 contient une liste brute de variables plus précise que le premier cadrage. Les champs ci-dessus couvrent les familles suivantes :

| Famille de variables V2 | Bloc UI cible | Règle de saisie |
|---|---|---|
| Identité signataire : `[civilite]`, `[prenom]`, `[nom]`, `[date_naissance]`, `[nationalite]`, `[nom_pere]`, `[nom_mere]` | Fiche Client ; Mandataire / signataire | Saisie une fois, réutilisable pour associé 1, gérant, signataire et représentant si les cases de réutilisation sont cochées. |
| Adresses personnelles : `[num_voie_perso]`, `[voie_perso]`, `[cp_perso]`, `[ville_perso]`, `[adresse_personnelle]`, `[adresse_perso_personne_1]`, `[adresse_perso_personne_2]` | Fiche Client ; Capital & Associés | Chaque adresse doit indiquer la personne concernée ; aucun champ `adresse` nu. |
| Société SELARL : `[denomination_societe]`, `[forme_sociale]`, `[forme_sociale_complete]`, `[capital_social]`, `[capital_lettres]`, `[ville_rcs]`, `[numero_rcs]` | Fiche Société | Source unique pour la SELARL ; peut alimenter acquéreur ou cessionnaire si l'utilisateur l'autorise. |
| Siège : `[num_voie_siege]`, `[voie_siege]`, `[cp_siege]`, `[ville_siege]`, `[adresse_siege]`, `[adresse_siege_acquereur]`, `[adresse_siege_cessionnaire]` | Siège social ; Cession de cabinet ; SCM | Adresse du siège SELARL réutilisable seulement via règle explicite. |
| Ordre : `[profession_reglementee]`, `[profession_reglementee_pluriel]`, `[ordre_departemental]`, `[adresse_conseil_ordre]`, `[cp_ordre]`, `[ville_ordre]`, `[numero_ordre]`, `[numero_rpps]` | Ordre professionnel | Bloc obligatoire si demande d'inscription, statuts professionnels ou cession avec vendeur réglementé. |
| Associés et gérant : `[nb_parts]`, `[nb_parts_total]`, `[valeur_nominale_part]`, `[civilite_personne_1]`, `[prenom_personne_1]`, `[nom_personne_1]`, `[civilite_personne_2]`, `[prenom_personne_2]`, `[nom_personne_2]` | Capital & Associés ; Fiche Client | Listes et parts contrôlées ; copier depuis le Praticien possible. |
| Régime communautaire : `[apport_personne_1]`, `[apport_lettres_personne_1]`, `[prenom_conjoint]`, `[nom_conjoint]` | Régime matrimonial / conjoint | Bloc activé seulement si régime communautaire = oui. |
| SCM cession : variables cédant, cessionnaire, société cédée, associés SCM, parts, prix, crédit vendeur et enregistrement | SCM | Bloc distinct de la cession de cabinet ; SELARL réutilisable comme cessionnaire. |
| Bail : bailleur, locataire, bail, locaux, dates, superficie, loyer | Bail | Bloc activé par cession et documents de bail/cession qui consomment ces champs. |
| Cession cabinet : vendeur, acquéreur, cabinet, locaux, exercices, prix, prêt, crédit vendeur, salariés, signatures | Cession de cabinet ; Banque / financement ; Bail ; Signature | Champs spécialisés par type médical/dentaire et acte/compromis ; ne pas généraliser aux autres cas. |
| Dérogation | Contexte & scénarios métier | La vraie V2 ne fournit pas les variables du formulaire multi-sites et marque `Dérogation SEL BNC` et `Dérogation cumul SELARL BNC` à remplir à la main ; ces documents restent hors génération pilote. |
| Lettre d'avertissement conjoint | Régime matrimonial / conjoint | La vraie V2 indique que le document ne figure pas parmi les sources fournies ; tout affichage générable doit porter cette réserve. |
