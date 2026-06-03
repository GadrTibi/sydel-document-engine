# TRACK-B-SELARL-FIELD-DEDUP-AUDIT-001 - Rapport d'audit champs SELARL V1

Date : 2026-05-26

## Conclusion binaire

PASS : aucune vraie duplication editable n'a ete detectee dans le parcours clean front SELARL V1.

Le parcours expose 72 champs de donnees editables, hors bouton d'action `Generer le dossier`.
Les reutilisations centrales sont faites par derivation interne et non par double saisie :

- Praticien -> personne signataire, associe unique, gerant, signataire document.
- Siege social -> domiciliation pour `DOC-002`.
- Capital social -> capital, apport numeraire et depot de fonds.
- Profession -> libelles professionnels, pluriel ordinal et choix `DOC-016` / `DOC-017`.

## Contexte prouve

Commandes executees depuis Track B :

```text
pwd
C:\Users\Gad\Desktop\Sydel\sydel-track-b

git rev-parse --show-toplevel
C:/Users/Gad/Desktop/Sydel/sydel-track-b

git branch --show-current
track-b/clean-rebuild

git status --short --branch
## track-b/clean-rebuild...origin/track-b/clean-rebuild
 M .gitignore
 M README.md
```

Le dirty state preexistant n'a pas ete modifie par cet audit.

## Fichiers audites

- `src/sydel_doc_engine/front_app/app.py`
- `src/sydel_doc_engine/front_app/routing.py`
- `src/sydel_doc_engine/front_app/dossier_selection.py`
- `src/sydel_doc_engine/front_app/data_entry.py`
- `src/sydel_doc_engine/front_app/shell.py`
- `src/sydel_doc_engine/front_app/generation.py`
- `src/sydel_doc_engine/front_app/selarl_slice.py`
- `src/sydel_doc_engine/front_app/legacy_boundary.py`
- `tests/unit/test_clean_front_app.py`
- `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md`

## Methode

La matrice ci-dessous recense les widgets editables du parcours `front_app/shell.py`.
Elle croise ensuite chaque champ avec `SelarlSliceInput`, `build_generation_context()`,
`selected_selarl_document_codes()`, les blocages `validate_selarl_input()` et les
documents generes par le moteur.

Les champs read-only comme les captions, warnings, lignes de documents et chemins de
sortie ne sont pas comptes comme champs utilisateur.

## Matrice des champs utilisateur

| # | field_id | Label affiche | Etape | Donnee metier representee | Variable / structure liee | Editable | Documents impactes |
|---:|---|---|---|---|---|---|---|
| 1 | `clean_dossier_type` | Type de dossier | Type de dossier | Choix du parcours dossier | `DossierTypeOption.key/structure` | Oui | Tous documents de la slice |
| 2 | `selarl_profession` | Profession | Qualification | Profession reglementee du praticien | `profession`, `statuts_sel.overlay`, libelles ordre | Oui | `DOC-034`, `DOC-016` ou `DOC-017` |
| 3 | `selarl_dossier_unipersonnel` | Dossier unipersonnel | Qualification | Regle Praticien = associe unique = gerant = signataire | `dossier_unipersonnel`, `DossierOptions.associe_unique` | Oui | `DOC-004`, `DOC-016`, `DOC-017` |
| 4 | `selarl_regime_communautaire` | Regime communautaire | Qualification | Condition d'activation du regime communautaire | `DossierOptions.regime_communautaire` | Oui | `DOC-005`; `DOC-006` visible reserve |
| 5 | `selarl_derogation` | Derogation | Cas hors perimetre V1 | Option hors generation V1 | `derogation` blocker | Oui | `DOC-013`, `DOC-014` hors V1 |
| 6 | `selarl_site_distinct` | Site distinct | Cas hors perimetre V1 | Option hors generation V1 | `site_distinct` blocker | Oui | Documents site distinct manuels |
| 7 | `selarl_cession` | Cession | Cas hors perimetre V1 | Option cession hors generation V1 | `cession` blocker | Oui | `DOC-007` a `DOC-012` hors V1 |
| 8 | `selarl_scm` | SCM | Cas hors perimetre V1 | Option SCM hors generation V1 | `scm` blocker | Oui | `DOC-031` a `DOC-033` hors V1 |
| 9 | `selarl_dossier_reference` | Reference dossier | Qualification | Reference interne dossier | `metadata.dossier_reference`, output dir | Oui | Aucun document juridique direct |
| 10 | `selarl_civilite` | Civilite | Fiche Client / Praticien | Civilite du praticien | `Person.civilite`, `Associe.civilite_affichage`, `DirigeantNomine.civilite_affichage` | Oui | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017`, `DOC-005 si actif` |
| 11 | `selarl_genre` | Genre | Fiche Client / Praticien | Genre grammatical du praticien | `Person.genre`, `Associe.genre`, `DirigeantNomine.genre` | Oui | `DOC-001`, `DOC-004`, `DOC-016/017` |
| 12 | `selarl_titre_affichage` | Titre affichage | Fiche Client / Praticien | Titre affiche du signataire | `Person.titre_affichage`, `Associe.titre_professionnel` | Oui | `DOC-034`, `DOC-016/017` |
| 13 | `selarl_prenom` | Prenom | Fiche Client / Praticien | Prenom du praticien | `Person.prenom`, `Associe.prenom`, `DirigeantNomine.prenom`, `DocumentSignataire.prenom` | Oui | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017`, `DOC-005 si actif` |
| 14 | `selarl_nom` | Nom | Fiche Client / Praticien | Nom du praticien | `Person.nom`, `Associe.nom`, `DirigeantNomine.nom`, `DocumentSignataire.nom` | Oui | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017`, `DOC-005 si actif` |
| 15 | `selarl_date_naissance` | Date de naissance | Fiche Client / Praticien | Date de naissance du praticien | `Person.date_naissance`, `Associe.date_naissance`, `DirigeantNomine.date_naissance` | Oui | `DOC-001`, `DOC-004`, `DOC-016/017` |
| 16 | `selarl_ville_naissance` | Ville de naissance | Fiche Client / Praticien | Ville de naissance du praticien | `Associe.ville_naissance`, `DirigeantNomine.ville_naissance` | Oui | `DOC-004`, `DOC-016/017` |
| 17 | `selarl_departement_naissance` | Departement naissance | Fiche Client / Praticien | Departement de naissance du praticien | `Associe.departement_naissance`, `DirigeantNomine.departement_naissance` | Oui | `DOC-004`, `DOC-016/017` |
| 18 | `selarl_nationalite` | Nationalite | Fiche Client / Praticien | Nationalite du praticien | `Person.nationalite`, `Associe.nationalite`, `DirigeantNomine.nationalite` | Oui | `DOC-001`, `DOC-004`, `DOC-016/017` |
| 19 | `selarl_situation_maritale` | Situation matrimoniale | Fiche Client / Praticien | Situation matrimoniale du praticien | `Associe.situation_maritale` | Oui | `DOC-016/017` |
| 20 | `selarl_regime_matrimonial` | Regime matrimonial | Fiche Client / Praticien | Regime matrimonial du praticien | `Associe.regime_matrimonial`, `RegimeCommunautaire.regime_matrimonial` | Oui | `DOC-016/017`, `DOC-005 si actif` |
| 21 | `selarl_numero_ordre` | Numero Ordre | Fiche Client / Praticien | Numero d'inscription a l'ordre | `Person.numero_inscription_ordre`, `Company.inscription_ordre.numero`, `SpfplOrdre.numero` | Oui | `DOC-034`, `DOC-016/017` |
| 22 | `selarl_numero_rpps` | Numero RPPS | Fiche Client / Praticien | Numero RPPS du praticien | `SpfplOrdre.numero_rpps` | Oui | `DOC-016/017` |
| 23 | `selarl_nom_pere` | Nom du pere | Fiche Client / Praticien | Filiation pere | `Person.nom_pere` | Oui | `DOC-001` |
| 24 | `selarl_nom_mere` | Nom de la mere | Fiche Client / Praticien | Filiation mere | `Person.nom_mere` | Oui | `DOC-001` |
| 25 | `selarl_adresse_num_voie` | No | Adresse personnelle | Numero de voie du domicile praticien | `Person.adresse_perso.num_voie`, `Associe.adresse_personnelle.num_voie` | Oui | `DOC-001`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017` |
| 26 | `selarl_adresse_voie` | Voie | Adresse personnelle | Voie du domicile praticien | `Person.adresse_perso.voie`, `Associe.adresse_personnelle.voie` | Oui | `DOC-001`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017` |
| 27 | `selarl_adresse_cp` | CP | Adresse personnelle | Code postal du domicile praticien | `Person.adresse_perso.cp`, `Associe.adresse_personnelle.cp` | Oui | `DOC-001`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017` |
| 28 | `selarl_adresse_ville` | Ville | Adresse personnelle | Ville du domicile praticien | `Person.adresse_perso.ville`, `Associe.adresse_personnelle.ville` | Oui | `DOC-001`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017` |
| 29 | `selarl_denomination` | Denomination | Fiche Societe | Denomination sociale | `Company.denomination` | Oui | `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017`, `DOC-005 si actif` |
| 30 | `selarl_capital_social` | Capital social | Fiche Societe | Montant du capital social | `Company.capital`, `Company.capital_social`, `CapitalContext.montant`, `Apport.montant`, `DepotFonds.montant`, `Associe.apport_numeraire` | Oui | `DOC-002`, `DOC-004`, `DOC-016/017`, `DOC-005 si actif` |
| 31 | `selarl_capital_social_lettres` | Capital social en lettres | Fiche Societe | Capital social en lettres | `Company.capital_social_lettres`, `CapitalContext.montant_lettres`, `Apport.montant_lettres`, `Associe.apport_numeraire_lettres` | Oui | `DOC-004`, `DOC-016/017`, `DOC-005 si actif` |
| 32 | `selarl_nb_parts_total` | Nombre de parts | Fiche Societe | Nombre total de parts | `Company.nb_parts_total`, `CapitalContext.nb_parts_total`, `Associe.nb_parts` | Oui | `DOC-004`, `DOC-016/017` |
| 33 | `selarl_nb_parts_total_lettres` | Nombre de parts en lettres | Fiche Societe | Nombre total de parts en lettres | `CapitalContext.nombre_titres_total_lettres` | Oui | `DOC-016/017` |
| 34 | `selarl_valeur_nominale_part` | Valeur nominale | Fiche Societe | Valeur nominale de la part | `CapitalContext.valeur_nominale_part`, `CapitalContext.valeur_nominale_titre` | Oui | `DOC-004`, `DOC-016/017` |
| 35 | `selarl_valeur_nominale_part_lettres` | Valeur nominale en lettres | Fiche Societe | Valeur nominale en lettres | `CapitalContext.valeur_nominale_titre_lettres` | Oui | `DOC-016/017` |
| 36 | `selarl_duree` | Duree sociale | Fiche Societe | Duree de la societe | `Company.duree` | Oui | `DOC-016/017` |
| 37 | `selarl_ville_rcs` | Ville RCS | Fiche Societe | Ville du RCS | `Company.ville_rcs` | Oui | `DOC-004`, `DOC-016/017` |
| 38 | `selarl_siege_num_voie` | No siege | Siege social | Numero de voie du siege | `Company.siege.num_voie`, `Domiciliation.adresse_domiciliation_affichee` derivee | Oui | `DOC-002`, `DOC-003`, `DOC-004`, `DOC-016/017` |
| 39 | `selarl_siege_voie` | Voie siege | Siege social | Voie du siege | `Company.siege.voie`, `Domiciliation.adresse_domiciliation_affichee` derivee | Oui | `DOC-002`, `DOC-003`, `DOC-004`, `DOC-016/017` |
| 40 | `selarl_siege_cp` | CP siege | Siege social | Code postal du siege | `Company.siege.cp`, `Domiciliation.adresse_domiciliation_affichee` derivee | Oui | `DOC-002`, `DOC-003`, `DOC-004`, `DOC-016/017` |
| 41 | `selarl_siege_ville` | Ville siege | Siege social | Ville du siege | `Company.siege.ville`, `Domiciliation.adresse_domiciliation_affichee` derivee | Oui | `DOC-002`, `DOC-003`, `DOC-004`, `DOC-016/017` |
| 42 | `selarl_ordre_conseil` | Conseil departemental de l'ordre | Ordre et mandataire | Conseil departemental de l'ordre | `OrdreProfessionnel.conseil_departemental_libelle`, `SpfplOrdre.professionnel` | Oui | `DOC-034`, `DOC-016/017` |
| 43 | `selarl_departement_ordre` | Departement d'inscription | Ordre et mandataire | Departement ordinal | `Company.inscription_ordre.departement`, `SpfplOrdre.departement` | Oui | `DOC-016/017` |
| 44 | `selarl_ordre_adresse_ligne_1` | Adresse ordre | Ordre et mandataire | Adresse du conseil de l'ordre | `OrdreAddress.ligne_1` | Oui | `DOC-034` |
| 45 | `selarl_ordre_cp` | CP ordre | Ordre et mandataire | Code postal du conseil de l'ordre | `OrdreAddress.cp` | Oui | `DOC-034` |
| 46 | `selarl_ordre_ville` | Ville ordre | Ordre et mandataire | Ville du conseil de l'ordre | `OrdreAddress.ville`, `Company.inscription_ordre.ville`, `SpfplOrdre.ville` | Oui | `DOC-034`, `DOC-016/017` |
| 47 | `selarl_mandataire_civilite` | Civilite mandataire | Ordre et mandataire | Civilite du mandataire | `Mandataire.civilite_affichage` | Oui | `DOC-034` |
| 48 | `selarl_mandataire_prenom` | Prenom mandataire | Ordre et mandataire | Prenom du mandataire | `Mandataire.prenom` | Oui | `DOC-034` |
| 49 | `selarl_mandataire_nom` | Nom mandataire | Ordre et mandataire | Nom du mandataire | `Mandataire.nom` | Oui | `DOC-034` |
| 50 | `selarl_mandataire_fonction` | Fonction mandataire | Ordre et mandataire | Fonction du mandataire | `Mandataire.fonction` | Oui | `DOC-034` |
| 51 | `selarl_mandataire_cabinet` | Cabinet mandataire | Ordre et mandataire | Cabinet du mandataire | `Mandataire.cabinet` | Oui | `DOC-034` |
| 52 | `selarl_signature_lieu` | Lieu de signature | Generation | Lieu de signature | `Signature.lieu`, `RegimeCommunautaireRenonciation.lieu_signature` | Oui | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017`, `DOC-005 si actif` |
| 53 | `selarl_signature_date` | Date de signature | Generation | Date de signature | `Signature.date`, `RegimeCommunautaireRenonciation.date_signature` | Oui | `DOC-001`, `DOC-002`, `DOC-003`, `DOC-004`, `DOC-034`, `DOC-016/017`, `DOC-005 si actif` |
| 54 | `selarl_signature_nombre_exemplaires` | Nombre d'exemplaires | Generation | Nombre d'exemplaires en lettres | `Signature.nombre_exemplaires`, `DocumentContext.nombre_exemplaires_lettres`, `RegimeCommunautaireRenonciation.nombre_exemplaires_lettres` | Oui | `DOC-004`, `DOC-016/017`, `DOC-005 si actif` |
| 55 | `selarl_decision_date` | Date decision | Generation | Date de decision / PV | `DecisionContext.date` | Oui | `DOC-004` |
| 56 | `selarl_reunion_date_lettres` | Date reunion en lettres | Generation | Date de reunion en lettres | `ReunionContext.date_lettres` | Oui | `DOC-004` |
| 57 | `selarl_reunion_heure` | Heure reunion | Generation | Heure de reunion | `ReunionContext.heure` | Oui | `DOC-004` |
| 58 | `selarl_depot_banque_nom` | Banque depot | Generation | Banque de depot des fonds | `DepotFonds.banque.nom` | Oui | `DOC-016/017` |
| 59 | `selarl_depot_banque_adresse` | Adresse banque | Generation | Adresse de la banque de depot | `DepotFonds.banque.adresse_affichee` | Oui | `DOC-017` surtout, `DOC-016/017` par prudence |
| 60 | `selarl_prestataire_signature_electronique` | Prestataire signature electronique | Generation | Prestataire de signature electronique | `Signature.prestataire_signature_electronique` | Oui | `DOC-016` |
| 61 | `selarl_exercice_debut` | Debut exercice | Generation | Debut d'exercice social | `ExerciceSocial.debut` | Oui | `DOC-016/017` |
| 62 | `selarl_exercice_fin` | Fin exercice | Generation | Fin d'exercice social | `ExerciceSocial.fin` | Oui | `DOC-016/017` |
| 63 | `selarl_exercice_cloture_premier` | Cloture premier exercice | Generation | Cloture du premier exercice | `ExerciceSocial.date_cloture_premier_exercice` | Oui | `DOC-016/017` |
| 64 | `selarl_lieu_exercice_adresse` | Lieu exercice | Generation | Adresse du lieu d'exercice | `ExerciceSocial.lieux[0].adresse_affichee` | Oui | `DOC-016/017` |
| 65 | `selarl_seuil_achat_materiel` | Seuil achat materiel | Generation | Seuil gerance achat materiel | `GeranceContext.seuil_achat_materiel` | Oui | `DOC-017` |
| 66 | `selarl_seuil_emprunt` | Seuil emprunt | Generation | Seuil gerance emprunt | `GeranceContext.seuil_emprunt` | Oui | `DOC-017` |
| 67 | `selarl_conjoint_civilite` | Civilite conjoint | Conjoint | Civilite du conjoint | `SpfplConjoint.civilite_affichage`, `Person.civilite` conjoint | Oui | `DOC-016`, `DOC-005 si actif` |
| 68 | `selarl_conjoint_genre` | Genre conjoint | Conjoint | Genre grammatical du conjoint | `Person.genre` conjoint | Oui | Pas consomme directement par les generateurs SELARL V1 observes |
| 69 | `selarl_conjoint_prenom` | Prenom conjoint | Conjoint | Prenom du conjoint | `SpfplConjoint.prenom`, `Person.prenom` conjoint | Oui | `DOC-016`, `DOC-005 si actif` |
| 70 | `selarl_conjoint_nom` | Nom conjoint | Conjoint | Nom du conjoint | `SpfplConjoint.nom`, `Person.nom` conjoint | Oui | `DOC-016`, `DOC-005 si actif` |
| 71 | `selarl_qualite_renoncee` | Qualite renoncee | Conjoint | Qualite renoncee par le conjoint | `RegimeCommunautaire.qualite_renoncee` | Oui | `DOC-005 si actif` |
| 72 | `selarl_date_courrier_avertissement` | Date courrier avertissement | Conjoint | Date du courrier d'avertissement | `RegimeCommunautaire.date_courrier_avertissement` | Oui | `DOC-005 si actif` |

## Duplications recherchees

### Duplications non detectees

- Meme donnee metier demandee deux fois : non detecte.
- Meme variable canonique collectee dans plusieurs widgets editables : non detecte.
- Libelles differents pour une meme donnee : non detecte.
- Identite praticien / associe / gerant / signataire : une seule saisie, puis derivation.
- Domiciliation : pas de champ separe ; elle est derivee du siege social.
- Apport numeraires / capital : pas de champ separe ; le capital social alimente l'apport.
- Statuts medecin / dentiste : la profession unique pilote le choix documentaire.

### Doublons apparents mais justifies

| Apparence | Analyse |
|---|---|
| `Civilite` et `Genre` | Donnees proches mais distinctes : civilite affichee vs genre grammatical. |
| Adresse personnelle, siege, ordre, banque, lieu exercice | Adresses distinctes par role metier. Les libelles courts `No`, `Voie`, `CP`, `Ville` sont encadres par la section visible. |
| `Departement naissance` et `Departement d'inscription` | L'un decrit l'etat civil, l'autre l'ordre professionnel. |
| `Date de signature`, `Date decision`, `Date reunion en lettres`, `Date courrier avertissement` | Evenements juridiques distincts, malgre des valeurs pouvant coincider. |
| `Capital social`, `Nombre de parts`, `Valeur nominale` | Donnees de capital liees mais non equivalentes. |
| Mandataire et praticien | Roles separes par contrat : le mandataire n'est pas derive du signataire. |

## Points ambigus hors duplication bloquante

1. `selarl_lieu_exercice_adresse` peut etre identique au siege social dans des dossiers simples. Conceptuellement, `lieu_exercice` et `siege_social` restent deux donnees distinctes ; toutefois l'UI actuelle oblige a saisir le lieu d'exercice alors que `build_generation_context()` prevoit un fallback vers le siege. Ce n'est pas une duplication canonique, mais c'est une friction de saisie potentielle.
2. Le bloc `Conjoint` est toujours visible. Les champs conjoint sont ignores hors `profession = chirurgien_dentiste` et hors `regime_communautaire = oui`, sauf affichage. Ce n'est pas une duplication, mais cela expose des champs non requis selon le contexte.
3. `selarl_date_courrier_avertissement` est visible meme quand le regime communautaire est inactif ; la valeur est ensuite forcee a `None`. Champ non duplique, mais conditionnellement inutile.
4. `selarl_seuil_achat_materiel` et `selarl_seuil_emprunt` sont marques par le blocage comme requis "pour les statuts medecin". La validation actuelle les exige aussi lorsque la profession est chirurgien-dentiste. Ce point releve d'une validation trop large, pas d'une duplication de champ.
5. Le contrat mentionne un mandataire requis pour `DOC-003`, mais le generateur actuel de procuration utilise encore ses constantes internes de mandataire. Les champs mandataire du clean front alimentent `DOC-034`. Ce point n'est pas une duplication de saisie, mais une divergence contrat / generateur existant a surveiller hors de ce ticket.
6. `selarl_conjoint_genre` alimente le modele `Person` du conjoint, mais les generateurs SELARL V1 observes consomment surtout civilite, prenom et nom. Champ non duplique ; utilite documentaire directe faible dans le scope actuel.

## Verdict

PASS.

Le clean front ne demande pas deux fois la meme donnee metier de maniere editable.
Les cas proches relevent soit de roles metier distincts, soit de derivations internes,
soit d'ambiguites UX conditionnelles a documenter. Aucun mini-fix n'a ete applique :
le ticket est reste en audit uniquement.
