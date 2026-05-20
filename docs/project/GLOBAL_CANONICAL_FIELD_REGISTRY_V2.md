# Registre canonique global V2 - proposition issue audit identite

Statut : proposition prudente pour arbitrage humain. Ce registre ne fusionne pas silencieusement les variables : il distingue l identite metier, les formes agregees/decomposees et les reutilisations conditionnelles.

## Synthese
- Variables brutes auditees : 1334 slugs normalises distincts sur 12379 lignes documentaires.
- Documents couverts : 43.
- Familles couvertes : 15.
- Champs canoniques proposes : 49.
- Slugs rattaches a au moins une proposition : 792.
- Slugs hors proposition initiale : 542.

## Regles de lecture
- Un champ avec `{role}` est un modele de champ role : il peut minimiser le front, mais chaque role reste une instance distincte tant qu une regle de reutilisation n est pas validee.
- Les adresses sont traitees avec vigilance maximale : forme affichee et composants peuvent representer la meme adresse, mais siege, domiciliation, cabinet, exercice et personne restent distincts par defaut.
- Les statuts `validé automatiquement` concernent seulement des alias forts deja coherents avec V1; les autres restent `à arbitrer`.

## Champs proposes
### signature.lieu
- Definition metier : Lieu de signature du document.
- Roles possibles : signature
- Variables sources rattachees : 2 slugs; lieu_signature, signature_lieu
- Documents couverts : 43; familles couvertes : 15
- Forme UI recommandee : Champ texte court avec reuse dossier possible.
- Regle de reutilisation eventuelle : Reutilisable par document si le lieu est commun au dossier.
- Risques de confusion : Peut differer entre documents signes a des dates/lieux differents.
- Statut : validé automatiquement

### signature.date
- Definition metier : Date de signature du document.
- Roles possibles : signature
- Variables sources rattachees : 3 slugs; date_signature, signature_date, signature_date_ou_zone_manuelle
- Documents couverts : 41; familles couvertes : 15
- Forme UI recommandee : Date avec option zone manuelle quand la source le demande.
- Regle de reutilisation eventuelle : Reutilisable seulement si la signature du lot est unique.
- Risques de confusion : Confusion avec date de decision, date PV, date bail, date effet.
- Statut : validé automatiquement

### signature.nombre_exemplaires
- Definition metier : Nombre d exemplaires signes ou emis.
- Roles possibles : signature/document
- Variables sources rattachees : 10 slugs; nombre_exemplaires_lettres, signature_nombre_exemplaires_lettres, cession_parts_nombre_exemplaires_lettres, document_nombre_exemplaires_lettres, nombre_exemplaires, signature_nombre_exemplaires, enregistrement_nombre_exemplaires, regime_communautaire_renonciation_nombre_exemplaires_lettres, cession_actions_nombre_exemplaires_lettres, document_nombre_exemplaires
- Documents couverts : 33; familles couvertes : 11
- Forme UI recommandee : Nombre + affichage lettres derive.
- Regle de reutilisation eventuelle : Deriver la version lettres depuis le nombre si possible.
- Risques de confusion : Certaines familles ont un nombre impose par document.
- Statut : validé automatiquement

### societe.denomination
- Definition metier : Denomination d une societe rolee.
- Roles possibles : societe principale, cible, cedee, SPFPL, SCM
- Variables sources rattachees : 6 slugs; denomination_societe, societe_denomination, societe_cible_denomination, societe_spfpl_denomination, cession_acquereur_denomination_societe, scm_cedee_denomination
- Documents couverts : 43; familles couvertes : 15
- Forme UI recommandee : Texte court role par entite.
- Regle de reutilisation eventuelle : Reutiliser uniquement entre roles societaires explicitement egaux.
- Risques de confusion : Fusion dangereuse entre societe dossier, cedee, cible, acquereur et SPFPL.
- Statut : à arbitrer

### societe.forme_sociale
- Definition metier : Forme juridique d une societe rolee.
- Roles possibles : societe principale, cible, cedee, apportee, commissaire
- Variables sources rattachees : 21 slugs; forme_sociale, societe_spfpl_forme_sociale, forme_sociale_complete, societe_cible_forme_sociale, societe_spfpl_forme_sociale_abregee, forme_sociale_acquereur, societe_cible_forme_sociale_complete, forme_sociale_societe_cedee, forme_sociale_abregee, forme_sociale_societe_apportee, forme_sociale_societe_1, societe_forme_sociale_abregee, societe_forme_sociale_complete, societe_forme_sociale, cession_acquereur_forme_sociale, commissaire_aux_apports_forme_sociale, evaluateur_apport_forme_sociale, forme_sociale_cessionnaire, forme_sociale_societe_2, societe_forme_sociale_affichage, societe_forme_sociale_libelle_long
- Documents couverts : 38; familles couvertes : 12
- Forme UI recommandee : Liste controlee + libelle libre si source legacy.
- Regle de reutilisation eventuelle : Reutiliser seulement pour la meme entite societaire.
- Risques de confusion : Les roles societaires proches ne sont pas interchangeables.
- Statut : à arbitrer

### societe.capital_social
- Definition metier : Capital social montant d une societe rolee.
- Roles possibles : societe principale, acquereur, cedee, apportee, SPFPL, SCM
- Variables sources rattachees : 12 slugs; capital_social, societe_spfpl_capital_social, societe_capital_social, societe_cible_capital_social, cession_acquereur_capital_social, commissaire_aux_apports_capital_social, evaluateur_apport_capital_social, capital_montant, cessionnaire_capital_social, scm_cedee_capital_social, societe_capital, capital
- Documents couverts : 38; familles couvertes : 12
- Forme UI recommandee : Montant structure + derive lettres.
- Regle de reutilisation eventuelle : Reutiliser uniquement pour la meme entite societaire.
- Risques de confusion : Confusion majeure entre capital de plusieurs societes et capital d operation.
- Statut : à arbitrer

### societe.rcs.numero
- Definition metier : Numero RCS d une societe rolee.
- Roles possibles : societe principale, acquereur, cedee, apportee, cessionnaire
- Variables sources rattachees : 13 slugs; numero_rcs_societe_cedee, societe_cible_numero_rcs, numero_rcs_acquereur, numero_rcs, numero_rcs_societe_apportee, numero_rcs_societe_1, societe_spfpl_numero_rcs, cession_acquereur_numero_rcs, societe_numero_rcs, commissaire_aux_apports_numero_rcs, evaluateur_apport_numero_rcs, numero_rcs_societe_2, scm_cedee_numero_rcs
- Documents couverts : 27; familles couvertes : 8
- Forme UI recommandee : Texte court controle.
- Regle de reutilisation eventuelle : Reutiliser seulement pour la meme societe identifiee.
- Risques de confusion : RCS de la societe dossier souvent distinct du RCS cedee/acquereur.
- Statut : à arbitrer

### societe.rcs.ville
- Definition metier : Ville RCS d une societe rolee.
- Roles possibles : societe principale, acquereur, cedee, apportee, cessionnaire
- Variables sources rattachees : 16 slugs; ville_rcs_societe_cedee, societe_cible_ville_rcs, ville_rcs, societe_ville_rcs, ville_rcs_cessionnaire, societe_spfpl_ville_rcs, ville_rcs_acquereur, ville_rcs_societe_apportee, ville_rcs_societe_1, cession_acquereur_rcs_ville, commissaire_aux_apports_ville_rcs, evaluateur_apport_ville_rcs, cessionnaire_ville_rcs, scm_cedee_ville_rcs, ville_rcs_societe_2, societe_rcs_ville
- Documents couverts : 32; familles couvertes : 11
- Forme UI recommandee : Texte court / ville.
- Regle de reutilisation eventuelle : Reutiliser seulement pour la meme societe identifiee.
- Risques de confusion : Peut etre confondue avec ville siege ou ville ordre.
- Statut : à arbitrer

### societe.siege.adresse_affichee
- Definition metier : Adresse affichee du siege social d une societe rolee.
- Roles possibles : societe principale, cible, cedee, SPFPL, SCM
- Variables sources rattachees : 11 slugs; adresse_siege, societe_cible_siege_adresse_affichee, societe_spfpl_siege_adresse_affichee, societe_siege_adresse_affichee, adresse_siege_cessionnaire, adresse_siege_societe_cedee, adresse_siege_acquereur, adresse_siege_societe_1, adresse_siege_societe_apportee, siege_affiche, adresse_siege_societe_2
- Documents couverts : 35; familles couvertes : 12
- Forme UI recommandee : Adresse affichee + composants optionnels.
- Regle de reutilisation eventuelle : Deriver depuis composants si ceux-ci sont valides.
- Risques de confusion : Adresse siege, domiciliation, cabinet et lieu exercice peuvent differer.
- Statut : à arbitrer

### societe.siege.num_voie
- Definition metier : Numero de voie du siege social.
- Roles possibles : societe rolee
- Variables sources rattachees : 5 slugs; num_voie_siege, societe_spfpl_siege_num_voie, societe_siege_num_voie, societe_cible_siege_num_voie, num_voie_siege_societe_2
- Documents couverts : 22; familles couvertes : 6
- Forme UI recommandee : Champ adresse composant.
- Regle de reutilisation eventuelle : Derivable vers adresse affichee.
- Risques de confusion : Role societaire a conserver.
- Statut : à arbitrer

### societe.siege.voie
- Definition metier : Libelle de voie du siege social.
- Roles possibles : societe rolee
- Variables sources rattachees : 7 slugs; num_voie_siege, voie_siege, societe_spfpl_siege_voie, societe_siege_voie, societe_cible_siege_voie, num_voie_siege_societe_2, voie_siege_societe_2
- Documents couverts : 22; familles couvertes : 6
- Forme UI recommandee : Champ adresse composant.
- Regle de reutilisation eventuelle : Derivable vers adresse affichee.
- Risques de confusion : Role societaire a conserver.
- Statut : à arbitrer

### societe.siege.cp
- Definition metier : Code postal du siege social.
- Roles possibles : societe rolee
- Variables sources rattachees : 5 slugs; cp_siege, societe_siege_cp, societe_spfpl_siege_cp, societe_cible_siege_cp, cp_siege_societe_2
- Documents couverts : 24; familles couvertes : 7
- Forme UI recommandee : Code postal.
- Regle de reutilisation eventuelle : Derivable vers adresse affichee.
- Risques de confusion : Role societaire a conserver.
- Statut : à arbitrer

### societe.siege.ville
- Definition metier : Ville du siege social.
- Roles possibles : societe rolee
- Variables sources rattachees : 5 slugs; ville_siege, societe_siege_ville, societe_spfpl_siege_ville, societe_cible_siege_ville, ville_siege_societe_2
- Documents couverts : 24; familles couvertes : 7
- Forme UI recommandee : Ville.
- Regle de reutilisation eventuelle : Derivable vers adresse affichee.
- Risques de confusion : Role societaire a conserver.
- Statut : à arbitrer

### personne.{role}.civilite_affichage
- Definition metier : Civilite affichee d une personne rolee.
- Roles possibles : praticien, associe, signataire, dirigeant, cedant, vendeur, conjoint, president
- Variables sources rattachees : 55 slugs; civilite, civilite_personne_2, civilite_conjoint, civilite_personne_1, civilite_vendeur, civilite_cedant, civilite_conjoint_cedant, cedant_civilite_affichage, reunion_president_civilite_affichage, apporteur_civilite_affichage, associes_list_civilite_affichage, cession_vendeur_civilite_affichage, civilite_acquereur_representant, civilite_representant_cessionnaire_courte, associes_list_conjoint_civilite_affichage, civilite_associe_societe_cedee_1, civilite_personne_3, conjoint_civilite_affichage, cession_acquereur_representant_civilite_affichage, cession_cabinet_precedent_proprietaire_civilite_affichage, cession_vendeur_conjoint_civilite_affichage, signataire_civilite_affichage, apporteur_ou_cedant_civilite_affichage, civilite_associe_societe_cedee_3, civilite_bailleur, civilite_courte_locataire, civilite_destinataire, civilite_locataire, civilite_personne_4, civilite_precedent_proprietaire, civilite_salarie_1, civilite_salarie_2, commissaire_aux_apports_representant_civilite_affichage, evaluateur_apport_representant_civilite_affichage, representant_civilite_affichage, societe_cible_dirigeant_civilite_affichage, ... (+19)
- Documents couverts : 43; familles couvertes : 15
- Forme UI recommandee : Liste civilite affichee.
- Regle de reutilisation eventuelle : Reutiliser seulement si le role source et cible designent la meme personne.
- Risques de confusion : Ne pas confondre avec genre grammatical.
- Statut : à arbitrer

### personne.{role}.genre
- Definition metier : Genre grammatical ou accord d une personne rolee.
- Roles possibles : personne rolee
- Variables sources rattachees : 11 slugs; cession_acquereur_representant_genre, cession_vendeur_genre, signataire_genre, associe_genre, dirigeant_genre, personne_genre, personne_signataire_genre, apporteur_genre, cedant_genre, conjoint_genre, dirigeant_nomine_genre
- Documents couverts : 17; familles couvertes : 7
- Forme UI recommandee : Enum accord.
- Regle de reutilisation eventuelle : Peut etre derive de civilite seulement si la regle est validee.
- Risques de confusion : Civilite et genre ne sont pas strictement le meme champ.
- Statut : à arbitrer

### personne.{role}.prenom
- Definition metier : Prenom d une personne rolee.
- Roles possibles : praticien, associe, signataire, dirigeant, cedant, vendeur, conjoint, representant
- Variables sources rattachees : 35 slugs; prenom, cedant_prenom, reunion_president_prenom, signataire_prenom, apporteur_prenom, associes_list_prenom, cession_vendeur_prenom, associes_list_conjoint_prenom, conjoint_prenom, societe_spfpl_representant_prenom, cession_acquereur_representant_prenom, cession_cabinet_precedent_proprietaire_prenom, cession_vendeur_conjoint_prenom, apporteur_ou_cedant_prenom, commissaire_aux_apports_representant_prenom, evaluateur_apport_representant_prenom, representant_prenom, societe_cible_dirigeant_prenom, actionnaire_unique_prenom, dirigeant_prenom, president_prenom, signature_signataire_sde_prenom, cedant_conjoint_prenom, associe_prenom, bail_bailleur_prenom, bail_locataire_prenom, cession_financement_destinataire_prenom, document_signataire_prenom, cessionnaire_representant_prenom, dirigeant_nomine_prenom, personne_signataire_prenom, actionnaire_unique_conjoint_prenom, associe_exercant_prenom, mandataire_prenom, representant_legal_prenom
- Documents couverts : 41; familles couvertes : 15
- Forme UI recommandee : Texte court.
- Regle de reutilisation eventuelle : Reutiliser par selection explicite de personne.
- Risques de confusion : Les roles distincts restent distincts par defaut.
- Statut : à arbitrer

### personne.{role}.nom
- Definition metier : Nom d une personne rolee.
- Roles possibles : praticien, associe, signataire, dirigeant, cedant, vendeur, conjoint, representant
- Variables sources rattachees : 42 slugs; nom, apport_numeraire_banque_nom, cedant_nom, note_information_operation_nom, reunion_president_nom, signataire_nom, apporteur_nom, associes_list_nom, cession_vendeur_nom, associes_list_conjoint_nom, conjoint_nom, societe_spfpl_representant_nom, cession_acquereur_representant_nom, cession_cabinet_precedent_proprietaire_nom, cession_vendeur_conjoint_nom, apporteur_conjoint_nom, apporteur_ou_cedant_nom, commissaire_aux_apports_representant_nom, evaluateur_apport_representant_nom, representant_nom, societe_cible_dirigeant_nom, actionnaire_unique_nom, banque_depot_nom, dirigeant_nom, president_nom, signature_signataire_sde_nom, cedant_conjoint_nom, mandataire_nom, associe_nom, bail_bailleur_nom, bail_locataire_nom, cession_financement_banque_nom, cession_financement_destinataire_nom, document_signataire_nom, capital_depot_banque_nom, cessionnaire_representant_nom, ... (+6)
- Documents couverts : 41; familles couvertes : 15
- Forme UI recommandee : Texte court.
- Regle de reutilisation eventuelle : Reutiliser par selection explicite de personne.
- Risques de confusion : Les roles distincts restent distincts par defaut.
- Statut : à arbitrer

### personne.{role}.date_naissance
- Definition metier : Date de naissance d une personne rolee.
- Roles possibles : personne rolee
- Variables sources rattachees : 19 slugs; date_naissance, date_naissance_cedant, date_naissance_vendeur, date_naissance_personne_2, associes_list_date_naissance, cedant_date_naissance, cession_vendeur_date_naissance, apporteur_date_naissance, date_naissance_bailleur, date_naissance_locataire, date_naissance_personne_1, bail_bailleur_date_naissance, bail_locataire_date_naissance, dirigeant_nomine_date_naissance, date_naissance_personne_n, personne_signataire_date_naissance, actionnaire_unique_date_naissance, date_naissance_personne_3, signataire_date_naissance
- Documents couverts : 31; familles couvertes : 10
- Forme UI recommandee : Date.
- Regle de reutilisation eventuelle : Reutiliser par personne selectionnee.
- Risques de confusion : Variables personne_1/personne_2 legacy ambiguës.
- Statut : à arbitrer

### personne.{role}.ville_naissance
- Definition metier : Ville de naissance d une personne rolee.
- Roles possibles : personne rolee
- Variables sources rattachees : 17 slugs; ville_naissance, ville_naissance_cedant, ville_naissance_vendeur, ville_naissance_personne_2, associes_list_ville_naissance, cedant_ville_naissance, cession_vendeur_ville_naissance, apporteur_ville_naissance, ville_naissance_bailleur, ville_naissance_locataire, ville_naissance_personne_1, bail_bailleur_ville_naissance, bail_locataire_ville_naissance, dirigeant_nomine_ville_naissance, ville_naissance_personne_n, actionnaire_unique_ville_naissance, ville_naissance_personne_3
- Documents couverts : 29; familles couvertes : 10
- Forme UI recommandee : Ville.
- Regle de reutilisation eventuelle : Reutiliser par personne selectionnee.
- Risques de confusion : Peut etre combinee avec CP/pays selon cession cabinets.
- Statut : à arbitrer

### personne.{role}.departement_naissance
- Definition metier : Departement ou code de naissance d une personne rolee.
- Roles possibles : personne rolee
- Variables sources rattachees : 15 slugs; departement_naissance, departement_naissance_cedant, departement_naissance_vendeur, associes_list_departement_naissance, cedant_departement_naissance, cession_vendeur_cp_naissance, cession_vendeur_departement_naissance, apporteur_departement_naissance, cp_naissance_vendeur, departement_naissance_personne_2, dirigeant_nomine_departement_naissance, departement_naissance_personne_1, departement_naissance_personne_n, actionnaire_unique_departement_naissance, departement_naissance_personne_3
- Documents couverts : 26; familles couvertes : 9
- Forme UI recommandee : Texte court.
- Regle de reutilisation eventuelle : Reutiliser par personne selectionnee.
- Risques de confusion : Departement naissance distinct du departement ordinal.
- Statut : à arbitrer

### personne.{role}.nationalite
- Definition metier : Nationalite d une personne rolee.
- Roles possibles : personne rolee
- Variables sources rattachees : 19 slugs; nationalite, nationalite_cedant, nationalite_vendeur, nationalite_personne_2, associes_list_nationalite, cedant_nationalite, cession_vendeur_nationalite, apporteur_nationalite, nationalite_bailleur, nationalite_locataire, nationalite_personne_1, bail_bailleur_nationalite, bail_locataire_nationalite, dirigeant_nomine_nationalite, nationalite_personne_n, personne_signataire_nationalite, actionnaire_unique_nationalite, nationalite_personne_3, signataire_nationalite
- Documents couverts : 31; familles couvertes : 10
- Forme UI recommandee : Texte court/liste.
- Regle de reutilisation eventuelle : Reutiliser par personne selectionnee.
- Risques de confusion : Les personnes du dossier peuvent avoir des nationalites differentes.
- Statut : à arbitrer

### personne.{role}.profession
- Definition metier : Profession ou qualification d une personne rolee.
- Roles possibles : praticien, vendeur, apporteur, signataire, associe
- Variables sources rattachees : 41 slugs; profession, profession_reglementee, profession_reglementee_pluriel, profession_vendeur, ordre_profession_reglementee, profession_cedant, societe_cible_profession_reglementee, societe_cible_profession_reglementee_pluriel, societe_spfpl_profession, cedant_profession_reglementee_pluriel, ordre_professionnel, qualification_principale, ordre_profession_reglementee_pluriel, associes_list_profession, cedant_profession, cession_vendeur_profession, apporteur_ordre_professionnel, apporteur_profession_reglementee, profession_bailleur, profession_locataire, profession_libelle, profession_libelle_pluriel, profession_societe_1, signataire_qualification_principale, actionnaire_unique_profession, bail_bailleur_profession, bail_locataire_profession, societe_profession, statuts_sas_profession, titre_professionnel, profession_personne_2, profession_personne_n, actionnaire_unique_qualification_principale, associe_exercant_qualification_principale, derogation_cumul_activite_sel_adresse_residence_professionnelle, ordre_profession_signataire_affichee, ... (+5)
- Documents couverts : 33; familles couvertes : 13
- Forme UI recommandee : Liste controlee + libelle affiche.
- Regle de reutilisation eventuelle : Reutiliser seulement pour la meme personne.
- Risques de confusion : Profession personnelle distincte de forme sociale ou activite societe.
- Statut : à arbitrer

### personne.{role}.fonction
- Definition metier : Fonction juridique ou qualite d une personne rolee.
- Roles possibles : dirigeant, president, representant, mandataire
- Variables sources rattachees : 57 slugs; fonction_dirigeant, fonction_acquereur_representant, societe_spfpl_dirigeant_fonction, dirigeant_nomine_ref_associe_index, dirigeant_fonction, cession_acquereur_representant_fonction, fonction_representant_cessionnaire, representant_fonction, societe_cible_dirigeant_civilite_affichage, societe_cible_dirigeant_fonction, societe_cible_dirigeant_nom, societe_cible_dirigeant_prenom, apporteur_fonction_dirigeant, cessionnaire_representant_fonction, dirigeant_adresse_personnelle_adresse_affichee, dirigeant_civilite_affichage, dirigeant_duree_mandat, dirigeant_nom, dirigeant_prenom, fonction_representant_societe_1, fonction_representant_societe_2, fonction_personne_1, dirigeant_nomine, dirigeant_nomine_date_naissance, dirigeant_nomine_departement_naissance, dirigeant_nomine_fonction, dirigeant_nomine_nationalite, dirigeant_nomine_ville_naissance, duree_mandat_dirigeant, fonction_mandataire, president_fonction, dirigeant_genre, dirigeant_nomine_adresse_personnelle_cp, dirigeant_nomine_adresse_personnelle_num_voie, dirigeant_nomine_adresse_personnelle_ville, dirigeant_nomine_adresse_personnelle_voie, ... (+21)
- Documents couverts : 40; familles couvertes : 13
- Forme UI recommandee : Liste controlee + libelle.
- Regle de reutilisation eventuelle : Peut etre derivee du role seulement si la spec le fixe.
- Risques de confusion : Fonction et qualite associe ne sont pas toujours identiques.
- Statut : à arbitrer

### personne.{role}.adresse_personnelle_affichee
- Definition metier : Adresse personnelle affichee d une personne rolee.
- Roles possibles : personne rolee
- Variables sources rattachees : 41 slugs; adresse_personnelle, adresse_cedant, adresse_vendeur, associes_list_adresse_personnelle_affichee, apporteur_adresse_personnelle_affichee, capital_souscription_president_adresse_personnelle_affichee, actionnaire_unique_adresse_personnelle_affichee, adresse_personnelle_adresse_affichee, dirigeant_adresse_personnelle_adresse_affichee, actionnaire_unique_adresse_personnelle_cp, actionnaire_unique_adresse_personnelle_num_voie, actionnaire_unique_adresse_personnelle_ville, actionnaire_unique_adresse_personnelle_voie, president_adresse_personnelle_affichee, adresse_perso_personne_2, adresse_perso_personne_n, adresse_personne_n, adresse_personnelle_affichee, dirigeant_nomine_adresse_personnelle_cp, dirigeant_nomine_adresse_personnelle_num_voie, dirigeant_nomine_adresse_personnelle_ville, dirigeant_nomine_adresse_personnelle_voie, mandataire_adresse, personne_signataire_adresse_perso_cp, personne_signataire_adresse_perso_num_voie, personne_signataire_adresse_perso_ville, personne_signataire_adresse_perso_voie, signataire_adresse_personnelle_affichee, adresse_perso_personne_1, adresse_personne_1, cedant_adresse_personnelle_adresse_affichee, signataire_adresse_cp, signataire_adresse_num_voie, signataire_adresse_personnelle_cp, signataire_adresse_personnelle_num_voie, signataire_adresse_personnelle_ville, ... (+5)
- Documents couverts : 32; familles couvertes : 11
- Forme UI recommandee : Adresse affichee + composants optionnels.
- Regle de reutilisation eventuelle : Deriver depuis composants si disponibles.
- Risques de confusion : Adresse personnelle, siege, cabinet et domiciliation doivent rester separes.
- Statut : à arbitrer

### personne.{role}.numero_rpps
- Definition metier : Numero RPPS d une personne professionnelle.
- Roles possibles : praticien, vendeur, apporteur, signataire
- Variables sources rattachees : 10 slugs; numero_rpps, ordre_numero_rpps, numero_rpps_cedant, cedant_ordre_numero_rpps, cession_vendeur_numero_rpps, apporteur_ordre_numero_rpps, numero_rpps_vendeur, cedant_numero_rpps, associes_list_numero_rpps, actionnaire_unique_ordre_numero_rpps
- Documents couverts : 21; familles couvertes : 7
- Forme UI recommandee : Texte court controle.
- Regle de reutilisation eventuelle : Reutiliser seulement par personne identifiee.
- Risques de confusion : Numero RPPS personnel distinct des numeros ordre/societe.
- Statut : à arbitrer

### personne.{role}.numero_ordre
- Definition metier : Numero ordinal ou inscription ordre d une personne ou societe.
- Roles possibles : personne/societe inscrite
- Variables sources rattachees : 16 slugs; numero_ordre, ordre_numero, ordre_numero_rpps, numero_ordre_vendeur, cedant_ordre_numero_rpps, cession_vendeur_numero_ordre, apporteur_ordre_numero, apporteur_ordre_numero_rpps, numero_ordre_cedant, cedant_ordre_numero, numero_inscription_ordre, signataire_numero_inscription_ordre, societe_inscription_ordre_numero, associes_list_numero_ordre, actionnaire_unique_ordre_numero, actionnaire_unique_ordre_numero_rpps
- Documents couverts : 23; familles couvertes : 8
- Forme UI recommandee : Texte court controle.
- Regle de reutilisation eventuelle : Reutiliser seulement si l inscrit est identique.
- Risques de confusion : Peut etre personnel ou societaire selon document.
- Statut : à arbitrer

### personne.conjoint.{attribut}
- Definition metier : Identite et attributs du conjoint rattache a une personne rolee.
- Roles possibles : conjoint de cedant/vendeur/apporteur/actionnaire
- Variables sources rattachees : 37 slugs; nom_conjoint, prenom_conjoint, civilite_conjoint, civilite_conjoint_cedant, nom_conjoint_cedant, prenom_conjoint_cedant, associes_list_conjoint_civilite_affichage, associes_list_conjoint_nom, associes_list_conjoint_prenom, conjoint_civilite_affichage, conjoint_nom, conjoint_prenom, nom_conjoint_vendeur, cession_vendeur_conjoint_civilite_affichage, cession_vendeur_conjoint_nom, cession_vendeur_conjoint_prenom, apporteur_conjoint_nom, cp_conjoint, num_voie_conjoint, ville_conjoint, voie_conjoint, civilite_conjoint_vendeur, conjoint_adresse_cp, conjoint_adresse_num_voie, conjoint_adresse_ville, conjoint_adresse_voie, prenom_conjoint_vendeur, cedant_conjoint_civilite_affichage, cedant_conjoint_nom, cedant_conjoint_prenom, cedant_conjoint, cedant_conjoint_identite_complete, actionnaire_unique_conjoint_civilite_affichage, actionnaire_unique_conjoint_nom, actionnaire_unique_conjoint_prenom, conjoint, ... (+1)
- Documents couverts : 23; familles couvertes : 8
- Forme UI recommandee : Bloc personne secondaire.
- Regle de reutilisation eventuelle : Reutiliser seulement par rattachement explicite au conjoint de la meme personne.
- Risques de confusion : Conjoint jamais equivalent a associe ou signataire par defaut.
- Statut : à arbitrer

### capital.titres.nombre_total
- Definition metier : Nombre total de parts ou actions.
- Roles possibles : societe/capital
- Variables sources rattachees : 16 slugs; capital_souscription_nb_actions_total, nb_parts_total, nb_parts_total_societe_cedee, societe_nb_parts_total, societe_cible_nb_parts_total, scm_cedee_nb_parts_total, nb_parts_total_societe_apportee, capital_nombre_titres_total, nb_parts_total_lettres, capital_nb_parts_total, capital_nombre_titres_total_lettres, societe_nb_parts_total_lettres, societe_cible_nb_actions_total, societe_nb_actions_total, societe_nb_actions_total_lettres, statuts_civils_nb_parts_total
- Documents couverts : 30; familles couvertes : 10
- Forme UI recommandee : Nombre + lettres derivees.
- Regle de reutilisation eventuelle : Deriver lettres depuis nombre si possible.
- Risques de confusion : Parts et actions doivent conserver le type de titre.
- Statut : à arbitrer

### capital.titres.valeur_nominale
- Definition metier : Valeur nominale d une part ou action.
- Roles possibles : societe/capital
- Variables sources rattachees : 20 slugs; valeur_nominale_part, capital_souscription_valeur_nominale_action, valeur_nominale_part_lettres, valeur_nominale_action_lettres, valeur_nominale_action, capital_souscription_valeur_nominale_action_lettres, apport_titres_valeur_nominale_action, apport_titres_valeur_nominale_action_lettres, societe_cible_valeur_nominale_part, societe_cible_valeur_nominale_part_lettres, capital_valeur_nominale_titre, capital_valeur_nominale_titre_lettres, scm_cedee_valeur_nominale_part, capital_valeur_nominale_part, societe_valeur_nominale_part, societe_valeur_nominale_part_lettres, societe_cible_valeur_nominale_action_lettres, societe_valeur_nominale_action, societe_valeur_nominale_action_lettres, societe_cible_valeur_nominale_action
- Documents couverts : 25; familles couvertes : 9
- Forme UI recommandee : Montant + lettres derivees.
- Regle de reutilisation eventuelle : Deriver lettres depuis montant.
- Risques de confusion : Part vs action et societe rolee a conserver.
- Statut : à arbitrer

### capital.repartition_associes
- Definition metier : Repartition du capital par associe ou actionnaire.
- Roles possibles : associes/actionnaires
- Variables sources rattachees : 18 slugs; nb_parts_personne_2, capital_souscription_repartition_actions, parts_personne_1, parts_personne_2, parts_personne_3, associes_list_nb_actions, societe_cible_repartition_capital_avant_operation, nb_parts_personne_1, plage_parts_personne_1, plage_parts_personne_2, parts_personne_4, plage_parts_personne_4, societe_cible_repartition_capital_apres_operation, nb_parts_personne_n, plage_parts_personne_n, actions_societe_associe_1, nb_parts_personne_3, associes_list_nb_parts
- Documents couverts : 22; familles couvertes : 7
- Forme UI recommandee : Table repetable.
- Regle de reutilisation eventuelle : Peut alimenter statuts et attestations si meme operation.
- Risques de confusion : Avant/apres operation et souscription initiale peuvent diverger.
- Statut : à arbitrer

### apport.numeraire.montant
- Definition metier : Montant des apports en numeraire.
- Roles possibles : apport/capital
- Variables sources rattachees : 10 slugs; apport_numeraire_banque_adresse_affichee, apport_numeraire_banque_nom, apport_numeraire_montant, apport_numeraire_montant_lettres, capital_souscription_apports_numeraire_montant, montant_apports_numeraire, associe_apport_numeraire, associe_apport_numeraire_lettres, associes_list_apport_numeraire, associes_list_apport_numeraire_lettres
- Documents couverts : 14; familles couvertes : 4
- Forme UI recommandee : Montant + lettres.
- Regle de reutilisation eventuelle : Somme potentielle du capital souscrit si validee.
- Risques de confusion : Apport numeraire distinct de capital social total.
- Statut : à arbitrer

### apport.nature.montant
- Definition metier : Montant ou valeur des apports en nature/titres.
- Roles possibles : apport
- Variables sources rattachees : 19 slugs; apport_titres_nb_parts, apport_titres_nb_parts_lettres, apport_titres_plage_parts, apport_titres_valeur_globale, montant_apports_nature, capital_souscription_apports_nature_montant, apport_titres_nature_titres, apport_titres_nb_actions_attribuees, apport_titres_nb_actions_attribuees_lettres, apport_titres_valeur_globale_lettres, apport_titres_valeur_nominale_action, apport_titres_valeur_nominale_action_lettres, apport_titres_valeur_par_titre, apport_titres_valeur_par_titre_lettres, valeur_apport_global, valeur_apport_global_lettres, valeur_apport_par_part, valeur_apport_par_part_lettres, apport_titres
- Documents couverts : 12; familles couvertes : 4
- Forme UI recommandee : Montant + description titres.
- Regle de reutilisation eventuelle : Peut alimenter capital si operation validee.
- Risques de confusion : Apport titres, apport nature et cession ne sont pas identiques.
- Statut : à arbitrer

### cession.parts.nombre
- Definition metier : Nombre de parts/actions cedees.
- Roles possibles : cession
- Variables sources rattachees : 7 slugs; nb_parts_cedees, cession_parts_nb_parts, cession_parts_nb_parts_lettres, nb_parts_cedees_lettres, nb_parts_scm_a_ceder, nb_actions_cedees, nb_actions_cedees_lettres
- Documents couverts : 15; familles couvertes : 4
- Forme UI recommandee : Nombre + type titre + lettres.
- Regle de reutilisation eventuelle : Deriver lettres depuis nombre.
- Risques de confusion : Parts/actions et SCM/SPFPL/SAS a distinguer.
- Statut : à arbitrer

### cession.parts.plage
- Definition metier : Numerotation ou plage des parts/actions cedees.
- Roles possibles : cession
- Variables sources rattachees : 26 slugs; plage_parts_cedees, apport_titres_plage_parts, cession_parts_plage_parts, plage_parts_societe_associe_1, plage_parts_apportees, plage_parts_personne_1, plage_parts_personne_2, plage_parts_total, plage_parts_personne_4, plage_parts_societe_nouvel_associe, scm_cedee_plage_parts_total, parts_debut, parts_debut_groupe_1, parts_debut_groupe_2, parts_debut_societe_2, parts_fin, parts_fin_groupe_1, parts_fin_groupe_2, parts_fin_societe_2, parts_debut_personne_n, parts_fin_personne_n, plage_parts_personne_n, parts_debut_personne_2, parts_debut_personne_3, parts_fin_personne_2, parts_fin_personne_3
- Documents couverts : 15; familles couvertes : 4
- Forme UI recommandee : Intervalle ou texte affiche.
- Regle de reutilisation eventuelle : Deriver plage si debut/fin valides.
- Risques de confusion : Peut diverger du simple nombre de titres.
- Statut : à arbitrer

### cession.prix.total
- Definition metier : Prix total de cession.
- Roles possibles : cession
- Variables sources rattachees : 12 slugs; prix_cession, prix_cession_lettres, cession_parts_prix_total, cession_parts_prix_total_lettres, cession_prix_total, cession_prix_total_lettres, prix_global_parts, prix_global_parts_lettres, scm_cession_prix_global, scm_cession_prix_global_lettres, cession_actions_prix_total, cession_actions_prix_total_lettres
- Documents couverts : 15; familles couvertes : 4
- Forme UI recommandee : Montant + lettres.
- Regle de reutilisation eventuelle : Peut etre calcule depuis prix unitaire x nombre si regle validee.
- Risques de confusion : Prix total distinct du prix unitaire et des composantes corporelles/incorporelles.
- Statut : à arbitrer

### cession.prix.unitaire
- Definition metier : Prix unitaire par part/action.
- Roles possibles : cession
- Variables sources rattachees : 8 slugs; prix_unitaire_part, prix_unitaire_part_lettres, cession_parts_prix_unitaire, cession_parts_prix_unitaire_lettres, scm_cession_prix_unitaire, scm_cession_prix_unitaire_lettres, cession_actions_prix_unitaire_action, cession_actions_prix_unitaire_action_lettres
- Documents couverts : 11; familles couvertes : 3
- Forme UI recommandee : Montant + lettres.
- Regle de reutilisation eventuelle : Peut calculer le total si nombre valide.
- Risques de confusion : Ne pas fusionner avec prix total.
- Statut : à arbitrer

### cession.cabinet.adresse
- Definition metier : Adresse du cabinet ou des locaux cedes.
- Roles possibles : cabinet/local professionnel
- Variables sources rattachees : 4 slugs; adresse_cabinet, cession_cabinet_adresse_affichee, cession_cabinet_adresse_locaux_affichee, locaux_adresse_affichee
- Documents couverts : 8; familles couvertes : 2
- Forme UI recommandee : Adresse affichee.
- Regle de reutilisation eventuelle : Reutilisable avec bail seulement si le document le dit.
- Risques de confusion : Cabinet, siege et lieu exercice peuvent diverger.
- Statut : à arbitrer

### cession.cabinet.prix_composantes
- Definition metier : Prix des elements corporels/incorporels du cabinet.
- Roles possibles : cession cabinet
- Variables sources rattachees : 8 slugs; prix_elements_corporels, prix_elements_corporels_lettres, prix_elements_incorporels, prix_elements_incorporels_lettres, cession_prix_elements_corporels, cession_prix_elements_corporels_lettres, cession_prix_elements_incorporels, cession_prix_elements_incorporels_lettres
- Documents couverts : 4; familles couvertes : 1
- Forme UI recommandee : Deux montants + lettres.
- Regle de reutilisation eventuelle : Peut sommer vers prix total si regle validee.
- Risques de confusion : Composantes distinctes juridiquement.
- Statut : à arbitrer

### bail.parties
- Definition metier : Parties du bail: bailleur et locataire.
- Roles possibles : bailleur/locataire
- Variables sources rattachees : 20 slugs; adresse_bailleur, adresse_locataire, bail_bailleur_adresse_affichee, bail_bailleur_civilite_affichage, bail_bailleur_date_naissance, bail_bailleur_nationalite, bail_bailleur_nom, bail_bailleur_prenom, bail_bailleur_profession, bail_bailleur_ville_naissance, bail_locataire, bail_locataire_adresse_affichee, bail_locataire_civilite_affichage, bail_locataire_civilite_courte, bail_locataire_date_naissance, bail_locataire_nationalite, bail_locataire_nom, bail_locataire_prenom, bail_locataire_profession, bail_locataire_ville_naissance
- Documents couverts : 2; familles couvertes : 1
- Forme UI recommandee : Blocs personne/societe rolees.
- Regle de reutilisation eventuelle : Reutiliser avec cession seulement si role explicite.
- Risques de confusion : Bailleur, locataire, vendeur et acquereur peuvent diverger.
- Statut : à arbitrer

### bail.dates
- Definition metier : Dates structurantes du bail.
- Roles possibles : bail
- Variables sources rattachees : 6 slugs; date_bail, date_debut_bail, date_fin_bail, date_reconduction_bail_1, date_reconduction_bail_2, cession_bail_date_bail
- Documents couverts : 6; familles couvertes : 2
- Forme UI recommandee : Dates.
- Regle de reutilisation eventuelle : Aucune reutilisation hors bail sans decision.
- Risques de confusion : Dates de bail distinctes des signatures et decisions.
- Statut : à arbitrer

### ordre.professionnel
- Definition metier : Conseil ordinal, departement, adresse et identifiers professionnels.
- Roles possibles : ordre professionnel
- Variables sources rattachees : 44 slugs; ordre_departemental, ordre_ville, ordre_profession_reglementee, ordre_numero, ordre_numero_rpps, ordre_departemental_cedant, ordre_departemental_vendeur, cedant_ordre_departemental, numero_ordre_vendeur, ordre_professionnel, ordre_profession_reglementee_pluriel, cedant_ordre_numero_rpps, cession_vendeur_ordre_departemental, departement_ordre, apporteur_ordre_departement, apporteur_ordre_numero, apporteur_ordre_numero_rpps, apporteur_ordre_professionnel, date_inscription_ordre_acquereur, numero_ordre_cedant, cedant_ordre_numero, ordre_departement_ou_ville, ville_ordre_sel, adresse_conseil_ordre, ordre_departement, societe_inscription_ordre_departement, societe_inscription_ordre_numero, societe_inscription_ordre_ville, ordre_adresse_affichee, actionnaire_unique_ordre_departemental, actionnaire_unique_ordre_numero, actionnaire_unique_ordre_numero_rpps, ordre_adresse_cp, ordre_adresse_ligne_1, ordre_adresse_ville, ordre_conseil_departemental, ... (+8)
- Documents couverts : 24; familles couvertes : 9
- Forme UI recommandee : Bloc institution + numeros.
- Regle de reutilisation eventuelle : Reutiliser par profession/personne/societe inscrite explicite.
- Risques de confusion : Ordre personnel et inscription societe peuvent diverger.
- Statut : à arbitrer

### derogation.{type}
- Definition metier : Variables propres aux demandes de derogation.
- Roles possibles : derogation
- Variables sources rattachees : 23 slugs; dossier_options_derogation, derogation_type, derogation_conditions_continuite_soins, derogation_conditions_environnement_travail, derogation_conditions_reponse_urgences, derogation_cumul_activite_externe_libelle, derogation_cumul_activite_individuelle_adresse_affichee, derogation_cumul_activite_individuelle_temps_hebdomadaire, derogation_cumul_activite_individuelle_type, derogation_cumul_activite_sel_temps_hebdomadaire, derogation_cumul_motifs_equipement_soumis_autorisation, derogation_cumul_motifs_equipement_usages_multiples, derogation_cumul_motifs_explication, derogation_cumul_motifs_regroupement_equipe, derogation, derogation_conditions_qualite_securite_autres_actes_materiels, derogation_conditions_qualite_securite_autres_actes_moyens_personnel, derogation_conditions_qualite_securite_consultations_materiels, derogation_conditions_qualite_securite_consultations_moyens_personnel, derogation_cumul_activite_sel_adresse_residence_professionnelle, derogation_mode_rendu, ordre_derogation_mention_manuelle, ordre_derogation_suffixe
- Documents couverts : 3; familles couvertes : 2
- Forme UI recommandee : Options + texte libre selon famille.
- Regle de reutilisation eventuelle : Aucune fusion globale hors type derogation.
- Risques de confusion : Variables souvent spec-only ou legacy.
- Statut : à arbitrer

### regime_communautaire.{document}
- Definition metier : Champs du batch regime communautaire.
- Roles possibles : apporteur/conjoint/regime
- Variables sources rattachees : 47 slugs; nom_conjoint, prenom_conjoint, civilite_conjoint, civilite_conjoint_cedant, nom_conjoint_cedant, prenom_conjoint_cedant, associes_list_conjoint_civilite_affichage, associes_list_conjoint_nom, associes_list_conjoint_prenom, conjoint_civilite_affichage, conjoint_nom, conjoint_prenom, nom_conjoint_vendeur, cession_vendeur_conjoint_civilite_affichage, cession_vendeur_conjoint_nom, cession_vendeur_conjoint_prenom, dossier_options_regime_communautaire, apporteur_conjoint_nom, cp_conjoint, num_voie_conjoint, ville_conjoint, voie_conjoint, civilite_conjoint_vendeur, conjoint_adresse_cp, conjoint_adresse_num_voie, conjoint_adresse_ville, conjoint_adresse_voie, prenom_conjoint_vendeur, regime_communautaire_date_courrier_avertissement, regime_communautaire_qualite_renoncee, regime_communautaire_regime_matrimonial, cedant_conjoint_civilite_affichage, cedant_conjoint_nom, cedant_conjoint_prenom, regime_communautaire_avertissement_date_signature, regime_communautaire_renonciation_date_signature, ... (+11)
- Documents couverts : 23; familles couvertes : 8
- Forme UI recommandee : Bloc conjoint + dates + options.
- Regle de reutilisation eventuelle : Reutiliser conjoint par personne explicite.
- Risques de confusion : Avertissement et renonciation ont dates/lieux distincts.
- Statut : à arbitrer

### spfpl.operation.type
- Definition metier : Type et contexte d operation SPFPL.
- Roles possibles : SPFPL
- Variables sources rattachees : 33 slugs; operation_spfpl_type, societe_spfpl_capital_social, societe_spfpl_denomination, societe_spfpl_forme_sociale, societe_spfpl_siege_adresse_affichee, societe_spfpl_forme_sociale_abregee, societe_spfpl_siege_cp, societe_spfpl_siege_num_voie, societe_spfpl_siege_ville, societe_spfpl_siege_voie, societe_spfpl_capital_social_lettres, societe_spfpl_profession, societe_spfpl_ville_rcs, note_information_operation_nom, note_information_operation_phrase, societe_spfpl_activite, societe_spfpl_dirigeant_fonction, societe_spfpl, societe_spfpl_libelle_forme_et_capital, societe_spfpl_libelle_forme_long, societe_spfpl_numero_rcs, societe_spfpl_representant_civilite_courte, societe_spfpl_representant_nom, societe_spfpl_representant_prenom, societe_spfpl_representant_identite_qualite, operation_spfpl, operation_spfpl_document_demande, operation_spfpl_nature_titres, activite_spfpl, societe_spfpl_departement_inscription_ordre, societe_spfpl_representant_civilite_affichage, societe_spfpl_representant_fonction, societe_spfpl_representant
- Documents couverts : 13; familles couvertes : 5
- Forme UI recommandee : Enum operation + champs contextuels.
- Regle de reutilisation eventuelle : Piloter les documents, pas fusionner avec societes proches.
- Risques de confusion : SPFPL creee/acquereuse/cible selon cas.
- Statut : à arbitrer

### scm_cession.{champ}
- Definition metier : Champs propres au bloc cession SCM.
- Roles possibles : SCM cedee/cession SCM
- Variables sources rattachees : 51 slugs; dossier_options_scm_cession, scm_cedee_nb_parts_total, scm_cession_agrement_date_limite, scm_cession_agrement_delai_mois, scm_cedee_capital_social, scm_cedee_cogerants_list, scm_cedee_denomination, scm_cedee_forme_juridique, scm_cedee_numero_rcs, scm_cedee_plage_parts_total, scm_cedee_siege_adresse_affichee, scm_cedee_valeur_nominale_part, scm_cedee_ville_rcs, scm_cession_agrement_date_pv, scm_cession_agrement_date_pv_lettres, scm_cession_associes_apres_cession_list, scm_cession_associes_avant_cession_list, scm_cession_associes_presents, scm_cession_associes_presents_list, scm_cession_credit_vendeur_actif, scm_cession_parts_cedees_nb, scm_cession_parts_cedees_plage, scm_cession_prix_global, scm_cession_prix_global_lettres, scm_cession_prix_unitaire, scm_cession_prix_unitaire_lettres, scm_cession, scm_cession_agrement, scm_cession_associes_apres_cession_list_parts_nb, scm_cession_associes_apres_cession_list_parts_plage, scm_cession_associes_avant_cession, scm_cession_associes_avant_cession_list_parts_nb, scm_cession_credit_vendeur_duree, scm_cession_credit_vendeur_majoration_interet_retard, scm_cession_credit_vendeur_montant, scm_cession_credit_vendeur_taux, ... (+15)
- Documents couverts : 3; familles couvertes : 1
- Forme UI recommandee : Bloc operation + parties + prix.
- Regle de reutilisation eventuelle : Reutiliser seulement dans le bloc SCM.
- Risques de confusion : Historique de blocage/resolution, roles sensibles.
- Statut : à arbitrer

### commissaire_aux_apports.{champ}
- Definition metier : Identite du commissaire/evaluateur aux apports et son representant.
- Roles possibles : commissaire/evaluateur
- Variables sources rattachees : 22 slugs; commissaire_aux_apports_rapport_annexe, commissaire_aux_apports_capital_social, commissaire_aux_apports_denomination, commissaire_aux_apports_forme_sociale, commissaire_aux_apports_numero_rcs, commissaire_aux_apports_presentation_complete, commissaire_aux_apports_representant_civilite_affichage, commissaire_aux_apports_representant_nom, commissaire_aux_apports_representant_prenom, commissaire_aux_apports_siege_adresse_affichee, commissaire_aux_apports_ville_rcs, evaluateur_apport_capital_social, evaluateur_apport_denomination, evaluateur_apport_forme_sociale, evaluateur_apport_numero_rcs, evaluateur_apport_representant_civilite_affichage, evaluateur_apport_representant_nom, evaluateur_apport_representant_prenom, evaluateur_apport_siege_adresse_affichee, evaluateur_apport_ville_rcs, commissaire_aux_apports, evaluateur_apport
- Documents couverts : 9; familles couvertes : 2
- Forme UI recommandee : Bloc societe + representant.
- Regle de reutilisation eventuelle : Ne pas reutiliser avec societe dossier.
- Risques de confusion : Entite tierce distincte de la SPFPL/societe cible.
- Statut : à arbitrer

### banque.{role}
- Definition metier : Banque de depot, financement ou apport numeraire.
- Roles possibles : banque depot/financement
- Variables sources rattachees : 14 slugs; nom_banque, adresse_banque, apport_numeraire_banque_adresse_affichee, apport_numeraire_banque_nom, banque_depot_adresse_affichee, banque_depot_nom, cession_financement_banque_nom, capital_depot_banque_adresse, capital_depot_banque_nom, capital_depot_compte_ouvert, capital_depot_date_depot, depot_fonds_banque_nom, depot_fonds, depot_fonds_montant
- Documents couverts : 19; familles couvertes : 6
- Forme UI recommandee : Bloc institution.
- Regle de reutilisation eventuelle : Reutiliser uniquement si la meme banque est confirmee.
- Risques de confusion : Banque financement et banque depot peuvent diverger.
- Statut : à arbitrer

### administration_fiscale.{role}
- Definition metier : Service fiscal ou service enregistrement.
- Roles possibles : administration fiscale
- Variables sources rattachees : 22 slugs; enregistrement_nombre_exemplaires, adresse_service_enregistrement, cp_ville_service_enregistrement, service_enregistrement, enregistrement_adresse_service, enregistrement_centre_finances_publiques, enregistrement_cp_ville_service, enregistrement_montant_droits, enregistrement_service, adresse_impots_ligne_1, adresse_impots_ligne_2, centre_impots, cp_impots, service_impots, ville_impots, impots, impots_adresse_ligne_1, impots_adresse_ligne_2, impots_centre, impots_cp, impots_service, impots_ville
- Documents couverts : 4; familles couvertes : 2
- Forme UI recommandee : Bloc institution/adresse.
- Regle de reutilisation eventuelle : Peut etre un parametrage local plutot qu un champ dossier.
- Risques de confusion : Risque de demander au front une constante cabinet.
- Statut : à arbitrer

### dossier.options.{option}
- Definition metier : Options et decisions de selection documentaire.
- Roles possibles : dossier
- Variables sources rattachees : 11 slugs; dossier_structure, dossier_options_cession, dossier_options_apport, dossier_options_associe_unique, dossier_options_scm_cession, dossier_options_derogation, dossier_options_regime_communautaire, dossier_options_scm_satellites, dossier_options_scm, dossier_options_site_distinct, dossier_options_option_is
- Documents couverts : 39; familles couvertes : 14
- Forme UI recommandee : Toggles/enum dossier.
- Regle de reutilisation eventuelle : Pilote la selection et les champs visibles.
- Risques de confusion : Certaines options sont derivees du cas et ne doivent pas etre redemandees.
- Statut : à arbitrer

## Slugs hors proposition initiale
Ces slugs ne sont pas rejetes. Ils doivent etre traites lors de la passe humaine ou document par document, surtout quand ils sont spec-only/template-only.

- Nombre : 542
- Principaux slugs : associes_list, nom_personne_2, prenom_personne_2, signature, nb_actions, denomination_societe_cedee, date_cloture_exercice_1, capital_lettres, regime_matrimonial, nb_parts_apportees, nom_personne_1, prenom_personne_1, situation_maritale, ville_ordre, capital_souscription_souscripteurs_list, montant_apport, montant_apport_lettres, fin_exercice, debut_exercice, nb_parts_apportees_lettres, date_du_jour, denomination_societe_acquereur, nom_vendeur, prenom_vendeur, associes_cible_list, cp_perso, date_origine_propriete, num_voie_perso, qualite_associe, ville_perso, voie_perso, chiffre_affaires_1, dossier_cession_type_cabinet, exercice_social_debut, exercice_social_fin, nom_signataire, prenom_signataire, resultat_1, date_pv, prenoms, capital_social_societe_cedee, denomination_societe_associe_1, exercice_social_premier_exercice_fin, societe, capital_social_cessionnaire, denomination_societe_cessionnaire, nom_cedant, nom_personne_3, prenom_cedant, prenom_personne_3, signature_acquereur, signature_vendeur, situation_maritale_cedant, adresse_locaux, apport_lettres_personne_1, apport_personne_1, capital_social_acquereur, chiffre_affaires_3, denomination_societe_1, dossier_cession_etape, duree_bail, nombre_pages_lettres, resultat_3, situation_maritale_vendeur, telephone_cabinet, denomination_societe_2, adresse_lieu_exercice, cession_salaries_list, date_reunion_lettres, duree_credit_vendeur, majoration_interet_retard, montant_credit_vendeur, nb_actions_lettres, nb_parts, prestataire_signature_electronique, reunion_annee_pv_lettres, reunion_date_pv, reunion_date_reunion_lettres, reunion_heure_reunion, reunion_president_qualite, ... (+462)
