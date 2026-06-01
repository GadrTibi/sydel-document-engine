# Sprint orchestrator protocol V1

Date : 2026-06-01

## Objet

Ce document definit l'orchestrateur de sprint operationnel pour les sprints par
type d'entreprise.

Il ne remplace pas l'orchestrateur moteur qui choisit les generateurs de
documents. Il protege le projet avant et pendant le developpement : il garde le
statut du sprint, les gates, les preuves attendues et la prochaine action.

Regle centrale :

```text
Ouverture de sprint != autorisation de developper.
```

Tout sprint commence en `NO-GO dev`.

## Difference avec l'orchestrateur moteur

| Sujet | Orchestrateur de sprint | Orchestrateur moteur |
| --- | --- | --- |
| Moment | Avant et pendant le sprint | Pendant une generation dossier |
| Role | Piloter les phases, gates, validations et blocages | Selectionner les generateurs documentaires |
| Source de statut | `docs/sprints/SPRINT_[TYPE]_V1.md` | catalogue moteur + contexte dossier |
| Risque evite | Partir en dev sans cadrage | Produire les mauvais documents |

## Source de verite du sprint

Chaque sprint actif doit avoir un fichier :

```text
docs/sprints/SPRINT_[TYPE]_V1.md
```

Ce fichier est la source de verite operationnelle du sprint. Codex doit le lire
avant de repondre a Naomie ou avant de reprendre un sprint par type
d'entreprise.

Si le fichier n'existe pas, Codex doit le creer en phase 0 avec le statut
`NO-GO dev`, puis s'arreter au cadrage.

## Champs obligatoires du suivi

Chaque fichier de sprint doit indiquer au minimum :

- `sprint_id` ;
- type d'entreprise ;
- branche cible ;
- pilote ;
- superviseur ;
- phase courante ;
- statut courant ;
- derniere action ;
- prochaine action ;
- blocages ;
- statut NotebookLM ;
- statut audit reutilisation ;
- statut matrice documentaire ;
- statut tickets ;
- statut validation Gad ;
- statut revue associe ;
- decision `GO dev` limitee, si elle existe.

## Phases obligatoires

| Phase | Nom | Statut par defaut | Preuve obligatoire |
| --- | --- | --- | --- |
| 0 | ACCUEIL | `NO-GO dev` | pilote identifie, type confirme |
| 1 | GIT_SETUP | `NO-GO dev` | branche cible connue, Git gere par Codex |
| 2 | SOURCES | `NO-GO dev` | sources et specs listees |
| 3 | NOTEBOOKLM | `NO-GO dev` | questions posees et reponses importees |
| 4 | REUSE_AUDIT | `NO-GO dev` | matrice reutilisation SELARL/global |
| 5 | MATRICE_DOCUMENTAIRE | `NO-GO dev` | documents classes par condition |
| 6 | PARCOURS_METIER | `NO-GO dev` | parcours utilisateur et donnees a saisir |
| 7 | TICKETS | `NO-GO dev` | tickets, criteres, ordre de sprint |
| 8 | VALIDATION_GAD | `NO-GO dev` | validation explicite de Gad |
| 9 | DEV_LIMITE | `GO dev ticket X` | ticket unique et scope borne |
| 10 | SMOKE | `GO test` | tests et smoke internes |
| 11 | ASSOCIE_REVIEW | `NO-GO cloture` | pack de test et retour associe |
| 12 | CORRECTIONS | selon retour | retours classes et traites |
| 13 | CLOTURE | `DONE` ou `PARTIAL` | statut canonique final |

## Gates anti-derapage

| Situation | Reponse obligatoire de Codex |
| --- | --- |
| Naomie dit seulement `Bonjour` dans un contexte Naomie/SELAS | Accueil sprint SELAS, verification branche, point pedagogie, aucun dev |
| Le contexte mentionne Naomi/Naomie mais le message est vague | Traiter comme accueil Naomie, pas comme demande generique |
| Naomie dit `Je veux lancer le sprint X` | Creer/lire le sprint, phase 0, `NO-GO dev`, puis lancer uniquement le sous-sprint NotebookLM |
| Naomie dit `Je veux lancer/demarrer/reprendre le sprint SELAS/CELAS` | Rester dans `SELAS-SOURCES-NOTEBOOKLM-001`, donner le prochain prompt NotebookLM a copier-coller, attendre sa reponse |
| Naomie demande de coder avant NotebookLM | Refuser le dev et lister les gates manquants |
| Gad demande un nouveau type d'entreprise | Ouvrir ou lire le sprint, confirmer `NO-GO dev` par defaut |
| NotebookLM n'a pas ete interroge | Rester avant phase 5, preparer les questions |
| Reuse audit absent | Interdire matrice finale et `GO dev` |
| Matrice documentaire absente | Interdire tickets et dev |
| Gad n'a pas donne de `GO dev` explicite | Interdire le code |
| L'associe n'a pas teste | Interdire cloture 100 % |

## Format de reponse obligatoire a Naomie

Quand Naomie intervient dans un sprint, Codex doit toujours structurer sa
reponse comme ceci :

```text
Statut sprint : [phase] / [NO-GO dev | GO cadrage | GO dev ticket X]
Action maintenant : [une seule action concrete]
Point pedagogie : [explication courte]
Prochaine etape : [ce qu'on fera ensuite]
```

Le point pedagogie est obligatoire a chaque reponse a Naomie.

Reponse interdite dans un contexte Naomie :

```text
Bonjour Naomi ! Je suis pret. Tu veux qu'on attaque quoi dans le moteur documentaire ?
```

Cette reponse est incorrecte car elle saute la verification branche/sprint et ne
declenche ni le `NO-GO dev`, ni le point pedagogie, ni la prochaine etape
NotebookLM.

## Sous-sprint NotebookLM

Pour un sprint pilote par Naomie, le premier sous-sprint operationnel est
NotebookLM. Il est actif avant l'audit de reutilisation, avant la matrice
documentaire, avant les tickets de code et avant toute production.

Quand Naomie dit qu'elle veut lancer, demarrer ou reprendre un sprint, Codex doit
comprendre :

```text
Action autorisee maintenant = lancer le sous-sprint NotebookLM.
Action interdite maintenant = developper, generer, produire, merger, pousser une fonctionnalite.
```

La reponse attendue est donc toujours :

```text
Statut sprint : Phase 3 - NOTEBOOKLM / NO-GO dev
Action maintenant : colle le Prompt NotebookLM NN dans NotebookLM, puis donne-moi la reponse brute.
Point pedagogie : NotebookLM sert a extraire les regles metier ; Codex les structure ensuite avant tout dev.
Prochaine etape : je note ta reponse dans le journal du sprint et je prepare le prompt suivant selon les trous.
```

Codex ne doit pas envoyer une liste globale de questions. Il doit donner un seul
prompt court, compatible avec la limite de caracteres NotebookLM.

Codex ne peut sortir du sous-sprint NotebookLM que si le journal du sprint
contient des reponses structurees suffisantes. Si une reponse cree un trou ou
une contradiction, le prompt suivant doit cibler ce trou, pas passer a la
matrice.

## Regles NotebookLM

NotebookLM est une base de connaissance a interroger largement. Codex ne doit
pas economiser les questions.

Si Codex n'a pas acces direct a NotebookLM, Codex prepare les questions et
demande a Gad ou Naomie de coller les reponses ou un export.

Pour un sprint pilote par Naomie, Codex ne doit pas demander vaguement une
"source NotebookLM". Il doit donner un prompt court a copier-coller, puis
attendre la reponse.

Regles de boucle :

1. un prompt NotebookLM a la fois ;
2. prompt court, compatible avec une limite de caracteres NotebookLM ;
3. reponse NotebookLM structuree par Codex dans le journal du sprint ;
4. prompt suivant choisi selon les manques reels ;
5. aucune economie de questions ;
6. aucune matrice finale avant couverture suffisante.

Chaque reponse NotebookLM doit etre transformee en structure :

- prompt utilise ;
- synthese fiable ;
- documents cites ;
- conditions d'apparition ;
- variables ou donnees ;
- contradictions ;
- informations non trouvees ;
- impact sur le sprint ;
- prochain prompt recommande.

La boucle NotebookLM peut s'arreter seulement quand Codex dispose au minimum de :

- inventaire documentaire SELAS ;
- conditions d'apparition / exclusion ;
- documents manuels, reserves et bloques ;
- differences SELARL / SELAS ;
- roles et gouvernance SELAS ;
- variables et donnees a saisir ;
- points reutilisables / non reutilisables ;
- questions ouvertes explicites.

Aucune reponse NotebookLM ne remplace :

- la source de verite ;
- une source DOCX ;
- une spec `docs/delivery/` ;
- un retour humain valide ;
- une decision explicite de Gad.

## Regles de reutilisation

Avant toute matrice finale et tout `GO dev`, Codex doit appliquer
`docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md`.

La reutilisation doit etre classee :

- `identique` ;
- `reuse-check` ;
- `adapter` ;
- `no-go`.

Un document ou une variable deja traite cote SELARL ne doit pas etre refait sans
raison. Mais il ne doit pas etre copie sans verifier les conditions, les roles,
les variables et les sources applicables au nouveau type.

## Regles Git / branche

Naomie ne gere pas Git.

Codex gere :

- verification de branche ;
- creation ou recuperation de branche ;
- commandes ;
- tests ;
- commits ;
- push, quand Gad le demande ou le valide.

Un sprint Naomie doit utiliser une branche dediee :

```text
codex/naomie-[type-entreprise]-sprint
```

## Regles de mise a jour

Codex doit mettre a jour le fichier de sprint quand :

- le sprint est ouvert ;
- une phase change ;
- un gate est satisfait ;
- un blocage apparait ;
- Gad donne ou retire un `GO dev` ;
- l'associe donne un retour ;
- le sprint est cloture ou reporte.

En fin de ticket, Codex doit aussi mettre a jour :

- `docs/project/01_EXECUTION_BOARD.md` ;
- `docs/project/04_LAST_STATE.md`.

## Regle de blocage

Si un sprint essaie de passer directement en production, generation ou
developpement sans les gates, Codex doit bloquer calmement :

```text
NO-GO dev.
Il manque : [gates manquants].
Action maintenant : [prochaine etape de cadrage].
```

Ce blocage est une protection du projet, pas une erreur de rythme.
