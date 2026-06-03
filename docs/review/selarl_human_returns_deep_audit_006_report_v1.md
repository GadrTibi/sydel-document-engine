# SELARL human returns deep audit 006 report V1

Ticket : `SELARL-HUMAN-RETURNS-DEEP-AUDIT-006`

Date : 2026-06-02

## Amendement 2026-06-03

Ce rapport est historique. Il a ete depasse par :

- `docs/review/selarl_returns_006_incident_generalized_audit_001_report_v1.md`

L'audit incident a trouve un ecart qui n'etait pas detecte ici :

- `DOC-002` autorisation de domiciliation rendait encore
  `pour une duree indeterminee`.

Correction appliquee le 2026-06-03 :

- `DOC-002` rend maintenant `pour 99 ans` ;
- le pack 005 local a ete regenere ;
- la regression SELARL ciblee affiche 187 tests passes.

Sources :

- `docs/review/selarl_human_returns_006_raw_v1.md`
- `docs/review/selarl_human_returns_triage_006_report_v1.md`
- `artifacts/selarl_closing_pack_005/`
- `artifacts/selarl_closing_pack_005/manifest_selarl_closing_pack_005.json`

## Verdict

Verdict historique : `DEPASSE - ecart DOC-002 trouve ensuite et corrige`.

Les retours humains 006 sont traites dans le pack 005 selon les controles
manifest et les tests cibles.

Ce rapport ne doit plus etre utilise comme feu vert autonome. Le verdict actif
est celui de l'audit incident du 2026-06-03, qui corrige `DOC-002` puis
revalide la regression SELARL ciblee.

## Controle par retour

| Retour | Statut pack 005 | Preuve |
| --- | --- | --- |
| R006-01 statuts clause matrimoniale | OK | Manifest : clause communaute dans scenarios regime |
| R006-02 article 8 accord associe | OK | Manifest : accord `associee unique` ; tests statuts OK |
| R006-03 annexe page suivante | OK | Tests statuts SEL existants OK |
| R006-04 tiret `Ouverture...` | OK | Tests statuts SEL existants OK |
| R006-05 DNC ville naissance | OK | Manifest : naissance avec ville |
| R006-06 option `au` ville naissance | OK code/test | Tests DNC/front OK ; pack 005 utilise le cas standard `a Lyon` |
| R006-07 PV forme juridique redigee | OK | Manifest : forme juridique redigee |
| R006-08 PV capital | OK | Manifest : `Au capital de 10 000 euros` |
| R006-09 adresses CP avant ville | OK | Manifest : aucun `Paris 750...` / `Lyon 690...` |
| R006-10 suppression encadres signature | OK | Manifest : signatures non encadrees `DOC-001` / `DOC-002` / `DOC-003` |
| R006-11 Ordre profession + departement | OK | Manifest : conseil compose depuis profession + departement |
| R006-12 `DOC-006` forme juridique redigee | OK | Manifest + pack regime |
| R006-13 adresse conjoint = associe | OK | Manifest : ancienne adresse conjoint absente, adresse associe presente |
| R006-14 `DOC-005` date sous ville retiree | OK | Manifest : pas de date sous ville avant objet |
| R006-15 duree sociale 99 ans | OK | Tests front/statuts OK |
| R006-16 siege identique adresse personnelle | OK | Tests front OK ; pack 005 utilise siege = adresse personnelle |
| R006-17 nationalite portugaise | OK code/test | Tests front OK |
| R006-18 nombre d'exemplaires = 4 | OK | Manifest : `DOC-006` quatre exemplaires ; tests front/regime OK |
| R006-19 qualite renoncee = associe | OK | Tests front/regime OK |
| R006-20 date courrier = jour | OK code/test | Tests front OK ; pack 005 derive les dates runtime |
| R006-21 procuration `agissant` | OK | Manifest : `demeurant..., agissant...` |

## Ecarts trouves puis corriges pendant audit

- `DOC-006` : `Fait en trois exemplaires` restait dans le premier pack 005 genere ; corrige en quatre exemplaires.
- `DOC-016` dentiste : l'accord autour de `associe unique` n'etait pas verrouille pour l'associee feminine ; corrige et teste.

## Validations

- Manifest pack 005 : 4 scenarios, 0 echec.
- Tests statuts/regime : 25 passes.
- Regression SELARL large : 166 passes.
- Ruff cible SELARL 006 : OK.

## Questions humaines

Aucune question humaine n'est necessaire pour ces retours 006 : les retours
sont suffisamment explicites et les ecarts trouves ont ete corriges.

## Suite

Prochain ticket recommande : `SELARL-FINAL-ASSOCIE-VALIDATION-001`.

Instruction associe : tester le pack 005 et remonter uniquement des ecarts
concrets document par document.
