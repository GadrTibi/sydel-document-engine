# SELAS spec DNC president 001

Date : 2026-06-02

Ticket : `SELAS-SPEC-DNC-PRESIDENT-001`

Statut : `DONE - spec documentaire`

Decision sprint : `NO-GO generation`

## Objet

Verifier et specifier la reutilisation de `DOC-001 - Declaration sur l'honneur
de non-condamnation` pour le parcours V1 :

```text
SELAS medecin, actionnaire unique, president unique, creation simple.
```

Ce livrable ne code rien, ne genere aucun DOCX/PDF/ZIP et ne valide pas encore
un pack SELAS. Il prepare un futur ticket de code borne :

```text
SELAS-DOC001-DNC-PRESIDENT-001
```

## Sources et livrables lus

- `docs/sprints/SPRINT_SELAS_SPEC_PRESIDENT_001.md`
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md`
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md`
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`
- `docs/sprints/SPRINT_SELAS_TICKETS_001.md`
- `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`
- `docs/delivery/lot_01_analysis_and_specs_v1.md`
- `src/sydel_doc_engine/generators/lot_01/declaration_non_condamnation.py`
- `tests/unit/test_declaration_non_condamnation.py`
- `src/sydel_doc_engine/front_data/selas_schema.py`

## Decision documentaire

`DOC-001` reste le document canonique cible pour la DNC President SELAS V1.

Decision :

- ne pas creer un nouveau code canonique pour la DNC President ;
- reutiliser le generateur `DOC-001` uniquement si le declarant est le
  `President` personne physique de la SELAS ;
- ne pas inserer de wording `President` dans le corps de la DNC tant qu'une spec
  texte ou une validation humaine ne le demande pas ;
- conserver la filiation comme donnee obligatoire, car elle est deja requise par
  la spec Lot 1 et par le generateur canonique actuel ;
- bloquer la generation si la filiation est absente.

## Pourquoi la reutilisation est possible

La DNC existante est centree sur une personne physique. Elle ne consomme pas la
forme sociale, le capital, les actions, les parts, le siege ou la fonction
dirigeante dans son texte courant.

La reutilisation SELAS est donc possible parce que les donnees utiles sont
transverses :

- identite civile ;
- genre grammatical ;
- date de naissance ;
- nationalite ;
- adresse personnelle ;
- filiation ;
- lieu et date de signature.

Le point SELAS sensible n'est pas un remplacement de texte `Gerant -> President`.
Le point sensible est le mapping : la personne qui signe la DNC doit etre le
President SELAS, pas un gerant SELARL, un mandataire ou un actionnaire non
dirigeant.

## Roles requis

| Role | Obligation | Regle |
| --- | --- | --- |
| `president` | Obligatoire | Personne physique declarant la non-condamnation |
| `signataire` | Obligatoire | Doit pointer explicitement vers le president pour ce document |
| `societe_principale` | Non consommee par le texte actuel | Utile au lot, pas au generateur `DOC-001` |
| `actionnaire` | Non consomme directement | Peut etre la meme personne en V1, mais pas deduit automatiquement |
| `mandataire` | Non consomme | Ne doit pas etre substitue au president |
| `directeur_general` | Bloque V1 | Non trouve dans les sources SELAS NotebookLM |

## Variables minimales

### President declarant

- `personne.president.genre`
- `personne.president.civilite_affichage`
- `personne.president.prenom`
- `personne.president.nom`
- `personne.president.date_naissance`
- `personne.president.nationalite`
- `personne.president.adresse_personnelle`
- `personne.president.nom_pere`
- `personne.president.nom_mere`

### Signature

- `signature.lieu`
- `signature.date`
- `signature.image` optionnelle selon le rendu existant

### Donnee collectee mais non consommee par le texte actuel

Le schema SELAS mentionne `lieu_naissance` dans le bloc President. Le generateur
canonique `DOC-001` actuel ne consomme pas cette donnee dans son texte.

Decision :

- ne pas rendre `lieu_naissance` obligatoire pour `DOC-001` sans modification
  de wording humainement validee ;
- continuer a la collecter dans le parcours global si elle est utile a d'autres
  documents.

## Filiation

Constat :

- la spec Lot 1 existante et le generateur `DOC-001` exigent `nom_pere` et
  `nom_mere` ;
- les reponses NotebookLM SELAS citent la DNC, mais ne confirment pas de facon
  stable la filiation comme champ SELAS source ;
- retirer la filiation serait un changement de logique documentaire et de texte.

Decision V1 :

- garder la filiation obligatoire pour la DNC President SELAS ;
- documenter l'ambiguite source NotebookLM ;
- bloquer la generation si `nom_pere` ou `nom_mere` manque ;
- ne pas rendre la filiation optionnelle sans validation humaine/juridique.

## Texte et wording

Le texte source `DOC-001` est conserve dans sa structure :

1. titre de declaration de non-condamnation ;
2. formule `Je soussigne/soussignee` selon le genre ;
3. identite civile ;
4. date de naissance ;
5. nationalite ;
6. adresse personnelle ;
7. filiation ;
8. declaration sur l'honneur ;
9. rappel des sanctions ;
10. lieu/date/signature.

Cette spec n'autorise aucun changement de phrase juridique.

Termes qui ne doivent pas apparaitre dans une DNC President SELAS V1 :

- `Gerant` ;
- `gerant` ;
- `Gérant` ;
- `gérant` ;
- `SELARL` ;
- `parts sociales` ;
- `Directeur General` ;
- `Directeur Général`.

Note : l'absence du mot `President` dans le texte final n'est pas un bug si le
document canonique reste centre sur la personne physique. Le role President doit
etre porte par le contexte et par le mapping signataire.

## Impact sur le schema front/data

Le schema SELAS contient deja une exigence `DOC-001` candidate avec l'ambiguite :

```text
selas_dnc_filiation_president
```

Le futur ticket de code/schema devra aligner l'exigence `DOC-001` avec la spec :

- ajouter explicitement `personne.president.nom_pere` ;
- ajouter explicitement `personne.president.nom_mere` ;
- ajouter explicitement `personne.president.nationalite` si absent ;
- verifier que l'adresse personnelle est decomposee selon les attentes du
  generateur ;
- conserver `lieu_naissance` comme champ global non consomme par `DOC-001`, sauf
  validation texte contraire.

## Controles obligatoires du futur ticket de code

Le futur ticket `SELAS-DOC001-DNC-PRESIDENT-001` devra tester que le texte genere
contient :

- le titre de declaration de non-condamnation ;
- la formule `Je soussigne` ou `Je soussignee` selon le genre ;
- le nom et prenom du President ;
- la date de naissance ;
- la nationalite ;
- l'adresse personnelle ;
- la filiation pere/mere ;
- le lieu et la date de signature ;
- le rappel des sanctions prevu par le document existant.

Il devra aussi tester :

- l'absence des termes interdits listes ci-dessus ;
- le blocage si `nom_pere` manque ;
- le blocage si `nom_mere` manque ;
- le blocage si le signataire n'est pas assigne au President ;
- l'absence de modification du texte juridique hors variables existantes.

## Conditions de blocage

La DNC President SELAS doit rester bloquee si :

- le President n'est pas renseigne ;
- le President n'est pas une personne physique ;
- le signataire n'est pas explicitement le President ;
- le genre manque ;
- la date de naissance manque ;
- la nationalite manque ;
- l'adresse personnelle manque ;
- `nom_pere` manque ;
- `nom_mere` manque ;
- le dossier tente d'utiliser un `Gerant` pour une SELAS ;
- un `Directeur General` est demande en V1.

## Decision sur les tickets suivants

Le prochain ticket de code possible devient :

```text
SELAS-DOC001-DNC-PRESIDENT-001
```

Mais seulement avec un `GO dev` borne pour ce document.

Sinon, la suite documentaire sans code peut continuer avec :

```text
SELAS-SPEC-DOC002-DOMICILIATION-001
```

ou :

```text
SELAS-SPEC-DECISION-PRESIDENT-001
```

## Criteres d'acceptation du present ticket

- decision de reutilisation de `DOC-001` documentee ;
- role President / signataire verrouille pour la DNC V1 ;
- filiation traitee comme obligatoire et ambiguite source documentee ;
- wording juridique conserve ;
- conditions de blocage listees ;
- futur ticket de code et controles attendus explicites ;
- pack SELAS maintenu bloque.
