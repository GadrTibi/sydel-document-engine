# la Chaloupe — pack d'embarquement du Mousse (Naomi)

*Face Capitaine. À lire par Gad, pas par Naomi.*

## C'est quoi
Dans **L'Équipage**, **la Chaloupe** est l'embarcation détachée que le navire amiral arme pour une
mission, sous les ordres du **Capitaine (Gad)**, et qui revient rendre compte. À son bord, **le Mousse
(Naomi)** pilote le *métier* d'un sprint et apprend ; son **second** (le Claude Code de Naomi) fait
tout le technique pour elle. Le Capitaine tient **tous les gates** (priorités, scope, `GO dev`, contact
humain externe, merge, déploiement).

Ce dossier `naomie/` est le **pack d'embarquement** : il s'installe tout seul sur la machine du Mousse
et cadre chaque session. 100 % dans le repo, rien de manuel à câbler.

## La seule ligne à donner à Naomi
> Sur le projet, ouvre Claude Code et tape : `/embarquer`

Rien d'autre. La commande `/embarquer` :
- fait le « **qui va là ?** » corsaire (opérateur = Naomi → **mode Mousse**) ;
- installe / met à jour la Chaloupe au global de sa machine (règle + protocole) ;
- charge le runtime Sydel (`naomie/NAOMIE_RUNTIME.md`) ;
- lit le worklog (message du Capitaine en attente ?) et vérifie remote + branche ;
- donne l'**accueil cadré** (Statut / Action unique / Point pédagogie / Prochaine étape).

Défaut tant que le Capitaine n'a pas dit `GO dev` : **NO-GO dev**.

## Ton de bord (pirate) — réservé au Mousse
Naomi débarque seule, en télétravail, sans rien connaître de L'Équipage. Pour qu'elle vive le sprint
comme un **jeu de rôle pirate**, son Claude lui parle en **corsaire** (fun, gamifié) **tout en restant
carré et productif** : la structure 4 lignes (Statut / Action unique / Point pédagogie / Prochaine
étape) et **tous les interdits durs** ne bougent pas — seul le **ton** devient pirate. **Avec toi
(Capitaine) : ton normal.** Le pirate s'arme **seulement après** que Naomi a confirmé être le Mousse au
« qui va là ? ». Détail : `naomie/EMBARQUEMENT.md` (section « Ton de bord — mode Mousse (pirate) »).

## Garde-fous DURS du Mousse (rappel)
Le Mousse ne fait **jamais** : `push sur main` · `merge` · `déploiement` · contact humain externe
(Rafael l'associé, Albane le sachant juridique, client, relecteur, administration) · décision de
scope-produit · modification d'une formulation juridique. Tout ça part **emballé** dans un **Pack de
passation** pour le Capitaine. C'est aussi verrouillé côté GitHub (`main` protégée, PR + revue Gad).

## Tout l'Équipage à bord — mais toujours via le Second
Le Second (le Claude du Mousse) peut **appeler tout l'Équipage** au service de Naomi : agents
globaux et projet (`sachant-juridique`, `product-manager`, `functional-reviewer`,
`git-branch-steward` — le marin des branches : il veille à ce que le Mousse reste sur `naomie/selas/*`,
jamais sur `main`…) ET **workflows** (manœuvres multi-agents) — toute la puissance du navire amiral.
Mais il reste le **garde-fou à la barre** : jamais une manœuvre qui franchit un interdit dur (push
`main`, merge, déploiement, contact terre ferme, scope produit, formulation juridique) ; il pèse la
pertinence et le coût (pas de fanout massif en aveugle) ; il garde le rythme **une manœuvre à la fois**
+ la pédagogie. Le Mousse **ne lance jamais** un agent ni un workflow lui-même : tout passe par le
Second qui filtre. Détail : `equipage/naomie/PROTOCOL.md` §13.

## Supervision (côté Capitaine)
Pour savoir où en est le Mousse, demande à ton Claude : **« où en est Naomi ? »**. Il lit les traces
(runtime → worklog → branche `naomie/selas/*` → commits) et répond au **format rapport boss** — pas
besoin d'un compte-rendu oral de Naomi.

## Contenu du pack
- `README.md` — ce fichier (face Capitaine).
- `EMBARQUEMENT.md` — ce que le second exécute à chaque `/embarquer` (idempotent).
- `NAOMIE_RUNTIME.md` — le runtime **Sydel** : la seule place des spécificités projet.
- `RECUP_CODEX.md` — procédure béton (pas-à-pas, pédagogie Git) pour récupérer + hisser le butin SELAS
  commencé avec Codex (mission d'ouverture).
- `worklog/WORKLOG.md` — journal du flux (rapports, messages du Capitaine, décisions).
- `equipage/rules/50-naomie-wing.md` — copie verbatim de la règle d'activation (charge utile à installer).
- `equipage/naomie/PROTOCOL.md` — copie verbatim du protocole complet (charge utile à installer).
- `../.claude/commands/embarquer.md` — la commande projet `/embarquer`.

> Point ouvert : **périmètre du Mousse = SELAS, À CONFIRMER par le Capitaine** (voir `NAOMIE_RUNTIME.md`).
