# Rapport SELARL-PILOT-PROTOCOL-001

## Source analysée

- Source V2 cible ajoutée : `project/source_truth/Documents_a_generer_par_cas_V2.docx`.
- Provenance locale utilisée : `docs/docssource_truth/Documents à générer par cas.docx`, fichier non suivi présent avant intervention.
- Hash SHA-256 V2 : `47860BBDD3997B1D35AC3F4833D6D5B650E35BCF2EA4C2B40952919FF6D4ABA5`.
- Correction postérieure : `SELARL-PILOT-SOURCE-VERIFY-001` a remplacé ce fichier provisoire par la vraie V2 fournie par l'associé, hash SHA-256 `2E9843AA1EC05A01D82DF5FCE12516A8EF49EA2B3842547D186204218C90B23F`.
- Source V1 de comparaison : `project/source_truth/Documents_a_generer_par_cas.docx`.
- Fichiers projet lus : `case_catalog.py`, rapport `CASE-CATALOG-001`, `business_wizard.py`, docs UI `19/20/21`, specs delivery liées à SELARL.

## État Git initial

- Branche : `main`.
- HEAD initial : `71efbae feat: connect business wizard to case catalog`.
- `git status` initial : working tree non strictement clean à cause de `docs/docssource_truth/`.
- `CASE-CATALOG-001` présent via le commit `7ee6d4f feat: add case document catalog v1` et son rapport.
- `UI-CASE-WIZARD-002` déjà terminé sur `main` via `71efbae`; modifications listées dans `docs/review/ui_case_wizard_002_report_v1.md`.
- Recommandation sur `UI-CASE-WIZARD-002` : ne pas poursuivre directement `UI-CASE-WIZARD-003` générique ; lancer d'abord le ticket ciblé SELARL issu du présent protocole.

## Fichiers créés

- `project/source_truth/Documents_a_generer_par_cas_V2.docx`
- `docs/project/PROCESS_BUILD_PROTOCOL_V1.md`
- `docs/project/SELARL_PROCESS_SPEC_V1.md`
- `docs/project/SELARL_FORM_SCHEMA_V1.md`
- `docs/project/SELARL_UI_WIZARD_SPEC_V1.md`
- `docs/project/SELARL_IMPLEMENTATION_PLAN_V1.md`
- `docs/review/selarl_pilot_protocol_001_report_v1.md`

## Décisions produit prises

- Le pilote SELARL doit partir des choix métier : profession, site distinct, SCM cession, régime communautaire, dérogation, cession, type de cabinet.
- Le formulaire cible est structuré par blocs métier, pas par document ni par variable brute.
- Le libellé SELARL cible est `Gérant / professionnel principal`.
- Aucun champ UI cible ne doit s'appeler seulement `adresse`.
- Les documents manuels restent visibles et exclus de la génération.
- Le `PV d'autorisation d'emprunt` ne doit pas apparaître comme document autonome dans le flux SELARL pilote ; l'emprunt reste une branche conditionnelle du `DOC-004`.

## Points d'ambiguïté

- La source V2 contient une ambiguïté de libellé autour de la ligne statuts médecin ; le fichier source vise le modèle médecins, mais la validation juriste reste recommandée.
- Le formulaire site distinct CD94 est manuel dans le catalogue ; une future phase devra décider s'il devient préremplissable.
- Point corrigé par `SELARL-PILOT-SOURCE-VERIFY-001` : dans la vraie V2, `DOC-013` ne fournit pas de variables exploitables pour le pilote et `DOC-014` est indiqué à remplir à la main ; ils ne doivent donc pas être générés dans le flux SELARL pilote sans arbitrage.
- L'appel de fonds SEL est présent dans le bloc cession ; son périmètre exact doit rester aligné avec les arbitrages déjà documentés.

## Retours utilisateur intégrés

- Signataire / associé 1 : ajout d'une règle de réutilisation et d'une proposition de case à cocher.
- `Dirigeant / pharmacien` : wording remplacé dans la cible SELARL par `Gérant / professionnel principal`.
- Champ `adresse` ambigu : règle explicite d'interdiction et liste des adresses qualifiées.
- PV d'autorisation d'emprunt : vérification source/catalogue/UI/specs et décision de ne pas créer de document autonome.

## Hors périmètre respecté

- Aucun fichier applicatif Python modifié.
- Aucun générateur modifié.
- Aucun moteur DOCX/PDF/ZIP modifié.
- Aucune formulation juridique source modifiée.
- Aucun nouveau worktree créé.
- Aucun push effectué.

## Tests lancés

- `.\.venv\Scripts\python.exe -m ruff check .`
- `.\.venv\Scripts\python.exe -m pytest`

## Résultats

- Ruff : OK, `All checks passed!`
- Pytest : OK, 217 tests passés.

## Prochaine étape recommandée

Lancer `SELARL-FORM-SCHEMA-IMPL-001` pour implémenter le schéma de formulaire SELARL côté Assistant métier, avec un scope limité aux champs et validations de formulaire, sans modifier les générateurs ni le moteur documentaire.
