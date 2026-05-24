# FRONT-ADDRESS-MODEL-001 - Rapport V1

## Perimetre

Ce ticket raffine la couche data du futur front global pour les adresses metier. Il ne
modifie ni l'UI visible, ni Streamlit, ni les generateurs, ni le moteur DOCX/PDF/ZIP.

## Sources utilisees

- `docs/review/front_data_layer_001_report_v1.md`
- `docs/review/front_role_model_001_report_v1.md`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`
- `docs/review/global_human_answers_integration_001_report_v1.md`
- `project/source_truth/albane_reponse_mail_selarl_v1.md`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/canonical_mapping.py`
- `src/sydel_doc_engine/front_data/validation.py`
- `src/sydel_doc_engine/front_data/role_model.py`
- `tests/unit/test_front_data_layer.py`
- `tests/unit/test_front_role_model.py`

ADR applicables : ADR-0001 source de verite documentaire et ADR-0005 mode de
travail Codex/repo-first.

## Objets et modules ajoutes

- `AddressDisplaySource` dans `models.py` pour tracer la provenance de la forme
  affichee : saisie manuelle, composants, regle de reutilisation, alias documentaire
  ou override.
- Champs `display_source`, `display_source_rule_id` et `display_override_reason`
  sur `AddressRecord`.
- `address_model.py` avec :
  - definitions d'usages d'adresse ;
  - politiques de reutilisation explicites ;
  - parsing de refs `address:*` ;
  - composition d'adresse affichee depuis les composants ;
  - helpers de verification forme affichee / composants.
- Validations adresse dediees via `validate_address_records`.

## Decisions de modelisation d'adresse

Une adresse reste un objet metier type par usage. Deux adresses identiques en texte
ne sont pas fusionnees si leurs usages different.

Usages couverts explicitement :

- `domicile_praticien`
- `adresse_personnelle`
- `lieu_exercice`
- `siege_social`
- `domiciliation`
- `cabinet_cede`
- `locaux_loues`
- `bailleur`
- `locataire`
- `banque`
- `ordre`
- `scm`
- `scm_cedee`
- `cessionnaire_scm`
- `societe_cible`
- `spfpl`

`domicile_cedant` reste conserve car les checks sentinelles l'utilisent pour les
cessions, avec reutilisation possible depuis `domicile_praticien` seulement via
regle explicite.

## Regles explicites

| Regle | Representation | Statut |
|---|---|---|
| `domiciliation = siege_social` | `address:siege_social -> address:domiciliation` | regle forte, mais activee et tracee |
| `siege_social = lieu_exercice` | `address:lieu_exercice -> address:siege_social` | jamais implicite |
| `scm = lieu_exercice` | `address:lieu_exercice -> address:scm` | standard, mais tracee |
| `scm_cedee != cessionnaire_scm` | pas de disponibilite sans adresse ou regle active | distinct par defaut |
| `cabinet_cede = lieu_exercice` | regle possible pour cession cabinet | explicite |
| `locaux_loues = lieu_exercice` | regle possible pour bail standard | explicite |

## Reutilisations permises

Les reutilisations permises sont encodees dans `ADDRESS_REUSE_POLICIES`. Elles
sont toutes `EXPLICIT_REUSE_ONLY` pour eviter toute propagation silencieuse.

Reutilisations encodees :

- siege social vers domiciliation ;
- lieu d'exercice vers siege social ;
- lieu d'exercice vers SCM ;
- lieu d'exercice vers cabinet cede ;
- lieu d'exercice vers locaux loues ;
- domicile praticien vers domicile cedant ;
- SCM cedee vers cessionnaire SCM, uniquement apres confirmation.

## Reutilisations interdites

Sont bloquees par validation :

- reutilisation d'une relation `DISTINCT_FIELDS` ;
- reutilisation implicite entre deux usages d'adresse distincts ;
- reutilisation entre deux usages sans politique enregistree ;
- deux sources actives concurrentes sur la meme adresse cible sans override ;
- adresse derivee sans source explicite ;
- override affiche sans valeur ou sans raison ;
- adresse attachee au mauvais type de partie, par exemple adresse de banque sur une
  personne physique.

## Formes agregees et decomposees

Le modele conserve une seule adresse metier, avec plusieurs formes possibles :

- composants : `street_number`, `street_name`, `postal_code`, `city`, `country` ;
- forme affichee : `display_value` ;
- source de la forme affichee : `display_source` ;
- trace de derivation : `display_source_rule_id` ;
- override documentaire : `display_source=OVERRIDE`, `display_override_reason`.

Si la forme affichee est derivee des composants, la derivation doit etre tracee.
Si un document legacy exige une ponctuation ou une casse particuliere, l'override
reste possible sans creer de nouveau champ metier concurrent.

## Mapping canonique

`canonical_mapping.py` expose maintenant des chemins plus explicites pour :

- adresse personnelle rolee et composants ;
- domicile du praticien ;
- siege social role et composants ;
- domiciliation affichee et composants ;
- lieu d'exercice principal et composants ;
- adresse ordre affichee et composants ;
- adresse banque ;
- adresse cabinet cede et composants ;
- adresses bailleur, locataire et locaux loues ;
- adresses SCM, SCM cedee, cessionnaire SCM ;
- adresses SPFPL et societe cible.

Les alias legacy restent traites comme formes documentaires. Par exemple
`domiciliation.adresse_domiciliation_affichee` reste un alias documentaire vers
`domiciliation.adresse`, pas un nouveau champ metier.

Point de vigilance : les placeholders `personne.{role}.*` et `societe.{role}.*`
restent volontiers generiques. Le mapping adresse ajoute des sous-chemins rolees,
mais ne cree aucun role par defaut. Le futur front devra toujours resoudre le role
avant de presenter ou reutiliser une adresse.

## Impacts sur les sentinelles

| Document | Impact adresse | Verdict adresse |
|---|---|---|
| DOC-002 | domiciliation couverte via regle explicite depuis siege ; alias affiche conserve comme forme documentaire | VERT |
| DOC-034 | adresse ordre mappee en forme affichee et composants | VERT adresse, reste ORANGE produit sur mandataire/derogation |
| DOC-017 | siege, adresse personnelle et banque restent explicites | ORANGE hors adresse sur capital/seuils |
| DOC-033 | domicile cedant, cessionnaire SCM et SCM cedee restent distincts par defaut | VERT |
| DOC-009 | cabinet, locaux, bailleur, locataire, siege et banque sont maintenant portables par la data layer | ORANGE hors adresse sur origine/bail/exercices |
| DOC-041 | SPFPL et societe cible ont des adresses dediees | ORANGE hors adresse sur apport_titres/evaluateur/commissaire |
| DOC-025 | SCM peut reutiliser le lieu d'exercice via regle tracee ; banque et siege restent explicites | ORANGE hors adresse sur associes/parts/apports |

## Ce qui reste ORANGE

- Modele dossier complet : les adresses sont pretes, mais le flow multi-operation
  doit encore orchestrer quand proposer les reutilisations.
- Bail / cession cabinet : les adresses sont explicites, mais origine, exercices,
  clauses bail et financement restent a structurer dans le flow dossier.
- Capital, titres, apports et associes SCM restent hors perimetre adresse.
- Les valeurs par defaut de banque/ordre ne doivent pas devenir des constantes
  magiques dans la data layer.

## Prototype actuel

- Garde : outil de diagnostic et bac a sable local.
- Jette : modele de saisie comme fondation produit.
- Migre : uniquement les enseignements de test et de diagnostic utiles.
- Diagnostic seul : les parcours Streamlit existants, qui ne doivent pas piloter
  le nouveau modele d'adresse.

## Validations

Validations executees :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 313 tests passes.

## Prochaine etape recommandee

Lancer `FRONT-DOSSIER-FLOW-001` pour definir le flow dossier complet global sur
la base de la data layer, des roles explicites et des adresses typees. Le ticket
devra rester hors UI visible tant que le flow produit n'est pas stabilise.
