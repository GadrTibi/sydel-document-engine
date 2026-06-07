# Company type sprint playbook V1

Date : 2026-06-01

## Objet

Ce document formalise la methode de sprint a appliquer avant tout developpement
d'un nouveau type d'entreprise.

Le suivi operationnel de chaque sprint est gere par
`docs/project/PROJECT_CONTROL_TOWER_V1.md`,
`docs/project/SPRINT_ORCHESTRATOR_PROTOCOL_V1.md` et par le fichier actif
`docs/sprints/SPRINT_[TYPE]_V1.md`. Le present playbook decrit la methode ; la
tour de controle indique le sprint actif, et le fichier de sprint indique l'etat
exact a l'instant T.

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
5. audit de deduplication front si le sprint touche la saisie utilisateur ;
6. matrice des documents attendus ;
7. decision `GO dev` ou `NO-GO dev` ;
8. boucle de test par l'associe en fin de sprint ;
9. statut canonique de fin de sprint.

## Amendement SELARL 2026-06-01

La fin de sprint SELARL a ajoute des regles qui deviennent obligatoires pour
tous les futurs types d'entreprise.

### Trois sources minimum

Avant de dire qu'un type d'entreprise est pret a developper ou a clore, Codex
doit trianguler au minimum :

1. le document de reference qui dit quels documents doivent etre produits ;
2. les retours modele / NotebookLM deja journalises ;
3. les retours humains disponibles, puis le retour final de l'associe.

Si l'une de ces trois sources manque, Codex ne doit pas inventer. Il doit
classer le point en `non trouve`, `reserve`, `manuel`, `bloque` ou `a valider`.

### Discipline anti-questions inutiles

Codex ne doit pas poser a Gad ou a l'associe des questions dont la reponse est
deja dans les sources, les specs ou une regle documentaire evidente. Exemple
SELARL : si le regime communautaire est actif, les sources disent deja que
`DOC-005` et `DOC-006` doivent etre produits ensemble.

Les questions humaines doivent donc porter uniquement sur :

- un ecart concret dans un document genere ;
- une contradiction entre sources ;
- une source manquante ;
- une variable mal placee ;
- un document absent ou en trop ;
- un arbitrage de scope.

Si ces questions deviennent bloquantes, Codex doit les formuler immediatement
avec le ticket, les sources deja verifiees, l'impact sur le sprint et l'action
possible en attendant. Le projet ne doit jamais rester bloque sans question
explicite a Gad ou sans decision sourcee.

### Fidelite source et pack actif

Quand un document est genere, la verification ne s'arrete pas au fait que le
DOCX existe. Codex doit verifier la fidelite :

- absence de placeholders ou parasites ;
- respect du wording source, sauf variables assumees ;
- comparaison ligne par ligne ou bloc par bloc pour les documents sensibles ;
- ZIP/manifest coherent ;
- pack actif clairement nomme.

Un pack corrige remplace les packs precedents. Codex ne doit jamais transmettre
a l'associe un ancien pack si un pack plus recent a corrige un ecart.

### Cloture canonique

Un sprint peut finir en trois etats seulement :

- `DONE` : le perimetre annonce est valide techniquement et humainement ;
- `PARTIAL` : un sous-perimetre est valide, mais des variantes restent ouvertes ;
- `BLOCKED` : une source, une decision ou un retour humain manque.

Le pourcentage n'est qu'une aide de pilotage. Le statut canonique prime.

## Roles

### Gad

Gad peut arbitrer le produit, le metier, les priorites et les decisions de
scope. Quand Gad demande d'accelerer, Codex doit quand meme proteger le projet :
si le metier n'est pas defini, le resultat reste `NO-GO dev`.

### Naomi

Naomi doit s'identifier avant de commencer un sprint :

```text
Je suis Naomi.
Je veux demarrer le sprint [type d'entreprise].
```

Quand Naomi conduit le sprint, Codex doit la guider etape par etape. Codex ne
doit pas sauter directement au dev. Chaque etape doit produire une sortie simple
a valider avant de passer a la suivante.

Si Naomi dit qu'elle veut lancer, demarrer ou reprendre le sprint, Codex doit
demarrer le sous-sprint NotebookLM, pas le developpement. Codex donne un seul
prompt court a copier-coller dans NotebookLM, attend la reponse brute de Naomi,
la structure dans le journal du sprint, puis choisit le prompt suivant selon les
trous. Cette boucle continue jusqu'a ce que Codex considere les informations
suffisantes pour passer a l'audit de reutilisation.

Si Naomi travaille depuis son ordinateur, elle doit suivre
`docs/project/NAOMIE_GITHUB_ONBOARDING_V1.md`. Elle ne gere pas Git elle-meme :
Codex gere la branche, les commandes, les tests et les checkpoints.

Naomi peut aussi demander une explication a tout moment selon
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

- identite du pilote : Gad ou Naomi ;
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
- une table des trois sources disponibles : reference, NotebookLM/modele,
  humain ;
- la liste des contradictions ;
- les questions ouvertes.

Regle : si Codex sait deja repondre depuis les sources, il note la decision au
lieu de poser une question humaine.

### Phase 2 - NotebookLM

Objectif : utiliser NotebookLM comme base de connaissance, sans economiser les
questions.

Si Codex a acces directement a NotebookLM, il doit interroger NotebookLM. Si
Codex n'a pas acces direct, il doit preparer les questions, puis demander a Gad
ou Naomi de coller les reponses ou un export.

Regle : aucune reponse NotebookLM ne remplace une source de verite ou un retour
humain. NotebookLM sert a explorer, comparer, detecter les cas, les exceptions et
les contradictions.

Pour Naomi, cette phase se pilote comme un sous-sprint :

1. Codex donne un prompt court ;
2. Naomi copie ce prompt dans NotebookLM ;
3. Naomi colle la reponse NotebookLM dans Codex ;
4. Codex structure la reponse dans le journal ;
5. Codex identifie les trous ;
6. Codex donne le prompt suivant ;
7. la boucle continue tant que les informations ne sont pas suffisantes.

Pendant ce sous-sprint, Codex ne doit pas produire de matrice finale, lancer un
audit de reutilisation, coder, generer ou pousser une fonctionnalite.

La phase NotebookLM est suffisante seulement si le journal permet de lister :

- les documents attendus ;
- les conditions d'apparition et d'exclusion ;
- les documents manuels, reserves ou bloques ;
- les roles et variables structurantes ;
- les differences avec SELARL ou avec les socles globaux ;
- les contradictions ou `non trouve`.

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

Avant de valider cette phase, appliquer
`docs/project/FRONT_INFORMATION_DEDUP_AGENT_PROTOCOL_V1.md` :

- une information metier identique est saisie une seule fois ;
- les reutilisations sont explicites ou derivees ;
- les constantes ne sont pas demandees a l'utilisateur ;
- les valeurs reutilisees peuvent etre affichees en lecture seule, pas
  redemandees comme champs editables.

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

Pour les documents juridiques sensibles, ajouter un controle de fidelite source
avant transmission humaine :

- rendu DOCX compare a la source ou au retour humain disponible ;
- differences classees en variable assumee, ecart reel ou hors source ;
- pack numerote et manifest associe.

### Phase 8 - Test de l'associe

Objectif : obtenir un retour humain externe a Codex.

Sorties obligatoires :

- pack de test prepare ;
- consignes de test limitees aux ecarts concrets ;
- retour humain de l'associe ;
- classement des retours : bug, wording, UX, source, arbitrage, hors scope.

Regle : le sprint n'est pas termine tant que le retour associe n'est pas traite
ou classe avec decision explicite.

Regle issue de la SELARL : l'associe ne doit pas recevoir une liste de questions
abstraites quand les sources repondent deja. Il doit recevoir un pack actif et
un format de retour de type :

```text
Verdict global : VALIDE / CORRECTIONS / BLOQUE
Scenario :
Document :
Ecart constate :
Correction demandee :
Source ou emplacement :
```

### Phase 9 - Boucle corrections

Objectif : traiter les retours humains sans casser le scope.

Chaque retour produit :

- une decision ;
- un ticket de correction ou un blocage ;
- un test ;
- une note si wording juridique change.

On boucle jusqu'a validation humaine ou decision explicite de report.

Apres chaque correction documentaire :

1. regenerer un nouveau pack ;
2. marquer l'ancien pack comme remplace ;
3. relancer les controles cibles ;
4. refaire l'audit des trois sources si l'ecart touchait un document produit ;
5. mettre a jour le brief associe.

### Phase 10 - Cloture

Objectif : rendre le sprint reprenable et fermer le type d'entreprise.

Sorties obligatoires :

- statut canonique final du type d'entreprise ;
- board mis a jour ;
- dernier etat mis a jour ;
- liste des points ouverts ;
- recommandation du sprint suivant ;
- methode reutilisable ajustee si necessaire.

La cloture doit dire explicitement :

- perimetre `DONE`, `PARTIAL` ou `BLOCKED` ;
- pack actif final ;
- documents generables ;
- documents manuels, reserves ou bloques ;
- retours associe traites ;
- ecarts reportes ;
- prochain sous-cas si le type n'est pas clos a 100 %.

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
Pilote : Gad / Naomi
Type d'entreprise :
Decision initiale : NO-GO dev

## Sources lues

## Questions NotebookLM posees

## Reponses NotebookLM utiles

## Journal NotebookLM structure

Pour chaque reponse :
- prompt utilise ;
- synthese fiable ;
- documents cites ;
- conditions ;
- variables ;
- contradictions ;
- non trouve ;
- impact sprint ;
- prompt suivant.

## Hierarchie des sources

## Triangulation trois sources

| Sujet | Reference documents a generer | NotebookLM / modele | Retour humain | Decision |
| --- | --- | --- | --- | --- |

## Matrice documentaire

| Condition | Document | Code | Statut source | Statut moteur | Statut front | Decision |
| --- | --- | --- | --- | --- | --- | --- |

## Audit de reutilisation

| Element | Source existante | Conditions identiques ? | Variables identiques ? | Decision | Action |
| --- | --- | --- | --- | --- | --- |

## Parcours metier

## Donnees a saisir

## Reutilisations explicites

## Audit deduplication front

## Documents manuels / reserves / bloques

## Tickets du sprint

| Ordre | Ticket | Statut | Objet | Criteria |
| --- | --- | --- | --- | --- |

## Scenarios de smoke

## Pack actif

| Version | Racine | Manifest | Statut | Remplace |
| --- | --- | --- | --- | --- |

## Audit fidelite source

## Audit trois sources avant validation associe

## Pack pour l'associe

## Brief associe

## Retours associe

## Corrections

## Questions interdites / deja resolues par les sources

## Statut final

## Prochaine recommandation
```

## Checklist Naomi

Naomi doit suivre cette checklist dans l'ordre :

1. dire explicitement `Je suis Naomi` ;
2. nommer le type d'entreprise du sprint ;
3. lire avec Codex le statut projet courant ;
4. recevoir de Codex le prompt NotebookLM courant ;
5. copier-coller ce prompt dans NotebookLM ;
6. coller la reponse NotebookLM brute dans Codex ;
7. laisser Codex structurer la reponse et donner le prompt suivant ;
8. repeter la boucle NotebookLM jusqu'au feu vert de Codex ;
9. faire ensuite seulement l'audit de reutilisation SELARL/global ;
10. valider la matrice documentaire avec Codex ;
11. valider les documents manuels/reserves/bloques ;
12. obtenir un `GO dev` uniquement pour un ticket borne ;
13. laisser Codex implementer et tester ;
14. preparer le pack de test pour l'associe ;
15. collecter le retour humain de l'associe ;
16. faire boucler les corrections ;
17. cloturer le sprint avec un statut canonique.

## Definition de done d'un sprint

Un sprint est termine seulement si :

- le type d'entreprise dispose d'un statut canonique ;
- tous les documents attendus sont classes ;
- les trois sources ont ete triangulees ou les manques sont documentes ;
- les reutilisations SELARL/globales sont explicites et justifiees ;
- les documents generables du perimetre ont DOCX et ZIP valides ;
- le pack actif final est identifie et les anciens packs ne sont plus transmis ;
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

1. transmettre le pack actif `artifacts/selarl_closing_pack_005/` ;
2. transmettre le brief `docs/review/selarl_final_validation_001_brief_v1.md` ;
3. demander seulement une validation finale ou des ecarts concrets ;
4. integrer ou classer les retours ;
5. lancer `SELARL-CANONICAL-CLOSE-001` si le pack est valide ;
6. sinon ouvrir un ticket borne ou un sous-cas unique avec `GO dev`.
