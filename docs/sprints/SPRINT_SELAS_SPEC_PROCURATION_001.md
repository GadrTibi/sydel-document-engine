# SELAS spec procuration 001

Date : 2026-06-02

Ticket : `SELAS-SPEC-PROCURATION-001`

Statut : `DONE - spec documentaire`

Decision sprint : `NO-GO generation`

## Objet

Verifier et specifier l'adaptation SELAS de `DOC-003 - Procuration` pour le
parcours V1 :

```text
SELAS medecin, actionnaire unique, president unique, creation simple.
```

Ce livrable ne code rien, ne genere aucun DOCX/PDF/ZIP et ne valide pas encore
un pack SELAS. Il prepare le futur ticket de code
`SELAS-DOC003-PROCURATION-PRESIDENT-001`.

## Sources et livrables lus

- `docs/sprints/SPRINT_SELAS_SPEC_PRESIDENT_001.md`
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md`
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md`
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- `src/sydel_doc_engine/generators/lot_01/procuration.py`
- `tests/unit/test_procuration.py`

## Decision documentaire

`DOC-003` reste le document canonique cible pour la procuration SELAS V1.

Decision :

- ne pas creer un nouveau code canonique pour la procuration president ;
- reutiliser le generateur `DOC-003` seulement si le contexte fournit une
  fonction dirigeant strictement resolue en `President` pour SELAS ;
- ne pas faire de remplacement texte global `gerant -> president` ;
- ne pas brancher la generation SELAS tant que le futur ticket de code n'ajoute
  pas les tests anti-regression.

## Pourquoi la reutilisation est possible

La procuration existante est deja parametree autour de donnees generiques :

- identite du signataire ;
- adresse personnelle ;
- fonction dirigeant ;
- forme sociale ;
- denomination ;
- siege social ;
- lieu/date de signature ;
- bloc mandataire SYDEL.

Le point SELAS sensible est donc concentre sur :

- `fonction_dirigeant` ;
- `forme_sociale` ;
- la separation signataire / mandataire ;
- les controles de texte final.

## Roles requis

| Role | Obligation | Regle |
| --- | --- | --- |
| `president` | Obligatoire | Dirigeant SELAS signataire de la procuration |
| `signataire` | Obligatoire | Peut pointer vers le president via assignment explicite |
| `mandataire` | Obligatoire | SYDEL ou mandataire configure ; distinct du signataire |
| `societe_principale` | Obligatoire | SELAS en constitution |
| `actionnaire` | Non consomme directement par la procuration | Reste distinct du president |

Interdiction :

- le role `gerant` ne doit pas etre requis pour une procuration SELAS ;
- le mandataire ne doit jamais etre deduit du president ;
- l'actionnaire ne doit pas etre deduit automatiquement comme signataire.

## Variables minimales

### Signataire / President

- `personne.president.civilite_affichage`
- `personne.president.genre`
- `personne.president.prenom`
- `personne.president.nom`
- `personne.president.adresse_personnelle`
- `personne.president.fonction_dirigeant`

Decision :

- pour SELAS V1, `fonction_dirigeant` doit valoir `President` dans le document ;
- la feminisation de la fonction (`Presidente`) reste reservee tant qu'aucune
  source/spec texte ne la valide ;
- le genre continue seulement a piloter `Je soussigne/soussignee`.

### Societe

- `societe.denomination`
- `societe.forme_sociale`
- `societe.siege`

Decision :

- `societe.forme_sociale` doit afficher `SELAS` ou la forme longue validee par
  la source si le futur ticket la fournit ;
- aucune mention `SELARL` ne doit apparaitre.

### Signature

- `signature.lieu`
- `signature.date`

### Mandataire

Le generateur existant utilise un bloc SYDEL configure.

Decision V1 :

- conserver le bloc mandataire existant pour le premier ticket de code ;
- ne pas rendre le mandataire implicite depuis le president ;
- documenter un futur ticket separe si SYDEL veut un mandataire configurable
  dans la procuration visible.

## Texte et wording

Le texte source `DOC-003` est conserve dans sa structure :

1. titre `Procuration` ;
2. identification du signataire ;
3. mention `Agissant en qualite de {fonction_dirigeant}` ;
4. identification de la societe ;
5. pouvoir donne au mandataire ;
6. paragraphes de mandat ;
7. bloc de signature.

Le seul wording SELAS autorise par cette spec est le remplissage variable de :

- `fonction_dirigeant = President` ;
- `forme_sociale = SELAS` ou forme longue validee.

Tout autre changement de phrase doit passer par une spec texte ou une validation
humaine.

## Controles obligatoires du futur ticket de code

Le futur ticket `SELAS-DOC003-PROCURATION-PRESIDENT-001` devra tester que le
texte genere contient :

- `Agissant en qualite de President` ;
- `SELAS` ou la forme sociale SELAS validee ;
- `Procuration` ;
- le bloc mandataire SYDEL ;
- le nom du signataire president ;
- l'adresse personnelle du president ;
- l'adresse du siege.

Il devra aussi tester l'absence de :

- `Gerant` ;
- `gerant` ;
- `SELARL` ;
- `parts sociales` ;
- `Directeur General` ;
- confusion entre mandataire et signataire.

## Conditions de blocage

La procuration SELAS doit rester bloquee si :

- le president n'est pas renseigne ;
- le signataire n'est pas explicitement assigne ;
- la fonction dirigeant n'est pas resolue en `President` ;
- la societe n'est pas de forme SELAS ;
- l'adresse personnelle du president manque ;
- le siege social manque ;
- le mandataire est absent ou non configure ;
- un directeur general est demande ;
- plusieurs actionnaires imposent une gouvernance non V1.

## Impact sur le schema front/data

Le schema `SELAS-FRONT-SCHEMA-001` contient deja une exigence `DOC-003`
compatible :

- roles : `PRESIDENT`, `SIGNATAIRE`, `MANDATAIRE`, `SOCIETE_PRINCIPALE` ;
- champs : `personne.president.*`, `personne.mandataire.*`,
  `societe.societe_principale.denomination`, `signature.*` ;
- ambiguite : `selas_procuration_president_wording`.

Cette spec permet de lever partiellement l'ambiguite de principe :

- `DOC-003` peut etre reutilise ;
- la fonction doit etre parametree strictement en `President` ;
- l'ambiguite de wording reste ouverte jusqu'au futur test/generation.

## Decision sur les tickets suivants

Le prochain ticket recommande devient :

```text
SELAS-DOC003-PROCURATION-PRESIDENT-001
```

Mais seulement si Gad accepte un `GO dev` borne pour ce document.

Sinon, la suite documentaire sans code peut continuer avec :

```text
SELAS-SPEC-DNC-PRESIDENT-001
```

## Criteres d'acceptation du present ticket

- decision de reutilisation de `DOC-003` documentee ;
- role president et fonction dirigeant verrouilles pour la procuration V1 ;
- mandataire maintenu distinct du signataire ;
- tests attendus du futur ticket de code listes ;
- conditions de blocage listees ;
- aucun code modifie ;
- aucune generation activee.

## Decision de sortie

`SELAS-SPEC-PROCURATION-001` est suffisant pour demander un `GO dev` borne sur
`SELAS-DOC003-PROCURATION-PRESIDENT-001`.

Le sprint reste en `NO-GO generation`.
