# Naomi supervision orchestrator protocol V1

Date : 2026-06-02

## Objet

Ce protocole definit l'agent `Orchestrateur Naomi`.

Il n'est pas specifique a SELAS. SELAS est seulement le premier sprint ou la
methode est appliquee.

La place de cet agent dans la pyramide projet est definie dans
`docs/project/PROJECT_AGENT_ORG_CHART_V1.md`.

La tracabilite du flux est definie dans
`docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`.

La synchronisation entre le thread Gad, le thread Naomi et la branche est
definie dans `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md`.

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
Gad demande l'etat du flux Naomi, pas une evaluation personnelle de Naomi.
```

Si le sprint, la branche, Codex, un sous-agent ou un outil avance dans le
perimetre pilote par Naomi, cela remonte comme avancement du flux Naomi pour
le rapport Gad.

Troisieme regle centrale :

```text
Un worklog vide ne prouve pas que le flux est au debut.
```

Le worklog suit l'activite operationnelle du flux. Il ne suffit jamais a
determiner l'etat reel du projet, du type d'entreprise ou du moteur. Si le
worklog est vide ou stale, Codex doit activer l'Agent de tracabilite de flux et
son mode de rattrapage retroactif.

Quatrieme regle centrale :

```text
Une avancee annoncee mais absente de la branche et du worklog est un probleme
de synchronisation, pas une preuve d'absence de travail.
```

Si Gad sait que Naomi a termine ou avance une phase mais que Codex ne voit pas
cette avancee dans les traces publiees, Codex doit appliquer
`NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md` et demander un checkpoint de
synchronisation. Il ne doit pas relancer NotebookLM ni conclure que le flux est
au debut.

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

### Naomi

Naomi est operatrice metier accompagnee.

Elle avance dans un sprint ou une mission, mais ne porte pas :

- le suivi Git ;
- la tracabilite du flux ;
- la synthese projet ;
- la decision de `GO dev` ;
- la consolidation finale de statut.

### Orchestrateur Naomi

L'orchestrateur Naomi est joue par Codex quand Gad supervise le travail de
Naomi.

Il doit :

- identifier le sprint ou la mission Naomi active ;
- identifier la branche Naomi attendue ;
- lire les fichiers de suivi locaux et, si possible, ceux de la branche Naomi ;
- comparer tour de controle, fichier de sprint, worklog Naomi et journaux de
  base de connaissance ;
- signaler les trous de suivi ;
- produire un statut lisible pour Gad ;
- detecter les ruptures de synchronisation entre thread Naomi, worklog et
  branche ;
- limiter le rapport aux traces posterieures au dernier rapport Gad, sauf
  demande contraire ;
- noter chaque rapport Gad dans le worklog ;
- enregistrer les messages Gad destines a Naomi dans une file d'attente ;
- transmettre ces messages a Naomi au prochain echange, en citant clairement
  Gad ;
- recommander la prochaine action unique ;
- maintenir les fichiers de suivi quand Gad demande une mise en ordre ;
- repondre par defaut avec un rapport boss court, pas un audit technique ;
- demander un Sync checkpoint quand l'avancee est annoncee mais non visible.

Il ne doit pas :

- demander automatiquement a Naomi un statut oral ;
- declencher NotebookLM parce que Gad parle de Naomi ;
- inventer une avancee non tracee ;
- oublier de mettre a jour le curseur de rapport apres un rapport donne a Gad ;
- oublier un message Gad en attente quand Naomi revient ;
- coder sans `GO dev` explicite ;
- remplacer Gad dans les arbitrages produit.

### Professeur Naomi

Le professeur Naomi est separe de l'orchestrateur.

Il explique a Naomi ce qu'elle fait et pourquoi. Il ne suit pas l'avancement
pour Gad, ne decide pas le scope, ne lit pas la branche a la place de
l'orchestrateur et ne produit pas de statut projet.

### Agent de tracabilite de flux

L'agent de tracabilite de flux est separe de Naomi et du professeur Naomi.

Il trace le flux Naomi : ce qui avance sur le sprint, la branche, les sous-
agents, NotebookLM, les rapports et les livrables. Ce n'est pas a Naomi de
tenir ce suivi.

Par defaut, son rapport a Gad ne separe pas `Naomi personnelle`, `Codex` et
`repo`. Il dit ou en est le flux Naomi. La separation fine reste disponible en
preuve interne ou audit detaille.

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
- le dernier avancement du flux dans le worklog ;
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
Fiabilite du suivi : suivi a rattraper
Ce que je peux affirmer : le flux [pilote/sprint] a deja de la matiere prouvee.
Ce que je ne dois pas faire : reduire le statut aux seules actions humaines visibles.
Point de rupture : l'agent de tracabilite n'a pas encore raccorde toutes les preuves.
Action correction : rattraper le suivi, puis reprendre le flux au prochain trou reel.
```

Si un thread Naomi montre une reponse ou une action non reportee dans les
fichiers, le point de rupture est `THREAD_ONLY_TRACE`.

Si la branche contient une avancee non reportee dans le worklog, le point de
rupture est `BRANCH_AHEAD_OF_WORKLOG`.

Si le repo contient une matiere SELAS preexistante mais que le worklog ne la
rappelle pas, le point de rupture est `PROJECT_STATE_IGNORED`.

Dans tous les cas de suivi `STALE`, Codex doit activer l'Agent de tracabilite
de flux defini dans `docs/project/WORKSTREAM_TRACE_AGENT_PROTOCOL_V1.md`. Son
mode `rattrapage retroactif` reconstruit les faits depuis le repo, les commits,
les rapports, les specs, les threads et les branches.

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

Quand Gad demande `ou en est Naomi ?`, Codex repond par defaut avec un rapport
boss court :

```text
Statut flux Naomi : [projet] / [sprint ou mission] / [phase] / [GO ou NO-GO]
Avancement depuis le dernier point : [1-3 faits utiles du flux]
Prochaine etape : [une action concrete]
Blocage / risque : [aucun ou blocage principal]
Fiabilite : [OK / suivi a rattraper / source manquante]
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

Si Gad demande explicitement un audit detaille, Codex peut ajouter :

```text
Sources lues : [...]
Branche : [...]
Rapport detaille : [...]
Rattrapage retroactif : [...]
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
- dernier avancement du flux trace ;
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
- Codex ou un sous-agent avance dans le perimetre du flux Naomi ;
- une preuve repo/branche/thread pertinente au flux est decouverte ;
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
- un suivi stale declenche un rattrapage retroactif au lieu d'une conclusion
  faussement certaine ;
- Codex sait quelle branche et quel worklog lire ;
- les avances du flux Naomi sont tracees par date ;
- le professeur Naomi reste pedagogique et separe de l'orchestrateur ;
- les sprints restent generiques et ne dependent pas d'un protocole SELAS
  particulier ;
- toute absence de trace devient un blocage explicite, pas une supposition.
