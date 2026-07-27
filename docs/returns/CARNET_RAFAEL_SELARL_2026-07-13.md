# Retours Rafael — SELARL (2026-07-13)

Source : Rafael (relais des retours). Verbatim = spec.

| # | Retour | Type | État |
|---|--------|------|------|
| R1 | 2ème lieu d'exercice : pourquoi le champ « Nom du 2e lieu d'exercice » existe ? | question/UI | à investiguer |
| R2 | Tous les champs « Civilité » = menu déroulant (Madame / Monsieur) | UI cohérence | à faire |
| R3 | Tous les champs « Situation matrimoniale » = même menu déroulant ; l'identité du conjoint n'est demandée QUE quand la situation s'y prête (marié/pacsé). Notamment situation matrimoniale du VENDEUR (SELARL cession de fonds libéral). | UI cohérence + conditionnel | à faire |
| R4 | Front créé/acheté : fautes d'orthographe « cabinet cree par le vendeur » → « créé », « cabinet achete par le vendeur » → « acheté ». | UI accents | à faire |
| R5 | Acte de cession de cabinet MÉDICAL : « né(e) le » ne s'adapte pas à la civilité. Homme connu → « né » (femme → « née »). | générateur accord genre | à faire |

## Analyse
- **R2/R3** : le praticien PRINCIPAL a déjà le bon pattern (menu `MATRIMONIAL_STATUS_PRESETS` + conjoint conditionnel `is_married_or_pacse` + `derive_gender_from_civilite`, shell.py ~468-510). Incohérence dans les SOUS-FORMULAIRES : vendeur cession distinct (civilité + situation LIBRES l.1292/1316, conjoint TOUJOURS affiché l.1330, `genre: None`) et associé (situation libre l.350). → propager le pattern canonique.
- **Bonus R2** : civilité vendeur en menu → **dériver le genre** (Madame/Monsieur) → résout R5 pour un vendeur distinct ET comble le trou R4 (genre vendeur non capturé).
- **R4** : piège — le mapping `"achete" in mode_label` casse avec l'accent (« acheté » ne contient pas « achete ») → fixer options + mapping + seeds (`_dev_fixtures`, `_seed_default`) ensemble.
- **R5** : modèle médical fige « né(e) le » (inclusif) ; résoudre au genre du vendeur (né/née) via remplacement token-level run-safe.
