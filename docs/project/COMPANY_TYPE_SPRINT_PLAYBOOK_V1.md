# Company type sprint playbook V1

Date : 2026-06-01

## Objet

Ce document formalise la methode de sprint a appliquer avant tout developpement
d'un nouveau type d'entreprise.

Le suivi operationnel de chaque sprint est gere par
`docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et par le fichier actif
`docs/sprints/SPRINT_[TYPE]_V1.md`. Le present playbook decrit la methode ; le
fichier de sprint indique l'etat exact a l'instant T.

La SELARL est le sprint pilote. Les prochains sprints doivent reutiliser la meme
methode, avec un perimetre clair :

`1 sprint = 1 type d'entreprise`

Un sprint couvre la totalite du type d'entreprise au sens produit : tous les
documents attendus sont inventories, classes, expliques et suivis. Cela ne veut
pas dire que tous les documents sont codes si une source manque, si un document
est manuel, ou si une decision humaine est requise. Dans ce cas, le sprint doit
le dire explicitement.

Ouvrir un sprint ne vaut jamais autorisation de developper. La decision par
defaut reste `NO-GO dev` jusqu'a validation explicite d'un ticket borne.

## Regle non negociable

Aucun developpement d'un nouveau type d'entreprise ne demarre sans :

1. sprint ecrit a l'avance ;
2. lecture des documents de reference ;
3. interrogation large de NotebookLM ou import de ses reponses ;
4. audit de reutilisation SELARL/global ;
5. matrice des documents attendus ;
6. decision `GO dev` ou `NO-GO dev` ;
7. boucle de test par l'associe en fin de sprint ;
8. statut canonique de fin de sprint.

## Roles

### Gad

Gad peut arbitrer le produit, le metier, les priorites et les decisions de
scope. Quand Gad demande d'accelerer, Codex doit quand meme proteger le projet :
si le metier n'est pas defini, le resultat reste `NO-GO dev`.

### Naomie

Naomie doit s'identifier avant de commencer un sprint :

```text
Je suis Naomie.
Je veux demarrer le sprint [type d'entreprise].
```

Quand Naomie conduit le sprint, Codex doit la guider etape par etape. Codex ne
doit pas sauter directement au dev. Chaque etape doit produire une sortie simple
a valider avant de passer a la suivante.

Si Naomie travaille depuis son ordinateur, elle doit suivre
`docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md`. Elle ne gere pas Git elle-meme :
Codex gere la branche, les commandes, les tests et les checkpoints.

Naomie peut aussi demander une explication a tout moment selon
`docs/project/NAOMIE_LEARNING_MENTOR_PROTOCOL_V1.md`, par exemple avec
`Question professeur : ...`.

### L'associe

L'associe ne travaille pas avec Codex. Il teste le produit ou relit les rendus et
renvoie un retour humain. Ce retour est obligatoire avant de declarer un sprint
termine a 100 %.

Les retours de l'associe priment sur les interpretations techniques, sous
reserve de ne pas contredire une source juridique sans arbitrage explicite.

## Cycle complet d'un sprint

### Phase 0 - Demarrage

Objectif : savoir qui pilote et quel type d'entreprise est ouvert.

Sorties obligatoires :

- identite du pilote : Gad ou Naomie ;
- type d'entreprise cible ;
- date d'ouverture du sprint ;
- decision initiale : `NO-GO dev` par defaut.

Regle : le sprint commence toujours en `NO-GO dev`.

### Phase 1 - Sources et references

Objectif : collecter ce qui fait autorite.

Sources a verifier :

- `project/source_truth/Documents_a_generer_par_cas.docx` ;
- versions V2/V3 si le sprint les utilise ;
- sources DOCX dans `project/source_documents/` ;
- specs `docs/delivery/` ;
- retours humains existants ;
- NotebookLM ;
- code existant uniquement comme controle, jamais comme source juridique.

Sortie obligatoire :

- une hierarchie des sources ;
- la liste des contradictions ;
- les questions ouvertes.

### Phase 2 - NotebookLM

Objectif : utiliser NotebookLM comme base de connaissance, sans economiser les
questions.

Si Codex a acces directement a NotebookLM, il doit interroger NotebookLM. Si
Codex n'a pas acces direct, il doit preparer les questions, puis demander a Gad
ou Naomie de coller les reponses ou un export.

Regle : aucune reponse NotebookLM ne remplace une source de verite ou un retour
humain. NotebookLM sert a explorer, comparer, detecter les cas, les exceptions et
les contradictions.

### Phase 3 - Matrice documentaire

Objectif : savoir exactement quels documents sont attendus.

Avant de fermer la matrice, Codex doit appliquer
`docs/project/REUSE_AUDIT_AGENT_PROTOCOL_V1.md` pour identifier ce qui est
deja couvert par la SELARL ou par les registres globaux. Le but est de reutiliser
ce qui est fiable, pas de refaire le meme travail.

Chaque document doit etre classe :

- generable ;
- reserve ;
- manuel ;
- bloque par source ;
- bloque par donnees ;
- hors scope ;
- non implemente ;
- deja implemente ;
- partial.

Sortie obligatoire :

- matrice documents par condition ;
- matrice de reutilisation `identique / reuse-check / adapter / no-go` ;
- liste des documents sans code ;
- liste des documents `DOC-XXX` ;
- decision pour chaque document.

### Phase 4 - Contrat metier-front

Objectif : decrire comment l'utilisateur saisit le dossier.

Sorties obligatoires :

- blocs de saisie metier ;
- roles personnes et societes ;
- adresses ;
- reutilisations explicites ;
- messages de blocage ;
- documents prets, reserves, manuels et bloques.

Regle : le formulaire part du metier, pas des generateurs.

### Phase 5 - Plan de sprint et tickets

Objectif : ecrire le sprint avant de coder.

Sorties obligatoires :

- sprint plan ;
- tickets dans `docs/project/01_EXECUTION_BOARD.md` ;
- ordre des tickets ;
- criteres d'acceptation ;
- validations attendues ;
- decision `GO dev` uniquement pour le premier ticket pret.

### Phase 6 - Implementation bornee

Objectif : coder seulement ce qui a ete autorise.

Regles :

- un ticket ne melange pas plusieurs types d'entreprise ;
- un ticket ne melange pas plusieurs sous-cas complexes sans decision explicite ;
- pas de wording juridique invente ;
- pas de document manuel automatise par accident ;
- tests et smoke obligatoires selon le risque.

### Phase 7 - Smoke interne

Objectif : verifier techniquement avant de demander un test humain.

Sorties obligatoires :

- scenario simple ;
- scenarios conditionnels majeurs ;
- ZIP dossier ;
- PDF si backend disponible ;
- controle placeholders ;
- rapport court.

### Phase 8 - Test de l'associe

Objectif : obtenir un retour humain externe a Codex.

Sorties obligatoires :

- pack de test prepare ;
- consignes de test ;
- retour humain de l'associe ;
- classement des retours : bug, wording, UX, source, arbitrage, hors scope.

Regle : le sprint n'est pas termine tant que le retour associe n'est pas traite
ou classe avec decision explicite.

### Phase 9 - Boucle corrections

Objectif : traiter les retours humains sans casser le scope.

Chaque retour produit :

- une decision ;
- un ticket de correction ou un blocage ;
- un test ;
- une note si wording juridique change.

On boucle jusqu'a validation humaine ou decision explicite de report.

### Phase 10 - Cloture

Objectif : rendre le sprint reprenable et fermer le type d'entreprise.

Sorties obligatoires :

- statut canonique final du type d'entreprise ;
- board mis a jour ;
- dernier etat mis a jour ;
- liste des points ouverts ;
- recommandation du sprint suivant ;
- methode reutilisable ajustee si necessaire.

## Questions NotebookLM obligatoires

Ces questions sont le socle minimal. Codex peut et doit en ajouter si le sprint
revele des zones floues.

### A. Perimetre general

1. Pour le type d'entreprise [X], quels documents doivent etre generes ?
2. Quels documents sont toujours attendus ?
3. Quels documents sont conditionnels ?
4. Quels documents sont explicitement a remplir a la main ?
5. Quels documents sont mentionnes mais sans source exploitable ?
6. Quels documents sont reserves ou incomplets ?
7. Quels documents semblent appartenir a un autre type d'entreprise ?
8. Quels cas ne doivent pas etre automatises en V1 ?

### B. Conditions d'apparition

1. Quelles conditions declenchent chaque document ?
2. Quelles conditions excluent chaque document ?
3. Quelles options peuvent etre combinees ?
4. Quelles combinaisons sont impossibles ou dangereuses ?
5. Quels cas simples doivent etre couverts en premier ?
6. Quels cas complexes doivent etre bloques ?
7. Quels cas doivent rester visibles mais non generes ?

### C. Roles et donnees

1. Qui est le client ?
2. Qui est le praticien ?
3. Qui est l'associe ?
4. Qui est le gerant ou dirigeant ?
5. Qui est le signataire ?
6. Qui est le mandataire ?
7. Quels roles peuvent etre la meme personne ?
8. Quels roles ne doivent jamais etre fusionnes automatiquement ?
9. Quelles adresses sont distinctes ?
10. Quelles adresses peuvent etre reutilisees seulement par option explicite ?

### D. Variables et formulaire

1. Quelles donnees doivent etre demandees a l'utilisateur ?
2. Quelles donnees peuvent etre derivees ?
3. Quelles donnees doivent rester saisies separement ?
4. Quels champs sont obligatoires par document ?
5. Quels champs deviennent obligatoires seulement sous condition ?
6. Quels champs doivent etre caches tant que la condition n'est pas active ?
7. Quelles donnees doivent etre en lettres ?
8. Quelles donnees doivent etre controlees mathematiquement ?
9. Quelles variables SELARL ou globales sont strictement reutilisables ?
10. Quelles variables ont le meme libelle mais pas le meme role metier ?

### D2. Reutilisation SELARL / global

1. Quels documents deja traites cote SELARL sont identiques pour [X] ?
2. Quels documents SELARL sont proches mais exigent une verification ?
3. Quels helpers, tests ou generateurs peuvent etre reutilises ?
4. Quels retours humains SELARL sont propres a la SELARL ?
5. Quels elements doivent etre classes `adapter` ?
6. Quels elements doivent etre classes `no-go` ?
7. Quel est le plus petit ticket reusable sans risque ?

### E. Wording juridique

1. Quels passages de wording sont sensibles ?
2. Quelles variantes de wording existent selon la profession ou la forme ?
3. Quels passages ne doivent pas etre modifies ?
4. Quels passages demandent une validation humaine ?
5. Quels retours humains priment sur la source brute ?
6. Quelles formulations sont contradictoires entre sources ?
7. Quels placeholders ou parasites sont connus ?

### F. Front et experience utilisateur

1. Quel parcours metier naturel l'utilisateur doit-il suivre ?
2. Quels blocs de saisie sont necessaires ?
3. Quels messages doivent apparaitre pour les documents manuels ?
4. Quels messages doivent apparaitre pour les documents reserves ?
5. Quels blocages doivent etre visibles avant de cliquer sur generation ?
6. Quels diagnostics doivent rester caches en mode equipe ?
7. Quels prefills de test sont utiles ?

### G. Tests et recette

1. Quel est le scenario simple minimal ?
2. Quels scenarios conditionnels doivent etre testes ?
3. Quel scenario mixte realiste doit etre teste ?
4. Quels documents doivent etre compares a une source ligne par ligne ?
5. Quels documents exigent une revue humaine avant validation ?
6. Quels tests doivent prouver l'absence de placeholders ?
7. Quels tests doivent prouver l'absence de documents reserves dans le ZIP ?

### H. Fin de sprint

1. Qu'est-ce qui permet de dire que le type d'entreprise est complet ?
2. Quels documents restent manuels meme en fin de sprint ?
3. Quels documents restent reserves ?
4. Quels points doivent etre reportes au backlog ?
5. Quels retours l'associe doit-il valider ?
6. Quelle est la prochaine forme sociale logique ?

## Template sprint

Chaque sprint doit creer ou mettre a jour un document de ce format :

```text
# Sprint [TYPE ENTREPRISE] V1

Date d'ouverture :
Pilote : Gad / Naomie
Type d'entreprise :
Decision initiale : NO-GO dev

## Sources lues

## Questions NotebookLM posees

## Reponses NotebookLM utiles

## Hierarchie des sources

## Matrice documentaire

| Condition | Document | Code | Statut source | Statut moteur | Statut front | Decision |
| --- | --- | --- | --- | --- | --- | --- |

## Audit de reutilisation

| Element | Source existante | Conditions identiques ? | Variables identiques ? | Decision | Action |
| --- | --- | --- | --- | --- | --- |

## Parcours metier

## Donnees a saisir

## Reutilisations explicites

## Documents manuels / reserves / bloques

## Tickets du sprint

| Ordre | Ticket | Statut | Objet | Criteria |
| --- | --- | --- | --- | --- |

## Scenarios de smoke

## Pack pour l'associe

## Retours associe

## Corrections

## Statut final

## Prochaine recommandation
```

## Checklist Naomie

Naomie doit suivre cette checklist dans l'ordre :

1. dire explicitement `Je suis Naomie` ;
2. nommer le type d'entreprise du sprint ;
3. lire avec Codex le statut projet courant ;
4. faire l'inventaire des sources ;
5. poser les questions NotebookLM ;
6. coller les reponses NotebookLM dans le chat ou dans un fichier source ;
7. faire l'audit de reutilisation SELARL/global ;
8. valider la matrice documentaire avec Codex ;
9. valider les documents manuels/reserves/bloques ;
10. obtenir un `GO dev` uniquement pour un ticket borne ;
11. laisser Codex implementer et tester ;
12. preparer le pack de test pour l'associe ;
13. collecter le retour humain de l'associe ;
14. faire boucler les corrections ;
15. cloturer le sprint avec un statut canonique.

## Definition de done d'un sprint

Un sprint est termine seulement si :

- le type d'entreprise dispose d'un statut canonique ;
- tous les documents attendus sont classes ;
- les reutilisations SELARL/globales sont explicites et justifiees ;
- les documents generables du perimetre ont DOCX et ZIP valides ;
- les documents reserves/manuels sont visibles comme tels ;
- les retours de l'associe sont traites ou explicitement reportes ;
- aucun wording juridique n'a derive sans validation ;
- le prochain sprint peut commencer sans relire toute la conversation.

## Application a la SELARL

La SELARL a deja produit les briques de methode :

- statut canonique : `docs/project/SELARL_CANONICAL_STATUS_V1.md` ;
- backlog/factory : `docs/project/SELARL_PRODUCTION_BACKLOG_V1.md` et
  `docs/project/SELARL_PRODUCTION_FACTORY_V1.md` ;
- contrats metier-front : `TRACK_B_SELARL_FRONT_CONTRACT_V1.md` et
  `TRACK_B_SELARL_MULTI_ASSOCIES_FRONT_CONTRACT_V1.md` ;
- locks humains : `SELARL_HUMAN_REFERENCE_LOCK_V1.md` ;
- rapports de preuve dans `docs/review/`.

Il reste a faire pour cloturer la SELARL a 100 % :

1. preparer le pack de revue associe/juriste ;
2. faire tester l'associe ;
3. integrer ou classer ses retours ;
4. confirmer le statut final ou ouvrir un sous-cas unique avec `GO dev`.
