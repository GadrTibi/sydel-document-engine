# Registre des golden blocs (composants partagés)

> **But** (Gad 2026-06-23) : un retour universel se traite UNE fois, au niveau du bloc partagé, et
> se propage à tous les cas. Ce registre dit **où vit chaque bloc** et **qui l'utilise** — pour
> changer au bon endroit (et connaître le blast radius) au lieu de copier-coller par type.
> Loi : un golden bloc est **appelé comme un service** (avec un préfixe/contexte), **jamais copié**.
> Règle de propagation = Q4 du triage (`docs/returns/METHODE.md`, règle 68).

## 1. Blocs partagés (appelés, pas copiés) — à modifier ICI pour propager

| Bloc | Fichier:rôle | Appelé par (blast radius) | Note |
|---|---|---|---|
| **Sous-formulaire CESSION** | `front_app/shell.py` `_render_cession_form(prefix=…)` | flux SELARL (dans shell) + `selas_multi_slice` (prefix='selas') | acte/compromis cabinet + bail ; le `prefix` adapte le wording. Tout retour cession = ici. |
| **Sous-formulaire CESSION SCM** | `front_app/shell.py` `_render_scm_cession_form(prefix=…)` | SELARL + `selas_multi_slice` | cession de parts SCM. |
| **Tronc commun (codes docs)** | `front_app/common_creation.py` `TRONC_COMMUN_CODES` (DNC/domiciliation/procuration) | `selarl`, `sas`, `spfpl`, `civil_statuts`, `selas_uni`, `selas_multi` | ajouter/retirer un doc de création commun = ici, couvre 6 types. |
| **Nommage DNC par dirigeant** (O24-02) | `app/ui_runtime.py` `rename_dnc_with_signataire(paths, ctx)` | `selarl`, `sas`, `spfpl`, `civil_statuts`, `selas_uni` (SELAS multi = sa propre logique 1 DNC/dirigeant) | renomme la DNC avec le nom du signataire. |
| **Filtre annexe « frais cabinet »** (O24-01) | `generators/lot_04/annexe_filter.py` `is_creation_fee_annexe_line(text)` | 3 boucles de rendu : `statuts_civils_common`, `statuts_scm`, `statuts_selas_multi` | exclut les 2 items Sydel de l'annexe de TOUS les statuts ; détection par structure. |
| **Génération documents** | `app/ui_runtime.py` `generate_docx_files_for_document_codes(ctx, dir, codes)` | tous les `generate_dossier` de type | point d'entrée unique de génération. |
| **Dérivations de champ** | `front_app/field_derivations.py` `calculate_nominal_value`, `MATRIMONIAL_STATUS_PRESETS`, `regime_communautaire_from_status`, `_MONTHS` (mois accentués sortie), `derive_gender_from_civilite` | tous les slices | valeurs/règles transverses. |
| **Helpers de saisie partagés** | `front_app/front_widgets.py` `seed_siege_from_perso`, `siege_same_as_perso_checkbox`, `seed_closing_date`, `seed_exercice_dates`, `seed_signature_lieu` | tous les slices | pré-remplissages gold. |

## 2. Dettes (COPIÉ par type — à extraire en golden bloc)

Ces concepts sont **dupliqués** : un retour universel les touchant exige N éditions (cause des défauts O24-01/03/05 ratés au premier passage). À extraire quand on y retouche.

| Concept dupliqué | Où (copies) | Risque | Cible |
|---|---|---|---|
| **Bloc adresse UI** (No/Voie/CP/Ville → une ligne, O24-03) | `selarl`, `sas`, `spfpl`, `civil_statuts`, `selas_uni` (chaque slice a ses 4 champs) ; SELAS = déjà sur une ligne via `_parse_address_full` | O24-03 propagé SELAS-only ; les autres types gardent 4 champs | extraire `render_one_line_address()` + `parse_address_full` partagés, appelés partout (propagation Q4). |
| **`_add_rendered_paragraph`** (rendu paragraphe statuts) | copié dans `statuts_civils_common`, `statuts_selas_multi`, `statuts_scm` | un filtre commun (ex. annexe) doit être recâblé 3× | unifier la primitive de rendu. |
| **Modèles `.docx` source** | un par type dans `project/source_documents/lot_04/` | une suppression d'annexe (O24-01) = N modèles ; on a préféré filtrer au rendu (golden bloc) | privilégier le **filtre au rendu** (cf. `annexe_filter`) plutôt que d'éditer N modèles. |
| **Affichage valeur nominale** (O24-05) | text_input désactivé recopié dans 6 slices/zones | un changement de patron = 6 éditions | candidat à un helper `render_valeur_nominale_field()`. |

## 3. Méthode

- **Retour universel** → le traiter au **bloc partagé** (§1). S'il n'existe pas encore, **l'extraire** d'abord (§2), puis traiter une fois.
- **Avant de coder un retour** : chercher ici si un bloc partagé le porte déjà (sinon = dette à extraire).
- **Vérification** : Akainu régénère TOUS les types concernés (pas seulement celui testé) — un retour « tous les cas » se prouve sur tous les cas.
