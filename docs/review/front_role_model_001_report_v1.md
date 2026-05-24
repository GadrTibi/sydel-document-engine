# Rapport FRONT-ROLE-MODEL-001

Date : 2026-05-24

## 1. Sources utilisees

- `docs/review/front_data_layer_001_report_v1.md`
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md`
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md`
- `docs/project/GLOBAL_FRONT_RULES_V1.md`
- `docs/project/GLOBAL_FRONT_SENTINEL_CHECKS_V1.csv`
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md`
- `src/sydel_doc_engine/front_data/models.py`
- `src/sydel_doc_engine/front_data/canonical_mapping.py`
- `src/sydel_doc_engine/front_data/validation.py`
- `tests/unit/test_front_data_layer.py`

## 2. Objets et regles ajoutes

Module cree :

- `src/sydel_doc_engine/front_data/role_model.py`

Ajouts principaux :

- `RoleFamily` pour classer les roles : identite personne, gouvernance,
  execution documentaire, partie d'operation, representation, tiers de controle,
  societe d'operation, institution, finance.
- `RoleDefinition` pour declarer cible, portee par defaut, portees autorisees,
  reutilisation par defaut, representation et tiers de controle.
- `RoleReusePolicy` pour limiter les reutilisations de roles a des cas documentes.
- `OrderRoleModel` pour sortir le modele ordre d'un pseudo-role entreprise.
- Helpers `assign_explicit_role`, `role_ref`, `parse_role_ref`,
  `role_from_canonical_path`, `role_placeholder_is_generic`.

`RoleAssignment` porte maintenant aussi :

- `represented_target_type`
- `represented_target_id`
- `represented_role`

Ces champs servent a tracer qu'un representant personne morale represente une
societe existante, sans fusionner la personne physique et la personne morale.

## 3. Decisions sur la portee des roles

Portee dossier :

- `praticien`, `gerant`, `president`, `societe_principale`, `banque` quand ils
  structurent tout le dossier.

Portee operation :

- `associe`, `vendeur`, `cedant`, `acquereur`, `cessionnaire`, `apporteur`,
  `bailleur`, `locataire`, `societe_cible`, `societe_apportee`,
  `spfpl_beneficiaire`, `scm`, `scm_cedee`, `ordre_professionnel`.

Portee document :

- `signataire`, `mandataire`, `representant_personne_morale` quand le document
  exige un intervenant local.

Portee lot :

- reservee aux roles d'execution documentaire reutilises pour un lot, notamment
  `signataire`, avec regle explicite.

Regle retenue :

- un role dont la portee naturelle est document ou operation ne devient pas global
  au dossier sans declaration explicite ;
- une reutilisation de role n'efface jamais les deux `RoleAssignment`.

## 4. Modele ordre

Le modele ordre est represente comme un faisceau de roles :

- inscrit personne physique : `signataire` du document ordinal ;
- societe inscrite : `societe_principale` ou societe rolee selon operation ;
- conseil de l'ordre : `ordre_professionnel`, cible `CompanyRecord` institution ;
- mandataire : `mandataire`, distinct du signataire.

Champs canoniques relies :

- `personne.{role}.numero_rpps`
- `personne.{role}.numero_ordre`
- `personne.{role}.profession`
- `ordre.adresse`
- `ordre.professionnel`

Decision :

- `ordre_professionnel` n'est pas l'inscrit ;
- `ordre_professionnel` n'est pas la societe inscrite ;
- le mandataire reste un role separe, configurable, sans valeur magique.

## 5. Signataire, mandataire, representant, commissaire

Distinctions testees :

- `mandataire != signataire` par defaut ;
- `representant_personne_morale != societe representee` ;
- `commissaire_aux_apports` et `evaluateur_apport` sont des tiers de controle,
  distincts des parties a l'operation ;
- un representant personne morale doit pointer vers une societe existante ;
- une reutilisation implicite `mandataire -> signataire` est bloquee.

## 6. Placeholders `{role}`

Les definitions generiques suivantes ne portent plus de role par defaut :

- `personne.{role}.*`
- `societe.{role}.*`

Un placeholder reste utile pour decrire une famille de champs, mais il ne cree
ni `praticien`, ni `societe_principale`, ni fusion silencieuse. Le role concret
doit venir d'un `RoleAssignment`.

## 7. Impacts sentinelles

| Document | Impact role model |
|---|---|
| `DOC-034` | Couverture renforcee : inscrit, societe inscrite, ordre, mandataire separes. |
| `DOC-041` | Couverture renforcee : apporteur, SPFPL, societe cible, evaluateur, commissaire distincts. |
| `DOC-033` | Couverture renforcee : cedant, cessionnaire, SCM cedee, representant cessionnaire distincts. |

Les autres sentinelles conservent leur couverture data-layer precedente.

## 8. Points encore ORANGE

- Le modele ordre est structure, mais le parametrage par profession/departement
  ordinal reste a affiner avec les ecrans et validations futures.
- Les roles de bailleur/locataire restent ouverts pour les cas ou la partie peut
  etre personne physique ou personne morale.
- Les calculs capital/titres/apports ne sont pas traites dans ce ticket.
- Les adresses typees et leurs reutilisations fines restent le prochain chantier.
- Aucun wording juridique ni generateur n'a ete modifie.

## 9. Tests

Tests ajoutes :

- `tests/unit/test_front_role_model.py`

Validation cible executee pendant le ticket :

- `.\.venv\Scripts\python.exe -m pytest tests/unit/test_front_role_model.py tests/unit/test_front_data_layer.py`
  : OK, 26 tests passes.

Validation finale :

- `.\.venv\Scripts\python.exe -m ruff check .` : OK.
- `.\.venv\Scripts\python.exe -m pytest` : OK, 298 tests passes.

## 10. Prochaine etape recommandee

Lancer `FRONT-ADDRESS-MODEL-001`.

La prochaine couche doit raffiner les adresses typees et les reutilisations :
domiciliation/siege, siege/lieu d'exercice, cabinet/locaux loues, SCM/SCM cedee,
cessionnaire SCM, ordre et banque.
