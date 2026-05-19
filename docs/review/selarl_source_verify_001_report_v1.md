# Rapport SELARL-PILOT-SOURCE-VERIFY-001

## Source V2 lue

- Source réelle lue : `project/source_truth/Documents_a_generer_par_cas_V2.docx`.
- Hash SHA-256 : `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Écart d'entrée constaté : la V2 réelle avait été déposée localement sous `project/source_truth/Documents à générer par cas V2.docx`, tandis que le chemin canonique commité apparaissait supprimé.
- Correction effectuée : le fichier réel a été déplacé vers le chemin canonique demandé, sans modification de son contenu.

## État Git initial

- Branche : `main`.
- Dernier commit présent : `882e62a docs: add selarl pilot protocol and form specs`.
- État initial : `project/source_truth/Documents_a_generer_par_cas_V2.docx` supprimé, `project/source_truth/Documents à générer par cas V2.docx` non suivi, `docs/docssource_truth/` non suivi préexistant.
- Aucun push effectué.

## Synthèse des écarts

La source V2 réelle confirme le cadrage général du pilote SELARL, mais corrige des points importants :

- `Dérogation cumul SELARL BNC` est explicitement `à remplir à la main`.
- Le formulaire multi-sites SEL est mentionné, mais la section variables indique qu'il n'est pas fourni dans les sources.
- `Lettre d'avertissement au conjoint` est indiquée comme absente des sources fournies.
- La V2 fournit de nombreuses variables brutes par document qui devaient être reprises dans les specs pour éviter des regroupements trop génériques.
- Aucun document autonome `PV d'autorisation d'emprunt` n'existe dans la V2.

## Matrice d'écarts

Note de lecture : la colonne `Statut actuel` décrit l'état observé avant les corrections de `SELARL-PILOT-SOURCE-VERIFY-001`. Le statut final corrigé est repris dans `Correction nécessaire` et dans la section `Corrections effectuées`. Pour éviter toute ambiguïté, `DOC-013` et `DOC-014` sont finaux `MANUAL_ONLY` / hors génération automatique dans le pilote SELARL vérifié.

| Élément V2 réel | Présent dans les specs ? | Présent dans case_catalog ? | Statut actuel | Statut attendu selon V2 | Écart identifié | Correction nécessaire | Fichier à corriger |
|---|---|---|---|---|---|---|---|
| Source V2 réelle hash `2E9843...B23F` | Non, l'ancien rapport citait le hash provisoire `47860...ABA5` | Sans objet | Fichier canonique supprimé, fichier accentué non suivi | Fichier réel au chemin canonique | Source vérité V2 précédente non fiable | Remplacer la source canonique par la vraie V2 et documenter le hash | `project/source_truth/Documents_a_generer_par_cas_V2.docx`, `docs/review/selarl_pilot_protocol_001_report_v1.md` |
| Documents dans tous les cas : non-condamnation, domiciliation, procuration | Oui, mais variables trop synthétiques | Oui | Générables | Générables | Variables brutes V2 non toutes reprises | Ajouter la liste des variables V2 brutes | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| PV nomination gérant | Oui, mais variables V2 trop résumées | Oui, `DOC-004` générable | Générable | Générable | Variables source détaillées absentes de la spec | Ajouter les placeholders V2 du PV | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Demande d'inscription à l'ordre | Oui, mais adresse du conseil de l'ordre insuffisamment explicite | Oui, `DOC-034` générable | Générable | Générable | `[adresse_conseil_ordre]`, `[cp_ordre]`, `[ville_ordre]` pas assez qualifiés | Ajouter le champ `Adresse du conseil de l'ordre` | `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Statuts chirurgien-dentiste | Oui, mais variables V2 détaillées absentes | Oui, `DOC-016` générable | Générable | Générable | Manquent notamment lieu d'exercice, banque, exercice social, signature électronique | Ajouter couverture V2 brute | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Statuts médecin | Oui, avec l'anomalie source connue | Oui, `DOC-017` générable | Générable | Générable | Manquent notamment adresse banque, seuils de gérance, exemplaires, signataire | Ajouter couverture V2 brute et champs correspondants | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Site distinct | Oui | Oui, `MANUAL_ONLY` | Manuel | Manuel | Conforme | Aucune correction catalogue | Aucun |
| Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL | Oui, mais présenté comme générable/formulaire à compléter | Avant correction : oui, `DOC-013` générable ; final : `DOC-013` `MANUAL_ONLY` | Avant correction : générable comme formulaire à compléter | Hors génération pilote : non fourni dans les sources variables V2 | Statut trop permissif | Statut final corrigé : manuel / hors génération pilote, visible mais exclu des codes générables | `src/sydel_doc_engine/domain/case_catalog.py`, `tests/unit/test_case_catalog.py`, specs SELARL |
| Dérogation SEL BNC | Oui | Oui, `MANUAL_ONLY` | Manuel | Manuel | Conforme | Aucune correction catalogue | Aucun |
| Dérogation cumul SELARL BNC | Oui, mais présenté comme générable/formulaire à compléter | Avant correction : oui, `DOC-014` générable ; final : `DOC-014` `MANUAL_ONLY` | Avant correction : générable comme formulaire à compléter | Manuel : V2 indique `à remplir à la main` | Statut incompatible avec la V2 | Statut final corrigé : manuel / hors génération pilote, visible mais exclu des codes générables | `src/sydel_doc_engine/domain/case_catalog.py`, `tests/unit/test_case_catalog.py`, specs SELARL |
| Lettre de renonciation conjoint | Oui, variables résumées | Oui, `DOC-005` générable | Générable | Générable | Variables V2 d'apport et conjoint à préciser | Ajouter couverture V2 brute | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Lettre d'avertissement au conjoint | Oui, présentée comme générable sans réserve | Oui, `DOC-006` générable | Générable | Réserve source : la V2 indique que le document ne figure pas parmi les sources fournies | Générabilité affichée sans prudence | Ajouter une réserve explicite dans les specs et futurs tickets UI | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_UI_WIZARD_SPEC_V1.md`, `docs/project/SELARL_IMPLEMENTATION_PLAN_V1.md` |
| SCM cession : PV AGE | Oui, mais variables détaillées absentes | Oui, `DOC-031` générable | Générable | Générable | Parts/personnes/plages et RCS non repris précisément | Ajouter variables V2 brutes et bloc SCM renforcé | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| SCM cession : Courrier SDE | Oui, mais variables détaillées absentes | Oui, `DOC-032` générable | Générable | Générable | `[montant_droits_enregistrement]` non explicite | Ajouter champ `Droits d'enregistrement SCM` | `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| SCM cession : acte de cession parts SCM | Oui, mais variables détaillées absentes | Oui, `DOC-033` générable | Générable | Générable | Adresse cédant, cessionnaire, société cédée, associés SCM et crédit vendeur trop synthétiques | Ajouter champs et variables V2 brutes | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Cession : Avenant contrat de bail | Oui, mais variables résumées | Oui, `DOC-007` générable | Générable | Générable | Adresse bailleur, locataire, dates/conditions du bail à qualifier | Ajouter champs bail détaillés | `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Cession : Appel de fonds SEL | Oui, mais variables résumées | Oui, `DOC-008` générable | Générable | Générable | Destinataire, banque, vendeur, acquéreur et signataire à qualifier | Ajouter couverture V2 brute et réserve de test UI | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Cabinet médical : acte | Oui, mais variables trop synthétiques | Oui, `DOC-009` générable | Générable | Générable | Adresse vendeur/exercice/cabinet, bail, exercices, prix, crédit vendeur, SCM et signatures non repris | Ajouter couverture V2 et champs cession spécialisés | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Cabinet médical : compromis | Oui, mais variables trop synthétiques | Oui, `DOC-010` générable | Générable | Générable | Adresse locaux, prêt, bail, exercices, prix et signatures insuffisamment couverts | Ajouter couverture V2 et champs cession spécialisés | `docs/project/SELARL_PROCESS_SPEC_V1.md`, `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Cabinet dentaire : acte | Oui, mais variables trop synthétiques | Oui, `DOC-011` générable | Générable | Générable | Salariés, précédent propriétaire, bail, prix, date entrée jouissance non repris | Ajouter champs dédiés | `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Cabinet dentaire : compromis | Oui, mais variables trop synthétiques | Oui, `DOC-012` générable | Générable | Générable | Adresse locaux/cabinet, prêt, bail, prix et signatures à préciser | Ajouter champs dédiés | `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| PV d'autorisation d'emprunt | Oui, comme exclusion | Non | Non autonome | Non autonome | Conforme : absent de la V2 | Conserver comme option du PV nomination gérant seulement | Aucun |
| Adresses qualifiées | Oui partiellement | Sans objet | Plusieurs adresses prévues mais liste incomplète | Toutes les adresses V2 doivent être qualifiées | Manquaient conseil de l'ordre, locataire, vendeur, cédant, cessionnaire, lieu d'exercice | Ajouter les adresses qualifiées et champs correspondants | `docs/project/SELARL_FORM_SCHEMA_V1.md` |
| Signataire / associé 1 | Oui | Sans objet | Règle présente | Règle attendue | Conforme | Aucune correction | Aucun |

## Corrections effectuées

- Remplacement de la source V2 canonique par la vraie V2 fournie.
- Correction du statut catalogue :
  - `formulaire_derogation_sites_sel` : `MANUAL_ONLY` pour le pilote vérifié ;
  - `derogation_cumul_selarl_bnc` : `MANUAL_ONLY`.
- Adaptation des tests unitaires du catalogue pour verrouiller ces statuts.
- Mise à jour de la spec processus SELARL avec les statuts V2 corrigés et les variables brutes.
- Mise à jour du schéma formulaire SELARL avec les champs d'adresse et de cession détaillés.
- Mise à jour de la spec wizard et du plan d'implémentation pour exclure `DOC-013` et `DOC-014` de la génération SELARL pilote.
- Mise à jour du rapport précédent pour signaler que son hash source était provisoire.

## Points d'ambiguïté restants

- `DOC-006` existe côté moteur, mais la vraie V2 indique que la lettre d'avertissement conjoint ne figure pas parmi les sources fournies. Le futur ticket UI doit l'afficher avec réserve ou demander arbitrage.
- `DOC-013` existe côté moteur, mais la vraie V2 ne fournit pas les variables du formulaire multi-sites ; il reste hors génération pilote tant qu'un juriste ne valide pas le préremplissage.
- Les variables de cession cabinet sont nombreuses et document par document ; le futur ticket formulaire doit éviter de les exposer toutes d'un coup sans regroupement métier.

## Impact sur les futurs tickets UI

- `SELARL-FORM-SCHEMA-IMPL-001` doit traiter `DOC-013` et `DOC-014` comme documents manuels / hors génération pilote.
- L'écran Documents attendus doit afficher la réserve source sur `DOC-006`.
- Les blocs d'adresse doivent utiliser des labels qualifiés, notamment conseil de l'ordre, vendeur, cabinet, locaux, bailleur, locataire, cédant et cessionnaire.
- Les tests UI doivent vérifier l'absence de `DOC-013` et `DOC-014` dans les codes générables SELARL quand `derogation = true`.

## Tests lancés

- `.\.venv\Scripts\python.exe -m ruff check .`
- `.\.venv\Scripts\python.exe -m pytest`

Résultats :

- Ruff : OK, `All checks passed!`
- Pytest : OK, 217 tests passés.

## Prochaine étape recommandée

Après cette réconciliation, reprendre `SELARL-FORM-SCHEMA-IMPL-001` en tenant compte des statuts V2 corrigés et de la réserve sur `DOC-006`.
