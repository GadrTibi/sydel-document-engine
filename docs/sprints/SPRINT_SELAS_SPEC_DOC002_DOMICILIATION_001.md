# SELAS spec DOC002 domiciliation 001

Date : 2026-06-02

Ticket : `SELAS-SPEC-DOC002-DOMICILIATION-001`

Statut : `DONE - spec documentaire`

Decision sprint : `NO-GO pack SELAS`

## Objet

Verrouiller la reutilisation SELAS du document canonique :

```text
DOC-002 - Autorisation de domiciliation
```

Cette spec prepare un futur ticket de code borne, sans generer de DOCX SELAS,
sans modifier le wording juridique et sans activer le pack SELAS.

## Perimetre

Inclus :

- SELAS medecin ;
- actionnaire unique ;
- president unique ;
- creation simple ;
- domiciliation au siege/cabinet ;
- document `DOC-002` existant comme base de reutilisation.

Exclus :

- domiciliation distincte du siege/cabinet sans arbitrage explicite ;
- multi-actionnaires ;
- directeur general ;
- cession de fonds ;
- SCM ;
- site distinct ou derogation ;
- changement de wording juridique.

## Sources lues

- `AGENTS.md` ;
- `docs/project/00_MASTER_PLAN.md` ;
- `docs/project/01_EXECUTION_BOARD.md` ;
- `docs/project/02_CODEX_WORKFLOW.md` ;
- `docs/project/03_HANDOFF_FOR_NEW_AGENT.md` ;
- `docs/project/04_LAST_STATE.md` ;
- `docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md` ;
- `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md` ;
- `docs/sprints/SPRINT_SELAS_V1.md` ;
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md` ;
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md` ;
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md` ;
- `docs/sprints/SPRINT_SELAS_TICKETS_001.md` ;
- `docs/delivery/lot_01_analysis_and_specs_v1.md` ;
- `src/sydel_doc_engine/generators/lot_01/autorisation_domiciliation.py` ;
- `tests/unit/test_autorisation_domiciliation.py` ;
- `src/sydel_doc_engine/front_data/canonical_mapping.py`.

## Decision documentaire

`DOC-002` reste le document canonique cible pour l'autorisation de domiciliation
SELAS.

La reutilisation est autorisee en V1 seulement parce que le texte existant est
neutre vis-a-vis de la forme sociale :

- il ne mentionne pas `SELARL` ;
- il ne mentionne pas `SELAS` ;
- il ne mentionne pas `Gerant` / `Gerante` ;
- il ne mentionne pas `President` / `Presidente` ;
- il ne mentionne pas `parts sociales` ;
- il ne mentionne pas `actions`.

Aucun nouveau document canonique n'est cree pour la SELAS.

## Regle President

Pour le parcours SELAS, le signataire du `DOC-002` est le president de la SELAS
dans le contexte dossier.

Le texte du `DOC-002` ne doit pas ajouter le mot `President`. La fonction du
signataire est une regle de contexte, pas un wording documentaire a inventer.

## Regle adresse

Point sensible : la spec Lot 1 initiale mentionnait un champ libre
`domiciliation.adresse_domiciliation_affichee`, mais le generateur actuel
utilise l'adresse du siege social de la societe comme adresse du cabinet.

Decision V1 SELAS :

- le `DOC-002` est generable seulement si la domiciliation est le siege/cabinet ;
- la regle de reutilisation doit etre explicite :

```text
address:siege_social -> address:domiciliation
```

- si une adresse de domiciliation distincte est saisie, le futur dev ne doit pas
  la consommer silencieusement ;
- dans ce cas, la generation SELAS du `DOC-002` reste bloquee ou reservee a un
  ticket separe.

## Variables requises

Variables personne / president signataire :

- `personne.president.genre` ;
- `personne.president.civilite_affichage` ;
- `personne.president.prenom` ;
- `personne.president.nom`.

Variables societe :

- `societe.societe_principale.denomination` ;
- `societe.societe_principale.capital_social` ;
- `societe.societe_principale.siege.adresse.num_voie` ;
- `societe.societe_principale.siege.adresse.voie` ;
- `societe.societe_principale.siege.adresse.cp` ;
- `societe.societe_principale.siege.adresse.ville`.

Variables signature :

- `signature.lieu` ;
- `signature.date`.

Variable de contexte utile mais non consommee par le texte actuel :

- `societe.societe_principale.forme_sociale`.

## Roles requis

Roles obligatoires :

- `PRESIDENT` ;
- `SIGNATAIRE` ;
- `SOCIETE_PRINCIPALE`.

Roles non requis pour ce document :

- `ACTIONNAIRE` ;
- `MANDATAIRE` ;
- `CONJOINT`.

Role bloque :

- `DIRECTEUR_GENERAL`.

## Controles de wording

Le futur ticket de code devra verifier la presence de :

- `AUTORISATION DE DOMICILIATION` ;
- `Je soussigné` ou `Je soussignée` selon le genre ;
- `autorise la domiciliation de la Société` ;
- la denomination sociale ;
- le capital social ;
- `en cours de formation` ;
- `dans les locaux du cabinet au` ;
- l'adresse siege/cabinet ;
- `pour une durée indéterminée` ;
- le lieu et la date de signature ;
- le nom du president signataire.

Le futur ticket de code devra verifier l'absence de :

- `SELARL` ;
- `Gérant` ;
- `Gerant` ;
- `gérant` ;
- `gerant` ;
- `parts sociales` ;
- `actions` ;
- `Directeur Général` ;
- `Directeur General` ;
- `Président` ;
- `President`.

## Blocages

La generation doit rester bloquee si :

- le president signataire est absent ;
- le genre grammatical du president est absent ;
- la civilite, le prenom ou le nom du signataire sont absents ;
- la denomination sociale est absente ;
- le capital social est absent ;
- un composant de l'adresse siege/cabinet est absent ;
- le lieu ou la date de signature est absent ;
- une adresse de domiciliation distincte du siege est fournie sans arbitrage ;
- un directeur general est demande ;
- le pack SELAS complet est demande avant smoke et revue humaine.

## Impact front / schema attendu

Le futur ticket de code devra aligner le schema SELAS du `DOC-002` avec cette
spec :

- declarer `PRESIDENT` comme role metier attendu ;
- conserver `SIGNATAIRE` comme role documentaire ;
- conserver `SOCIETE_PRINCIPALE` ;
- exiger `societe.societe_principale.capital_social` ;
- exiger les composants de `societe.societe_principale.siege.adresse` ;
- garder la regle de reutilisation explicite `siege_social -> domiciliation` ;
- ne pas presenter une adresse de domiciliation distincte comme generable dans
  le parcours SELAS simple.

## Tests attendus pour le futur dev

Le futur ticket `SELAS-DOC002-DOMICILIATION-001` devra ajouter ou verifier :

1. un cas SELAS president masculin generant le `DOC-002` sans mention SELARL,
   Gerant, President, parts sociales ou actions ;
2. un cas SELAS presidente feminine avec `Je soussignée` ;
3. un blocage si le president signataire manque ;
4. un blocage si le capital social manque ;
5. un blocage si le siege/cabinet est incomplet ;
6. un blocage si lieu/date de signature manque ;
7. un controle schema sur les roles `PRESIDENT`, `SIGNATAIRE` et
   `SOCIETE_PRINCIPALE` ;
8. un controle schema sur la regle explicite `siege_social -> domiciliation`.

## Conclusion

`DOC-002` est un bon candidat de reutilisation SELAS, mais uniquement comme
document neutre et siege/cabinet.

La prochaine etape recommandee est :

```text
SELAS-DOC002-DOMICILIATION-001
```

Ce futur ticket peut etre code de maniere limitee, mais il ne doit toujours pas
activer le pack SELAS complet.
