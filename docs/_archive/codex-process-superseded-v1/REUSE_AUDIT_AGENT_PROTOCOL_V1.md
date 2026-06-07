# Reuse audit agent protocol V1

Date : 2026-06-01

## Objet

Ce document definit le sous-agent specialise `Reuse Auditor`.

Son role est de proteger le projet contre le travail refait inutilement quand un
nouveau sprint de type d'entreprise demarre. Il doit chercher ce qui existe deja
cote SELARL et dans les registres globaux, puis dire ce qui peut etre reutilise,
adapte ou bloque.

## Decision produit

Avant tout nouveau sprint :

`Audit reuse obligatoire avant GO dev`

Le sprint ne peut pas passer en implementation tant que les documents, variables,
conditions, helpers, generateurs, tests et mappings deja disponibles n'ont pas
ete compares au besoin du nouveau type d'entreprise.

## Role du sous-agent

Nom recommande :

```text
Reuse Auditor
```

Mission :

1. reperer les documents deja traites dans la SELARL ;
2. reperer les variables deja normalisees ;
3. reperer les conditions metier deja codees ou documentees ;
4. reperer les generateurs, helpers, tests et mappings reutilisables ;
5. classer chaque element en decision simple ;
6. signaler les points qui demandent NotebookLM, Gad, Naomi ou l'associe.

Le sous-agent travaille en lecture seule tant qu'un ticket de modification
precis n'a pas ete ouvert.

Regle issue de la SELARL : le sous-agent doit distinguer ce qui est reutilisable
par preuve de ce qui est seulement similaire. Il ne doit pas transformer un
retour humain SELARL en regle globale sans verifier la source du nouveau type
d'entreprise.

## Sources obligatoires du sous-agent

Le sous-agent doit lire au minimum :

- `AGENTS.md` ;
- `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` ;
- `docs/project/SELARL_CANONICAL_STATUS_V1.md` ;
- `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md` ;
- `docs/project/SELARL_PRODUCTION_FACTORY_V1.md` ;
- `docs/project/TRACK_B_SELARL_FRONT_CONTRACT_V1.md` ;
- `docs/project/TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md` ;
- `docs/project/SELARL_HUMAN_REFERENCE_LOCK_V1.md` ;
- `docs/project/GLOBAL_VARIABLE_IDENTITY_MATRIX_V1.csv` ;
- `docs/project/GLOBAL_VARIABLE_RAW_INVENTORY_V1.csv` ;
- `docs/project/GLOBAL_CANONICAL_FIELD_REGISTRY_V2_1.md` ;
- `docs/project/08_DICTIONNAIRE_VARIABLES_CANONIQUES_V1.md` ;
- `docs/project/09_TABLE_MAPPING_DOCUMENTS_VARIABLES_V1.md` ;
- `docs/project/GLOBAL_FRONT_OBJECT_MODEL_V1.md` ;
- `docs/project/GLOBAL_FRONT_RULES_V1.md` ;
- `docs/project/GLOBAL_FRONT_ARCHITECTURE_V1.md` ;
- `docs/project/FRONT_MIGRATION_MAP_V1.md` ;
- `docs/project/GLOBAL_FRONT_REBUILD_BACKLOG_V1.md` ;
- les specs pertinentes dans `docs/delivery/` ;
- les rapports pertinents dans `docs/review/` ;
- le catalogue et le registre moteur dans `src/` si le sprint passe vers le code.

## Matrice de decision obligatoire

Le sous-agent doit produire une matrice de ce format :

| Element | Source existante | Usage nouveau sprint | Conditions identiques ? | Variables identiques ? | Decision | Risque | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DOC-XXX / variable / helper | chemin | cas cible | oui/non/a verifier | oui/non/a verifier | identique / reuse-check / adapter / no-go | faible/moyen/fort | prochaine action |

La matrice doit aussi indiquer, dans les notes du sprint, si la preuve vient :

- d'une source juridique ou spec ;
- de NotebookLM / modele ;
- d'un retour humain ;
- du code existant seulement.

Le code existant seul ne suffit jamais a classer `identique`.

## Decisions possibles

### `identique`

L'element peut etre reutilise tel quel.

Conditions :

- meme source juridique ou source compatible ;
- memes variables canoniques ;
- memes conditions d'apparition ;
- aucun wording juridique a modifier.

### `reuse-check`

L'element semble reutilisable, mais exige une verification.

Exemples :

- meme document, mais forme sociale differente ;
- variable identique en apparence, mais role metier different ;
- condition semblable, mais exception possible ;
- source NotebookLM ou retour humain a confirmer.

### `adapter`

L'element existant doit etre adapte.

Exemples :

- helper technique reutilisable, wording different ;
- meme role front, mais libelle ou obligation differente ;
- meme document canonique, mais overlay par profession ou forme sociale ;
- tests existants reutilisables avec nouveaux fixtures.

### `no-go`

L'element ne doit pas etre reutilise pour le moment.

Exemples :

- source manquante ;
- document manuel ;
- wording sensible non valide ;
- conditions contradictoires ;
- risque de fusionner deux roles distincts ;
- scope du sprint trop large.

## Questions humaines et reuse

Le `Reuse Auditor` ne doit pas demander a Gad ou a l'associe de confirmer un
element deja prouve par source/spec. Il doit noter la decision et passer a la
suite.

Il doit demander une validation humaine seulement si :

- deux sources se contredisent ;
- la source du nouveau type manque ;
- le meme nom cache un role different ;
- le wording devrait changer ;
- le retour humain SELARL semble non transposable ;
- un document genere montre un ecart concret.

## Questions NotebookLM specifiques reuse

En plus des questions du playbook, poser :

1. Pour le type d'entreprise cible, quels documents sont strictement identiques a ceux deja traites en SELARL ?
2. Quels documents ont le meme nom mais des conditions differentes ?
3. Quelles variables ont le meme libelle mais ne representent pas le meme role ?
4. Quelles variables SELARL peuvent etre reutilisees sans changement ?
5. Quelles variables SELARL doivent etre renommees, separees ou bloquees ?
6. Quels documents SELARL ne doivent jamais etre reutilises pour ce type ?
7. Quels tests SELARL couvrent deja un comportement commun ?
8. Quels retours humains SELARL sont reutilisables, et lesquels sont propres a la SELARL ?
9. Quels cas doivent rester `NO-GO dev` malgre une apparente similarite ?
10. Quel est le plus petit ticket reutilisable sans risque ?

## Sortie attendue avant GO dev

Avant le premier ticket code du sprint, il faut produire :

- une matrice de reuse ;
- une liste `reutiliser tel quel` ;
- une liste `reutiliser apres verification` ;
- une liste `adapter` ;
- une liste `ne pas reutiliser` ;
- les questions ouvertes ;
- le premier ticket `GO dev` borne, ou la decision `NO-GO dev`.

## Classifications variables a respecter

Quand l'audit touche les variables, le sous-agent doit reutiliser les
classifications globales existantes :

- `SAME_FIELD` ;
- `SAME_DATA_DIFFERENT_SHAPE` ;
- `EXPLICIT_REUSE_ONLY` ;
- `DISTINCT_FIELDS` ;
- `UNCERTAIN_REQUIRES_HUMAN_DECISION`.

Regle : pas de fusion silencieuse des roles, personnes ou adresses. Une
reutilisation implicite n'est acceptable que si elle est deja prevue par source,
spec ou decision humaine.

## Socles techniques a verifier avant duplication

Avant de creer un nouveau modele, helper ou test, verifier notamment :

- `src/sydel_doc_engine/front_data/` ;
- `src/sydel_doc_engine/domain/case_catalog.py` ;
- `src/sydel_doc_engine/registry/catalog.py` ;
- `src/sydel_doc_engine/orchestrator/service.py` ;
- `src/sydel_doc_engine/app/ui_runtime.py` ;
- `tests/unit/test_front_data_layer.py` ;
- `tests/unit/test_front_role_model.py` ;
- `tests/unit/test_front_address_model.py` ;
- `tests/unit/test_front_dossier_flow.py` ;
- `tests/unit/test_front_document_status_layer.py` ;
- `tests/unit/test_front_generation_actions.py` ;
- `tests/unit/test_clean_front_app.py` ;
- `tests/unit/test_orchestrator_service.py` ;
- `tests/unit/test_registry_seed.py`.

Les adaptateurs SELARL peuvent servir de patrons de structure, mais jamais de
source de verite globale :

- `src/sydel_doc_engine/app/front_selarl_complete.py` ;
- `src/sydel_doc_engine/app/front_generation_actions.py` ;
- `src/sydel_doc_engine/front_app/selarl_slice.py`.

## Integration dans le sprint Naomi

Quand Naomi ouvre un sprint, Codex doit lancer ou jouer ce role avant le plan de
dev.

Si l'environnement permet les sous-agents, Codex lance un sous-agent
`Reuse Auditor` en lecture seule.

Si l'environnement ne permet pas les sous-agents, Codex execute lui-meme ce
protocole et ecrit la meme matrice dans le sprint plan.

## Garde-fous

- Le code existant n'est pas une source juridique.
- La SELARL sert de methode et de base de reutilisation, pas de preuve que tout
  vaut pour les autres formes.
- Une variable avec le meme nom peut cacher un role different.
- Une condition qui semble identique doit etre confirmee par source ou retour
  humain.
- Aucun wording juridique ne doit etre generalise sans validation.
- Reutiliser veut dire reduire le risque, pas accelerer au prix du metier.
