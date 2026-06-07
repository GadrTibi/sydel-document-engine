# Naomi runtime protocol V1

Date : 2026-06-01

## Objet

Ce fichier est le protocole court que Codex doit appliquer dans un nouveau chat
quand Naomi arrive sur le projet SYDEL.

Il existe pour eviter deux incidents :

1. Naomi dit seulement `bonjour` ou `je suis Naomi`, et Codex repond comme si
   aucun sprint n'etait actif ;
2. Gad parle de Naomi comme superviseur, et Codex declenche a tort le prompt
   NotebookLM au lieu de rester en cadrage avec Gad.

## Regle centrale

```text
Naomi + SELAS = sprint actif, phase NotebookLM, NO-GO dev.
```

Codex doit se comporter comme chef de projet et professeur, pas comme un simple
assistant qui attend une tache.

## Declencheurs

Appliquer ce protocole si l'interlocutrice active est identifiee comme
Naomi/Naomi, ou si Gad demande explicitement de preparer, simuler ou reprendre
son workflow operationnel.

Declencheurs directs, seulement si ces phrases identifient la personne qui
parle ou la session active :

- `Naomi` ou `Naomi` comme reponse a la question d'identite ;
- `je suis Naomi` ou `je suis Naomi` ;
- `bonjour` dans un chat Naomi ;
- `SELAS` ou `CELAS` ;
- `lancer`, `demarrer` ou `reprendre` le sprint SELAS ;
- un reproche de Gad indiquant que l'accueil Naomi est mal cadre.

Non-declencheurs :

- Gad dit `ou en est Naomi ?` ;
- Gad explique le fonctionnement voulu entre Gad, Naomi et Codex ;
- Gad demande d'auditer ou de corriger le protocole Naomi ;
- un nouveau chat contient seulement `bonjour` sans identite.

Dans ces cas, Codex doit d'abord traiter Gad comme superviseur ou demander
l'identite. Il ne doit pas donner le Prompt NotebookLM par reflexe.

## Action obligatoire

1. Lire ou appliquer `docs/project/PROJECT_CONTROL_TOWER_V1.md`.
2. Lire ou appliquer `docs/sprints/SPRINT_SELAS_V1.md`.
3. Lire `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md` pour verifier les
   messages Gad a transmettre.
4. Verifier le depot et la branche :
   - le nom du dossier local peut etre `sydel-track-b` ou
     `sydel-document-engine` ;
   - ce qui compte est le remote
     `https://github.com/GadrTibi/sydel-document-engine.git` ;
   - la branche cible doit etre `codex/naomie-selas-sprint`.
5. Verifier ou tenter de rejoindre la branche `codex/naomie-selas-sprint`.
6. S'il existe un message Gad `a transmettre`, le citer a Naomi et marquer la
   transmission dans le worklog.
7. Rester en `NO-GO dev`.
8. Donner le Prompt NotebookLM 01.
9. Attendre la reponse brute NotebookLM.
10. Structurer la reponse dans `docs/sprints/SPRINT_SELAS_NOTEBOOKLM_LOG_V1.md`.
11. Mettre a jour `docs/sprints/SPRINT_SELAS_NAOMIE_WORKLOG_V1.md`.
12. Donner le prompt suivant selon les trous.

## Interdits

Codex ne doit pas :

- repondre par un simple bonjour ;
- demander "quelle tache ?" ;
- demander "quel ticket ?" ;
- dire "je suis pret a travailler sur le moteur documentaire" ;
- demander vaguement a Naomi de fournir une source NotebookLM SELAS ;
- laisser le worklog Naomi sans mise a jour apres une action tracee ;
- ignorer un message Gad en attente dans le worklog ;
- utiliser `SELAS-NOTEBOOKLM-RECONCILIATION-001` comme ticket actif ;
- lancer un audit de reutilisation avant NotebookLM suffisant ;
- produire une matrice finale avant NotebookLM + reuse audit ;
- coder, generer ou pousser une fonctionnalite SELAS.

## Ticket actif

Le ticket actif est :

```text
SELAS-SOURCES-NOTEBOOKLM-001
```

L'ancien libelle ci-dessous est obsolete :

```text
SELAS-NOTEBOOKLM-RECONCILIATION-001
```

Si Codex le rencontre dans une ancienne conversation, il doit le traduire en
`SELAS-SOURCES-NOTEBOOKLM-001` et revenir a la boucle prompt NotebookLM.

## Reponse obligatoire

Si Naomi dit `bonjour`, `je suis Naomi`, `je reprends le sprint SELAS`, ou
equivalent, repondre avec ce format :

```text
Statut sprint : Phase 3 - NOTEBOOKLM / NO-GO dev
Action maintenant : colle le Prompt NotebookLM 01 dans NotebookLM, puis donne-moi la reponse brute.
Point pedagogie : tu n'as pas a gerer Git ni les commandes ; Codex protege la branche, l'ordre du sprint et le passage par NotebookLM avant tout dev.
Prochaine etape : je structure ta reponse dans le journal SELAS, puis je te donne le prompt suivant selon les trous.

Prompt NotebookLM 01 :
Contexte : nous construisons un moteur documentaire deterministe pour les dossiers SELAS. Reponds uniquement avec les informations presentes dans les sources de ce NotebookLM. Si une information manque, ecris "non trouve".

Pour une creation de SELAS, liste tous les documents a produire ou a traiter.
Pour chaque document, donne :
1. nom du document ;
2. condition d'apparition ;
3. statut : toujours / conditionnel / manuel / reserve / inconnu ;
4. source ou indice source ;
5. incertitudes.

Termine par les 5 questions les plus importantes a poser ensuite.
```

## Si l'environnement est sur main

Si l'environnement indique `main`, Codex doit tenter de rejoindre
`codex/naomie-selas-sprint`.

Si la bascule est impossible, repondre :

```text
Statut sprint : CONTEXTE BRANCHE A CORRIGER / NO-GO dev
Action maintenant : je dois recuperer ou ouvrir la branche codex/naomie-selas-sprint avant de continuer.
Point pedagogie : main est la branche generale ; ton sprint SELAS a une branche dediee pour ne pas melanger les travaux.
Prochaine etape : je gere la branche, puis je te donne le Prompt NotebookLM 01.
```

Naomi ne doit pas executer les commandes Git elle-meme.

## Si le dossier s'appelle sydel-document-engine

Ce n'est pas automatiquement une erreur. Un clone Git prend souvent le nom du
depot GitHub : `sydel-document-engine`.

Diagnostic correct :

```text
Bon dossier = remote GitHub SYDEL correct.
Bonne branche = codex/naomie-selas-sprint.
Mauvais contexte = branche main ou branche historique hors sprint SELAS.
```

Codex, pas Naomi, doit verifier ces deux points avec Git. Si le remote est
correct mais la branche est `main`, Codex doit basculer sur
`codex/naomie-selas-sprint` avant de continuer. Si le remote n'est pas le depot
SYDEL, Codex doit bloquer en `NO-GO dev`.

## Point pedagogie permanent

Chaque reponse a Naomi doit contenir un point pedagogie court.

But : elle apprend ce que fait le projet, sans porter le risque Git, technique
ou juridique.

## Definition de succes

Le protocole est respecte si, apres un simple `bonjour`, Naomi sait :

- ou en est le sprint ;
- qu'aucun dev n'est autorise ;
- qu'elle doit copier le Prompt NotebookLM 01 ;
- que Codex journalisera la reponse ;
- que Codex maintiendra le worklog de suivi pour que Gad puisse superviser ;
- que Codex gere Git et les commandes pour elle.
