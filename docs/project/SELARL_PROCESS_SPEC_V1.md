# Spécification processus SELARL V1

Ticket source : `SELARL-PILOT-PROTOCOL-001`

## Objet

Cette spec reconstruit la logique produit du pilote SELARL à partir de la source de vérité V2, sans modifier l'UI, le moteur DOCX/PDF/ZIP ni les générateurs.

Source V2 utilisée : `project/source_truth/Documents_a_generer_par_cas_V2.docx`.

Vérification `SELARL-PILOT-SOURCE-VERIFY-001` : la vraie V2 lue le 2026-05-19 a pour hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`. Elle remplace le fichier V2 provisoire utilisé au ticket initial.

## A. Choix de qualification du dossier SELARL

| Question métier | Valeurs | Usage |
|---|---|---|
| Profession | `medecin`, `chirurgien_dentiste` | Sélection des statuts SELARL et des champs ordre/profession. |
| Site distinct | oui / non | Affiche le formulaire CD94 manuel. |
| SCM cession | oui / non | Affiche le mini-batch cession de parts SCM vers SELARL. |
| Régime communautaire | oui / non | Affiche les lettres conjoint / renonciation. |
| Dérogation | oui / non | Affiche les pièces de dérogation attendues, toutes hors génération SELARL pilote tant que la vraie V2 reste non fournie / manuelle. |
| Cession | oui / non | Affiche bail, appel de fonds et cession de cabinet selon sous-choix. |
| Si cession : type de cabinet | `cabinet_medical`, `cabinet_dentaire`, `aucun` | Sélectionne les actes/compromis médicaux ou dentaires. |

Règle de cohérence : `cabinet_medical` ou `cabinet_dentaire` ne peut être actif que si `cession = oui`. Si `cession = non`, le type de cabinet doit être `aucun`.

Point d'attention source : la V2 fournie contient une anomalie de libellé autour de la ligne des statuts médecins. Le fichier source pointe vers le modèle médecins ; la qualification produit conserve donc le choix `medecin` demandé par le ticket et déjà présent dans le catalogue.

## B. Documents attendus par bloc

| Bloc | Documents attendus |
|---|---|
| Documents communs dans tous les cas | Déclaration sur l'honneur de non-condamnation ; Autorisation de domiciliation ; Procuration. |
| Documents SELARL de base | PV nomination gérant ; Demande d'inscription à l'ordre. |
| Documents chirurgien-dentiste | Statuts SELARL chirurgien-dentiste. |
| Documents médecin | Statuts SELARL médecin. |
| Documents site distinct | Formulaire de déclaration préalable de site distinct CD94 avec la SEL, manuel. |
| Documents SCM cession | PV AGE cession part SCM ; Courrier SDE cession SCM ; Acte de cession des parts de la SCM vers SELARL. |
| Documents régime communautaire | Lettre de renonciation à revendiquer la qualité d'associé ; Lettre d'avertissement au conjoint. Correction 2026-06-01 : la réserve historique sur `DOC-006` est levée, car la source DOCX Lot 2 existe. |
| Documents dérogation | Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL non fourni dans les sources variables V2 ; Dérogation SEL BNC manuelle ; Dérogation cumul SELARL BNC manuelle. |
| Documents cession | Avenant contrat de bail ; Appel de fonds SEL. |
| Documents cabinet médical | Acte de cession d'un cabinet médical ; Compromis de cession d'un cabinet médical. |
| Documents cabinet dentaire | Acte de cession d'un cabinet dentaire ; Compromis de cession d'un cabinet dentaire. |

## C. Documents et variables par document

| Bloc métier | Document | Fichier source | DOC | Statut | Variables nécessaires | Bloc UI principal |
|---|---|---|---|---|---|---|
| Commun | Déclaration sur l'honneur de non-condamnation | `Declaration sur l'honneur de non condamnation.docx` | `DOC-001` | générable | `signataire`, `signataire.adresse_personnelle`, `signature` | Fiche Client ; Signature |
| Commun | Autorisation de domiciliation | `Autorisation de domiciliation.docx` | `DOC-002` | générable | `signataire`, `societe`, `domiciliation.adresse_affichee`, `signature` | Société ; Siège social ; Signature |
| Commun | Procuration | `Procuration.docx` | `DOC-003` | générable | `signataire`, `societe`, `societe.siege`, `signature` | Mandataire / signataire ; Société |
| SELARL base | PV nomination gérant | `PV nomination gerant.docx` | `DOC-004` | générable | `societe`, `associes[]`, `dirigeant_nomine`, `decision`, `reunion`, `capital`, `emprunt`, `bien_immobilier`, `signature` | Société ; Associés ; Fiche Client ; Banque / financement |
| SELARL base | Demande d'inscription à l'ordre | `Demande d'inscription a l'ordre.docx` | `DOC-034` | générable | `signataire`, `societe`, `ordre`, `mandataire`, `signature`, `dossier.options.derogation` | Ordre professionnel ; Mandataire / signataire |
| Chirurgien-dentiste | Statuts SELARL chirurgien-dentiste | `Modele statuts SELARL chirurgien dentiste sans communaute.docx` | `DOC-016` | générable | `statuts_sel`, `societe`, `associes[]`, `dirigeant_nomine`, `signature` | Société ; Associés ; Fiche Client |
| Médecin | Statuts SELARL médecin | `Modele statuts SELARL medecins.docx` | `DOC-017` | générable | `statuts_sel`, `societe`, `associes[]`, `dirigeant_nomine`, `signature` | Société ; Associés ; Fiche Client |
| Site distinct | Formulaire de déclaration préalable de site distinct CD94 avec la SEL | `Formulaire de declaration prealable de site distinct-CD94 avec la SEL.docx` | aucun | manuel | Données ordinales et site distinct, à confirmer par juriste avant automatisation | Ordre professionnel ; Conditions spécifiques |
| SCM cession | PV AGE cession part SCM | `PV AGE cession part SCM.docx` | `DOC-031` | générable | `scm_cession`, `scm_cession.scm_cedee`, `scm_cession.cessionnaire`, `scm_cession.associes_*[]`, `signature` | SCM |
| SCM cession | Courrier SDE cession SCM | `Courrier SDE.docx` | `DOC-032` | générable | `scm_cession`, `scm_cession.enregistrement`, `scm_cession.signataire_sde`, `signature` | SCM ; Signature |
| SCM cession | Acte de cession des parts de la SCM vers SELARL | `Acte de cession des parts de la SCM a la SELARL.docx` | `DOC-033` | générable | `scm_cession`, `scm_cession.scm_cedee`, `scm_cession.cessionnaire`, `scm_cession.cedant`, `scm_cession.prix`, `signature` | SCM |
| Régime communautaire | Lettre de renonciation à revendiquer la qualité d'associé | `Lettre de renonciation a revendiquer la qualite d'associe.docx` | `DOC-005` | générable | `signataire`, `conjoint`, `societe`, `apport`, `regime_communautaire.renonciation`, `signature` | Régime matrimonial / conjoint |
| Régime communautaire | Lettre d'avertissement au conjoint | `Lettre d'avertissement au conjoint en cas d'apport d'un bien commun.docx` | `DOC-006` | générable | `signataire`, `conjoint`, adresse du conjoint derivee depuis l'adresse personnelle de l'associe/signataire, `societe`, `apport`, `regime_communautaire.avertissement`, `signature` | Régime matrimonial / conjoint |
| Dérogation | Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL | `Formulaire de derogation pour exercer sur plusieurs sites avec la SEL.docx` | `DOC-013` | manuel pour le pilote SELARL / source variables non fournie | aucune variable fournie dans la vraie V2 ; ne pas envoyer à la génération SELARL pilote sans arbitrage | Ordre professionnel ; Conditions spécifiques |
| Dérogation | Dérogation SEL BNC | non précisé dans la source V2 | aucun | manuel | Pièce manuelle ; zones narratives sensibles | Conditions spécifiques |
| Dérogation | Demande de dérogation cumul SELARL BNC | non fourni comme source exploitable V2 | `DOC-014` connu moteur | manuel pour le pilote SELARL | la vraie V2 indique explicitement `à remplir à la main` ; ne pas envoyer à la génération SELARL pilote | Conditions spécifiques |
| Cession | Avenant contrat de bail | `Avenant Contrat de bail.docx` | `DOC-007` | générable | `bail`, `societe`, `cession.cabinet`, `signature` | Bail ; Cession de cabinet |
| Cession | Appel de fonds SEL | `appel de fond sel.docx` | `DOC-008` | générable | `societe`, `cession.financement`, `cession.vendeur`, `cession.acquereur`, `signature` | Banque / financement ; Cession de cabinet |
| Cabinet médical | Acte de cession d'un cabinet médical | `Acte de cession d_un cabinet medical.docx` | `DOC-009` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `signature` | Cession de cabinet |
| Cabinet médical | Compromis de cession d'un cabinet médical | `Compromis de cession d_un cabinet medical.docx` | `DOC-010` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `signature` | Cession de cabinet |
| Cabinet dentaire | Acte de cession d'un cabinet dentaire | `Acte de cession d'un cabinet dentaire.docx` | `DOC-011` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `cession.salaries[]`, `signature` | Cession de cabinet |
| Cabinet dentaire | Compromis de cession d'un cabinet dentaire | `Compromis de cession d_un cabinet dentaire.docx` | `DOC-012` | générable | `cession.cabinet`, `cession.vendeur`, `cession.acquereur`, `cession.financement`, `cession.prix`, `cession.salaries[]`, `signature` | Cession de cabinet |

## Documents hors flux SELARL pilote

- `Demande de dérogation cumul SELARL salariée` n'est pas dans le flux SELARL pilote V2 ; elle est rattachée au chemin SELAS dans le catalogue et reste non implémentée.
- `PV d'autorisation d'emprunt` n'apparaît pas comme document autonome dans la source V2 ni dans le catalogue SELARL. L'emprunt est une branche conditionnelle du `DOC-004` PV nomination gérant, pilotée par `emprunt.actif`.

## Variables V2 brutes vérifiées

Cette section complète la table précédente avec les variables réellement listées dans la vraie V2. Elle sert de point de contrôle pour le formulaire et évite de remplacer la source par des paquets de variables trop génériques.

| Document | Variables V2 brutes | Bloc métier principal |
|---|---|---|
| Déclaration sur l'honneur de non-condamnation | `[civilite]`, `[prenom]`, `[nom]`, `[date_naissance]`, `[num_voie_perso]`, `[voie_perso]`, `[cp_perso]`, `[ville_perso]`, `[nationalite]`, `[nom_pere]`, `[nom_mere]`, `[lieu_signature]`, `[date_signature]` | Fiche Client ; Signature |
| Autorisation de domiciliation | `[civilite]`, `[prenom]`, `[nom]`, `[denomination_societe]`, `[capital_social]`, `[num_voie_siege]`, `[voie_siege]`, `[cp_siege]`, `[ville_siege]`, `[lieu_signature]`, `[date_signature]` | Société ; Siège social ; Signature |
| Procuration | `[civilite]`, `[prenom]`, `[nom]`, `[num_voie_perso]`, `[voie_perso]`, `[cp_perso]`, `[ville_perso]`, `[fonction_dirigeant]`, `[denomination_societe]`, `[num_voie_siege]`, `[voie_siege]`, `[cp_siege]`, `[ville_siege]`, `[lieu_signature]`, `[date_signature]` | Mandataire / signataire ; Société ; Siège social |
| PV nomination gérant | `[denomination_societe]`, `[forme_sociale]`, `[capital_social]`, `[num_voie_siege]`, `[voie_siege]`, `[cp_siege]`, `[ville_siege]`, `[date_decision]`, `[date_reunion_lettres]`, `[nb_parts]`, `[valeur_nominale_part]`, `[denomination_societe_1]`, `[nb_parts_societe_1]`, `[prenom_personne_2]`, `[nom_personne_2]`, `[nb_parts_personne_2]`, `[civilite_personne_1]`, `[prenom_personne_1]`, `[nom_personne_1]`, `[profession_personne_1]`, `[date_naissance_personne_1]`, `[ville_naissance_personne_1]`, `[adresse_perso_personne_1]`, `[nationalite_personne_1]`, `[civilite_personne_2]`, `[profession_personne_2]`, `[date_naissance_personne_2]`, `[ville_naissance_personne_2]`, `[adresse_perso_personne_2]`, `[nationalite_personne_2]`, `[lieu_signature]` | Société ; Associés ; Fiche Client |
| Demande d'inscription à l'ordre | `[prenom]`, `[nom]`, `[profession_reglementee]`, `[adresse_personnelle]`, `[profession_reglementee_pluriel]`, `[adresse_conseil_ordre]`, `[cp_ordre]`, `[ville_ordre]`, `[lieu_signature]`, `[date_signature]`, `[denomination_societe]`, `[civilite_mandataire]`, `[prenom_mandataire]`, `[nom_mandataire]`, `[fonction_mandataire]`, `[denomination_cabinet_mandataire]` | Ordre professionnel ; Mandataire / signataire |
| Statuts chirurgien-dentiste | `[denomination_societe]`, `[forme_sociale_complete]`, `[profession_reglementee]`, `[capital_social]`, `[adresse_siege]`, `[civilite]`, `[prenom]`, `[nom]`, `[profession]`, `[date_naissance]`, `[ville_naissance]`, `[departement_naissance]`, `[nationalite]`, `[adresse_personnelle]`, `[profession_reglementee_pluriel]`, `[ordre_departemental]`, `[numero_rpps]`, `[forme_sociale]`, `[adresse_lieu_exercice]`, `[duree_societe]`, `[montant_apport]`, `[montant_apport_lettres]`, `[nom_banque]`, `[capital_lettres]`, `[nb_parts_total]`, `[valeur_nominale_part]`, `[debut_exercice]`, `[fin_exercice]`, `[date_cloture_exercice_1]`, `[prestataire_signature_electronique]`, `[lieu_signature]`, `[date_signature]` | Société ; Fiche Client ; Ordre professionnel ; Banque / financement ; Signature |
| Statuts médecin | `[denomination_societe]`, `[capital_social]`, `[adresse_siege]`, `[civilite]`, `[prenom]`, `[nom]`, `[profession]`, `[date_naissance]`, `[ville_naissance]`, `[departement_naissance]`, `[nationalite]`, `[adresse_personnelle]`, `[ville_ordre]`, `[numero_ordre]`, `[numero_rpps]`, `[forme_sociale_complete]`, `[capital_lettres]`, `[nom_banque]`, `[adresse_banque]`, `[nb_parts_total]`, `[valeur_nominale_part]`, `[civilite_personne_2]`, `[prenom_personne_2]`, `[nom_personne_2]`, `[seuil_achat_materiel]`, `[seuil_emprunt_gerance]`, `[date_cloture_exercice_1]`, `[lieu_signature]`, `[date_signature]`, `[nombre_exemplaires_lettres]`, `[prenom_signataire]`, `[nom_signataire]` | Société ; Fiche Client ; Ordre professionnel ; Banque / financement ; Signature |
| Site distinct | aucune variable fournie ; la V2 précise que le formulaire est à remplir à la main et non fourni dans les sources textuelles | Ordre professionnel ; Conditions spécifiques |
| PV AGE cession part SCM | `[denomination_societe]`, `[capital_social]`, `[adresse_siege]`, `[ville_rcs]`, `[numero_rcs]`, `[date_du_jour]`, `[date_pv_lettres]`, `[nb_parts_total]`, `[valeur_nominale_part]`, `[civilite_personne_1]`, `[prenom_personne_1]`, `[nom_personne_1]`, `[parts_personne_1]`, `[civilite_personne_2]`, `[prenom_personne_2]`, `[nom_personne_2]`, `[parts_personne_2]`, `[civilite_personne_3]`, `[prenom_personne_3]`, `[nom_personne_3]`, `[parts_personne_3]`, `[denomination_societe_nouvel_associe]`, `[plage_parts_total]`, `[plage_parts_personne_1]`, `[plage_parts_personne_2]`, `[plage_parts_societe_nouvel_associe]`, `[civilite_personne_4]`, `[prenom_personne_4]`, `[nom_personne_4]`, `[parts_personne_4]`, `[plage_parts_personne_4]` | SCM ; Société ; Associés |
| Courrier SDE cession SCM | `[lieu_signature]`, `[date_signature]`, `[montant_droits_enregistrement]`, `[prenom_signataire]`, `[nom_signataire]` | SCM ; Signature |
| Acte de cession des parts de la SCM à la SELARL | `[civilite_cedant]`, `[prenom_cedant]`, `[nom_cedant]`, `[profession_cedant]`, `[date_naissance_cedant]`, `[ville_naissance_cedant]`, `[departement_naissance_cedant]`, `[nationalite_cedant]`, `[adresse_cedant]`, `[situation_maritale_cedant]`, `[civilite_conjoint_cedant]`, `[prenom_conjoint_cedant]`, `[nom_conjoint_cedant]`, `[ordre_departemental_cedant]`, `[numero_ordre_cedant]`, `[numero_rpps_cedant]`, `[denomination_societe_cessionnaire]`, `[capital_social_cessionnaire]`, `[adresse_siege_cessionnaire]`, `[ville_rcs_cessionnaire]`, `[denomination_societe_cedee]`, `[nb_parts_cedees]`, `[capital_social_societe_cedee]`, `[nb_parts_total_societe_cedee]`, `[ville_rcs_societe_cedee]`, `[numero_rcs_societe_cedee]`, `[civilite_associe_societe_cedee_1]`, `[prenom_associe_societe_cedee_1]`, `[nom_associe_societe_cedee_1]`, `[civilite_associe_societe_cedee_3]`, `[prenom_associe_societe_cedee_3]`, `[nom_associe_societe_cedee_3]`, `[plage_parts_cedees]`, `[prix_unitaire_part_lettres]`, `[prix_unitaire_part]`, `[prix_global_parts_lettres]`, `[prix_global_parts]`, `[montant_credit_vendeur]`, `[duree_credit_vendeur]`, `[taux_credit_vendeur]`, `[lieu_signature]`, `[nombre_exemplaires_lettres]`, `[civilite_representant_cessionnaire_courte]`, `[prenom_representant_cessionnaire]`, `[nom_representant_cessionnaire]` | SCM ; Cessionnaire ; Cédant ; Signature |
| Lettre de renonciation | `[lieu_signature]`, `[date_signature]`, `[civilite]`, `[prenom]`, `[nom]`, `[date_du_jour]`, `[denomination_societe]`, `[forme_sociale_complete]`, `[apport_personne_1]`, `[apport_lettres_personne_1]`, `[prenom_conjoint]`, `[nom_conjoint]` | Régime matrimonial / conjoint |
| Lettre d'avertissement au conjoint | source DOCX Lot 2 ; variables moteur `signataire`, `conjoint`, adresse du conjoint derivee depuis l'adresse personnelle de l'associe/signataire, `societe`, `apport`, `regime_communautaire.avertissement`, `signature` | Régime matrimonial / conjoint |
| Dérogations | aucune variable fournie ; le formulaire multi-sites est non fourni dans les sources, `Dérogation SEL BNC` et `Dérogation cumul SELARL BNC` sont à remplir à la main | Conditions spécifiques |
| Avenant contrat de bail | `[date_du_jour]`, `[civilite_bailleur]`, `[prenom_bailleur]`, `[nom_bailleur]`, `[profession_bailleur]`, `[date_naissance_bailleur]`, `[ville_naissance_bailleur]`, `[nationalite_bailleur]`, `[adresse_bailleur]`, `[civilite_locataire]`, `[prenom_locataire]`, `[nom_locataire]`, `[profession_locataire]`, `[date_naissance_locataire]`, `[ville_naissance_locataire]`, `[nationalite_locataire]`, `[adresse_locataire]`, `[date_bail]`, `[denomination_societe]`, `[ville_rcs]`, `[adresse_siege]`, `[civilite_courte_locataire]`, `[lieu_signature]`, `[nombre_exemplaires_lettres]`, `[date_signature]` | Bail ; Cession de cabinet ; Signature |
| Appel de fonds SEL | `[nom_banque]`, `[lieu_signature]`, `[date_signature]`, `[civilite_destinataire]`, `[prenom_destinataire]`, `[nom_destinataire]`, `[denomination_societe]`, `[civilite_vendeur]`, `[prenom_vendeur]`, `[nom_vendeur]`, `[denomination_societe_acquereur]`, `[prenom_signataire]`, `[nom_signataire]` | Banque / financement ; Cession de cabinet ; Signature |
| Acte de cession cabinet médical | variables vendeur, acquéreur, cabinet, bail, exercices, prix, crédit vendeur, SCM, immatriculation, ordre et signatures listées en V2 : notamment `[adresse_vendeur]`, `[adresse_exercice_vendeur]`, `[adresse_siege_acquereur]`, `[adresse_cabinet]`, `[date_bail]`, `[loyer_mensuel]`, `[prix_cession]`, `[montant_credit_vendeur]`, `[signature_acquereur]`, `[signature_vendeur]` | Cession de cabinet ; Bail ; Banque / financement ; Signature |
| Compromis de cession cabinet médical | variables vendeur, acquéreur, locaux, bail, exercices, prix, prêt et signatures listées en V2 : notamment `[adresse_vendeur]`, `[adresse_cabinet]`, `[adresse_locaux]`, `[date_bail]`, `[montant_pret]`, `[taux_pret]`, `[duree_pret]`, `[signature_acquereur]`, `[signature_vendeur]` | Cession de cabinet ; Bail ; Banque / financement ; Signature |
| Acte de cession cabinet dentaire | variables vendeur, conjoint, acquéreur, précédent propriétaire, bail, exercices, prix, salariés et signature listées en V2 : notamment `[adresse_vendeur]`, `[adresse_siege_acquereur]`, `[telephone_cabinet]`, `[civilite_salarie_1]`, `[prenom_salarie_1]`, `[nom_salarie_1]`, `[date_entree_jouissance]` | Cession de cabinet ; Bail ; Banque / financement ; Signature |
| Compromis de cession cabinet dentaire | variables vendeur, acquéreur, cabinet/locaux, bail, prix, prêt et signatures listées en V2 : notamment `[adresse_vendeur]`, `[adresse_cabinet]`, `[adresse_locaux]`, `[montant_pret]`, `[signature_acquereur]`, `[signature_vendeur]` | Cession de cabinet ; Bail ; Banque / financement ; Signature |

## Points d'ambiguïté à valider

- Confirmer le libellé source de la ligne statuts médecin dans la V2.
- Confirmer si le formulaire site distinct CD94 doit rester seulement manuel dans l'Assistant ou être prérempli dans une phase ultérieure.
- Confirmer si `DOC-013` peut redevenir un formulaire prérempli dans un ticket ultérieur malgré l'absence de variables dans la vraie V2 ; pour le pilote vérifié il reste hors génération.
- `DOC-014` est manuel dans la vraie V2 et ne doit pas redevenir générable dans le flux SELARL sans validation explicite de l'associé.
- Confirmer le périmètre d'appel de fonds SEL pour les cessions non dentaires, car le moteur V1 le limite historiquement.
