# Rapport exécutif — GLOBAL-VARIABLE-INVENTORY-001

## Synthèse
- Inventaire CSV : `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv`
- Nombre total de lignes de variables brutes : 12443
- Nombre de slugs normalisés distincts sur documents `DOC-XXX` : 1334
- Nombre de documents `DOC-XXX` couverts : 43
- Nombre de familles documentaires couvertes : 15
- Lignes `GLOBAL` de référentiel hors document : 64

## Couverture documentaire
- Documents couverts : DOC-001, DOC-002, DOC-003, DOC-004, DOC-005, DOC-006, DOC-007, DOC-008, DOC-009, DOC-010, DOC-011, DOC-012, DOC-013, DOC-014, DOC-015, DOC-016, DOC-017, DOC-018, DOC-019, DOC-020, DOC-021, DOC-022, DOC-023, DOC-024, DOC-025, DOC-026, DOC-027, DOC-028, DOC-029, DOC-030, DOC-031, DOC-032, DOC-033, DOC-034, DOC-035, DOC-036, DOC-037, DOC-038, DOC-039, DOC-040, DOC-041, DOC-042, DOC-043
- Documents `DOC-001` à `DOC-043` sans ligne inventoriée : aucun
- Documents hors plage `DOC-001` à `DOC-043` : aucun

## Familles couvertes
- SCM cession : 1184 lignes
- SPFPL spécifique : 3827 lignes
- acte de cession d'actions : 280 lignes
- bail / appel de fonds : 439 lignes
- cession cabinets : 1867 lignes
- dérogations : 353 lignes
- documents communs : 707 lignes
- ordre : 155 lignes
- régime communautaire : 448 lignes
- satellites SAS : 369 lignes
- satellites SCM : 566 lignes
- statuts SAS : 160 lignes
- statuts SEL : 776 lignes
- statuts SPFPL : 463 lignes
- statuts civils : 785 lignes

## Sources exploitées
- `template_docx` : 1483 lignes
- `source_truth_v1` : 0 lignes
- `source_truth_v2` : 512 lignes
- `source_truth_v3` : 512 lignes
- `spec_delivery` : 9260 lignes
- `code_mapping` : 667 lignes
- `legacy_source` : 9 lignes

Note source : `source_truth_v1` ne contient pas de placeholders variables extractibles ; il reste la source métier de cas/documents, mais n'ajoute pas de ligne variable brute dans ce CSV.

## Formes probables
- `atomic` : 5747 lignes
- `composite` : 1127 lignes
- `boolean` : 189 lignes
- `free_text` : 102 lignes
- `date` : 962 lignes
- `amount` : 3271 lignes
- `list_repeated` : 1045 lignes

## Variables les plus fréquentes
- `[lieu_signature]` / slug `lieu_signature` : 131 lignes source
- `[date_signature]` / slug `date_signature` : 123 lignes source
- `[denomination_societe]` / slug `denomination_societe` : 119 lignes source
- `[nom]` / slug `nom` : 100 lignes source
- `[prenom]` / slug `prenom` : 100 lignes source
- `dossier.structure` / slug `dossier_structure` : 94 lignes source
- `signature.lieu` / slug `signature_lieu` : 93 lignes source
- `signature.date` / slug `signature_date` : 92 lignes source
- `[capital_social]` / slug `capital_social` : 86 lignes source
- `[adresse_siege]` / slug `adresse_siege` : 78 lignes source
- `[civilite]` / slug `civilite` : 73 lignes source
- `[forme_sociale]` / slug `forme_sociale` : 67 lignes source
- `[valeur_nominale_part]` / slug `valeur_nominale_part` : 62 lignes source
- `associes[]` / slug `associes_list` : 61 lignes source
- `[nombre_exemplaires_lettres]` / slug `nombre_exemplaires_lettres` : 55 lignes source
- `societe.denomination` / slug `societe_denomination` : 50 lignes source
- `[nom_personne_2]` / slug `nom_personne_2` : 50 lignes source
- `[prenom_personne_2]` / slug `prenom_personne_2` : 50 lignes source
- `[adresse_personnelle]` / slug `adresse_personnelle` : 49 lignes source
- `[ville_siege]` / slug `ville_siege` : 48 lignes source

## Principaux groupes suspects repérés
- Personnes indexées / rôles locaux : 679 lignes, 90 slugs, 29 documents
- Adresses et sièges : 1843 lignes, 201 slugs, 43 documents
- Signature et dates : 382 lignes, 17 slugs, 43 documents
- Capital, parts, actions, apports : 2954 lignes, 325 slugs, 38 documents
- Cession : vendeur / cédant / acquéreur / cessionnaire : 1847 lignes, 180 slugs, 21 documents
- Ordre professionnel / RPPS : 656 lignes, 70 slugs, 24 documents

Ces groupes sont des regroupements suspects pour audit, pas des décisions de fusion. Les variantes locales restent distinctes dans le CSV.

## Principaux risques visibles
- Les alias `personne_1`, `personne_2`, etc. coexistent avec des rôles métier (`associes[]`, `signataire`, `dirigeant_nomine`) : risque de doublons UI si le V2 ne tranche pas par rôle.
- Les adresses sont parfois composites (`[adresse_siege]`) et parfois atomisées (`[num_voie_siege]`, `[voie_siege]`, `[cp_siege]`, `[ville_siege]`) : risque de perte d'identité sémantique ou de double saisie.
- Les rôles de cession (`vendeur`, `cedant`, `acquereur`, `cessionnaire`, `societe_cedee`) doivent être audités document par document avant toute fusion.
- Plusieurs sources sont des specs de niveaux différents (cadrage, arbitrage, spec texte, spec canonique) : elles exposent des intentions et des réserves, pas toutes des champs runtime validés.
- Le document `DOC-023` est couvert par specs/source truth/code mapping, mais son template n'est pas présent dans `project/source_documents/` au même titre que les autres sources.
- Le legacy `.doc` `Liste dépenses communes SCM.doc` n'a pas été parsé directement ; les variables `legacy_source` reflètent le DOCX converti homonyme.

## Qualité des sources
- `template_docx` : meilleure source brute pour placeholders présents physiquement dans les templates, mais certains templates contiennent des variantes historiques ou des placeholders locaux.
- `source_truth_v1` : source métier de référence pour le périmètre documentaire, sans variables brutes extractibles.
- `source_truth_v2` / `source_truth_v3` : sources riches pour l'inventaire SELARL/global, utiles pour audit, à ne pas traiter comme fusion canonique définitive.
- `spec_delivery` : source riche mais hétérogène ; elle mélange variables brutes, variables canoniques, packs et décisions de blocage.
- `code_mapping` : utile pour rattacher les documents aux packs canoniques V1 et aux conditions moteur ; ce n'est pas une source brute de wording juridique.
- `legacy_source` : couverture minimale prudente, avec note explicite lorsque l'extraction directe du `.doc` n'est pas fiable.

## Prochaines étapes recommandées
1. Construire un registre V2 de candidats canoniques par groupe suspect, en conservant les liens vers toutes les lignes brutes du CSV.
2. Valider avec un juriste les rôles métier avant toute fusion (`personne_*`, `signataire`, `dirigeant`, `associe`, `cedant`, `vendeur`, `acquereur`).
3. Décider une politique globale pour adresses composites vs atomisées avant le rebuild front.
4. Produire une matrice V2 `variable_canonique -> raw_variables -> documents -> source_origin` avant toute modification UI.
5. Recontrôler les sources manquantes ou legacy, notamment `DOC-023` et les `.doc` historiques, avant d'en faire des champs front obligatoires.
