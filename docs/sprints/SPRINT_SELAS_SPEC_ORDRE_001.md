# SELAS spec ordre 001

Date : 2026-06-02

Ticket : `SELAS-SPEC-ORDRE-001`

Statut : `DONE - spec documentaire`

Decision sprint : `NO-GO pack`

## Objet

Verrouiller l'usage SELAS de `DOC-034 - Demande d'inscription a l'Ordre`
avant tout branchement documentaire SELAS.

Ce livrable ne code rien, ne modifie aucun generateur, ne genere aucun
DOCX/PDF/ZIP, ne change aucune source DOCX et ne valide aucun wording juridique
nouveau. Il fixe seulement les conditions de reutilisation du document ordre
dans le parcours SELAS V1.

## Sources et livrables lus

- `docs/delivery/lot_02_demande_inscription_ordre_cadrage_v1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_canonique_v1.md`
- `docs/delivery/lot_02_demande_inscription_ordre_spec_texte_v1.md`
- `docs/sprints/SPRINT_SELAS_REUSE_AUDIT_001.md`
- `docs/sprints/SPRINT_SELAS_MATRIX_001.md`
- `docs/sprints/SPRINT_SELAS_FRONT_CONTRACT_001.md`
- `docs/sprints/SPRINT_SELAS_TICKETS_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_PRESIDENT_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_STATUTS_MEDECIN_AU_001.md`
- `docs/sprints/SPRINT_SELAS_SPEC_CAPITAL_ACTIONS_001.md`
- `src/sydel_doc_engine/front_data/selas_schema.py`
- `src/sydel_doc_engine/generators/lot_02/demande_inscription_ordre.py`
- `tests/unit/test_demande_inscription_ordre.py`

ADR applicables :

- ADR-0001 : source de verite documentaire ;
- ADR-0002 : moteur par document canonique ;
- ADR-0003 : livraison par lots documentaires ;
- ADR-0005 : mode Codex repo-first.

## Perimetre V1

Inclus :

- structure : `SELAS` ;
- profession active du premier parcours : medecin ;
- creation simple ;
- actionnaire unique ;
- president unique ;
- signataire principal personne physique ;
- mandataire formalites distinct ;
- demande d'inscription de la societe au tableau de l'Ordre ;
- adresse ordinale explicite ;
- pieces ordinales visibles comme pieces attendues.

Exclus :

- SELAS chirurgien-dentiste tant que les statuts dentiste SELAS restent sans
  source analysee ;
- site distinct ou derogation automatisee ;
- exercice dans plusieurs structures ;
- multi-actionnaires ;
- directeur general ;
- SCM ;
- cession de fonds ou cabinet ;
- micro-holding, personne morale actionnaire ou actions de preference ;
- modele departemental specifique non source ;
- automatisation des plans/devis comme documents `DOC-XXX`.

## Decision documentaire

`DOC-034 - Demande d'inscription a l'Ordre` est le document canonique cible pour
la SELAS V1.

La reutilisation est autorisee en `reuse-check fort`, car la spec texte ordre
indique que les variantes SELARL et SELAS ont un overlay visible identique pour
ce document. La reutilisation ne vaut pas activation du pack SELAS : elle
autorise seulement un futur ticket borne `SELAS-DOC034-ORDRE-001` si Gad donne
un `GO dev` explicite.

Le document ne doit pas etre reconstruit depuis une substitution globale
SELARL -> SELAS. Il doit consommer l'overlay `SELARL_SELAS` deja decrit dans les
specs ordre, avec une structure dossier `SELAS`.

## Regle de role President

Dans ce document, la formule :

```text
Monsieur le President
```

designe le destinataire ordinal, c'est-a-dire le president du Conseil
departemental de l'Ordre.

Cette formule ne doit pas etre rattachee au role metier `President` de la SELAS.
Le president SELAS peut etre le signataire du dossier, mais le libelle ordinal
reste une variable d'ordre :

- `ordre.destinataire_appel`

et non une variable de gouvernance SELAS.

## Roles et donnees obligatoires

### Roles

| Role | Statut V1 | Note |
| --- | --- | --- |
| `signataire` | Obligatoire | En parcours SELAS simple, pointe vers le president/praticien via reuse explicite. |
| `mandataire` | Obligatoire | Distinct du signataire ; peut venir d'une configuration SYDEL ou de champs dossier. |
| `societe_principale` | Obligatoire | Societe SELAS a inscrire. |
| `ordre_professionnel` | Obligatoire | Conseil departemental, profession ordinale, adresse, appel. |
| `president` | Contexte dossier | Ne pilote pas `ordre.destinataire_appel`. |
| `actionnaire` | Contexte dossier | Non consomme directement par `DOC-034` V1. |

### Donnees minimales

- `dossier.structure = SELAS`
- `dossier.options.derogation = false` pour le parcours V1 simple
- `signataire.titre_affichage`
- `signataire.prenom`
- `signataire.nom`
- `signataire.adresse_personnelle_affichee`
- `societe.denomination`
- `ordre.conseil_departemental_libelle`
- `ordre.destinataire_appel`
- `ordre.profession_signataire_affichee`
- `ordre.profession_ligne_destinataire`
- `ordre.profession_reglementee_pluriel`
- `ordre.adresse.ligne_1`
- `ordre.adresse.cp`
- `ordre.adresse.ville`
- `mandataire.civilite_affichage`, `mandataire.prenom`, `mandataire.nom`,
  `mandataire.fonction`, `mandataire.cabinet`
- ou `mandataire.libelle_affiche` resolu par configuration
- `signature.lieu`
- `signature.date`

Donnees professionnelles utiles cote front, mais non toutes consommees par le
texte `DOC-034` actuel :

- numero RPPS ;
- numero d'inscription a l'Ordre ;
- profession reglementee ;
- departement ou ville du Conseil de l'Ordre.

## Regles de generation futures

Un futur ticket code `SELAS-DOC034-ORDRE-001` devra :

1. utiliser `DOC-034` sans creer un nouveau code canonique ;
2. passer `dossier.structure = SELAS` au generateur ordre ;
3. utiliser l'overlay `SELARL_SELAS` ;
4. bloquer si une donnee ordinale obligatoire manque ;
5. bloquer si aucun mandataire complet ne peut etre resolu ;
6. bloquer si `dossier.options.derogation == true` sans mention manuelle
   explicitement fournie ;
7. ne jamais rendre le litteral source residuel `Derogation ?` ;
8. ne pas ajouter de wording de site distinct ou de derogation ;
9. ne pas feminiser automatiquement `associe`, `praticien`, `exercant` ou
   l'appel ordinal ;
10. ne pas confondre `President` SELAS et president du Conseil de l'Ordre ;
11. verifier l'absence de `SELARL`, `gerant`, `parts sociales`,
   `Directeur General` et `Derogation ?` dans une sortie SELAS simple.

## Pieces ordinales plans/devis

NotebookLM signale que certains Ordres peuvent demander des plans des locaux ou
des devis de materiel.

Decision V1 :

- ces pieces ne sont pas des documents `DOC-XXX` generes par le moteur dans ce
  ticket ;
- elles doivent apparaitre cote front comme pieces attendues ou pieces a joindre
  selon le conseil ordinal / la profession / le departement ;
- elles ne doivent pas bloquer la generation de `DOC-034` par defaut ;
- elles peuvent bloquer la readiness du dossier ordre si le parcours produit
  choisit un mode `dossier complet pour depot ordinal` ;
- le caractere strictement bloquant par departement reste un arbitrage produit
  separe, hors present ticket.

Regle pratique V1 :

```text
DOC-034 generable si les champs du document sont complets.
Dossier ordre complet non garanti si plans/devis requis mais absents.
```

## Cas bloques

Le parcours SELAS V1 doit bloquer ou sortir du pack simple si :

- `dossier.options.derogation == true` sans mention manuelle validee ;
- site distinct ou deuxieme lieu d'exercice ;
- exercice dans plusieurs structures ;
- modele departemental specifique exige mais non source ;
- mandataire absent ou ambigu ;
- adresse du Conseil de l'Ordre absente ;
- profession ordinale plurielle absente ;
- SELAS chirurgien-dentiste tant que le sprint reste limite au medecin ;
- multi-actionnaires, directeur general, SCM, cession, micro-holding ou actions
  de preference.

## Impact front/data

Le schema SELAS actuel expose deja `DOC-034` avec :

- roles `SIGNATAIRE`, `MANDATAIRE`, `SOCIETE_PRINCIPALE`,
  `ORDRE_PROFESSIONNEL` ;
- adresses `ORDRE` et `ADRESSE_PERSONNELLE` ;
- champs ordre/profession/RPPS/numero ordre/options derogation ;
- ambiguites `selas_ordre_pieces_plans_devis` et `mandataire_configurable`.

Decision spec :

- `mandataire_configurable` n'est plus une ambiguite bloquante si le futur code
  accepte `mandataire.libelle_affiche` ou les champs detailles ;
- `selas_ordre_pieces_plans_devis` reste une reserve produit front : pieces
  attendues a afficher, blocage dossier complet a arbitrer ;
- le role `PRESIDENT` n'a pas besoin d'etre ajoute aux roles directs du
  document si le role `SIGNATAIRE` pointe explicitement vers le president.

## Criteres d'acceptation d'un futur ticket code

Un futur `SELAS-DOC034-ORDRE-001` sera acceptable si :

- un contexte SELAS simple genere `demande_inscription_ordre.docx` ;
- le texte ne contient aucun placeholder source `[` ou `]` ;
- le texte ne contient pas `Derogation ?` ;
- le texte ne contient pas `SELARL`, `gerant`, `parts sociales` ou
  `Directeur General` ;
- le texte conserve l'objet `Demande d'inscription au tableau de l'Ordre` ;
- le texte rend la denomination de la SELAS ;
- le texte rend les donnees ordinales medecin et l'adresse du Conseil ;
- le mandataire est rendu depuis les donnees ou la configuration, pas en dur ;
- la derogation sans mention manuelle bloque ;
- les plans/devis sont affichables comme pieces attendues, sans etre confondus
  avec un document genere.

## Decision de sortie

`SELAS-SPEC-ORDRE-001` est suffisant pour autoriser une demande de `GO dev`
borne sur :

```text
SELAS-DOC034-ORDRE-001
```

Ce futur ticket devra rester limite a `DOC-034` et au parcours SELAS medecin
actionnaire unique / president unique. Il ne devra pas activer le pack SELAS
complet.

Prochaine action recommandee : `SELAS-SPEC-REGIME-COMMUNAUTAIRE-001`, ou
validation outillee des tickets deja codes (`DOC-001`, `DOC-002`, `DOC-003`).
