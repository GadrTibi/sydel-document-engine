# CASE-CATALOG-001 - rapport V1

## Source analysée
- Source demandée : `docs/source_truth/documents_a_generer_par_cas_v1.md` ou `docs/source_truth/Documents à générer par cas.docx`.
- Source effectivement présente et analysée : `project/source_truth/Documents_a_generer_par_cas.docx`.
- ADR applicable : `docs/adr/0001-source-of-truth.md`.
- Le chemin `docs/source_truth/` n'existe pas dans ce workspace ; la source Word canonique du dépôt a donc été utilisée.

## Familles modélisées
- SELARL
- SELAS
- SPFPL cession
- SPFPL apport
- SCS
- SCI, avec variante `sci_iris`
- SCM
- SAS

## Conditions modélisées
- `profession = medecin`
- `profession = chirurgien_dentiste`
- `site_distinct = true`
- `scm = true`
- `scm_cession = true`
- `regime_communautaire = true`
- `derogation = true`
- `cession = true`
- `cabinet_type = medical`
- `cabinet_type = dentaire`
- `associe_unique = true / false`
- `sci_iris = true / false`
- `option_is = true`
- `cession_actions = true / false`

## Résultat de modélisation
- Documents attendus uniques dans le catalogue métier : 46.
- Occurrences source modélisées : 104.
- Documents mappés à un `DOC-XXX` existant : 43.
- Documents générables : 43.
- Documents manuels : 2.
- Documents non encore implémentés : 1.
- Documents en `NEEDS_MAPPING` : 0.

## Documents générables
Tous les 43 documents du registre moteur actuel sont représentés dans le catalogue métier :

| Code | Document |
|---|---|
| DOC-001 | Déclaration sur l'honneur de non-condamnation |
| DOC-002 | Autorisation de domiciliation |
| DOC-003 | Procuration |
| DOC-004 | PV nomination gérant |
| DOC-005 | Lettre de renonciation à revendiquer la qualité d'associé |
| DOC-006 | Lettre d'avertissement au conjoint en cas d'apport d'un bien commun |
| DOC-007 | Avenant contrat de bail |
| DOC-008 | Appel de fonds SEL |
| DOC-009 | Acte de cession d'un cabinet médical |
| DOC-010 | Compromis de cession d'un cabinet médical |
| DOC-011 | Acte de cession d'un cabinet dentaire |
| DOC-012 | Compromis de cession d'un cabinet dentaire |
| DOC-013 | Formulaire de dérogation pour exercer sur plusieurs sites avec la SEL |
| DOC-014 | Demande de dérogation cumul SELARL BNC |
| DOC-015 | Statuts SAS / SPFPL médecins |
| DOC-016 | Statuts SELARL chirurgien-dentiste |
| DOC-017 | Statuts SELARL médecin |
| DOC-018 | Statuts SELAS médecin |
| DOC-019 | Statuts SCS |
| DOC-020 | Statuts SCI |
| DOC-021 | Statuts SCI IRIS |
| DOC-022 | Lettre option IS |
| DOC-023 | PV rémunération président |
| DOC-024 | Attestation sur le capital / liste des souscripteurs SAS |
| DOC-025 | Statuts SCM |
| DOC-026 | Pacte d'associés SCM |
| DOC-027 | Contrat d'exercice professionnel à frais communs |
| DOC-028 | Règlement intérieur de la SCM |
| DOC-029 | Acte de cession d'actions SPFPL |
| DOC-030 | Liste dépenses communes SCM |
| DOC-031 | PV AGE cession part SCM |
| DOC-032 | Courrier SDE cession SCM |
| DOC-033 | Acte de cession des parts de la SCM vers SEL |
| DOC-034 | Demande d'inscription à l'ordre |
| DOC-035 | Statuts SPFPL cession |
| DOC-036 | Statuts SPFPL apport |
| DOC-037 | Note d'information SPFPL |
| DOC-038 | PV agrément cession SPFPL - associé unique |
| DOC-039 | PV agrément cession SPFPL - plusieurs associés |
| DOC-040 | Acte de cession de parts SPFPL |
| DOC-041 | Contrat d'apport SEL vers SPFPL |
| DOC-042 | Attestation sur le capital / liste des souscripteurs SPFPL |
| DOC-043 | Attestation nomination commissaire aux apports |

## Documents manuels
| Document | Condition | Statut |
|---|---|---|
| Formulaire de déclaration préalable de site distinct CD94 avec la SEL | SELARL + `site_distinct = true` | `MANUAL_ONLY` |
| Dérogation SEL BNC | SELARL + `derogation = true` | `MANUAL_ONLY` |

Ces documents ne sont pas présentés comme générables par `get_expected_documents(...)`.

## Documents non encore implémentés
| Document | Condition | Statut | Note |
|---|---|---|---|
| Demande de dérogation cumul SELARL salariée | SELAS + `derogation = true` | `NOT_IMPLEMENTED` | Source legacy `.doc`, conversion DOCX propre non disponible dans le moteur V1. |

## Ambiguïtés de mapping
Aucune occurrence n'est restée en `NEEDS_MAPPING`.

Points de vigilance documentés dans le catalogue :
- La ligne SELARL `Si médecin` contient un libellé source incohérent `Statuts dentiste`; le fichier source pointe bien vers le modèle médecins et le mapping retenu est `DOC-017`.
- La ligne SPFPL apport parle de `comm. aux comptes`, tandis que le fichier et le registre parlent de commissaire aux apports ; le mapping retenu est `DOC-043`.
- `Liste dépenses communes SCM` est listé en `.doc` dans la source vérité, mais le registre moteur utilise la source DOCX convertie sous `DOC-030`.
- `Acte de cession d'actions` est sans nom de fichier complet dans l'extraction Word ; le registre moteur expose le document sous `DOC-029`.

## Prochaines décisions métier nécessaires
- Décider si les documents `MANUAL_ONLY` doivent rester hors génération produit ou devenir des formulaires préremplis dans une phase ultérieure.
- Fournir ou convertir une source DOCX propre pour `Demande_derogation_cumul_SELARL_salariee.doc` avant toute automatisation.
- Décider comment le futur assistant métier doit demander les conditions `scm`, `scm_cession`, `cession_actions` et `cabinet_type`.
- Décider si `get_expected_documents(...)` devient la source de sélection produit de l'UI métier ou reste un service d'audit tant que l'orchestrateur historique pilote la génération.

## Validation
- Tests ciblés ajoutés : `tests/unit/test_case_catalog.py`.
- Le test de mapping vérifie que les 43 documents générables correspondent exactement aux 43 `DOC-XXX` du registre actuel.
- Aucun wording juridique source n'a été réécrit.
