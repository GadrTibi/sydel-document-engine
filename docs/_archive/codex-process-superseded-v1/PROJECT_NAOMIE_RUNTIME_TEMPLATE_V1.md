# Project Naomi runtime template V1

Date : 2026-06-01

## Objet

Ce template sert a creer le protocole local Naomi d'un projet.

Il doit etre recopie dans chaque projet puis rempli avec les informations
specifiques du projet. Il applique la doctrine globale :

- `GLOBAL_NAOMIE_COLLABORATION_PROTOCOL_V1.md`

## A remplir pour chaque projet

```text
Projet :
Superviseur :
Pilote accompagnee :
Role de Codex :

Remote GitHub attendu :
Dossier local possible :
Branche principale :
Branche Naomi :

Mission ou sprint actif :
Phase courante :
Statut courant :
Ticket ou action active :

Fichiers de memoire projet :
- board :
- dernier etat :
- plan :
- handoff :
- protocole local :
- protocole orchestrateur Naomi :
- protocole sync Naomi :
- worklog Naomi :
- dernier rapport Gad :
- messages Gad a transmettre :

Base de connaissance :
Mode d'interrogation :
Journal des reponses :
Sources a trianguler :
- reference projet :
- base de connaissance :
- retour humain :

Prochaine action autorisee :
Actions interdites :

Reponse type si Naomi dit bonjour :
Reponse type si identite inconnue dit bonjour :
Reponse type si Gad s'identifie :
Reponse type si Gad demande ou en est Naomi :
```

## Protocole local minimal

Chaque projet doit definir au minimum :

1. comment demander l'identite si un nouveau chat commence par un simple
   `bonjour` ;
2. comment reconnaitre que Gad est l'interlocuteur superviseur ;
3. comment reconnaitre que Naomi est l'interlocutrice active ;
4. comment verifier le bon depot ;
5. comment verifier la bonne branche ;
6. quel fichier lire pour l'etat courant ;
7. quelle action donner a Naomi ;
8. quel point pedagogie donner ;
9. quelles actions sont interdites tant que le gate n'est pas passe.
10. ou journaliser les reponses de base de connaissance ;
11. quel pack actif transmettre a un humain ;
12. quelles questions sont deja resolues par les sources et ne doivent pas etre
    reposees.
13. ou lire le worklog Naomi ;
14. comment repondre a Gad sans demander a Naomi un statut oral.
15. comment noter le dernier rapport Gad ;
16. ou conserver les messages Gad a transmettre a Naomi.
17. comment produire un commit/push ou un `Sync packet` quand une phase avance
    dans le thread Naomi.

## Reponse type identite inconnue

```text
Bonjour, tu es Gad ou Naomi ?
Je te route ensuite sur le bon protocole projet.
```

## Reponse type Gad

```text
Statut projet : [nom projet] / supervision Gad / [phase]
Action maintenant : [action de pilotage ou cadrage demandee par Gad]
Point de controle : [gate, branche, sprint ou decision utile]
Prochaine etape : [suite immediate]
```

## Reponse type statut du flux Naomi pour Gad

```text
Statut flux Naomi : [projet] / [sprint ou mission] / [phase] / [GO ou NO-GO]
Avancement depuis le dernier point : [1 a 3 faits utiles du flux]
Prochaine etape : [une action concrete]
Blocage / risque : [aucun ou blocage principal]
Fiabilite : [OK / suivi a rattraper / source manquante]
```

Le rapport detaille, avec branche, sources lues, curseur exact et separation
Naomi/Codex/outils, est reserve a une demande explicite d'audit.

Si l'avancee est annoncee par Gad ou Naomi mais absente des traces publiees,
repondre `avancee annoncee, synchronisation manquante` et demander le checkpoint
de `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md`.

## Message Gad a transmettre type

```text
Message de Gad :
"[message exact]"
```

Apres transmission, marquer le message `transmis` dans le worklog Naomi.

## Reponse type generique

```text
Statut projet : [nom projet] / [phase] / [GO ou NO-GO]
Action maintenant : [une seule action concrete]
Point pedagogie : [explication courte]
Prochaine etape : [suite immediate]
```

## Blocage type mauvaise branche

```text
Statut projet : CONTEXTE BRANCHE A CORRIGER / NO-GO dev
Action maintenant : je dois verifier ou rejoindre la branche [branche].
Point pedagogie : le dossier local n'est pas la preuve ; la branche determine le rail de travail.
Prochaine etape : je gere Git, puis je reprends le sprint depuis le dernier etat.
```

## Blocage type mauvais depot

```text
Statut projet : MAUVAIS DEPOT / NO-GO dev
Action maintenant : je dois verifier le remote attendu avant toute suite.
Point pedagogie : le remote indique a quel projet GitHub ce dossier appartient.
Prochaine etape : ouvrir ou cloner le bon projet, puis relire la memoire projet.
```

## Base de connaissance type

```text
Action maintenant : copie le Prompt 01 dans [base de connaissance], puis colle-moi la reponse brute.
Point pedagogie : la base sert a extraire les regles ; Codex les structure ensuite avant tout plan ou dev.
Prochaine etape : je note la reponse dans le journal et je prepare le prompt suivant selon les trous.
```

## Revue humaine type

```text
Action maintenant : transmets uniquement le pack actif [pack] et le brief [brief].
Point pedagogie : l'humain ne doit pas repondre a des questions abstraites deja tranchees par les sources ; il valide ou annote des ecarts concrets.
Prochaine etape : Codex classe les retours, ouvre un ticket borne si besoin, regenere un nouveau pack, puis met a jour le statut canonique.
```

## Checklist d'installation locale

Codex doit verifier :

- `git remote -v` ;
- branche active ;
- statut local ;
- presence des fichiers de memoire ;
- presence du fichier runtime local ;
- presence du protocole orchestrateur Naomi ;
- presence du worklog Naomi du sprint ;
- date du dernier rapport Gad ;
- messages Gad en attente ;
- derniere action officielle ;
- prochain gate.
- pack actif et packs remplaces ;
- journal des reponses de base de connaissance.

Naomi ne doit pas executer ces commandes elle-meme.

## Definition de reprise correcte

Un nouveau chat est correctement cadre si, apres lecture du protocole local, il
peut repondre sans demander a Gad :

- quel projet est actif ;
- qui parle ;
- quelle branche utiliser ;
- quelle phase est en cours ;
- quelle action donner a Naomi ;
- ce qui est interdit ;
- quel fichier mettre a jour ensuite.
