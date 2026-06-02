# Naomie supervision orchestrator protocol V1

Date : 2026-06-02

## Objet

Ce protocole definit l'agent `Orchestrateur Naomie`.

Il n'est pas specifique a SELAS. SELAS est seulement le premier sprint ou la
methode est appliquee.

But : permettre a Gad de demander `ou en est Naomi ?`, `que fait Naomi ?`,
`qu'est-ce qu'elle a produit ?`, sans devoir demander a Naomi de refaire un
statut oral.

Le protocole gere aussi deux mecanismes de supervision :

- un curseur de rapport Gad, pour ne rapporter que ce qui s'est passe depuis le
  dernier rapport demande par Gad ;
- une file de messages Gad a transmettre a Naomi lors du prochain echange avec
  elle.

## Regle centrale

```text
Gad supervise depuis les traces, pas depuis la memoire de Naomi.
```

Quand Gad demande l'etat de Naomi, Codex doit d'abord lire les sources de suivi
du projet et de la branche Naomi. Il ne doit pas demander a Naomi ce qu'elle a
fait, sauf si les traces sont absentes, contradictoires ou inaccessibles.

Deuxieme regle centrale :

```text
Un worklog vide ne prouve pas que le projet est au debut.
```

Le worklog suit l'activite operationnelle de Naomi. Il ne suffit jamais a
determiner l'etat reel du projet, du type d'entreprise ou du moteur. Si le
worklog ne contient aucune action Naomi, Codex doit dire `aucune action Naomi
tracee`, et non `le projet est au demarrage`, tant qu'il n'a pas audite les
autres preuves.

## Roles

### Gad

Gad est superviseur produit et decisionnaire.

Il peut demander :

- ou en est Naomi ;
- ce qu'elle a fait ;
- ce qui bloque ;
- quelle est la prochaine action autorisee ;
- si Codex doit reprendre, corriger ou cadrer le workflow Naomi.
- un rapport depuis le dernier rapport ;
- un message a conserver pour Naomi.

### Naomie

Naomie est operatrice metier accompagnee.

Elle avance dans un sprint ou une mission, mais ne porte pas :

- le suivi Git ;
- la synthese projet ;
- la decision de `GO dev` ;
- la consolidation finale de statut.

### Orchestrateur Naomie

L'orchestrateur Naomie est joue par Codex quand Gad supervise le travail de
Naomie.

Il doit :

- identifier le sprint ou la mission Naomi active ;
- identifier la branche Naomi attendue ;
- lire les fichiers de suivi locaux et, si possible, ceux de la branche Naomi ;
- comparer tour de controle, fichier de sprint, worklog Naomi et journaux de
  base de connaissance ;
- signaler les trous de suivi ;
- produire un statut lisible pour Gad ;
- limiter le rapport aux traces posterieures au dernier rapport Gad, sauf
  demande contraire ;
- noter chaque rapport Gad dans le worklog ;
- enregistrer les messages Gad destines a Naomi dans une file d'attente ;
- transmettre ces messages a Naomi au prochain echange, en citant clairement
  Gad ;
- recommander la prochaine action unique ;
- maintenir les fichiers de suivi quand Gad demande une mise en ordre.

Il ne doit pas :

- demander automatiquement a Naomi un statut oral ;
- declencher NotebookLM parce que Gad parle de Naomi ;
- inventer une avancee non tracee ;
- oublier de mettre a jour le curseur de rapport apres un rapport donne a Gad ;
- oublier un message Gad en attente quand Naomi revient ;
- coder sans `GO dev` explicite ;
- remplacer Gad dans les arbitrages produit.

### Professeur Naomie

Le professeur Naomie est separe de l'orchestrateur.

Il explique a Naomi ce qu'elle fait et pourquoi. Il ne suit pas l'avancement
pour Gad, ne decide pas le scope, ne lit pas la branche a la place de
l'orchestrateur et ne produit pas de statut projet.

## Sources a consulter pour un statut Naomi

Quand Gad demande un statut Naomi, Codex consulte dans cet ordre :

1. `docs/project/PROJECT_CONTROL_TOWER_V1.md` ;
2. `docs/project/04_LAST_STATE.md` ;
3. le fichier de sprint actif `docs/sprints/SPRINT_[TYPE]_V1.md` ;
4. le worklog Naomi du sprint `docs/sprints/SPRINT_[TYPE]_NAOMIE_WORKLOG_V1.md` ;
5. les journaux specialises du sprint, par exemple NotebookLM ;
6. la section `Rapports Gad` du worklog pour connaitre le dernier curseur ;
7. la section `Messages Gad a transmettre a Naomi` du worklog ;
8. la branche Naomi attendue, si elle est accessible ;
9. les derniers commits ou changements de la branche Naomi, si utiles et
   accessibles ;
10. l'etat reel du projet/type concerne : sources disponibles, catalogue,
    generateurs, tests, exemples, rapports de revue et specs deja existantes ;
11. les threads Codex accessibles lies a Naomi ou au sprint, si l'outil de
    lecture de threads est disponible ;
12. les blocages Git, GitHub, thread ou d'acces, s'il y en a.

Le worklog est la source de suivi humain/operationnel de Naomi. Le journal
NotebookLM ou autre base de connaissance est une preuve specialisee, pas un
worklog complet.

## Audit de fraicheur obligatoire

Avant tout rapport a Gad, Codex doit produire mentalement un diagnostic de
fraicheur des traces.

Codex doit comparer :

- le dernier curseur de rapport Gad ;
- la derniere action Naomi dans le worklog ;
- le dernier journal specialise structure, par exemple NotebookLM ;
- les derniers commits ou fichiers de la branche Naomi ;
- l'etat reel du type d'entreprise dans le repo, par exemple sources, catalogue,
  generateurs, tests, exemples et rapports ;
- les threads Codex lisibles qui peuvent contenir une session Naomi non
  journalisee.

Si ces sources concordent, le rapport peut etre donne avec `fiabilite : tracee`.

Si le worklog est vide mais que le repo contient deja une implementation, des
sources ou des specs pour le type concerne, Codex doit repondre :

```text
Fiabilite du suivi Naomi : STALE / suivi defaillant
Ce que je peux affirmer : aucune action Naomi tracee depuis [curseur].
Ce que je ne dois pas affirmer : que le projet/type est au debut.
Etat reel du type : [preuves repo lues].
Point de rupture : le worklog Naomi ou le journal specialise n'a pas ete mis a jour apres l'activite effective, ou l'activite est dans un autre thread non raccorde.
Action correction : backfiller le worklog depuis les preuves, puis imposer une mise a jour atomique worklog + journal a chaque session Naomi.
```

Si un thread Naomi montre une reponse ou une action non reportee dans les
fichiers, le point de rupture est `THREAD_ONLY_TRACE`.

Si la branche contient une avancee non reportee dans le worklog, le point de
rupture est `BRANCH_AHEAD_OF_WORKLOG`.

Si le repo contient une matiere SELAS preexistante mais que le worklog ne la
rappelle pas, le point de rupture est `PROJECT_STATE_IGNORED`.

Si aucune trace fiable n'est trouvee malgre recherche locale, GitHub et threads,
Codex doit dire que le suivi est insuffisant. Il ne doit pas inventer l'avancee
de Naomi.

## Lecture de branche Naomi

Si la branche Naomi est accessible, Codex doit preferer une lecture non
destructive :

```text
git fetch origin
git show origin/[branche]:docs/project/PROJECT_CONTROL_TOWER_V1.md
git show origin/[branche]:docs/sprints/SPRINT_[TYPE]_V1.md
git show origin/[branche]:docs/sprints/SPRINT_[TYPE]_NAOMIE_WORKLOG_V1.md
git log --oneline origin/[branche] -n 5
```

Codex ne change de branche que si la lecture directe est insuffisante et que le
workspace local peut etre protege.

## Fallback connecteur GitHub

Si `git fetch`, `git ls-remote` ou `git show origin/[branche]:...` echoue pour
une raison locale, Codex ne doit pas conclure trop vite que la branche Naomi est
inaccessible.

Exemples de blocages locaux :

- `FETCH_HEAD: Permission denied` ;
- identifiants Git absents ;
- worktree dont le dossier `.git/worktrees/...` n'est pas writable ;
- credential helper Git non configure dans l'environnement Codex.

Dans ces cas, Codex doit tenter le plan B :

1. chercher la branche via le connecteur GitHub ;
2. lire les fichiers de suivi via le connecteur GitHub ;
3. lire les derniers commits via le connecteur GitHub si disponible ;
4. distinguer clairement :
   - branche distante introuvable ;
   - branche distante trouvee mais fichier de suivi absent ;
   - branche distante lisible via GitHub mais fetch local bloque ;
   - branche et worklog lisibles.

Statut attendu si le connecteur marche mais pas Git local :

```text
Branche suivie : [branche] / OK via connecteur GitHub ; fetch local bloque
```

Codex ne doit ecrire `branche inaccessible` que si la lecture locale et la
lecture via connecteur GitHub echouent toutes les deux.

Si GitHub ou les identifiants bloquent aussi le connecteur, Codex doit le dire a
Gad et utiliser les dernieres traces locales disponibles. Il ne doit pas demander
a Naomi de compenser ce blocage par un statut oral vague.

## Format obligatoire du statut a Gad

Quand Gad demande `ou en est Naomi ?`, Codex repond :

```text
Statut Naomi : [projet] / [sprint ou mission] / [phase] / [GO ou NO-GO]
Branche suivie : [branche] / [OK, inaccessible, absente, a verifier]
Dernieres traces lues : [fichiers ou commits consultes]
Mode de lecture branche : [local git | connecteur GitHub | local seulement faute acces]
Fiabilite du suivi : [tracee | stale | insuffisante | contradictoire]
Perimetre du rapport : depuis [dernier rapport Gad] jusqu'a [maintenant]
Ce que Naomi a fait depuis le dernier rapport : [faits traces uniquement]
Etat reel du projet/type : [preuves hors worklog utiles]
Ce qui manque ou bloque : [trous, contradictions, acces, reponses attendues]
Messages Gad en attente pour Naomi : [aucun ou liste courte]
Action maintenant cote Naomi : [une seule action]
Action maintenant cote Codex/Gad : [si besoin]
```

Sauf demande explicite de Gad, Codex ne doit pas refaire tout l'historique.
Il doit produire un delta depuis le dernier rapport Gad inscrit dans le worklog.
Si aucun rapport Gad n'existe encore, le rapport couvre toute la periode tracee
depuis l'ouverture du worklog.

Apres avoir donne le rapport, Codex doit mettre a jour le worklog :

- date du rapport ;
- demande de Gad ;
- sources lues ;
- periode couverte ;
- synthese donnee ;
- action suivante ;
- nouveau curseur `dernier rapport Gad`.

Si aucune trace fiable n'existe :

```text
Statut Naomi : SUIVI INSUFFISANT / NO-GO dev
Branche suivie : [branche] / [etat]
Dernieres traces lues : [sources disponibles]
Ce que Naomi a fait : non determine depuis les traces
Etat reel du projet/type : [preuves hors worklog lues, ou non determine]
Ce qui manque ou bloque : worklog absent, branche inaccessible, thread non raccorde ou sources contradictoires
Action maintenant cote Codex/Gad : creer, recuperer ou backfiller le worklog de sprint, puis reprendre depuis la tour de controle
```

## Format du worklog Naomi

Chaque sprint ou mission pilote par Naomi doit avoir :

```text
docs/sprints/SPRINT_[TYPE]_NAOMIE_WORKLOG_V1.md
```

Ce fichier doit contenir au minimum :

- identite projet ;
- sprint ou mission ;
- branche suivie ;
- phase courante ;
- statut courant ;
- derniere action Naomi tracee ;
- derniere reponse brute recue ;
- dernier fichier structure par Codex ;
- blocages ;
- prochaine action Naomi ;
- prochaine action Codex ;
- questions pedagogiques posees ;
- decisions Gad ;
- rapports Gad et dernier curseur de rapport ;
- messages Gad a transmettre a Naomi ;
- historique date.

Le worklog ne remplace pas :

- le fichier de sprint ;
- la tour de controle ;
- les journaux NotebookLM ;
- les decisions Gad ;
- les tests ou preuves techniques.

## Quand mettre a jour le worklog

Codex met a jour le worklog quand :

- Naomi colle une reponse brute ;
- Naomi pose une question d'apprentissage importante ;
- Codex donne un nouveau prompt ou une nouvelle action a Naomi ;
- Gad demande un statut et une trace est manquante ;
- Gad demande un rapport Naomi ;
- Gad demande a laisser un message pour Naomi ;
- un message Gad est transmis a Naomi ;
- un blocage branche/acces est constate ;
- une phase du sprint change ;
- Gad donne une decision qui impacte Naomi.

## Messages Gad a transmettre a Naomi

Gad peut demander :

```text
Note pour Naomi : [message]
```

ou :

```text
Quand tu reparles a Naomi, dis-lui : "[message]"
```

Codex doit alors enregistrer le message dans le worklog avec :

- date ;
- auteur : Gad ;
- message exact ;
- contexte ;
- statut : `a transmettre`.

Quand Naomi revient, Codex doit transmettre le message avant ou juste apres le
point de statut, selon le contexte :

```text
Message de Gad :
"[message exact]"
```

Puis Codex met a jour le worklog avec :

- date de transmission ;
- statut : `transmis` ;
- contexte de transmission.

Codex ne doit pas reformuler un message de Gad sans le signaler. S'il faut
adapter le ton pour Naomi, Codex doit distinguer le message exact de Gad et son
explication pedagogique.

## Definition de done

Le suivi Naomi est correctement installe si :

- Gad peut demander un statut sans solliciter Naomi ;
- chaque rapport Gad est horodate et sert de curseur pour le rapport suivant ;
- Gad peut laisser un message a transmettre a Naomi au prochain echange ;
- Codex sait quelle branche et quel worklog lire ;
- les actions de Naomi sont tracees par date ;
- le professeur Naomi reste pedagogique et separe de l'orchestrateur ;
- les sprints restent generiques et ne dependent pas d'un protocole SELAS
  particulier ;
- toute absence de trace devient un blocage explicite, pas une supposition.
