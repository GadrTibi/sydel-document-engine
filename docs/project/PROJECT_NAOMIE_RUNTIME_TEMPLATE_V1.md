# Project Naomie runtime template V1

Date : 2026-06-01

## Objet

Ce template sert a creer le protocole local Naomie d'un projet.

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
Branche Naomie :

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

Base de connaissance :
Mode d'interrogation :
Journal des reponses :

Prochaine action autorisee :
Actions interdites :

Reponse type si Naomie dit bonjour :
```

## Protocole local minimal

Chaque projet doit definir au minimum :

1. comment reconnaitre que Naomie est dans le contexte ;
2. comment verifier le bon depot ;
3. comment verifier la bonne branche ;
4. quel fichier lire pour l'etat courant ;
5. quelle action donner a Naomie ;
6. quel point pedagogie donner ;
7. quelles actions sont interdites tant que le gate n'est pas passe.

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

## Checklist d'installation locale

Codex doit verifier :

- `git remote -v` ;
- branche active ;
- statut local ;
- presence des fichiers de memoire ;
- presence du fichier runtime local ;
- derniere action officielle ;
- prochain gate.

Naomie ne doit pas executer ces commandes elle-meme.

## Definition de reprise correcte

Un nouveau chat est correctement cadre si, apres lecture du protocole local, il
peut repondre sans demander a Gad :

- quel projet est actif ;
- qui parle ;
- quelle branche utiliser ;
- quelle phase est en cours ;
- quelle action donner a Naomie ;
- ce qui est interdit ;
- quel fichier mettre a jour ensuite.
