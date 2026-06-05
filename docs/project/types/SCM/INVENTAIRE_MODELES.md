# SCM — Inventaire des modèles tokenisés (V1)

> **Statut : FONDATION (sources).** Ce document recense les modèles `.docx`/`.doc` réellement
> présents pour le type **SCM** (Société Civile de Moyens). Il décrit **ce que le fichier
> EST** d'après ses variables et son contenu — **PAS** dans quel cas il s'assemble (la carte
> officielle cas → documents est **MANQUANTE**, cf. `CARTOGRAPHIE_TENTATIVE.md`).
> Aucun wording inventé. `dérivé` ≠ `confirmé`.

## Provenance

- **Source Drive (lecture seule) :**
  `C:\Users\Gad\Downloads\Documents avec variables-20260604T122837Z-3-001\Documents avec variables\création scm\`
- **Copiés (NFC, dédupliqués) dans :** `project/source_documents/scm/`
- **11 modèles** copiés (10 `.docx` + 1 `.doc` legacy) + `variables_source_scm.csv` (référence des variables fournie avec le lot Drive).
- **Aucun doublon octet-pour-octet** détecté (hash MD5 distinct sur chaque fichier).
- Tokens extraits par **scan XML complet** (les `[token]` fragmentés sur plusieurs runs sont récupérés ;
  l'extraction paragraphe-par-paragraphe sous-compte — piège connu).

## Tableau modèle → variables tokenisées → nature présumée

| Modèle (nom propre dans `source_documents/scm/`) | Nb tokens | Variables tokenisées | Ce que le document paraît être (1 phrase) |
|---|---|---|---|
| `Statuts SCM.docx` | 38 | `[adresse_banque]`, `[adresse_perso_personne_2]`, `[adresse_siege_societe_1]`, `[apport_lettres_personne_2]`, `[apport_lettres_societe_1]`, `[apport_societe_1]`, `[capital_lettres]`, `[capital_social]`, `[capital_social_societe_1]`, `[civilite_personne_1]`, `[civilite_personne_2]`, `[cp_siege]`, `[date_naissance_personne_2]`, `[denomination_societe]`, `[denomination_societe_1]`, `[denomination_societe_courte]`, `[fonction_personne_1]`, `[forme_sociale]`, `[forme_sociale_societe_1]`, `[lieu_signature]`, `[nationalite_personne_2]`, `[nb_parts]`, `[nb_parts_personne_2]`, `[nom_banque]`, `[nom_personne_1]`, `[nom_personne_2]`, `[num_voie_siege]`, `[numero_rcs_societe_1]`, `[prenom_personne_1]`, `[prenom_personne_2]`, `[profession_personne_2]`, `[profession_societe_1]`, `[situation_maritale_personne_2]`, `[valeur_nominale_part]`, `[ville_naissance_personne_2]`, `[ville_rcs_societe_1]`, `[ville_siege]`, `[voie_siege]` | Statuts constitutifs de la SCM (capital, apports, parts, associés — un associé personne physique + un associé société). |
| `Pacte d_associes SCM.docx` | 16 | `[adresse_siege]`, `[capital_social]`, `[civilite_personne_1]`, `[civilite_personne_2]`, `[date_signature]`, `[denomination_societe]`, `[forme_sociale]`, `[lieu_signature]`, `[nb_parts_sociales]`, `[nom_personne_1]`, `[nom_personne_2]`, `[numero_rcs]`, `[prenom_personne_1]`, `[prenom_personne_2]`, `[ville_rcs]`, `[ville_tribunal]` | Pacte d'associés de la SCM (relations entre deux associés). |
| `Contrat frais communs SCM.docx` | 23 | `[adresse_locaux]`, `[adresse_siege_societe_1]`, `[capital_social_societe_1]`, `[capital_social_societe_2]`, `[civilite_representant_societe_1]`, `[civilite_representant_societe_2]`, `[date_effet_contrat]`, `[date_signature]`, `[denomination_societe_1]`, `[denomination_societe_2]`, `[fonction_representant_societe_1]`, `[fonction_representant_societe_2]`, `[forme_sociale_societe_1]`, `[forme_sociale_societe_2]`, `[lieu_signature]`, `[nom_representant_societe_1]`, `[nom_representant_societe_2]`, `[numero_rcs_societe_1]`, `[numero_rcs_societe_2]`, `[prenom_representant_societe_1]`, `[prenom_representant_societe_2]`, `[ville_rcs_societe_1]`, `[ville_rcs_societe_2]` | Contrat de répartition des frais communs entre deux sociétés (les SEL des associés). |
| `Reglement interieur SCM.docx` | 29 | `[adresse_locaux]`, `[adresse_siege_societe_1]`, `[adresse_siege_societe_2]`, `[annee_reference_charges]`, `[capital_social_societe_1]`, `[capital_social_societe_2]`, `[date_attribution_responsabilites]`, `[date_fin_gestion_administrative]`, `[date_signature]`, `[denomination_societe]`, `[denomination_societe_1]`, `[denomination_societe_2]`, `[fonction_representant_societe_1]`, `[fonction_representant_societe_2]`, `[forme_sociale]`, `[identite_praticien_1]`, `[identite_praticien_2]`, `[identite_representant_societe_1]`, `[identite_representant_societe_2]`, `[lieu_signature]`, `[numero_rcs_societe_1]`, `[numero_rcs_societe_2]`, `[seuil_depense_commune]`, `[telephone_praticien_1]`, `[telephone_praticien_2]`, `[titre_representant_societe_1]`, `[titre_representant_societe_2]`, `[ville_rcs_societe_1]`, `[ville_rcs_societe_2]` | Règlement intérieur de la SCM (répartition des dépenses communes, responsabilités, praticiens). Nom Drive d'origine : « 2024 RÈGLEMENT INTÉRIEUR … SCM DES DOCTEURS XX ». |
| `Liste depenses communes SCM.doc` | n/a | **`.doc` legacy binaire — non lisible par python-docx ; tokens non extraits.** À convertir en `.docx` pour tokenisation. | Liste/tableau des dépenses communes de la SCM (annexe au règlement / contrat frais communs). |
| `Fiche de creation SCM.docx` | 4 | `[capital_social]`, `[date_cloture_exercice]`, `[date_cloture_exercice_1]`, `[forme_sociale]` | Fiche récapitulative de création de la SCM (probable formulaire interne ; très peu de tokens → champs majoritairement libres / cases à cocher). |
| `PV nomination gerant SCM.docx` | 31 | `[adresse_perso_personne_1]`, `[adresse_perso_personne_2]`, `[capital_social]`, `[civilite_personne_1]`, `[civilite_personne_2]`, `[cp_siege]`, `[date_decision]`, `[date_naissance_personne_1]`, `[date_naissance_personne_2]`, `[date_reunion_lettres]`, `[denomination_societe]`, `[denomination_societe_1]`, `[forme_sociale]`, `[lieu_signature]`, `[nationalite_personne_1]`, `[nationalite_personne_2]`, `[nb_parts]`, `[nb_parts_personne_2]`, `[nb_parts_societe_1]`, `[nom_personne_1]`, `[nom_personne_2]`, `[num_voie_siege]`, `[prenom_personne_1]`, `[prenom_personne_2]`, `[profession_personne_1]`, `[profession_personne_2]`, `[valeur_nominale_part]`, `[ville_naissance_personne_1]`, `[ville_naissance_personne_2]`, `[ville_siege]`, `[voie_siege]` | Procès-verbal de nomination du gérant de la SCM. |
| `Autorisation de domiciliation SCM.docx` | 11 | `[capital_social]`, `[civilite]`, `[cp_siege]`, `[date_signature]`, `[denomination_societe]`, `[lieu_signature]`, `[nom]`, `[num_voie_siege]`, `[prenom]`, `[ville_siege]`, `[voie_siege]` | Autorisation de domiciliation du siège de la SCM (modèle commun, repris de la trame SEL). |
| `Declaration non condamnation SCM.docx` | 13 | `[civilite]`, `[cp_perso]`, `[date_naissance]`, `[date_signature]`, `[lieu_signature]`, `[nationalite]`, `[nom]`, `[nom_mere]`, `[nom_pere]`, `[num_voie_perso]`, `[prenom]`, `[ville_perso]`, `[voie_perso]` | Déclaration sur l'honneur de non-condamnation (modèle commun, repris de la trame SEL). |
| `Procuration SCM.docx` | 14 | `[civilite]`, `[cp_perso]`, `[cp_siege]`, `[date_signature]`, `[denomination_societe]`, `[fonction_dirigeant]`, `[nom]`, `[num_voie_perso]`, `[num_voie_siege]`, `[prenom]`, `[ville_perso]`, `[ville_siege]`, `[voie_perso]`, `[voie_siege]` | Procuration (probable mandat aux formalités SYDEL). **Piège** : tokens fragmentés sur runs ; au moins une occurrence `num_voie_siege]` sans crochet ouvrant dans la source — à vérifier. |
| `Avenant contrat de bail SCM.docx` | 29 | `[adresse_bailleur]`, `[adresse_locataire]`, `[adresse_responsable]`, `[adresse_siege]`, `[civilite]`, `[civilite_bailleur]`, `[civilite_locataire]`, `[date_bail]`, `[date_naissance_bailleur]`, `[date_naissance_locataire]`, `[date_signature]`, `[denomination_ancien_locataire]`, `[denomination_societe]`, `[lieu_signature]`, `[nationalite_bailleur]`, `[nationalite_locataire]`, `[nom]`, `[nom_bailleur]`, `[nom_locataire]`, `[nombre_exemplaires]`, `[numero_avenant]`, `[prenom]`, `[prenom_bailleur]`, `[prenom_locataire]`, `[profession_bailleur]`, `[profession_locataire]`, `[signature_bailleur]`, `[ville_naissance_bailleur]`, `[ville_naissance_locataire]` | Avenant au contrat de bail (changement de locataire vers la SCM). Modèle proche de l'avenant de bail SELARL — **à dédoublonner conceptuellement** avec la couche partagée. |

## Notes de fidélité / pièges relevés

1. **`.doc` legacy** (`Liste depenses communes SCM.doc`) : binaire Word 97-2003, non tokenisable par
   python-docx. Une variante `.docx` existe déjà dans `project/source_documents/lot_05/`
   (`Liste dépenses communes SCM.docx`) — **vérifier l'équivalence** avant de retenir l'une ou l'autre.
2. **Tokens fragmentés sur runs** : l'extraction fiable se fait au niveau XML (déjà appliquée ici).
   Toute reconstruction de générateur doit utiliser un remplissage tolérant aux runs scindés.
3. **Modèles « communs »** (`Autorisation de domiciliation`, `Declaration non condamnation`,
   `Procuration`) : ce sont des trames partagées entre types (déjà présentes pour la SELARL dans
   `lot_01`/`lot_02`). **Ne pas dupliquer la couche partagée** — au moment du moteur, réutiliser le
   générateur commun et n'ajouter qu'un mapping SCM si nécessaire.
4. **`variables_source_scm.csv`** (fourni avec le lot Drive) déclare ~165 variables candidates dont
   beaucoup ne sont **pas** présentes dans les 11 modèles ci-dessus : c'est un **dictionnaire
   transverse** (cession, bail, multi-sociétés…), pas la liste effective d'un cas SCM. À traiter comme
   référence, pas comme contrat.
