# SELAS matrix 001

Date : 2026-06-01

Ticket : `SELAS-MATRIX-001`

Statut : `DONE - cadrage lecture seule`

Decision sprint : `NO-GO dev`

## Objet

Produire la matrice documentaire SELAS provisoire a partir :

- du journal NotebookLM SELAS ;
- de l'audit de reutilisation `SELAS-REUSE-AUDIT-001` ;
- du catalogue documentaire existant ;
- des specs deja disponibles.

Cette matrice ne vaut pas `GO dev`. Elle sert a preparer le futur contrat
metier-front et les arbitrages de scope.

## Perimetre recommande pour un premier sprint dev futur

Le seul perimetre qui semble raisonnable pour un premier ticket futur est :

```text
SELAS medecin, associe unique, president unique, creation simple, sans cession,
sans SCM, sans derogation, sans site distinct, sans directeur general, sans
micro-holding, sans actions de preference, hors multi-actionnaires.
```

Ce perimetre reste en `NO-GO dev` tant que Gad n'a pas valide un ticket borne et
tant que les specs SELAS president / procuration / statuts ne sont pas
explicitement fermees.

## Matrice documentaire principale

| Condition | Document | Code | Statut source | Statut moteur | Statut front SELAS | Decision matrice | Notes / action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Toujours | Declaration de non-condamnation du president | `DOC-001` | Source Lot 1 + indice NotebookLM SELAS ; filiation president non confirmee par NotebookLM | Generateur existant Lot 1 | Non branche SELAS | `reuse-check` | Reutilisation probable des donnees personne/signature ; verifier fonction `President` et filiation avant code |
| Toujours | Autorisation de domiciliation | `DOC-002` | Source Lot 1 ; document neutre selon audit | Generateur existant Lot 1 | Non branche SELAS | `reuse-check` | Candidat le plus proche d'une reutilisation forte, sous reserve source SELAS/source truth |
| Toujours | Procuration | `DOC-003` | Source Lot 1 + NotebookLM : doit mentionner `President` | Generateur existant Lot 1 | Non branche SELAS | `adapter` | Ne pas faire de remplacement global ; spec SELAS requise pour la fonction du signataire |
| Toujours | Decision / PV de nomination du president | Proche `DOC-004` mais libelle canonique SELAS a confirmer | Source PV gerant SELARL + indices NotebookLM ; gouvernance SELAS differente | Generateur PV gerant existant | Non branche SELAS | `adapter` | Creer une spec president SELAS ; DG exclu ; ne pas reutiliser le titre `gerant` |
| Toujours | Demande d'inscription a l'Ordre | `DOC-034` | Spec ordre couvre SELARL/SELAS ; source NotebookLM nommee | Generateur existant ; overlay SELARL/SELAS documente | Non branche SELAS | `reuse-check` | Verifier pieces plans/devis et eventuels formulaires departementaux ; pas de lock humain SELAS |
| Profession = medecin | Statuts SELAS medecin | `DOC-018` | Source DOCX repo `Statuts_SELAS_medecin.docx` + spec statuts SEL | Generateur/catalogue existant cote moteur | Non branche SELAS produit | `adapter` | Premier candidat statuts ; associe unique uniquement ; actions/president a verrouiller |
| Profession = chirurgien-dentiste | Statuts SELAS dentiste | A definir | NotebookLM indique le besoin, source repo non identifiee | Non etabli | Non branche SELAS | `no-go` provisoire | Trouver la source DOCX dentiste SELAS avant toute promesse produit |
| Toujours ou capital | Attestation depot capital / liste souscripteurs | A definir, possiblement famille `DOC-024`/`DOC-042` a ne pas confondre | Sources attestation/liste souscripteurs ambiguës | Moteur SPFPL/SAS existe, pas SELAS creation simple qualifiee | Non branche SELAS | `reserve` | Identifier document canonique exact et source SELAS avant matrice generable |
| Regime communautaire = oui | Lettre de renonciation conjoint | `DOC-005` | Source SELAS presente + batch regime | Generateur existant | Non branche SELAS | `reuse-check` | Effet juridique SELAS a arbitrer ; ne pas extrapoler depuis SELARL |
| Regime communautaire = oui | Lettre d'avertissement conjoint | `DOC-006` | Source batch, mais historiquement reserve SELARL | Generateur existant | Non branche SELAS | `reserve` / `no-go` | Garder hors premier ticket tant que decision SELAS pas explicite |
| Cession fonds / passage BNC vers SELAS | Acte de cession cabinet medical | `DOC-009` | Specs cession existantes ; NotebookLM indique redaction personnalisee | Generateur existant | Non branche SELAS | `manuel` / `no-go V1 simple` | Hors happy path ; origine propriete et prix exigent sous-formulaire/arbitrages |
| Cession fonds / passage BNC vers SELAS | Compromis cession cabinet medical | `DOC-010` | Specs cession existantes | Generateur existant | Non branche SELAS | `manuel` / `no-go V1 simple` | Hors happy path |
| Cession fonds / passage BNC vers SELAS | Acte de cession cabinet dentaire | `DOC-011` | Specs cession existantes | Generateur existant | Non branche SELAS | `manuel` / `no-go V1 simple` | Hors happy path |
| Cession fonds / passage BNC vers SELAS | Compromis cession cabinet dentaire | `DOC-012` | Specs cession existantes | Generateur existant | Non branche SELAS | `manuel` / `no-go V1 simple` | Hors happy path |
| Cession / bail | Avenant contrat de bail | `DOC-007` | Specs bail SELARL/SELAS existantes | Generateur existant | Non branche SELAS | `reserve` | Lie a cession ; hors premier parcours simple |
| Cession / financement | Appel de fonds SEL | `DOC-008` | Source/registre limite SELARL ; SELAS bloquee dans notes moteur | Generateur existant SELARL seulement | Non branche SELAS | `no-go` | Wording SELAS bloque en V1 moteur |
| SCM = oui | PV AGE cession parts SCM | `DOC-031` | Source SELAS presente + specs SCM | Generateur existant avec overlay SELARL/SELAS | Non branche SELAS | `adapter` / hors V1 simple | Sous-cas dedie requis ; ne pas melanger au premier ticket |
| SCM = oui | Courrier SDE cession SCM | `DOC-032` | Source SELAS presente + specs SCM | Generateur existant avec divergence SELAS documentee | Non branche SELAS | `adapter` / hors V1 simple | Sous-cas dedie requis |
| SCM = oui | Acte cession parts SCM vers SEL | `DOC-033` | Source SELARL transformee + source SELAS dediee conservee | Generateur existant | Non branche SELAS | `adapter` / hors V1 simple | Sous-cas dedie requis |
| Site distinct / derogation | Formulaire derogation multi-sites SEL | `DOC-013` | Spec derogation existe ; NotebookLM cite site distinct | Generateur formulaire a completer | Non branche SELAS | `manuel` / `reserve` | Afficher comme attendu/manuel ; ne pas promettre generation automatique |
| Derogation cumul | Demande derogation cumul SELARL salariee | Sans code SELAS propre dans catalogue | Source legacy .doc non convertie ; libelle SELARL | Non implemente pour SELAS | Non branche SELAS | `no-go` | Ne pas transposer a SELAS sans source dediee |
| Multi-actionnaires | PV/statuts/actionnaires multiples | A definir | NotebookLM signale risque ; sources pluriel incompletes | Structures partielles cote SELARL seulement | Non branche SELAS | `no-go V1 simple` | Reporter ; actions, votes, droits financiers, accords pluriel a specifier |
| Directeur general | PV nomination DG | A definir | Raw manifest signale une source `.doc`, NotebookLM dit non trouve pour V1 | Non implemente | Non branche SELAS | `no-go` | Exclure du premier parcours |
| Micro-holding / actions de preference | Statuts SELAS avec MH | A definir | Source `modele Statuts SELAS avec MH.docx` lue globalement | Non branche | Non branche SELAS | `no-go V1 simple` | Ticket separe ; personne morale, actions de preference, droits derogatoires |
| Pieces ordinales | Plans locaux / devis materiel | Hors `DOC-XXX` pour l'instant | NotebookLM cite exigences selon Ordre | Non moteur | Non front | `manuel` / `reserve` | A afficher comme pieces attendues ; caractere bloquant UI a arbitrer |

## Pack candidat V1 simple

Ce pack est une hypothese produit, pas une autorisation de dev.

| Ordre | Document | Code | Decision | Blocage avant dev |
| --- | --- | --- | --- | --- |
| 1 | Declaration de non-condamnation president | `DOC-001` | `reuse-check` | confirmer filiation et fonction president |
| 2 | Autorisation de domiciliation | `DOC-002` | `reuse-check` | confirmer neutralite SELAS |
| 3 | Procuration president | `DOC-003` | `adapter` | spec wording president |
| 4 | Decision / PV nomination president | proche `DOC-004` | `adapter` | spec document canonique SELAS |
| 5 | Demande inscription Ordre | `DOC-034` | `reuse-check` | confirmer pieces ordinales et overlay SELAS |
| 6 | Statuts SELAS medecin | `DOC-018` | `adapter` | lock source/spec SELAS associe unique |
| 7 | Lettre renonciation conjoint, si communaute | `DOC-005` | `reuse-check` | arbitrage regime communautaire SELAS |

## Documents exclus du premier pack candidat

| Famille | Decision | Raison |
| --- | --- | --- |
| Statuts SELAS dentiste | `no-go provisoire` | Source DOCX dentiste SELAS non identifiee dans le repo |
| `DOC-006` avertissement conjoint | `reserve` | Decision SELAS non explicite |
| Cession fonds / cabinet | `manuel` / `no-go V1 simple` | Redaction personnalisee et origine propriete complexe |
| SCM cession | `adapter` mais hors V1 simple | Sous-cas dedie et donnees nombreuses |
| Derogations / site distinct | `manuel` / `reserve` | Formulaires a completer et logique ordinale a arbitrer |
| Multi-actionnaires | `no-go V1 simple` | Actions, votes, droits financiers, accords et statuts pluriels non verrouilles |
| Directeur general | `no-go` | Non trouve dans NotebookLM V1 ; source raw non qualifiee |
| Micro-holding / actions de preference | `no-go V1 simple` | Cas complexe distinct, source dediee et arbitrage humain requis |

## Donnees minimales a prevoir pour le futur contrat front

### Bloc dossier

- type de dossier : `SELAS` ;
- profession : `medecin` d'abord, `chirurgien_dentiste` seulement apres source ;
- associe unique : oui pour le premier perimetre ;
- options : regime communautaire, cession, SCM, derogation, site distinct ;
- toutes les options complexes doivent bloquer ou afficher une preparation
  manuelle dans le premier parcours.

### Bloc personnes

- praticien ;
- actionnaire unique ;
- president ;
- signataire ;
- mandataire ;
- conjoint conditionnel.

Regle : en dossier unipersonnel seulement, le praticien peut alimenter
actionnaire unique, president et signataire. Aucune fusion silencieuse hors de
ce cas.

### Bloc societe / capital

- denomination ;
- forme sociale complete/abregee SELAS ;
- siege ;
- lieu d'exercice ;
- capital ;
- nombre d'actions ;
- valeur nominale ;
- banque de depot ;
- numerotation des actions : decision ouverte.

## Questions ouvertes avant `GO dev`

1. Gad valide-t-il que le premier perimetre est `SELAS medecin associe unique`
   seulement ?
2. Quelle source doit servir pour les statuts SELAS dentiste ?
3. La DNC president exige-t-elle toujours la filiation complete dans le parcours
   SELAS ?
4. La numerotation des actions doit-elle etre automatique ou saisie par le
   juriste ?
5. `DOC-006` doit-il rester reserve ou etre inclus pour SELAS regime
   communautaire ?
6. Les plans/devis Ordre sont-ils bloquants dans le parcours ou simplement
   listes comme pieces attendues ?
7. L'interface doit-elle dire `Actionnaire` ou garder `Associe` comme terme
   transversal avec wording documentaire adapte ?

## Decision de sortie

`SELAS-MATRIX-001` est suffisant pour passer a la preparation du contrat
metier-front SELAS en lecture seule : `SELAS-FRONT-CONTRACT-001`.

Il ne donne aucun `GO dev`.
