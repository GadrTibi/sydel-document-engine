# Naomi GitHub onboarding V1

Date : 2026-06-01

## Objet

Ce document est le mode d'emploi pour installer le projet SYDEL sur
l'ordinateur de Naomi et commencer un sprint sur une branche propre.

Il sert aussi a Gad et Codex pour preparer la branche de depart.

La couche pedagogique associee est definie dans
`docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`.

Le suivi operationnel d'un sprint Naomi est defini dans
`docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md`. Pour la SELAS, l'etat actif
est `docs/sprints/SPRINT_SELAS_V1.md`.

La synchronisation entre le thread Naomi, le thread Gad, le worklog et la
branche est definie dans `docs/project/NAOMIE_WORKSTREAM_SYNC_PROTOCOL_V1.md`.

## Principe operationnel

Naomi ne pilote pas GitHub, Git, les branches, les commits, les push ou les
commandes terminal.

Naomi doit seulement :

1. installer les outils demandes par le guide Git ;
2. donner acces au depot GitHub si necessaire ;
3. ouvrir Codex dans le dossier projet ;
4. s'identifier ;
5. decrire le sprint metier ;
6. valider les questions, matrices et retours metier ;
7. poser des questions d'apprentissage quand elle veut comprendre.

Codex gere :

- le clone ou la recuperation du projet ;
- la branche ;
- les commandes Git ;
- l'environnement Python ;
- les tests ;
- les commits/push uniquement quand Gad l'a demande ou valide ;
- les mises a jour de la memoire projet.
- les checkpoints de synchronisation quand une phase est terminee ou quand Gad
  ne voit pas l'avancee.

Gad garde l'arbitrage final sur le type d'entreprise, la base de branche et les
validations metier sensibles.

## Couche professeur

Naomi peut demander une explication a tout moment avec :

```text
Question professeur : [sa question]
```

Exemples :

```text
Question professeur : c'est quoi une branche ?
Question professeur : pourquoi on fait un audit de reutilisation ?
Question professeur : c'est quoi NO-GO dev ?
```

Codex doit alors expliquer sans lancer de dev et sans demander a Naomi
d'executer les commandes elle-meme.

## Regle de depart

Naomi ne doit pas developper sur `main` ni directement sur
`track-b/clean-rebuild`.

Le nom du dossier local n'est pas une preuve suffisante. Gad travaille dans un
worktree appele `sydel-track-b`, tandis qu'un clone standard sur l'ordinateur de
Naomi peut s'appeler `sydel-document-engine`. Les deux peuvent pointer vers le
meme depot GitHub.

Ce que Codex doit verifier pour Naomi :

- remote : `https://github.com/GadrTibi/sydel-document-engine.git` ;
- branche active : `codex/naomie-selas-sprint` pour le sprint SELAS.

Si Naomi est dans `sydel-document-engine` mais sur `main`, le dossier peut etre
bon mais la branche est mauvaise pour le sprint. Codex doit basculer sur la
branche de sprint ou bloquer en `NO-GO dev`.

Concretement, elle ne doit pas lancer elle-meme de commandes Git. Si une action
Git est necessaire, elle demande a Codex de la faire.

Si Naomi pense qu'une phase est terminee, elle ne doit pas seulement le dire
dans le chat. Codex doit produire un checkpoint :

- soit commit + push sur la branche de sprint ;
- soit `Sync packet` complet si le push est bloque.

Pour chaque nouveau type d'entreprise :

`1 sprint = 1 branche = 1 type d'entreprise`

Nom de branche recommande :

```text
codex/naomie-[type-entreprise]-sprint
```

Exemples :

```text
codex/naomie-selas-sprint
codex/naomie-scm-sprint
codex/naomie-sci-sprint
```

## Prealable cote Gad

Avant de lancer Naomi sur une branche distante, Gad doit verifier que la base
du projet est propre :

1. les documents de gouvernance sont relus ;
2. le checkpoint local est commite ;
3. le checkpoint est pousse sur GitHub ;
4. le type d'entreprise du sprint est choisi.

Tant que ces quatre points ne sont pas vrais, la branche Naomi peut etre
preparee en documentation, mais elle ne doit pas devenir la branche de travail
principale.

## Creation de la branche par Gad ou Codex

Commandes reservees a Gad ou Codex, pas a Naomi :

```powershell
git switch track-b/clean-rebuild
git pull --ff-only origin track-b/clean-rebuild
git switch -c codex/naomie-[type-entreprise]-sprint
git push -u origin codex/naomie-[type-entreprise]-sprint
```

Remplacer `[type-entreprise]` par le type choisi.

Si le projet a ete fusionne ailleurs avant le sprint, Gad peut choisir une autre
branche de base, mais la decision doit etre ecrite dans
`docs/project/01_EXECUTION_BOARD.md`.

## Installation sur l'ordinateur de Naomi

### 1. Installer les outils

Naomi doit installer ou faire installer :

- Git ;
- Python 3.11 ou plus ;
- un terminal PowerShell ;
- un acces GitHub au depot ;
- VS Code ou un editeur equivalent, optionnel mais recommande.

Apres cette etape, Naomi ne gere plus les commandes. Codex prendra la main dans
le terminal du projet.

Depot GitHub :

```text
https://github.com/GadrTibi/sydel-document-engine.git
```

### 2. Ouvrir Codex et demander l'installation projet

Naomi doit dire a Codex :

```text
Je suis Naomi.
J'ai installe Git/Python et j'ai acces au depot GitHub.
Peux-tu installer le projet SYDEL sur mon ordinateur et te placer sur ma branche de sprint ?
```

Codex execute alors les etapes techniques.

### 3. Cloner le projet

Commandes reservees a Codex :

```powershell
git clone https://github.com/GadrTibi/sydel-document-engine.git
cd sydel-document-engine
```

### 4. Recuperer la branche de sprint

Commandes reservees a Codex, si Gad a deja pousse la branche :

```powershell
git fetch origin
git switch codex/naomie-[type-entreprise]-sprint
```

Si la branche n'existe pas encore, Codex doit s'arreter et le signaler a Gad.
Naomi ne doit pas inventer une branche sans type d'entreprise valide.

### 5. Creer l'environnement Python

Commandes reservees a Codex :

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Si `py -3.11` n'est pas reconnu :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

### 6. Verifier que le projet fonctionne

Commandes reservees a Codex :

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
```

Pour ouvrir l'application locale propre Track B :

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\sydel_doc_engine\front_app\app.py --server.port 8501
```

Si le port 8501 est deja occupe, utiliser 8502 ou 8503.

## Demarrage d'un sprint par Naomi

Dans Codex, Naomi doit commencer exactement par :

```text
Je suis Naomi.
Je veux demarrer le sprint [type d'entreprise].
```

Codex doit ensuite lui faire suivre, dans l'ordre :

1. `docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` ;
2. le fichier actif `docs/sprints/SPRINT_[TYPE]_V1.md` s'il existe ;
3. `docs/project/COMPANY_TYPE_SPRINT_PLAYBOOK_V1.md` ;
4. `docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` ;
5. `docs/project/PRODUCT_GUARDRAIL_PROTOCOL_V1.md` ;
6. la source de verite `project/source_truth/Documents_a_generer_par_cas.docx` ;
7. les specs et sources du type d'entreprise cible.

Le sprint commence toujours en `NO-GO dev`.

## Travail quotidien sur branche

Naomi ne gere pas la branche au quotidien. Elle ouvre Codex dans le projet et
dit :

```text
Je suis Naomi.
Je reprends le sprint [type d'entreprise].
Peux-tu verifier l'etat Git, la branche et les tests avant qu'on continue ?
```

Codex execute les commandes necessaires.

Avant de commencer une session, commandes reservees a Codex :

```powershell
git status --short --branch
git fetch origin
```

Si Gad a mis a jour la branche de base, commande reservee a Codex :

```powershell
git merge origin/track-b/clean-rebuild
```

Naomi ne doit jamais utiliser `git reset --hard`. Codex ne doit jamais utiliser
de commande destructive sans consigne explicite de Gad.

## Fin de session Naomi

Avant de demander une revue, commandes reservees a Codex :

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
git status --short
```

Puis, si Gad valide le scope, commandes reservees a Codex :

```powershell
git add docs src tests
git commit -m "Document sprint [type entreprise]"
git push
```

Le commit doit rester limite au sprint en cours.

## Ce que Naomi ne doit pas faire

- modifier la source de verite sans decision explicite ;
- coder un document sans source recue et spec ecrite ;
- changer du wording juridique pour le rendre plus joli ;
- refaire des variables ou generateurs deja traites sans audit de reuse ;
- melanger deux types d'entreprise dans la meme branche ;
- lancer des commandes Git ou terminal sans Codex ;
- declarer un sprint termine sans retour de l'associe ou report explicite.

## Definition d'une branche prete

Une branche Naomi est prete seulement si :

- elle part d'une base projet poussee sur GitHub ;
- elle porte le nom du type d'entreprise ;
- le sprint est ouvert dans `docs/project/01_EXECUTION_BOARD.md` ;
- le sprint plan existe avant le premier code ;
- l'audit de reutilisation SELARL/global a ete fait ;
- Codex a donne un `GO dev` limite a un ticket precis.
