# SELARL returns 006 incident generalized audit 001 report V1

Date : 2026-06-03

Ticket : `SELARL-RETURNS-006-INCIDENT-GENERALIZED-AUDIT-001`

Demande : Gad demande si les exemples donnes par l'associe signalent seulement
des cas ponctuels ou un probleme general de propagation des retours humains 006.

## Verdict

Verdict initial de l'audit : `PARTIAL`.

Verdict apres correction : `PASS - candidat validation associe`.

Conclusion PM : le retour de l'associe etait fonde sur au moins deux points :

- l'adresse conjoint avait ete corrigee dans le rendu `DOC-006`, mais pas dans
  toutes les branches front/schema ;
- l'autorisation de domiciliation `DOC-002` contenait encore
  `pour une duree indeterminee` alors que le retour associe demandait `pour
  99 ans`.

Ces deux points sont maintenant corriges dans le code actif et couverts par des
tests. Il ne faut pas presenter cela comme une garantie juridique absolue de
100 %. Il est propre de le presenter comme une version candidate de validation
associe, avec demande d'ecarts concrets.

## Cause racine

La cause n'etait pas un manque d'information metier.

La cause etait une propagation incomplete :

- certains tickets ont corrige le generateur ou le pack, mais pas toutes les
  surfaces front/schema ;
- le retour `duree = 99 ans` avait ete interprete comme `duree sociale` et
  variables front/statuts, sans etre applique a la phrase de domiciliation
  deja signalee par l'associe ;
- certains rapports `DONE` etaient trop confiants et ne distinguaient pas assez
  `sortie document`, `champ front`, `schema`, `tests` et `pack actif`.

## Corrections appliquees pendant cet audit

| Point | Avant | Apres | Preuve |
| --- | --- | --- | --- |
| `DOC-002` autorisation de domiciliation | `pour une duree indeterminee` | `pour 99 ans` | generateur + test `test_autorisation_domiciliation_contains_essential_texts` |
| Pack actif local | `DOC-002` ancien wording dans les DOCX existants | pack 005 regenere localement avec `doc002_duration_99_years=true` | `artifacts/selarl_closing_pack_005/manifest_selarl_closing_pack_005.json` |
| Adresse conjoint front | champ pouvait survivre dans des branches front/schema | aucune saisie adresse conjoint dans clean front / assistant metier SELARL ; adresse derivee | `selarl_returns_006_conjoint_address_front_lock_001_report_v1.md` + tests anti-regression |

## Controle des exemples associe

| Exemple associe | Statut actuel | Commentaire |
| --- | --- | --- |
| Retirer les blocs de signature | `OK` | Les tables encadrees restantes du pack sont des titres, pas des signatures. Les signatures `DOC-001`, `DOC-002`, `DOC-003` sont non encadrees. |
| Autorisation de domiciliation : remplacer `duree indeterminee` par `99 ans` | `CORRIGE MAINTENANT` | C'etait un vrai manque. Le generateur et le test ont ete corriges. |
| Adresse conjoint identique a l'associe, supprimer la saisie interface | `OK APRES INCIDENT` | C'etait un vrai manque precedent. La correction front/schema est maintenant appliquee. |

Point de vigilance : le texte `duree indeterminee` existe encore dans les PV de
nomination gerant, mais il vise la duree du mandat de gerant. Ce n'est pas la
duree de domiciliation ni la duree sociale. Il ne doit pas etre modifie sans
retour humain explicite sur le `DOC-004`.

## Revue des retours humains 006

| Retour | Statut | Preuve principale |
| --- | --- | --- |
| Statuts : mention communaute / separation de biens | `OK` | tests statuts + pack regime communautaire |
| Statuts : accord `associe` genre/nombre | `OK` | tests statuts ; pack actuel male rend `associe unique`, tests couvrent aussi l'accord |
| Statuts : annexe page suivante | `OK` | tests statuts |
| Statuts : tiret devant `Ouverture...` | `OK` | pack statuts contient `- Ouverture...` |
| DNC : ville de naissance avec `a/au` | `OK` | tests DNC + front + single document |
| PV : forme juridique redigee | `OK` | tests PV + manifest |
| PV : `Au capital de {capital social}` | `OK` | tests PV + manifest |
| Adresses CP avant ville | `OK` | tests adresses + manifest |
| Signatures sans encadre | `OK` | tests DOC-001/002/003 + audit tables signature |
| Ordre : conseil compose depuis profession + departement | `OK` | tests ordre + manifest |
| Lettre avertissement conjoint : forme juridique redigee | `OK` | tests regime + manifest |
| Lettre avertissement conjoint : adresse conjoint derivee | `OK` | tests front/schema + manifest |
| Lettre renonciation : date sous ville retiree | `OK` | tests regime + manifest |
| Variables front : duree sociale cachee / 99 ans | `OK` | tests front + derivation clean front |
| Siege social identique adresse personnelle | `OK` | front simple + tests de derivation |
| Nationalite portugaise | `OK` | test clean front |
| Nombre d'exemplaires cache / 4 | `OK` | tests front + manifest `DOC-006` |
| Qualite renoncee cachee / associe | `OK` | tests front + contexte regime |
| Date courrier derivee du jour | `OK` | tests front + contexte regime |
| Procuration : `demeurant..., agissant...` | `OK` | tests procuration + manifest |
| DOC-002 : domiciliation `pour 99 ans` | `CORRIGE MAINTENANT` | test DOC-002 + manifest |

## Validations executees

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_autorisation_domiciliation.py -q`
  : OK, 8 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_autorisation_domiciliation.py tests/unit/test_clean_front_app.py::test_clean_front_selarl_generation_smoke tests/unit/test_clean_front_app.py::test_clean_front_selarl_medecin_regime_communautaire_generation_smoke -q`
  : OK, 10 tests passes.
- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_demande_inscription_ordre.py tests/unit/test_clean_front_app.py tests/unit/test_front_generation_actions.py tests/unit/test_front_dossier_data_entry.py tests/unit/test_business_wizard.py tests/unit/test_single_document_mode.py tests/unit/test_lot_04_statuts_sel_exercice.py tests/unit/test_pv_nomination_gerant.py tests/unit/test_declaration_non_condamnation.py tests/unit/test_autorisation_domiciliation.py tests/unit/test_procuration.py tests/unit/test_regime_communautaire.py tests/unit/test_selarl_form_schema.py -q`
  : OK, 187 tests passes.
- `.\.venv\Scripts\python.exe -m ruff check ...` sur les fichiers touches :
  OK.

Manifest local pack 005 :

- 4 scenarios ;
- 6 / 6 / 8 / 8 DOCX ;
- 0 controle en echec ;
- `doc002_duration_99_years=true` pour les 4 scenarios.

## Risques restants

- Les artefacts `artifacts/` sont ignores par Git. La correction fiable a
  pousser est donc le code generateur + tests + docs, pas seulement les DOCX
  locaux.
- Les anciens rapports historiques peuvent encore contenir les anciens textes
  comme references de source ou historique. Ils ne doivent pas etre lus comme
  etat actif sans `04_LAST_STATE.md`.
- Le sprint SELARL simple/regime reste `PARTIAL` tant que l'associe n'a pas
  valide la version candidate ou retourne des ecarts concrets.

## Decision

Action recommandee : faire tester cette version par l'associe comme candidat de
validation, en demandant uniquement :

```text
Dis-moi les ecarts concrets restants document par document, ou valide le
perimetre simple/regime.
```

Ne pas affirmer que la SELARL globale tous cas confondus est terminee.
