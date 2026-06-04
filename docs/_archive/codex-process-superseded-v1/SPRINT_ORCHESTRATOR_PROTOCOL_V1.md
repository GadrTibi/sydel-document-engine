# Sprint orchestrator protocol V1

Date : 2026-06-01

## Objet

Ce document definit l'orchestrateur de sprint operationnel pour les sprints par
type d'entreprise.

Il s'inscrit sous la tour de controle globale
`docs/project/PROJECT_CONTROL_TOWER_V1.md`, qui indique quel sprint est actif,
quelle phase est en cours et quelle action est autorisee maintenant.

Pour Naomi/SELAS, appliquer aussi le protocole court prioritaire
`docs/project/NAOMIE_RUNTIME_PROTOCOL_V1.md`.

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
avant de repondre a Naomi ou avant de reprendre un sprint par type
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
- worklog Naomi si le sprint est pilote par Naomi ;
- dernier rapport Gad et messages Gad en attente si le sprint est pilote par
  Naomi ;
- statut NotebookLM ;
- statut audit reutilisation ;
- statut matrice documentaire ;
- statut tickets ;
- statut validation Gad ;
- statut revue associe ;
- pack actif et packs remplaces ;
- statut audit fidelite source ;
- statut audit trois sources ;
- questions humaines deja resolues par les sources ;
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
| 11 | SOURCE_FIDELITY | `NO-GO cloture` | pack actif, controle source et audit trois sources |
| 12 | ASSOCIE_REVIEW | `NO-GO cloture` | brief d'ecarts concrets et retour associe |
| 13 | CORRECTIONS | selon retour | retours classes et traites |
| 14 | CLOTURE | `DONE` ou `PARTIAL` ou `BLOCKED` | statut canonique final |

## Gates anti-derapage

| Situation | Reponse obligatoire de Codex |
| --- | --- |
| Nouveau chat : `Bonjour` sans identite | Demander `Bonjour, tu es Gad ou Naomi ? Je te route ensuite sur le bon protocole projet.` Aucun sprint, aucune tache, aucun NotebookLM avant identification |
| Gad parle de Naomi/Naomi, SELAS ou du protocole | Traiter Gad comme superviseur produit ; ne pas declencher NotebookLM sauf demande explicite de simulation/preparation/reprise du workflow Naomi |
| Gad demande ou en est Naomi | Appliquer `NAOMIE_SUPERVISION_ORCHESTRATOR_PROTOCOL_V1.md` + `WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`, lire les traces/worklog/branche, puis repondre sur le flux Naomi sans demander un statut oral a Naomi |
| Gad demande un rapport Naomi | Produire un rapport boss court differentiel depuis le dernier rapport Gad inscrit dans le worklog, puis mettre a jour le curseur |
| Gad laisse un message pour Naomi | Enregistrer le message exact dans le worklog avec statut `a transmettre`; le citer au prochain echange avec Naomi puis le marquer `transmis` |
| Naomi dit seulement `Bonjour` apres identification comme Naomi/SELAS | Accueil sprint SELAS, verification branche, point pedagogie, Prompt NotebookLM 01, aucun dev |
| L'interlocutrice active est Naomi/Naomi mais le message est vague | Traiter comme accueil Naomi, pas comme demande generique |
| Naomi dit `Je veux lancer le sprint X` | Creer/lire le sprint, phase 0, `NO-GO dev`, puis lancer uniquement le sous-sprint NotebookLM |
| Naomi dit `Je veux lancer/demarrer/reprendre le sprint SELAS/CELAS` | Rester dans `SELAS-SOURCES-NOTEBOOKLM-001`, donner le prochain prompt NotebookLM a copier-coller, attendre sa reponse |
| Naomi demande de coder avant NotebookLM | Refuser le dev et lister les gates manquants |
| Gad demande un nouveau type d'entreprise | Ouvrir ou lire le sprint, confirmer `NO-GO dev` par defaut |
| NotebookLM n'a pas ete interroge | Rester avant phase 5, preparer les questions |
| Reuse audit absent | Interdire matrice finale et `GO dev` |
| Matrice documentaire absente | Interdire tickets et dev |
| Gad n'a pas donne de `GO dev` explicite | Interdire le code |
| Pack actif non identifie apres correction | Interdire la revue associe |
| Audit trois sources absent avant revue finale | Interdire la cloture 100 % |
| Question humaine deja resolue par source/spec | Ne pas poser la question, noter la decision source |
| L'associe n'a pas teste | Interdire cloture 100 % |

## Format de reponse obligatoire a Naomi

Quand Naomi intervient dans un sprint, Codex doit toujours structurer sa
reponse comme ceci :

```text
Statut sprint : [phase] / [NO-GO dev | GO cadrage | GO dev ticket X]
Action maintenant : [une seule action concrete]
Point pedagogie : [explication courte]
Prochaine etape : [ce qu'on fera ensuite]
```

Le point pedagogie est obligatoire a chaque reponse a Naomi.

Pour Naomi/SELAS, un simple `bonjour` suffit a declencher le Prompt NotebookLM
01 seulement si l'interlocutrice active est deja identifiee comme Naomi/Naomi.
Si l'identite est inconnue, Codex doit d'abord demander si la personne est Gad
ou Naomi. Codex ne doit pas attendre que Naomi choisisse une tache apres son
identification.

Reponse interdite dans un contexte Naomi :

```text
Bonjour Naomi ! Je suis pret. Tu veux qu'on attaque quoi dans le moteur documentaire ?
```

Cette reponse est incorrecte car elle saute la verification branche/sprint et ne
declenche ni le `NO-GO dev`, ni le point pedagogie, ni la prochaine etape
NotebookLM.

## Sous-sprint NotebookLM

Pour un sprint pilote par Naomi, le premier sous-sprint operationnel est
NotebookLM. Il est actif avant l'audit de reutilisation, avant la matrice
documentaire, avant les tickets de code et avant toute production.

Quand Naomi dit qu'elle veut lancer, demarrer ou reprendre un sprint, Codex doit
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
demande a Gad ou Naomi de coller les reponses ou un export.

Pour un sprint pilote par Naomi, Codex ne doit pas demander vaguement une
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

Chaque avance du flux Naomi doit aussi mettre a jour le worklog du sprint.
Ce suivi est porte par l'Agent de tracabilite de flux
`docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`, pas par Naomi :

- dernier avancement du flux ;
- reponse brute recue ;
- fichier structure par Codex ;
- blocages ;
- prochaine action Naomi ;
- prochaine action Codex ;
- decision Gad si elle existe.
- message Gad transmis ou encore en attente.

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

## Regles de fidelite source et retours humains

La lecon SELARL est obligatoire pour les prochains sprints : Codex ne doit pas
demander a l'humain de confirmer ce que les sources disent deja. Avant de
solliciter Gad ou l'associe, Codex doit d'abord verifier :

- le document de reference qui liste les documents a produire ;
- les notes NotebookLM / modele deja structurees ;
- les sources DOCX et specs disponibles ;
- les retours humains deja versionnes ou fournis.

Les questions humaines autorisees sont uniquement :

- ecart concret dans un DOCX produit ;
- contradiction entre sources ;
- source absente ;
- variable mal injectee ;
- document absent, en trop, manuel ou reserve a arbitrer ;
- choix de scope.

Avant une revue associe, le sprint doit avoir :

- un pack actif numerote ;
- un manifest ou une liste des documents attendus ;
- un brief de revue limite aux ecarts ;
- les anciens packs marques comme remplaces ;
- un audit trois sources si le perimetre touche des documents juridiques
  sensibles.

Si une correction est faite apres retour humain, Codex doit regenerer un nouveau
pack, relancer les controles cibles et mettre a jour le fichier de sprint avant
de redemander une validation.

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

Naomi ne gere pas Git.

Codex gere :

- verification de branche ;
- creation ou recuperation de branche ;
- commandes ;
- tests ;
- commits ;
- push, quand Gad le demande ou le valide.

Un sprint Naomi doit utiliser une branche dediee :

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
