# RECUP_CODEX — récupérer le butin SELAS commencé avec Codex (mission d'ouverture)

*Procédure de bord, exécutée par le **second** (le Claude de Naomi) **sur la machine du Mousse**, une
manœuvre à la fois, ton corsaire, pédagogie Git à chaque étape. Naomi apprend en faisant.*

> 🏴‍☠️ **L'histoire** : le Mousse avait déjà commencé à travailler la SELAS avec un autre matelot
> (Codex), mais le **butin n'a jamais été hissé** sur le navire commun (le remote GitHub). Il dort
> quelque part sur le disque de Naomi. Notre mission : le **retrouver sans rien casser**, le **ranger
> proprement dans la bonne cale** (sa branche), et le **hisser** vers le navire — puis rendre compte au
> Capitaine.

> ⚓ **Note d'alignement** : Naomi travaille désormais dans un **clone neuf** (base propre + Chaloupe =
> son atelier d'avenir). Pour la récupération, le Second inspecte l'**ANCIEN dossier Codex** qu'elle
> pointe (lecture seule) et choisit le chemin le plus sûr : (Cas A, le plus probable) pousser sa branche
> directement depuis l'ancien dossier ; sinon transplanter le travail dans le clone neuf sur
> `naomie/selas/<ticket>`. **L'ancien dossier reste intact.**

---

## Avant de larguer les amarres (pré-conditions DURES)
Cette mission **ne démarre PAS** tant que ces deux pavillons ne sont pas levés :
1. **Périmètre confirmé** : le Capitaine a confirmé que le périmètre du Mousse est bien la **SELAS**
   (cf. `NAOMIE_RUNTIME.md`). Tant que c'est `à confirmer`, la manœuvre du moment = **faire trancher le
   Capitaine** (message worklog), pas récupérer/coder.
2. **`GO dev` du Capitaine** : pavillon GO levé. Par défaut **NO-GO dev**.

Si l'un des deux manque → **on reste à quai**. Tu l'expliques au Mousse en corsaire, et la seule
manœuvre proposée est d'obtenir ces feux verts via le Capitaine.

**Cordages auxquels on ne touche JAMAIS, même pour cette mission** : pas de `push sur main`, pas de
`merge`, pas de `déploiement`, pas de contact de la **terre ferme** (Rafael, Albane, client, relecteur).
Le Mousse hisse une branche `naomie/selas/<ticket>`, point. Le reste, c'est le Capitaine à la barre.

---

## Règle d'or de la manœuvre
**Une seule action à la fois.** Tu donnes UNE commande à Naomi → elle la lance → elle te **recopie la
sortie brute** → tu lis, tu journalises, tu expliques (le mot du gabier) → manœuvre suivante. Jamais une
grande liste de commandes d'un coup. **On ne devine rien : on regarde d'abord, on agit ensuite.**

---

## Étape 1 — Retrouver la cale où dort le butin (localiser le dossier)
🧭 **Manœuvre** : demande à Naomi où elle travaillait la SELAS avec Codex — le **dossier sur son
disque** (souvent quelque chose comme `Desktop\Sydel\...` ou un clone séparé). Fais-lui ouvrir un
terminal **dans ce dossier**, puis lance :
```
git rev-parse --is-inside-work-tree
git rev-parse --show-toplevel
```
📚 **Le mot du gabier** : un dépôt Git, c'est un dossier qui contient un sous-dossier caché `.git` — la
« mémoire » du navire. `--is-inside-work-tree` répond `true` si on est bien dans un dépôt ;
`--show-toplevel` donne le chemin de la **racine** du dépôt. Si ça renvoie une erreur « not a git
repository », c'est qu'on n'est pas dans le bon dossier → on cherche le bon avant tout.

➡️ **Cap suivant** : une fois la racine confirmée, on regarde dans quel état est la cale (Étape 2).

---

## Étape 2 — Ouvrir l'écoutille et regarder l'état (sans rien toucher)
🧭 **Manœuvre** : fais lancer, **dans l'ordre**, ces commandes de **lecture seule** (elles ne modifient
RIEN) et recopie-toi la sortie de chacune :
```
git status
git log --oneline -15
git branch -a
git stash list
```
📚 **Le mot du gabier** :
- `git status` = « qu'est-ce qui traîne sur le pont ? » → fichiers modifiés non enregistrés
  (*not staged*), fichiers prêts à enregistrer (*staged*), fichiers tout neufs jamais suivis
  (*untracked*). C'est l'état **vivant** du travail.
- `git log --oneline` = le **journal de bord** des enregistrements (*commits*) déjà faits. S'il y a des
  commits récents SELAS ici, le travail est **déjà enregistré localement** — il ne manque sans doute que
  le `push` (le cas le plus probable !).
- `git branch -a` = toutes les **cales** (branches), locales et distantes (`remotes/...`).
- `git stash list` = la **réserve** : du travail mis de côté temporairement. Parfois le butin Codex
  dort là.

🔎 **Diagnostic** (tu classes la situation) :
- **Cas A — commits locaux non poussés** (le plus probable) : `git log` montre des commits SELAS récents,
  `git status` dit souvent *« your branch is ahead of 'origin/...' by N commits »*. → **Il manque juste
  un `git push`.** On file à l'Étape 3 puis 5–6.
- **Cas B — travail non commité** : `git status` montre des fichiers modifiés/untracked SELAS mais aucun
  commit dédié. → Il faudra **enregistrer (commit) avant de hisser**. Étape 3 → 4 → 5–6.
- **Cas C — travail planqué dans un stash / une branche orpheline** : repérable via `git stash list` ou
  `git branch -a`. → On le **restaure** d'abord (`git stash show -p`, `git stash apply`…), **sans
  écraser** l'existant, puis Cas B.
- **Cas D — rien de récupérable proprement** : aucune trace exploitable. → **On ne ment pas** : pas de
  « c'est fait ». On produit un **Sync packet** (état structuré) pour le Capitaine et on s'arrête.

➡️ **Cap suivant** : on vérifie le navire d'attache et le pavillon de Naomi (Étape 3).

---

## Étape 3 — Vérifier le navire d'attache (remote) et le pavillon (compte GitHub)
🧭 **Manœuvre** : fais lancer :
```
git remote -v
```
Le remote `origin` **doit** pointer sur :
`https://github.com/GadrTibi/sydel-document-engine.git`.
Vérifie aussi **qui signe** — le compte GitHub de Naomi (le Mousse) est **`naomiguetta10-prog`** :
```
git config user.name
git config user.email
```

📚 **Le mot du gabier** : le **remote** est l'adresse du navire commun sur GitHub ; `origin` est son
petit nom par défaut. `user.name` / `user.email` décident **sous quel pavillon** les commits sont signés
— c'est la **traçabilité** : on veut que le butin du Mousse soit signé du **compte de Naomi**, pas d'un
autre.

🔧 **Si le remote est absent ou faux** (Cas « pas de remote / mauvais remote ») :
- absent → on l'ajoute :
  `git remote add origin https://github.com/GadrTibi/sydel-document-engine.git`
- mauvais → on le corrige :
  `git remote set-url origin https://github.com/GadrTibi/sydel-document-engine.git`
🔧 **Si la signature n'est pas celle de Naomi**, on la pose **pour ce dépôt** (local, pas global) :
```
git config user.name "Naomi Guetta"
git config user.email "<l'email du compte naomiguetta10-prog>"
```
> 🦜 **Authentification** : au moment de hisser (push), GitHub demandera de prouver que c'est bien
> Naomi. Si ça coince, c'est une histoire de **connexion à son compte** (token / GitHub CLI / cache
> d'identifiants) — pas une histoire de code. On règle l'auth **avant** de pousser ; on ne contourne
> jamais en poussant sous un autre compte.

➡️ **Cap suivant** : on prépare la bonne cale, la branche du Mousse (Étape 4).

---

## Étape 4 — Préparer la bonne cale (branche `naomie/selas/<ticket>`)
> ⚓ **Avant de manœuvrer la branche** : **fais valider la manœuvre de branche par l'agent
> `git-branch-steward`** (base de départ correcte, branche `naomie/selas/<ticket>`, jamais
> `main`/branche du Capitaine) AVANT de créer/basculer, et **ne commit jamais avant d'être sur ta
> branche**.

🧭 **Manœuvre** : on range le butin dans **SA** cale, jamais dans `main`, jamais dans une cale du
Capitaine (`review/selarl`, `streamlit/*`, …). D'abord on regarde où on est :
```
git branch --show-current
```
Puis on crée/bascule sur la branche du Mousse (remplace `<ticket>` par l'intitulé court du sprint, ex.
`naomie/selas/recup-codex`) :
```
git switch -c naomie/selas/<ticket>
```
Si la branche existe déjà, on s'y pose simplement :
```
git switch naomie/selas/<ticket>
```

📚 **Le mot du gabier** : une **branche** est une ligne de travail séparée — comme une cale dédiée. On
isole le travail du Mousse pour ne **jamais** percuter `main` (le pont principal, protégé) ni le couloir
du Capitaine. `switch -c` = *create* (créer puis basculer) ; `switch` seul = juste basculer.

> ⚠️ **Cas A (commits déjà locaux)** : si les commits SELAS sont déjà sur une branche locale, ne crée
> pas une cale vide à côté en perdant le travail. Vérifie d'abord sur quelle branche vivent ces commits
> (`git log --oneline` + `git branch`). Au besoin, fais relire l'état au Capitaine via Sync packet
> plutôt que de réorganiser les branches en aveugle.

➡️ **Cap suivant** : enregistrer le butin (Étape 5).

---

## Étape 5 — Enregistrer le butin (commit propre, signé du Mousse)
*(À faire seulement en **Cas B / C** — du travail non encore commité. En **Cas A**, le butin est déjà
enregistré : saute directement à l'Étape 6.)*

🧭 **Manœuvre** : on regarde **précisément** ce qu'on s'apprête à embarquer, puis on l'enregistre :
```
git status
git add -A
git status
git commit -m "feat(selas): récupération du travail SELAS commencé avec Codex"
```
📚 **Le mot du gabier** :
- `git add -A` = « charger sur le pont » tout ce qui est modifié/nouveau (*staging*). On relance
  `git status` **après** pour vérifier qu'on embarque bien ce qu'on veut, **rien de parasite** (pas de
  secrets, pas de gros fichiers de travail Codex non désirés).
- `git commit -m "..."` = sceller un **enregistrement** horodaté et signé. Le message décrit le butin en
  clair. Comme la signature a été réglée à l'Étape 3, ce commit porte le **pavillon de Naomi**.

➡️ **Cap suivant** : hisser les couleurs (Étape 6).

---

## Étape 6 — Hisser le butin vers le navire (push de la BRANCHE, jamais `main`)
🧭 **Manœuvre** : on pousse **la branche du Mousse** vers `origin` (la première fois, `-u` relie la cale
locale à sa jumelle distante) :
```
git push -u origin naomie/selas/<ticket>
```
📚 **Le mot du gabier** : `push` = **hisser** les enregistrements locaux vers le navire commun (GitHub).
`-u origin <branche>` crée la branche côté distant et mémorise le lien, pour qu'ensuite un simple
`git push` suffise. **On pousse une branche `naomie/selas/*`, JAMAIS `main`** — `main` est le pont du
Capitaine, protégé.

🔧 **Si GitHub refuse** :
- *« could not read Username / authentication failed »* → souci d'**auth** (Étape 3) : reconnecter le
  compte `naomiguetta10-prog` (GitHub CLI / token), puis re-`push`. **Une seule** relance pour confirmer
  si c'était transitoire ; pas de boucle.
- *« updates were rejected »* → quelqu'un a poussé entre-temps : **stop**, ne force **jamais**
  (`--force` interdit). On rapporte au Capitaine.

✅ **Preuve visible** : tant que le `push` n'a pas réussi, le travail n'est **PAS** « fait ». La preuve,
c'est la **branche visible sur GitHub** (ou, à défaut, un Sync packet). Pas de preuve → « synchronisation
manquante », jamais « fait ».

➡️ **Cap suivant** : rendre compte au Capitaine (Étape 7).

---

## Étape 7 — Rendre compte au Capitaine (Pack de passation)
🧭 **Manœuvre** : une fois le butin hissé (ou si on est bloqué), tu rédiges le **Pack de passation** au
format du protocole (§7) et tu le déposes pour le Capitaine, puis tu mets à jour `naomie/worklog/`.
```
PACK DE PASSATION — Sydel / SELAS / [date]
1. Ce qui a été fait : butin SELAS commencé avec Codex récupéré et hissé.
2. Où : branche naomie/selas/<ticket> · commit(s) [hash] · (lien GitHub si dispo)
3. Vérifié : [git push OK / branche visible sur GitHub] — preuves (sortie des commandes)
4. À VALIDER PAR LE CAPITAINE (terre ferme) : [rien, ou écarts concrets sourcés à faire trancher]
5. À DÉPLOYER PAR LE CAPITAINE : rien (le Mousse ne déploie jamais)
6. Décisions produit en attente : [périmètre SELAS confirmé ? questions A/B/C] — ou « aucune »
7. Reste à faire : [prochaines manœuvres — ex. PR à ouvrir/relire côté Capitaine]
```
📚 **Le mot du gabier** : le **Pack de passation** est l'artefact pivot — c'est par lui que le Mousse
remet le travail au Capitaine. Tout ce qui touche la **terre ferme** (relecteur, associé) ou un
**déploiement / merge** est **listé pour le Capitaine**, jamais exécuté par le Mousse.

➡️ **Cap suivant** : worklog à jour, et on attend les ordres du Capitaine. 🏴‍☠️
