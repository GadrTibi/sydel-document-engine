# Matrice de parité — tous types vs gold SELARL

> Worklist déterministe (workflows `wbrfu8vl3` + `wg19zsrm6`, 2026-06-19). Gold = SELARL.
> Légende : `OK` présent · `~` partiel · `X` absent · `J` différence justifiée (ne pas toucher).
> Méthode : [METHODE_PARITE_GOLD.md](METHODE_PARITE_GOLD.md). Retours : [retours/REGISTRE_RETOURS.md](retours/REGISTRE_RETOURS.md).

| Commodité | SELARL (gold) | SELAS pluri | SAS | SPFPL | Civils (SCI/SCM/SCS/IRIS) | SELAS uni méd. |
|---|---|---|---|---|---|---|
| date_picker_today | ~ | ~ | ~ | ~ | ~ | X |
| nominal_value_readonly | OK | OK | OK | OK | OK | OK |
| siège=adresse_checkbox | OK | X | X | X | X | X |
| second_lieu_exercice (MOTEUR) | OK | X(m) | X(m) | X(m) | X(m) | X(front*) |
| auto_closing_date (31 déc N+1) | ~ | X | X | X | X | X |
| capital_number_input_grouped | ~ | X | X | X | X | X |
| field_example_hints | ~ | n/a | ~ | ~ | X | ~ |
| lieu_signature=ville_siège | OK | X | X | X | OK (+fort) | X |
| exercice_dates_prefilled | OK | X | X | X | J (moteur) | X |
| mandataire_editable | OK | X | X | X | X | X |
| nationalite_dropdown | OK | OK | X | X | OK | OK |
| madame_la_presidente | OK | X | J (pas d'ordre) | X | X (SCM only) | X |

**Cause racine confirmée (5 audits)** : chaque slice réimplémente ses helpers de rendu (`_t/_i/_date`) au lieu de consommer la couche partagée → date_picker amputé partout + absence en cascade des commodités front-pur.

## Plan d'exécution (vagues)
- **VAGUE 0 — couche partagée** (`front_widgets.py`, prérequis) : helper date ✅ déjà extrait ; ajouter text/int avec `help=`, `capital_input`, `siege_same_as_personal`, `mandataire_inputs`, seeders (exercice/clôture/lieu signature), `ordre_president_feminin_toggle` ; déplacer `render_nationalite_selectbox` ici. **SELARL byte-identique** + 1 test unitaire/helper. Aucun slice modifié → risque doc nul.
- **VAGUE 1 — consommer le helper date** : les 5 slices pointent sur `front_widgets.date_input_with_today`, suppression des `_date` locaux. Ferme date_picker_today partout.
- **VAGUE 2 — commodités sans impact moteur** : brancher par type nationalité, capital, siège=adresse, mandataire, lieu_signature, exercice_dates, auto_closing. Respecter les `J`.
- **VAGUE 3 — madame_la_presidente** : toggle + mapping (SELAS uni/pluri, SPFPL) ; SCM = champ féminin dans `OrdreInput` + `cc.ordre_professionnel`. Pas SAS.
- **VAGUE 4 — second_lieu (MOTEUR, séparé)** : SELAS uni = front-pur (mapper 2 champs) ; SAS/SPFPL = ticket moteur ; Civils = moteur + **GO Albane**.

## Différences justifiées (NE PAS toucher)
- SAS / madame_la_presidente : pas d'`OrdreProfessionnel` dans le bundle SAS.
- Civils / lieu_signature : champ supprimé (§18.4), repris auto de `siege_ville` — plus fort que le gold.
- Civils / exercice_dates : `StatutsCivilsContext` n'expose pas début/fin.
- nominal_value_readonly : déjà conforme partout (champ disabled, plus strict que la caption gold).

## Question métier (flag, pas build)
**second_lieu pour Civils (SCI/SCM/SCS) + SPFPL holding** : une civile/holding peut-elle légitimement porter un 2e lieu d'exercice, ou est-ce une différence justifiée par la forme ? → **Albane**. Ne pas deviner.

## Anomalies documents (hors parité UX)
- **ANO-008** : DOC-008 (appel de fonds) au plan SELAS mais jamais généré (gate moteur SELARL-only) → aligner plan/génération.
- **ANO-045** : DOC-045 (attestation capital SELAS) au case_catalog canon (« modèle Albane 2026-06-17 ») mais absent de `SELAS_BUNDLE_CODES` → câbler au bundle.
